# Roadmap

## v0.1 — Foundation, orchestration, lighting, Google preflight

Status: foundation implemented in draft PR.

Implemented:
- skill operating contract and Google mode separation;
- current Google core/full packs;
- visual-attention, typography, color, contrast and density references;
- persistent brand and creative-memory contracts;
- structured brief/concept/run/output schemas;
- structured intake and explicit output math;
- deterministic banner matrix;
- Matreshka-compatible subagent orchestration;
- one fresh `BANNER_DESIGNER` context per final banner job by default;
- independent reference-analysis and review roles;
- 30-scheme lighting intelligence;
- scene-lighting vs composition-lighting distinction;
- dependency-free Google static image validator and regression tests.

The foundation can specify, count, split and technically validate a banner run without inventing universal design laws.

## v0.2 — Deterministic renderer and pack builder

Status: in development; baseline runtime implemented.

Implemented:
- main `SKILL.md` routes production through the materializer, render spec, renderer, pack runner and readiness-manifest gates;
- Python + Pillow renderer decision (`docs/ADR-001-renderer.md`);
- `requirements.txt`;
- `schemas/banner-render-spec.schema.json`;
- separate `schemas/banner-matrix.schema.json` so the lightweight job matrix is not confused with the full controller-owned `banner-run` contract;
- `config/layout-presets.json` covering every Google layout family in the registry;
- exact PNG/JPG rendering;
- real font measurement and line wrapping;
- fail-closed `FAIL_COPY_OVERFLOW` instead of silent text shrink below minimum;
- fail-closed `FAIL_LAYOUT` when a small format cannot carry a content slot;
- logo contain-fit and hero focal-point cover crop;
- composition-lighting primitives: spotlight, protected copy gradient/scrim and vignette;
- flat-color contrast calculation and optional contrast gates;
- explicit PNG byte failure and bounded JPEG quality reduction;
- contact-sheet generator;
- matrix-driven pack runner;
- render-spec to matrix identity checks;
- one-job-per-row materializer producing narrow task briefs and render-spec shells without inventing missing facts;
- overwrite protection for worker files unless controller explicitly uses `--force`;
- real pack-runner handoff to `validate_google_banner.py`;
- pack report with per-job failures;
- output manifest emitted only for a fully passing pack;
- exact-size regression coverage for all seven core formats;
- 41-test green CI baseline before the latest documentation/skill wiring.

Remaining before v0.2 completion:
- photographic local contrast sampling behind text;
- local hero edge glow;
- tonal text plate primitive;
- explicit logo clearspace tokens beyond baseline slots;
- richer manifest timestamps/spec snapshot provenance;
- reusable example run fixture with hero/logo assets;
- visual review fixture/contact-sheet acceptance baseline;
- end-to-end eval of interview → matrix → materialized subagent jobs → rendered/validated pack.

## v0.3 — Visual QA intelligence

Planned:
- AOI inventory and advisory saliency preflight;
- photographic glyph-region contrast map;
- clutter/complexity heuristics;
- brand consistency and lighting-hotspot checks;
- cross-size design-drift detection;
- independent performance/art/typography/lighting/platform review roles.

## v0.4 — Performance feedback loop

Planned:
- Google Ads API integration;
- creative/asset ID ↔ local variant mapping;
- impressions/clicks/conversions/cost/value retrieval;
- controlled winner/loser analysis;
- evidence-based updates to `CREATIVE_MEMORY.md`;
- next-test proposals without over-attributing causality.

## Future adapters

The core may later support other static/display platforms, but v0.x must preserve Google correctness rather than chase fake universality.
