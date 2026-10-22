# Typography, color, and contrast

## 1. Serif vs sans-serif

**Evidence level: RESEARCH EVIDENCE**

Controlled research does not support a universal claim that serif or sans-serif typography always produces better reading performance. Arditi & Cho found no meaningful reading-speed advantage attributable simply to serif presence. Later comparisons likewise show that specific font, spacing, size, task, and layout matter.

Therefore do not write rules such as:
- "digital ads must use sans serif";
- "serif is always more premium and less readable";
- "sans serif always increases CTR."

## 2. September 2026 typography intelligence

**Evidence level: CURRENT TYPOGRAPHY / CULTURAL SIGNAL + PRODUCTION HEURISTIC**

The current style snapshot adds two useful 2026 signals:

1. **Serif voices are visibly returning in technology/AI branding.** Monotype's 2026 commentary describes technology/AI brands using serif typography to communicate a more human, authoritative or trustworthy tone after a long period dominated by neutral geometric sans systems.
2. **Variable fonts are mature production tools.** Weight/width axes can help build a more consistent campaign type system and adapt density across formats without introducing another family.

Neither signal is a performance law.

Do not infer:
- serif = higher trust or conversion for every category;
- variable font = better ad performance;
- a 2026 trend should override the approved brand type system.

Use `config/style-intelligence-library.json` and `references/style-intelligence-2026.md` when visual direction is unresolved.

## 3. Font-source precedence

Resolve actual font choice in this order:

1. approved brand font from `BRAND.md` / `DESIGN.md` / supplied brand assets;
2. explicitly approved campaign/custom typeface;
3. typography profile recommended by Style Intelligence;
4. verified production fallback.

A style recommendation selects a **typographic role profile**, not an unquestionable font file.

Before a named candidate becomes production-ready, verify:
- usage/license rights;
- local font file availability for deterministic rendering;
- required script and language coverage;
- Cyrillic/Belarusian quality when those languages are used;
- actual glyph shapes, not merely Unicode support;
- required weight/width axes or static styles;
- target-size raster readability;
- width efficiency in narrow/micro formats;
- compression behavior in the final export.

If any mandatory check is unresolved, return `NEEDS_FONT_ASSET` or a controller-approved fallback rather than silently substituting a random system font.

## 4. Production default for small digital banners

**Evidence level: PRODUCTION HEURISTIC**

For micro and small raster ads, begin with a highly legible screen-oriented family featuring:
- open letterforms;
- clear counters;
- sufficient x-height;
- stable medium/semibold/bold weights;
- non-extreme width;
- good required-script support.

A serif display face may be appropriate for luxury/editorial/trust-oriented branding in large text, but validate the actual raster output.

Default system:
- one type family;
- up to two or three purposeful weights;
- optional second family only when brand system or concept materially benefits.

This is clutter control, not a magic number.

## 5. Typography profiles used by Style Intelligence

The current library may recommend role profiles such as:
- `TYPE_ENTERPRISE_VARIABLE_SANS`;
- `TYPE_EDITORIAL_SERIF_SANS`;
- `TYPE_QUIET_LUXURY_SERIF`;
- `TYPE_HUMANIST_SANS`;
- `TYPE_CONDENSED_PROMO`;
- `TYPE_TECH_MONO_ACCENT`;
- `TYPE_EXPRESSIVE_DISPLAY_RESTRAINED`;
- `TYPE_SOFT_SERIF_HUMAN`;
- `TYPE_LOCAL_SCRIPT_AWARE`.

These profiles specify character and constraints. Font names inside the library are **candidate examples only** and must be runtime-verified.

### Variable-font use

Variable width/weight is useful when:
- one campaign must survive rectangle, leaderboard, vertical and micro formats;
- the same family has a legitimate width axis;
- a controlled width adjustment preserves identity better than switching fonts.

Do not synthetically squeeze glyphs with image transforms or arbitrary CSS scaling when a real font axis/style does not exist.

### Expressive type

A representative 300x250 may legitimately use more expressive display type than a 320x50.

If that voice fails small-view QA:
- keep the campaign's approved utility family;
- preserve hierarchy/color/signature device;
- remove the expressive family from the micro format instead of shrinking it into illegibility.

This is adaptation, not design drift.

## 6. Typography hierarchy

A normal uploaded display hierarchy may contain:
- H1: primary proposition / offer;
- H2/support: one clarifier or proof point when space permits;
- CTA: action phrase;
- brand/logo;
- legal: only when required.

Do not create six typographic levels in a 300x250 ad.

The role hierarchy should match the selected Style Intelligence attention profile. For example:
- `ATTENTION_PRODUCT_PROOF` normally keeps product/UI dominant and type as the commercial reading path;
- `ATTENTION_OFFER_FIRST` lets the offer outrank the hero;
- `ATTENTION_TYPOGRAPHIC_STATEMENT` makes type itself the primary visual mass.

Do not choose a type style independently from the intended scan path.

## 7. Starting size bands

**Evidence level: PRODUCTION HEURISTIC**

These are starting bands to validate at actual pixel size. Typeface metrics differ, so pixel size alone is insufficient.

| Format family | Headline start | Support start | CTA start |
|---|---:|---:|---:|
| 300/320x50 | 14-20 px | usually omit | 10-14 px |
| 468x60 | 16-22 px | usually omit | 11-15 px |
| 728/970x90 | 20-32 px | 12-16 px | 13-18 px |
| 300x250 / 336x280 | 24-38 px | 14-19 px | 14-19 px |
| 160x600 | 20-30 px | 13-17 px | 13-17 px |
| 300x600 | 28-42 px | 16-20 px | 16-20 px |
| 970x250 | 36-52 px | 18-24 px | 16-22 px |

Use real rendered bounds. If copy does not fit, rewrite/remove lower-priority content or use an approved format-specific copy reduction before shrinking essential text below useful legibility.

Mandatory qualifiers cannot be dropped only to make the typography look cleaner.

## 8. Line length and copy shape

**Evidence level: PRODUCTION HEURISTIC**

Prefer short headline units that can be understood quickly. Useful starting targets:
- micro banner: 2-6 words;
- normal rectangle/vertical: 3-8 words in primary headline;
- support: one concise line or two short lines;
- CTA: typically 1-3 words in the campaign language.

These are not platform limits. Use actual language morphology and business meaning.

For Cyrillic copy, test actual word width rather than importing assumptions from English examples.

## 9. Contrast

**Evidence level: ACCESSIBILITY STANDARD USED AS INTERNAL QA**

WCAG 2.2 specifies minimum contrast of 4.5:1 for normal text and 3:1 for large-scale text, with exceptions including logotypes. Google does not thereby impose WCAG on every raster ad; use these ratios as strong internal readability targets.

Internal validator targets:
- normal essential text: >=4.5:1;
- large essential text: >=3:1;
- critical micro-banner copy: prefer margin above minimum because of rasterization/compression.

Do not round a failing ratio upward.

## 10. Text over photography

**Evidence level: PRODUCTION HEURISTIC**

A single contrast ratio sampled from the image is insufficient when text crosses a textured/variable photograph.

Use one or more of:
- controlled solid/gradient text zone;
- localized image darkening/lightening;
- crop repositioning;
- text backing panel;
- restrained shadow/stroke only if compatible with brand/style.

Validate worst-case background under glyphs, not only average luminance.

Lighting and type must be planned together. A current cinematic or tactile treatment is not acceptable if specular highlights or shadows destroy the copy-safe field.

## 11. Color strategy

There is no universal "best converting" CTA color.

Choose color from:
1. brand system;
2. local contrast;
3. semantic role;
4. differentiation from surrounding elements;
5. category/context;
6. selected style strategy;
7. testable campaign hypothesis.

Suggested role model:
- brand base;
- neutral/background;
- attention accent;
- CTA/action accent.

A CTA should be distinguishable from its immediate background. It does not need to be the most saturated object in the composition if that destroys hierarchy.

## 12. Premium vs performance style

Do not equate premium with low contrast or tiny type. Premium can come from spacing, material imagery, refined type, restrained palette and composition while keeping essential text legible.

Do not equate performance with fluorescent clutter. A banner can be direct and high-contrast without looking cheap.

Likewise, do not equate "modern 2026" with serif, brutalism, maximalism, tactile 3D or any single visual trend. Modernity is assessed as a fit-sensitive overlay.

## 13. Compression awareness

Small raster text degrades under JPEG compression and resampling. Validate final exported files, not only source canvases.

If text sharpness matters, PNG may be preferable when file-size constraints allow; otherwise tune JPEG quality while preserving legibility.

Run actual-size inspection after final compression. A type choice that only looks good in the source canvas is not production-ready.
