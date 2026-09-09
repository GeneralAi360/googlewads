import importlib.util
import struct
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "validate_google_banner.py"
SPEC = importlib.util.spec_from_file_location("validator", MODULE_PATH)
validator = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(validator)


def fake_png(width: int, height: int, animated: bool = False, pad_to: int | None = None) -> bytes:
    data = (
        b"\x89PNG\r\n\x1a\n"
        + struct.pack(">I", 13)
        + b"IHDR"
        + struct.pack(">II", width, height)
        + b"\x08\x02\x00\x00\x00"
        + b"\x00\x00\x00\x00"
    )
    if animated:
        data += struct.pack(">I", 8) + b"acTL" + struct.pack(">II", 2, 0) + b"\x00\x00\x00\x00"
    if pad_to and len(data) < pad_to:
        data += b"X" * (pad_to - len(data))
    return data


def fake_gif(width: int, height: int, frames: int = 1) -> bytes:
    header = b"GIF89a"
    lsd = struct.pack("<HHBBB", width, height, 0x80, 0, 0)
    gct = b"\x00\x00\x00\xff\xff\xff"
    image = (
        b"\x2c"
        + struct.pack("<HHHHB", 0, 0, width, height, 0)
        + b"\x02"
        + b"\x01\x00"
        + b"\x00"
    )
    return header + lsd + gct + image * frames + b"\x3b"


def fake_jpeg(width: int, height: int) -> bytes:
    # Minimal structure sufficient for the dimension parser: SOI + SOF0 + EOI.
    sof_payload = b"\x08" + struct.pack(">HHB", height, width, 1) + b"\x01\x11\x00"
    sof = b"\xff\xc0" + struct.pack(">H", len(sof_payload) + 2) + sof_payload
    return b"\xff\xd8" + sof + b"\xff\xd9"


class ValidatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = validator.load_config()

    def write_temp(self, suffix: str, data: bytes) -> Path:
        tmp = tempfile.NamedTemporaryFile(suffix=suffix, delete=False)
        tmp.write(data)
        tmp.close()
        self.addCleanup(lambda: Path(tmp.name).unlink(missing_ok=True))
        return Path(tmp.name)

    def test_core_png_passes(self):
        path = self.write_temp(".png", fake_png(300, 250))
        result = validator.validate(path, "demand_gen_uploaded_display", "core", self.config)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["dimension"], "300x250")

    def test_wrong_dimension_fails_core_pack(self):
        path = self.write_temp(".png", fake_png(301, 250))
        result = validator.validate(path, "demand_gen_uploaded_display", "core", self.config)
        self.assertEqual(result["status"], "FAIL")
        self.assertTrue(any("dimension" in err for err in result["errors"]))

    def test_conservative_size_limit(self):
        path = self.write_temp(".png", fake_png(300, 250, pad_to=150001))
        result = validator.validate(path, "demand_gen_uploaded_display", "core", self.config)
        self.assertEqual(result["status"], "FAIL")
        self.assertTrue(any("file size" in err for err in result["errors"]))

    def test_extension_signature_mismatch_fails(self):
        path = self.write_temp(".jpg", fake_png(300, 250))
        result = validator.validate(path, "demand_gen_uploaded_display", "core", self.config)
        self.assertEqual(result["status"], "FAIL")
        self.assertTrue(any("extension" in err for err in result["errors"]))

    def test_static_gif_passes_demand_gen(self):
        path = self.write_temp(".gif", fake_gif(320, 50, frames=1))
        result = validator.validate(path, "demand_gen_uploaded_display", "core", self.config)
        self.assertEqual(result["status"], "PASS")
        self.assertFalse(result["animated"])

    def test_animated_gif_fails_demand_gen(self):
        path = self.write_temp(".gif", fake_gif(320, 50, frames=2))
        result = validator.validate(path, "demand_gen_uploaded_display", "core", self.config)
        self.assertEqual(result["status"], "FAIL")
        self.assertTrue(result["animated"])
        self.assertTrue(any("animation" in err for err in result["errors"]))

    def test_animated_gif_general_mode_warns(self):
        path = self.write_temp(".gif", fake_gif(320, 50, frames=2))
        result = validator.validate(path, "uploaded_display_general", "full", self.config)
        self.assertEqual(result["status"], "PASS")
        self.assertTrue(result["warnings"])

    def test_jpeg_dimensions_are_read(self):
        path = self.write_temp(".jpg", fake_jpeg(336, 280))
        result = validator.validate(path, "demand_gen_uploaded_display", "core", self.config)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["dimension"], "336x280")

    def test_apng_fails_static_demand_gen_mode(self):
        path = self.write_temp(".png", fake_png(300, 250, animated=True))
        result = validator.validate(path, "demand_gen_uploaded_display", "core", self.config)
        self.assertEqual(result["status"], "FAIL")
        self.assertTrue(result["animated"])


if __name__ == "__main__":
    unittest.main()
