#!/usr/bin/env python3
"""Build a deterministic banner-job matrix for uploaded display production.

This helper does not design banners. It turns explicit run dimensions into one
job row per concept × size × variant × language so the controller can dispatch
fresh, narrow banner-worker contexts without losing output-count traceability.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FORMATS_PATH = ROOT / "config" / "google-formats.json"


class MatrixError(ValueError):
    pass


def load_formats() -> dict[str, Any]:
    return json.loads(FORMATS_PATH.read_text(encoding="utf-8"))


def parse_csv(value: str) -> list[str]:
    items = [part.strip() for part in value.split(",") if part.strip()]
    if not items:
        raise MatrixError("list value cannot be empty")
    return items


def concept_ids(count: int) -> list[str]:
    if count < 1:
        raise MatrixError("concept count must be >= 1")
    return [f"C{i:02d}" for i in range(1, count + 1)]


def variant_ids(count: int) -> list[str]:
    if count < 1:
        raise MatrixError("variant count must be >= 1")
    return [f"V{i:02d}" for i in range(1, count + 1)]


def safe_language_token(language: str) -> str:
    token = re.sub(r"[^A-Za-z0-9_-]+", "-", language.strip()).strip("-")
    if not token:
        raise MatrixError(f"invalid language token: {language!r}")
    return token


def resolve_sizes(config: dict[str, Any], pack: str | None, sizes: list[str] | None) -> list[str]:
    if pack and sizes:
        raise MatrixError("use either --pack or --sizes, not both")
    if pack:
        try:
            return list(config["packs"][pack])
        except KeyError as exc:
            raise MatrixError(f"unknown pack: {pack}") from exc
    if sizes:
        unknown = [size for size in sizes if size not in config["formats"]]
        if unknown:
            raise MatrixError("unsupported sizes: " + ", ".join(unknown))
        return sizes
    return list(config["packs"]["core"])


def build_matrix(*, run_id: str, concepts: int, sizes: list[str], variants: int, languages: list[str], output_format: str, output_root: str, config: dict[str, Any]) -> dict[str, Any]:
    if not run_id.strip():
        raise MatrixError("run_id cannot be empty")

    output_format = output_format.lower().lstrip(".")
    if output_format == "jpeg":
        output_format = "jpg"
    if output_format not in {"png", "jpg", "gif"}:
        raise MatrixError("output format must be png, jpg/jpeg, or gif")

    c_ids = concept_ids(concepts)
    v_ids = variant_ids(variants)
    lang_tokens = [(lang, safe_language_token(lang)) for lang in languages]

    rows: list[dict[str, Any]] = []
    for concept_id in c_ids:
        for size in sizes:
            fmt = config["formats"][size]
            for variant_id in v_ids:
                for language, lang_token in lang_tokens:
                    job_id = f"{concept_id}-S{size}-{variant_id}-L{lang_token}"
                    output_path = Path(output_root) / run_id / job_id / f"{job_id}.{output_format}"
                    rows.append({
                        "job_id": job_id,
                        "concept_id": concept_id,
                        "variant_id": variant_id,
                        "language": language,
                        "width": fmt["width"],
                        "height": fmt["height"],
                        "dimension": size,
                        "layout_family": fmt["family"],
                        "google_name": fmt["google_name"],
                        "output_format": output_format,
                        "output_path": output_path.as_posix(),
                        "review_status": "NOT_STARTED",
                        "validation_status": "NOT_STARTED",
                        "status": "PLANNED",
                    })

    expected = concepts * len(sizes) * variants * len(languages)
    if len(rows) != expected:
        raise AssertionError("matrix row count does not match output math")

    return {
        "run_id": run_id,
        "concept_count": concepts,
        "size_count": len(sizes),
        "variant_count": variants,
        "language_count": len(languages),
        "sizes": sizes,
        "languages": languages,
        "output_format": output_format,
        "output_math": {
            "formula": "concept_count * size_count * variant_count * language_count",
            "total": expected,
        },
        "expected_output_files": expected,
        "banner_matrix": rows,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build one deterministic job row per banner output.")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--concepts", type=int, required=True)
    parser.add_argument("--pack", choices=["core", "full"])
    parser.add_argument("--sizes", help="Comma-separated explicit Google uploaded-display sizes, e.g. 300x250,728x90")
    parser.add_argument("--variants", type=int, default=1)
    parser.add_argument("--languages", default="ru")
    parser.add_argument("--format", default="png", dest="output_format")
    parser.add_argument("--output-root", default="outputs")
    parser.add_argument("--out", type=Path)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    config = load_formats()
    try:
        explicit_sizes = parse_csv(args.sizes) if args.sizes else None
        sizes = resolve_sizes(config, args.pack, explicit_sizes)
        languages = parse_csv(args.languages)
        result = build_matrix(
            run_id=args.run_id,
            concepts=args.concepts,
            sizes=sizes,
            variants=args.variants,
            languages=languages,
            output_format=args.output_format,
            output_root=args.output_root,
            config=config,
        )
    except MatrixError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    payload = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(payload + "\n", encoding="utf-8")
    else:
        print(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
