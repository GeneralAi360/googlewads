#!/usr/bin/env python3
"""Bind frozen creative copy/provenance into per-banner render-spec shells."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


class CreativeBindingError(ValueError):
    pass


def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise CreativeBindingError(f"file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise CreativeBindingError(f"invalid JSON {path}: {exc}") from exc


def frozen_map(freeze: dict[str, Any]) -> dict[str, dict[str, Any]]:
    if freeze.get("status") != "CREATIVE_CONTRACTS_FROZEN":
        raise CreativeBindingError("creative freeze is not ready")
    items = freeze.get("contracts") or []
    result = {item.get("concept_id"): item for item in items}
    if None in result or len(result) != len(items):
        raise CreativeBindingError("creative freeze concept IDs are invalid/duplicate")
    return result


def _apply_copy_override(copy: dict[str, Any], override: Any, label: str) -> None:
    if override is None:
        return
    if not isinstance(override, dict):
        raise CreativeBindingError(f"{label} copy override must be an object")
    allowed = {"headline", "support", "offer", "cta"}
    unknown = sorted(set(override) - allowed)
    if unknown:
        raise CreativeBindingError(f"{label} copy override has unknown keys: {', '.join(unknown)}")
    for key, value in override.items():
        copy[key] = value


def variant_copy(
    contract: dict[str, Any],
    variant_id: str,
    language: str,
    layout_family: str | None = None,
    dimension: str | None = None,
) -> dict[str, Any]:
    variants = {item["variant_id"]: item for item in contract["variants"]}
    if variant_id not in variants:
        raise CreativeBindingError(f"variant {variant_id} missing in {contract['concept_id']}")
    variant = variants[variant_id]
    copies = variant["copy_by_language"]
    if language not in copies:
        raise CreativeBindingError(f"language {language} missing in {contract['concept_id']}/{variant_id}")
    value = copies[language]
    result = {
        "headline": value["headline"],
        "support": value.get("support"),
        "offer": value.get("offer"),
        "cta": value["cta"],
    }
    if layout_family:
        family_override = (variant.get("copy_overrides_by_layout_family") or {}).get(layout_family)
        _apply_copy_override(result, family_override, f"layout family {layout_family}")
    if dimension:
        dimension_override = (variant.get("copy_overrides_by_dimension") or {}).get(dimension)
        _apply_copy_override(result, dimension_override, f"dimension {dimension}")
    if not isinstance(result.get("headline"), str) or not result["headline"].strip():
        raise CreativeBindingError(f"{contract['concept_id']}/{variant_id}/{language}: final headline cannot be empty")
    if not isinstance(result.get("cta"), str) or not result["cta"].strip():
        raise CreativeBindingError(f"{contract['concept_id']}/{variant_id}/{language}: final CTA cannot be empty")
    return result


def apply(matrix: dict[str, Any], freeze: dict[str, Any], contracts_dir: Path, spec_dir: Path, *, out_index: Path | None = None) -> dict[str, Any]:
    rows = matrix.get("banner_matrix")
    if not isinstance(rows, list) or not rows:
        raise CreativeBindingError("banner_matrix must be non-empty")
    frozen = frozen_map(freeze)
    bindings = []
    preproduction_sha = freeze.get("preproduction_freeze_sha256")
    for row in rows:
        concept_id, variant_id, language = row.get("concept_id"), row.get("variant_id"), row.get("language")
        meta = frozen.get(concept_id)
        if meta is None:
            raise CreativeBindingError(f"creative freeze missing {concept_id}")
        contract_path = contracts_dir / f"{concept_id}.creative.json"
        contract = load_json(contract_path)
        if meta.get("path") != contract_path.as_posix() or meta.get("sha256") is None:
            raise CreativeBindingError(f"creative freeze path mismatch for {concept_id}")
        art = contract.get("art_direction") or {}
        art_direction_id = art.get("art_direction_id")
        if not isinstance(art_direction_id, str) or not art_direction_id:
            raise CreativeBindingError(f"{concept_id}: frozen art_direction_id missing")
        if meta.get("art_direction_id") != art_direction_id:
            raise CreativeBindingError(f"{concept_id}: creative freeze art_direction_id mismatch")
        spec_path = spec_dir / f"{row['job_id']}.json"
        spec = load_json(spec_path)
        if spec.get("job_id") != row["job_id"]:
            raise CreativeBindingError(f"spec job mismatch: {row['job_id']}")
        copy = variant_copy(contract, variant_id, language, row.get("layout_family"), row.get("dimension"))
        spec["copy"] = copy
        lighting = contract.get("lighting") or {}
        spec["provenance"] = {
            **(spec.get("provenance") or {}),
            "brand_id": contract.get("brand_id"),
            "art_direction_id": art_direction_id,
            "preproduction_freeze_sha256": preproduction_sha,
            "creative_contract_id": concept_id,
            "creative_contract_path": contract_path.as_posix(),
            "creative_contract_sha256": meta["sha256"],
            "hero_asset_id": (spec.get("provenance") or {}).get("hero_asset_id"),
            "reference_dna_ids": contract.get("reference_dna_ids") or [],
            "source_grounding_ids": meta.get("source_grounding_ids") or [],
            "lighting_scheme_id": lighting.get("lighting_scheme_id")
        }
        spec_path.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        bindings.append({
            "job_id": row["job_id"],
            "concept_id": concept_id,
            "variant_id": variant_id,
            "language": language,
            "layout_family": row.get("layout_family"),
            "dimension": row.get("dimension"),
            "art_direction_id": art_direction_id,
            "preproduction_freeze_sha256": preproduction_sha,
            "render_spec_path": spec_path.as_posix(),
            "creative_contract_path": contract_path.as_posix(),
            "creative_contract_sha256": meta["sha256"],
            "applied_copy": copy,
        })
    result = {"status": "CREATIVE_CONTRACTS_APPLIED", "expected_jobs": len(rows), "bindings": bindings}
    if out_index:
        out_index.parent.mkdir(parents=True, exist_ok=True)
        out_index.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply frozen creative contracts to materialized banner render specs")
    parser.add_argument("--matrix", type=Path, required=True)
    parser.add_argument("--creative-freeze", type=Path, required=True)
    parser.add_argument("--contracts-dir", type=Path, required=True)
    parser.add_argument("--spec-dir", type=Path, required=True)
    parser.add_argument("--out-index", type=Path)
    args = parser.parse_args()
    try:
        result = apply(load_json(args.matrix), load_json(args.creative_freeze), args.contracts_dir, args.spec_dir, out_index=args.out_index)
    except CreativeBindingError as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, ensure_ascii=False))
        return 2
    print(json.dumps({"status": result["status"], "jobs": result["expected_jobs"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
