# Google Ads Performance Banner Designer

A production-grade AI skill for researching, planning, designing, adapting, rendering, reviewing, validating, and iterating performance advertising banners for Google Ads.

The system is intentionally broader than a GDN prompt. It separates business facts, market/category evidence, design decisions, approvals, production jobs, rendered artifacts, technical validation, visual review, and later campaign learning into explicit contracts.

## Canonical pipeline

```text
context
→ structured intake
→ run freeze + banner matrix
→ supplied-reference DNA
→ competitive creative research
→ category design map
→ detailed design brief
→ 3 written art directions when style is unresolved
→ written art-direction approval
→ 1 high-fidelity representative design
→ representative-design approval
→ PREPRODUCTION_FROZEN
→ frozen creative contracts
→ one job per final output
→ deterministic render
→ Google technical preflight
→ manifest/contact sheet
→ actual/grayscale/squint/thumbnail QA
→ independent banner reviews
→ pack review
→ readiness gate
→ delivery
→ performance learning
```

The full pack is deliberately **not** rendered before the representative design is approved.

## Current development

Branch: `dev/performance-banner-designer-v0.2`

Draft PR: `#2`.

`main` remains unchanged. v0.2 is in active hardening after a real Work acceptance test exposed a weak preproduction design path.

## REAL-01 — why the pipeline changed

The first real B2B Work test produced three 300x250 preview directions that were technically valid but visually weak: nearly the same layout grammar, generic/toy-like cloud imagery, insufficient category maturity, and no competitor/category advertising research before rendering.

That failure is now a permanent regression case in `evals/real-world-failures.json`.

The system now blocks the behavior that caused it:
- unresolved art direction cannot be rendered before competitive/category research;
- three visual directions must first exist as materially different **written specifications**;
- the written direction must be approved before image generation;
- exactly one high-fidelity representative design must be approved before full-pack scale-out;
- asset quality, professional category fit, and anti-generic-AI quality are explicit gates.

## Structured intake and run freeze

`config/intake-question-pool.json` contains the 52-question internal pool. `scripts/plan_banner_intake.py` marks questions `RESOLVED`, `MISSING`, `CONDITIONAL`, or `NOT_APPLICABLE` and asks only unresolved material questions.

The planner keeps concept, size, variant, language, and final-file counts separate. Ambiguous requests such as “10 banners in 7 sizes” block instead of guessing.

`scripts/freeze_banner_run.py` freezes Google mode/spec snapshot, exact sizes, output math, context SHA-256 and the immutable `banner-matrix.json`.

The matrix is a completion/planning artifact at this stage. It does **not** authorize scale-out.

## Supplied references

One narrow `REFERENCE_ANALYST` may be used per supplied reference. `REFERENCE_DNA` captures composition, hierarchy, typography, palette, whitespace, CTA behavior, crop, image treatment, lighting, transferable principles and literal elements that must not be copied.

## Competitive Creative Intelligence

`references/competitive-creative-intelligence.md` defines the mandatory market/category research layer for unresolved/new advertising design.

When live access exists, prefer actual advertising evidence from current official ad libraries/transparency products, then first-party performance data/published cases, then specialist ad-intelligence/swipe services and competitor product/landing pages. Public design repositories and galleries remain craft references rather than performance proof.

`scripts/materialize_competitive_research_jobs.py` creates one read-only `COMPETITOR_RESEARCHER` task per target/query.

The machine-readable result follows `schemas/competitive-creative-research.schema.json`.

### Performance evidence is explicit

Observed ads receive one tier:
- `A_VERIFIED_OWN_METRICS`
- `B_PUBLISHED_CASE_METRICS`
- `C_PLATFORM_PERFORMANCE_SIGNAL`
- `D_MARKET_PROXY`
- `E_DESIGN_REFERENCE_ONLY`

A reference is never called **high-converting** merely because it is attractive, long-running, frequently seen, or present in a swipe library. Conversion claims require actual conversion-related tier A/B evidence.

`FULL` research currently requires at least three relevant creatives across at least two advertisers/independent targets. This is a coverage heuristic, not a scientific performance law. Insufficient market evidence becomes `DEGRADED` and requires explicit acceptance.

## Category Design Map

`schemas/category-design-map.schema.json` turns raw competitor observations into category-level design context:
- mature category signals;
- dominant visual/commercial patterns;
- hero strategies;
- trust signals;
- category clichés;
- generic-AI risks;
- differentiated opportunities;
- careful performance-evidence interpretation.

This map informs art direction but is not a template to copy.

## Detailed design brief

Before preview rendering, `design-brief.json` follows `schemas/design-brief.schema.json` and binds to the exact competitive-research and category-map hashes.

It captures campaign/audience/message, brand context, art-direction strategy, primary AOI and scan path, image/hero strategy, typography, palette/contrast, layout/alignment/whitespace, scene/composition lighting, information density, small-format simplification, exact output matrix and review requirements.

### Asset-quality policy

The design brief must explicitly reject by default:
- visibly low-resolution or stretched raster assets;
- generic AI clipart;
- toy/clay 3D styling unless that look was deliberately approved;
- inconsistent illustration/render styles across the campaign;
- fake/placeholder logos in final work;
- imagery that fails professional category fit.

A final 300x250 file is small, but its source assets still need to be production quality.

## Written art direction before images

Visual direction is resolved through:
- `ART_DIRECTION_LOCKED`
- `ART_DIRECTION_PREVIEW_3`
- `ART_DIRECTION_AUTOSELECT_3`

For preview/autoselect modes, three **written** candidate systems are produced first. They must differ materially in composition, hero strategy, typography, palette relationship, image/lighting treatment, graphic device, trust signals, whitespace character and anti-patterns. A color swap or a different right-side icon is not a new art direction.

The selected written direction is recorded in `art-direction-approval.json` and bound to the exact design-brief SHA via `schemas/art-direction-approval.schema.json`.

## One high-fidelity representative before scale-out

After written approval, the controller renders one representative format—normally 300x250 unless another format is more informative.

This is not a rough moodboard thumbnail. It is intended to be close to production quality.

`representative-design-approval.json` must pass:
- asset quality;
- professional category fit;
- hierarchy;
- typography;
- brand fidelity;
- commercial-message fidelity;
- hero/crop quality;
- lighting/contrast;
- CTA clarity;
- anti-generic-AI quality.

The approval is SHA-256-bound to the exact representative artifact. Changing the image invalidates the approval.

## Preproduction freeze

`scripts/freeze_preproduction_design.py` binds the exact chain:

```text
competitive research
→ category design map
→ design brief
→ written art-direction approval
→ representative-design approval
→ exact banner matrix
```

A successful result is `PREPRODUCTION_FROZEN`.

It fails closed on stale hashes, unaccepted degraded research, unsupported performance claims, weak coverage, output-matrix mismatch, missing asset-quality policy, incomplete written direction, failed representative checks, missing artifact, or changed representative bytes.

## Frozen creative contracts

Normal production creative freeze now consumes the preproduction freeze:

```bash
python scripts/freeze_creative_contracts.py \
  --matrix run/freeze/banner-matrix.json \
  --contracts-dir run/creative-contracts \
  --preproduction-freeze run/preproduction-freeze.json \
  --out run/creative-freeze.json
```

The creative contract cannot silently switch to another `art_direction_id`. Its preproduction lineage is propagated into per-banner render-spec provenance.

## Matreshka-style production jobs

Only after the preproduction/creative gates pass does `scripts/materialize_banner_jobs.py` become the full-pack production handoff.

One matrix row = one traceable final banner job. A `BANNER_DESIGNER` receives only job-local frozen context and may not redefine offer, CTA, brand, concept, approved art direction or dimensions.

For `3 concepts × 7 sizes × 2 variants × 1 language`, the system expects exactly 42 final files and 42 jobs.

## Deterministic renderer and lighting

`scripts/render_banner.py` uses Pillow for exact PNG/JPG composition. It owns approved typography/logo, layout, focal crop, composition lighting, dimensions and bounded compression.

Explicit failures include `FAIL_COPY_OVERFLOW`, `FAIL_LAYOUT`, `FAIL_CONTRAST`, `FAIL_LOCAL_CONTRAST`, `FAIL_FILE_SIZE`, and `FAIL_ASSET`.

The 30 lighting schemes are production heuristics. The system separates `SCENE_LIGHTING` from `COMPOSITION_LIGHTING`; implemented primitives include edge glow, spotlight, copy scrim, vignette and text plate. Lighting may support hierarchy but never becomes a claimed conversion law.

## Google technical pack

`scripts/render_banner_pack.py` validates matrix/spec identity and creative/art-direction binding, renders every row, calls `scripts/validate_google_banner.py`, creates a contact sheet and writes a provenance manifest only for a technically passing pack.

Technical Google PASS is not design PASS.

## Diagnostic visual QA and final review

`scripts/build_design_qa_views.py` produces review-only actual/grayscale/squint/25%-thumbnail evidence bound to the exact output SHA.

Every final `DESIGN_REVIEWER` checks concept/brand fidelity, **asset quality, professional category fit, anti-generic-AI quality**, hierarchy, lighting, typography, actual-size readability, thumbnail/grayscale/squint behavior, contrast, density, crop/safe zones and CTA clarity.

A final `PACK_REVIEWER` checks cross-size concept/brand/design grammar, lighting consistency where relevant, intentional recomposition, small-format simplification, duplicates/missing outputs and generic/template drift.

`scripts/assess_pack_readiness.py` keeps `delivery_status` separate from `run_rigor`. A changed output invalidates its old visual evidence/review.

## Canonical seven-format E2E

`scripts/demo_end_to_end.py` now exercises the synthetic full deterministic chain:

```text
intake
→ run freeze
→ synthetic competitive research
→ category design map
→ detailed design brief
→ written 3-direction approval
→ 300x250 representative approval
→ PREPRODUCTION_FROZEN
→ creative/art-direction freeze
→ per-job binding
→ 7 deterministic renders
→ real Google validator
→ manifest/contact sheet
→ design-QA views
→ 7 DESIGN_REVIEWER tasks + pack-review task
```

It deliberately does not fabricate reviewer reports or advertising-performance evidence.

## Google static core pack

- 300x250
- 336x280
- 728x90
- 970x90
- 160x600
- 300x600
- 320x50

One design grammar is preserved while each layout family is recomposed; the representative banner is never mechanically resized into the pack.

## Validation status

The deterministic code milestone containing the new preproduction gates has passed GitHub Actions. `docs/v0.2-release-gate.md` intentionally keeps v0.2 blocked until the same class of real Work task that produced `REAL-01` is re-run successfully and the remaining independent visual/repository review gates are satisfied (or degraded rigor is explicitly accepted).

Do not merge `main` merely because CI is green.
