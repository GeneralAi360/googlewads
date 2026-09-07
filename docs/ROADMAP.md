# Roadmap

## v0.1 — Foundation, orchestration, lighting, Google preflight

Status: **implemented**.

Implemented:
- controller / Matreshka-style subagent architecture;
- Google mode and size registry;
- evidence hierarchy;
- visual-attention, typography, color, contrast, density references;
- 30-scheme lighting vocabulary;
- static Google technical validator.

## v0.2 — Meaning-to-reviewed-and-policy-preflight static production system

Status: **active release-candidate hardening in `dev/performance-banner-designer-v0.2`; not merged**.

The release candidate has been strengthened through real Work acceptance failures, user-provided visual methodologies, September 2026 style/banner/typography research, and a September 7 2026 review of current official Google Advertising Policies.

Source-derived design ideas and trend signals are production heuristics/currentness evidence, not conversion laws. Local policy preflight is risk reduction, not a guarantee of Google approval.

### Core implemented foundation

- structured intake and output ambiguity detection;
- immutable run freeze and banner matrix;
- supplied-reference / REFERENCE_DNA path;
- Competitive Creative Intelligence and A–E performance-evidence tiers;
- category design map;
- `IDEA_ARCHITECTURE`, presentation mode, emotional target and visual character;
- September 2026 Style Intelligence + attention/typography strategy;
- focus budget / forbidden visuals / Creative Chaos Audit;
- commercial-message / CTA and brand-identity locks;
- real-asset / `NEEDS_ASSET` gate;
- pre-render Google policy-risk screen;
- meaning/style/AOI-linked `LIGHTING_INTENT`;
- written art-direction approval;
- one high-fidelity representative before scale-out;
- frozen campaign design system and preproduction/creative SHA binding;
- one job per final output;
- exact Pillow renderer and per-layout-family recomposition;
- Google technical preflight;
- visual diagnostics / independent banner and pack review;
- Google Ads exact-artifact policy preflight;
- pack-level policy aggregation;
- final local Google-ready precheck;
- hidden-key visual-review eval harness;
- real user-acceptance regression corpus (`REAL-01`, `REAL-02`).

### Meaning-first design layer — implemented

`IDEA_ARCHITECTURE` resolves core idea, single takeaway, presentation mode, emotional target, creative tension, rationale and disruption level before style.

`VISUAL_CHARACTER` records a flexible character signature and axes rather than a closed list of style presets.

Focus budget, forbidden visuals and Creative Chaos Audit prevent accidental complexity and first-generation-is-final behavior.

Optional Creative Disruption methods remain test hypotheses, not performance laws.

### STYLE INTELLIGENCE — September 2026 implemented

Purpose: recommend a **visual strategy above the individual banner** rather than asking a model to pick a fashionable style name.

Canonical dependency:

`IDEA → PRESENTATION → EMOTION → CATEGORY → VISUAL CHARACTER → STYLE INTELLIGENCE → ATTENTION / TYPOGRAPHY → POLICY RISK → LIGHTING INTENT → ART DIRECTION`

Implemented:
- `config/style-intelligence-library.json`;
- `references/style-intelligence-2026.md`;
- strategy context/recommendation/gate schemas;
- `scripts/recommend_visual_styles.py`;
- `scripts/validate_style_strategy_gate.py`;
- style ranking/drift regressions.

A strategy composes foundation grammar, optional current overlay, execution language, attention profile, typography profile, lighting affinity and format resilience.

Currentness is capped at 5%. A trend cannot rescue weak category/truth/attention/type/light/format fit. Stale trend data disables currentness until refreshed.

The recommender creates `SAFE_STRONG`, `CURRENT_DIFFERENTIATED`, and `CONTROLLED_WILDCARD`; wildcard stays inside the requested disruption corridor.

The chosen strategy, recommendation SHA and exact foundation/overlay/execution/attention/typography IDs are frozen through art direction and campaign design system.

### Attention and typography — implemented

Attention strategy expresses intended scan path and salience budget instead of assuming a universal Z-pattern or fixed CTA location.

Typography is role-based. Actual fonts require runtime verification for license, real local file, language/script, Cyrillic/Belarusian glyph quality where needed, weights/widths and exact-raster readability.

2026 serif/variable-font signals are cultural/production signals, not conversion rules.

### Lighting linked to meaning and style — implemented

`CORE IDEA → PRESENTATION → EMOTION → VISUAL CHARACTER → STYLE STRATEGY → PRIMARY AOI → LIGHTING INTENT → SCENE/COMPOSITION LIGHTING`

The 30 lighting schemes are candidate vocabulary, not a free-standing style picker.

Real UI/product-proof can make scene lighting `NOT_APPLICABLE`; truthful product evidence outranks spectacle.

### Campaign Design System — implemented

After representative approval, `campaign-design-system.json` freezes semantic/style/lighting identity plus grid, type/offer/CTA/brand behavior, hero/crop language, background/accent, whitespace, format adaptations and forbidden patterns.

The representative is evidence of the system, not a canvas to resize.

### Google Ads Policy Preflight — September 7 2026 implemented

Purpose: reduce disapproval risk **before and after** rendering without pretending that local tooling can guarantee moderation approval.

Implemented:
- `references/google-ads-policy-preflight.md`;
- `config/google-ads-policy-snapshot.json`;
- `schemas/google-policy-context.schema.json`;
- `schemas/google-policy-report.schema.json`;
- `scripts/validate_google_policy.py`;
- `scripts/aggregate_google_policy_reports.py`;
- `scripts/assess_google_ready.py`;
- policy preflight and pack aggregation regressions.

#### Pre-render policy risk

Before art direction is finalized, resolve vertical/category, target geography, material claims/qualifiers, third-party trademark/affiliation state, destination support, certification/targeting concerns and obvious misleading-design exclusions.

#### Final exact-artifact policy preflight

Each final banner policy review is bound to exact output SHA and combines exact creative/copy, advertiser identity, claims, landing page, trademark context and vertical/geo/targeting evidence.

Explicit misleading-design checks include fake system/dialog/menu/request UI, non-functional controls, download/install UI, misleading pseudo-interactions, transparent background, segmented/multi-ad appearance and contextless/disproportionate standalone buttons.

Material claims require verified evidence and destination support. Advertised offers/CTA must be available/easy to find from the destination.

Destination evidence covers working URL, domain/relevance, AdsBot crawlability state, target-geo accessibility, advertiser identity and useful/original content.

Trademark and restricted-vertical decisions are contextual. Unresolved evidence returns review-required rather than invented permission.

Policy statuses:
- `GOOGLE_POLICY_PREFLIGHT_PASS`;
- `GOOGLE_POLICY_PREFLIGHT_BLOCKED`;
- `GOOGLE_POLICY_PREFLIGHT_INCOMPLETE`;
- `POLICY_REVIEW_REQUIRED`.

Every final output must have an exact-SHA PASS report before pack policy aggregation passes.

`GOOGLE_READY_PRECHECK_PASS` requires ordinary design/readiness + policy PASS and still sets `google_upload_approval_guaranteed=false`.

### Verified deterministic milestone

Current canonical pipeline:
- full unittest suite: **157 tests, OK**;
- canonical Style Intelligence + Google Policy `SKILL.md`: GitHub Actions **PASS**.

The suite includes style selection/drift, real-UI truth, typography runtime policy, lighting, misleading-design, PNG transparency, material claim, destination incompleteness, trademark review, policy-SHA and pack aggregation regressions.

### Current v0.2 validation work

Before v0.2 can be fully validated:

1. Continue the real Work MITGROUP task:
   - resolve exact commercial/brand/asset facts;
   - resolve idea/visual character;
   - run/approve Style Intelligence;
   - run pre-render Google policy risk;
   - derive lighting intent;
   - render and approve one representative 300x250;
   - freeze campaign design system;
   - only then scale out;
   - run exact-artifact policy preflight against final MITGROUP banner(s), real offer/landing page and Bitrix24 trademark/advertiser-role context;
   - require pack policy PASS before a Google-ready claim.
2. Incorporate next user style examples as reference DNA/reusable style vocabulary.
3. Execute six hidden-key visual evals in genuinely fresh reviewer contexts.
4. Perform genuinely independent final repository/PR review.
5. Merge only with explicit user approval.

## v0.3 — Motion creative: GIF / video / HTML5

Planned after static v0.2 is proven:
- shared idea/brand/claim/art-direction/style/policy contracts;
- `MotionIntent` bridge from Matreshka Content Factory;
- Remotion deterministic motion;
- GIF duration/FPS/byte optimization and validator;
- motion-specific Google technical/policy checks;
- video matrix across aspect/duration/language/variant;
- Content Factory bridge for footage/generated media/voice/evidence QA;
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
