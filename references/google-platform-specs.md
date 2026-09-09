# Google Ads platform specifications

Status snapshot: 2026-09-04.

This file is a cached operational reference, not a permanent source of truth. Google Ads products and requirements change. Resolve current official documentation whenever compliance is material.

## 1. Uploaded Display ads on Demand Gen

**Evidence level: PLATFORM REQUIREMENT / OFFICIAL RECOMMENDATION**

Google currently allows static uploaded display creatives to serve on GDN inventory within Demand Gen. Current guidance states:

- up to 20 image assets per ad;
- JPG, PNG, or non-animated GIF;
- maximum file size: 150 KB;
- recommended dimensions:
  - 300x250 — medium rectangle;
  - 336x280 — large rectangle;
  - 728x90 — leaderboard;
  - 970x90 — large leaderboard;
  - 160x600 — wide skyscraper;
  - 300x600 — half-page;
  - 320x50 — mobile leaderboard;
- animations are not supported in this current Demand Gen uploaded-display mode.

These seven dimensions are the default `core-pack` for v0.1.

## 2. Full uploaded image-ad dimension library

**Evidence level: PLATFORM REQUIREMENT**

Google's uploaded display specification lists the following dimensions for image ads:

### Square / rectangle
- 200x200
- 240x400
- 250x250
- 250x360
- 300x250
- 336x280
- 580x400

### Skyscraper
- 120x600
- 160x600
- 300x600
- 300x1050

### Leaderboard / horizontal
- 468x60
- 728x90
- 930x180
- 970x90
- 970x250
- 980x120

### Mobile
- 300x50
- 320x50
- 320x100

For legacy/general uploaded image ads, Google lists GIF/JPG/PNG and 150 KB maximum. Some regional dimensions have special availability. Do not assume every historical dimension is equally valuable for a current campaign.

## 3. Responsive Display image assets

**Evidence level: PLATFORM REQUIREMENT / BEST PRACTICE**

Current Responsive Display guidance includes:

### Image ratios
- landscape 1.91:1 — recommended 1200x628, minimum 600x314;
- square 1:1 — recommended 1200x1200, minimum 300x300;
- vertical 9:16 — recommended 900x1600, minimum 600x1067;
- max image file size listed by Google: 5120 KB.

### Copy assets
- short headline: up to 30 characters, 1-5;
- long headline: up to 90 characters, 1;
- description: up to 90 characters, 1-5;
- business name: up to 25 characters.

### Image construction guidance
Google recommends:
- no overlaid logo on the marketing image;
- avoid overlaid text;
- do not overlay fake buttons;
- make product/service the focus;
- blank space should not exceed 80% of the image;
- avoid unnecessary collage imagery;
- avoid artificial composite backgrounds where possible;
- use high-quality logos.

Important: the `blank space <=80%` statement applies to responsive image guidance. It is not a universal rule for how much of a finished uploaded display banner must be filled.

## 4. Demand Gen asset-based image ads

**Evidence level: PLATFORM REQUIREMENT / RECOMMENDATION**

Current Demand Gen image asset guidance includes:

- horizontal 1.91:1 — recommended 1200x628, minimum 600x314;
- square 1:1 — recommended 1200x1200, minimum 300x300;
- vertical 4:5 — recommended 960x1200, minimum 480x600;
- vertical 9:16 — recommended 1080x1920, minimum 600x1067, particularly relevant to Shorts inventory;
- image max file size: 5 MB in current guidance;
- logo 1:1 — recommended 1200x1200;
- headline: max 40 characters, 1-5; at least one headline should be 30 characters or fewer to ensure Display serving / avoid incomplete Ad Strength condition;
- descriptions: max 90 characters, 1-5;
- business name: max 25 characters.

Do not bake text/CTA/logo into the image merely because uploaded-display banners use composed art. These are different modes.

## 5. Uploaded image ads vs asset-based ads

Use this decision rule:

### Uploaded Display
The raster file is the complete ad creative. Typography, offer, logo, CTA treatment, and image can be composed into exact pixels.

### Responsive Display / Demand Gen asset ad
The image is an asset inside a layout Google may assemble. Keep it robust when paired with separate text and logo assets.

Confusing these modes causes duplicate headlines, duplicate logos, unreadable small text, crop failures, and fake-button policy problems.

## 6. HTML5 and animation note

Google's general uploaded-display documentation lists HTML5 ZIP support with a 600 KB size limit and provides additional rules. General animated GIF image ads have rules such as total animation length <=30 seconds and frame rate slower than 5 FPS.

However, the current Demand Gen Uploaded Display guidance says uploaded display animations are not supported. Resolve the exact campaign mode before approving animation.

## 7. Dynamic preflight instruction

Before a final production export, check current official pages for:

1. campaign type availability;
2. uploaded display support;
3. allowed formats;
4. max file size;
5. recommended/exact dimensions;
6. text character limits;
7. animation rules;
8. regional restrictions.

If live Google guidance conflicts with this file, update the working specification and record the date/source.
