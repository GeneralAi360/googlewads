# Commercial Job Lock, Graphic Banner Brief, and Visual Concept Exploration

## Purpose

A banner can be visually polished and still be wrong if it advertises the wrong commercial action or if the visual problem was never clearly defined before rendering.

The controller must distinguish four separate things:

1. **Product / service identity** — what the business sells or supports.
2. **Commercial job** — what this specific campaign is asking the market to do now.
3. **Campaign objective** — what outcome the advertiser measures, such as a lead or sale.
4. **Graphic Banner Brief** — the user-approved advertising/design problem and visual boundaries that constrain later A/B/C exploration.

These are not interchangeable.

For example, all of the following may concern Bitrix24 but are materially different commercial jobs:

- new license purchase;
- license renewal;
- purchase or renewal in one campaign;
- implementation service;
- consultation.

A design for `IMPLEMENTATION_SERVICE` must not silently survive when the user corrects the task to `NEW_LICENSE_PURCHASE` or `PURCHASE_OR_RENEWAL`.

Likewise, a correct commercial job must not jump directly into abstract geometry or hero generation merely because the design problem is still under-specified.

## Canonical dependency

`USER BUSINESS FACTS`
`-> COMMERCIAL JOB LOCK`
`-> RESEARCH / CATEGORY EVIDENCE`
`-> GRAPHIC BANNER BRIEF`
`-> USER APPROVES / REVISES BRIEF`
`-> IDEA / STYLE / ART DIRECTION`
`-> VISUAL CONCEPT EXPLORATION`
`-> USER SELECTION / VISUAL APPROVAL`
`-> PRODUCTION`.

The commercial job is resolved before research/meaning/style. The Graphic Banner Brief is created after relevant research/category evidence and **before first-round visual rendering**.

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

- commercial job: `NEW_LICENSE_PURCHASE`;
- campaign objective: `LEAD_GENERATION`;
- CTA: `Выбрать редакцию`.

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

- Graphic Banner Brief and its user decision;
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

## Mandatory Graphic Banner Brief gate

Load `references/graphic-banner-brief.md`.

After commercial-job resolution and relevant research/category work, create `graphic-banner-brief.json` matching `schemas/graphic-banner-brief.schema.json`.

The brief must make the advertising problem explicit before visual form is explored. It freezes at least:

- exact commercial core / CTA / brand;
- audience decision context;
- first-glance takeaway;
- primary / secondary / forbidden message semantics;
- desired user reaction;
- banner role and persuasion/trust mechanism;
- visual-semantic job;
- composition hierarchy / scan roles / CTA integration / brand anchor;
- typography boundaries;
- color / lighting boundaries;
- graphic-style boundaries;
- hard anti-failure rules;
- first-round concept-generation rules;
- presentation-ready quality bar.

Validate:

```bash
python scripts/validate_graphic_banner_brief.py \
  --commercial-job run/commercial/campaign-commercial-job.json \
  --brief run/design/graphic-banner-brief.json \
  --out run/design/graphic-banner-brief-gate.json
```

A valid brief returns:

`GRAPHIC_BANNER_BRIEF_READY_FOR_USER_APPROVAL`

with:

- `render_allowed=false`;
- `full_production_allowed=false`.

Do not render A/B/C at this point.

### User-facing brief presentation

Show a concise human-readable brief first, then optionally the JSON artifact. The user should be able to judge whether the advertising/design problem is correct without imagining a visual.

Ask only:

- `APPROVE BRIEF`;
- `REVISE BRIEF`.

### Exact user decision

Create `graphic-banner-brief-decision.json` matching `schemas/graphic-banner-brief-decision.schema.json` and validate:

```bash
python scripts/validate_graphic_banner_brief_decision.py \
  --brief run/design/graphic-banner-brief.json \
  --decision run/design/graphic-banner-brief-decision.json \
  --out run/design/graphic-banner-brief-decision-gate.json
```

Only exact current brief bytes plus:

- `decided_by = USER`;
- `decision = APPROVE`;

may produce:

`GRAPHIC_BANNER_BRIEF_APPROVED`

and unlock first-round visual exploration.

`REVISE` keeps rendering blocked and requires new brief bytes/SHA followed by another user decision.

No Style Intelligence recommendation, controller preference, art director or designer can approve this gate on behalf of the user.

### Brief approval is not visual approval

`APPROVE BRIEF` means:

> The advertising problem, hierarchy, design boundaries and exploration rules are correct.

It does **not** mean:

> I approve a rendered design.

Later visual selection/approval remains mandatory.

## Graphic-brief anti-failure floor

At minimum hard reject:

- abstract geometry without commercial meaning;
- decorative form substituted for advertising idea;
- raw generated image used as a visual concept;
- presentation-slide composition;
- generic 3D object without task-specific meaning;
- missing brand anchor;
- commercial job not understandable at first glance;
- visuals that require a long rationale to become meaningful;
- visual novelty replacing clarity.

Hero generation is optional and must not be the default first step for concept exploration.

A/B/C must differ first by **advertising logic**, not merely by visual form.

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

Visual exploration is allowed only after `GRAPHIC_BANNER_BRIEF_APPROVED` unless an explicitly approved existing campaign design system makes a new brief unnecessary for a continuation task.

Unless the visual direction is explicitly locked by the user, the first user-facing visual round defaults to:

`EXPLORE_3`

Create exactly three **materially different rendered concepts** in the same representative size and with the same frozen commercial job/message/Graphic Banner Brief constraints.

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

Before those visual differences, the controller should also state the distinct **advertising logic** of A/B/C, such as product/evidence-led, decision/choice-led, typography/commercial-message-led, comparison-led, proof-led, or another task-specific mechanism.

Changing only background color, button color, illustration style, crop, or abstract-object shape is insufficient.

## Pre-show concept quality gate

Before a visual concept is shown to the user, the exact complete `BANNER_COMPOSITE` follows the current pre-show review contract under `references/concept-composite-and-pre-show-quality.md`.

A raw hero, visual asset, prompt output or written rationale cannot receive presentation-ready status.

The user must not be the first basic QA pass for obviously weak work.

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

The selected concept then follows the visual approval path:

`SELECT -> REVISE IF NEEDED -> APPROVE -> PRODUCTION ASSETS/FIDELITY -> SCALE-OUT`.

Do not continue producing all three directions unless the user explicitly wants multiple final concepts.

## REAL-06 / REAL-08 rules

REAL-06 established that exact commercial-job fidelity and genuine visual choice must precede scale-out.

REAL-08 established that a correct commercial job and even complete-banner validation are still insufficient if the skill starts drawing before the **advertising/design brief itself** is approved. Repeated abstract blue glass/metal directions exposed the missing user-approved Graphic Banner Brief boundary.

Both are permanent regressions.
