# Visual review evaluation contract

This file defines how `DESIGN_REVIEWER` / `PACK_REVIEWER` quality should be evaluated beyond deterministic schema checks.

## Why this exists

A renderer can prove dimensions, file size, copy identity, contrast samples and hashes. It cannot by itself prove that a banner has good visual hierarchy, that a crop preserves product comprehension, or that a campaign pack feels visually coherent.

The visual reviewer therefore has a separate judgment role. The eval fixtures in `evals/visual-review-evals.json` encode known visual defects and expected findings.

## Independence rule

The reviewer must receive the rendered artifact and task-local frozen context, but **must not receive `expected_findings` or scoring keys before writing the review**.

A review is not independent when the same context that produced the banner is simply asked to approve itself without a fresh visual pass. When a host cannot provide fresh visual context, report degraded rigor rather than pretending independence.

## Required reviewer inputs

For a single banner:
- exact rendered image at actual dimensions;
- dimension and layout family;
- frozen creative-contract excerpt: proposition, CTA, scan path, approved copy;
- relevant brand/design tokens only;
- relevant lighting/reference directive only;
- review checklist.

For a pack:
- contact sheet;
- individual files when the contact sheet hides actual-size problems;
- frozen campaign identity/tokens;
- manifest with dimension/job IDs.

## Required output

Each finding must contain:
- severity: `CRITICAL | IMPORTANT | MINOR`;
- stable finding code;
- visible evidence tied to the artifact;
- why it matters to comprehension/brand/legibility/hierarchy;
- smallest useful correction;
- whether the issue is banner-local or campaign-wide.

The reviewer must not claim conversion/CTR effects unless actual campaign evidence exists.

## Current eval set

`VR-01` photographic copy-zone glare — tests local legibility judgment.

`VR-02` logo dominance — tests AOI/hierarchy judgment without applying a universal logo-size rule.

`VR-03` destructive focal crop — tests whether the reviewer notices loss of essential product comprehension.

`VR-04` overloaded 320x50 — tests density adaptation rather than fixed fill-percentage thinking.

`VR-05` decorative lighting stealing focal priority — tests whether light is judged as hierarchy, not decoration.

`VR-06` cross-size design drift — tests pack-level consistency without demanding identical geometry across aspect ratios.

## Pass criteria

For the fixture suite:
- all expected `CRITICAL` findings must be detected;
- at least 80% of expected `IMPORTANT` findings must be detected;
- zero unsupported false `CRITICAL` findings;
- every finding must cite visible evidence;
- reviewer must avoid the fixture's listed `must_not_claim` statements.

These thresholds are an evaluation contract, not a scientific statement about advertising performance.
