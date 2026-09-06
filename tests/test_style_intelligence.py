import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "recommend_visual_styles.py"
LIBRARY = ROOT / "config" / "style-intelligence-library.json"


def load_module():
    spec = importlib.util.spec_from_file_location("recommend_visual_styles", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class StyleIntelligenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_module()
        cls.library = json.loads(LIBRARY.read_text(encoding="utf-8"))

    def enterprise_context(self, **overrides):
        value = {
            "context_id": "STYLECTX-CRM-001",
            "category_tags": ["B2B", "ENTERPRISE_TECH", "SAAS"],
            "presentation_mode": "PRODUCT_PROOF",
            "primary_emotion": "CONTROL",
            "secondary_emotions": ["TRUST", "PRECISION"],
            "avoid_emotions": ["PLAYFULNESS", "HYPE"],
            "target_order_to_virality": 0.18,
            "target_aesthetics_to_innovation": 0.68,
            "disruption_level": "LOW",
            "hero_type": "PRODUCT_UI",
            "asset_truth_mode": "REAL_ASSET",
            "layout_families": ["rectangle", "leaderboard", "narrow_vertical", "micro_horizontal"],
            "language_scripts": ["CYRILLIC"],
            "brand_traits": ["ENTERPRISE", "PRECISE", "TRUST"],
            "avoid_tags": ["TOY", "FAKE_UI", "CYBERPUNK", "GENERIC_AI"],
            "category_cliches": ["GENERIC_SAAS_GRADIENT", "CLOUD_ICON"],
            "currentness_preference": "BALANCED",
            "typography_goal": "ENTERPRISE",
            "notes": "Synthetic enterprise-style selection regression",
        }
        value.update(overrides)
        return value

    def retail_context(self):
        return {
            "context_id": "STYLECTX-RETAIL-001",
            "category_tags": ["RETAIL", "EVENTS", "FASHION"],
            "presentation_mode": "PROMOTION_LED",
            "primary_emotion": "ENERGY",
            "secondary_emotions": ["CURIOSITY"],
            "avoid_emotions": [],
            "target_order_to_virality": 0.78,
            "target_aesthetics_to_innovation": 0.55,
            "disruption_level": "HIGH",
            "hero_type": "TYPOGRAPHY",
            "asset_truth_mode": "TYPE_ONLY",
            "layout_families": ["rectangle", "leaderboard", "micro_horizontal"],
            "language_scripts": ["CYRILLIC"],
            "brand_traits": ["BOLD", "YOUTH"],
            "avoid_tags": ["QUIET_LUXURY"],
            "category_cliches": [],
            "currentness_preference": "CURRENT",
            "typography_goal": "EXPRESSIVE",
            "notes": None,
        }

    def test_enterprise_real_ui_prefers_product_reality_or_swiss_as_safe(self):
        result = self.module.recommend(self.enterprise_context(), self.library)
        self.assertEqual(result["status"], "STYLE_STRATEGY_READY")
        safe = result["recommendations"][0]
        self.assertEqual(safe["lane"], "SAFE_STRONG")
        self.assertIn(
            safe["components"]["foundation_id"],
            {"FOUNDATION_PRODUCT_REALITY_SYSTEMS", "FOUNDATION_SWISS_COMMERCIAL"},
        )
        self.assertNotIn(safe["components"]["overlay_id"], {"OVERLAY_REALITY_WARP", "OVERLAY_RETRO_FUTURISM"})
        self.assertEqual(safe["components"]["attention_id"], "ATTENTION_PRODUCT_PROOF")

    def test_fake_or_generated_product_ui_is_penalized(self):
        result = self.module.recommend(
            self.enterprise_context(asset_truth_mode="GENERATED"),
            self.library,
        )
        ui_candidates = [
            item for item in result["recommendations"]
            if item["components"]["execution_id"] == "EXEC_UI_MACRO_CROP"
        ]
        self.assertTrue(ui_candidates)
        self.assertTrue(all(item["scores"]["asset_truth_fit"] <= 0.15 for item in ui_candidates))

    def test_three_lanes_use_distinct_foundations(self):
        result = self.module.recommend(self.enterprise_context(), self.library)
        recommendations = result["recommendations"]
        self.assertEqual([item["lane"] for item in recommendations], [
            "SAFE_STRONG",
            "CURRENT_DIFFERENTIATED",
            "CONTROLLED_WILDCARD",
        ])
        foundations = [item["components"]["foundation_id"] for item in recommendations]
        self.assertEqual(len(foundations), len(set(foundations)))

    def test_currentness_is_capped_and_never_claims_performance(self):
        result = self.module.recommend(self.enterprise_context(), self.library)
        self.assertLessEqual(result["policy"]["currentness_weight_cap"], 0.05)
        for item in result["recommendations"]:
            self.assertEqual(item["performance_claim"], "NO_PERFORMANCE_PREDICTION")
            self.assertGreaterEqual(item["score_total"], 0)
            self.assertLessEqual(item["score_total"], 1)

    def test_typography_recommendation_requires_runtime_verification(self):
        result = self.module.recommend(self.enterprise_context(), self.library)
        for item in result["recommendations"]:
            plan = item["typography_plan"]
            self.assertTrue(plan["profile_id"])
            self.assertIn("VERIFY", plan["candidate_status"])
            self.assertIsInstance(plan["candidate_examples"], list)

    def test_stale_library_disables_currentness(self):
        stale = copy.deepcopy(self.library)
        stale["snapshot_date"] = "2025-01-01"
        result = self.module.recommend(self.enterprise_context(), stale)
        self.assertEqual(result["currentness_status"], "STALE_CURRENTNESS_DISABLED")
        for item in result["recommendations"]:
            self.assertEqual(item["scores"]["currentness"], 0.0)
            self.assertIsNone(item["components"]["overlay_id"])

    def test_high_disruption_context_gets_materially_expressive_wildcard(self):
        result = self.module.recommend(self.retail_context(), self.library)
        safe, _, wildcard = result["recommendations"]
        foundations = {item["id"]: item for item in self.library["foundation_profiles"]}
        safe_axis = foundations[safe["components"]["foundation_id"]]["order_to_virality"]
        wildcard_axis = foundations[wildcard["components"]["foundation_id"]]["order_to_virality"]
        self.assertGreaterEqual(wildcard_axis, 0.45)
        self.assertNotEqual(safe["components"]["foundation_id"], wildcard["components"]["foundation_id"])


if __name__ == "__main__":
    unittest.main()
