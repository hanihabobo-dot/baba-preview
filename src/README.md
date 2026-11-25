# Baba Law Firm website — source

The pages in the repository root are generated. Edit the files in `src/` and rebuild:

```
python3 src/build.py               # preview build (what GitHub Pages serves): noindex, preview notes
python3 src/build.py --production  # launch build: indexable, robots.txt lists the sitemap, no preview notes, no login
python3 src/build.py --set-password  # set or change the preview password, then build the preview
```

The production build also writes `.htaccess` for Apache / cPanel hosting (`production_htaccess()` in
`build.py`): HTTPS and the bare domain, extensionless addresses, the 404 page, security headers (HSTS,
nosniff, Referrer-Policy, frame protection, Permissions-Policy), cache rules, MIME types and compression.
`src/package_production.py` makes the upload ZIP from a production build without touching the preview.

Python 3.9+ only; no other dependencies.

## Where things live

| What | File |
|---|---|
| Approved copy, one file per page | `src/content/**/*.txt` |
| Titles and meta descriptions (Dr. Baba's tables) | `src/seo.json` |
| Contact details, map pin, form endpoint, cookie register, Legal 500 switch, photographs, portraits, capability groups | `src/site_config.py` |
| Page layouts | `src/templates.py` |
| Styles (concatenated into `assets/css/site.css`) | `src/css/*.css` |
| Behaviour (menu, consent, form, map, WhatsApp button above the cookie banner) | `assets/js/site.js` |

### Content files

The wording is the approved copy of 19 October 2026 ("Website Content – Reviewed Final Versions" and
"Contact and Legal Pages"), word for word. The format mirrors the client's document:

```
# Page title
~ Tagline (the italic line under a title or section heading)
## Section heading
### Sub-heading
- List item (service lists: **Name** — description)
-> Button or link →
Plain lines are paragraphs. **bold**, *italic*, and " \\ " for a line break.
```

The Capabilities and Industries index pages read their tagline, introduction and closing Contact block from
`capabilities/index.txt` and `industries/index.txt` (client's texts of 24 and 25 November 2026); the lists come from
`CAPABILITIES`, `CAPABILITY_GROUPS` and `INDUSTRIES` in `site_config.py`. The Capabilities introduction gives the
number of practice areas in words ("seventeen"): the build stops if it no longer matches `CAPABILITIES`.

`contact.txt` keeps the order of the client's document, and the page follows it (client request of
21 November, replacing the form-first order of 29 October): Get in Touch, Contact Details, Send an Enquiry,
What Happens Next, Visit Our Office. The two introductory paragraphs stand in the heading, beside the arched
photograph. Since the client's request of 23 November, Get in Touch has two buttons
without the address or the number on them, Contact Details run name, address, P.O. Box, Telephone, Fax, and
there is no contact line above the form. The Get in Touch caution is shown beneath the form. The Quick Contact
QR code beside the map is `assets/img/qr/email-qr.svg`, made by `src/make_email_qr.py` (see that file).

The picture shown when a link is shared, `assets/img/og-image.png` (1200 × 630), carries the home tagline and
"Damascus · Since" `FOUNDING_YEAR`. After changing either, run `python3 src/make_og_image.py` (needs Node.js with
Playwright) and rebuild; the pages link it with `?v=` and a hash of the file, so apps fetch the new picture.

Two formatting slips in the supplied PDF were normalised, without changing any words:
the Energy & Power lead-in "Oil and gas exploration, production and refining." is bold like
its siblings (the developer notes ask for every Key Legal Issues lead-in in bold), and the three
"Key Considerations for Foreign Investors" items are all sub-headings (only the first was italic).

## URLs

As in Dr. Baba's table: lowercase, no extensions. Canonical tags, structured data and
`sitemap.xml` use the production form (`https://babalawfirm.net/our-firm`). The three section pages
are directory indexes (`/capabilities/`, `/industries/`, `/our-people/`): a static host answers the form
without the slash with a redirect, so their links, canonical tags and sitemap entries all use the
trailing slash, and nothing points at a redirect. The old preview addresses sent on 10 October redirect
to the new pages (`LEGACY_REDIRECTS` in `site_config.py`). `capabilities.html` and `industries.html` must
not exist as files, because GitHub Pages would serve them for `/capabilities` and `/industries`; the
preview 404 page sends those two old addresses on instead (`LEGACY_404_REDIRECTS`).

## Before launch (from the client's implementation notes)

- **Domain**: confirm `babalawfirm.net` (`DOMAIN` in `site_config.py`); HTTPS only, with http:// and
  www/non-www redirected (301) to the canonical form.
- **Section addresses**: the host must answer `/capabilities`, `/industries` and `/our-people` with the
  directory index (or a 301 to `/capabilities/` etc.), and must not keep files named `capabilities.html`
  or `industries.html` from an earlier upload.
- **Staging**: the preview asks for a password (`login.html`; only a salted PBKDF2 hash is stored, in
  `src/preview-login.json`). It keeps casual visitors out, but it is a browser-side check, not access
  control: GitHub Pages cannot require a login, so the files stay public to anyone who requests them
  directly, and the repository is public. For real authentication until launch, as the notes ask,
  make the repository private and host the preview behind a login (e.g. Cloudflare Pages with
  Cloudflare Access).
- **Enquiry form**: set `FORM_ENDPOINT` to a handler that delivers to info@babalawfirm.net (and
  confirm the mailbox is active). Without it the form validates and shows the confirmation only.
- **Map**: done. The firm confirmed the location on 19 October; `MAP` in `site_config.py` holds the
  office coordinates. The map loads only on request or with consent, with a "Get Directions" link.
  Because Google Maps is an optional technology, the consent banner is now shown, and the cookie scan
  must cover what Google Maps sets once loaded.
- **Cookies**: `COOKIE_REGISTER` (name, provider, purpose, category, duration) lists the consent record
  (`blf-consent-v2`, local storage) and must list only what the site really sets. A scan on 31 October 2026
  requested the Google Maps embed from the command line (empty cookie jar, every redirect followed) and
  saw Google set no cookie, so there is no Maps row yet and Cookie Settings still shows a one-line Google
  Maps note (our wording, for the client to approve). A command-line scan cannot see cookies that Google's
  scripts set in the browser, so a browser-based scan of the live domain (map loaded after consent, as an
  EU/UK and a Syria-region visitor) must confirm this before launch: add one row per cookie it finds,
  with the category exactly "Maps" (the note then disappears). Do not state on the Cookie Policy that
  Google sets no cookies. Add optional categories to `OPTIONAL_CATEGORIES`; the banner (Reject / Accept /
  Settings) appears automatically when there is at least one.
- **Analytics and Search Console**: install a privacy-respecting analytics tool and submit
  `/sitemap.xml` in Google Search Console.
- **Policies**: record the launch date internally as the effective date of the Privacy and Cookie
  Policies; show "Last updated" only when a policy is later amended.
- **Photographs and portraits**: all photographs (`PHOTOS` in `site_config.py`) are self-hosted in
  `assets/img/photos/` as `{key}-{width}.avif/.webp/.jpg`, so the pages load nothing from third parties. Replace each
  with its original when it arrives, under the same name, in the same three formats (the build uses the widths it finds
  on disk), and adjust `alt` and `pos`. Only compressed copies (sent over WhatsApp) have arrived so far:
  - `hero` (home) and `panorama` (Visit Our Office band on Contact, which uses the `hero` files through `"file"`):
    Damascus at dusk from Mount Qasioun, Adobe Stock 56856854, licensed by the firm. 1280 px only, so the hero is
    soft on large and high-density screens: the licensed full-size file is needed (640-2400 px for the hero).
  - The arched photographs beside the page titles, placed by `PAGE_PHOTOS`: `office` (Contact, the firm's own
    photograph), `hejaz` (Capabilities), `umayyad` (Industries) and `central-bank` (Regulatory Compliance & Sanctions),
    cropped to 4:5 as in the client's document of 25 November 2026. The last three are stills from the firm's film of
    Damascus, used at the firm's request. 420-784 px wide after cropping.
  - `door`, `street` (21 November) and Tawfeeq Baba's two certificates under Our Heritage on Our Firm (`cert-licence`,
    `cert-bar`, captions in `FIRM_CERTIFICATES`; straightened out of one photograph of both frames, about 700 px wide
    each; each picture opens its largest JPEG for reading). Replace the certificates with scans when they arrive.
  Portraits: `PORTRAITS[...]["src"]`, served as AVIF/WebP with a JPEG fallback at 640 and 800 px.
- **The Legal 500**: `LEGAL500` in `site_config.py`, an optional link to the firm's page in the guide, is off. Switch
  it on only when the client asks, with `url` set to that page: the home photograph then shows "Legal 500" at its foot
  on the right, the footer of every page "The Legal 500", and Our Firm a line linking to the firm's page. The client's
  notes of 24 November ask, following The Legal 500's logo rules, not to describe the firm as "ranked" or
  "recommended" and not to use their logos unless the firm is actually ranked; set `badge` to a logo file only then.
- **careers@babalawfirm.net**: confirm it is active and monitored.

## Dated information (review every three months)

Some passages state facts that go out of date. A named person at the firm should own a review every three
months (record the name and the date of the last review here once agreed), check each place below against
current sources and send any change to be made in the content files:

- Energy & Power (Industries): "The Energy Sector in Syria", the paragraphs on the November 2025
  agreements and on transit (April and July 2026).
- Telecommunications (Industries): "The Telecommunications Sector in Syria", third paragraph (June 2026).
- Aviation (Industries): "The Aviation Sector in Syria".
- Technology & FinTech (Capabilities): "Financial Technology and Electronic Payments" (August and
  September 2026).
- Regulatory Compliance & Sanctions (Capabilities): "International Sanctions", the list of measures
  lifting the sanctions.
