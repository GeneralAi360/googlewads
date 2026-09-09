#!/usr/bin/env python3
"""Validate first-round visual concept exploration and commercial-job fidelity.

Default behavior is EXPLORE_3 unless an explicit USER_LOCKED direction exists.
Every user-facing concept must be a complete BANNER_COMPOSITE and must pass two
fresh-context exact-artifact pre-show art-director reviews. Raw hero assets or
self-declared inline PASS states are insufficient.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from itertools import combinations
from pathlib import Path
from typing import Any


class VisualConceptSetError(ValueError):
    pass


DESIGN_AXES = (
    "hero_logic",
    "composition_system",
    "attention_profile",
    "typography_profile",
    "graphic_device",
    "lighting_language",
)

PRE_SHOW_CHECKS = (
    "commercial_job_fidelity",
    "banner_composite_complete",
    "primary_message_visible",
    "cta_visible_and_integrated",
    "brand_anchor_visible",
    "hero_semantic_relevance",
    "advertising_impact",
    "compositional_confidence",
    "typographic_craft",
    "visual_polish",
    "category_premium_bar",
    "non_generic_identity",
    "ad_not_presentation_slide",
    "small_format_viability",
)


def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise VisualConceptSetError(f"file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise VisualConceptSetError(f"invalid JSON {path}: {exc}") from exc


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_sha(value: dict[str, Any]) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _require_file(path_value: Any, expected_sha: Any, label: str) -> Path:
    path = Path(str(path_value or ""))
    if not path.is_file():
        raise VisualConceptSetError(f"{label} not found: {path}")
    actual = sha256_file(path)
    if expected_sha != actual:
        raise VisualConceptSetError(f"{label} SHA-256 is stale or mismatched")
    return path


def _validate_commercial_job(lock: dict[str, Any]) -> tuple[str, str]:
    if lock.get("status") != "COMMERCIAL_JOB_LOCKED":
        raise VisualConceptSetError("commercial job must be COMMERCIAL_JOB_LOCKED")
    job_id = str(lock.get("commercial_job_id") or "").strip()
    if not job_id:
        raise VisualConceptSetError("commercial_job_id is required")
    job_type = lock.get("job_type")
    if job_type not in {
        "NEW_LICENSE_PURCHASE",
        "LICENSE_RENEWAL",
        "PURCHASE_OR_RENEWAL",
        "IMPLEMENTATION_SERVICE",
        "CONSULTATION",
        "OTHER",
    }:
        raise VisualConceptSetError("commercial job_type is unsupported")
    return job_id, canonical_sha(lock)


def _preview_contract(entry: dict[str, Any], job_id: str) -> dict[str, Any]:
    contract_path = _require_file(entry.get("preview_contract_path"), entry.get("preview_contract_sha256"), "preview contract")
    preview = load_json(contract_path)
    if preview.get("status") != "VISUAL_CONCEPT_RENDERED":
        raise VisualConceptSetError("preview contract must be VISUAL_CONCEPT_RENDERED")
    if preview.get("visual_concept_id") != entry.get("visual_concept_id"):
        raise VisualConceptSetError("preview contract visual_concept_id mismatch")
    if preview.get("commercial_job_id") != job_id:
        raise VisualConceptSetError("preview contract is bound to a stale/different commercial job")
    if preview.get("artifact_role") != "BANNER_COMPOSITE":
        raise VisualConceptSetError("user-facing concept must be a BANNER_COMPOSITE, not a raw hero asset")
    if preview.get("render_stage") != "USER_FACING_CONCEPT_COMPOSITE":
        raise VisualConceptSetError("preview contract render_stage must be USER_FACING_CONCEPT_COMPOSITE")
    composition = preview.get("composition_contract") or {}
    if composition.get("raw_generated_asset_is_final_artifact") is not False:
        raise VisualConceptSetError("raw generated hero cannot be the final user-facing concept artifact")
    visible = composition.get("mandatory_visible_elements") or {}
    for key in ("primary_message", "commercial_job_cue", "cta", "brand_anchor"):
        if not str(visible.get(key) or "").strip():
            raise VisualConceptSetError(f"preview composition is missing mandatory visible element: {key}")

    artifact_path = _require_file(entry.get("artifact_path"), entry.get("artifact_sha256"), "concept artifact")
    if preview.get("artifact_path") != artifact_path.as_posix():
        raise VisualConceptSetError("concept-set artifact path differs from preview contract")
    if preview.get("artifact_sha256") != entry.get("artifact_sha256"):
        raise VisualConceptSetError("concept-set artifact SHA differs from preview contract")
    raw_paths = [Path(str(item)).resolve() for item in composition.get("raw_generated_asset_paths") or []]
    if artifact_path.resolve() in raw_paths:
        raise VisualConceptSetError("concept artifact is a raw generated asset instead of a composed banner")
    return preview


def _validate_review_report(
    report: dict[str, Any],
    *,
    concept_id: str,
    commercial_job_id: str,
    artifact_path: Path,
    artifact_sha: str,
) -> str:
    if report.get("reviewed_by") != "ART_DIRECTOR_REVIEWER":
        raise VisualConceptSetError("pre-show review must be performed by ART_DIRECTOR_REVIEWER")
    context_id = str(report.get("reviewer_context_id") or "").strip()
    if not context_id:
        raise VisualConceptSetError("pre-show reviewer_context_id is required")
    independence = report.get("independence") or {}
    if independence.get("fresh_context") is not True:
        raise VisualConceptSetError("pre-show reviewer must use a fresh context")
    if independence.get("prior_review_verdict_visible") is not False:
        raise VisualConceptSetError("pre-show reviewer must not see prior review verdicts")
    if report.get("visual_concept_id") != concept_id:
        raise VisualConceptSetError("pre-show review visual_concept_id mismatch")
    if report.get("commercial_job_id") != commercial_job_id:
        raise VisualConceptSetError("pre-show review commercial_job_id mismatch")
    if report.get("artifact_role") != "BANNER_COMPOSITE":
        raise VisualConceptSetError("pre-show review target must be BANNER_COMPOSITE")
    if report.get("artifact_path") != artifact_path.as_posix() or report.get("artifact_sha256") != artifact_sha:
        raise VisualConceptSetError("pre-show review is not bound to the exact concept artifact")

    checks = report.get("checks") or {}
    failures: list[str] = []
    for name in PRE_SHOW_CHECKS:
        check = checks.get(name)
        if not isinstance(check, dict):
            raise VisualConceptSetError(f"pre-show review missing structured check: {name}")
        if check.get("status") != "PASS":
            failures.append(name)
        if not str(check.get("evidence") or "").strip():
            raise VisualConceptSetError(f"pre-show review check {name} requires visible-artifact evidence")
    if failures:
        raise VisualConceptSetError(
            f"{concept_id}: pre-show visual review failed checks: " + ", ".join(failures)
        )
    if report.get("status") != "PRESENTATION_READY_DESIGN":
        raise VisualConceptSetError(f"{concept_id}: pre-show review verdict must be PRESENTATION_READY_DESIGN")
    return context_id


def _validate_pre_show_reviews(
    entry: dict[str, Any],
    *,
    job_id: str,
    artifact_path: Path,
    artifact_sha: str,
) -> list[str]:
    refs = entry.get("pre_show_review_reports")
    if not isinstance(refs, list) or len(refs) != 2:
        raise VisualConceptSetError("each concept requires exactly two pre_show_review_reports")
    contexts: list[str] = []
    for index, ref in enumerate(refs, 1):
        if not isinstance(ref, dict):
            raise VisualConceptSetError("pre_show_review_reports entries must be objects")
        report_path = _require_file(ref.get("path"), ref.get("sha256"), f"pre-show review report {index}")
        report = load_json(report_path)
        contexts.append(
            _validate_review_report(
                report,
                concept_id=str(entry.get("visual_concept_id")),
                commercial_job_id=job_id,
                artifact_path=artifact_path,
                artifact_sha=artifact_sha,
            )
        )
    if len(set(contexts)) != 2:
        raise VisualConceptSetError("two pre-show reviews must use distinct reviewer_context_id values")
    return contexts


def _distinct_axis_count(left: dict[str, Any], right: dict[str, Any]) -> int:
    a = left.get("design_axes") or {}
    b = right.get("design_axes") or {}
    for axis in DESIGN_AXES:
        if not str(a.get(axis) or "").strip() or not str(b.get(axis) or "").strip():
            raise VisualConceptSetError(f"design axis {axis} is required for every concept")
    return sum(str(a[axis]).strip().lower() != str(b[axis]).strip().lower() for axis in DESIGN_AXES)


def validate(commercial_job: dict[str, Any], concept_set: dict[str, Any]) -> dict[str, Any]:
    job_id, job_sha = _validate_commercial_job(commercial_job)
    if concept_set.get("status") != "VISUAL_CONCEPT_SET_RENDERED":
        raise VisualConceptSetError("concept set status must be VISUAL_CONCEPT_SET_RENDERED")
    if concept_set.get("commercial_job_id") != job_id or concept_set.get("commercial_job_sha256") != job_sha:
        raise VisualConceptSetError("concept set commercial-job binding is stale or mismatched")

    mode = concept_set.get("mode")
    source = concept_set.get("direction_lock_source")
    concepts = concept_set.get("concepts")
    if not isinstance(concepts, list):
        raise VisualConceptSetError("concepts must be a list")

    if mode == "EXPLORE_3":
        if source not in {"NONE", "INTERNAL_RECOMMENDATION"}:
            raise VisualConceptSetError("EXPLORE_3 cannot use USER_LOCKED provenance")
        if len(concepts) != 3:
            raise VisualConceptSetError("unlocked first-round exploration requires exactly three concepts")
    elif mode == "SINGLE_USER_LOCKED":
        if source != "USER_LOCKED":
            raise VisualConceptSetError("single-concept mode requires explicit USER_LOCKED provenance")
        if len(concepts) != 1:
            raise VisualConceptSetError("SINGLE_USER_LOCKED requires exactly one concept")
        if not str(concept_set.get("user_lock_evidence") or "").strip():
            raise VisualConceptSetError("SINGLE_USER_LOCKED requires user_lock_evidence")
    else:
        raise VisualConceptSetError("mode must be EXPLORE_3 or SINGLE_USER_LOCKED")

    ids = [str(item.get("visual_concept_id") or "") for item in concepts if isinstance(item, dict)]
    if len(ids) != len(concepts) or any(not item for item in ids) or len(ids) != len(set(ids)):
        raise VisualConceptSetError("visual concept IDs must be non-empty and unique")

    review_contexts: dict[str, list[str]] = {}
    for entry in concepts:
        if not isinstance(entry, dict):
            raise VisualConceptSetError("every concept entry must be an object")
        _preview_contract(entry, job_id)
        artifact_path = Path(str(entry.get("artifact_path") or ""))
        artifact_sha = str(entry.get("artifact_sha256") or "")
        review_contexts[str(entry["visual_concept_id"])] = _validate_pre_show_reviews(
            entry,
            job_id=job_id,
            artifact_path=artifact_path,
            artifact_sha=artifact_sha,
        )

    pairwise = []
    if mode == "EXPLORE_3":
        for left, right in combinations(concepts, 2):
            diff = _distinct_axis_count(left, right)
            pairwise.append({
                "left": left["visual_concept_id"],
                "right": right["visual_concept_id"],
                "distinct_axes": diff,
            })
            if diff < 3:
                raise VisualConceptSetError(
                    f"{left['visual_concept_id']} vs {right['visual_concept_id']} differ on only {diff} design axes; >=3 required"
                )

    sheet = _require_file(
        concept_set.get("comparison_contact_sheet_path"),
        concept_set.get("comparison_contact_sheet_sha256"),
        "comparison contact sheet",
    )

    return {
        "status": "VISUAL_CONCEPT_SET_AWAITING_USER_SELECTION",
        "concept_set_id": concept_set.get("concept_set_id"),
        "commercial_job_id": job_id,
        "commercial_job_sha256": job_sha,
        "mode": mode,
        "direction_lock_source": source,
        "visual_exploration_count": len(concepts),
        "visual_concept_ids": ids,
        "pairwise_distinction": pairwise,
        "comparison_contact_sheet_path": sheet.as_posix(),
        "pre_show_review_contexts": review_contexts,
        "all_pre_show_quality_reviews_pass": True,
        "presentation_ready_design": True,
        "full_production_allowed": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate commercial-job-bound visual concept exploration")
    parser.add_argument("--commercial-job", type=Path, required=True)
    parser.add_argument("--concept-set", type=Path, required=True)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    try:
        result = validate(load_json(args.commercial_job), load_json(args.concept_set))
    except VisualConceptSetError as exc:
        result = {"status": "VISUAL_CONCEPT_SET_BLOCKED", "presentation_ready_design": False, "full_production_allowed": False, "error": str(exc)}
    payload = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(payload + "\n", encoding="utf-8")
    else:
        print(payload)
    return 0 if result.get("status") == "VISUAL_CONCEPT_SET_AWAITING_USER_SELECTION" else 2


if __name__ == "__main__":
    raise SystemExit(main())
