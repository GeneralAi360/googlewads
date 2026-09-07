# Visual Concept Approval Contract

## Purpose

The user approves a **visual concept**, not a text-only art-direction description.

Written strategy, Style Intelligence, attention, typography, lighting and art-direction documents are internal preproduction contracts that prepare the visual concept. They may be reviewed internally, but they do not substitute for the user's visual approval.

## Canonical user-facing flow

`QUESTIONS / INTAKE -> STRATEGY -> VISUAL CONCEPT -> USER APPROVAL -> FULL PRODUCTION`

Expanded:

1. collect only the questions needed to create the campaign correctly;
2. resolve business facts, scope, research/category context, idea, visual character, style strategy, attention, typography, policy risk and lighting intent;
3. internally freeze a sufficiently detailed art-direction plan;
4. resolve required production assets;
5. create one real high-fidelity representative visual concept, normally 300x250 unless another format is more representative;
6. show the rendered concept to the user with a short rationale;
7. wait for the user's explicit decision;
8. validate the exact user decision against the exact rendered bytes;
9. only `APPROVE` authorizes campaign-design-system freeze and full-pack production.

## The approval artifact is visual

The primary approval artifact must be an actual rendered banner image bound by SHA-256.

A text description such as "light field, UI on the right, CTA below" is not sufficient user approval evidence.

The visual concept should already demonstrate the intended:
- composition and grid;
- primary AOI and scan path;
- hero/image treatment;
- typography and hierarchy;
- color system;
- lighting behavior;
- CTA treatment;
- brand treatment;
- whitespace/density;
- premium/category character;
- anti-generic-AI quality;
- policy-safe visual behavior.

A short written rationale may accompany the image, but it supports the visual artifact and never replaces it.

## User decisions

Use `schemas/visual-concept-decision.schema.json` for the exact-artifact user decision.

### APPROVE

The exact visual concept is accepted by the user.

Requirements:
- exact artifact path and SHA are recorded;
- `decided_by = USER`;
- representative approval also has `approved_by = USER`;
- representative quality checks pass;
- the campaign design system may now be frozen from this approved visual grammar;
- full-pack scale-out may begin only after all remaining production gates pass.

Before scale-out run:

```bash
python scripts/validate_visual_concept_approval.py \
  --representative-approval run/design/representative-design-approval.json \
  --visual-decision run/design/visual-concept-decision.json \
  --out run/design/visual-concept-scaleout-gate.json
```

Required result:

`VISUAL_CONCEPT_APPROVED`

with:
- `campaign_design_system_freeze_allowed=true`;
- `full_production_allowed=true`.

### REVISE

The user accepts the general direction but requests changes.

Requirements:
- do not scale out;
- record the requested changes;
- create a new version of the representative visual concept;
- previous approval, if any, is invalid for the changed bytes;
- show the revised visual again for explicit user approval.

Use `scripts/validate_visual_concept_decision.py` to materialize the state `VISUAL_CONCEPT_REVISE_REQUESTED`.

### REJECT

The user rejects the visual direction.

Requirements:
- do not scale out;
- return to the smallest upstream layer responsible for the problem: art direction, style strategy, visual character, idea architecture, offer/brand, or assets;
- do not multiply variants from the rejected visual system.

Use `scripts/validate_visual_concept_decision.py` to materialize the state `VISUAL_CONCEPT_REJECTED`.

## One concept or several

Default behavior: create **one strongest visual concept** when research and user context provide a clear direction.

Create 2–3 rendered concept alternatives only when the visual direction is genuinely unresolved or the user explicitly requests alternatives.

Do not create three near-identical previews merely to satisfy a number. Alternatives must differ materially in visual grammar, hero logic, composition, type, attention, image treatment and/or lighting.

## Asset boundary

`NEEDS_ASSET` blocks visual-concept rendering when the chosen concept requires a missing authentic asset. It does not block upstream strategic reasoning.

If the concept requires real UI/logo/product evidence and generated substitution is forbidden, stop at the render boundary and request the real asset.

## Full-production boundary

Never produce the full banner pack before explicit approval of the visual representative concept.

The sequence is:

`VISUAL CONCEPT RENDERED -> USER APPROVE -> SCALEOUT GATE -> CAMPAIGN DESIGN SYSTEM -> FULL SIZE / VARIANT MATRIX`

Not:

`TEXT DESCRIPTION -> ASSUME APPROVAL -> FULL PACK`

## Completion semantics

Use explicit states:
- `VISUAL_CONCEPT_NOT_RENDERED`;
- `VISUAL_CONCEPT_BLOCKED_BY_ASSET`;
- `VISUAL_CONCEPT_AWAITING_USER_APPROVAL`;
- `VISUAL_CONCEPT_REVISE_REQUESTED`;
- `VISUAL_CONCEPT_REJECTED`;
- `VISUAL_CONCEPT_APPROVED`;
- `FULL_PRODUCTION_BLOCKED_BY_VISUAL_APPROVAL`.

Only `VISUAL_CONCEPT_APPROVED` may unlock full production.