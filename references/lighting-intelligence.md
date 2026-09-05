# Lighting Intelligence for Performance Banners

## Source and evidence status

This module is derived from the user-supplied PDF **"СВЕТ — 30 схем освещения"** by `@mama_mozg` and is now explicitly linked to the idea/visual-character methodology in `references/idea-architecture-visual-character.md`.

The lighting source presents 30 practical prompt patterns for commercial product photography and argues that scene lighting, camera/lens/aperture cues, object position, reflections, framing, and small physical imperfections make generated images feel more photographic.

Treat the 30 schemes as **PRODUCTION HEURISTICS / creative vocabulary**, not as scientific proof that one lighting setup increases CTR or conversions.

The exact structured catalog lives in `config/lighting-schemes.json`.

## Lighting is downstream of meaning

Do **not** pick a lighting scheme directly from the product category or because the setup looks dramatic.

The canonical dependency is:

`CORE IDEA -> PRESENTATION MODE -> EMOTIONAL TARGET -> VISUAL CHARACTER -> PRIMARY AOI -> LIGHTING INTENT -> SCENE/COMPOSITION LIGHTING`

Before a scheme or deterministic lighting primitive is selected, the design brief must resolve:
- `idea_architecture`;
- `presentation_mode`;
- primary/secondary emotional target and avoided tone;
- `visual_character` signature;
- primary AOI and intended scan path;
- copy-safe requirements;
- `lighting_intent`.

The 30-scheme catalog is therefore a **candidate vocabulary inside `LIGHTING_INTENT`**, not a menu the worker may browse independently.

### Lighting intent contract

`lighting_intent` answers:
1. What role does light play in the core idea?
2. Which AOI should light support?
3. Which emotional target should it reinforce?
4. How does it fit the approved visual character?
5. Is physical/scene lighting required, optional, or not applicable?
6. Is deterministic composition lighting required, optional, or not applicable?
7. Which scheme IDs/primitives are allowed?
8. What lighting behavior is explicitly forbidden?

The art direction must inherit the exact `lighting_intent_id`. The campaign design system then freezes its cross-size lighting behavior. Banner workers may adapt the implementation to the aspect ratio, but they may not invent a new lighting character.

### Real product/UI special case

When the hero is a truthful flat interface screenshot or another identity-critical real asset:
- `SCENE_LIGHTING` may be `NOT_APPLICABLE`;
- no fake neon, photographic relighting, or generated glow may imply that the interface itself has changed;
- preserve real product colors;
- use only restrained `COMPOSITION_LIGHTING` when needed for separation/readability;
- keyline, matte underlay, small contact shadow, local scrim, or tonal separation may be more truthful than a dramatic spotlight.

For a `PRODUCT_PROOF` concept, truthful product evidence outranks lighting spectacle.

### Emotion-to-light alignment

This is a design heuristic, not a performance law.

Examples:
- `CONTROL / TRUST` -> coherent, restrained, predictable separation; avoid chaotic neon or theatrical hotspots unless the brand explicitly requires them;
- `PREMIUM / STATUS` -> deliberate material definition, controlled reflections, dark-field/rim/low-key candidates where appropriate;
- `WARMTH / RELIEF` -> soft directional/window/golden-hour candidates where the actual context supports them;
- `ENERGY / TENSION` -> hard light, bold shadow, duotone or higher contrast may be candidates, but only if the message remains readable;
- `CURIOSITY` -> selective reveal or directional contrast may help, but should not obscure the proposition.

A mismatch between emotional target and lighting intent is a preproduction failure, not something a renderer should improvise around.

## What should be integrated into banner production

The useful idea is broader than "pick a pretty light preset."

Lighting is part of the attention system.

A banner can use light to:
- establish the primary focal object;
- separate a product/person from the background;
- create depth and perceived material quality;
- create or protect a copy-safe zone;
- turn a shadow, beam, rim, reflection, or brightness gradient into a directional cue;
- support category expectations when those expectations match the approved idea/character;
- reduce visual clutter by letting low-priority regions fall quieter;
- reinforce accepted reference DNA.

Do not use lighting to compensate for unclear messaging or broken typography.

## Two lighting layers

### 1. SCENE_LIGHTING

Light that belongs inside the hero image itself.

Examples:
- three-point lighting on a product;
- rim light around perfume;
- window light on a lifestyle scene;
- backlight through a glass bottle;
- hard shadow cast by a product;
- neon reflections on a device.

This layer should be planned before or during image generation/photography.

`scene_lighting.mode` is one of:
- `REQUIRED`;
- `OPTIONAL`;
- `NOT_APPLICABLE`.

If `REQUIRED`, at least one candidate scheme from the 30-scheme library must be justified. If `NOT_APPLICABLE`, do not attach a fake scene-lighting scheme.

### 2. COMPOSITION_LIGHTING

Restrained tonal shaping added during deterministic banner composition.

Examples:
- a soft radial spotlight behind the product;
- a subtle vignette that reduces background competition;
- a directional dark-to-light gradient/scrim that protects copy;
- a local glow behind a dark product edge;
- a soft tonal plate behind headline text;
- slight darkening of a noisy photographic region.

Current deterministic primitives:
- `hero_edge_glow`;
- `spotlight`;
- `copy_scrim`;
- `vignette`;
- `text_plate`.

The design brief whitelists primitives through `lighting_intent`. `campaign-design-system.json` may narrow that set, never expand it.

This layer is not permission to paint random effects over the banner. It must remain subordinate to the idea, emotion, visual character, brand, and primary AOI.

## Attention rules

### Brightest point

The brightest point often attracts attention, but brightness competes with size, contrast, faces, saturated color, sharp edges, text scale, and motion.

Therefore do not assume "brightest = guaranteed first fixation."

Use brightness as one cue in a coordinated hierarchy.

### Rim and separation

Rim/back light is especially useful when:
- product and background have similar luminance;
- the approved concept requires premium/dark presentation;
- the product silhouette matters.

Do not over-rim every edge until the product looks synthetic.

### Shadow as vector

A long hard shadow, blinds pattern, or directional beam can function like a visual arrow.

Use it deliberately:
- toward product/offer/CTA when it supports the intended scan path;
- away from copy if it would create texture behind small text.

Do not let a dramatic shadow become more salient than the offer.

### Copy-safe zone

A copy-safe region should have:
- controlled luminance;
- low local texture;
- no strong specular hotspot;
- no striped/sharp shadow through letters;
- adequate contrast for the exact type size;
- enough negative space around the text block.

A source image may be beautiful and still be unusable for a banner if there is nowhere to place readable copy.

### Faces and gaze

When a person is present:
- light the face enough to preserve expression;
- do not create a facial hotspot that defeats the intended product/offer hierarchy;
- if gaze direction is used as an attention cue, lighting should support rather than contradict it.

### CTA

Do not automatically make the CTA the brightest element.

The CTA needs local separation and discoverability, but the overall scan path may be `hero -> offer -> CTA -> brand`.

A glowing CTA can look cheap or fake if the brand/visual character does not support it.

## Material-aware lighting

### Transparent glass / liquid

Prefer as candidates:
- backlit glass;
- bright field;
- dark field;
- linear gradients;
- controlled black cards/edge definition;
- splash freeze for dynamic beverage/beauty concepts.

Watch for unreadable labels, fake refraction, blown highlights, and reflections behind text.

### Glossy bottle / cosmetics

Prefer as candidates:
- butterfly beauty;
- soft wraparound;
- linear gradient;
- three-point hero;
- reflective floor luxury.

Watch for excessive synthetic gloss, label glare, and uncontrolled mirrored text/graphics.

### Metal / jewelry / watches

Prefer as candidates:
- rim on black;
- low-key luxury;
- light tent macro;
- reflective floor;
- controlled strip reflections.

Watch for clipped metallic highlights, fake chrome, and distracting edge sparkle.

### Matte packaging

Prefer as candidates:
- high-key clean;
- soft wraparound;
- overcast;
- three-point hero;
- hard-light graphic setups for bold brands.

Watch for lighting that erases texture/shape or makes package and background merge.

### Technology / gadgets

Possible candidates include:
- underlit glow;
- gel duotone;
- blue hour;
- neon practical;
- rim on black;
- hard light for graphic campaigns.

But `technology` alone never authorizes cyberpunk. A clean factual enterprise-tech character may explicitly forbid neon/colored reflections.

### Food / natural / wellness

Possible candidates include:
- window light;
- golden hour;
- overcast;
- dappled botanical;
- candlelight for intimate/winter contexts;
- flat lay.

Watch for muddy color casts, artificial gloss, and props becoming primary AOIs.

## Scheme families from the supplied PDF

### Studio and classic — 1 to 7
1. Three-point hero
2. Rembrandt
3. Split light
4. Butterfly beauty
5. Rim on black
6. High-key clean
7. Low-key luxury

### Character and art — 8 to 10
8. Chiaroscuro
9. Hard light / bold shadow
10. Soft wraparound

### Glass, liquid, reflections — 11 to 19
11. Backlit glass
12. Dark field glass
13. Bright field glass
14. Linear gradient bottle
15. Underlit glow base
16. Splash freeze
17. Gel duotone
18. Window blinds shadow
19. Light tent macro

### Natural light and atmosphere — 20 to 28
20. Golden hour
21. Blue hour
22. Window light lifestyle
23. Harsh noon editorial
24. Overcast soft daylight
25. Volumetric god rays
26. Neon practical
27. Candlelight intimate
28. Dappled botanical

### Composition and angle — 29 to 30
29. Flat lay top-down
30. Reflective floor luxury

The last two are not purely lighting schemes. They combine viewpoint/composition with light and should be treated accordingly.

## Selection procedure

For each concept:

1. Read the frozen `IDEA_ARCHITECTURE`.
2. Read presentation mode and primary emotional target.
3. Read the visual-character signature and avoided tones.
4. Identify primary AOI and intended scan path.
5. Identify product material / asset truth requirements.
6. Identify copy-safe requirement for the layout family.
7. Read relevant reference-lighting DNA.
8. Decide whether scene light is `REQUIRED`, `OPTIONAL`, or `NOT_APPLICABLE`.
9. Exclude schemes that conflict with idea, emotion, character, material, brand, or truthfulness.
10. If applicable, select a small candidate set from the 30-scheme library and explain why.
11. Decide whether composition lighting is needed and whitelist only the required primitives.
12. Record forbidden lighting behaviors.
13. Validate the selected representative at actual banner size.
14. Freeze cross-size behavior in `campaign-design-system.json`.

Do not generate all 30 schemes by default. Generating 30 lighting variations is only appropriate when the user explicitly wants a lighting exploration.

## Lighting choice by objective — secondary heuristic

Use this table **only after** idea/emotion/visual-character filtering.

| Goal / mood | Strong starting candidates |
|---|---|
| clean e-commerce | 1, 6, 10, 13, 19, 24 |
| premium/luxury | 2, 5, 7, 8, 12, 14, 30 |
| beauty/cosmetics | 4, 10, 14, 17, 28, 30 |
| transparent bottle/liquid | 11, 12, 13, 14, 16 |
| technology | 5, 15, 17, 21, 26 |
| bold/editorial | 3, 9, 18, 23, 25 |
| warm lifestyle | 20, 22, 27 |
| natural/wellness | 22, 24, 28, 29 |
| dynamic/fresh | 9, 16, 17, 20 |
| macro/detail | 19, 14, 5 |

This is not a performance ranking.

## Banner-family considerations

### Micro horizontal
Avoid complex lighting texture. Strong priorities: one clean hero silhouette, simple background, predictable copy-safe region, and no striped/god-ray texture behind text.

### Leaderboard
Directional light and horizontal shadow/reflection can reinforce the horizontal scan path. Reserve a clean text strip.

### Rectangle
Most flexible family; can support stronger hero photography, controlled light falloff, foreground/background depth, and more expressive lighting when the campaign system allows it.

### Narrow vertical
Use vertical structures where relevant: rim, top-down spotlight, underglow, vertical reflection, controlled gradient. Avoid wide cinematic scenes that collapse when cropped.

### Large vertical
Can support more atmosphere but still needs a dominant focal region.

### Billboard
Wide negative space is valuable. A hero can occupy one side while a light gradient/scrim protects copy on the other.

## Generative prompt guidance

The supplied lighting PDF includes camera, lens, aperture, angle, and imperfection cues in each prompt.

Retain them when they help define the intended photographic look, but treat them as descriptive controls, not guarantees of physically exact optics.

The most important invariant is:

`idea + emotion + visual character + material + light source + direction + softness + contrast + reflections/shadows + camera angle + copy-safe composition + realistic texture`

When generation is used, create `hero-generation-spec.json`. Critical text and logos remain outside generated imagery.

## QA checklist

Before accepting a lighting treatment:
- [ ] It matches the frozen `lighting_intent_id`.
- [ ] It supports the core idea rather than inventing a new one.
- [ ] It reinforces the primary emotional target and avoids forbidden tone.
- [ ] It matches the approved visual character.
- [ ] Primary AOI is clearer, not weaker.
- [ ] Product/person remains recognizable and truthful.
- [ ] Material reads plausibly.
- [ ] Copy-safe region remains readable.
- [ ] No hotspot crosses essential small text.
- [ ] Shadow/reflection does not create a false focal point.
- [ ] Lighting direction is internally coherent.
- [ ] Background light does not flatten logo/CTA contrast.
- [ ] Color cast respects brand/product color.
- [ ] The result works at actual banner size.
- [ ] Cross-size implementations remain inside the frozen campaign lighting system.
