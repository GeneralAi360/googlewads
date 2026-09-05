# Typography, color, and contrast

## 1. Serif vs sans-serif

**Evidence level: RESEARCH EVIDENCE**

Controlled research does not support a universal claim that serif or sans-serif typography always produces better reading performance. Arditi & Cho found no meaningful reading-speed advantage attributable simply to serif presence. Later comparisons likewise show that specific font, spacing, size, task, and layout matter.

Therefore do not write rules such as:
- "digital ads must use sans serif";
- "serif is always more premium and less readable";
- "sans serif always increases CTR."

## 2. Production default for small digital banners

**Evidence level: PRODUCTION HEURISTIC**

For micro and small raster ads, begin with a highly legible screen-oriented family featuring:
- open letterforms;
- clear counters;
- sufficient x-height;
- stable medium/semibold/bold weights;
- non-extreme width;
- good Cyrillic support when Russian/Belarusian text is used.

A serif display face may be appropriate for luxury/editorial branding in large text, but validate the actual raster output.

Default system:
- one type family;
- up to two weights;
- optional second family only when brand system or concept materially benefits.

This is a clutter-control heuristic, not an evidence-based magic number.

## 3. Typography hierarchy

A normal uploaded display hierarchy may contain:

- H1: primary proposition / offer;
- H2/support: one clarifier or proof point when space permits;
- CTA: action phrase;
- brand/logo;
- legal: only when required.

Do not create six typographic levels in a 300x250 ad.

## 4. Starting size bands

**Evidence level: PRODUCTION HEURISTIC**

These are starting bands to be validated at actual pixel size. Typeface metrics differ, so pixel size alone is not sufficient.

| Format family | Headline start | Support start | CTA start |
|---|---:|---:|---:|
| 300/320x50 | 14-20 px | usually omit | 10-14 px |
| 468x60 | 16-22 px | usually omit | 11-15 px |
| 728/970x90 | 20-32 px | 12-16 px | 13-18 px |
| 300x250 / 336x280 | 24-38 px | 14-19 px | 14-19 px |
| 160x600 | 20-30 px | 13-17 px | 13-17 px |
| 300x600 | 28-42 px | 16-20 px | 16-20 px |
| 970x250 | 36-52 px | 18-24 px | 16-22 px |

Use real rendered bounds. If copy does not fit, rewrite or remove lower-priority content before shrinking essential text to illegibility.

## 5. Line length and copy shape

**Evidence level: PRODUCTION HEURISTIC**

Prefer short headline units that can be understood quickly. Useful starting targets:
- micro banner: 2-6 words;
- normal rectangle/vertical: 3-8 words in primary headline;
- support: one concise line or two short lines;
- CTA: typically 1-3 words in the language of the campaign.

These are not platform limits. Use actual language morphology and business meaning.

## 6. Contrast

**Evidence level: ACCESSIBILITY STANDARD USED AS INTERNAL QA**

WCAG 2.2 specifies minimum contrast of 4.5:1 for normal text and 3:1 for large-scale text, with exceptions including logotypes. Google does not thereby impose WCAG on every raster ad; use these ratios as a strong internal readability target.

Internal validator targets:
- normal essential text: >=4.5:1;
- large essential text: >=3:1;
- critical micro-banner copy: prefer margin above the minimum due to rasterization/compression.

Do not round a failing ratio upward.

## 7. Text over photography

**Evidence level: PRODUCTION HEURISTIC**

A single contrast ratio sampled from the image is insufficient when text crosses a textured/variable photograph.

Use one or more of:
- a controlled solid/gradient text zone;
- localized image darkening/lightening;
- crop repositioning;
- text backing panel;
- restrained shadow/stroke only if compatible with brand.

Validate worst-case background under the glyphs, not only average image luminance.

## 8. Color strategy

There is no universal "best converting" CTA color.

Choose color from:
1. brand system;
2. local contrast;
3. semantic role;
4. differentiation from surrounding elements;
5. category/context;
6. testable campaign hypothesis.

Suggested role model:
- brand base;
- neutral/background;
- attention accent;
- CTA/action accent.

A CTA should be distinguishable from its immediate background. It does not need to be the most saturated object in the entire composition if that would destroy hierarchy.

## 9. Premium vs performance style

Do not equate premium with low contrast or tiny type. Premium can come from spacing, material imagery, restrained palette, type quality, and composition while keeping essential text legible.

Do not equate performance with fluorescent clutter. A banner can be direct and high-contrast without appearing cheap.

## 10. Compression awareness

Small raster text degrades under JPEG compression and resampling. Validate final exported files, not only source canvases. If text sharpness matters, PNG may be preferable when file-size constraints allow; otherwise tune JPEG quality while preserving legibility.
