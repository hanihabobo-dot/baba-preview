# Baba Law Firm website — source

The pages in the repository root are generated. Edit the files in `src/` and rebuild:

```
python3 src/build.py               # preview build (what GitHub Pages serves): noindex, preview notes
python3 src/build.py --production  # launch build: indexable, robots.txt lists the sitemap, no preview notes, no login
python3 src/build.py --set-password  # set or change the preview password, then build the preview
```

Python 3.9+ only; no other dependencies.

## Where things live

| What | File |
|---|---|
| Approved copy, one file per page | `src/content/**/*.txt` |
| Titles and meta descriptions (Dr. Baba's tables) | `src/seo.json` |
| Contact details, map pin, form endpoint, cookie register, photographs, portraits, capability groups | `src/site_config.py` |
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

`contact.txt` keeps the order of the client's document, but the page shows Send an Enquiry first (notes of
29 October): the second paragraph of that section (Telephone · Email · Video-call meetings) is the line above
the form, and the Get in Touch caution is shown above the form as well.

Two formatting slips in the supplied PDF were normalised, without changing any words:
the Energy & Power lead-in "Oil and gas exploration, production and refining." is bold like
its siblings (the developer notes ask for every Key Legal Issues lead-in in bold), and the three
"Key Considerations for Foreign Investors" items are all sub-headings (only the first was italic).

## URLs

As in Dr. Baba's table: lowercase, no extensions. Canonical tags, structured data and
`sitemap.xml` use the production form (`https://babalawfirm.net/our-people`). On GitHub Pages the
three section pages are directory indexes (`/capabilities/`, `/industries/`, `/our-people/`), so
the address bar shows a trailing slash there. The old preview addresses sent on 10 October redirect
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
- **Photographs and portraits**: the four stock stand-ins (`PHOTOS`, free-licence photographs from
  Unsplash and Pexels) are self-hosted in `assets/img/photos/` as `{key}-{width}.avif/.webp/.jpg`, so the
  pages load nothing from third parties. They are still to be replaced by the firm's own photographs
  (rights confirmed): export the new ones under the same names, in the same three formats (the build uses
  the widths it finds on disk) and adjust `alt` and `pos`. The home hero's "Damascus at night" rests on the
  photographer's own location tag; ask the firm to confirm it recognises the view. Add the portraits
  (`PORTRAITS[...]["src"]`, served as AVIF/WebP with a JPEG fallback at 640 and 1200 px).
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
