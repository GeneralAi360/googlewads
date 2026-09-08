# Preproduction gate order and blocking boundaries

This reference defines **which failures stop which phases**.

Two real Work failures motivate it:

1. `REAL-03` — a correct `NEEDS_ASSET` result incorrectly skipped upstream IDEA / STYLE / attention / typography / LIGHTING work.
2. `REAL-05` — after strategy completed, `NEEDS_ASSET` was still treated as a reason to show the user no actual banner concept at all.

The failure was not that production assets were missing. The failure was applying a production-readiness state to the wrong user-facing boundary.

## Canonical dependency

`BUSINESS / MARKET -> IDEA -> VISUAL CHARACTER -> STYLE INTELLIGENCE -> ATTENTION / TYPOGRAPHY -> POLICY RISK -> LIGHTING INTENT -> INTERNAL WRITTEN ART DIRECTION -> REQUIRED-ASSET CONTRACT -> RENDERED VISUAL CONCEPT -> USER DECISION -> PRODUCTION ASSET COMPLETION IF NEEDED -> PRODUCTION REPRESENTATIVE -> SCALE-OUT`

Production asset validation still matters. It simply has a narrower blocking scope than before.

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

## Blocking boundary matrix

### `NEEDS_ASSET`

Blocks:
- treating concept-only surrogates as production assets;
- final production representative when required real assets are still missing;
- campaign design system freeze if the selected path requires production representative evidence;
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
- internal written art-direction development;
- pre-render Google policy-risk analysis;
- creation of `required_assets` contract;
- rendering a safe `VISUAL_SYSTEM_WITH_ASSET_SLOTS` concept preview;
- showing the user a short plain-language concept summary;
- asking the user `APPROVE / REVISE / REJECT` on that rendered visual system.

If a strategy depends on an unknown asset property, use an explicit constraint/slot and mark the affected implementation detail `PENDING_ASSET_INSPECTION`; do not hide the design.

### Concept preview with surrogates

If any preview asset is not production-ready:
- `approval_scope = VISUAL_SYSTEM_WITH_ASSET_SLOTS`;
- `production_asset_readiness = NEEDS_ASSET`;
- `not_for_delivery = true`;
- full production remains blocked after user approval until real assets are supplied and fidelity is verified.

A concept preview is allowed to be high-fidelity in composition, typography, color, CTA, whitespace, attention and graphic system while using explicitly declared asset slots.

### Unsafe concept surrogate

If the only way to visualize the concept would be to fabricate an authentic-looking product UI/logo or violate privacy/rights constraints, do **not** create that fake asset.

Use a structural placeholder instead. If even a structural placeholder cannot communicate the concept, report `VISUAL_CONCEPT_PREVIEW_BLOCKED` with the exact reason. This should be exceptional.

### `BRAND_IDENTITY_UNRESOLVED`

Blocks any user-facing stage that would require choosing/displaying one of conflicting identities. It may still allow category research and generic idea exploration. Do not let a worker silently choose the brand.

### `COMMERCIAL_LOCK_CONFLICT`

Blocks a visual concept when proposition/CTA/qualifier are materially unresolved. Research/style analysis may continue only if it does not silently pick one conflicting message.

### `PRE_RENDER_POLICY_BLOCKED`

Blocks rendering/approval of the affected concept. It does not prevent revising IDEA / STYLE / ART DIRECTION to remove the issue.

### `RESEARCH_RIGOR = DEGRADED`

Does not block strategy or concept preview when explicitly accepted. It lowers evidence rigor and prohibits performance claims.

## Controller rule

A controller/user prompt must not reorder hard gates so a downstream implementation state blocks upstream reasoning or user-visible concept communication.

Do **not** use:

`validate production assets -> if NEEDS_ASSET stop everything`

The correct logic is:

`resolve strategy -> define required assets -> determine concept-preview asset mode -> render/show concept -> user decision -> resolve final production assets -> production/fidelity gates`.

## Reporting rule

When production assets are missing, report three tracks:

1. `STRATEGY_STATUS` — semantic/style/art-direction work;
2. `VISUAL_CONCEPT_STATUS` — whether a rendered design has been shown to the user;
3. `PRODUCTION_ASSET_READINESS` — `ASSETS_READY` or `NEEDS_ASSET`.

Expected strong state with missing final assets:

```text
IDEA_ARCHITECTURE = READY
VISUAL_CHARACTER = READY
STYLE_STRATEGY = SELECTED
ATTENTION_PROFILE = READY
TYPOGRAPHY_PROFILE = READY
LIGHTING_INTENT = READY
PRE_RENDER_POLICY = PASS
VISUAL_CONCEPT_STATUS = AWAITING_USER_APPROVAL
VISUAL_CONCEPT_APPROVAL_SCOPE = VISUAL_SYSTEM_WITH_ASSET_SLOTS
PRODUCTION_ASSET_READINESS = NEEDS_ASSET
FULL_PRODUCTION = BLOCKED_PENDING_USER_DECISION_AND_REAL_ASSETS
```

The user should see the concept even though production cannot yet finish.
