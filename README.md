# Google Ads Performance Banner Designer

A production-grade AI skill for planning, designing, adapting, rendering, reviewing, validating, and iterating performance advertising banners for Google Ads.

The project is broader than a legacy GDN banner prompt. It treats business intake, reference analysis, art direction, creative strategy, Matreshka-style subagent production, lighting, exact raster composition, independent visual review, Google technical validation, and later performance learning as one connected production system.

## Core pipeline

`context -> 52-question intake -> run freeze -> reference DNA -> art-direction decision -> frozen creative contracts -> banner matrix -> one job per output -> deterministic render -> Google preflight -> manifest/contact sheet -> thumbnail/grayscale/squint QA views -> independent banner reviews -> pack review -> readiness gate -> delivery -> performance learning`

## Current development

Branch: `dev/performance-banner-designer-v0.2`

`main` remains unchanged. v0.2 must not be merged until final review/reconciliation is complete.

## What is executable now

### Structured intake and freeze

`config/intake-question-pool.json` contains 52 potential questions. `scripts/plan_banner_intake.py` marks them `RESOLVED`, `MISSING`, `CONDITIONAL`, or `NOT_APPLICABLE` and asks only unresolved material questions.

The planner keeps concept count, size count, variant count, language count, and total output count explicit. Ambiguous wording such as “10 banners in 7 sizes” blocks production instead of guessing.

`scripts/freeze_banner_run.py` creates the immutable production envelope only after intake is ready. It records Google mode/spec snapshot, exact size list, output math, context hash, matrix hash, `run-freeze.json`, and `banner-matrix.json`.

### Reference analysis

Reference-driven work uses one narrow read-only `REFERENCE_ANALYST` job per supplied reference. Machine-readable `REFERENCE_DNA` captures composition, hierarchy, typography, color, whitespace, CTA treatment, image/crop behavior, lighting, transferable principles, and literal elements that must not be copied.

### Art direction before scale-out

`references/art-direction-and-design-craft.md` adds production design craft synthesized from useful patterns found in public design skills while preserving the repository evidence policy.

Visual direction is resolved through one of:
- `ART_DIRECTION_LOCKED` — existing brand/design identity already governs the work;
- `ART_DIRECTION_PREVIEW_3` — three genuinely different representative visual systems are shown to the user before the full pack;
- `ART_DIRECTION_AUTOSELECT_3` — three isolated candidates are ranked by an independent art-direction reviewer in unattended workflows.

The selected `art_direction_id` becomes part of the frozen creative contract, is propagated into every render spec and output manifest, and is checked again before rendering. A banner worker cannot silently swap the approved visual language.

The design-craft layer also adds silhouette-first hierarchy, intentional alignment, structural whitespace, anti-template/anti-generic-AI guardrails, aspect-ratio-specific crop recomposition, and thumbnail/grayscale/squint diagnostics. Contextual heuristics such as “CTA always bottom-right” or “20% text maximum” are deliberately not promoted to universal rules.

### Frozen creative contracts

Concept contracts preserve proposition, proof, CTA, visual idea, primary AOI, scan path, brand, art direction, reference IDs, source grounding, lighting choice, variants, languages, and controlled copy overrides by layout family/dimension.

`scripts/freeze_creative_contracts.py`, `scripts/apply_creative_contracts.py`, and `scripts/validate_creative_bindings.py` SHA-bind those decisions to every banner job. Worker mutation of copy, art direction, reference/source provenance, brand, or lighting fails the binding gate.

### Matreshka-style job isolation

`scripts/materialize_banner_jobs.py` creates one narrow task and one render-spec shell per final matrix row. One fresh `BANNER_DESIGNER` context per row is the default when the host supports real isolation.

For `3 concepts × 7 sizes × 2 variants × 1 language`, the system expects exactly **42 final files and 42 traceable jobs**.

### Lighting intelligence

The user-supplied 30-lighting-scheme guide is encoded as production heuristics in `config/lighting-schemes.json` and `references/lighting-intelligence.md`.

The system distinguishes:
- `SCENE_LIGHTING` — light inside the photographed/generated hero;
- `COMPOSITION_LIGHTING` — controlled post-composite hierarchy tools.

Implemented composition primitives include `hero_edge_glow`, `spotlight`, `copy_scrim`, `vignette`, and `text_plate`. Lighting serves material read, separation, hierarchy, and copy-safe regions; it is not treated as a guaranteed CTR/conversion law.

### Deterministic renderer

`scripts/render_banner.py` uses Pillow for exact PNG/JPG composition and owns critical copy, logo/brand name, fonts, layout, focal crop, composition lighting, output dimensions, and bounded compression.

Explicit failure states include:
- `FAIL_COPY_OVERFLOW`;
- `FAIL_LAYOUT`;
- `FAIL_CONTRAST`;
- `FAIL_LOCAL_CONTRAST`;
- `FAIL_FILE_SIZE`;
- `FAIL_ASSET`.

Photographic copy-zone contrast is measured before text is drawn. Logo clearspace is explicit. Small formats drop approved secondary content through controlled contract overrides rather than silently shrinking everything.

### Google technical pack and provenance

`scripts/render_banner_pack.py` verifies matrix identity and frozen creative/art-direction binding, renders every row, invokes `scripts/validate_google_banner.py`, creates a contact sheet, and emits `output-manifest.json` only for a fully technically passing pack.

The manifest records output/render-spec/matrix SHA-256 values plus Google snapshot, concept, brand, art-direction, reference, source-grounding, hero, and lighting provenance.

Technical PASS is not design PASS.

### Diagnostic visual QA

`scripts/build_design_qa_views.py` creates review-only views for every exact output:
- actual output reference;
- exact-size grayscale;
- exact-size squint/blur;
- 25% thumbnail/glance board.

They are hash-bound to the source output and are never upload/delivery assets. They expose failures that can be hidden when tiny Google banners are enlarged in a design UI: weak hierarchy, color-only hierarchy, decorative light dominating the message, unreadable thumbnail behavior, and noise from secondary detail.

### Independent review and readiness

`scripts/materialize_review_jobs.py` creates one read-only `DESIGN_REVIEWER` task per final banner plus one `PACK_REVIEWER` task. Diagnostic views are attached only when their source hash and files are valid.

Individual review covers concept/brand fidelity, primary AOI, lighting, typography, actual-size readability, thumbnail behavior, grayscale and squint hierarchy, contrast, density, crop, CTA, and anti-template/generic styling.

Pack review covers expected files, duplicates, concept/brand consistency, campaign design grammar, cross-size lighting consistency where relevant, layout adaptation, small-format simplification, and contact-sheet quality.

`scripts/assess_pack_readiness.py` separates:
- `delivery_status` — whether required outputs/reviews pass;
- `run_rigor` — whether actual independent contexts were available.

A changed output invalidates its previous review through SHA binding.

### Visual-review calibration harness

The repo includes six intentionally flawed synthetic visual cases covering:
- photographic copy glare/contrast;
- logo dominance;
- destructive hero crop;
- overloaded 320x50;
- decorative lighting stealing focal priority;
- cross-size campaign drift.

The harness generates real image artifacts, materializes one fresh read-only reviewer task per case without leaking the hidden answer key, defines a machine-readable review-report schema, and scores critical/important recall, false critical findings, and prohibited performance/design myths.

Unit tests prove the harness itself is deterministic. They do **not** prove a model's visual judgment until the six cases are executed through genuinely fresh visual contexts and scored.

### Canonical seven-format E2E fixture

`scripts/demo_end_to_end.py` now exercises:

`intake -> run freeze -> 7 core matrix rows -> job materialization -> approved creative + art-direction freeze -> binding -> deterministic JPG render -> real Google validator -> manifest/contact sheet -> grayscale/squint/thumbnail QA views -> 7 independent review tasks + pack-review task`

The fixture intentionally stops before inventing reviewer reports.

## Google core pack

Current encoded Uploaded Display core sizes:
- 300x250
- 336x280
- 728x90
- 970x90
- 160x600
- 300x600
- 320x50

The skill preserves one creative/design grammar while rebuilding composition per layout family. It never treats a representative preview as a master canvas to resize mechanically.

## Evidence policy

Every reusable rule is classified as:
1. platform requirement;
2. research evidence;
3. production heuristic;
4. test hypothesis.

This prevents imported design advice or internet conventions from becoming false universal laws.

## Current verification

GitHub Actions passes **114/114 tests** on `dev/performance-banner-designer-v0.2` at the current verified milestone.

Coverage includes intake/freeze, Google formats, 30 lighting schemes, reference DNA, art-direction/creative freeze and mutation detection, layout families, exact rendering, crop/clearspace/lighting/local contrast, compression, Google preflight, manifest provenance, design-QA diagnostic views, review materialization/readiness, hidden-key visual-review eval infrastructure, and the canonical seven-format intake-to-review-dispatch E2E.

See `docs/ROADMAP.md` for the remaining external validation step and later v0.3/v0.4 work.
