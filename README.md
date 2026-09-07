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

`references/idea-architecture-visual-character.md` formalizes:
- `IDEA_ARCHITECTURE`;
- presentation mode;
- emotional target;
- visual-character signature;
- focus budget;
- forbidden visuals;
- Creative Chaos Audit;
- generation-is-not-final workflow;
- campaign design system after representative approval.

A design brief explicitly answers what the visual means, what single takeaway should remain after a glance, how the idea is presented, which emotion/state it should create, what creative tension makes the concept non-generic, and why this mechanism fits the communication problem.

## Style Intelligence — September 2026

Style is modeled as a strategy above the individual banner rather than a rigid preset or fashionable label.

Machine-readable layer:
- `config/style-intelligence-library.json`;
- `references/style-intelligence-2026.md`;
- `schemas/style-strategy-context.schema.json`;
- `schemas/style-strategy-recommendation.schema.json`;
- `schemas/style-strategy-gate.schema.json`;
- `scripts/recommend_visual_styles.py`;
- `scripts/validate_style_strategy_gate.py`.

A style strategy combines:
- foundation grammar;
- optional contemporary overlay;
- execution language;
- attention profile;
- typography profile;
- lighting affinity;
- format resilience.

The recommender produces three decision-support lanes:
- `SAFE_STRONG`;
- `CURRENT_DIFFERENTIATED`;
- `CONTROLLED_WILDCARD`.

Trend/currentness influence is deliberately capped at 5%. Currentness can break a tie between already suitable strategies; it cannot rescue a strategy that fails category trust, asset truth, attention, typography, lighting or multi-format resilience.

The wildcard stays inside the requested disruption corridor, so difference alone cannot justify an inappropriate visual character.

The selected style recommendation is SHA-bound into the art direction and campaign design system. Component drift is fail-closed.

## Attention and typography

Style selection includes an explicit attention plan / intended scan path rather than assuming one universal Z-pattern or CTA position.

Typography is role-based rather than selected by fashion alone. Candidate profiles include enterprise variable sans, editorial serif+sans, quiet-luxury serif, humanist sans, condensed promotional display, technical mono accent, controlled expressive display, soft-serif/human-trust and script-aware systems.

Actual font files still require runtime verification for license, local availability, language/script support, Cyrillic/Belarusian glyph quality when needed, real weights/widths, exact raster readability and micro-format behavior.

No font family is presented as universally higher-converting.

## Lighting is connected to meaning and style

`references/lighting-intelligence.md` contains the 30 practical lighting schemes, but the schemes are candidate vocabulary inside a semantic lighting contract rather than an independent style picker.

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

`LIGHTING_INTENT` records relationship to idea, primary AOI, emotional function, visual-character/style alignment, scene-lighting mode, candidate schemes when relevant, allowed composition primitives, copy-safe strategy, focal priority and forbidden lighting behavior.

For truthful product-UI proof, scene lighting may be `NOT_APPLICABLE`; fake neon/photorender relighting is prohibited by default and real product colors remain truthful.

## Structured Hero Generation

When `image_strategy.source_mode` is `GENERATED` or `HYBRID`, the system requires `hero-generation-spec.json` matching `schemas/hero-generation-spec.schema.json`.

Generation receives exact idea, style, emotion, composition, camera/crop, lighting and forbidden-element context. Critical copy and logo remain outside the generated hero whenever deterministic composition can own them.

Generation is a source/draft stage:

`RAW → SELECT → REMOVE EXCESS → REFINE → ADD EXACT TYPE/BRAND/CTA → QUALITY PASS`

## Commercial and brand locks

`commercial_lock` freezes proposition, approved CTA allowlist, product/version, proof and required qualifiers.

Art direction changes CTA treatment, not CTA wording.

`brand_identity_lock` freezes one canonical brand ID/display name plus explicitly approved aliases.

## Real asset readiness

`representative-asset-manifest.json` + `scripts/validate_representative_assets.py` verifies file existence, SHA, source type, dimensions, substitution policy, privacy review, rights approval and real-logo requirements.

Missing required real UI/logo/product asset returns `NEEDS_ASSET`.

## One representative before scale-out

One high-fidelity representative must PASS idea, emotion, style/character, lighting, asset/category, hierarchy/type, brand/message, crop, CTA and anti-generic-AI checks before scale-out.

After representative approval, `campaign-design-system.json` freezes reusable design grammar rather than a master canvas to resize.

## Google technical preflight

One final matrix row = one traceable banner job.

The deterministic renderer owns exact approved copy/logo/fonts/layout/crop/dimensions/compression and composition lighting. Formats are recomposed per layout family rather than resized from a master canvas.

`render_banner_pack.py` checks creative/design-system provenance and Google technical requirements before emitting the final manifest/contact sheet.

**Technical Google PASS is not design PASS and is not Google policy PASS.**

## Visual QA and independent review

Diagnostic views:
- actual;
- grayscale;
- squint/blur;
- 25% thumbnail.

Individual review checks idea, emotion, visual character/style, campaign design system, lighting intent, brand/category/assets, hierarchy/type/crop/contrast/CTA and anti-template quality.

Pack review checks those identities across sizes.

## Google Ads Policy Preflight — September 7 2026

The repository includes a separate policy layer based on current official Google Advertising Policies. It is designed to reduce disapproval risk, not to guarantee moderation approval.

Implemented:
- `references/google-ads-policy-preflight.md`;
- `config/google-ads-policy-snapshot.json`;
- `schemas/google-policy-context.schema.json`;
- `schemas/google-policy-report.schema.json`;
- `scripts/validate_google_policy.py`;
- `scripts/aggregate_google_policy_reports.py`;
- `scripts/assess_google_ready.py`.

### Two policy stages

**Pre-render policy risk** prevents expensive work on a concept that already contains unresolved restricted-vertical, affiliation, trademark, claim, destination or misleading-design risk.

**Final exact-artifact policy preflight** combines:

`EXACT FINAL BANNER + EXACT COPY + ADVERTISER IDENTITY + CLAIM EVIDENCE + LANDING PAGE + TRADEMARK CONTEXT + VERTICAL/GEO/TARGETING CONTEXT + GOOGLE_POLICY_REVIEWER`

Checks include:
- final artifact SHA/dimensions/format;
- transparent-background image-ad detection;
- image quality / essential text legibility;
- misleading system/site warning/dialog/menu imitation;
- non-functional controls;
- download/install UI in image ads;
- misleading arrows/pseudo-interaction;
- segmented/multi-ad appearance;
- contextless/disproportionate standalone button;
- advertiser identity / affiliation;
- material claim verification;
- destination relevance;
- advertised offer/CTA availability;
- destination working/domain/crawlability/accessibility/original-content evidence;
- trademark contextual review;
- restricted vertical/certification/targeting separation;
- AI-generated/edited disclosure/label review state when applicable.

Policy statuses:
- `GOOGLE_POLICY_PREFLIGHT_PASS`;
- `GOOGLE_POLICY_PREFLIGHT_BLOCKED`;
- `GOOGLE_POLICY_PREFLIGHT_INCOMPLETE`;
- `POLICY_REVIEW_REQUIRED`.

Every semantic policy review is bound to the exact final artifact SHA. Pack aggregation fails on missing/stale reports.

Final local status is `GOOGLE_READY_PRECHECK_PASS` only when design/readiness and policy preflight both pass.

Even then:

`google_upload_approval_guaranteed = false`

Google may still review ad, destination, account, advertiser verification, campaign settings, targeting, geography and third-party information.

## Verified deterministic milestone

- current full unittest suite: **157 tests, OK**;
- canonical Style Intelligence + Google Policy `SKILL.md` head: GitHub Actions **PASS**.

The suite includes Style Intelligence, real-UI truth, typography, lighting, policy, destination, claim, trademark and pack-policy aggregation regressions.

Deterministic CI proves tooling/contracts, not independent visual judgment, campaign performance or final Google approval.

## Next acceptance step

Continue the real MITGROUP Work task using the latest meaning/style/lighting/policy pipeline:
- resolve real assets and exact business/trademark relationship;
- produce one high-fidelity representative only after asset readiness;
- approve/freeze campaign design system;
- only then scale out;
- run Google policy preflight against the exact final creative(s), exact offer and real landing page;
- require policy pack PASS before a `Google-ready` delivery claim.

The user's next banner-style examples will be analyzed as reference/style evidence and used to expand reusable design vocabulary without becoming compulsory templates or unverified high-converting claims.

See `docs/ROADMAP.md` and `docs/v0.2-release-gate.md`.

## Future

v0.3 remains reserved for motion creative: GIF/video/HTML5 architecture, Remotion and Content Factory integration, including motion-specific technical and Google policy validation, after static v0.2 is proven.
