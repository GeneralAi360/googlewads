# Visual Concept Approval Contract

## Purpose

The user approves **visible advertising design**, not a text-only art-direction description and not a raw hero-generation output.

Written strategy, Style Intelligence, attention, typography, lighting and art-direction documents are internal preproduction contracts. Generated imagery, UI crops, photos, illustrations, textures and 3D objects are component assets. None of them substitute for user judgment of the complete banner.

Three permanent rules now govern visual approval:

1. missing production-grade assets must not leave the user with nothing visual to judge;
2. an internal recommendation must not be treated as if the user already selected/locked a visual direction;
3. a `HERO_ASSET_CANDIDATE` must never be shown or reviewed as if it were the final `BANNER_COMPOSITE`.

Load before first-round rendering:

- `references/commercial-job-and-concept-exploration.md`;
- `references/concept-composite-and-pre-show-quality.md`.

## Canonical user-facing flow

When the direction is not explicitly user-locked:

`QUESTIONS / INTAKE -> COMMERCIAL JOB LOCK -> STRATEGY -> 3 COMPLETE BANNER COMPOSITES -> TWO FRESH PRE-SHOW REVIEWS EACH -> USER SELECTION -> REVISE/APPROVE -> PRODUCTION ASSET COMPLETION IF NEEDED -> FULL PRODUCTION`

When the user has explicitly locked a direction:

`QUESTIONS / INTAKE -> COMMERCIAL JOB LOCK -> STRATEGY -> 1 COMPLETE LOCKED-DIRECTION BANNER COMPOSITE -> PRE-SHOW REVIEW -> USER APPROVAL -> PRODUCTION ASSET COMPLETION IF NEEDED -> FULL PRODUCTION`

The user-facing exploration count is separate from `deliverables.concept_count`. A campaign may ultimately produce one concept while still showing three alternatives in the first visual decision round.

## What counts as a user lock

`SINGLE_USER_LOCKED` is allowed only when there is explicit user evidence.

Valid examples:
- the user explicitly says to use a specific direction;
- the user already approved an exact rendered concept;
- the user supplies an approved campaign design system and asks to continue it.

The following are **not** user locks:
- Style Intelligence recommendation;
- controller recommendation;
- research/category recommendation;
- previous Work recommendation;
- `ART_DIRECTOR_REVIEWER` preference;
- a written A/B/C recommendation never visually approved by the user.

Those use `direction_lock_source = INTERNAL_RECOMMENDATION` or `NONE` and still require `EXPLORE_3` on the first visual round.

## First-round EXPLORE_3

Unless `USER_LOCKED` evidence exists, render exactly three materially different concepts in the same representative size, normally 300x250.

Every concept must share the same frozen commercial-job/message facts, but must differ in visual grammar.

Pairwise distinction is evaluated across:
- hero logic;
- composition system;
- attention profile;
- typography profile;
- graphic device;
- lighting language.

Every pair must differ on at least three axes.

Do not satisfy the requirement with:
- palette swaps;
- the same copy-left/image-right template with different images;
- minor crop changes;
- different button colors;
- three variants of the same generic SaaS card.

## A hero asset is not a concept

The user-facing artifact must be:

`artifact_role = BANNER_COMPOSITE`

and:

`render_stage = USER_FACING_CONCEPT_COMPOSITE`.

A generated image may first exist as `HERO_ASSET_CANDIDATE`. Before it can contribute to a visual concept, it must be composed with the campaign system.

A valid banner composite must already include the visible roles needed to judge the advertisement:
- primary message;
- commercial-job cue;
- CTA;
- brand anchor;
- hero/visual device where applicable;
- typography hierarchy;
- color/background system;
- whitespace/density;
- relevant temporary/production asset slots.

The `composition_contract` in `visual-concept-preview.json` records these mandatory visible elements and all raw generated asset paths.

`raw_generated_asset_is_final_artifact` must always be `false`.

The preview validator decodes the actual raster and verifies that its real PNG/JPEG dimensions equal the declared representative dimensions. A raw generated asset path reused as the concept artifact is rejected.

## Generated imagery behavior

Image generation is optional, not mandatory.

If it is used:

`GENERATE COMPONENT -> SELECT -> REFINE IF NEEDED -> COMPOSE BANNER -> ADD DETERMINISTIC TYPE/CTA/BRAND -> REVIEW COMPLETE COMPOSITE`.

Never:

`GENERATE IMAGE -> CALL IT CONCEPT -> REVIEW PASS -> SHOW USER`.

Reject/abandon a generated hero when:
- it is generic decoration with no defensible relation to the commercial job;
- the same object could be dropped into unrelated SaaS advertising unchanged;
- the copy must explain what the visual supposedly means;
- repeated generation is stalling progress without producing a semantically useful asset.

When generation is low-value, return to type-led, product-led, editorial, structural or another appropriate visual strategy rather than waiting indefinitely.

## Two exact-artifact pre-show reviews

Create and validate `visual-concept-set.json` with `scripts/validate_visual_concept_set.py`.

Every first-round concept requires exactly **two fresh review reports** matching `schemas/pre-show-visual-review.schema.json`.

Both reviewers inspect the exact `BANNER_COMPOSITE` bytes the user would see.

Required independence metadata:
- distinct `reviewer_context_id` values;
- `fresh_context = true`;
- `prior_review_verdict_visible = false`.

A reviewer may return `PRESENTATION_READY_DESIGN` only when all required checks PASS with visible-artifact evidence:
- commercial-job fidelity;
- complete banner composite;
- primary-message visibility;
- CTA visibility and integration;
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

A bare list of PASS booleans is not enough. Each check must explain what was actually visible in the artifact.

If either reviewer returns `REVISE_BEFORE_SHOW`, revise internally and repeat the review on the new exact bytes.

The user must not be the first basic design QA pass.

This remains a design-quality gate, not performance prediction.

## User-facing presentation

For EXPLORE_3 show:

1. one comparison/contact sheet containing A, B and C;
2. each individual **complete banner composite**;
3. one short concept card per concept;
4. a simple decision request such as:
   - `SELECT A`;
   - `SELECT B`;
   - `SELECT C`;
   - `REVISE`;
   - `REJECT ALL`.

Do not lead with internal JSON dumps, raw image-generation galleries or hero candidate sheets.

Each concept card explains:
- commercial angle;
- core idea;
- primary AOI;
- scan path;
- style strategy;
- typography character;
- lighting behavior;
- format adaptation;
- any visible temporary concept-only assets.

## After selection

Once the user selects one of the three systems, subsequent work may continue one concept at a time.

Selection is not necessarily final approval. The selected concept can be revised until the user gives `APPROVE`.

Do not continue scaling all three unless the user explicitly requests several final campaign concepts.

## Production asset readiness versus concept visibility

Production asset readiness and visual concept visibility are separate concerns.

A `NEEDS_ASSET` state must not by itself prevent a safe rendered concept preview.

Two approval scopes exist.

### `EXACT_PRODUCTION_ARTIFACT`

Use when all required production assets are ready and the concept is already a production-ready representative.

The user approves the exact rendered bytes.

### `VISUAL_SYSTEM_WITH_ASSET_SLOTS`

Use when the visible design can be judged now but one or more production assets are not yet ready.

Allowed concept-only asset modes:
- `LOW_RES_AUTHENTIC_SURROGATE`;
- `REFERENCE_ONLY_SURROGATE`;
- `STRUCTURAL_PLACEHOLDER`;
- `TEXT_BRAND_PLACEHOLDER`.

Never use:
- generated fake Bitrix24 UI;
- invented product screens presented as authentic;
- generated/fabricated logos;
- invented trademark/partner badges;
- fabricated client data;
- unsupported claims.

A surrogate preview must remain:
- `approval_scope = VISUAL_SYSTEM_WITH_ASSET_SLOTS`;
- `production_asset_readiness = NEEDS_ASSET`;
- `not_for_delivery = true`.

Validate each complete preview with:

```bash
python scripts/validate_visual_concept_preview.py \
  --preview run/design/{visual_concept_id}.visual-concept-preview.json \
  --out run/design/{visual_concept_id}.visual-concept-preview-gate.json
```

Each preview is bound to the current `commercial_job_id` so a stale implementation concept cannot survive a switch to license purchase/renewal.

## User decisions on the selected concept

Use `schemas/visual-concept-decision.schema.json`.

### APPROVE — exact production artifact

For `EXACT_PRODUCTION_ARTIFACT`:
- exact path/SHA are recorded;
- `decided_by = USER`;
- ordinary representative/scale-out gates may continue.

### APPROVE — visual system with asset slots

For `VISUAL_SYSTEM_WITH_ASSET_SLOTS`:
- status becomes `VISUAL_CONCEPT_APPROVED_ASSET_PENDING`;
- full production remains blocked;
- only the still-missing production assets are requested;
- when real assets arrive, create a production representative from the approved visual system;
- `ART_DIRECTOR_REVIEWER` checks exact approved-preview -> production fidelity;
- fidelity `PASS` may continue without a redundant second user approval;
- `MATERIAL_DRIFT` must be shown to the user again.

The reviewer cannot approve a new direction. The reviewer may only attest that replacing declared temporary slots preserved the user-approved system.

### REVISE

- keep scale-out blocked;
- record feedback;
- render the revised selected concept;
- show the actual visual again.

### REJECT

- keep scale-out blocked;
- return to the smallest responsible upstream layer;
- if all first-round concepts are rejected, produce a new materially different exploration set rather than cosmetic remixes.

## Full-production boundary

Permitted paths:

`3 COMPLETE BANNER COMPOSITES -> TWO REVIEWS EACH -> USER SELECTS -> USER APPROVES PRODUCTION-READY VISUAL -> EXACT SCALEOUT GATE -> FULL PRODUCTION`

or:

`3 COMPLETE BANNER COMPOSITES -> TWO REVIEWS EACH -> USER SELECTS -> USER APPROVES VISUAL SYSTEM WITH ASSET SLOTS -> REAL ASSETS -> PRODUCTION REPRESENTATIVE -> FIDELITY PASS -> FULL PRODUCTION`.

A `SINGLE_USER_LOCKED` path replaces the initial three only when explicit user lock evidence exists.

Forbidden shortcuts:

`INTERNAL RECOMMENDATION -> ASSUME USER LOCK -> ONE CONCEPT`

`NEEDS_ASSET -> SHOW NOTHING -> WAIT`

`TEXT DESCRIPTION -> ASSUME APPROVAL -> FULL PACK`

`RAW HERO -> PRESENTATION_READY_DESIGN -> SHOW USER`.

## Completion semantics

Use explicit states such as:
- `HERO_ASSET_CANDIDATE`;
- `VISUAL_CONCEPT_SET_AWAITING_USER_SELECTION`;
- `VISUAL_CONCEPT_AWAITING_USER_APPROVAL`;
- `VISUAL_CONCEPT_REVISE_REQUESTED`;
- `VISUAL_CONCEPT_REJECTED`;
- `VISUAL_CONCEPT_APPROVED`;
- `VISUAL_CONCEPT_APPROVED_ASSET_PENDING`;
- `VISUAL_CONCEPT_APPROVED_VIA_SYSTEM_FIDELITY`;
- `PRODUCTION_ASSETS_PENDING`;
- `MATERIAL_VISUAL_DRIFT_REQUIRES_REAPPROVAL`;
- `FULL_PRODUCTION_BLOCKED_BY_VISUAL_APPROVAL`.

`NEEDS_ASSET` is a production-readiness state, not a reason to hide the concept. An internal recommendation is decision support, not proof that the user chose the direction. A raw generated image is a component asset, not the banner the user is asked to approve.
