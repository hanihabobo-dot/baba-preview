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
# Dr. Baba's notes: add the embedded map and "Get Directions" only after the exact
# office location is verified. Set VERIFIED = True and the coordinates once the
# firm sends its Google Maps link for the Al-Iskan Building.
MAP = {
    "VERIFIED": False,
    "LAT": None,
    "LNG": None,
}

# ---------------------------------------------------------------- enquiry form
# The preview cannot send email. Set an endpoint (for example a form service or
# the production CMS handler) that delivers submissions to info@babalawfirm.net.
FORM_ENDPOINT = ""

# ---------------------------------------------------------------- cookie register
# Fill in from the cookie scan of the configured live website (Dr. Baba's notes:
# "Do not publish a generic list of cookies that the website does not actually use").
# Each entry: name, provider, purpose, category ("Strictly necessary", "Analytics", ...),
# duration. Optional categories get a toggle in Cookie Settings and switch the banner on.
COOKIE_REGISTER = []
OPTIONAL_CATEGORIES = []   # e.g. [{"key": "analytics", "name": "Analytics", "description": "..."}]

# ---------------------------------------------------------------- photographs
# Stand-ins until the firm supplies its own photographs (with rights confirmed).
UNSPLASH = "https://images.unsplash.com/{id}?auto=format&fit=crop&w={w}&q=72"
PEXELS = "https://images.pexels.com/photos/{id}/pexels-photo-{id}.jpeg?auto=compress&cs=tinysrgb&w={w}"
PHOTOS = {
    "hero": {"src": ("unsplash", "photo-1561760041-f446e77d0885"), "alt": "Damascus at night", "pos": "60% 55%"},
    "window": {"src": ("pexels", "30615454"), "alt": "A wooden mashrabiya window set in a banded stone wall", "pos": "65% 45%"},
    "courtyard": {"src": ("pexels", "34682160"), "alt": "A Damascene courtyard with a fountain and banded stone walls", "pos": "50% 60%"},
    "skyline": {"src": ("unsplash", "photo-1561757780-9eb29837fbe9"), "alt": "Modern Damascus at night", "pos": "50% 60%"},
}

# Portraits: set "src" to the processed portrait path once received (e.g. assets/img/people/mohamad-baba).
PORTRAITS = {
    "mohamad-baba": {"initials": "MB", "src": None},
    "tawfeeq-baba": {"initials": "TB", "src": None},
}

# ---------------------------------------------------------------- page lists (order as supplied)
CAPABILITIES = [
    ("company-formation", "Company Formation & Corporate Structuring"),
    ("corporate-governance", "Corporate Governance & Compliance"),
    ("corporate-commercial", "Corporate & Commercial"),
    ("mergers-acquisitions", "Mergers, Acquisitions & Restructuring"),
    ("foreign-investment", "Foreign Investment & Market Entry"),
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
    ("contact", "Contact"),
]
FOOTER_NAV = PRIMARY_NAV + [("careers", "Careers")]
FOOTER_LEGAL = [("privacy-policy", "Privacy Policy"), ("cookie-policy", "Cookie Policy"), ("legal-notice", "Legal Notice")]

# Old preview addresses sent to the client on 10 October: keep them working.
LEGACY_REDIRECTS = {
    "people.html": "our-people/",
    "people/tawfeeq-baba.html": "our-people/tawfeeq-baba",
    "people/mohamad-baba.html": "our-people/mohamad-baba",
    "capabilities.html": "capabilities/",
    "industries.html": "industries/",
    "capabilities/foreign-investment-market-entry.html": "capabilities/foreign-investment",
    "capabilities/regulatory-government-public-procurement.html": "capabilities/government-public-procurement",
}
