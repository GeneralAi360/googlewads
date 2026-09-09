#!/usr/bin/env python3
"""Create a review-only contact sheet for a banner pack."""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable

try:
    from PIL import Image, ImageDraw, ImageFont, ImageOps
except ImportError as exc:  # pragma: no cover
    raise SystemExit("Pillow is required. Install dependencies from requirements.txt") from exc


def build_contact_sheet(files: Iterable[Path], out: Path, *, columns: int = 3, cell_width: int = 360, cell_height: int = 280, margin: int = 16, label_height: int = 42) -> Path:
    paths = [Path(p) for p in files]
    if not paths:
        raise ValueError("at least one banner file is required")
    if columns < 1:
        raise ValueError("columns must be >= 1")
    rows = (len(paths) + columns - 1) // columns
    sheet_w = margin + columns * (cell_width + margin)
    sheet_h = margin + rows * (cell_height + label_height + margin)
    sheet = Image.new("RGB", (sheet_w, sheet_h), "#F2F2F2")
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()

    for index, path in enumerate(paths):
        if not path.is_file():
            raise FileNotFoundError(path)
        col = index % columns
        row = index // columns
        x0 = margin + col * (cell_width + margin)
        y0 = margin + row * (cell_height + label_height + margin)
        with Image.open(path) as source:
            image = source.convert("RGB")
            thumb = ImageOps.contain(image, (cell_width, cell_height), Image.Resampling.LANCZOS)
            px = x0 + (cell_width - thumb.width) // 2
            py = y0 + (cell_height - thumb.height) // 2
            sheet.paste(thumb, (px, py))
            draw.rectangle((x0, y0, x0 + cell_width, y0 + cell_height), outline="#CCCCCC", width=1)
            label = f"{path.name}  |  {image.width}x{image.height}"
            draw.text((x0, y0 + cell_height + 10), label, fill="#222222", font=font)

    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out, format="PNG", optimize=True)
    return out


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build a review-only banner contact sheet")
    parser.add_argument("files", nargs="+", type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--columns", type=int, default=3)
    parser.add_argument("--cell-width", type=int, default=360)
    parser.add_argument("--cell-height", type=int, default=280)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    build_contact_sheet(args.files, args.out, columns=args.columns, cell_width=args.cell_width, cell_height=args.cell_height)
    print(args.out.as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
