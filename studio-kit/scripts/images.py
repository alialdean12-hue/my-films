"""Find photos for a video: several candidates per query from Pixabay, Wikimedia Commons or Openverse, a numbered contact sheet to pick from, and a credits file.
  python3 images.py "titanic ship" outdir [--source pixabay|wikimedia|openverse|auto] [--n 6]
Python use: fetch(query, outdir, source, n) -> [{"file","title","author","license","page"}], sheet(files, out_jpg)
source "auto": wikimedia first (best for history, real people, places, artworks), then pixabay, then openverse.
Pixabay needs PIXABAY_KEY. Wikimedia/Openverse need no key; credits are written for licences that ask for them."""
import json, os, re, subprocess, sys, time, urllib.parse, urllib.request
UA = "studio-kit/1.0 (educational video tool)"
def get(url, tries=3):
    for k in range(tries):
        try: return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=40).read()
        except Exception as e:
            if k == tries - 1: raise
            time.sleep(2 + 3 * k)
def _save(url, path): open(path, "wb").write(get(url)); return path
def pixabay(q, out, n):
    key = os.environ.get("PIXABAY_KEY")
    if not key: return []
    d = json.loads(get("https://pixabay.com/api/?" + urllib.parse.urlencode({"key": key, "q": q, "per_page": max(3, n), "safesearch": "true", "image_type": "photo"})))
    res = []
    for h in d.get("hits", [])[:n]:
        f = os.path.join(out, f"px{h['id']}.jpg"); _save(h.get("largeImageURL") or h["webformatURL"], f)
        res.append(dict(file=f, title=h.get("tags", ""), author=h.get("user", ""), license="Pixabay Content License", page=h.get("pageURL", "")))
    return res
def wikimedia(q, out, n):
    u = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode({"action": "query", "generator": "search", "gsrnamespace": 6, "gsrsearch": q + " filetype:bitmap", "gsrlimit": n * 2,
        "prop": "imageinfo", "iiprop": "url|extmetadata|mime", "iiurlwidth": 1600, "format": "json"})
    d = json.loads(get(u)); res = []
    for p in sorted(d.get("query", {}).get("pages", {}).values(), key=lambda p: p.get("index", 0)):
        ii = (p.get("imageinfo") or [{}])[0]
        if ii.get("mime") not in ("image/jpeg", "image/png"): continue
        md = ii.get("extmetadata", {}); lic = md.get("LicenseShortName", {}).get("value", "")
        if not re.search(r"public domain|cc0|cc by|cc-by|pd", lic, re.I): continue
        f = os.path.join(out, f"wm{p['pageid']}.jpg"); _save(ii.get("thumburl") or ii["url"], f)
        res.append(dict(file=f, title=p.get("title", ""), author=re.sub("<[^>]+>", "", md.get("Artist", {}).get("value", ""))[:80], license=lic, page=ii.get("descriptionurl", "")))
        if len(res) >= n: break
    return res
def openverse(q, out, n):
    d = json.loads(get("https://api.openverse.org/v1/images/?" + urllib.parse.urlencode({"q": q, "page_size": n * 2, "license_type": "commercial"}))); res = []
    for r in d.get("results", []):
        try: f = _save(r["url"], os.path.join(out, f"ov{r['id'][:8]}.jpg"))
        except Exception: continue
        res.append(dict(file=f, title=r.get("title", ""), author=r.get("creator", ""), license=f"{r.get('license','')} {r.get('license_version','')}".strip(), page=r.get("foreign_landing_url", "")))
        if len(res) >= n: break
    return res
SRC = {"pixabay": pixabay, "wikimedia": wikimedia, "openverse": openverse}
def fetch(q, out, source="auto", n=6):
    os.makedirs(out, exist_ok=True); order = ["wikimedia", "pixabay", "openverse"] if source == "auto" else [source]
    errors = []
    for s in order:
        try:
            r = SRC[s](q, out, n)
            if r: return r
        except Exception as e: errors.append(f"{s}: {type(e).__name__}")
    raise SystemExit(f"NO PHOTOS for «{q}» ({', '.join(errors) or 'no results'}). Try simpler English words, another source, or give \"img\" files.")
def sheet(files, out, cols=3):
    """numbered contact sheet (1..n) so the agent can choose with "pick"."""
    n = len(files); inputs = sum((["-i", f] for f in files), [])
    fc = "".join(f"[{k}]scale=360:640:force_original_aspect_ratio=increase,crop=360:640,drawbox=x=0:y=0:w=90:h=90:color=black@0.7:t=fill,drawtext=text='{k+1}':fontsize=64:fontcolor=yellow:x=24:y=10[v{k}];" for k in range(n))
    rows = (n + cols - 1) // cols
    while n < rows * cols: fc += f"color=black:s=360x640[v{n}];"; n += 1
    lay = "|".join(f"{(k%cols)*360}_{(k//cols)*640}" for k in range(n))
    fc += "".join(f"[v{k}]" for k in range(n)) + f"xstack=inputs={n}:layout={lay}"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error"] + inputs + ["-filter_complex", fc, "-q:v", "4", out], check=True)
    return out
if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) < 2: sys.exit(__doc__)
    src = a[a.index("--source") + 1] if "--source" in a else "auto"; n = int(a[a.index("--n") + 1]) if "--n" in a else 6
    r = fetch(a[0], a[1], src, n); sheet([x["file"] for x in r], os.path.join(a[1], "sheet.jpg"))
    json.dump(r, open(os.path.join(a[1], "credits.json"), "w"), ensure_ascii=False, indent=1)
    for k, x in enumerate(r): print(k + 1, x["license"], "|", x["title"][:60])
