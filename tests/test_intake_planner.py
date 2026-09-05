import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "plan_banner_intake.py"


def load_module():
    spec = importlib.util.spec_from_file_location("plan_banner_intake", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class IntakePlannerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_module()

    def base_context(self):
        return {
            "formats": {"mode": "demand_gen_uploaded_display", "pack": "core"},
            "deliverables": {
                "concept_count": 2,
                "variant_count": 1,
                "languages": ["ru"],
                "output_format": "jpg",
            },
            "business": {
                "product_service": "Synthetic demo product",
                "geography": "Minsk",
            },
            "campaign": {
                "objective": "lead",
                "landing_page": "https://example.invalid",
                "funnel_stage": "product-aware",
                "primary_action": "request quote",
            },
            "audience": {"primary": "Homeowners"},
            "offer": {
                "primary_value_proposition": "Synthetic proposition",
                "price": None,
                "proof_points": [],
                "cta": "Request quote",
            },
            "constraints": {
                "legal_disclaimers": [],
                "prohibited_claims": [],
            },
            "brand": {
                "no_formal_system": True,
                "no_logo_asset": True,
                "allow_font_fallback": True,
                "allow_run_local_palette": True,
                "real_photos": [],
                "ai_hero_allowed": True,
                "people_faces_policy": "not required",
                "additional_rules": [],
                "prohibited_elements": [],
            },
            "visual": {
                "hero_subject": "product",
                "mood": "clean",
                "material_lighting": None,
                "lighting_style": None,
                "copy_safe_zone": "right",
                "effect_policy": "restrained",
            },
            "production": {
                "approval_step": False,
                "confidentiality_restrictions": None,
            },
        }

    def test_pool_has_exactly_52_unique_questions(self):
        pool = self.module.load_pool()
        ids = [item["id"] for item in pool["questions"]]
        self.assertEqual(len(ids), 52)
        self.assertEqual(len(set(ids)), 52)
        self.assertEqual(ids[0], "Q01")
        self.assertEqual(ids[-1], "Q52")

    def test_core_pack_output_math_and_contact_sheet_default(self):
        result = self.module.plan_intake(self.base_context(), depth="standard")
        self.assertEqual(result["output_math"]["size_count"], 7)
        self.assertEqual(result["output_math"]["total"], 14)
        self.assertIn(
            {"path": "deliverables.contact_sheet", "value": True, "question_id": "Q08"},
            result["defaulted_values"],
        )

    def test_count_phrase_without_semantics_is_explicit_ambiguity(self):
        context = self.base_context()
        context["deliverables"]["raw_banner_count_phrase"] = "10 banners in 7 sizes"
        result = self.module.plan_intake(context, depth="quick")
        self.assertEqual(result["status"], "OUTPUT_COUNT_AMBIGUOUS")
        question = next(item for item in result["questions"] if item["id"] == "Q06")
        self.assertEqual(question["state"], "MISSING")

    def test_count_phrase_with_semantics_resolves_q06(self):
        context = self.base_context()
        context["deliverables"]["raw_banner_count_phrase"] = "10 banners in 7 sizes"
        context["deliverables"]["count_semantics"] = "concepts_across_sizes"
        result = self.module.plan_intake(context)
        question = next(item for item in result["questions"] if item["id"] == "Q06")
        self.assertEqual(question["state"], "RESOLVED")

    def test_reference_and_performance_blocks_stay_conditional_when_unused(self):
        result = self.module.plan_intake(self.base_context())
        by_id = {item["id"]: item for item in result["questions"]}
        for qid in ["Q31", "Q32", "Q33", "Q34", "Q35", "Q36", "Q43", "Q44", "Q45", "Q46"]:
            self.assertEqual(by_id[qid]["state"], "CONDITIONAL")

    def test_multiple_references_activate_primary_reference_question(self):
        context = self.base_context()
        context["references"] = {
            "requested": True,
            "items": ["ref-a", "ref-b"],
            "liked_attributes": ["composition"],
            "disliked_attributes": [],
            "similarity_level": "principles",
            "mandatory_elements": [],
        }
        result = self.module.plan_intake(context)
        by_id = {item["id"]: item for item in result["questions"]}
        self.assertEqual(by_id["Q35"]["state"], "MISSING")
        context["references"]["primary_reference"] = "ref-a"
        result = self.module.plan_intake(context)
        by_id = {item["id"]: item for item in result["questions"]}
        self.assertEqual(by_id["Q35"]["state"], "RESOLVED")

    def test_quick_mode_caps_visible_questions_but_reports_remaining(self):
        result = self.module.plan_intake({}, depth="quick", quick_limit=3)
        self.assertEqual(len(result["next_questions"]), 3)
        self.assertGreater(result["remaining_unshown_production_questions"], 0)

    def test_explicit_null_and_empty_values_count_as_resolved(self):
        context = self.base_context()
        result = self.module.plan_intake(context)
        by_id = {item["id"]: item for item in result["questions"]}
        self.assertEqual(by_id["Q17"]["state"], "RESOLVED")
        self.assertEqual(by_id["Q18"]["state"], "RESOLVED")
        self.assertEqual(by_id["Q20"]["state"], "RESOLVED")


if __name__ == "__main__":
    unittest.main()
