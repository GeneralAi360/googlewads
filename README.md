# Google Ads Performance Banner Designer

A production-grade AI skill for planning, designing, adapting, rendering, validating, and iterating performance advertising banners for Google Ads.

The project is broader than a legacy GDN banner prompt. It separates asset-based Google formats from fully composed Uploaded Display creatives and treats intake, reference analysis, creative strategy, subagent production, lighting, exact raster rendering, technical validation, and performance learning as one system.

## Core pipeline

`Business context -> unresolved-question intake -> reference DNA -> frozen creative contracts -> banner matrix -> materialized one-job briefs/specs -> one narrow banner worker per row -> deterministic render -> independent review -> Google preflight -> pack assembly -> performance learning`

## Current development branch

`dev/performance-banner-designer-v0.1`

Draft PR: `#1 feat: Performance Banner Designer v0.1 foundation`

## Current implementation

### Controller and design intelligence
- `SKILL.md` — complete skill execution contract;
- `references/intake-and-run-contract.md` — 52-question internal intake pool with resolved/missing states;
- `references/subagent-orchestration.md` — Matreshka-compatible narrow subagent model;
- `assets/banner-task-brief-template.md` — one-banner task contract;
- `references/lighting-intelligence.md` + `config/lighting-schemes.json` — 30 lighting schemes treated as production heuristics;
- `references/visual-attention.md` — eye tracking, banner blindness, gaze direction, AOIs, complexity;
- `references/typography-color-contrast.md` — type hierarchy, font evidence, contrast and color;
- `references/layout-families-and-density.md` — multi-format adaptation and information budgets.

### Google platform layer
- `references/google-platform-specs.md` — Google modes, dimensions, limits, and dynamic-refresh rule;
- `config/google-formats.json` — machine-readable format registry;
- `scripts/validate_google_banner.py` — static image technical preflight.

### Banner-run contracts
- `schemas/business-brief.schema.json`;
- `schemas/banner-concept.schema.json`;
- `schemas/banner-run.schema.json` — full controller-owned run with creative contracts/context;
- `schemas/banner-matrix.schema.json` — deterministic final-job matrix document;
- `schemas/banner-render-spec.schema.json` — one worker render spec;
- `schemas/output-manifest.schema.json` — fully passing pack manifest;
- `scripts/build_banner_matrix.py` — deterministic `concepts × sizes × variants × languages` matrix;
- `scripts/materialize_banner_jobs.py` — one task brief + one render-spec shell per matrix row, without inventing missing facts.

### Deterministic renderer / pack builder
- `requirements.txt` — Pillow raster dependency;
- `docs/ADR-001-renderer.md` — renderer decision record;
- `config/layout-presets.json` — normalized layout-family baselines;
- `scripts/render_banner.py` — exact-size PNG/JPG renderer with real text measurement, focal crop, logo placement, CTA/offer composition, contrast gates and composition lighting;
- `scripts/build_contact_sheet.py` — review-only mixed-format overview;
- `scripts/render_banner_pack.py` — matrix-driven render + Google validation + contact sheet + output manifest.

The renderer never silently rewrites copy or shrinks it below the configured minimum. Unsupported content in a small layout returns an explicit failure instead of being squeezed into the banner.

## Default Uploaded Display core pack

The current core pack encoded for Uploaded Display within Demand Gen is:

- 300x250
- 336x280
- 728x90
- 970x90
- 160x600
- 300x600
- 320x50

The skill does **not** resize one master design into these formats. One creative contract is rebuilt through the relevant layout families.

## One banner per job

For a run with `3 concepts × 7 sizes × 2 variants × 1 language`, the controller creates **42 matrix rows** and therefore 42 traceable final banner jobs by default.

Materialize those jobs with:

```bash
python scripts/materialize_banner_jobs.py \
  --matrix run/banner-matrix.json \
  --out-dir run/jobs
```

This creates `run/jobs/task-briefs/{job_id}.md`, `run/jobs/render-specs/{job_id}.json`, and a `dispatch-index.json`. Existing worker files are not overwritten unless the controller explicitly uses `--force`.

Each `BANNER_DESIGNER` receives only its frozen concept, relevant brand/reference/lighting context, exact dimension/layout family, exact approved copy and one output path. The worker may adapt the composition but may not redefine the offer, price, CTA, brand, or creative contract.

## Pack rendering

After worker render specs are complete:

```bash
python scripts/render_banner_pack.py \
  --matrix run/banner-matrix.json \
  --spec-dir run/jobs/render-specs \
  --mode demand_gen_uploaded_display \
  --pack core \
  --contact-sheet run/contact-sheet.png \
  --manifest run/output-manifest.json \
  --report run/pack-report.json
```

The pack runner returns `PASS` only when **every** matrix row renders and passes Google technical preflight. `output-manifest.json` is created only for a fully passing pack.

## Design evidence policy

Every reusable rule is classified as:

1. platform requirement;
2. research evidence;
3. production heuristic;
4. test hypothesis.

This prevents common mistakes such as treating a responsive-image blank-space recommendation as a universal fill percentage, declaring one font category or CTA color universally superior, or treating a lighting preset as a guaranteed CTR improvement.

## Tests

GitHub Actions installs renderer dependencies and runs the full regression suite for matrix logic/schema alignment, lighting configuration, job materialization, contact sheets, deterministic rendering, pack assembly, real Google preflight integration, and the original dependency-free image validator.

Current verified baseline: **41/41 tests PASS** on the development branch.

## Roadmap

See `docs/ROADMAP.md`.
