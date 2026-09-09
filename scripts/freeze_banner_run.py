#!/usr/bin/env python3
"""Freeze a ready banner intake into an immutable production matrix.

This is the executable production gate between questioning and banner jobs.
It refuses to create a matrix while the intake planner reports material gaps or
ambiguous output math.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
GOOGLE_FORMATS = ROOT / "config" / "google-formats.json"


class FreezeError(ValueError):
    def __init__(self, code: str, message: str, *, intake: dict[str, Any] | None = None):
        super().__init__(message)
        self.code = code
        self.intake = intake


def load_script(name: str):
    path = HERE / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise FreezeError("FAIL_RUNTIME", f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def canonical_json_bytes(value: dict[str, Any]) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sha256_json(value: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def nested(data: dict[str, Any], path: str, default=None):
    current: Any = data
    for part in path.split("."):
        if not isinstance(current, dict) or part not in current:
            return default
        current = current[part]
    return current


def normalize_output_format(value: Any) -> str:
    output_format = str(value or "").lower().lstrip(".")
    if output_format == "jpeg":
        output_format = "jpg"
    if output_format not in {"png", "jpg"}:
        raise FreezeError(
            "UNSUPPORTED_RENDER_FORMAT",
            f"deterministic v0.2 renderer supports png/jpg; got {value!r}",
        )
    return output_format


def freeze_context(
    context: dict[str, Any],
    *,
    run_id: str,
    out_dir: Path,
    output_root: str | None = None,
) -> dict[str, Any]:
    if not run_id.strip():
        raise FreezeError("FAIL_RUN_ID", "run_id cannot be empty")

    intake_module = load_script("plan_banner_intake")
    matrix_module = load_script("build_banner_matrix")
    intake = intake_module.plan_intake(context, depth="standard")
    if intake["status"] != "READY_TO_FREEZE":
        blocker_ids = [item["id"] for item in intake["next_questions"] if item["gate"] == "production"]
        raise FreezeError(
            intake["status"],
            f"intake is not ready to freeze; unresolved production questions: {', '.join(blocker_ids) or 'none listed'}",
            intake=intake,
        )

    google_mode = nested(context, "formats.mode")
    if google_mode not in {"demand_gen_uploaded_display", "uploaded_display_general"}:
        raise FreezeError(
            "UNSUPPORTED_FREEZE_MODE",
            f"static banner freeze supports uploaded-display modes; got {google_mode!r}",
            intake=intake,
        )

    math = intake.get("output_math")
    if not math:
        raise FreezeError("FAIL_OUTPUT_MATH", "READY_TO_FREEZE without output math is inconsistent", intake=intake)

    output_format = normalize_output_format(nested(context, "deliverables.output_format"))
    concepts = int(math["concept_count"])
    variants = int(math["variant_count"])
    sizes = list(math["sizes"])
    languages = list(math["languages"])
    root = output_root or nested(context, "production.output_root") or "outputs"

    google_config = json.loads(GOOGLE_FORMATS.read_text(encoding="utf-8"))
    matrix = matrix_module.build_matrix(
        run_id=run_id,
        concepts=concepts,
        sizes=sizes,
        variants=variants,
        languages=languages,
        output_format=output_format,
        output_root=root,
        config=google_config,
    )
    if matrix["expected_output_files"] != math["total"]:
        raise FreezeError(
            "FAIL_OUTPUT_MATH",
            f"matrix total {matrix['expected_output_files']} != intake total {math['total']}",
            intake=intake,
        )

    out_dir.mkdir(parents=True, exist_ok=True)
    matrix_path = out_dir / "banner-matrix.json"
    if matrix_path.exists() or (out_dir / "run-freeze.json").exists():
        raise FreezeError("FREEZE_ALREADY_EXISTS", f"refusing to overwrite existing freeze in {out_dir}", intake=intake)
    matrix_path.write_text(json.dumps(matrix, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    context_hash = sha256_json(context)
    matrix_hash = sha256_json(matrix)
    freeze = {
        "freeze_id": f"freeze-{run_id}-{context_hash[:12]}",
        "run_id": run_id,
        "status": "FROZEN",
        "frozen_at": utc_now_iso(),
        "google_mode": google_mode,
        "google_spec_snapshot_date": google_config.get("snapshot_date"),
        "google_spec_snapshot_source": "config/google-formats.json",
        "business_brief_id": context.get("business_brief_id"),
        "brand_id": nested(context, "brand.brand_id"),
        "reference_dna_ids": list(nested(context, "references.reference_dna_ids", []) or []),
        "concept_count": concepts,
        "size_count": len(sizes),
        "variant_count": variants,
        "language_count": len(languages),
        "sizes": sizes,
        "languages": languages,
        "output_format": output_format,
        "expected_output_files": matrix["expected_output_files"],
        "intake_status": intake["status"],
        "intake_state_counts": intake["state_counts"],
        "intake_context_sha256": context_hash,
        "matrix_path": matrix_path.as_posix(),
        "matrix_sha256": matrix_hash,
    }
    freeze_path = out_dir / "run-freeze.json"
    freeze_path.write_text(json.dumps(freeze, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"status": "FROZEN", "freeze": freeze, "freeze_path": freeze_path.as_posix(), "matrix": matrix, "intake": intake}


def failure_payload(exc: FreezeError) -> dict[str, Any]:
    payload: dict[str, Any] = {"status": exc.code, "error": str(exc)}
    if exc.intake is not None:
        payload["intake"] = {
            "status": exc.intake.get("status"),
            "state_counts": exc.intake.get("state_counts"),
            "production_missing_count": exc.intake.get("production_missing_count"),
            "next_questions": exc.intake.get("next_questions"),
            "output_math": exc.intake.get("output_math"),
        }
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Freeze a ready banner intake into a production matrix")
    parser.add_argument("--context", type=Path, required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--output-root")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    try:
        context = json.loads(args.context.read_text(encoding="utf-8"))
        result = freeze_context(context, run_id=args.run_id, out_dir=args.out_dir, output_root=args.output_root)
        payload = {"status": result["status"], "freeze_path": result["freeze_path"], "matrix_path": result["freeze"]["matrix_path"], "expected_output_files": result["freeze"]["expected_output_files"]}
        exit_code = 0
    except (OSError, json.JSONDecodeError) as exc:
        payload = {"status": "FAIL_INPUT", "error": str(exc)}
        exit_code = 2
    except FreezeError as exc:
        payload = failure_payload(exc)
        exit_code = 2
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(text + "\n", encoding="utf-8")
    print(text)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
