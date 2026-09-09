# ADR-001 — Deterministic raster renderer baseline

Status: accepted for v0.2 baseline.

## Context

The banner skill needs exact Google dimensions, deterministic spelling and pricing, real font measurement, focal-point crop control, simple lighting overlays, predictable PNG/JPEG export, and explicit file-size failure states. The renderer must also remain usable from one narrow banner-worker job without requiring the worker to own an entire pack.

## Options considered

### HTML/CSS + browser screenshot

Strengths: strong layout primitives, familiar responsive model, broad web typography support.

Costs: browser/runtime dependency, screenshot orchestration, font-loading timing, browser-version drift, and more moving parts for a task whose final artifact is a raster file rather than a live web page.

### SVG + Sharp / Node

Strengths: vector-first composition, deterministic geometry, good raster export, attractive future path for reusable vector templates.

Costs: introduces a Node toolchain next to the current Python validation scripts and complicates a single-runtime portable baseline. Advanced text shaping still depends on font/runtime behavior.

### Python + Pillow

Strengths: exact raster dimensions, image crop/composite, FreeType text measurement, JPEG quality control, PNG optimization, simple gradients/blur/lighting primitives, and easy integration with existing Python tests/validators.

Costs: complex typographic shaping can vary by Pillow build and RAQM availability; CSS-like layout is not native; sophisticated vector effects may require a future extension.

## Decision

Use **Python + Pillow** for the v0.2 deterministic renderer baseline.

The decision is deliberately narrow: Pillow is the precision raster layer, not the creative-strategy layer. Banner workers still decide the concept and may override normalized slots, but the renderer owns exact pixels, approved copy, logo placement, fit checks, composition-lighting primitives, and export.

## Guardrails

- Do not vendor proprietary fonts into this repository. A real brand font path must be supplied by the project/run when required.
- Do not silently shrink text below the configured minimum. Return `FAIL_COPY_OVERFLOW`.
- Do not silently change PNG to JPEG or vice versa to satisfy size limits.
- JPEG may lower quality only within the explicit configured range.
- Flat-color contrast may be calculated exactly; text over photography still needs local/visual checking.
- `copy_scrim`, `spotlight`, and `vignette` are composition-lighting primitives, not claims that a lighting effect improves CTR.
- Layout presets are baseline production heuristics, not immutable design templates. A frozen creative contract may provide slot overrides.

## Revisit when

Reconsider SVG/Sharp or browser rendering if we need advanced script shaping across many languages, reusable vector masters, richer masking/effects, or HTML5 motion production. Any future renderer must preserve the same explicit failure semantics and banner-job contract.
