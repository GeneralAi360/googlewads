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


def materialize_reviews(
    matrix: dict[str, Any],
    manifest: dict[str, Any],
    out_dir: Path,
    *,
    manifest_path: Path | None = None,
    contact_sheet_path: Path | None = None,
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
        task = f"""# Independent design review — {row['job_id']}

## Immutable reviewed artifact
- Output: `{item['path']}`
- SHA-256: `{item['sha256']}`
- Dimension: `{row['width']}x{row['height']}`
- Layout family: `{row['layout_family']}`
- Concept: `{row.get('concept_id')}`
- Variant: `{row.get('variant_id')}`
- Language: `{row.get('language')}`
- Review report target: `{report_path.as_posix()}`

## Context boundary
Review this banner read-only in a fresh independent context when the host supports it. The controller must provide only the frozen creative contract, brand/design context, relevant REFERENCE_DNA, lighting directive and this artifact. Do not modify the banner. Do not create child agents. Do not inspect unrelated concepts unless needed for a controller-approved cross-size check.

## Mandatory checks
- concept fidelity
- brand fidelity
- visual hierarchy
- lighting/focal guidance
- typography and actual-size legibility
- color/contrast
- information density
- crop/safe zones
- CTA clarity
- actual-size inspection

Write a report matching `schemas/banner-review.schema.json`. `reviewed_output_sha256` must equal `{item['sha256']}`. A changed output requires a new review.
"""
        task_path.write_text(task, encoding="utf-8")
        jobs.append({"job_id": row["job_id"], "task_path": task_path.as_posix(), "report_path": report_path.as_posix(), "output_sha256": item["sha256"]})

    pack_task_path = out_dir / "pack-review-task.md"
    pack_report_path = out_dir / "pack-review.json"
    if not force and (pack_task_path.exists() or pack_report_path.exists()):
        raise ReviewMaterializeError("refusing to overwrite pack review files")
    manifest_hash = sha256_file(manifest_path) if manifest_path and manifest_path.is_file() else hashlib.sha256(json.dumps(manifest, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
    pack_task_path.write_text(
        f"""# Independent pack review

- Manifest SHA-256: `{manifest_hash}`
- Expected files: `{len(rows)}`
- Contact sheet: `{contact_sheet_path.as_posix() if contact_sheet_path else 'CONTROLLER_MUST_PROVIDE'}`
- Report target: `{pack_report_path.as_posix()}`

Review the whole pack read-only after all individual banner reviews pass. Check missing/duplicate files, cross-size concept and brand consistency, deliberate layout adaptation, small-format simplification, and the contact sheet at representative display size. Do not fix files. Write `schemas/pack-review.schema.json`. A changed manifest requires a new pack review.
""",
        encoding="utf-8",
    )
    index = {
        "expected_banner_reviews": len(rows),
        "banner_reviews": jobs,
        "pack_review_task": pack_task_path.as_posix(),
        "pack_review_report": pack_report_path.as_posix(),
        "manifest_sha256": manifest_hash,
    }
    index_path = out_dir / "review-index.json"
    index_path.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return index


def main() -> int:
    parser = argparse.ArgumentParser(description="Materialize independent review tasks for a passing banner pack")
    parser.add_argument("--matrix", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--contact-sheet", type=Path)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    try:
        matrix = load_json(args.matrix)
        manifest = load_json(args.manifest)
        result = materialize_reviews(matrix, manifest, args.out_dir, manifest_path=args.manifest, contact_sheet_path=args.contact_sheet, force=args.force)
    except ReviewMaterializeError as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, ensure_ascii=False))
        return 2
    print(json.dumps({"status": "READY_FOR_REVIEW", "index": (args.out_dir / 'review-index.json').as_posix(), "reviews": result['expected_banner_reviews']}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
