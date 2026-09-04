import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "build_banner_matrix.py"


def load_module():
    spec = importlib.util.spec_from_file_location("build_banner_matrix", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class BannerMatrixTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_module()
        cls.config = cls.module.load_formats()

    def test_core_pack_2_concepts_produces_14_rows(self):
        sizes = self.module.resolve_sizes(self.config, "core", None)
        result = self.module.build_matrix(run_id="demo", concepts=2, sizes=sizes, variants=1, languages=["ru"], output_format="png", output_root="outputs", config=self.config)
        self.assertEqual(result["expected_output_files"], 14)
        self.assertEqual(len(result["banner_matrix"]), 14)

    def test_output_math_includes_variants_and_languages(self):
        result = self.module.build_matrix(run_id="demo", concepts=2, sizes=["300x250", "728x90"], variants=2, languages=["ru", "en"], output_format="png", output_root="outputs", config=self.config)
        self.assertEqual(result["expected_output_files"], 16)

    def test_each_job_id_is_unique(self):
        result = self.module.build_matrix(run_id="demo", concepts=3, sizes=["300x250", "320x50"], variants=2, languages=["ru"], output_format="jpg", output_root="outputs", config=self.config)
        ids = [row["job_id"] for row in result["banner_matrix"]]
        self.assertEqual(len(ids), len(set(ids)))

    def test_layout_family_comes_from_google_registry(self):
        result = self.module.build_matrix(run_id="demo", concepts=1, sizes=["300x250", "320x50", "160x600"], variants=1, languages=["ru"], output_format="png", output_root="outputs", config=self.config)
        families = {row["dimension"]: row["layout_family"] for row in result["banner_matrix"]}
        self.assertEqual(families["300x250"], "rectangle")
        self.assertEqual(families["320x50"], "micro_horizontal")
        self.assertEqual(families["160x600"], "narrow_vertical")

    def test_explicit_unsupported_size_is_rejected(self):
        with self.assertRaises(self.module.MatrixError):
            self.module.resolve_sizes(self.config, None, ["999x999"])

    def test_pack_and_explicit_sizes_are_mutually_exclusive(self):
        with self.assertRaises(self.module.MatrixError):
            self.module.resolve_sizes(self.config, "core", ["300x250"])

    def test_language_is_sanitized_only_in_job_id_not_semantics(self):
        result = self.module.build_matrix(run_id="demo", concepts=1, sizes=["300x250"], variants=1, languages=["pt-BR"], output_format="png", output_root="outputs", config=self.config)
        row = result["banner_matrix"][0]
        self.assertEqual(row["language"], "pt-BR")
        self.assertIn("Lpt-BR", row["job_id"])

    def test_matrix_schema_required_shape_matches_builder_output(self):
        schema = json.loads((ROOT / "schemas" / "banner-matrix.schema.json").read_text(encoding="utf-8"))
        result = self.module.build_matrix(run_id="demo", concepts=1, sizes=["300x250"], variants=1, languages=["ru"], output_format="png", output_root="outputs", config=self.config)
        for key in schema["required"]:
            self.assertIn(key, result)
        row = result["banner_matrix"][0]
        for key in schema["properties"]["banner_matrix"]["items"]["required"]:
            self.assertIn(key, row)
        self.assertEqual(result["output_math"]["formula"], schema["properties"]["output_math"]["properties"]["formula"]["const"])


if __name__ == "__main__":
    unittest.main()
