# Public GitHub Design Skills Reviewed for v0.2

This document records public skill/repository patterns reviewed while strengthening banner design craft. These repositories are implementation/design-method inspirations, not scientific authorities.

## `vanducng/skills` — `marketing-design`

Useful patterns retained:
- banner workflow explicitly asks purpose, platform, content, brand, style and quantity;
- broad art-direction vocabulary instead of one generic AI aesthetic;
- exact-size HTML/CSS/screenshot thinking for banner output;
- separate imagery generation from layout/composition.

Not imported as universal rules:
- CTA always bottom-right;
- universal central 70–80% safe zone;
- universal 20% text maximum;
- universal font-size thresholds;
- unsupported “highest CTR” labels.

## `caorachel-lab/frontend-posters`

Strongest transferable craft patterns:
- fixed canvas at authored target dimensions;
- if direction is unresolved, create three real previews rather than verbal mood boards;
- keep actual content/assets stable across preview directions so the user compares design systems;
- compose hook/image masses before details;
- inspect full-size artifact and reduced thumbnail;
- automated bounds/overflow/collision QA plus visual inspection;
- avoid app/dashboard/card UI habits in graphic-design artifacts.

Adapted into this repository as art-direction preview modes, aspect-ratio recomposition, actual-size review and thumbnail diagnostics.

## `rahamanbinujit/claude-design-engine`

Useful patterns retained:
- hierarchy as relative visual contrast rather than decoration;
- squint test;
- grayscale diagnostic;
- self-review before delivery;
- research/reference-first mindset;
- explicit anti-generic design concern.

Not imported as laws:
- exact 4:1 headline/body ratio;
- “exactly four hierarchy levels”;
- one accent color universally;
- prohibition on pure black/white;
- any aesthetic score as a performance prediction.

## `social-media-skills/skills`

### `design-and-templates`
Useful: persistent brand kit, small reusable design grammar, consistency across related assets, safe-zone/mobile-legibility mindset.

### `thumbnail-design`
Useful: one primary focal point, small-view legibility, meaningful A/B variants, title/visual complementarity, gaze only when relevant.

Performance percentages and universal engagement claims from external skills are not promoted into this repository without stronger evidence.

## `AgriciDaniel/claude-ads` — creative audit

Useful principle: keep creative quality, platform compliance and measured performance as separate judgments. A good-looking banner is not automatically compliant; a compliant banner is not automatically good; neither implies performance without campaign data.

## `Salah-XD/equipt` — ad creative brief

Useful: explicit gate for product/offer, platform, objective, audience, brand, quantity and format before detailed production; separate messaging angles from finished executions.

Social-platform generalizations from that skill are not treated as Google display laws.

## Resulting v0.2 additions

The review above directly informed:
- `references/art-direction-and-design-craft.md`;
- three-mode art-direction resolution;
- frozen `art_direction_id` provenance;
- anti-template / anti-generic-AI checks;
- silhouette-first hierarchy;
- aspect-ratio crop recomposition;
- actual-size + thumbnail + grayscale + squint review views;
- campaign-level design grammar in pack review;
- explicit evidence discipline for imported heuristics.
