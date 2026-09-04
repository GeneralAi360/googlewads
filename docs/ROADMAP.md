# Roadmap

## v0.1 — Foundation, orchestration, lighting, Google preflight

Status: **implemented in draft PR**.

Implemented:
- core skill/controller contract and Google mode separation;
- evidence hierarchy: platform requirement / research evidence / production heuristic / test hypothesis;
- current Google core/full uploaded-display registry;
- visual-attention, typography, color, contrast and density references;
- persistent brand and creative-memory contracts;
- 30-scheme lighting intelligence from the user-provided guide;
- Matreshka-compatible controller/subagent roles;
- dependency-free Google static-image validator.

## v0.2 — Intake-to-reviewed-pack production pipeline

Status: **feature-rich development candidate; not merged**.

Implemented:
- machine-readable 52-question intake pool;
- `quick / standard / deep` intake planner;
- `RESOLVED / MISSING / CONDITIONAL / NOT_APPLICABLE` state model;
- explicit output math `concepts × sizes × variants × languages`;
- ambiguity detection for requests such as “10 banners in 7 sizes”;
- freeze gate that prevents matrix creation while production questions remain unresolved;
- freeze hashes, Google mode/spec snapshot and overwrite protection;
- deterministic banner matrix and separate matrix schema;
- one task brief/render-spec shell per final banner row;
- fresh `BANNER_DESIGNER` context per row by default;
- machine-readable independent `REFERENCE_ANALYST` jobs and `REFERENCE_DNA` readiness contract;
- concept-level approved creative contracts with exact per-language/per-format copy adaptation;
- creative-contract freeze, SHA-256 binding, provenance propagation and pre-render mutation detection;
- Pillow renderer ADR and runtime dependency;
- layout presets for every Google registry family;
- exact PNG/JPG rendering;
- real font measurement and wrapping;
- fail-closed text overflow and unsupported-layout semantics;
- focal-point hero crop;
- explicit logo clearspace;
- scene-lighting vs composition-lighting separation;
- composition primitives: hero edge glow, spotlight, copy scrim, vignette, text plate;
- CTA/flat contrast checks;
- photographic copy-zone local contrast sampling and gate;
- Pillow compatibility path preferring `get_flattened_data()` with legacy fallback;
- bounded JPEG compression / explicit PNG oversize failure;
- contact-sheet generator;
- matrix-driven pack runner;
- render-spec ↔ matrix identity validation;
- real handoff to `validate_google_banner.py`;
- provenance manifest only for fully technically passing packs;
- per-file + render-spec + matrix SHA-256 provenance;
- Google spec snapshot propagation;
- synthetic intake-to-seven-format E2E fixture;
- one independent `DESIGN_REVIEWER` task per final banner;
- exact-output hash binding for reviews;
- one independent `PACK_REVIEWER` task;
- final readiness gate that separates `DELIVERY_STATUS` from `RUN_RIGOR` and blocks full-rigor completion when review independence is missing;
- **84/84 green GitHub Actions tests** at the current milestone.

Remaining before v0.2 completion:
- add visual-judgment eval fixtures that exercise actual rendered hierarchy/crop/contrast/density/brand-drift findings, not only deterministic report contracts;
- run those evals through a genuinely fresh visual reviewer when the host provides independent visual context;
- perform a final independent repository review of v0.2 and reconcile important findings;
- decide whether to keep the historical development branch name or cut a clean `dev/performance-banner-designer-v0.2` branch/release before merge.

## v0.3 — Visual QA intelligence

Planned:
- AOI inventory;
- advisory saliency preflight;
- richer photographic glyph-region contrast maps;
- clutter/visual-complexity heuristics;
- automatic brand-consistency signals;
- lighting hotspot/noise checks;
- cross-size design-drift detection;
- multi-agent visual-quality council for high-stakes packs;
- representative visual fixtures with expected reviewer findings.

Saliency and complexity scoring remain advisory; they must not be presented as CTR prediction.

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
