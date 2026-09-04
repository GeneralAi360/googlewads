#!/usr/bin/env python3
"""Create and verify a synthetic seven-format Google core-pack demo run.

This fixture uses synthetic copy and imagery only. It exists to prove the local
production pipeline, not to demonstrate campaign performance.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent


def load_script(name: str):
    path = HERE / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def create_demo_hero(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    image = Image.new("RGB", (1200, 800), "#E9DED1")
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 520, 800), fill="#D5C1AA")
    draw.rectangle((520, 0, 1200, 800), fill="#F5EFE8")
    draw.rounded_rectangle((700, 145, 1020, 665), radius=36, fill="#7D5E48")
    draw.rounded_rectangle((760, 210, 960, 595), radius=24, fill="#E6C98D")
    draw.ellipse((650, 620, 1070, 720), fill="#CBB8A5")
    image.save(path, "JPEG", quality=90, optimize=True)
    return path


def fill_specs(matrix: dict[str, Any], dispatch_dir: Path, hero_path: Path, font_path: str) -> None:
    specs_dir = dispatch_dir / "render-specs"
    for row in matrix["banner_matrix"]:
        spec_path = specs_dir / f"{row['job_id']}.json"
        spec = json.loads(spec_path.read_text(encoding="utf-8"))
        family = row["layout_family"]
        copy = {
            "headline": "Кухни на заказ",
            "support": "Синтетический demo-подзаголовок",
            "offer": "DEMO OFFER",
            "cta": "Рассчитать",
        }
        if family == "micro_horizontal":
            copy["headline"] = "Кухни на заказ"
            copy["support"] = None
            copy["offer"] = None
        spec.update(
            {
                "background": {"color": "#F5EFE8"},
                "hero": {
                    "path": hero_path.as_posix(),
                    "focal_point": [0.78, 0.5],
                    "mode": "full_bleed" if family == "micro_horizontal" else "slot",
                },
                "logo": {"brand_name": "DEMO", "clearspace_ratio": 0.08},
                "copy": copy,
                "brand": {
                    "font_regular": font_path,
                    "font_bold": font_path,
                    "text_color": "#1A1715",
                    "muted_text_color": "#4F4740",
                    "accent_color": "#D5AE62",
                    "cta_fill": "#1A1715",
                    "cta_text": "#FFFFFF",
                    "offer_fill": "#E6C98D",
                    "offer_text": "#1A1715",
                },
                "lighting": (
                    {
                        "copy_scrim": {
                            "enabled": True,
                            "side": "left",
                            "color": "#FFFFFF",
                            "max_opacity": 190,
                            "extent": 0.75,
                        }
                    }
                    if family == "micro_horizontal"
                    else {
                        "hero_edge_glow": {
                            "enabled": True,
                            "target_slot": "hero",
                            "color": "#FFFFFF",
                            "opacity": 45,
                            "expand_px": 6,
                            "blur": 6,
                        }
                    }
                ),
                "qa": {"min_cta_contrast": 4.5},
                "provenance": {
                    "brand_id": "demo-brand",
                    "creative_contract_id": "demo-C01",
                    "hero_asset_id": "demo-hero-01",
                    "reference_dna_ids": [],
                    "source_grounding_ids": ["synthetic-demo-fixture"],
                    "lighting_scheme_id": None,
                },
                "output": {
                    "path": row["output_path"],
                    "format": "jpg",
                    "target_max_bytes": 150000,
                    "jpeg_quality": 90,
                    "min_jpeg_quality": 68,
                },
            }
        )
        spec_path.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def run_demo(out_dir: Path) -> dict[str, Any]:
    out_dir.mkdir(parents=True, exist_ok=True)
    matrix_module = load_script("build_banner_matrix")
    materializer = load_script("materialize_banner_jobs")
    renderer = load_script("render_banner")
    pack_runner = load_script("render_banner_pack")

    config = matrix_module.load_formats()
    sizes = matrix_module.resolve_sizes(config, "core", None)
    matrix = matrix_module.build_matrix(
        run_id="demo-core",
        concepts=1,
        sizes=sizes,
        variants=1,
        languages=["ru"],
        output_format="jpg",
        output_root=(out_dir / "outputs").as_posix(),
        config=config,
    )
    matrix["brand_id"] = "demo-brand"
    matrix["spec_snapshot_date"] = config.get("snapshot_date")
    matrix_path = out_dir / "banner-matrix.json"
    matrix_path.write_text(json.dumps(matrix, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    dispatch_dir = out_dir / "dispatch"
    materializer.materialize(matrix, dispatch_dir)
    hero_path = create_demo_hero(out_dir / "assets" / "demo-hero.jpg")
    fill_specs(matrix, dispatch_dir, hero_path, renderer.resolve_font_path(None))

    result = pack_runner.render_pack(
        matrix,
        dispatch_dir / "render-specs",
        mode="demand_gen_uploaded_display",
        pack="core",
        contact_sheet=out_dir / "contact-sheet.png",
        manifest_path=out_dir / "output-manifest.json",
    )
    report_path = out_dir / "pack-report.json"
    report_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the synthetic seven-format banner production demo")
    parser.add_argument("--out-dir", type=Path, default=Path("demo-output"))
    args = parser.parse_args()
    result = run_demo(args.out_dir)
    print(json.dumps({"status": result["status"], "output": args.out_dir.as_posix()}, ensure_ascii=False))
    return 0 if result["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
