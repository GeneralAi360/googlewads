#!/usr/bin/env python3
"""Recommend three visual-strategy lanes before art direction.

This is deterministic decision support. It ranks craft/semantic fit from a curated
style library and never predicts CTR, CVR, CPA, ROAS, or conversion lift.
"""
from __future__ import annotations

import argparse
import json
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any


class StyleRecommendationError(ValueError):
    pass


def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise StyleRecommendationError(f"file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise StyleRecommendationError(f"invalid JSON {path}: {exc}") from exc


def _norm(value: Any) -> str:
    return str(value or "").strip().upper().replace(" ", "_").replace("-", "_")


def _set(values: Any) -> set[str]:
    if not isinstance(values, list):
        return set()
    return {_norm(item) for item in values if str(item or "").strip()}


def _require_context(context: dict[str, Any]) -> None:
    required = (
        "context_id", "category_tags", "presentation_mode", "primary_emotion",
        "target_order_to_virality", "target_aesthetics_to_innovation", "disruption_level",
        "hero_type", "asset_truth_mode", "layout_families", "language_scripts",
        "brand_traits", "avoid_tags", "currentness_preference", "typography_goal",
    )
    missing = [key for key in required if key not in context]
    if missing:
        raise StyleRecommendationError("missing context fields: " + ", ".join(missing))
    if not isinstance(context["category_tags"], list) or not context["category_tags"]:
        raise StyleRecommendationError("category_tags must be a non-empty list")
    if not isinstance(context["layout_families"], list) or not context["layout_families"]:
        raise StyleRecommendationError("layout_families must be a non-empty list")
    for key in ("target_order_to_virality", "target_aesthetics_to_innovation"):
        value = context[key]
        if not isinstance(value, (int, float)) or not 0 <= float(value) <= 1:
            raise StyleRecommendationError(f"{key} must be 0..1")
    if context["disruption_level"] not in {"LOW", "MEDIUM", "HIGH"}:
        raise StyleRecommendationError("disruption_level must be LOW/MEDIUM/HIGH")


def _ratio_match(wanted: set[str], available: set[str], neutral: float = 0.35) -> float:
    if not wanted or not available:
        return neutral
    hits = len(wanted & available)
    if hits == 0:
        return 0.0
    return min(1.0, hits / max(1, min(len(wanted), 3)))


def _axis_score(actual: float, target: float) -> float:
    return max(0.0, 1.0 - abs(float(actual) - float(target)))


def _currentness_status(library: dict[str, Any]) -> tuple[str, bool]:
    raw = library.get("snapshot_date")
    try:
        snap = date.fromisoformat(str(raw))
    except ValueError as exc:
        raise StyleRecommendationError("library snapshot_date must be YYYY-MM-DD") from exc
    age = (datetime.now(timezone.utc).date() - snap).days
    return ("CURRENT", True) if age <= 90 else ("STALE_CURRENTNESS_DISABLED", False)


def _best_overlay(context: dict[str, Any], library: dict[str, Any], current_enabled: bool) -> tuple[dict[str, Any] | None, float]:
    preference = context["currentness_preference"]
    if preference == "EVERGREEN" or not current_enabled:
        return None, 0.0
    signals = (
        _set(context.get("category_tags"))
        | _set(context.get("brand_traits"))
        | {_norm(context.get("primary_emotion")), _norm(context.get("hero_type")), _norm(context.get("presentation_mode"))}
    )
    avoids = _set(context.get("avoid_tags")) | _set(context.get("category_cliches"))
    best = None
    best_score = 0.0
    for overlay in library.get("current_overlays") or []:
        affinity = _set(overlay.get("affinity_tags"))
        prohibited = _set(overlay.get("avoid_tags"))
        affinity_score = _ratio_match(signals, affinity, neutral=0.15)
        penalty = 0.35 if (prohibited & avoids) else 0.0
        currentness = float(overlay.get("currentness", 0.0))
        strength = {"BALANCED": 0.25, "CURRENT": 0.45, "EXPERIMENTAL_BALANCED": 0.35}.get(preference, 0.2)
        score = (1 - strength) * affinity_score + strength * currentness - penalty
        if score > best_score:
            best_score, best = score, overlay
    if best_score < 0.18:
        return None, 0.0
    return best, max(0.0, min(1.0, best_score))


def _best_execution(context: dict[str, Any], library: dict[str, Any], foundation: dict[str, Any]) -> tuple[dict[str, Any], float]:
    mode = _norm(context["presentation_mode"])
    hero = _norm(context["hero_type"])
    best = None
    best_score = -1.0
    for execution in library.get("execution_languages") or []:
        modes = _set(execution.get("presentation_modes"))
        heroes = _set(execution.get("hero_types"))
        mode_score = 1.0 if mode in modes else 0.15
        hero_score = 1.0 if hero in heroes else 0.35
        score = 0.65 * mode_score + 0.35 * hero_score
        if score > best_score:
            best, best_score = execution, score
    if best is None:
        raise StyleRecommendationError("style library has no execution languages")
    return best, max(0.0, min(1.0, best_score))


def _best_typography(context: dict[str, Any], library: dict[str, Any], foundation: dict[str, Any]) -> tuple[dict[str, Any], float]:
    candidates = set(foundation.get("typography_profile_candidates") or [])
    profiles = library.get("typography_profiles") or []
    goal = _norm(context.get("typography_goal"))
    goal_map = {
        "ENTERPRISE": {"B2B", "ENTERPRISE", "PRODUCT_UI", "MICRO_FORMAT"},
        "EDITORIAL": {"EDITORIAL", "CULTURE"},
        "PREMIUM": {"PREMIUM", "LUXURY", "BEAUTY", "REAL_ESTATE"},
        "PROMO": {"PROMOTION_LED", "RETAIL", "EVENTS", "SPORT"},
        "HUMAN": {"HUMAN_CONTEXT", "HEALTHCARE", "EDUCATION", "SERVICES"},
        "TECHNICAL": {"TECH", "DEVTOOLS", "DATA", "WORKFLOW"},
        "EXPRESSIVE": {"FASHION", "ENTERTAINMENT", "YOUTH", "EDITORIAL_STATEMENT"},
        "LOCAL": {"LOCAL", "CULTURAL", "MULTILINGUAL"},
    }
    wanted = goal_map.get(goal, set())
    best = None
    best_score = -1.0
    for profile in profiles:
        base = 0.72 if profile.get("id") in candidates else 0.35
        fit = _ratio_match(wanted, _set(profile.get("best_for")), neutral=0.65 if goal == "AUTO" else 0.25)
        score = 0.55 * base + 0.45 * fit
        if "CYRILLIC" in _set(context.get("language_scripts")) and not profile.get("candidate_status"):
            score -= 0.15
        if score > best_score:
            best, best_score = profile, score
    if best is None:
        raise StyleRecommendationError("style library has no typography profiles")
    return best, max(0.0, min(1.0, best_score))


def _format_resilience(context: dict[str, Any], foundation: dict[str, Any]) -> float:
    values = foundation.get("format_resilience") or {}
    scores = [float(values.get(family, 0.6)) for family in context["layout_families"]]
    return sum(scores) / len(scores)


def _asset_truth_fit(context: dict[str, Any], execution: dict[str, Any]) -> float:
    truth = _norm(execution.get("truth_requirement"))
    mode = context["asset_truth_mode"]
    hero = _norm(context["hero_type"])
    if "REAL_UI" in truth and hero == "PRODUCT_UI":
        return 1.0 if mode == "REAL_ASSET" else 0.15
    if "EXACT_DETERMINISTIC_TYPE" in truth:
        return 1.0 if mode in {"TYPE_ONLY", "REAL_ASSET", "HYBRID"} else 0.75
    if "VERIFIED_SOURCE" in truth:
        return 0.95 if mode == "REAL_ASSET" else 0.4
    return 0.85 if mode in {"REAL_ASSET", "TYPE_ONLY"} else 0.72


def _attention_fit(context: dict[str, Any], library: dict[str, Any], execution: dict[str, Any], foundation: dict[str, Any]) -> tuple[dict[str, Any], float]:
    desired_id = execution.get("attention_profile")
    profiles = {item["id"]: item for item in library.get("attention_profiles") or []}
    attention = profiles.get(desired_id)
    if attention is None:
        candidate_ids = foundation.get("attention_profile_candidates") or []
        attention = profiles.get(candidate_ids[0]) if candidate_ids else None
    if attention is None:
        raise StyleRecommendationError("cannot resolve attention profile")
    mode = _norm(context["presentation_mode"])
    score = 1.0 if mode in _set(attention.get("compatible_modes")) else 0.55
    return attention, score


def _foundation_candidate(context: dict[str, Any], library: dict[str, Any], foundation: dict[str, Any], current_enabled: bool) -> dict[str, Any]:
    categories = _set(context.get("category_tags"))
    emotions = {_norm(context.get("primary_emotion"))} | _set(context.get("secondary_emotions"))
    mode = _norm(context.get("presentation_mode"))
    hero = _norm(context.get("hero_type"))

    presentation_fit = 1.0 if mode in _set(foundation.get("presentation_affinity")) else 0.2
    category_fit = _ratio_match(categories, _set(foundation.get("category_affinity")), neutral=0.25)
    emotion_fit = _ratio_match(emotions, _set(foundation.get("emotion_affinity")), neutral=0.3)
    hero_fit = 1.0 if hero in _set(foundation.get("hero_affinity")) else 0.45

    execution, execution_fit = _best_execution(context, library, foundation)
    attention, attention_fit = _attention_fit(context, library, execution, foundation)
    typography, typography_fit = _best_typography(context, library, foundation)
    overlay, overlay_fit = _best_overlay(context, library, current_enabled)

    axis_fit = 0.5 * _axis_score(foundation.get("order_to_virality", 0.5), context["target_order_to_virality"]) + 0.5 * _axis_score(foundation.get("aesthetics_to_innovation", 0.5), context["target_aesthetics_to_innovation"])
    category_fit = 0.8 * category_fit + 0.2 * axis_fit
    attention_fit = 0.75 * attention_fit + 0.25 * execution_fit
    asset_truth_fit = _asset_truth_fit(context, execution)
    format_fit = _format_resilience(context, foundation)
    lighting_fit = 1.0 if (hero == "PRODUCT_UI" and "TRUTHFUL_UI" in _set(foundation.get("lighting_character"))) else 0.78
    if context["disruption_level"] == "LOW" and float(foundation.get("order_to_virality", 0.5)) > 0.65:
        category_fit *= 0.68
    elif context["disruption_level"] == "HIGH" and float(foundation.get("order_to_virality", 0.5)) < 0.25:
        category_fit *= 0.86

    currentness = float(overlay.get("currentness", 0.0)) if overlay and current_enabled else 0.0
    weights = library.get("ranking_weights") or {}
    scores = {
        "presentation_fit": presentation_fit,
        "category_fit": category_fit,
        "emotion_fit": emotion_fit,
        "attention_fit": attention_fit,
        "typography_fit": typography_fit,
        "asset_truth_fit": asset_truth_fit,
        "format_resilience": format_fit,
        "lighting_fit": lighting_fit,
        "currentness": currentness,
    }
    total = sum(float(weights.get(key, 0.0)) * value for key, value in scores.items())
    avoids = _set(context.get("avoid_tags")) | _set(context.get("category_cliches")) | _set(context.get("avoid_emotions"))
    risk_tags = list(foundation.get("risk_tags") or [])
    if overlay:
        risk_tags.extend(item for item in overlay.get("avoid_tags") or [] if _norm(item) in avoids)
    if hero_fit < 0.5:
        risk_tags.append("HERO_STYLE_MISMATCH")
        total -= 0.06
    if overlay and currentness >= 0.9:
        nontrend = sum(value for key, value in scores.items() if key != "currentness") / 8
        if nontrend < 0.64:
            risk_tags.append("TREND_OVERFIT_RISK")
    total = max(0.0, min(1.0, total))

    return {
        "foundation": foundation,
        "overlay": overlay,
        "execution": execution,
        "attention": attention,
        "typography": typography,
        "scores": {key: round(value, 4) for key, value in scores.items()},
        "score_total": round(total, 4),
        "risk_flags": list(dict.fromkeys(risk_tags)),
        "overlay_fit": overlay_fit,
    }


def _strategy(candidate: dict[str, Any], lane: str, index: int) -> dict[str, Any]:
    foundation = candidate["foundation"]
    overlay = candidate["overlay"]
    execution = candidate["execution"]
    attention = candidate["attention"]
    typography = candidate["typography"]
    rationale = [
        f"Foundation {foundation['label']} fits the communication structure and category constraints.",
        f"Execution {execution['label']} supports the selected presentation mode and hero type.",
        f"Attention plan is {attention['id']} and typography profile is {typography['id']}.",
    ]
    if overlay:
        rationale.append(f"2026 overlay {overlay['label']} is applied as a subordinate currentness layer, not as the core idea.")
    return {
        "strategy_id": f"STYLE-{lane}-{index:02d}-{foundation['id'].replace('FOUNDATION_', '')}",
        "lane": lane,
        "score_total": candidate["score_total"],
        "components": {
            "foundation_id": foundation["id"],
            "overlay_id": overlay["id"] if overlay else None,
            "execution_id": execution["id"],
            "attention_id": attention["id"],
            "typography_id": typography["id"],
        },
        "scores": candidate["scores"],
        "attention_plan": {
            "scan_path": attention.get("scan_path") or [],
            "salience_budget": attention.get("salience_budget"),
        },
        "typography_plan": {
            "profile_id": typography["id"],
            "character": typography.get("character"),
            "max_families": typography.get("max_families"),
            "max_weights": typography.get("max_weights"),
            "variable_font_preferred": typography.get("variable_font_preferred"),
            "candidate_examples": typography.get("candidate_examples") or [],
            "candidate_status": typography.get("candidate_status"),
        },
        "lighting_affinity": foundation.get("lighting_character") or [],
        "rationale": rationale,
        "risk_flags": candidate["risk_flags"],
        "performance_claim": "NO_PERFORMANCE_PREDICTION",
    }


def recommend(context: dict[str, Any], library: dict[str, Any]) -> dict[str, Any]:
    _require_context(context)
    status, current_enabled = _currentness_status(library)
    candidates = [
        _foundation_candidate(context, library, foundation, current_enabled)
        for foundation in library.get("foundation_profiles") or []
    ]
    if len(candidates) < 3:
        raise StyleRecommendationError("style library requires at least three foundation profiles")
    candidates.sort(key=lambda item: item["score_total"], reverse=True)
    policy = library.get("policy") or {}
    minimum = float(policy.get("minimum_candidate_score", 0.55))
    wildcard_minimum = float(policy.get("wildcard_minimum_score", 0.5))

    safe = candidates[0]
    remaining = [item for item in candidates[1:] if item["score_total"] >= minimum]
    if not remaining:
        remaining = candidates[1:]

    current = max(
        remaining,
        key=lambda item: item["score_total"] + 0.08 * item["scores"]["currentness"],
    )
    remaining2 = [item for item in candidates if item is not safe and item is not current]
    threshold = wildcard_minimum if context["disruption_level"] in {"MEDIUM", "HIGH"} else minimum
    eligible = [item for item in remaining2 if item["score_total"] >= threshold] or remaining2
    if not eligible:
        raise StyleRecommendationError("not enough distinct candidates for top-3 lanes")

    safe_axis = float(safe["foundation"].get("order_to_virality", 0.5))
    current_axis = float(current["foundation"].get("order_to_virality", 0.5))
    wildcard = max(
        eligible,
        key=lambda item: item["score_total"] + 0.08 * (abs(float(item["foundation"].get("order_to_virality", 0.5)) - safe_axis) + abs(float(item["foundation"].get("order_to_virality", 0.5)) - current_axis)),
    )

    recommendations = [
        _strategy(safe, "SAFE_STRONG", 1),
        _strategy(current, "CURRENT_DIFFERENTIATED", 2),
        _strategy(wildcard, "CONTROLLED_WILDCARD", 3),
    ]
    return {
        "status": "STYLE_STRATEGY_READY",
        "context_id": context["context_id"],
        "library_snapshot_date": library["snapshot_date"],
        "currentness_status": status,
        "recommendations": recommendations,
        "policy": {
            "currentness_weight_cap": float((library.get("policy") or {}).get("trend_weight_cap", 0.05)),
            "top3_are_decision_support": True,
            "art_director_approval_required": True,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Recommend three visual-strategy lanes before art direction")
    parser.add_argument("--context", type=Path, required=True)
    parser.add_argument("--library", type=Path, default=Path("config/style-intelligence-library.json"))
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = recommend(load_json(args.context), load_json(args.library))
    except StyleRecommendationError as exc:
        print(json.dumps({"status": "STYLE_STRATEGY_FAIL", "error": str(exc)}, ensure_ascii=False))
        return 2
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "out": args.out.as_posix()}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
