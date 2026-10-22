#!/usr/bin/env python3
"""Gate final completion on exact-artifact independent design and pack review."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


class ReadinessError(ValueError):
    pass


def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ReadinessError(f"file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ReadinessError(f"invalid JSON {path}: {exc}") from exc


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def blocking_review_problem(review: dict[str, Any]) -> str | None:
    if review.get("status") != "PASS":
        return f"review status is {review.get('status')!r}"
    checks = review.get("checks") or {}
    bad = [name for name, value in checks.items() if value in {"FAIL", "UNCHECKABLE"}]
    if bad:
        return "failed/uncheckable checks: " + ", ".join(bad)
    blocking = [item for item in review.get("findings") or [] if item.get("blocking")]
    if blocking:
        return f"{len(blocking)} blocking finding(s) remain"
    return None


def assess_readiness(
    matrix: dict[str, Any],
    manifest: dict[str, Any],
    review_dir: Path,
    pack_review_path: Path,
    *,
    manifest_path: Path | None = None,
    require_independent: bool = True,
) -> dict[str, Any]:
    rows = matrix.get("banner_matrix")
    files = manifest.get("files")
    if not isinstance(rows, list) or not rows:
        raise ReadinessError("banner_matrix must be non-empty")
    if not isinstance(files, list) or len(files) != len(rows):
        raise ReadinessError("manifest file count must match matrix")
    manifest_by_job = {item.get("job_id"): item for item in files}
    if len(manifest_by_job) != len(files):
        raise ReadinessError("manifest job IDs must be unique")

    review_results = []
    missing_reviews = []
    failed_reviews = []
    rigor_degradations = []
    for row in rows:
        job_id = row["job_id"]
        item = manifest_by_job.get(job_id)
        if item is None:
            failed_reviews.append({"job_id": job_id, "reason": "manifest missing job"})
            continue
        path = review_dir / f"{job_id}.review.json"
        if not path.is_file():
            missing_reviews.append(job_id)
            continue
        review = load_json(path)
        problem = None
        if review.get("job_id") != job_id:
            problem = f"review job_id {review.get('job_id')!r} does not match {job_id!r}"
        elif review.get("reviewer_role") != "DESIGN_REVIEWER":
            problem = "reviewer_role must be DESIGN_REVIEWER"
        elif review.get("reviewed_output_sha256") != item.get("sha256"):
            problem = "reviewed output hash is stale or mismatched"
        elif review.get("reviewed_output_path") != item.get("path"):
            problem = "reviewed output path does not match manifest"
        else:
            problem = blocking_review_problem(review)
        if not review.get("independent_context", False):
            rigor_degradations.append(f"{job_id}: reviewer was not independent")
            if require_independent and problem is None:
                problem = "independent review context required"
        if problem:
            failed_reviews.append({"job_id": job_id, "reason": problem})
        else:
            review_results.append({"job_id": job_id, "status": "PASS", "review_path": path.as_posix()})

    pack_problem = None
    pack_review = None
    if not pack_review_path.is_file():
        pack_problem = "pack review report missing"
    else:
        pack_review = load_json(pack_review_path)
        expected_manifest_hash = sha256_file(manifest_path) if manifest_path and manifest_path.is_file() else None
        if pack_review.get("reviewer_role") != "PACK_REVIEWER":
            pack_problem = "reviewer_role must be PACK_REVIEWER"
        elif expected_manifest_hash and pack_review.get("manifest_sha256") != expected_manifest_hash:
            pack_problem = "pack review manifest hash is stale or mismatched"
        else:
            pack_problem = blocking_review_problem(pack_review)
        if not pack_review.get("independent_context", False):
            rigor_degradations.append("PACK_REVIEWER: reviewer was not independent")
            if require_independent and pack_problem is None:
                pack_problem = "independent pack review context required"

    if missing_reviews:
        status = "REVIEW_INCOMPLETE"
    elif failed_reviews or pack_problem:
        status = "REVIEW_FAILED"
    else:
        status = "READY"

    delivery_status = "COMPLETE" if status == "READY" else "INCOMPLETE"
    run_rigor = "FULL" if not rigor_degradations else "DEGRADED"
    completion_claim_allowed = status == "READY" and (not require_independent or run_rigor == "FULL")
    return {
        "status": status,
        "delivery_status": delivery_status,
        "run_rigor": run_rigor,
        "completion_claim_allowed": completion_claim_allowed,
        "expected_banner_reviews": len(rows),
        "passed_banner_reviews": len(review_results),
        "missing_banner_reviews": missing_reviews,
        "failed_banner_reviews": failed_reviews,
        "pack_review_status": "PASS" if pack_review is not None and pack_problem is None else "FAIL",
        "pack_review_problem": pack_problem,
        "rigor_degradations": rigor_degradations,
        "banner_reviews": review_results,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Assess final banner-pack delivery readiness")
    parser.add_argument("--matrix", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--review-dir", type=Path, required=True)
    parser.add_argument("--pack-review", type=Path, required=True)
    parser.add_argument("--allow-degraded-review", action="store_true")
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    try:
        result = assess_readiness(
            load_json(args.matrix),
            load_json(args.manifest),
            args.review_dir,
            args.pack_review,
            manifest_path=args.manifest,
            require_independent=not args.allow_degraded_review,
        )
    except ReadinessError as exc:
        result = {"status": "FAIL_INPUT", "delivery_status": "INCOMPLETE", "completion_claim_allowed": False, "error": str(exc)}
    payload = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(payload + "\n", encoding="utf-8")
    else:
        print(payload)
    return 0 if result.get("completion_claim_allowed") else 2


if __name__ == "__main__":
    raise SystemExit(main())
