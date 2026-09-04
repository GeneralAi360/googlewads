import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class RealWorldFailureTests(unittest.TestCase):
    def test_real_01_requires_research_written_direction_and_representative_gate(self):
        data = json.loads((ROOT / "evals" / "real-world-failures.json").read_text(encoding="utf-8"))
        cases = {item["case_id"]: item for item in data["cases"]}
        case = cases["REAL-01"]
        expected = set(case["expected_findings"])
        for code in (
            "PREMATURE_RENDER_BEFORE_MARKET_RESEARCH",
            "ART_DIRECTIONS_NOT_MATERIALLY_DISTINCT",
            "GENERIC_AI_CLIPART",
            "ASSET_QUALITY_BELOW_PRODUCTION",
            "DESIGN_NOT_PROFESSIONAL_ENOUGH",
        ):
            self.assertIn(code, expected)
        regressions = "\n".join(case["required_regressions"])
        self.assertIn("written art direction", regressions)
        self.assertIn("high-fidelity representative design", regressions)
        self.assertIn("full pack scale-out", regressions)
        self.assertIn("Do not label", case["performance_claim_policy"])


if __name__ == "__main__":
    unittest.main()
