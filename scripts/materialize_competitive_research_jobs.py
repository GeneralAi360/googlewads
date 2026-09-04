#!/usr/bin/env python3
"""Materialize narrow read-only competitor/ad-library research tasks from a research plan."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


class CompetitiveResearchMaterializeError(ValueError):
    pass


def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        raise CompetitiveResearchMaterializeError(f"cannot read JSON {path}: {exc}") from exc


def materialize(plan: dict[str, Any], out_dir: Path, *, force: bool = False) -> dict[str, Any]:
    research_id = plan.get("research_id")
    category = plan.get("category")
    targets = plan.get("targets")
    if not isinstance(research_id, str) or not research_id:
        raise CompetitiveResearchMaterializeError("research_id is required")
    if not isinstance(category, str) or not category:
        raise CompetitiveResearchMaterializeError("category is required")
    if not isinstance(targets, list) or not targets:
        raise CompetitiveResearchMaterializeError("targets must be a non-empty list")

    tasks_dir = out_dir / "tasks"
    reports_dir = out_dir / "reports"
    tasks_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)
    seen: set[str] = set()
    jobs = []
    for target in targets:
        if not isinstance(target, dict):
            raise CompetitiveResearchMaterializeError("each target must be an object")
        target_id = target.get("target_id")
        query = target.get("advertiser_or_query")
        if not isinstance(target_id, str) or not target_id or target_id in seen:
            raise CompetitiveResearchMaterializeError("target IDs must be non-empty and unique")
        seen.add(target_id)
        if not isinstance(query, str) or not query:
            raise CompetitiveResearchMaterializeError(f"{target_id}: advertiser_or_query is required")
        source_priority = target.get("source_priority") or ["GOOGLE_ADS_TRANSPARENCY", "LINKEDIN_AD_LIBRARY", "OTHER"]
        task_path = tasks_dir / f"{target_id}.md"
        report_path = reports_dir / f"{target_id}.research.json"
        if not force and (task_path.exists() or report_path.exists()):
            raise CompetitiveResearchMaterializeError(f"refusing to overwrite research files for {target_id}")
        task_path.write_text(
            f"""# Competitive creative research — {target_id}\n\n"
            f"Research ID: `{research_id}`\n"
            f"Category: `{category}`\n"
            f"Target/query: `{query}`\n"
            f"Source priority: `{json.dumps(source_priority, ensure_ascii=False)}`\n"
            f"Report target: `{report_path.as_posix()}`\n\n"
            "## Role boundary\n"
            "Work read-only in a fresh `COMPETITOR_RESEARCHER` context when available. Do not design banners. Do not modify campaign facts. Do not copy competitor identity.\n\n"
            "## Research behavior\n"
            "Prefer real current ads from official ad libraries/transparency tools. Use specialist intelligence/swipe services or competitor pages only as secondary evidence. Record source URLs and what is actually observable.\n\n"
            "For every relevant creative capture commercial angle, hero type, composition, typography, palette/contrast, CTA treatment, whitespace/density, trust signals, image/UI/illustration treatment, lighting when meaningful, transferable principles and literal elements not to copy.\n\n"
            "## Performance evidence\n"
            "Assign exactly one tier: A_VERIFIED_OWN_METRICS, B_PUBLISHED_CASE_METRICS, C_PLATFORM_PERFORMANCE_SIGNAL, D_MARKET_PROXY, or E_DESIGN_REFERENCE_ONLY. Never call D/E evidence high-converting. Tier C is only a platform performance signal. A/B may support conversion claims only when the cited metric is actually conversion-related.\n\n"
            "Return structured JSON facts to the controller; do not synthesize final art direction.\n",
            encoding="utf-8",
        )
        jobs.append({"target_id": target_id, "task_path": task_path.as_posix(), "report_path": report_path.as_posix(), "advertiser_or_query": query})

    index = {"research_id": research_id, "category": category, "expected_reports": len(jobs), "jobs": jobs}
    index_path = out_dir / "competitive-research-dispatch.json"
    index_path.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return index


def main() -> int:
    p = argparse.ArgumentParser(description="Materialize one read-only competitive creative research task per target")
    p.add_argument("--plan", type=Path, required=True)
    p.add_argument("--out-dir", type=Path, required=True)
    p.add_argument("--force", action="store_true")
    a = p.parse_args()
    try:
        result = materialize(load_json(a.plan), a.out_dir, force=a.force)
    except CompetitiveResearchMaterializeError as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, ensure_ascii=False))
        return 2
    print(json.dumps({"status": "READY_FOR_RESEARCH", "jobs": result["expected_reports"], "index": (a.out_dir / "competitive-research-dispatch.json").as_posix()}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
