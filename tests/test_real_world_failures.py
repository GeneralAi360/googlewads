import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class RealWorldFailureTests(unittest.TestCase):
    def load_cases(self):
        data = json.loads((ROOT / "evals" / "real-world-failures.json").read_text(encoding="utf-8"))
        return {item["case_id"]: item for item in data["cases"]}

    def test_real_01_requires_research_written_direction_and_representative_gate(self):
        case = self.load_cases()["REAL-01"]
        expected = set(case["expected_findings"])
        for code in (
            "PREMATURE_RENDER_BEFORE_MARKET_RESEARCH",
            "ART_DIRECTIONS_NOT_MATERIALLY_DISTINCT",
            "GENERIC_AI_CLIPART",
            "ASSET_QUALITY_BELOW_PRODUCTION",
            "DESIGN_NOT_PROFESSIONAL_ENOUGH",
        ):
            self.assertIn(code, expected)
        regressions = "\n".join(case["required_regressions"])
        self.assertIn("written art direction", regressions)
        self.assertIn("high-fidelity representative design", regressions)
        self.assertIn("full pack scale-out", regressions)
        self.assertIn("Do not label", case["performance_claim_policy"])

    def test_real_02_locks_commercial_brand_and_real_assets(self):
        case = self.load_cases()["REAL-02"]
        expected = set(case["expected_findings"])
        for code in (
            "COMMERCIAL_MESSAGE_DRIFT",
            "UNAPPROVED_CTA_INTRODUCED",
            "BRAND_IDENTITY_UNRESOLVED",
            "REAL_PRODUCT_ASSET_REQUIRED",
        ):
            self.assertIn(code, expected)
        regressions = "\n".join(case["required_regressions"])
        self.assertIn("allowlist of approved CTA", regressions)
        self.assertIn("canonical brand identity", regressions)
        self.assertIn("NEEDS_ASSET", regressions)
        self.assertIn("generated substitution disabled", regressions)
        self.assertIn("creative freeze must reject CTA", regressions)
        self.assertIn("DEGRADED research", case["performance_claim_policy"])

    def test_real_03_scopes_needs_asset_to_production_boundary(self):
        case = self.load_cases()["REAL-03"]
        expected = set(case["expected_findings"])
        for code in (
            "ASSET_GATE_APPLIED_TOO_EARLY",
            "UPSTREAM_STRATEGY_SKIPPED_BY_DOWNSTREAM_GATE",
            "IDEA_ARCHITECTURE_UNNECESSARILY_BLOCKED",
            "STYLE_INTELLIGENCE_UNNECESSARILY_BLOCKED",
            "LIGHTING_INTENT_UNNECESSARILY_BLOCKED",
            "RENDER_BLOCKER_SCOPE_TOO_BROAD",
        ):
            self.assertIn(code, expected)
        regressions = "\n".join(case["required_regressions"])
        self.assertIn("NEEDS_ASSET must block production representative rendering", regressions)
        self.assertIn("not IDEA_ARCHITECTURE", regressions)
        self.assertIn("Style Intelligence", regressions)
        self.assertIn("LIGHTING_INTENT", regressions)
        self.assertIn("STRATEGY_STATUS", regressions)
        self.assertIn("PRODUCTION_ASSET_READINESS", regressions)
        self.assertIn("orchestration order", case["performance_claim_policy"])

    def test_real_04_requires_user_approval_of_rendered_visual_concept(self):
        case = self.load_cases()["REAL-04"]
        expected = set(case["expected_findings"])
        for code in (
            "TEXT_ONLY_APPROVAL_INSUFFICIENT",
            "VISUAL_CONCEPT_MUST_BE_PRIMARY_APPROVAL_ARTIFACT",
            "USER_VISUAL_APPROVAL_REQUIRED_BEFORE_SCALEOUT",
            "REVISE_REQUIRES_NEW_VISUAL_VERSION",
            "REJECT_MUST_RETURN_UPSTREAM",
            "FULL_PACK_BLOCKED_BEFORE_VISUAL_APPROVAL",
        ):
            self.assertIn(code, expected)
        regressions = "\n".join(case["required_regressions"])
        self.assertIn("internal preproduction freeze", regressions)
        self.assertIn("rendered visual concept image", regressions)
        self.assertIn("user APPROVE", regressions)
        self.assertIn("REVISE", regressions)
        self.assertIn("REJECT", regressions)
        self.assertIn("changed approved preview bytes invalidate", regressions)
        self.assertIn("does not imply advertising performance", case["performance_claim_policy"])

    def test_real_05_requires_visible_concept_even_when_production_assets_are_missing(self):
        case = self.load_cases()["REAL-05"]
        expected = set(case["expected_findings"])
        for code in (
            "PRODUCTION_ASSET_GATE_HID_VISUAL_CONCEPT",
            "NO_RENDERED_CONCEPT_FOR_USER",
            "NO_USER_FACING_CONCEPT_CARD",
            "PRODUCTION_READINESS_CONFUSED_WITH_CONCEPT_VISIBILITY",
            "ASSET_SURROGATE_PATH_MISSING",
            "USER_CANNOT_APPROVE_WHAT_THEY_CANNOT_SEE",
        ):
            self.assertIn(code, expected)
        regressions = "\n".join(case["required_regressions"])
        self.assertIn("safe user-facing visual concept preview", regressions)
        self.assertIn("never generated fake UI or fake logos", regressions)
        self.assertIn("not_for_delivery", regressions)
        self.assertIn("short concept card", regressions)
        self.assertIn("visual system only", regressions)
        self.assertIn("material visual drift", regressions)
        self.assertIn("production UX controls", case["performance_claim_policy"])


if __name__ == "__main__":
    unittest.main()
