#!/usr/bin/env python3
"""Materialize one read-only review task per banner plus one pack-review task."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


class ReviewMaterializeError(ValueError):
    pass


def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ReviewMaterializeError(f"file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ReviewMaterializeError(f"invalid JSON {path}: {exc}") from exc


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_qa_views(path: Path | None) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    if path is None:
        return {}, {}
    payload = load_json(path)
    jobs = payload.get("jobs")
    if not isinstance(jobs, list):
        raise ReviewMaterializeError("design QA index requires jobs list")
    by_job: dict[str, dict[str, Any]] = {}
    for item in jobs:
        job_id = item.get("job_id")
        if not isinstance(job_id, str) or not job_id:
            raise ReviewMaterializeError("design QA index contains empty job_id")
        if job_id in by_job:
            raise ReviewMaterializeError(f"duplicate design QA job: {job_id}")
        by_job[job_id] = item
    return payload, by_job


def _validate_qa_item(job_id: str, item: dict[str, Any], qa_item: dict[str, Any]) -> dict[str, str]:
    if qa_item.get("source_sha256") != item.get("sha256"):
        raise ReviewMaterializeError(f"stale design QA diagnostics for {job_id}")
    views = qa_item.get("views") or {}
    required_views = ("actual", "grayscale", "squint", "thumbnail_board")
    missing_views = [name for name in required_views if not views.get(name)]
    if missing_views:
        raise ReviewMaterializeError(f"design QA diagnostics missing views for {job_id}: " + ", ".join(missing_views))
    if Path(str(views["actual"])).as_posix() != Path(str(item.get("path"))).as_posix():
        raise ReviewMaterializeError(f"design QA actual view does not match manifest output for {job_id}")
    missing_files = [name for name in required_views if not Path(str(views[name])).is_file()]
    if missing_files:
        raise ReviewMaterializeError(f"design QA diagnostic files missing for {job_id}: " + ", ".join(missing_files))
    return {name: str(views[name]) for name in required_views}


def materialize_reviews(
    matrix: dict[str, Any],
    manifest: dict[str, Any],
    out_dir: Path,
    *,
    manifest_path: Path | None = None,
    contact_sheet_path: Path | None = None,
    qa_index_path: Path | None = None,
    force: bool = False,
) -> dict[str, Any]:
    rows = matrix.get("banner_matrix")
    files = manifest.get("files")
    if not isinstance(rows, list) or not rows:
        raise ReviewMaterializeError("banner_matrix must be a non-empty list")
    if not isinstance(files, list) or not files:
        raise ReviewMaterializeError("manifest files must be a non-empty list")
    by_job = {item.get("job_id"): item for item in files}
    if len(by_job) != len(files) or None in by_job:
        raise ReviewMaterializeError("manifest job IDs must be non-empty and unique")
    missing = [row["job_id"] for row in rows if row["job_id"] not in by_job]
    if missing:
        raise ReviewMaterializeError("manifest missing jobs: " + ", ".join(missing))

    required_manifest_identity = (
        "campaign_design_system_id", "campaign_design_system_sha256", "idea_architecture_id",
        "visual_character_signature_id", "lighting_intent_id",
    )
    missing_identity = [key for key in required_manifest_identity if not manifest.get(key)]
    if missing_identity:
        raise ReviewMaterializeError("manifest missing frozen design identity: " + ", ".join(missing_identity))

    qa_payload, qa_by_job = _load_qa_views(qa_index_path)
    if qa_by_job:
        qa_missing = [row["job_id"] for row in rows if row["job_id"] not in qa_by_job]
        if qa_missing:
            raise ReviewMaterializeError("design QA index missing jobs: " + ", ".join(qa_missing))

    tasks_dir = out_dir / "banner-review-tasks"
    reports_dir = out_dir / "banner-review-reports"
    tasks_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)
    jobs = []
    for row in rows:
        item = by_job[row["job_id"]]
        task_path = tasks_dir / f"{row['job_id']}.md"
        report_path = reports_dir / f"{row['job_id']}.review.json"
        if not force and (task_path.exists() or report_path.exists()):
            raise ReviewMaterializeError(f"refusing to overwrite review files for {row['job_id']}")

        for key in required_manifest_identity:
            if item.get(key) != manifest.get(key):
                raise ReviewMaterializeError(f"{row['job_id']}: file-level {key} differs from pack manifest")

        qa_section = ""
        qa_item = qa_by_job.get(row["job_id"])
        if qa_item:
            views = _validate_qa_item(row["job_id"], item, qa_item)
            qa_section = f"""
## Diagnostic review views
These are **diagnostic-only derivatives** of the exact output. They are not delivery assets and must not replace inspection of the original.
- Actual output: `{views['actual']}`
- 25% glance board: `{views['thumbnail_board']}`
- Grayscale hierarchy: `{views['grayscale']}`
- Squint/blur hierarchy: `{views['squint']}`

Use them to test whether hierarchy survives small-view, luminance-only, and blurred-mass inspection. Do not infer CTR or a universal design law from these diagnostics.
"""

        task = f"""# Independent design review — {row['job_id']}

## Immutable reviewed artifact
- Output: `{item['path']}`
- SHA-256: `{item['sha256']}`
- Dimension: `{row['width']}x{row['height']}`
- Layout family: `{row['layout_family']}`
- Concept: `{row.get('concept_id')}`
- Variant: `{row.get('variant_id')}`
- Language: `{row.get('language')}`
- Idea architecture: `{manifest['idea_architecture_id']}`
- Visual character: `{manifest['visual_character_signature_id']}`
- Lighting intent: `{manifest['lighting_intent_id']}`
- Campaign design system: `{manifest['campaign_design_system_id']}`
- Campaign design system SHA-256: `{manifest['campaign_design_system_sha256']}`
- Review report target: `{report_path.as_posix()}`
{qa_section}
## Context boundary
Review this banner read-only in a fresh independent context when the host supports it. The controller must provide only the frozen creative contract, campaign design system, idea architecture, visual-character signature, lighting intent, brand context, relevant REFERENCE_DNA and this exact artifact. Do not modify the banner. Do not create child agents.

## Mandatory checks
- concept fidelity
- **idea fidelity**: the artifact still communicates the frozen core idea and single takeaway
- **emotional fidelity**: the artifact expresses the approved primary emotional target and does not drift into avoided tones
- **visual-character fidelity**: the design remains inside the approved character coordinates/vocabulary rather than becoming a generic style
- **campaign-design-system fidelity**: grid, hero, crop, headline/offer/CTA/brand behavior, whitespace and adaptation follow the frozen campaign system
- brand fidelity
- asset quality
- professional category fit
- visual hierarchy / primary AOI
- **lighting-intent fidelity**: scene/composition lighting serves the approved idea, emotion, primary AOI and copy-safe strategy
- lighting/focal guidance: no decorative hotspot/glow steals priority
- typography and actual-size legibility
- 25% glance/thumbnail behavior when diagnostics exist
- grayscale hierarchy when diagnostics exist
- squint/blur hierarchy when diagnostics exist
- color/contrast
- information density
- crop/safe zones
- CTA clarity
- anti-generic-AI / anti-template quality
- actual-size inspection

Write a report matching `schemas/banner-review.schema.json`. `reviewed_output_sha256` must equal `{item['sha256']}`. A changed output requires a new review.
"""
        task_path.write_text(task, encoding="utf-8")
        jobs.append({
            "job_id": row["job_id"], "task_path": task_path.as_posix(), "report_path": report_path.as_posix(),
            "output_sha256": item["sha256"], "design_qa_attached": bool(qa_item),
        })

    pack_task_path = out_dir / "pack-review-task.md"
    pack_report_path = out_dir / "pack-review.json"
    if not force and (pack_task_path.exists() or pack_report_path.exists()):
        raise ReviewMaterializeError("refusing to overwrite pack review files")
    manifest_hash = (
        sha256_file(manifest_path)
        if manifest_path and manifest_path.is_file()
        else hashlib.sha256(json.dumps(manifest, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
    )
    pack_task_path.write_text(
        f"""# Independent pack review

- Manifest SHA-256: `{manifest_hash}`
- Expected files: `{len(rows)}`
- Idea architecture: `{manifest['idea_architecture_id']}`
- Visual character: `{manifest['visual_character_signature_id']}`
- Lighting intent: `{manifest['lighting_intent_id']}`
- Campaign design system: `{manifest['campaign_design_system_id']}`
- Contact sheet: `{contact_sheet_path.as_posix() if contact_sheet_path else 'CONTROLLER_MUST_PROVIDE'}`
- Design QA index: `{qa_index_path.as_posix() if qa_index_path else 'NOT_PROVIDED'}`
- Report target: `{pack_report_path.as_posix()}`

Review the whole pack read-only after all individual banner reviews pass. Check missing/duplicate files, cross-size concept, **idea**, emotional and visual-character consistency, frozen campaign-design-system consistency, brand/category/asset quality, cross-size **lighting-intent** fidelity, deliberate recomposition, small-format simplification and contact-sheet quality. Different aspect ratios may recompose geometry but must preserve the approved system. Do not fix files. Write `schemas/pack-review.schema.json`. A changed manifest requires a new pack review.
""",
        encoding="utf-8",
    )
    index = {
        "expected_banner_reviews": len(rows), "banner_reviews": jobs,
        "pack_review_task": pack_task_path.as_posix(), "pack_review_report": pack_report_path.as_posix(),
        "manifest_sha256": manifest_hash,
        "campaign_design_system_id": manifest["campaign_design_system_id"],
        "idea_architecture_id": manifest["idea_architecture_id"],
        "visual_character_signature_id": manifest["visual_character_signature_id"],
        "lighting_intent_id": manifest["lighting_intent_id"],
        "design_qa_index": qa_index_path.as_posix() if qa_index_path else None,
        "design_qa_attached": bool(qa_payload),
    }
    index_path = out_dir / "review-index.json"
    index_path.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return index


def main() -> int:
    parser = argparse.ArgumentParser(description="Materialize independent review tasks for a passing banner pack")
    parser.add_argument("--matrix", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--contact-sheet", type=Path)
    parser.add_argument("--qa-index", type=Path)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    try:
        result = materialize_reviews(load_json(args.matrix), load_json(args.manifest), args.out_dir, manifest_path=args.manifest, contact_sheet_path=args.contact_sheet, qa_index_path=args.qa_index, force=args.force)
    except ReviewMaterializeError as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, ensure_ascii=False))
        return 2
    print(json.dumps({"status": "READY_FOR_REVIEW", "index": (args.out_dir / "review-index.json").as_posix(), "reviews": result["expected_banner_reviews"], "design_qa_attached": result["design_qa_attached"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
