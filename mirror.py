#!/usr/bin/env python3
"""Mirror team4788.com (a Framer site) into ./site as self-contained static files."""
import re, os, html, urllib.request, urllib.parse, sys, glob
from collections import deque

SITE = "https://team4788.com"
OUT = "docs"  # GitHub Pages serves main:/docs
CDN = ("framerusercontent.com", "app.framerstatic.com", "fonts.gstatic.com", "fonts.googleapis.com")
TEXT = (".html", ".mjs", ".js", ".css", ".svg", ".json")
STOP = r'[^\s"\'()<>,\\`{}]'
URL_RE = re.compile(r'https://(?:' + "|".join(re.escape(h) for h in CDN) + r')/' + STOP + "+")
REL_MJS_RE = re.compile(r'[\w-]+\.[\w-]+\.mjs')                       # sibling bundle chunks
NEW_URL_RE = re.compile(r'new URL\(`\./([^`]+)`,`(https://framerusercontent\.com/[^`]+)`\)')  # CMS chunks

MAILTO = """async function wu(e,t,n){let f=[...t.entries()].filter(([k,v])=>typeof v=="string"&&v&&!k.startsWith("__framer_"));location.href="mailto:FirstRoboticsTeam@curtin.edu.au?subject="+encodeURIComponent("Website enquiry from "+(t.get("Name")||"team4788.com"))+"&body="+encodeURIComponent(f.map(([k,v])=>k+": "+v).join("\\n\\n"));return new Response("{}",{status:200})}"""

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        return urllib.request.urlopen(req, timeout=60).read()
    except urllib.error.HTTPError as e:
        if url.startswith(SITE) and e.code == 404: return e.read()  # custom 404 page
        raise

def local(url):
    u = urllib.parse.urlsplit(url)
    if u.netloc == "team4788.com":
        p = u.path.strip("/")
        return os.path.join(OUT, "404.html" if p == "404" else os.path.join(p, "index.html"))
    return os.path.join(OUT, u.netloc, u.path.lstrip("/"))  # query dropped: ?scale-down-to= etc.

pages = re.findall(r"<loc>([^<]+)", get(SITE + "/sitemap.xml").decode())
queue, seen = deque(pages), set()
while queue:
    url = queue.popleft()
    key = url.split("?")[0].replace("&amp;", "&")
    if key in seen or (key.endswith("/") and not key.startswith(SITE)): continue
    seen.add(key)
    path = local(key)
    if not os.path.exists(path):
        try: data = get(key)
        except Exception as e: print("FAIL", key, e, file=sys.stderr); continue
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, "wb").write(data)
    if path.endswith(TEXT) or key.startswith(SITE):
        text = html.unescape(open(path, "rb").read().decode("utf-8", "replace"))
        queue.extend(URL_RE.findall(text))
        base = key.rsplit("/", 1)[0] + "/"
        if path.endswith(".mjs"): queue.extend(base + m for m in REL_MJS_RE.findall(text))
        for r, b in NEW_URL_RE.findall(text):  # CMS chunks are fetched from /cms/, not /modules/
            queue.append(urllib.parse.urljoin(b, "./" + r).replace("/modules/", "/cms/"))
print(f"fetched {len(seen)} files")

# rewrite absolute CDN/site URLs to root-relative local paths and drop resize queries
for root, _, files in os.walk(OUT):
    for f in files:
        p = os.path.join(root, f)
        if not p.endswith(TEXT): continue
        s = open(p, "rb").read().decode("utf-8", "replace")
        n = re.sub(r'(https://framerusercontent\.com/' + STOP.replace("}", "}?") + r'+)\?' + STOP + "*", r"\1", s)
        for h in CDN: n = n.replace(f"https://{h}/", f"/{h}/")
        n = n.replace(SITE + "/", "/").replace(SITE, "/")
        # new URL(rel, base) needs an absolute base
        n = n.replace("new URL(`./", "new URL(location.origin+`/`+`./").replace("`,`/framerusercontent.com/", "`,location.origin+`/framerusercontent.com/")
        n = n.replace("new URL(location.origin+`/`+`./", "new URL(`./")
        if p.endswith(".html"):  # drop Framer analytics + on-page editor loader
            n = re.sub(r'<script async src="/?(?:https://)?events\.framer\.com/script\?v=2"[^>]*></script>', "", n)
            n = re.sub(r'<script>try\{if\(localStorage\.get\("__framer_force_showing_editorbar_since"\)\)[^<]*</script>', "", n)
        if p.endswith(".mjs"):
            # static hosts can't serve ?range=a-b,c-d: fetch whole file, slice ranges client-side
            n, k = re.subn(r'(\w+)\.searchParams\.set\(`range`,\w+\);let (\w+)=await (\w+)\(\1\);(if\(\2\.status!==200\)throw Error\(`Request failed: \$\{\2\.status\} \$\{\2\.statusText\}`\);)let (\w+)=await \2\.arrayBuffer\(\),(\w+)=new Uint8Array\(\5\);if\(\6\.length!==(\w+)\)',
                r'let \2=await \3(\1);\4let \5=await \2.arrayBuffer(),\6=new Uint8Array(\7);{let o=0;for(let e of n)\6.set(new Uint8Array(\5,e.from,e.to-e.from),o),o+=e.to-e.from}if(\6.length!==\7)', n)
            if "`range`" in n and not k: print("WARN: range fetch not patched in", p, file=sys.stderr)
            # contact forms: Framer's form API dies with the subscription -> open a prefilled email instead
            n, k = re.subn(r'async function wu\(e,t,n\)\{.*?\}\}function Tu', lambda m: MAILTO + "function Tu", n, count=1, flags=re.S)
            if "Framer-POW" in n: print("WARN: form submit not patched in", p, file=sys.stderr)
            n = n.replace("children:`Thank you`}", "children:`Now send it from your email app`}")
            n = re.sub(r'EditorBar:c===void 0\?void 0:\(\(\)=>\{.*?\}\)\(\),adaptLayoutToTextDirection', "EditorBar:void 0,adaptLayoutToTextDirection", n, flags=re.S)
        if n != s: open(p, "wb").write(n.encode())
