# Chihiro Bakehouse — Website Concept

A polished, responsive static website concept by **PauzeDevs**, prepared as a proposal for Chihiro Bakehouse in Lucknow.

> **Important:** This is an unofficial demo, not the café's official website. It must not imply endorsement. The content, branding, photography, address, hours, and social details need confirmation and approval before the site is used as a business website.

## Preview

GitHub Pages URL:

https://pauzedevs.github.io/websitedemo/

A validation-only workflow runs from `.github/workflows/validate.yml` on pushes and pull requests. GitHub Pages deployment is handled by the repository's Pages configuration. If the site stops updating, open **Settings → Pages** and check that the source is set to the `main` branch and repository root. Then inspect the **pages build and deployment** workflow in **Actions**.

The site is a plain static HTML/CSS/JavaScript project; no package installation or build framework is required.

## Project structure

- `index.html` — semantic page content, metadata, sections, and accessible labels.
- `assets/css/styles.css` — design tokens, typography, responsive layout, focus styles, and reduced-motion handling.
- `assets/js/main.js` — mobile navigation behavior and current-year footer.
- `assets/images/favicon.svg` — lightweight custom concept favicon.
- `scripts/check_site.py` — dependency-free checks for repeated IDs, broken in-page links, missing local assets, image alt/dimensions, and key accessibility behaviors.
- `.github/workflows/validate.yml` — runs lightweight site-integrity checks on pushes and pull requests; GitHub Pages handles publishing through its configured Pages source.

## Design and behavior

- A cream base, PauzeX-style forest-green typography and accents, and a soft sage-green hero inspired by the café’s soothing green exterior described in the [Knocksense café feature](https://www.knocksense.com/lucknow/ks-discovery-from-pour-overs-to-pastries-3-new-lucknow-cafes-youll-love-exploring/). Typography pairs Instrument Serif with DM Sans and DM Mono.
- Responsive layouts for desktop, tablet, and small mobile screens.
- Mobile menu supports expanded-state semantics, Escape to close, outside-click close, and link-selection close.
- Navigation remains visible on narrow screens if JavaScript is disabled.
- Skip-to-content link, visible keyboard focus, descriptive image alt text, semantic landmarks, and reduced-motion support.
- Hero image loads eagerly at high priority; supporting images use lazy loading and asynchronous decoding.
- Search indexing is disabled for the concept demo.


## Menu research and accuracy

The site links directly to Chihiro's Google Maps place listing for directions and current business information:

https://www.google.com/maps/search/?api=1&query=Chihiro%20Bakehouse%2C%203%20Mahatma%20Gandhi%20Marg%2C%20Lucknow%20226002&query_place_id=ChIJ3-WMnKT9mzkRPZfLOTZiVbk

I could not retrieve a reliable, structured, up-to-date menu with individual prices from Google Maps. To avoid inventing prices, the showcase deliberately has no prices and labels itself as a set of menu highlights. The selected item names are based on public menu-related listing mentions and published local coverage:
- Google Maps place listing: linked above; use it to verify the current listing and photos.
- Curly Tales, published 16 December 2025: https://curlytales.com/india/food/discover/new-cafe-alert-chihiro-brings-specialty-coffee-and-scratch-made-desserts-to-lucknow-cantonment/
- Knocksense café feature: https://www.knocksense.com/lucknow/ks-discovery-from-pour-overs-to-pastries-3-new-lucknow-cafes-youll-love-exploring/

The current showcase uses six cards: specialty coffee and hearty café food as broad categories described in coverage, plus four specifically named desserts from the Knocksense feature: Berry Tart, Spiced Carrot Cake, Smoky Pineapple Upside Down, and Banoffee Tart. That feature was published on 26 November 2025, so even those items are not guaranteed to be available today. Confirm the exact names, ingredients, prices, and availability directly with Chihiro before launch. Opening hours can vary between listings, so the site points visitors to Google Maps rather than hard-coding an uncertain schedule.

## Before production

Obtain the café's approval and replace or verify the following:

1. The business name, visual identity, copy, and permission to use its branding.
2. Real menu items, descriptions, prices, dietary/allergen notes, and availability.
3. Exact address, contact methods, hours, and social-profile URL.
4. All photographs and their usage rights. Current remote Unsplash images are illustrative placeholders and should be licensed/approved for the final site; they are not photos of Chihiro’s actual food or building.
5. The story section and any statements about ingredients, methods, or the café's experience.

Remove the `noindex, nofollow` robots metadata only when the site is authorized and ready to be discoverable. There is no native cart, checkout, payment processing, reservation system, or enquiry backend. No Swiggy or Zomato links are shown because the café’s outlet listings have not been verified.

## Local validation

With Python 3 installed, run:

```bash
python scripts/check_site.py
```

This validates basic site integrity. It does not replace real-browser testing, visual checks on devices, or a full accessibility audit.

## Credits

Concept and implementation: PauzeDevs.
