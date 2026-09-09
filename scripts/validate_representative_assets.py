#!/usr/bin/env python3
"""Validate representative-design assets against the frozen design brief requirements."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from PIL import Image


class RepresentativeAssetError(ValueError):
    pass


def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise RepresentativeAssetError(f"file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise RepresentativeAssetError(f"invalid JSON {path}: {exc}") from exc


def canonical_sha(value: dict[str, Any]) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _image_dimensions(path: Path) -> tuple[int, int] | None:
    try:
        with Image.open(path) as image:
            return image.size
    except Exception:
        return None


def validate_assets(design_brief: dict[str, Any], manifest: dict[str, Any]) -> dict[str, Any]:
    brief_id = design_brief.get("design_brief_id")
    if not isinstance(brief_id, str) or not brief_id:
        raise RepresentativeAssetError("design_brief_id is required")
    brief_sha = canonical_sha(design_brief)
    if manifest.get("design_brief_id") != brief_id or manifest.get("design_brief_sha256") != brief_sha:
        raise RepresentativeAssetError("asset manifest is stale or bound to a different design brief")

    requirements = design_brief.get("required_assets")
    if not isinstance(requirements, list):
        raise RepresentativeAssetError("design brief required_assets must be a list")
    req_by_id = {}
    for req in requirements:
        if not isinstance(req, dict) or not req.get("asset_id"):
            raise RepresentativeAssetError("every required_assets item needs asset_id")
        if req["asset_id"] in req_by_id:
            raise RepresentativeAssetError(f"duplicate required asset id: {req['asset_id']}")
        req_by_id[req["asset_id"]] = req

    assets = manifest.get("assets")
    if not isinstance(assets, list):
        raise RepresentativeAssetError("asset manifest assets must be a list")
    asset_by_id = {}
    for asset in assets:
        if not isinstance(asset, dict) or not asset.get("asset_id"):
            raise RepresentativeAssetError("every asset manifest item needs asset_id")
        if asset["asset_id"] in asset_by_id:
            raise RepresentativeAssetError(f"duplicate asset manifest id: {asset['asset_id']}")
        asset_by_id[asset["asset_id"]] = asset

    issues: list[dict[str, str]] = []
    ready_assets: list[dict[str, Any]] = []
    for asset_id, req in req_by_id.items():
        asset = asset_by_id.get(asset_id)
        if asset is None:
            if req.get("required"):
                issues.append({"asset_id": asset_id, "code": "MISSING", "message": "required asset is missing"})
            continue
        if asset.get("role") != req.get("role"):
            issues.append({"asset_id": asset_id, "code": "ROLE_MISMATCH", "message": "asset role differs from design brief"})
            continue
        source_type = asset.get("source_type")
        accepted_sources = set(req.get("accepted_source_types") or [])
        if source_type not in accepted_sources:
            issues.append({"asset_id": asset_id, "code": "SOURCE_NOT_APPROVED", "message": f"source_type {source_type!r} is not approved"})
            continue
        if (asset.get("generated_substitute") or source_type == "GENERATED") and not req.get("generated_substitute_allowed", False):
            issues.append({"asset_id": asset_id, "code": "GENERATED_SUBSTITUTE_FORBIDDEN", "message": "generated substitute is forbidden for this asset"})
            continue

        path_value = asset.get("path")
        if not isinstance(path_value, str) or not path_value:
            issues.append({"asset_id": asset_id, "code": "PATH_MISSING", "message": "asset path is missing"})
            continue
        path = Path(path_value)
        if not path.is_file():
            issues.append({"asset_id": asset_id, "code": "FILE_MISSING", "message": f"asset file not found: {path}"})
            continue
        digest = sha256_file(path)
        if asset.get("sha256") != digest:
            issues.append({"asset_id": asset_id, "code": "STALE_HASH", "message": "asset SHA-256 is stale or mismatched"})
            continue
        if req.get("privacy_review_required") and not asset.get("privacy_checked"):
            issues.append({"asset_id": asset_id, "code": "PRIVACY_NOT_CHECKED", "message": "privacy review is required"})
            continue
        if req.get("rights_approval_required") and asset.get("rights_status") != "APPROVED":
            issues.append({"asset_id": asset_id, "code": "RIGHTS_NOT_APPROVED", "message": "usage rights are not approved"})
            continue

        min_w = req.get("min_width")
        min_h = req.get("min_height")
        dimensions = _image_dimensions(path) if (min_w or min_h) else None
        if (min_w or min_h) and dimensions is None:
            issues.append({"asset_id": asset_id, "code": "DIMENSIONS_UNCHECKABLE", "message": "required raster dimensions could not be inspected"})
            continue
        if dimensions:
            width, height = dimensions
            if min_w and width < int(min_w):
                issues.append({"asset_id": asset_id, "code": "LOW_RESOLUTION", "message": f"width {width} < required {min_w}"})
                continue
            if min_h and height < int(min_h):
                issues.append({"asset_id": asset_id, "code": "LOW_RESOLUTION", "message": f"height {height} < required {min_h}"})
                continue
        ready_assets.append({"asset_id": asset_id, "path": path.as_posix(), "sha256": digest, "role": asset.get("role")})

    brand_lock = design_brief.get("brand_identity_lock") or {}
    if brand_lock.get("logo_asset_required"):
        required_logo_ids = [req["asset_id"] for req in requirements if req.get("required") and req.get("role") == "LOGO"]
        if not required_logo_ids:
            issues.append({"asset_id": "BRAND_LOGO", "code": "LOGO_REQUIREMENT_MISSING", "message": "brand identity lock requires a real logo asset requirement"})

    missing_ids = sorted({item["asset_id"] for item in issues})
    status = "ASSETS_READY" if not issues else "NEEDS_ASSET"
    return {
        "status": status,
        "design_brief_id": brief_id,
        "design_brief_sha256": brief_sha,
        "required_asset_count": sum(1 for req in requirements if req.get("required")),
        "ready_asset_count": len(ready_assets),
        "ready_assets": ready_assets,
        "missing_asset_ids": missing_ids,
        "issues": issues,
    }


def main() -> int:
    p = argparse.ArgumentParser(description="Validate assets required before representative banner rendering")
    p.add_argument("--design-brief", type=Path, required=True)
    p.add_argument("--asset-manifest", type=Path, required=True)
    p.add_argument("--out", type=Path)
    a = p.parse_args()
    try:
        result = validate_assets(load_json(a.design_brief), load_json(a.asset_manifest))
    except RepresentativeAssetError as exc:
        result = {"status": "FAIL_INPUT", "error": str(exc)}
    payload = json.dumps(result, ensure_ascii=False, indent=2)
    if a.out:
        a.out.parent.mkdir(parents=True, exist_ok=True)
        a.out.write_text(payload + "\n", encoding="utf-8")
    else:
        print(payload)
    return 0 if result.get("status") == "ASSETS_READY" else 2


if __name__ == "__main__":
    raise SystemExit(main())
