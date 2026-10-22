#!/usr/bin/env python3
"""Dependency-free preflight for Google uploaded display image files.

Checks exact pixel dimensions, file extension/signature, conservative file-size
limit, and static/animated state for modes that forbid animation.

This validator intentionally does not claim to validate creative policy,
visual hierarchy, copy accuracy, or animated GIF timing.
"""

from __future__ import annotations

import argparse
import json
import struct
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config" / "google-formats.json"


class ImageReadError(ValueError):
    pass


def load_config() -> dict[str, Any]:
    with CONFIG_PATH.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def _skip_gif_subblocks(data: bytes, pos: int) -> int:
    while True:
        if pos >= len(data):
            raise ImageReadError("truncated GIF sub-block")
        size = data[pos]
        pos += 1
        if size == 0:
            return pos
        pos += size
        if pos > len(data):
            raise ImageReadError("truncated GIF sub-block payload")


def read_gif(data: bytes) -> tuple[int, int, bool]:
    if len(data) < 13 or data[:6] not in (b"GIF87a", b"GIF89a"):
        raise ImageReadError("invalid GIF")

    width, height = struct.unpack("<HH", data[6:10])
    packed = data[10]
    pos = 13

    if packed & 0x80:
        gct_entries = 2 ** ((packed & 0x07) + 1)
        pos += 3 * gct_entries

    frames = 0
    while pos < len(data):
        marker = data[pos]

        if marker == 0x3B:  # trailer
            break

        if marker == 0x21:  # extension
            if pos + 2 > len(data):
                raise ImageReadError("truncated GIF extension")
            pos += 2
            pos = _skip_gif_subblocks(data, pos)
            continue

        if marker == 0x2C:  # image descriptor
            if pos + 10 > len(data):
                raise ImageReadError("truncated GIF image descriptor")
            frames += 1
            local_packed = data[pos + 9]
            pos += 10
            if local_packed & 0x80:
                lct_entries = 2 ** ((local_packed & 0x07) + 1)
                pos += 3 * lct_entries
            if pos >= len(data):
                raise ImageReadError("missing GIF LZW code size")
            pos += 1  # LZW minimum code size
            pos = _skip_gif_subblocks(data, pos)
            continue

        raise ImageReadError(f"unexpected GIF block marker 0x{marker:02x}")

    return width, height, frames > 1


def read_png(data: bytes) -> tuple[int, int, bool]:
    if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ImageReadError("invalid PNG")
    if data[12:16] != b"IHDR":
        raise ImageReadError("PNG missing IHDR")
    width, height = struct.unpack(">II", data[16:24])
    animated = b"acTL" in data
    return width, height, animated


def read_jpeg(data: bytes) -> tuple[int, int, bool]:
    if len(data) < 4 or data[:2] != b"\xff\xd8":
        raise ImageReadError("invalid JPEG")

    sof_markers = {
        0xC0, 0xC1, 0xC2, 0xC3,
        0xC5, 0xC6, 0xC7,
        0xC9, 0xCA, 0xCB,
        0xCD, 0xCE, 0xCF,
    }

    pos = 2
    while pos < len(data):
        if data[pos] != 0xFF:
            pos += 1
            continue

        while pos < len(data) and data[pos] == 0xFF:
            pos += 1
        if pos >= len(data):
            break

        marker = data[pos]
        pos += 1

        if marker in (0xD8, 0xD9) or 0xD0 <= marker <= 0xD7 or marker == 0x01:
            continue

        if pos + 2 > len(data):
            break
        seglen = struct.unpack(">H", data[pos:pos + 2])[0]
        if seglen < 2 or pos + seglen > len(data):
            raise ImageReadError("invalid JPEG segment length")

        if marker in sof_markers:
            if seglen < 7:
                raise ImageReadError("truncated JPEG SOF")
            height, width = struct.unpack(">HH", data[pos + 3:pos + 7])
            return width, height, False

        pos += seglen

    raise ImageReadError("JPEG dimensions not found")


def inspect_image(path: Path) -> dict[str, Any]:
    data = path.read_bytes()
    ext = path.suffix.lower().lstrip(".")

    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        fmt = "png"
        width, height, animated = read_png(data)
    elif data.startswith((b"GIF87a", b"GIF89a")):
        fmt = "gif"
        width, height, animated = read_gif(data)
    elif data.startswith(b"\xff\xd8"):
        fmt = "jpeg"
        width, height, animated = read_jpeg(data)
    else:
        raise ImageReadError("unsupported or unrecognized image signature")

    return {
        "path": str(path),
        "extension": ext,
        "detected_format": fmt,
        "width": width,
        "height": height,
        "dimension": f"{width}x{height}",
        "bytes": len(data),
        "animated": animated,
    }


def validate(path: Path, mode_name: str, pack_name: str, config: dict[str, Any]) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    errors: list[str] = []
    warnings: list[str] = []

    try:
        info = inspect_image(path)
    except (OSError, ImageReadError) as exc:
        return {
            "path": str(path),
            "status": "FAIL",
            "errors": [str(exc)],
            "warnings": [],
            "checks": [],
        }

    mode = config["modes"][mode_name]
    allowed_dims = set(config["packs"][pack_name])

    extension_normalized = "jpg" if info["extension"] == "jpeg" else info["extension"]
    allowed_extensions = {"jpg" if x == "jpeg" else x for x in mode["allowed_extensions"]}
    detected_normalized = "jpg" if info["detected_format"] == "jpeg" else info["detected_format"]

    format_ok = extension_normalized in allowed_extensions and detected_normalized in allowed_extensions
    checks.append({"name": "format", "ok": format_ok, "value": info["detected_format"]})
    if not format_ok:
        errors.append("file format is not allowed for selected mode")

    extension_matches = extension_normalized == detected_normalized
    checks.append({"name": "extension_matches_signature", "ok": extension_matches, "value": info["extension"]})
    if not extension_matches:
        errors.append("file extension does not match detected image signature")

    dimension_ok = info["dimension"] in allowed_dims
    checks.append({"name": "dimension", "ok": dimension_ok, "value": info["dimension"]})
    if not dimension_ok:
        errors.append(f"dimension {info['dimension']} is not in selected {pack_name} pack")

    max_bytes = int(mode["max_file_size_bytes_conservative"])
    size_ok = info["bytes"] <= max_bytes
    checks.append({"name": "file_size", "ok": size_ok, "value": info["bytes"], "max": max_bytes})
    if not size_ok:
        errors.append(f"file size {info['bytes']} bytes exceeds conservative limit {max_bytes} bytes")

    if info["animated"] and not mode["animation_allowed"]:
        checks.append({"name": "animation", "ok": False, "value": "animated"})
        errors.append("animation is not allowed for selected mode")
    else:
        checks.append({"name": "animation", "ok": True, "value": "animated" if info["animated"] else "static"})

    if info["animated"] and mode["animation_allowed"]:
        manual = mode.get("animation_manual_checks", [])
        warnings.append("animated creative requires manual timing/frame-rate checks: " + "; ".join(manual))

    return {
        **info,
        "mode": mode_name,
        "pack": pack_name,
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "warnings": warnings,
        "checks": checks,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate Google uploaded display image files")
    parser.add_argument("files", nargs="+", type=Path)
    parser.add_argument(
        "--mode",
        default="demand_gen_uploaded_display",
        choices=["demand_gen_uploaded_display", "uploaded_display_general"],
    )
    parser.add_argument("--pack", default=None, choices=["core", "full"])
    parser.add_argument("--json", action="store_true", help="Print JSON only")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    config = load_config()
    pack = args.pack or config["modes"][args.mode]["default_pack"]
    results = [validate(path, args.mode, pack, config) for path in args.files]

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for result in results:
            print(f"[{result['status']}] {result['path']}")
            if "dimension" in result:
                print(f"  {result['dimension']} | {result['bytes']} bytes | {result['detected_format']} | {'animated' if result['animated'] else 'static'}")
            for error in result.get("errors", []):
                print(f"  ERROR: {error}")
            for warning in result.get("warnings", []):
                print(f"  WARN: {warning}")

    return 0 if all(r["status"] == "PASS" for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
