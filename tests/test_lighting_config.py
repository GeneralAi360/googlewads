import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LIGHTING_CONFIG = ROOT / "config" / "lighting-schemes.json"
BANNER_RUN_SCHEMA = ROOT / "schemas" / "banner-run.schema.json"


class LightingConfigTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(LIGHTING_CONFIG.read_text(encoding="utf-8"))
        cls.schemes = cls.data["schemes"]

    def test_exactly_30_schemes(self):
        self.assertEqual(len(self.schemes), 30)

    def test_ids_are_unique_and_complete(self):
        ids = [scheme["id"] for scheme in self.schemes]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(sorted(ids), list(range(1, 31)))

    def test_slugs_are_unique(self):
        slugs = [scheme["slug"] for scheme in self.schemes]
        self.assertEqual(len(slugs), len(set(slugs)))

    def test_required_fields_exist(self):
        required = {"id", "slug", "name_ru", "name_en", "group", "mood", "best_for", "light_logic", "contrast", "copy_space", "attention_use", "cautions"}
        for scheme in self.schemes:
            self.assertTrue(required.issubset(scheme), scheme.get("id"))

    def test_expected_groups_exist(self):
        groups = {scheme["group"] for scheme in self.schemes}
        self.assertEqual(groups, {"studio_classic", "character_art", "glass_liquid_reflections", "natural_atmosphere", "composition_angle"})

    def test_source_is_not_mislabeled_as_research(self):
        self.assertEqual(self.data["source"]["evidence_class"], "production_heuristic")


class BannerRunSchemaSmokeTests(unittest.TestCase):
    def test_banner_run_schema_is_valid_json_and_has_matrix(self):
        schema = json.loads(BANNER_RUN_SCHEMA.read_text(encoding="utf-8"))
        self.assertEqual(schema["type"], "object")
        self.assertIn("banner_matrix", schema["properties"])
        self.assertIn("expected_output_files", schema["required"])


if __name__ == "__main__":
    unittest.main()
