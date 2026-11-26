"""Find photos for a video: several candidates per query from Pixabay, Wikimedia Commons or Openverse, a numbered contact sheet to pick from, and a credits file.
  python3 images.py "titanic ship" outdir [--source pixabay|wikimedia|openverse|auto] [--n 6]
Python use: fetch(query, outdir, source, n) -> [{"file","title","author","license","page"}], sheet(files, out_jpg)
source "auto": Wikipedia article photos ("wiki"), then Openverse (free real photos: Commons, Flickr CC), Wikimedia search, and a little Pixabay stock.
Pixabay needs PIXABAY_KEY. Wikimedia/Openverse need no key; credits are written for licences that ask for them."""
import json, os, re, subprocess, sys, time, urllib.parse, urllib.request
UA = "MyFilmsStudioKit/1.2 (https://github.com/alialdean12-hue/my-films; educational shorts) python-urllib"
DOWN = set()   # sites that keep refusing (429) are skipped for the rest of the run; the other open sources are used
def get(url, tries=4):
    """polite download: on 429 (too many requests) waits a little (Retry-After, max 15 s) and retries once; a site that refuses twice is skipped."""
    host = urllib.parse.urlparse(url).netloc
    if host in DOWN: raise RuntimeError(f"{host} is refusing requests: skipped")
    refused = 0
    for k in range(tries):
        try: return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=40).read()
        except Exception as e:
            if getattr(e, "code", 0) == 429:
                refused += 1
                if refused >= 2:
                    if not host.startswith("upload."): DOWN.add(host)   # image files: only this one fails
                    raise
                ra = (getattr(e, "headers", None) or {}).get("Retry-After") or 8
                try: ra = float(ra)
                except ValueError: ra = 8
                time.sleep(min(15, ra))
            elif k == tries - 1: raise
            else: time.sleep(2 + 3 * k)
    raise RuntimeError("download failed")
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
    """open photos (Wikimedia Commons, Flickr CC, museums) with their licence; commercial use allowed; no tiny images."""
    d = json.loads(get("https://api.openverse.org/v1/images/?" + urllib.parse.urlencode({"q": q, "page_size": n * 3, "license_type": "commercial", "mature": "false"}))); res = []
    for r in d.get("results", []):
        if (r.get("width") or 999) < 500 or (r.get("height") or 999) < 400: continue
        try: f = _save(r["url"], os.path.join(out, f"ov{r['id'][:8]}.jpg"))
        except Exception: continue
        res.append(dict(file=f, title=r.get("title", ""), author=r.get("creator", ""), license=f"{r.get('license','')} {r.get('license_version','')}".strip(), page=r.get("foreign_landing_url", "")))
        if len(res) >= n: break
    return res
def pixabay_videos(q, out, n):
    """short stock videos (no audio needed). Returns the same dicts with "file" = mp4 and "thumb" = jpg."""
    key = os.environ.get("PIXABAY_KEY")
    if not key: raise SystemExit("PIXABAY_KEY is not set: videos need it.")
    d = json.loads(get("https://pixabay.com/api/videos/?" + urllib.parse.urlencode({"key": key, "q": q, "per_page": max(3, n), "safesearch": "true"})))
    res = []
    for h in d.get("hits", [])[:n]:
        v = h["videos"].get("medium") or h["videos"].get("small")
        if not v or not v.get("url"): continue
        f = os.path.join(out, f"pv{h['id']}.mp4"); _save(v["url"], f); th = f[:-4] + ".jpg"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "1", "-i", f, "-frames:v", "1", "-vf", "scale=640:-2", th])
        res.append(dict(file=f, thumb=th, title=h.get("tags", ""), author=h.get("user", ""), license="Pixabay Content License", page=h.get("pageURL", ""), duration=h.get("duration", 0)))
    return res
def fetch_videos(q, out, n=6):
    os.makedirs(out, exist_ok=True); r = pixabay_videos(q, out, n)
    if not r: raise SystemExit(f"NO VIDEOS for «{q}». Try simpler English words or use a photo (\"query\").")
    return r
def vertical(src, dst, dur, start=0.0, fps=30):
    """centre-crop to 1080x1920, exact length (loops if the clip is short), no audio."""
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-stream_loop", "-1", "-ss", f"{start}", "-i", src, "-t", f"{dur:.2f}", "-an",
                    "-vf", f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps={fps}", "-c:v", "libx264", "-preset", "fast", "-crf", "20", "-pix_fmt", "yuv420p", dst], check=True)
    return dst
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import remote
CACHE = os.environ.get("MEDIA_CACHE") or os.path.join(remote.ROOT, "media_cache")
def cache_key(q, photos="auto", wiki=None):
    import hashlib; return hashlib.sha1(f"{q.strip().lower()}|{photos}|{wiki or ''}".encode()).hexdigest()[:12]
def from_cache(q, photos="auto", wiki=None):
    """photos already fetched (here or by GitHub). Returns the list or None."""
    d = os.path.join(CACHE, cache_key(q, photos, wiki)); m = os.path.join(d, "credits.json")
    if not os.path.exists(m): return None
    res = json.load(open(m))
    for r in res: r["file"] = os.path.join(d, os.path.basename(r["file"])); r["thumb"] = os.path.join(d, os.path.basename(r.get("thumb") or r["file"]))
    return res
def ensure(queries):
    """queries = [(q, photos)] or [(q, photos, wiki)]. When this machine cannot reach Wikimedia, GitHub fetches all missing ones in ONE request."""
    queries = [tuple(x) + (None,) * (3 - len(x)) for x in queries]
    miss = {cache_key(q, p, w): dict(key=cache_key(q, p, w), q=q, photos=p, wiki=w) for q, p, w in queries if q and not from_cache(q, p, w)}
    if not miss or not remote.blocked("https://commons.wikimedia.org/"): return
    bad = remote.request("media", list(miss.values()), CACHE)
    if bad: print("NO PHOTOS for:", " | ".join(b["q"] for b in bad), "-> change these queries (simpler English words).", file=sys.stderr)
def fetch_mixed(q, out, n_wm=3, n_px=3, n_vid=0, video_q=None, photos="auto", wiki=None):
    """candidates for one scene: Wikimedia photos + Pixabay photos (videos only if n_vid>0).
    Each item has "kind" (photo|video) and "source"; "file" is a jpg or mp4, "thumb" a jpg for the sheet.
    Looks first in media_cache (filled here or by GitHub through ensure())."""
    c = from_cache(q, photos, wiki)
    if c: return c
    os.makedirs(out, exist_ok=True); res = []
    for t in ([wiki] if isinstance(wiki, str) else (wiki or [])):   # real photos of the event first
        try:
            for r in wiki_article(t, out, 4): r.update(kind="photo", source="wikipedia", thumb=r["file"]); res.append(r)
        except Exception as e: print(f"  wikipedia «{t}»: {type(e).__name__}", file=sys.stderr)
    plan = {"auto": [("openverse", 3), ("wikimedia", 2), ("pixabay", max(1, n_px - 1))], "wikimedia": [("wikimedia", n_wm + n_px)], "pixabay": [("pixabay", n_wm + n_px)], "openverse": [("openverse", n_wm + n_px)], "none": []}[photos]
    for src, n in plan:
        try:
            for r in SRC[src](q, out, n): r.update(kind="photo", source=src, thumb=r["file"]); res.append(r)
        except Exception as e: print(f"  {src}: {type(e).__name__}", file=sys.stderr)
    if photos == "auto" and sum(r["source"] != "pixabay" for r in res) < 2:   # too few real photos: ask Openverse for more
        try:
            seen = {r.get("page") for r in res}
            for r in openverse(q + " photo", out, 4):
                if r.get("page") not in seen: r.update(kind="photo", source="openverse", thumb=r["file"]); res.append(r)
        except Exception: pass
    if n_vid:
        try:
            for r in pixabay_videos(video_q or q, out, n_vid): r.update(kind="video", source="pixabay"); res.append(r)
        except (Exception, SystemExit) as e: print(f"  videos: {e}", file=sys.stderr)
    if not res: raise SystemExit(f"NO PHOTOS for «{q}». Try simpler English words, or give \"img\" files.")
    return res
def mixed_sheet(res, out):
    return sheet([r["thumb"] for r in res], out, labels=[f"{'VIDEO' if r['kind'] == 'video' else 'PHOTO'} {r['source'].upper()}" for r in res])
def wiki_article(title, out, n=6, lang="en"):
    """real photos of a real event/person/place: the images of its Wikipedia article (only free files hosted on Wikimedia Commons)."""
    if ":" in title[:4]: lang, title = title.split(":", 1)
    d = json.loads(get(f"https://{lang}.wikipedia.org/api/rest_v1/page/media-list/" + urllib.parse.quote(title.replace(" ", "_"))))
    res = []
    for it in d.get("items", []):
        if it.get("type") != "image" or not it.get("srcset"): continue
        src = "https:" + it["srcset"][-1]["src"]
        if "/wikipedia/commons/" not in src or src.lower().endswith((".svg", ".svg.png", ".gif")): continue
        name = it.get("title", "").replace("File:", "")
        if name.lower().endswith((".svg", ".gif")) or re.search(r"coat.of.arms|emblem|logo|flag.of|seal.of|signature|map", name, re.I): continue
        f = os.path.join(out, "wa" + re.sub(r"[^A-Za-z0-9]", "", name)[:40] + ".jpg")
        try: _save(src, f)
        except Exception: continue
        res.append(dict(file=f, title=name, author="Wikimedia Commons", license="see page (free licence on Commons)", page="https://commons.wikimedia.org/wiki/" + urllib.parse.quote(it.get("title", "").replace(" ", "_"))))
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
def sheet(files, out, cols=3, labels=None):
    """numbered contact sheet (1..n) so the agent can choose with "pick"; labels = text under the number (e.g. VIDEO PIXABAY)."""
    n = len(files); inputs = sum((["-i", f] for f in files), [])
    lab = labels or [""] * n
    fc = "".join(f"[{k}]scale=360:640:force_original_aspect_ratio=increase,crop=360:640,drawbox=x=0:y=0:w=360:h=90:color=black@0.7:t=fill,drawtext=text='{k+1}':fontsize=64:fontcolor=yellow:x=20:y=10"
                 + (f",drawtext=text='{lab[k]}':fontsize=30:fontcolor={'#7cff7c' if 'VIDEO' in lab[k] else 'white'}:x=100:y=30" if lab[k] else "") + f"[v{k}];" for k in range(n))
    rows = (n + cols - 1) // cols
    while n < rows * cols: fc += f"color=black:s=360x640[v{n}];"; n += 1
    lay = "|".join(f"{(k%cols)*360}_{(k//cols)*640}" for k in range(n))
    fc += "".join(f"[v{k}]" for k in range(n)) + f"xstack=inputs={n}:layout={lay}"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error"] + inputs + ["-filter_complex", fc, "-frames:v", "1", "-update", "1", "-q:v", "4", out], check=True)
    return out
if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) < 2: sys.exit(__doc__)
    src = a[a.index("--source") + 1] if "--source" in a else "auto"; n = int(a[a.index("--n") + 1]) if "--n" in a else 6
    r = fetch(a[0], a[1], src, n); sheet([x["file"] for x in r], os.path.join(a[1], "sheet.jpg"))
    json.dump(r, open(os.path.join(a[1], "credits.json"), "w"), ensure_ascii=False, indent=1)
    for k, x in enumerate(r): print(k + 1, x["license"], "|", x["title"][:60])
