#!/usr/bin/env python3
"""Small, dependency-free checks for the Chihiro static site."""

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
        self.robots_meta = None
        self.menu_filters = []
        self.menu_categories = []
        self.external_link_errors = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)

        element_id = attrs.get("id")
        if element_id:
            self.ids.append(element_id)

        if tag == "meta" and attrs.get("name", "").lower() == "robots":
            self.robots_meta = attrs.get("content", "").lower()

        href = attrs.get("href", "")
        if tag == "a" and href.startswith("#") and len(href) > 1:
            self.fragment_links.append(href[1:])

        if tag == "button" and attrs.get("data-filter"):
            self.menu_filters.append(attrs["data-filter"])

        if tag == "article" and "menu-card" in attrs.get("class", "").split():
            if attrs.get("data-category"):
                self.menu_categories.append(attrs["data-category"])

        if tag == "a" and attrs.get("target") == "_blank":
            rel_tokens = set(attrs.get("rel", "").lower().split())
            if not {"noopener", "noreferrer"}.issubset(rel_tokens):
                self.external_link_errors.append(
                    f'External new-tab link must use rel="noopener noreferrer": {attrs.get("href", "[no href]")}'
                )

        if tag == "img":
            if "alt" not in attrs:
                self.image_errors.append("Image is missing an alt attribute.")
            if not attrs.get("width") or not attrs.get("height"):
                self.image_errors.append(
                    f"Image should declare width and height: {attrs.get('src', '[no src]')}"
                )

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
                    self.local_assets.append(
                        f"Insecure HTTP asset URL found: {asset_url}"
                    )
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

    if not parser.menu_categories:
        errors.append("No menu cards were found.")
    if not parser.menu_filters or "all" not in parser.menu_filters:
        errors.append("Menu filtering must provide an 'all' filter.")
    missing_filters = sorted(set(parser.menu_categories) - set(parser.menu_filters))
    if missing_filters:
        errors.append("Menu categories have no matching filter: " + ", ".join(missing_filters))
    allowed_categories = {"drinks", "desserts", "savoury"}
    invalid_categories = sorted(set(parser.menu_categories) - allowed_categories)
    if invalid_categories:
        errors.append("Unknown menu category value(s): " + ", ".join(invalid_categories))

    required_files = (
        ROOT / "assets" / "css" / "styles.css",
        ROOT / "assets" / "js" / "main.js",
        ROOT / "assets" / "images" / "favicon.svg",
    )
    for required in required_files:
        if not required.is_file():
            errors.append(f"Required file is missing: {required.relative_to(ROOT)}")

    css = (ROOT / "assets" / "css" / "styles.css").read_text(encoding="utf-8") if (ROOT / "assets" / "css" / "styles.css").is_file() else ""
    js = (ROOT / "assets" / "js" / "main.js").read_text(encoding="utf-8") if (ROOT / "assets" / "js" / "main.js").is_file() else ""
    if "prefers-reduced-motion: reduce" not in css:
        errors.append("Stylesheet should respect prefers-reduced-motion.")
    if 'aria-expanded' not in js or 'Escape' not in js:
        errors.append("Mobile navigation should expose its state and support Escape.")
    if "data-filter" not in js or "aria-pressed" not in js:
        errors.append("Menu filters must update both visible cards and accessible state.")
    if "query_place_id=ChIJ3-WMnKT9mzkRPZfLOTZiVbk" not in html:
        errors.append("Directions should point at the resolved Chihiro Maps place listing.")
    if parser.robots_meta and "noindex" not in parser.robots_meta:
        print("NOTE: robots meta no longer contains noindex; confirm this is intentional before production.")

    if errors:
        print("Site validation failed:")
        for error in errors:
            print(f" - {error}")
        raise SystemExit(1)

    print(
        "Site validation passed: unique IDs, in-page links, local assets, "
        "image alt/dimensions, safe external links, menu category controls, navigation behavior, and reduced-motion support."
    )


if __name__ == "__main__":
    main()
