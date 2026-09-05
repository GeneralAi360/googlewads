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

## Real acceptance failures that changed the system

### REAL-01

The first Work acceptance test created three technically valid but weak B2B 300x250 previews before sufficient market/category research. The directions shared nearly the same template and used toy-like/generic cloud imagery.

Permanent requirements:
- research before unresolved design;
- category map before art direction;
- three written directions before images;
- one high-fidelity representative before scale-out;
- explicit asset/category/anti-generic-AI quality gates.

### REAL-02

The next Work run produced a much stronger product-reality direction but still allowed art direction to introduce an unapproved CTA and ambiguous brand naming while correctly recognizing the need for real Bitrix24 UI.

Permanent requirements:
- `commercial_lock`;
- `brand_identity_lock`;
- `required_assets`;
- `representative-asset-manifest.json`;
- fail-closed `NEEDS_ASSET`;
- creative-freeze enforcement of approved CTA/proposition/brand identity.

Both cases live in `evals/real-world-failures.json`.

## Meaning before style

The user-supplied visual-methodology presentation added a semantic design layer. Its ideas are treated as **production heuristics**, not performance laws.

`references/idea-architecture-visual-character.md` formalizes:
- `IDEA_ARCHITECTURE`;
- presentation mode;
- emotional target;
- visual-character signature;
- focus budget;
- forbidden visuals;
- Creative Chaos Audit;
- generation-is-not-final workflow;
- campaign design system after representative approval.

### IDEA_ARCHITECTURE

A design brief now explicitly answers:
- what the visual means;
- what single takeaway should remain after a glance;
- how the idea is presented;
- which emotion/state it should create;
- what creative tension makes the concept non-generic;
- why this mechanism fits the communication problem.

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

The practical one-main-idea / one-main-hero / one-main-emotion / one-main-visual-language rule is used as a heuristic, not a universal law. More complex concepts require explicit rationale.

Before art direction the machine-readable audit checks idea clarity, presentation/emotion resolution, character coherence, lighting alignment, overload, composition, forbidden list, platform adaptation, and whether first generation is incorrectly treated as final.

## Lighting is connected to meaning

`references/lighting-intelligence.md` still contains the 30 practical lighting schemes, but their architectural role changed.

```text
CORE IDEA
→ PRESENTATION MODE
→ EMOTIONAL TARGET
→ VISUAL CHARACTER
→ PRIMARY AOI
→ LIGHTING INTENT
→ SCENE LIGHTING / COMPOSITION LIGHTING
```

The 30 schemes are candidate vocabulary inside `LIGHTING_INTENT`, not an independent style picker.

### LIGHTING_INTENT

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

Current deterministic primitives:
- `hero_edge_glow`;
- `spotlight`;
- `copy_scrim`;
- `vignette`;
- `text_plate`.

### Real UI special case

For truthful product-UI proof:
- scene lighting may be `NOT_APPLICABLE`;
- real UI colors remain truthful;
- fake photographic relighting/neon is prohibited by default;
- restrained keyline/scrim/separation is allowed only when needed.

Product truth outranks lighting spectacle.

## Structured Hero Generation

When `image_strategy.source_mode` is `GENERATED` or `HYBRID`, the system requires `hero-generation-spec.json` matching `schemas/hero-generation-spec.schema.json`.

It binds the exact brief, art direction, idea, visual character, lighting intent, format, subject, environment, crop/camera/copy-safe zone, lighting, emotion and forbidden elements.

Critical generated text/logo is prohibited:
- `generated_text_allowed=false`;
- `generated_logo_allowed=false`.

Generation is a source/draft stage:

`RAW → SELECT → REMOVE EXCESS → REFINE → ADD EXACT TYPE/BRAND/CTA → QUALITY PASS`

## Commercial and brand locks

`commercial_lock` freezes proposition, approved CTA allowlist, product/version, proof and required qualifiers.

Art direction changes CTA treatment, not CTA wording.

`brand_identity_lock` freezes one canonical brand ID/display name plus explicitly approved aliases.

## Real asset readiness

`representative-asset-manifest.json` + `scripts/validate_representative_assets.py` verifies file existence, SHA, source type, dimensions, substitution policy, privacy review, rights approval and real-logo requirements.

Missing required real UI/logo/product asset returns `NEEDS_ASSET`.

## Written art direction before images

Modes:
- `ART_DIRECTION_LOCKED`;
- `ART_DIRECTION_PREVIEW_3`;
- `ART_DIRECTION_AUTOSELECT_3`.

Preview/autoselect requires three materially different written systems before any preview image. Every approved direction inherits the frozen idea, presentation mode, emotional target, visual-character signature and lighting-intent ID.

## One representative before scale-out

One high-fidelity representative must PASS:
- idea fidelity;
- emotional fidelity;
- visual-character fidelity;
- lighting-intent fidelity;
- asset/category quality;
- hierarchy/type;
- brand/message fidelity;
- crop;
- lighting/contrast;
- CTA clarity;
- anti-generic-AI quality.

## Campaign Design System

After representative approval, `campaign-design-system.json` freezes:
- idea/character/lighting IDs;
- art direction;
- grid;
- headline/offer/CTA behavior;
- brand anchor;
- hero/crop language;
- background/accent;
- lighting system;
- whitespace;
- per-layout-family adaptation;
- forbidden patterns.

The representative is evidence of the system, not a master canvas to resize.

Campaign lighting may narrow the primitives allowed by the design brief, never expand them.

## Preproduction freeze

`scripts/freeze_preproduction_design.py` binds:

`research → category map → meaning/character/lighting design brief → art approval → representative → campaign design system → exact matrix`.

The result must be `PREPRODUCTION_FROZEN` before production scale-out.

## Creative binding and provenance

The following propagate through creative freeze → render spec → output manifest → review task:
- preproduction SHA;
- campaign-design-system ID/SHA;
- idea-architecture ID;
- visual-character ID;
- lighting-intent ID;
- art-direction ID;
- creative-contract identity;
- optional hero-generation-spec identity.

Worker drift is rejected.

## Deterministic rendering and Google preflight

One final matrix row = one traceable banner job.

The Pillow renderer owns exact copy/logo/fonts/layout/crop/dimensions/compression and deterministic composition lighting.

Formats are recomposed per layout family rather than resized from a master canvas.

`render_banner_pack.py` checks creative/design-system provenance and Google technical requirements before emitting the final manifest/contact sheet.

Technical PASS is not design PASS.

## Visual QA and independent review

Diagnostic views:
- actual;
- grayscale;
- squint/blur;
- 25% thumbnail.

Individual review checks idea, emotion, visual character, campaign design system, lighting intent, brand/category/assets, hierarchy/type/crop/contrast/CTA and anti-template quality.

Pack review checks those identities across sizes.

## Verified deterministic milestone

- full meaning-first / lighting-linked unittest suite: **136 tests, OK**;
- latest branch heads after documentation synchronization: GitHub Actions **PASS**.

Deterministic CI proves tooling/contracts, not independent visual judgment.

## Next acceptance step

The user's next banner-style examples will be analyzed as reference/style evidence and used to expand `VISUAL_CHARACTER`, `style_tags`, composition/typography/image/lighting DNA and, where useful, eval/regression cases.

They will **not** become a finite compulsory template list and will not be called high-converting without performance evidence.

See `docs/ROADMAP.md` and `docs/v0.2-release-gate.md`.

## Future

v0.3 remains reserved for motion creative: GIF/video/HTML5 architecture, Remotion and Content Factory integration after static v0.2 is proven.
