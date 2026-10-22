#!/usr/bin/env python3
"""Build non-delivery diagnostic views for independent visual review.

For each technically passing banner in an output manifest, create:
- grayscale view at exact output dimensions;
- squint/blur view at exact output dimensions;
- 25% thumbnail placed on a neutral review board without upscaling it.

These artifacts are review aids only. They are never Google upload assets and never
replace inspection of the exact original output.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFilter, ImageOps


class QAViewError(ValueError):
    pass


def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise QAViewError(f"file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise QAViewError(f"invalid JSON {path}: {exc}") from exc


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _save_png(image: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, "PNG", optimize=True)


def _thumbnail_board(source: Image.Image, label: str, scale: float = 0.25) -> tuple[Image.Image, tuple[int, int]]:
    if not 0 < scale <= 1:
        raise QAViewError("thumbnail scale must be in (0, 1]")
    preview_size = (
        max(1, round(source.width * scale)),
        max(1, round(source.height * scale)),
    )
    preview = source.convert("RGB").resize(preview_size, Image.Resampling.LANCZOS)
    board_width, board_height = 640, 360
    board = Image.new("RGB", (board_width, board_height), "#F2F2F2")
    draw = ImageDraw.Draw(board)
    x = (board_width - preview.width) // 2
    y = max(52, (board_height - preview.height) // 2)
    board.paste(preview, (x, y))
    draw.text((20, 18), label, fill="#222222")
    draw.text(
        (20, board_height - 28),
        f"25% diagnostic preview: {preview.width}x{preview.height}px inside board",
        fill="#555555",
    )
    return board, preview_size


def build_views(manifest: dict[str, Any], out_dir: Path) -> dict[str, Any]:
    files = manifest.get("files")
    if not isinstance(files, list) or not files:
        raise QAViewError("manifest.files must be a non-empty list")

    records: list[dict[str, Any]] = []
    seen: set[str] = set()
    for item in files:
        job_id = item.get("job_id")
        if not isinstance(job_id, str) or not job_id:
            raise QAViewError("every manifest file needs a non-empty job_id")
        if job_id in seen:
            raise QAViewError(f"duplicate job_id: {job_id}")
        seen.add(job_id)
        if item.get("status") != "PASS":
            raise QAViewError(f"QA views require passing manifest item: {job_id}")

        source_path = Path(str(item.get("path") or ""))
        if not source_path.is_file():
            raise QAViewError(f"output not found for {job_id}: {source_path}")
        actual_sha = sha256_file(source_path)
        expected_sha = item.get("sha256")
        if expected_sha and actual_sha != expected_sha:
            raise QAViewError(f"source hash mismatch for {job_id}")

        job_dir = out_dir / job_id
        grayscale_path = job_dir / "grayscale.png"
        squint_path = job_dir / "squint.png"
        thumbnail_path = job_dir / "thumbnail-board.png"

        with Image.open(source_path) as opened:
            source = opened.convert("RGB")
            grayscale = ImageOps.grayscale(source).convert("RGB")
            blur_radius = max(1.5, min(source.width, source.height) * 0.045)
            squint = source.filter(ImageFilter.GaussianBlur(radius=blur_radius))
            board, preview_size = _thumbnail_board(source, f"{job_id} — glance test")
            _save_png(grayscale, grayscale_path)
            _save_png(squint, squint_path)
            _save_png(board, thumbnail_path)

        records.append(
            {
                "job_id": job_id,
                "source_path": source_path.as_posix(),
                "source_sha256": actual_sha,
                "source_width": int(item.get("width") or 0),
                "source_height": int(item.get("height") or 0),
                "diagnostic_only": True,
                "views": {
                    "actual": source_path.as_posix(),
                    "grayscale": grayscale_path.as_posix(),
                    "squint": squint_path.as_posix(),
                    "thumbnail_board": thumbnail_path.as_posix(),
                },
                "thumbnail_preview_size": list(preview_size),
                "squint_blur_radius": round(float(blur_radius), 3),
            }
        )

    out_dir.mkdir(parents=True, exist_ok=True)
    index = {
        "artifact_role": "DESIGN_QA_DIAGNOSTICS_ONLY",
        "delivery_asset": False,
        "source_manifest_campaign_id": manifest.get("campaign_id"),
        "expected_jobs": len(records),
        "jobs": records,
    }
    index_path = out_dir / "design-qa-index.json"
    index_path.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    index["index_path"] = index_path.as_posix()
    return index


def main() -> int:
    parser = argparse.ArgumentParser(description="Build thumbnail, grayscale, and squint diagnostic views")
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = build_views(load_json(args.manifest), args.out_dir)
    except QAViewError as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, ensure_ascii=False))
        return 2
    print(json.dumps({"status": "PASS", "jobs": result["expected_jobs"], "index": result["index_path"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
