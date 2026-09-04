#!/usr/bin/env python3
"""Render, validate, and manifest a complete banner matrix."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

HERE = Path(__file__).resolve().parent


class PackError(ValueError):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code


def load_script(name: str):
    path = HERE / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise PackError("FAIL_RUNTIME", f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise PackError("FAIL_INPUT", f"file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise PackError("FAIL_INPUT", f"invalid JSON {path}: {exc}") from exc


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical_json_sha256(value: dict[str, Any]) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256_bytes(payload)


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def validate_matrix(matrix: dict[str, Any]) -> list[dict[str, Any]]:
    rows = matrix.get("banner_matrix")
    if not isinstance(rows, list) or not rows:
        raise PackError("FAIL_MATRIX", "banner_matrix must be a non-empty list")
    expected = matrix.get("expected_output_files", len(rows))
    if int(expected) != len(rows):
        raise PackError("FAIL_MATRIX", f"expected_output_files={expected} but matrix has {len(rows)} rows")
    ids = [row.get("job_id") for row in rows]
    if any(not item for item in ids) or len(ids) != len(set(ids)):
        raise PackError("FAIL_MATRIX", "job IDs must be non-empty and unique")
    return rows


def assert_spec_matches_row(spec: dict[str, Any], row: dict[str, Any]) -> None:
    checks = {
        "job_id": row.get("job_id"),
        "width": row.get("width"),
        "height": row.get("height"),
        "layout_family": row.get("layout_family"),
    }
    mismatches = []
    for key, expected in checks.items():
        if spec.get(key) != expected:
            mismatches.append(f"{key}: spec={spec.get(key)!r} matrix={expected!r}")
    if mismatches:
        raise PackError("FAIL_SPEC_MATRIX_MISMATCH", "; ".join(mismatches))


def _dedupe(values: list[str] | None) -> list[str]:
    return list(dict.fromkeys(item for item in (values or []) if item))


def _contract_copy(contract: dict[str, Any], variant_id: str, language: str) -> dict[str, Any]:
    variants = contract.get("variants") or []
    by_variant = {item.get("variant_id"): item for item in variants if isinstance(item, dict) and item.get("variant_id")}
    if variant_id not in by_variant:
        raise PackError("FAIL_CREATIVE_BINDING", f"contract missing variant {variant_id}")
    copies = by_variant[variant_id].get("copy_by_language") or {}
    if language not in copies:
        raise PackError("FAIL_CREATIVE_BINDING", f"contract missing language {language} for {variant_id}")
    value = copies[language]
    if not isinstance(value, dict):
        raise PackError("FAIL_CREATIVE_BINDING", f"contract copy is malformed for {variant_id}/{language}")
    return {
        "headline": value.get("headline"),
        "support": value.get("support"),
        "offer": value.get("offer"),
        "cta": value.get("cta"),
    }


def assert_frozen_creative_binding(spec: dict[str, Any], row: dict[str, Any], *, required: bool) -> None:
    provenance = spec.get("provenance") or {}
    contract_id = provenance.get("creative_contract_id")
    contract_path_value = provenance.get("creative_contract_path")
    contract_sha = provenance.get("creative_contract_sha256")
    has_any = any(value not in {None, ""} for value in (contract_id, contract_path_value, contract_sha))

    if not has_any:
        if required:
            raise PackError("FAIL_CREATIVE_BINDING", "frozen creative binding is required before production render")
        return
    if not all(value not in {None, ""} for value in (contract_id, contract_path_value, contract_sha)):
        raise PackError("FAIL_CREATIVE_BINDING", "creative binding requires ID, path, and SHA-256 together")

    concept_id = row.get("concept_id")
    variant_id = row.get("variant_id")
    language = row.get("language")
    if not all(isinstance(value, str) and value for value in (concept_id, variant_id, language)):
        raise PackError("FAIL_CREATIVE_BINDING", "matrix row needs concept_id, variant_id, and language for creative binding")
    if contract_id != concept_id:
        raise PackError("FAIL_CREATIVE_BINDING", f"creative_contract_id {contract_id!r} != matrix concept {concept_id!r}")

    contract_path = Path(contract_path_value)
    contract = load_json(contract_path)
    actual_sha = canonical_json_sha256(contract)
    if actual_sha != contract_sha:
        raise PackError("FAIL_CREATIVE_BINDING", "creative contract SHA-256 is stale or mismatched")
    if contract.get("concept_id") != concept_id or contract.get("status") != "APPROVED":
        raise PackError("FAIL_CREATIVE_BINDING", "creative contract identity/status does not match frozen matrix")

    expected_copy = _contract_copy(contract, variant_id, language)
    if spec.get("copy") != expected_copy:
        raise PackError("FAIL_CREATIVE_BINDING", "render-spec copy differs from approved creative contract")

    expected_refs = contract.get("reference_dna_ids") or []
    if provenance.get("reference_dna_ids") != expected_refs:
        raise PackError("FAIL_CREATIVE_BINDING", "render-spec reference_dna_ids differ from creative contract")
    expected_sources = [item.get("source_id") for item in contract.get("source_grounding") or [] if isinstance(item, dict) and item.get("source_id")]
    if provenance.get("source_grounding_ids") != expected_sources:
        raise PackError("FAIL_CREATIVE_BINDING", "render-spec source grounding differs from creative contract")
    if provenance.get("brand_id") != contract.get("brand_id"):
        raise PackError("FAIL_CREATIVE_BINDING", "render-spec brand_id differs from creative contract")
    expected_lighting = (contract.get("lighting") or {}).get("lighting_scheme_id")
    if provenance.get("lighting_scheme_id") != expected_lighting:
        raise PackError("FAIL_CREATIVE_BINDING", "render-spec lighting scheme differs from creative contract")


def build_manifest(
    matrix: dict[str, Any],
    jobs: list[dict[str, Any]],
    mode: str,
    pack: str,
    spec_snapshot_date: str | None,
) -> dict[str, Any]:
    files = []
    jobs_by_id = {job["job_id"]: job for job in jobs}
    for row in matrix["banner_matrix"]:
        job = jobs_by_id[row["job_id"]]
        if job["status"] != "PASS":
            raise PackError("FAIL_MANIFEST", "manifest requires a fully passing pack")
        render = job["render"]
        saved = render["output"]
        output_path = Path(render["output_path"])
        provenance = job.get("spec_provenance") or {}
        reference_ids = _dedupe((provenance.get("reference_dna_ids") or []) + (row.get("reference_dna_ids") or []))
        files.append(
            {
                "job_id": row["job_id"],
                "concept_id": row.get("concept_id"),
                "variant_id": row.get("variant_id") or row["job_id"],
                "language": row.get("language"),
                "dimension": row.get("dimension") or f"{row['width']}x{row['height']}",
                "google_name": row.get("google_name"),
                "path": render["output_path"],
                "sha256": sha256_file(output_path),
                "render_spec_path": job["spec_path"],
                "render_spec_sha256": job.get("render_spec_sha256"),
                "width": row["width"],
                "height": row["height"],
                "bytes": saved.get("bytes"),
                "format": saved.get("format"),
                "layout_family": row.get("layout_family"),
                "brand_id": provenance.get("brand_id") or matrix.get("brand_id"),
                "creative_contract_id": provenance.get("creative_contract_id"),
                "creative_contract_path": provenance.get("creative_contract_path"),
                "creative_contract_sha256": provenance.get("creative_contract_sha256"),
                "hero_asset_id": provenance.get("hero_asset_id") or row.get("hero_asset_id"),
                "reference_dna_ids": reference_ids,
                "source_grounding_ids": _dedupe(provenance.get("source_grounding_ids")),
                "lighting_scheme_id": provenance.get("lighting_scheme_id") or row.get("lighting_scheme_id"),
                "status": "PASS",
                "checks": ["creative_binding", "deterministic_render", "google_technical_preflight"] if provenance.get("creative_contract_sha256") else ["deterministic_render", "google_technical_preflight"],
            }
        )
    return {
        "campaign_id": matrix.get("run_id") or "banner-run",
        "generated_at": utc_now_iso(),
        "platform_mode": mode,
        "google_pack": pack,
        "spec_snapshot_date": spec_snapshot_date,
        "matrix_sha256": canonical_json_sha256(matrix),
        "render_engine": "pillow-deterministic-v0.2",
        "files": files,
    }


def render_pack(
    matrix: dict[str, Any],
    spec_dir: Path,
    *,
    mode: str = "demand_gen_uploaded_display",
    pack: str = "core",
    contact_sheet: Path | None = None,
    manifest_path: Path | None = None,
    technical_validator: Callable[[Path, str, str], dict[str, Any]] | None = None,
    require_creative_binding: bool = False,
) -> dict[str, Any]:
    rows = validate_matrix(matrix)
    renderer = load_script("render_banner")
    sheet = load_script("build_contact_sheet")
    validator_module = None
    google_config = None
    spec_snapshot_date = matrix.get("spec_snapshot_date") or matrix.get("google_spec_snapshot_date")

    if technical_validator is None:
        validator_module = load_script("validate_google_banner")
        google_config = validator_module.load_config()
        if mode not in google_config["modes"]:
            raise PackError("FAIL_MODE", f"unknown validation mode: {mode}")
        if pack not in google_config["packs"]:
            raise PackError("FAIL_PACK", f"unknown Google pack: {pack}")
        spec_snapshot_date = google_config.get("snapshot_date") or spec_snapshot_date

        def technical_validator(path: Path, mode_name: str, pack_name: str):
            return validator_module.validate(path, mode_name, pack_name, google_config)

    jobs: list[dict[str, Any]] = []
    passed_files: list[Path] = []
    for row in rows:
        job_id = row["job_id"]
        spec_path = spec_dir / f"{job_id}.json"
        job = {
            "job_id": job_id,
            "spec_path": spec_path.as_posix(),
            "render_spec_sha256": None,
            "spec_provenance": {},
            "status": "FAIL",
            "render": None,
            "validation": None,
            "error": None,
        }
        try:
            raw_spec = spec_path.read_bytes()
            job["render_spec_sha256"] = sha256_bytes(raw_spec)
            try:
                spec = json.loads(raw_spec.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                raise PackError("FAIL_INPUT", f"invalid render spec {spec_path}: {exc}") from exc
            assert_spec_matches_row(spec, row)
            assert_frozen_creative_binding(spec, row, required=require_creative_binding)
            job["spec_provenance"] = dict(spec.get("provenance") or {})

            output = dict(spec.get("output") or {})
            output["path"] = str(row["output_path"])
            output["format"] = row.get("output_format", output.get("format", "png"))
            if google_config is not None:
                output.setdefault(
                    "target_max_bytes",
                    int(google_config["modes"][mode]["max_file_size_bytes_conservative"]),
                )
            spec["output"] = output

            render_report = renderer.render_banner(spec)
            output_path = Path(render_report["output_path"])
            validation = technical_validator(output_path, mode, pack)
            job["render"] = render_report
            job["validation"] = validation
            if validation.get("status") != "PASS":
                raise PackError(
                    "FAIL_TECHNICAL_PREFLIGHT",
                    "; ".join(validation.get("errors") or ["technical validation failed"]),
                )
            job["status"] = "PASS"
            passed_files.append(output_path)
        except (OSError, PackError, getattr(renderer, "RenderError", ValueError)) as exc:
            job["error"] = {"code": getattr(exc, "code", "FAIL_JOB"), "message": str(exc)}
        jobs.append(job)

    passed = sum(1 for job in jobs if job["status"] == "PASS")
    expected = len(rows)
    status = "PASS" if passed == expected else "FAIL"

    contact = None
    if passed_files and contact_sheet is not None:
        sheet.build_contact_sheet(passed_files, contact_sheet)
        contact = contact_sheet.as_posix()

    failures = [
        {
            "job_id": job["job_id"],
            **(job["error"] or {"code": "FAIL_JOB", "message": "unknown failure"}),
        }
        for job in jobs
        if job["status"] != "PASS"
    ]

    manifest = None
    manifest_sha256 = None
    if status == "PASS" and manifest_path is not None:
        manifest_data = build_manifest(matrix, jobs, mode, pack, spec_snapshot_date)
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(json.dumps(manifest_data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        manifest = manifest_path.as_posix()
        manifest_sha256 = sha256_file(manifest_path)

    return {
        "status": status,
        "run_id": matrix.get("run_id"),
        "expected_output_files": expected,
        "passed_output_files": passed,
        "failed_output_files": expected - passed,
        "google_spec_snapshot_date": spec_snapshot_date,
        "creative_binding_required": require_creative_binding,
        "contact_sheet": contact,
        "manifest": manifest,
        "manifest_sha256": manifest_sha256,
        "jobs": jobs,
        "failures": failures,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Render every row in a banner matrix from per-job render specs")
    parser.add_argument("--matrix", required=True, type=Path)
    parser.add_argument("--spec-dir", required=True, type=Path)
    parser.add_argument("--mode", default="demand_gen_uploaded_display")
    parser.add_argument("--pack", default="core")
    parser.add_argument("--contact-sheet", type=Path)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--allow-unbound-creative", action="store_true", help="Development/legacy only: permit render specs without a frozen creative contract")
    parser.add_argument("--report", required=True, type=Path)
    args = parser.parse_args()
    try:
        result = render_pack(
            load_json(args.matrix),
            args.spec_dir,
            mode=args.mode,
            pack=args.pack,
            contact_sheet=args.contact_sheet,
            manifest_path=args.manifest,
            require_creative_binding=not args.allow_unbound_creative,
        )
    except PackError as exc:
        result = {"status": "FAIL", "failures": [{"code": exc.code, "message": str(exc)}]}
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "report": args.report.as_posix()}, ensure_ascii=False))
    return 0 if result["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
