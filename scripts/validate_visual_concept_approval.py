#!/usr/bin/env python3
"""Fail-closed gate: only exact-artifact USER APPROVE unlocks campaign scale-out."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


class VisualApprovalError(ValueError):
    pass


def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise VisualApprovalError(f"file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise VisualApprovalError(f"invalid JSON {path}: {exc}") from exc


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate(representative: dict[str, Any], decision: dict[str, Any]) -> dict[str, Any]:
    if representative.get("status") != "APPROVED":
        raise VisualApprovalError("representative visual concept is not approved")
    if representative.get("approved_by") != "USER":
        raise VisualApprovalError("representative approval must be made by USER")
    if decision.get("decided_by") != "USER" or decision.get("decision") != "APPROVE":
        raise VisualApprovalError("full production requires an explicit USER APPROVE decision")

    rep_path = Path(str(representative.get("artifact_path") or ""))
    decision_path = Path(str(decision.get("artifact_path") or ""))
    if not rep_path.is_file():
        raise VisualApprovalError(f"representative artifact not found: {rep_path}")
    if rep_path.as_posix() != decision_path.as_posix():
        raise VisualApprovalError("user decision points to a different visual artifact")

    actual_sha = sha256_file(rep_path)
    if representative.get("artifact_sha256") != actual_sha:
        raise VisualApprovalError("representative approval artifact SHA is stale or mismatched")
    if decision.get("artifact_sha256") != actual_sha:
        raise VisualApprovalError("user decision artifact SHA is stale or mismatched")

    quality_checks = representative.get("quality_checks") or {}
    failed_checks = [name for name, value in quality_checks.items() if value != "PASS"]
    if failed_checks:
        raise VisualApprovalError("representative quality checks are not all PASS: " + ", ".join(sorted(failed_checks)))

    return {
        "status": "VISUAL_CONCEPT_APPROVED",
        "visual_concept_id": decision.get("visual_concept_id"),
        "artifact_path": rep_path.as_posix(),
        "artifact_sha256": actual_sha,
        "representative_approval_id": representative.get("approval_id"),
        "user_decision_id": decision.get("decision_id"),
        "campaign_design_system_freeze_allowed": True,
        "full_production_allowed": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Require exact-artifact USER visual approval before campaign scale-out")
    parser.add_argument("--representative-approval", type=Path, required=True)
    parser.add_argument("--visual-decision", type=Path, required=True)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    try:
        result = validate(load_json(args.representative_approval), load_json(args.visual_decision))
    except VisualApprovalError as exc:
        result = {
            "status": "FULL_PRODUCTION_BLOCKED_BY_VISUAL_APPROVAL",
            "campaign_design_system_freeze_allowed": False,
            "full_production_allowed": False,
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
