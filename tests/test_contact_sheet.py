import importlib.util
import tempfile
import unittest
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "build_contact_sheet.py"


def load_module():
    spec = importlib.util.spec_from_file_location("build_contact_sheet", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class ContactSheetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_module()

    def test_builds_review_sheet_for_mixed_banner_sizes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            files = []
            for name, size, color in [
                ("a.png", (300, 250), "red"),
                ("b.png", (728, 90), "blue"),
                ("c.png", (160, 600), "green"),
            ]:
                path = root / name
                Image.new("RGB", size, color).save(path)
                files.append(path)
            out = root / "contact-sheet.png"
            result = self.module.build_contact_sheet(files, out, columns=2, cell_width=320, cell_height=240)
            self.assertEqual(result, out)
            self.assertTrue(out.is_file())
            with Image.open(out) as image:
                self.assertEqual(image.format, "PNG")
                self.assertGreater(image.width, 640)
                self.assertGreater(image.height, 500)

    def test_rejects_empty_file_list(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                self.module.build_contact_sheet([], Path(tmp) / "empty.png")


if __name__ == "__main__":
    unittest.main()
