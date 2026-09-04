#!/usr/bin/env python3
"""Plan user-facing banner intake from the 52-question pool.

The planner does not invent answers. Presence of an explicit JSON field counts
as resolved even when its value is null/false/empty, allowing the controller to
record deliberate answers such as "no proof" or "no formal brand system".
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
POOL_PATH = ROOT / "config" / "intake-question-pool.json"
FORMATS_PATH = ROOT / "config" / "google-formats.json"
MISSING = object()


class IntakeError(ValueError):
    pass


def load_pool() -> dict[str, Any]:
    return json.loads(POOL_PATH.read_text(encoding="utf-8"))


def load_formats() -> dict[str, Any]:
    return json.loads(FORMATS_PATH.read_text(encoding="utf-8"))


def get_path(data: dict[str, Any], path: str):
    current: Any = data
    for part in path.split("."):
        if not isinstance(current, dict) or part not in current:
            return MISSING
        current = current[part]
    return current


def path_present(data: dict[str, Any], path: str) -> bool:
    return get_path(data, path) is not MISSING


def any_path_present(data: dict[str, Any], paths: list[str]) -> bool:
    return any(path_present(data, path) for path in paths)


def reference_items(data: dict[str, Any]) -> list[Any]:
    value = get_path(data, "references.items")
    return value if isinstance(value, list) else []


def condition_active(condition: str, data: dict[str, Any], output_math: dict[str, Any] | None) -> bool:
    if condition == "always":
        return True
    if condition == "raw_count_phrase":
        return path_present(data, "deliverables.raw_banner_count_phrase")
    if condition == "multi_output":
        return bool(output_math and output_math["total"] > 1)
    if condition == "references":
        requested = get_path(data, "references.requested")
        return requested is True or bool(reference_items(data))
    if condition == "multiple_references":
        return len(reference_items(data)) > 1
    if condition == "performance":
        requested = get_path(data, "performance.requested")
        raw = get_path(data, "performance_data")
        return requested is True or (raw is not MISSING and raw is not None)
    if condition == "visual":
        skip = get_path(data, "visual.skip_questions")
        if skip is True:
            return False
        mode = get_path(data, "formats.mode")
        return mode in {"demand_gen_uploaded_display", "uploaded_display_general", "html5"}
    raise IntakeError(f"unknown condition: {condition}")


def resolve_sizes(data: dict[str, Any], formats: dict[str, Any]) -> list[str] | None:
    pack = get_path(data, "formats.pack")
    dimensions = get_path(data, "formats.dimensions")
    if pack is not MISSING and pack not in {None, ""}:
        if pack not in formats["packs"]:
            raise IntakeError(f"unknown Google pack: {pack}")
        return list(formats["packs"][pack])
    if isinstance(dimensions, list) and dimensions:
        unknown = [size for size in dimensions if size not in formats["formats"]]
        if unknown:
            raise IntakeError("unsupported sizes: " + ", ".join(unknown))
        return list(dimensions)
    return None


def positive_int(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int) and value >= 1:
        return value
    return None


def calculate_output_math(data: dict[str, Any], formats: dict[str, Any]) -> dict[str, Any] | None:
    concepts = positive_int(get_path(data, "deliverables.concept_count"))
    variants = positive_int(get_path(data, "deliverables.variant_count"))
    languages = get_path(data, "deliverables.languages")
    sizes = resolve_sizes(data, formats)
    if concepts is None or variants is None or not isinstance(languages, list) or not languages or not sizes:
        return None
    total = concepts * len(sizes) * variants * len(languages)
    return {
        "formula": "concept_count * size_count * variant_count * language_count",
        "concept_count": concepts,
        "size_count": len(sizes),
        "variant_count": variants,
        "language_count": len(languages),
        "sizes": sizes,
        "languages": languages,
        "total": total,
    }


def plan_intake(data: dict[str, Any], *, depth: str = "standard", quick_limit: int = 5) -> dict[str, Any]:
    if depth not in {"quick", "standard", "deep"}:
        raise IntakeError("depth must be quick, standard, or deep")
    pool = load_pool()
    formats = load_formats()
    output_math = calculate_output_math(data, formats)
    states = []
    defaults: list[dict[str, Any]] = []
    explicit_na = set(data.get("not_applicable_questions") or [])

    for question in pool["questions"]:
        qid = question["id"]
        if qid in explicit_na:
            state = "NOT_APPLICABLE"
            reason = "explicit_controller_state"
        elif qid == "Q06" and not path_present(data, "deliverables.raw_banner_count_phrase"):
            state = "NOT_APPLICABLE"
            reason = "no_raw_count_phrase"
        elif question.get("default") == "true_for_multi_output" and condition_active(question["condition"], data, output_math) and not any_path_present(data, question["paths"]):
            state = "RESOLVED"
            reason = "default_true_for_multi_output"
            defaults.append({"path": "deliverables.contact_sheet", "value": True, "question_id": qid})
        elif not condition_active(question["condition"], data, output_math):
            state = "CONDITIONAL"
            reason = "condition_not_active"
        elif any_path_present(data, question["paths"]):
            state = "RESOLVED"
            reason = "explicit_context"
        else:
            state = "MISSING"
            reason = "unresolved"
        states.append({**question, "state": state, "reason": reason})

    production_missing = [item for item in states if item["state"] == "MISSING" and item["gate"] == "production"]
    advisory_missing = [item for item in states if item["state"] == "MISSING" and item["gate"] == "advisory"]
    ambiguous = any(item["id"] == "Q06" and item["state"] == "MISSING" for item in states)

    if ambiguous:
        status = "OUTPUT_COUNT_AMBIGUOUS"
    elif production_missing:
        status = "BRIEF_INCOMPLETE"
    else:
        status = "READY_TO_FREEZE"

    if depth == "quick":
        candidates = production_missing[: max(1, quick_limit)]
    elif depth == "standard":
        candidates = production_missing
    else:
        candidates = production_missing + advisory_missing

    next_questions = [
        {"id": item["id"], "section": item["section"], "text": item["text"], "gate": item["gate"]}
        for item in candidates
    ]

    section_counts: dict[str, dict[str, int]] = {}
    for item in states:
        section_counts.setdefault(item["section"], {state: 0 for state in pool["states"]})
        section_counts[item["section"]][item["state"]] += 1

    return {
        "status": status,
        "depth": depth,
        "question_count": len(states),
        "state_counts": {state: sum(1 for item in states if item["state"] == state) for state in pool["states"]},
        "section_counts": section_counts,
        "production_missing_count": len(production_missing),
        "advisory_missing_count": len(advisory_missing),
        "remaining_unshown_production_questions": max(0, len(production_missing) - len([q for q in next_questions if q["gate"] == "production"])),
        "output_math": output_math,
        "defaulted_values": defaults,
        "next_questions": next_questions,
        "questions": states,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Plan banner intake from partial structured context")
    parser.add_argument("--context", type=Path, required=True)
    parser.add_argument("--depth", choices=["quick", "standard", "deep"], default="standard")
    parser.add_argument("--quick-limit", type=int, default=5)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    try:
        context = json.loads(args.context.read_text(encoding="utf-8"))
        result = plan_intake(context, depth=args.depth, quick_limit=args.quick_limit)
    except (OSError, json.JSONDecodeError, IntakeError) as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    payload = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(payload + "\n", encoding="utf-8")
    else:
        print(payload)
    return 0


if __name__ == "__main__":
    import sys
    raise SystemExit(main())
