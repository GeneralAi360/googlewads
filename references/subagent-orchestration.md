# Subagent Orchestration for Banner Runs

This contract adapts the narrow-context controller model used by Matreshka Agent to advertising-design production.

The purpose is not to spawn agents for spectacle. It is to keep a large banner pack from becoming one overloaded context, while preserving one controller-owned brief and one coherent design system.

## Controller authority

The controller owns:

- user intent and accepted business facts;
- current Google mode/spec snapshot;
- brand/design identity;
- reference synthesis;
- creative concept contracts;
- lighting-plan approval;
- banner matrix;
- output count;
- dispatch boundaries;
- review adjudication;
- technical validation;
- final completion claim.

Subagents cannot expand scope or redefine these authorities.

## Shared immutable run state

Before banner production, freeze:

- `BUSINESS_BRIEF`
- `BRAND_CONTEXT`
- `REFERENCE_DNA` when applicable
- `GOOGLE_SPEC_SNAPSHOT`
- one `CREATIVE_CONTRACT` per concept
- one `LIGHTING_PLAN` per concept or banner job
- `BANNER_MATRIX`

The controller may pass only the relevant slice to each agent.

Do not send the whole conversation, all references, every concept, every output, or the whole campaign history to every banner worker.

## Role 1 — REFERENCE_ANALYST

Use when references are supplied.

### Input

- one reference or a small coherent reference set;
- user statement about what they like/dislike, if available;
- business category only when needed to judge transferability.

### Output

A read-only `REFERENCE_DNA` record:

- dominant layout/grid;
- focal point;
- scan path;
- copy hierarchy;
- type behavior;
- color behavior;
- whitespace/density;
- CTA behavior;
- hero scale/crop;
- lighting direction/quality/color;
- shadows/reflections;
- mood;
- transferable principles;
- literal elements not to copy;
- uncertainties.

### Boundary

Do not generate final banners. Do not invent brand facts. Do not decide campaign strategy.

Multiple reference analysts may run in parallel because they are read-only.

## Role 2 — CREATIVE_STRATEGIST

Use when multiple concepts are requested or strategy is not already frozen.

One strategist should normally own one proposed concept direction.

### Input

- minimal business brief;
- verified offer/proof;
- target audience/funnel state;
- approved brand context;
- synthesized reference DNA if relevant.

### Output

A concept proposal containing:

- concept thesis;
- primary proposition;
- hook;
- visual idea;
- CTA;
- evidence/source grounding;
- intended attention path;
- recommended lighting family;
- risks;
- test hypothesis.

### Boundary

No final banner files. No platform-limit invention. No unsupported claims.

The controller selects/merges/rejects concepts and then freezes `CREATIVE_CONTRACT`.

## Role 3 — LIGHTING_DIRECTOR

Use when hero imagery is generated or relit and lighting materially affects hierarchy.

### Input

- product/material;
- concept mood;
- focal-object priority;
- copy-safe-zone need;
- brand palette;
- reference-lighting DNA;
- allowed lighting library.

### Output

- selected `lighting_scheme_id`;
- optional alternative scheme;
- scene-lighting directive;
- post-composite lighting directive;
- copy-safe zone;
- highlight/hotspot warnings;
- shadow/reflection direction;
- material-specific notes.

### Boundary

Lighting supports the frozen concept; it may not become a new concept.

## Role 4 — BANNER_DESIGNER

Default production worker.

### Granularity

**One banner matrix row = one fresh banner-worker task context by default.**

A row is one:
- concept;
- size;
- variant;
- language;
- final output file.

This is the primary mechanism that prevents context overload.

### Input

Only the narrow task brief:

- job ID;
- exact dimensions;
- layout family;
- exact approved copy;
- exact logo/brand assets;
- frozen concept ID;
- relevant reference DNA;
- relevant lighting directive;
- Google technical constraints;
- output path;
- banner-specific QA gate.

### Allowed decisions

The worker may:

- reflow elements for the assigned format;
- reduce/remove secondary content according to hierarchy rules;
- choose format-appropriate crop within the approved hero strategy;
- tune spacing/scale within the frozen design contract;
- apply the approved scene/composition lighting plan.

### Forbidden decisions

The worker may not:

- change product/offer/price;
- invent proof;
- change CTA semantics;
- change brand identity;
- redefine the concept;
- create a new lighting concept outside the approved plan;
- produce other sizes;
- write shared run state;
- modify another worker's output;
- create child agents.

If the assigned information cannot fit without breaking hierarchy/legibility, return `FORMAT_CONFLICT` rather than silently shrinking everything.

## Role 5 — DESIGN_REVIEWER

Independent, read-only.

Review the rendered banner at actual size and, for a pack, in contact-sheet context.

Review:

- concept fidelity;
- brand consistency;
- visual hierarchy;
- reference use;
- lighting and focal control;
- typography;
- color/contrast;
- density;
- crop;
- CTA clarity;
- actual-size legibility;
- cross-size consistency.

Return findings classified:

- `CRITICAL`
- `IMPORTANT`
- `MINOR`
- `PASS`

Do not fix files.

## Role 6 — PACK_REVIEWER

Use after individual banner jobs are assembled.

Review the matrix/contact sheet for:

- missing rows;
- accidental duplicates;
- inconsistent logo treatment;
- inconsistent visual identity;
- unintended concept drift;
- cross-size hierarchy failures;
- filenames/variant IDs;
- pack-level completeness.

This role is read-only.

## Technical validator

The technical validator is deterministic code, not a subjective agent.

For supported uploaded-display static banners run `scripts/validate_google_banner.py`.

Agent review cannot substitute for exact dimension/file-size/signature validation.

## Dispatch sequence

Default sequence:

1. Controller builds question pool and freezes run brief.
2. `REFERENCE_ANALYST` agents inspect references if present.
3. Controller synthesizes `REFERENCE_DNA`.
4. `CREATIVE_STRATEGIST` agents propose requested concepts if needed.
5. Controller freezes `CREATIVE_CONTRACT` records.
6. `LIGHTING_DIRECTOR` selects lighting where needed.
7. Controller creates every `BANNER_MATRIX` row.
8. Dispatch one `BANNER_DESIGNER` fresh context per row.
9. Run technical preflight for each produced file.
10. Dispatch independent `DESIGN_REVIEWER` checks.
11. Controller adjudicates findings.
12. One consolidated fix wave to the original worker thread for confirmed material issues.
13. Targeted re-review and technical revalidation.
14. `PACK_REVIEWER` inspects complete contact sheet/matrix.
15. Controller delivers only when all required rows have terminal status.

## Parallelism and isolation

### Safe to parallelize

- independent reference analysis;
- independent concept proposals;
- read-only design reviews;
- banner workers **only if** each worker writes to a disjoint path and the host provides real isolated/fresh contexts.

### Do not parallelize blindly

Do not let multiple writers edit:

- the same banner file;
- the same concept contract;
- `BRAND.md`;
- the banner matrix;
- shared manifest;
- a shared generated source file.

Those remain controller-owned or sequential.

## Degraded mode

If the host cannot create fresh independent subagent contexts:

1. state `SUBAGENT_MODE=DEGRADED`;
2. group banner work by one layout family at a time;
3. keep a narrow resettable brief for each job;
4. do not claim reviewer independence if the same context is reused;
5. still keep the matrix and exact job boundaries.

## Job IDs

Recommended deterministic ID:

`C{concept}-S{width}x{height}-V{variant}-L{language}`

Examples:

- `C01-S300x250-V01-Lru`
- `C01-S728x90-V01-Lru`
- `C02-S300x600-V02-Len`

Output path:

`outputs/{run_id}/{job_id}/{job_id}.png`

This gives every writer a disjoint directory and makes review/validation traceable.

## Banner-worker report

Every banner worker returns:

- job ID;
- status;
- output path;
- concept ID;
- size;
- layout family;
- copy actually rendered;
- lighting scheme ID;
- intentional content removed for the size;
- known visual risks;
- technical preflight status if available;
- requested controller decision if blocked.

## Stop statuses

- `NEEDS_CONTEXT`
- `FORMAT_CONFLICT`
- `ASSET_MISSING`
- `CLAIM_UNVERIFIED`
- `REFERENCE_CONFLICT`
- `LIGHTING_CONFLICT`
- `DESIGN_CHANGED`
- `DESIGN_DRIFT`
- `TECHNICAL_BLOCKED`
- `PASS`

A subagent stops rather than expanding scope.

## Matreshka compatibility

When Matreshka Agent is installed/available, use its native subagent/fresh-context mechanisms and preserve its controller principles:

- controller retains authority;
- narrow task briefs;
- no child agents;
- exact write/inspect allowlists where the host supports them;
- stable threads for fixes/rechecks;
- independent read-only review when the host can guarantee it;
- explicit degraded mode when it cannot.

This skill does not duplicate Matreshka's runtime. It defines the banner-specific roles, contracts, and payloads to route through that runtime.
