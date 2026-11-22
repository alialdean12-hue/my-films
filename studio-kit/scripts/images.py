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
def fetch_mixed(q, out, n_wm=3, n_px=3, n_vid=3, video_q=None, photos="auto"):
    """candidates for one scene: Wikimedia photos + Pixabay photos + Pixabay videos (any part may be empty).
    Each item has "kind" (photo|video) and "source"; "file" is a jpg or mp4, "thumb" a jpg for the sheet."""
    os.makedirs(out, exist_ok=True); res = []
    plan = {"auto": [("wikimedia", n_wm), ("pixabay", n_px)], "wikimedia": [("wikimedia", n_wm + n_px)], "pixabay": [("pixabay", n_wm + n_px)], "openverse": [("openverse", n_wm + n_px)], "none": []}[photos]
    for src, n in plan:
        try:
            for r in SRC[src](q, out, n): r.update(kind="photo", source=src, thumb=r["file"]); res.append(r)
        except Exception as e: print(f"  {src}: {type(e).__name__}", file=sys.stderr)
    if not res and photos == "auto":
        try:
            for r in openverse(q, out, n_wm + n_px): r.update(kind="photo", source="openverse", thumb=r["file"]); res.append(r)
        except Exception: pass
    if n_vid:
        try:
            for r in pixabay_videos(video_q or q, out, n_vid): r.update(kind="video", source="pixabay"); res.append(r)
        except (Exception, SystemExit) as e: print(f"  videos: {e}", file=sys.stderr)
    if not res: raise SystemExit(f"NO PHOTOS OR VIDEOS for «{q}». Try simpler English words, or give \"img\" files.")
    return res
def mixed_sheet(res, out):
    return sheet([r["thumb"] for r in res], out, labels=[f"{'VIDEO' if r['kind'] == 'video' else 'PHOTO'} {r['source'].upper()}" for r in res])
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
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error"] + inputs + ["-filter_complex", fc, "-q:v", "4", out], check=True)
    return out
if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) < 2: sys.exit(__doc__)
    src = a[a.index("--source") + 1] if "--source" in a else "auto"; n = int(a[a.index("--n") + 1]) if "--n" in a else 6
    r = fetch(a[0], a[1], src, n); sheet([x["file"] for x in r], os.path.join(a[1], "sheet.jpg"))
    json.dump(r, open(os.path.join(a[1], "credits.json"), "w"), ensure_ascii=False, indent=1)
    for k, x in enumerate(r): print(k + 1, x["license"], "|", x["title"][:60])
