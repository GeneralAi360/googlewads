#!/usr/bin/env python3
"""Validate the exact commercial job advertised by a banner campaign.

This gate exists because product identity, campaign objective, CTA wording, and the
commercial transaction/service job are different facts. A material job change
invalidates downstream creative strategy instead of being patched with copy drift.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


class CommercialJobError(ValueError):
    pass


JOB_TYPES = {
    "NEW_LICENSE_PURCHASE",
    "LICENSE_RENEWAL",
    "PURCHASE_OR_RENEWAL",
    "IMPLEMENTATION_SERVICE",
    "CONSULTATION",
    "OTHER",
}


def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise CommercialJobError(f"file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise CommercialJobError(f"invalid JSON {path}: {exc}") from exc


def canonical_sha(value: dict[str, Any]) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise CommercialJobError(f"{name} is required")
    return value.strip()


def validate_lock(lock: dict[str, Any]) -> dict[str, Any]:
    if lock.get("status") != "COMMERCIAL_JOB_LOCKED":
        raise CommercialJobError("status must be COMMERCIAL_JOB_LOCKED")

    job_id = _text(lock.get("commercial_job_id"), "commercial_job_id")
    product = _text(lock.get("product_or_service"), "product_or_service")
    job_type = lock.get("job_type")
    if job_type not in JOB_TYPES:
        raise CommercialJobError("unsupported job_type")

    structure = lock.get("purchase_renewal_structure")
    if job_type == "PURCHASE_OR_RENEWAL":
        if structure not in {"COMBINED", "SEPARATE_VARIANTS"}:
            raise CommercialJobError("PURCHASE_OR_RENEWAL requires COMBINED or SEPARATE_VARIANTS")
    elif structure != "NOT_APPLICABLE":
        raise CommercialJobError(f"{job_type} requires purchase_renewal_structure=NOT_APPLICABLE")

    target = _text(lock.get("target_transaction"), "target_transaction")
    scope = lock.get("allowed_message_scope")
    if not isinstance(scope, list) or not scope or any(not isinstance(x, str) or not x.strip() for x in scope):
        raise CommercialJobError("allowed_message_scope must be a non-empty list of strings")
    if len(scope) != len(set(scope)):
        raise CommercialJobError("allowed_message_scope must be unique")

    excluded = lock.get("excluded_job_types")
    if not isinstance(excluded, list) or any(x not in JOB_TYPES for x in excluded):
        raise CommercialJobError("excluded_job_types contains an unsupported value")
    if len(excluded) != len(set(excluded)):
        raise CommercialJobError("excluded_job_types must be unique")
    if job_type in excluded:
        raise CommercialJobError("current job_type cannot also be excluded")

    source = lock.get("source_basis")
    if source not in {"USER_EXPLICIT", "VERIFIED_CAMPAIGN_BRIEF", "VERIFIED_LANDING_PAGE", "OTHER"}:
        raise CommercialJobError("unsupported source_basis")
    if source == "OTHER":
        _text(lock.get("source_note"), "source_note")
    if lock.get("change_requires_controller_reapproval") is not True:
        raise CommercialJobError("commercial job changes must require controller reapproval")

    return {
        "status": "COMMERCIAL_JOB_LOCK_PASS",
        "commercial_job_id": job_id,
        "commercial_job_sha256": canonical_sha(lock),
        "product_or_service": product,
        "job_type": job_type,
        "purchase_renewal_structure": structure,
        "target_transaction": target,
        "invalidate_downstream": False,
    }


def compare(previous: dict[str, Any], current: dict[str, Any]) -> dict[str, Any]:
    previous_result = validate_lock(previous)
    current_result = validate_lock(current)
    material_keys = (
        "product_or_service",
        "job_type",
        "purchase_renewal_structure",
        "target_transaction",
        "allowed_message_scope",
        "excluded_job_types",
    )
    changed = [key for key in material_keys if previous.get(key) != current.get(key)]
    if not changed and previous_result["commercial_job_sha256"] == current_result["commercial_job_sha256"]:
        return current_result
    if not changed:
        return current_result
    return {
        **current_result,
        "status": "COMMERCIAL_JOB_CHANGED",
        "changed_fields": changed,
        "previous_commercial_job_id": previous_result["commercial_job_id"],
        "previous_commercial_job_sha256": previous_result["commercial_job_sha256"],
        "invalidate_downstream": True,
        "invalidate_artifacts": [
            "idea_architecture",
            "style_strategy",
            "attention_profile",
            "typography_profile",
            "lighting_intent_if_meaning_changed",
            "art_direction",
            "visual_concept_previews",
            "visual_user_decisions",
            "campaign_design_system",
            "creative_contracts",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate or compare a campaign commercial-job lock")
    parser.add_argument("--lock", type=Path, required=True)
    parser.add_argument("--previous-lock", type=Path)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    try:
        current = load_json(args.lock)
        result = compare(load_json(args.previous_lock), current) if args.previous_lock else validate_lock(current)
    except CommercialJobError as exc:
        result = {"status": "COMMERCIAL_JOB_INVALID", "invalidate_downstream": True, "error": str(exc)}
    payload = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(payload + "\n", encoding="utf-8")
    else:
        print(payload)
    return 0 if result.get("status") in {"COMMERCIAL_JOB_LOCK_PASS", "COMMERCIAL_JOB_CHANGED"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
