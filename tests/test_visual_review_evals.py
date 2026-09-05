import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVALS = ROOT / "evals" / "visual-review-evals.json"


class VisualReviewEvalContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(EVALS.read_text(encoding="utf-8"))

    def test_fixture_ids_are_unique_and_six_cases_exist(self):
        cases = self.data["cases"]
        ids = [case["id"] for case in cases]
        self.assertEqual(len(cases), 6)
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(ids, [f"VR-{index:02d}" for index in range(1, 7)])

    def test_expected_findings_have_evidence_and_smallest_fix(self):
        allowed = {"CRITICAL", "IMPORTANT", "MINOR"}
        for case in self.data["cases"]:
            self.assertTrue(case["expected_findings"], case["id"])
            for finding in case["expected_findings"]:
                self.assertIn(finding["severity"], allowed)
                self.assertTrue(finding["code"])
                self.assertTrue(finding["evidence"])
                self.assertTrue(finding["recommended_fix"])

    def test_expected_findings_are_hidden_from_reviewer(self):
        protocol = self.data["evaluation_protocol"]
        self.assertTrue(protocol["expected_findings_hidden_from_reviewer"])
        self.assertEqual(protocol["reviewer_context"], "fresh_read_only_visual")

    def test_scoring_requires_all_critical_and_no_false_critical(self):
        scoring = self.data["evaluation_protocol"]["scoring"]
        self.assertEqual(scoring["critical_expected_finding_recall"], 1.0)
        self.assertEqual(scoring["false_critical_findings_max"], 0)
        self.assertGreaterEqual(scoring["important_expected_finding_recall_min"], 0.8)
        self.assertTrue(scoring["must_reference_visible_evidence"])

    def test_cases_explicitly_block_performance_myth_claims(self):
        all_claims = [claim.lower() for case in self.data["cases"] for claim in case.get("must_not_claim", [])]
        joined = " ".join(all_claims)
        self.assertIn("ctr", joined)
        self.assertIn("fill percentage", joined)
        self.assertIn("brightest pixel", joined)


if __name__ == "__main__":
    unittest.main()
