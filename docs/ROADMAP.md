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

The release candidate has been strengthened through real Work acceptance failures and two user-provided design methodologies: the 30-lighting-scheme guide and the 38-page `ВИЗУАЛ И УПАКОВКА` presentation.

Source-derived visual-methodology ideas are treated as production heuristics, not conversion laws.

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

Added after analysis of the user-supplied visual-methodology presentation:

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
   - extensible `style_tags`;
   - intentionally not frozen to a finite style list so future banner-style examples can expand it.

4. **Focus budget**
   - one-idea/hero/emotion/visual-language default as a heuristic;
   - more complex systems require explicit rationale.

5. **Forbidden visuals**
   - global / brand / concept layers.

6. **Creative Chaos Audit**
   - idea/takeaway/presentation/emotion/character resolved;
   - lighting supports idea;
   - no accidental overload;
   - composition intentional;
   - platform adaptation planned;
   - first generation is not final.

7. **Optional Creative Disruption Library**
   - pain visualization, paradox, personification, genre mask, unexpected comparison, narrative packaging etc.;
   - always a test hypothesis, never a claimed performance law.

### Lighting linked to meaning — implemented

Lighting is now explicitly downstream of creative meaning:

`CORE IDEA → PRESENTATION MODE → EMOTIONAL TARGET → VISUAL CHARACTER → PRIMARY AOI → LIGHTING INTENT → SCENE/COMPOSITION LIGHTING`

Implemented:
- `lighting_intent` inside design brief;
- scene-light mode `REQUIRED / OPTIONAL / NOT_APPLICABLE`;
- justified candidate scheme IDs from the 30-scheme library;
- composition-light mode and primitive whitelist;
- copy-safe / focal-priority policies;
- forbidden lighting behaviors;
- real-UI/product-proof rule where fake relighting is prohibited;
- art direction must inherit exact `lighting_intent_id`;
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

### Provenance and review — implemented

The following now propagate through creative freeze → render specs → output manifest → review tasks:
- preproduction SHA;
- campaign-design-system ID/SHA;
- idea-architecture ID;
- visual-character ID;
- lighting-intent ID;
- art-direction ID;
- creative-contract identity.

Worker drift is fail-closed.

Banner review now checks:
- idea fidelity;
- emotional fidelity;
- visual-character fidelity;
- campaign-design-system fidelity;
- lighting-intent fidelity.

Pack review checks those across sizes.

### Current v0.2 validation work

Before v0.2 can be fully validated:

1. Keep deterministic CI green on the final meaning-first/lighting-linked head.
2. Continue the real Work MITGROUP task from the updated skill:
   - validate commercial/brand locks;
   - validate required real UI/logo assets;
   - create one representative 300x250 only after `ASSETS_READY`;
   - verify idea/emotion/character/lighting fidelity;
   - freeze campaign design system;
   - only then test scale-out.
3. Incorporate the user's next banner-style examples as visual-character/reference vocabulary and evaluate whether they reveal additional system gaps.
4. Execute six hidden-key visual eval cases through genuinely fresh visual reviewer contexts and score them.
5. Perform a genuinely independent final repository/PR review and reconcile important findings.
6. Merge only with explicit user approval.

If fresh independent reviewer contexts are unavailable, report this as an external rigor blocker instead of fabricating reports.

## v0.3 — Motion creative: GIF / video / HTML5

Planned after static v0.2 is proven:
- shared idea/brand/claim/art-direction contracts;
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
- automatic brand/character consistency signals;
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
