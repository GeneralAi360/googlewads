import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_SCRIPT = ROOT / "scripts" / "build_visual_eval_fixtures.py"
MATERIALIZER_SCRIPT = ROOT / "scripts" / "materialize_visual_eval_jobs.py"


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class VisualEvalMaterializerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixtures = load(FIXTURE_SCRIPT, "visual_eval_fixtures_for_materializer")
        cls.materializer = load(MATERIALIZER_SCRIPT, "visual_eval_materializer")

    def test_creates_one_fresh_readonly_task_per_case(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fixture_root = root / "fixtures"
            fixture_manifest = self.fixtures.build(fixture_root)
            result = self.materializer.materialize(fixture_manifest, root / "dispatch")
            self.assertEqual(result["status"], "VISUAL_EVAL_TASKS_READY")
            self.assertEqual(result["task_count"], 6)
            self.assertTrue(result["hidden_key_not_materialized"])
            for task_info in result["tasks"]:
                task = json.loads(Path(task_info["task_path"]).read_text(encoding="utf-8"))
                self.assertEqual(task["role"], "DESIGN_REVIEWER")
                self.assertEqual(task["reviewer_context"], "fresh_read_only_visual")
                self.assertTrue(task["artifact_paths"])

    def test_tasks_do_not_contain_hidden_expected_finding_codes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fixture_manifest = self.fixtures.build(root / "fixtures")
            result = self.materializer.materialize(fixture_manifest, root / "dispatch")
            hidden = json.loads((ROOT / "evals" / "visual-review-evals.json").read_text(encoding="utf-8"))
            hidden_codes = {
                finding["code"]
                for case in hidden["cases"]
                for finding in case["expected_findings"]
            }
            for task_info in result["tasks"]:
                task_text = Path(task_info["task_path"]).read_text(encoding="utf-8")
                for code in hidden_codes:
                    self.assertNotIn(code, task_text)

    def test_refuses_to_overwrite_tasks_without_force(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fixture_manifest = self.fixtures.build(root / "fixtures")
            self.materializer.materialize(fixture_manifest, root / "dispatch")
            with self.assertRaises(self.materializer.VisualEvalMaterializeError):
                self.materializer.materialize(fixture_manifest, root / "dispatch")

    def test_force_allows_controller_rebuild(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fixture_manifest = self.fixtures.build(root / "fixtures")
            self.materializer.materialize(fixture_manifest, root / "dispatch")
            result = self.materializer.materialize(fixture_manifest, root / "dispatch", force=True)
            self.assertEqual(result["task_count"], 6)


if __name__ == "__main__":
    unittest.main()
