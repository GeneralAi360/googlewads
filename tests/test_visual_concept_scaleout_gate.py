import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_visual_concept_approval.py"


def load_module():
    spec = importlib.util.spec_from_file_location("validate_visual_concept_approval", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class VisualConceptScaleoutGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_module()

    def fixtures(self, root: Path):
        artifact = root / "visual-concept.png"
        artifact.write_bytes(b"approved-visual-bytes")
        sha = self.module.sha256_file(artifact)
        checks = {
            key: "PASS" for key in (
                "idea_fidelity", "emotional_fidelity", "visual_character_fidelity", "lighting_intent_fidelity",
                "asset_quality", "professional_category_fit", "hierarchy", "typography", "brand_fidelity",
                "commercial_message_fidelity", "hero_crop", "lighting_contrast", "cta_clarity", "anti_generic_ai",
            )
        }
        representative = {
            "approval_id": "RDA-001",
            "status": "APPROVED",
            "approved_by": "USER",
            "artifact_path": artifact.as_posix(),
            "artifact_sha256": sha,
            "quality_checks": checks,
        }
        decision = {
            "decision_id": "VCD-001",
            "visual_concept_id": "VC-001",
            "artifact_path": artifact.as_posix(),
            "artifact_sha256": sha,
            "decided_by": "USER",
            "decision": "APPROVE",
        }
        return representative, decision, artifact

    def test_exact_user_approve_unlocks_scaleout(self):
        with tempfile.TemporaryDirectory() as tmp:
            representative, decision, _ = self.fixtures(Path(tmp))
            result = self.module.validate(representative, decision)
            self.assertEqual(result["status"], "VISUAL_CONCEPT_APPROVED")
            self.assertTrue(result["campaign_design_system_freeze_allowed"])
            self.assertTrue(result["full_production_allowed"])

    def test_internal_reviewer_cannot_unlock_scaleout(self):
        with tempfile.TemporaryDirectory() as tmp:
            representative, decision, _ = self.fixtures(Path(tmp))
            representative["approved_by"] = "ART_DIRECTOR_REVIEWER"
            with self.assertRaises(self.module.VisualApprovalError):
                self.module.validate(representative, decision)

    def test_revise_cannot_unlock_scaleout(self):
        with tempfile.TemporaryDirectory() as tmp:
            representative, decision, _ = self.fixtures(Path(tmp))
            decision["decision"] = "REVISE"
            with self.assertRaises(self.module.VisualApprovalError):
                self.module.validate(representative, decision)

    def test_changed_bytes_invalidate_scaleout(self):
        with tempfile.TemporaryDirectory() as tmp:
            representative, decision, artifact = self.fixtures(Path(tmp))
            artifact.write_bytes(b"changed-after-user-approval")
            with self.assertRaises(self.module.VisualApprovalError):
                self.module.validate(representative, decision)

    def test_decision_for_different_artifact_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            representative, decision, _ = self.fixtures(root)
            other = root / "other.png"
            other.write_bytes(b"other-visual")
            decision["artifact_path"] = other.as_posix()
            decision["artifact_sha256"] = self.module.sha256_file(other)
            with self.assertRaises(self.module.VisualApprovalError):
                self.module.validate(representative, decision)


if __name__ == "__main__":
    unittest.main()
