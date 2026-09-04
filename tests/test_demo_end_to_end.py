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

    def test_intake_to_seven_format_demo_runs_through_real_google_preflight(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = self.module.run_demo(root)
            self.assertEqual(result["status"], "PASS")
            self.assertEqual(result["intake_status"], "READY_TO_FREEZE")
            self.assertEqual(result["expected_output_files"], 7)
            self.assertEqual(result["passed_output_files"], 7)
            self.assertEqual(result["failed_output_files"], 0)
            self.assertTrue((root / "freeze" / "run-freeze.json").is_file())
            self.assertTrue((root / "freeze" / "banner-matrix.json").is_file())
            self.assertTrue((root / "contact-sheet.png").is_file())
            self.assertTrue((root / "output-manifest.json").is_file())
            self.assertTrue((root / "pack-report.json").is_file())

            freeze = json.loads((root / "freeze" / "run-freeze.json").read_text(encoding="utf-8"))
            matrix = json.loads((root / "freeze" / "banner-matrix.json").read_text(encoding="utf-8"))
            manifest = json.loads((root / "output-manifest.json").read_text(encoding="utf-8"))
            dispatch = json.loads((root / "dispatch" / "dispatch-index.json").read_text(encoding="utf-8"))
            self.assertEqual(freeze["status"], "FROZEN")
            self.assertEqual(freeze["expected_output_files"], 7)
            self.assertEqual(len(matrix["banner_matrix"]), 7)
            self.assertEqual(len(manifest["files"]), 7)
            self.assertEqual(len(dispatch["jobs"]), 7)

            expected_sizes = {(row["width"], row["height"]) for row in matrix["banner_matrix"]}
            actual_sizes = set()
            for item in manifest["files"]:
                path = Path(item["path"])
                self.assertTrue(path.is_file())
                with Image.open(path) as image:
                    actual_sizes.add(image.size)
                self.assertEqual(item["status"], "PASS")
                self.assertRegex(item["sha256"], r"^[0-9a-f]{64}$")
            self.assertEqual(actual_sizes, expected_sizes)


if __name__ == "__main__":
    unittest.main()
