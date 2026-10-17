#!/usr/bin/env python3
"""Build the Baba Law Firm website from src/ into the repository root.

    python3 src/build.py               # preview build (GitHub Pages: noindex, preview notes)
    python3 src/build.py --production  # production build (indexable, no preview notes)

Content: src/content/*.txt (the approved copy, word for word)
SEO:     src/seo.json (titles and descriptions from Dr. Baba's tables)
Styles:  src/css/*.css, concatenated into assets/css/site.css
"""
import json
import shutil
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent
ROOT = SRC.parent
sys.path.insert(0, str(SRC))

import site_config as C                                    # noqa: E402
import templates as T                                     # noqa: E402
from markup import parse                                  # noqa: E402

SEO = json.loads((SRC / "seo.json").read_text(encoding="utf-8"))


def registry():
    pages = {}
    H = ("Home", "")

    def add(href, out, type_, content, h1, crumbs, section=None, slug=None, body=""):
        key = "/" + href.rstrip("/") if href else "/"
        pages[href] = {
            "href": href, "out": out, "type": type_, "h1": h1, "crumbs": crumbs, "section_href": section,
            "slug": slug, "seo": SEO[key], "body_class": body,
            "doc": parse(SRC / "content" / f"{content}.txt") if content else None,
        }

    add("", "index.html", "home", "home", "Syrian Law. International Perspective.", [H], body="page-home")
    add("our-firm", "our-firm.html", "firm", "our-firm", "Our Firm", [H, ("Our Firm", "our-firm")], "our-firm", body="page-firm")
    add("our-people/", "our-people/index.html", "people", "our-people/index", "Our People",
        [H, ("Our People", "our-people/")], "our-people/", body="page-people")
    for slug, name in C.PEOPLE:
        add("our-people/" + slug, f"our-people/{slug}.html", "profile", "our-people/" + slug, name,
            [H, ("Our People", "our-people/"), (name, "our-people/" + slug)], "our-people/", slug=slug, body="page-profile")
    add("capabilities/", "capabilities/index.html", "cap-index", None, "Capabilities",
        [H, ("Capabilities", "capabilities/")], "capabilities/", body="page-index")
    for slug, title in C.CAPABILITIES:
        add("capabilities/" + slug, f"capabilities/{slug}.html", "capability", "capabilities/" + slug, title,
            [H, ("Capabilities", "capabilities/"), (title, "capabilities/" + slug)], "capabilities/", slug=slug,
            body="page-practice page-capability")
    add("industries/", "industries/index.html", "ind-index", None, "Industries",
        [H, ("Industries", "industries/")], "industries/", body="page-index")
    for slug, title in C.INDUSTRIES:
        add("industries/" + slug, f"industries/{slug}.html", "industry", "industries/" + slug, title,
            [H, ("Industries", "industries/"), (title, "industries/" + slug)], "industries/", slug=slug,
            body="page-practice page-industry")
    add("contact", "contact.html", "contact", "contact", "Contact", [H, ("Contact", "contact")], "contact", body="page-contact")
    add("careers", "careers.html", "careers", "careers", "Careers", [H, ("Careers", "careers")], body="page-careers")
    add("privacy-policy", "privacy-policy.html", "legal", "privacy-policy", "Privacy Policy",
        [H, ("Privacy Policy", "privacy-policy")], body="page-legal")
    add("cookie-policy", "cookie-policy.html", "legal", "cookie-policy", "Cookie Policy",
        [H, ("Cookie Policy", "cookie-policy")], body="page-legal page-cookies")
    add("legal-notice", "legal-notice.html", "legal", "legal-notice", "Legal Notice",
        [H, ("Legal Notice", "legal-notice")], body="page-legal")
    add("sitemap", "sitemap.html", "sitemap", None, "Sitemap", [H, ("Sitemap", "sitemap")], body="page-sitemap")
    add("404", "404.html", "404", None, "Page Not Found", [], body="page-404")
    return pages


RENDER = {
    "home": T.render_home, "firm": T.render_firm, "people": T.render_people, "profile": T.render_profile,
    "cap-index": T.render_index, "ind-index": T.render_index, "capability": T.render_practice,
    "industry": T.render_practice, "contact": T.render_contact, "careers": T.render_careers,
    "legal": T.render_legal, "sitemap": T.render_sitemap, "404": T.render_404,
}

# Files from the earlier preview that this build no longer produces (replaced by redirects).
OBSOLETE = ["people/tawfeeq-baba.html", "people/mohamad-baba.html", "people.html", "capabilities.html", "industries.html",
            "capabilities/foreign-investment-market-entry.html", "capabilities/regulatory-government-public-procurement.html",
            "assets/img/lattice.svg"]


def build(production=False):
    pages = registry()
    ctx = T.Ctx(pages, production)
    logo_defs = (SRC / "partials" / "logo-defs.svg").read_text(encoding="utf-8")

    for rel_path in OBSOLETE:
        p = ROOT / rel_path
        if p.exists():
            p.unlink()

    written = []
    for page in pages.values():
        main = RENDER[page["type"]](ctx, page)
        html = T.layout(ctx, page, main, page["body_class"], overlay=page["type"] == "home", logo_defs=logo_defs)
        out = ROOT / page["out"]
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html, encoding="utf-8")
        written.append(page["out"])

    # Old preview addresses keep working (preview only; they never existed on the production domain).
    for old, new in (C.LEGACY_REDIRECTS.items() if not production else []):
        out = ROOT / old
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(T.redirect_stub(T.rel(old.replace(".html", ""), new), T.canonical(new)), encoding="utf-8")

    # XML sitemap: every public page at its canonical HTTPS URL (no 404, no redirects).
    urls = [T.canonical(p["href"]) for p in pages.values() if p["type"] != "404"]
    xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    xml += [f"  <url><loc>{u}</loc></url>" for u in urls]
    xml.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(xml) + "\n", encoding="utf-8")

    if production:
        robots = f"User-agent: *\nAllow: /\n\nSitemap: {C.DOMAIN}/sitemap.xml\n"
    else:
        robots = ("# Preview build: not for indexing. The production build allows crawling and lists the sitemap:\n"
                  f"# Sitemap: {C.DOMAIN}/sitemap.xml\nUser-agent: *\nDisallow: /\n")
    (ROOT / "robots.txt").write_text(robots, encoding="utf-8")

    # Stylesheet: concatenate the partials.
    css_parts = sorted((SRC / "css").glob("*.css"))
    css = "/* Baba Law Firm — generated from src/css/ by src/build.py. Edit the partials, not this file. */\n\n"
    css += "\n\n".join(p.read_text(encoding="utf-8") for p in css_parts)
    (ROOT / "assets" / "css" / "site.css").write_text(css, encoding="utf-8")

    print(f"Built {len(written)} pages, {0 if production else len(C.LEGACY_REDIRECTS)} redirects, {len(urls)} sitemap URLs "
          f"({'production' if production else 'preview'}).")
    return pages


if __name__ == "__main__":
    build(production="--production" in sys.argv)
