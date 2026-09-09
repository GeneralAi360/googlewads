#!/usr/bin/env python3
"""Create hidden-key-safe visual-review eval tasks from generated artifacts."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


class VisualEvalMaterializeError(ValueError):
    pass


def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise VisualEvalMaterializeError(f"file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise VisualEvalMaterializeError(f"invalid JSON {path}: {exc}") from exc


def task_for(case_id: str, artifacts: list[str], reports_dir: Path) -> dict[str, Any]:
    if not case_id.startswith("VR-"):
        raise VisualEvalMaterializeError(f"invalid case ID: {case_id}")
    if not artifacts:
        raise VisualEvalMaterializeError(f"case {case_id} has no artifacts")
    return {
        "case_id": case_id,
        "role": "DESIGN_REVIEWER",
        "reviewer_context": "fresh_read_only_visual",
        "artifact_paths": artifacts,
        "output_report_path": (reports_dir / f"{case_id}.review.json").as_posix(),
        "instructions": [
            "Inspect the supplied rendered artifact(s) visually at actual size where possible.",
            "Do not modify any artifact.",
            "Identify only issues supported by visible evidence.",
            "For every finding provide severity, a stable descriptive code, evidence, why it matters, smallest correction, and scope.",
            "Do not infer CTR, conversion or universal design laws from the image.",
            "Return JSON matching schemas/visual-review-report.schema.json.",
        ],
        "forbidden_context": [
            "evals/visual-review-evals.json expected_findings",
            "evals/visual-review-evals.json must_not_claim",
            "visual-review score results",
            "another reviewer's answer"
        ]
    }


def materialize(fixtures_manifest: dict[str, Any], out_dir: Path, *, force: bool = False) -> dict[str, Any]:
    cases = fixtures_manifest.get("cases")
    if not isinstance(cases, dict) or not cases:
        raise VisualEvalMaterializeError("fixture manifest must contain cases object")
    tasks_dir = out_dir / "tasks"
    reports_dir = out_dir / "reports"
    tasks_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)
    tasks = []
    for case_id, artifacts in sorted(cases.items()):
        if not isinstance(artifacts, list) or not all(isinstance(item, str) and item for item in artifacts):
            raise VisualEvalMaterializeError(f"bad artifact list for {case_id}")
        task = task_for(case_id, artifacts, reports_dir)
        path = tasks_dir / f"{case_id}.task.json"
        if path.exists() and not force:
            raise VisualEvalMaterializeError(f"refusing to overwrite existing task: {path}")
        path.write_text(json.dumps(task, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        tasks.append({"case_id": case_id, "task_path": path.as_posix(), "output_report_path": task["output_report_path"]})
    index = {
        "status": "VISUAL_EVAL_TASKS_READY",
        "reviewer_context": "fresh_read_only_visual",
        "task_count": len(tasks),
        "tasks": tasks,
        "hidden_key_not_materialized": True
    }
    index_path = out_dir / "visual-eval-dispatch.json"
    index_path.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return index


def main() -> int:
    parser = argparse.ArgumentParser(description="Materialize hidden-key-safe visual-review tasks")
    parser.add_argument("--fixtures", required=True, type=Path)
    parser.add_argument("--out-dir", required=True, type=Path)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    try:
        result = materialize(load_json(args.fixtures), args.out_dir, force=args.force)
    except VisualEvalMaterializeError as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, ensure_ascii=False))
        return 2
    print(json.dumps({"status": result["status"], "task_count": result["task_count"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
