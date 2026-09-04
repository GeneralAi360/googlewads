# Google Ads Performance Banner Designer

A production-grade AI skill for planning, designing, adapting, rendering, reviewing, validating, and iterating performance advertising banners for Google Ads.

The project is broader than a legacy GDN banner prompt. It separates asset-based Google formats from fully composed Uploaded Display creatives and treats intake, reference analysis, creative strategy, Matreshka-style subagent production, lighting, exact raster rendering, independent visual review, technical validation, and performance learning as one system.

## Core pipeline

`context -> 52-question intake state -> freeze gate -> reference DNA -> frozen creative contracts -> banner matrix -> one job per output -> banner workers -> deterministic render + Google preflight -> contact sheet + provenance manifest -> independent banner reviews -> pack review -> readiness gate -> delivery -> performance learning`

## Current development

Branch: `dev/performance-banner-designer-v0.1`

Draft PR: `#1 feat: Performance Banner Designer v0.2 production pipeline`

The PR remains draft and is not merged into `main`.

## What is executable now

### 1. Structured intake

`config/intake-question-pool.json` contains the machine-readable 52-question pool. `scripts/plan_banner_intake.py` reads partial structured context, marks every question as `RESOLVED`, `MISSING`, `CONDITIONAL`, or `NOT_APPLICABLE`, calculates output math, and exposes only unresolved questions appropriate to `quick`, `standard`, or `deep` mode.

It does not treat `null`, `false`, or an empty list as automatically missing. Those values may represent deliberate answers such as “no proof”, “no disclaimer”, or “no formal brand system”.

### 2. Production freeze gate

`scripts/freeze_banner_run.py` is the boundary between questioning and production. It refuses to create a matrix while intake is `BRIEF_INCOMPLETE` or `OUTPUT_COUNT_AMBIGUOUS`.

A successful freeze records:
- Google mode and local spec snapshot;
- concept/size/variant/language counts;
- exact output total;
- input-context SHA-256;
- matrix SHA-256;
- immutable `banner-matrix.json`;
- `run-freeze.json`.

The deterministic v0.2 renderer freezes only PNG/JPG uploaded-display production. Unsupported modes/formats fail explicitly instead of silently using the wrong pipeline.

### 3. Matreshka-style job isolation

`references/subagent-orchestration.md` and `assets/banner-task-brief-template.md` define the controller/subagent contract.

`scripts/materialize_banner_jobs.py` creates exactly one narrow task brief and one render-spec shell per final matrix row. Existing worker files are not overwritten unless the controller explicitly reconciles the run with `--force`.

For `3 concepts × 7 sizes × 2 variants × 1 language`, the system expects **42 final files and 42 traceable banner jobs**.

### 4. Lighting intelligence

The user-supplied 30-lighting-scheme guide is represented as production heuristics in `config/lighting-schemes.json` and `references/lighting-intelligence.md`.

The skill distinguishes:
- `SCENE_LIGHTING` — light inside the photographed/generated hero;
- `COMPOSITION_LIGHTING` — controlled post-composite hierarchy tools.

Implemented composition primitives:
- `hero_edge_glow`;
- `spotlight`;
- `copy_scrim`;
- `vignette`;
- `text_plate`.

Lighting is not treated as a guaranteed CTR/conversion law.

### 5. Deterministic renderer

`scripts/render_banner.py` uses Pillow for exact PNG/JPG composition. It owns critical copy, logo/brand name, fonts, layout, focal crop, lighting overlays, output dimensions, and compression.

Important failure semantics:
- `FAIL_COPY_OVERFLOW` — text cannot fit above the allowed minimum size;
- `FAIL_LAYOUT` — the selected format intentionally has no slot for supplied information;
- `FAIL_CONTRAST` — flat/CTA contrast gate fails;
- `FAIL_LOCAL_CONTRAST` — photographic copy-zone contrast is too weak;
- `FAIL_FILE_SIZE` — byte target cannot be met;
- `FAIL_ASSET` — an approved required asset is unavailable.

The renderer measures local photographic contrast before drawing text and can use a controlled text plate/scrim rather than relying on visual guesswork. Logo clearspace is explicit and reported.

### 6. Google technical pack

`scripts/render_banner_pack.py` renders every matrix row, verifies render-spec identity against the immutable matrix, calls `scripts/validate_google_banner.py`, creates a contact sheet, and emits `output-manifest.json` only when every file passes technical preflight.

The manifest records hashes and provenance, including matrix hash, output hash, render-spec hash, Google snapshot date, concept/brand/reference/lighting/source IDs, and generation timestamp.

A technical manifest does **not** by itself mean final design readiness.

### 7. Independent review gate

`scripts/materialize_review_jobs.py` creates one read-only `DESIGN_REVIEWER` task per output plus one `PACK_REVIEWER` task.

Each banner review is bound to the exact output SHA-256. If the banner changes, the old review is stale and cannot approve the new file.

`scripts/assess_pack_readiness.py` requires:
- every banner review to pass;
- concept/brand/hierarchy/lighting/type/color/density/crop/CTA/actual-size checks;
- one pack-level cross-size/contact-sheet review;
- independent contexts by default.

Only then may the controller return `delivery_status=COMPLETE` and allow the final completion claim. If independence is unavailable, delivery/process rigor are reported separately rather than faking full rigor.

### 8. Seven-format end-to-end fixture

`scripts/demo_end_to_end.py` proves the real local chain using synthetic business facts and synthetic imagery only:

`intake -> freeze -> 7 core matrix rows -> materialize -> deterministic JPG render -> Google validator -> contact sheet -> provenance manifest`

It is a pipeline fixture, not evidence of advertising performance.

## Google core pack

The current encoded Uploaded Display core pack is:

- 300x250
- 336x280
- 728x90
- 970x90
- 160x600
- 300x600
- 320x50

The skill never mechanically rescales one canvas into all seven formats. It preserves the creative contract while rebuilding composition by layout family.

## Evidence policy

Every reusable rule is classified as:

1. platform requirement;
2. research evidence;
3. production heuristic;
4. test hypothesis.

This prevents unsupported rules such as a universal fill percentage, a universally superior serif/sans category, a universally best CTA color, or a guaranteed-performing lighting scheme.

## Current verification

GitHub Actions currently passes **65/65 tests** on the draft branch. Coverage includes:
- Google image preflight;
- format registry and matrix math;
- 30 lighting schemes;
- 52-question intake planner;
- freeze gate;
- one-job-per-row materialization;
- all seven core dimensions;
- text overflow/layout/file-size/contrast failures;
- focal crop, clearspace and composition lighting;
- photographic local contrast;
- pack builder and provenance manifest;
- real Google-validator integration;
- intake-to-seven-format E2E fixture;
- independent banner review and pack-readiness gate.

See `docs/ROADMAP.md` for remaining v0.2 work and later performance/visual-QA layers.
