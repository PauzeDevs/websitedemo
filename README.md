# Chihiro Bakehouse — Website Concept

A polished, responsive static website concept by **PauzeDevs**, prepared as a proposal for Chihiro Bakehouse in Lucknow.

> **Important:** This is an unofficial demo, not the café's official website. It must not imply endorsement. The content, branding, photography, address, hours, and social details need confirmation and approval before the site is used as a business website.

## Preview

Expected GitHub Pages URL after Pages is configured and the workflow succeeds:

https://pauzedevs.github.io/websitedemo/

The workflow is in `.github/workflows/deploy.yml`. To enable deployment for the first time:

1. Open this repository on GitHub and select **Settings → Pages**.
2. Under **Build and deployment**, set **Source** to **GitHub Actions**.
3. Open **Actions** and inspect the **Validate and deploy static site** workflow.
4. After both validation and deployment succeed, open the Pages URL above.

The site is a plain static HTML/CSS/JavaScript project; no package installation or build framework is required.

## Project structure

- `index.html` — semantic page content, metadata, sections, and accessible labels.
- `assets/css/styles.css` — design tokens, typography, responsive layout, focus styles, and reduced-motion handling.
- `assets/js/main.js` — mobile navigation behavior and current-year footer.
- `assets/images/favicon.svg` — lightweight custom concept favicon.
- `scripts/check_site.py` — dependency-free checks for repeated IDs, broken in-page links, missing local assets, image alt/dimensions, and key accessibility behaviors.
- `.github/workflows/deploy.yml` — runs validation and deploys the static site to GitHub Pages.

## Design and behavior

- PauzeX-inspired forest green, cream, soft sage, and a controlled lime accent, paired with Instrument Serif, DM Sans, and DM Mono.
- Responsive layouts for desktop, tablet, and small mobile screens.
- Mobile menu supports expanded-state semantics, Escape to close, outside-click close, and link-selection close.
- Navigation remains visible on narrow screens if JavaScript is disabled.
- Skip-to-content link, visible keyboard focus, descriptive image alt text, semantic landmarks, and reduced-motion support.
- Hero image loads eagerly at high priority; supporting images use lazy loading and asynchronous decoding.
- Search indexing is disabled for the concept demo.


## Menu research and accuracy

The public Google Maps search listing is linked from the site for current photos, directions, and business information:
https://www.google.com/maps/search/?api=1&query=Chihiro%20Bakehouse%2C%203%20Mahatma%20Gandhi%20Marg%2C%20Lucknow%20226002

I could not retrieve a reliable, structured, current menu with prices directly from the Google Maps page, so this demo does **not** invent prices or claim to be the full official menu. The current selection of coffee styles, teas/matcha, berry tart, spiced carrot cake, smoky pineapple upside-down cake, banoffee tart, waffles, sandwiches, and brunch plates is based on published local coverage:
- Curly Tales, published 16 December 2025: https://curlytales.com/india/food/discover/new-cafe-alert-chihiro-brings-specialty-coffee-and-scratch-made-desserts-to-lucknow-cantonment/
- Knocksense, café feature: https://www.knocksense.com/lucknow/ks-discovery-from-pour-overs-to-pastries-3-new-lucknow-cafes-youll-love-exploring/

Those are menu highlights, not a guarantee that each item is currently available. Confirm the actual menu and price list directly with Chihiro before launch. Opening-hour listings vary across third-party sources, so the site points visitors to Google Maps for current hours rather than hard-coding a possibly stale schedule.

## Before production

Obtain the café's approval and replace or verify the following:

1. The business name, visual identity, copy, and permission to use its branding.
2. Real menu items, descriptions, prices, dietary/allergen notes, and availability.
3. Exact address, contact methods, hours, and social-profile URL.
4. All photographs and their usage rights. Current remote Unsplash images are illustrative placeholders and should be licensed/approved for the final site.
5. The story section and any statements about ingredients, methods, or the café's experience.

Remove the `noindex, nofollow` robots metadata only when the site is authorized and ready to be discoverable. No online ordering, payments, reservations, backend, analytics, or enquiry form is implemented.

## Local validation

With Python 3 installed, run:

```bash
python scripts/check_site.py
```

This validates basic site integrity. It does not replace real-browser testing, visual checks on devices, or a full accessibility audit.

## Credits

Concept and implementation: PauzeDevs.
