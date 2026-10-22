import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "aggregate_google_policy_reports.py"


def load_module():
    spec = importlib.util.spec_from_file_location("aggregate_google_policy_reports", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class GooglePolicyPackTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_module()

    def manifest(self):
        return {
            "files": [
                {"job_id": "JOB-A", "sha256": "a" * 64},
                {"job_id": "JOB-B", "sha256": "b" * 64},
            ]
        }

    def write_report(self, root: Path, job_id: str, sha: str, status: str):
        (root / f"{job_id}.google-policy-report.json").write_text(
            json.dumps({
                "status": status,
                "creative_sha256": sha,
                "approval_guaranteed": False,
            }),
            encoding="utf-8",
        )

    def test_all_exact_policy_reports_pass_pack(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_report(root, "JOB-A", "a" * 64, "GOOGLE_POLICY_PREFLIGHT_PASS")
            self.write_report(root, "JOB-B", "b" * 64, "GOOGLE_POLICY_PREFLIGHT_PASS")
            result = self.module.aggregate(self.manifest(), root)
            self.assertEqual(result["status"], "GOOGLE_POLICY_PREFLIGHT_PASS")
            self.assertEqual(result["passed_reports"], 2)
            self.assertFalse(result["approval_guaranteed"])

    def test_stale_report_hash_blocks_pack_clearance(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_report(root, "JOB-A", "f" * 64, "GOOGLE_POLICY_PREFLIGHT_PASS")
            self.write_report(root, "JOB-B", "b" * 64, "GOOGLE_POLICY_PREFLIGHT_PASS")
            result = self.module.aggregate(self.manifest(), root)
            self.assertEqual(result["status"], "GOOGLE_POLICY_PREFLIGHT_INCOMPLETE")
            self.assertTrue(result["failed_reports"])

    def test_single_review_required_prevents_pack_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_report(root, "JOB-A", "a" * 64, "GOOGLE_POLICY_PREFLIGHT_PASS")
            self.write_report(root, "JOB-B", "b" * 64, "POLICY_REVIEW_REQUIRED")
            result = self.module.aggregate(self.manifest(), root)
            self.assertEqual(result["status"], "POLICY_REVIEW_REQUIRED")


if __name__ == "__main__":
    unittest.main()
