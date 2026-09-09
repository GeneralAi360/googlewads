#!/usr/bin/env python3
"""Validate a user decision on a rendered visual concept.

Two approval scopes are supported:
- EXACT_PRODUCTION_ARTIFACT: user approved the actual production-ready representative bytes;
- VISUAL_SYSTEM_WITH_ASSET_SLOTS: user approved the rendered composition/style system while one or more production assets are still surrogate/placeholder. This never unlocks full production by itself.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


class VisualConceptDecisionError(ValueError):
    pass


def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise VisualConceptDecisionError(f"file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise VisualConceptDecisionError(f"invalid JSON {path}: {exc}") from exc


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate(decision: dict[str, Any]) -> dict[str, Any]:
    if decision.get("decided_by") != "USER":
        raise VisualConceptDecisionError("visual concept decision must be made by USER")

    visual_concept_id = str(decision.get("visual_concept_id") or "").strip()
    if not visual_concept_id:
        raise VisualConceptDecisionError("visual_concept_id is required")

    artifact_path = Path(str(decision.get("artifact_path") or ""))
    if not artifact_path.is_file():
        raise VisualConceptDecisionError(f"visual concept artifact not found: {artifact_path}")
    actual_sha = sha256_file(artifact_path)
    if decision.get("artifact_sha256") != actual_sha:
        raise VisualConceptDecisionError("visual concept artifact SHA-256 is stale or mismatched")

    user_decision = decision.get("decision")
    if user_decision not in {"APPROVE", "REVISE", "REJECT"}:
        raise VisualConceptDecisionError("decision must be APPROVE, REVISE, or REJECT")

    scope = decision.get("approval_scope") or "EXACT_PRODUCTION_ARTIFACT"
    if scope not in {"EXACT_PRODUCTION_ARTIFACT", "VISUAL_SYSTEM_WITH_ASSET_SLOTS"}:
        raise VisualConceptDecisionError("unsupported approval_scope")

    feedback = str(decision.get("feedback") or "").strip()
    if user_decision in {"REVISE", "REJECT"} and not feedback:
        raise VisualConceptDecisionError(f"{user_decision} requires user feedback")

    if user_decision == "APPROVE":
        if scope == "EXACT_PRODUCTION_ARTIFACT":
            status = "VISUAL_CONCEPT_APPROVED"
            expected_next = "FREEZE_CAMPAIGN_DESIGN_SYSTEM"
            full_production_allowed = True
            production_asset_completion_allowed = True
        else:
            status = "VISUAL_CONCEPT_APPROVED_ASSET_PENDING"
            expected_next = "COLLECT_PRODUCTION_ASSETS_AND_MATERIALIZE"
            full_production_allowed = False
            production_asset_completion_allowed = True
    elif user_decision == "REVISE":
        status = "VISUAL_CONCEPT_REVISE_REQUESTED"
        expected_next = "RENDER_REVISED_VISUAL_CONCEPT"
        full_production_allowed = False
        production_asset_completion_allowed = False
    else:
        status = "VISUAL_CONCEPT_REJECTED"
        expected_next = "RETURN_UPSTREAM"
        full_production_allowed = False
        production_asset_completion_allowed = False

    if decision.get("next_action") not in {None, expected_next}:
        raise VisualConceptDecisionError(f"next_action must be {expected_next} for {user_decision}/{scope}")

    return {
        "status": status,
        "visual_concept_id": visual_concept_id,
        "artifact_path": artifact_path.as_posix(),
        "artifact_sha256": actual_sha,
        "approval_scope": scope,
        "decision": user_decision,
        "next_action": expected_next,
        "full_production_allowed": full_production_allowed,
        "production_asset_completion_allowed": production_asset_completion_allowed,
        "user_feedback": feedback or None,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate explicit user decision on a rendered visual concept")
    parser.add_argument("--decision", type=Path, required=True)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    try:
        result = validate(load_json(args.decision))
    except VisualConceptDecisionError as exc:
        result = {
            "status": "VISUAL_CONCEPT_DECISION_INVALID",
            "full_production_allowed": False,
            "production_asset_completion_allowed": False,
            "error": str(exc),
        }
    payload = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(payload + "\n", encoding="utf-8")
    else:
        print(payload)
    valid_statuses = {
        "VISUAL_CONCEPT_APPROVED",
        "VISUAL_CONCEPT_APPROVED_ASSET_PENDING",
        "VISUAL_CONCEPT_REVISE_REQUESTED",
        "VISUAL_CONCEPT_REJECTED",
    }
    return 0 if result.get("status") in valid_statuses else 2


if __name__ == "__main__":
    raise SystemExit(main())
