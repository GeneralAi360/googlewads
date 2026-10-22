#!/usr/bin/env python3
"""Aggregate exact-artifact Google policy reports for a banner pack."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


VALID = {
    "GOOGLE_POLICY_PREFLIGHT_PASS",
    "GOOGLE_POLICY_PREFLIGHT_BLOCKED",
    "GOOGLE_POLICY_PREFLIGHT_INCOMPLETE",
    "POLICY_REVIEW_REQUIRED",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def aggregate(manifest: dict[str, Any], report_dir: Path) -> dict[str, Any]:
    files = manifest.get("files") or []
    if not files:
        return {
            "status": "GOOGLE_POLICY_PREFLIGHT_INCOMPLETE",
            "approval_guaranteed": False,
            "expected_reports": 0,
            "passed_reports": 0,
            "missing_reports": [],
            "failed_reports": [{"job_id": None, "reason": "manifest contains no files"}],
            "reports": [],
            "final_statement": "Policy pack aggregation cannot pass without final creative files."
        }

    results = []
    missing = []
    failed = []
    statuses = []
    for item in files:
        job_id = item.get("job_id")
        path = report_dir / f"{job_id}.google-policy-report.json"
        if not path.is_file():
            missing.append(job_id)
            continue
        report = load_json(path)
        status = report.get("status")
        statuses.append(status)
        if status not in VALID:
            failed.append({"job_id": job_id, "reason": f"invalid policy status: {status!r}"})
            continue
        if report.get("creative_sha256") != item.get("sha256"):
            failed.append({"job_id": job_id, "reason": "policy report is stale or bound to different creative bytes"})
            continue
        if report.get("approval_guaranteed") is not False:
            failed.append({"job_id": job_id, "reason": "policy report must state approval_guaranteed=false"})
            continue
        results.append({"job_id": job_id, "status": status, "path": path.as_posix()})

    if missing or failed:
        status = "GOOGLE_POLICY_PREFLIGHT_INCOMPLETE"
    elif any(value == "GOOGLE_POLICY_PREFLIGHT_BLOCKED" for value in statuses):
        status = "GOOGLE_POLICY_PREFLIGHT_BLOCKED"
    elif any(value == "POLICY_REVIEW_REQUIRED" for value in statuses):
        status = "POLICY_REVIEW_REQUIRED"
    elif any(value == "GOOGLE_POLICY_PREFLIGHT_INCOMPLETE" for value in statuses):
        status = "GOOGLE_POLICY_PREFLIGHT_INCOMPLETE"
    else:
        status = "GOOGLE_POLICY_PREFLIGHT_PASS"

    return {
        "status": status,
        "approval_guaranteed": False,
        "expected_reports": len(files),
        "passed_reports": sum(1 for item in results if item["status"] == "GOOGLE_POLICY_PREFLIGHT_PASS"),
        "missing_reports": missing,
        "failed_reports": failed,
        "reports": results,
        "final_statement": (
            "Every final creative has a passing local Google Ads policy preflight; final Google review still applies."
            if status == "GOOGLE_POLICY_PREFLIGHT_PASS"
            else "The pack is not locally cleared as Google-ready; resolve all policy reports before delivery."
        )
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Aggregate per-banner Google policy preflight reports")
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--report-dir", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result = aggregate(load_json(args.manifest), args.report_dir)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "out": args.out.as_posix()}, ensure_ascii=False))
    return 0 if result["status"] == "GOOGLE_POLICY_PREFLIGHT_PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
