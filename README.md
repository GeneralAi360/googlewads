# Google Ads Performance Banner Designer

A production-grade AI skill for planning, designing, adapting, validating, and iterating performance advertising banners for Google Ads.

The project is broader than a legacy GDN banner prompt. It separates current Google asset-based formats from fully composed Uploaded Display creatives and treats visual design, platform compliance, exact dimensions, and performance learning as one system.

## Core pipeline

`Business context -> grounding -> creative angles -> hierarchy -> layout family -> deterministic composition -> visual QA -> Google preflight -> export -> performance learning`

## Current development branch

`dev/performance-banner-designer-v0.1`

## v0.1 contents

- `SKILL.md` — execution contract for the skill;
- `references/google-platform-specs.md` — current Google modes, dimensions, limits, and dynamic-refresh rule;
- `references/visual-attention.md` — eye tracking, banner blindness, gaze direction, AOIs, complexity;
- `references/typography-color-contrast.md` — serif/sans evidence, type hierarchy, size heuristics, contrast and color;
- `references/layout-families-and-density.md` — multi-format adaptation and information budgets;
- `references/rendering-and-validation.md` — deterministic composition and QA model;
- `references/research-sources.md` — evidence/source registry;
- `config/google-formats.json` — machine-readable Google format registry;
- `schemas/` — structured brief, concept, and output manifest contracts;
- `templates/BRAND.template.md` — persistent brand/design system for each business;
- `templates/CREATIVE_MEMORY.template.md` — learnings from real campaign performance;
- `scripts/validate_google_banner.py` — dependency-free static image preflight for dimensions, file type, file size, and animation state.

## Default Uploaded Display core pack

Current Google guidance for Uploaded Display creatives within Demand Gen recommends:

- 300x250
- 336x280
- 728x90
- 970x90
- 160x600
- 300x600
- 320x50

The skill does **not** resize one master design into these formats. It preserves one creative concept while rebuilding composition by layout family.

## Design evidence policy

Every rule is classified as:

1. platform requirement;
2. research evidence;
3. production heuristic;
4. test hypothesis.

This prevents common mistakes such as treating a responsive-image blank-space recommendation as a universal fill percentage, or claiming that one font category or CTA color always performs best.

## Validator

Example:

```bash
python scripts/validate_google_banner.py outputs/banner_300x250.png --mode demand_gen_uploaded_display --pack core
```

The validator uses a conservative 150,000-byte ceiling for Google's stated 150 KB static uploaded-display limit. It recognizes PNG, JPEG, and GIF without third-party packages and detects animated GIF/APNG for modes that require static images.

## Roadmap

See `docs/ROADMAP.md`.
