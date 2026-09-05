import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build_design_qa_views.py"


def load_module():
    spec = importlib.util.spec_from_file_location("build_design_qa_views", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class DesignQAViewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_module()

    def create_source(self, path: Path, size=(300, 250)) -> str:
        path.parent.mkdir(parents=True, exist_ok=True)
        image = Image.new("RGB", size, "#EFEFEF")
        image.save(path, "PNG")
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def test_builds_actual_grayscale_squint_and_thumbnail_views(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "banner.png"
            digest = self.create_source(source)
            manifest = {
                "campaign_id": "demo",
                "files": [
                    {
                        "job_id": "C01-S300x250-V01-Lru",
                        "path": source.as_posix(),
                        "sha256": digest,
                        "width": 300,
                        "height": 250,
                        "status": "PASS",
                    }
                ],
            }
            result = self.module.build_views(manifest, root / "qa")
            self.assertEqual(result["expected_jobs"], 1)
            item = result["jobs"][0]
            self.assertTrue(item["diagnostic_only"])
            self.assertEqual(item["thumbnail_preview_size"], [75, 62])
            for name in ("grayscale", "squint", "thumbnail_board"):
                self.assertTrue(Path(item["views"][name]).is_file())
            with Image.open(item["views"]["grayscale"]) as image:
                self.assertEqual(image.size, (300, 250))
            with Image.open(item["views"]["squint"]) as image:
                self.assertEqual(image.size, (300, 250))
            with Image.open(item["views"]["thumbnail_board"]) as image:
                self.assertEqual(image.size, (640, 360))
            self.assertTrue((root / "qa" / "design-qa-index.json").is_file())

    def test_hash_mismatch_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "banner.png"
            self.create_source(source)
            manifest = {
                "files": [
                    {
                        "job_id": "job",
                        "path": source.as_posix(),
                        "sha256": "0" * 64,
                        "width": 300,
                        "height": 250,
                        "status": "PASS",
                    }
                ]
            }
            with self.assertRaises(self.module.QAViewError) as ctx:
                self.module.build_views(manifest, root / "qa")
            self.assertIn("hash mismatch", str(ctx.exception))

    def test_nonpassing_manifest_item_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "banner.png"
            digest = self.create_source(source)
            manifest = {
                "files": [
                    {
                        "job_id": "job",
                        "path": source.as_posix(),
                        "sha256": digest,
                        "width": 300,
                        "height": 250,
                        "status": "FAIL",
                    }
                ]
            }
            with self.assertRaises(self.module.QAViewError):
                self.module.build_views(manifest, root / "qa")


if __name__ == "__main__":
    unittest.main()
