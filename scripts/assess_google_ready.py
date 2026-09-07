#!/usr/bin/env python3
"""Combine design/readiness evidence with Google Ads policy preflight.

This emits a local precheck status only. It never guarantees Google approval.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def assess(readiness: dict[str, Any], policy: dict[str, Any]) -> dict[str, Any]:
    problems: list[str] = []
    if not readiness.get("completion_claim_allowed", False):
        problems.append(f"design/readiness gate not complete: {readiness.get('status')}")
    if policy.get("status") != "GOOGLE_POLICY_PREFLIGHT_PASS":
        problems.append(f"Google policy preflight not passed: {policy.get('status')}")
    if policy.get("approval_guaranteed") is not False:
        problems.append("policy report must explicitly state approval_guaranteed=false")

    status = "GOOGLE_READY_PRECHECK_PASS" if not problems else "GOOGLE_READY_PRECHECK_BLOCKED"
    return {
        "status": status,
        "google_upload_approval_guaranteed": False,
        "design_readiness_status": readiness.get("status"),
        "policy_preflight_status": policy.get("status"),
        "problems": problems,
        "statement": (
            "Local design, technical and policy prechecks passed. Final Google Ads review and account/campaign eligibility still apply."
            if not problems
            else "Do not label this creative Google-ready until the listed local blockers are resolved."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Assess final local Google-ready status")
    parser.add_argument("--readiness", type=Path, required=True)
    parser.add_argument("--policy-report", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result = assess(load_json(args.readiness), load_json(args.policy_report))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "out": args.out.as_posix()}, ensure_ascii=False))
    return 0 if result["status"] == "GOOGLE_READY_PRECHECK_PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
