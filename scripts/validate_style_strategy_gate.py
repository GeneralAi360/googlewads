#!/usr/bin/env python3
"""Validate selected style strategy against recommendation and campaign system."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


class StyleGateError(ValueError):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code


def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise StyleGateError("FAIL_INPUT", f"file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise StyleGateError("FAIL_INPUT", f"invalid JSON {path}: {exc}") from exc


def canonical_sha(value: dict[str, Any]) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _required_text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise StyleGateError("STYLE_STRATEGY_INVALID", f"{label} is required")
    return value


def validate(
    recommendation: dict[str, Any],
    art_approval: dict[str, Any],
    campaign_system: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if recommendation.get("status") != "STYLE_STRATEGY_READY":
        raise StyleGateError("STYLE_RECOMMENDATION_NOT_READY", "style recommendation is not ready")
    recommendations = recommendation.get("recommendations")
    if not isinstance(recommendations, list) or len(recommendations) != 3:
        raise StyleGateError("STYLE_RECOMMENDATION_INVALID", "style recommendation must contain exactly three lanes")
    by_id = {}
    for item in recommendations:
        strategy_id = item.get("strategy_id") if isinstance(item, dict) else None
        if not isinstance(strategy_id, str) or not strategy_id or strategy_id in by_id:
            raise StyleGateError("STYLE_RECOMMENDATION_INVALID", "strategy IDs must be non-empty and unique")
        if item.get("performance_claim") != "NO_PERFORMANCE_PREDICTION":
            raise StyleGateError("STYLE_PERFORMANCE_CLAIM_INVALID", f"{strategy_id}: style strategy cannot claim performance")
        by_id[strategy_id] = item

    if art_approval.get("status") != "APPROVED":
        raise StyleGateError("ART_DIRECTION_NOT_APPROVED", "art-direction approval is not approved")
    direction = art_approval.get("selected_direction")
    if not isinstance(direction, dict):
        raise StyleGateError("STYLE_STRATEGY_INVALID", "selected_direction is required")

    strategy_id = _required_text(direction.get("style_strategy_id"), "selected_direction.style_strategy_id")
    strategy = by_id.get(strategy_id)
    if strategy is None:
        raise StyleGateError("STYLE_STRATEGY_NOT_RECOMMENDED", f"selected style strategy is not in recommendation: {strategy_id}")

    expected_sha = canonical_sha(recommendation)
    if direction.get("style_recommendation_sha256") != expected_sha:
        raise StyleGateError("STYLE_RECOMMENDATION_STALE", "art direction is not bound to exact style recommendation")
    if direction.get("style_library_snapshot_date") != recommendation.get("library_snapshot_date"):
        raise StyleGateError("STYLE_SNAPSHOT_MISMATCH", "art direction style snapshot differs from recommendation")
    if direction.get("style_strategy_lane") != strategy.get("lane"):
        raise StyleGateError("STYLE_LANE_MISMATCH", "art direction style lane differs from selected recommendation")
    if direction.get("style_components") != strategy.get("components"):
        raise StyleGateError("STYLE_COMPONENT_MISMATCH", "art direction style components differ from selected recommendation")

    policy = recommendation.get("policy") or {}
    if policy.get("top3_are_decision_support") is not True or policy.get("art_director_approval_required") is not True:
        raise StyleGateError("STYLE_RECOMMENDATION_INVALID", "style recommendation policy must remain decision support")
    currentness_cap = policy.get("currentness_weight_cap")
    if not isinstance(currentness_cap, (int, float)) or float(currentness_cap) > 0.1:
        raise StyleGateError("STYLE_TREND_OVERWEIGHT", "currentness weight exceeds allowed gate maximum")

    campaign_binding = "NOT_APPLICABLE"
    campaign_id = None
    if campaign_system is not None:
        if campaign_system.get("status") != "APPROVED":
            raise StyleGateError("CAMPAIGN_DESIGN_SYSTEM_NOT_APPROVED", "campaign design system is not approved")
        campaign_id = _required_text(campaign_system.get("campaign_design_system_id"), "campaign_design_system_id")
        if campaign_system.get("art_direction_id") != direction.get("art_direction_id"):
            raise StyleGateError("STYLE_CAMPAIGN_MISMATCH", "campaign system art_direction_id differs from approved direction")
        if campaign_system.get("style_strategy_id") != strategy_id:
            raise StyleGateError("STYLE_CAMPAIGN_MISMATCH", "campaign system style_strategy_id differs from approved direction")
        if campaign_system.get("style_recommendation_sha256") != expected_sha:
            raise StyleGateError("STYLE_CAMPAIGN_MISMATCH", "campaign system style recommendation SHA differs from approved direction")
        campaign_binding = "PASS"

    return {
        "status": "STYLE_STRATEGY_FROZEN",
        "style_strategy_id": strategy_id,
        "style_strategy_lane": strategy["lane"],
        "recommendation_sha256": expected_sha,
        "library_snapshot_date": recommendation["library_snapshot_date"],
        "art_direction_id": _required_text(direction.get("art_direction_id"), "selected_direction.art_direction_id"),
        "campaign_system_checked": campaign_system is not None,
        "campaign_design_system_id": campaign_id,
        "checks": {
            "recommendation_integrity": "PASS",
            "selected_strategy_exists": "PASS",
            "lane_match": "PASS",
            "component_match": "PASS",
            "snapshot_match": "PASS",
            "no_performance_prediction": "PASS",
            "campaign_binding": campaign_binding,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate selected style strategy against exact recommendation")
    parser.add_argument("--recommendation", type=Path, required=True)
    parser.add_argument("--art-direction-approval", type=Path, required=True)
    parser.add_argument("--campaign-design-system", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = validate(
            load_json(args.recommendation),
            load_json(args.art_direction_approval),
            load_json(args.campaign_design_system) if args.campaign_design_system else None,
        )
    except StyleGateError as exc:
        result = {"status": exc.code, "error": str(exc)}
        print(json.dumps(result, ensure_ascii=False))
        return 2
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "out": args.out.as_posix()}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
