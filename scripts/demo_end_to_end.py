#!/usr/bin/env python3
"""Create a synthetic seven-format Google core-pack production demo.

Canonical deterministic path:
intake -> run freeze -> competitive research -> category design map -> detailed
design brief -> written art-direction approval -> high-fidelity representative
approval -> PREPRODUCTION_FROZEN -> creative freeze -> per-job binding -> render ->
Google technical preflight -> manifest -> diagnostic design-QA views -> independent
review-task materialization.

It deliberately stops before fabricating DESIGN_REVIEWER/PACK_REVIEWER reports. All
business facts, market observations and imagery are synthetic fixtures.
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
        "production": {"approval_step": True, "confidentiality_restrictions": None},
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
            "mode": "ART_DIRECTION_PREVIEW_3",
            "art_direction_id": "AD-DEMO-CLEAN-PREMIUM",
            "visual_thesis": "Warm restrained product-led commercial composition",
            "selection_provenance": "USER_APPROVED",
            "representative_preview_id": "PREVIEW-DEMO-300x250",
            "selected_from_candidate_ids": ["AD-A", "AD-B", "AD-C"],
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


def create_representative_preview(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    image = Image.new("RGB", (300, 250), "#F5EFE8")
    draw = ImageDraw.Draw(image)
    draw.rectangle((20, 22, 155, 48), fill="#1A1715")
    draw.rectangle((20, 68, 175, 98), fill="#7D5E48")
    draw.rounded_rectangle((20, 170, 120, 205), radius=8, fill="#1A1715")
    draw.rounded_rectangle((178, 34, 280, 210), radius=16, fill="#D5C1AA")
    draw.rounded_rectangle((198, 60, 260, 182), radius=12, fill="#E6C98D")
    image.save(path, "PNG")
    return path


def _write_json(path: Path, value: dict[str, Any]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def create_and_freeze_preproduction(matrix: dict[str, Any], out_dir: Path, freeze_module) -> dict[str, Any]:
    pre = out_dir / "preproduction"
    research = {
        "research_id": "CR-DEMO-001",
        "status": "COMPETITIVE_RESEARCH_COMPLETE",
        "coverage_status": "FULL",
        "degradation_reason": None,
        "category": "synthetic kitchen category",
        "queries": ["synthetic competitor A", "synthetic competitor B"],
        "creatives": [],
        "synthesis": {
            "commercial_patterns": ["clear product proposition"],
            "visual_patterns": ["product-led hero"],
            "trust_patterns": ["real product/space visual"],
            "category_cliches": ["generic decorative clipart"],
            "opportunities": ["clean premium product realism"],
        },
    }
    for index, advertiser in enumerate(("Synthetic A", "Synthetic B", "Synthetic B"), 1):
        research["creatives"].append({
            "creative_id": f"SYN-AD-{index}",
            "advertiser": advertiser,
            "source_type": "OTHER",
            "source_url": f"https://example.invalid/synthetic-ad-{index}",
            "observed_at": None,
            "creative_type": "static_display",
            "commercial_angle": "synthetic category observation",
            "visual_system": {
                "hero_type": "product-led",
                "composition": "copy plus dominant product",
                "typography": "restrained",
                "palette_contrast": "warm neutral",
                "cta_treatment": "single action",
                "whitespace_density": "controlled",
                "trust_signals": ["product realism"],
                "image_treatment": "clean product visualization",
                "lighting": "soft directional",
            },
            "performance_evidence": {
                "tier": "E_DESIGN_REFERENCE_ONLY",
                "note": "synthetic design reference only; no performance inference",
                "conversion_metric_verified": False,
            },
            "transferable_principles": ["product should look mature and category-appropriate"],
            "do_not_copy": ["identity", "literal composition"],
        })
    research_path = _write_json(pre / "competitive-creative-research.json", research)
    research_sha = freeze_module.canonical_sha(research)

    category_map = {
        "category_map_id": "CDM-DEMO-001",
        "research_id": research["research_id"],
        "research_sha256": research_sha,
        "category": research["category"],
        "source_creative_ids": [item["creative_id"] for item in research["creatives"]],
        "mature_category_signals": ["dominant product hero", "restrained commercial hierarchy"],
        "dominant_patterns": ["clear offer + product"],
        "hero_strategies": ["product-led"],
        "trust_signals": ["real product/space read"],
        "category_cliches": ["generic decorative icon"],
        "generic_ai_risks": ["toy 3D icon", "generic AI clipart"],
        "design_opportunities": ["premium product realism with strong whitespace"],
        "performance_interpretation": "Synthetic reference-only fixture; no conversion claim",
    }
    category_path = _write_json(pre / "category-design-map.json", category_map)
    category_sha = freeze_module.canonical_sha(category_map)

    sizes = sorted({row.get("dimension") or f"{row['width']}x{row['height']}" for row in matrix["banner_matrix"]})
    languages = sorted({row["language"] for row in matrix["banner_matrix"]})
    concepts = {row["concept_id"] for row in matrix["banner_matrix"]}
    variants = {row["variant_id"] for row in matrix["banner_matrix"]}
    design_brief = {
        "design_brief_id": "DB-DEMO-001",
        "competitive_research_id": research["research_id"],
        "competitive_research_sha256": research_sha,
        "category_map_id": category_map["category_map_id"],
        "category_map_sha256": category_sha,
        "campaign": {"objective": "lead"},
        "commercial_message": {"primary_proposition": "Synthetic custom-kitchen proposition", "cta": "Рассчитать"},
        "audience": {"primary": "Synthetic homeowners"},
        "brand_context": {"brand_id": "demo-brand"},
        "references": {},
        "art_direction_strategy": {"mode": "ART_DIRECTION_PREVIEW_3", "candidate_count": 3, "representative_format": "300x250"},
        "visual_hierarchy": {"primary_aoi": "product hero", "primary_message": "offer", "secondary_aoi": "headline", "intended_scan_path": ["product hero", "headline", "cta", "brand"], "brand_priority": 4},
        "image_strategy": {"hero_type": "product-led", "product_scale": "dominant", "copy_safe_area_required": True},
        "asset_quality_policy": {
            "reject_low_resolution_assets": True,
            "reject_generic_ai_clipart": True,
            "reject_unapproved_toy_clay_style": True,
            "reject_style_mismatch": True,
            "require_professional_category_fit": True,
            "notes": ["synthetic fixture"],
        },
        "typography": {"character": "restrained commercial"},
        "color": {"strategy": "warm neutral brand-led"},
        "layout": {"strategy": "dominant product mass + grouped copy"},
        "lighting": {"scene": "soft directional", "composition": "restrained separation"},
        "information_density": {"policy": "glance-first"},
        "small_format_policy": {"removal_order": ["support", "offer"]},
        "outputs": {"concept_count": len(concepts), "variant_count": len(variants), "languages": languages, "sizes": sizes, "expected_files": len(matrix["banner_matrix"])},
        "review_requirements": {"actual_size": True, "asset_quality": True, "professional_category_fit": True, "thumbnail": True, "grayscale": True, "squint": True},
    }
    brief_path = _write_json(pre / "design-brief.json", design_brief)
    brief_sha = freeze_module.canonical_sha(design_brief)

    art_approval = {
        "approval_id": "ADA-DEMO-001",
        "status": "APPROVED",
        "approved_by": "USER",
        "approved_at": None,
        "design_brief_id": design_brief["design_brief_id"],
        "design_brief_sha256": brief_sha,
        "selected_direction": {
            "art_direction_id": "AD-DEMO-CLEAN-PREMIUM",
            "label": "Clean Premium Product",
            "candidate_ids": ["AD-A", "AD-B", "AD-C"],
            "visual_thesis": "Warm restrained product-led commercial composition",
            "composition": "copy grouped away from a dominant product mass",
            "hero_strategy": "clean product hero; no generic clipart",
            "typography": "restrained strong commercial hierarchy",
            "palette": "warm neutral with dark action",
            "lighting_image_treatment": "soft directional material light and restrained composition separation",
            "graphic_device": "single product hero with tonal accents",
            "trust_signals": ["product realism"],
            "whitespace_character": "controlled premium",
            "anti_patterns": ["toy 3D icons", "generic AI clipart", "random glass cards"],
        },
        "notes": "Synthetic user-approval fixture",
    }
    art_path = _write_json(pre / "art-direction-approval.json", art_approval)
    art_sha = freeze_module.canonical_sha(art_approval)

    preview_path = create_representative_preview(pre / "representative-300x250.png")
    representative = {
        "approval_id": "RDA-DEMO-001",
        "status": "APPROVED",
        "approved_by": "USER",
        "approved_at": None,
        "art_direction_approval_id": art_approval["approval_id"],
        "art_direction_approval_sha256": art_sha,
        "art_direction_id": art_approval["selected_direction"]["art_direction_id"],
        "preview_id": "PREVIEW-DEMO-300x250",
        "artifact_path": preview_path.as_posix(),
        "artifact_sha256": freeze_module.sha256_file(preview_path),
        "width": 300,
        "height": 250,
        "quality_checks": {key: "PASS" for key in (
            "asset_quality", "professional_category_fit", "hierarchy", "typography", "brand_fidelity",
            "commercial_message_fidelity", "hero_crop", "lighting_contrast", "cta_clarity", "anti_generic_ai",
        )},
        "notes": "Synthetic high-fidelity approval contract fixture",
    }
    representative_path = _write_json(pre / "representative-design-approval.json", representative)

    freeze_path = out_dir / "preproduction-freeze.json"
    return freeze_module.freeze_preproduction(
        matrix,
        research,
        category_map,
        design_brief,
        art_approval,
        representative,
        freeze_path,
        research_path=research_path,
        category_map_path=category_path,
        design_brief_path=brief_path,
        art_approval_path=art_path,
        representative_approval_path=representative_path,
    )


def create_and_freeze_creative(matrix: dict[str, Any], out_dir: Path, freeze_module, preproduction_freeze: dict[str, Any]) -> tuple[Path, dict[str, Any]]:
    contracts_dir = out_dir / "creative-contracts"
    contracts_dir.mkdir(parents=True, exist_ok=True)
    contract_path = contracts_dir / "C01.creative.json"
    contract_path.write_text(json.dumps(demo_creative_contract(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    freeze_path = out_dir / "creative-freeze.json"
    creative_freeze = freeze_module.freeze_contracts(
        matrix,
        contracts_dir,
        freeze_path,
        preproduction_freeze=preproduction_freeze,
    )
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
    preproduction_freezer = load_script("freeze_preproduction_design")
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

    preproduction_freeze = create_and_freeze_preproduction(matrix, out_dir, preproduction_freezer)

    dispatch_dir = out_dir / "dispatch"
    materializer.materialize(matrix, dispatch_dir)

    contracts_dir, creative_freeze = create_and_freeze_creative(matrix, out_dir, creative_freezer, preproduction_freeze)
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
    result["preproduction_freeze_path"] = (out_dir / "preproduction-freeze.json").as_posix()
    result["preproduction_status"] = preproduction_freeze["status"]
    result["preproduction_research_rigor"] = preproduction_freeze["research_rigor"]
    result["creative_freeze_path"] = (out_dir / "creative-freeze.json").as_posix()
    result["creative_preproduction_sha256"] = creative_freeze.get("preproduction_freeze_sha256")
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
