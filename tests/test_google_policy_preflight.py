import importlib.util
import json
import tempfile
import unittest
from datetime import date
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_google_policy.py"
READY = ROOT / "scripts" / "assess_google_ready.py"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class GooglePolicyPreflightTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.validator = load_module(VALIDATOR, "validate_google_policy")
        cls.ready = load_module(READY, "assess_google_ready")

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.image = self.root / "banner.png"
        Image.new("RGB", (300, 250), "white").save(self.image)
        self.sha = self.validator.sha256_file(self.image)

    def tearDown(self):
        self.tmp.cleanup()

    def snapshot(self):
        return {
            "snapshot_date": date.today().isoformat(),
            "freshness": {
                "max_age_days_for_general_delivery": 45,
                "restricted_vertical_requires_live_refresh": True,
            },
        }

    def context(self):
        return {
            "policy_context_id": "POLCTX-001",
            "policy_snapshot_date": date.today().isoformat(),
            "campaign_mode": "uploaded_display_static",
            "target_countries": ["BY"],
            "creative": {
                "file_path": str(self.image),
                "file_sha256": self.sha,
                "width": 300,
                "height": 250,
                "format": "PNG",
                "animation_state": "STATIC",
            },
            "copy": {
                "headline": "Облачный Битрикс24",
                "support": None,
                "offer": "Бесплатная настройка при покупке лицензии",
                "cta": "Получить консультацию",
                "business_name": "MITGROUP",
                "legal_or_qualifier": "при покупке лицензии",
            },
            "business_identity": {
                "advertiser_name": "MITGROUP",
                "banner_business_name_matches": True,
                "affiliation_claimed": False,
                "affiliation_verified": False,
                "notes": None,
            },
            "claims": [],
            "destination": {
                "final_url": "https://example.test/bitrix24",
                "working": "PASS",
                "domain_match": "PASS",
                "google_adsbot_crawlable": "PASS",
                "target_geo_accessible": "PASS",
                "offer_easy_to_find": "PASS",
                "cta_action_available": "PASS",
                "advertiser_identity_matches": "PASS",
                "original_useful_content": "PASS",
            },
            "trademark_review": {
                "third_party_trademark_used": False,
                "trademarks": [],
                "status": "NOT_APPLICABLE",
                "basis": None,
            },
            "vertical_review": {
                "classification": "B2B_SOFTWARE_SERVICES",
                "restricted_or_sensitive": False,
                "status": "NOT_APPLICABLE",
                "certification_required": None,
                "certification_verified": None,
                "targeting_policy_status": "NOT_APPLICABLE",
                "notes": None,
            },
            "ai_asset_review": {
                "ai_generated_or_edited": False,
                "label_or_disclosure_review": "NOT_APPLICABLE",
                "notes": None,
            },
            "semantic_visual_review": {
                "reviewer_role": "GOOGLE_POLICY_REVIEWER",
                "independent_context": True,
                "reviewed_artifact_sha256": self.sha,
                "image_quality": "PASS",
                "essential_text_legible": "PASS",
                "fills_canvas": "PASS",
                "system_warning_or_dialog_mimic": "ABSENT",
                "nonfunctional_controls": "ABSENT",
                "download_install_ui": "ABSENT",
                "misleading_arrows_or_interactions": "ABSENT",
                "segmented_or_multi_ad_appearance": "ABSENT",
                "contextless_or_disproportionate_button": "ABSENT",
                "distracting_or_flashing": "ABSENT",
                "inappropriate_content": "ABSENT",
                "manipulated_media_deceptive": "ABSENT",
                "notes": None,
            },
        }

    def test_clean_banner_context_passes_without_approval_guarantee(self):
        result = self.validator.validate(self.context(), self.snapshot())
        self.assertEqual(result["status"], "GOOGLE_POLICY_PREFLIGHT_PASS")
        self.assertFalse(result["approval_guaranteed"])
        self.assertEqual(result["blockers"], [])

    def test_transparent_background_blocks_image_ad(self):
        rgba = Image.new("RGBA", (300, 250), (255, 255, 255, 255))
        rgba.putpixel((0, 0), (255, 255, 255, 0))
        rgba.save(self.image)
        ctx = self.context()
        ctx["creative"]["file_sha256"] = self.validator.sha256_file(self.image)
        ctx["semantic_visual_review"]["reviewed_artifact_sha256"] = ctx["creative"]["file_sha256"]
        result = self.validator.validate(ctx, self.snapshot())
        codes = {item["code"] for item in result["blockers"]}
        self.assertEqual(result["status"], "GOOGLE_POLICY_PREFLIGHT_BLOCKED")
        self.assertIn("MISLEADING_DESIGN_TRANSPARENT_BACKGROUND", codes)

    def test_fake_system_dialog_blocks(self):
        ctx = self.context()
        ctx["semantic_visual_review"]["system_warning_or_dialog_mimic"] = "PRESENT"
        result = self.validator.validate(ctx, self.snapshot())
        codes = {item["code"] for item in result["blockers"]}
        self.assertIn("POLICY_SYSTEM_WARNING_OR_DIALOG_MIMIC_PRESENT", codes)

    def test_unverified_material_claim_blocks(self):
        ctx = self.context()
        ctx["claims"] = [{
            "text": "Настройка бесплатно",
            "material": True,
            "verification_status": "UNVERIFIED",
            "source": None,
            "destination_support": "PASS",
            "offer_available": "PASS",
        }]
        result = self.validator.validate(ctx, self.snapshot())
        self.assertIn("UNVERIFIED_MATERIAL_CLAIM", {item["code"] for item in result["blockers"]})

    def test_unknown_destination_evidence_is_incomplete(self):
        ctx = self.context()
        ctx["destination"]["google_adsbot_crawlable"] = "UNKNOWN"
        result = self.validator.validate(ctx, self.snapshot())
        self.assertEqual(result["status"], "GOOGLE_POLICY_PREFLIGHT_INCOMPLETE")
        self.assertEqual(result["policy_scopes"]["destination_policy"], "INCOMPLETE")

    def test_trademark_review_required_stops_local_clearance(self):
        ctx = self.context()
        ctx["trademark_review"] = {
            "third_party_trademark_used": True,
            "trademarks": ["Bitrix24"],
            "status": "REVIEW_REQUIRED",
            "basis": None,
        }
        result = self.validator.validate(ctx, self.snapshot())
        self.assertEqual(result["status"], "POLICY_REVIEW_REQUIRED")
        self.assertEqual(result["policy_scopes"]["trademark_policy"], "REVIEW_REQUIRED")

    def test_google_ready_requires_design_and_policy_pass(self):
        readiness = {"status": "READY", "completion_claim_allowed": True}
        policy = self.validator.validate(self.context(), self.snapshot())
        result = self.ready.assess(readiness, policy)
        self.assertEqual(result["status"], "GOOGLE_READY_PRECHECK_PASS")
        self.assertFalse(result["google_upload_approval_guaranteed"])

        policy["status"] = "GOOGLE_POLICY_PREFLIGHT_INCOMPLETE"
        blocked = self.ready.assess(readiness, policy)
        self.assertEqual(blocked["status"], "GOOGLE_READY_PRECHECK_BLOCKED")


if __name__ == "__main__":
    unittest.main()
