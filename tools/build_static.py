#!/usr/bin/env python3
"""Build self-contained copies of aslm-2026-preview.html.

  docs/       -> GitHub Pages site (images bundled, served from the repo)
  _artifact/  -> copy published to the claude.ai preview link

Every https://sawa-tech.com/wp-content/uploads/... image referenced by the
preview is downloaded once into tools/.cache, resized/re-encoded where it is
oversized, and written to <out>/assets/<basename>. The favicon stays remote.

Usage:  python3 tools/build_static.py
"""
import io, pathlib, re, urllib.request
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "aslm-2026-preview.html"
CACHE = ROOT / "tools" / ".cache"
URL_RE = re.compile(r'https://sawa-tech\.com/wp-content/uploads/\d{4}/\d{2}/([^"\'\s)]+)')
KEEP_REMOTE = {"cropped-sawatech-favicon-32x32.webp"}
# max rendered width x2 for retina; anything wider is downscaled
MAX_W = {
    "1-Healthcare-Translation-Services-That-Put-Patient-Safety-First.webp": 1000,
    "Process-Section-Visuals-03-1.webp": 900,
}

def fetch(url, name):
    CACHE.mkdir(parents=True, exist_ok=True)
    p = CACHE / name
    if not p.exists():
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        p.write_bytes(urllib.request.urlopen(req, timeout=30).read())
    return p.read_bytes()

def optimise(name, data):
    if name not in MAX_W:
        return data
    im = Image.open(io.BytesIO(data))
    w = MAX_W[name]
    if im.width > w:
        im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    out = io.BytesIO()
    im.save(out, "WEBP", quality=80, method=6)
    return out.getvalue() if out.tell() < len(data) else data

def build(out_dir, html):
    assets = out_dir / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    def repl(m):
        name = m.group(1)
        if name in KEEP_REMOTE:
            return m.group(0)
        target = assets / name
        if not target.exists():
            target.write_bytes(optimise(name, fetch(m.group(0), name)))
        return "assets/" + name
    page = URL_RE.sub(repl, html)
    # preload hint must match the local hero path
    (out_dir / "index.html").write_text(page, encoding="utf-8")
    return page

def main():
    html = SRC.read_text(encoding="utf-8")
    for d in ("docs", "_artifact"):
        for f in (ROOT / d / "assets").glob("*"):
            f.unlink()
    build(ROOT / "docs", html)
    (ROOT / "docs" / ".nojekyll").touch()
    art = html.replace(
        "<title>SawaTech at ASLM 2026 | Life Sciences Localization</title>",
        "<title>SawaTech ASLM 2026</title>")
    build(ROOT / "_artifact", art)
    for d in ("docs", "_artifact"):
        total = sum(f.stat().st_size for f in (ROOT / d / "assets").glob("*"))
        print(f"{d}: {len(list((ROOT / d / 'assets').glob('*')))} assets, {total/1024:.0f} KB")

if __name__ == "__main__":
    main()
