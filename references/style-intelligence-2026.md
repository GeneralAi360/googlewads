# Style Intelligence — September 2026

## Purpose

This module helps the controller recommend **visual strategy families before art direction**. It is not a template gallery and it is not a performance-prediction system.

The central rule is:

`IDEA -> PRESENTATION MODE -> EMOTION -> CATEGORY -> VISUAL CHARACTER -> STYLE INTELLIGENCE -> ATTENTION / TYPOGRAPHY / LIGHTING -> ART DIRECTION`

A trend may make a suitable strategy feel current. It may not make an unsuitable strategy good.

## Evidence status

Style and trend sources are separated by role:

- **FOUNDATION STYLE REFERENCE** — historical/formal design grammar;
- **CURRENT TREND SIGNAL** — what is visibly gaining cultural/design momentum in 2026;
- **CURRENT BANNER CRAFT REFERENCE** — recent banner executions and visual categories;
- **AD CRAFT REFERENCE** — advertising execution patterns;
- **TYPOGRAPHY SIGNAL** — changes in type culture/technology;
- **PERFORMANCE EVIDENCE** — only when actual verified campaign metrics exist.

A style library entry is never called high-converting merely because it is current, award-winning, curated, popular, long-running, or present in an ad gallery.

## Current source map — snapshot 2026-09-06

### Design Style Book

`https://www.designstylebook.com/graphic-design`

Role: **FOUNDATION STYLE REFERENCE**.

Current catalog exposes 78 named graphic-design styles and 188+ formal traits. Useful transferable grammars include Swiss Style, Plakatstil, Bauhaus, Blue Note, Postmodern, Punk, Japanese Postwar Graphic, Y2K, Brutalist Web and many others.

Use this source to understand formal structure and lineage, not to decide that an old movement is currently fashionable.

### STYLEBASE

`https://stylebase.art/`

Role: **CULTURAL STYLE REFERENCE**.

Useful because it deliberately expands beyond the Western canon with directions such as Korean Modern Poster, Vietnamese Dong Ho, Central Asian Ornament, Islamic Geometric and Soviet/Post-Soviet Vernacular.

Use it to avoid a globally generic design vocabulary and to improve culturally specific work. Do not reduce culture to decorative tokens.

### BANNER LIBRARY

`https://design-library.jp/?hl=en`

Role: **CURRENT BANNER CRAFT REFERENCE**.

At the September 2026 snapshot the site contains 8,300+ banner examples and supports practical filters such as Simple, Luxurious/Elegant, Natural/Refreshing, Typography only, Illustration, Retro/Ethnic, Neon/Cyber, Cutout and category filters.

Use it to inspect how current banner compositions actually allocate space, image scale, type, color and CTA treatment. It is not conversion evidence.

### Canva 2026 — Imperfect by Design

`https://www.canva.com/newsroom/news/design-trends-2026/`

Role: **CURRENT TREND SIGNAL**.

Relevant signals include:
- Opt-Out Era — structured simplicity, serif, simple branding, anti-cuteness;
- Explorecore — calm editorial layouts and serif-led exploration;
- Texture Check — tactile/material surfaces;
- Reality Warp — liminal/surreal synthetic imagery;
- Prompt Playground — productivity/UI/data/computing aesthetics;
- Drama Club — cinematic/theatrical presentation;
- Notes App Chic / Zinegeist — raw, handmade, anti-polish expression;
- local/heritage-led directions.

Treat search-growth numbers as platform trend evidence, not advertising-performance proof.

### Adobe 2026 Creative Trends

`https://blog.adobe.com/en/publish/2025/12/09/four-creative-trends-define-marketing-2026`

Role: **CURRENT TREND SIGNAL**.

Four major signals:
- All the Feels — sensory/tactile materiality;
- Connectioneering — authentic people and connection;
- Surreal Silliness — playful impossible imagery;
- Local Flavor — regionally authentic culture/community.

These are useful overlays for already-correct concepts, not mandatory campaign directions.

### Envato 2026 Graphic Design Trends

`https://elements.envato.com/learn/graphic-design-trends`

Role: **CURRENT TREND SIGNAL**.

Relevant 2026 directions include neo-minimalism, retro futurism, saturation revival, organic flow, dual aesthetics and AI-assisted workflows followed by human art direction.

The strongest transferable production idea is **dual aesthetics**: a controlled system can carry one deliberately expressive device without becoming chaotic.

### Monotype — typography signals

Variable-font resource:
`https://www.monotype.com/resources/variable-fonts`

Serif/AI-brand article:
`https://www.monotype.com/company/thought-leadership/why-ai-brands-are-obsessed-serif-fonts`

Role: **TYPOGRAPHY SIGNAL**.

Useful 2026 signals:
- variable fonts are mature enough to be treated as a normal design-system tool;
- serif use is visibly increasing in technology/AI branding as brands seek more human, authoritative or trustworthy tone;
- neither signal means serif or variable fonts improve CTR.

## Architecture: style is a layered strategy

Never store a final recommendation as one word such as `minimalism` or `cyberpunk`.

A visual strategy is composed from layers:

1. **Foundation grammar** — the structural design logic.
2. **Contemporary overlay** — an optional current signal.
3. **Execution language** — how the idea is physically expressed.
4. **Attention profile** — what should be seen first and next.
5. **Typography profile** — type voice and production constraints.
6. **Lighting affinity** — how light should support the strategy.
7. **Format resilience** — whether the system survives Google layout families.

Example:

`Swiss Commercial + Opt-Out Era + Real UI Macro Crop + Product-Proof Attention + Enterprise Variable Sans + Restrained Composition Lighting`

is a strategy.

`Minimal blue SaaS` is not.

## Recommendation lanes

When visual direction is unresolved, Style Intelligence should create **three strategic lanes**, not three random style labels:

### A — SAFE_STRONG

Highest total fit to idea, category, truth, attention, typography and formats.

This is not intentionally boring. It is the strongest low-regret system.

### B — CURRENT_DIFFERENTIATED

A high-fit strategy with a current 2026 overlay that adds distinction without damaging brand/category credibility.

Currentness is allowed to break a tie between good strategies. It cannot rescue a weak one.

### C — CONTROLLED_WILDCARD

A materially different strategy that respects the same frozen idea/commercial/brand truth but explores a higher-disruption visual language.

It must still exceed the minimum fit threshold. A wildcard is not permission for random surrealism.

## Ranking model

The default weighting in `config/style-intelligence-library.json` is:

- presentation fit — 18%;
- category fit — 16%;
- emotion fit — 12%;
- attention fit — 14%;
- typography fit — 11%;
- asset-truth fit — 10%;
- format resilience — 9%;
- lighting fit — 5%;
- currentness — 5%.

The low currentness weight is deliberate.

A contemporary but semantically wrong style should lose to a slightly less trendy but better strategy.

## Attention integration

Style choice must never be independent from visual attention.

Each strategy must specify:
- primary AOI;
- scan path;
- salience budget;
- what must remain subordinate;
- whether image, product UI, offer, proof, typography or face carries first attention;
- whether the intended hierarchy survives actual size, 25% thumbnail, grayscale and squint diagnostics.

Eye-tracking research in `references/visual-attention.md` remains contextual evidence. Do not reduce it to a universal Z-pattern or universal CTA position.

## Typography integration

A strategy must recommend a **typographic role profile**, not blindly pick a trendy font name.

Resolve in this order:

1. approved brand typeface;
2. approved custom/campaign typeface;
3. style-intelligence typography profile;
4. verified production fallback.

Every candidate font must be checked for:
- license/usage rights;
- local file availability for deterministic rendering;
- required language/script coverage, including Cyrillic when Russian/Belarusian text is used;
- actual glyph quality;
- weight/width availability;
- raster readability at exact banner size;
- width efficiency for small formats;
- contrast and compression behavior.

Candidate examples in the config are examples only. Never claim that a named family is universally modern or optimal.

### 2026 type signals

Use these as weak currentness priors only:
- serif display voices are more visible in technology/AI branding than during the previous decade of uniform geometric sans;
- variable fonts are a mature option for controlled weight/width adaptation;
- expressive typography is culturally prominent, but micro-banner readability still outranks expression.

For 320x50 or dense leaderboard formats, a restrained high-legibility type system may intentionally differ from the more expressive representative typography while preserving campaign identity.

## Lighting integration

Style Intelligence does not directly choose a final lighting scheme.

It supplies **lighting affinity** to `LIGHTING_INTENT`.

Examples:
- Product Reality / Systems -> truthful UI, restrained separation, no fake relighting;
- Neo-Minimal / Quiet Luxury -> controlled material light, soft/rim/low-key options when the physical product supports them;
- Human Authentic -> natural/window/overcast starting points;
- Bold Poster -> graphic hard-light or no scene lighting depending on execution;
- Controlled Maximalism -> light remains subordinate to the one expressive device;
- Reality Warp -> expressive scene lighting is possible only if the idea itself permits surrealism.

`LIGHTING_INTENT` remains the authoritative contract.

## Typography and style must survive the format matrix

The representative design may use a distinctive display typeface or large visual device. The campaign system must define what happens when that treatment cannot survive 320x50, 728x90 or 160x600.

Do not force a style to survive by shrinking it.

Possible adaptations:
- remove secondary type family;
- switch display role to the approved utility family;
- reduce decorative texture;
- simplify hero crop;
- preserve one signature graphic device;
- preserve color/type character while changing composition.

## Anti-trend-overfit gate

Reject or down-rank a recommendation when:
- it exists only because it is fashionable;
- it conflicts with the category trust requirement;
- it needs fake product imagery;
- it requires unreadable typography;
- it collapses in micro formats;
- it contradicts the emotional target;
- it duplicates a category cliché the category map explicitly identified;
- it produces generic AI polish without a brand-specific idea.

## Runtime artifact

Before written art directions, create:

`style-strategy-context.json`

and run:

```bash
python scripts/recommend_visual_styles.py \
  --context run/design/style-strategy-context.json \
  --library config/style-intelligence-library.json \
  --out run/design/style-strategy-recommendation.json
```

The result must be treated as **decision support for the Art Director**, not automatic proof that the top-ranked strategy will perform best in market.

The selected art direction should cite the chosen strategy ID(s) in its rationale or design-brief references so the provenance is traceable.

## User-provided style examples

When the user supplies new banner examples:

1. analyze each with REFERENCE_DNA;
2. identify whether it represents a new foundation, overlay, execution language, typography profile, attention pattern or only a one-off decorative device;
3. add only reusable vocabulary to the style library;
4. never copy another brand identity literally;
5. never promote a style into a performance rule without campaign evidence;
6. add regression/eval cases if the example reveals a gap in the current system.
