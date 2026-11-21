"""Baba Law Firm website: site-wide settings.

Everything a reviewer may need to change before launch lives here: the domain,
the contact details (one source, so they are identical everywhere), the map
pin, the enquiry-form endpoint and the cookie register.
"""

# ---------------------------------------------------------------- build modes
# Preview build (GitHub Pages): noindex on every page, preview notes visible.
# Production build: `python3 src/build.py --production`.
SITE_NAME = "Baba Law Firm"
DOMAIN = "https://babalawfirm.net"          # canonical domain: confirm before launch
PREVIEW_BASE_PATH = "/baba-preview/"         # GitHub Pages project path (404 page only)
LANG = "en"
FOUNDING_YEAR = "1967"

# ---------------------------------------------------------------- contact details
EMAIL = "info@babalawfirm.net"
EMAIL_SUBJECT = "Legal Enquiry - Baba Law Firm"
EMAIL_HREF = "mailto:info@babalawfirm.net?subject=Legal%20Enquiry%20-%20Baba%20Law%20Firm"
CAREERS_EMAIL = "careers@babalawfirm.net"
WHATSAPP_DISPLAY = "+963 96 555 0000"
WHATSAPP_HREF = "https://wa.me/963965550000"          # no prefilled message
PHONES = [("+963 11 666 4221", "+963116664221"), ("+963 11 666 4226", "+963116664226")]
FAX = "+963 11 666 3221"
ADDRESS_LINE = "Mazzeh Highway, Al-Iskan Building, 8th Floor, next to the Ministry of Justice, Damascus, Syria"
STREET = "Mazzeh Highway, Al-Iskan Building, 8th Floor"
PO_BOX_LINE = "P.O. Box 7777, Damascus"
PO_BOX = "7777"

# ---------------------------------------------------------------- map
# Confirmed by the firm on 19 October (the Google Maps link in the Contact and Legal Pages
# document: Baba Law Firm, Eskan Towers). That link is a directions link that also carries
# the sender's own starting point, so only the office coordinates are used here; do not
# copy the link itself into the repository.
MAP = {
    "VERIFIED": True,
    "LAT": 33.497052,
    "LNG": 36.247348,
}

# ---------------------------------------------------------------- enquiry form
# The preview cannot send email. Set an endpoint (for example a form service or
# the production CMS handler) that delivers submissions to info@babalawfirm.net.
FORM_ENDPOINT = ""

# ---------------------------------------------------------------- cookie register
# Fill in from the cookie scan of the configured live website (Dr. Baba's notes:
# "Do not publish a generic list of cookies that the website does not actually use").
# Each entry: name, provider, purpose, category ("Strictly necessary", "Analytics", "Maps", ...),
# duration. Optional categories get a toggle in Cookie Settings and switch the banner on; a row in
# the category "Maps" replaces the Google Maps note under the register (Ctx in templates.py).
# The consent record (assets/js/site.js) is listed now. Scan of 31 October 2026: the Google Maps embed
# (MAP above) was requested from the command line with an empty cookie jar, following every redirect, and
# Google set no cookie in any response, so no Maps row is listed. That scan cannot see cookies that
# Google's scripts set in the browser: a browser-based scan of the live domain (map loaded after
# consent, as an EU/UK and a Syria-region visitor) must confirm this before launch. Add a row per
# cookie it finds, and only those.
COOKIE_REGISTER = [
    {"name": "blf-consent-v2", "provider": "Baba Law Firm",
     "purpose": "Records your choices in Cookie Settings (kept in your browser's local storage)",
     "category": "Strictly necessary", "duration": "Until you clear your browser's storage"},
]
OPTIONAL_CATEGORIES = []   # e.g. [{"key": "analytics", "name": "Analytics", "description": "..."}]

# ---------------------------------------------------------------- photographs
# Stock stand-ins (free-licence photographs from Unsplash and Pexels), now self-hosted in PHOTO_DIR so the
# pages load nothing from third parties. Replace them with the firm's own photographs (rights confirmed):
# export each as AVIF, WebP and JPEG at several widths under the same names and adjust "alt" and "pos".
PHOTO_DIR = "assets/img/photos"   # {key}-{width}.avif / .webp / .jpg for each key below; the build uses the widths on disk
PHOTOS = {
    "hero": {"alt": "Damascus at night", "pos": "60% 55%"},
    # Received from the firm on 21 November 2026 at 800-1280 px (compressed copies): used only in the small
    # arched frames and, for the panorama, a band no wider than the picture itself. Replace with the originals when they arrive.
    # The door is the photograph as received (854 x 1280, not cropped). "arch" is the circle fitted to the outer
    # edge of its stone arch, in pixels of the 854-wide picture: the arch's axis is at x = 398.5 (28.5 px left of
    # the picture's middle) and a least-squares fit through 13 points on the edge gives the centre height 536.3.
    # templates.arch_fit() places the picture so that this centre is the centre of the frame's round top.
    "door": {"alt": "A carved wooden door under an arch of banded stone in old Damascus", "pos": "50% 40%",
             "arch": {"w": 854, "h": 1280, "cx": 398.5, "cy": 536.3},
             # Set by hand by Hani with the alignment tool on 21 November 2026; wins over the computed fit.
             "place": {"width": "107.15%", "left": "0.92%", "top": "-10.89%"}},
    "street": {"alt": "A lane in old Damascus spanned by a row of stone arches", "pos": "45% 50%"},
    "panorama": {"alt": "Damascus at dusk, seen from Mount Qasioun", "pos": "50% 70%"},
}

# Home hero film (received 21 November 2026 as a 480p copy; the shot of a mural carrying a photographer's
# watermark is cut out; the full frame is kept, except the last shot, which is cropped to lose its black side bars): silent, looped, wide screens only, started by site.js
# over the hero photograph, which stays as the picture for phones, reduced motion and data saving.
HERO_VIDEO = "assets/video/damascus-full-854.mp4"   # rename with each re-encode, so no browser shows a cached older cut

# Portraits (received 21 November 2026): 4:5 crops at 640 and 800 px wide, AVIF/WebP/JPEG
# (the photographs were sent at 800 px; replace with larger originals when available).
PORTRAITS = {
    "mohamad-baba": {"initials": "MB", "src": "assets/img/people/mohamad-baba"},
    "tawfeeq-baba": {"initials": "TB", "src": "assets/img/people/tawfeeq-baba"},
}

# ---------------------------------------------------------------- page lists (order as supplied)
CAPABILITIES = [
    ("company-formation", "Company Formation & Corporate Structuring"),
    ("corporate-governance", "Corporate Governance & Compliance"),
    ("corporate-commercial", "Corporate & Commercial"),
    ("mergers-acquisitions", "Mergers, Acquisitions & Restructuring"),
    ("foreign-investment", "Foreign Investment & Market Entry"),
    ("market-feasibility-studies", "Market & Feasibility Studies"),
    ("banking-finance", "Banking & Finance"),
    ("regulatory-compliance-sanctions", "Regulatory Compliance & Sanctions"),
    ("arbitration-dispute-resolution", "Arbitration & Dispute Resolution"),
    ("projects-construction-infrastructure", "Projects, Construction & Infrastructure"),
    ("real-estate-development", "Real Estate & Development"),
    ("employment", "Employment"),
    ("intellectual-property-data-protection", "Intellectual Property & Data Protection"),
    ("technology-fintech", "Technology & FinTech"),
    ("tax-customs", "Tax & Customs"),
    ("government-public-procurement", "Regulatory, Government & Public Procurement"),
    ("administrative-law-council-of-state", "Administrative Law & Council of State Proceedings"),
]
# The Capabilities index groups the pages under four headings (Dr. Baba's notes of 19 October),
# with links to the groups at the top of the page.
CAPABILITY_GROUPS = [
    ("Establishing & Managing a Business",
     ["company-formation", "corporate-governance", "corporate-commercial", "employment"]),
    ("Investment, Finance & Transactions",
     ["market-feasibility-studies", "mergers-acquisitions", "foreign-investment", "banking-finance", "tax-customs"]),
    ("Regulation, Technology & Public Authorities",
     ["regulatory-compliance-sanctions", "intellectual-property-data-protection", "technology-fintech",
      "government-public-procurement"]),
    ("Projects, Property & Dispute Resolution",
     ["projects-construction-infrastructure", "real-estate-development", "arbitration-dispute-resolution",
      "administrative-law-council-of-state"]),
]
INDUSTRIES = [
    ("banking-financial-services", "Banking & Financial Services"),
    ("construction-infrastructure", "Construction & Infrastructure"),
    ("real-estate-urban-development", "Real Estate & Urban Development"),
    ("energy-power", "Energy & Power"),
    ("telecommunications", "Telecommunications"),
    ("technology-fintech", "Technology & FinTech"),
    ("aviation", "Aviation"),
    ("manufacturing-trade", "Manufacturing & Trade"),
    ("hospitality-tourism", "Hospitality & Tourism"),
    ("healthcare-life-sciences", "Healthcare & Life Sciences"),
    ("diplomatic-missions-ngos", "Diplomatic Missions, International Organisations & NGOs"),
]
PEOPLE = [
    ("mohamad-baba", "Dr. Mohamad Baba"),
    ("tawfeeq-baba", "Tawfeeq Baba"),
]

PRIMARY_NAV = [
    ("our-firm", "Our Firm"),
    ("our-people/", "Our People"),
    ("capabilities/", "Capabilities"),
    ("industries/", "Industries"),
    # A second way in to the sanctions page (client notes of 29 October); it stays in the Capabilities list.
    ("capabilities/regulatory-compliance-sanctions", "Sanctions & Compliance"),
    ("contact", "Contact"),
]
FOOTER_NAV = PRIMARY_NAV + [("careers", "Careers")]
FOOTER_LEGAL = [("privacy-policy", "Privacy Policy"), ("cookie-policy", "Cookie Policy"), ("legal-notice", "Legal Notice")]

# Old preview addresses sent to the client on 10 October: keep them working.
LEGACY_REDIRECTS = {
    "people.html": "our-people/",
    "people/tawfeeq-baba.html": "our-people/tawfeeq-baba",
    "people/mohamad-baba.html": "our-people/mohamad-baba",
    "capabilities/foreign-investment-market-entry.html": "capabilities/foreign-investment",
    "capabilities/regulatory-government-public-procurement.html": "capabilities/government-public-procurement",
}
# No stub file for these: GitHub Pages would serve capabilities.html for /capabilities, the address of
# the Capabilities index itself. Without it, /capabilities answers 301 to /capabilities/, and the
# preview 404 page sends the old .html addresses on.
LEGACY_404_REDIRECTS = {
    "capabilities.html": "capabilities/",
    "industries.html": "industries/",
}
