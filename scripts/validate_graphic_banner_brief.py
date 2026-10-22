#!/usr/bin/env python3
"""Validate the user-reviewable Graphic Banner Brief before visual exploration.

This gate exists because a correct commercial job can still drift into weak or
abstract visual exploration when no explicit advertising-design brief has been
approved. The brief is not the final art direction; it freezes the commercial
message, advertising role, design boundaries, anti-failure rules, and the rules
for generating the first user-facing concept set.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


class GraphicBannerBriefError(ValueError):
    pass


REQUIRED_ANTI_FAILURE_RULES = {
    "abstract_geometry_without_commercial_meaning",
    "decorative_form_substituted_for_ad_idea",
    "raw_generated_image_used_as_concept",
    "presentation_slide_composition",
    "generic_saas_template",
    "generic_3d_object",
    "cta_appended_after_layout",
    "brand_missing",
    "commercial_job_not_understood_at_first_glance",
    "requires_long_rationale_to_understand_visual",
    "visual_novelty_replacing_clarity",
}

REQUIRED_QUALITY_CHECKS = {
    "COMMERCIAL_JOB_FIDELITY",
    "FIRST_GLANCE_CLARITY",
    "ADVERTISING_IMPACT",
    "COMPOSITIONAL_CONFIDENCE",
    "TYPOGRAPHIC_CRAFT",
    "VISUAL_POLISH",
    "CATEGORY_PREMIUM_BAR",
    "NON_GENERIC_IDENTITY",
    "CTA_INTEGRATION",
    "BRAND_INTEGRATION",
    "HERO_SEMANTIC_RELEVANCE",
    "AD_NOT_PRESENTATION_SLIDE",
    "SMALL_FORMAT_VIABILITY",
}

JOB_TYPES = {
    "NEW_LICENSE_PURCHASE",
    "LICENSE_RENEWAL",
    "PURCHASE_OR_RENEWAL",
    "IMPLEMENTATION_SERVICE",
    "CONSULTATION",
    "OTHER",
}


def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise GraphicBannerBriefError(f"file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise GraphicBannerBriefError(f"invalid JSON {path}: {exc}") from exc


def canonical_sha(value: dict[str, Any]) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise GraphicBannerBriefError(f"{name} is required")
    return value.strip()


def _nonempty_list(value: Any, name: str, minimum: int = 1) -> list[Any]:
    if not isinstance(value, list) or len(value) < minimum:
        raise GraphicBannerBriefError(f"{name} must contain at least {minimum} item(s)")
    return value


def validate(commercial_job: dict[str, Any], brief: dict[str, Any]) -> dict[str, Any]:
    if commercial_job.get("status") != "COMMERCIAL_JOB_LOCKED":
        raise GraphicBannerBriefError("commercial job must be COMMERCIAL_JOB_LOCKED")
    job_id = _text(commercial_job.get("commercial_job_id"), "commercial_job.commercial_job_id")
    job_type = commercial_job.get("job_type")
    if job_type not in JOB_TYPES:
        raise GraphicBannerBriefError("commercial job_type is unsupported")
    job_sha = canonical_sha(commercial_job)

    if brief.get("schema_version") != "1.0":
        raise GraphicBannerBriefError("schema_version must be 1.0")
    brief_id = _text(brief.get("brief_id"), "brief_id")
    if brief.get("status") != "GRAPHIC_BANNER_BRIEF_READY_FOR_USER_REVIEW":
        raise GraphicBannerBriefError("brief status must be GRAPHIC_BANNER_BRIEF_READY_FOR_USER_REVIEW")
    if brief.get("approval_required") is not True:
        raise GraphicBannerBriefError("graphic banner brief requires explicit user approval")

    bindings = brief.get("source_bindings") or {}
    if bindings.get("commercial_job_id") != job_id:
        raise GraphicBannerBriefError("brief is bound to a different commercial_job_id")
    if bindings.get("commercial_job_sha256") != job_sha:
        raise GraphicBannerBriefError("brief commercial-job SHA is stale or mismatched")
    if bindings.get("research_rigor") not in {"FULL", "DEGRADED", "NOT_APPLICABLE"}:
        raise GraphicBannerBriefError("source_bindings.research_rigor is invalid")

    core = brief.get("commercial_core") or {}
    brief_job = core.get("commercial_job") or {}
    if brief_job.get("job_type") != job_type:
        raise GraphicBannerBriefError("commercial_core job_type differs from commercial-job lock")
    _text(brief_job.get("plain_language"), "commercial_core.commercial_job.plain_language")

    brand = core.get("brand") or {}
    _text(brand.get("display_name"), "commercial_core.brand.display_name")
    product = core.get("product") or {}
    _text(product.get("name"), "commercial_core.product.name")
    _nonempty_list(product.get("scope"), "commercial_core.product.scope")
    _text(core.get("campaign_objective"), "commercial_core.campaign_objective")

    audience = core.get("audience") or {}
    for key in ("primary", "decision_context", "funnel_state"):
        _text(audience.get(key), f"commercial_core.audience.{key}")
    _nonempty_list(core.get("geography"), "commercial_core.geography")
    _nonempty_list(core.get("languages"), "commercial_core.languages")

    cta = core.get("cta") or {}
    cta_text = _text(cta.get("text"), "commercial_core.cta.text")
    if cta.get("status") != "LOCKED":
        raise GraphicBannerBriefError("CTA must be LOCKED before brief approval")

    message = brief.get("message_architecture") or {}
    _text(message.get("first_glance_takeaway"), "message_architecture.first_glance_takeaway")
    _text(message.get("primary_message"), "message_architecture.primary_message")
    if _text(message.get("cta_message"), "message_architecture.cta_message") != cta_text:
        raise GraphicBannerBriefError("message_architecture.cta_message must exactly match locked CTA")
    if _text(message.get("brand_message"), "message_architecture.brand_message") != brand.get("display_name").strip():
        raise GraphicBannerBriefError("message_architecture.brand_message must match canonical display brand")
    _nonempty_list(message.get("mandatory_information"), "message_architecture.mandatory_information", minimum=3)
    _nonempty_list(message.get("message_priority"), "message_architecture.message_priority", minimum=3)
    if message.get("max_message_complexity") not in {"LOW", "LOW_TO_MEDIUM", "MEDIUM"}:
        raise GraphicBannerBriefError("message complexity must stay bounded")

    strategy = brief.get("advertising_strategy") or {}
    _text(strategy.get("banner_role"), "advertising_strategy.banner_role")
    _text(strategy.get("desired_user_reaction"), "advertising_strategy.desired_user_reaction")
    _text(strategy.get("persuasion_mechanism"), "advertising_strategy.persuasion_mechanism")
    _text(strategy.get("trust_mechanism"), "advertising_strategy.trust_mechanism")
    _nonempty_list(strategy.get("visual_should_answer"), "advertising_strategy.visual_should_answer", minimum=3)
    if strategy.get("visual_must_not_depend_on_explanation") is not True:
        raise GraphicBannerBriefError("visual_must_not_depend_on_explanation must be true")
    _nonempty_list(strategy.get("allowed_banner_families"), "advertising_strategy.allowed_banner_families", minimum=2)
    _nonempty_list(strategy.get("discouraged_banner_families"), "advertising_strategy.discouraged_banner_families")

    semantics = brief.get("visual_semantics") or {}
    _text(semantics.get("primary_visual_job"), "visual_semantics.primary_visual_job")
    hero = semantics.get("hero_requirement") or {}
    for key in ("hero_semantic_test_required", "hero_must_support_commercial_job", "generic_visual_rejection_test"):
        if hero.get(key) is not True:
            raise GraphicBannerBriefError(f"visual_semantics.hero_requirement.{key} must be true")
    product_ui = semantics.get("product_ui") or {}
    if product_ui.get("fake_ui_allowed") is not False:
        raise GraphicBannerBriefError("fake product UI must be forbidden")

    composition = brief.get("composition_brief") or {}
    _text(composition.get("representative_size"), "composition_brief.representative_size")
    _text(composition.get("primary_aoi"), "composition_brief.primary_aoi")
    _nonempty_list(composition.get("required_scan_path_roles"), "composition_brief.required_scan_path_roles", minimum=3)
    _nonempty_list(composition.get("hierarchy_requirements"), "composition_brief.hierarchy_requirements", minimum=2)
    _text(composition.get("negative_space"), "composition_brief.negative_space")
    _text(composition.get("cta_integration"), "composition_brief.cta_integration")
    _text(composition.get("brand_anchor"), "composition_brief.brand_anchor")

    typography = brief.get("typography_brief") or {}
    if typography.get("font_family_count_max") not in {1, 2}:
        raise GraphicBannerBriefError("typography must use at most two font families")
    _nonempty_list(typography.get("craft_checks"), "typography_brief.craft_checks", minimum=4)

    light = brief.get("color_and_lighting_brief") or {}
    if light.get("decorative_lighting_forbidden") is not True:
        raise GraphicBannerBriefError("decorative lighting must be explicitly forbidden")
    if light.get("materiality_requires_semantic_reason") is not True:
        raise GraphicBannerBriefError("materiality must require a semantic reason")

    boundaries = brief.get("graphic_style_boundaries") or {}
    _nonempty_list(boundaries.get("desired_character"), "graphic_style_boundaries.desired_character", minimum=3)
    _nonempty_list(boundaries.get("must_not_look_like"), "graphic_style_boundaries.must_not_look_like", minimum=3)

    anti = brief.get("anti_failure_rules")
    if not isinstance(anti, dict):
        raise GraphicBannerBriefError("anti_failure_rules must be an object")
    missing_rules = sorted(REQUIRED_ANTI_FAILURE_RULES - set(anti))
    if missing_rules:
        raise GraphicBannerBriefError("missing anti-failure rules: " + ", ".join(missing_rules))
    for name, value in anti.items():
        if value not in {"REJECT", "REVIEW_REQUIRED"}:
            raise GraphicBannerBriefError(f"anti_failure_rules.{name} must be REJECT or REVIEW_REQUIRED")
    for hard_reject in (
        "abstract_geometry_without_commercial_meaning",
        "decorative_form_substituted_for_ad_idea",
        "raw_generated_image_used_as_concept",
        "presentation_slide_composition",
        "generic_3d_object",
        "commercial_job_not_understood_at_first_glance",
        "visual_novelty_replacing_clarity",
    ):
        if anti.get(hard_reject) != "REJECT":
            raise GraphicBannerBriefError(f"anti_failure_rules.{hard_reject} must be REJECT")

    generation = brief.get("concept_generation_rules") or {}
    required_true = (
        "user_brief_approval_required_before_render",
        "all_concepts_same_commercial_job",
        "material_difference_required",
        "concepts_should_differ_by_advertising_logic",
        "hero_generation_is_optional",
        "hero_generation_must_not_be_first_default_step",
        "raw_generated_asset_is_never_visual_concept",
        "complete_banner_composite_required",
    )
    for key in required_true:
        if generation.get(key) is not True:
            raise GraphicBannerBriefError(f"concept_generation_rules.{key} must be true")
    if generation.get("user_facing_artifact_role") != "BANNER_COMPOSITE":
        raise GraphicBannerBriefError("user-facing artifact role must be BANNER_COMPOSITE")
    mode = generation.get("first_round_mode")
    count = generation.get("concept_count")
    if mode == "EXPLORE_3" and count != 3:
        raise GraphicBannerBriefError("EXPLORE_3 requires concept_count=3")
    if mode == "SINGLE_USER_LOCKED" and count != 1:
        raise GraphicBannerBriefError("SINGLE_USER_LOCKED requires concept_count=1")
    if mode not in {"EXPLORE_3", "SINGLE_USER_LOCKED"}:
        raise GraphicBannerBriefError("unsupported first_round_mode")
    if not isinstance(generation.get("minimum_distinct_design_axes"), int) or generation["minimum_distinct_design_axes"] < 3:
        raise GraphicBannerBriefError("minimum_distinct_design_axes must be >=3")

    quality = brief.get("concept_quality_bar") or {}
    if quality.get("required_status") != "PRESENTATION_READY_DESIGN":
        raise GraphicBannerBriefError("concept quality bar must require PRESENTATION_READY_DESIGN")
    checks = set(_nonempty_list(quality.get("checks"), "concept_quality_bar.checks", minimum=8))
    missing_checks = sorted(REQUIRED_QUALITY_CHECKS - checks)
    if missing_checks:
        raise GraphicBannerBriefError("concept quality bar missing checks: " + ", ".join(missing_checks))
    if quality.get("user_must_not_be_first_basic_qa") is not True:
        raise GraphicBannerBriefError("user must not be the first basic visual QA pass")

    scope = brief.get("deliverable_scope") or {}
    if scope.get("brief_stage_output") != "NO_IMAGES":
        raise GraphicBannerBriefError("brief stage must produce NO_IMAGES")
    if scope.get("full_pack_before_visual_approval") is not False:
        raise GraphicBannerBriefError("full pack must remain blocked before visual approval")

    return {
        "status": "GRAPHIC_BANNER_BRIEF_READY_FOR_USER_APPROVAL",
        "brief_id": brief_id,
        "brief_sha256": canonical_sha(brief),
        "commercial_job_id": job_id,
        "commercial_job_sha256": job_sha,
        "first_round_mode": mode,
        "visual_exploration_count": count,
        "render_allowed": False,
        "full_production_allowed": False,
        "next_user_decision": ["APPROVE BRIEF", "REVISE BRIEF"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Graphic Banner Brief before user approval")
    parser.add_argument("--commercial-job", type=Path, required=True)
    parser.add_argument("--brief", type=Path, required=True)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    try:
        result = validate(load_json(args.commercial_job), load_json(args.brief))
    except GraphicBannerBriefError as exc:
        result = {
            "status": "GRAPHIC_BANNER_BRIEF_INVALID",
            "render_allowed": False,
            "full_production_allowed": False,
            "error": str(exc),
        }
    payload = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(payload + "\n", encoding="utf-8")
    else:
        print(payload)
    return 0 if result.get("status") == "GRAPHIC_BANNER_BRIEF_READY_FOR_USER_APPROVAL" else 2


if __name__ == "__main__":
    raise SystemExit(main())
