# team4788.com

The Team 4788 website. A Jekyll site in `docs/`, built and hosted by GitHub Pages from `main:/docs` (repo Hazzer890/team4788.com). Pushing to `main` publishes it, there is no build step to run and no Actions workflow.

Third-party at runtime: the YouTube embeds on the robot pages and the Google Maps embed on `/contact/`. Everything else (fonts, images, CSS) is served from this repo. There is no JavaScript.

## Where things are

| Path | What it is |
|------|------------|
| `docs/_config.yml` | Site title, URL, email address, plugins |
| `docs/_data/nav.yml` | Header menu |
| `docs/_data/sponsors.yml` | Sponsor logos (home page and `/sponsors/`) |
| `docs/_data/socials.yml` | Social links (footer, home page, `/contact/`) |
| `docs/_robots/` | One file per robot |
| `docs/_posts/` | Blog posts |
| `docs/_layouts/`, `docs/_includes/` | Templates: `default` (header and footer), `page`, `post`, `robot` |
| `docs/assets/css/site.css` | The one stylesheet, colours and fonts are variables at the top |
| `docs/assets/img/`, `docs/assets/fonts/` | Images and fonts |

## Add a robot

Copy `docs/_robots/2025frcrobot.md` to `docs/_robots/2027frcrobot.md` and edit the front matter. The file name is the URL (`/2027frcrobot/`). The robot shows up in the header menu, on `/robots/` and in the robot strip on the home page (the strip needs a `thumb`).

Images go in `docs/assets/img/robots/`. Every field except `title`, `year` and `game` is optional, a page with nothing else filled in shows "Render coming soon". `2026frcrobot.md` is a stub like that at the moment.

## Add a blog post

Add `docs/_posts/YYYY-MM-DD-some-slug.md`:

```markdown
---
title: "Post title"
date: 2026-03-01
image: /assets/img/blog/some-slug.jpg
image_alt: "What the cover image shows"
---

Post text in Markdown.
```

It is published at `/blog/some-slug/` and listed on `/blog/`. Images for the post go in `docs/assets/img/blog/`.

## Add or fill in a page

Add `docs/name.md` with a `title` in the front matter and it is published at `/name/`. Add it to `docs/_data/nav.yml` to put it in the menu.

A page with a title and no content shows the "under construction" message. Diversity, Downloads, Handbook, Media, Resources, Robot Demos and Support are like that now, writing content into the file replaces the message.

To retire a URL, add `redirect_from: /old-url/` to the page that replaces it (see `contact.md`).

## Preview locally

Needs Ruby and Bundler (`sudo pacman -S ruby`).

    cd docs
    bundle install                 # first time only, installs into docs/vendor
    bundle exec jekyll serve       # http://localhost:4000

The `github-pages` gem pins the same Jekyll and plugins that GitHub Pages runs.

After a build, `python3 check.py` from the repo root checks `docs/_site` for broken internal links, images without alt text, and that every URL from the old Framer site still exists or redirects.

## DNS (Namecheap)

In Namecheap > Domain List > team4788.com > Advanced DNS, the records are:

| Type  | Host | Value                   |
|-------|------|-------------------------|
| A     | @    | 185.199.108.153         |
| A     | @    | 185.199.109.153         |
| A     | @    | 185.199.110.153         |
| A     | @    | 185.199.111.153         |
| CNAME | www  | hazzer890.github.io.    |

Leave any MX/TXT records alone. In the repo, Settings > Pages > "Enforce HTTPS" should be ticked once GitHub reports the certificate is issued (up to an hour after DNS propagates). Cancel Framer only after https://team4788.com loads from GitHub Pages.

## History

Until November 2026 `docs/` was a static mirror of the old Framer site, kept working by `mirror.py` and `patch.py`. Those, the Framer export and the Team Structure page text are in the git history before the `rebuild` branch was merged.
