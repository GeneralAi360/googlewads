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
        cls.creative_schema = json.loads((ROOT / "schemas" / "creative-contract.schema.json").read_text(encoding="utf-8"))
        cls.output_schema = json.loads((ROOT / "schemas" / "output-manifest.schema.json").read_text(encoding="utf-8"))
        cls.banner_review_schema = json.loads((ROOT / "schemas" / "banner-review.schema.json").read_text(encoding="utf-8"))
        cls.pack_review_schema = json.loads((ROOT / "schemas" / "pack-review.schema.json").read_text(encoding="utf-8"))

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
            "art_direction": {
                "mode": "ART_DIRECTION_LOCKED",
                "art_direction_id": "AD-C01-LOCKED",
                "visual_thesis": "Product-led restrained grid",
                "selection_provenance": "BRAND_LOCKED",
                "representative_preview_id": None,
                "selected_from_candidate_ids": [],
                "alignment_logic": "copy left, hero right",
                "graphic_device": "product hero",
                "image_treatment": "clean commercial",
                "whitespace_character": "restrained",
                "anti_template_exclusions": [],
            },
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
        self.assertEqual(spec["provenance"]["art_direction_id"], "AD-C01-LOCKED")

    def test_creative_contract_sha_schema_requires_64_hex_when_non_null(self):
        sha_schema = self.schema["properties"]["provenance"]["properties"]["creative_contract_sha256"]
        self.assertIn("string", sha_schema["type"])
        self.assertEqual(sha_schema["pattern"], "^[0-9a-f]{64}$")

    def test_art_direction_is_required_and_provenance_fields_are_schema_allowed(self):
        self.assertIn("art_direction", self.creative_schema["required"])
        self.assertIn("art_direction_id", self.schema["properties"]["provenance"]["properties"])
        manifest_props = self.output_schema["properties"]["files"]["items"]["properties"]
        self.assertIn("art_direction_id", manifest_props)

    def test_lighting_target_selector_schema_matches_renderer_runtime(self):
        defs = self.schema["$defs"]
        for name in ("heroGlow", "textPlate"):
            properties = defs[name]["properties"]
            self.assertIn("target_slot", properties)
            self.assertIn("target_slots", properties)
            self.assertIn("box", properties)

    def test_banner_review_schema_allows_design_diagnostic_checks(self):
        properties = self.banner_review_schema["properties"]["checks"]["properties"]
        for name in (
            "thumbnail_glance",
            "grayscale_hierarchy",
            "squint_hierarchy",
            "anti_template_generic_style",
        ):
            self.assertIn(name, properties)

    def test_pack_review_schema_allows_campaign_design_grammar_checks(self):
        properties = self.pack_review_schema["properties"]["checks"]["properties"]
        for name in (
            "campaign_design_grammar",
            "cross_size_lighting_consistency",
            "anti_template_generic_style",
        ):
            self.assertIn(name, properties)


if __name__ == "__main__":
    unittest.main()
