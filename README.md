# Google Ads Performance Banner Designer

Repository for a production-grade AI skill that plans, designs, adapts, validates, and exports performance advertising banners for Google Ads.

The project is intentionally broader than a single legacy GDN workflow. It supports the current Google advertising model where responsive assets and Uploaded Display creatives can be used across Display / Demand Gen inventory.

## Goal

Turn a business brief into a grounded advertising concept and a technically valid banner pack while preserving brand consistency, visual hierarchy, readability, platform compliance, and exact output dimensions.

Core pipeline:

`Business context -> evidence/grounding -> creative strategy -> layout family -> rendering -> visual QA -> Google spec validation -> export -> performance learning`

Development work for v0.1 lives on the `dev/performance-banner-designer-v0.1` branch.
