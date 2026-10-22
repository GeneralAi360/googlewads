import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class Real07CompositeQualityTests(unittest.TestCase):
    def test_real07_requires_banner_composite_and_exact_review(self):
        case = json.loads((ROOT / "evals" / "real-world-failure-real07.json").read_text(encoding="utf-8"))
        self.assertEqual(case["case_id"], "REAL-07")
        expected = set(case["expected_findings"])
        for code in (
            "RAW_HERO_ASSET_MISTAKEN_FOR_BANNER",
            "IMAGE_GENERATION_STALLED_BEFORE_COMPOSITE",
            "REVIEW_PASS_BEFORE_BANNER_COMPOSITE",
            "ART_DIRECTOR_REVIEW_FALSE_POSITIVE",
            "GENERIC_ABSTRACT_HERO_WITHOUT_COMMERCIAL_MEANING",
            "BANNER_COPY_CTA_BRAND_NOT_PRESENT_AT_REVIEW_TIME",
        ):
            self.assertIn(code, expected)
        regressions = "\n".join(case["required_regressions"])
        self.assertIn("HERO_ASSET_CANDIDATE", regressions)
        self.assertIn("BANNER_COMPOSITE", regressions)
        self.assertIn("exact dimensions", regressions)
        self.assertIn("two fresh reviewer contexts", regressions)
        self.assertIn("hero_semantic_relevance", regressions)
        self.assertIn("stalled or low-value image-generation", regressions)
        self.assertIn("do not predict CTR", case["performance_claim_policy"])

    def test_pre_show_review_schema_targets_exact_banner_composite(self):
        schema = json.loads((ROOT / "schemas" / "pre-show-visual-review.schema.json").read_text(encoding="utf-8"))
        self.assertEqual(schema["properties"]["artifact_role"]["const"], "BANNER_COMPOSITE")
        self.assertEqual(schema["properties"]["reviewed_by"]["const"], "ART_DIRECTOR_REVIEWER")
        required_checks = set(schema["properties"]["checks"]["required"])
        for name in (
            "banner_composite_complete",
            "hero_semantic_relevance",
            "advertising_impact",
            "typographic_craft",
            "visual_polish",
            "category_premium_bar",
            "non_generic_identity",
        ):
            self.assertIn(name, required_checks)


if __name__ == "__main__":
    unittest.main()
