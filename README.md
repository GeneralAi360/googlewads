# Google Ads Performance Banner Designer

A production-grade AI skill for researching, planning, designing, adapting, rendering, reviewing, validating, and iterating professional advertising banners for Google Ads.

The project intentionally treats banner creation as a **creative-production system**, not a single image prompt.

## Canonical pipeline

```text
BUSINESS CONTEXT
→ structured intake
→ run freeze + banner matrix
→ supplied-reference DNA
→ competitive creative research
→ category design map
→ IDEA_ARCHITECTURE
→ presentation mode
→ emotional target
→ VISUAL_CHARACTER
→ focus budget / forbidden list / chaos audit
→ commercial + brand locks
→ LIGHTING_INTENT
→ detailed design brief
→ 3 written art directions when unresolved
→ written art-direction approval
→ representative asset readiness
→ optional HERO_GENERATION_SPEC
→ generation/select/refine when generation is used
→ one high-fidelity representative
→ representative approval
→ CAMPAIGN_DESIGN_SYSTEM
→ PREPRODUCTION_FROZEN
→ frozen creative contracts
→ one job per final output
→ exact format recomposition
→ deterministic render
→ Google technical preflight
→ manifest/contact sheet
→ actual/grayscale/squint/thumbnail QA
→ independent banner reviews
→ pack review
→ readiness
→ delivery
→ performance learning
```

The full pack is deliberately not rendered before one representative design proves the idea, visual character, lighting behavior, and professional quality.

## Current development

Branch: `dev/performance-banner-designer-v0.2`

Draft PR: `#2`.

`main` remains unchanged.

## Why the preproduction system became strict

### REAL-01

The first Work acceptance test created three technically valid but weak B2B 300x250 previews before sufficient market/category research. The directions shared nearly the same template and used toy-like/generic cloud imagery.

This produced permanent requirements:
- research before unresolved design;
- category map before art direction;
- three written directions before images;
- one high-fidelity representative before scale-out;
- explicit asset/category/anti-generic-AI quality gates.

### REAL-02

The next Work run produced a much stronger product-reality direction but still allowed art direction to introduce an unapproved CTA and ambiguous brand naming while correctly recognizing the need for real Bitrix24 UI.

This produced:
- `commercial_lock`;
- `brand_identity_lock`;
- `required_assets`;
- `representative-asset-manifest.json`;
- fail-closed `NEEDS_ASSET` behavior;
- creative-freeze enforcement of approved CTA/proposition/brand identity.

Both cases live in `evals/real-world-failures.json`.

## Meaning before style

The user-supplied visual-methodology presentation added a new semantic design layer. Its concepts are treated as **production heuristics**, not performance laws.

`references/idea-architecture-visual-character.md` formalizes:
- `IDEA_ARCHITECTURE`;
- presentation mode;
- emotional target;
- visual-character signature;
- focus budget;
- forbidden visuals;
- creative chaos audit;
- generation-is-not-final workflow;
- campaign design system after representative approval.

### IDEA_ARCHITECTURE

A design brief now explicitly answers:
- what the visual means;
- what one takeaway should remain after a glance;
- how the idea is presented;
- which emotion/state it should create;
- what creative tension makes the concept non-generic;
- why this visual mechanism fits the communication problem.

Supported presentation modes include product proof, outcome/pain visualization, explainer, workflow, before/after, human context, character, metaphor, paradox, editorial statement, social proof and promotion-led execution.

## Visual Character

Style is modeled as a flexible system rather than a rigid preset list.

`visual_character` contains:
- `primary_character`;
- optional secondary character;
- `order_to_virality` from 0..1;
- `aesthetics_to_innovation` from 0..1;
- extensible `style_tags`;
- rationale.

This is deliberately open-ended. Additional banner-style examples can extend the vocabulary without turning the skill into a list of templates.

## Focus budget and Creative Chaos Audit

The practical “one main idea / one main hero / one main emotion / one main visual language” rule is used as a heuristic, not a universal law. More complex concepts require explicit rationale.

Before art direction, the machine-readable chaos audit verifies:
- idea and takeaway are clear;
- presentation and emotion are resolved;
- visual character is coherent;
- lighting supports the idea;
- information is not overloaded;
- composition is intentional;
- forbidden list exists;
- platform adaptation is planned;
- first generation is not treated as final.

## Lighting is connected to meaning

`references/lighting-intelligence.md` still contains the 30 practical lighting schemes, but their role changed.

Lighting is now downstream of meaning:

```text
CORE IDEA
→ PRESENTATION MODE
→ EMOTIONAL TARGET
→ VISUAL CHARACTER
→ PRIMARY AOI
→ LIGHTING INTENT
→ SCENE LIGHTING / COMPOSITION LIGHTING
```

The 30 schemes are candidate vocabulary inside `LIGHTING_INTENT`, not a menu that a worker may choose because something “looks cool.”

### `LIGHTING_INTENT`

It records:
- relationship of light to the idea;
- primary AOI role;
- emotional function;
- visual-character alignment;
- scene-lighting mode;
- candidate scheme IDs where applicable;
- composition-lighting mode;
- allowed deterministic primitives;
- copy-safe strategy;
- focal priority;
- forbidden lighting behavior.

Scene/composition lighting can each be `REQUIRED`, `OPTIONAL`, or `NOT_APPLICABLE`.

Current deterministic composition primitives:
- `hero_edge_glow`;
- `spotlight`;
- `copy_scrim`;
- `vignette`;
- `text_plate`.

### Real UI special case

For a truthful product-UI proof concept:
- scene lighting may be `NOT_APPLICABLE`;
- real UI colors must remain truthful;
- fake photographic relighting/neon is not allowed by default;
- restrained separation/keyline/scrim may be used only when needed.

Product truth outranks lighting spectacle.

## Structured Hero Generation

When `image_strategy.source_mode` is `GENERATED` or `HYBRID`, the system requires `hero-generation-spec.json` matching `schemas/hero-generation-spec.schema.json`.

The spec binds:
- exact design brief;
- art direction;
- idea architecture;
- visual character;
- lighting intent;
- format/aspect/source resolution;
- subject/action/environment;
- crop/camera/copy-safe zone;
- lighting;
- emotion;
- forbidden elements.

Critical text and logos remain deterministic:
- `generated_text_allowed=false`;
- `generated_logo_allowed=false`.

Generation follows:

`RAW -> SELECT -> REMOVE EXCESS -> REFINE COMPOSITION -> ADD EXACT TYPE/BRAND/CTA -> QUALITY PASS`

## Commercial and brand locks

`commercial_lock` freezes exact proposition, approved CTA allowlist, product/version, proof and required qualifiers.

Art direction can change how CTA looks, not what it says.

`brand_identity_lock` freezes one canonical brand ID/display name plus explicitly approved aliases.

If identity is ambiguous, production stops instead of guessing.

## Real asset readiness

`representative-asset-manifest.json` + `scripts/validate_representative_assets.py` verifies real required assets before representative rendering.

The validator checks:
- file existence;
- SHA;
- accepted source type;
- actual raster dimensions;
- substitution policy;
- privacy review;
- rights approval;
- real-logo requirements.

If a required real UI/logo/product asset is missing, the correct status is `NEEDS_ASSET`.

## Written art direction before images

Art-direction modes:
- `ART_DIRECTION_LOCKED`;
- `ART_DIRECTION_PREVIEW_3`;
- `ART_DIRECTION_AUTOSELECT_3`.

Preview/autoselect requires three materially different written systems before any preview image. Every approved direction inherits the frozen idea, presentation mode, emotional target, visual-character signature and lighting-intent ID.

A color or illustration swap is not a different art direction.

## One representative before scale-out

One high-fidelity representative must PASS:
- idea fidelity;
- emotional fidelity;
- visual-character fidelity;
- lighting-intent fidelity;
- asset quality;
- professional category fit;
- hierarchy;
- typography;
- brand/message fidelity;
- crop;
- lighting/contrast;
- CTA clarity;
- anti-generic-AI quality.

Its approval is SHA-bound to the exact artifact.

## Campaign Design System

After representative approval, `campaign-design-system.json` becomes the cross-size source of truth.

It freezes:
- idea/character/lighting IDs;
- grid/alignment logic;
- headline/offer/CTA behavior;
- brand-anchor behavior;
- hero/crop treatment;
- background/accent systems;
- lighting system;
- whitespace character;
- per-layout-family adaptation rules;
- forbidden patterns.

The representative is proof of the system, not a master canvas to resize.

Campaign lighting may narrow the primitives allowed by the design brief, never expand them.

## Preproduction freeze

`scripts/freeze_preproduction_design.py` now binds:

```text
competitive research
→ category map
→ design brief
  ↳ commercial/brand locks
  ↳ idea architecture
  ↳ emotional target
  ↳ visual character
  ↳ focus/forbidden/chaos audit
  ↳ lighting intent
→ written art-direction approval
→ representative approval
→ campaign design system
→ exact banner matrix
```

The result must be `PREPRODUCTION_FROZEN` before production scale-out.

## Creative binding and provenance

Creative freeze propagates into every render spec and final manifest:
- preproduction freeze SHA;
- campaign-design-system ID/SHA;
- idea-architecture ID;
- visual-character signature ID;
- lighting-intent ID;
- art-direction ID;
- creative-contract SHA;
- references/sources;
- lighting scheme;
- optional hero-generation-spec identity.

Worker mutation of frozen identity is rejected.

## One job per output and deterministic rendering

One final matrix row = one traceable `BANNER_DESIGNER` job.

The Pillow renderer owns exact copy/logo/fonts/layout/crop/dimensions/compression and deterministic composition-lighting primitives.

Formats are recomposed per layout family rather than resized from a master canvas.

## Google technical preflight

`scripts/render_banner_pack.py` checks matrix/spec identity, creative/design-system provenance, exact dimensions/type/size/static state and Google constraints, then creates contact sheet + manifest only for a passing pack.

Technical PASS is not design PASS.

## Visual QA and independent review

Diagnostic views:
- actual;
- grayscale;
- squint/blur;
- 25% thumbnail.

Each independent banner review now checks concept plus:
- idea fidelity;
- emotional fidelity;
- visual-character fidelity;
- campaign-design-system fidelity;
- lighting-intent fidelity;
- asset/category/brand quality;
- hierarchy/type/crop/contrast/CTA;
- anti-template / anti-generic-AI behavior.

Pack review checks the same identities across sizes, including cross-size lighting-intent consistency.

## Current verification boundary

Deterministic CI validates the contracts/tooling. It does not prove that an independent model has good visual judgment.

Remaining release validation still includes real Work acceptance, fresh visual-review eval execution and genuinely independent final repository review. See `docs/v0.2-release-gate.md`.

## Future

v0.3 remains reserved for motion creative: GIF/video/HTML5 architecture, Remotion and Content Factory integration. Static v0.2 must first prove the complete meaning-to-design-to-pack workflow.
