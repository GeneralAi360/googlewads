#!/usr/bin/env python3
"""Create a synthetic seven-format Google core-pack production demo.

The demo exercises the canonical deterministic path through:
intake -> run freeze -> matrix -> job materialization -> approved creative/art-direction
freeze -> per-job binding -> render -> Google technical preflight -> manifest ->
diagnostic design-QA views -> independent review-task materialization.

It deliberately stops before fabricating DESIGN_REVIEWER/PACK_REVIEWER reports. All
business facts and imagery are synthetic fixtures.
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


def complete_demo_context() -> dict[str, Any]:
    return {
        "formats": {"mode": "demand_gen_uploaded_display", "pack": "core"},
        "deliverables": {
            "concept_count": 1,
            "variant_count": 1,
            "languages": ["ru"],
            "output_format": "jpg",
        },
        "business": {"product_service": "Synthetic demo kitchens", "geography": "Minsk"},
        "campaign": {
            "objective": "lead",
            "landing_page": "https://example.invalid/demo",
            "funnel_stage": "product-aware",
            "primary_action": "request quote",
        },
        "audience": {"primary": "Synthetic homeowners"},
        "offer": {
            "primary_value_proposition": "Synthetic custom-kitchen proposition",
            "price": None,
            "proof_points": [],
            "cta": "Рассчитать",
        },
        "constraints": {"legal_disclaimers": [], "prohibited_claims": []},
        "brand": {
            "brand_id": "demo-brand",
            "no_formal_system": True,
            "no_logo_asset": True,
            "allow_font_fallback": True,
            "allow_run_local_palette": True,
            "real_photos": [],
            "ai_hero_allowed": True,
            "people_faces_policy": "not required",
            "additional_rules": [],
            "prohibited_elements": [],
        },
        "visual": {
            "hero_subject": "product",
            "mood": "clean premium",
            "material_lighting": None,
            "lighting_style": None,
            "copy_safe_zone": "layout-family dependent",
            "effect_policy": "restrained",
        },
        "production": {"approval_step": False, "confidentiality_restrictions": None},
    }


def demo_creative_contract() -> dict[str, Any]:
    return {
        "concept_id": "C01",
        "status": "APPROVED",
        "angle": "offer-led synthetic demo",
        "audience_state": "product-aware",
        "primary_proposition": "Synthetic custom-kitchen proposition",
        "supporting_proof": None,
        "visual_idea": "Clean product-led kitchen hero with copy-safe region",
        "primary_aoi": "product hero",
        "scan_path": ["product hero", "headline", "cta", "brand"],
        "brand_id": "demo-brand",
        "art_direction": {
            "mode": "ART_DIRECTION_LOCKED",
            "art_direction_id": "AD-DEMO-CLEAN-PREMIUM",
            "visual_thesis": "Warm restrained product-led commercial composition",
            "selection_provenance": "BRAND_LOCKED",
            "representative_preview_id": None,
            "selected_from_candidate_ids": [],
            "alignment_logic": "copy and action grouped away from dominant product mass",
            "graphic_device": "single product hero with restrained tonal accents",
            "image_treatment": "clean warm commercial product image",
            "whitespace_character": "restrained and breathable",
            "anti_template_exclusions": ["random glass cards", "decorative blobs", "unmotivated neon glow"],
        },
        "reference_dna_ids": [],
        "lighting": {
            "lighting_scheme_id": None,
            "scene_directive": "soft warm directional product light",
            "composition_directive": "restrained copy separation only",
        },
        "source_grounding": [
            {"source_id": "synthetic-demo-fixture", "supports": "all synthetic demo proposition/copy"}
        ],
        "variants": [
            {
                "variant_id": "V01",
                "test_hypothesis": "pipeline baseline only; no performance claim",
                "visual_direction_override": None,
                "copy_by_language": {
                    "ru": {
                        "headline": "Кухни на заказ",
                        "support": "Синтетический demo-подзаголовок",
                        "offer": "DEMO OFFER",
                        "cta": "Рассчитать",
                    }
                },
                "copy_overrides_by_layout_family": {
                    "micro_horizontal": {"support": None, "offer": None}
                },
            }
        ],
    }


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


def create_and_freeze_creative(matrix: dict[str, Any], out_dir: Path, freeze_module) -> tuple[Path, dict[str, Any]]:
    contracts_dir = out_dir / "creative-contracts"
    contracts_dir.mkdir(parents=True, exist_ok=True)
    contract_path = contracts_dir / "C01.creative.json"
    contract_path.write_text(json.dumps(demo_creative_contract(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    freeze_path = out_dir / "creative-freeze.json"
    creative_freeze = freeze_module.freeze_contracts(matrix, contracts_dir, freeze_path)
    return contracts_dir, creative_freeze


def complete_bound_specs(matrix: dict[str, Any], dispatch_dir: Path, hero_path: Path, font_path: str) -> None:
    specs_dir = dispatch_dir / "render-specs"
    for row in matrix["banner_matrix"]:
        spec_path = specs_dir / f"{row['job_id']}.json"
        spec = json.loads(spec_path.read_text(encoding="utf-8"))
        family = row["layout_family"]
        provenance = dict(spec.get("provenance") or {})
        provenance["hero_asset_id"] = "demo-hero-01"
        spec.update(
            {
                "background": {"color": "#F5EFE8"},
                "hero": {
                    "path": hero_path.as_posix(),
                    "focal_point": [0.78, 0.5],
                    "mode": "full_bleed" if family == "micro_horizontal" else "slot",
                },
                "logo": {"brand_name": "DEMO", "clearspace_ratio": 0.08},
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
                "provenance": provenance,
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
    run_freeze = load_script("freeze_banner_run")
    materializer = load_script("materialize_banner_jobs")
    creative_freezer = load_script("freeze_creative_contracts")
    creative_apply = load_script("apply_creative_contracts")
    creative_validate = load_script("validate_creative_bindings")
    renderer = load_script("render_banner")
    pack_runner = load_script("render_banner_pack")
    qa_builder = load_script("build_design_qa_views")
    review_materializer = load_script("materialize_review_jobs")

    freeze_result = run_freeze.freeze_context(
        complete_demo_context(),
        run_id="demo-core",
        out_dir=out_dir / "freeze",
        output_root=(out_dir / "outputs").as_posix(),
    )
    matrix = freeze_result["matrix"]
    dispatch_dir = out_dir / "dispatch"
    materializer.materialize(matrix, dispatch_dir)

    contracts_dir, creative_freeze = create_and_freeze_creative(matrix, out_dir, creative_freezer)
    creative_apply.apply(
        matrix,
        creative_freeze,
        contracts_dir,
        dispatch_dir / "render-specs",
        out_index=out_dir / "creative-bindings.json",
    )
    binding_report = creative_validate.validate(
        matrix,
        creative_freeze,
        contracts_dir,
        dispatch_dir / "render-specs",
    )
    if binding_report["status"] != "CREATIVE_BINDING_PASS":
        raise RuntimeError(f"synthetic creative binding failed: {binding_report}")

    hero_path = create_demo_hero(out_dir / "assets" / "demo-hero.jpg")
    complete_bound_specs(matrix, dispatch_dir, hero_path, renderer.resolve_font_path(None))

    manifest_path = out_dir / "output-manifest.json"
    contact_sheet_path = out_dir / "contact-sheet.png"
    result = pack_runner.render_pack(
        matrix,
        dispatch_dir / "render-specs",
        mode=freeze_result["freeze"]["google_mode"],
        pack="core",
        contact_sheet=contact_sheet_path,
        manifest_path=manifest_path,
        require_creative_binding=True,
    )
    if result["status"] == "PASS":
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        qa_index = qa_builder.build_views(manifest, out_dir / "design-qa")
        review_index = review_materializer.materialize_reviews(
            matrix,
            manifest,
            out_dir / "review",
            manifest_path=manifest_path,
            contact_sheet_path=contact_sheet_path,
            qa_index_path=Path(qa_index["index_path"]),
        )
        result["design_qa_index"] = qa_index["index_path"]
        result["review_index"] = (out_dir / "review" / "review-index.json").as_posix()
        result["expected_review_tasks"] = review_index["expected_banner_reviews"]
        result["independent_review_reports_fabricated"] = False

    result["freeze_path"] = freeze_result["freeze_path"]
    result["creative_freeze_path"] = (out_dir / "creative-freeze.json").as_posix()
    result["creative_binding_status"] = binding_report["status"]
    result["intake_status"] = freeze_result["intake"]["status"]
    report_path = out_dir / "pack-report.json"
    report_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the synthetic intake-to-review-dispatch banner production demo")
    parser.add_argument("--out-dir", type=Path, default=Path("demo-output"))
    args = parser.parse_args()
    result = run_demo(args.out_dir)
    print(json.dumps({"status": result["status"], "output": args.out_dir.as_posix()}, ensure_ascii=False))
    return 0 if result["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
