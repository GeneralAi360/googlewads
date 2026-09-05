import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "freeze_banner_run.py"


def load_module():
    spec = importlib.util.spec_from_file_location("freeze_banner_run", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def complete_context():
    return {
        "formats": {"mode": "demand_gen_uploaded_display", "pack": "core"},
        "deliverables": {
            "concept_count": 1,
            "variant_count": 1,
            "languages": ["ru"],
            "output_format": "jpg",
        },
        "business": {"product_service": "Synthetic demo product", "geography": "Minsk"},
        "campaign": {
            "objective": "lead",
            "landing_page": "https://example.invalid",
            "funnel_stage": "product-aware",
            "primary_action": "request quote",
        },
        "audience": {"primary": "Homeowners"},
        "offer": {
            "primary_value_proposition": "Synthetic proposition",
            "price": None,
            "proof_points": [],
            "cta": "Request quote",
        },
        "constraints": {"legal_disclaimers": [], "prohibited_claims": []},
        "brand": {
            "brand_id": "demo-brand",
            "no_formal_system": True,
            "no_logo_asset": True,
            "allow_font_fallback": True,
            "allow_run_local_palette": True,
            "real_photos": [],
            "ai_hero_allowed": True,
            "people_faces_policy": "not required",
            "additional_rules": [],
            "prohibited_elements": [],
        },
        "visual": {
            "hero_subject": "product",
            "mood": "clean",
            "material_lighting": None,
            "lighting_style": None,
            "copy_safe_zone": "right",
            "effect_policy": "restrained",
        },
        "production": {
            "approval_step": False,
            "confidentiality_restrictions": None,
        },
    }


class FreezeBannerRunTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_module()

    def test_incomplete_context_does_not_create_matrix(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "freeze"
            with self.assertRaises(self.module.FreezeError) as ctx:
                self.module.freeze_context({}, run_id="bad", out_dir=out)
            self.assertEqual(ctx.exception.code, "BRIEF_INCOMPLETE")
            self.assertFalse((out / "banner-matrix.json").exists())
            self.assertFalse((out / "run-freeze.json").exists())

    def test_ambiguous_banner_count_does_not_create_matrix(self):
        context = complete_context()
        context["deliverables"]["raw_banner_count_phrase"] = "10 banners in 7 sizes"
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "freeze"
            with self.assertRaises(self.module.FreezeError) as ctx:
                self.module.freeze_context(context, run_id="ambiguous", out_dir=out)
            self.assertEqual(ctx.exception.code, "OUTPUT_COUNT_AMBIGUOUS")
            self.assertFalse((out / "banner-matrix.json").exists())

    def test_ready_context_freezes_current_google_core_pack(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = self.module.freeze_context(
                complete_context(),
                run_id="ready",
                out_dir=root / "freeze",
                output_root=(root / "outputs").as_posix(),
            )
            freeze = result["freeze"]
            self.assertEqual(result["status"], "FROZEN")
            self.assertEqual(freeze["intake_status"], "READY_TO_FREEZE")
            self.assertEqual(freeze["size_count"], 7)
            self.assertEqual(freeze["expected_output_files"], 7)
            self.assertEqual(len(result["matrix"]["banner_matrix"]), 7)
            config = json.loads((ROOT / "config" / "google-formats.json").read_text(encoding="utf-8"))
            self.assertEqual(freeze["google_spec_snapshot_date"], config["snapshot_date"])
            self.assertRegex(freeze["intake_context_sha256"], r"^[0-9a-f]{64}$")
            self.assertRegex(freeze["matrix_sha256"], r"^[0-9a-f]{64}$")
            self.assertTrue((root / "freeze" / "banner-matrix.json").is_file())
            self.assertTrue((root / "freeze" / "run-freeze.json").is_file())

    def test_renderer_unsupported_gif_is_rejected_at_freeze(self):
        context = complete_context()
        context["deliverables"]["output_format"] = "gif"
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "freeze"
            with self.assertRaises(self.module.FreezeError) as ctx:
                self.module.freeze_context(context, run_id="gif", out_dir=out)
            self.assertEqual(ctx.exception.code, "UNSUPPORTED_RENDER_FORMAT")
            self.assertFalse((out / "banner-matrix.json").exists())

    def test_freeze_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            out = root / "freeze"
            self.module.freeze_context(complete_context(), run_id="once", out_dir=out, output_root=(root / "outputs").as_posix())
            with self.assertRaises(self.module.FreezeError) as ctx:
                self.module.freeze_context(complete_context(), run_id="once", out_dir=out, output_root=(root / "outputs").as_posix())
            self.assertEqual(ctx.exception.code, "FREEZE_ALREADY_EXISTS")


if __name__ == "__main__":
    unittest.main()
