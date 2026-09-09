# Art direction and design craft

This reference strengthens visual-quality decisions for performance banners without turning style conventions into fake performance laws.

The rules below are **PRODUCTION HEURISTICS** unless another evidence label is stated explicitly. They were synthesized from practical design-skill patterns found in public GitHub skills including `vanducng/skills` marketing-design, `caorachel-lab/frontend-posters`, `rahamanbinujit/claude-design-engine`, and `social-media-skills/skills` thumbnail-design. They are not treated as research evidence merely because another skill states them.

## 1. Design the visual thesis before decoration

A banner should have one coherent visual thesis:
- one dominant message or subject;
- one primary alignment logic;
- one controlled palette relationship;
- one recognizable graphic or photographic device;
- one intentional route from attention to action.

If the design still depends on decorative blobs, glows, cards, borders, gradients, badges, shadows, or extra icons after the message hierarchy is removed, the decoration is doing too much work.

### Anti-template / anti-AI-slop check

Reject or revise designs that feel interchangeable across unrelated brands because they rely on:
- generic purple/blue gradients with no brand reason;
- random glass panels;
- evenly distributed decorative shapes;
- multiple independent accent effects;
- repeated card UI patterns inside a raster advertisement;
- excessive symmetric centering by habit;
- decoration added before hierarchy is resolved.

A deliberate simple design is preferable to a visually busy generic one.

## 2. Resolve visual direction before multiplying formats

When the brand/design direction is **already locked** by `BRAND.md`, `ДИЗАЙН.md`, an approved reference direction, or an approved previous campaign, do not invent alternative styles merely for variety.

When visual direction is materially unresolved, use one of these controller modes:

### `ART_DIRECTION_LOCKED`
Use the approved system directly.

### `ART_DIRECTION_PREVIEW_3`
Create three genuinely different representative previews using the **same approved message, same product/hero constraints, and same representative banner size**:
- A — restrained / clarity-first;
- B — expressive / attention-first;
- C — context-specific wildcard derived from category, brand, or references.

Do not present three palette swaps of one layout. The user should be comparing actual systems: typography, composition, image treatment, whitespace, scale, and graphic device.

### `ART_DIRECTION_AUTOSELECT_3`
For unattended production, create the same three directions in isolated exploration contexts, then let an independent `ART_DIRECTOR_REVIEWER` rank them against the frozen concept and brand constraints. Freeze the selected direction before creating the full banner matrix.

The representative preview is not a master canvas to be resized later. It exists only to choose the visual language.

## 3. Build hierarchy from silhouette first

Before detail copy and decoration, resolve the large masses:
1. primary subject / hero mass;
2. headline silhouette;
3. CTA/action mass;
4. brand anchor;
5. only then support/proof and decoration.

The relative difference between levels matters more than any universal absolute font ratio.

### Strong hierarchy usually survives several transformations

Use the following as diagnostic views, not scientific tests:
- full color at actual output size;
- 25% thumbnail / glance size;
- grayscale;
- squint/blur view.

A banner is suspect if its intended focal point disappears completely in any of these views while decoration remains dominant.

## 4. Glance / approach / read model

Adapt the useful poster-design idea of multiple viewing distances to banner advertising:

### Glance
What can be understood in roughly a moment?
- primary subject;
- core proposition or hook;
- obvious action direction.

### Approach
What becomes clear after the initial stop?
- supporting proof or offer;
- product/service identity;
- brand.

### Read
What requires intentional reading?
- qualification;
- legal line;
- secondary details.

Small formats may support only the **glance** layer plus brand/action. Do not shrink large-format detail copy until it technically fits.

## 5. One focal point, but not one visual object

A banner may contain multiple objects, but it should normally have one primary attention winner.

Use hierarchy dimensions deliberately:
- size;
- position;
- contrast;
- luminance;
- saturation;
- sharpness;
- isolation / whitespace;
- face/gaze direction;
- edge density;
- typography weight.

Do not stack every possible emphasis technique on every element. Redundant emphasis often creates amateur-looking competition.

## 6. Whitespace is structural

Whitespace is not a fill target. Use it to:
- isolate the focal object;
- separate semantic groups;
- create premium restraint when brand-appropriate;
- preserve copy-safe regions;
- make the CTA distinct without making it enormous.

Never grade a banner by a universal percentage of empty or filled area.

## 7. Alignment and deliberate tension

Start with one dominant alignment system. Break it only when the break creates a clear focal or compositional reason.

Avoid:
- near-alignments that look accidental;
- floating elements with no relationship to the grid;
- inconsistent outer padding across related elements;
- centering every block by default.

Allow:
- intentional crop at canvas edges for decorative/non-semantic objects;
- controlled asymmetry;
- one deliberate alignment break for emphasis.

Semantic content must still respect the banner's safe-zone and clearspace rules.

## 8. Typography craft

Existing typography evidence remains in `typography-color-contrast.md`. This section adds production craft:

- Choose line breaks intentionally for primary copy.
- Judge the **shape** of the headline, not just whether it fits.
- Prefer fewer stronger type levels over many subtly different sizes.
- Do not solve an overloaded banner by adding a third font family.
- Do not solve fit by tracking text unnaturally tight or shrinking below the configured minimum.
- Check numerals, currency symbols, Cyrillic/Latin coverage, punctuation, and brand-specific glyphs in the actual font.
- Text can be the dominant graphic device when the concept is typography-led; it does not need a redundant image merely to fill space.

## 9. Color and grayscale robustness

Color may create hierarchy, but the design should not depend on color alone when size, weight, position, or luminance can reinforce the same relationship.

Use grayscale as a diagnostic:
- if all hierarchy disappears, inspect luminance and scale relationships;
- if a decorative accent remains more dominant than the proposition, revise it;
- if CTA and copy collapse into the background, revise contrast.

Do not infer ad performance from grayscale success.

## 10. Thumbnail / small-view test

For each final output, inspect a reduced diagnostic view in addition to actual size.

Ask:
- is the hero still recognizable?
- is the headline still a distinct text shape?
- is the intended first AOI still dominant?
- does the CTA remain distinguishable?
- have small details turned into visual noise?

A reduced preview is especially important because browsers/design UIs often enlarge small Google banners during review and hide real legibility problems.

## 11. Image and crop craft

Before using an image, record:
- subject position;
- crop tolerance;
- empty/copy-safe regions;
- important product geometry;
- face/gaze direction if present;
- dominant highlights and shadows;
- background edge density.

For each layout family recompose the crop. Do not preserve the same normalized crop coordinates blindly when the aspect ratio changes enough to destroy the subject.

The hero should not be stretched. Product geometry, logo geometry, and faces must remain plausible.

## 12. Art direction and lighting must agree

Lighting is part of the visual thesis.

Before selecting a lighting scheme, determine:
- desired material read;
- desired mood;
- primary AOI;
- copy-safe region;
- whether background separation is needed;
- whether the format is too small for dramatic lighting complexity.

A dramatic lighting treatment that wins the squint/blur test instead of the product or proposition is a design failure even if it is aesthetically attractive.

## 13. Campaign consistency without clone-like resizing

A banner family should feel related through a shared design grammar:
- palette/tokens;
- type roles;
- image treatment;
- shape language;
- CTA treatment;
- lighting logic;
- border/radius behavior where applicable;
- spacing character;
- concept and proposition.

But layouts may change substantially by aspect ratio.

Consistency means **same visual language**, not same coordinates.

## 14. Review order

A `DESIGN_REVIEWER` should inspect in this order:
1. concept/message fidelity;
2. primary AOI and scan path;
3. actual-size readability;
4. thumbnail/glance behavior;
5. grayscale hierarchy;
6. squint/blur hierarchy;
7. crop/product integrity;
8. lighting and copy-zone behavior;
9. alignment/spacing;
10. brand consistency;
11. decorative restraint;
12. CTA/action clarity.

Technical Google validity is checked separately and must not substitute for visual judgment.

## 15. Evidence discipline for imported design heuristics

Do **not** import as universal rules merely because another skill says them. Examples that remain contextual/testable rather than universal:
- “CTA must be bottom-right”;
- “headline/body must always be 4:1”;
- “one accent color only”;
- “exactly four hierarchy levels”;
- “20% text maximum”;
- “faces increase engagement”;
- “this layout has the highest CTR”;
- “central 70–80% is always the safe zone”.

Where a platform has an actual technical rule, the platform rule wins. Where research exists, cite the research. Otherwise keep the statement a production heuristic or test hypothesis.

## 16. Public skill inspirations reviewed

The following repositories were reviewed for practical design-system ideas:
- `vanducng/skills` — marketing-design / banner art-direction catalog and exact-size HTML/screenshot workflow;
- `caorachel-lab/frontend-posters` — fixed-canvas discipline, three real visual directions, thumbnail validation, layout QA;
- `rahamanbinujit/claude-design-engine` — hierarchy diagnostics, self-review, anti-generic design emphasis;
- `social-media-skills/skills` — brand-kit/template-system consistency and thumbnail one-focal-point/mobile-legibility patterns.

These are implementation inspirations, not scientific authorities.