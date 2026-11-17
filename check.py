#!/usr/bin/env python3
"""Check the built site: run `bundle exec jekyll build` in docs/ first, then `python3 check.py`.
Fails if an internal link or asset is missing, an image has no alt text, or a URL from the old Framer site is gone."""
import os, re, sys, glob
SITE = "docs/_site"
OLD = """/ /2021frcrobot/ /2022frcrobot/ /2023frcrobot/ /2024frcrobot/ /2025frcrobot/ /about/ /blog/
/blog/2024-build-blog-design-guidelines/ /blog/2025-cad-resources/ /blog/offseason-25-carbon-fibre-shafts/
/blog/offseason-25-electrical-can-connectors/ /blog/offseason-25-robust-vision/ /contact/ /diversity/ /downloads/ /faq/
/first/ /handbook/ /location/ /media/ /recruitment/ /resources/ /roboacademy/ /robotdemos/ /robots/ /structure/ /support/
/workshops/""".split()

def exists(url):
    p = SITE + url.split("#")[0].split("?")[0]
    return os.path.isfile(p) or os.path.isfile(os.path.join(p, "index.html"))

errors = []
pages = glob.glob(f"{SITE}/**/*.html", recursive=True)
for page in pages:
    html = open(page, encoding="utf-8").read()
    for url in re.findall(r'(?:href|src)="(/[^"/][^"]*|/)"', html):
        if not exists(url): errors.append(f"{page}: broken link {url}")
    for img in re.findall(r"<img[^>]*>", html):
        if not re.search(r'alt="[^"]+"', img): errors.append(f"{page}: image without alt text {img}")
    for bad in ("framerusercontent", "spline", "unpkg"):
        if bad in html: errors.append(f"{page}: still mentions {bad}")
for url in OLD:
    if not exists(url): errors.append(f"old URL missing: {url}")

print(f"{len(pages)} pages checked, {len(errors)} problems")
print("\n".join(errors))
sys.exit(1 if errors else 0)
