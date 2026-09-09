import importlib.util
import tempfile
import unittest
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_visual_concept_preview.py"


def load_module():
    spec = importlib.util.spec_from_file_location("validate_visual_concept_preview", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class VisualConceptPreviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_module()

    def preview(self, root: Path, *, surrogate=True):
        artifact = root / "concept-preview.png"
        Image.new("RGB", (300, 250), "white").save(artifact, "PNG")
        if surrogate:
            slots = [
                {
                    "asset_id": "ui",
                    "role": "PRODUCT_UI",
                    "preview_mode": "STRUCTURAL_PLACEHOLDER",
                    "production_ready": False,
                    "generated_fake_asset": False,
                    "source": None,
                    "notes": "Reserved real UI aperture; no fake dashboard details",
                },
                {
                    "asset_id": "logo",
                    "role": "LOGO",
                    "preview_mode": "LOW_RES_AUTHENTIC_SURROGATE",
                    "production_ready": False,
                    "generated_fake_asset": False,
                    "source": "existing-low-res-authentic-logo",
                    "notes": "Authentic logo only for concept read; production master still required",
                },
            ]
            scope = "VISUAL_SYSTEM_WITH_ASSET_SLOTS"
            readiness = "NEEDS_ASSET"
            not_for_delivery = True
        else:
            slots = [
                {
                    "asset_id": "ui",
                    "role": "PRODUCT_UI",
                    "preview_mode": "PRODUCTION_ASSET",
                    "production_ready": True,
                    "generated_fake_asset": False,
                    "source": "approved-ui.png",
                    "notes": "Production asset",
                }
            ]
            scope = "EXACT_PRODUCTION_ARTIFACT"
            readiness = "ASSETS_READY"
            not_for_delivery = False
        return {
            "visual_concept_id": "VC-001",
            "commercial_job_id": "CJ-001",
            "status": "VISUAL_CONCEPT_RENDERED",
            "artifact_role": "BANNER_COMPOSITE",
            "render_stage": "USER_FACING_CONCEPT_COMPOSITE",
            "artifact_path": artifact.as_posix(),
            "artifact_sha256": self.module.sha256_file(artifact),
            "width": 300,
            "height": 250,
            "approval_scope": scope,
            "composition_contract": {
                "composition_method": "IMAGE_GENERATION_PLUS_COMPOSITOR",
                "mandatory_visible_elements": {
                    "primary_message": "Битрикс24",
                    "commercial_job_cue": "Новая лицензия",
                    "cta": "Выбрать редакцию",
                    "brand_anchor": "MITGROUP",
                },
                "raw_generated_asset_paths": [(root / "raw-hero.png").as_posix()],
                "raw_generated_asset_is_final_artifact": False,
            },
            "concept_summary": {
                "core_idea": "real product proof inside a calm operational system",
                "commercial_angle": "purchase or renewal of the product license",
                "primary_aoi": "product UI aperture",
                "scan_path": ["headline", "UI aperture", "CTA", "brand"],
                "style_strategy": "Product Reality / Systems",
                "typography": "enterprise Cyrillic sans",
                "lighting": "restrained composition separation; no UI relighting",
                "adaptation_note": "micro formats collapse UI and preserve proposition/action/brand",
            },
            "asset_slots": slots,
            "production_asset_readiness": readiness,
            "not_for_delivery": not_for_delivery,
            "policy_note": "Concept-only surrogates cannot be uploaded as ads",
        }, artifact

    def test_missing_production_assets_do_not_block_rendered_concept_preview(self):
        with tempfile.TemporaryDirectory() as tmp:
            preview, _ = self.preview(Path(tmp), surrogate=True)
            result = self.module.validate(preview)
            self.assertEqual(result["status"], "VISUAL_CONCEPT_AWAITING_USER_APPROVAL")
            self.assertEqual(result["commercial_job_id"], "CJ-001")
            self.assertEqual(result["artifact_role"], "BANNER_COMPOSITE")
            self.assertEqual((result["width"], result["height"]), (300, 250))
            self.assertEqual(result["production_asset_readiness"], "NEEDS_ASSET")
            self.assertTrue(result["contains_nonproduction_surrogates"])
            self.assertTrue(result["user_can_approve_visual_system"])
            self.assertFalse(result["full_production_allowed"])

    def test_commercial_job_id_is_required(self):
        with tempfile.TemporaryDirectory() as tmp:
            preview, _ = self.preview(Path(tmp), surrogate=True)
            preview.pop("commercial_job_id")
            with self.assertRaises(self.module.VisualConceptPreviewError):
                self.module.validate(preview)

    def test_raw_generated_hero_cannot_be_final_visual_concept(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            preview, artifact = self.preview(root, surrogate=True)
            preview["composition_contract"]["raw_generated_asset_paths"] = [artifact.as_posix()]
            with self.assertRaises(self.module.VisualConceptPreviewError):
                self.module.validate(preview)

    def test_artifact_role_must_be_banner_composite(self):
        with tempfile.TemporaryDirectory() as tmp:
            preview, _ = self.preview(Path(tmp), surrogate=True)
            preview["artifact_role"] = "HERO_ASSET"
            with self.assertRaises(self.module.VisualConceptPreviewError):
                self.module.validate(preview)

    def test_declared_dimensions_must_match_actual_raster(self):
        with tempfile.TemporaryDirectory() as tmp:
            preview, _ = self.preview(Path(tmp), surrogate=True)
            preview["width"] = 512
            with self.assertRaises(self.module.VisualConceptPreviewError):
                self.module.validate(preview)

    def test_generated_fake_asset_is_forbidden_even_for_preview(self):
        with tempfile.TemporaryDirectory() as tmp:
            preview, _ = self.preview(Path(tmp), surrogate=True)
            preview["asset_slots"][0]["generated_fake_asset"] = True
            with self.assertRaises(self.module.VisualConceptPreviewError):
                self.module.validate(preview)

    def test_surrogate_preview_cannot_be_marked_delivery_ready(self):
        with tempfile.TemporaryDirectory() as tmp:
            preview, _ = self.preview(Path(tmp), surrogate=True)
            preview["not_for_delivery"] = False
            with self.assertRaises(self.module.VisualConceptPreviewError):
                self.module.validate(preview)

    def test_exact_production_preview_remains_supported(self):
        with tempfile.TemporaryDirectory() as tmp:
            preview, _ = self.preview(Path(tmp), surrogate=False)
            result = self.module.validate(preview)
            self.assertEqual(result["approval_scope"], "EXACT_PRODUCTION_ARTIFACT")
            self.assertEqual(result["production_asset_readiness"], "ASSETS_READY")
            self.assertFalse(result["contains_nonproduction_surrogates"])

    def test_stale_preview_bytes_fail_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            preview, artifact = self.preview(Path(tmp), surrogate=True)
            Image.new("RGB", (300, 250), "black").save(artifact, "PNG")
            with self.assertRaises(self.module.VisualConceptPreviewError):
                self.module.validate(preview)


if __name__ == "__main__":
    unittest.main()
