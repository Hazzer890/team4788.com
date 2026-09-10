# team4788.com static copy

`docs/` is a self-contained static mirror of https://team4788.com (a Framer site),
made by `mirror.py`. Hosted on GitHub Pages from `main:/docs` (repo Hazzer890/team4788.com). Any static
host works: upload the contents of `docs/` at the domain root.

- Pages are `<path>/index.html`, so `/about` works everywhere.
- `404.html` is the custom not-found page; most hosts pick it up automatically.
- All Framer CDN assets live under `docs/framerusercontent.com/` etc. Nothing loads from Framer at runtime.
- Framer analytics and the on-page editor bar are stripped.

## Known gaps

- The contact forms (home page and `/contact`) have no backend. Submitting opens
  the visitor's email app with a prefilled message to FirstRoboticsTeam@curtin.edu.au
  (patched in `mirror.py`). Swap in Formspree or similar if you want real submissions.
- The site is a frozen snapshot: edits mean editing HTML by hand or rebuilding elsewhere.

## Regenerate

    python3 mirror.py   # rm -rf docs first for a clean run
