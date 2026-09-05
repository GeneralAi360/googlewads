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
        cls.design_brief_schema = json.loads((ROOT / "schemas" / "design-brief.schema.json").read_text(encoding="utf-8"))
        cls.preproduction_schema = json.loads((ROOT / "schemas" / "preproduction-freeze.schema.json").read_text(encoding="utf-8"))
        cls.hero_generation_schema = json.loads((ROOT / "schemas" / "hero-generation-spec.schema.json").read_text(encoding="utf-8"))
        cls.campaign_system_schema = json.loads((ROOT / "schemas" / "campaign-design-system.schema.json").read_text(encoding="utf-8"))

    def test_design_system_provenance_keys_are_schema_allowed_and_applied(self):
        matrix = {
            "run_id": "schema-demo", "expected_output_files": 1,
            "banner_matrix": [{
                "job_id": "C01-S300x250-V01-Lru", "concept_id": "C01", "variant_id": "V01", "language": "ru",
                "width": 300, "height": 250, "dimension": "300x250", "layout_family": "rectangle",
                "output_path": "outputs/demo.png", "output_format": "png",
            }],
        }
        contract = {
            "concept_id": "C01", "status": "APPROVED", "angle": "offer-led", "primary_proposition": "Verified proposition",
            "supporting_proof": None, "visual_idea": "Product hero", "primary_aoi": "product", "scan_path": ["product", "headline", "cta"],
            "brand_id": "brand-demo",
            "art_direction": {
                "mode": "ART_DIRECTION_LOCKED", "art_direction_id": "AD-C01-LOCKED", "visual_thesis": "Product-led restrained grid",
                "selection_provenance": "BRAND_LOCKED", "representative_preview_id": None, "selected_from_candidate_ids": [],
                "alignment_logic": "copy left, hero right", "graphic_device": "product hero", "image_treatment": "clean commercial",
                "whitespace_character": "restrained", "anti_template_exclusions": [],
            },
            "reference_dna_ids": [], "lighting": {"lighting_scheme_id": None, "scene_directive": None, "composition_directive": None},
            "source_grounding": [{"source_id": "source-1", "supports": "proposition"}],
            "variants": [{"variant_id": "V01", "test_hypothesis": "baseline", "visual_direction_override": None, "copy_by_language": {"ru": {"headline": "Заголовок", "support": None, "offer": None, "cta": "CTA"}}}],
        }
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            contracts = root / "contracts"
            contracts.mkdir()
            contract_path = contracts / "C01.creative.json"
            contract_path.write_text(json.dumps(contract, ensure_ascii=False), encoding="utf-8")
            contract_sha = self.freeze.canonical_sha(contract)
            creative_freeze = {
                "status": "CREATIVE_CONTRACTS_FROZEN", "preproduction_freeze_sha256": "1" * 64,
                "campaign_design_system_id": "CDS-1", "campaign_design_system_sha256": "2" * 64,
                "idea_architecture_id": "IDEA-1", "visual_character_signature_id": "VC-1", "lighting_intent_id": "LIGHT-1",
                "contracts": [{"concept_id": "C01", "path": contract_path.as_posix(), "sha256": contract_sha, "source_grounding_ids": ["source-1"], "art_direction_id": "AD-C01-LOCKED"}],
            }
            jobs = root / "jobs"
            self.materializer.materialize(matrix, jobs)
            self.apply.apply(matrix, creative_freeze, contracts, jobs / "render-specs")
            spec = json.loads((jobs / "render-specs" / "C01-S300x250-V01-Lru.json").read_text(encoding="utf-8"))

        allowed = set(self.schema["properties"]["provenance"]["properties"])
        actual = set(spec["provenance"])
        self.assertTrue(actual <= allowed, f"runtime provenance fields not allowed by schema: {sorted(actual - allowed)}")
        for name, expected in (("campaign_design_system_id", "CDS-1"), ("idea_architecture_id", "IDEA-1"), ("visual_character_signature_id", "VC-1"), ("lighting_intent_id", "LIGHT-1")):
            self.assertEqual(spec["provenance"][name], expected)

    def test_design_brief_requires_meaning_character_focus_and_lighting(self):
        required = set(self.design_brief_schema["required"])
        for name in ("idea_architecture", "visual_character", "focus_budget", "forbidden_visuals", "creative_chaos_audit", "lighting_intent"):
            self.assertIn(name, required)
        lighting = self.design_brief_schema["properties"]["lighting_intent"]
        self.assertIn("scene_lighting", lighting["required"])
        self.assertIn("composition_lighting", lighting["required"])

    def test_hero_generation_schema_keeps_critical_text_and_logo_out_of_generation(self):
        self.assertEqual(self.hero_generation_schema["properties"]["generated_text_allowed"]["const"], False)
        self.assertEqual(self.hero_generation_schema["properties"]["generated_logo_allowed"]["const"], False)
        for name in ("idea_architecture_id", "visual_character_signature_id", "lighting_intent_id"):
            self.assertIn(name, self.hero_generation_schema["required"])

    def test_preproduction_freeze_requires_campaign_system_and_semantic_ids(self):
        required = set(self.preproduction_schema["required"])
        for name in ("campaign_design_system", "idea_architecture_id", "visual_character_signature_id", "lighting_intent_id"):
            self.assertIn(name, required)

    def test_campaign_design_system_has_lighting_and_format_adaptation_contract(self):
        required = set(self.campaign_system_schema["required"])
        for name in ("lighting_system", "format_adaptation_rules", "idea_architecture_id", "visual_character_signature_id", "lighting_intent_id"):
            self.assertIn(name, required)

    def test_lighting_target_selector_schema_matches_renderer_runtime(self):
        defs = self.schema["$defs"]
        for name in ("heroGlow", "textPlate"):
            properties = defs[name]["properties"]
            self.assertIn("target_slot", properties)
            self.assertIn("target_slots", properties)
            self.assertIn("box", properties)

    def test_banner_review_schema_requires_semantic_and_lighting_fidelity(self):
        required = set(self.banner_review_schema["properties"]["checks"]["required"])
        for name in ("idea_fidelity", "emotional_fidelity", "visual_character_fidelity", "campaign_design_system_fidelity", "lighting_intent_fidelity"):
            self.assertIn(name, required)

    def test_pack_review_schema_requires_cross_size_semantic_and_lighting_consistency(self):
        required = set(self.pack_review_schema["properties"]["checks"]["required"])
        for name in ("idea_consistency", "emotional_consistency", "visual_character_consistency", "campaign_design_system_consistency", "cross_size_lighting_intent_consistency"):
            self.assertIn(name, required)

    def test_output_manifest_allows_campaign_design_provenance(self):
        top = self.output_schema["properties"]
        file_props = top["files"]["items"]["properties"]
        for name in ("campaign_design_system_id", "campaign_design_system_sha256", "idea_architecture_id", "visual_character_signature_id", "lighting_intent_id"):
            self.assertIn(name, top)
            self.assertIn(name, file_props)


if __name__ == "__main__":
    unittest.main()
