# Banner Task {{JOB_ID}} — {{CONCEPT_ID}} / {{WIDTH}}x{{HEIGHT}} / {{VARIANT_ID}} / {{LANGUAGE}}

## Goal

Produce exactly one final banner file for this banner-matrix row.

## Run routing

- Run ID: `{{RUN_ID}}`
- Job ID: `{{JOB_ID}}`
- Role: `BANNER_DESIGNER`
- Google mode: `{{GOOGLE_MODE}}`
- Layout family: `{{LAYOUT_FAMILY}}`
- Exact size: `{{WIDTH}}x{{HEIGHT}}`
- Output format: `{{PNG_JPG_GIF}}`
- Output path: `{{OUTPUT_PATH}}`
- Report path: `{{REPORT_PATH}}`

## Frozen identities

- Business brief ID/hash: `{{BUSINESS_BRIEF_ID}}`
- Brand/design identity: `{{BRAND_ID}}`
- Creative contract ID/hash: `{{CREATIVE_CONTRACT_ID}}`
- Reference DNA ID(s): `{{REFERENCE_DNA_IDS_OR_NONE}}`
- Lighting plan ID: `{{LIGHTING_PLAN_ID_OR_NONE}}`
- Google spec snapshot: `{{GOOGLE_SPEC_ID}}`

These are controller-owned. Do not redefine them.

## Exact message

Render only approved copy:

- Primary headline: `{{HEADLINE}}`
- Offer/price: `{{OFFER_OR_NONE}}`
- Supporting proof: `{{SUPPORT_OR_NONE}}`
- CTA: `{{CTA}}`
- Brand name: `{{BRAND_NAME}}`
- Legal/disclaimer: `{{LEGAL_OR_NONE}}`

If all approved text cannot fit legibly, follow the allowed removal order below rather than inventing or silently shrinking to unreadability.

## Information priority

1. `{{PRIMARY_AOI}}`
2. `{{PRIMARY_MESSAGE}}`
3. CTA
4. Brand
5. `{{OPTIONAL_SUPPORT}}`

Allowed content removal for this size:
`{{REMOVAL_ORDER}}`

Never remove mandatory legal text.

## Visual contract

- Hero subject: `{{HERO_SUBJECT}}`
- Crop/focal rule: `{{CROP_RULE}}`
- Intended scan path: `{{SCAN_PATH}}`
- Copy-safe zone: `{{COPY_SAFE_ZONE}}`
- Typography context: `{{TYPE_CONTEXT}}`
- Color context: `{{COLOR_CONTEXT}}`
- Grid/spacing context: `{{GRID_CONTEXT}}`
- CTA treatment: `{{CTA_CONTEXT}}`

## Lighting contract

- Scheme ID: `{{LIGHTING_SCHEME_ID_OR_NONE}}`
- Scene lighting: `{{SCENE_LIGHTING_DIRECTIVE}}`
- Composition lighting: `{{COMPOSITION_LIGHTING_DIRECTIVE}}`
- Highlight/hotspot restrictions: `{{HOTSPOT_RESTRICTIONS}}`
- Shadow/reflection direction: `{{SHADOW_REFLECTION_RULE}}`

Lighting may support hierarchy but may not redefine the concept.

## Reference context

Use only these transferable principles:
`{{REFERENCE_PRINCIPLES}}`

Do not copy:
`{{REFERENCE_LITERAL_EXCLUSIONS}}`

## Technical constraints

- Exact pixel dimensions: `{{WIDTH}}x{{HEIGHT}}`
- Max file size: `{{MAX_FILE_BYTES}}`
- Allowed format(s): `{{ALLOWED_FORMATS}}`
- Animation: `{{ANIMATION_RULE}}`
- Actual-size review required: `YES`

## Allowed work

Write only:
- `{{OUTPUT_PATH}}`
- `{{REPORT_PATH}}`
- `{{JOB_LOCAL_TEMP_PATH_OR_NONE}}`

Inspect only:
- `{{APPROVED_ASSET_PATHS}}`
- `{{APPROVED_CONTEXT_PATHS}}`

Do not modify:
- shared banner matrix;
- brand/design docs;
- concept contracts;
- other job folders;
- other banners.

## Role boundary

You may:
- reflow for this exact format;
- alter crop inside the approved hero strategy;
- remove approved secondary content according to the removal order;
- tune spacing and scale within the frozen design system;
- apply the approved lighting plan.

You may not:
- change product/offer/price;
- invent claims/proof;
- change CTA semantics;
- change logo/brand identity;
- redefine the concept;
- add a new lighting concept;
- create child agents;
- produce another size;
- edit another worker's file.

## Design QA gate

Before reporting PASS:

- [ ] primary AOI is intentional;
- [ ] primary proposition is readable quickly;
- [ ] CTA is discoverable;
- [ ] logo/brand is clear but not accidentally dominant;
- [ ] typography is readable at 100% actual pixel size;
- [ ] no clipping/collision;
- [ ] contrast is adequate;
- [ ] copy is not placed over uncontrolled glare/noise/striped shadow;
- [ ] lighting reinforces rather than competes with hierarchy;
- [ ] hero crop is recognizable;
- [ ] spacing/alignment follows the frozen design context;
- [ ] only approved copy is rendered.

## Technical gate

Run the applicable preflight.

Expected:
- exact dimension;
- allowed format;
- file size under current platform limit;
- allowed static/animated state;
- valid file signature.

## Report

Return:

- Job ID
- Status
- Output path
- Size
- Concept ID
- Variant
- Language
- Copy actually rendered
- Content intentionally removed
- Lighting scheme ID
- Known visual risks
- Technical preflight result
- Any controller decision required

## Stop conditions

Return without expanding scope:

- `NEEDS_CONTEXT`
- `ASSET_MISSING`
- `FORMAT_CONFLICT`
- `CLAIM_UNVERIFIED`
- `REFERENCE_CONFLICT`
- `LIGHTING_CONFLICT`
- `DESIGN_CHANGED`
- `DESIGN_DRIFT`
- `TECHNICAL_BLOCKED`

If the banner cannot be made legible under the frozen constraints, return `FORMAT_CONFLICT`.
