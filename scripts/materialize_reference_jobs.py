#!/usr/bin/env python3
"""Create one narrow read-only REFERENCE_ANALYST task per supplied reference."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


class ReferenceJobError(ValueError):
    pass


def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ReferenceJobError(f"file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ReferenceJobError(f"invalid JSON {path}: {exc}") from exc


def normalize_items(context: dict[str, Any]) -> list[dict[str, str]]:
    references = context.get("references") or {}
    items = references.get("items") or []
    if not isinstance(items, list):
        raise ReferenceJobError("references.items must be a list")
    normalized = []
    ids = set()
    for index, item in enumerate(items, start=1):
        if isinstance(item, str):
            ref_id, source = f"REF{index:02d}", item
        elif isinstance(item, dict):
            source = item.get("source") or item.get("path") or item.get("url")
            ref_id = item.get("reference_id") or item.get("id") or f"REF{index:02d}"
        else:
            raise ReferenceJobError(f"unsupported reference item at index {index}")
        if not isinstance(source, str) or not source.strip():
            raise ReferenceJobError(f"reference {ref_id!r} has no source")
        if not isinstance(ref_id, str) or not ref_id.strip():
            raise ReferenceJobError(f"reference at index {index} has invalid ID")
        if ref_id in ids:
            raise ReferenceJobError(f"duplicate reference ID: {ref_id}")
        ids.add(ref_id)
        normalized.append({"reference_id": ref_id, "source": source})
    return normalized


def materialize(context: dict[str, Any], out_dir: Path, *, force: bool = False) -> dict[str, Any]:
    items = normalize_items(context)
    if not items:
        return {"status": "REFERENCE_NOT_APPLICABLE", "expected_reference_jobs": 0, "jobs": []}
    references = context.get("references") or {}
    liked = references.get("liked_attributes") or []
    disliked = references.get("disliked_attributes") or []
    similarity = references.get("similarity_level")
    primary = references.get("primary_reference")
    mandatory = references.get("mandatory_elements") or []

    task_dir = out_dir / "reference-tasks"
    report_dir = out_dir / "reference-reports"
    task_dir.mkdir(parents=True, exist_ok=True)
    report_dir.mkdir(parents=True, exist_ok=True)
    jobs = []
    for item in items:
        ref_id, source = item["reference_id"], item["source"]
        task_path = task_dir / f"{ref_id}.md"
        report_path = report_dir / f"{ref_id}.reference-dna.json"
        if not force and (task_path.exists() or report_path.exists()):
            raise ReferenceJobError(f"refusing to overwrite reference job {ref_id}")
        task_path.write_text(
            f"""# REFERENCE_ANALYST — {ref_id}

## One-source boundary
Analyze only this supplied reference as visual/design evidence:
- Reference ID: `{ref_id}`
- Source: `{source}`
- Output report: `{report_path.as_posix()}`

## User preference context
- Liked attributes: `{json.dumps(liked, ensure_ascii=False)}`
- Disliked attributes: `{json.dumps(disliked, ensure_ascii=False)}`
- Requested similarity level: `{similarity}`
- Primary reference declared by controller: `{primary}`
- Mandatory reference elements: `{json.dumps(mandatory, ensure_ascii=False)}`

## Required extraction
Describe only what the reference actually supports:
- composition/grid;
- focal object and scan path;
- typography behavior;
- color/contrast;
- whitespace/density;
- CTA treatment;
- subject/product/person scale;
- lighting direction/softness/temperature/reflections/shadows;
- angle/crop;
- mood/brand signals;
- transferable design principles;
- literal elements that must not be copied;
- uncertainties/unobservable points.

## Boundaries
This is a read-only analysis task. Do not create child agents. Do not redesign the banner. Do not invent the referenced business's results, audience, strategy, font name, colors, or conversion performance when they cannot be observed. Do not turn a reference pattern into a universal design law. Do not copy another brand's logo, wording, proprietary identity, or unsupported claims.

Write exactly one JSON report matching `schemas/reference-dna.schema.json`, with `analyst_role=REFERENCE_ANALYST`, `reference_id={ref_id}`, and `source` exactly as supplied.
""",
            encoding="utf-8",
        )
        jobs.append({"reference_id": ref_id, "source": source, "task_path": task_path.as_posix(), "report_path": report_path.as_posix()})
    index = {"status": "READY_FOR_REFERENCE_ANALYSIS", "expected_reference_jobs": len(jobs), "jobs": jobs}
    (out_dir / "reference-index.json").write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return index


def main() -> int:
    parser = argparse.ArgumentParser(description="Materialize one reference-analysis subagent task per supplied reference")
    parser.add_argument("--context", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    try:
        result = materialize(load_json(args.context), args.out_dir, force=args.force)
    except ReferenceJobError as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, ensure_ascii=False))
        return 2
    print(json.dumps({"status": result["status"], "jobs": result["expected_reference_jobs"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
