# Rendering and validation model

## 1. Split creative generation from precision composition

Use generative tools for exploratory visual material when appropriate. Use deterministic layout/rendering for critical advertising content.

Generative layer may create:
- environment/background;
- lifestyle scene;
- non-text hero art;
- mood/style exploration.

Deterministic layer owns:
- exact approved logo / brand name;
- price and offer;
- headline/support copy;
- CTA;
- disclaimer when required;
- typography;
- focal crop;
- composition-lighting overlays;
- exact dimensions;
- export format;
- compression.

A good-looking AI image with an incorrect price, logo, or brand spelling fails QA.

## 2. v0.2 renderer baseline

The accepted baseline is Python + Pillow. See `docs/ADR-001-renderer.md`.

Implemented components:
- `config/layout-presets.json` — normalized layout-family presets;
- `schemas/banner-render-spec.schema.json` — one deterministic render spec per banner-matrix row;
- `scripts/render_banner.py` — exact PNG/JPG renderer;
- `scripts/build_contact_sheet.py` — review-only overview;
- `scripts/render_banner_pack.py` — matrix-driven pack runner;
- `scripts/validate_google_banner.py` — Google technical preflight.

Pillow is the precision raster layer, not the creative-strategy layer. Layout presets are production heuristics and may be overridden by a frozen banner task when the concept requires another composition.

## 3. One banner = one render spec

Each final banner job should have a render spec containing:
- `job_id` identical to its banner-matrix row;
- exact width and height;
- exact layout family;
- approved copy slots;
- logo/brand asset;
- brand font paths and color tokens;
- optional hero path and focal point;
- optional composition-lighting primitives;
- output path/format/byte target;
- optional contrast gates.

The pack runner rejects a render spec whose `job_id`, width, height, or layout family differs from the frozen matrix row.

## 4. Text fitting is fail-closed

The renderer measures the actual selected font and tries sizes only inside the configured range.

It must not silently shrink below the minimum. If the approved copy does not fit, return:

`FAIL_COPY_OVERFLOW`

The correct follow-up is a controller/design decision: shorten the copy, alter the approved layout, or explicitly change the typography contract. A renderer is not authorized to rewrite the offer.

If a layout family intentionally has no `offer` or `support` slot, passing that content returns `FAIL_LAYOUT` rather than squeezing it into an unrelated area.

## 5. Focal crop and assets

Hero images use cover-crop with an explicit normalized focal point when supplied. Logos use contain-fit so the deterministic layer does not crop the brand mark.

The renderer does not recreate a supplied logo with AI and does not vendor proprietary fonts. Real brand font files/paths must be provided by the project/run when required.

## 6. Composition lighting

Implemented deterministic primitives:
- radial `spotlight`;
- directional `copy_scrim` / protected copy gradient;
- restrained `vignette`.

These are hierarchy tools, not performance claims. They may separate a hero from the background, protect a copy zone, or control edge brightness. They must not create uncontrolled glare beneath critical text or become the accidental primary AOI.

Still planned in v0.2:
- local hero edge glow;
- tonal text plate;
- richer local photographic contrast sampling.

Scene lighting remains part of the source hero image and follows `references/lighting-intelligence.md`.

## 7. Contrast

For flat colors, `scripts/render_banner.py` calculates relative luminance and contrast ratio and can enforce explicit minimums.

For text over photography, average-background contrast is insufficient. Local luminance variation across the actual glyph region still requires visual/local-image QA; do not claim that the current flat-color calculation proves photographic readability.

## 8. Export and byte limits

PNG and JPG are supported by the v0.2 renderer.

Rules:
- exact width/height are preserved;
- PNG is optimized but is not silently converted to JPG to meet a byte limit;
- JPG quality may step down only inside the render spec's explicit `jpeg_quality` → `min_jpeg_quality` interval;
- if the file remains too large, return `FAIL_FILE_SIZE`;
- the pack runner then sends the rendered file through `validate_google_banner.py`.

This preserves the difference between creative/render failure and Google technical failure.

## 9. Matrix-driven pack assembly

The pack runner consumes:
- one `BANNER_MATRIX` JSON;
- a directory containing `{job_id}.json` render specs;
- Google validation mode/pack;
- optional contact-sheet path;
- optional output-manifest path;
- a mandatory run report path.

Example:

```bash
python scripts/render_banner_pack.py \
  --matrix run/banner-matrix.json \
  --spec-dir run/render-specs \
  --mode demand_gen_uploaded_display \
  --pack core \
  --contact-sheet run/contact-sheet.png \
  --manifest run/output-manifest.json \
  --report run/pack-report.json
```

The run is `PASS` only when every matrix row renders and passes Google technical preflight.

A missing render spec, mismatched matrix/spec identity, copy overflow, file-size failure, contrast failure, or Google validator failure keeps the full pack in `FAIL`.

## 10. Output manifest

`output-manifest.json` is emitted only for a fully passing pack. It maps each final file to its concept/variant, path, dimensions, file bytes/format, layout family, and passed checks.

An incomplete run may produce a diagnostic pack report and a partial review contact sheet, but it must not emit a manifest that implies full campaign readiness.

## 11. Contact sheet

The contact sheet displays mixed banner sizes inside consistent review cells and labels each file with filename and native dimensions.

It is review-only and is never a Google upload asset. A contact sheet does not replace inspection of critical banners at 100% actual pixel size.

## 12. Technical preflight

### Uploaded Display static
Check:
- exact width and height;
- allowed dimension for selected pack;
- allowed file type;
- final file size;
- static/animated state allowed by current mode;
- no corrupted file;
- filename/job mapping.

### Responsive / Demand Gen assets
Check separately:
- exact aspect ratio / minimum dimensions;
- file size;
- crop robustness;
- absence of inappropriate overlaid logos/text/buttons;
- separate text asset character limits;
- logo format and ratio.

Do not apply the finished-banner raster pipeline blindly to asset-based ads.

## 13. Visual preflight

Check at 100% size:
- proposition is understandable without zooming;
- hierarchy is obvious;
- CTA remains distinct;
- logo is identifiable but not accidentally dominant;
- focal image remains recognizable;
- copy is not clipped;
- lighting does not sabotage copy-safe areas;
- JPEG/PNG export has not damaged text or product edges.

## 14. Pack-level consistency

A pack passes visually only when:
- all size adaptations remain faithful to the frozen creative contract;
- brand tokens are consistent;
- layout differences are intentional;
- small formats remove low-priority content instead of shrinking everything;
- no worker silently changes offer/price/CTA;
- all files are named and traceable.

## 15. Failure states

Use explicit states such as:
- `PASS`
- `FAIL_LAYOUT`
- `FAIL_LAYOUT_FAMILY`
- `FAIL_COPY_OVERFLOW`
- `FAIL_CONTRAST`
- `FAIL_FILE_SIZE`
- `FAIL_DIMENSIONS`
- `FAIL_FORMAT`
- `FAIL_ASSET`
- `FAIL_SPEC_MATRIX_MISMATCH`
- `FAIL_TECHNICAL_PREFLIGHT`
- `FAIL_BRAND_CONSISTENCY`
- `FAIL_UNSUPPORTED_CLAIM`
- `REVIEW_VISUAL_HIERARCHY`
- `REVIEW_POLICY`

Do not hide a failed requirement behind a generic quality score.
