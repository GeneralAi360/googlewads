#!/usr/bin/env python3
"""Validate approved creative contracts against the frozen banner matrix."""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class CreativeFreezeError(ValueError):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code


def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise CreativeFreezeError("FAIL_INPUT", f"file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise CreativeFreezeError("FAIL_INPUT", f"invalid JSON {path}: {exc}") from exc


def canonical_sha(value: dict[str, Any]) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def expected_axes(matrix: dict[str, Any]) -> dict[str, dict[str, set[str]]]:
    rows = matrix.get("banner_matrix")
    if not isinstance(rows, list) or not rows:
        raise CreativeFreezeError("FAIL_MATRIX", "banner_matrix must be non-empty")
    axes: dict[str, dict[str, set[str]]] = {}
    for row in rows:
        concept = row.get("concept_id")
        variant = row.get("variant_id")
        language = row.get("language")
        if not all(isinstance(value, str) and value for value in (concept, variant, language)):
            raise CreativeFreezeError("FAIL_MATRIX", "every row needs concept_id, variant_id and language")
        axes.setdefault(concept, {}).setdefault(variant, set()).add(language)
    return axes


def validated_reference_ids(reference_index: dict[str, Any] | None) -> set[str] | None:
    if reference_index is None:
        return None
    if reference_index.get("status") not in {"REFERENCE_DNA_READY", "REFERENCE_NOT_APPLICABLE"}:
        raise CreativeFreezeError("REFERENCE_DNA_NOT_READY", "reference analysis index is not ready")
    return {item["reference_id"] for item in reference_index.get("reports") or []}


def validate_preproduction_freeze(
    preproduction: dict[str, Any] | None,
    matrix: dict[str, Any],
) -> tuple[str | None, str | None, dict[str, Any] | None, dict[str, Any] | None]:
    if preproduction is None:
        return None, None, None, None
    if preproduction.get("status") != "PREPRODUCTION_FROZEN":
        raise CreativeFreezeError("PREPRODUCTION_NOT_FROZEN", "preproduction design gate is not frozen")
    if preproduction.get("matrix_sha256") != canonical_sha(matrix):
        raise CreativeFreezeError("PREPRODUCTION_STALE", "preproduction freeze matrix hash is stale/mismatched")
    art_direction_id = preproduction.get("selected_art_direction_id")
    if not isinstance(art_direction_id, str) or not art_direction_id.strip():
        raise CreativeFreezeError("PREPRODUCTION_INVALID", "preproduction freeze selected_art_direction_id is required")
    representative_sha = preproduction.get("representative_artifact_sha256")
    if not isinstance(representative_sha, str) or len(representative_sha) != 64:
        raise CreativeFreezeError("PREPRODUCTION_INVALID", "preproduction freeze representative artifact SHA is required")
    commercial_lock = preproduction.get("commercial_lock")
    if not isinstance(commercial_lock, dict):
        raise CreativeFreezeError("PREPRODUCTION_INVALID", "preproduction freeze commercial_lock is required")
    brand_lock = preproduction.get("brand_identity_lock")
    if not isinstance(brand_lock, dict):
        raise CreativeFreezeError("PREPRODUCTION_INVALID", "preproduction freeze brand_identity_lock is required")
    return canonical_sha(preproduction), art_direction_id, commercial_lock, brand_lock


def validate_art_direction(contract: dict[str, Any], concept_id: str) -> dict[str, Any]:
    art = contract.get("art_direction")
    if not isinstance(art, dict):
        raise CreativeFreezeError("CREATIVE_ART_DIRECTION_ERROR", f"{concept_id}: art_direction must be frozen before production")
    mode = art.get("mode")
    if mode not in {"ART_DIRECTION_LOCKED", "ART_DIRECTION_PREVIEW_3", "ART_DIRECTION_AUTOSELECT_3"}:
        raise CreativeFreezeError("CREATIVE_ART_DIRECTION_ERROR", f"{concept_id}: invalid art_direction mode")
    for key in ("art_direction_id", "visual_thesis", "selection_provenance"):
        if not isinstance(art.get(key), str) or not art[key].strip():
            raise CreativeFreezeError("CREATIVE_ART_DIRECTION_ERROR", f"{concept_id}: art_direction.{key} is required")
    if art["selection_provenance"] not in {"BRAND_LOCKED", "USER_APPROVED", "ART_DIRECTOR_REVIEWER"}:
        raise CreativeFreezeError("CREATIVE_ART_DIRECTION_ERROR", f"{concept_id}: invalid art-direction selection provenance")
    candidates = art.get("selected_from_candidate_ids") or []
    if len(candidates) != len(set(candidates)):
        raise CreativeFreezeError("CREATIVE_ART_DIRECTION_ERROR", f"{concept_id}: duplicate art-direction candidate IDs")
    if mode in {"ART_DIRECTION_PREVIEW_3", "ART_DIRECTION_AUTOSELECT_3"}:
        if len(candidates) < 3:
            raise CreativeFreezeError("CREATIVE_ART_DIRECTION_ERROR", f"{concept_id}: {mode} requires at least three candidate IDs")
        if not isinstance(art.get("representative_preview_id"), str) or not art["representative_preview_id"].strip():
            raise CreativeFreezeError("CREATIVE_ART_DIRECTION_ERROR", f"{concept_id}: selected representative_preview_id is required")
    return art


def _validate_preproduction_locks(
    contract: dict[str, Any],
    concept_id: str,
    commercial_lock: dict[str, Any] | None,
    brand_lock: dict[str, Any] | None,
) -> None:
    if commercial_lock is not None:
        expected_prop = commercial_lock.get("primary_proposition")
        if contract.get("primary_proposition") != expected_prop:
            raise CreativeFreezeError(
                "CREATIVE_COMMERCIAL_LOCK_MISMATCH",
                f"{concept_id}: primary proposition differs from preproduction commercial lock",
            )
        approved_ctas = set(commercial_lock.get("approved_ctas") or [])
        if not approved_ctas:
            raise CreativeFreezeError("PREPRODUCTION_INVALID", "preproduction commercial lock has no approved CTA")
        for variant in contract.get("variants") or []:
            for language, copy in (variant.get("copy_by_language") or {}).items():
                if copy.get("cta") not in approved_ctas:
                    raise CreativeFreezeError(
                        "CREATIVE_COMMERCIAL_LOCK_MISMATCH",
                        f"{concept_id}/{variant.get('variant_id')}/{language}: CTA is not pre-approved",
                    )
            for scope_name in ("copy_overrides_by_layout_family", "copy_overrides_by_dimension"):
                for scope_id, override in (variant.get(scope_name) or {}).items():
                    if isinstance(override, dict) and override.get("cta") is not None and override.get("cta") not in approved_ctas:
                        raise CreativeFreezeError(
                            "CREATIVE_COMMERCIAL_LOCK_MISMATCH",
                            f"{concept_id}/{variant.get('variant_id')}/{scope_name}/{scope_id}: CTA override is not pre-approved",
                        )
    if brand_lock is not None:
        expected_brand_id = brand_lock.get("brand_id")
        if expected_brand_id is not None and contract.get("brand_id") != expected_brand_id:
            raise CreativeFreezeError(
                "CREATIVE_BRAND_LOCK_MISMATCH",
                f"{concept_id}: brand_id differs from preproduction brand identity lock",
            )


def validate_contract(
    contract: dict[str, Any],
    concept_id: str,
    variants: dict[str, set[str]],
    allowed_reference_ids: set[str] | None,
    *,
    preproduction_art_direction_id: str | None = None,
    preproduction_commercial_lock: dict[str, Any] | None = None,
    preproduction_brand_lock: dict[str, Any] | None = None,
) -> None:
    if contract.get("concept_id") != concept_id:
        raise CreativeFreezeError("CREATIVE_CONCEPT_MISMATCH", f"{concept_id}: contract concept_id mismatch")
    if contract.get("status") != "APPROVED":
        raise CreativeFreezeError("CREATIVE_NOT_APPROVED", f"{concept_id}: status must be APPROVED")
    for key in ("angle", "primary_proposition", "visual_idea", "primary_aoi"):
        if not isinstance(contract.get(key), str) or not contract[key].strip():
            raise CreativeFreezeError("CREATIVE_INCOMPLETE", f"{concept_id}: {key} is required")
    if not isinstance(contract.get("scan_path"), list) or len(contract["scan_path"]) < 2:
        raise CreativeFreezeError("CREATIVE_INCOMPLETE", f"{concept_id}: scan_path needs at least two stages")
    art = validate_art_direction(contract, concept_id)
    if preproduction_art_direction_id is not None and art.get("art_direction_id") != preproduction_art_direction_id:
        raise CreativeFreezeError("CREATIVE_PREPRODUCTION_MISMATCH", f"{concept_id}: creative art_direction_id differs from preproduction-approved direction")
    _validate_preproduction_locks(contract, concept_id, preproduction_commercial_lock, preproduction_brand_lock)

    grounding = contract.get("source_grounding")
    if not isinstance(grounding, list) or not grounding:
        raise CreativeFreezeError("CREATIVE_UNGROUNDED", f"{concept_id}: source_grounding cannot be empty")
    for item in grounding:
        if not isinstance(item, dict) or not item.get("source_id") or not item.get("supports"):
            raise CreativeFreezeError("CREATIVE_UNGROUNDED", f"{concept_id}: malformed source_grounding entry")
    refs = contract.get("reference_dna_ids") or []
    if len(refs) != len(set(refs)):
        raise CreativeFreezeError("CREATIVE_REFERENCE_ERROR", f"{concept_id}: duplicate reference_dna_ids")
    if allowed_reference_ids is not None:
        unknown = [ref for ref in refs if ref not in allowed_reference_ids]
        if unknown:
            raise CreativeFreezeError("CREATIVE_REFERENCE_ERROR", f"{concept_id}: unvalidated reference IDs: {', '.join(unknown)}")
    lighting = contract.get("lighting") or {}
    scheme_id = lighting.get("lighting_scheme_id")
    if scheme_id is not None and (not isinstance(scheme_id, int) or not 1 <= scheme_id <= 30):
        raise CreativeFreezeError("CREATIVE_LIGHTING_ERROR", f"{concept_id}: lighting_scheme_id must be 1..30 or null")

    candidate_variants = contract.get("variants")
    if not isinstance(candidate_variants, list) or not candidate_variants:
        raise CreativeFreezeError("CREATIVE_INCOMPLETE", f"{concept_id}: variants are required")
    by_variant = {}
    for item in candidate_variants:
        variant_id = item.get("variant_id") if isinstance(item, dict) else None
        if not variant_id or variant_id in by_variant:
            raise CreativeFreezeError("CREATIVE_VARIANT_ERROR", f"{concept_id}: invalid/duplicate variant ID")
        by_variant[variant_id] = item
    if set(by_variant) != set(variants):
        raise CreativeFreezeError("CREATIVE_VARIANT_ERROR", f"{concept_id}: variants {sorted(by_variant)} != matrix {sorted(variants)}")
    for variant_id, languages in variants.items():
        copies = by_variant[variant_id].get("copy_by_language")
        if not isinstance(copies, dict):
            raise CreativeFreezeError("CREATIVE_COPY_ERROR", f"{concept_id}/{variant_id}: copy_by_language missing")
        missing_languages = sorted(language for language in languages if language not in copies)
        if missing_languages:
            raise CreativeFreezeError("CREATIVE_COPY_ERROR", f"{concept_id}/{variant_id}: missing languages {missing_languages}")
        for language in languages:
            copy = copies[language]
            if not isinstance(copy, dict) or not str(copy.get("headline") or "").strip() or not str(copy.get("cta") or "").strip():
                raise CreativeFreezeError("CREATIVE_COPY_ERROR", f"{concept_id}/{variant_id}/{language}: headline and CTA required")


def freeze_contracts(
    matrix: dict[str, Any],
    contracts_dir: Path,
    out_path: Path,
    *,
    reference_index: dict[str, Any] | None = None,
    preproduction_freeze: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if out_path.exists():
        raise CreativeFreezeError("CREATIVE_FREEZE_EXISTS", f"refusing to overwrite {out_path}")
    axes = expected_axes(matrix)
    allowed_refs = validated_reference_ids(reference_index)
    preproduction_sha, approved_art_direction_id, commercial_lock, brand_lock = validate_preproduction_freeze(preproduction_freeze, matrix)
    frozen = []
    for concept_id in sorted(axes):
        path = contracts_dir / f"{concept_id}.creative.json"
        contract = load_json(path)
        validate_contract(
            contract,
            concept_id,
            axes[concept_id],
            allowed_refs,
            preproduction_art_direction_id=approved_art_direction_id,
            preproduction_commercial_lock=commercial_lock,
            preproduction_brand_lock=brand_lock,
        )
        art = contract["art_direction"]
        frozen.append({
            "concept_id": concept_id,
            "path": path.as_posix(),
            "sha256": canonical_sha(contract),
            "variant_ids": sorted(axes[concept_id]),
            "languages": sorted({language for languages in axes[concept_id].values() for language in languages}),
            "brand_id": contract.get("brand_id"),
            "art_direction_id": art["art_direction_id"],
            "reference_dna_ids": contract.get("reference_dna_ids") or [],
            "source_grounding_ids": [item["source_id"] for item in contract["source_grounding"]],
            "lighting_scheme_id": (contract.get("lighting") or {}).get("lighting_scheme_id")
        })
    extra = sorted(path.stem.replace(".creative", "") for path in contracts_dir.glob("*.creative.json") if path.stem.replace(".creative", "") not in axes)
    if extra:
        raise CreativeFreezeError("CREATIVE_EXTRA_CONTRACT", "contracts without matrix concepts: " + ", ".join(extra))
    result = {
        "status": "CREATIVE_CONTRACTS_FROZEN",
        "frozen_at": utc_now_iso(),
        "matrix_sha256": canonical_sha(matrix),
        "preproduction_freeze_id": preproduction_freeze.get("freeze_id") if preproduction_freeze else None,
        "preproduction_freeze_sha256": preproduction_sha,
        "concept_count": len(frozen),
        "contracts": frozen
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Freeze approved creative contracts against the banner matrix")
    parser.add_argument("--matrix", type=Path, required=True)
    parser.add_argument("--contracts-dir", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--reference-index", type=Path)
    parser.add_argument(
        "--preproduction-freeze",
        type=Path,
        required=True,
        help="Required normal-production binding proving competitive research, design brief, written art direction and representative design approval",
    )
    args = parser.parse_args()
    try:
        reference_index = load_json(args.reference_index) if args.reference_index else None
        result = freeze_contracts(
            load_json(args.matrix),
            args.contracts_dir,
            args.out,
            reference_index=reference_index,
            preproduction_freeze=load_json(args.preproduction_freeze),
        )
    except CreativeFreezeError as exc:
        print(json.dumps({"status": exc.code, "error": str(exc)}, ensure_ascii=False))
        return 2
    print(json.dumps({"status": result["status"], "concepts": result["concept_count"], "out": args.out.as_posix()}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
