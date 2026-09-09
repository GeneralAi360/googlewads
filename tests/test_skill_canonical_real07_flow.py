import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"


class CanonicalSkillReal07FlowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = SKILL.read_text(encoding="utf-8")

    def test_exact_commercial_job_precedes_market_and_visual_strategy(self):
        text = self.text
        commercial = text.index("# Phase 1 — Exact campaign commercial-job lock")
        research = text.index("# Phase 5 — Competitive Creative Intelligence")
        idea = text.index("# Phase 7 — IDEA_ARCHITECTURE")
        self.assertLess(commercial, research)
        self.assertLess(commercial, idea)
        self.assertIn("Product identity, commercial job, campaign objective and CTA are separate facts.", text)

    def test_raw_hero_is_explicitly_not_user_facing_banner(self):
        text = self.text
        self.assertIn("HERO_ASSET_CANDIDATE", text)
        self.assertIn("artifact_role = BANNER_COMPOSITE", text)
        self.assertIn("raw_generated_asset_is_final_artifact=false", text)
        self.assertIn("Generation is optional and must not stall the run", text)
        self.assertIn("It is **not** a visual concept by itself.", text)
        self.assertIn("A raw hero gallery, generated 3D object, UI screenshot or written rationale does not count.", text)
        self.assertIn("Generated hero is a component candidate, not the user-facing banner.", text)

    def test_first_round_requires_explore3_and_two_fresh_reviews(self):
        text = self.text
        self.assertIn("# Phase 15 — Decide first-round visual exploration mode", text)
        self.assertIn("## `EXPLORE_3`", text)
        self.assertIn("exactly **two fresh `ART_DIRECTOR_REVIEWER` reports**", text)
        self.assertIn("prior_review_verdict_visible=false", text)
        self.assertIn("PRESENTATION_READY_DESIGN", text)
        self.assertIn("SELECT A", text)
        self.assertIn("SELECT B", text)
        self.assertIn("SELECT C", text)

    def test_new_real07_references_are_in_loading_map(self):
        text = self.text
        self.assertIn("references/concept-composite-and-pre-show-quality.md", text)
        self.assertIn("schemas/pre-show-visual-review.schema.json", text)
        self.assertIn("scripts/validate_visual_concept_preview.py", text)
        self.assertIn("scripts/validate_visual_concept_set.py", text)
        self.assertIn("evals/real-world-failure-real07.json", text)


if __name__ == "__main__":
    unittest.main()
