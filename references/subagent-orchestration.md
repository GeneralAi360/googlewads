# Subagent Orchestration for Banner Runs

This contract adapts the narrow-context controller model used by Matreshka Agent to advertising-design production.

The purpose is not to spawn agents for spectacle. It is to keep a large banner program from becoming one overloaded context while preserving one controller-owned commercial truth, visual strategy, design system, policy state, and output matrix.

Load `references/gate-order-and-blocking-boundaries.md` whenever a downstream gate returns a stop state. A stop state must block only the phases that actually depend on it.

## Controller authority

The controller owns:

- user intent and accepted business facts;
- commercial/CTA truth;
- canonical brand identity;
- Google mode/spec/policy snapshot;
- reference and competitive-research synthesis;
- IDEA_ARCHITECTURE and emotional target;
- VISUAL_CHARACTER;
- Style Intelligence context/recommendation/selection;
- attention and typography strategy;
- pre-render policy-risk classification;
- LIGHTING_INTENT;
- required-asset contract and asset-readiness adjudication;
- art-direction approval;
- representative approval;
- campaign design system;
- banner matrix/output count;
- dispatch boundaries;
- review adjudication;
- Google technical and policy validation;
- final completion/Google-ready claim.

Subagents cannot expand scope or redefine these authorities.

## Critical gate-order rule

Do not let a downstream implementation gate stop upstream reasoning.

Canonical strategic order:

`BUSINESS / MARKET -> IDEA -> VISUAL CHARACTER -> STYLE INTELLIGENCE -> ATTENTION / TYPOGRAPHY -> POLICY RISK -> LIGHTING INTENT -> WRITTEN ART DIRECTION -> REQUIRED-ASSET CONTRACT -> ASSET READINESS -> REPRESENTATIVE RENDER`

`NEEDS_ASSET` is **not** a global stop state.

It blocks:
- representative render;
- representative approval;
- representative-dependent campaign-system freeze;
- scale-out/full pack;
- final exact-artifact technical/policy validation.

It does not by itself block:
- IDEA_ARCHITECTURE;
- VISUAL_CHARACTER;
- Style Intelligence lanes;
- attention profile;
- typography profile;
- LIGHTING_INTENT;
- written art-direction reasoning;
- pre-render Google policy-risk analysis.

If an asset property is unknown, use `CONDITIONAL` / `PENDING_ASSET_INSPECTION` for the affected detail and continue the upstream strategy rather than skipping the whole layer.

## Shared immutable run state

Before production scale-out, freeze the relevant chain:

- `BUSINESS_BRIEF` / accepted intake;
- `COMMERCIAL_LOCK`;
- `BRAND_IDENTITY_LOCK`;
- `REFERENCE_DNA` when applicable;
- competitive/category research state;
- `IDEA_ARCHITECTURE`;
- `VISUAL_CHARACTER`;
- selected `STYLE_STRATEGY` + exact recommendation SHA/components;
- attention/typography strategy;
- `LIGHTING_INTENT`;
- written art-direction approval;
- required asset contract and validated representative assets;
- representative approval;
- `CAMPAIGN_DESIGN_SYSTEM`;
- `GOOGLE_SPEC_SNAPSHOT`;
- `BANNER_MATRIX`;
- one `CREATIVE_CONTRACT` per final concept.

The controller may pass only the relevant slice to each agent.

Do not send the whole conversation, all references, every concept, every output, or the whole campaign history to every worker.

## Role 1 — REFERENCE_ANALYST

Use when references are supplied.

### Input

- one reference or small coherent reference set;
- user statement about what they like/dislike, if available;
- business category only when needed to judge transferability.

### Output

A read-only `REFERENCE_DNA` record:

- dominant layout/grid;
- focal point and scan path;
- copy/type behavior;
- color/contrast;
- whitespace/density;
- CTA behavior;
- hero scale/crop;
- lighting/shadow/reflection behavior;
- mood/brand signals;
- transferable principles;
- literal elements not to copy;
- uncertainties.

### Boundary

No final banners. No invented brand facts. No campaign-strategy authority.

## Role 2 — COMPETITOR_RESEARCHER

Read-only researcher for one advertiser/query/source target.

Records observed evidence, source URL, date, evidence tier, and limitations. It must not label a creative high-converting without permitted A/B conversion evidence.

## Role 3 — IDEA / STYLE STRATEGY WORK

The controller may use narrow strategists/reviewers for semantic or style exploration, but it retains the final decision.

Expected outputs may include:
- core idea / single takeaway;
- presentation mode;
- emotional target;
- visual-character signature;
- Style Intelligence lane proposal;
- attention plan;
- typography role;
- lighting affinity;
- risks/anti-patterns.

These stages can run while required production assets are missing, provided asset truth is represented honestly in the context.

## Role 4 — LIGHTING_DIRECTOR

Use when scene/composition lighting materially affects hierarchy or asset treatment.

### Input

- frozen idea/presentation/emotion;
- selected style strategy;
- primary AOI;
- product/material/asset truth;
- copy-safe needs;
- brand palette;
- relevant reference-lighting DNA;
- allowed lighting library.

### Output

- `LIGHTING_INTENT` candidate;
- scene-lighting mode and candidate scheme IDs where applicable;
- composition-lighting mode and allowed primitives;
- copy-safe strategy;
- focal priority;
- forbidden lighting behaviors.

### Boundary

Lighting supports the frozen strategy; it may not become a new concept or fabricate product UI.

## Role 5 — ART_DIRECTION_DESIGNER / ART_DIRECTOR_REVIEWER

Art directions are written before representative rendering when unresolved.

Each direction must inherit:
- commercial and brand locks;
- idea/emotion;
- visual character;
- exact Style Intelligence strategy identity/components;
- attention/typography;
- lighting intent;
- policy exclusions.

A direction may identify required assets even when they are not yet available. Missing assets block representative rendering, not the written art-direction reasoning itself.

## Role 6 — BANNER_DESIGNER

Default production worker after preproduction is genuinely ready.

### Granularity

**One banner matrix row = one fresh banner-worker task context by default.**

A row is one concept × size × variant × language × final output file.

### Input

Only the narrow task brief:

- job ID;
- exact dimensions/layout family;
- exact approved copy;
- exact approved assets;
- frozen campaign design system;
- concept/style/idea/lighting IDs;
- relevant reference DNA;
- Google technical/policy constraints relevant to the artifact;
- output path;
- banner-specific QA gate.

### Allowed decisions

The worker may:

- reflow elements for the assigned format;
- remove lower-priority content according to frozen hierarchy rules;
- choose an approved format-appropriate crop;
- tune spacing/scale within the campaign design system;
- apply approved composition-lighting behavior.

### Forbidden decisions

The worker may not:

- change product/offer/price/qualifier;
- invent proof;
- change CTA semantics;
- change advertiser/brand identity;
- invent partner/affiliate/trademark status;
- redefine idea/style/lighting;
- fabricate real product UI/logo when substitution is forbidden;
- produce other sizes;
- write shared run state;
- modify another worker's output;
- create child agents.

If the assigned information cannot fit without breaking hierarchy/legibility, return `FORMAT_CONFLICT` rather than silently shrinking everything.

## Role 7 — DESIGN_REVIEWER

Independent, read-only.

Review the exact rendered banner and its diagnostics for:

- concept/idea/emotion fidelity;
- visual-character/style-strategy fidelity;
- campaign-design-system fidelity;
- brand consistency;
- asset quality/truth;
- category fit;
- visual hierarchy/primary AOI;
- lighting-intent fidelity;
- typography/readability;
- color/contrast/density;
- crop/safe zones;
- CTA clarity;
- anti-generic-AI quality;
- actual-size/thumbnail/grayscale/squint behavior.

Do not fix files.

## Role 8 — GOOGLE_POLICY_REVIEWER

Independent/read-only when the host supports a fresh context.

Review the exact artifact SHA plus exact ad/destination context for current Google Ads policy risk, including misleading design, claims, destination support, advertiser identity, affiliation/trademark context, restricted-vertical applicability, and other policy facts defined by the policy contract.

This role cannot guarantee Google approval.

## Role 9 — PACK_REVIEWER

Use after individual jobs are assembled and individually reviewed.

Review:

- missing/duplicate rows;
- cross-size idea/style/brand/lighting consistency;
- intentional recomposition;
- small-format simplification;
- asset/category quality consistency;
- filenames/variant IDs;
- contact-sheet and pack completeness.

Read-only.

## Deterministic validators

Deterministic code, not subjective agents, owns exact checks such as:
- dimensions/file signatures/file size;
- matrix/spec bindings;
- commercial/style/design-system provenance;
- representative asset file/hash/dimension/rights/privacy state;
- Google technical preflight;
- exact-SHA policy report aggregation;
- final Google-ready local precheck.

Agent review cannot substitute for deterministic validation, and deterministic PASS cannot substitute for design/policy judgment where semantic review is required.

## Canonical dispatch sequence

1. Controller resolves intake, commercial/brand truth and output scope.
2. Freeze planning envelope/matrix without dispatching final production.
3. Analyze supplied references and competitive/category evidence.
4. Resolve IDEA_ARCHITECTURE and emotional target.
5. Resolve VISUAL_CHARACTER.
6. Run Style Intelligence and choose/approve strategy lane.
7. Resolve attention and typography roles.
8. Run pre-render Google policy-risk screen.
9. Resolve LIGHTING_INTENT.
10. Produce/approve written art direction.
11. Define exact `required_assets` from that strategy/direction.
12. Validate representative assets.
    - if `NEEDS_ASSET`, report exact missing files and stop **before render only**;
    - do not retroactively mark steps 4–10 `NOT_RUN`.
13. When `ASSETS_READY`, render exactly one high-fidelity representative.
14. Review/approve representative.
15. Freeze campaign design system.
16. Freeze preproduction/creative contracts.
17. Dispatch one `BANNER_DESIGNER` context per final matrix row.
18. Run Google technical preflight for each output.
19. Build diagnostic QA views and dispatch independent design reviews.
20. Run exact-artifact Google policy preflight and pack aggregation.
21. Run pack review/readiness and final local Google-ready precheck.
22. Deliver only when all required gates have terminal passing status.

## Parallelism and isolation

### Safe to parallelize

- independent reference analysis;
- independent competitor/source research;
- independent written concept/style proposals before selection;
- read-only design/policy reviews;
- banner workers only if each worker writes to a disjoint path and the host provides real isolated/fresh contexts.

### Do not parallelize blindly

Do not let multiple writers edit the same:
- banner artifact;
- commercial/brand lock;
- design brief;
- art-direction approval;
- campaign design system;
- banner matrix;
- shared manifest;
- generated source asset.

Those remain controller-owned or sequential.

## Degraded mode

If the host cannot create fresh independent subagent contexts:

1. state `SUBAGENT_MODE=DEGRADED`;
2. group production work narrowly;
3. keep resettable task briefs;
4. do not claim reviewer independence when the same context is reused;
5. still preserve exact matrix/job/gate boundaries.

## Job IDs

Recommended deterministic ID:

`C{concept}-S{width}x{height}-V{variant}-L{language}`

Examples:
- `C01-S300x250-V01-Lru`
- `C01-S728x90-V01-Lru`
- `C02-S300x600-V02-Len`

Output path:

`outputs/{run_id}/{job_id}/{job_id}.png`

## Worker report

Every banner worker returns:

- job ID/status/output path;
- concept/size/layout/variant/language;
- copy actually rendered;
- frozen idea/style/lighting identity;
- intentional content removed for the size;
- known visual/policy risks;
- technical preflight status if available;
- requested controller decision if blocked.

## Stop statuses and scope

Typical statuses:
- `NEEDS_CONTEXT`;
- `FORMAT_CONFLICT`;
- `NEEDS_ASSET` / `ASSET_MISSING`;
- `CLAIM_UNVERIFIED`;
- `REFERENCE_CONFLICT`;
- `LIGHTING_CONFLICT`;
- `POLICY_REVIEW_REQUIRED`;
- `PRE_RENDER_POLICY_BLOCKED`;
- `DESIGN_CHANGED`;
- `DESIGN_DRIFT`;
- `TECHNICAL_BLOCKED`;
- `PASS`.

A subagent stops rather than expanding scope, but the controller must apply the stop **only to dependent downstream phases** according to `references/gate-order-and-blocking-boundaries.md`.

## Matreshka compatibility

When Matreshka Agent is installed/available, use its native fresh-context mechanisms and preserve its controller principles:

- controller retains authority;
- narrow task briefs;
- no child agents;
- exact write/inspect allowlists where supported;
- stable threads for fixes/rechecks;
- independent read-only review when the host can guarantee it;
- explicit degraded mode when it cannot.

This skill does not duplicate Matreshka's runtime. It defines banner-specific roles, contracts, gate order, and payloads to route through that runtime.
