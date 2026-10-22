#!/usr/bin/env python3
"""Validate an exact-SHA USER decision on a Graphic Banner Brief."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


class GraphicBannerBriefDecisionError(ValueError):
    pass


def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise GraphicBannerBriefDecisionError(f"file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise GraphicBannerBriefDecisionError(f"invalid JSON {path}: {exc}") from exc


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate(brief_path: Path, decision: dict[str, Any]) -> dict[str, Any]:
    brief = load_json(brief_path)
    if brief.get("status") != "GRAPHIC_BANNER_BRIEF_READY_FOR_USER_REVIEW":
        raise GraphicBannerBriefDecisionError("brief is not in user-review state")
    brief_id = str(brief.get("brief_id") or "").strip()
    if not brief_id:
        raise GraphicBannerBriefDecisionError("brief_id is missing")

    if decision.get("brief_id") != brief_id:
        raise GraphicBannerBriefDecisionError("decision brief_id mismatch")
    actual_sha = sha256_file(brief_path)
    if decision.get("brief_sha256") != actual_sha:
        raise GraphicBannerBriefDecisionError("decision is bound to stale/different brief bytes")
    if decision.get("decided_by") != "USER":
        raise GraphicBannerBriefDecisionError("only USER may approve or revise the Graphic Banner Brief")

    action = decision.get("decision")
    if action == "APPROVE":
        return {
            "status": "GRAPHIC_BANNER_BRIEF_APPROVED",
            "brief_id": brief_id,
            "brief_sha256": actual_sha,
            "decided_by": "USER",
            "visual_exploration_allowed": True,
            "full_production_allowed": False,
            "next_stage": "FIRST_ROUND_VISUAL_EXPLORATION",
        }
    if action == "REVISE":
        feedback = decision.get("feedback")
        if not isinstance(feedback, str) or not feedback.strip():
            raise GraphicBannerBriefDecisionError("REVISE requires non-empty feedback")
        return {
            "status": "GRAPHIC_BANNER_BRIEF_REVISE_REQUESTED",
            "brief_id": brief_id,
            "brief_sha256": actual_sha,
            "decided_by": "USER",
            "feedback": feedback.strip(),
            "visual_exploration_allowed": False,
            "full_production_allowed": False,
            "next_stage": "REVISE_GRAPHIC_BANNER_BRIEF",
        }
    raise GraphicBannerBriefDecisionError("decision must be APPROVE or REVISE")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate exact-SHA user decision on Graphic Banner Brief")
    parser.add_argument("--brief", type=Path, required=True)
    parser.add_argument("--decision", type=Path, required=True)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    try:
        result = validate(args.brief, load_json(args.decision))
    except GraphicBannerBriefDecisionError as exc:
        result = {
            "status": "GRAPHIC_BANNER_BRIEF_DECISION_INVALID",
            "visual_exploration_allowed": False,
            "full_production_allowed": False,
            "error": str(exc),
        }
    payload = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(payload + "\n", encoding="utf-8")
    else:
        print(payload)
    return 0 if result.get("status") in {"GRAPHIC_BANNER_BRIEF_APPROVED", "GRAPHIC_BANNER_BRIEF_REVISE_REQUESTED"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
