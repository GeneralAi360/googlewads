import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class Real08GraphicBannerBriefTests(unittest.TestCase):
    def test_real08_requires_user_approved_graphic_brief_before_render(self):
        case = json.loads((ROOT / "evals" / "real-world-failure-real08.json").read_text(encoding="utf-8"))
        self.assertEqual(case["case_id"], "REAL-08")
        findings = set(case["expected_findings"])
        for code in (
            "VISUAL_EXPLORATION_STARTED_BEFORE_USER_APPROVED_GRAPHIC_BRIEF",
            "ABSTRACT_GEOMETRY_USED_TO_FILL_UNSPECIFIED_DESIGN_PROBLEM",
            "DECORATIVE_FORM_SUBSTITUTED_FOR_ADVERTISING_IDEA",
            "HERO_GENERATION_BECAME_DEFAULT_DESIGN_STRATEGY",
        ):
            self.assertIn(code, findings)
        regressions = "\n".join(case["required_regressions"])
        self.assertIn("Graphic Banner Brief", regressions)
        self.assertIn("decided_by=USER", regressions)
        self.assertIn("hero generation is optional", regressions)
        self.assertIn("advertising logic", regressions)

    def test_commercial_job_reference_loads_graphic_brief_gate(self):
        text = (ROOT / "references" / "commercial-job-and-concept-exploration.md").read_text(encoding="utf-8")
        self.assertIn("GRAPHIC BANNER BRIEF", text.upper())
        self.assertIn("references/graphic-banner-brief.md", text)
        self.assertIn("validate_graphic_banner_brief.py", text)
        self.assertIn("validate_graphic_banner_brief_decision.py", text)
        self.assertIn("GRAPHIC_BANNER_BRIEF_APPROVED", text)
        self.assertIn("Do not render A/B/C at this point", text)

    def test_graphic_brief_reference_requires_two_distinct_user_decisions(self):
        text = (ROOT / "references" / "graphic-banner-brief.md").read_text(encoding="utf-8")
        self.assertIn("APPROVE BRIEF", text)
        self.assertIn("REVISE BRIEF", text)
        self.assertIn("Brief approval is **not** approval of any visual", text)
        self.assertIn("decided_by = USER", text)
        self.assertIn("visual_exploration_allowed=true", text)

    def test_schema_encodes_no_images_before_brief_approval(self):
        schema = json.loads((ROOT / "schemas" / "graphic-banner-brief.schema.json").read_text(encoding="utf-8"))
        required = set(schema["required"])
        for field in (
            "commercial_core",
            "message_architecture",
            "advertising_strategy",
            "anti_failure_rules",
            "concept_generation_rules",
            "concept_quality_bar",
            "deliverable_scope",
        ):
            self.assertIn(field, required)
        scope = schema["properties"]["deliverable_scope"]["properties"]
        self.assertEqual(scope["brief_stage_output"]["const"], "NO_IMAGES")
        generation = schema["properties"]["concept_generation_rules"]["properties"]
        self.assertEqual(generation["user_brief_approval_required_before_render"]["const"], True)
        self.assertEqual(generation["hero_generation_must_not_be_first_default_step"]["const"], True)
        self.assertEqual(generation["user_facing_artifact_role"]["const"], "BANNER_COMPOSITE")


if __name__ == "__main__":
    unittest.main()
