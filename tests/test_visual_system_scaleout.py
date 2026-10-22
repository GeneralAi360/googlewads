import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_visual_system_scaleout.py"


def load_module():
    spec = importlib.util.spec_from_file_location("validate_visual_system_scaleout", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class VisualSystemScaleoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_module()

    def fixtures(self, root: Path):
        preview = root / "preview.png"
        preview.write_bytes(b"approved-preview")
        production = root / "production.png"
        production.write_bytes(b"production-with-real-assets")
        preview_sha = self.module.sha256_file(preview)
        production_sha = self.module.sha256_file(production)

        decision = {
            "decision_id": "VCD-001",
            "visual_concept_id": "VC-001",
            "artifact_path": preview.as_posix(),
            "artifact_sha256": preview_sha,
            "approval_scope": "VISUAL_SYSTEM_WITH_ASSET_SLOTS",
            "decided_by": "USER",
            "decision": "APPROVE",
            "feedback": None,
            "next_action": "COLLECT_PRODUCTION_ASSETS_AND_MATERIALIZE",
        }
        fidelity = {
            "report_id": "VSF-001",
            "status": "PASS",
            "reviewed_by": "ART_DIRECTOR_REVIEWER",
            "visual_concept_id": "VC-001",
            "approved_preview_artifact_path": preview.as_posix(),
            "approved_preview_artifact_sha256": preview_sha,
            "production_artifact_path": production.as_posix(),
            "production_artifact_sha256": production_sha,
            "checks": {key: "PASS" for key in (
                "composition", "hierarchy", "typography", "palette", "cta_treatment", "brand_anchor",
                "asset_slot_geometry", "attention_path", "lighting_intent", "copy_fidelity",
                "no_new_claims", "no_new_visual_language",
            )},
            "asset_substitutions": [
                {
                    "asset_id": "ui",
                    "role": "PRODUCT_UI",
                    "from_preview_mode": "STRUCTURAL_PLACEHOLDER",
                    "production_asset_path": (root / "real-ui.png").as_posix(),
                    "production_asset_sha256": "a" * 64,
                }
            ],
        }
        checks = {key: "PASS" for key in (
            "idea_fidelity", "emotional_fidelity", "visual_character_fidelity", "lighting_intent_fidelity",
            "asset_quality", "professional_category_fit", "hierarchy", "typography", "brand_fidelity",
            "commercial_message_fidelity", "hero_crop", "lighting_contrast", "cta_clarity", "anti_generic_ai",
        )}
        representative = {
            "approval_id": "RDA-002",
            "status": "APPROVED",
            "approved_by": "SYSTEM_FIDELITY_GATE",
            "approval_scope": "APPROVED_VISUAL_SYSTEM_FIDELITY",
            "artifact_path": production.as_posix(),
            "artifact_sha256": production_sha,
            "user_visual_decision_id": "VCD-001",
            "user_visual_decision_sha256": self.module.canonical_sha(decision),
            "visual_system_fidelity_report_id": "VSF-001",
            "visual_system_fidelity_report_sha256": self.module.canonical_sha(fidelity),
            "quality_checks": checks,
        }
        readiness = {"status": "ASSETS_READY"}
        return decision, representative, fidelity, readiness, preview, production

    def test_user_approved_system_plus_fidelity_unlocks_scaleout(self):
        with tempfile.TemporaryDirectory() as tmp:
            decision, representative, fidelity, readiness, _, _ = self.fixtures(Path(tmp))
            result = self.module.validate(decision, representative, fidelity, readiness)
            self.assertEqual(result["status"], "VISUAL_CONCEPT_APPROVED_VIA_SYSTEM_FIDELITY")
            self.assertTrue(result["full_production_allowed"])
            self.assertFalse(result["user_reapproval_required"])

    def test_material_drift_requires_user_reapproval(self):
        with tempfile.TemporaryDirectory() as tmp:
            decision, representative, fidelity, readiness, _, _ = self.fixtures(Path(tmp))
            fidelity["status"] = "MATERIAL_DRIFT"
            with self.assertRaises(self.module.VisualSystemScaleoutError):
                self.module.validate(decision, representative, fidelity, readiness)

    def test_missing_real_assets_keeps_scaleout_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            decision, representative, fidelity, readiness, _, _ = self.fixtures(Path(tmp))
            readiness["status"] = "NEEDS_ASSET"
            with self.assertRaises(self.module.VisualSystemScaleoutError):
                self.module.validate(decision, representative, fidelity, readiness)

    def test_reviewer_without_user_approve_cannot_unlock(self):
        with tempfile.TemporaryDirectory() as tmp:
            decision, representative, fidelity, readiness, _, _ = self.fixtures(Path(tmp))
            decision["decided_by"] = "ART_DIRECTOR_REVIEWER"
            with self.assertRaises(self.module.VisualSystemScaleoutError):
                self.module.validate(decision, representative, fidelity, readiness)

    def test_changed_production_bytes_invalidate_fidelity(self):
        with tempfile.TemporaryDirectory() as tmp:
            decision, representative, fidelity, readiness, _, production = self.fixtures(Path(tmp))
            production.write_bytes(b"changed-after-fidelity")
            with self.assertRaises(self.module.VisualSystemScaleoutError):
                self.module.validate(decision, representative, fidelity, readiness)


if __name__ == "__main__":
    unittest.main()
