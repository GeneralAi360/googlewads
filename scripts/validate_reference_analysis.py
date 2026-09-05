#!/usr/bin/env python3
"""Validate that every supplied reference has a usable REFERENCE_DNA report."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent


class ReferenceValidationError(ValueError):
    pass


def load_script(name: str):
    spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    if spec is None or spec.loader is None:
        raise ReferenceValidationError(f"cannot load script {name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ReferenceValidationError(f"file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ReferenceValidationError(f"invalid JSON {path}: {exc}") from exc


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate(context: dict[str, Any], reports_dir: Path, *, require_independent: bool = True) -> dict[str, Any]:
    job_module = load_script("materialize_reference_jobs")
    expected = job_module.normalize_items(context)
    if not expected:
        return {"status": "REFERENCE_NOT_APPLICABLE", "run_rigor": "FULL", "expected": 0, "passed": 0, "reports": [], "failures": []}
    reports = []
    failures = []
    degradations = []
    required_observations = {
        "composition_grid", "focal_object_scan_path", "typography", "color_contrast", "whitespace_density",
        "cta_treatment", "subject_scale", "lighting", "angle_crop", "mood_brand_signals"
    }
    for item in expected:
        path = reports_dir / f"{item['reference_id']}.reference-dna.json"
        if not path.is_file():
            failures.append({"reference_id": item["reference_id"], "reason": "report missing"})
            continue
        report = load_json(path)
        reason = None
        if report.get("reference_id") != item["reference_id"]:
            reason = "reference_id mismatch"
        elif report.get("source") != item["source"]:
            reason = "source mismatch"
        elif report.get("analyst_role") != "REFERENCE_ANALYST":
            reason = "analyst_role must be REFERENCE_ANALYST"
        elif report.get("status") != "PASS":
            reason = f"analysis status is {report.get('status')!r}"
        elif set((report.get("observations") or {}).keys()) != required_observations:
            reason = "observations do not contain the exact required fields"
        elif not isinstance(report.get("transferable_principles"), list) or not isinstance(report.get("do_not_copy"), list) or not isinstance(report.get("uncertainties"), list):
            reason = "DNA list fields are malformed"
        if not report.get("independent_context", False):
            degradations.append(f"{item['reference_id']}: analyst context was not independent")
            if require_independent and reason is None:
                reason = "independent analyst context required"
        if reason:
            failures.append({"reference_id": item["reference_id"], "reason": reason})
        else:
            reports.append({"reference_id": item["reference_id"], "source": item["source"], "path": path.as_posix(), "sha256": sha256_file(path)})
    status = "REFERENCE_DNA_READY" if not failures and len(reports) == len(expected) else "REFERENCE_ANALYSIS_INCOMPLETE"
    return {
        "status": status,
        "run_rigor": "FULL" if not degradations else "DEGRADED",
        "expected": len(expected),
        "passed": len(reports),
        "reports": reports,
        "failures": failures,
        "rigor_degradations": degradations,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate one REFERENCE_DNA report per supplied reference")
    parser.add_argument("--context", type=Path, required=True)
    parser.add_argument("--reports-dir", type=Path, required=True)
    parser.add_argument("--allow-degraded", action="store_true")
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    try:
        result = validate(load_json(args.context), args.reports_dir, require_independent=not args.allow_degraded)
    except ReferenceValidationError as exc:
        result = {"status": "FAIL_INPUT", "error": str(exc)}
    payload = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(payload + "\n", encoding="utf-8")
    else:
        print(payload)
    return 0 if result.get("status") in {"REFERENCE_DNA_READY", "REFERENCE_NOT_APPLICABLE"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
