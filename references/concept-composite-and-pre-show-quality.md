# Banner Concept Composite and Pre-show Quality Gate

## Purpose

A generated image, hero asset, texture, 3D object, UI crop, photograph, illustration, or other visual component is **not** a banner concept by itself.

The user evaluates advertising design, not an upstream source asset.

The permanent boundary is:

`RAW / GENERATED / REFERENCE ASSET -> SELECT / REFINE -> BANNER COMPOSITION -> TYPE / CTA / BRAND / COMMERCIAL CUE -> EXACT 300x250 COMPOSITE -> PRE-SHOW REVIEW -> USER`

Never:

`IMAGE GENERATION OUTPUT -> call it a banner concept -> reviewer PASS -> show user`.

This reference was added after REAL-07, where Work generated polished-looking abstract blue/metal hero imagery and stalled in image generation while the system had already reported `PRESENTATION_READY_DESIGN = PASS`. The artifact visible to the user was not yet a composed advertisement and had no obvious purchase-license message, CTA, or brand anchor.

## Artifact roles

Use explicit roles.

### `HERO_ASSET_CANDIDATE`

An upstream component. Examples:
- generated 3D object;
- product/environment image;
- official UI screenshot;
- photo;
- abstract material device;
- background/texture.

It may be visually strong, but it cannot receive user visual-concept approval.

### `BANNER_COMPOSITE`

The only valid user-facing visual-concept artifact.

It must already integrate the visible campaign system at the representative size:
- primary message;
- explicit commercial-job cue;
- CTA;
- brand anchor;
- hero/visual device where applicable;
- typography hierarchy;
- composition/grid;
- color/lighting treatment;
- whitespace/density;
- real or declared concept-only asset slots.

A raw hero can be one component of the composite. It cannot be the composite itself.

## Composition contract

Every `visual-concept-preview.json` must declare:

- `artifact_role = BANNER_COMPOSITE`;
- `render_stage = USER_FACING_CONCEPT_COMPOSITE`;
- `composition_method`;
- exact mandatory visible primary message;
- commercial-job cue;
- CTA;
- brand anchor;
- all raw generated asset paths used upstream;
- `raw_generated_asset_is_final_artifact = false`.

The preview validator checks exact SHA, decodable PNG/JPEG bytes and actual raster dimensions. It rejects a raw generated asset path that is reused as the final concept artifact.

This is a deterministic provenance gate. It does not pretend to OCR or judge aesthetics automatically.

## Generated hero rule

Image generation is allowed only when the selected visual direction benefits from it and the commercial meaning remains clear.

Generation should produce **component assets**, not user-facing banners.

For each generated component ask:

1. What semantic role does it play?
2. Is the relation to the commercial job visible, or is it merely decorative?
3. Could the same image be dropped into an unrelated SaaS campaign without changing meaning?
4. Does it force the advertising copy to explain an otherwise meaningless object?

If the image is mostly decorative/generic, reject it as a hero before composition.

Do not keep generating variants merely because the provider can generate them. A stalled or low-value generation step should be abandoned in favor of a stronger type-led, product-led, editorial, or structural direction.

## Pre-show review is exact-artifact review

A reviewer may issue `PRESENTATION_READY_DESIGN` only for the exact `BANNER_COMPOSITE` bytes the user will see.

Reviewing any of the following is insufficient:
- written art direction;
- hero-generation prompt;
- raw image-generation output;
- screenshot reference;
- component sheet;
- verbal concept description.

Each candidate requires **two fresh review contexts** with different `reviewer_context_id` values.

The second reviewer must not see the first review verdict.

Both reviews must be bound to:
- exact `visual_concept_id`;
- exact `commercial_job_id`;
- exact artifact path;
- exact artifact SHA;
- `artifact_role = BANNER_COMPOSITE`.

## Required review checks

Every review records `PASS/FAIL` plus visible-artifact evidence for:

- `commercial_job_fidelity`;
- `banner_composite_complete`;
- `primary_message_visible`;
- `cta_visible_and_integrated`;
- `brand_anchor_visible`;
- `hero_semantic_relevance`;
- `advertising_impact`;
- `compositional_confidence`;
- `typographic_craft`;
- `visual_polish`;
- `category_premium_bar`;
- `non_generic_identity`;
- `ad_not_presentation_slide`;
- `small_format_viability`.

A bare boolean without evidence is not a valid fresh review report.

## Quality bar

`PRESENTATION_READY_DESIGN` means more than readable, technically valid or policy-safe.

The reviewer must be able to defend that:
- the first glance contains a strong advertising idea;
- the layout feels intentional rather than assembled from blocks;
- type scale, line breaks, spacing and optical alignment feel crafted;
- visual depth/material treatment is controlled rather than accidental;
- the concept can sit next to mature B2B/SaaS advertising without looking amateur;
- the visual language is not interchangeable generic SaaS styling;
- the CTA belongs to the composition;
- the hero has semantic relevance to the commercial job;
- the result reads as an advertisement, not a deck slide or isolated art asset.

If either reviewer cannot support these claims from the exact artifact, verdict is `REVISE_BEFORE_SHOW`.

## REAL-07 failure signatures

Permanent findings:

- `RAW_HERO_ASSET_MISTAKEN_FOR_BANNER`;
- `IMAGE_GENERATION_STALLED_BEFORE_COMPOSITE`;
- `REVIEW_PASS_BEFORE_BANNER_COMPOSITE`;
- `ART_DIRECTOR_REVIEW_FALSE_POSITIVE`;
- `GENERIC_ABSTRACT_HERO_WITHOUT_COMMERCIAL_MEANING`;
- `BANNER_COPY_CTA_BRAND_NOT_PRESENT_AT_REVIEW_TIME`;
- `USER_FORCED_TO_REJECT_BASIC_VISUAL_QUALITY`.

## Recovery rule

When REAL-07 is detected:

1. preserve the valid commercial-job lock, research and policy facts;
2. invalidate only failed visual concepts, generated hero selections and stale pre-show reviews;
3. do not repeat intake unless a business fact changed;
4. return to visual strategy / hero selection / composition as needed;
5. create complete 300x250 banner composites;
6. run two exact-artifact fresh reviews;
7. show the user only concepts that pass the new composite + review gates.

The full pack remains blocked until normal user selection/approval gates pass.
