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
| Behaviour (menu, consent, form, map) | `assets/js/site.js` |

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

Two formatting slips in the supplied PDF were normalised, without changing any words:
the Energy & Power lead-in "Oil and gas exploration, production and refining." is bold like
its siblings (the developer notes ask for every Key Legal Issues lead-in in bold), and the three
"Key Considerations for Foreign Investors" items are all sub-headings (only the first was italic).

## URLs

As in Dr. Baba's table: lowercase, no extensions. Canonical tags, structured data and
`sitemap.xml` use the production form (`https://babalawfirm.net/our-people`). On GitHub Pages the
three section pages are directory indexes (`/capabilities/`, `/industries/`, `/our-people/`), so
the address bar shows a trailing slash there. The old preview addresses sent on 10 October redirect
to the new pages (`LEGACY_REDIRECTS` in `site_config.py`).

## Before launch (from the client's implementation notes)

- **Domain**: confirm `babalawfirm.net` (`DOMAIN` in `site_config.py`); HTTPS only, with http:// and
  www/non-www redirected (301) to the canonical form.
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
- **Cookies**: run a cookie scan of the configured site and fill `COOKIE_REGISTER` (name, provider,
  purpose, category, duration). It already lists the consent record (`blf-consent-v2`, local storage);
  until the scan adds what Google Maps sets, Cookie Settings shows a one-line Google Maps note (our
  wording, for the client to approve). Add optional categories to `OPTIONAL_CATEGORIES`; the banner
  (Reject / Accept / Settings) appears automatically when there is at least one.
- **Analytics and Search Console**: install a privacy-respecting analytics tool and submit
  `/sitemap.xml` in Google Search Console.
- **Policies**: record the launch date internally as the effective date of the Privacy and Cookie
  Policies; show "Last updated" only when a policy is later amended.
- **Photographs and portraits**: replace the four stock stand-ins (`PHOTOS`) and add the portraits
  (`PORTRAITS[...]["src"]`, served as AVIF/WebP with a JPEG fallback at 640 and 1200 px).
- **careers@babalawfirm.net**: confirm it is active and monitored.
