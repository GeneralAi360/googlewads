import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "business-brief.schema.json"


class BusinessBriefCommercialJobTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = json.loads(SCHEMA.read_text(encoding="utf-8"))

    def test_business_brief_allows_product_service_used_by_intake(self):
        props = self.schema["properties"]["business"]["properties"]
        self.assertIn("product_service", props)

    def test_campaign_allows_exact_commercial_job_used_by_intake(self):
        props = self.schema["properties"]["campaign"]["properties"]
        self.assertIn("commercial_job", props)
        allowed = set(props["commercial_job"]["enum"])
        for job in (
            "NEW_LICENSE_PURCHASE",
            "LICENSE_RENEWAL",
            "PURCHASE_OR_RENEWAL",
            "IMPLEMENTATION_SERVICE",
            "CONSULTATION",
            "OTHER",
        ):
            self.assertIn(job, allowed)


if __name__ == "__main__":
    unittest.main()
