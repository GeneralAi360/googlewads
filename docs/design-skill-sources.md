# Design-skill and methodology sources

This repository separates **useful design process ideas** from **scientific/performance evidence**. Public skills, practitioner presentations and creative tools may contribute production heuristics or vocabulary, but they do not become conversion laws merely because they look authoritative.

## Public design skills reviewed

### `caorachel-lab/frontend-posters`
Useful patterns:
- fixed-canvas thinking;
- multiple materially distinct directions before selection;
- thumbnail inspection;
- rendered-output QA.

Not imported as universal rules:
- fixed CTA position;
- fixed text/fill ratio;
- one mandatory poster layout.

### `rahamanbinujit/claude-design-engine`
Useful patterns:
- squint test;
- grayscale hierarchy check;
- self-review / hierarchy debugging;
- anti-template thinking.

### `vanducng/skills` — marketing design
Useful patterns:
- art-direction vocabulary;
- campaign-oriented visual thinking;
- explicit design choices rather than generic rendering.

### `social-media-skills` / thumbnail-oriented workflows
Useful patterns:
- small-view legibility;
- persistent design grammar;
- strong focal hierarchy.

## User-supplied practitioner methodology — `ВИЗУАЛ И УПАКОВКА`

The 38-page presentation contributed a **meaning-first visual-development methodology**. It is not treated as peer-reviewed research or proof of advertising performance.

Transferred as production heuristics:
- “idea first, visual second”;
- task → idea → presentation → emotion → style/character → prompt/generation → selection → refinement → adaptation → final;
- separate semantic idea from visual embodiment;
- presentation modes chosen by communication task rather than what merely looks interesting;
- one clear focal idea/hero/emotion/visual language as a default complexity heuristic;
- negative/forbidden list as a first-class creative constraint;
- first generation is a draft, not the final design;
- campaign/system thinking instead of one-off images;
- visual-character matrix rather than a rigid list of styles;
- optional disruptive devices such as paradox, pain visualization, genre masks or personification as test hypotheses.

Implemented in:
- `references/idea-architecture-visual-character.md`;
- `references/creative-disruption-library.md`;
- `schemas/design-brief.schema.json`;
- `schemas/hero-generation-spec.schema.json`;
- `schemas/campaign-design-system.schema.json`;
- `scripts/freeze_preproduction_design.py`.

The style vocabulary is intentionally extensible because the user plans to provide additional banner-style examples. Those examples should enrich `VISUAL_CHARACTER`, `style_tags`, reference DNA, and possibly evaluation cases — not create a closed list of compulsory templates.

## User-supplied lighting methodology — `СВЕТ — 30 схем освещения`

The 30 practical lighting patterns remain a production vocabulary, not performance evidence.

The important architectural change is that lighting is no longer selected independently. It is downstream of meaning:

`CORE IDEA → PRESENTATION MODE → EMOTIONAL TARGET → VISUAL CHARACTER → PRIMARY AOI → LIGHTING INTENT → SCENE/COMPOSITION LIGHTING`

Implemented in:
- `references/lighting-intelligence.md`;
- `config/lighting-schemes.json`;
- `lighting_intent` in `design-brief.json`;
- campaign lighting inside `campaign-design-system.json`;
- representative/banner/pack review fidelity checks.

## Evidence discipline

Do not import these statements as universal facts:
- “brightest object is always seen first”;
- “emotion always sells better”;
- “visual paradox increases CTR”;
- “CTA should always be bottom-right”;
- “text should always occupy less than N%”;
- “one lighting scheme is best for a category”;
- “one visual style is inherently high-converting.”

Use them only as testable hypotheses when appropriate.
