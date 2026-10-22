# Graphic Banner Brief — user approval contract before visual rendering

## Purpose

The skill must not jump from business facts/research directly into hero generation or visual exploration.

Before any new user-facing concept is rendered, it must first convert the accepted campaign facts into a **Graphic Banner Brief** that the user can review and approve.

The brief answers:

- what exact advertising job the banner performs;
- what the viewer should understand at first glance;
- what action the banner should cause;
- what information is primary/secondary/forbidden;
- what role the product, CTA and brand play;
- what composition/type/color/lighting constraints matter;
- what visual directions are appropriate or discouraged;
- which known failure modes must be rejected before rendering;
- how the later A/B/C concept round is allowed to differ.

It is **not** a finished visual concept and it is **not** a hidden art-direction approval. It is the user-approved design problem definition that constrains later internal art direction and visual exploration.

## Canonical boundary

For a new/unresolved campaign:

`QUESTIONS / INTAKE`
`-> EXACT COMMERCIAL JOB LOCK`
`-> RESEARCH / CATEGORY EVIDENCE`
`-> GRAPHIC BANNER BRIEF`
`-> USER: APPROVE BRIEF / REVISE BRIEF`
`-> IDEA / VISUAL CHARACTER / STYLE / ATTENTION / TYPE / LIGHT`
`-> INTERNAL ART DIRECTION`
`-> EXPLORE_3 COMPLETE BANNER COMPOSITES`
`-> USER SELECTS / REVISES / APPROVES VISUAL`
`-> PRODUCTION`.

No visual concept rendering is allowed before `GRAPHIC_BANNER_BRIEF_APPROVED`, except when an existing user-approved campaign design system explicitly bypasses new-brief creation for a continuation task.

## Why this gate exists

REAL-07 showed that even after commercial-job correction and stronger visual review gates, Work could still drift into abstract blue/metal hero generation. The model was trying to solve an under-specified visual problem by inventing pseudo-premium geometry.

The Graphic Banner Brief prevents that failure by forcing explicit agreement on the advertising problem and design boundaries **before** visual exploration.

The failure pattern is:

`CORRECT COMMERCIAL JOB -> VAGUE DESIGN PROBLEM -> ABSTRACT HERO SEARCH -> GEOMETRIC/PSEUDO-PREMIUM OUTPUT -> USER REJECTS BASIC DIRECTION`.

The intended pattern is:

`CORRECT COMMERCIAL JOB -> USER-APPROVED GRAPHIC BANNER BRIEF -> DISTINCT ADVERTISING LOGICS -> COMPLETE BANNER COMPOSITES -> USER VISUAL CHOICE`.

## Required user-facing brief sections

The user-facing summary should be concise and understandable. Do not lead with JSON.

At minimum show:

1. **Campaign / commercial job** — what is being sold/asked now.
2. **Audience / decision context** — who sees the banner and what decision they are making.
3. **First-glance takeaway** — one sentence that should be understood in roughly 1–2 seconds.
4. **Primary / secondary message** — semantic hierarchy, not necessarily final copy.
5. **CTA** — exact locked action string.
6. **Desired user reaction** — what the viewer should do/think next.
7. **Banner role / persuasion mechanism** — product-led, decision-led, offer-led, typography-led, evidence-led, etc., as a constraint family rather than a final concept.
8. **Composition requirements** — hierarchy, AOI/scan roles, whitespace, CTA integration, brand anchor, small-format survival.
9. **Typography constraints** — tone, family count, readability/craft checks.
10. **Color / lighting boundaries** — purpose and forbidden decoration.
11. **What the design must not become** — concrete anti-failure list.
12. **What happens after approval** — normally three materially different complete 300x250 concepts.

Then ask only:

- `APPROVE BRIEF`;
- `REVISE BRIEF`.

## First-glance takeaway

The brief must include a single `first_glance_takeaway`.

This is not necessarily literal banner copy. It is the semantic test:

> What should the viewer understand immediately without reading a rationale?

If this cannot be stated clearly in one short sentence, the brief is not ready.

## Desired user reaction

The brief must distinguish visual admiration from commercial action.

Invalid target:

> “The viewer should see a premium technological design.”

Valid pattern:

> “The viewer should understand the offer/action and want to continue to the relevant product decision.”

Design exists to support the advertising job, not vice versa.

## Visual-semantic requirement

Every later hero/visual device must pass both tests:

### Commercial semantic test

Does the visual materially support the exact commercial job, product decision, proof, or action?

### Generic substitution test

If the product/brand copy were replaced with an unrelated SaaS, bank, hosting company, crypto platform, or generic B2B service, would the visual still work almost unchanged?

If yes, the visual is likely too generic and should be revised or rejected unless there is a strong documented reason.

A beautiful abstract form is not a valid advertising idea merely because a later explanation assigns it meaning.

## Anti-failure rules

The canonical brief must explicitly classify at least these cases:

- abstract geometry without commercial meaning -> `REJECT`;
- decorative form substituted for advertising idea -> `REJECT`;
- raw generated image used as concept -> `REJECT`;
- presentation-slide composition -> `REJECT`;
- generic SaaS template -> `REJECT` or explicit review-required path;
- generic 3D object -> `REJECT`;
- CTA appended after layout -> `REJECT` or explicit review-required path;
- missing brand anchor -> `REJECT`;
- commercial job not understandable at first glance -> `REJECT`;
- visual requires long rationale to become meaningful -> `REJECT`;
- novelty replaces clarity -> `REJECT`.

These are production-quality controls, not performance predictions.

## Concept generation rules after approval

For unresolved first-round exploration:

- `first_round_mode = EXPLORE_3`;
- exactly 3 concepts;
- all share the exact approved commercial job / CTA / brand constraints;
- concepts differ by **advertising logic**, not only by shape/style;
- every pair differs materially on >=3 design axes;
- hero generation is optional;
- hero generation is not the default first step;
- raw generated asset is never the user-facing visual concept;
- every user-facing result is a complete `BANNER_COMPOSITE`;
- every complete concept must pass the existing pre-show exact-artifact quality gates.

Examples of different advertising logic include:

- product/evidence-led;
- decision/choice-led;
- commercial-message/typography-led;
- comparison-led;
- outcome-led;
- proof-led;
- another task-specific logic with a clear commercial rationale.

Do not define A/B/C merely as “light 3D / dark 3D / typography.”

## Approval provenance

Create `graphic-banner-brief.json` matching `schemas/graphic-banner-brief.schema.json` and validate:

```bash
python scripts/validate_graphic_banner_brief.py \
  --commercial-job run/commercial/campaign-commercial-job.json \
  --brief run/design/graphic-banner-brief.json \
  --out run/design/graphic-banner-brief-gate.json
```

Required pre-decision state:

`GRAPHIC_BANNER_BRIEF_READY_FOR_USER_APPROVAL`.

The validator must keep:

- `render_allowed=false`;
- `full_production_allowed=false`.

The user decision is a separate exact-SHA artifact matching `schemas/graphic-banner-brief-decision.schema.json`.

Validate:

```bash
python scripts/validate_graphic_banner_brief_decision.py \
  --brief run/design/graphic-banner-brief.json \
  --decision run/design/graphic-banner-brief-decision.json \
  --out run/design/graphic-banner-brief-decision-gate.json
```

Only:

- `decided_by = USER`;
- `decision = APPROVE`;
- exact current brief SHA;

may produce:

`GRAPHIC_BANNER_BRIEF_APPROVED`

and:

`visual_exploration_allowed=true`.

No controller, Style Intelligence agent, reviewer or designer can approve this gate on the user's behalf.

## REVISE BRIEF

`REVISE` requires concrete user feedback and returns:

`GRAPHIC_BANNER_BRIEF_REVISE_REQUESTED`.

Visual rendering remains blocked. Update the brief, create new bytes/SHA, show the revised human-readable brief, and ask again.

## Relationship to later visual approval

Brief approval is **not** approval of any visual.

There are two separate user decisions:

1. **APPROVE BRIEF** — “Yes, this is the right advertising/design problem and constraints.”
2. **SELECT / APPROVE VISUAL** — “Yes, this rendered design system is the direction to produce.”

Neither substitutes for the other.

## Completion rule

Before first-round rendering, the controller must be able to prove:

- exact commercial job locked;
- required research/category evidence complete or explicitly accepted degraded;
- Graphic Banner Brief valid;
- exact current brief SHA approved by USER;
- later concept generation remains inside that approved contract.

If not, stop with one of:

- `GRAPHIC_BANNER_BRIEF_MISSING`;
- `GRAPHIC_BANNER_BRIEF_INVALID`;
- `GRAPHIC_BANNER_BRIEF_AWAITING_USER_APPROVAL`;
- `GRAPHIC_BANNER_BRIEF_REVISE_REQUESTED`;
- `GRAPHIC_BANNER_BRIEF_STALE`.
