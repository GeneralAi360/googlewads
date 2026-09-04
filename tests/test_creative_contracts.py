import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FREEZE = ROOT / "scripts" / "freeze_creative_contracts.py"
APPLY = ROOT / "scripts" / "apply_creative_contracts.py"
VALIDATE = ROOT / "scripts" / "validate_creative_bindings.py"
MATERIALIZE = ROOT / "scripts" / "materialize_banner_jobs.py"


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class CreativeContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.freeze = load(FREEZE, "freeze_creative_contracts")
        cls.apply = load(APPLY, "apply_creative_contracts")
        cls.validate = load(VALIDATE, "validate_creative_bindings")
        cls.materializer = load(MATERIALIZE, "materialize_banner_jobs")

    def matrix(self):
        rows = []
        for size, width, height, family in [("300x250", 300, 250, "rectangle"), ("320x50", 320, 50, "micro_horizontal")]:
            rows.append({"job_id": f"C01-S{size}-V01-Lru", "concept_id": "C01", "variant_id": "V01", "language": "ru", "width": width, "height": height, "dimension": size, "layout_family": family, "output_path": f"outputs/{size}.png", "output_format": "png"})
        return {"run_id": "demo", "expected_output_files": 2, "banner_matrix": rows}

    def contract(self):
        return {
            "concept_id": "C01",
            "status": "APPROVED",
            "angle": "offer-led",
            "audience_state": "product-aware",
            "primary_proposition": "Verified demo proposition",
            "supporting_proof": None,
            "visual_idea": "Product hero with copy-safe zone",
            "primary_aoi": "product",
            "scan_path": ["product", "headline", "cta"],
            "brand_id": "brand-demo",
            "reference_dna_ids": ["REF-A"],
            "lighting": {"lighting_scheme_id": 1, "scene_directive": "soft directional", "composition_directive": "restrained"},
            "source_grounding": [{"source_id": "landing-page", "supports": "primary proposition"}],
            "variants": [{"variant_id": "V01", "test_hypothesis": "baseline", "visual_direction_override": None, "copy_by_language": {"ru": {"headline": "Кухни на заказ", "support": None, "offer": None, "cta": "Рассчитать"}}}]
        }

    def write_contract(self, root, value=None):
        contracts = root / "contracts"
        contracts.mkdir(exist_ok=True)
        path = contracts / "C01.creative.json"
        path.write_text(json.dumps(value or self.contract(), ensure_ascii=False, indent=2), encoding="utf-8")
        return contracts, path

    def test_freeze_requires_approved_contract_and_exact_matrix_axes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            contract = self.contract()
            contract["status"] = "DRAFT"
            contracts, _ = self.write_contract(root, contract)
            with self.assertRaises(self.freeze.CreativeFreezeError) as ctx:
                self.freeze.freeze_contracts(self.matrix(), contracts, root / "freeze.json")
            self.assertEqual(ctx.exception.code, "CREATIVE_NOT_APPROVED")

    def test_missing_matrix_language_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            contract = self.contract()
            contract["variants"][0]["copy_by_language"] = {"en": {"headline": "Kitchens", "support": None, "offer": None, "cta": "Quote"}}
            contracts, _ = self.write_contract(root, contract)
            with self.assertRaises(self.freeze.CreativeFreezeError) as ctx:
                self.freeze.freeze_contracts(self.matrix(), contracts, root / "freeze.json")
            self.assertEqual(ctx.exception.code, "CREATIVE_COPY_ERROR")

    def test_unvalidated_reference_id_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            contracts, _ = self.write_contract(root)
            reference_index = {"status": "REFERENCE_DNA_READY", "reports": [{"reference_id": "OTHER"}]}
            with self.assertRaises(self.freeze.CreativeFreezeError) as ctx:
                self.freeze.freeze_contracts(self.matrix(), contracts, root / "freeze.json", reference_index=reference_index)
            self.assertEqual(ctx.exception.code, "CREATIVE_REFERENCE_ERROR")

    def test_frozen_contract_applies_exact_copy_and_provenance_to_every_job(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            matrix = self.matrix()
            contracts, _ = self.write_contract(root)
            reference_index = {"status": "REFERENCE_DNA_READY", "reports": [{"reference_id": "REF-A"}]}
            creative_freeze = self.freeze.freeze_contracts(matrix, contracts, root / "creative-freeze.json", reference_index=reference_index)
            jobs = root / "jobs"
            self.materializer.materialize(matrix, jobs)
            result = self.apply.apply(matrix, creative_freeze, contracts, jobs / "render-specs", out_index=root / "bindings.json")
            self.assertEqual(result["status"], "CREATIVE_CONTRACTS_APPLIED")
            self.assertEqual(result["expected_jobs"], 2)
            for row in matrix["banner_matrix"]:
                spec = json.loads((jobs / "render-specs" / f"{row['job_id']}.json").read_text(encoding="utf-8"))
                self.assertEqual(spec["copy"]["headline"], "Кухни на заказ")
                self.assertEqual(spec["copy"]["cta"], "Рассчитать")
                self.assertEqual(spec["provenance"]["creative_contract_id"], "C01")
                self.assertRegex(spec["provenance"]["creative_contract_sha256"], r"^[0-9a-f]{64}$")
                self.assertEqual(spec["provenance"]["reference_dna_ids"], ["REF-A"])
                self.assertEqual(spec["provenance"]["source_grounding_ids"], ["landing-page"])

    def test_binding_validator_detects_worker_copy_mutation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            matrix = self.matrix()
            contracts, _ = self.write_contract(root)
            creative_freeze = self.freeze.freeze_contracts(matrix, contracts, root / "creative-freeze.json")
            jobs = root / "jobs"
            self.materializer.materialize(matrix, jobs)
            self.apply.apply(matrix, creative_freeze, contracts, jobs / "render-specs")
            first = jobs / "render-specs" / f"{matrix['banner_matrix'][0]['job_id']}.json"
            spec = json.loads(first.read_text(encoding="utf-8"))
            spec["copy"]["cta"] = "Worker changed CTA"
            first.write_text(json.dumps(spec, ensure_ascii=False), encoding="utf-8")
            result = self.validate.validate(matrix, creative_freeze, contracts, jobs / "render-specs")
            self.assertEqual(result["status"], "CREATIVE_BINDING_FAIL")
            self.assertIn("copy differs", result["failures"][0]["reason"])

    def test_untouched_bindings_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            matrix = self.matrix()
            contracts, _ = self.write_contract(root)
            creative_freeze = self.freeze.freeze_contracts(matrix, contracts, root / "creative-freeze.json")
            jobs = root / "jobs"
            self.materializer.materialize(matrix, jobs)
            self.apply.apply(matrix, creative_freeze, contracts, jobs / "render-specs")
            result = self.validate.validate(matrix, creative_freeze, contracts, jobs / "render-specs")
            self.assertEqual(result["status"], "CREATIVE_BINDING_PASS")
            self.assertEqual(result["passed_jobs"], 2)


if __name__ == "__main__":
    unittest.main()
