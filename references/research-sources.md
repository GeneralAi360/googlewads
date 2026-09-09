# Research and evidence sources

This file records the source hierarchy used by `performance-banner-designer`.

## Source classes

### PLATFORM REQUIREMENT
Current official platform documentation. Mandatory when applicable.

Examples:
- Google Ads creative dimensions/types/byte limits;
- current animation constraints;
- current Google Advertising Policies.

At execution time, current official documentation outranks dated local snapshots.

### RESEARCH EVIDENCE
Peer-reviewed or otherwise credible empirical research used contextually.

Examples:
- visual-attention / eye-tracking research;
- typography/readability research.

Research results must not be converted into universal layout or conversion laws.

### PRODUCTION HEURISTIC
Practitioner/design methodology that can improve workflow but does not prove performance.

Examples:
- lighting-scheme vocabulary;
- squint/grayscale/thumbnail checks;
- focus-budget heuristics;
- current style taxonomy;
- fixed-canvas design practices.

### TEST HYPOTHESIS
A plausible creative idea that should be validated in campaign data rather than stated as a fact.

Examples:
- a visual paradox may increase stopping power;
- product-proof execution may outperform an abstract metaphor in a given category.

## Competitor-performance evidence tiers

- `A_VERIFIED_OWN_METRICS`;
- `B_PUBLISHED_CASE_METRICS`;
- `C_PLATFORM_PERFORMANCE_SIGNAL`;
- `D_MARKET_PROXY`;
- `E_DESIGN_REFERENCE_ONLY`.

Do not call a creative high-converting without appropriate conversion-related A/B evidence.

## Current Google technical sources

Primary local snapshot:
- `references/google-platform-specs.md`;
- `config/google-formats.json`.

Refresh official Google documentation at execution time when possible.

## Current Google Advertising Policy sources

Primary local policy snapshot:
- `references/google-ads-policy-preflight.md`;
- `config/google-ads-policy-snapshot.json`.

The snapshot reviewed current official English Google Advertising Policy pages on 2026-09-07, including relevant policy families for image/display advertising:
- Image ad requirements;
- Image quality;
- Misrepresentation;
- Misleading ad design;
- Unreliable claims;
- Unclear relevance;
- Unavailable offers;
- Destination requirements;
- Trademarks;
- Inappropriate content;
- restricted/sensitive categories and certifications when applicable;
- personalized advertising/targeting restrictions when applicable.

English Google Advertising Policy text is treated as the policy enforcement source of truth. Translated/local guidance is useful to the user but must not silently override the English policy rule.

The local snapshot has a freshness policy. Restricted/sensitive categories require live/current policy resolution rather than assuming an old cached rule remains valid.

## Policy evidence is not performance evidence

Keep policy and conversion evidence independent.

`GOOGLE_POLICY_PREFLIGHT_PASS` means no unresolved blocker was found in the evidence provided to the local policy gate. It does not predict CTR/CVR and does not guarantee Google approval.

Google policy assessment can depend on:
- exact creative;
- landing page/destination;
- advertiser/business identity;
- account verification/eligibility;
- target geography;
- certification;
- targeting/personalization;
- trademark complaints/relationship;
- third-party information.

Therefore never convert local policy checks into an approval probability.

## User-provided design methodology sources

The user-supplied lighting guide and visual-packaging presentation are retained as practitioner methodologies with explicit production-heuristic status.

Their strongest reusable ideas are integrated into:
- `references/lighting-intelligence.md`;
- `references/idea-architecture-visual-character.md`;
- `references/creative-disruption-library.md`.

## September 2026 Style Intelligence sources

Current style/currentness research is summarized in:
- `references/style-intelligence-2026.md`;
- `config/style-intelligence-library.json`.

Currentness is intentionally a subordinate ranking factor. It must not override category fit, product truth, attention hierarchy, typography, lighting or multi-format resilience.

## Audit rule

Every significant rule used by the system should be traceable to one of these classes. If its evidence status is unclear, downgrade it to a production heuristic or test hypothesis rather than overclaiming certainty.
