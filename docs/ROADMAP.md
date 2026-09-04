# Roadmap

## v0.1 — Foundation, orchestration, lighting, Google preflight

Status: **implemented**.

Implemented:
- core controller and Google mode separation;
- evidence hierarchy: platform requirement / research evidence / production heuristic / test hypothesis;
- current Google core/full uploaded-display registry;
- visual-attention, typography, color, contrast and density references;
- persistent brand and creative-memory contracts;
- 30-scheme lighting intelligence from the user-provided guide;
- Matreshka-compatible controller/subagent roles;
- dependency-free Google static-image validator.

## v0.2 — Intake-to-reviewed-pack production pipeline

Status: **release candidate in `dev/performance-banner-designer-v0.2`; not merged**.

Implemented:
- machine-readable 52-question intake pool;
- `quick / standard / deep` intake planner;
- `RESOLVED / MISSING / CONDITIONAL / NOT_APPLICABLE` state model;
- explicit output math `concepts × sizes × variants × languages`;
- ambiguity detection for requests such as “10 banners in 7 sizes”;
- run freeze gate, hashes, Google spec snapshot and overwrite protection;
- deterministic banner matrix and separate matrix schema;
- one task brief/render-spec shell per final banner row;
- fresh `BANNER_DESIGNER` context per row by default;
- independent `REFERENCE_ANALYST` jobs and machine-readable `REFERENCE_DNA` readiness contract;
- three-mode art-direction resolution: locked / three user previews / three independent candidates with reviewer selection;
- design-craft reference with silhouette-first hierarchy, structural whitespace, intentional alignment, aspect-ratio crop recomposition and anti-template/anti-generic-AI guardrails;
- concept-level approved creative contracts with exact per-language/per-format copy adaptation;
- required frozen `art_direction_id` and visual thesis inside every approved creative contract;
- creative/art-direction freeze, SHA-256 binding, provenance propagation and worker-mutation detection;
- Pillow renderer ADR/runtime and layout presets for every Google registry family;
- exact PNG/JPG rendering with real font measurement/wrapping;
- fail-closed text overflow and unsupported-layout semantics;
- focal-point hero crop and explicit logo clearspace;
- scene-lighting vs composition-lighting separation;
- composition primitives: hero edge glow, spotlight, copy scrim, vignette, text plate;
- CTA/flat contrast and photographic copy-zone local contrast gates;
- bounded JPEG compression / explicit PNG oversize failure;
- contact-sheet generator and matrix-driven pack runner;
- render-spec ↔ matrix identity validation;
- frozen creative + art-direction validation inside pack runner;
- real handoff to `validate_google_banner.py`;
- provenance manifest only for fully technically passing packs;
- per-file + render-spec + matrix SHA-256 provenance including art-direction/source/reference/lighting identity;
- Google spec snapshot propagation;
- review-only design-QA generator producing exact-size grayscale, exact-size squint/blur and 25% thumbnail/glance views;
- hash-bound QA diagnostic index; stale/missing diagnostic files fail before reviewer dispatch;
- one independent `DESIGN_REVIEWER` task per final banner with actual-size + diagnostic-view checks;
- one independent `PACK_REVIEWER` task with campaign-design-grammar checks;
- final readiness gate separating `DELIVERY_STATUS` from `RUN_RIGOR`;
- six hidden-key visual-judgment eval cases covering photo contrast, logo dominance, destructive crop, micro-format overload, lighting hierarchy and cross-size drift;
- deterministic flawed-artifact generator, hidden-key-safe reviewer materializer, review-report schema and scorer;
- canonical seven-format synthetic E2E now reaches creative/art-direction freeze, real Google preflight, manifest, design-QA generation and independent review-task dispatch without fabricating review reports;
- clean v0.2 development branch created;
- **114/114 GitHub Actions tests PASS** at the current verified milestone.

### Remaining before v0.2 can be called fully validated

Only validation that requires genuinely independent model contexts remains:

1. Execute all six hidden-key visual eval cases through fresh visual `DESIGN_REVIEWER` contexts and score returned reports. Passing unit tests prove the harness, not the model's visual judgment.
2. Perform a genuinely independent final repository review of v0.2 and reconcile any important findings.
3. After those two checks, open/finalize the v0.2 PR and merge only with explicit approval.

If the current host cannot provide fresh independent visual/repository reviewer contexts, report this as an external rigor blocker rather than generating fake reviewer reports or claiming `RUN_RIGOR=FULL`.

## v0.3 — Visual QA intelligence

Planned beyond the v0.2 human/model-review gate:
- automated AOI inventory;
- advisory saliency preflight;
- richer photographic glyph-region contrast maps;
- clutter/visual-complexity heuristics;
- automatic brand-consistency signals;
- lighting hotspot/noise checks;
- automated cross-size design-drift signals;
- multi-agent visual-quality council for high-stakes packs;
- larger representative visual-eval corpus.

Saliency and complexity scoring remain advisory and must never be presented as CTR prediction.

## v0.4 — Performance feedback loop

Planned:
- Google Ads API integration;
- creative/asset ID ↔ local variant mapping;
- impressions/clicks/conversions/cost/value retrieval;
- controlled winner/loser analysis;
- evidence-based updates to `CREATIVE_MEMORY.md`;
- next-test proposals without over-attributing causality;
- compare lighting/visual treatments only when the experiment isolates those variables.

## Future adapters

The architecture may later support Meta, LinkedIn, and other display/static systems, but v0.x must preserve Google correctness rather than chase fake universality.
