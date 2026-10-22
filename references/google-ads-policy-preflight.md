# Google Ads policy preflight

Snapshot reviewed: **2026-09-07**.

This layer is separate from pixel/file technical validation. A creative can satisfy dimensions, file size and format and still be disapproved by Google Ads policy.

## Authority and freshness

At execution time, prefer the current English-language Google Advertising Policies Help Center. Google states that the English policy text is the official language used for enforcement.

Local policy files are a dated snapshot and must not be presented as permanently current. If web access exists, refresh material policy families before a real production delivery, especially for regulated or sensitive verticals.

Primary official policy families for image/display creative preflight:
- Image ad requirements;
- Image quality / Editorial;
- Misrepresentation;
- Misleading ad design;
- Unreliable claims;
- Unclear relevance;
- Unavailable offers;
- Destination requirements;
- Trademarks;
- Inappropriate content;
- restricted vertical policies and certifications when applicable;
- personalized advertising / targeting restrictions when applicable.

## No approval guarantee

`GOOGLE_POLICY_PREFLIGHT_PASS` means the local skill found no unresolved blocker in the evidence it was given. It does **not** guarantee Google approval.

Google can review the ad, landing page, account, advertiser identity, targeting, geography and third-party information. Some rules require account-level eligibility, certification or jurisdiction-specific review that a local banner validator cannot prove from pixels alone.

Never say:
- "Google will definitely approve this";
- "100% policy safe";
- "guaranteed to pass moderation".

Preferred wording:
- "No blocking issue found in the current Google Ads policy preflight; final Google review still applies."

## Two-stage policy workflow

### A. PRE-RENDER POLICY RISK SCREEN

Before art direction is approved, classify:
- advertised vertical/product;
- target countries;
- sensitive/restricted category possibility;
- commercial claims and their sources;
- third-party brands/trademarks;
- offer/price/discount availability;
- landing-page relevance;
- whether special certification/age/geography/targeting restrictions may apply.

A restricted/sensitive vertical that has not been resolved must return `POLICY_REVIEW_REQUIRED`, not proceed by assumption.

### B. FINAL CREATIVE + DESTINATION PREFLIGHT

Run against the final exported banner, exact copy, exact business identity and final landing page.

It must cover the policy families below.

## Misleading ad design — especially important for banners

Current Google policy examples include disallowing image ads that resemble system/site warnings, messages/dialogs/menus/request notifications, contain non-functional UI controls, download/install buttons or icons, transparent backgrounds, segmented images, repeated copies that look like multiple ads, moving/clicking arrows, or standalone buttons whose context/function is unclear or whose prominence is disproportionate.

Policy preflight therefore requires explicit visual review fields for:
- system-warning mimicry;
- fake dialog/menu/request notification;
- non-functional input/radio/checkbox/close controls;
- download/install button/icon;
- misleading arrows or pseudo-interactions;
- transparent-background image ad;
- segmented/multi-ad appearance;
- disproportionate/contextless standalone button.

A normal clearly contextual CTA such as `Получить консультацию` can be acceptable as part of a coherent advertisement; the gate is about misleading/non-functional design, not a blanket ban on CTA treatment.

## Image quality / editorial

Block or require revision for:
- sideways/upside-down output;
- image not filling the chosen ad canvas when the format requires full coverage;
- blurry/unclear/unrecognizable imagery;
- illegible essential text;
- strobing/flashing/distracting visual behavior;
- expansion/encroachment outside the ad frame;
- punctuation/capitalization/editorial abuse when applicable.

This skill may deterministically verify exact geometry/file properties, but blur, recognizability, misleading visual design and some editorial judgments remain semantic visual-review responsibilities.

## Misrepresentation and claims

Every material commercial claim must be grounded.

Block:
- inaccurate or improbable expected outcomes presented as likely;
- unsupported guarantees;
- fabricated reviews/ratings/certifications;
- false affiliation/endorsement;
- inaccurate advertiser/business identity;
- deceptive manipulated media;
- omission of material qualifiers when their omission changes the offer meaning.

For third-party implementation/reseller advertising, be explicit about the advertiser's role when needed and avoid implying official affiliation unless verified.

## Unavailable offer and unclear relevance

The exact advertised offer, price, promotion, product/service and CTA should be available and easy to find/use at the destination.

Block when:
- advertised offer is expired/unavailable;
- price is inaccurate;
- CTA action cannot reasonably be completed from the landing page;
- destination does not accurately describe the advertised product/service;
- landing page and banner represent different advertisers/products without clear explanation.

## Destination requirements

The destination should be:
- working on common browsers/devices;
- accessible in the target location;
- crawlable by Google AdsBot;
- consistent with the final/display URL and redirect rules;
- useful and navigable;
- not merely a bridge/doorway/parked/under-construction page;
- sufficiently original/useful.

A local preflight may record verified HTTP/domain observations, but Google AdsBot-specific or account-specific results can still differ at enforcement time.

## Trademarks and third-party product brands

Third-party trademarks are not automatically forbidden, but use can be restricted after a complaint, especially for direct competitors or confusing/deceptive use.

For a reseller/integrator concept such as advertising Bitrix24:
- store the trademark/brand used;
- store the asserted relationship/basis for use;
- verify the landing page clearly represents the advertiser and its relationship to the product/service;
- never imply endorsement/official-partner status unless verified.

`TRADEMARK_REVIEW_REQUIRED` is preferable to inventing authorization.

## Restricted/sensitive content

The controller must classify the vertical before delivery. Examples that can require special policy handling include healthcare/medicines, alcohol, gambling, financial services, political content, sexual content, dangerous products/services and other restricted categories.

Do not encode a single static universal rule for all countries. Store target geography and applicable certification/restriction state, and refresh the relevant current policy at execution time.

## Personalized advertising is separate from creative approval

Some sensitive-interest rules concern targeting/personalization rather than whether a raster banner is visually acceptable. Keep these states separate:
- `CREATIVE_POLICY`;
- `DESTINATION_POLICY`;
- `VERTICAL_CERTIFICATION`;
- `TARGETING_POLICY`;
- `ACCOUNT_ELIGIBILITY`.

A banner can be visually acceptable while the campaign is restricted from personalized targeting.

## AI-generated/edited assets

When AI-generated or AI-edited assets are used, record it. Google currently exposes AI content label settings and notes that some jurisdictions require disclosures/labels. This is not a substitute for legal review. Never claim the local skill proves jurisdictional AI-label compliance.

## Required machine-readable artifacts

- `google-policy-context.json` — controller/reviewer evidence and declarations;
- `google-policy-report.json` — deterministic policy gate output;
- optional source snapshot/config under `config/google-ads-policy-snapshot.json`.

## Status semantics

- `GOOGLE_POLICY_PREFLIGHT_PASS` — no unresolved blocker in supplied evidence;
- `GOOGLE_POLICY_PREFLIGHT_BLOCKED` — one or more known blocking issues;
- `GOOGLE_POLICY_PREFLIGHT_INCOMPLETE` — required evidence is missing/unknown;
- `POLICY_REVIEW_REQUIRED` — sensitive/restricted or ambiguous category needs current policy resolution.

Only `GOOGLE_POLICY_PREFLIGHT_PASS` may feed the final Google-ready precheck, and even then final Google review still applies.
