# Idea architecture, visual character, and lighting linkage

## Source status

This reference is adapted from the user-supplied 38-page presentation **«ВИЗУАЛ И УПАКОВКА»**. The presentation is a practitioner methodology for visual concept development, prompting, selection, refinement, and packaging. Treat its claims as **PRODUCTION HEURISTICS / creative vocabulary**, not as scientific proof of CTR/CVR lift.

The strongest transferable sequence is:

`TASK -> IDEA -> PRESENTATION -> EMOTION -> VISUAL CHARACTER -> LIGHTING INTENT -> PROMPT/ASSET PLAN -> GENERATE/SELECT -> REFINE -> ADAPT -> FINAL`

The system must not jump from a business brief directly to a generated image.

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

Examples include control, trust, relief, ambition, urgency, energy, curiosity, status, warmth, tension, playfulness. These are not performance laws.

The emotional target should constrain:
- visual character;
- lighting;
- color;
- typography;
- crop and subject treatment;
- disruption level.

Example: an enterprise CRM direction whose target is `CONTROL + TRUST` should not silently drift into playful toy lighting, chaotic neon, or ironic mascot treatment.

## 3. VISUAL_CHARACTER

Style names are tools, not goals. Record a visual-character signature so art-direction candidates differ structurally rather than by palette only.

Use two advisory axes inspired by the presentation's character matrix:

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

Suggested initial character families, deliberately open for later extension with the user's banner-style examples:
- clean / commercial;
- bright / viral;
- artistic / atmospheric;
- technological / futuristic;
- factual / characterful.

Do not freeze a 31-style list as eternal truth. New style examples may extend the vocabulary without changing the underlying character coordinates.

## 4. FOCUS_BUDGET

Adapt the presentation's practical “one” rule as a **PRODUCTION HEURISTIC**, not a universal law.

Default planning budget:
- one primary idea;
- one primary hero/focal object;
- one primary emotion;
- one primary visual language;
- a small number of accent details.

The schema allows deviations, but deviations require a rationale. Complex concepts are allowed; accidental complexity is not.

Small formats should normally be stricter than large formats.

## 5. CREATIVE_CHAOS_AUDIT

Before art-direction approval, audit the strategy for the failure patterns emphasized by the presentation:
- core idea unclear;
- trying to fit everything into one banner;
- mixed visual languages without purpose;
- forbidden list missing/ignored;
- no platform/aspect-ratio adaptation plan;
- composition not deliberately controlled;
- first generation treated as final.

The audit proves process completeness, not aesthetic quality or advertising performance.

## 6. FORBIDDEN_VISUALS

Maintain three layers:

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

These lists are controller-owned constraints.

## 7. LIGHTING_INTENT — connect meaning to light

Lighting must be derived from the idea architecture, emotional target, visual character, material/asset type, primary AOI, and copy-safe requirements.

Do **not** choose a lighting scheme because it is visually impressive in isolation.

A lighting intent must answer:
- What role does light play in the core idea?
- Which AOI should it support?
- Which emotion should it reinforce?
- Does the hero require real scene lighting, composition lighting, both, or neither?
- Which lighting schemes are candidate heuristics and why?
- What lighting behaviors are forbidden because they would contradict the concept?

### Scene-lighting modes
- `REQUIRED` — the photographed/generated scene needs an explicit scheme;
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

Use these as hierarchy tools, not decoration presets.

### Lighting alignment examples

#### Product proof / real UI
- scene lighting may be `NOT_APPLICABLE`;
- composition lighting should usually be restrained;
- no fake glow implying a fabricated UI surface;
- preserve truthful product colors;
- use tonal separation/keyline/shadow only if needed for hierarchy.

#### Premium physical product
- scene lighting may carry material definition and status;
- candidate schemes may come from the 30-scheme lighting library;
- strongest highlight must not destroy label/readability or copy-safe space.

#### Pain visualization
- contrast/shadow may support tension;
- it must still preserve the commercial message and not become theatrical noise.

#### Clean commercial
- high-key/soft wraparound/controlled neutral light may fit;
- do not infer that high-key converts better.

## 8. HERO GENERATION SPEC

When a hero is generated, generation receives a structured spec rather than a loose prompt:

`FORMAT + SUBJECT + STATE/ACTION + ENVIRONMENT + COMPOSITION + CAMERA/CROP + LIGHTING + VISUAL CHARACTER + EMOTION + DETAILS + FORBIDDEN ELEMENTS`

Critical text, CTA, legal copy, and logos remain deterministic whenever possible.

A generated asset is a source/hero candidate, not a finished banner.

## 9. GENERATION IS NOT FINAL

Use the presentation's iterative logic:

`RAW GENERATION -> SELECT -> REMOVE EXCESS -> COMPOSITION REFINEMENT -> DETERMINISTIC TYPE/BRAND/CTA -> QUALITY PASS -> REPRESENTATIVE REVIEW`

Do not treat first generation as final output.

## 10. CAMPAIGN DESIGN SYSTEM AFTER REPRESENTATIVE APPROVAL

After one high-fidelity representative passes, freeze the design grammar before scale-out.

The campaign design system should preserve:
- idea architecture;
- visual-character signature;
- art-direction identity;
- hierarchy intent;
- grid/alignment logic;
- headline/offer/CTA behavior;
- brand-anchor behavior;
- hero/crop language;
- background/accent system;
- lighting intent and allowed lighting behavior;
- whitespace character;
- format-adaptation rules;
- forbidden patterns.

Workers adapt composition per layout family while remaining inside this system.

The representative is evidence of the system, not a master canvas to resize.
