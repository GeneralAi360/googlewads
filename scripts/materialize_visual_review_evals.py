#!/usr/bin/env python3
"""Canonical entrypoint for materializing hidden-key visual-review eval jobs.

The implementation lives in `materialize_visual_eval_jobs.py`. This wrapper keeps
the SKILL-facing command explicit without duplicating eval logic.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
TARGET = HERE / "materialize_visual_eval_jobs.py"


def _load():
    spec = importlib.util.spec_from_file_location("materialize_visual_eval_jobs", TARGET)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {TARGET}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    return _load().main()


if __name__ == "__main__":
    raise SystemExit(main())
