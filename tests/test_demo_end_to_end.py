import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "demo_end_to_end.py"


def load_module():
    spec = importlib.util.spec_from_file_location("demo_end_to_end", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class DemoEndToEndTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_module()

    def test_intake_to_seven_format_demo_reaches_independent_review_dispatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = self.module.run_demo(root)
            self.assertEqual(result["status"], "PASS")
            self.assertEqual(result["intake_status"], "READY_TO_FREEZE")
            self.assertEqual(result["preproduction_status"], "PREPRODUCTION_FROZEN")
            self.assertEqual(result["preproduction_research_rigor"], "FULL")
            self.assertRegex(result["creative_preproduction_sha256"], r"^[0-9a-f]{64}$")
            self.assertEqual(result["creative_binding_status"], "CREATIVE_BINDING_PASS")
            self.assertEqual(result["expected_output_files"], 7)
            self.assertEqual(result["passed_output_files"], 7)
            self.assertEqual(result["failed_output_files"], 0)
            self.assertEqual(result["expected_review_tasks"], 7)
            self.assertFalse(result["independent_review_reports_fabricated"])

            required = [
                root / "freeze" / "run-freeze.json",
                root / "freeze" / "banner-matrix.json",
                root / "preproduction" / "competitive-creative-research.json",
                root / "preproduction" / "category-design-map.json",
                root / "preproduction" / "design-brief.json",
                root / "preproduction" / "art-direction-approval.json",
                root / "preproduction" / "representative-design-approval.json",
                root / "preproduction" / "representative-300x250.png",
                root / "preproduction-freeze.json",
                root / "creative-freeze.json",
                root / "creative-bindings.json",
                root / "contact-sheet.png",
                root / "output-manifest.json",
                root / "design-qa" / "design-qa-index.json",
                root / "review" / "review-index.json",
                root / "review" / "pack-review-task.md",
                root / "pack-report.json",
            ]
            self.assertTrue(all(path.is_file() for path in required))
            self.assertFalse((root / "review" / "pack-review.json").exists())

            freeze = json.loads((root / "freeze" / "run-freeze.json").read_text(encoding="utf-8"))
            matrix = json.loads((root / "freeze" / "banner-matrix.json").read_text(encoding="utf-8"))
            preproduction = json.loads((root / "preproduction-freeze.json").read_text(encoding="utf-8"))
            creative_freeze = json.loads((root / "creative-freeze.json").read_text(encoding="utf-8"))
            manifest = json.loads((root / "output-manifest.json").read_text(encoding="utf-8"))
            dispatch = json.loads((root / "dispatch" / "dispatch-index.json").read_text(encoding="utf-8"))
            qa_index = json.loads((root / "design-qa" / "design-qa-index.json").read_text(encoding="utf-8"))
            review_index = json.loads((root / "review" / "review-index.json").read_text(encoding="utf-8"))

            self.assertEqual(freeze["status"], "FROZEN")
            self.assertEqual(freeze["expected_output_files"], 7)
            self.assertEqual(preproduction["status"], "PREPRODUCTION_FROZEN")
            self.assertEqual(preproduction["research_rigor"], "FULL")
            self.assertEqual(preproduction["selected_art_direction_id"], "AD-DEMO-CLEAN-PREMIUM")
            self.assertEqual(creative_freeze["status"], "CREATIVE_CONTRACTS_FROZEN")
            self.assertEqual(creative_freeze["contracts"][0]["art_direction_id"], "AD-DEMO-CLEAN-PREMIUM")
            self.assertEqual(creative_freeze["preproduction_freeze_id"], preproduction["freeze_id"])
            self.assertRegex(creative_freeze["preproduction_freeze_sha256"], r"^[0-9a-f]{64}$")
            self.assertEqual(len(matrix["banner_matrix"]), 7)
            self.assertEqual(len(manifest["files"]), 7)
            self.assertEqual(len(dispatch["jobs"]), 7)
            self.assertEqual(qa_index["expected_jobs"], 7)
            self.assertEqual(review_index["expected_banner_reviews"], 7)
            self.assertTrue(review_index["design_qa_attached"])

            first_spec = json.loads((root / "dispatch" / "render-specs" / f"{matrix['banner_matrix'][0]['job_id']}.json").read_text(encoding="utf-8"))
            self.assertEqual(first_spec["provenance"]["preproduction_freeze_sha256"], creative_freeze["preproduction_freeze_sha256"])

            expected_sizes = {(row["width"], row["height"]) for row in matrix["banner_matrix"]}
            actual_sizes = set()
            for item in manifest["files"]:
                path = Path(item["path"])
                self.assertTrue(path.is_file())
                with Image.open(path) as image:
                    actual_sizes.add(image.size)
                self.assertEqual(item["status"], "PASS")
                self.assertEqual(item["art_direction_id"], "AD-DEMO-CLEAN-PREMIUM")
                self.assertIn("art_direction_binding", item["checks"])
                self.assertRegex(item["sha256"], r"^[0-9a-f]{64}$")
                qa_job = next(job for job in qa_index["jobs"] if job["job_id"] == item["job_id"])
                self.assertEqual(qa_job["source_sha256"], item["sha256"])
                for view in ("grayscale", "squint", "thumbnail_board"):
                    self.assertTrue(Path(qa_job["views"][view]).is_file())
                review_job = next(job for job in review_index["banner_reviews"] if job["job_id"] == item["job_id"])
                self.assertTrue(review_job["design_qa_attached"])
                self.assertTrue(Path(review_job["task_path"]).is_file())
                self.assertFalse(Path(review_job["report_path"]).exists())
            self.assertEqual(actual_sizes, expected_sizes)


if __name__ == "__main__":
    unittest.main()
