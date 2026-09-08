# Intake and Banner Run Contract

This file defines the question pool and the run-freezing process used before banner production.

The skill should not interrogate the user mechanically. First inspect supplied context, files, brand docs, references, campaign material, landing pages and prior decisions. Build the full question pool internally, mark resolved fields, then ask only material unresolved questions.

A central rule from REAL-06:

> Product identity is not the same as the exact commercial job of the campaign.

For example, “Bitrix24” may be the product while the commercial job is license purchase, license renewal, purchase/renewal, implementation, or consultation. The skill must not silently choose among them.

Load `references/commercial-job-and-concept-exploration.md` whenever the exact transaction/service job or first-round visual direction is not already user-locked.

## Question states

For every question use one state:

- `RESOLVED` — the answer is explicit and trustworthy.
- `MISSING` — required before the relevant gate.
- `CONDITIONAL` — ask only if the related feature is used.
- `NOT_APPLICABLE` — irrelevant to this run.

Questions may declare `resolution = all` when several facts are jointly required. Q10 uses this so both broad product/service and exact commercial job must be known.

## A. Deliverable questions

1. What Google ad mode is required?
2. How many materially different **final production concepts** are needed after visual-direction selection?
3. Which exact dimensions or Google pack are needed?
4. How many A/B variants are needed per final concept/size?
5. Which languages/locales are required?
6. If the user says “N banners,” does this mean total files or concepts repeated across sizes?
7. What final raster format is needed?
8. Is a contact sheet required? Default: yes for multi-output runs.

### Final concept count != first-round exploration count

Keep these separate:

- `deliverables.concept_count` — how many concept systems will ultimately be produced/scaled;
- `visual_exploration_count` — how many alternative visual directions the user sees before selecting the system.

Default unlocked first round:

`visual_exploration_count = 3`

A campaign may end with `deliverables.concept_count = 1` after the user chooses one of those three.

## Output math

Keep separate:

- `C = final concept_count`
- `S = size_count`
- `V = variant_count`
- `L = language_count`

Expected final raster files:

`TOTAL = C × S × V × L`

Exploration previews are approval artifacts and are not included in final delivery count unless explicitly requested as final concepts.

If “10 banners in 7 sizes” is ambiguous, return `OUTPUT_COUNT_AMBIGUOUS` and ask one clarifying question.

## B. Campaign purpose and commercial job

9. What is the campaign trying to achieve?
   - sale;
   - lead;
   - call/message;
   - registration;
   - app action;
   - awareness;
   - remarketing;
   - another measurable objective.

10. What exact product/service **and commercial job** are being promoted?

The product/service and commercial job are both required.

Current normalized commercial-job examples:
- `NEW_LICENSE_PURCHASE`;
- `LICENSE_RENEWAL`;
- `PURCHASE_OR_RENEWAL`;
- `IMPLEMENTATION_SERVICE`;
- `CONSULTATION`;
- `OTHER`.

If `PURCHASE_OR_RENEWAL`, resolve whether purchase + renewal are:
- one `COMBINED` message; or
- `SEPARATE_VARIANTS`.

This is distinct from campaign objective and CTA.

Example:

```text
PRODUCT = Bitrix24 license
COMMERCIAL_JOB = PURCHASE_OR_RENEWAL
CAMPAIGN_OBJECTIVE = LEAD_GENERATION
CTA = Оставить заявку
```

11. What landing page/destination is used?
12. Who is the target audience?
13. What geography matters?
14. What funnel/awareness state is this for?
15. What exact action should the user take after seeing the ad?

After resolving Q10, create/validate `campaign-commercial-job.json` before creative strategy.

A material commercial-job correction invalidates stale idea/style/art-direction/visual-concept work instead of being treated as a copy tweak.

## C. Offer and message

16. What is the primary proposition?
17. Is there a verified price, promotion, deadline, bonus, or explicitly none?
18. What verified proof can be used, including explicitly none?
19. What CTA is approved?
20. Are legal disclaimers or mandatory statements required?
21. What claims/topics/phrases are forbidden?

Do not invent proof or commercial conditions merely to fill space.

## D. Brand and assets

22. Is there an existing `BRAND.md`, `ДИЗАЙН.md`, `DESIGN.md`, brand guide or design system, or explicitly none?
23. Which logo files/variants are approved, or explicitly none?
24. Which fonts are approved/available, or may a run-local fallback be used?
25. Which brand colors are approved, or may a run-local palette be proposed?
26. Are real product/service images available, including explicitly none?
27. May AI-generated hero images be used?
28. Are people/faces allowed or desired?
29. Are there brand-specific UI/photo/retouching rules?
30. What visual elements must never be used?

If no formal design system exists, propose a temporary run-local system rather than silently inventing permanent brand identity.

## E. Reference questions

Ask this block only when references exist or the user wants reference-driven work.

31. Which references should be analyzed?
32. What does the user like in them?
33. What should be changed/avoided?
34. How close should the result be?
35. Which reference is primary if they conflict?
36. Is any specific reference element mandatory?

Extract transferable `REFERENCE_DNA`; do not copy another brand literally.

## F. Visual and lighting questions

Ask only when genuinely unresolved or when the user's answer materially changes the output.

37. What is the hero subject?
38. What mood is required?
39. Are there material-specific lighting needs?
40. Is a specific lighting style/reference required?
41. Should the image reserve a copy-safe zone?
42. Are glows/neon/god rays/hard shadows/colored gels acceptable?

Do not re-ask these when the user has already supplied enough constraints for the controller to decide internally.

## G. Performance and iteration

Ask when prior campaign data exists.

43. Which existing creatives are winners/losers?
44. Which metric matters most?
45. What audience/placement/context produced the result?
46. What variables actually differed?

Do not over-attribute performance to one visual element when multiple variables changed.

## H. Production constraints

47. Deadline/release date?
48. Naming convention?
49. Required source files or only finals?
50. Is a user approval step required before the full pack? For this skill, visual approval is normally required unless the user explicitly delegates/locks a previously approved system.
51. External tool/model restrictions?
52. Confidentiality/asset-use restrictions?

## Recommended user-facing intake behavior

### Quick

If the user provided almost everything, ask only unresolved blockers, often 1–5 questions.

### Standard

Group unresolved material questions into one concise questionnaire.

### Deep

Use when explicitly requested or when the brief/policy/brand context is complex.

Do not ask one question at a time unless one answer determines many downstream branches.

## Freeze sequence

Before creative strategy can be treated as current, freeze at least:

- business/product identity;
- exact commercial job lock;
- campaign objective/audience/geography/landing page;
- commercial proposition/CTA/qualifiers;
- brand identity state;
- Google mode/spec snapshot;
- final concept count;
- size list;
- variant count;
- languages;
- expected final-file count;
- asset/truth constraints.

Then research/strategy may proceed.

Before first user-facing visual round, determine direction-lock provenance:

- `USER_LOCKED` -> one locked-direction visual concept may be rendered;
- otherwise -> `EXPLORE_3` and show three materially distinct rendered concepts.

A later material commercial-job change returns `COMMERCIAL_JOB_CHANGED` and invalidates stale downstream meaning/design artifacts rather than silently drifting.
