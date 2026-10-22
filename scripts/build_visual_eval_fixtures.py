#!/usr/bin/env python3
"""Materialize synthetic visual-review evaluation artifacts.

These files are intentionally flawed. They are not ad recommendations and are
never upload-ready assets. A fresh visual reviewer should inspect the generated
images without seeing evals/visual-review-evals.json expected findings.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


class EvalFixtureError(ValueError):
    pass


def font(size: int, bold: bool = False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).is_file():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def save(image: Image.Image, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    image.convert("RGB").save(path, "PNG", optimize=True)
    return path


def vr01(path: Path):
    image = Image.new("RGB", (300, 250), "#222222")
    draw = ImageDraw.Draw(image)
    # Alternating local luminance behind the copy zone: intentionally unstable.
    for x in range(0, 300, 30):
        fill = "#F7F7F7" if (x // 30) % 2 == 0 else "#555555"
        draw.rectangle((x, 0, x + 30, 250), fill=fill)
    draw.rounded_rectangle((185, 70, 285, 210), radius=18, fill="#9B6B47")
    draw.text((18, 22), "КУХНИ\nНА ЗАКАЗ", font=font(32, True), fill="#FFFFFF", spacing=3)
    draw.rounded_rectangle((18, 188, 128, 230), radius=10, fill="#111111")
    draw.text((36, 200), "РАСЧЁТ", font=font(15, True), fill="#FFFFFF")
    return save(image, path)


def vr02(path: Path):
    image = Image.new("RGB", (300, 250), "#F1ECE6")
    draw = ImageDraw.Draw(image)
    draw.text((18, 18), "MEGABRAND", font=font(50, True), fill="#111111")
    draw.rounded_rectangle((178, 88, 286, 210), radius=18, fill="#8D674E")
    draw.text((20, 145), "Кухни на заказ", font=font(18, True), fill="#312B27")
    draw.rounded_rectangle((20, 192, 125, 229), radius=9, fill="#312B27")
    draw.text((31, 202), "Рассчитать", font=font(12, True), fill="#FFFFFF")
    return save(image, path)


def vr03(path: Path):
    image = Image.new("RGB", (160, 600), "#EDE7E0")
    draw = ImageDraw.Draw(image)
    # Product is visibly truncated on the right, including the identifying red feature.
    draw.rounded_rectangle((-42, 85, 138, 365), radius=24, fill="#645047")
    draw.rectangle((118, 125, 176, 240), fill="#C82929")
    draw.text((12, 395), "ПРЕМИУМ\nПРОДУКТ", font=font(23, True), fill="#191715", spacing=4)
    draw.rounded_rectangle((12, 515, 148, 565), radius=10, fill="#191715")
    draw.text((30, 531), "ПОДРОБНЕЕ", font=font(13, True), fill="#FFFFFF")
    return save(image, path)


def vr04(path: Path):
    image = Image.new("RGB", (320, 50), "#FBF7F2")
    draw = ImageDraw.Draw(image)
    draw.rectangle((2, 2, 48, 48), fill="#1D1B19")
    draw.text((7, 18), "LOGO", font=font(8, True), fill="#FFFFFF")
    draw.text((54, 3), "Кухни на заказ", font=font(11, True), fill="#171513")
    draw.text((54, 17), "Бесплатный замер", font=font(8), fill="#5B524A")
    draw.rounded_rectangle((154, 3, 211, 22), radius=5, fill="#E7C57C")
    draw.text((161, 8), "-20%", font=font(8, True), fill="#171513")
    draw.ellipse((217, 5, 237, 25), fill="#BC3030")
    draw.text((220, 11), "5", font=font(8, True), fill="#FFFFFF")
    draw.rounded_rectangle((242, 7, 316, 43), radius=7, fill="#171513")
    draw.text((251, 19), "РАСЧЁТ", font=font(9, True), fill="#FFFFFF")
    draw.text((54, 31), "5 лет гарантии • доставка", font=font(7), fill="#6D6259")
    return save(image, path)


def vr05(path: Path):
    image = Image.new("RGB", (336, 280), "#17191E")
    draw = ImageDraw.Draw(image)
    draw.ellipse((245, -55, 380, 80), fill="#FFF5B8")
    draw.rounded_rectangle((122, 54, 230, 198), radius=20, fill="#4B5664")
    draw.text((20, 186), "ТЕХНОЛОГИЯ\nДЛЯ ДОМА", font=font(24, True), fill="#FFFFFF", spacing=3)
    draw.rounded_rectangle((20, 238, 128, 270), radius=8, fill="#20A7E8")
    draw.text((35, 247), "УЗНАТЬ", font=font(12, True), fill="#06121A")
    return save(image, path)


def vr06(root: Path):
    files = []
    configs = [
        ("300x250", (300, 250)),
        ("728x90", (728, 90)),
        ("160x600", (160, 600)),
        ("320x50", (320, 50)),
    ]
    for name, size in configs:
        width, height = size
        drift = name == "728x90"
        bg = "#092A40" if not drift else "#F2D23B"
        text = "#FFFFFF" if not drift else "#222222"
        image = Image.new("RGB", size, bg)
        draw = ImageDraw.Draw(image)
        brand_size = max(10, min(24, height // 5))
        headline_size = max(11, min(28, height // 4))
        draw.text((max(5, width // 30), max(4, height // 10)), "NOVA" if not drift else "NOVA!", font=font(brand_size, True), fill=text)
        draw.text((max(5, width // 30), max(18, height // 2 - headline_size)), "Умный дом", font=font(headline_size, not drift), fill=text)
        button_w = max(70, min(150, width // 4))
        button_h = max(22, min(48, height // 3))
        x1 = width - button_w - max(5, width // 30)
        y1 = height - button_h - max(4, height // 10)
        if drift:
            draw.rectangle((x1, y1, x1 + button_w, y1 + button_h), fill="#E02C46")
        else:
            draw.rounded_rectangle((x1, y1, x1 + button_w, y1 + button_h), radius=max(4, button_h // 3), fill="#1CC4A5")
        draw.text((x1 + 10, y1 + max(4, button_h // 4)), "УЗНАТЬ", font=font(max(9, button_h // 3), True), fill="#08222D" if not drift else "#FFFFFF")
        path = root / f"VR-06-{name}.png"
        save(image, path)
        files.append(path)
    return files


def build(out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)
    generated = {
        "VR-01": [vr01(out_dir / "VR-01-300x250.png")],
        "VR-02": [vr02(out_dir / "VR-02-300x250.png")],
        "VR-03": [vr03(out_dir / "VR-03-160x600.png")],
        "VR-04": [vr04(out_dir / "VR-04-320x50.png")],
        "VR-05": [vr05(out_dir / "VR-05-336x280.png")],
        "VR-06": vr06(out_dir),
    }
    manifest = {
        "status": "VISUAL_EVAL_FIXTURES_READY",
        "warning": "Intentionally flawed synthetic creatives for reviewer evaluation only; not ad recommendations or upload assets.",
        "cases": {
            case_id: [path.as_posix() for path in paths]
            for case_id, paths in generated.items()
        },
    }
    manifest_path = out_dir / "visual-eval-fixtures.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


def main():
    parser = argparse.ArgumentParser(description="Generate intentionally flawed banner images for visual-review evals")
    parser.add_argument("--out-dir", type=Path, default=Path("visual-eval-output"))
    args = parser.parse_args()
    result = build(args.out_dir)
    print(json.dumps({"status": result["status"], "out_dir": args.out_dir.as_posix()}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
