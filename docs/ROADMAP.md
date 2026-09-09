# Roadmap

## v0.1 — Foundation, orchestration, lighting, Google technical preflight

Status: **implemented**.

Implemented:

- controller / Matreshka-style subagent architecture;
- Google mode / size registry;
- evidence hierarchy;
- visual-attention, typography, color, contrast and density references;
- 30-scheme lighting vocabulary;
- deterministic static Google technical validator.

## v0.2 — Meaning-to-user-approved-and-policy-preflight static production system

Status: **active release-candidate hardening in `dev/performance-banner-designer-v0.2`; not merged**.

The release candidate is being hardened through real Work acceptance failures, user-provided visual methodology, September 2026 style/banner/typography research, and current Google Advertising Policy review.

Source-derived design ideas and trend signals remain heuristics/currentness evidence rather than conversion laws. Local policy preflight reduces risk but never guarantees Google approval.

### Canonical v0.2 UX

`QUESTIONS / INTAKE`
`→ EXACT COMMERCIAL JOB LOCK`
`→ RESEARCH / CATEGORY`
`→ IDEA / VISUAL CHARACTER`
`→ STYLE INTELLIGENCE`
`→ ATTENTION / TYPOGRAPHY`
`→ POLICY RISK`
`→ LIGHTING INTENT`
`→ INTERNAL ART DIRECTION`
`→ FIRST-ROUND VISUAL EXPLORATION`
`→ USER SELECTS / REVISES / APPROVES`
`→ PRODUCTION ASSETS / FIDELITY`
`→ CAMPAIGN DESIGN SYSTEM`
`→ FULL STATIC PRODUCTION`
`→ GOOGLE TECHNICAL PREFLIGHT`
`→ DESIGN REVIEW`
`→ FINAL GOOGLE POLICY PREFLIGHT`
`→ GOOGLE_READY_PRECHECK`

### Real acceptance regressions

The current permanent corpus contains:

- `REAL-01` — premature rendering + generic/toy B2B visuals;
- `REAL-02` — CTA/brand drift + real-asset truth;
- `REAL-03` — production asset blocker applied too early;
- `REAL-04` — text-only approval substituted for visual approval;
- `REAL-05` — production `NEEDS_ASSET` hid the user-facing concept;
- `REAL-06` — wrong commercial job + internal recommendation treated as user lock + only one weak concept shown.

### Exact commercial-job lock — implemented

Product identity, campaign objective, CTA and exact commercial job are separate.

Implemented:

- `references/commercial-job-and-concept-exploration.md`;
- `schemas/campaign-commercial-job.schema.json`;
- `scripts/validate_campaign_commercial_job.py`;
- intake Q10 requires both product/service and exact commercial job;
- material job changes invalidate stale downstream strategy/visuals;
- purchase/renewal campaigns resolve `COMBINED` vs `SEPARATE_VARIANTS`;
- business-brief schema exposes `campaign.commercial_job` and `business.product_service`.

### First-round visual exploration — implemented

Final campaign concept count is separate from exploration count.

Unless explicit user-lock evidence exists:

`visual_exploration_count = 3`

The first round must show three materially different rendered concepts in one representative size.

Implemented:

- `schemas/visual-concept-set.schema.json`;
- `scripts/validate_visual_concept_set.py`;
- `EXPLORE_3` vs `SINGLE_USER_LOCKED` semantics;
- internal recommendation cannot count as `USER_LOCKED`;
- pairwise distinction across hero/composition/attention/type/graphic-device/light axes;
- exact commercial-job binding on concept previews;
- pre-show `ART_DIRECTOR_REVIEWER` quality gate;
- explicit `ad_not_presentation_slide` rejection;
- A/B/C comparison/contact-sheet contract.

### Meaning-first design layer — implemented

`IDEA_ARCHITECTURE` resolves core idea, takeaway, presentation mode, emotional target, creative tension, rationale and disruption level before style.

`VISUAL_CHARACTER` records a flexible character signature rather than a closed style preset.

Focus budget, forbidden visuals and Creative Chaos Audit prevent accidental complexity and first-generation-is-final behavior.

Creative disruption remains optional test-hypothesis vocabulary, not performance law.

### Style Intelligence — September 2026 implemented

The system recommends a strategy above the banner:

`foundation grammar + current overlay + execution language + attention profile + typography profile + lighting affinity + format resilience`.

Implemented:

- `config/style-intelligence-library.json`;
- `references/style-intelligence-2026.md`;
- context/recommendation/gate schemas;
- `scripts/recommend_visual_styles.py`;
- `scripts/validate_style_strategy_gate.py`.

Decision-support lanes:

- `SAFE_STRONG`;
- `CURRENT_DIFFERENTIATED`;
- `CONTROLLED_WILDCARD`.

Currentness remains capped; it cannot rescue weak category fit, product truth, attention, typography, lighting or format resilience.

### Attention / typography — implemented

Attention uses intended scan path and salience budget rather than a universal Z-pattern or fixed CTA position.

Typography is role-based. Actual font use requires runtime checks for file, license, script/Cyrillic support, available weights/widths and exact-raster readability.

### Lighting linked to meaning — implemented

Canonical dependency:

`IDEA → PRESENTATION → EMOTION → VISUAL CHARACTER → STYLE STRATEGY → PRIMARY AOI → LIGHTING INTENT → SCENE / COMPOSITION LIGHTING`.

The 30 lighting schemes are candidate vocabulary, not a performance ranking. Real UI/product proof can make scene lighting `NOT_APPLICABLE`.

### Asset truth + concept visibility — implemented

Production `NEEDS_ASSET` remains fail closed for final production but no longer blocks upstream strategy or safe concept visibility.

Concept preview supports declared:

- `REFERENCE_ONLY_SURROGATE`;
- `LOW_RES_AUTHENTIC_SURROGATE`;
- `STRUCTURAL_PLACEHOLDER`;
- `TEXT_BRAND_PLACEHOLDER`.

Fake/generated product UI and fake/generated logos remain prohibited.

A preview with temporary asset slots stays `not_for_delivery=true` and cannot unlock full production until real assets and fidelity gates pass.

### User visual approval — implemented

Written art direction is internal. The user approves rendered design.

User decision states:

- `APPROVE`;
- `REVISE`;
- `REJECT`.

Exact visual bytes are SHA-bound.

After approval of a concept with temporary asset slots, real-asset substitution may continue without a second approval only when the visual-system fidelity review is `PASS`; `MATERIAL_DRIFT` requires reapproval.

### Campaign Design System — implemented

After valid user-rooted visual approval, `campaign-design-system.json` freezes reusable design grammar:

- semantic/style/lighting IDs;
- grid;
- type roles;
- commercial message/CTA/brand behavior;
- hero/crop language;
- background/accent;
- whitespace/density;
- format adaptation;
- forbidden patterns.

Other sizes recompose instead of mechanically resizing the representative.

### Google Ads Policy Preflight — implemented

Separate from Google technical validity.

Implemented:

- `references/google-ads-policy-preflight.md`;
- dated policy snapshot;
- policy context/report schemas;
- exact-SHA semantic policy review;
- misleading-design checks;
- image/text quality checks;
- claims/qualifiers/destination support;
- advertiser identity / affiliation / trademark context;
- restricted-vertical/certification/targeting state;
- pack policy aggregation;
- final `GOOGLE_READY_PRECHECK_PASS`.

No local gate promises actual Google moderation approval.

### Deterministic verification

**202 tests — OK.**

GitHub Actions run `34223811999` / #541 completed **SUCCESS** after REAL-06 commercial-job / three-concept exploration hardening and business-brief schema alignment.

### Remaining v0.2 acceptance work

1. Re-run MITGROUP from the corrected commercial job:
   - Bitrix24 license purchase / renewal, not implementation;
   - resolve combined vs separate purchase/renewal structure.
2. Do not reuse A2 as a user-approved direction.
3. Render three materially different 300x250 first-round concepts.
4. Pre-review all three before presentation.
5. Show A/B/C comparison + individual concepts + concept cards.
6. Capture user selection.
7. Revise selected direction until explicit visual `APPROVE`.
8. Resolve selected-system production assets/fidelity.
9. Freeze campaign design system and scale out requested static formats.
10. Run exact-artifact Google technical + policy preflight on the real pack.
11. Execute hidden-key visual evals in genuinely fresh reviewer contexts.
12. Perform independent final repository/PR review.
13. Merge only with explicit user approval.

## v0.3 — Motion creative: GIF / video / HTML5

Planned after static v0.2 is proven:

- shared meaning/brand/commercial/style/policy contracts;
- `MotionIntent` bridge from Matreshka Content Factory;
- Remotion deterministic motion;
- GIF duration/FPS/byte optimization and validator;
- motion-specific Google technical/policy checks;
- video matrix across aspect/duration/language/variant;
- Content Factory bridge for footage/generated media/evidence QA;
- HTML5 as a separate production/validation path.

## v0.4 — Automated visual QA intelligence

Planned:

- AOI inventory;
- advisory saliency preflight;
- photographic glyph-region contrast maps;
- clutter/complexity heuristics;
- automated cross-size design drift;
- visual-character/style consistency signals;
- lighting hotspot/noise checks;
- multi-agent visual-quality council;
- larger real-world eval corpus.

No automated visual score will be presented as CTR prediction.

## v0.5 — Performance feedback loop

Planned:

- Google Ads API integration;
- creative/asset ID ↔ local variant mapping;
- impressions/clicks/conversions/cost/value retrieval;
- controlled winner/loser analysis;
- evidence-based creative memory;
- next-test proposals without over-attributing causality.
