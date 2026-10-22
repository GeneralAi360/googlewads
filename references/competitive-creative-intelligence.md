# Competitive Creative Intelligence

This reference defines the mandatory market/design research layer before unresolved art direction is rendered at scale.

## Purpose

A banner system can be technically correct and still look amateur, generic, or category-inappropriate. Before art direction is selected, the controller must understand how the category communicates commercially and visually.

The objective is not to copy competitors. The objective is to extract:
- commercial patterns;
- category trust signals;
- mature visual language;
- recurring hero strategies;
- proof/CTA conventions;
- useful whitespace/density patterns;
- obvious category clichés and weak generic-AI patterns;
- design opportunities that remain differentiated.

## Source priority

When live web access exists, prefer actual advertising evidence over inspiration galleries.

Suggested source order:
1. official ad libraries/transparency products for the target platform;
2. official ad libraries of adjacent B2B/social platforms when the category is better represented there;
3. verified own campaign creative + metrics;
4. published case studies with attributable metrics;
5. specialist ad-intelligence/swipe services such as Foreplay, AdPlexity, Motion, or current equivalents;
6. competitor landing pages/product pages;
7. design galleries / public GitHub design-methodology repositories as craft references only.

Examples and capabilities change. Resolve current availability at execution time rather than treating a service name as a permanent dependency.

## Research roles

Use one narrow `COMPETITOR_RESEARCHER` context per target/query when real isolated contexts exist. The controller synthesizes the results.

A researcher records what is actually visible and the source identity. It does not invent performance.

## Performance-evidence tiers

Every observed ad gets exactly one tier:

- `A_VERIFIED_OWN_METRICS` — first-party campaign metrics available to the user/system.
- `B_PUBLISHED_CASE_METRICS` — attributable public case with actual metrics.
- `C_PLATFORM_PERFORMANCE_SIGNAL` — the platform itself labels or surfaces the creative as high/top performing. This is a platform signal, not proof of conversion rate.
- `D_MARKET_PROXY` — longevity, many variants, broad placement, or other market proxy.
- `E_DESIGN_REFERENCE_ONLY` — visual/copy reference without performance evidence.

Never call an ad "high-converting" unless conversion performance is actually supported by tier A or B evidence and the cited metric is conversion-related. Tier C may be described only as a platform performance signal. Tiers D/E are not performance claims.

## Required output: COMPETITIVE_CREATIVE_RESEARCH

Record for each creative:
- source / URL / advertiser;
- observed creative type;
- commercial angle;
- hero type;
- composition/alignment;
- typography behavior;
- palette/contrast;
- CTA treatment;
- whitespace/information density;
- trust signals;
- image/UI/illustration treatment;
- lighting when meaningful;
- performance-evidence tier and evidence note;
- transferable principles;
- literal elements not to copy.

`FULL` research coverage currently requires at least three relevant creatives across at least two advertisers/independent targets. This is a production coverage heuristic, not a scientific law. When the market cannot supply that evidence, use `DEGRADED` and require explicit degraded acceptance before freeze.

## Category Design Map

The controller synthesizes research into a `CATEGORY_DESIGN_MAP`.

It should answer:
- What makes category advertising look trustworthy/mature?
- What signals enterprise / premium / technical / consumer / promotional positioning?
- Which hero treatments are common?
- Which patterns are overused?
- Which generic-AI patterns would make the work look cheap?
- Which visual opportunity is differentiated while remaining legible for the category?

The map is not a style preset. It is evidence and constraint context for art direction.

## Detailed Design Brief

Before any art-direction preview is rendered, produce `design-brief.json` containing at minimum:
- campaign and audience;
- commercial message;
- brand context;
- research/category-map identity;
- primary AOI and intended scan path;
- hero/image strategy;
- asset-quality policy;
- typography strategy;
- palette/contrast strategy;
- lighting strategy;
- whitespace/information-density behavior;
- small-format removal policy;
- exact output matrix summary;
- review requirements.

## Written art-direction gate

For unresolved style, generate three **written** art-direction specifications first. Each candidate must state:
- visual thesis;
- composition system;
- hero strategy;
- typography character/hierarchy;
- palette relationship;
- lighting/image treatment;
- graphic device;
- trust signals;
- whitespace character;
- explicit anti-patterns.

Do not render previews until the written direction is approved by the user or a genuinely independent `ART_DIRECTOR_REVIEWER` in unattended mode.

## Representative high-fidelity gate

After written approval, render exactly one representative high-fidelity format for the selected direction (normally 300x250 unless another format is materially more representative).

This is not a sketch. It must be close to production quality and use final/approved assets where available.

Before full-pack scale-out, the representative artifact must pass:
- asset quality / resolution;
- professional category fit;
- no generic AI clipart / toy-clay styling unless explicitly approved;
- hierarchy;
- typography;
- brand fidelity;
- commercial message fidelity;
- crop/hero quality;
- lighting/contrast;
- CTA clarity.

The approval is SHA-256-bound to the exact representative file. Changing the file invalidates approval.

## Asset quality gate

By default reject:
- visibly low-resolution or stretched raster assets;
- screenshot/compression artifacts used as hero imagery;
- obvious generic AI clipart;
- toy/clay iconography without an explicit art-direction reason;
- inconsistent illustration/render styles within one campaign;
- placeholder/fake logos;
- generic stock that weakens category credibility;
- generated imagery that does not match the approved visual thesis.

A tiny final Google format is not an excuse for a low-quality source asset. Render/composite from sufficiently clean source material and downsample deliberately.

## No scale-out before approval

The full banner matrix may exist as a planning artifact, but `BANNER_DESIGNER` jobs for the full pack must not be dispatched until `PREPRODUCTION_FROZEN` proves:

`competitive research -> category map -> detailed design brief -> written art-direction approval -> representative high-fidelity approval`.
