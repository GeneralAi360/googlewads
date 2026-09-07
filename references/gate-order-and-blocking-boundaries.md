# Preproduction gate order and blocking boundaries

This reference defines **which failures stop which phases**. It exists because a real Work acceptance run returned `NEEDS_ASSET` and then incorrectly skipped IDEA_ARCHITECTURE, VISUAL_CHARACTER, Style Intelligence, attention, typography, and LIGHTING_INTENT.

The failure was not that `NEEDS_ASSET` was wrong. The failure was treating it as a global stop state.

## Canonical dependency

`BUSINESS / MARKET -> IDEA -> VISUAL CHARACTER -> STYLE INTELLIGENCE -> ATTENTION / TYPOGRAPHY -> POLICY RISK -> LIGHTING INTENT -> WRITTEN ART DIRECTION -> REQUIRED-ASSET CONTRACT -> ASSET READINESS -> REPRESENTATIVE RENDER`

Asset readiness belongs **after** the strategic/design-system work that determines what assets are required.

## Blocking boundary matrix

### `NEEDS_ASSET`

Blocks:
- representative rendering;
- representative approval;
- campaign design system freeze when it requires representative evidence;
- scale-out/full-pack rendering;
- final exact-artifact Google technical/policy review.

Does **not** block by itself:
- IDEA_ARCHITECTURE;
- emotional target;
- VISUAL_CHARACTER;
- Style Intelligence recommendation lanes;
- attention profile;
- typography profile;
- LIGHTING_INTENT;
- written art-direction development;
- pre-render Google policy-risk analysis;
- creation of `required_assets` contract;
- explanation of exact missing asset specifications.

If a strategy depends on an unknown asset property (for example the real UI crop cannot be characterized at all), continue with an explicit assumption/constraint and mark the affected field `CONDITIONAL` or `PENDING_ASSET_INSPECTION`; do not skip the entire strategic layer.

### `BRAND_IDENTITY_UNRESOLVED`

Blocks any stage that would require choosing/displaying a brand identity. It may still allow category research and generic idea exploration that does not choose between conflicting identities. Controller must not let a worker silently select an identity.

### `COMMERCIAL_LOCK_CONFLICT`

Blocks art-direction approval and rendering when proposition/CTA/qualifier are material to the banner. Research/style analysis may continue only if it does not silently pick one conflicting commercial message.

### `PRE_RENDER_POLICY_BLOCKED`

Blocks approval/rendering of the affected concept. It does not prevent the system from revising IDEA / STYLE / ART DIRECTION to remove the policy issue.

### `RESEARCH_RIGOR = DEGRADED`

Does not block strategy work when explicitly accepted. It lowers evidence rigor and prohibits performance claims.

## Controller rule

A controller/user prompt must not reorder hard gates in a way that makes a downstream implementation gate block upstream reasoning.

In particular, do **not** issue instructions equivalent to:

`validate assets -> if not ASSETS_READY stop -> then run IDEA/STYLE`

The correct order is:

`resolve IDEA/STYLE/ATTENTION/TYPE/LIGHT -> define required assets -> validate assets -> stop before render if NEEDS_ASSET`.

## Reporting rule

When assets are missing, report both tracks:

1. `STRATEGY_STATUS` — which semantic/style/art-direction phases are complete;
2. `RENDER_READINESS` — `ASSETS_READY` or `NEEDS_ASSET`.

Example:

```text
IDEA_ARCHITECTURE = READY
VISUAL_CHARACTER = READY
STYLE_STRATEGY = SELECTED
ATTENTION_PROFILE = READY
TYPOGRAPHY_PROFILE = READY
LIGHTING_INTENT = READY
PRE_RENDER_POLICY = PASS
ASSET_READINESS = NEEDS_ASSET
REPRESENTATIVE_RENDER = BLOCKED
```

This is the expected state for a strong preproduction run that has finished thinking but is waiting for real production assets.
