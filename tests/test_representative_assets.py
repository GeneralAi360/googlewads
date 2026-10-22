import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_representative_assets.py"


def load_module():
    spec = importlib.util.spec_from_file_location("validate_representative_assets", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class RepresentativeAssetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_module()

    def brief(self):
        return {
            "design_brief_id": "DB-ASSET-01",
            "brand_identity_lock": {
                "brand_id": "brand",
                "display_name": "BRAND",
                "logo_asset_required": True,
                "alternate_names_allowed": [],
            },
            "required_assets": [
                {
                    "asset_id": "bitrix-ui",
                    "role": "PRODUCT_UI",
                    "required": True,
                    "generated_substitute_allowed": False,
                    "accepted_source_types": ["USER_PROVIDED", "OFFICIAL_PRODUCT"],
                    "min_width": 1200,
                    "min_height": 600,
                    "privacy_review_required": True,
                    "rights_approval_required": True,
                },
                {
                    "asset_id": "brand-logo",
                    "role": "LOGO",
                    "required": True,
                    "generated_substitute_allowed": False,
                    "accepted_source_types": ["USER_PROVIDED", "BRAND_OWNED"],
                    "min_width": None,
                    "min_height": None,
                    "privacy_review_required": False,
                    "rights_approval_required": True,
                },
            ],
        }

    def make_png(self, path: Path, size=(1400, 700)):
        Image.new("RGB", size, "white").save(path)

    def manifest(self, root: Path, brief):
        ui = root / "ui.png"
        logo = root / "logo.png"
        self.make_png(ui, (1400, 700))
        self.make_png(logo, (600, 180))
        return {
            "manifest_id": "AM-01",
            "design_brief_id": brief["design_brief_id"],
            "design_brief_sha256": self.module.canonical_sha(brief),
            "status": "ASSETS_READY",
            "assets": [
                {
                    "asset_id": "bitrix-ui",
                    "role": "PRODUCT_UI",
                    "required": True,
                    "source_type": "OFFICIAL_PRODUCT",
                    "path": ui.as_posix(),
                    "sha256": self.module.sha256_file(ui),
                    "width": 1400,
                    "height": 700,
                    "generated_substitute": False,
                    "privacy_checked": True,
                    "rights_status": "APPROVED",
                },
                {
                    "asset_id": "brand-logo",
                    "role": "LOGO",
                    "required": True,
                    "source_type": "BRAND_OWNED",
                    "path": logo.as_posix(),
                    "sha256": self.module.sha256_file(logo),
                    "width": 600,
                    "height": 180,
                    "generated_substitute": False,
                    "privacy_checked": True,
                    "rights_status": "APPROVED",
                },
            ],
        }

    def test_real_ui_and_brand_logo_allow_representative_render(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            brief = self.brief()
            result = self.module.validate_assets(brief, self.manifest(root, brief))
            self.assertEqual(result["status"], "ASSETS_READY")
            self.assertEqual(result["missing_asset_ids"], [])

    def test_missing_real_ui_returns_needs_asset(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            brief = self.brief()
            manifest = self.manifest(root, brief)
            manifest["assets"] = [item for item in manifest["assets"] if item["asset_id"] != "bitrix-ui"]
            result = self.module.validate_assets(brief, manifest)
            self.assertEqual(result["status"], "NEEDS_ASSET")
            self.assertIn("bitrix-ui", result["missing_asset_ids"])

    def test_generated_fake_ui_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            brief = self.brief()
            manifest = self.manifest(root, brief)
            ui = next(item for item in manifest["assets"] if item["asset_id"] == "bitrix-ui")
            ui["source_type"] = "GENERATED"
            ui["generated_substitute"] = True
            result = self.module.validate_assets(brief, manifest)
            self.assertEqual(result["status"], "NEEDS_ASSET")
            codes = {item["code"] for item in result["issues"]}
            self.assertTrue({"SOURCE_NOT_APPROVED", "GENERATED_SUBSTITUTE_FORBIDDEN"} & codes)

    def test_low_resolution_ui_is_rejected_from_actual_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            brief = self.brief()
            manifest = self.manifest(root, brief)
            ui = next(item for item in manifest["assets"] if item["asset_id"] == "bitrix-ui")
            path = Path(ui["path"])
            self.make_png(path, (900, 500))
            ui["sha256"] = self.module.sha256_file(path)
            ui["width"] = 1400
            ui["height"] = 700
            result = self.module.validate_assets(brief, manifest)
            self.assertEqual(result["status"], "NEEDS_ASSET")
            self.assertIn("LOW_RESOLUTION", {item["code"] for item in result["issues"]})

    def test_privacy_and_rights_are_fail_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            brief = self.brief()
            manifest = self.manifest(root, brief)
            ui = next(item for item in manifest["assets"] if item["asset_id"] == "bitrix-ui")
            ui["privacy_checked"] = False
            result = self.module.validate_assets(brief, manifest)
            self.assertEqual(result["status"], "NEEDS_ASSET")
            self.assertIn("PRIVACY_NOT_CHECKED", {item["code"] for item in result["issues"]})


if __name__ == "__main__":
    unittest.main()
