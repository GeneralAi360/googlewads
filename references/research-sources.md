# Research and platform source registry

Last reviewed: 2026-09-04.

This file records provenance for the rules used by the skill. Re-check live platform pages before production because platform requirements change.

## Official Google Ads sources

### Uploaded display ads specifications
https://support.google.com/google-ads/answer/1722096

Used for:
- GIF/JPG/PNG uploaded image-ad formats;
- 150 KB file-size limit;
- full uploaded-display dimension table;
- general animated GIF constraints;
- HTML5 size references.

### Demand Gen — image assets and uploaded display
https://support.google.com/google-ads/answer/17140672

Used for:
- current Uploaded Display support on GDN inventory within Demand Gen;
- current seven recommended uploaded-display sizes;
- up to 20 assets;
- static/non-animated condition for this mode;
- 150 KB limit.

### Responsive Display best practices
https://support.google.com/google-ads/answer/9823397

Used for:
- no overlaid logos;
- avoid overlaid text;
- no fake overlaid buttons;
- product/service focus;
- blank-space guidance;
- avoid collages/composite backgrounds.

### Responsive Display specs
https://support.google.com/google-ads/answer/17090561

Used for current Responsive Display text-asset limits.

### Create a Responsive Display ad
https://support.google.com/google-ads/answer/7005917

Used for image/logo dimensions and file-size guidance.

### Demand Gen campaign specs
https://support.google.com/google-ads/answer/17091672

Used for:
- 40-character Demand Gen headlines;
- 30-character-or-shorter Display-serving note;
- 90-character descriptions;
- business-name limit;
- common Demand Gen image ratios.

### Demand Gen creative asset guidelines
https://support.google.com/google-ads/answer/13704860

Used for current recommended Demand Gen image sizes and ratios.

## Eye tracking and visual attention

### Peker, Dalveren & Inal (2021)
"The Effects of the Content Elements of Online Banner Ads on Visual Attention: Evidence from An-Eye-Tracking Study"
Future Internet, 13(1), 18.
https://doi.org/10.3390/fi13010018
https://www.mdpi.com/1999-5903/13/1/18

Relevant evidence:
- image area attracted the most attention among image/brand/discount AOIs in the study;
- middle areas were noticed first;
- left areas tended to be noticed earlier than right;
- discount magnitude and brand familiarity changed attention patterns.

Limit: one study/context is not a universal positioning law.

### Palcu, Sudkamp & Florack (2017)
"Judgments at Gaze Value: Gaze Cuing in Banner Advertisements, Its Effect on Attention Allocation and Product Judgments"
Frontiers in Psychology, 8:881.
https://doi.org/10.3389/fpsyg.2017.00881
https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2017.00881/full

Relevant evidence:
- gaze toward product increased likelihood of looking at product;
- gaze direction affected purchase intention in the experiment;
- animated face banners attracted more attention than static versions.

Limit: do not infer that every banner needs a face or animation.

### Visual complexity study (2023)
"Effects of Visual Complexity of Banner Ads on Website Users’ Perceptions"
Applied Sciences, 13(24), 13317.
https://www.mdpi.com/2076-3417/13/24/13317

Relevant evidence:
- high-complexity ads could be noticed slightly faster but received less sustained fixation/looking and were judged less appealing in the study;
- supports complexity control, not sterile minimalism as a universal rule.

## Typography

### Arditi & Cho — Serifs and font legibility
https://pmc.ncbi.nlm.nih.gov/articles/PMC4612630/

Relevant evidence:
- no continuous-reading-speed effect attributable simply to serifs;
- no universal serif/sans superiority can be claimed from category alone.

### Daxer et al. (2022)
"Towards a standardisation of reading charts: Font effects on reading performance—Times New Roman with serifs versus the sans serif font Helvetica"
https://pmc.ncbi.nlm.nih.gov/articles/PMC9804255/

Relevant evidence:
- no significant reading-time/speed difference in the controlled comparison described;
- actual font and layout matter.

### Vecino et al. (2022)
"How does serif vs sans serif typeface impact the usability of e-commerce websites?"
https://pmc.ncbi.nlm.nih.gov/articles/PMC9680897/

Relevant evidence:
- study did not find serif/sans category to determine usability/reading speed in the tested e-commerce prototype.

## Contrast / accessibility

### WCAG 2.2 — Contrast Minimum
https://www.w3.org/TR/WCAG22/#contrast-minimum
https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html

Internal QA targets derived from the standard:
- 4.5:1 normal text;
- 3:1 large-scale text;
- logotype exception acknowledged.

Use as readability QA guidance. Do not misrepresent it as a Google Ads raster-banner submission requirement.

## External skill inspirations

### coreyhaines31/marketingskills — ad-creative
https://github.com/coreyhaines31/marketingskills/tree/main/skills/ad-creative

Ideas adopted at architectural level:
- grounded inputs;
- concept generation before production;
- iterative performance loop;
- separating winning patterns from new exploration;
- source-grounded claims.

Do not copy template rankings blindly from Meta into Google Display; placement and attention context differ.

### google/skills — Google Ads API quickstart
https://github.com/google/skills/tree/main/skills/ads/google-ads-api-quickstart

Architectural lesson:
- dynamically resolve changing Google versions/specifications rather than hardcoding stale platform assumptions.
