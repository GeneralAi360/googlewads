import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "render_banner_pack.py"


def load_module():
    spec = importlib.util.spec_from_file_location("render_banner_pack", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class PackBuilderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_module()
        renderer_spec = importlib.util.spec_from_file_location("renderer", ROOT / "scripts" / "render_banner.py")
        cls.renderer = importlib.util.module_from_spec(renderer_spec)
        assert renderer_spec.loader is not None
        renderer_spec.loader.exec_module(cls.renderer)
        cls.font = cls.renderer.resolve_font_path(None)

    def base_spec(self, job, width, height, family, output):
        return {
            "job_id": job,
            "width": width,
            "height": height,
            "layout_family": family,
            "background": {"color": "#FFFFFF"},
            "hero": None,
            "logo": {"brand_name": "BRAND"},
            "copy": {"headline": "Кухни на заказ", "support": None, "offer": None, "cta": "Рассчитать"},
            "brand": {
                "font_regular": self.font,
                "font_bold": self.font,
                "text_color": "#111111",
                "cta_fill": "#111111",
                "cta_text": "#FFFFFF",
            },
            "provenance": {
                "brand_id": "brand-demo",
                "creative_contract_id": None,
                "hero_asset_id": None,
                "reference_dna_ids": ["ref-01"],
                "source_grounding_ids": ["source-01"],
                "lighting_scheme_id": 1,
            },
            "output": {"path": str(output), "format": "png"},
        }

    def test_complete_matrix_returns_pack_pass_and_provenance_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            specs = root / "specs"
            specs.mkdir()
            outputs = root / "out"
            rows = []
            for job, width, height, family in [
                ("C01-S300x250-V01-Lru", 300, 250, "rectangle"),
                ("C01-S320x50-V01-Lru", 320, 50, "micro_horizontal"),
            ]:
                output = outputs / job / f"{job}.png"
                row = {
                    "job_id": job,
                    "concept_id": "C01",
                    "variant_id": "V01",
                    "language": "ru",
                    "width": width,
                    "height": height,
                    "dimension": f"{width}x{height}",
                    "layout_family": family,
                    "google_name": "Demo format",
                    "reference_dna_ids": ["ref-row"],
                    "lighting_scheme_id": 1,
                    "output_path": str(output),
                    "output_format": "png",
                }
                rows.append(row)
                spec = self.base_spec(job, width, height, family, output)
                if family == "micro_horizontal":
                    spec["copy"]["support"] = None
                    spec["copy"]["offer"] = None
                (specs / f"{job}.json").write_text(json.dumps(spec, ensure_ascii=False), encoding="utf-8")
            matrix = {
                "run_id": "demo",
                "brand_id": "brand-controller",
                "expected_output_files": 2,
                "banner_matrix": rows,
            }

            def validator(path, mode, pack):
                with Image.open(path) as image:
                    size = image.size
                return {"status": "PASS", "errors": [], "dimension": f"{size[0]}x{size[1]}"}

            result = self.module.render_pack(
                matrix,
                specs,
                contact_sheet=root / "sheet.png",
                manifest_path=root / "manifest.json",
                technical_validator=validator,
            )
            self.assertEqual(result["status"], "PASS")
            self.assertEqual(result["passed_output_files"], 2)
            self.assertTrue((root / "sheet.png").is_file())
            self.assertTrue((root / "manifest.json").is_file())
            self.assertRegex(result["manifest_sha256"], r"^[0-9a-f]{64}$")

            manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(len(manifest["files"]), 2)
            self.assertTrue(manifest["generated_at"].endswith("Z"))
            self.assertEqual(manifest["render_engine"], "pillow-deterministic-v0.2")
            self.assertRegex(manifest["matrix_sha256"], r"^[0-9a-f]{64}$")
            first = manifest["files"][0]
            self.assertRegex(first["sha256"], r"^[0-9a-f]{64}$")
            self.assertRegex(first["render_spec_sha256"], r"^[0-9a-f]{64}$")
            self.assertEqual(first["brand_id"], "brand-demo")
            self.assertIsNone(first["creative_contract_id"])
            self.assertEqual(first["lighting_scheme_id"], 1)
            self.assertEqual(first["reference_dna_ids"], ["ref-01", "ref-row"])
            self.assertEqual(first["source_grounding_ids"], ["source-01"])

    def test_real_google_validator_integrates_with_pack_runner_and_snapshot(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            specs = root / "specs"
            specs.mkdir()
            job = "C01-S300x250-V01-Lru"
            output = root / "out" / f"{job}.png"
            row = {
                "job_id": job,
                "concept_id": "C01",
                "variant_id": "V01",
                "language": "ru",
                "width": 300,
                "height": 250,
                "dimension": "300x250",
                "layout_family": "rectangle",
                "google_name": "Inline rectangle",
                "output_path": str(output),
                "output_format": "png",
            }
            (specs / f"{job}.json").write_text(
                json.dumps(self.base_spec(job, 300, 250, "rectangle", output), ensure_ascii=False),
                encoding="utf-8",
            )
            manifest_path = root / "manifest.json"
            result = self.module.render_pack(
                {"run_id": "integration", "expected_output_files": 1, "banner_matrix": [row]},
                specs,
                mode="demand_gen_uploaded_display",
                pack="core",
                manifest_path=manifest_path,
            )
            self.assertEqual(result["status"], "PASS")
            self.assertEqual(result["jobs"][0]["validation"]["status"], "PASS")
            config = self.module.load_script("validate_google_banner").load_config()
            self.assertEqual(result["google_spec_snapshot_date"], config["snapshot_date"])
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            self.assertEqual(manifest["spec_snapshot_date"], config["snapshot_date"])
            self.assertEqual(manifest["google_pack"], "core")

    def test_missing_spec_blocks_full_pack(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            specs = root / "specs"
            specs.mkdir()
            matrix = {
                "run_id": "demo",
                "expected_output_files": 1,
                "banner_matrix": [
                    {
                        "job_id": "missing",
                        "width": 300,
                        "height": 250,
                        "layout_family": "rectangle",
                        "output_path": str(root / "missing.png"),
                        "output_format": "png",
                    }
                ],
            }
            result = self.module.render_pack(
                matrix,
                specs,
                technical_validator=lambda *args: {"status": "PASS", "errors": []},
            )
            self.assertEqual(result["status"], "FAIL")
            self.assertEqual(result["failed_output_files"], 1)
            self.assertEqual(result["failures"][0]["job_id"], "missing")

    def test_failed_pack_does_not_emit_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            specs = root / "specs"
            specs.mkdir()
            manifest = root / "manifest.json"
            matrix = {
                "run_id": "demo",
                "expected_output_files": 1,
                "banner_matrix": [
                    {
                        "job_id": "missing",
                        "width": 300,
                        "height": 250,
                        "layout_family": "rectangle",
                        "output_path": str(root / "missing.png"),
                        "output_format": "png",
                    }
                ],
            }
            result = self.module.render_pack(
                matrix,
                specs,
                manifest_path=manifest,
                technical_validator=lambda *args: {"status": "PASS", "errors": []},
            )
            self.assertEqual(result["status"], "FAIL")
            self.assertFalse(manifest.exists())

    def test_spec_matrix_mismatch_fails_job(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            specs = root / "specs"
            specs.mkdir()
            job = "j"
            row = {
                "job_id": job,
                "width": 300,
                "height": 250,
                "layout_family": "rectangle",
                "output_path": str(root / "j.png"),
                "output_format": "png",
            }
            bad = self.base_spec(job, 336, 280, "rectangle", root / "x.png")
            (specs / "j.json").write_text(json.dumps(bad), encoding="utf-8")
            result = self.module.render_pack(
                {"expected_output_files": 1, "banner_matrix": [row]},
                specs,
                technical_validator=lambda *args: {"status": "PASS", "errors": []},
            )
            self.assertEqual(result["failures"][0]["code"], "FAIL_SPEC_MATRIX_MISMATCH")


if __name__ == "__main__":
    unittest.main()
