import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BRIEF_SCRIPT = ROOT / "scripts" / "validate_graphic_banner_brief.py"
DECISION_SCRIPT = ROOT / "scripts" / "validate_graphic_banner_brief_decision.py"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class GraphicBannerBriefTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.brief_mod = load_module(BRIEF_SCRIPT, "validate_graphic_banner_brief")
        cls.decision_mod = load_module(DECISION_SCRIPT, "validate_graphic_banner_brief_decision")

    def commercial_job(self):
        return {
            "commercial_job_id": "CJ-MIT-B24-PURCHASE",
            "status": "COMMERCIAL_JOB_LOCKED",
            "product_or_service": "Bitrix24 license",
            "job_type": "NEW_LICENSE_PURCHASE",
            "purchase_renewal_structure": "NOT_APPLICABLE",
            "target_transaction": "purchase a new Bitrix24 license",
            "allowed_message_scope": ["new license purchase", "cloud and box editions"],
            "excluded_job_types": ["LICENSE_RENEWAL", "IMPLEMENTATION_SERVICE", "CONSULTATION"],
            "source_basis": "USER_EXPLICIT",
            "source_note": None,
            "change_requires_controller_reapproval": True,
        }

    def brief(self):
        job = self.commercial_job()
        return {
            "schema_version": "1.0",
            "brief_id": "GBB-MIT-B24-PURCHASE-001",
            "status": "GRAPHIC_BANNER_BRIEF_READY_FOR_USER_REVIEW",
            "approval_required": True,
            "source_bindings": {
                "commercial_job_id": job["commercial_job_id"],
                "commercial_job_sha256": self.brief_mod.canonical_sha(job),
                "landing_page": "https://crm.mitgroup.ru",
                "research_rigor": "DEGRADED",
                "competitive_research_sha256": None,
                "category_design_map_sha256": None,
                "commercial_lock_sha256": None,
                "brand_identity_lock_sha256": None,
            },
            "commercial_core": {
                "brand": {"brand_id": "mitgroup", "display_name": "MITGROUP"},
                "product": {"name": "Битрикс24", "scope": ["CLOUD", "BOX"]},
                "commercial_job": {"job_type": "NEW_LICENSE_PURCHASE", "plain_language": "Покупка новой лицензии Битрикс24"},
                "campaign_objective": "LEAD_GENERATION",
                "audience": {
                    "primary": "Руководители и владельцы бизнеса, выбирающие Битрикс24",
                    "decision_context": "Выбор новой лицензии / редакции",
                    "funnel_state": "PRODUCT_AWARE",
                },
                "geography": ["Беларусь"],
                "languages": ["ru"],
                "destination": {"url": "https://crm.mitgroup.ru", "destination_job_match": "PASS"},
                "cta": {"text": "Выбрать редакцию", "status": "LOCKED"},
                "promotional_offer": {"status": "NONE", "text": None},
                "affiliation_claim": {"status": "NONE", "text": None},
            },
            "message_architecture": {
                "first_glance_takeaway": "Можно выбрать новую лицензию Битрикс24.",
                "primary_message": "Новая лицензия Битрикс24",
                "secondary_message": "Облачная и коробочная версии",
                "cta_message": "Выбрать редакцию",
                "brand_message": "MITGROUP",
                "mandatory_information": ["Битрикс24", "новая лицензия", "Выбрать редакцию", "MITGROUP"],
                "optional_information": ["облачная версия", "коробочная версия"],
                "forbidden_information": ["внедрение", "продление", "неподтвержденная скидка"],
                "message_priority": ["COMMERCIAL_JOB", "PRODUCT", "CTA", "BRAND"],
                "max_message_complexity": "LOW_TO_MEDIUM",
            },
            "advertising_strategy": {
                "banner_role": "COMMERCIAL_DECISION_AD",
                "desired_user_reaction": "Понять предложение и перейти к выбору редакции.",
                "persuasion_mechanism": "CLARITY_OF_CHOICE",
                "trust_mechanism": "PRODUCT_AND_COMMERCIAL_CLARITY",
                "visual_should_answer": ["Что рекламируется?", "Какое действие предлагается?", "Почему это связано именно с выбором лицензии?"],
                "visual_must_not_depend_on_explanation": True,
                "allowed_banner_families": ["PRODUCT_LED", "DECISION_LED", "TYPOGRAPHY_LED"],
                "discouraged_banner_families": ["ABSTRACT_TECH_METAPHOR", "DECORATIVE_3D_OBJECT", "PRESENTATION_SLIDE"],
            },
            "visual_semantics": {
                "primary_visual_job": "Усилить понятность выбора новой лицензии.",
                "hero_requirement": {
                    "hero_is_required": False,
                    "allowed_hero_roles": ["PRODUCT_PROOF", "DECISION_OBJECT", "TYPOGRAPHIC_HERO"],
                    "hero_semantic_test_required": True,
                    "hero_must_support_commercial_job": True,
                    "generic_visual_rejection_test": True,
                },
                "product_ui": {"required": False, "allowed_when_semantically_useful": True, "fake_ui_allowed": False},
                "product_scope_representation": {"must_be_visible": False, "representation": "CONCEPT_DEPENDENT"},
            },
            "composition_brief": {
                "representative_size": "300x250",
                "primary_aoi": "CONCEPT_DEPENDENT",
                "required_scan_path_roles": ["PRIMARY_MESSAGE", "COMMERCIAL_OR_PRODUCT_CUE", "CTA", "BRAND"],
                "hierarchy_requirements": ["single dominant entry point", "secondary copy must not compete"],
                "negative_space": "Use whitespace to support hierarchy and premium clarity",
                "cta_integration": "CTA must belong to the composition, not be appended afterward",
                "brand_anchor": "Visible but subordinate to the commercial message",
                "small_format_resilience": ["product/commercial message survives", "CTA survives", "brand survives"],
            },
            "typography_brief": {
                "role": "PRIMARY_COMMERCIAL_STRUCTURE",
                "tone": ["MODERN", "B2B", "CONFIDENT", "PRECISE"],
                "avoid": ["DEFAULT_OFFICE_LOOK", "FUTURISTIC_GAMING"],
                "font_family_count_max": 2,
                "headline": "1-3 lines, must survive thumbnail",
                "secondary_copy": "low-to-medium priority and may not drive the layout",
                "cta": "immediately legible",
                "script_requirements": ["CYRILLIC_REQUIRED", "RUNTIME_FONT_VERIFICATION"],
                "craft_checks": ["OPTICAL_ALIGNMENT", "LINE_BREAKS", "WEIGHT_CONTRAST", "SPACING", "READABILITY"],
            },
            "color_and_lighting_brief": {
                "palette_strategy": "CONCEPT_DEPENDENT_WITHIN_BRAND_AND_CATEGORY",
                "contrast_priority": "HIGH",
                "lighting_purpose": "HIERARCHY_AND_MATERIAL_SEPARATION",
                "decorative_lighting_forbidden": True,
                "materiality_requires_semantic_reason": True,
                "forbidden_behaviors": ["NEON_FOR_DECORATION", "FAKE_CINEMATIC_RELIGHTING"],
            },
            "graphic_style_boundaries": {
                "desired_character": ["PROFESSIONAL", "MODERN", "COMMERCIAL", "PREMIUM_B2B"],
                "must_not_look_like": ["POWERPOINT_SLIDE", "GENERIC_SAAS_TEMPLATE", "AI_ART_DEMO", "ABSTRACT_3D_POSTER"],
            },
            "anti_failure_rules": {
                "abstract_geometry_without_commercial_meaning": "REJECT",
                "decorative_form_substituted_for_ad_idea": "REJECT",
                "raw_generated_image_used_as_concept": "REJECT",
                "presentation_slide_composition": "REJECT",
                "generic_saas_template": "REVIEW_REQUIRED",
                "generic_3d_object": "REJECT",
                "cta_appended_after_layout": "REJECT",
                "brand_missing": "REJECT",
                "commercial_job_not_understood_at_first_glance": "REJECT",
                "requires_long_rationale_to_understand_visual": "REJECT",
                "visual_novelty_replacing_clarity": "REJECT",
            },
            "concept_generation_rules": {
                "user_brief_approval_required_before_render": True,
                "first_round_mode": "EXPLORE_3",
                "concept_count": 3,
                "representative_size": "300x250",
                "all_concepts_same_commercial_job": True,
                "material_difference_required": True,
                "minimum_distinct_design_axes": 3,
                "concepts_should_differ_by_advertising_logic": True,
                "hero_generation_is_optional": True,
                "hero_generation_must_not_be_first_default_step": True,
                "raw_generated_asset_is_never_visual_concept": True,
                "complete_banner_composite_required": True,
                "user_facing_artifact_role": "BANNER_COMPOSITE",
            },
            "concept_quality_bar": {
                "required_status": "PRESENTATION_READY_DESIGN",
                "checks": [
                    "COMMERCIAL_JOB_FIDELITY", "FIRST_GLANCE_CLARITY", "ADVERTISING_IMPACT",
                    "COMPOSITIONAL_CONFIDENCE", "TYPOGRAPHIC_CRAFT", "VISUAL_POLISH",
                    "CATEGORY_PREMIUM_BAR", "NON_GENERIC_IDENTITY", "CTA_INTEGRATION",
                    "BRAND_INTEGRATION", "HERO_SEMANTIC_RELEVANCE", "AD_NOT_PRESENTATION_SLIDE",
                    "SMALL_FORMAT_VIABILITY"
                ],
                "user_must_not_be_first_basic_qa": True,
            },
            "deliverable_scope": {"brief_stage_output": "NO_IMAGES", "full_pack_before_visual_approval": False},
        }

    def test_valid_brief_blocks_render_until_user_decision(self):
        result = self.brief_mod.validate(self.commercial_job(), self.brief())
        self.assertEqual(result["status"], "GRAPHIC_BANNER_BRIEF_READY_FOR_USER_APPROVAL")
        self.assertFalse(result["render_allowed"])
        self.assertEqual(result["visual_exploration_count"], 3)

    def test_commercial_job_sha_mismatch_fails(self):
        brief = self.brief()
        brief["source_bindings"]["commercial_job_sha256"] = "0" * 64
        with self.assertRaises(self.brief_mod.GraphicBannerBriefError):
            self.brief_mod.validate(self.commercial_job(), brief)

    def test_abstract_geometry_rule_is_hard_reject(self):
        brief = self.brief()
        brief["anti_failure_rules"]["abstract_geometry_without_commercial_meaning"] = "REVIEW_REQUIRED"
        with self.assertRaises(self.brief_mod.GraphicBannerBriefError):
            self.brief_mod.validate(self.commercial_job(), brief)

    def test_hero_generation_cannot_be_default_first_step(self):
        brief = self.brief()
        brief["concept_generation_rules"]["hero_generation_must_not_be_first_default_step"] = False
        with self.assertRaises(self.brief_mod.GraphicBannerBriefError):
            self.brief_mod.validate(self.commercial_job(), brief)

    def test_locked_cta_must_match_message_architecture(self):
        brief = self.brief()
        brief["message_architecture"]["cta_message"] = "Оставить заявку"
        with self.assertRaises(self.brief_mod.GraphicBannerBriefError):
            self.brief_mod.validate(self.commercial_job(), brief)

    def test_user_approve_unlocks_visual_exploration_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "graphic-banner-brief.json"
            path.write_text(json.dumps(self.brief(), ensure_ascii=False, indent=2), encoding="utf-8")
            decision = {
                "brief_id": self.brief()["brief_id"],
                "brief_sha256": self.decision_mod.sha256_file(path),
                "decision": "APPROVE",
                "decided_by": "USER",
                "feedback": None,
            }
            result = self.decision_mod.validate(path, decision)
            self.assertEqual(result["status"], "GRAPHIC_BANNER_BRIEF_APPROVED")
            self.assertTrue(result["visual_exploration_allowed"])
            self.assertFalse(result["full_production_allowed"])

    def test_non_user_cannot_approve_brief(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "graphic-banner-brief.json"
            path.write_text(json.dumps(self.brief(), ensure_ascii=False, indent=2), encoding="utf-8")
            decision = {
                "brief_id": self.brief()["brief_id"],
                "brief_sha256": self.decision_mod.sha256_file(path),
                "decision": "APPROVE",
                "decided_by": "CONTROLLER",
                "feedback": None,
            }
            with self.assertRaises(self.decision_mod.GraphicBannerBriefDecisionError):
                self.decision_mod.validate(path, decision)

    def test_stale_brief_sha_cannot_unlock_visual_exploration(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "graphic-banner-brief.json"
            path.write_text(json.dumps(self.brief(), ensure_ascii=False, indent=2), encoding="utf-8")
            decision = {
                "brief_id": self.brief()["brief_id"],
                "brief_sha256": "f" * 64,
                "decision": "APPROVE",
                "decided_by": "USER",
                "feedback": None,
            }
            with self.assertRaises(self.decision_mod.GraphicBannerBriefDecisionError):
                self.decision_mod.validate(path, decision)

    def test_revise_requires_feedback_and_keeps_render_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "graphic-banner-brief.json"
            path.write_text(json.dumps(self.brief(), ensure_ascii=False, indent=2), encoding="utf-8")
            decision = {
                "brief_id": self.brief()["brief_id"],
                "brief_sha256": self.decision_mod.sha256_file(path),
                "decision": "REVISE",
                "decided_by": "USER",
                "feedback": "Сделать коммерческую иерархию ещё проще.",
            }
            result = self.decision_mod.validate(path, decision)
            self.assertEqual(result["status"], "GRAPHIC_BANNER_BRIEF_REVISE_REQUESTED")
            self.assertFalse(result["visual_exploration_allowed"])


if __name__ == "__main__":
    unittest.main()
