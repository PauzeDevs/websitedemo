#!/usr/bin/env python3
"""Dependency-free integrity checks for the Chihiro static website concept."""

from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
HTML_FILE = ROOT / "index.html"


class SiteParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = []
        self.fragment_links = []
        self.local_assets = []
        self.image_errors = []
        self.external_link_errors = []
        self.robots_meta = None
        self.theme_color = None
        self.menu_items = 0
        self.menu_prices = 0
        self.ticker_has_role = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        element_id = attrs.get("id")
        if element_id:
            self.ids.append(element_id)

        if tag == "meta":
            name = attrs.get("name", "").lower()
            if name == "robots":
                self.robots_meta = attrs.get("content", "").lower()
            elif name == "theme-color":
                self.theme_color = attrs.get("content", "").lower()

        if "ticker" in attrs.get("class", "").split() and attrs.get("role") == "note":
            self.ticker_has_role = True

        href = attrs.get("href", "")
        if tag == "a" and href.startswith("#") and len(href) > 1:
            self.fragment_links.append(href[1:])

        if tag == "a" and attrs.get("target") == "_blank":
            rel_tokens = set(attrs.get("rel", "").lower().split())
            if not {"noopener", "noreferrer"}.issubset(rel_tokens):
                self.external_link_errors.append(
                    f'External new-tab link must use rel="noopener noreferrer": {href or "[no href]"}'
                )

        if tag == "h5":
            self.menu_items += 1
        if tag == "span" and "menu-price" in attrs.get("class", "").split():
            self.menu_prices += 1

        if tag == "img":
            if "alt" not in attrs or not attrs.get("alt", "").strip():
                self.image_errors.append(f"Image is missing meaningful alt text: {attrs.get('src', '[no src]')}")
            if not attrs.get("width") or not attrs.get("height"):
                self.image_errors.append(f"Image should declare width and height: {attrs.get('src', '[no src]')}")

        asset_url = None
        if tag == "img":
            asset_url = attrs.get("src")
        elif tag == "script":
            asset_url = attrs.get("src")
        elif tag == "link":
            rel = attrs.get("rel", "").lower().split()
            if "stylesheet" in rel or "icon" in rel:
                asset_url = href

        if asset_url:
            parsed = urlsplit(asset_url)
            if parsed.scheme in {"http", "https", "data"} or asset_url.startswith("//"):
                if parsed.scheme == "http":
                    self.local_assets.append(f"Insecure HTTP asset URL found: {asset_url}")
            else:
                asset_path = (ROOT / parsed.path).resolve()
                if ROOT not in asset_path.parents and asset_path != ROOT:
                    self.local_assets.append(f"Asset path escapes repository: {asset_url}")
                elif not asset_path.is_file():
                    self.local_assets.append(f"Missing local asset: {asset_url}")


def main():
    if not HTML_FILE.is_file():
        raise SystemExit("FAIL: index.html is missing.")

    html = HTML_FILE.read_text(encoding="utf-8")
    parser = SiteParser()
    parser.feed(html)
    parser.close()
    errors = []

    duplicates = [item for item, count in Counter(parser.ids).items() if count > 1]
    if duplicates:
        errors.append("Duplicate HTML id(s): " + ", ".join(sorted(duplicates)))

    missing_targets = sorted(set(parser.fragment_links) - set(parser.ids))
    if missing_targets:
        errors.append("Broken in-page link target(s): " + ", ".join(missing_targets))

    errors.extend(parser.local_assets)
    errors.extend(parser.image_errors)
    errors.extend(parser.external_link_errors)

    if parser.theme_color != "#f0f4e9":
        errors.append("Browser theme-color should match the cream/sage page palette (#f0f4e9).")
    if not parser.ticker_has_role:
        errors.append('The labeled ticker should use role="note" for accessible semantics.')
    if parser.menu_items < 35 or parser.menu_prices < 35:
        errors.append(
            f"Menu transcription appears incomplete: found {parser.menu_items} item names and {parser.menu_prices} price labels."
        )
    if "noindex" not in (parser.robots_meta or ""):
        print("NOTE: confirm indexing is appropriate before production launch.")

    required_files = (
        ROOT / "assets" / "css" / "styles.css",
        ROOT / "assets" / "js" / "main.js",
        ROOT / "assets" / "images" / "favicon.svg",
    )
    for required in required_files:
        if not required.is_file():
            errors.append(f"Required file is missing: {required.relative_to(ROOT)}")

    css_path = ROOT / "assets" / "css" / "styles.css"
    js_path = ROOT / "assets" / "js" / "main.js"
    css = css_path.read_text(encoding="utf-8") if css_path.is_file() else ""
    js = js_path.read_text(encoding="utf-8") if js_path.is_file() else ""
    if "prefers-reduced-motion: reduce" not in css:
        errors.append("Stylesheet should respect prefers-reduced-motion.")
    if "aria-expanded" not in js or "Escape" not in js:
        errors.append("Mobile navigation should expose its state and support Escape.")
    if 'setAttribute("aria-expanded"' not in js:
        errors.append("Mobile navigation should update aria-expanded when toggled.")
    if "ChIJ3-WMnKT9mzkRPZfLOTZiVbk" not in html:
        errors.append("Directions should point to the configured Chihiro Maps listing.")
    if "menu-toolbar" in html or "menu-filter" in html:
        errors.append("Obsolete card-filter markup remains after replacing it with readable menu text.")

    if errors:
        print("Site validation failed:")
        for error in errors:
            print(" - " + error)
        raise SystemExit(1)

    print(
        f"Site validation passed: unique IDs, in-page links, local assets, image alt/dimensions, "
        f"safe external links, {parser.menu_items} menu items and {parser.menu_prices} price labels, "
        "theme color, ticker semantics, navigation behavior, and reduced-motion support."
    )


if __name__ == "__main__":
    main()
