#!/usr/bin/env python3
"""Make the launch upload: a zip of the production site, ready for the firm's hosting.

    python3 src/package_production.py            # writes baba-law-firm-site.zip next to the repository folder

It copies the repository to a temporary folder, runs the production build there (no password page,
indexable, no /baba-preview/ paths, robots.txt with the sitemap, an Apache .htaccess) and zips only the
files a web server needs: no src/, no .git, no preview redirect stubs. The repository itself stays the
preview. Unzip the result into the web root (public_html on cPanel) so that index.html sits at the top.
"""
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
import site_config as C  # noqa: E402

SKIP_TOP = {"src", ".git", ".github", ".gitignore", ".nojekyll", "login.html", "README.md", "__pycache__"}

with tempfile.TemporaryDirectory() as tmp:
    work = Path(tmp) / "site"
    shutil.copytree(ROOT, work, ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"))
    for old in C.LEGACY_REDIRECTS:                      # preview-only stubs
        (work / old).unlink(missing_ok=True)
    shutil.rmtree(work / "people", ignore_errors=True)
    subprocess.run([sys.executable, str(work / "src" / "build.py"), "--production"], check=True)
    out = ROOT.parent / "baba-law-firm-site.zip"
    count = 0
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(work.rglob("*")):
            rel = f.relative_to(work)
            if f.is_dir() or rel.parts[0] in SKIP_TOP or f.suffix in {".py", ".pyc"}:
                continue
            z.write(f, rel.as_posix())
            count += 1
    print(f"Wrote {out} ({count} files, {out.stat().st_size // 1024} KB). Unzip it into the web root (public_html).")
