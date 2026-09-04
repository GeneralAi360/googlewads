# Roadmap

## v0.1 — Foundation, orchestration, lighting, Google preflight

Status: **implemented**.

Implemented:
- core controller and Google mode separation;
- evidence hierarchy: platform requirement / research evidence / production heuristic / test hypothesis;
- Google core/full uploaded-display registry;
- visual-attention, typography, color, contrast and density references;
- persistent brand and creative-memory contracts;
- 30-scheme lighting intelligence;
- Matreshka-compatible controller/subagent roles;
- dependency-free Google static-image validator.

## v0.2 — Research-to-reviewed-pack production pipeline

Status: **active release-candidate hardening in `dev/performance-banner-designer-v0.2`; not merged**.

The first real Work acceptance test exposed a preproduction design failure: three superficially different 300x250 directions were rendered before category/competitor creative research, reused almost the same layout grammar, and relied on generic/toy-like cloud imagery that did not reach a professional B2B standard. This is recorded as `REAL-01` in `evals/real-world-failures.json`.

### Existing implemented foundation

- machine-readable 52-question intake pool and quick/standard/deep planner;
- explicit output math and ambiguity detection;
- immutable run freeze and deterministic banner matrix;
- independent supplied-reference analysis / REFERENCE_DNA;
- Google mode separation;
- art-direction identity and design-craft rules;
- creative-contract freeze, SHA binding and mutation detection;
- one banner job per final output;
- Pillow exact-size renderer;
- layout-family recomposition, crop, type fitting, clearspace, lighting and contrast gates;
- real Google preflight and provenance manifest;
- design-QA grayscale/squint/thumbnail views;
- hash-bound DESIGN_REVIEWER and PACK_REVIEWER task materialization;
- readiness gate separating delivery completeness from review rigor;
- hidden-key visual-review eval harness;
- synthetic seven-format E2E and real user-acceptance regression corpus.

### New mandatory preproduction design gates

Implemented after `REAL-01`:

1. **Competitive Creative Intelligence**
   - `references/competitive-creative-intelligence.md`;
   - `schemas/competitive-creative-research.schema.json`;
   - performance-evidence tiers A–E;
   - prohibition on calling reference ads high-converting without conversion evidence;
   - one narrow `COMPETITOR_RESEARCHER` task per target/query via `scripts/materialize_competitive_research_jobs.py`.

2. **Category Design Map**
   - `schemas/category-design-map.schema.json`;
   - mature category signals, hero strategies, trust signals, category clichés, generic-AI risks and differentiated opportunities.

3. **Detailed Design Brief**
   - `schemas/design-brief.schema.json`;
   - exact research/category hashes, AOI/scan path, hero strategy, typography/color/layout/lighting/density, output math and mandatory asset-quality policy.

4. **Written Art Direction Approval**
   - `schemas/art-direction-approval.schema.json`;
   - three written materially different directions before preview rendering for preview/autoselect mode;
   - approval bound to exact design-brief SHA.

5. **Representative High-Fidelity Approval**
   - `schemas/representative-design-approval.schema.json`;
   - one representative artifact before full-pack scale-out;
   - asset quality, professional category fit, hierarchy, typography, brand/message fidelity, crop, lighting, CTA and anti-generic-AI checks must all PASS;
   - approval bound to exact representative artifact SHA.

6. **Preproduction Freeze**
   - `schemas/preproduction-freeze.schema.json`;
   - `scripts/freeze_preproduction_design.py`;
   - binds competitive research → category map → design brief → written approval → representative approval → exact banner matrix;
   - detects stale hashes, degraded/unaccepted research, weak coverage, unsupported performance claims, output mismatch and changed representative artifact.

7. **Creative freeze linkage**
   - normal `freeze_creative_contracts.py` CLI now requires `--preproduction-freeze`;
   - creative `art_direction_id` must equal the preproduction-approved direction;
   - preproduction freeze SHA is propagated into per-banner render-spec provenance.

8. **Canonical E2E update**
   - synthetic E2E now includes the whole preproduction approval chain before creative freeze and full render scale-out;
   - reviewer reports are still never fabricated.

### Current v0.2 validation work

Before v0.2 can be called fully validated:

1. Keep deterministic CI green after the new preproduction gates and reconcile any regressions.
2. Repeat the same real Work task that produced `REAL-01` and verify behavior changes: research first, written directions before images, one high-fidelity representative approval before pack scale-out.
3. Execute all six hidden-key visual eval cases through genuinely fresh visual DESIGN_REVIEWER contexts and score returned reports.
4. Perform a genuinely independent final repository/PR review and reconcile important findings.
5. Merge only with explicit user approval.

If fresh independent reviewer contexts are unavailable, report this as an external rigor blocker rather than manufacturing reports.

## v0.3 — Motion creative: GIF / video / HTML5 architecture

Planned after static v0.2 is proven on the real Work task:
- shared advertising brief/brand/claim/art-direction contracts;
- `MotionIntent` bridge inspired by Matreshka Content Factory;
- Remotion deterministic motion renderer for appropriate code-motion ads;
- GIF-specific duration/FPS/size validation and optimization;
- video creative matrix across aspect/duration/language/variant;
- bridge to Content Factory for live footage, generated media, asset resolution and rendered-evidence QA;
- HTML5 display path kept separate from GIF/video where appropriate.

## v0.4 — Automated visual QA intelligence

Planned:
- AOI inventory;
- advisory saliency preflight;
- richer photographic glyph-region contrast maps;
- clutter/visual-complexity heuristics;
- automated brand-consistency signals;
- lighting hotspot/noise checks;
- automated cross-size design-drift signals;
- multi-agent visual-quality council;
- larger representative eval corpus.

Saliency/complexity remain advisory and must not be presented as CTR prediction.

## v0.5 — Performance feedback loop

Planned:
- Google Ads API integration;
- creative/asset ID ↔ local variant mapping;
- impressions/clicks/conversions/cost/value retrieval;
- controlled winner/loser analysis;
- evidence-based `CREATIVE_MEMORY.md` updates;
- next-test proposals without over-attributing causality;
- optional integration with creative-analytics tools when available.

## Future adapters

The architecture may later support Meta, LinkedIn and other creative systems, but Google correctness and explicit evidence boundaries remain primary.
