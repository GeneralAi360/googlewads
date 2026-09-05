import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class CopyAdaptationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.freeze = load(ROOT / "scripts" / "freeze_creative_contracts.py", "freeze_creative_contracts_adapt")
        cls.apply = load(ROOT / "scripts" / "apply_creative_contracts.py", "apply_creative_contracts_adapt")
        cls.validate = load(ROOT / "scripts" / "validate_creative_bindings.py", "validate_creative_bindings_adapt")
        cls.materializer = load(ROOT / "scripts" / "materialize_banner_jobs.py", "materialize_banner_jobs_adapt")
        cls.pack = load(ROOT / "scripts" / "render_banner_pack.py", "render_banner_pack_adapt")
        cls.renderer = load(ROOT / "scripts" / "render_banner.py", "render_banner_adapt")
        cls.font = cls.renderer.resolve_font_path(None)

    def matrix(self, root: Path):
        return {
            "run_id": "adapt-demo", "expected_output_files": 2,
            "banner_matrix": [
                {"job_id": "C01-S300x250-V01-Lru", "concept_id": "C01", "variant_id": "V01", "language": "ru", "width": 300, "height": 250, "dimension": "300x250", "layout_family": "rectangle", "output_path": (root / "out" / "rectangle.png").as_posix(), "output_format": "png"},
                {"job_id": "C01-S320x50-V01-Lru", "concept_id": "C01", "variant_id": "V01", "language": "ru", "width": 320, "height": 50, "dimension": "320x50", "layout_family": "micro_horizontal", "output_path": (root / "out" / "micro.png").as_posix(), "output_format": "png"},
            ],
        }

    def contract(self):
        return {
            "concept_id": "C01", "status": "APPROVED", "angle": "offer-led", "audience_state": "product-aware",
            "primary_proposition": "Verified proposition", "supporting_proof": "Verified proof", "visual_idea": "Product hero",
            "primary_aoi": "product", "scan_path": ["product", "headline", "cta"], "brand_id": "brand-demo",
            "art_direction": {
                "mode": "ART_DIRECTION_LOCKED", "art_direction_id": "AD-C01-LOCKED", "visual_thesis": "Product-led restrained grid",
                "selection_provenance": "BRAND_LOCKED", "representative_preview_id": None, "selected_from_candidate_ids": [],
                "alignment_logic": "copy left, hero right", "graphic_device": "product hero", "image_treatment": "clean commercial",
                "whitespace_character": "restrained", "anti_template_exclusions": [],
            },
            "reference_dna_ids": [], "lighting": {"lighting_scheme_id": None, "scene_directive": None, "composition_directive": None},
            "source_grounding": [{"source_id": "landing-page", "supports": "proposition"}],
            "variants": [{
                "variant_id": "V01", "test_hypothesis": "baseline", "visual_direction_override": None,
                "copy_by_language": {"ru": {"headline": "Полный заголовок", "support": "Поддерживающий текст", "offer": "DEMO OFFER", "cta": "Рассчитать"}},
                "copy_overrides_by_layout_family": {"micro_horizontal": {"headline": "Короткий заголовок", "support": None, "offer": None}},
                "copy_overrides_by_dimension": {"320x50": {"headline": "320 заголовок"}},
            }],
        }

    @staticmethod
    def add_design_identity(creative_freeze):
        creative_freeze.update({
            "preproduction_freeze_sha256": "a" * 64,
            "campaign_design_system_id": "CDS-ADAPT-1", "campaign_design_system_sha256": "b" * 64,
            "idea_architecture_id": "IDEA-ADAPT-1", "visual_character_signature_id": "VC-ADAPT-1", "lighting_intent_id": "LIGHT-ADAPT-1",
        })
        return creative_freeze

    def prepare_bound_specs(self, root: Path):
        matrix = self.matrix(root)
        contracts = root / "contracts"
        contracts.mkdir()
        contract_path = contracts / "C01.creative.json"
        contract_path.write_text(json.dumps(self.contract(), ensure_ascii=False, indent=2), encoding="utf-8")
        creative_freeze = self.add_design_identity(self.freeze.freeze_contracts(matrix, contracts, root / "creative-freeze.json"))
        jobs = root / "jobs"
        self.materializer.materialize(matrix, jobs)
        self.apply.apply(matrix, creative_freeze, contracts, jobs / "render-specs")
        for row in matrix["banner_matrix"]:
            spec_path = jobs / "render-specs" / f"{row['job_id']}.json"
            spec = json.loads(spec_path.read_text(encoding="utf-8"))
            spec["background"] = {"color": "#FFFFFF"}
            spec["logo"] = {"brand_name": "BRAND"}
            spec["brand"] = {"font_regular": self.font, "font_bold": self.font, "text_color": "#111111", "cta_fill": "#111111", "cta_text": "#FFFFFF", "offer_fill": "#EEEEEE", "offer_text": "#111111"}
            spec["output"] = {"path": row["output_path"], "format": "png"}
            spec_path.write_text(json.dumps(spec, ensure_ascii=False, indent=2), encoding="utf-8")
        return matrix, contracts, creative_freeze, jobs

    def test_dimension_override_wins_and_micro_removes_secondary_copy(self):
        contract = self.contract()
        rectangle = self.apply.variant_copy(contract, "V01", "ru", "rectangle", "300x250")
        micro = self.apply.variant_copy(contract, "V01", "ru", "micro_horizontal", "320x50")
        self.assertEqual(rectangle["headline"], "Полный заголовок")
        self.assertEqual(rectangle["support"], "Поддерживающий текст")
        self.assertEqual(rectangle["offer"], "DEMO OFFER")
        self.assertEqual(micro["headline"], "320 заголовок")
        self.assertIsNone(micro["support"])
        self.assertIsNone(micro["offer"])
        self.assertEqual(micro["cta"], "Рассчитать")

    def test_bound_specs_pass_binding_validator_with_size_adaptations(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            matrix, contracts, creative_freeze, jobs = self.prepare_bound_specs(root)
            result = self.validate.validate(matrix, creative_freeze, contracts, jobs / "render-specs")
            self.assertEqual(result["status"], "CREATIVE_BINDING_PASS")
            self.assertEqual(result["passed_jobs"], 2)

    def test_pack_runner_requires_binding_and_passes_valid_adapted_pack(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            matrix, _, _, jobs = self.prepare_bound_specs(root)

            def validator(path, mode, pack):
                with Image.open(path) as image:
                    size = image.size
                return {"status": "PASS", "errors": [], "dimension": f"{size[0]}x{size[1]}"}

            result = self.pack.render_pack(matrix, jobs / "render-specs", technical_validator=validator, require_creative_binding=True, manifest_path=root / "manifest.json")
            self.assertEqual(result["status"], "PASS")
            manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["campaign_design_system_id"], "CDS-ADAPT-1")
            self.assertEqual(manifest["lighting_intent_id"], "LIGHT-ADAPT-1")
            self.assertTrue(all("campaign_design_system_binding" in item["checks"] for item in manifest["files"]))

    def test_pack_runner_rejects_worker_copy_mutation_even_without_separate_validator(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            matrix, _, _, jobs = self.prepare_bound_specs(root)
            target = jobs / "render-specs" / "C01-S320x50-V01-Lru.json"
            spec = json.loads(target.read_text(encoding="utf-8"))
            spec["copy"]["headline"] = "Worker mutation"
            target.write_text(json.dumps(spec, ensure_ascii=False), encoding="utf-8")
            result = self.pack.render_pack(matrix, jobs / "render-specs", technical_validator=lambda *args: {"status": "PASS", "errors": []}, require_creative_binding=True)
            self.assertEqual(result["status"], "FAIL")
            failure = next(item for item in result["failures"] if item["job_id"] == "C01-S320x50-V01-Lru")
            self.assertEqual(failure["code"], "FAIL_CREATIVE_BINDING")
            self.assertIn("copy differs", failure["message"])

    def test_pack_runner_rejects_unbound_spec_when_required(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            matrix = self.matrix(root)
            jobs = root / "jobs"
            self.materializer.materialize(matrix, jobs)
            for row in matrix["banner_matrix"]:
                path = jobs / "render-specs" / f"{row['job_id']}.json"
                spec = json.loads(path.read_text(encoding="utf-8"))
                spec["copy"] = {"headline": "H", "support": None, "offer": None, "cta": "C"}
                spec["brand"] = {"font_regular": self.font, "font_bold": self.font, "text_color": "#111111", "cta_fill": "#111111", "cta_text": "#FFFFFF"}
                spec["logo"] = None
                spec["background"] = {"color": "#FFFFFF"}
                spec["output"] = {"path": row["output_path"], "format": "png"}
                path.write_text(json.dumps(spec), encoding="utf-8")
            result = self.pack.render_pack(matrix, jobs / "render-specs", technical_validator=lambda *args: {"status": "PASS", "errors": []}, require_creative_binding=True)
            self.assertEqual(result["status"], "FAIL")
            self.assertTrue(all(item["code"] == "FAIL_CREATIVE_BINDING" for item in result["failures"]))


if __name__ == "__main__":
    unittest.main()
