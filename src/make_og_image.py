"""Regenerate assets/img/og-image.png, the picture shown when a link to the site is shared (1200 x 630).

    python3 src/make_og_image.py      # needs Node.js with Playwright; the site build needs neither

It sets the home tagline (the "~" line of src/content/home.txt, one sentence per line) and
"DAMASCUS · SINCE <FOUNDING_YEAR>" over src/og/og-background.png (the navy pattern, the logo and the ablaq
stripe of the first card), in Cormorant Garamond and Manrope from assets/fonts. Run it again when the tagline or
the founding year changes, then rebuild: the pages link the picture as og-image.png?v=<hash of the file>
(templates.og_image()), so a new picture gets a new address and messaging apps do not keep the old one.
"""
import base64
import html
import re
import subprocess
import sys
import tempfile
from pathlib import Path

SRC = Path(__file__).resolve().parent
ROOT = SRC.parent
sys.path.insert(0, str(SRC))
import site_config as C                                    # noqa: E402
from markup import parse                                  # noqa: E402

OUT = ROOT / "assets" / "img" / "og-image.png"
FONTS = ROOT / "assets" / "fonts"

# Measured on the first card: text starts at x 83; the tagline is Cormorant Garamond 500 with the display
# letter-spacing; 90 px keeps "International Perspective." about as wide as the first card's longest line.
TAGLINE = {"size": 90, "x": 83, "baselines": (367, 456)}
SMALL = {"size": 20.5, "x": 83.5, "baseline": 529}

RENDER_JS = r"""
const { chromium } = require('playwright');
(async () => {
  const [page_file, out] = process.argv.slice(1);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: 1 });
  await p.goto('file://' + page_file);
  await p.evaluate(async () => {
    await document.fonts.load('500 90px OgSerif'); await document.fonts.load('700 20px OgSans'); await document.fonts.ready;
  });
  await p.locator('svg').screenshot({ path: out });
  await b.close();
})();
"""


def data_uri(path, mime):
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()


def page(lines, small):
    t, s = TAGLINE, SMALL
    spans = "".join(f'<tspan x="{t["x"]}" y="{y}">{html.escape(line)}</tspan>' for line, y in zip(lines, t["baselines"]))
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face {{ font-family: OgSerif; font-weight: 300 700;
  src: url({data_uri(FONTS / "cormorant-garamond-latin-wght-normal.woff2", "font/woff2")}) format("woff2"); }}
@font-face {{ font-family: OgSans; font-weight: 200 800;
  src: url({data_uri(FONTS / "manrope-latin-wght-normal.woff2", "font/woff2")}) format("woff2"); }}
html, body {{ margin: 0; background: #101C2C; }} svg {{ display: block; }}
</style></head><body>
<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
<image href="{data_uri(SRC / "og" / "og-background.png", "image/png")}" x="0" y="0" width="1200" height="630"/>
<text font-family="OgSerif" font-weight="500" font-size="{t["size"]}" letter-spacing="{-0.015 * t["size"]:.3f}" fill="#F5F2EC">{spans}</text>
<text font-family="OgSans" font-weight="700" font-size="{s["size"]}" letter-spacing="{0.18 * s["size"]:.3f}" fill="#B8956A" x="{s["x"]}" y="{s["baseline"]}">{html.escape(small)}</text>
</svg></body></html>"""


def main():
    tagline = parse(SRC / "content" / "home.txt").tagline or ""
    lines = re.split(r"(?<=\.)\s+(?=[A-Z])", tagline.strip())
    if len(lines) != 2:
        raise SystemExit(f"make_og_image: expected a tagline of two sentences in home.txt, found {tagline!r}")
    small = f"DAMASCUS · SINCE {C.FOUNDING_YEAR}"
    with tempfile.TemporaryDirectory() as tmp:
        page_file = Path(tmp) / "og.html"
        page_file.write_text(page(lines, small), encoding="utf-8")
        shot = Path(tmp) / "og.png"
        subprocess.run(["node", "-e", RENDER_JS, str(page_file), str(shot)], check=True)
        try:
            from PIL import Image
            Image.open(shot).convert("RGB").save(OUT, optimize=True)
        except ImportError:
            OUT.write_bytes(shot.read_bytes())
    print(f"Wrote {OUT.relative_to(ROOT)}: {' / '.join(lines)} · {small}")


if __name__ == "__main__":
    main()
