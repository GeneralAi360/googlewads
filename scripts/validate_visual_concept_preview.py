#!/usr/bin/env python3
"""Validate a user-facing rendered banner concept without weakening production asset gates.

A visual concept shown to the user must be a complete banner composite. Raw image-generation
outputs are component assets only and cannot pass this gate as the final concept artifact.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from PIL import Image


class VisualConceptPreviewError(ValueError):
    pass


def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise VisualConceptPreviewError(f"file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise VisualConceptPreviewError(f"invalid JSON {path}: {exc}") from exc


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _validate_raster(path: Path, declared_width: Any, declared_height: Any) -> tuple[int, int, str]:
    try:
        with Image.open(path) as image:
            actual_width, actual_height = image.size
            image_format = str(image.format or "").upper()
    except Exception as exc:  # Pillow raises multiple image-decoding exception types
        raise VisualConceptPreviewError(f"visual concept artifact is not a decodable raster image: {path}") from exc

    if not isinstance(declared_width, int) or not isinstance(declared_height, int):
        raise VisualConceptPreviewError("preview width/height must be integers")
    if (actual_width, actual_height) != (declared_width, declared_height):
        raise VisualConceptPreviewError(
            f"visual concept raster dimensions {actual_width}x{actual_height} do not match declared {declared_width}x{declared_height}"
        )
    if image_format not in {"PNG", "JPEG"}:
        raise VisualConceptPreviewError(f"user-facing static concept must be PNG/JPEG, got {image_format or 'unknown'}")
    return actual_width, actual_height, image_format


def _validate_composition_contract(preview: dict[str, Any], artifact_path: Path) -> dict[str, Any]:
    if preview.get("artifact_role") != "BANNER_COMPOSITE":
        raise VisualConceptPreviewError("user-facing visual concept artifact_role must be BANNER_COMPOSITE")
    if preview.get("render_stage") != "USER_FACING_CONCEPT_COMPOSITE":
        raise VisualConceptPreviewError("render_stage must be USER_FACING_CONCEPT_COMPOSITE")

    contract = preview.get("composition_contract")
    if not isinstance(contract, dict):
        raise VisualConceptPreviewError("composition_contract is required")
    method = contract.get("composition_method")
    if method not in {
        "DETERMINISTIC_COMPOSITOR",
        "HTML_SCREENSHOT_COMPOSITE",
        "DESIGN_TOOL_COMPOSITE",
        "IMAGE_GENERATION_PLUS_COMPOSITOR",
    }:
        raise VisualConceptPreviewError("unsupported composition_method")

    visible = contract.get("mandatory_visible_elements")
    if not isinstance(visible, dict):
        raise VisualConceptPreviewError("composition_contract.mandatory_visible_elements is required")
    for key in ("primary_message", "commercial_job_cue", "cta", "brand_anchor"):
        if not str(visible.get(key) or "").strip():
            raise VisualConceptPreviewError(f"mandatory_visible_elements.{key} is required")

    raw_paths = contract.get("raw_generated_asset_paths")
    if not isinstance(raw_paths, list) or any(not str(item).strip() for item in raw_paths):
        raise VisualConceptPreviewError("raw_generated_asset_paths must be a list of non-empty paths")
    if contract.get("raw_generated_asset_is_final_artifact") is not False:
        raise VisualConceptPreviewError("raw_generated_asset_is_final_artifact must be false")

    normalized_artifact = artifact_path.resolve()
    for raw in raw_paths:
        try:
            raw_path = Path(str(raw)).resolve()
        except Exception as exc:
            raise VisualConceptPreviewError(f"invalid raw generated asset path: {raw}") from exc
        if raw_path == normalized_artifact:
            raise VisualConceptPreviewError(
                "raw/generated hero asset cannot be the user-facing banner concept; compose typography/CTA/brand first"
            )

    return {
        "composition_method": method,
        "mandatory_visible_elements": visible,
        "raw_generated_asset_count": len(raw_paths),
    }


def validate(preview: dict[str, Any]) -> dict[str, Any]:
    if preview.get("status") != "VISUAL_CONCEPT_RENDERED":
        raise VisualConceptPreviewError("preview status must be VISUAL_CONCEPT_RENDERED")

    artifact_path = Path(str(preview.get("artifact_path") or ""))
    if not artifact_path.is_file():
        raise VisualConceptPreviewError(f"visual concept preview artifact not found: {artifact_path}")
    actual_sha = sha256_file(artifact_path)
    if preview.get("artifact_sha256") != actual_sha:
        raise VisualConceptPreviewError("visual concept preview artifact SHA-256 is stale or mismatched")

    concept_id = str(preview.get("visual_concept_id") or "").strip()
    if not concept_id:
        raise VisualConceptPreviewError("visual_concept_id is required")
    commercial_job_id = str(preview.get("commercial_job_id") or "").strip()
    if not commercial_job_id:
        raise VisualConceptPreviewError("commercial_job_id is required")

    composition = _validate_composition_contract(preview, artifact_path)
    actual_width, actual_height, image_format = _validate_raster(
        artifact_path, preview.get("width"), preview.get("height")
    )

    scope = preview.get("approval_scope")
    if scope not in {"EXACT_PRODUCTION_ARTIFACT", "VISUAL_SYSTEM_WITH_ASSET_SLOTS"}:
        raise VisualConceptPreviewError("unsupported approval_scope")

    slots = preview.get("asset_slots")
    if not isinstance(slots, list):
        raise VisualConceptPreviewError("asset_slots must be a list")

    surrogate_modes = {
        "REFERENCE_ONLY_SURROGATE",
        "LOW_RES_AUTHENTIC_SURROGATE",
        "STRUCTURAL_PLACEHOLDER",
        "TEXT_BRAND_PLACEHOLDER",
    }
    allowed_modes = surrogate_modes | {"PRODUCTION_ASSET"}
    has_surrogate = False
    for slot in slots:
        if not isinstance(slot, dict):
            raise VisualConceptPreviewError("every asset slot must be an object")
        mode = slot.get("preview_mode")
        if mode not in allowed_modes:
            raise VisualConceptPreviewError(f"unsupported preview asset mode: {mode}")
        if slot.get("generated_fake_asset") is not False:
            raise VisualConceptPreviewError("generated fake UI/logo/assets are forbidden in concept previews")
        if mode in surrogate_modes:
            has_surrogate = True
            if slot.get("production_ready") is not False:
                raise VisualConceptPreviewError("surrogate asset slots cannot be marked production_ready")
        elif slot.get("production_ready") is not True:
            raise VisualConceptPreviewError("PRODUCTION_ASSET slots must be production_ready")

    readiness = preview.get("production_asset_readiness")
    if readiness not in {"ASSETS_READY", "NEEDS_ASSET"}:
        raise VisualConceptPreviewError("production_asset_readiness must be ASSETS_READY or NEEDS_ASSET")

    if has_surrogate:
        if scope != "VISUAL_SYSTEM_WITH_ASSET_SLOTS":
            raise VisualConceptPreviewError("surrogate assets require VISUAL_SYSTEM_WITH_ASSET_SLOTS approval scope")
        if readiness != "NEEDS_ASSET":
            raise VisualConceptPreviewError("surrogate preview must preserve NEEDS_ASSET production state")
        if preview.get("not_for_delivery") is not True:
            raise VisualConceptPreviewError("surrogate preview must be marked not_for_delivery=true")
    else:
        if scope != "EXACT_PRODUCTION_ARTIFACT":
            raise VisualConceptPreviewError("all-production preview should use EXACT_PRODUCTION_ARTIFACT scope")
        if readiness != "ASSETS_READY":
            raise VisualConceptPreviewError("exact production preview requires ASSETS_READY")

    summary = preview.get("concept_summary") or {}
    for key in (
        "core_idea",
        "commercial_angle",
        "primary_aoi",
        "style_strategy",
        "typography",
        "lighting",
        "adaptation_note",
    ):
        if not str(summary.get(key) or "").strip():
            raise VisualConceptPreviewError(f"concept_summary.{key} is required")
    scan_path = summary.get("scan_path")
    if not isinstance(scan_path, list) or not scan_path or any(not str(item).strip() for item in scan_path):
        raise VisualConceptPreviewError("concept_summary.scan_path must be a non-empty list")

    return {
        "status": "VISUAL_CONCEPT_AWAITING_USER_APPROVAL",
        "visual_concept_id": concept_id,
        "commercial_job_id": commercial_job_id,
        "artifact_role": "BANNER_COMPOSITE",
        "render_stage": "USER_FACING_CONCEPT_COMPOSITE",
        "artifact_path": artifact_path.as_posix(),
        "artifact_sha256": actual_sha,
        "width": actual_width,
        "height": actual_height,
        "image_format": image_format,
        "approval_scope": scope,
        "production_asset_readiness": readiness,
        "contains_nonproduction_surrogates": has_surrogate,
        "composition_method": composition["composition_method"],
        "raw_generated_asset_count": composition["raw_generated_asset_count"],
        "user_can_approve_visual_system": True,
        "full_production_allowed": False,
        "not_for_delivery": bool(preview.get("not_for_delivery")),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate rendered visual concept banner composite and asset-slot semantics")
    parser.add_argument("--preview", type=Path, required=True)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    try:
        result = validate(load_json(args.preview))
    except VisualConceptPreviewError as exc:
        result = {
            "status": "VISUAL_CONCEPT_PREVIEW_INVALID",
            "user_can_approve_visual_system": False,
            "full_production_allowed": False,
            "error": str(exc),
        }
    payload = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(payload + "\n", encoding="utf-8")
    else:
        print(payload)
    return 0 if result.get("status") == "VISUAL_CONCEPT_AWAITING_USER_APPROVAL" else 2


if __name__ == "__main__":
    raise SystemExit(main())
