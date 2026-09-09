#!/usr/bin/env python3
"""Deterministic PNG/JPG banner renderer for one banner-matrix job.

The renderer owns exact composition of approved copy/logo/assets. Generative
imagery may be supplied as a hero asset, but critical advertising text is
rendered deterministically.
"""
from __future__ import annotations

import argparse
import json
import os
import statistics
import sys
from pathlib import Path
from typing import Any

try:
    from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps
except ImportError as exc:
    raise SystemExit("Pillow is required; install requirements.txt") from exc

ROOT = Path(__file__).resolve().parents[1]
PRESETS = ROOT / "config" / "layout-presets.json"


class RenderError(ValueError):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code


def load_presets() -> dict[str, Any]:
    return json.loads(PRESETS.read_text(encoding="utf-8"))


def resolve_family(presets: dict[str, Any], family: str) -> dict[str, Any]:
    try:
        current = dict(presets["families"][family])
    except KeyError as exc:
        raise RenderError("FAIL_LAYOUT_FAMILY", f"unknown layout family: {family}") from exc
    parent = current.pop("inherits", None)
    if not parent:
        return current
    base = resolve_family(presets, parent)
    result = dict(base)
    for key, value in current.items():
        if key in {"slots", "text"}:
            result[key] = {**base.get(key, {}), **value}
        else:
            result[key] = value
    return result


def color(value: str) -> tuple[int, ...]:
    if not isinstance(value, str) or not value.startswith("#") or len(value) not in {7, 9}:
        raise RenderError("FAIL_COLOR", f"invalid color: {value!r}")
    try:
        return tuple(int(value[i : i + 2], 16) for i in range(1, len(value), 2))
    except ValueError as exc:
        raise RenderError("FAIL_COLOR", f"invalid color: {value!r}") from exc


def luminance(rgb: tuple[int, ...]) -> float:
    values = []
    for value in rgb[:3]:
        x = value / 255
        values.append(x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4)
    return 0.2126 * values[0] + 0.7152 * values[1] + 0.0722 * values[2]


def contrast_ratio(a: str, b: str) -> float:
    x, y = luminance(color(a)), luminance(color(b))
    high, low = max(x, y), min(x, y)
    return (high + 0.05) / (low + 0.05)


def pixel_contrast(text_color: str, pixel: tuple[int, ...]) -> float:
    x, y = luminance(color(text_color)), luminance(pixel)
    high, low = max(x, y), min(x, y)
    return (high + 0.05) / (low + 0.05)


def resolve_font_path(path: str | None) -> str:
    candidates = [
        path,
        os.getenv("BANNER_FONT_PATH"),
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
    ]
    for candidate in candidates:
        if candidate and Path(candidate).is_file():
            return str(candidate)
    raise RenderError("FAIL_FONT", "provide brand.font_regular or BANNER_FONT_PATH")


def box_px(width: int, height: int, value: list[float] | None) -> tuple[int, int, int, int]:
    if not isinstance(value, list) or len(value) != 4 or value[2] <= 0 or value[3] <= 0:
        raise RenderError("FAIL_LAYOUT", f"bad slot: {value!r}")
    x, y, box_width, box_height = value
    return (
        round(x * width),
        round(y * height),
        round((x + box_width) * width),
        round((y + box_height) * height),
    )


def inset_box(box: tuple[int, int, int, int], amount: int) -> tuple[int, int, int, int]:
    amount = max(0, int(amount))
    left, top, right, bottom = box
    result = left + amount, top + amount, right - amount, bottom - amount
    if result[2] <= result[0] or result[3] <= result[1]:
        raise RenderError("FAIL_LOGO_CLEARSPACE", f"clearspace {amount}px collapses logo slot {box}")
    return result


def expand_box(
    box: tuple[int, int, int, int], amount: int, width: int, height: int
) -> tuple[int, int, int, int]:
    left, top, right, bottom = box
    amount = max(0, int(amount))
    return max(0, left - amount), max(0, top - amount), min(width, right + amount), min(height, bottom + amount)


def union_boxes(boxes: list[tuple[int, int, int, int]]) -> tuple[int, int, int, int]:
    if not boxes:
        raise RenderError("FAIL_LIGHTING", "lighting primitive has no usable target box")
    return (
        min(item[0] for item in boxes),
        min(item[1] for item in boxes),
        max(item[2] for item in boxes),
        max(item[3] for item in boxes),
    )


def wrap(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, max_width: int, max_lines: int) -> list[str] | None:
    words = " ".join(str(text).split()).split()
    lines: list[str] = []
    current = ""
    for word in words:
        if draw.textlength(word, font=font) > max_width:
            return None
        candidate = word if not current else current + " " + word
        if draw.textlength(candidate, font=font) <= max_width:
            current = candidate
        else:
            lines.append(current)
            current = word
            if len(lines) >= max_lines:
                return None
    if current:
        lines.append(current)
    return lines if len(lines) <= max_lines else None


def fit(
    draw: ImageDraw.ImageDraw,
    text: str,
    box: tuple[int, int, int, int],
    font_path: str,
    rules: dict[str, Any],
) -> tuple[ImageFont.FreeTypeFont, int, list[str], int, int, int]:
    left, top, right, bottom = box
    max_width, max_height = max(1, right - left), max(1, bottom - top)
    minimum, maximum = int(rules["min_px"]), int(rules["max_px"])
    max_lines = int(rules.get("max_lines", 1))
    if minimum < 1 or maximum < minimum:
        raise RenderError("FAIL_TEXT_RULE", f"bad text rules: {rules}")
    for size in range(maximum, minimum - 1, -1):
        font = ImageFont.truetype(font_path, size)
        lines = wrap(draw, text, font, max_width, max_lines)
        if lines is None:
            continue
        spacing = max(1, round(size * 0.16))
        rendered = "\n".join(lines)
        bounds = draw.multiline_textbbox((0, 0), rendered, font=font, spacing=spacing)
        rendered_width, rendered_height = bounds[2] - bounds[0], bounds[3] - bounds[1]
        if rendered_width <= max_width and rendered_height <= max_height:
            return font, size, lines, spacing, rendered_width, rendered_height
    raise RenderError("FAIL_COPY_OVERFLOW", f"copy cannot fit at minimum {minimum}px: {text!r}")


def text_in_box(
    canvas: Image.Image,
    text: str,
    box: tuple[int, int, int, int],
    font_path: str,
    rules: dict[str, Any],
    fill: str,
    align: str = "left",
) -> dict[str, Any] | None:
    if not text or not box:
        return None
    draw = ImageDraw.Draw(canvas)
    font, size, lines, spacing, rendered_width, rendered_height = fit(draw, text, box, font_path, rules)
    left, top, right, bottom = box
    y = top + max(0, (bottom - top - rendered_height) // 2)
    x, anchor = left, "la"
    if align == "center":
        x, anchor = left + (right - left) // 2, "ma"
    draw.multiline_text(
        (x, y),
        "\n".join(lines),
        font=font,
        fill=color(fill),
        spacing=spacing,
        align=align,
        anchor=anchor,
    )
    return {
        "text": text,
        "box": list(box),
        "font_size": size,
        "lines": lines,
        "rendered_width": rendered_width,
        "rendered_height": rendered_height,
    }


def paste(
    canvas: Image.Image,
    path: str,
    box: tuple[int, int, int, int],
    mode: str = "cover",
    focal: list[float] | tuple[float, float] = (0.5, 0.5),
) -> None:
    source_path = Path(path)
    if not source_path.is_file():
        raise RenderError("FAIL_ASSET", f"asset not found: {path}")
    with Image.open(source_path) as source:
        size = max(1, box[2] - box[0]), max(1, box[3] - box[1])
        if mode == "cover":
            image = ImageOps.fit(
                source.convert("RGB"),
                size,
                Image.Resampling.LANCZOS,
                centering=(
                    max(0, min(1, float(focal[0]))),
                    max(0, min(1, float(focal[1]))),
                ),
            ).convert("RGBA")
            position = box[:2]
        elif mode == "contain":
            image = source.convert("RGBA")
            image.thumbnail(size, Image.Resampling.LANCZOS)
            position = box[0] + (size[0] - image.width) // 2, box[1] + (size[1] - image.height) // 2
        else:
            raise RenderError("FAIL_ASSET", f"bad fit mode: {mode}")
        canvas.alpha_composite(image, dest=position)


def _target_box(
    item: dict[str, Any],
    slots: dict[str, Any],
    width: int,
    height: int,
    *,
    default_slots: list[str] | None = None,
) -> tuple[int, int, int, int]:
    if item.get("box") is not None:
        return box_px(width, height, item["box"])
    names = item.get("target_slots") or default_slots or []
    if item.get("target_slot"):
        names = [item["target_slot"]]
    boxes = [box_px(width, height, slots[name]) for name in names if slots.get(name)]
    return union_boxes(boxes)


def _composite_mask(canvas: Image.Image, mask: Image.Image, fill: str) -> None:
    overlay = Image.new("RGBA", canvas.size, (*color(fill)[:3], 255))
    overlay.putalpha(mask)
    canvas.alpha_composite(overlay)


def apply_lighting(canvas: Image.Image, cfg: dict[str, Any], slots: dict[str, Any]) -> list[str]:
    width, height = canvas.size
    applied: list[str] = []

    hero_glow = cfg.get("hero_edge_glow") or {}
    if hero_glow.get("enabled"):
        target = _target_box(hero_glow, slots, width, height, default_slots=["hero"])
        expand = int(hero_glow.get("expand_px", max(4, round(min(width, height) * 0.025))))
        outer = expand_box(target, expand, width, height)
        opacity = max(0, min(255, int(hero_glow.get("opacity", 90))))
        radius = max(0, int(hero_glow.get("radius_px", 0)))
        mask = Image.new("L", (width, height), 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle(outer, radius=radius + expand, fill=opacity)
        draw.rounded_rectangle(target, radius=radius, fill=0)
        blur = max(0, int(hero_glow.get("blur", max(4, expand))))
        if blur:
            mask = mask.filter(ImageFilter.GaussianBlur(blur))
        _composite_mask(canvas, mask, hero_glow.get("color", "#FFFFFF"))
        applied.append("hero_edge_glow")

    spotlight = cfg.get("spotlight") or {}
    if spotlight.get("enabled"):
        center_x, center_y = spotlight.get("center", [0.5, 0.4])
        radius_x, radius_y = spotlight.get("radius", [0.35, 0.25])
        mask = Image.new("L", (width, height), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse(
            [
                round((center_x - radius_x) * width),
                round((center_y - radius_y) * height),
                round((center_x + radius_x) * width),
                round((center_y + radius_y) * height),
            ],
            fill=max(0, min(255, int(spotlight.get("opacity", 80)))),
        )
        blur = max(0, int(spotlight.get("blur", max(8, min(width, height) * 0.08))))
        if blur:
            mask = mask.filter(ImageFilter.GaussianBlur(blur))
        _composite_mask(canvas, mask, spotlight.get("color", "#FFFFFF"))
        applied.append("spotlight")

    scrim = cfg.get("copy_scrim") or {}
    if scrim.get("enabled"):
        side = scrim.get("side", "bottom")
        extent = max(0.05, min(1, float(scrim.get("extent", 0.55))))
        opacity = max(0, min(255, int(scrim.get("max_opacity", 128))))
        mask = Image.new("L", (width, height), 0)
        draw = ImageDraw.Draw(mask)
        steps = height if side in {"top", "bottom"} else width
        edge = max(1, round(steps * extent))
        for index in range(edge):
            alpha = round(opacity * (index / max(1, edge - 1)))
            alpha = opacity - alpha if side in {"top", "left"} else alpha
            if side == "bottom":
                draw.line((0, height - edge + index, width, height - edge + index), fill=alpha)
            elif side == "top":
                draw.line((0, index, width, index), fill=alpha)
            elif side == "right":
                draw.line((width - edge + index, 0, width - edge + index, height), fill=alpha)
            elif side == "left":
                draw.line((index, 0, index, height), fill=alpha)
            else:
                raise RenderError("FAIL_LIGHTING", f"bad scrim side: {side}")
        _composite_mask(canvas, mask, scrim.get("color", "#000000"))
        applied.append("copy_scrim")

    vignette = cfg.get("vignette") or {}
    if vignette.get("enabled"):
        opacity = max(0, min(255, int(vignette.get("opacity", 80))))
        softness = max(0.05, min(0.95, float(vignette.get("softness", 0.45))))
        mask = Image.radial_gradient("L").resize((width, height), Image.Resampling.BILINEAR)
        threshold = round(255 * (1 - softness))
        mask = mask.point(
            lambda value: 0 if value < threshold else round(opacity * (value - threshold) / max(1, 255 - threshold))
        )
        _composite_mask(canvas, mask, vignette.get("color", "#000000"))
        applied.append("vignette")

    plate = cfg.get("text_plate") or {}
    if plate.get("enabled"):
        target = _target_box(plate, slots, width, height, default_slots=["headline", "support"])
        padding = max(0, int(plate.get("padding_px", max(3, round(min(width, height) * 0.015)))))
        target = expand_box(target, padding, width, height)
        opacity = max(0, min(255, int(plate.get("opacity", 170))))
        mask = Image.new("L", (width, height), 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle(target, radius=max(0, int(plate.get("radius_px", 8))), fill=opacity)
        _composite_mask(canvas, mask, plate.get("color", "#000000"))
        applied.append("text_plate")

    return applied


def sample_local_contrast(
    canvas: Image.Image,
    box: tuple[int, int, int, int],
    text_color: str,
    *,
    grid: int = 20,
) -> dict[str, Any]:
    left, top, right, bottom = box
    if right <= left or bottom <= top:
        raise RenderError("FAIL_CONTRAST", f"invalid local contrast box: {box}")
    crop = canvas.convert("RGB").crop((left, top, right, bottom))
    sample_width, sample_height = min(grid, crop.width), min(grid, crop.height)
    crop = crop.resize((max(1, sample_width), max(1, sample_height)), Image.Resampling.BOX)
    if hasattr(crop, "get_flattened_data"):
        pixels = list(crop.get_flattened_data())
    else:
        pixels = list(crop.getdata())
    ratios = sorted(pixel_contrast(text_color, pixel) for pixel in pixels)
    local_luminance = [luminance(pixel) for pixel in pixels]
    p10_index = max(0, min(len(ratios) - 1, round((len(ratios) - 1) * 0.10)))
    return {
        "samples": len(ratios),
        "min": round(ratios[0], 3),
        "p10": round(ratios[p10_index], 3),
        "median": round(statistics.median(ratios), 3),
        "mean": round(statistics.fmean(ratios), 3),
        "max": round(ratios[-1], 3),
        "luminance_range": round(max(local_luminance) - min(local_luminance), 4),
    }


def pill(
    canvas: Image.Image,
    text: str,
    box: tuple[int, int, int, int],
    font_path: str,
    rules: dict[str, Any],
    fill: str,
    text_color: str,
    radius: int,
) -> dict[str, Any] | None:
    if not text or not box:
        return None
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle(box, radius=max(0, radius), fill=color(fill))
    left, top, right, bottom = box
    padding = max(2, round(min(right - left, bottom - top) * 0.10))
    return text_in_box(
        canvas,
        text,
        (left + padding, top + padding, right - padding, bottom - padding),
        font_path,
        rules,
        text_color,
        "center",
    )


def save(canvas: Image.Image, path: Path, output: dict[str, Any]) -> dict[str, Any]:
    file_format = output.get("format", path.suffix.lstrip(".") or "png").lower()
    file_format = "jpg" if file_format == "jpeg" else file_format
    target = output.get("target_max_bytes")
    if target is not None and int(target) < 1000:
        raise RenderError("FAIL_FILE_SIZE_RULE", "target_max_bytes < 1000")
    target = int(target) if target else None
    path.parent.mkdir(parents=True, exist_ok=True)

    if file_format == "png":
        canvas.convert("RGB").save(path, "PNG", optimize=True)
        size = path.stat().st_size
        if target and size > target:
            path.unlink(missing_ok=True)
            raise RenderError("FAIL_FILE_SIZE", f"PNG {size} > {target} bytes")
        return {"format": "png", "bytes": size}

    if file_format == "jpg":
        high, low = int(output.get("jpeg_quality", 92)), int(output.get("min_jpeg_quality", 70))
        if not 20 <= low <= high <= 100:
            raise RenderError("FAIL_FILE_SIZE_RULE", "invalid JPEG quality range")
        for quality in range(high, low - 1, -2):
            canvas.convert("RGB").save(path, "JPEG", quality=quality, optimize=True, progressive=True)
            size = path.stat().st_size
            if not target or size <= target:
                return {"format": "jpg", "bytes": size, "jpeg_quality": quality}
        path.unlink(missing_ok=True)
        raise RenderError("FAIL_FILE_SIZE", f"JPEG remains above {target} bytes at quality {low}")

    raise RenderError("FAIL_FORMAT", f"renderer supports png/jpg, got {file_format}")


def render_banner(spec: dict[str, Any]) -> dict[str, Any]:
    required = ["job_id", "width", "height", "layout_family", "copy", "brand", "output"]
    missing = [key for key in required if key not in spec]
    if missing:
        raise RenderError("FAIL_SPEC", "missing: " + ", ".join(missing))

    width, height = int(spec["width"]), int(spec["height"])
    if width < 1 or height < 1:
        raise RenderError("FAIL_DIMENSIONS", "width/height must be positive")

    layout = resolve_family(load_presets(), str(spec["layout_family"]))
    overrides = spec.get("overrides") or {}
    slots = {**layout.get("slots", {}), **(overrides.get("slots") or {})}
    text_rules = dict(layout.get("text", {}))
    for key, value in (overrides.get("text") or {}).items():
        text_rules[key] = {**text_rules.get(key, {}), **value}

    background = (spec.get("background") or {}).get("color", "#FFFFFF")
    canvas = Image.new("RGBA", (width, height), (*color(background)[:3], 255))

    def slot(name: str) -> tuple[int, int, int, int] | None:
        return box_px(width, height, slots[name]) if slots.get(name) else None

    hero = spec.get("hero") or {}
    hero_path = hero.get("path")
    hero_mode = hero.get("mode", layout.get("hero_mode", "slot"))
    if hero_path:
        if hero_mode in {"full_bleed", "full_bleed_optional"}:
            hero_box = (0, 0, width, height)
        else:
            hero_box = slot("hero")
            if hero_box is None:
                raise RenderError("FAIL_LAYOUT", "layout family has no hero slot")
        paste(canvas, hero_path, hero_box, "cover", hero.get("focal_point", [0.5, 0.5]))

    lighting_applied = apply_lighting(canvas, spec.get("lighting") or {}, slots)
    pre_text_canvas = canvas.copy()

    brand = spec.get("brand") or {}
    regular = resolve_font_path(brand.get("font_regular"))
    bold = resolve_font_path(brand.get("font_bold") or regular)
    text_color = brand.get("text_color", "#111111")
    muted_color = brand.get("muted_text_color", text_color)

    elements: dict[str, Any] = {}
    local_contrast: dict[str, Any] = {}

    logo = spec.get("logo") or {}
    logo_slot = slot("logo")
    if (logo.get("path") or logo.get("brand_name")) and logo_slot is None:
        raise RenderError("FAIL_LAYOUT", "layout family has no logo slot")
    if logo_slot is not None and (logo.get("path") or logo.get("brand_name")):
        ratio = float(logo.get("clearspace_ratio", 0) or 0)
        if ratio < 0 or ratio >= 0.5:
            raise RenderError("FAIL_LOGO_CLEARSPACE", "logo.clearspace_ratio must be >= 0 and < 0.5")
        ratio_px = round(min(logo_slot[2] - logo_slot[0], logo_slot[3] - logo_slot[1]) * ratio)
        clearspace_px = max(int(logo.get("clearspace_px", 0) or 0), ratio_px)
        protected_logo_box = inset_box(logo_slot, clearspace_px) if clearspace_px else logo_slot
        if logo.get("path"):
            paste(canvas, logo["path"], protected_logo_box, "contain")
            elements["logo"] = {
                "box": list(protected_logo_box),
                "slot_box": list(logo_slot),
                "clearspace_px": clearspace_px,
                "asset": logo["path"],
            }
        else:
            local_contrast["brand_name"] = sample_local_contrast(pre_text_canvas, protected_logo_box, text_color)
            elements["brand_name"] = text_in_box(
                canvas,
                logo["brand_name"],
                protected_logo_box,
                bold,
                {
                    "min_px": max(8, round(height * 0.035)),
                    "max_px": max(10, round(height * 0.08)),
                    "max_lines": 1,
                },
                text_color,
            )
            elements["brand_name"]["slot_box"] = list(logo_slot)
            elements["brand_name"]["clearspace_px"] = clearspace_px

    copy = spec.get("copy") or {}
    for name, font_path, fill in [("headline", bold, text_color), ("support", regular, muted_color)]:
        if copy.get(name):
            target_box = slot(name)
            if name not in text_rules or target_box is None:
                raise RenderError("FAIL_LAYOUT", f"layout family has no usable {name} slot/rules")
            local_contrast[name] = sample_local_contrast(pre_text_canvas, target_box, fill)
            elements[name] = text_in_box(canvas, copy[name], target_box, font_path, text_rules[name], fill)

    for name in ("offer", "cta"):
        if copy.get(name) and (name not in text_rules or slot(name) is None):
            raise RenderError("FAIL_LAYOUT", f"layout family has no usable {name} slot/rules")

    if copy.get("offer"):
        offer_box = slot("offer")
        assert offer_box is not None
        elements["offer"] = pill(
            canvas,
            copy["offer"],
            offer_box,
            bold,
            text_rules["offer"],
            brand.get("offer_fill", brand.get("accent_color", "#F0EAE2")),
            brand.get("offer_text", text_color),
            int(brand.get("offer_radius_px", max(2, (offer_box[3] - offer_box[1]) // 4))),
        )

    if copy.get("cta"):
        cta_box = slot("cta")
        assert cta_box is not None
        elements["cta"] = pill(
            canvas,
            copy["cta"],
            cta_box,
            bold,
            text_rules["cta"],
            brand.get("cta_fill", brand.get("accent_color", "#111111")),
            brand.get("cta_text", "#FFFFFF"),
            int(brand.get("cta_radius_px", max(2, (cta_box[3] - cta_box[1]) // 5))),
        )

    ratios: dict[str, Any] = {
        "cta_text_vs_fill": (
            round(
                contrast_ratio(
                    brand.get("cta_text", "#FFFFFF"),
                    brand.get("cta_fill", brand.get("accent_color", "#111111")),
                ),
                3,
            )
            if copy.get("cta")
            else None
        ),
        "flat_text_vs_background": None,
        "local_text": local_contrast,
    }
    full_bleed = bool(hero_path and hero_mode in {"full_bleed", "full_bleed_optional"})
    if not full_bleed:
        ratios["flat_text_vs_background"] = round(contrast_ratio(text_color, background), 3)

    qa = spec.get("qa") or {}
    if qa.get("min_cta_contrast") is not None and ratios["cta_text_vs_fill"] is not None:
        if ratios["cta_text_vs_fill"] < float(qa["min_cta_contrast"]):
            raise RenderError(
                "FAIL_CONTRAST",
                f"CTA contrast {ratios['cta_text_vs_fill']}:1 below minimum {qa['min_cta_contrast']}:1",
            )
    if qa.get("min_flat_text_contrast") is not None and ratios["flat_text_vs_background"] is not None:
        if ratios["flat_text_vs_background"] < float(qa["min_flat_text_contrast"]):
            raise RenderError(
                "FAIL_CONTRAST",
                f"flat contrast {ratios['flat_text_vs_background']}:1 below minimum {qa['min_flat_text_contrast']}:1",
            )
    if qa.get("min_local_text_contrast") is not None:
        minimum = float(qa["min_local_text_contrast"])
        failing = {name: metrics["p10"] for name, metrics in local_contrast.items() if metrics["p10"] < minimum}
        if failing:
            details = ", ".join(f"{name}={value}:1" for name, value in failing.items())
            raise RenderError(
                "FAIL_LOCAL_CONTRAST",
                f"10th-percentile local contrast below {minimum}:1: {details}",
            )

    output = spec["output"] or {}
    path = Path(output.get("path", ""))
    if not str(path):
        raise RenderError("FAIL_SPEC", "output.path required")
    saved = save(canvas, path, output)

    return {
        "status": "PASS",
        "job_id": spec["job_id"],
        "width": width,
        "height": height,
        "layout_family": spec["layout_family"],
        "output_path": path.as_posix(),
        "output": saved,
        "elements": elements,
        "lighting_applied": lighting_applied,
        "contrast": ratios,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Render one deterministic banner from a render spec")
    parser.add_argument("--spec", type=Path, required=True)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    try:
        report = render_banner(json.loads(args.spec.read_text(encoding="utf-8")))
    except (OSError, json.JSONDecodeError, RenderError) as exc:
        print(
            json.dumps(
                {"status": "FAIL", "code": getattr(exc, "code", "FAIL_RENDER"), "error": str(exc)},
                ensure_ascii=False,
                indent=2,
            ),
            file=sys.stderr,
        )
        return 2
    payload = json.dumps(report, ensure_ascii=False, indent=2)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(payload + "\n", encoding="utf-8")
    else:
        print(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
