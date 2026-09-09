import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_campaign_commercial_job.py"
SCHEMA = ROOT / "schemas" / "campaign-commercial-job.schema.json"


def load_module():
    spec = importlib.util.spec_from_file_location("validate_campaign_commercial_job", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class CampaignCommercialJobTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_module()

    def lock(self, job_type="PURCHASE_OR_RENEWAL", structure="SEPARATE_VARIANTS"):
        return {
            "commercial_job_id": "CJ-B24-LICENSE-001",
            "status": "COMMERCIAL_JOB_LOCKED",
            "product_or_service": "Bitrix24 license",
            "job_type": job_type,
            "purchase_renewal_structure": structure,
            "target_transaction": "purchase or renew a Bitrix24 license",
            "allowed_message_scope": ["license purchase", "license renewal"],
            "excluded_job_types": ["IMPLEMENTATION_SERVICE", "CONSULTATION"],
            "source_basis": "USER_EXPLICIT",
            "source_note": None,
            "change_requires_controller_reapproval": True,
        }

    def test_purchase_or_renewal_lock_passes(self):
        result = self.module.validate_lock(self.lock())
        self.assertEqual(result["status"], "COMMERCIAL_JOB_LOCK_PASS")
        self.assertEqual(result["job_type"], "PURCHASE_OR_RENEWAL")
        self.assertFalse(result["invalidate_downstream"])

    def test_purchase_or_renewal_requires_structure(self):
        lock = self.lock(structure="NOT_APPLICABLE")
        with self.assertRaises(self.module.CommercialJobError):
            self.module.validate_lock(lock)

    def test_noncombined_job_rejects_purchase_structure(self):
        lock = self.lock(job_type="IMPLEMENTATION_SERVICE", structure="SEPARATE_VARIANTS")
        lock["target_transaction"] = "implement Bitrix24"
        lock["allowed_message_scope"] = ["implementation service"]
        lock["excluded_job_types"] = ["NEW_LICENSE_PURCHASE", "LICENSE_RENEWAL"]
        with self.assertRaises(self.module.CommercialJobError):
            self.module.validate_lock(lock)

    def test_implementation_to_license_change_invalidates_downstream(self):
        previous = self.lock(job_type="IMPLEMENTATION_SERVICE", structure="NOT_APPLICABLE")
        previous["commercial_job_id"] = "CJ-B24-IMPLEMENT-OLD"
        previous["target_transaction"] = "implement Bitrix24"
        previous["allowed_message_scope"] = ["implementation service"]
        previous["excluded_job_types"] = ["NEW_LICENSE_PURCHASE", "LICENSE_RENEWAL", "PURCHASE_OR_RENEWAL"]
        current = self.lock()
        result = self.module.compare(previous, current)
        self.assertEqual(result["status"], "COMMERCIAL_JOB_CHANGED")
        self.assertTrue(result["invalidate_downstream"])
        self.assertIn("job_type", result["changed_fields"])
        self.assertIn("visual_concept_previews", result["invalidate_artifacts"])
        self.assertIn("campaign_design_system", result["invalidate_artifacts"])

    def test_current_job_cannot_be_excluded(self):
        lock = self.lock()
        lock["excluded_job_types"].append("PURCHASE_OR_RENEWAL")
        with self.assertRaises(self.module.CommercialJobError):
            self.module.validate_lock(lock)

    def test_schema_contains_distinct_license_and_implementation_jobs(self):
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        values = set(schema["properties"]["job_type"]["enum"])
        self.assertIn("NEW_LICENSE_PURCHASE", values)
        self.assertIn("LICENSE_RENEWAL", values)
        self.assertIn("PURCHASE_OR_RENEWAL", values)
        self.assertIn("IMPLEMENTATION_SERVICE", values)


if __name__ == "__main__":
    unittest.main()
