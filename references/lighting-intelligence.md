# Lighting Intelligence for Performance Banners

## Source and evidence status

This module is derived from the user-supplied PDF **"СВЕТ — 30 схем освещения"** by `@mama_mozg`.

The source presents 30 practical prompt patterns for commercial product photography and argues that scene lighting, camera/lens/aperture cues, object position, reflections, framing, and small physical imperfections make generated images feel more photographic.

Treat the 30 schemes as **PRODUCTION HEURISTICS / creative vocabulary**, not as scientific proof that one lighting setup increases CTR or conversions.

The exact structured catalog lives in `config/lighting-schemes.json`.

## What should be integrated into banner production

The useful idea is broader than "pick a pretty light preset."

Lighting is part of the attention system.

A banner can use light to:

- establish the primary focal object;
- separate a product/person from the background;
- create depth and perceived material quality;
- create or protect a copy-safe zone;
- turn a shadow, beam, rim, reflection, or brightness gradient into a directional cue;
- support category expectations: clean healthcare/e-commerce, dark luxury, warm lifestyle, high-energy tech, etc.;
- reduce visual clutter by letting low-priority regions fall quieter;
- reinforce the accepted reference DNA.

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

### 2. COMPOSITION_LIGHTING

Restrained tonal shaping added during deterministic banner composition.

Examples:
- a soft radial spotlight behind the product;
- a subtle vignette that reduces background competition;
- a directional dark-to-light gradient that protects copy;
- a local glow behind a dark product edge;
- a soft tonal plate behind headline text;
- slight darkening of a noisy photographic region.

This layer is not permission to paint random effects over the banner. It must remain subordinate to the concept and brand.

## Attention rules

### Brightest point

The brightest point often attracts attention, but brightness competes with:
- size;
- contrast;
- faces;
- saturated color;
- sharp edges;
- text scale;
- motion.

Therefore do not assume "brightest = guaranteed first fixation."

Use brightness as one cue in a coordinated hierarchy.

### Rim and separation

Rim/back light is especially useful when:
- product and background have similar luminance;
- the concept requires premium/dark presentation;
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

The CTA needs local separation and discoverability, but the overall scan path may be:
`hero -> offer -> CTA -> brand`.

A glowing CTA can look cheap or fake if the brand does not support it.

## Material-aware lighting

### Transparent glass / liquid

Prefer:
- backlit glass;
- bright field;
- dark field;
- linear gradients;
- controlled black cards/edge definition;
- splash freeze for dynamic beverage/beauty concepts.

Watch for:
- unreadable labels;
- fake refraction;
- blown highlights;
- reflections behind text.

### Glossy bottle / cosmetics

Prefer:
- butterfly beauty;
- soft wraparound;
- linear gradient;
- three-point hero;
- reflective floor luxury.

Watch for:
- excessive synthetic gloss;
- label glare;
- uncontrolled mirrored text/graphics.

### Metal / jewelry / watches

Prefer:
- rim on black;
- low-key luxury;
- light tent macro;
- reflective floor;
- controlled strip reflections.

Watch for:
- clipped metallic highlights;
- fake chrome;
- distracting edge sparkle.

### Matte packaging

Prefer:
- high-key clean;
- soft wraparound;
- overcast;
- three-point hero;
- hard-light graphic setups for bold brands.

Watch for:
- lighting that erases texture/shape;
- background and package merging.

### Technology / gadgets

Prefer:
- underlit glow;
- gel duotone;
- blue hour;
- neon practical;
- rim on black;
- hard light for graphic campaigns.

Watch for:
- cliché cyberpunk when brand is not tech-noir;
- colored reflections reducing text legibility.

### Food / natural / wellness

Prefer:
- window light;
- golden hour;
- overcast;
- dappled botanical;
- candlelight for intimate/winter contexts;
- flat lay.

Watch for:
- muddy color casts;
- overly artificial gloss;
- props becoming primary AOIs.

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

1. Identify product material.
2. Identify brand mood.
3. Identify the primary AOI.
4. Identify the copy-safe-zone requirement for the target layout family.
5. Read relevant reference-lighting DNA.
6. Exclude schemes that conflict with material or brand.
7. Select one primary scheme.
8. Optionally select one alternative for a controlled visual test.
9. Translate the scheme into a banner-specific scene directive.
10. Validate the resulting image inside the actual banner, not in isolation.

Do not generate all 30 schemes by default.

The PDF includes a workflow for generating 30 prompts under one product, but the banner skill should use the library selectively. Generating 30 lighting variations is only appropriate when the user explicitly wants a lighting exploration.

## Lighting choice by objective — production heuristic

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

This table is a selection heuristic, not a performance ranking.

## Banner-family considerations

### Micro horizontal

Avoid complex lighting texture. Strong priorities:
- one clean hero silhouette;
- simple background;
- predictable copy-safe region;
- no stripes/god rays behind text.

High-key, soft wraparound, clean rim, simple hard-shadow setups often translate better than busy atmospheric scenes.

### Leaderboard

Directional light and horizontal shadow/reflection can reinforce the horizontal scan path.

Reserve a clean text strip.

### Rectangle

Most flexible family. Can support:
- stronger hero photography;
- clear light falloff;
- foreground/background depth;
- more expressive lighting.

### Narrow vertical

Use vertical lighting structures:
- rim;
- top-down spotlight;
- underglow;
- vertical reflection;
- controlled gradient.

Avoid wide cinematic scenes that collapse when cropped.

### Large vertical

Can support more atmospheric storytelling but still needs a dominant focal region.

### Billboard

Wide negative space is valuable. A hero can occupy one side while a light gradient or shadow creates a clean copy field on the other.

## Generative prompt guidance

The supplied PDF includes camera, lens, aperture, angle, and imperfection cues in each prompt.

Retain them when they help define the intended photographic look, but treat them as descriptive controls, not guarantees of physically exact optics.

The most important invariant for this skill is not the camera brand. It is:

`material + light source + direction + softness + contrast + reflections/shadows + camera angle + copy-safe composition + realistic texture`

## QA checklist

Before accepting a lighting treatment:

- [ ] Primary AOI is clearer, not weaker.
- [ ] Product/person remains recognizable.
- [ ] Material reads plausibly.
- [ ] Copy-safe region remains readable.
- [ ] No hotspot crosses essential small text.
- [ ] Shadow/reflection does not create a false focal point.
- [ ] Lighting direction is internally coherent.
- [ ] Background light does not flatten logo/CTA contrast.
- [ ] Color cast respects brand/product color.
- [ ] The result still works at actual banner size.
- [ ] The treatment is consistent with other sizes in the same concept.
