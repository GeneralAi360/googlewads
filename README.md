# Google Ads Performance Banner Designer

A production-grade AI skill for researching, planning, designing, adapting, rendering, reviewing, validating, policy-preflighting, and iterating professional advertising banners for Google Ads.

The project treats banner creation as a **creative-production system**, not a single image prompt.

## Canonical pipeline

```text
BUSINESS CONTEXT
→ structured intake / frozen output matrix
→ references + competitive/category research
→ IDEA_ARCHITECTURE / presentation / emotion
→ VISUAL_CHARACTER
→ STYLE INTELLIGENCE
→ attention + typography strategy
→ PRE-RENDER GOOGLE POLICY RISK
→ LIGHTING_INTENT
→ commercial / brand / asset locks
→ written art direction
→ asset readiness
→ one high-fidelity representative
→ representative approval
→ CAMPAIGN_DESIGN_SYSTEM
→ PREPRODUCTION_FROZEN / creative freeze
→ one job per output / exact recomposition
→ deterministic render
→ GOOGLE TECHNICAL PREFLIGHT
→ visual diagnostics + independent design review
→ FINAL GOOGLE ADS POLICY PREFLIGHT
→ exact-SHA policy pack aggregation
→ GOOGLE_READY_PRECHECK
→ delivery / performance learning
```

The full pack is never scaled out before one representative proves the design system.

## Current development

- Branch: `dev/performance-banner-designer-v0.2`
- Draft PR: `#2`
- `main` remains unchanged.

## Real acceptance regressions

`REAL-01` captured premature rendering, nearly identical directions and generic/toy-like B2B imagery before market/category research.

`REAL-02` captured a stronger product-reality direction that still drifted into an unapproved CTA and ambiguous brand identity while correctly demanding real product UI.

These failures produced permanent research-first, commercial/brand-lock, real-asset and representative-approval gates.

## Meaning / Style / Attention / Typography / Lighting

The skill resolves meaning before style. Style Intelligence is a controller layer above the banner: foundation grammar + optional contemporary overlay + execution language + attention profile + typography profile + lighting affinity + format resilience.

It returns `SAFE_STRONG`, `CURRENT_DIFFERENTIATED`, and `CONTROLLED_WILDCARD`. Trend/currentness is capped at 5%, disabled when stale, and cannot override category fit, product truth, attention, typography, lighting or multi-format resilience.

Attention uses an intended scan path/salience plan, not a universal Z-pattern. Typography is role-based and actual fonts require runtime license/file/script/Cyrillic/Belarusian/weight/width/raster verification where applicable.

Lighting follows:

`IDEA → PRESENTATION → EMOTION → VISUAL CHARACTER → STYLE STRATEGY → PRIMARY AOI → LIGHTING INTENT`

The 30 lighting schemes are candidate vocabulary, not a free-standing style picker. Real UI can make scene lighting `NOT_APPLICABLE`.

## Asset truth / representative / campaign system

Identity/product-specific assets use explicit requirements and fail-closed `NEEDS_ASSET`. Generated critical logo/UI substitutes are forbidden where real assets are required.

Only one near-production representative is rendered first. After approval, `campaign-design-system.json` freezes reusable design grammar. Other aspect ratios recompose rather than resize.

## Google technical preflight != Google policy preflight

Technical validation checks things such as exact dimensions, file format/bytes and static state. It does not prove advertising-policy compliance.

The repository therefore has a separate Google Ads Policy layer:
- `references/google-ads-policy-preflight.md`
- `config/google-ads-policy-snapshot.json`
- `schemas/google-policy-context.schema.json`
- `schemas/google-policy-report.schema.json`
- `scripts/validate_google_policy.py`
- `scripts/aggregate_google_policy_reports.py`
- `scripts/assess_google_ready.py`

### Pre-render Google policy risk

Before art direction, resolve product/vertical, target geography, material claims/qualifiers, third-party trademark/affiliation, destination support, certification/targeting concerns and obvious misleading-design exclusions.

### Final exact-artifact policy preflight

Each final banner review is bound to exact output SHA and combines:

`FINAL BANNER + EXACT COPY + ADVERTISER IDENTITY + CLAIM EVIDENCE + LANDING PAGE + TRADEMARK CONTEXT + VERTICAL/GEO/TARGETING CONTEXT + GOOGLE_POLICY_REVIEWER`

It screens image quality/legibility and current misleading-design issues such as fake system/dialog UI, non-functional controls, download/install UI, pseudo-interactions, transparent background, segmented/multi-ad appearance and contextless/disproportionate buttons.

Material claims require verified evidence and destination support. Advertised offer/CTA must be available/easy to find at the destination. Destination working/domain/crawlability/accessibility/identity/original-content evidence is tracked separately.

Trademark/affiliation and restricted verticals are contextual: unresolved evidence returns review-required instead of invented authorization.

Policy states:
- `GOOGLE_POLICY_PREFLIGHT_PASS`
- `GOOGLE_POLICY_PREFLIGHT_BLOCKED`
- `GOOGLE_POLICY_PREFLIGHT_INCOMPLETE`
- `POLICY_REVIEW_REQUIRED`

Pack policy aggregation requires exact-SHA PASS for every final artifact.

`GOOGLE_READY_PRECHECK_PASS` requires both ordinary design/readiness and policy PASS.

It always carries:

`google_upload_approval_guaranteed = false`

because final Google review may also depend on destination, account, advertiser verification, campaign settings, targeting, geography and third-party information.

## Verified deterministic milestone

**157 tests — OK**.

Canonical Style Intelligence + Google Policy `SKILL.md` head has GitHub Actions **PASS**.

Deterministic CI proves tooling/contracts, not independent visual judgment, campaign performance or actual Google approval.

## Next acceptance

Continue the real MITGROUP Work run through real assets → style/policy-risk/lighting → one representative → campaign system → full pack → exact-artifact Google policy preflight against the real landing page and Bitrix24 advertiser/trademark context.

Do not call the pack Google-ready until policy pack aggregation and final local Google-ready precheck pass.

See `docs/ROADMAP.md` and `docs/v0.2-release-gate.md`.

## Future

v0.3: GIF/video/HTML5 + Remotion/Content Factory + motion-specific Google technical/policy validation after static v0.2 is proven.
