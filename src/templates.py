"""Page templates for the Baba Law Firm website.

Three page families, as approved: Home is photographic, the capability and industry
pages are typographic, and the People pages are built around the portraits.
All wording comes from src/content/ (the approved copy); this module adds markup only.
"""
import html
import json
import re

import site_config as C
from markup import inline, plain, strip_arrow, split_lead, split_bold_lead, nowrap

# ---------------------------------------------------------------- small helpers

def esc(s):
    return html.escape(s, quote=True)


def slugify(text):
    t = plain(text).lower().replace("&", "and")
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    return t


ARROW = ('<svg class="arrow" viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
         '<path d="M4 12h15M13.5 6.5 19 12l-5.5 5.5" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="square"/></svg>')
EXT = ('<svg class="ext" viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
       '<path d="M14 5h5v5M19 5l-8 8M17 14v5H5V7h5" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>')
ICON_MAIL = ('<svg class="icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
             '<path d="M3.75 6.25h16.5v11.5H3.75zM4.5 7l7.5 6 7.5-6" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/></svg>')
ICON_CHAT = ('<svg class="icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
             '<path d="M4.25 5.25h15.5v10.5h-8.5l-4.5 3.75v-3.75h-2.5z" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/></svg>')
ICON_PHONE = ('<svg class="icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
              '<path d="M7.2 3.75h2.6l1.3 4.1-2 1.5a10.6 10.6 0 0 0 5.6 5.6l1.5-2 4.05 1.3v2.6a2 2 0 0 1-2.2 2A15.9 15.9 0 0 1 5.2 5.95a2 2 0 0 1 2-2.2z" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/></svg>')

CTA_TARGETS = {
    "Explore Our Capabilities": "capabilities/",
    "Explore Our Industries": "industries/",
    "Contact Us": "contact",
    "Meet Our People": "our-people/",
    "Contact the Firm": "contact",
}


def depth(href):
    d = href.rsplit("/", 1)[0] if "/" in href else ""
    return len(d.split("/")) if d else 0


class Ctx:
    """Build context: the page registry, the parsed documents and the build mode."""

    def __init__(self, pages, production):
        self.pages = pages                    # key -> page dict
        self.production = production
        self.preview = not production
        self.by_href = {p["href"]: p for p in pages.values()}
        self.cap_by_title = {t: s for s, t in C.CAPABILITIES}
        self.ind_by_title = {t: s for s, t in C.INDUSTRIES}
        self.optional = list(C.OPTIONAL_CATEGORIES)
        if C.MAP["VERIFIED"]:
            self.optional.append({
                "key": "maps", "name": "Maps",
                "description": "Google Maps on the Contact page. When allowed, the map loads automatically; otherwise it loads only when you choose to load it.",
            })


def rel(frm, to):
    """Relative URL from the page at `frm` to the page or asset at `to`."""
    r = "../" * depth(frm) + to
    return r or "./"


def canonical(href):
    """Production URL (Dr. Baba's table: lowercase, no extensions, no trailing slash)."""
    if href == "":
        return C.DOMAIN + "/"
    return C.DOMAIN + "/" + href.rstrip("/")


# ---------------------------------------------------------------- media

def photo_url(key, w):
    kind, pid = C.PHOTOS[key]["src"]
    tpl = C.UNSPLASH if kind == "unsplash" else C.PEXELS
    return tpl.format(id=pid, w=w)


def img(key, sizes, eager=False, cls=""):
    p = C.PHOTOS[key]
    widths = [640, 960, 1280, 1600, 2000, 2400]
    srcset = ", ".join(f"{photo_url(key, w)} {w}w" for w in widths)
    load = 'loading="eager" fetchpriority="high"' if eager else 'loading="lazy"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="{esc(photo_url(key, 1600))}" srcset="{esc(srcset)}" sizes="{sizes}" '
            f'alt="{esc(p["alt"])}" {load} decoding="async" style="object-position:{p["pos"]}">')


def portrait(slug, name, frm, role=""):
    p = C.PORTRAITS[slug]
    if p["src"]:
        base = rel(frm, p["src"])
        return (f'<div class="portrait"><picture>'
                f'<source type="image/avif" srcset="{base}-640.avif 640w, {base}-1200.avif 1200w" sizes="(min-width: 960px) 30vw, 90vw">'
                f'<source type="image/webp" srcset="{base}-640.webp 640w, {base}-1200.webp 1200w" sizes="(min-width: 960px) 30vw, 90vw">'
                f'<img src="{base}-1200.jpg" width="1200" height="1500" alt="{esc(name)}{", " + esc(role) if role else ""}, Baba Law Firm" loading="lazy" decoding="async">'
                f'</picture></div>')
    return (f'<div class="portrait"><div class="portrait-ph" aria-hidden="true">'
            f'<span class="portrait-initials">{p["initials"]}</span></div></div>')


# ---------------------------------------------------------------- links and buttons

def btn(href, label, variant="btn--primary", extra=""):
    return f'<a class="btn {variant}" href="{esc(href)}"{extra}><span>{esc(label)}</span>{ARROW}</a>'


def link_arrow(href, label, extra_cls="", hidden_suffix=""):
    hs = f'<span class="visually-hidden">{esc(hidden_suffix)}</span>' if hidden_suffix else ""
    c = f"link-arrow {extra_cls}".strip()
    return f'<a class="{c}" href="{esc(href)}"><span>{esc(label)}{hs}</span>{ARROW}</a>'


def cta_href(ctx, page, label):
    return rel(page["href"], CTA_TARGETS[label])


def email_links(text):
    links = {}
    for addr in (C.EMAIL, C.CAREERS_EMAIL):
        if addr in text:
            links[addr] = f'<a href="mailto:{addr}">{addr}</a>'
    return links


def para(text, links=None, cls=""):
    l = email_links(text)
    if links:
        l.update({k: v for k, v in links.items() if k in plain(text)})
    c = f' class="{cls}"' if cls else ""
    return f"<p{c}>{inline(text, l or None)}</p>"


def two_lines(text):
    """'A. B.' -> two spans, so a two-sentence tagline sets on two lines."""
    parts = re.split(r"(?<=\.)\s+(?=[A-Z])", text)
    if len(parts) == 1:
        return inline(text)
    return " ".join(f'<span class="line">{inline(p)}</span>' for p in parts)


def lead_items(items, cls, name_cls, desc_cls, numbered=False, tag="ul"):
    out = []
    for i, it in enumerate(items, 1):
        name, desc = split_lead(it)
        num = f'<span class="{cls}-num" aria-hidden="true">{i:02d}</span>' if numbered else ""
        out.append(f'<li class="{cls}-item">{num}<strong class="{name_cls}">{inline(name)}</strong>'
                   f'<span class="sep"> — </span><span class="{desc_cls}">{inline(desc)}</span></li>')
    return f'<{tag} class="{cls}" role="list">' + "".join(out) + f"</{tag}>"


def render_blocks(ctx, page, blocks, links=None):
    """Generic rendering of paragraphs, lists, sub-headings and arrow links."""
    out = []
    for b in blocks:
        if b.kind == "p":
            out.append(para(b.text, links))
        elif b.kind == "note":
            out.append(f'<p class="italic-line">{inline(b.text, email_links(b.text) or None)}</p>')
        elif b.kind == "h3":
            out.append(f'<h3 class="sub-h">{inline(b.text)}</h3>')
        elif b.kind == "ul":
            if all(split_lead(i)[0] for i in b.items):
                out.append(lead_items(b.items, "svc-list", "svc-name", "svc-desc"))
            else:
                out.append('<ul class="bullets">' + "".join(f"<li>{inline(i)}</li>" for i in b.items) + "</ul>")
        elif b.kind == "cta":
            label = strip_arrow(b.text)
            out.append(f'<p class="cta-line">{link_arrow(cta_href(ctx, page, label), label)}</p>')
    return "\n".join(out)


# ---------------------------------------------------------------- shared blocks

def breadcrumb_html(page):
    crumbs = page["crumbs"]
    items = []
    for i, (label, href) in enumerate(crumbs):
        if i == len(crumbs) - 1:
            items.append(f'<li><span aria-current="page">{esc(label)}</span></li>')
        else:
            items.append(f'<li><a href="{esc(rel(page["href"], href))}">{esc(label)}</a></li>')
    return f'<nav class="breadcrumb" aria-label="Breadcrumb"><ol>{"".join(items)}</ol></nav>'


def page_hero(ctx, page, doc, intro_html=None, cls="", show_crumbs=False, title=None):
    crumbs = breadcrumb_html(page) if show_crumbs else ""
    tagline = f'<p class="page-tagline">{inline(doc.tagline)}</p>' if doc.tagline else ""
    intro = intro_html if intro_html is not None else (
        '<div class="page-intro">' + "".join(para(b.text) for b in doc.intro if b.kind == "p") + "</div>" if doc.intro else "")
    return f'''
<section class="page-hero page-hero--ivory {cls}" aria-labelledby="page-title">
  <div class="container">
    {crumbs}
    <h1 class="h1 page-title" id="page-title">{esc(title or doc.title)}</h1>
    {tagline}
    {intro}
  </div>
</section>'''


def cta_band(ctx, page, section, statement=None, body_blocks=None, button_label="Contact Us", sid="contact"):
    """Closing 'Contact' block: label, statement, sentence and button on navy."""
    blocks = section.blocks if body_blocks is None else body_blocks
    if statement is None:
        h3 = [b for b in blocks if b.kind == "h3"]
        statement = h3[0].text if h3 else section.tagline
    paras = "".join(para(b.text, cls="lead") for b in blocks if b.kind == "p")
    cta = [b for b in blocks if b.kind == "cta"]
    label = strip_arrow(cta[0].text) if cta else button_label
    target = rel(page["href"], CTA_TARGETS.get(label, "contact"))
    stmt = f'<p class="cta-statement">{inline(statement)}</p>' if statement else ""
    return f'''
<section class="section cta-band cta-band--navy" aria-labelledby="{sid}-title">
  <div class="container cta-inner">
    <div class="cta-text">
      <h2 class="label sec-label" id="{sid}-title">{esc(section.heading)}</h2>
      {stmt}
      {paras}
    </div>
    <div class="cta-actions">{btn(target, label, "btn--light")}</div>
  </div>
</section>'''


def rail_section(ctx, page, s, cls="", body=None, sid=None, links=None, after=""):
    sid = sid or slugify(s.heading)
    tagline = f'<p class="sec-tagline">{inline(s.tagline)}</p>' if s.tagline else ""
    content = body if body is not None else render_blocks(ctx, page, s.blocks, links)
    return f'''
<section class="doc-sec rail {cls}" aria-labelledby="{sid}">
  <h2 class="label sec-label" id="{sid}">{esc(s.heading)}</h2>
  <div class="doc-sec-body">
    {tagline}
    <div class="prose">{content}</div>{after}
  </div>
</section>'''


# ---------------------------------------------------------------- home

def render_home(ctx, page):
    d = page["doc"]
    h = page["href"]
    intro = "".join(para(b.text) for b in d.intro if b.kind == "p")
    hero = f'''
<section class="hero" aria-labelledby="hero-title">
  <div class="hero-media">{img("hero", "100vw", eager=True)}</div>
  <div class="container hero-content">
    <h1 class="display hero-title" id="hero-title">{two_lines(d.tagline)}</h1>
    <div class="hero-sub">
      <div class="hero-intro">{intro}</div>
      <div class="hero-actions">
        {btn(rel(h, "capabilities/"), "Explore Our Capabilities", "btn--light")}
        {btn(rel(h, "contact"), "Contact Us", "btn--ghost-light")}
      </div>
    </div>
  </div>
</section>'''

    s = d.section("At a Glance")
    glance = f'''
<section class="section section--white home-glance" aria-labelledby="glance-title">
  <div class="container">
    <div class="glance-head">
      <h2 class="label sec-label" id="glance-title">{esc(s.heading)}</h2>
      <p class="sec-tagline">{inline(s.tagline)}</p>
    </div>
    {lead_items(s.blocks[0].items, "glance", "glance-term", "glance-desc")}
  </div>
</section>'''

    s = d.section("A Market Opening to Investment")
    market = f'''
<section class="section home-market" aria-labelledby="market-title">
  <div class="container home-split">
    <figure class="home-split-media arch-crop reveal">{img("window", "(min-width: 960px) 34vw, 220px")}</figure>
    <div class="home-split-text reveal">
      <h2 class="label sec-label" id="market-title">{esc(s.heading)}</h2>
      <p class="sec-tagline">{inline(s.tagline)}</p>
      <div class="prose">{"".join(para(b.text) for b in s.blocks if b.kind == "p")}</div>
    </div>
  </div>
</section>'''

    s = d.section("How We Help")
    items = [i for b in s.blocks if b.kind == "ul" for i in b.items]
    helpsec = f'''
<section class="section section--white home-help" aria-labelledby="help-title">
  <div class="container rail">
    <h2 class="label sec-label" id="help-title">{esc(s.heading)}</h2>
    <div>
      <p class="sec-tagline">{inline(s.tagline)}</p>
      {lead_items(items, "stage", "stage-name", "stage-desc", numbered=True)}
      <p class="cta-line">{link_arrow(rel(h, "capabilities/"), "Explore Our Capabilities")}</p>
    </div>
  </div>
</section>'''

    s = d.section("Why Baba Law Firm")
    why = f'''
<section class="section section--navy home-why" aria-labelledby="why-title">
  <div class="container rail">
    <h2 class="label sec-label" id="why-title">{esc(s.heading)}</h2>
    <div>
      <p class="sec-tagline">{inline(s.tagline)}</p>
      {lead_items(s.blocks[0].items, "why", "why-name", "why-desc")}
    </div>
  </div>
</section>'''

    s = d.section("Industries We Serve")
    ind_items = [b for b in s.blocks if b.kind == "ul"][0].items
    links = []
    for name in ind_items:
        slug = ctx.ind_by_title[plain(name)]
        links.append(f'<li><a class="ind-link" href="{esc(rel(h, "industries/" + slug))}"><span>{inline(name)}</span>{ARROW}</a></li>')
    industries = f'''
<section class="section home-industries" aria-labelledby="industries-title">
  <div class="container rail">
    <h2 class="label sec-label" id="industries-title">{esc(s.heading)}</h2>
    <div>
      <p class="sec-tagline">{inline(s.tagline)}</p>
      <div class="prose">{"".join(para(b.text) for b in s.blocks if b.kind == "p")}</div>
      <ul class="ind-links" role="list">{"".join(links)}</ul>
      <p class="cta-line">{link_arrow(rel(h, "industries/"), "Explore Our Industries")}</p>
    </div>
  </div>
</section>'''

    s = d.section("Our People")
    people = f'''
<section class="section section--sand home-people" aria-labelledby="people-title">
  <div class="container home-people-grid">
    <div class="home-people-head reveal">
      <h2 class="label sec-label" id="people-title">{esc(s.heading)}</h2>
      <p class="sec-tagline">{inline(s.tagline)}</p>
    </div>
    <div class="home-people-text reveal">
      <div class="prose">{"".join(para(b.text) for b in s.blocks if b.kind == "p")}</div>
      <p class="cta-line">{link_arrow(rel(h, "our-people/"), "Meet Our People")}</p>
    </div>
  </div>
</section>'''

    s = d.section("Contact")
    contact = f'''
<section class="section home-contact" aria-labelledby="contact-title">
  <div class="container home-contact-centre reveal">
    <h2 class="label sec-label" id="contact-title">{esc(s.heading)}</h2>
    <p class="sec-tagline">{inline(s.tagline)}</p>
    {"".join(para(b.text, cls="lead") for b in s.blocks if b.kind == "p")}
    <div class="actions">{btn(rel(h, "contact"), "Contact Us")}</div>
  </div>
</section>'''
    return hero + glance + market + helpsec + why + industries + people + contact


# ---------------------------------------------------------------- our firm

def render_firm(ctx, page):
    d = page["doc"]
    h = page["href"]
    ps = [b for b in d.intro if b.kind == "p"]
    intro = f'''
    <div class="firm-hero-body">
      {para(ps[0].text, cls="serif-lg firm-hero-lead")}
      <div class="prose firm-hero-text">{"".join(para(b.text) for b in ps[1:])}</div>
    </div>'''
    hero = page_hero(ctx, page, d, intro_html=intro, cls="firm-hero")

    s = d.section("Our Heritage")
    heritage = f'''
<section class="section section--white firm-heritage" aria-labelledby="our-heritage">
  <div class="container firm-story-grid">
    <div class="firm-story-media reveal"><figure class="arch"><div class="arch-frame">{img("courtyard", "(min-width: 960px) 36vw, 90vw")}</div></figure></div>
    <div class="firm-story-text reveal">
      <h2 class="label sec-label" id="our-heritage">{esc(s.heading)}</h2>
      <p class="sec-tagline">{inline(s.tagline)}</p>
      <div class="prose">{render_blocks(ctx, page, s.blocks)}</div>
    </div>
  </div>
</section>'''

    leadership = d.section("Our Leadership")
    practice = d.section("Our Practice")
    body = f'''
<div class="section firm-body">
  <div class="container">
    {rail_section(ctx, page, leadership)}
    {rail_section(ctx, page, practice)}
  </div>
</div>'''

    a, b = d.section("Working Across Borders"), d.section("How We Work")
    pair = f'''
<section class="section section--sand firm-pair" aria-label="{esc(a.heading)}; {esc(b.heading)}">
  <div class="container firm-pair-grid">
    <div class="firm-pair-col reveal">
      <h2 class="label sec-label" id="{slugify(a.heading)}">{esc(a.heading)}</h2>
      <p class="sec-tagline">{inline(a.tagline)}</p>
      <div class="prose">{render_blocks(ctx, page, a.blocks)}</div>
    </div>
    <div class="firm-pair-col reveal">
      <h2 class="label sec-label" id="{slugify(b.heading)}">{esc(b.heading)}</h2>
      <p class="sec-tagline">{inline(b.tagline)}</p>
      <div class="prose">{render_blocks(ctx, page, b.blocks)}</div>
    </div>
  </div>
</section>'''
    contact = d.section("Contact Baba Law Firm")
    return hero + heritage + body + pair + cta_band(ctx, page, contact, statement=contact.tagline)


# ---------------------------------------------------------------- people

def person_row(ctx, page, name, blocks, alt=False):
    """A lawyer on Our People: portrait, role, name, credentials, introduction, link."""
    slug = [s for s, n in C.PEOPLE if n == name][0]
    head = blocks[0].text                                   # **Role** \\ credentials
    role, cred = [x.strip() for x in head.split(" \\\\ ", 1)]
    role = plain(role)
    paras = [b for b in blocks[1:] if b.kind == "p"]
    href = rel(page["href"], "our-people/" + slug)
    return f'''
      <li class="person-row{' person-row--alt' if alt else ''}">
        <a class="person-portrait" href="{esc(href)}" tabindex="-1" aria-hidden="true">{portrait(slug, name, page["href"], role)}</a>
        <div class="person-text reveal">
          <p class="person-role">{esc(role)}</p>
          <h3 class="h2 person-name"><a href="{esc(href)}">{esc(name)}</a></h3>
          <p class="person-cred">{cred_line(cred)}</p>
          <div class="prose">{"".join(para(p.text) for p in paras)}</div>
          <p class="cta-line">{link_arrow(href, "View Profile", hidden_suffix=": " + name)}</p>
        </div>
      </li>'''


def cred_line(text):
    """'A | B' credentials: keep the separator, styled."""
    parts = [inline(p.strip()) for p in text.split("|")]
    return '<span class="cred-sep"> | </span>'.join(f'<span class="cred">{p}</span>' for p in parts)


def render_people(ctx, page):
    d = page["doc"]
    hero = page_hero(ctx, page, d, cls="people-hero")
    lead = d.section("Our Leadership")
    rows, cur = [], None
    for b in lead.blocks:
        if b.kind == "h3":
            cur = [b.text, []]
            rows.append(cur)
        elif cur:
            cur[1].append(b)
    people_html = "".join(person_row(ctx, page, n, bl, alt=i % 2 == 1) for i, (n, bl) in enumerate(rows))
    leadership = f'''
<section class="section section--white people-list" aria-labelledby="our-leadership">
  <div class="container">
    <h2 class="label sec-label people-list-label" id="our-leadership">{esc(lead.heading)}</h2>
    <ul class="people-rows" role="list">{people_html}
    </ul>
  </div>
</section>'''
    team = d.section("Our Legal Team")
    team_html = f'''
<div class="section people-team">
  <div class="container">{rail_section(ctx, page, team)}</div>
</div>'''
    contact = d.section("Contact Our Team")
    return hero + leadership + team_html + cta_band(ctx, page, contact, statement=contact.tagline)


def render_profile(ctx, page):
    d = page["doc"]
    slug = page["slug"]
    role, cred = [x.strip() for x in d.intro[0].text.split(" \\\\ ", 1)]
    hero = f'''
<section class="profile-hero" aria-labelledby="page-title">
  <div class="container">{breadcrumb_html(page)}</div>
  <div class="container profile-grid">
    <div class="profile-head">
      <p class="profile-role">{esc(plain(role))}</p>
      <h1 class="h1 profile-name" id="page-title">{esc(d.title)}</h1>
      <p class="profile-cred">{cred_line(cred)}</p>
    </div>
    <div class="profile-portrait">{portrait(slug, d.title, page["href"], plain(role))}</div>
  </div>
</section>'''

    bio = d.section("Profile")
    facts = []
    for s in d.sections:
        if s.heading in ("Profile", "Contact"):
            continue
        sid = slugify(s.heading)
        if s.heading.startswith("Areas of"):
            items = s.blocks[0].items
            body = '<ul class="fact-list" role="list">' + "".join(f"<li>{inline(i)}</li>" for i in items) + "</ul>"
        elif s.heading == "Professional Background":
            rows = []
            for b in s.blocks:
                parts = b.text.split(" \\\\ ")
                when = plain(parts[0])
                rest = "".join(f'<span class="tl-line">{inline(x)}</span>' for x in parts[1:])
                rows.append(f'<li class="tl-item"><strong class="tl-when">{esc(when)}</strong>{rest}</li>')
            body = '<ol class="timeline" role="list">' + "".join(rows) + "</ol>"
        elif s.heading == "Education":
            rows = []
            for b in s.blocks:
                parts = b.text.split(" \\\\ ")
                lines = "".join(f'<span class="edu-line">{inline(x)}</span>' for x in parts[1:])
                rows.append(f'<li class="edu-item"><strong class="edu-degree">{inline(plain(parts[0]))}</strong>{lines}</li>')
            body = '<ul class="edu-list" role="list">' + "".join(rows) + "</ul>"
        elif s.heading == "Languages":
            body = "".join(f'<p class="langs">{cred_line(b.text)}</p>' for b in s.blocks)
        else:   # memberships
            body = "".join(para(b.text) for b in s.blocks)
        facts.append(f'<section class="fact" aria-labelledby="{sid}"><h2 class="fact-title" id="{sid}">{esc(s.heading)}</h2>{body}</section>')

    body = f'''
<div class="section section--white profile-body">
  <div class="container profile-grid">
    <section class="profile-bio" aria-labelledby="profile">
      <h2 class="label sec-label" id="profile">{esc(bio.heading)}</h2>
      <div class="prose">{"".join(para(b.text) for b in bio.blocks)}</div>
    </section>
    <div class="profile-facts">{"".join(facts)}</div>
  </div>
</div>'''
    contact = d.section("Contact")
    firm, place = [plain(x).strip() for x in contact.blocks[0].text.split(" \\\\ ")]
    label = strip_arrow([b for b in contact.blocks if b.kind == "cta"][0].text)
    band = f'''
<section class="section cta-band cta-band--navy profile-contact" aria-labelledby="contact-title">
  <div class="container cta-inner">
    <div class="cta-text">
      <h2 class="label sec-label" id="contact-title">{esc(contact.heading)}</h2>
      <p class="cta-statement">{esc(firm)}</p>
      <p class="lead">{esc(place)}</p>
    </div>
    <div class="cta-actions">{btn(rel(page["href"], CTA_TARGETS[label]), label, "btn--light")}</div>
  </div>
</section>'''
    return hero + body + band


# ---------------------------------------------------------------- capabilities and industries

def related_band(ctx, page, sections):
    cols = []
    for s in sections:
        kind = "capabilities" if s.heading == "Related Capabilities" else "industries"
        lookup = ctx.cap_by_title if kind == "capabilities" else ctx.ind_by_title
        items = []
        for name in s.blocks[0].items:
            slug = lookup[plain(name)]
            items.append(f'<li><a class="related-link" href="{esc(rel(page["href"], kind + "/" + slug))}"><span>{inline(name)}</span>{ARROW}</a></li>')
        sid = slugify(s.heading)
        cols.append(f'''
    <section class="related-col" aria-labelledby="{sid}">
      <h2 class="label sec-label" id="{sid}">{esc(s.heading)}</h2>
      <ul class="related-list" role="list">{"".join(items)}</ul>
    </section>''')
    return f'''
<div class="section section--sand related-band">
  <div class="container related-grid{' related-grid--single' if len(cols) == 1 else ''}">{"".join(cols)}
  </div>
</div>'''


def render_practice(ctx, page):
    d = page["doc"]
    kind = page["type"]
    hero = page_hero(ctx, page, d, cls="practice-hero", show_crumbs=True,
                     intro_html='<div class="page-intro practice-intro">' +
                     "".join(para(b.text, cls="lead" if i == 0 else "") for i, b in enumerate(d.intro)) + "</div>")
    secs = []
    for s in d.sections:
        if s.heading in ("Related Capabilities", "Related Industries", "Contact"):
            continue
        if s.heading == "How We Assist":
            intro = "".join(para(b.text, cls="svc-intro") for b in s.blocks if b.kind == "p")
            lists = "".join(lead_items(b.items, "svc-list", "svc-name", "svc-desc") for b in s.blocks if b.kind == "ul")
            secs.append(rail_section(ctx, page, s, cls="doc-sec--assist", body=intro + lists))
        elif s.heading.startswith("Key Legal Issues"):
            rows = []
            for b in s.blocks:
                lead, rest = split_bold_lead(b.text)
                rows.append(f'<p class="issue"><strong class="issue-lead">{inline(lead)}</strong> {inline(rest)}</p>'
                            if lead else para(b.text))
            secs.append(rail_section(ctx, page, s, cls="doc-sec--issues", body='<div class="issues">' + "".join(rows) + "</div>"))
        else:
            secs.append(rail_section(ctx, page, s))
    body = f'''
<div class="section section--white practice-body">
  <div class="container">{"".join(secs)}
  </div>
</div>'''
    related = related_band(ctx, page, [s for s in d.sections if s.heading.startswith("Related ")])
    contact = d.section("Contact")
    return hero + body + related + cta_band(ctx, page, contact)


def render_index(ctx, page):
    kind = page["type"]            # cap-index | ind-index
    items = C.CAPABILITIES if kind == "cap-index" else C.INDUSTRIES
    folder = "capabilities/" if kind == "cap-index" else "industries/"
    rows = []
    for i, (slug, title) in enumerate(items, 1):
        doc = ctx.pages[folder + slug]["doc"]
        rows.append(f'''
      <li><a class="cap-row" href="{esc(rel(page["href"], folder + slug))}">
        <span class="cap-row-num" aria-hidden="true">{i:02d}</span>
        <h2 class="cap-row-title">{esc(title)}</h2>
        <p class="cap-row-desc">{inline(doc.tagline)}</p>
        <span class="cap-row-arrow">{ARROW}</span>
      </a></li>''')
    return f'''
<section class="index-page" aria-labelledby="page-title">
  <div class="container">
    {breadcrumb_html(page)}
    <h1 class="h1 page-title" id="page-title">{esc(page["h1"])}</h1>
    <ol class="cap-rows" role="list">{"".join(rows)}
    </ol>
  </div>
</section>'''


# ---------------------------------------------------------------- contact

def render_contact(ctx, page):
    d = page["doc"]
    h = page["href"]
    hero = page_hero(ctx, page, d, cls="contact-hero")

    git = d.section("Get in Touch")
    ps = [b for b in git.blocks if b.kind == "p"]
    ctas = [strip_arrow(b.text) for b in git.blocks if b.kind == "cta"]
    # Blocks as supplied: introduction, "Send Us an Email ->", address, "Contact Us on WhatsApp ->", number, caution
    intro_p, email_p, wa_p, notice_p = ps[0], ps[1], ps[2], ps[3]
    methods = f'''
      <ul class="methods" role="list">
        <li><a class="method" href="{esc(C.EMAIL_HREF)}">
          <span class="method-icon">{ICON_MAIL}</span>
          <span class="method-label">{esc(ctas[0])}</span>
          <span class="method-value">{esc(plain(email_p.text))}</span>
          <span class="method-arrow">{ARROW}</span>
        </a></li>
        <li><a class="method" href="{esc(C.WHATSAPP_HREF)}" rel="noopener">
          <span class="method-icon">{ICON_CHAT}</span>
          <span class="method-label">{esc(ctas[1])}</span>
          <span class="method-value">{esc(plain(wa_p.text))}</span>
          <span class="method-arrow">{ARROW}</span>
        </a></li>
      </ul>'''
    git_html = f'''
    <section class="contact-git" aria-labelledby="get-in-touch">
      <h2 class="label sec-label" id="get-in-touch">{esc(git.heading)}</h2>
      <p class="sec-tagline">{inline(git.tagline)}</p>
      {para(intro_p.text, cls="contact-git-intro")}
      {methods}
      {para(notice_p.text, cls="contact-caution")}
    </section>'''

    det = d.section("Contact Details")
    lines = det.blocks[0].text.split(" \\\\ ")
    firm = plain(lines[0])
    tel_label, tel_nums = lines[1].split(": ", 1)
    tel_html = '<span class="cred-sep"> | </span>'.join(
        f'<a href="tel:{dict(C.PHONES)[n.strip()]}">{esc(n.strip())}</a>' for n in tel_nums.split("|"))
    det_html = f'''
    <section class="contact-details" aria-labelledby="contact-details">
      <h2 class="label sec-label" id="contact-details">{esc(det.heading)}</h2>
      <p class="sec-tagline">{inline(det.tagline)}</p>
      <address class="office-card">
        <p class="office-firm">{esc(firm)}</p>
        <p class="office-line"><span class="office-label">{esc(tel_label)}:</span> {tel_html}</p>
        <p class="office-line">{nowrap(esc(lines[2]))}</p>
        <p class="office-line">{esc(lines[3])}</p>
        <p class="office-line">{esc(lines[4])}</p>
      </address>
    </section>'''
    top = f'''
<section class="section section--white contact-top" aria-label="{esc(git.heading)}; {esc(det.heading)}">
  <div class="container contact-top-grid">{git_html}{det_html}
  </div>
</section>'''

    enq = d.section("Send an Enquiry")
    enq_ps = [b for b in enq.blocks if b.kind == "p"]
    fields = [b for b in enq.blocks if b.kind == "ul"][0].items
    form = enquiry_form(ctx, page, fields)
    after = "".join(para(b.text, cls="form-after") for b in enq_ps[1:])
    nxt = d.section("What Happens Next")
    steps = lead_items(nxt.blocks[0].items, "steps", "step-name", "step-desc", numbered=True, tag="ol")
    enquiry = f'''
<section class="section enquiry" aria-label="{esc(enq.heading)}; {esc(nxt.heading)}">
  <div class="container enquiry-grid">
    <section class="enquiry-main" aria-labelledby="send-an-enquiry">
      <h2 class="label sec-label" id="send-an-enquiry">{esc(enq.heading)}</h2>
      <p class="sec-tagline">{inline(enq.tagline)}</p>
      {para(enq_ps[0].text, cls="enquiry-intro")}
      {form}
      <div class="form-after-wrap">{after}</div>
    </section>
    <section class="enquiry-next" aria-labelledby="what-happens-next">
      <h2 class="label sec-label" id="what-happens-next">{esc(nxt.heading)}</h2>
      <p class="sec-tagline">{inline(nxt.tagline)}</p>
      {steps}
    </section>
  </div>
</section>'''

    visit = d.section("Visit Our Office")
    visit_ps = [b for b in visit.blocks if b.kind == "p" and not b.text.startswith("[")]
    other = d.section("Other Enquiries")
    oname, otext = split_lead(other.blocks[0].items[0])
    # "please visit Careers →": the last word is the link to the Careers page
    otext_plain = strip_arrow(otext)
    head, last = otext_plain.rsplit(" ", 1)
    other_html = (f'<p class="other-line"><strong>{inline(oname)}</strong><span class="sep"> — </span>'
                  f'{inline(head)} <a class="inline-arrow" href="{esc(rel(h, "careers"))}">{esc(last)}{ARROW}</a></p>')
    visit_html = f'''
<section class="section section--white visit" aria-labelledby="visit-our-office">
  <div class="container visit-grid">
    <div class="visit-text">
      <h2 class="label sec-label" id="visit-our-office">{esc(visit.heading)}</h2>
      <p class="sec-tagline">{inline(visit.tagline)}</p>
      <div class="prose">{"".join(para(b.text) for b in visit_ps)}</div>
      <section class="other-enquiries" aria-labelledby="other-enquiries">
        <h2 class="label sec-label" id="other-enquiries">{esc(other.heading)}</h2>
        {other_html}
      </section>
    </div>
    <div class="visit-map">{map_block(ctx, page)}</div>
  </div>
</section>'''
    return hero + top + enquiry + visit_html


def map_block(ctx, page):
    if C.MAP["VERIFIED"]:
        lat, lng = C.MAP["LAT"], C.MAP["LNG"]
        src = f"https://maps.google.com/maps?q={lat},{lng}&z=17&output=embed"
        directions = f"https://www.google.com/maps/dir/?api=1&destination={lat},{lng}"
        return f'''
      <div class="contact-map" data-map data-map-src="{esc(src)}" data-map-title="Google Map: Baba Law Firm, Damascus">
        <div class="contact-map-ph">
          <p class="contact-map-addr">{nowrap(esc(C.ADDRESS_LINE))}</p>
          <button type="button" class="btn btn--light btn--sm" data-map-load><span>Load Google Map</span></button>
          <p class="contact-map-note">Loading the map connects to Google, which may set cookies. See our <a href="{esc(rel(page["href"], "cookie-policy"))}">Cookie Policy</a>.</p>
        </div>
      </div>
      <p class="map-directions"><a class="link-arrow" href="{esc(directions)}" target="_blank" rel="noopener"><span>Get Directions<span class="visually-hidden"> (opens in a new tab)</span></span>{EXT}</a></p>'''
    note = ('<p class="preview-note">Preview: the map and a “Get Directions” link will be added once the exact office location is confirmed.</p>'
            if ctx.preview else "")
    return f'''
      <div class="map-pending">
        <div class="map-pending-media" aria-hidden="true">{img("skyline", "(min-width: 960px) 50vw, 100vw")}</div>
        <div class="map-pending-text">
          <p class="map-pending-firm">Baba Law Firm</p>
          <p class="map-pending-addr">{nowrap(esc(C.ADDRESS_LINE))}</p>
          {note}
        </div>
      </div>'''


def enquiry_form(ctx, page, fields):
    """The enquiry form, with the labels exactly as supplied."""
    def label_parts(raw):
        req = raw.endswith(" *")
        return (raw[:-2] if req else raw), req

    def field(fid, raw, control, full=False, name_attr=None):
        lab, req = label_parts(raw)
        star = ' <span class="req" aria-hidden="true">*</span>' if req else ""
        return (f'<div class="field{" field--full" if full else ""}" data-label="{esc(lab)}">'
                f'<label for="{fid}">{esc(lab)}{star}</label>{control}'
                f'<p class="field-error" id="{fid}-error"></p></div>')

    names = [plain(x) for x in fields]
    area_opts = "".join(f"<option>{esc(t)}</option>" for _, t in C.CAPABILITIES) + "<option>Other</option>"
    lang_opts = "".join(f"<option>{l}</option>" for l in ("Arabic", "English", "French"))
    ack_label = [x for x in fields if x.startswith("**Privacy acknowledgement")][0]
    ack_title, ack_text = split_lead(ack_label)
    ack_title = plain(ack_title)
    pp = rel(page["href"], "privacy-policy")
    ack_html = inline(ack_text, {"Privacy Policy": f'<a href="{esc(pp)}" target="_blank" rel="noopener">Privacy Policy<span class="visually-hidden"> (opens in a new tab)</span></a>'})
    req_ack = ack_title.endswith(" *")
    ack_legend = ack_title[:-2] if req_ack else ack_title

    def inp(fid, name, typ="text", req=False, auto="", extra=""):
        r = " required" if req else ""
        a = f' autocomplete="{auto}"' if auto else ""
        return f'<input class="input" type="{typ}" id="{fid}" name="{name}"{r}{a} aria-describedby="{fid}-error"{extra}>'

    endpoint = f' action="{esc(C.FORM_ENDPOINT)}" data-endpoint="{esc(C.FORM_ENDPOINT)}"' if C.FORM_ENDPOINT else ""
    preview = (' data-preview="true"' if ctx.preview and not C.FORM_ENDPOINT else "")
    rows = [
        '<div class="form-row form-row--2">'
        + field("enq-name", names[0], inp("enq-name", "name", req=True, auto="name", extra=' autocapitalize="words"'))
        + field("enq-org", names[1], inp("enq-org", "organisation", auto="organization"))
        + "</div>",
        '<div class="form-row form-row--2">'
        + field("enq-email", names[2], inp("enq-email", "email", "email", req=True, auto="email", extra=' spellcheck="false"'))
        + field("enq-tel", names[3], inp("enq-tel", "telephone", "tel", auto="tel", extra=' inputmode="tel"'))
        + "</div>",
        '<div class="form-row form-row--2">'
        + field("enq-area", names[4], f'<select class="select" id="enq-area" name="area" aria-describedby="enq-area-error"><option value="">Select…</option>{area_opts}</select>')
        + field("enq-lang", names[5], f'<select class="select" id="enq-lang" name="language" aria-describedby="enq-lang-error"><option value="">Select…</option>{lang_opts}</select>')
        + "</div>",
        field("enq-subject", names[6], inp("enq-subject", "subject", req=True), full=True),
        field("enq-message", names[7], '<textarea class="textarea" id="enq-message" name="message" required aria-describedby="enq-message-error" rows="7"></textarea>', full=True),
        f'''<fieldset class="field field--consent" data-label="{esc(ack_legend)}">
          <legend>{esc(ack_legend)}{' <span class="req" aria-hidden="true">*</span>' if req_ack else ""}</legend>
          <label class="check"><input type="checkbox" id="enq-privacy" name="privacy" value="yes"{" required" if req_ack else ""} aria-describedby="enq-privacy-error"><span>{ack_html}</span></label>
          <p class="field-error" id="enq-privacy-error"></p>
        </fieldset>''',
    ]
    submit_label = "Submit Enquiry"
    success_note = ('<p class="preview-note">Preview: this form is not yet connected, so no message has been sent. '
                    'On the live website, enquiries are delivered to info@babalawfirm.net.</p>' if preview else "")
    return f'''
      <form class="form enquiry-form" id="enquiry-form" method="post" novalidate data-form data-success="enquiry-success"{endpoint}{preview} aria-labelledby="send-an-enquiry">
        <div class="error-summary" data-error-summary tabindex="-1" hidden role="alert"></div>
        {"".join(rows)}
        <div class="hp" aria-hidden="true"><label for="enq-website">Leave this field empty</label><input type="text" id="enq-website" name="website" tabindex="-1" autocomplete="off"></div>
        <div class="form-submit"><button class="btn btn--primary" type="submit"><span>{submit_label}</span>{ARROW}</button></div>
      </form>
      <div class="form-success" id="enquiry-success" tabindex="-1" hidden role="status">
        <p class="form-success-title">Thank you.</p>
        <p>We will review your message and contact you to discuss how we may assist.</p>
        {success_note}
      </div>
      <div class="form-failure" id="enquiry-failure" tabindex="-1" hidden role="alert">
        <p>Your enquiry could not be sent. Please email <a href="{esc(C.EMAIL_HREF)}">{C.EMAIL}</a> or call <a href="tel:{C.PHONES[0][1]}">{C.PHONES[0][0]}</a>.</p>
      </div>'''


# ---------------------------------------------------------------- legal pages, careers, sitemap, 404

def legal_heading(text):
    m = re.match(r"^(\d+)\.\s+(.*)$", text)
    if m:
        return f'<span class="legal-num">{m.group(1)}.</span> {esc(m.group(2))}', m.group(2)
    return esc(text), text


def render_legal(ctx, page):
    d = page["doc"]
    h = page["href"]
    meta = ""
    intro_blocks = list(d.intro)
    if intro_blocks and intro_blocks[0].kind == "p" and intro_blocks[0].text.startswith("Effective from"):
        meta = f'<div class="legal-meta"><p class="legal-updated"><span>{esc(intro_blocks[0].text)}</span></p></div>'
        intro_blocks = intro_blocks[1:]
    hero = page_hero(ctx, page, d, intro_html=meta, cls="legal-hero")

    links = {
        "Contact page": f'<a href="{esc(rel(h, "contact"))}">Contact page</a>',
        "Cookie Policy": f'<a href="{esc(rel(h, "cookie-policy"))}">Cookie Policy</a>',
        "Privacy Policy": f'<a href="{esc(rel(h, "privacy-policy"))}">Privacy Policy</a>',
    }
    settings_btn = '<button type="button" class="inline-link" data-cookie-settings>Cookie Settings</button>'
    toc, secs = [], []
    for s in d.sections:
        sid = slugify(re.sub(r"^\d+\.\s+", "", s.heading))
        head_html, head_text = legal_heading(s.heading)
        num = re.match(r"^(\d+)\.", s.heading)
        toc_num = f'<span class="legal-toc-num">{num.group(1)}</span>' if num else ""
        toc.append(f'<li><a href="#{sid}">{toc_num}<span class="legal-toc-text">{esc(head_text)}</span></a></li>')
        parts = []
        if s.tagline:
            parts.append(f'<p class="italic-line">{inline(s.tagline, email_links(s.tagline) or None)}</p>')
        if s.heading == "Contact Information":
            parts.append(legal_address(d, s))
        else:
            for b in s.blocks:
                if b.kind == "p":
                    t = b.text
                    l = {k: v for k, v in links.items() if k in t and k != d.title}
                    if "Cookie Settings →" in t:
                        l["Cookie Settings →"] = settings_btn
                    elif "Cookie Settings" in t:
                        l["Cookie Settings"] = settings_btn
                    parts.append(para(t, l))
                elif b.kind == "ul":
                    parts.append('<ul class="legal-list bullets">' + "".join(f"<li>{inline(i)}</li>" for i in b.items) + "</ul>")
                elif b.kind == "h3":
                    parts.append(f'<h3 class="legal-h3">{inline(b.text)}</h3>')
        secs.append(f'<section class="legal-section" aria-labelledby="{sid}"><h2 class="legal-h2" id="{sid}">{head_html}</h2>{"".join(parts)}</section>')
    intro_html = "".join(para(b.text, {k: v for k, v in links.items() if k in b.text and k != d.title}) for b in intro_blocks)
    intro_sec = f'<div class="legal-intro">{intro_html}</div>' if intro_html else ""
    toc_list = "".join(toc)
    return hero + f'''
<div class="section legal-body">
  <div class="container legal-layout">
    <div class="legal-toc-col">
      <nav class="legal-toc" aria-labelledby="toc-title">
        <p class="legal-toc-title" id="toc-title">On this page</p>
        <ol class="legal-toc-list" role="list">{toc_list}</ol>
      </nav>
      <details class="legal-toc-m">
        <summary><span>On this page</span><span class="legal-toc-m-icon" aria-hidden="true"></span></summary>
        <nav aria-label="On this page (collapsed list)"><ol class="legal-toc-list" role="list">{toc_list}</ol></nav>
      </details>
    </div>
    <article class="legal-article">
      {intro_sec}
      {"".join(secs)}
    </article>
  </div>
</div>'''


def legal_address(d, s):
    """Legal Notice > Contact Information, with email and telephone as links."""
    ps = [b.text for b in s.blocks]
    first = '<span class="legal-sep">|</span>'.join(f"<span>{esc(x.strip())}</span>" for x in ps[0].split("|"))
    addr_label, addr = ps[1].split(": ", 1)
    mail_label, mail = ps[2].split(": ", 1)
    tel_label, tels = ps[3].split(": ", 1)
    tel_html = '<span class="legal-sep">|</span>'.join(
        f'<a href="tel:{dict(C.PHONES)[t.strip()]}">{esc(t.strip())}</a>' for t in tels.split("|"))
    return f'''
      <address class="legal-address">
        <p class="legal-address-firm">{first}</p>
        <p>{esc(addr_label)}: {nowrap(esc(addr))}</p>
        <p class="legal-address-contact">{esc(mail_label)}: <a href="mailto:{esc(mail)}">{esc(mail)}</a></p>
        <p class="legal-address-contact">{esc(tel_label)}: {tel_html}</p>
      </address>'''


def render_careers(ctx, page):
    d = page["doc"]
    h = page["href"]
    hero = page_hero(ctx, page, d, cls="careers-hero")
    secs = []
    for s in d.sections:
        if s.heading == "What We Look For":
            body = lead_items(s.blocks[0].items, "skills", "skill-name", "skill-desc")
            secs.append(rail_section(ctx, page, s, body=body))
        elif s.heading == "Current Opportunities":
            ps = [b for b in s.blocks if not b.text.startswith("[")]
            body = "".join(para(b.text) for b in ps)
            body += ('<div class="vacancies" role="status"><p>There are currently no advertised vacancies. '
                     'General applications are welcome.</p></div>')
            secs.append(rail_section(ctx, page, s, body=body))
        elif s.heading == "Apply to Join Us":
            parts = []
            for b in s.blocks:
                if b.kind == "cta":
                    parts.append(f'<div class="actions apply-actions">{btn("mailto:" + C.CAREERS_EMAIL, strip_arrow(b.text))}</div>')
                else:
                    parts.append(para(b.text))
            secs.append(rail_section(ctx, page, s, cls="doc-sec--apply", body="".join(parts)))
        elif s.heading == "Applicant Privacy":
            l = {"Privacy Policy": f'<a href="{esc(rel(h, "privacy-policy"))}">Privacy Policy</a>'}
            secs.append(rail_section(ctx, page, s, links=l))
        else:
            secs.append(rail_section(ctx, page, s))
    return hero + f'''
<div class="section section--white careers-body">
  <div class="container">{"".join(secs)}
  </div>
</div>'''


def render_sitemap(ctx, page):
    h = page["href"]

    def li(href, label):
        return f'<li><a href="{esc(rel(h, href))}">{esc(label)}</a></li>'
    groups = [
        ("The Firm", [("", "Home"), ("our-firm", "Our Firm"), ("our-people/", "Our People")] +
         [("our-people/" + s, n) for s, n in C.PEOPLE]),
        ("Capabilities", [("capabilities/", "All Capabilities")] + [("capabilities/" + s, t) for s, t in C.CAPABILITIES]),
        ("Industries", [("industries/", "All Industries")] + [("industries/" + s, t) for s, t in C.INDUSTRIES]),
        ("Contact and Information", [("contact", "Contact"), ("careers", "Careers"), ("privacy-policy", "Privacy Policy"),
                                     ("cookie-policy", "Cookie Policy"), ("legal-notice", "Legal Notice")]),
    ]
    cols = "".join(
        f'<section class="sitemap-group" aria-labelledby="sm-{slugify(g)}"><h2 class="label sec-label" id="sm-{slugify(g)}">{esc(g)}</h2>'
        f'<ul class="sitemap-list" role="list">{"".join(li(a, b) for a, b in items)}</ul></section>'
        for g, items in groups)
    return f'''
<section class="index-page sitemap-page" aria-labelledby="page-title">
  <div class="container">
    {breadcrumb_html(page)}
    <h1 class="h1 page-title" id="page-title">Sitemap</h1>
    <div class="sitemap-grid">{cols}</div>
  </div>
</section>'''


def render_404(ctx, page):
    links = [("our-firm", "Our Firm"), ("capabilities/", "Capabilities"), ("industries/", "Industries"), ("contact", "Contact")]
    items = "".join(f"<li>{link_arrow(href, label)}</li>" for href, label in links)
    return f'''
<section class="nf" aria-labelledby="nf-title">
  <div class="container nf-grid">
    <div class="nf-text">
      <h1 class="h1" id="nf-title">Page Not Found</h1>
      <p class="lead">The page you are looking for may have been moved or renamed, or may no longer be available.</p>
      <ul class="nf-links" role="list">{items}</ul>
    </div>
    <div class="nf-arch" aria-hidden="true"><div class="nf-arch-frame"><span class="nf-code">404</span></div></div>
  </div>
</section>'''


# ---------------------------------------------------------------- structured data

def firm_node():
    return {
        "@type": "LegalService",
        "@id": C.DOMAIN + "/#firm",
        "name": C.SITE_NAME,
        "url": C.DOMAIN + "/",
        "logo": C.DOMAIN + "/assets/img/logo/baba-law-firm-logo.png",
        "image": C.DOMAIN + "/assets/img/og-image.png",
        "foundingDate": C.FOUNDING_YEAR,
        "email": C.EMAIL,
        "telephone": C.PHONES[0][0],
        "faxNumber": C.FAX,
        "address": {
            "@type": "PostalAddress",
            "streetAddress": C.STREET,
            "postOfficeBoxNumber": C.PO_BOX,
            "addressLocality": "Damascus",
            "addressCountry": "SY",
        },
        "availableLanguage": ["ar", "en", "fr"],
        "areaServed": {"@type": "Country", "name": "Syria"},
    }


PERSON_SCHEMA = {
    "mohamad-baba": {
        "name": "Mohamad Baba", "honorificPrefix": "Dr.", "jobTitle": "Managing Partner",
        "alumniOf": ["Islamic University of Lebanon", "Fordham University School of Law", "Beirut Arab University"],
        "knowsLanguage": ["ar", "en", "fr"],
        "memberOf": "Syrian Bar Association — Damascus Branch",
    },
    "tawfeeq-baba": {
        "name": "Tawfeeq Baba", "jobTitle": "Senior Counsel",
        "alumniOf": ["University of Aleppo"],
    },
}


def jsonld(ctx, page):
    graph = [firm_node()]
    crumbs = page.get("crumbs") or []
    if crumbs:
        graph.append({
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "name": label, "item": canonical(href)}
                for i, (label, href) in enumerate(crumbs)
            ],
        })
    url = canonical(page["href"])
    if page["type"] == "profile":
        p = PERSON_SCHEMA[page["slug"]]
        node = {"@type": "Person", "@id": url + "#person", "name": p["name"], "jobTitle": p["jobTitle"],
                "url": url, "worksFor": {"@id": C.DOMAIN + "/#firm"},
                "alumniOf": [{"@type": "CollegeOrUniversity", "name": n} for n in p["alumniOf"]]}
        if "honorificPrefix" in p:
            node["honorificPrefix"] = p["honorificPrefix"]
        if "knowsLanguage" in p:
            node["knowsLanguage"] = p["knowsLanguage"]
        if "memberOf" in p:
            node["memberOf"] = {"@type": "Organization", "name": p["memberOf"]}
        if C.PORTRAITS[page["slug"]]["src"]:
            node["image"] = C.DOMAIN + "/" + C.PORTRAITS[page["slug"]]["src"] + "-1200.jpg"
        graph.append(node)
    if page["type"] in ("capability", "industry"):
        graph.append({"@type": "Service", "@id": url + "#service", "name": page["h1"], "serviceType": page["h1"],
                      "url": url, "description": page["seo"]["description"],
                      "provider": {"@id": C.DOMAIN + "/#firm"},
                      "areaServed": {"@type": "Country", "name": "Syria"}})
    if page["type"] == "home":
        graph.append({"@type": "WebSite", "@id": C.DOMAIN + "/#website", "url": C.DOMAIN + "/",
                      "name": C.SITE_NAME, "inLanguage": "en", "publisher": {"@id": C.DOMAIN + "/#firm"}})
    data = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))
    return '<script type="application/ld+json">' + data.replace("</", "<\\/") + "</script>"


# ---------------------------------------------------------------- page shell

def header(ctx, page, overlay):
    h = page["href"]
    cur = page.get("section_href")
    def current(href):
        if href != cur:
            return ""
        return ' aria-current="page"' if href == h else ' aria-current="true"'
    items = "".join(f'<li><a href="{esc(rel(h, href))}"{current(href)}>{esc(label)}</a></li>'
                    for href, label in C.PRIMARY_NAV)
    home = rel(h, "")
    brand = (f'<a class="brand" href="{esc(home)}"><svg class="brand-logo" viewBox="0 0 1230 314" aria-hidden="true" focusable="false">'
             f'<use href="#baba-logo"/></svg><span class="visually-hidden">Baba Law Firm — home</span></a>')
    phone = C.PHONES[0]
    return f'''
<a class="skip-link" href="#main">Skip to main content</a>
<header class="site-header{' is-overlay' if overlay else ''}" data-header>
  <div class="container header-inner">
    {brand}
    <nav class="primary-nav" aria-label="Main"><ul class="nav-list" role="list">{items}</ul></nav>
    <div class="header-actions">
      <a class="header-icon" href="{esc(C.EMAIL_HREF)}">{ICON_MAIL}<span class="visually-hidden">Email {C.EMAIL}</span></a>
      <a class="header-icon" href="{esc(C.WHATSAPP_HREF)}" rel="noopener">{ICON_CHAT}<span class="visually-hidden">WhatsApp {C.WHATSAPP_DISPLAY}</span></a>
      <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="mobile-menu" data-menu-open>
        <span class="menu-toggle-label">Menu</span><span class="menu-icon" aria-hidden="true"><span></span><span></span></span>
      </button>
    </div>
  </div>
</header>
<div class="mobile-menu" id="mobile-menu" role="dialog" aria-modal="true" aria-label="Menu" hidden data-menu>
  <div class="mobile-menu-top container">
    {brand.replace('class="brand"', 'class="brand" tabindex="-1"')}
    <button class="menu-close" type="button" data-menu-close><span>Close</span><span class="menu-x" aria-hidden="true"></span></button>
  </div>
  <nav class="container mobile-nav" aria-label="Main menu"><ul class="mobile-nav-list" role="list">{items}</ul></nav>
  <div class="container mobile-menu-foot">
    <ul class="mobile-contact" role="list">
      <li><span class="mobile-contact-label">Email</span><a href="{esc(C.EMAIL_HREF)}">{C.EMAIL}</a></li>
      <li><span class="mobile-contact-label">WhatsApp</span><a href="{esc(C.WHATSAPP_HREF)}" rel="noopener">{C.WHATSAPP_DISPLAY}</a></li>
      <li><span class="mobile-contact-label">Telephone</span><a href="tel:{phone[1]}">{phone[0]}</a></li>
    </ul>
  </div>
</div>'''


def footer(ctx, page):
    h = page["href"]
    nav = "".join(f'<li><a href="{esc(rel(h, href))}">{esc(label)}</a></li>' for href, label in C.FOOTER_NAV)
    legal = "".join(f'<li><a href="{esc(rel(h, href))}">{esc(label)}</a></li>' for href, label in C.FOOTER_LEGAL)
    tels = '<span class="footer-sep" aria-hidden="true"> | </span>'.join(f'<a href="tel:{t}">{d}</a>' for d, t in C.PHONES)
    return f'''
<footer class="site-footer">
  <div class="ablaq-band" aria-hidden="true"></div>
  <div class="container footer-top">
    <div class="footer-brand">
      <a class="brand" href="{esc(rel(h, ''))}"><svg class="brand-logo" viewBox="0 0 1230 314" aria-hidden="true" focusable="false"><use href="#baba-logo"/></svg><span class="visually-hidden">Baba Law Firm — home</span></a>
    </div>
    <nav class="footer-nav" aria-label="Footer"><ul role="list">{nav}</ul></nav>
    <ul role="list" class="footer-contact">
      <li><span class="footer-label">Email</span><a href="{esc(C.EMAIL_HREF)}">{C.EMAIL}</a></li>
      <li><span class="footer-label">WhatsApp</span><a href="{esc(C.WHATSAPP_HREF)}" rel="noopener">{C.WHATSAPP_DISPLAY}</a></li>
      <li><span class="footer-label">Telephone</span><span class="footer-tels">{tels}</span></li>
    </ul>
    <address class="footer-address">
      <span class="footer-label">Office</span>
      <span class="footer-firm">{C.SITE_NAME}</span>
      <span>{nowrap(esc(C.ADDRESS_LINE))}</span>
      <span>{esc(C.PO_BOX_LINE)}</span>
    </address>
  </div>
  <div class="container footer-bottom">
    <ul role="list" class="footer-legal">{legal}<li><button type="button" class="link-button" data-cookie-settings>Cookie Settings</button></li><li><a href="{esc(rel(h, 'sitemap'))}">Sitemap</a></li></ul>
    <p class="footer-copy">&copy; <span data-year>2026</span> Baba Law Firm. All rights reserved.</p>
  </div>
</footer>'''


def cookie_ui(ctx, page):
    h = page["href"]
    opt = ctx.optional
    toggles = ""
    if opt:
        rows = "".join(f'''
        <div class="consent-row">
          <div><h3 class="consent-name" id="c-{o["key"]}-l">{esc(o["name"])}</h3><p id="c-{o["key"]}-d">{esc(o["description"])}</p></div>
          <label class="switch"><input type="checkbox" name="{o["key"]}" aria-labelledby="c-{o["key"]}-l" aria-describedby="c-{o["key"]}-d" data-consent-toggle="{o["key"]}"><span class="switch-ui" aria-hidden="true"></span></label>
        </div>''' for o in opt)
        toggles = f'''
      <fieldset class="consent-list">
        <legend class="visually-hidden">Cookie categories</legend>
        <div class="consent-row">
          <div><h3 class="consent-name">Strictly necessary</h3><p>Required for the website to work securely, including the record of your choices here.</p></div>
          <span class="consent-fixed">Always on</span>
        </div>{rows}
      </fieldset>'''
    if C.COOKIE_REGISTER:
        trs = "".join(
            f'<tr><th scope="row" data-label="Name"><code>{esc(c["name"])}</code></th><td data-label="Provider">{esc(c["provider"])}</td>'
            f'<td data-label="Purpose">{esc(c["purpose"])}</td><td data-label="Category">{esc(c["category"])}</td><td data-label="Duration">{esc(c["duration"])}</td></tr>'
            for c in C.COOKIE_REGISTER)
        register = f'''
      <div class="cookie-table-wrap"><table class="cookie-table">
        <caption class="visually-hidden">Cookie register</caption>
        <thead><tr><th scope="col">Name</th><th scope="col">Provider</th><th scope="col">Purpose</th><th scope="col">Category</th><th scope="col">Duration</th></tr></thead>
        <tbody>{trs}</tbody>
      </table></div>'''
    else:
        register = '<p class="register-empty">This website currently sets no cookies and uses no similar technologies.</p>'
    if ctx.preview:
        register += ('<p class="preview-note">Preview: before launch, this register is completed from a cookie scan of the configured live website, '
                     'listing each cookie or similar technology with its provider, purpose, category and duration.</p>')
    actions = ('<button type="submit" class="btn btn--primary btn--sm" value="save" data-consent="save"><span>Save Choices</span></button>'
               '<button type="submit" class="btn btn--ghost btn--sm" value="reject" data-consent="reject"><span>Reject Optional</span></button>'
               if opt else '<button type="submit" class="btn btn--primary btn--sm" value="close"><span>Close</span></button>')
    intro = ("Strictly necessary technologies are always active. Optional technologies are used only with your consent, "
             "and you can change your choice here at any time." if opt else
             "Strictly necessary technologies are always active. Optional technologies, if introduced, will be used only with your consent.")
    dialog = f'''
<dialog class="cookie-dialog" aria-labelledby="cookie-dialog-title" data-cookie-dialog>
  <form method="dialog" class="cookie-dialog-inner">
    <h2 id="cookie-dialog-title" class="h3">Cookie Settings</h2>
    <p>{intro} See our <a href="{esc(rel(h, 'cookie-policy'))}">Cookie Policy</a>.</p>
    {toggles}
    <h3 class="register-title">Cookie Register</h3>
    {register}
    <div class="cookie-actions">{actions}</div>
  </form>
</dialog>'''
    banner = ""
    if opt:
        names = ", ".join(o["name"].lower() for o in opt)
        banner = f'''
<div class="cookie-banner" role="region" aria-label="Cookie consent" hidden data-cookie-banner>
  <div class="cookie-banner-inner">
    <p class="cookie-title">Cookies on this website</p>
    <p>We use strictly necessary technologies to run this website. With your consent, we would also like to use optional technologies ({esc(names)}). See our <a href="{esc(rel(h, 'cookie-policy'))}">Cookie Policy</a>.</p>
    <div class="cookie-actions">
      <button type="button" class="btn btn--primary btn--sm" data-consent="reject"><span>Reject</span></button>
      <button type="button" class="btn btn--primary btn--sm" data-consent="accept"><span>Accept</span></button>
      <button type="button" class="link-button" data-cookie-settings>Settings</button>
    </div>
  </div>
</div>'''
    return banner + dialog


def layout(ctx, page, main_html, body_class, overlay=False, logo_defs=""):
    h = page["href"]
    seo = page["seo"]
    is404 = page["type"] == "404"
    base = f'<base href="{C.PREVIEW_BASE_PATH if ctx.preview else "/"}">\n' if is404 else ""
    robots = "noindex, nofollow" if (ctx.preview or is404) else "index, follow"
    url = canonical(h)
    canon = "" if is404 else f'<link rel="canonical" href="{url}">\n'
    og_url = "" if is404 else f'<meta property="og:url" content="{url}">\n'
    a = lambda p: esc(rel(h, p))
    title = esc(seo["title"])
    desc = esc(seo["description"])
    ld = "" if is404 else jsonld(ctx, page)
    opt_keys = ",".join(o["key"] for o in ctx.optional)
    return f'''<!doctype html>
<html lang="{C.LANG}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{base}<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="{robots}">
{canon}<meta property="og:type" content="{"profile" if page["type"] == "profile" else "website"}">
<meta property="og:locale" content="en_GB">
<meta property="og:site_name" content="Baba Law Firm">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
{og_url}<meta property="og:image" content="{C.DOMAIN}/assets/img/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Baba Law Firm">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{C.DOMAIN}/assets/img/og-image.png">
<meta name="theme-color" content="#101C2C">
<link rel="icon" href="{a('assets/img/favicon.svg')}" type="image/svg+xml">
<link rel="icon" href="{a('assets/img/favicon-32.png')}" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="{a('assets/img/apple-touch-icon.png')}">
<link rel="preload" href="{a('assets/fonts/manrope-latin-wght-normal.woff2')}" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{a('assets/fonts/cormorant-garamond-latin-wght-normal.woff2')}" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{a('assets/css/site.css')}">
<script>document.documentElement.classList.add('js');setTimeout(function(){{if(!window.BLF_READY)document.documentElement.classList.remove('js')}},2500)</script>
{ld}
</head>
<body class="{body_class}" data-optional="{opt_keys}">
{logo_defs}{header(ctx, page, overlay)}
<main id="main" tabindex="-1"{' class="has-overlay-header"' if overlay else ''}>
{main_html}
</main>
{footer(ctx, page)}
{cookie_ui(ctx, page)}
<script src="{a('assets/js/site.js')}" defer></script>
</body>
</html>
'''


def redirect_stub(target_rel, target_canonical):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Baba Law Firm</title>
<meta name="robots" content="noindex">
<link rel="canonical" href="{target_canonical}">
<meta http-equiv="refresh" content="0; url={target_rel}">
</head>
<body>
<p>This page has moved: <a href="{target_rel}">continue to the new page</a>.</p>
</body>
</html>
'''
