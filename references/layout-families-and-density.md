# Layout families and information density

## 1. Never use one-canvas resize

**Evidence level: PRODUCTION RULE**

Aspect ratios change the available reading path. A 320x50 banner and 300x600 banner are not the same design at different scales.

Preserve the creative idea; redesign the composition.

## 2. Core Google pack -> layout families

### Micro horizontal
- 320x50

Information budget:
- logo/brand anchor;
- one short proposition or offer;
- CTA.

Normally omit:
- body copy;
- secondary proof;
- multiple badges;
- long legal text unless mandatory.

Typical flow:
`brand | proposition | CTA`

### Leaderboard
- 728x90
- 970x90

Information budget:
- product/visual or brand anchor;
- headline/offer;
- optional compact support/proof;
- CTA.

Typical flow:
`visual -> proposition -> CTA` with brand integrated into one end or near the visual.

### Rectangle
- 300x250
- 336x280

Information budget:
- hero product/service image;
- headline;
- optional offer/support;
- CTA;
- logo.

This family has enough depth for a clear visual hierarchy but still cannot support a brochure.

### Narrow vertical
- 160x600

Information budget:
- hero/crop;
- headline;
- offer/support;
- CTA;
- logo.

Use vertical sequencing deliberately. Avoid a long centered column of tiny text.

### Large vertical
- 300x600

Information budget:
- stronger hero storytelling;
- headline;
- one support/proof block;
- offer;
- CTA;
- logo.

Do not fill extra height simply because it exists. Large negative space can help hierarchy when the focal object remains strong.

## 3. Extended families

### Small square
- 200x200
- 250x250

### Alternate rectangles
- 240x400
- 250x360
- 580x400

### Narrow skyscraper
- 120x600

### Portrait
- 300x1050

### Short horizontal
- 468x60

### Large horizontal / billboard
- 930x180
- 970x250
- 980x120

### Mobile
- 300x50
- 320x100

Each extended format must map to the nearest family only as a starting point. Re-check composition because dimension changes can materially affect copy and crop.

## 4. Density is not fill percentage

There is no established universal scientific rule that an effective completed banner should be 30%, 50%, 70%, or any other fixed percentage "filled."

Do not calculate quality from pixel occupancy alone.

Instead evaluate:
- meaningful AOI count;
- text line count;
- words per hierarchy level;
- whitespace usefulness;
- hero scale;
- number of competing colors/shapes;
- time-to-understand at actual size.

Google's responsive-image statement that blank space should not exceed 80% belongs to that asset context and must not be generalized to every banner.

## 5. Meaningful AOI budget

**Evidence level: PRODUCTION HEURISTIC**

Typical target: 3-5 meaningful AOIs.

Examples:

### 320x50
1. brand
2. proposition
3. CTA

### 300x250
1. hero/product
2. headline/offer
3. support/proof (optional)
4. CTA
5. brand

### 300x600
1. hero/product
2. headline
3. proof/offer
4. CTA
5. brand

If decorative sticker, pattern, icon set, gradient flare, and background type all become attention objects, complexity is too high even if text is short.

## 6. Information-removal rule

When adapting from a large format to a smaller format, remove information in this order:

1. decorative copy;
2. secondary explanation;
3. secondary proof/badges;
4. non-essential imagery;
5. support line.

Preserve as long as possible:
- primary proposition;
- real CTA/action;
- brand identification;
- mandatory legal constraint;
- verified offer when it is the core proposition.

## 7. Safe insets

**Evidence level: PRODUCTION HEURISTIC**

Google does not provide one universal safe-margin percentage for all uploaded display sizes. Begin with a deliberate outer inset and validate visually.

Suggested starting logic:
- micro formats: at least 4 px practical inset where possible;
- other formats: start around 4-6% of the shorter dimension for critical text/logo, then adjust to composition;
- preserve extra logo clearspace defined by the brand guide.

Do not treat these values as platform rules.

## 8. Cropping strategy

For each family specify:
- focal point x/y;
- allowed crop sides;
- protected face/product areas;
- negative-space zone reserved for text;
- whether image can be removed in micro format.

A composition may intentionally use no hero image in 320x50 while using one in 300x600. That is adaptation, not inconsistency.

## 9. Real-size test

Every final design must be inspected at 100% pixel size. Zoomed-up design review can hide unreadable text and weak CTA separation.

Also review the pack together to ensure it feels like one campaign rather than unrelated banners.
