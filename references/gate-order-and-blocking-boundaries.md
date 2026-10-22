# Preproduction gate order and blocking boundaries

This reference defines **which failures stop which phases**.

Three real Work failures motivate it:

1. `REAL-03` — a correct `NEEDS_ASSET` result incorrectly skipped upstream IDEA / STYLE / attention / typography / LIGHTING work.
2. `REAL-05` — after strategy completed, `NEEDS_ASSET` was still treated as a reason to show the user no actual banner concept at all.
3. `REAL-06` — a stale implementation-service assumption survived into the rendered preview even though the actual campaign was for Bitrix24 license purchase/renewal, and an internal A2 recommendation was mistaken for a user-locked direction.

## Canonical dependency

`BUSINESS FACTS -> COMMERCIAL JOB LOCK -> MARKET / RESEARCH -> IDEA -> VISUAL CHARACTER -> STYLE INTELLIGENCE -> ATTENTION / TYPOGRAPHY -> POLICY RISK -> LIGHTING INTENT -> INTERNAL ART DIRECTION -> FIRST-ROUND VISUAL EXPLORATION -> USER SELECTION / APPROVAL -> PRODUCTION ASSET COMPLETION IF NEEDED -> PRODUCTION REPRESENTATIVE -> SCALE-OUT`

The exact commercial job is upstream of creative strategy. Production asset readiness is downstream of semantic/style reasoning and does not by itself hide the design from the user.

## Commercial-job boundary

Product identity, campaign objective, CTA wording and the commercial job are separate facts.

Examples for one Bitrix24 product family:
- `NEW_LICENSE_PURCHASE`;
- `LICENSE_RENEWAL`;
- `PURCHASE_OR_RENEWAL`;
- `IMPLEMENTATION_SERVICE`;
- `CONSULTATION`.

### `COMMERCIAL_JOB_UNRESOLVED`

Blocks:
- idea architecture that depends on the transaction/service being advertised;
- commercial-message hierarchy;
- art direction;
- rendered visual concepts;
- user approval;
- production.

Does not block:
- generic category research that does not silently choose a transaction;
- landing-page inspection;
- brand/asset inventory.

Do not infer `IMPLEMENTATION_SERVICE` merely because a company also implements the product. Do not infer license purchase/renewal merely because license cards exist. Ask the minimum necessary question when the exact job is not already explicit.

### `COMMERCIAL_JOB_CHANGED`

A material change such as:

`IMPLEMENTATION_SERVICE -> PURCHASE_OR_RENEWAL`

invalidates stale downstream artifacts. Do not preserve the old visual by changing one line of copy.

At minimum reconsider/invalidate:
- idea architecture;
- commercial hierarchy;
- style-strategy context/recommendation when meaning changes;
- attention/type hierarchy;
- lighting intent if AOI/meaning changes;
- art direction;
- rendered visual concepts;
- visual user decisions;
- campaign design system;
- creative contracts.

## Visual exploration boundary

Final production concept count and first-round exploration count are different.

`deliverables.concept_count = 1` may coexist with `visual_exploration_count = 3`.

### Unlocked direction

If `direction_lock_source` is:
- `NONE`; or
- `INTERNAL_RECOMMENDATION`;

first user-facing exploration must use `EXPLORE_3` and render exactly three materially distinct concepts.

An internal Style Intelligence/controller/research/art-director recommendation is decision support, not user lock evidence.

### Explicit user lock

`SINGLE_USER_LOCKED` is allowed only with `direction_lock_source = USER_LOCKED` and explicit evidence that the user chose/approved that direction.

### Insufficient exploration

A single concept is blocking when no user lock exists.

Three concepts are still blocking if they are cosmetic variants. Every pair must differ on at least three of:
- hero logic;
- composition system;
- attention profile;
- typography profile;
- graphic device;
- lighting language.

Before user presentation, each concept must pass an exact-artifact `ART_DIRECTOR_REVIEWER` quality gate including:
- commercial-job fidelity;
- professional category fit;
- ad-not-presentation-slide;
- hierarchy;
- typography;
- CTA integration;
- visual distinctiveness;
- anti-template quality;
- small-format viability.

These checks control craft and semantic correctness; they are not performance predictions.

## Two asset-readiness notions

### Concept-preview readiness

Question:

> Can the system show the user the intended visual design without fabricating product/brand truth?

This may be possible with:
- production assets;
- low-resolution authentic surrogates;
- reference-only authentic/public surrogates;
- neutral structural placeholders;
- neutral text-brand placeholders.

Concept preview never permits fake/generated product UI or fake logos.

### Production asset readiness

Question:

> Are the exact assets acceptable for final advertising production and delivery?

This remains governed by `representative-asset-readiness.json` and may correctly return `NEEDS_ASSET` while concept-preview readiness is still `READY`.

## `NEEDS_ASSET`

Blocks:
- treating concept-only surrogates as production assets;
- final production representative when required real assets are missing;
- campaign design system freeze when production representative evidence is required;
- scale-out/full-pack production;
- final exact-artifact Google technical/policy review;
- delivery/upload-ready claims.

Does **not** block by itself:
- IDEA_ARCHITECTURE;
- emotional target;
- VISUAL_CHARACTER;
- Style Intelligence recommendation lanes;
- attention profile;
- typography profile;
- LIGHTING_INTENT;
- internal art-direction development;
- pre-render Google policy-risk analysis;
- creation of `required_assets` contract;
- rendering a safe `VISUAL_SYSTEM_WITH_ASSET_SLOTS` concept preview;
- first-round EXPLORE_3;
- showing concept cards/contact sheet;
- user visual selection/approval.

If a strategy depends on an unknown asset property, use an explicit constraint/slot and mark the affected implementation detail `PENDING_ASSET_INSPECTION`; do not hide the design.

## Concept preview with surrogates

If any preview asset is not production-ready:
- `approval_scope = VISUAL_SYSTEM_WITH_ASSET_SLOTS`;
- `production_asset_readiness = NEEDS_ASSET`;
- `not_for_delivery = true`;
- full production remains blocked after user approval until real assets are supplied and fidelity is verified.

A concept preview may be high-fidelity in composition, typography, color, CTA, whitespace, attention and graphic system while using explicitly declared asset slots.

## Unsafe concept surrogate

If visualizing a concept would require fabricating an authentic-looking product UI/logo or violating privacy/rights constraints, do **not** create that fake asset.

Use a structural placeholder instead. If even a structural placeholder cannot communicate the concept, report `VISUAL_CONCEPT_PREVIEW_BLOCKED` with the exact reason.

## Other stop states

### `BRAND_IDENTITY_UNRESOLVED`

Blocks any user-facing stage that requires choosing/displaying one of conflicting identities. Generic category research may continue. Do not let a worker silently select the brand.

### `COMMERCIAL_LOCK_CONFLICT`

Blocks a visual concept when proposition/CTA/qualifier are materially unresolved. Research/style analysis may continue only if it does not silently choose one conflicting message.

### `PRE_RENDER_POLICY_BLOCKED`

Blocks rendering/approval of the affected concept. It does not prevent revising IDEA / STYLE / ART DIRECTION to remove the issue.

### `RESEARCH_RIGOR = DEGRADED`

Does not block strategy or concept preview when explicitly accepted. It lowers evidence rigor and prohibits performance claims.

## Controller rule

A controller/user prompt must not reorder hard gates so a downstream implementation state blocks upstream reasoning or user-visible concept communication.

Do **not** use:

`broad product known -> assume commercial job -> design`

or:

`internal recommendation -> assume user lock -> show one concept`

or:

`validate production assets -> if NEEDS_ASSET stop everything`.

Correct logic:

`resolve exact commercial job -> strategy -> three concepts unless USER_LOCKED -> show user -> selection/approval -> production assets/fidelity -> scale-out`.

## Reporting rule

Report separate tracks:

1. `COMMERCIAL_JOB_STATUS`;
2. `STRATEGY_STATUS`;
3. `VISUAL_EXPLORATION_STATUS`;
4. `VISUAL_CONCEPT_STATUS` for the selected concept;
5. `PRODUCTION_ASSET_READINESS`.

Expected strong unlocked first-round state:

```text
COMMERCIAL_JOB = LOCKED
STRATEGY_STATUS = COMPLETE
VISUAL_EXPLORATION_MODE = EXPLORE_3
VISUAL_EXPLORATION_COUNT = 3
VISUAL_CONCEPT_SET = AWAITING_USER_SELECTION
PRODUCTION_ASSET_READINESS = NEEDS_ASSET   # allowed for preview path
FULL_PRODUCTION = BLOCKED_PENDING_USER_SELECTION
```

The user should receive genuine visual choice, not a stale commercial assumption or a single internally preselected design.
