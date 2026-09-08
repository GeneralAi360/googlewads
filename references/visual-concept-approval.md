# Visual Concept Approval Contract

## Purpose

The user approves a **visual concept**, not a text-only art-direction description.

Written strategy, Style Intelligence, attention, typography, lighting and art-direction documents are internal preproduction contracts that prepare the visual concept. They may be reviewed internally, but they do not substitute for the user's visual approval.

A second principle is equally important:

> Missing production-grade assets must not leave the user with nothing visual to judge.

Production asset readiness and user concept visibility are separate concerns.

## Canonical user-facing flow

`QUESTIONS / INTAKE -> STRATEGY -> RENDERED VISUAL CONCEPT -> USER APPROVAL -> PRODUCTION ASSET COMPLETION IF NEEDED -> FULL PRODUCTION`

Expanded:

1. collect only the questions needed to create the campaign correctly;
2. resolve business facts, scope, research/category context, idea, visual character, style strategy, attention, typography, policy risk and lighting intent;
3. internally freeze a sufficiently detailed art-direction plan;
4. determine which production assets are required;
5. render one user-facing visual concept, normally 300x250 unless another format is more representative;
6. if production assets are available, render with them;
7. if production assets are missing, render a **concept preview** using only explicitly declared non-production surrogates/asset slots that do not fabricate the product or brand;
8. show the rendered concept plus a short plain-language concept summary;
9. wait for the user's explicit `APPROVE / REVISE / REJECT`;
10. after `APPROVE`, continue automatically as far as possible; request missing production assets only when they are actually needed;
11. after real assets replace concept-only surrogates, verify fidelity to the user-approved visual system;
12. if the real-asset substitution causes material visual drift, show the changed concept again; otherwise no second user approval is required;
13. only a valid exact-artifact approval path or approved-system-plus-fidelity path may unlock campaign-system freeze and full-pack production.

## The user must see both the concept and the design

Every concept presentation must contain two user-facing outputs:

1. **Rendered visual concept** — the primary approval artifact.
2. **Short concept card** — a concise explanation of:
   - core idea;
   - primary AOI;
   - scan path;
   - selected style strategy;
   - typography character;
   - lighting behavior;
   - how the system will adapt across formats;
   - which visible elements are temporary concept-only surrogates, if any.

A long internal JSON dump does not count as presenting the concept.
A text-only art direction does not count as presenting the concept.
A `NEEDS_ASSET` list by itself does not count as presenting the concept.

## Two visual-concept approval scopes

### 1. `EXACT_PRODUCTION_ARTIFACT`

Use when all required production assets are ready and the rendered concept is already production-grade.

The exact image bytes are the approval target.

`USER APPROVE` can proceed through the exact-artifact scale-out gate.

### 2. `VISUAL_SYSTEM_WITH_ASSET_SLOTS`

Use when the user should be able to judge the design now, but one or more production assets are not yet ready.

The rendered concept must still show the actual design system:
- real copy;
- real CTA wording;
- composition/grid;
- headline hierarchy;
- typography character;
- color/background system;
- CTA treatment;
- whitespace/density;
- service rails/graphic devices;
- UI/logo slot size and position;
- attention path;
- lighting behavior;
- category/premium character.

The user is approving this visible design system, not claiming that temporary asset bytes are production assets.

Status after approval:

`VISUAL_CONCEPT_APPROVED_ASSET_PENDING`

This permits production asset completion, but does **not** by itself permit final ad delivery or scale-out.

## Allowed concept-only asset modes

A concept preview may use only declared modes from `schemas/visual-concept-preview.schema.json`.

### `LOW_RES_AUTHENTIC_SURROGATE`

Example: a real MITGROUP logo that is too small for final delivery but sufficient to communicate approximate brand placement in the concept.

It must remain `production_ready=false`.

### `REFERENCE_ONLY_SURROGATE`

Example: an attributable official/public product screenshot used only to demonstrate the intended product aperture/crop before the advertiser supplies an approved production source.

It must not be represented as a cleared final ad asset.

### `STRUCTURAL_PLACEHOLDER`

A neutral design block that communicates **geometry and hierarchy only**.

For a real-UI concept it may show the reserved UI aperture, crop ratio, border treatment and relationship to copy, but it must not invent a fake Bitrix24 dashboard or fake controls.

### `TEXT_BRAND_PLACEHOLDER`

When the authentic logo is unavailable, the canonical approved display name may be typeset neutrally to show the brand-anchor location. It must not imitate or fabricate the missing logo artwork.

## Forbidden even in concept preview

Never use:
- generated fake Bitrix24 UI;
- invented product screens presented as authentic;
- generated/fabricated logo artwork;
- invented trademark/partner badges;
- fabricated client data;
- unsupported claims;
- a surrogate preview as a final Google Ads file.

Any preview containing non-production surrogates must be:
- `approval_scope = VISUAL_SYSTEM_WITH_ASSET_SLOTS`;
- `production_asset_readiness = NEEDS_ASSET`;
- `not_for_delivery = true`.

Validate with:

```bash
python scripts/validate_visual_concept_preview.py \
  --preview run/design/visual-concept-preview.json \
  --out run/design/visual-concept-preview-gate.json
```

Required user-facing state:

`VISUAL_CONCEPT_AWAITING_USER_APPROVAL`

## User decisions

Use `schemas/visual-concept-decision.schema.json`.

### APPROVE — exact production artifact

For `approval_scope = EXACT_PRODUCTION_ARTIFACT`:

- exact artifact path/SHA are recorded;
- `decided_by = USER`;
- full production may unlock after the ordinary representative quality/scale-out gates pass.

### APPROVE — visual system with asset slots

For `approval_scope = VISUAL_SYSTEM_WITH_ASSET_SLOTS`:

- the user-approved preview path/SHA are recorded;
- status becomes `VISUAL_CONCEPT_APPROVED_ASSET_PENDING`;
- full production remains blocked;
- the skill should request/resolve only the still-missing production assets;
- when real assets arrive, it automatically materializes a production representative using the approved design system;
- an `ART_DIRECTOR_REVIEWER` compares the production representative to the exact user-approved preview;
- if fidelity is `PASS`, the user-rooted system-fidelity scale-out gate may continue without a second approval;
- if fidelity is `MATERIAL_DRIFT`, the changed visual must be shown to the user again.

The reviewer cannot approve a new direction. The reviewer may only attest that asset substitution preserved the direction already approved by the user.

For the no-second-approval path run:

```bash
python scripts/validate_visual_system_scaleout.py \
  --visual-decision run/design/visual-concept-decision.json \
  --representative-approval run/design/representative-design-approval.json \
  --fidelity-report run/design/visual-system-fidelity-report.json \
  --asset-readiness run/design/representative-asset-readiness.json \
  --out run/design/visual-system-scaleout-gate.json
```

Required result:

`VISUAL_CONCEPT_APPROVED_VIA_SYSTEM_FIDELITY`

### REVISE

- do not scale out;
- record the requested changes;
- create a new rendered visual concept version;
- show it again for explicit user approval.

### REJECT

- do not scale out;
- return to the smallest upstream layer responsible for the problem;
- create a materially new visual concept rather than multiplying the rejected system.

## One concept or several

Default behavior: create **one strongest rendered visual concept** when research and user context provide a clear direction.

Create 2–3 rendered alternatives only when the direction is genuinely unresolved or the user explicitly requests alternatives.

Do not create three near-identical previews merely to satisfy a count.

## Full-production boundary

Permitted paths are:

`PRODUCTION-READY VISUAL -> USER APPROVE -> EXACT SCALEOUT GATE -> FULL PRODUCTION`

or:

`CONCEPT PREVIEW WITH ASSET SLOTS -> USER APPROVE -> REAL ASSETS -> PRODUCTION REPRESENTATIVE -> FIDELITY PASS -> FULL PRODUCTION`

Not:

`NEEDS_ASSET -> SHOW NOTHING -> WAIT`

and not:

`TEXT DESCRIPTION -> ASSUME APPROVAL -> FULL PACK`.

## Completion semantics

Use explicit states:
- `VISUAL_CONCEPT_NOT_RENDERED`;
- `VISUAL_CONCEPT_AWAITING_USER_APPROVAL`;
- `VISUAL_CONCEPT_REVISE_REQUESTED`;
- `VISUAL_CONCEPT_REJECTED`;
- `VISUAL_CONCEPT_APPROVED`;
- `VISUAL_CONCEPT_APPROVED_ASSET_PENDING`;
- `VISUAL_CONCEPT_APPROVED_VIA_SYSTEM_FIDELITY`;
- `PRODUCTION_ASSETS_PENDING`;
- `MATERIAL_VISUAL_DRIFT_REQUIRES_REAPPROVAL`;
- `FULL_PRODUCTION_BLOCKED_BY_VISUAL_APPROVAL`.

`NEEDS_ASSET` is a production-readiness state. It is no longer a valid reason to hide the concept from the user when a safe rendered concept preview can be produced.
