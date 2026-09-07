import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_visual_concept_decision.py"
REP_SCHEMA = ROOT / "schemas" / "representative-design-approval.schema.json"
ART_SCHEMA = ROOT / "schemas" / "art-direction-approval.schema.json"


def load_module():
    spec = importlib.util.spec_from_file_location("validate_visual_concept_decision", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class VisualConceptApprovalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_module()

    def make_decision(self, root: Path, decision="APPROVE", decided_by="USER", feedback=None):
        artifact = root / "visual-concept-300x250.png"
        artifact.write_bytes(b"exact-visual-concept")
        payload = {
            "decision_id": "VCD-001",
            "visual_concept_id": "VC-300x250-001",
            "artifact_path": artifact.as_posix(),
            "artifact_sha256": self.module.sha256_file(artifact),
            "decided_by": decided_by,
            "decision": decision,
            "feedback": feedback,
            "decided_at": None,
            "next_action": {
                "APPROVE": "FREEZE_CAMPAIGN_DESIGN_SYSTEM",
                "REVISE": "RENDER_REVISED_VISUAL_CONCEPT",
                "REJECT": "RETURN_UPSTREAM",
            }[decision],
        }
        return payload, artifact

    def test_approve_unlocks_full_production(self):
        with tempfile.TemporaryDirectory() as tmp:
            payload, _ = self.make_decision(Path(tmp), "APPROVE")
            result = self.module.validate(payload)
            self.assertEqual(result["status"], "VISUAL_CONCEPT_APPROVED")
            self.assertTrue(result["full_production_allowed"])

    def test_revise_requires_feedback_and_keeps_scaleout_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            payload, _ = self.make_decision(Path(tmp), "REVISE", feedback="Make UI larger and CTA calmer")
            result = self.module.validate(payload)
            self.assertEqual(result["status"], "VISUAL_CONCEPT_REVISE_REQUESTED")
            self.assertFalse(result["full_production_allowed"])

    def test_reject_returns_upstream_and_keeps_scaleout_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            payload, _ = self.make_decision(Path(tmp), "REJECT", feedback="Visual direction is not acceptable")
            result = self.module.validate(payload)
            self.assertEqual(result["next_action"], "RETURN_UPSTREAM")
            self.assertFalse(result["full_production_allowed"])

    def test_non_user_cannot_approve_visual_concept(self):
        with tempfile.TemporaryDirectory() as tmp:
            payload, _ = self.make_decision(Path(tmp), "APPROVE", decided_by="ART_DIRECTOR_REVIEWER")
            with self.assertRaises(self.module.VisualConceptDecisionError):
                self.module.validate(payload)

    def test_stale_visual_bytes_invalidate_decision(self):
        with tempfile.TemporaryDirectory() as tmp:
            payload, artifact = self.make_decision(Path(tmp), "APPROVE")
            artifact.write_bytes(b"changed-after-user-review")
            with self.assertRaises(self.module.VisualConceptDecisionError):
                self.module.validate(payload)

    def test_representative_schema_requires_user_approval(self):
        schema = json.loads(REP_SCHEMA.read_text(encoding="utf-8"))
        self.assertEqual(schema["properties"]["approved_by"]["const"], "USER")
        self.assertIn("Visual Concept", schema["title"])

    def test_written_art_direction_is_not_user_visual_approval(self):
        schema = json.loads(ART_SCHEMA.read_text(encoding="utf-8"))
        allowed = set(schema["properties"]["approved_by"]["enum"])
        self.assertNotIn("USER", allowed)
        self.assertIn("Internal", schema["title"])


if __name__ == "__main__":
    unittest.main()
