#!/usr/bin/env python3
"""Freeze research, idea architecture, art direction, representative proof and design system before scale-out."""
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


def _matrix_axes(matrix: dict[str, Any]) -> tuple[set[str], set[str], set[str], set[str], set[str]]:
    rows = matrix.get("banner_matrix")
    if not isinstance(rows, list) or not rows:
        raise PreproductionFreezeError("FAIL_MATRIX", "banner_matrix must be non-empty")
    concepts = {str(row.get("concept_id")) for row in rows}
    variants = {str(row.get("variant_id")) for row in rows}
    languages = {str(row.get("language")) for row in rows}
    sizes = {row.get("dimension") or f"{row.get('width')}x{row.get('height')}" for row in rows}
    layout_families = {str(row.get("layout_family")) for row in rows if row.get("layout_family")}
    return concepts, variants, languages, sizes, layout_families


def _validate_design_locks(design_brief: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
    commercial_lock = design_brief.get("commercial_lock")
    if not isinstance(commercial_lock, dict):
        raise PreproductionFreezeError("COMMERCIAL_LOCK_MISSING", "design brief commercial_lock is required")
    proposition = _require_text(commercial_lock.get("primary_proposition"), "commercial_lock.primary_proposition")
    approved_ctas = commercial_lock.get("approved_ctas")
    if not isinstance(approved_ctas, list) or not approved_ctas or any(not isinstance(item, str) or not item.strip() for item in approved_ctas):
        raise PreproductionFreezeError("COMMERCIAL_LOCK_MISSING", "commercial_lock.approved_ctas must contain at least one CTA")
    if len(approved_ctas) != len(set(approved_ctas)):
        raise PreproductionFreezeError("COMMERCIAL_LOCK_INVALID", "commercial_lock.approved_ctas must be unique")
    if commercial_lock.get("copy_change_requires_controller_reapproval") is not True:
        raise PreproductionFreezeError("COMMERCIAL_LOCK_INVALID", "copy changes must require controller reapproval")
    commercial_message = design_brief.get("commercial_message") or {}
    if commercial_message.get("primary_proposition") not in {None, proposition}:
        raise PreproductionFreezeError("COMMERCIAL_LOCK_MISMATCH", "commercial_message primary proposition differs from commercial_lock")
    if commercial_message.get("cta") is not None and commercial_message.get("cta") not in approved_ctas:
        raise PreproductionFreezeError("COMMERCIAL_LOCK_MISMATCH", "commercial_message CTA is not in commercial_lock approved_ctas")

    brand_lock = design_brief.get("brand_identity_lock")
    if not isinstance(brand_lock, dict):
        raise PreproductionFreezeError("BRAND_IDENTITY_UNRESOLVED", "design brief brand_identity_lock is required")
    _require_text(brand_lock.get("display_name"), "brand_identity_lock.display_name")
    alternate_names = brand_lock.get("alternate_names_allowed")
    if not isinstance(alternate_names, list) or len(alternate_names) != len(set(alternate_names)):
        raise PreproductionFreezeError("BRAND_IDENTITY_UNRESOLVED", "alternate_names_allowed must be a unique list")
    brand_context = design_brief.get("brand_context") or {}
    if brand_context.get("brand_id") is not None and brand_context.get("brand_id") != brand_lock.get("brand_id"):
        raise PreproductionFreezeError("BRAND_IDENTITY_UNRESOLVED", "brand_context.brand_id differs from brand_identity_lock.brand_id")
    context_display = brand_context.get("display_name")
    if context_display is not None and context_display not in {brand_lock["display_name"], *alternate_names}:
        raise PreproductionFreezeError("BRAND_IDENTITY_UNRESOLVED", "brand_context display_name is not approved by brand_identity_lock")

    required_assets = design_brief.get("required_assets")
    if not isinstance(required_assets, list):
        raise PreproductionFreezeError("ASSET_REQUIREMENTS_MISSING", "design brief required_assets must be a list")
    asset_ids = [item.get("asset_id") for item in required_assets if isinstance(item, dict)]
    if len(asset_ids) != len(required_assets) or any(not item for item in asset_ids) or len(asset_ids) != len(set(asset_ids)):
        raise PreproductionFreezeError("ASSET_REQUIREMENTS_INVALID", "required asset IDs must be non-empty and unique")
    if brand_lock.get("logo_asset_required"):
        logo_requirements = [item for item in required_assets if item.get("required") and item.get("role") == "LOGO"]
        if not logo_requirements:
            raise PreproductionFreezeError("ASSET_REQUIREMENTS_MISSING", "brand identity requires an explicit LOGO asset requirement")
        if any(item.get("generated_substitute_allowed") for item in logo_requirements):
            raise PreproductionFreezeError("ASSET_REQUIREMENTS_INVALID", "generated logo substitutes cannot satisfy a locked brand identity")
    return commercial_lock, brand_lock, required_assets


def _validate_idea_character_lighting(design_brief: dict[str, Any]) -> tuple[str, str, str]:
    idea = design_brief.get("idea_architecture")
    if not isinstance(idea, dict):
        raise PreproductionFreezeError("IDEA_ARCHITECTURE_MISSING", "design brief idea_architecture is required")
    idea_id = _require_text(idea.get("idea_architecture_id"), "idea_architecture.idea_architecture_id")
    for key in ("core_idea", "single_takeaway", "creative_tension", "why_this_visual"):
        _require_text(idea.get(key), f"idea_architecture.{key}")
    if idea.get("presentation_mode") not in {
        "PRODUCT_PROOF", "OUTCOME_VISUALIZATION", "PAIN_VISUALIZATION", "EXPLAINER", "BEFORE_AFTER",
        "WORKFLOW", "HUMAN_CONTEXT", "CHARACTER", "VISUAL_METAPHOR", "VISUAL_PARADOX",
        "EDITORIAL_STATEMENT", "SOCIAL_PROOF", "PROMOTION_LED", "OTHER",
    }:
        raise PreproductionFreezeError("IDEA_ARCHITECTURE_INVALID", "unsupported presentation_mode")
    emotional = idea.get("emotional_target") or {}
    primary_emotion = _require_text(emotional.get("primary"), "idea_architecture.emotional_target.primary")
    if emotional.get("intensity") not in {"RESTRAINED", "MODERATE", "HIGH"}:
        raise PreproductionFreezeError("IDEA_ARCHITECTURE_INVALID", "emotional intensity must be RESTRAINED/MODERATE/HIGH")
    if idea.get("disruption_level") not in {"LOW", "MEDIUM", "HIGH"}:
        raise PreproductionFreezeError("IDEA_ARCHITECTURE_INVALID", "disruption_level must be LOW/MEDIUM/HIGH")

    visual = design_brief.get("visual_character")
    if not isinstance(visual, dict):
        raise PreproductionFreezeError("VISUAL_CHARACTER_MISSING", "design brief visual_character is required")
    visual_id = _require_text(visual.get("signature_id"), "visual_character.signature_id")
    _require_text(visual.get("primary_character"), "visual_character.primary_character")
    _require_text(visual.get("rationale"), "visual_character.rationale")
    for key in ("order_to_virality", "aesthetics_to_innovation"):
        value = visual.get(key)
        if not isinstance(value, (int, float)) or not 0 <= float(value) <= 1:
            raise PreproductionFreezeError("VISUAL_CHARACTER_INVALID", f"visual_character.{key} must be 0..1")
    if not isinstance(visual.get("style_tags"), list) or not visual["style_tags"]:
        raise PreproductionFreezeError("VISUAL_CHARACTER_INVALID", "visual_character.style_tags cannot be empty")

    focus = design_brief.get("focus_budget")
    if not isinstance(focus, dict):
        raise PreproductionFreezeError("FOCUS_BUDGET_MISSING", "design brief focus_budget is required")
    deviation = str(focus.get("deviation_rationale") or "").strip()
    default_exceeded = any(int(focus.get(key, 0)) > 1 for key in (
        "primary_idea_count", "primary_hero_count", "primary_emotion_count", "primary_visual_language_count"
    )) or int(focus.get("accent_detail_max", 0)) > 3
    if default_exceeded and not deviation:
        raise PreproductionFreezeError("FOCUS_BUDGET_UNJUSTIFIED", "focus budget exceeds default heuristic without deviation_rationale")

    forbidden = design_brief.get("forbidden_visuals")
    if not isinstance(forbidden, dict) or not all(isinstance(forbidden.get(key), list) for key in ("global", "brand", "concept")):
        raise PreproductionFreezeError("FORBIDDEN_VISUALS_MISSING", "global/brand/concept forbidden_visuals lists are required")

    chaos = design_brief.get("creative_chaos_audit")
    if not isinstance(chaos, dict) or chaos.get("status") != "PASS" or chaos.get("blockers"):
        raise PreproductionFreezeError("CREATIVE_CHAOS_AUDIT_FAILED", "creative chaos audit must PASS with zero blockers")
    required_true = (
        "core_idea_clear", "single_takeaway_clear", "presentation_mode_resolved", "emotional_target_resolved",
        "visual_character_coherent", "lighting_supports_idea", "composition_intentional",
        "forbidden_list_present", "platform_adaptation_planned",
    )
    if any(chaos.get(key) is not True for key in required_true) or chaos.get("information_overload") is not False or chaos.get("first_generation_is_final") is not False:
        raise PreproductionFreezeError("CREATIVE_CHAOS_AUDIT_FAILED", "creative chaos audit contains a failed strategy check")

    image_strategy = design_brief.get("image_strategy") or {}
    source_mode = image_strategy.get("source_mode")
    if source_mode not in {"REAL_ASSET", "GENERATED", "HYBRID", "NONE"}:
        raise PreproductionFreezeError("IMAGE_STRATEGY_INVALID", "image_strategy.source_mode is required")
    if source_mode in {"GENERATED", "HYBRID"} and image_strategy.get("hero_generation_spec_required") is not True:
        raise PreproductionFreezeError("HERO_GENERATION_SPEC_REQUIRED", "generated/hybrid hero strategy requires hero_generation_spec")

    lighting = design_brief.get("lighting_intent")
    if not isinstance(lighting, dict):
        raise PreproductionFreezeError("LIGHTING_INTENT_MISSING", "design brief lighting_intent is required")
    lighting_id = _require_text(lighting.get("lighting_intent_id"), "lighting_intent.lighting_intent_id")
    for key in ("relationship_to_idea", "primary_aoi_role", "emotional_function", "visual_character_alignment"):
        _require_text(lighting.get(key), f"lighting_intent.{key}")
    scene = lighting.get("scene_lighting") or {}
    scene_mode = scene.get("mode")
    scheme_ids = scene.get("candidate_scheme_ids")
    if scene_mode not in {"REQUIRED", "OPTIONAL", "NOT_APPLICABLE"} or not isinstance(scheme_ids, list):
        raise PreproductionFreezeError("LIGHTING_INTENT_INVALID", "scene lighting mode/candidate_scheme_ids invalid")
    if scene_mode == "REQUIRED" and not scheme_ids:
        raise PreproductionFreezeError("LIGHTING_INTENT_INVALID", "required scene lighting needs at least one candidate scheme")
    if scene_mode == "NOT_APPLICABLE" and scheme_ids:
        raise PreproductionFreezeError("LIGHTING_INTENT_INVALID", "NOT_APPLICABLE scene lighting cannot carry scheme candidates")
    if any(not isinstance(item, int) or not 1 <= item <= 30 for item in scheme_ids) or len(scheme_ids) != len(set(scheme_ids)):
        raise PreproductionFreezeError("LIGHTING_INTENT_INVALID", "scene lighting scheme IDs must be unique integers 1..30")
    _require_text(scene.get("rationale"), "lighting_intent.scene_lighting.rationale")

    composition = lighting.get("composition_lighting") or {}
    comp_mode = composition.get("mode")
    primitives = composition.get("allowed_primitives")
    valid_primitives = {"hero_edge_glow", "spotlight", "copy_scrim", "vignette", "text_plate"}
    if comp_mode not in {"REQUIRED", "OPTIONAL", "NOT_APPLICABLE"} or not isinstance(primitives, list):
        raise PreproductionFreezeError("LIGHTING_INTENT_INVALID", "composition lighting mode/allowed_primitives invalid")
    if any(item not in valid_primitives for item in primitives) or len(primitives) != len(set(primitives)):
        raise PreproductionFreezeError("LIGHTING_INTENT_INVALID", "composition lighting primitives are invalid/duplicate")
    if comp_mode == "REQUIRED" and not primitives:
        raise PreproductionFreezeError("LIGHTING_INTENT_INVALID", "required composition lighting needs an allowed primitive")
    if comp_mode == "NOT_APPLICABLE" and primitives:
        raise PreproductionFreezeError("LIGHTING_INTENT_INVALID", "NOT_APPLICABLE composition lighting cannot allow primitives")
    for key in ("copy_safe_zone_strategy", "focal_priority", "rationale"):
        _require_text(composition.get(key), f"lighting_intent.composition_lighting.{key}")
    if not isinstance(lighting.get("forbidden_behaviors"), list) or not lighting["forbidden_behaviors"]:
        raise PreproductionFreezeError("LIGHTING_INTENT_INVALID", "lighting_intent.forbidden_behaviors cannot be empty")

    if primary_emotion.lower() not in str(lighting.get("emotional_function") or "").lower():
        # Advisory semantics are free text; require only that the lighting function explicitly addresses the primary emotion.
        raise PreproductionFreezeError("LIGHTING_EMOTION_MISMATCH", "lighting emotional_function must explicitly reference the primary emotional target")
    return idea_id, visual_id, lighting_id


def _validate_campaign_design_system(
    system: dict[str, Any],
    *,
    design_brief: dict[str, Any],
    design_sha: str,
    art_approval: dict[str, Any],
    art_sha: str,
    representative_approval: dict[str, Any],
    representative_sha: str,
    art_direction_id: str,
    idea_id: str,
    visual_id: str,
    lighting_id: str,
    layout_families: set[str],
) -> str:
    if system.get("status") != "APPROVED":
        raise PreproductionFreezeError("CAMPAIGN_DESIGN_SYSTEM_NOT_APPROVED", "campaign design system must be APPROVED")
    if system.get("design_brief_id") != design_brief.get("design_brief_id") or system.get("design_brief_sha256") != design_sha:
        raise PreproductionFreezeError("CAMPAIGN_DESIGN_SYSTEM_STALE", "campaign design system design-brief binding is stale")
    if system.get("art_direction_approval_id") != art_approval.get("approval_id") or system.get("art_direction_approval_sha256") != art_sha:
        raise PreproductionFreezeError("CAMPAIGN_DESIGN_SYSTEM_STALE", "campaign design system art-direction binding is stale")
    if system.get("representative_approval_id") != representative_approval.get("approval_id") or system.get("representative_approval_sha256") != representative_sha:
        raise PreproductionFreezeError("CAMPAIGN_DESIGN_SYSTEM_STALE", "campaign design system representative binding is stale")
    expected = {
        "art_direction_id": art_direction_id,
        "idea_architecture_id": idea_id,
        "visual_character_signature_id": visual_id,
        "lighting_intent_id": lighting_id,
    }
    for key, value in expected.items():
        if system.get(key) != value:
            raise PreproductionFreezeError("CAMPAIGN_DESIGN_SYSTEM_MISMATCH", f"campaign design system {key} differs from approved preproduction")
    for key in (
        "campaign_design_system_id", "grid_logic", "headline_behavior", "offer_behavior", "cta_behavior",
        "brand_anchor_behavior", "hero_treatment", "crop_language", "background_system", "accent_system",
        "whitespace_character",
    ):
        _require_text(system.get(key), f"campaign_design_system.{key}")
    if not system.get("forbidden_patterns"):
        raise PreproductionFreezeError("CAMPAIGN_DESIGN_SYSTEM_INCOMPLETE", "campaign design system forbidden_patterns cannot be empty")
    adaptation = system.get("format_adaptation_rules")
    if not isinstance(adaptation, dict):
        raise PreproductionFreezeError("CAMPAIGN_DESIGN_SYSTEM_INCOMPLETE", "format_adaptation_rules are required")
    missing_families = sorted(family for family in layout_families if not str(adaptation.get(family) or "").strip())
    if missing_families:
        raise PreproductionFreezeError("CAMPAIGN_DESIGN_SYSTEM_INCOMPLETE", "missing format adaptation rules: " + ", ".join(missing_families))
    lighting_system = system.get("lighting_system") or {}
    allowed = lighting_system.get("allowed_primitives")
    brief_allowed = set((design_brief.get("lighting_intent") or {}).get("composition_lighting", {}).get("allowed_primitives") or [])
    if not isinstance(allowed, list) or not set(allowed) <= brief_allowed:
        raise PreproductionFreezeError("CAMPAIGN_LIGHTING_SYSTEM_MISMATCH", "campaign lighting primitives exceed lighting_intent")
    for key in ("scene_policy", "composition_policy", "focal_priority", "copy_safe_policy"):
        _require_text(lighting_system.get(key), f"campaign_design_system.lighting_system.{key}")
    if not lighting_system.get("forbidden_behaviors"):
        raise PreproductionFreezeError("CAMPAIGN_LIGHTING_SYSTEM_MISMATCH", "campaign lighting forbidden_behaviors cannot be empty")
    return _require_text(system.get("campaign_design_system_id"), "campaign_design_system_id")


def freeze_preproduction(
    matrix: dict[str, Any],
    research: dict[str, Any],
    category_map: dict[str, Any],
    design_brief: dict[str, Any],
    art_approval: dict[str, Any],
    representative_approval: dict[str, Any],
    campaign_design_system: dict[str, Any],
    out_path: Path,
    *,
    research_path: Path,
    category_map_path: Path,
    design_brief_path: Path,
    art_approval_path: Path,
    representative_approval_path: Path,
    campaign_design_system_path: Path,
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

    commercial_lock, brand_lock, required_assets = _validate_design_locks(design_brief)
    idea_id, visual_id, lighting_id = _validate_idea_character_lighting(design_brief)

    quality = design_brief.get("asset_quality_policy") or {}
    for key in (
        "reject_low_resolution_assets", "reject_generic_ai_clipart", "reject_unapproved_toy_clay_style",
        "reject_style_mismatch", "require_professional_category_fit",
    ):
        if quality.get(key) is not True:
            raise PreproductionFreezeError("ASSET_QUALITY_POLICY_MISSING", f"design brief must enforce {key}=true")

    concepts, variants, languages, sizes, layout_families = _matrix_axes(matrix)
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
    if direction.get("idea_architecture_id") != idea_id:
        raise PreproductionFreezeError("ART_DIRECTION_IDEA_MISMATCH", "approved direction does not inherit the frozen idea architecture")
    if direction.get("visual_character_signature_id") != visual_id:
        raise PreproductionFreezeError("ART_DIRECTION_CHARACTER_MISMATCH", "approved direction does not inherit the visual-character signature")
    if direction.get("lighting_intent_id") != lighting_id:
        raise PreproductionFreezeError("ART_DIRECTION_LIGHTING_MISMATCH", "approved direction does not inherit lighting_intent")
    if direction.get("presentation_mode") != (design_brief.get("idea_architecture") or {}).get("presentation_mode"):
        raise PreproductionFreezeError("ART_DIRECTION_IDEA_MISMATCH", "approved direction presentation_mode differs from idea architecture")
    if str(direction.get("emotional_target") or "").strip().lower() != str((design_brief.get("idea_architecture") or {}).get("emotional_target", {}).get("primary") or "").strip().lower():
        raise PreproductionFreezeError("ART_DIRECTION_EMOTION_MISMATCH", "approved direction primary emotion differs from idea architecture")
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
    campaign_system_id = _validate_campaign_design_system(
        campaign_design_system,
        design_brief=design_brief,
        design_sha=design_sha,
        art_approval=art_approval,
        art_sha=art_sha,
        representative_approval=representative_approval,
        representative_sha=rep_approval_sha,
        art_direction_id=art_direction_id,
        idea_id=idea_id,
        visual_id=visual_id,
        lighting_id=lighting_id,
        layout_families=layout_families,
    )
    campaign_system_sha = canonical_sha(campaign_design_system)

    matrix_sha = canonical_sha(matrix)
    fingerprint = hashlib.sha256((matrix_sha + research_sha + category_sha + design_sha + art_sha + rep_approval_sha + artifact_sha + campaign_system_sha).encode("utf-8")).hexdigest()
    result = {
        "status": "PREPRODUCTION_FROZEN",
        "freeze_id": f"PPF-{fingerprint[:16]}",
        "frozen_at": utc_now_iso(),
        "matrix_sha256": matrix_sha,
        "research_rigor": research_rigor,
        "competitive_research": {"id": research_id, "path": research_path.as_posix(), "sha256": research_sha},
        "category_design_map": {"id": category_map_id, "path": category_map_path.as_posix(), "sha256": category_sha},
        "design_brief": {"id": design_brief_id, "path": design_brief_path.as_posix(), "sha256": design_sha},
        "commercial_lock": commercial_lock,
        "brand_identity_lock": brand_lock,
        "required_asset_ids": [item["asset_id"] for item in required_assets if item.get("required")],
        "idea_architecture_id": idea_id,
        "visual_character_signature_id": visual_id,
        "lighting_intent_id": lighting_id,
        "art_direction_approval": {"id": art_approval["approval_id"], "path": art_approval_path.as_posix(), "sha256": art_sha},
        "representative_design_approval": {"id": representative_approval["approval_id"], "path": representative_approval_path.as_posix(), "sha256": rep_approval_sha},
        "campaign_design_system": {"id": campaign_system_id, "path": campaign_design_system_path.as_posix(), "sha256": campaign_system_sha},
        "selected_art_direction_id": art_direction_id,
        "representative_artifact_path": artifact_path.as_posix(),
        "representative_artifact_sha256": artifact_sha,
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


def main() -> int:
    p = argparse.ArgumentParser(description="Freeze competitive research through approved representative and campaign design system before scale-out")
    p.add_argument("--matrix", type=Path, required=True)
    p.add_argument("--competitive-research", type=Path, required=True)
    p.add_argument("--category-map", type=Path, required=True)
    p.add_argument("--design-brief", type=Path, required=True)
    p.add_argument("--art-direction-approval", type=Path, required=True)
    p.add_argument("--representative-approval", type=Path, required=True)
    p.add_argument("--campaign-design-system", type=Path, required=True)
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
            load_json(a.campaign_design_system),
            a.out,
            research_path=a.competitive_research,
            category_map_path=a.category_map,
            design_brief_path=a.design_brief,
            art_approval_path=a.art_direction_approval,
            representative_approval_path=a.representative_approval,
            campaign_design_system_path=a.campaign_design_system,
            allow_degraded_research=a.allow_degraded_research,
        )
    except PreproductionFreezeError as exc:
        print(json.dumps({"status": exc.code, "error": str(exc)}, ensure_ascii=False))
        return 2
    print(json.dumps({"status": result["status"], "freeze_id": result["freeze_id"], "out": a.out.as_posix()}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
