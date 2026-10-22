# Idea architecture, visual character, style intelligence, and lighting linkage

## Source status

This reference is adapted from the user-supplied 38-page presentation **«ВИЗУАЛ И УПАКОВКА»** and subsequent September 2026 style-library research.

The presentation is a practitioner methodology for visual concept development, prompting, selection, refinement, and packaging. Treat its claims as **PRODUCTION HEURISTICS / creative vocabulary**, not scientific proof of CTR/CVR lift.

Current style/trend sources are also **design/currentness signals**, not advertising-performance proof unless separately grounded by actual campaign metrics.

The canonical sequence is:

`TASK -> MARKET/CATEGORY EVIDENCE -> IDEA -> PRESENTATION -> EMOTION -> VISUAL CHARACTER -> STYLE INTELLIGENCE -> ATTENTION/TYPOGRAPHY -> LIGHTING INTENT -> ART DIRECTION -> ASSET PLAN -> GENERATE/SELECT/REFINE -> REPRESENTATIVE -> CAMPAIGN DESIGN SYSTEM -> ADAPT -> REVIEW`

The system must not jump from a business brief directly to a generated image or a trendy style name.

## 1. IDEA_ARCHITECTURE

Resolve the semantic visual idea before style.

Required questions:
- What is the **core idea** the banner should embody?
- What is the **single takeaway** a user should retain after a glance?
- What is the chosen **presentation mode** for expressing the idea?
- What primary **emotion/state** should the design create?
- What **creative tension** makes the idea meaningful rather than generic?
- Why is this visual strategy better suited to the business problem than obvious category clichés?

A strong idea is not the same as a headline and not the same as a style tag.

### Presentation modes

Use one primary mode and optionally one subordinate mode when needed:
- `PRODUCT_PROOF` — real product/UI/physical product is the proof;
- `OUTCOME_VISUALIZATION` — show the desired result;
- `PAIN_VISUALIZATION` — make the problem visible;
- `EXPLAINER` — explain a mechanism quickly;
- `BEFORE_AFTER` — show transformation;
- `WORKFLOW` — show a process/sequence;
- `HUMAN_CONTEXT` — product in a credible human/work context;
- `CHARACTER` — mascot/personification;
- `VISUAL_METAPHOR` — encode an abstract idea in an image;
- `VISUAL_PARADOX` — surprising but comprehensible contradiction;
- `EDITORIAL_STATEMENT` — typography/editorial composition carries the idea;
- `SOCIAL_PROOF` — testimonial/rating/case evidence is the hero;
- `PROMOTION_LED` — price/offer/promotion is the visual hero;
- `OTHER` — only with an explicit rationale.

Do not choose the mode because it is fashionable. Choose it because it solves the communication job.

## 2. EMOTIONAL_TARGET

Emotion is part of the design specification, not decoration added after composition.

Record:
- one primary emotional target;
- optional secondary targets;
- emotions/tones to avoid;
- intensity: `RESTRAINED`, `MODERATE`, or `HIGH`.

Examples include control, trust, relief, ambition, urgency, energy, curiosity, status, warmth, tension and playfulness. These are not performance laws.

The emotional target constrains:
- visual character;
- style-strategy ranking;
- lighting;
- color;
- typography;
- crop and subject treatment;
- disruption level.

Example: an enterprise CRM direction whose target is `CONTROL + TRUST` should not silently drift into playful toy lighting, chaotic neon, surreal comedy or ironic mascot treatment.

## 3. VISUAL_CHARACTER

Style names are tools, not goals. Record a visual-character signature so art-direction candidates differ structurally rather than by palette only.

Use two advisory axes:

### `order_to_virality`
- `0.0` = orderly / commercial / controlled;
- `1.0` = attention-first / expressive / viral.

### `aesthetics_to_innovation`
- `0.0` = aesthetic / metaphorical / atmospheric;
- `1.0` = innovative / future / technological.

Also record:
- `primary_character`;
- optional `secondary_character`;
- style tags;
- rationale.

Do not freeze a finite style list as eternal truth. New user examples and researched style libraries may extend the vocabulary without changing the underlying character coordinates.

## 4. STYLE_INTELLIGENCE — choose a visual strategy above the banner

Load:
- `references/style-intelligence-2026.md`;
- `config/style-intelligence-library.json`.

Style Intelligence exists between visual character and art direction. Its job is to answer:

> Given this idea, category, emotion, truth constraints, target attention path, typography needs, formats and lighting character, which visual systems are the strongest candidates now?

It must not answer:

> Which trendy style should we use?

### A style strategy is layered

A valid strategy combines:
1. foundation grammar;
2. optional contemporary overlay;
3. execution language;
4. attention profile;
5. typography profile;
6. lighting affinity;
7. format resilience.

Example:

`Product Reality / Systems + restrained 2026 editorial overlay + real UI macro-crop + product-proof attention + enterprise variable sans + truthful low-effect lighting`

This is actionable.

`Modern blue SaaS` is not.

### Runtime recommendation

Create `style-strategy-context.json` from already resolved strategy facts, then run:

```bash
python scripts/recommend_visual_styles.py \
  --context run/design/style-strategy-context.json \
  --library config/style-intelligence-library.json \
  --out run/design/style-strategy-recommendation.json
```

The system returns three materially different lanes:
- `SAFE_STRONG` — highest low-regret fit;
- `CURRENT_DIFFERENTIATED` — strong fit plus a subordinate current 2026 signal;
- `CONTROLLED_WILDCARD` — a more distinctive but still semantically compatible direction.

The wildcard must remain inside the requested disruption corridor. It is not permission to maximize difference for its own sake.

### Currentness is deliberately weak

Currentness is a tie-breaker, not the main score.

A current visual direction must be down-ranked if it:
- conflicts with brand/category trust;
- needs fake product imagery;
- breaks the intended attention hierarchy;
- requires unreadable typography;
- collapses in micro formats;
- contradicts emotional target;
- recreates a category cliché;
- produces generic AI polish without a brand-specific idea.

If the current-trend snapshot is stale, currentness contribution is disabled until refreshed.

### Style selection provenance

The written art direction must bind to the exact selected recommendation:
- `style_strategy_id`;
- lane;
- exact recommendation SHA;
- library snapshot date;
- foundation / overlay / execution / attention / typography component IDs.

Validate with:

```bash
python scripts/validate_style_strategy_gate.py \
  --recommendation run/design/style-strategy-recommendation.json \
  --art-direction-approval run/design/art-direction-approval.json \
  --out run/design/style-strategy-gate.json
```

After representative approval and `campaign-design-system.json`, rerun the gate with `--campaign-design-system` so the campaign grammar cannot silently switch style strategy.

Style recommendation is decision support. The approved art direction remains the creative decision.

## 5. ATTENTION IS PART OF STYLE SELECTION

A visual style is unsuitable if its attention behavior conflicts with the communication job.

Style Intelligence must return an attention profile containing:
- primary AOI;
- intended scan path;
- salience budget;
- subordinate elements;
- whether product/UI, offer, typography, face, proof, comparison or workflow should lead.

Use `references/visual-attention.md` for evidence boundaries.

Never reduce eye-tracking guidance to a universal Z-pattern, fixed CTA position or "center-left always wins" rule.

The recommended hierarchy must later survive:
- actual-size view;
- 25% glance/thumbnail;
- grayscale;
- squint/blur.

## 6. TYPOGRAPHY IS PART OF STYLE SELECTION

Style Intelligence recommends a **typographic role profile**, not a fashionable font name.

Resolve font source in this order:
1. approved brand font;
2. approved campaign/custom font;
3. selected style-intelligence typography profile;
4. verified production fallback.

Any named font candidate remains provisional until runtime verifies:
- license/usage rights;
- local font file availability for deterministic rendering;
- required language/script and glyph coverage;
- Cyrillic/Belarusian quality where required;
- weight/width availability;
- actual-size raster readability;
- width efficiency for small formats;
- compression behavior.

A distinctive display face may intentionally disappear in `320x50` if it cannot survive at a useful size. Campaign identity is preserved through role, hierarchy, color and graphic grammar rather than forced tiny display typography.

See `references/typography-color-contrast.md`.

## 7. FOCUS_BUDGET

Adapt the presentation's practical “one” rule as a **PRODUCTION HEURISTIC**, not a universal law.

Default planning budget:
- one primary idea;
- one primary hero/focal object;
- one primary emotion;
- one primary visual language;
- a small number of accent details.

The schema allows deviations, but deviations require rationale. Complex concepts are allowed; accidental complexity is not.

Small formats should normally be stricter than large formats.

## 8. CREATIVE_CHAOS_AUDIT

Before art-direction approval, audit:
- core idea unclear;
- trying to fit everything into one banner;
- mixed visual languages without purpose;
- style selected only because it is trendy;
- forbidden list missing/ignored;
- no platform/aspect-ratio adaptation plan;
- composition not deliberately controlled;
- attention profile contradicts primary message;
- typography role has no viable small-format plan;
- lighting does not support the idea;
- first generation treated as final.

The audit proves process completeness, not aesthetic quality or advertising performance.

## 9. FORBIDDEN_VISUALS

Maintain three layers.

### Global
Examples:
- fake logos;
- unreadable generated critical text;
- fabricated claims/metrics;
- generated substitutes where a real identity/product asset is required.

### Brand
Examples:
- unapproved colors;
- prohibited imagery;
- forbidden logo treatments.

### Concept
Examples:
- toy cloud;
- generic neural-network lines;
- stock-looking people;
- fake dashboard;
- glassmorphism;
- random neon glow.

These lists are controller-owned constraints and also influence style-strategy ranking.

## 10. LIGHTING_INTENT — connect meaning and style to light

Lighting must be derived from idea architecture, emotional target, selected style strategy, visual character, material/asset type, primary AOI and copy-safe requirements.

Do **not** choose a lighting scheme because it is visually impressive in isolation.

A lighting intent must answer:
- What role does light play in the core idea?
- Which AOI should it support?
- Which emotion should it reinforce?
- How should it align with the selected visual style strategy?
- Does the hero require real scene lighting, composition lighting, both, or neither?
- Which lighting schemes are candidate heuristics and why?
- What lighting behaviors are forbidden because they contradict the concept/style/truth requirement?

### Scene-lighting modes
- `REQUIRED` — photographed/generated scene needs an explicit scheme;
- `OPTIONAL` — a scheme may help but is not concept-critical;
- `NOT_APPLICABLE` — e.g. a flat real product UI screenshot where fake scene lighting would reduce truthfulness.

### Composition-lighting modes
- `REQUIRED`;
- `OPTIONAL`;
- `NOT_APPLICABLE`.

Allowed deterministic primitives currently include:
- `hero_edge_glow`;
- `spotlight`;
- `copy_scrim`;
- `vignette`;
- `text_plate`.

Use them as hierarchy tools, not decoration presets.

### Alignment examples

#### Product proof / real UI
- scene lighting may be `NOT_APPLICABLE`;
- composition lighting should usually be restrained;
- no fake glow implying fabricated UI material;
- preserve truthful product colors;
- use tonal separation/keyline/shadow only when needed for hierarchy.

#### Neo-minimal / quiet luxury physical product
- controlled scene light may carry material definition and status;
- soft wrap, rim, dark-field or low-key candidates may be appropriate depending on material;
- do not trade essential readability for atmosphere.

#### Human authentic
- natural/window/overcast treatments are strong starting heuristics when they preserve expression and context;
- do not convert a documentary concept into glossy stock aesthetics.

#### Bold poster
- scene lighting may be unnecessary;
- a hard graphic shadow or high-contrast product treatment may support the poster grammar;
- the lighting effect must remain subordinate to message/offer.

#### Controlled maximalism
- allow one expressive lighting/device relationship at most unless the approved direction explicitly budgets more;
- do not let every surface glow.

## 11. HERO GENERATION SPEC

When a hero is generated, generation receives a structured spec rather than a loose prompt:

`FORMAT + SUBJECT + STATE/ACTION + ENVIRONMENT + COMPOSITION + CAMERA/CROP + LIGHTING + VISUAL CHARACTER/STYLE STRATEGY + EMOTION + DETAILS + FORBIDDEN ELEMENTS`

Critical text, CTA, legal copy and logos remain deterministic whenever possible.

A generated asset is a source/hero candidate, not a finished banner.

## 12. GENERATION IS NOT FINAL

Use the iterative logic:

`RAW GENERATION -> SELECT -> REMOVE EXCESS -> COMPOSITION REFINEMENT -> DETERMINISTIC TYPE/BRAND/CTA -> QUALITY PASS -> REPRESENTATIVE REVIEW`

Do not treat first generation as final output.

## 13. CAMPAIGN DESIGN SYSTEM AFTER REPRESENTATIVE APPROVAL

After one high-fidelity representative passes, freeze design grammar before scale-out.

The campaign design system should preserve:
- idea architecture;
- selected style-strategy identity and exact recommendation SHA;
- visual-character signature;
- art-direction identity;
- attention/hierarchy intent;
- typography roles;
- grid/alignment logic;
- headline/offer/CTA behavior;
- brand-anchor behavior;
- hero/crop language;
- background/accent system;
- lighting intent and allowed lighting behavior;
- whitespace character;
- format-adaptation rules;
- forbidden patterns.

Run `validate_style_strategy_gate.py` again with the campaign system before scale-out.

Workers adapt composition per layout family while remaining inside this system.

The representative is evidence of the system, not a master canvas to resize.
