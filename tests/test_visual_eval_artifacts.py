import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build_visual_eval_fixtures.py"


def load_module():
    spec = importlib.util.spec_from_file_location("build_visual_eval_fixtures", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class VisualEvalArtifactTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_module()

    def test_materializes_all_six_eval_cases(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = self.module.build(root)
            self.assertEqual(result["status"], "VISUAL_EVAL_FIXTURES_READY")
            self.assertEqual(set(result["cases"]), {f"VR-{i:02d}" for i in range(1, 7)})
            self.assertEqual(len(result["cases"]["VR-06"]), 4)
            for paths in result["cases"].values():
                for path in paths:
                    self.assertTrue(Path(path).is_file())

    def test_fixture_dimensions_match_eval_contract(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = self.module.build(root)
            expected_single = {
                "VR-01": (300, 250),
                "VR-02": (300, 250),
                "VR-03": (160, 600),
                "VR-04": (320, 50),
                "VR-05": (336, 280),
            }
            for case_id, size in expected_single.items():
                with Image.open(result["cases"][case_id][0]) as image:
                    self.assertEqual(image.size, size)
            expected_pack = {(300, 250), (728, 90), (160, 600), (320, 50)}
            actual_pack = set()
            for path in result["cases"]["VR-06"]:
                with Image.open(path) as image:
                    actual_pack.add(image.size)
            self.assertEqual(actual_pack, expected_pack)

    def test_fixture_manifest_labels_artifacts_as_intentionally_flawed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.module.build(root)
            manifest = json.loads((root / "visual-eval-fixtures.json").read_text(encoding="utf-8"))
            warning = manifest["warning"].lower()
            self.assertIn("intentionally flawed", warning)
            self.assertIn("not ad recommendations", warning)


if __name__ == "__main__":
    unittest.main()
