# Rendering and validation model

## 1. Split creative generation from precision composition

Use generative tools for exploratory visual material when appropriate. Use deterministic layout/rendering for critical advertising content.

Generative layer may create:
- environment/background;
- lifestyle scene;
- non-text hero art;
- mood/style exploration.

Deterministic layer owns:
- logo;
- brand name;
- price;
- headline;
- CTA;
- disclaimer;
- typography;
- exact dimensions;
- export format;
- compression.

## 2. Why this split is mandatory

Image generation can alter spelling, digits, logos, product geometry, or layout. Those errors are unacceptable in production advertising.

A good-looking AI image with an incorrect price or brand name fails QA.

## 3. Render specification

Each variant should be represented by a structured object containing at least:

- campaign ID;
- concept ID;
- variant ID;
- platform mode;
- width/height;
- layout family;
- copy strings;
- asset paths/IDs;
- font family/weights;
- color tokens;
- focal crop;
- intended scan path;
- output path;
- QA state.

Use `schemas/banner-concept.schema.json` and `schemas/output-manifest.schema.json`.

## 4. Technical preflight

### Uploaded Display static
Check:
- exact width and height;
- allowed dimension for selected pack;
- allowed file type;
- final file size;
- animation status allowed by current campaign mode;
- readable/correct text;
- no corruption.

### Responsive / Demand Gen assets
Check:
- exact aspect ratio / minimum dimensions;
- file size;
- crop robustness;
- absence of inappropriate overlaid logos/text/buttons;
- separate text asset character limits;
- logo format and ratio.

## 5. Visual preflight

Check at 100% size:
- can the proposition be understood without zooming?
- is hierarchy obvious?
- does CTA remain distinct?
- is logo identifiable but not accidentally dominant?
- is the focal image still recognizable?
- are lines clipped?
- does JPEG/PNG export change text sharpness?

## 6. Contrast preflight

For flat-color text zones, calculate contrast mathematically.

For text over imagery, additionally inspect local luminance variation under the full glyph region. Average-background contrast can be misleading.

## 7. Pack-level consistency

A pack passes only when:
- all variants share the same core proposition/concept;
- brand tokens are consistent;
- layout differences are intentional;
- no small format contains leftovers that only made sense in the large format;
- files are named and traceable.

## 8. Naming convention

Recommended:

`{campaign}_{concept}_{variant}_{width}x{height}.{ext}`

Example:

`kitchens_sep26_offer-a_v03_300x250.png`

Avoid ambiguous names such as `banner-final-final2.png`.

## 9. Contact sheet

For a multi-format pack, create an overview showing all variants with dimension labels. The contact sheet is for review only and is not an upload asset.

## 10. Failure states

Use explicit states:
- `PASS`
- `FAIL_PLATFORM_SPEC`
- `FAIL_FILE_SIZE`
- `FAIL_DIMENSIONS`
- `FAIL_COPY_OVERFLOW`
- `FAIL_CONTRAST`
- `FAIL_BRAND_CONSISTENCY`
- `FAIL_UNSUPPORTED_CLAIM`
- `REVIEW_VISUAL_HIERARCHY`
- `REVIEW_POLICY`

Do not hide a failed requirement behind a generic quality score.
