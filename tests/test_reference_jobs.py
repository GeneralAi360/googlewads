import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATERIALIZE = ROOT / "scripts" / "materialize_reference_jobs.py"
VALIDATE = ROOT / "scripts" / "validate_reference_analysis.py"


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class ReferenceJobsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.materializer = load(MATERIALIZE, "materialize_reference_jobs")
        cls.validator = load(VALIDATE, "validate_reference_analysis")

    def context(self):
        return {
            "references": {
                "requested": True,
                "items": [
                    {"reference_id": "REF-A", "source": "https://example.invalid/a"},
                    {"reference_id": "REF-B", "source": "uploads/reference-b.png"}
                ],
                "liked_attributes": ["composition", "lighting"],
                "disliked_attributes": ["tiny copy"],
                "similarity_level": "design principles",
                "primary_reference": "REF-A",
                "mandatory_elements": []
            }
        }

    def report(self, ref_id, source, independent=True):
        return {
            "reference_id": ref_id,
            "source": source,
            "analyst_role": "REFERENCE_ANALYST",
            "independent_context": independent,
            "status": "PASS",
            "observations": {
                "composition_grid": "asymmetric",
                "focal_object_scan_path": "hero to offer",
                "typography": "large headline",
                "color_contrast": "high contrast",
                "whitespace_density": "moderate negative space",
                "cta_treatment": "compact",
                "subject_scale": "large hero",
                "lighting": "soft directional",
                "angle_crop": "three-quarter crop",
                "mood_brand_signals": "premium clean"
            },
            "user_preference_alignment": {"liked": ["composition"], "disliked": ["tiny copy"]},
            "transferable_principles": ["preserve one clear focal object"],
            "do_not_copy": ["brand logo", "literal headline"],
            "uncertainties": [],
            "summary": "fixture"
        }

    def test_one_task_per_reference_without_report_precreation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = self.materializer.materialize(self.context(), root)
            self.assertEqual(result["status"], "READY_FOR_REFERENCE_ANALYSIS")
            self.assertEqual(result["expected_reference_jobs"], 2)
            self.assertEqual(len(result["jobs"]), 2)
            for job in result["jobs"]:
                self.assertTrue(Path(job["task_path"]).is_file())
                self.assertFalse(Path(job["report_path"]).exists())

    def test_no_references_is_not_applicable(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = self.materializer.materialize({}, Path(tmp))
            self.assertEqual(result["status"], "REFERENCE_NOT_APPLICABLE")
            self.assertEqual(result["expected_reference_jobs"], 0)

    def test_duplicate_reference_ids_fail(self):
        context = {"references": {"items": [{"id": "A", "source": "one"}, {"id": "A", "source": "two"}]}}
        with self.assertRaises(self.materializer.ReferenceJobError):
            self.materializer.normalize_items(context)

    def test_complete_independent_reports_become_reference_dna_ready(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            reports = root / "reports"
            reports.mkdir()
            for item in self.materializer.normalize_items(self.context()):
                path = reports / f"{item['reference_id']}.reference-dna.json"
                path.write_text(json.dumps(self.report(item["reference_id"], item["source"])), encoding="utf-8")
            result = self.validator.validate(self.context(), reports)
            self.assertEqual(result["status"], "REFERENCE_DNA_READY")
            self.assertEqual(result["passed"], 2)
            self.assertEqual(result["run_rigor"], "FULL")
            self.assertRegex(result["reports"][0]["sha256"], r"^[0-9a-f]{64}$")

    def test_source_mismatch_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            reports = root / "reports"
            reports.mkdir()
            first = self.materializer.normalize_items(self.context())[0]
            bad = self.report(first["reference_id"], "wrong-source")
            (reports / f"{first['reference_id']}.reference-dna.json").write_text(json.dumps(bad), encoding="utf-8")
            result = self.validator.validate({"references": {"items": [first]}}, reports)
            self.assertEqual(result["status"], "REFERENCE_ANALYSIS_INCOMPLETE")
            self.assertIn("source mismatch", result["failures"][0]["reason"])

    def test_non_independent_analysis_is_degraded_and_blocked_by_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            reports = root / "reports"
            reports.mkdir()
            first = self.materializer.normalize_items(self.context())[0]
            (reports / f"{first['reference_id']}.reference-dna.json").write_text(json.dumps(self.report(first["reference_id"], first["source"], independent=False)), encoding="utf-8")
            result = self.validator.validate({"references": {"items": [first]}}, reports)
            self.assertEqual(result["status"], "REFERENCE_ANALYSIS_INCOMPLETE")
            self.assertEqual(result["run_rigor"], "DEGRADED")


if __name__ == "__main__":
    unittest.main()
