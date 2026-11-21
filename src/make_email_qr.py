"""Regenerate assets/img/qr/email-qr.svg, the Quick Contact QR code on the Contact page.

    pip install segno          # only for this script; the site build needs nothing
    python3 src/make_email_qr.py

The code carries C.EMAIL_HREF (the same mailto: link as the email buttons), black on white,
with the standard four-module quiet zone and no logo. Run it again if the address or subject
changes, then rebuild and scan the result with a phone before publishing.
"""
import re
import sys
from pathlib import Path

import segno

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
import site_config as C  # noqa: E402

OUT = ROOT / "assets/img/qr/email-qr.svg"

qr = segno.make(C.EMAIL_HREF, error="m", micro=False)
OUT.parent.mkdir(parents=True, exist_ok=True)
qr.save(str(OUT), scale=1, border=4, dark="#000", light="#fff", xmldecl=False, svgclass=None,
        lineclass=None, nl=False)
# Scale with CSS: a viewBox instead of fixed pixel size, and crisp module edges.
svg = OUT.read_text()
size = qr.symbol_size(scale=1, border=4)[0]
svg = re.sub(r'width="\d+" height="\d+"',
             f'viewBox="0 0 {size} {size}" shape-rendering="crispEdges"', svg, count=1)
OUT.write_text(svg + "\n")
print(f"{OUT.relative_to(ROOT)}: version {qr.version}-{qr.error}, {size}x{size} modules incl. quiet zone")
