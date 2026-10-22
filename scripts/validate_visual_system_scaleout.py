#!/usr/bin/env python3
"""Allow scale-out after a user-approved concept preview only when real assets are ready and the production representative preserves the approved visual system.

This gate is for the path where the user approved VISUAL_SYSTEM_WITH_ASSET_SLOTS.
It never treats a reviewer as the source of approval: the reviewer only attests that production asset substitution did not materially change the user-approved visual system.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


class VisualSystemScaleoutError(ValueError):
    pass


def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise VisualSystemScaleoutError(f"file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise VisualSystemScaleoutError(f"invalid JSON {path}: {exc}") from exc


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_sha(value: dict[str, Any]) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def validate(
    decision: dict[str, Any],
    representative: dict[str, Any],
    fidelity: dict[str, Any],
    asset_readiness: dict[str, Any],
) -> dict[str, Any]:
    if decision.get("decided_by") != "USER" or decision.get("decision") != "APPROVE":
        raise VisualSystemScaleoutError("visual-system scaleout requires explicit USER APPROVE")
    if decision.get("approval_scope") != "VISUAL_SYSTEM_WITH_ASSET_SLOTS":
        raise VisualSystemScaleoutError("decision approval_scope must be VISUAL_SYSTEM_WITH_ASSET_SLOTS")

    preview_path = Path(str(decision.get("artifact_path") or ""))
    if not preview_path.is_file():
        raise VisualSystemScaleoutError(f"approved concept preview not found: {preview_path}")
    preview_sha = sha256_file(preview_path)
    if decision.get("artifact_sha256") != preview_sha:
        raise VisualSystemScaleoutError("approved concept preview SHA is stale or mismatched")

    if asset_readiness.get("status") != "ASSETS_READY":
        raise VisualSystemScaleoutError("production assets are not ASSETS_READY")

    if fidelity.get("status") != "PASS":
        raise VisualSystemScaleoutError("production representative materially drifts from approved visual system")
    if fidelity.get("reviewed_by") != "ART_DIRECTOR_REVIEWER":
        raise VisualSystemScaleoutError("fidelity report must come from ART_DIRECTOR_REVIEWER")
    if fidelity.get("visual_concept_id") != decision.get("visual_concept_id"):
        raise VisualSystemScaleoutError("fidelity report visual_concept_id mismatch")
    if fidelity.get("approved_preview_artifact_path") != preview_path.as_posix():
        raise VisualSystemScaleoutError("fidelity report points to a different approved preview")
    if fidelity.get("approved_preview_artifact_sha256") != preview_sha:
        raise VisualSystemScaleoutError("fidelity report preview SHA mismatch")

    checks = fidelity.get("checks") or {}
    required_fidelity_checks = (
        "composition", "hierarchy", "typography", "palette", "cta_treatment", "brand_anchor",
        "asset_slot_geometry", "attention_path", "lighting_intent", "copy_fidelity",
        "no_new_claims", "no_new_visual_language",
    )
    failed_fidelity = [name for name in required_fidelity_checks if checks.get(name) != "PASS"]
    if failed_fidelity:
        raise VisualSystemScaleoutError("fidelity checks not PASS: " + ", ".join(failed_fidelity))

    if representative.get("status") != "APPROVED":
        raise VisualSystemScaleoutError("production representative is not approved")
    if representative.get("approved_by") != "SYSTEM_FIDELITY_GATE":
        raise VisualSystemScaleoutError("preview-approved path requires SYSTEM_FIDELITY_GATE representative approval")
    if representative.get("approval_scope") != "APPROVED_VISUAL_SYSTEM_FIDELITY":
        raise VisualSystemScaleoutError("representative approval scope mismatch")

    production_path = Path(str(representative.get("artifact_path") or ""))
    if not production_path.is_file():
        raise VisualSystemScaleoutError(f"production representative not found: {production_path}")
    production_sha = sha256_file(production_path)
    if representative.get("artifact_sha256") != production_sha:
        raise VisualSystemScaleoutError("production representative SHA is stale or mismatched")
    if fidelity.get("production_artifact_path") != production_path.as_posix():
        raise VisualSystemScaleoutError("fidelity report points to a different production representative")
    if fidelity.get("production_artifact_sha256") != production_sha:
        raise VisualSystemScaleoutError("fidelity report production SHA mismatch")

    decision_sha = canonical_sha(decision)
    fidelity_sha = canonical_sha(fidelity)
    if representative.get("user_visual_decision_id") != decision.get("decision_id"):
        raise VisualSystemScaleoutError("representative decision ID binding mismatch")
    if representative.get("user_visual_decision_sha256") != decision_sha:
        raise VisualSystemScaleoutError("representative decision SHA binding mismatch")
    if representative.get("visual_system_fidelity_report_id") != fidelity.get("report_id"):
        raise VisualSystemScaleoutError("representative fidelity report ID binding mismatch")
    if representative.get("visual_system_fidelity_report_sha256") != fidelity_sha:
        raise VisualSystemScaleoutError("representative fidelity report SHA binding mismatch")

    quality_checks = representative.get("quality_checks") or {}
    failed_quality = [name for name, value in quality_checks.items() if value != "PASS"]
    if failed_quality:
        raise VisualSystemScaleoutError("production representative quality checks not all PASS: " + ", ".join(sorted(failed_quality)))

    return {
        "status": "VISUAL_CONCEPT_APPROVED_VIA_SYSTEM_FIDELITY",
        "visual_concept_id": decision.get("visual_concept_id"),
        "approved_preview_artifact_sha256": preview_sha,
        "production_representative_artifact_sha256": production_sha,
        "user_decision_id": decision.get("decision_id"),
        "fidelity_report_id": fidelity.get("report_id"),
        "campaign_design_system_freeze_allowed": True,
        "full_production_allowed": True,
        "user_reapproval_required": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate user-approved visual-system fidelity after real asset substitution")
    parser.add_argument("--visual-decision", type=Path, required=True)
    parser.add_argument("--representative-approval", type=Path, required=True)
    parser.add_argument("--fidelity-report", type=Path, required=True)
    parser.add_argument("--asset-readiness", type=Path, required=True)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    try:
        result = validate(
            load_json(args.visual_decision),
            load_json(args.representative_approval),
            load_json(args.fidelity_report),
            load_json(args.asset_readiness),
        )
    except VisualSystemScaleoutError as exc:
        result = {
            "status": "FULL_PRODUCTION_BLOCKED_BY_VISUAL_SYSTEM_FIDELITY",
            "campaign_design_system_freeze_allowed": False,
            "full_production_allowed": False,
            "user_reapproval_required": True,
            "error": str(exc),
        }
    payload = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(payload + "\n", encoding="utf-8")
    else:
        print(payload)
    return 0 if result.get("full_production_allowed") else 2


if __name__ == "__main__":
    raise SystemExit(main())
