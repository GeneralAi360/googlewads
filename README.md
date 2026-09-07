# Google Ads Performance Banner Designer

A production-grade AI skill for researching, planning, designing, adapting, rendering, reviewing, validating, policy-preflighting, and iterating professional advertising banners for Google Ads.

The project intentionally treats banner creation as a **creative-production system**, not a single image prompt.

## Canonical pipeline

```text
BUSINESS CONTEXT
→ structured intake
→ run freeze + banner matrix
→ supplied-reference DNA
→ competitive creative research
→ category design map
→ IDEA_ARCHITECTURE
→ presentation mode
→ emotional target
→ VISUAL_CHARACTER
→ STYLE INTELLIGENCE
→ attention / typography strategy
→ PRE-RENDER GOOGLE POLICY RISK
→ LIGHTING_INTENT
→ detailed design brief
→ 3 written art directions when unresolved
→ written art-direction approval
→ representative asset readiness
→ optional HERO_GENERATION_SPEC
→ generation/select/refine when generation is used
→ one high-fidelity representative
→ representative approval
→ CAMPAIGN_DESIGN_SYSTEM
→ PREPRODUCTION_FROZEN
→ frozen creative contracts
→ one job per final output
→ exact format recomposition
→ deterministic render
→ Google technical preflight
→ manifest/contact sheet
→ actual/grayscale/squint/thumbnail QA
→ independent banner reviews
→ pack review
→ design readiness
→ FINAL GOOGLE ADS POLICY PREFLIGHT
→ exact-SHA policy pack aggregation
→ GOOGLE_READY_PRECHECK
→ delivery
→ performance learning
```

The full pack is deliberately not rendered before one representative design proves the idea, visual character, style strategy, lighting behavior, and professional quality.

## Current development

Branch: `dev/performance-banner-designer-v0.2`

Draft PR: `#2`.

`main` remains unchanged.

## Real acceptance failures that changed the system

### REAL-01

The first Work acceptance test created three technically valid but weak B2B 300x250 previews before sufficient market/category research. The directions shared nearly the same template and used toy-like/generic cloud imagery.

Permanent requirements:
- research before unresolved design;
- category map before art direction;
- three written directions before images;
- one high-fidelity representative before scale-out;
- explicit asset/category/anti-generic-AI quality gates.

### REAL-02

The next Work run produced a much stronger product-reality direction but still allowed art direction to introduce an unapproved CTA and ambiguous brand naming while correctly recognizing the need for real Bitrix24 UI.

Permanent requirements:
- `commercial_lock`;
- `brand_identity_lock`;
- `required_assets`;
- `representative-asset-manifest.json`;
- fail-closed `NEEDS_ASSET`;
- creative-freeze enforcement of approved CTA/proposition/brand identity.

Both cases live in `evals/real-world-failures.json`.

## Meaning before style

The user-supplied visual-methodology presentation added a semantic design layer. Its ideas are treated as **production heuristics**, not performance laws.

`references/idea-architecture-visual-character.md` formalizes `IDEA_ARCHITECTURE`, presentation mode, emotional target, visual character, focus budget, forbidden visuals, Creative Chaos Audit, generation-is-not-final workflow and campaign design-system thinking.

## Style Intelligence — September 2026

Style is modeled as a strategy above the individual banner rather than a rigid preset or fashionable label.

Implemented machine-readable layer:
- `config/style-intelligence-library.json`;
- `references/style-intelligence-2026.md`;
- style context/recommendation/gate schemas;
- `scripts/recommend_visual_styles.py`;
- `scripts/validate_style_strategy_gate.py`.

A style strategy combines foundation grammar, optional contemporary overlay, execution language, attention profile, typography profile, lighting affinity and format resilience.

The recommender produces `SAFE_STRONG`, `CURRENT_DIFFERENTIATED`, and `CONTROLLED_WILDCARD`. Trend/currentness influence is capped at 5%, stale trend data disables currentness, and wildcard remains inside the requested disruption corridor.

The selected strategy/recommendation SHA/components are frozen through art direction and campaign design system. Style drift is fail-closed.

## Attention and typography

Style selection includes an explicit intended scan path / salience plan rather than assuming a universal Z-pattern or CTA position.

Typography is role-based rather than fashion-selected. Actual font files require runtime verification for license, local availability, language/script, Cyrillic/Belarusian quality when applicable, weights/widths, exact raster readability and micro-format behavior.

No font family is presented as universally higher-converting.

## Lighting is connected to meaning and style

```text
CORE IDEA
→ PRESENTATION MODE
→ EMOTIONAL TARGET
→ VISUAL CHARACTER
→ STYLE STRATEGY
→ PRIMARY AOI
→ LIGHTING INTENT
→ SCENE LIGHTING / COMPOSITION LIGHTING
```

The 30 practical lighting schemes are candidate vocabulary inside `LIGHTING_INTENT`, not an independent style picker.

For truthful product-UI proof, scene lighting may be `NOT_APPLICABLE`; fake neon/photorender relighting is prohibited by default and real product colors remain truthful.

## Generated hero and asset truth

Generated/HYBRID heroes use a structured `hero-generation-spec.json`. Critical text/logo remain deterministic whenever possible. Generation is a draft/source stage rather than a final banner.

Real identity/product assets are validated through `representative-asset-manifest.json` and `validate_representative_assets.py`; missing required real UI/logo returns `NEEDS_ASSET`.

## One representative before scale-out

One high-fidelity representative must pass semantic/style/lighting/asset/category/hierarchy/type/brand/message/crop/CTA/anti-generic-AI checks before full production.

After representative approval, `campaign-design-system.json` freezes reusable campaign grammar rather than a master canvas to resize.

## Google technical preflight

The deterministic renderer owns exact approved copy/logo/fonts/layout/crop/dimensions/compression and composition lighting. Formats are recomposed per layout family rather than resized from a master canvas.

**Technical Google PASS is not design PASS and is not Google policy PASS.**

## Visual QA and independent review

Diagnostic views include actual, grayscale, squint/blur and 25% thumbnail. Individual and pack reviewers check semantic/style/design-system/lighting/brand/category/asset/hierarchy/type/crop/contrast/CTA consistency.

## Google Ads Policy Preflight — September 7 2026

The repository includes a separate policy layer based on current official Google Advertising Policies. It reduces disapproval risk but does not guarantee moderation approval.

Implemented:
- `references/google-ads-policy-preflight.md`;
- `config/google-ads-policy-snapshot.json`;
- `schemas/google-policy-context.schema.json`;
- `schemas/google-policy-report.schema.json`;
- `scripts/validate_google_policy.py`;
- `scripts/aggregate_google_policy_reports.py`;
- `scripts/assess_google_ready.py`.

### Two policy stages

**Pre-render policy risk** resolves vertical/geography, material claims/qualifiers, third-party trademark/affiliation state, destination support, certification/targeting concerns and obviously incompatible misleading-design devices before production.

**Final exact-artifact policy preflight** combines:

`EXACT FINAL BANNER + EXACT COPY + ADVERTISER IDENTITY + CLAIM EVIDENCE + LANDING PAGE + TRADEMARK CONTEXT + VERTICAL/GEO/TARGETING CONTEXT + GOOGLE_POLICY_REVIEWER`

Checks include final artifact SHA/dimensions/format, transparent background, image quality/legibility, misleading system/dialog/menu imitation, non-functional controls, download/install UI, pseudo-interactions, segmented/multi-ad appearance, contextless/disproportionate buttons, advertiser identity/affiliation, material claims, destination relevance/offer/CTA availability, URL/crawlability/accessibility/original-content evidence, trademark context, restricted vertical/certification/targeting and AI disclosure-review state when applicable.

Policy statuses:
- `GOOGLE_POLICY_PREFLIGHT_PASS`;
- `GOOGLE_POLICY_PREFLIGHT_BLOCKED`;
- `GOOGLE_POLICY_PREFLIGHT_INCOMPLETE`;
- `POLICY_REVIEW_REQUIRED`.

Every policy review is bound to the exact final artifact SHA. Pack aggregation fails on missing/stale reports.

Final local status is `GOOGLE_READY_PRECHECK_PASS` only when design/readiness and policy preflight both pass.

Even then:

`google_upload_approval_guaranteed = false`

Google may still review ad, destination, account, advertiser verification, campaign settings, targeting, geography and third-party information.

## Verified deterministic milestone

- full unittest suite: **157 tests, OK**;
- canonical Style Intelligence + Google Policy `SKILL.md` head: GitHub Actions **PASS**.

Deterministic CI proves tooling/contracts, not independent visual judgment, campaign performance or final Google approval.

## Next acceptance step

Continue the real MITGROUP Work task using the latest meaning/style/policy/lighting pipeline, then run exact-artifact policy preflight against the real landing page and Bitrix24 advertiser/trademark relationship. Require policy pack PASS before a Google-ready delivery claim.

The user's next banner-style examples will expand reusable style/reference vocabulary only when they add actual system value.

See `docs/ROADMAP.md` and `docs/v0.2-release-gate.md`.

## Future

v0.3 remains reserved for motion creative: GIF/video/HTML5 architecture, Remotion and Content Factory integration, including motion-specific technical and Google policy validation, after static v0.2 is proven.
