# Intake and Banner Run Contract

This file defines the question pool and the run-freezing process used before banner production.

The skill should not interrogate the user mechanically. First inspect supplied context, files, brand docs, references, campaign material, and prior decisions. Build the full question pool internally, mark resolved fields, then ask only material unresolved questions.

## Question states

For every question use one state:

- `RESOLVED` — the answer is explicit and trustworthy.
- `MISSING` — required before production.
- `CONDITIONAL` — ask only if the related feature is used.
- `NOT_APPLICABLE` — irrelevant to this run.

## A. Deliverable questions — mandatory

These questions define what must actually be produced.

1. What Google ad mode is required?
   - Demand Gen image assets
   - Responsive Display assets
   - Uploaded Display static banners
   - HTML5/animated planning

2. How many materially different creative concepts are needed?

3. Which exact dimensions are needed?
   - explicit list, or
   - Google core pack, or
   - full pack

4. How many A/B variants are needed per concept/size?

5. How many languages/locales are required?

6. Does "N banners" mean:
   - N total files, or
   - N concepts repeated across all sizes?

7. What final formats are needed?
   - PNG
   - JPG
   - static GIF when supported
   - source/editable representation if applicable

8. Is a contact sheet/overview required? Default: yes for multi-banner runs.

## Output math

Keep these quantities separate:

- `C = concept_count`
- `S = size_count`
- `V = variant_count`
- `L = language_count`

Expected final raster files:

`TOTAL = C × S × V × L`

Example:

- 3 concepts
- 7 sizes
- 2 variants
- 1 language

`3 × 7 × 2 × 1 = 42 files`

Show this number to the user before production when the run is non-trivial.

If the user says "make 10 banners in 7 sizes" and the intended multiplication is unclear, return `OUTPUT_COUNT_AMBIGUOUS` and ask one clarifying question.

## B. Campaign purpose — mandatory unless already known

9. What is the campaign trying to achieve?
   - sale
   - lead
   - call/message
   - registration
   - app action
   - awareness
   - remarketing
   - another measurable action

10. What product/service is being promoted?

11. What landing page or destination is used?

12. Who is the target audience?

13. What geography matters?

14. What funnel/awareness state is this for?
   - cold/problem-aware
   - solution-aware
   - product-aware
   - remarketing
   - existing customer

15. What exact action should the user take after seeing the ad?

## C. Offer and message — mandatory

16. What is the primary proposition?

17. Is there a verified offer, price, promotion, deadline, or bonus?

18. What proof can be used?
   - factual differentiator
   - verified number
   - certification
   - real review/testimonial
   - warranty
   - case result
   - none

19. What CTA is approved?

20. Are legal disclaimers or mandatory statements required?

21. What claims, topics, or phrases are forbidden?

Do not invent a missing proof point merely to fill visual space.

## D. Brand and assets

22. Is there an existing `BRAND.md`, `ДИЗАЙН.md`, `DESIGN.md`, brand guide, or design system?

23. Which logo files and variants are approved?

24. Which fonts are approved/available?

25. Which brand colors are approved?

26. Are there real product/service photos?

27. May AI-generated hero images be used?

28. Are people/faces allowed or desired?

29. Are there brand-specific button, corner-radius, icon, photography, or retouching rules?

30. What visual elements must never be used?

If no formal design system exists, propose a temporary run-local system rather than silently inventing a permanent brand identity.

## E. Reference questions

Ask this block only when references exist or the user wants reference-driven work.

31. Which references should be analyzed?

32. For each reference, what does the user like?
   - composition
   - lighting
   - typography
   - color
   - density
   - premium feel
   - photography
   - CTA
   - overall mood
   - another feature

33. What does the user dislike or want changed?

34. How close should the result be?
   - mood only
   - design principles
   - similar composition logic
   - close reinterpretation while preserving own brand

35. Which reference is primary if references conflict?

36. Is any specific reference element mandatory?

The skill must extract transferable design principles into `REFERENCE_DNA`; it must not simply imitate the source.

## F. Visual and lighting questions

Ask only when the visual direction is not already determined.

37. What is the hero subject?
   - product
   - person
   - environment
   - interface/screenshot
   - abstract visual

38. What mood is required?
   - clean
   - premium
   - warm
   - trustworthy
   - energetic
   - technological
   - editorial
   - natural
   - dramatic
   - another

39. Are there material-specific lighting needs?
   - transparent glass/liquid
   - glossy bottle
   - metal/jewelry
   - matte packaging
   - food
   - fabric
   - skin/beauty
   - screen/device

40. Is a specific lighting style/reference required?

41. Should the image reserve a copy-safe zone? Where if known?

42. Are artificial glows, neon, god rays, hard shadows, or colored gels acceptable?

If no preference exists, the lighting director selects a scheme from `config/lighting-schemes.json` based on product material, mood, hierarchy, and copy-safe needs.

## G. Performance and iteration

Ask this block when prior campaign data exists.

43. Which existing creatives are winners/losers?

44. Which metric matters most?
   - CTR
   - conversion rate
   - CPA/CPL
   - ROAS/value
   - another

45. What audience/placement/context produced the result?

46. What variables were actually different between creatives?

Do not over-attribute performance to a visual element when multiple variables changed.

## H. Production constraints

47. Deadline or release date?

48. Naming convention?

49. Required source files or only final assets?

50. Any approval step before rendering the full pack?

51. Any external tool/model restrictions?

52. Any confidentiality or asset-use restrictions?

## Recommended user-facing intake behavior

### Quick run

If the user provided almost everything, ask only the unresolved blockers, often 2-5 questions.

### Standard run

Group the unresolved questions into one concise questionnaire with sections:
- campaign;
- offer;
- references/assets;
- deliverables.

### Deep run

Use when the user explicitly wants strategy/research or when the brief is high-risk/complex. Resolve the full applicable pool.

Do not ask one question at a time unless the user prefers an interview flow or a single answer determines many downstream questions.

## Freeze gate

Production starts only after the controller can freeze:

- `BUSINESS_BRIEF_ID`
- `BRAND_ID` or run-local brand state
- `REFERENCE_DNA_ID` or `NONE`
- Google mode/spec snapshot
- concept count
- size list
- variant count
- language count
- total expected files
- mandatory copy/offer/CTA
- allowed hero asset strategy
- output path convention

Then create the `BANNER_MATRIX`.

A later material change returns `DESIGN_CHANGED` and requires controller reconciliation rather than silent drift.
