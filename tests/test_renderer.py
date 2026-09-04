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
            "copy": {"headline": "Кухни на заказ", "support": "Бесплатный замер", "offer": "от 2990 BYN", "cta": "Рассчитать"},
            "brand": {
                "font_regular": self.font,
                "font_bold": self.font,
                "text_color": "#111111",
                "muted_text_color": "#444444",
                "accent_color": "#E8C77A",
                "cta_fill": "#111111",
                "cta_text": "#FFFFFF"
            },
            "lighting": {},
            "output": {"path": str(out), "format": "png"}
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
                "spotlight": {"enabled": True, "center": [0.25, 0.4], "radius": [0.20, 0.25], "color": "#FFFFFF", "opacity": 80, "blur": 20},
                "copy_scrim": {"enabled": True, "side": "right", "color": "#000000", "max_opacity": 70, "extent": 0.55},
                "vignette": {"enabled": True, "opacity": 40, "softness": 0.35}
            }
            spec["output"] = {"path": str(out), "format": "jpg", "jpeg_quality": 92, "min_jpeg_quality": 70}
            report = self.module.render_banner(spec)
            self.assertEqual(set(report["lighting_applied"]), {"spotlight", "copy_scrim", "vignette"})
            with Image.open(out) as image:
                self.assertEqual(image.size, (970, 250))

    def test_png_target_overflow_is_explicit_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "tiny-limit.png"
            spec = self.make_spec(out, 300, 250, "rectangle")
            spec["output"]["target_max_bytes"] = 1000
            with self.assertRaises(self.module.RenderError) as ctx:
                self.module.render_banner(spec)
            self.assertEqual(ctx.exception.code, "FAIL_FILE_SIZE")

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


if __name__ == "__main__":
    unittest.main()
