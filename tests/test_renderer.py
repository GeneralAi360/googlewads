import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "render_banner.py"


def load_module():
    spec = importlib.util.spec_from_file_location("render_banner", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class RendererTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_module()
        cls.font = cls.module.resolve_font_path(None)

    def make_spec(self, out: Path, width: int, height: int, family: str, hero: Path | None = None):
        return {
            "schema_version": "0.2.0",
            "job_id": f"test-{width}x{height}",
            "width": width,
            "height": height,
            "layout_family": family,
            "background": {"color": "#F3F0E8"},
            "hero": ({"path": str(hero), "focal_point": [0.5, 0.5]} if hero else None),
            "logo": {"brand_name": "BRAND"},
            "copy": {
                "headline": "Кухни на заказ",
                "support": "Бесплатный замер",
                "offer": "от 2990 BYN",
                "cta": "Рассчитать",
            },
            "brand": {
                "font_regular": self.font,
                "font_bold": self.font,
                "text_color": "#111111",
                "muted_text_color": "#444444",
                "accent_color": "#E8C77A",
                "cta_fill": "#111111",
                "cta_text": "#FFFFFF",
            },
            "lighting": {},
            "output": {"path": str(out), "format": "png"},
        }

    def test_core_layout_families_render_exact_dimensions(self):
        cases = [
            (300, 250, "rectangle"),
            (336, 280, "rectangle"),
            (728, 90, "leaderboard"),
            (970, 90, "leaderboard"),
            (160, 600, "narrow_vertical"),
            (300, 600, "large_vertical"),
            (320, 50, "micro_horizontal"),
        ]
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            for width, height, family in cases:
                with self.subTest(size=f"{width}x{height}"):
                    out = tmp / f"{width}x{height}.png"
                    spec = self.make_spec(out, width, height, family)
                    if family == "micro_horizontal":
                        spec["copy"]["support"] = None
                        spec["copy"]["offer"] = None
                    report = self.module.render_banner(spec)
                    self.assertEqual(report["status"], "PASS")
                    with Image.open(out) as image:
                        self.assertEqual(image.size, (width, height))

    def test_copy_overflow_fails_instead_of_shrinking_below_minimum(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "overflow.png"
            spec = self.make_spec(out, 320, 50, "micro_horizontal")
            spec["copy"]["headline"] = "ОЧЕНЬ ДЛИННЫЙ НЕПОМЕЩАЮЩИЙСЯ ЗАГОЛОВОК " * 8
            spec["copy"]["support"] = None
            spec["copy"]["offer"] = None
            spec["overrides"] = {"text": {"headline": {"min_px": 18, "max_px": 18, "max_lines": 1}}}
            with self.assertRaises(self.module.RenderError) as ctx:
                self.module.render_banner(spec)
            self.assertEqual(ctx.exception.code, "FAIL_COPY_OVERFLOW")
            self.assertFalse(out.exists())

    def test_hero_focal_crop_and_lighting_preserve_exact_size(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            hero = Image.new("RGB", (800, 400), "#CC3333")
            for x in range(400, 800):
                for y in range(400):
                    hero.putpixel((x, y), (30, 80, 190))
            hero_path = tmp / "hero.jpg"
            hero.save(hero_path, quality=90)
            out = tmp / "lit.jpg"
            spec = self.make_spec(out, 970, 250, "billboard", hero_path)
            spec["hero"]["focal_point"] = [0.8, 0.5]
            spec["lighting"] = {
                "hero_edge_glow": {
                    "enabled": True,
                    "target_slot": "hero",
                    "color": "#FFFFFF",
                    "opacity": 70,
                    "expand_px": 10,
                    "blur": 8,
                },
                "spotlight": {
                    "enabled": True,
                    "center": [0.25, 0.4],
                    "radius": [0.20, 0.25],
                    "color": "#FFFFFF",
                    "opacity": 80,
                    "blur": 20,
                },
                "copy_scrim": {
                    "enabled": True,
                    "side": "right",
                    "color": "#000000",
                    "max_opacity": 70,
                    "extent": 0.55,
                },
                "vignette": {"enabled": True, "opacity": 40, "softness": 0.35},
                "text_plate": {
                    "enabled": True,
                    "target_slots": ["headline", "support"],
                    "color": "#FFFFFF",
                    "opacity": 40,
                    "radius_px": 8,
                },
            }
            spec["output"] = {"path": str(out), "format": "jpg", "jpeg_quality": 92, "min_jpeg_quality": 70}
            report = self.module.render_banner(spec)
            self.assertEqual(
                set(report["lighting_applied"]),
                {"hero_edge_glow", "spotlight", "copy_scrim", "vignette", "text_plate"},
            )
            with Image.open(out) as image:
                self.assertEqual(image.size, (970, 250))

    def test_png_target_overflow_is_explicit_failure_and_removes_invalid_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "tiny-limit.png"
            spec = self.make_spec(out, 300, 250, "rectangle")
            spec["output"]["target_max_bytes"] = 1000
            with self.assertRaises(self.module.RenderError) as ctx:
                self.module.render_banner(spec)
            self.assertEqual(ctx.exception.code, "FAIL_FILE_SIZE")
            self.assertFalse(out.exists())

    def test_layout_presets_cover_all_google_registry_families(self):
        formats = json.loads((ROOT / "config" / "google-formats.json").read_text(encoding="utf-8"))
        presets = self.module.load_presets()
        families = {entry["family"] for entry in formats["formats"].values()}
        missing = []
        for family in families:
            try:
                self.module.resolve_family(presets, family)
            except self.module.RenderError:
                missing.append(family)
        self.assertEqual(missing, [])

    def test_contrast_ratio_and_optional_gate(self):
        self.assertAlmostEqual(self.module.contrast_ratio("#000000", "#FFFFFF"), 21.0, places=3)
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "contrast.png"
            spec = self.make_spec(out, 300, 250, "rectangle")
            spec["brand"]["cta_fill"] = "#777777"
            spec["brand"]["cta_text"] = "#888888"
            spec["qa"] = {"min_cta_contrast": 3.0}
            with self.assertRaises(self.module.RenderError) as ctx:
                self.module.render_banner(spec)
            self.assertEqual(ctx.exception.code, "FAIL_CONTRAST")

    def test_unsupported_copy_slot_fails_cleanly(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "micro-offer.png"
            spec = self.make_spec(out, 320, 50, "micro_horizontal")
            spec["copy"]["support"] = None
            spec["copy"]["offer"] = "Скидка"
            with self.assertRaises(self.module.RenderError) as ctx:
                self.module.render_banner(spec)
            self.assertEqual(ctx.exception.code, "FAIL_LAYOUT")

    def test_local_photo_contrast_fails_without_plate_and_passes_with_plate(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            hero = Image.new("RGB", (640, 100), "#F7F7F7")
            hero_path = root / "bright.jpg"
            hero.save(hero_path, quality=95)

            failing = self.make_spec(root / "fail.png", 320, 50, "micro_horizontal", hero_path)
            failing["hero"]["mode"] = "full_bleed"
            failing["logo"] = None
            failing["copy"] = {"headline": "Кухни на заказ", "support": None, "offer": None, "cta": None}
            failing["brand"]["text_color"] = "#FFFFFF"
            failing["qa"] = {"min_local_text_contrast": 4.5}
            with self.assertRaises(self.module.RenderError) as ctx:
                self.module.render_banner(failing)
            self.assertEqual(ctx.exception.code, "FAIL_LOCAL_CONTRAST")
            self.assertFalse((root / "fail.png").exists())

            passing = self.make_spec(root / "pass.png", 320, 50, "micro_horizontal", hero_path)
            passing["hero"]["mode"] = "full_bleed"
            passing["logo"] = None
            passing["copy"] = {"headline": "Кухни на заказ", "support": None, "offer": None, "cta": None}
            passing["brand"]["text_color"] = "#FFFFFF"
            passing["lighting"] = {
                "text_plate": {
                    "enabled": True,
                    "target_slots": ["headline"],
                    "color": "#000000",
                    "opacity": 255,
                    "padding_px": 0,
                    "radius_px": 0,
                }
            }
            passing["qa"] = {"min_local_text_contrast": 4.5}
            report = self.module.render_banner(passing)
            self.assertGreaterEqual(report["contrast"]["local_text"]["headline"]["p10"], 4.5)
            self.assertTrue((root / "pass.png").is_file())

    def test_logo_clearspace_is_explicit_and_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "logo-space.png"
            spec = self.make_spec(out, 300, 250, "rectangle")
            spec["logo"] = {"brand_name": "BRAND", "clearspace_ratio": 0.15, "clearspace_px": 2}
            report = self.module.render_banner(spec)
            element = report["elements"]["brand_name"]
            self.assertGreater(element["clearspace_px"], 0)
            self.assertGreater(element["box"][0], element["slot_box"][0])
            self.assertGreater(element["box"][1], element["slot_box"][1])

    def test_local_contrast_report_exposes_luminance_variation(self):
        canvas = Image.new("RGB", (100, 20), "#FFFFFF")
        draw = canvas.load()
        for x in range(50):
            for y in range(20):
                draw[x, y] = (0, 0, 0)
        metrics = self.module.sample_local_contrast(canvas, (0, 0, 100, 20), "#FFFFFF", grid=10)
        self.assertGreater(metrics["luminance_range"], 0.9)
        self.assertLess(metrics["min"], 1.1)
        self.assertGreater(metrics["max"], 20)


if __name__ == "__main__":
    unittest.main()
