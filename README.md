# Google Ads Performance Banner Designer

A production-grade AI skill for researching, planning, visually exploring, composing, reviewing, adapting, rendering, validating and policy-preflighting professional advertising banners for Google Ads.

The project treats banner creation as a **creative-production system**, not a single image prompt.

## Canonical user-facing pipeline

```text
BUSINESS CONTEXT
→ structured intake
→ EXACT COMMERCIAL JOB LOCK
→ output envelope / matrix
→ references + competitive/category research
→ IDEA_ARCHITECTURE / presentation / emotion
→ VISUAL_CHARACTER
→ STYLE INTELLIGENCE
→ attention + typography
→ PRE-RENDER GOOGLE POLICY RISK
→ LIGHTING_INTENT
→ internal art direction
→ first-round visual exploration
→ optional component-asset generation
→ COMPLETE 300x250 BANNER COMPOSITES
→ TWO FRESH EXACT-ARTIFACT PRE-SHOW REVIEWS PER CONCEPT
→ USER SELECTS / REVISES / APPROVES
→ production assets / fidelity
→ CAMPAIGN_DESIGN_SYSTEM
→ full format recomposition
→ GOOGLE TECHNICAL PREFLIGHT
→ design QA / independent review
→ FINAL GOOGLE ADS POLICY PREFLIGHT
→ exact-SHA policy pack aggregation
→ GOOGLE_READY_PRECHECK
→ delivery / performance learning
```

The full pack is never scaled out before a valid user-rooted visual approval path passes.

## Current development

- Branch: `dev/performance-banner-designer-v0.2`
- Draft PR: `#2`
- `main` remains unchanged.

## Real acceptance regressions

The current release candidate is being hardened against failures discovered in real ChatGPT Work runs:

- `REAL-01` — generic/toy-like B2B art rendered before sufficient market/category research;
- `REAL-02` — unapproved CTA/brand drift and missing real-product asset truth;
- `REAL-03` — production `NEEDS_ASSET` incorrectly stopped upstream semantic/style work;
- `REAL-04` — text-only art-direction approval substituted for approval of rendered design;
- `REAL-05` — missing production assets left the user with no visual concept to judge;
- `REAL-06` — wrong commercial job, internal recommendation treated as a user lock, insufficient first-round exploration, presentation-slide-like work;
- `REAL-07` — raw generated hero imagery was treated as presentation-ready banner design and pre-show review produced a false positive.

Canonical cumulative regression corpus: `evals/real-world-failures.json`.

## Exact commercial job

Product identity, campaign objective, CTA and commercial job are different facts.

For example, Bitrix24 may be the product while the campaign job is:

- `NEW_LICENSE_PURCHASE`;
- `LICENSE_RENEWAL`;
- `PURCHASE_OR_RENEWAL`;
- `IMPLEMENTATION_SERVICE`;
- `CONSULTATION`.

A material job change invalidates stale downstream creative meaning instead of patching the old design with new copy.

Relevant contracts:

- `references/commercial-job-and-concept-exploration.md`
- `schemas/campaign-commercial-job.schema.json`
- `scripts/validate_campaign_commercial_job.py`

## First-round visual exploration

`deliverables.concept_count` is the final production concept count, not the number of alternatives shown before visual selection.

Unless the user explicitly locked a direction, the first visual round is:

`EXPLORE_3`

Three concepts share the same frozen commercial facts but differ materially across visual grammar. Every pair must differ on at least three of:

- hero logic;
- composition system;
- attention profile;
- typography profile;
- graphic device;
- lighting language.

An internal Style Intelligence/controller/reviewer recommendation is not `USER_LOCKED` provenance.

## REAL-07: raw hero != complete banner

A generated image, photograph, product/UI crop, illustration, texture or 3D object is an upstream component such as:

`HERO_ASSET_CANDIDATE`.

It is not the visual concept the user approves.

The only valid user-facing concept role is:

`BANNER_COMPOSITE`.

A complete concept must already include the visible advertising system, including primary message, commercial-job cue, CTA and brand anchor.

The canonical boundary is:

```text
RAW / GENERATED / REFERENCE ASSET
→ select / refine
→ BANNER COMPOSITION
→ deterministic typography / CTA / brand
→ exact representative raster
→ pre-show review
→ user
```

Never:

```text
image-generation output
→ call it a banner concept
→ reviewer PASS
→ user approval
```

See `references/concept-composite-and-pre-show-quality.md`.

## Exact concept validation

`schemas/visual-concept-preview.schema.json` and `scripts/validate_visual_concept_preview.py` require:

- `artifact_role = BANNER_COMPOSITE`;
- `render_stage = USER_FACING_CONCEPT_COMPOSITE`;
- exact commercial-job binding;
- exact artifact SHA;
- actual PNG/JPEG decoding;
- actual dimensions matching declared dimensions;
- explicit composition method;
- mandatory message/commercial cue/CTA/brand roles;
- all raw generated asset paths;
- `raw_generated_asset_is_final_artifact=false`;
- safe concept-only asset-slot semantics where production assets are pending.

A raw generated asset cannot reuse the final concept path.

## Two fresh pre-show art-director reviews

Each first-round concept requires exactly two reports matching `schemas/pre-show-visual-review.schema.json`.

Both reviewers inspect the exact complete banner bytes and must have:

- different `reviewer_context_id` values;
- `fresh_context=true`;
- `prior_review_verdict_visible=false`.

`PRESENTATION_READY_DESIGN` requires evidence-bearing PASS for:

- commercial-job fidelity;
- complete banner composite;
- primary-message visibility;
- CTA visibility/integration;
- brand-anchor visibility;
- hero semantic relevance;
- advertising impact;
- compositional confidence;
- typographic craft;
- visual polish;
- category premium bar;
- non-generic identity;
- ad-not-presentation-slide;
- small-format viability.

The user should not be the first basic visual QA pass.

## Asset truth and visual approval

Production asset readiness and concept visibility are separate concerns.

Safe concept-only modes can communicate the visual system while production remains `NEEDS_ASSET`:

- `REFERENCE_ONLY_SURROGATE`;
- `LOW_RES_AUTHENTIC_SURROGATE`;
- `STRUCTURAL_PLACEHOLDER`;
- `TEXT_BRAND_PLACEHOLDER`.

Fake/generated product UI and fake logos remain prohibited.

The user selects/revises/approves the rendered design. Written art direction and raw image-generation assets cannot substitute for visual approval.

After approved concept-only asset slots are replaced with real assets, a fidelity gate may continue without redundant approval only when there is no material visual drift.

## Meaning / Style / Attention / Typography / Lighting

The skill resolves meaning before style.

Style Intelligence combines foundation grammar, optional contemporary overlay, execution language, attention profile, typography profile, lighting affinity and format resilience.

It returns:

- `SAFE_STRONG`;
- `CURRENT_DIFFERENTIATED`;
- `CONTROLLED_WILDCARD`.

Currentness is capped at 5% and cannot override category fit, truth, attention, typography, lighting or format resilience.

Lighting follows:

`IDEA → PRESENTATION → EMOTION → VISUAL CHARACTER → STYLE STRATEGY → PRIMARY AOI → LIGHTING INTENT`.

Real UI may make scene lighting `NOT_APPLICABLE`.

## Google technical preflight != Google policy preflight

Technical validation checks dimensions, type, bytes and static state. It does not prove policy compliance.

The separate Google Ads policy layer covers pre-render risk and final exact-artifact + destination evidence, including misleading design, image/text quality, material claims/qualifiers, advertiser identity, landing-page relevance/offer availability, trademark/affiliation context and restricted vertical/certification/targeting state where applicable.

`GOOGLE_READY_PRECHECK_PASS` still carries:

`google_upload_approval_guaranteed = false`.

## Verified deterministic milestone

**215 tests — OK.**

GitHub Actions run `34327142240` / #583 completed **SUCCESS** on the canonical REAL-07 flow after the semantic-invariant test correction.

The deterministic suite checks commercial-job integrity, first-round exploration semantics, complete-banner artifact roles, raw-hero rejection, exact raster dimensions, two fresh exact-artifact pre-show reviews, user-only visual approval/fidelity, Style Intelligence, lighting, deterministic production, Google technical validation and Google policy gates.

This does **not** prove campaign performance, independent artistic excellence or actual Google approval.

## Current MITGROUP acceptance state

The valid business state is:

- `COMMERCIAL_JOB = NEW_LICENSE_PURCHASE`;
- cloud + box license scope;
- CTA `Выбрать редакцию`;
- `PROMOTIONAL_OFFER = NONE`;
- renewal and implementation excluded from the current run.

Old implementation/A2 material is stale/rejected.

The latest generic blue/metal image-generation output is also rejected as a banner concept. It may exist only as failed raw component evidence; no user-selected current visual system exists.

The next real acceptance must resume at complete-banner visual exploration, not repeat business intake unless a business fact changed.

## Merge rule

Do not merge because deterministic CI is green.

Merge only after real Work acceptance of the corrected visual flow, real-pack policy acceptance, independent rigor (or explicit degraded-rigor acceptance), and explicit user approval.

See `docs/v0.2-release-gate.md` and `docs/ROADMAP.md`.

## Future

v0.3: GIF/video/HTML5 + Remotion/Content Factory + motion-specific Google technical/policy validation after static v0.2 is proven.
