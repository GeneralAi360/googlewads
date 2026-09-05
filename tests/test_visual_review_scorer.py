import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "score_visual_review_evals.py"
EVALS = ROOT / "evals" / "visual-review-evals.json"


def load_module():
    spec = importlib.util.spec_from_file_location("score_visual_review_evals", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def perfect_report(case):
    findings = []
    for item in case["expected_findings"]:
        findings.append(
            {
                "severity": item["severity"],
                "code": item["code"],
                "evidence": item["evidence"],
                "why_it_matters": "Visible hierarchy/legibility/brand issue.",
                "recommended_fix": item["recommended_fix"],
                "scope": case["scope"],
            }
        )
    return {"case_id": case["id"], "summary": "Artifact reviewed from visible evidence.", "findings": findings}


class VisualReviewScorerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_module()
        cls.evals = json.loads(EVALS.read_text(encoding="utf-8"))

    def write_reports(self, root: Path, mutator=None, omit=None):
        root.mkdir(parents=True, exist_ok=True)
        for case in self.evals["cases"]:
            if case["id"] == omit:
                continue
            report = perfect_report(case)
            if mutator:
                report = mutator(case, report)
            (root / f"{case['id']}.review.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    def test_perfect_reports_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            reports = Path(tmp)
            self.write_reports(reports)
            result = self.module.score_suite(self.evals, reports)
            self.assertEqual(result["status"], "PASS")
            self.assertEqual(result["critical_recall"], 1.0)
            self.assertEqual(result["important_recall"], 1.0)
            self.assertEqual(result["false_critical_count"], 0)
            self.assertEqual(result["prohibited_claim_count"], 0)

    def test_missing_report_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            reports = Path(tmp)
            self.write_reports(reports, omit="VR-03")
            result = self.module.score_suite(self.evals, reports)
            self.assertEqual(result["status"], "FAIL")
            self.assertEqual(result["missing_reports"], ["VR-03"])

    def test_missing_critical_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            reports = Path(tmp)
            def mutator(case, report):
                if case["id"] == "VR-01":
                    report["findings"] = []
                return report
            self.write_reports(reports, mutator=mutator)
            result = self.module.score_suite(self.evals, reports)
            self.assertEqual(result["status"], "FAIL")
            self.assertLess(result["critical_recall"], 1.0)

    def test_false_critical_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            reports = Path(tmp)
            def mutator(case, report):
                if case["id"] == "VR-02":
                    report["findings"].append({
                        "severity": "CRITICAL",
                        "code": "INVENTED_CRITICAL",
                        "evidence": "A visible but non-expected condition.",
                        "why_it_matters": "Overstated.",
                        "recommended_fix": "None.",
                        "scope": "single_banner",
                    })
                return report
            self.write_reports(reports, mutator=mutator)
            result = self.module.score_suite(self.evals, reports)
            self.assertEqual(result["status"], "FAIL")
            self.assertEqual(result["false_critical_count"], 1)

    def test_prohibited_claim_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            reports = Path(tmp)
            def mutator(case, report):
                if case["id"] == "VR-01":
                    report["summary"] = "CTR will be low because of this layout."
                return report
            self.write_reports(reports, mutator=mutator)
            result = self.module.score_suite(self.evals, reports)
            self.assertEqual(result["status"], "FAIL")
            self.assertGreater(result["prohibited_claim_count"], 0)

    def test_missing_evidence_is_rejected(self):
        case = self.evals["cases"][0]
        report = perfect_report(case)
        report["findings"][0]["evidence"] = ""
        with self.assertRaises(self.module.EvalScoreError):
            self.module.score_case(case, report)


if __name__ == "__main__":
    unittest.main()
