import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class SchemaAlignmentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.materializer = load_module(ROOT / "scripts" / "materialize_banner_jobs.py", "materialize_banner_jobs")
        cls.freeze = load_module(ROOT / "scripts" / "freeze_creative_contracts.py", "freeze_creative_contracts")
        cls.apply = load_module(ROOT / "scripts" / "apply_creative_contracts.py", "apply_creative_contracts")
        cls.schema = json.loads((ROOT / "schemas" / "banner-render-spec.schema.json").read_text(encoding="utf-8"))

    def test_creative_binding_provenance_keys_are_schema_allowed(self):
        matrix = {
            "run_id": "schema-demo",
            "expected_output_files": 1,
            "banner_matrix": [{
                "job_id": "C01-S300x250-V01-Lru",
                "concept_id": "C01",
                "variant_id": "V01",
                "language": "ru",
                "width": 300,
                "height": 250,
                "dimension": "300x250",
                "layout_family": "rectangle",
                "output_path": "outputs/demo.png",
                "output_format": "png"
            }]
        }
        contract = {
            "concept_id": "C01",
            "status": "APPROVED",
            "angle": "offer-led",
            "primary_proposition": "Verified proposition",
            "supporting_proof": None,
            "visual_idea": "Product hero",
            "primary_aoi": "product",
            "scan_path": ["product", "headline", "cta"],
            "brand_id": "brand-demo",
            "reference_dna_ids": [],
            "lighting": {"lighting_scheme_id": None, "scene_directive": None, "composition_directive": None},
            "source_grounding": [{"source_id": "source-1", "supports": "proposition"}],
            "variants": [{
                "variant_id": "V01",
                "test_hypothesis": "baseline",
                "visual_direction_override": None,
                "copy_by_language": {"ru": {"headline": "Заголовок", "support": None, "offer": None, "cta": "CTA"}}
            }]
        }
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            contracts = root / "contracts"
            contracts.mkdir()
            (contracts / "C01.creative.json").write_text(json.dumps(contract, ensure_ascii=False), encoding="utf-8")
            creative_freeze = self.freeze.freeze_contracts(matrix, contracts, root / "creative-freeze.json")
            jobs = root / "jobs"
            self.materializer.materialize(matrix, jobs)
            self.apply.apply(matrix, creative_freeze, contracts, jobs / "render-specs")
            spec = json.loads((jobs / "render-specs" / "C01-S300x250-V01-Lru.json").read_text(encoding="utf-8"))

        allowed = set(self.schema["properties"]["provenance"]["properties"])
        actual = set(spec["provenance"])
        self.assertTrue(actual <= allowed, f"runtime provenance fields not allowed by schema: {sorted(actual - allowed)}")
        self.assertIn("creative_contract_path", actual)
        self.assertIn("creative_contract_sha256", actual)

    def test_creative_contract_sha_schema_requires_64_hex_when_non_null(self):
        sha_schema = self.schema["properties"]["provenance"]["properties"]["creative_contract_sha256"]
        self.assertIn("string", sha_schema["type"])
        self.assertEqual(sha_schema["pattern"], "^[0-9a-f]{64}$")


if __name__ == "__main__":
    unittest.main()
