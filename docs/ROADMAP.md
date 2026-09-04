# Roadmap

## v0.1 — Foundation, orchestration, lighting, and static Google preflight

Status: in development.

Implemented / current goals:
- define skill operating contract;
- separate asset-based ads from finished uploaded banners;
- encode current Google core/full packs;
- document visual-attention evidence;
- document typography/color/density rules with evidence labels;
- define persistent `BRAND.md` and creative memory;
- add JSON schemas;
- add dependency-free technical validator for static image dimensions/file size/animation state;
- add structured intake/question pool;
- make concept count, size count, variants, languages, and total output count explicit;
- add a banner-run matrix contract;
- add Matreshka-compatible subagent orchestration;
- default to one fresh `BANNER_DESIGNER` context per final banner job;
- add independent reference-analysis and review roles;
- add 30-scheme lighting intelligence derived from the user-supplied lighting guide;
- distinguish scene lighting from composition lighting;
- add lighting-config regression tests.

Exit criteria:
- a new business brief can be represented structurally;
- the skill asks only unresolved material questions before production;
- the requested total output count is unambiguous;
- references can be converted into reusable `REFERENCE_DNA`;
- a concept can be adapted into layout families;
- every final banner can be represented by exactly one banner-matrix row;
- banner jobs can be dispatched with narrow immutable task briefs;
- a static file can be preflighted against the selected Google pack;
- lighting is selected as a hierarchy tool rather than decorative default;
- no core rule depends on a fabricated universal fill %, font category, CTA color, or lighting-performance claim.

## v0.2 — Deterministic renderer and pack builder

Planned:
- renderer contract for PNG/JPG;
- font loading and exact text measurement;
- grids and layout-family templates;
- text fitting without silent font shrink;
- logo clearspace tokens;
- image focal-point/crop controls;
- scene hero ingestion;
- composition-lighting primitives:
  - radial spotlight;
  - protected copy gradient;
  - restrained vignette;
  - local hero edge glow;
  - tonal text plate;
- contrast calculation for flat backgrounds;
- local contrast sampling for photographic copy zones;
- contact-sheet generator;
- pack-level manifest generator;
- banner-matrix driven batch export;
- regression fixtures for all core dimensions.

Preferred implementation decision will be made after comparing SVG/Sharp, HTML/CSS screenshot rendering, and Python imaging for exactness, font behavior, portability, lighting overlays, and compression control.

## v0.3 — Visual QA intelligence

Planned:
- automated AOI inventory;
- saliency preflight as advisory only;
- local contrast sampling behind text on photography;
- clutter/visual-complexity heuristics;
- brand consistency checks;
- lighting hotspot/noise checks;
- cross-size design-drift detection;
- multi-agent creative review:
  - performance strategist;
  - art director;
  - typography reviewer;
  - lighting/focal reviewer;
  - platform compliance reviewer.

## v0.4 — Performance feedback loop

Planned:
- Google Ads API integration;
- map creative/asset IDs to local variant IDs;
- fetch impressions/clicks/conversions/cost/value;
- controlled winner/loser analysis;
- update `CREATIVE_MEMORY.md` from evidence;
- propose next tests without over-attributing causality;
- compare lighting/visual treatments only when the test design isolates those variables.

## Future platform adapters

The core is intentionally platform-neutral enough to later support Meta, LinkedIn, and other display/static systems, but v0.x must not dilute Google correctness to achieve fake universality.
