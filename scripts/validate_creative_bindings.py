#!/usr/bin/env python3
"""Fail if a banner worker mutates frozen creative copy/provenance."""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent


class BindingValidationError(ValueError):
    pass


def load_script(name: str):
    spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    if spec is None or spec.loader is None:
        raise BindingValidationError(f"cannot load {name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        raise BindingValidationError(f"cannot read JSON {path}: {exc}") from exc


def validate(matrix: dict[str, Any], creative_freeze: dict[str, Any], contracts_dir: Path, spec_dir: Path) -> dict[str, Any]:
    apply_module = load_script("apply_creative_contracts")
    frozen = apply_module.frozen_map(creative_freeze)
    rows = matrix.get("banner_matrix") or []
    failures = []
    passed = []
    for row in rows:
        job_id = row["job_id"]
        concept_id, variant_id, language = row["concept_id"], row["variant_id"], row["language"]
        meta = frozen.get(concept_id)
        if meta is None:
            failures.append({"job_id": job_id, "reason": "concept missing from creative freeze"})
            continue
        contract_path = contracts_dir / f"{concept_id}.creative.json"
        spec_path = spec_dir / f"{job_id}.json"
        try:
            contract = load_json(contract_path)
            spec = load_json(spec_path)
            expected_copy = apply_module.variant_copy(
                contract,
                variant_id,
                language,
                row.get("layout_family"),
                row.get("dimension"),
            )
            provenance = spec.get("provenance") or {}
            problems = []
            if spec.get("copy") != expected_copy:
                problems.append("copy differs from frozen creative contract")
            if provenance.get("creative_contract_id") != concept_id:
                problems.append("creative_contract_id mismatch")
            if provenance.get("creative_contract_path") != contract_path.as_posix():
                problems.append("creative_contract_path mismatch")
            if provenance.get("creative_contract_sha256") != meta.get("sha256"):
                problems.append("creative_contract_sha256 mismatch")
            if provenance.get("reference_dna_ids") != (contract.get("reference_dna_ids") or []):
                problems.append("reference_dna_ids mismatch")
            if provenance.get("source_grounding_ids") != (meta.get("source_grounding_ids") or []):
                problems.append("source_grounding_ids mismatch")
            if provenance.get("brand_id") != contract.get("brand_id"):
                problems.append("brand_id mismatch")
            if provenance.get("lighting_scheme_id") != (contract.get("lighting") or {}).get("lighting_scheme_id"):
                problems.append("lighting_scheme_id mismatch")
            if problems:
                failures.append({"job_id": job_id, "reason": "; ".join(problems)})
            else:
                passed.append(job_id)
        except (BindingValidationError, getattr(apply_module, "CreativeBindingError", ValueError)) as exc:
            failures.append({"job_id": job_id, "reason": str(exc)})
    return {
        "status": "CREATIVE_BINDING_PASS" if not failures and len(passed) == len(rows) else "CREATIVE_BINDING_FAIL",
        "expected_jobs": len(rows),
        "passed_jobs": len(passed),
        "failures": failures,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate banner render specs against frozen creative contracts")
    parser.add_argument("--matrix", type=Path, required=True)
    parser.add_argument("--creative-freeze", type=Path, required=True)
    parser.add_argument("--contracts-dir", type=Path, required=True)
    parser.add_argument("--spec-dir", type=Path, required=True)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    try:
        result = validate(load_json(args.matrix), load_json(args.creative_freeze), args.contracts_dir, args.spec_dir)
    except BindingValidationError as exc:
        result = {"status": "FAIL_INPUT", "error": str(exc)}
    payload = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(payload + "\n", encoding="utf-8")
    else:
        print(payload)
    return 0 if result.get("status") == "CREATIVE_BINDING_PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
