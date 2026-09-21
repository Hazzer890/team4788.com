# team4788.com static copy

`docs/` is a self-contained static mirror of https://team4788.com (a Framer site),
made by `mirror.py` and then tidied by `patch.py`. Hosted on GitHub Pages from `main:/docs` (repo Hazzer890/team4788.com). Any static
host works: upload the contents of `docs/` at the domain root.

- Pages are `<path>/index.html`, so `/about` works everywhere.
- `404.html` is the custom not-found page; most hosts pick it up automatically.
- All Framer CDN assets live under `docs/framerusercontent.com/` etc. Nothing loads from Framer at runtime.
- Still third-party at runtime: YouTube and Google Maps embeds, and the 3D robot viewers on the robot pages (Spline runtime from unpkg.com, scenes from my.spline.design, about 11 MB each). If the Spline account lapses the 3D viewers go blank, the rest of the page is fine.
- Framer analytics and the on-page editor bar are stripped.

## Going live (DNS at Namecheap)

In Namecheap > Domain List > team4788.com > Advanced DNS, delete the existing
A records for `@` and the CNAME for `www`, then add:

| Type  | Host | Value                   |
|-------|------|-------------------------|
| A     | @    | 185.199.108.153         |
| A     | @    | 185.199.109.153         |
| A     | @    | 185.199.110.153         |
| A     | @    | 185.199.111.153         |
| CNAME | www  | hazzer890.github.io.    |

Leave any MX/TXT records alone. Then in the repo: Settings > Pages > tick
"Enforce HTTPS" once GitHub reports the certificate is issued (up to an hour
after DNS propagates). Cancel Framer only after https://team4788.com loads.

## Known gaps

- The contact forms (home page and `/contact`) have no backend. Submitting opens
  the visitor's email app with a prefilled message to FirstRoboticsTeam@curtin.edu.au
  (patched in `mirror.py`). Swap in Formspree or similar if you want real submissions.
- The site is a frozen snapshot: edits mean editing HTML by hand or rebuilding elsewhere.

## patch.py

Fixes that Framer can't make for us any more. It only reads `docs/`, so it keeps working after Framer is cancelled, and it is safe to run twice. Needs Pillow.

- `<base>` tag on every page, because GitHub Pages serves `/about` as `/about/` and Framer's relative menu links 404 from there.
- Per-page titles, absolute canonical/og URLs, `robots.txt`, `sitemap.xml`, `favicon.ico`.
- Alt text for every image (the `ALTS` table), footer year (`YEAR`), AliExpress tracking junk trimmed.
- Images wider than 2000 px are resized in place, Framer used to do this on the fly.

## Regenerate

    python3 mirror.py   # rm -rf docs first for a clean run (only while the Framer site is still up)
    python3 patch.py
