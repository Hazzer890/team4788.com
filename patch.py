#!/usr/bin/env python3
"""Post-process docs/ (the static Framer mirror). Idempotent; run after mirror.py or on its own."""
import re, os, glob, html, json

OUT, SITE, YEAR = "docs", "https://team4788.com", "2026"
TITLES = {"/robots": "Robots", "/structure": "Team Structure"}  # pages whose first <h1> makes a poor title
TEXT = (".html", ".mjs", ".json")

ALTS = {  # Framer shipped these images with empty alt text
    "W9kjXX2bu4FtxS9T31bg6rAWc.svg": "Team 4788 logo", "K1NqENN9TtGXLaJ4LCUNcML3hAQ.png": "GitHub",
    "BnSOuVrnJu6CLsMKHoFtIwo56E.png": "Facebook", "bDO2tCEZLUMZ13Rp8FFIDnzZqw.png": "Instagram",
    "klrzdbi8fD9PwSubPyNqdJJeXY.png": "YouTube", "ZGcawMVpDAc5AuRWouP6Fc4ipLE.png": "Curtin University",
    "8S9ifvl8suPkERIV0ysp09RryZQ.png": "DNA Racing", "mOTrGj7jbAv5B4pLGzOYjV5gc.png": "WARES",
    "jKyr7DDxDhvk7JEuQL9MDUJ7LS4.png": "Paradigm Machines", "ftgHJakPPpCIV5pneRHY76eew.png": "DSM Engineers",
    "8w1FlEqOqcQXnQrGQQQ8L6juqE.png": "Packaging Perth", "OzPDvTFyi9bYE0iVrfHAZm2A4.png": "Artifactory, Perth's maker space",
    "eSlvDiO5AlvfuNtCu7U9ODJ9kLw.jpg": "Team 4788 in pink shirts with their robot and a FIRST Robotics Competition banner",
    "H7TlMx5pQDfdZDKhgaSOvyBBFOQ.jpg": "Team 4788's robot driving across the field during a match",
    "lRnGMWMf1Zz7Q1S71FvPCN7toI.jpg": "Team members and guests kneeling beside the robot on stage",
    "jUtGkI5SbKNSalbB4zizyQ3cBEA.jpg": "Team 4788's robot beside the reef on a Reefscape field",
    "keqsCVUzcZ9MV3O2ebgF6ohixCI.png": "CAD model of Gup X, the 2025 robot",
    "V91ych1Z3VmzcYyZKLiVwx9V2GI.png": "Two students programming the robot at a laptop",
    "xaLmtgRqwOUeE6jMb8vIFBmgE.png": "Two open gearboxes on a workbench",
    "zjeHPdlewcis4h13jJWTJmXdxyQ.png": "CAD render of Notedog Millionare, the 2024 robot",
    "wUKZaeOhvgKSx6n55xrgJuoWI.png": "The 2024 robot in the workshop",
    "fxJFoNtgncIB31Ph8aLBjW6JBg.png": "Two team members working on the robot",
    "e3woKCxN9xwEu9iVDu9qpsB0cI.png": "Group photo of teams and their robots at an event",
    "46HdFSIQLN09D7aWGGWIIwgc.png": "CAD render of Whiplash, the 2023 robot",
    "7TDVDIOZtRKlp5Ybum0AcqdAr4.png": "The 2023 robot with its arm raised in a classroom",
    "jnUImQrXshEHUVFI8un8sfwU.png": "Three team members working at a laptop",
    "JgX5knY1KOKVzsnwDStF5rdD0Rk.png": "CAD render of Mercury, the 2022 robot",
    "ZnmuFHjxVlbF0gFkA1Tjp2KcQ.png": "Close-up of the robot's shooter and green vision light ring",
    "gUEmQgRZM4z157pj8YctJjAqms.png": "Two team members at a laptop giving a thumbs up",
    "bbf4cJL28lQUubLH0THjZuijybc.png": "CAD render of Slinger, the 2021 robot",
    "SqVHWzrEvYWKJBsJT3zx3LHicT4.png": "Mercury, the 2022 robot", "Chi0dWFXq3JpA4FOT3Heiec6O8.png": "Whiplash, the 2023 robot",
    "QIC766O7fYkiz9fEorkHr8kOsQ.png": "Notedog Millionare, the 2024 robot", "l9qR1jTdiHkPUOJ0cfF1VJeZU.png": "Gup X, the 2025 robot",
    "rDWNwSgTmKA4IK1JtSts8yumeAU.png": "Reefscape game logo", "zdAdhaDfD03VIaZgID0DBgACI5c.svg": "Crescendo game logo",
    "RMsS37oPPSQyEspVSfrAu69Velo.svg": "Charged Up game logo", "DZnjVWjQYGQOmX99yHfoOzNaPA.svg": "Rapid React game logo",
    "pdnif0VpQDecwqAilj0YBrfc8fw.png": "CAD model of a plate with curved grooves", "mBBbzGhuRgiZed1SGlinI5w4WjI.png": "CAD model of box tube with a hole pattern",
    "jxAju0kRlr70tx53Pbubaax94.png": "CAD model of four pink spacers", "JO6moAwGFxt4m3WPUN7wLbYJaJU.png": "Render of a CAN breakout PCB",
    "UEaHrix91ncg1mCc6NrQCjHhw.png": "Render of a CAN-over-RJ45 PCB", "iVxIEVNmCRU4YZioCdEbMC5Z5o.png": "Render of a small power PCB",
    "kQJnKVd11ll6S2akhZar1Ao6T6E.png": "Render of a CAN-over-RJ45 PCB", "3j0q9UByZzAu4ZP5TFarOdDxhrw.png": "Render of a blue PCB",
    "hcbk5J6g0vvnUCnQNFzeZUtEpI.png": "CAD model of a shaft end insert", "sbcGCL2jJEXbIEgRP12fATbHiWM.png": "CAD model of a threaded shaft end insert",
    "3wjz2ZxRoMwvs9IuEVOAFuE4UTk.jpg": "Team members in pink shirts at a competition",
    "u8vd9w1hGLnt3eCzsvSCpLDS8.jpg": "Team members working on robot 9982 in the pits",
}

def img_alt(m):
    tag = m.group(0)
    src = re.search(r' src="[^"]*/([^"/?]+)"', tag)
    alt = src and ALTS.get(src.group(1))
    if not alt: return tag
    alt = html.escape(alt)
    return tag.replace('alt=""', f'alt="{alt}"') if 'alt="' in tag else tag.replace("<img ", f'<img alt="{alt}" ', 1)

def edit(path, fn):
    s = open(path, encoding="utf-8").read()
    n = fn(s)
    if n != s: open(path, "w", encoding="utf-8").write(n)

def everywhere(s):  # page HTML and the JS/CMS chunks that re-render it
    s = re.sub(r"(Control, )20\d\d", r"\g<1>" + YEAR, s)                                # footer copyright
    s = re.sub(r"(aliexpress\.com/item/\d+\.html)\?[^\"'`\\\s<)]*", r"\1", s)            # tracking junk
    s = re.sub(r"alt:``((?:(?!alt:`).){0,400}?src:`[^`]*/([^`/]+)`)", lambda m: f"alt:`{ALTS.get(m.group(2), '')}`{m.group(1)}", s)
    # mobile hero: % height in an auto-height parent collapses in Safari, so the subtitle overlaps the headline
    s = re.sub(r"(\.framer-r5qw9o ?\{ ?(?:order:0;)?height: ?)22%", r"\1auto", s)
    return s.replace("http://www.firstinspires.org", "https://www.firstinspires.org")

routes, titles = [], {}
def page(path):
    route = "/" + os.path.dirname(os.path.relpath(path, OUT))  # docs/about/index.html -> /about
    is404 = path.endswith("404.html")
    if is404: route = "/"
    else: routes.append(route)
    def fn(s):
        # GitHub Pages serves /about as /about/, which breaks Framer's relative links (./contact)
        if "<base " not in s: s = s.replace("<head>", f'<head>\n    <base href="{route}">', 1)
        # crawlers and link previews need absolute URLs
        s = re.sub(r'(<link rel="canonical" href="|<meta property="og:url" content="|<meta (?:property="og|name="twitter):image" content=")/', r"\1" + SITE + "/", s)
        if route != "/": s = re.sub(r'((?:rel="canonical" href|og:url" content)="' + SITE + route + ')"', r'\1/"', s)
        s = re.sub(r"<img [^>]*>", img_alt, s)
        if not is404 and "<title>Team 4788</title>" in s:
            h1 = re.search(r"<h1[^>]*>([\s\S]*?)</h1>", s)
            name = TITLES.get(route) or html.unescape(re.sub(r"<[^>]+>", "", h1.group(1))).strip()
            if m := re.fullmatch(r"/(20\d\d)frcrobot", route): name += f" ({m.group(1)} robot)"
            t = html.escape(f"{name} | Team 4788")
            s = s.replace("<title>Team 4788</title>", f"<title>{t}</title>")
            s = re.sub(r'(<meta (?:property="og|name="twitter):title" content=")Team 4788"', r"\g<1>" + t + '"', s)
            titles[route] = f"{name} | Team 4788"
        return s
    edit(path, fn)

for p in glob.glob(f"{OUT}/**/*", recursive=True):
    if p.endswith(TEXT): edit(p, everywhere)
    if p.endswith(".html"): page(p)

# Framer's runtime resets document.title to its one default; look the page up by path instead
if titles:
    js = "title:(" + json.dumps(titles).replace("`", "") + ")[location.pathname.replace(/\\/$/,``)]||`Team 4788`}}"
    for p in glob.glob(f"{OUT}/**/*.mjs", recursive=True): edit(p, lambda s: s.replace("title:`Team 4788`}}", js))

open(f"{OUT}/robots.txt", "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
open(f"{OUT}/sitemap.xml", "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + "".join(f"  <url><loc>{SITE}{r.rstrip('/')}/</loc></url>\n" for r in sorted(routes)) + "</urlset>\n")

# Framer resized images on the fly; the mirror only has camera originals. Shrink them in place.
from PIL import Image, ImageOps
icon = re.search(r'<link href="/([^"]+)" rel="icon"', open(f"{OUT}/index.html", encoding="utf-8").read()).group(1)
Image.open(f"{OUT}/{icon}").save(f"{OUT}/favicon.ico", sizes=[(32, 32), (48, 48)])
MAXW = 2000
for p in glob.glob(f"{OUT}/framerusercontent.com/**/*", recursive=True):
    if not p.lower().endswith((".jpg", ".jpeg", ".png")) or os.path.getsize(p) < 300_000: continue
    im = Image.open(p)
    if im.width <= MAXW: continue
    fmt, tmp = im.format, p + ".tmp"
    im = ImageOps.exif_transpose(im)
    im = im.convert("RGBA" if fmt == "PNG" else "RGB").resize((MAXW, round(im.height * MAXW / im.width)), Image.LANCZOS)
    im.save(tmp, fmt, optimize=True, **({"quality": 82, "progressive": True} if fmt == "JPEG" else {}))
    if os.path.getsize(tmp) < os.path.getsize(p): os.replace(tmp, p)
    else: os.remove(tmp)
