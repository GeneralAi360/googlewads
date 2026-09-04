# Roadmap

## v0.1 — Foundation and static Google preflight

Status: in development.

Goals:
- define skill operating contract;
- separate asset-based ads from finished uploaded banners;
- encode current Google core/full packs;
- document visual-attention evidence;
- document typography/color/density rules with evidence labels;
- define persistent `BRAND.md` and creative memory;
- add JSON schemas;
- add dependency-free technical validator for static image dimensions/file size/animation state.

Exit criteria:
- a new business brief can be represented structurally;
- a concept can be adapted into layout families;
- a static file can be preflighted against the selected Google pack;
- no core rule depends on a fabricated universal fill %, font category, or CTA color claim.

## v0.2 — Deterministic renderer

Planned:
- renderer contract for PNG/JPG;
- font loading and exact text measurement;
- grids and layout-family templates;
- text fitting without silent font shrink;
- logo clearspace tokens;
- image focal-point/crop controls;
- contrast calculation for flat backgrounds;
- contact-sheet generator;
- pack-level manifest generator;
- regression fixtures for all core dimensions.

Preferred implementation decision will be made after comparing SVG/Sharp, HTML/CSS screenshot rendering, and Python imaging for exactness, font behavior, portability, and compression control.

## v0.3 — Visual QA intelligence

Planned:
- automated AOI inventory;
- saliency preflight as advisory only;
- local contrast sampling behind text on photography;
- clutter/visual-complexity heuristics;
- brand consistency checks;
- multi-agent creative review: performance strategist, art director, typography reviewer, platform compliance reviewer.

## v0.4 — Performance feedback loop

Planned:
- Google Ads API integration;
- map creative/asset IDs to local variant IDs;
- fetch impressions/clicks/conversions/cost/value;
- controlled winner/loser analysis;
- update `CREATIVE_MEMORY.md` from evidence;
- propose next tests without over-attributing causality.

## Future platform adapters

The core is intentionally platform-neutral enough to later support Meta, LinkedIn, and other display/static systems, but v0.x must not dilute Google correctness to achieve fake universality.
