#!/usr/bin/env python3
"""Freeze market research, design brief, written art direction and representative approval before scale-out."""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class PreproductionFreezeError(ValueError):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code


def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise PreproductionFreezeError("FAIL_INPUT", f"file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise PreproductionFreezeError("FAIL_INPUT", f"invalid JSON {path}: {exc}") from exc


def canonical_sha(value: dict[str, Any]) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _require_text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise PreproductionFreezeError("PREPRODUCTION_INCOMPLETE", f"{label} is required")
    return value


def _validate_research(research: dict[str, Any], allow_degraded: bool) -> str:
    if research.get("status") != "COMPETITIVE_RESEARCH_COMPLETE":
        raise PreproductionFreezeError("COMPETITIVE_RESEARCH_INCOMPLETE", "competitive research is not complete")
    coverage = research.get("coverage_status")
    creatives = research.get("creatives")
    if not isinstance(creatives, list) or not creatives:
        raise PreproductionFreezeError("COMPETITIVE_RESEARCH_INCOMPLETE", "competitive research requires observed creatives")
    ids = [item.get("creative_id") for item in creatives if isinstance(item, dict)]
    if len(ids) != len(creatives) or any(not item for item in ids) or len(ids) != len(set(ids)):
        raise PreproductionFreezeError("COMPETITIVE_RESEARCH_INVALID", "creative IDs must be non-empty and unique")
    advertisers = {str(item.get("advertiser") or "").strip() for item in creatives}
    advertisers.discard("")
    if coverage == "FULL":
        if len(creatives) < 3 or len(advertisers) < 2:
            raise PreproductionFreezeError(
                "COMPETITIVE_RESEARCH_COVERAGE_LOW",
                "FULL research currently requires >=3 relevant creatives across >=2 advertisers/targets",
            )
        rigor = "FULL"
    elif coverage == "DEGRADED":
        reason = str(research.get("degradation_reason") or "").strip()
        if not reason:
            raise PreproductionFreezeError("COMPETITIVE_RESEARCH_DEGRADED", "degraded research requires a reason")
        if not allow_degraded:
            raise PreproductionFreezeError("COMPETITIVE_RESEARCH_DEGRADED", "degraded research requires explicit acceptance")
        rigor = "DEGRADED_ACCEPTED"
    else:
        raise PreproductionFreezeError("COMPETITIVE_RESEARCH_INVALID", "coverage_status must be FULL or DEGRADED")

    prohibited_claim_fragments = ("high-converting", "high converting", "высококонверсион")
    for item in creatives:
        evidence = item.get("performance_evidence") or {}
        tier = evidence.get("tier")
        note = str(evidence.get("note") or "").lower()
        if evidence.get("conversion_metric_verified") and tier not in {"A_VERIFIED_OWN_METRICS", "B_PUBLISHED_CASE_METRICS"}:
            raise PreproductionFreezeError(
                "PERFORMANCE_EVIDENCE_INVALID",
                f"{item.get('creative_id')}: verified conversion metric requires tier A or B",
            )
        if tier in {"C_PLATFORM_PERFORMANCE_SIGNAL", "D_MARKET_PROXY", "E_DESIGN_REFERENCE_ONLY"} and any(fragment in note for fragment in prohibited_claim_fragments):
            raise PreproductionFreezeError(
                "PERFORMANCE_CLAIM_UNSUPPORTED",
                f"{item.get('creative_id')}: non-metric evidence cannot be called high-converting",
            )
    return rigor


def _matrix_axes(matrix: dict[str, Any]) -> tuple[set[str], set[str], set[str], set[str]]:
    rows = matrix.get("banner_matrix")
    if not isinstance(rows, list) or not rows:
        raise PreproductionFreezeError("FAIL_MATRIX", "banner_matrix must be non-empty")
    concepts = {str(row.get("concept_id")) for row in rows}
    variants = {str(row.get("variant_id")) for row in rows}
    languages = {str(row.get("language")) for row in rows}
    sizes = {row.get("dimension") or f"{row.get('width')}x{row.get('height')}" for row in rows}
    return concepts, variants, languages, sizes


def freeze_preproduction(
    matrix: dict[str, Any],
    research: dict[str, Any],
    category_map: dict[str, Any],
    design_brief: dict[str, Any],
    art_approval: dict[str, Any],
    representative_approval: dict[str, Any],
    out_path: Path,
    *,
    research_path: Path,
    category_map_path: Path,
    design_brief_path: Path,
    art_approval_path: Path,
    representative_approval_path: Path,
    allow_degraded_research: bool = False,
) -> dict[str, Any]:
    if out_path.exists():
        raise PreproductionFreezeError("PREPRODUCTION_FREEZE_EXISTS", f"refusing to overwrite {out_path}")

    research_rigor = _validate_research(research, allow_degraded_research)
    research_id = _require_text(research.get("research_id"), "research_id")
    research_sha = canonical_sha(research)

    if category_map.get("research_id") != research_id or category_map.get("research_sha256") != research_sha:
        raise PreproductionFreezeError("CATEGORY_MAP_STALE", "category design map is not bound to the exact competitive research")
    category_map_id = _require_text(category_map.get("category_map_id"), "category_map_id")
    source_ids = set(category_map.get("source_creative_ids") or [])
    research_ids = {item["creative_id"] for item in research["creatives"]}
    if not source_ids or not source_ids <= research_ids:
        raise PreproductionFreezeError("CATEGORY_MAP_INVALID", "category map source IDs must come from competitive research")
    for key in ("mature_category_signals", "generic_ai_risks", "design_opportunities"):
        if not category_map.get(key):
            raise PreproductionFreezeError("CATEGORY_MAP_INCOMPLETE", f"category map {key} cannot be empty")
    category_sha = canonical_sha(category_map)

    design_brief_id = _require_text(design_brief.get("design_brief_id"), "design_brief_id")
    if design_brief.get("competitive_research_id") != research_id or design_brief.get("competitive_research_sha256") != research_sha:
        raise PreproductionFreezeError("DESIGN_BRIEF_STALE", "design brief research binding is stale/mismatched")
    if design_brief.get("category_map_id") != category_map_id or design_brief.get("category_map_sha256") != category_sha:
        raise PreproductionFreezeError("DESIGN_BRIEF_STALE", "design brief category-map binding is stale/mismatched")

    quality = design_brief.get("asset_quality_policy") or {}
    for key in (
        "reject_low_resolution_assets",
        "reject_generic_ai_clipart",
        "reject_unapproved_toy_clay_style",
        "reject_style_mismatch",
        "require_professional_category_fit",
    ):
        if quality.get(key) is not True:
            raise PreproductionFreezeError("ASSET_QUALITY_POLICY_MISSING", f"design brief must enforce {key}=true")

    concepts, variants, languages, sizes = _matrix_axes(matrix)
    outputs = design_brief.get("outputs") or {}
    rows = matrix["banner_matrix"]
    expected = int(matrix.get("expected_output_files", len(rows)))
    if outputs.get("expected_files") != expected:
        raise PreproductionFreezeError("DESIGN_BRIEF_OUTPUT_MISMATCH", "design brief expected_files does not match matrix")
    if set(outputs.get("sizes") or []) != sizes:
        raise PreproductionFreezeError("DESIGN_BRIEF_OUTPUT_MISMATCH", "design brief sizes do not match matrix")
    if outputs.get("concept_count") != len(concepts) or outputs.get("variant_count") != len(variants):
        raise PreproductionFreezeError("DESIGN_BRIEF_OUTPUT_MISMATCH", "design brief concept/variant counts do not match matrix")
    if set(outputs.get("languages") or []) != languages:
        raise PreproductionFreezeError("DESIGN_BRIEF_OUTPUT_MISMATCH", "design brief languages do not match matrix")

    strategy = design_brief.get("art_direction_strategy") or {}
    mode = strategy.get("mode")
    candidate_count = int(strategy.get("candidate_count", 0))
    if mode in {"ART_DIRECTION_PREVIEW_3", "ART_DIRECTION_AUTOSELECT_3"} and candidate_count < 3:
        raise PreproductionFreezeError("ART_DIRECTION_INCOMPLETE", f"{mode} requires at least three written candidates")
    if mode == "ART_DIRECTION_LOCKED" and candidate_count < 1:
        raise PreproductionFreezeError("ART_DIRECTION_INCOMPLETE", "locked art direction still requires one explicit written direction")
    design_sha = canonical_sha(design_brief)

    if art_approval.get("status") != "APPROVED":
        raise PreproductionFreezeError("ART_DIRECTION_NOT_APPROVED", "written art direction is not approved")
    if art_approval.get("design_brief_id") != design_brief_id or art_approval.get("design_brief_sha256") != design_sha:
        raise PreproductionFreezeError("ART_DIRECTION_APPROVAL_STALE", "art-direction approval is not bound to the exact design brief")
    direction = art_approval.get("selected_direction") or {}
    art_direction_id = _require_text(direction.get("art_direction_id"), "selected_direction.art_direction_id")
    required_direction_fields = (
        "visual_thesis", "composition", "hero_strategy", "typography", "palette",
        "lighting_image_treatment", "graphic_device", "whitespace_character",
    )
    for key in required_direction_fields:
        _require_text(direction.get(key), f"selected_direction.{key}")
    if not direction.get("anti_patterns"):
        raise PreproductionFreezeError("ART_DIRECTION_INCOMPLETE", "selected direction requires anti_patterns")
    candidates = direction.get("candidate_ids") or []
    if mode in {"ART_DIRECTION_PREVIEW_3", "ART_DIRECTION_AUTOSELECT_3"} and len(set(candidates)) < 3:
        raise PreproductionFreezeError("ART_DIRECTION_INCOMPLETE", "approved preview/autoselect direction must trace to >=3 candidates")
    art_sha = canonical_sha(art_approval)

    if representative_approval.get("status") != "APPROVED":
        raise PreproductionFreezeError("REPRESENTATIVE_DESIGN_NOT_APPROVED", "representative high-fidelity design is not approved")
    if representative_approval.get("art_direction_approval_id") != art_approval.get("approval_id") or representative_approval.get("art_direction_approval_sha256") != art_sha:
        raise PreproductionFreezeError("REPRESENTATIVE_APPROVAL_STALE", "representative approval is not bound to the exact written art direction")
    if representative_approval.get("art_direction_id") != art_direction_id:
        raise PreproductionFreezeError("REPRESENTATIVE_APPROVAL_STALE", "representative art_direction_id differs from approved direction")
    checks = representative_approval.get("quality_checks") or {}
    required_checks = (
        "asset_quality", "professional_category_fit", "hierarchy", "typography", "brand_fidelity",
        "commercial_message_fidelity", "hero_crop", "lighting_contrast", "cta_clarity", "anti_generic_ai",
    )
    failed = [name for name in required_checks if checks.get(name) != "PASS"]
    if failed:
        raise PreproductionFreezeError("REPRESENTATIVE_DESIGN_FAILED", "representative checks not PASS: " + ", ".join(failed))

    artifact_path = Path(_require_text(representative_approval.get("artifact_path"), "representative artifact_path"))
    if not artifact_path.is_file():
        raise PreproductionFreezeError("REPRESENTATIVE_ARTIFACT_MISSING", f"representative artifact not found: {artifact_path}")
    artifact_sha = sha256_file(artifact_path)
    if representative_approval.get("artifact_sha256") != artifact_sha:
        raise PreproductionFreezeError("REPRESENTATIVE_APPROVAL_STALE", "representative artifact SHA-256 is stale/mismatched")

    representative_format = strategy.get("representative_format")
    if representative_format:
        actual_format = f"{representative_approval.get('width')}x{representative_approval.get('height')}"
        if actual_format != representative_format:
            raise PreproductionFreezeError("REPRESENTATIVE_FORMAT_MISMATCH", f"approved representative {actual_format} != brief {representative_format}")

    rep_approval_sha = canonical_sha(representative_approval)
    matrix_sha = canonical_sha(matrix)
    fingerprint = hashlib.sha256((matrix_sha + research_sha + category_sha + design_sha + art_sha + rep_approval_sha + artifact_sha).encode("utf-8")).hexdigest()
    result = {
        "status": "PREPRODUCTION_FROZEN",
        "freeze_id": f"PPF-{fingerprint[:16]}",
        "frozen_at": utc_now_iso(),
        "matrix_sha256": matrix_sha,
        "research_rigor": research_rigor,
        "competitive_research": {"id": research_id, "path": research_path.as_posix(), "sha256": research_sha},
        "category_design_map": {"id": category_map_id, "path": category_map_path.as_posix(), "sha256": category_sha},
        "design_brief": {"id": design_brief_id, "path": design_brief_path.as_posix(), "sha256": design_sha},
        "art_direction_approval": {"id": art_approval["approval_id"], "path": art_approval_path.as_posix(), "sha256": art_sha},
        "representative_design_approval": {"id": representative_approval["approval_id"], "path": representative_approval_path.as_posix(), "sha256": rep_approval_sha},
        "selected_art_direction_id": art_direction_id,
        "representative_artifact_path": artifact_path.as_posix(),
        "representative_artifact_sha256": artifact_sha,
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


def main() -> int:
    p = argparse.ArgumentParser(description="Freeze competitive research through representative design approval before banner scale-out")
    p.add_argument("--matrix", type=Path, required=True)
    p.add_argument("--competitive-research", type=Path, required=True)
    p.add_argument("--category-map", type=Path, required=True)
    p.add_argument("--design-brief", type=Path, required=True)
    p.add_argument("--art-direction-approval", type=Path, required=True)
    p.add_argument("--representative-approval", type=Path, required=True)
    p.add_argument("--allow-degraded-research", action="store_true")
    p.add_argument("--out", type=Path, required=True)
    a = p.parse_args()
    try:
        result = freeze_preproduction(
            load_json(a.matrix),
            load_json(a.competitive_research),
            load_json(a.category_map),
            load_json(a.design_brief),
            load_json(a.art_direction_approval),
            load_json(a.representative_approval),
            a.out,
            research_path=a.competitive_research,
            category_map_path=a.category_map,
            design_brief_path=a.design_brief,
            art_approval_path=a.art_direction_approval,
            representative_approval_path=a.representative_approval,
            allow_degraded_research=a.allow_degraded_research,
        )
    except PreproductionFreezeError as exc:
        print(json.dumps({"status": exc.code, "error": str(exc)}, ensure_ascii=False))
        return 2
    print(json.dumps({"status": result["status"], "freeze_id": result["freeze_id"], "out": a.out.as_posix()}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
