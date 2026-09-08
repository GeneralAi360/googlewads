# Google Ads Performance Banner Designer

A production-grade AI skill for researching, planning, exploring, designing, adapting, rendering, reviewing, validating and policy-preflighting professional Google Ads banners.

The project treats banner creation as a **creative-production system**, not a single image prompt.

## Canonical user flow

```text
BUSINESS CONTEXT
→ structured intake
→ EXACT COMMERCIAL JOB LOCK
→ output/run freeze
→ references + competitive/category research
→ IDEA_ARCHITECTURE / presentation / emotion
→ VISUAL_CHARACTER
→ STYLE INTELLIGENCE
→ attention + typography
→ PRE-RENDER GOOGLE POLICY RISK
→ LIGHTING_INTENT
→ internal art direction
→ FIRST-ROUND VISUAL EXPLORATION
→ user selects a rendered direction
→ revise / approve selected visual
→ production asset completion if needed
→ production representative / fidelity
→ CAMPAIGN_DESIGN_SYSTEM
→ full multi-format production
→ GOOGLE TECHNICAL PREFLIGHT
→ visual QA / independent review
→ FINAL GOOGLE ADS POLICY PREFLIGHT
→ exact-SHA policy pack aggregation
→ GOOGLE_READY_PRECHECK
→ delivery / performance learning
```

The system must not scale a full pack before user-rooted visual approval.

## Exact commercial job is a first-class fact

Product identity, campaign objective, CTA, and the exact commercial transaction/service job are different facts.

For example, all of these may concern Bitrix24 but are different campaign jobs:

- new license purchase;
- license renewal;
- purchase or renewal;
- implementation service;
- consultation.

The campaign commercial job is frozen in `campaign-commercial-job.json` and validated with `scripts/validate_campaign_commercial_job.py`.

A material job change invalidates meaning-dependent downstream strategy and visuals instead of preserving a stale design with a copy edit.

See `references/commercial-job-and-concept-exploration.md`.

## Visual exploration before selection

Final campaign concept count and first-round exploration count are separate.

A campaign can have:

- `final concept_count = 1`;
- `visual_exploration_count = 3`.

Unless the user explicitly locked a direction, first-round visual exploration uses `EXPLORE_3`: three materially different rendered concepts in the same representative size.

An internal Style Intelligence recommendation, category recommendation, previous Work recommendation, or reviewer preference is **not** a user lock.

Three concepts must differ materially across hero logic, composition, attention, typography, graphic device and/or lighting language; palette swaps and near-identical SaaS layouts do not count.

Before the user sees them, an `ART_DIRECTOR_REVIEWER` must PASS each rendered concept for:

- commercial-job fidelity;
- professional category fit;
- ad-not-presentation-slide quality;
- hierarchy;
- typography;
- CTA integration;
- visual distinctiveness;
- anti-template quality;
- small-format viability.

The validated set uses:

- `schemas/visual-concept-set.schema.json`;
- `scripts/validate_visual_concept_set.py`.

The user should receive A/B/C together, not a hidden internal winner masquerading as an approved direction.

## Visual approval and pending assets

The user approves the **rendered visual**, not a text-only art direction.

Production asset readiness is separate from concept visibility.

If production assets are missing, the skill may still show a high-fidelity concept using declared safe temporary modes:

- authentic low-resolution surrogate;
- reference-only authentic/public surrogate;
- structural placeholder;
- text-brand placeholder.

Fake/generated product UI and fake/generated logos are prohibited even in concept previews.

A surrogate concept remains:

- `production_asset_readiness = NEEDS_ASSET`;
- `not_for_delivery = true`;
- `approval_scope = VISUAL_SYSTEM_WITH_ASSET_SLOTS`.

After user approval and real asset substitution, a fidelity gate may continue without redundant second approval only when there is no material visual drift. Material drift must be shown again.

See `references/visual-concept-approval.md` and `references/gate-order-and-blocking-boundaries.md`.

## Meaning / Style / Attention / Typography / Lighting

The skill resolves meaning before style.

Style Intelligence is a controller layer above the individual banner:

`foundation grammar + optional current overlay + execution language + attention profile + typography profile + lighting affinity + format resilience`.

It returns:

- `SAFE_STRONG`;
- `CURRENT_DIFFERENTIATED`;
- `CONTROLLED_WILDCARD`.

Trend/currentness is capped and cannot rescue poor category fit, product truth, attention, typography, lighting or format resilience.

Lighting follows:

`IDEA → PRESENTATION → EMOTION → VISUAL CHARACTER → STYLE STRATEGY → PRIMARY AOI → LIGHTING INTENT`.

The 30 lighting schemes are candidate vocabulary, not a free-standing style picker. Real UI can make scene lighting `NOT_APPLICABLE`.

## Google technical preflight != Google policy preflight

Technical validation checks exact dimensions, bytes, file format and static-state requirements. It does not prove advertising-policy compliance.

The separate policy layer includes:

- `references/google-ads-policy-preflight.md`;
- `config/google-ads-policy-snapshot.json`;
- `schemas/google-policy-context.schema.json`;
- `schemas/google-policy-report.schema.json`;
- `scripts/validate_google_policy.py`;
- `scripts/aggregate_google_policy_reports.py`;
- `scripts/assess_google_ready.py`.

It checks misleading design, image/text quality, commercial claims/qualifiers, destination consistency, advertiser identity, affiliation/trademark context, restricted verticals and other applicable policy evidence.

`GOOGLE_READY_PRECHECK_PASS` is local risk reduction only and never guarantees Google approval.

## Real acceptance regressions

The current hardening branch carries six permanent real-world regressions:

- `REAL-01` — premature/generic/toy-like B2B rendering;
- `REAL-02` — commercial/brand drift and real-asset truth;
- `REAL-03` — downstream asset gate blocked upstream strategy;
- `REAL-04` — text approval substituted for visual approval;
- `REAL-05` — missing production assets hid the visual concept;
- `REAL-06` — wrong commercial job + one weak internally-selected concept instead of genuine user-facing exploration.

See `evals/real-world-failures.json`.

## Current deterministic milestone

Branch: `dev/performance-banner-designer-v0.2`

Draft PR: `#2`

`main` remains unchanged.

**200 tests — OK.**

GitHub Actions run `34219191379` / #527 completed **SUCCESS** on `98e8313717082f6b78ed699ea822d1eaeba51a32` after REAL-06 hardening.

Deterministic CI proves contracts/tooling, not campaign performance, independent visual excellence, or actual Google approval.

## Next real acceptance

The next MITGROUP run must not reuse the stale implementation-service assumption or treat A2 as user-approved.

It must:

1. ask/resolve the exact Bitrix24 license commercial job;
2. resolve purchase vs renewal structure;
3. preserve the correct commercial job through strategy;
4. render three materially different 300x250 visual concepts because no direction is currently user-locked;
5. pre-review all three for basic visual quality before showing them;
6. let the user select/revise/approve one direction;
7. only then complete production assets, scale-out, technical QA and final Google policy preflight.

See `docs/v0.2-release-gate.md`.

## Future

v0.3: GIF/video/HTML5 + Remotion/Content Factory + motion-specific Google technical/policy validation after static v0.2 is proven.
