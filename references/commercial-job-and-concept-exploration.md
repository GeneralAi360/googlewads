# Commercial Job Lock and Visual Concept Exploration

## Purpose

A banner can be visually polished and still be wrong if it advertises the wrong commercial action.

The controller must distinguish three separate things:

1. **Product / service identity** — what the business sells or supports.
2. **Commercial job** — what this specific campaign is asking the market to do now.
3. **Campaign objective** — what outcome the advertiser measures, such as a lead or sale.

These are not interchangeable.

For example, all of the following may concern Bitrix24 but are materially different commercial jobs:

- new license purchase;
- license renewal;
- purchase or renewal in one campaign;
- implementation service;
- consultation.

A design for `IMPLEMENTATION_SERVICE` must not silently survive when the user corrects the task to `PURCHASE_OR_RENEWAL`.

## Canonical dependency

`USER BUSINESS FACTS -> COMMERCIAL JOB LOCK -> RESEARCH / STRATEGY -> VISUAL CONCEPT EXPLORATION -> USER SELECTION -> PRODUCTION`

The commercial job is resolved **before** idea architecture and visual concept rendering.

## Commercial job types

Current normalized vocabulary:

- `NEW_LICENSE_PURCHASE`;
- `LICENSE_RENEWAL`;
- `PURCHASE_OR_RENEWAL`;
- `IMPLEMENTATION_SERVICE`;
- `CONSULTATION`;
- `OTHER` with an explicit note.

This vocabulary describes the transaction/service job. It does not replace CTA wording.

Example:

- commercial job: `PURCHASE_OR_RENEWAL`;
- campaign objective: `LEAD_GENERATION`;
- CTA: `Оставить заявку`.

The three may legitimately coexist, but they must not be collapsed into one field.

## Purchase + renewal structure

When `job_type = PURCHASE_OR_RENEWAL`, resolve whether the campaign uses:

- `COMBINED` — purchase and renewal are deliberately presented together in one message; or
- `SEPARATE_VARIANTS` — purchase and renewal become separate commercial variants.

Do not choose this silently when it materially changes copy, visual hierarchy, landing-page relevance, or output count.

## Commercial job lock

Create `campaign-commercial-job.json` matching `schemas/campaign-commercial-job.schema.json`.

Freeze:

- stable `commercial_job_id`;
- exact product/service;
- normalized `job_type`;
- purchase/renewal structure when applicable;
- plain-language target transaction;
- allowed message scope;
- excluded commercial jobs;
- source basis;
- `change_requires_controller_reapproval=true`.

Validate with:

```bash
python scripts/validate_campaign_commercial_job.py \
  --lock run/commercial/campaign-commercial-job.json \
  --out run/commercial/campaign-commercial-job-gate.json
```

If a prior lock exists, compare it:

```bash
python scripts/validate_campaign_commercial_job.py \
  --lock run/commercial/campaign-commercial-job.json \
  --previous-lock run/commercial/previous-campaign-commercial-job.json \
  --out run/commercial/campaign-commercial-job-gate.json
```

A material job change returns `COMMERCIAL_JOB_CHANGED` and requires downstream strategy/concept invalidation. This is not an error; it is a controlled reset.

## Downstream invalidation

A material commercial-job change invalidates stale artifacts whose meaning depended on the old job, including as applicable:

- idea architecture;
- commercial message hierarchy;
- style-strategy context/recommendation;
- attention plan;
- typography hierarchy;
- lighting intent when AOI/meaning changes;
- written art direction;
- rendered visual concept previews;
- visual user decisions;
- campaign design system;
- creative contracts.

Do not preserve an implementation-service concept merely by changing one line of copy to purchase/renewal.

## Final concept count is not exploration count

`deliverables.concept_count` answers:

> How many creative concepts will ultimately be produced/scaled in the final campaign?

It does **not** answer:

> How many alternative visual directions should the user see before choosing the design system?

These are separate quantities.

A campaign may have:

- final `concept_count = 1`;
- first-round `visual_exploration_count = 3`.

The user then selects one direction and only that system is scaled out.

## Default visual exploration rule

Unless the visual direction is explicitly locked by the user, the first user-facing visual round defaults to:

`EXPLORE_3`

Create exactly three **materially different rendered concepts** in the same representative size and with the same frozen commercial job/message constraints.

An internal Style Intelligence recommendation, controller recommendation, previous Work suggestion, category-map recommendation, or art-director preference is **not** a user lock.

Only explicit user evidence such as:

- “use this exact direction”;
- approval of a prior rendered concept;
- an approved campaign/design system supplied by the user;

may justify:

`SINGLE_USER_LOCKED`.

The lock provenance must be recorded as `USER_LOCKED`.

## Three concepts must be genuinely different

For `EXPLORE_3`, the three concepts must not be palette swaps or tiny rearrangements.

Each concept records six design axes:

1. `hero_logic`;
2. `composition_system`;
3. `attention_profile`;
4. `typography_profile`;
5. `graphic_device`;
6. `lighting_language`.

Every pair of concepts must differ on at least **three** axes.

Examples of meaningful differences:

- product/edition selector vs renewal-continuity idea vs typographic commercial statement;
- interface proof vs license-object/product-system framing vs editorial decision architecture;
- type-led composition vs object-led composition vs split decision/comparison composition.

Changing only background color, button color, illustration style, or crop is insufficient.

## Pre-show concept quality gate

Before a visual concept is shown to the user, an `ART_DIRECTOR_REVIEWER` checks the actual rendered artifact.

Required PASS checks:

- `commercial_job_fidelity` — the visual/message actually advertise the locked transaction/service;
- `professional_category_fit` — appropriate for the category and audience;
- `ad_not_presentation_slide` — it reads as an advertisement, not a deck slide/dashboard screenshot pasted into a frame;
- `hierarchy` — clear attention winner and message order;
- `typography` — intentional, legible, crafted hierarchy;
- `cta_integration` — action belongs to the composition instead of looking appended;
- `visual_distinctiveness` — not interchangeable generic SaaS/template treatment;
- `anti_template` — no obvious layout-by-habit/generic AI slop;
- `small_format_viability` — core system can survive the requested format family.

These checks are design-quality gates, not CTR/conversion predictions.

A concept that fails should be revised internally before presentation. Do not make the user act as the first basic QA pass for obviously weak work.

## Concept-set artifact

Create `visual-concept-set.json` matching `schemas/visual-concept-set.schema.json` and validate:

```bash
python scripts/validate_visual_concept_set.py \
  --commercial-job run/commercial/campaign-commercial-job.json \
  --concept-set run/design/visual-concept-set.json \
  --out run/design/visual-concept-set-gate.json
```

For `EXPLORE_3`, required result:

`VISUAL_CONCEPT_SET_AWAITING_USER_SELECTION`

The user should receive:

- one comparison contact sheet containing all three concepts;
- each individual concept at the representative size;
- one short concept card per direction;
- a simple choice: `A / B / C`, `REVISE`, or `REJECT ALL`.

## After user selection

Once the user chooses a concept, subsequent refinement may proceed one concept at a time.

The selected concept then follows the existing visual approval path:

`SELECT -> REVISE IF NEEDED -> APPROVE -> PRODUCTION ASSETS/FIDELITY -> SCALE-OUT`.

Do not continue producing all three directions unless the user explicitly wants multiple final concepts.

## REAL-06 rule

The MITGROUP acceptance run exposed two coupled failures:

1. a stale `IMPLEMENTATION_SERVICE` assumption survived even though the actual campaign was for Bitrix24 license purchase/renewal;
2. one internally recommended A2 direction was treated as if the user had already locked it, so no genuine visual choice was presented.

Both are permanent regressions.
