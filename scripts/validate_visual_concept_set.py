#!/usr/bin/env python3
"""Validate first-round visual concept exploration and commercial-job fidelity.

Default behavior is EXPLORE_3 unless an explicit USER_LOCKED direction exists.
The validator checks exact preview/artifact hashes, commercial-job binding,
pre-show art-director quality checks, contact-sheet integrity, and pairwise
material distinction across six design axes.
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

QUALITY_CHECKS = (
    "commercial_job_fidelity",
    "professional_category_fit",
    "ad_not_presentation_slide",
    "hierarchy",
    "typography",
    "cta_integration",
    "visual_distinctiveness",
    "anti_template",
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
    artifact_path = _require_file(entry.get("artifact_path"), entry.get("artifact_sha256"), "concept artifact")
    if preview.get("artifact_path") != artifact_path.as_posix():
        raise VisualConceptSetError("concept-set artifact path differs from preview contract")
    if preview.get("artifact_sha256") != entry.get("artifact_sha256"):
        raise VisualConceptSetError("concept-set artifact SHA differs from preview contract")
    return preview


def _validate_quality(entry: dict[str, Any]) -> None:
    review = entry.get("quality_review") or {}
    if review.get("reviewed_by") != "ART_DIRECTOR_REVIEWER":
        raise VisualConceptSetError("each concept requires ART_DIRECTOR_REVIEWER quality review")
    if review.get("status") != "PASS":
        raise VisualConceptSetError(f"{entry.get('visual_concept_id')}: pre-show quality review did not PASS")
    checks = review.get("checks") or {}
    failed = [name for name in QUALITY_CHECKS if checks.get(name) != "PASS"]
    if failed:
        raise VisualConceptSetError(
            f"{entry.get('visual_concept_id')}: pre-show quality checks failed: " + ", ".join(failed)
        )


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

    previews = []
    for entry in concepts:
        if not isinstance(entry, dict):
            raise VisualConceptSetError("every concept entry must be an object")
        previews.append(_preview_contract(entry, job_id))
        _validate_quality(entry)

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
        "all_pre_show_quality_reviews_pass": True,
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
        result = {"status": "VISUAL_CONCEPT_SET_BLOCKED", "full_production_allowed": False, "error": str(exc)}
    payload = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(payload + "\n", encoding="utf-8")
    else:
        print(payload)
    return 0 if result.get("status") == "VISUAL_CONCEPT_SET_AWAITING_USER_SELECTION" else 2


if __name__ == "__main__":
    raise SystemExit(main())
