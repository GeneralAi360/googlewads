# Visual attention and eye-tracking guidance

This reference converts research into contextual design guidance. It deliberately rejects simplistic rules such as "people always scan a banner in a Z" or "put the CTA bottom-right because eyes always finish there."

## 1. Banner blindness

**Evidence level: RESEARCH EVIDENCE**

Banner blindness describes the tendency for users to ignore regions that look or behave like advertising, including visually prominent areas. The design implication is not "make everything louder." Excessive salience can add noise without creating comprehension.

Operational response:
- make the commercial proposition immediately understandable;
- minimize irrelevant decoration;
- use relevant imagery rather than generic attention bait;
- build a coherent scan path instead of competing hotspots.

## 2. Content elements and first attention

**Evidence level: RESEARCH EVIDENCE**

Peker, Dalveren, and Inal (2021) used eye tracking on online banner advertisements with image, brand, and discount areas. In their study:
- image was the most attractive of the three content elements;
- middle areas were noticed first;
- left-side areas were generally noticed earlier than right-side areas;
- higher discount rates attracted more attention;
- brand familiarity altered what participants focused on.

Do not turn this into "always put the product in the center-left." Use it as a default prior when no stronger business/visual reason exists.

### Production interpretation

For an unfamiliar brand, a strong product/service visual may need to do more initial work than the logo. For a known brand with a meaningful promotion, the offer can carry more attention.

## 3. Faces and gaze direction

**Evidence level: RESEARCH EVIDENCE**

Palcu, Sudkamp, and Florack (2017) studied faces and gaze cues in banner advertisements. A face looking toward the product increased the likelihood that participants looked at the product. Gaze direction also influenced later purchase intention in the experiment. Animated face conditions captured more attention than static face conditions.

Important limits:
- a face is not automatically better than no face;
- gaze direction can help direct attention when a person naturally belongs in the creative;
- the person's gaze should not unintentionally pull attention away from the product, headline, or CTA;
- do not add a stock face only because an eye-tracking study exists.

### Design check

If a face is present, ask:
1. Where is the face looking?
2. Does that direction support the intended scan path?
3. Is the face itself becoming a stronger AOI than the commercial object?
4. Would removing the face improve comprehension?

## 4. Visual complexity

**Evidence level: RESEARCH EVIDENCE**

A 2023 eye-tracking study on banner-ad visual complexity found low-complexity ads outperformed high-complexity ads on sustained visual attention and perceived appeal in that experiment. More complex ads could be noticed slightly faster but received less fixation and fewer looks overall.

Operational lesson:
- first notice is not the same as useful attention;
- salience should lead into comprehension;
- clutter can win the first millisecond and lose the message.

## 5. Areas of Interest (AOIs)

**Evidence level: PRODUCTION HEURISTIC**

Model a composed banner as a small set of meaningful attention objects:

- hero/product/service image;
- headline/value proposition;
- offer/price/proof;
- CTA;
- logo/brand;
- legal/disclaimer if mandatory.

Decorative shapes are not business AOIs, but they can still steal saliency.

### Default AOI budget

Aim for roughly 3-5 meaningful AOIs in an ordinary performance banner. This is a production heuristic, not a scientific constant.

Micro banners may contain only:
1. brand;
2. one proposition/offer;
3. CTA.

Large formats can support one additional proof/support element.

## 6. Intended scan path

Before rendering, explicitly state the desired order, for example:

`product -> offer -> CTA -> brand`

or

`headline -> product evidence -> CTA -> brand`

After rendering, inspect whether size, contrast, face direction, color, and position actually produce that hierarchy.

## 7. Predictive saliency

**Evidence level: EXPERIMENTAL QA / TEST HYPOTHESIS**

A predictive-saliency model can be useful as a preflight tool to detect accidental hotspots. It is not a CTR predictor and cannot replace human review or campaign experiments.

Use it to ask:
- Is decoration hotter than headline/product?
- Does a face trap attention?
- Does logo dominate before proposition for an unknown brand?
- Is CTA effectively invisible?

Do not convert saliency score into a claim of advertising effectiveness.

## 8. What not to encode as universal law

Do not encode:
- mandatory F-pattern or Z-pattern scanning for every banner;
- a fixed CTA corner;
- mandatory face usage;
- mandatory product-center placement;
- a fixed percentage of image/text coverage;
- the idea that maximal contrast everywhere is optimal.

The skill should create hierarchy, not visual shouting.
