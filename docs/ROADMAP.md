# Roadmap

## v0.1 — Foundation, orchestration, lighting, Google preflight

Status: **implemented**.

Implemented:
- controller / Matreshka-style subagent architecture;
- Google mode and size registry;
- evidence hierarchy;
- visual-attention, typography, color, contrast, density references;
- 30-scheme lighting vocabulary;
- static Google validator.

## v0.2 — Meaning-to-reviewed-pack static production system

Status: **active release-candidate hardening in `dev/performance-banner-designer-v0.2`; not merged**.

The release candidate has been strengthened through real Work acceptance failures, user-provided visual methodologies, and a September 2026 review of contemporary style/banner/typography sources.

Source-derived design ideas and trend signals are treated as production heuristics/currentness evidence, not conversion laws.

### Core implemented foundation

- 52-question structured intake and ambiguity detection;
- immutable run freeze and banner matrix;
- supplied-reference / REFERENCE_DNA path;
- Competitive Creative Intelligence and A–E performance-evidence tiers;
- category design map;
- commercial-message lock / CTA allowlist;
- canonical brand-identity lock;
- required real-asset contract and `NEEDS_ASSET` validator;
- written art-direction approval;
- one high-fidelity representative before scale-out;
- creative-contract SHA binding;
- one job per final output;
- exact Pillow renderer and per-layout-family recomposition;
- Google technical preflight;
- provenance manifest/contact sheet;
- actual/grayscale/squint/thumbnail QA;
- independent banner/pack review contracts;
- readiness evaluator;
- hidden-key visual-review eval harness;
- real user-acceptance regression corpus (`REAL-01`, `REAL-02`).

### Meaning-first design layer — implemented

1. **IDEA_ARCHITECTURE**
   - core idea;
   - single takeaway;
   - presentation mode;
   - emotional target / avoided tone;
   - creative tension;
   - rationale;
   - disruption level.

2. **Presentation-mode vocabulary**
   - product proof;
   - outcome/pain visualization;
   - explainer/workflow/before-after;
   - human context;
   - character/metaphor/paradox;
   - editorial/social-proof/promotion-led.

3. **VISUAL_CHARACTER**
   - flexible primary/secondary character;
   - `order_to_virality` axis;
   - `aesthetics_to_innovation` axis;
   - extensible `style_tags`.

4. **Focus budget / forbidden visuals / Creative Chaos Audit**
   - one-idea/hero/emotion/visual-language default as a heuristic;
   - global / brand / concept exclusions;
   - no accidental overload;
   - first generation is not final.

5. **Optional Creative Disruption Library**
   - pain visualization, paradox, personification, genre mask, unexpected comparison, narrative packaging etc.;
   - always a test hypothesis, never a claimed performance law.

### STYLE INTELLIGENCE — September 2026 layer implemented

Purpose: recommend a **visual strategy above the individual banner** instead of asking a model to pick a fashionable style name.

Canonical dependency:

`IDEA → PRESENTATION → EMOTION → CATEGORY → VISUAL CHARACTER → STYLE INTELLIGENCE → ATTENTION / TYPOGRAPHY → LIGHTING INTENT → ART DIRECTION`

Added:
- `config/style-intelligence-library.json` with snapshot date and refresh policy;
- `references/style-intelligence-2026.md`;
- `schemas/style-strategy-context.schema.json`;
- `schemas/style-strategy-recommendation.schema.json`;
- `schemas/style-strategy-gate.schema.json`;
- `scripts/recommend_visual_styles.py`;
- `scripts/validate_style_strategy_gate.py`;
- deterministic ranking regressions in `tests/test_style_intelligence.py`.

#### Layered strategy model

A strategy is composed from:
1. foundation grammar;
2. optional contemporary overlay;
3. execution language;
4. attention profile;
5. typography profile;
6. lighting affinity;
7. format resilience.

Current foundation profiles include:
- Clean Commercial / Swiss;
- Product Reality / Systems;
- Neo-Minimal / Quiet Luxury;
- Editorial Modern;
- Human Authentic;
- Bold Poster / Saturated;
- Controlled Maximalism / Dual Aesthetic;
- Local / Cultural Vernacular.

The library is deliberately extensible. User-provided examples can add reusable vocabulary without turning examples into rigid templates.

#### Current 2026 overlays

Currentness overlays include signals such as:
- Opt-Out Era;
- Explorecore;
- Texture Check / tactile material;
- Reality Warp;
- Prompt Playground / productivity aesthetic;
- Drama Club / cinematic;
- Human Connection;
- Local Flavor;
- Dual Aesthetics;
- Retro Futurism;
- Saturation Revival;
- Organic Flow.

Trend weight is capped at **5%**. Currentness can break a tie between already appropriate strategies; it cannot rescue a strategy that fails category, truth, attention, typography, lighting or format fit.

If the trend snapshot is older than the configured freshness window, currentness contribution becomes zero until refreshed.

#### Three recommendation lanes

The recommender creates exactly three decision-support lanes:
- `SAFE_STRONG`;
- `CURRENT_DIFFERENTIATED`;
- `CONTROLLED_WILDCARD`.

The wildcard is constrained to the task's disruption corridor. A HIGH-disruption job cannot pick quiet minimalism simply because it is different; a LOW-disruption enterprise job cannot pick chaotic maximalism merely for novelty.

#### Style selection provenance

Written art direction now carries:
- exact `style_strategy_id`;
- lane;
- style recommendation SHA;
- library snapshot date;
- foundation / overlay / execution / attention / typography component IDs.

`validate_style_strategy_gate.py` fails closed on:
- stale recommendation;
- strategy not present in the recommendation;
- component drift;
- lane drift;
- unsupported performance claim;
- campaign-design-system style drift.

The campaign design system carries the same style-strategy identity and exact recommendation SHA.

### Attention integration — implemented

Style recommendation includes an explicit attention profile rather than assuming style and hierarchy are independent.

Current attention profiles include:
- product proof;
- offer first;
- hero first;
- face/gaze guided;
- typographic statement;
- comparison;
- workflow;
- proof first.

These define intended scan path and salience budget. Eye-tracking research remains contextual evidence; no universal Z-pattern or fixed CTA position is claimed.

Final diagnostics still include actual-size, 25% thumbnail, grayscale and squint/blur views.

### Typography intelligence — September 2026 implemented

Updated `references/typography-color-contrast.md` and the style library with type-role profiles.

Current typography profiles include:
- enterprise variable sans;
- editorial serif + sans;
- quiet-luxury serif;
- humanist sans;
- condensed promotional display;
- technical mono accent;
- expressive display, controlled;
- soft serif / human trust;
- local/script-aware typography.

2026 signals such as serif resurgence in technology/AI branding and mature variable-font workflows are treated as **current cultural/production signals**, not conversion rules.

Font-source precedence:
1. approved brand font;
2. approved campaign/custom font;
3. style-intelligence role profile;
4. verified fallback.

Every actual font candidate must still pass license, local-file, language/script, Cyrillic/Belarusian glyph, weight/width and exact-raster checks.

### Lighting linked to meaning and style — implemented

Lighting is explicitly downstream of creative meaning and style strategy:

`CORE IDEA → PRESENTATION → EMOTION → VISUAL CHARACTER → STYLE STRATEGY → PRIMARY AOI → LIGHTING INTENT → SCENE/COMPOSITION LIGHTING`

Implemented:
- `lighting_intent` inside design brief;
- scene-light mode `REQUIRED / OPTIONAL / NOT_APPLICABLE`;
- justified candidate scheme IDs from the 30-scheme library;
- composition-light mode and primitive whitelist;
- copy-safe / focal-priority policies;
- forbidden lighting behaviors;
- real-UI/product-proof rule where fake relighting is prohibited;
- art direction inherits exact lighting identity;
- campaign design system can narrow but never expand allowed lighting primitives;
- independent reviews check lighting-intent fidelity, not just contrast.

### Structured generated-hero path — implemented contract

`schemas/hero-generation-spec.schema.json` binds:
- exact design brief;
- art direction;
- idea architecture;
- visual character;
- lighting intent;
- source format/composition/crop;
- subject/environment;
- scene lighting;
- forbidden elements.

Generated critical text/logo is explicitly forbidden. Generation is a source/draft stage, not a finished banner.

### Campaign Design System — implemented

After representative approval, `campaign-design-system.json` freezes:
- idea/character/lighting identity;
- selected style strategy and exact recommendation SHA;
- art direction;
- grid;
- headline/offer/CTA/brand behavior;
- hero/crop language;
- background/accent system;
- lighting system;
- whitespace;
- per-layout-family adaptation;
- forbidden patterns.

The representative becomes evidence of the system, not a canvas to resize.

### Verified deterministic milestone

Current verified pipeline milestone after Style Intelligence integration:
- full unittest suite: **147 tests, OK**;
- GitHub Actions push/PR checks: **PASS** on the Style Intelligence + 2026 typography integration head.

The suite now includes regressions for:
- enterprise real-UI strategy selection;
- fake/generated UI penalty;
- three distinct strategy lanes;
- capped trend influence;
- stale-trend currentness disable;
- runtime typography verification requirement;
- disruption-corridor wildcard selection;
- stale style recommendation SHA;
- component drift;
- campaign style drift.

### Current v0.2 validation work

Before v0.2 can be fully validated:

1. Continue the real Work MITGROUP task from the latest skill/reference set:
   - validate commercial/brand locks;
   - validate required real UI/logo assets;
   - resolve IDEA_ARCHITECTURE and visual character;
   - run Style Intelligence and inspect the three strategic lanes;
   - confirm selected strategy becomes the written art direction without component drift;
   - resolve lighting intent from the chosen meaning/style strategy;
   - create one representative 300x250 only after `ASSETS_READY`;
   - verify idea/emotion/style/character/lighting fidelity;
   - freeze campaign design system;
   - rerun style-strategy gate with campaign system;
   - only then test scale-out.
2. Incorporate the user's next creative/banner-style examples as reference DNA and reusable style-library vocabulary; evaluate whether they reveal additional gaps.
3. Execute six hidden-key visual eval cases through genuinely fresh visual reviewer contexts and score them.
4. Perform a genuinely independent final repository/PR review and reconcile important findings.
5. Merge only with explicit user approval.

If fresh independent reviewer contexts are unavailable, report this as an external rigor blocker instead of fabricating reports.

## v0.3 — Motion creative: GIF / video / HTML5

Planned after static v0.2 is proven:
- shared idea/brand/claim/art-direction/style contracts;
- `MotionIntent` bridge from Matreshka Content Factory;
- Remotion deterministic motion for code-motion ads;
- GIF duration/FPS/byte optimization and validator;
- video matrix across aspect/duration/language/variant;
- Content Factory bridge for footage/generated media/voice/rendered-evidence QA;
- HTML5 display as a separate production/validation path.

## v0.4 — Automated visual QA intelligence

Planned:
- AOI inventory;
- advisory saliency preflight;
- photographic glyph-region contrast maps;
- clutter/complexity heuristics;
- automatic brand/character/style consistency signals;
- lighting hotspot/noise checks;
- automated cross-size design drift;
- multi-agent visual-quality council;
- larger real-world eval corpus.

No automated visual score should be presented as CTR prediction.

## v0.5 — Performance feedback loop

Planned:
- Google Ads API integration;
- creative/asset ID ↔ local variant mapping;
- impressions/clicks/conversions/cost/value retrieval;
- controlled winner/loser analysis;
- evidence-based `CREATIVE_MEMORY.md` updates;
- next-test proposals without over-attributing causality;
- optional creative-analytics integrations when useful.
