"""Fetch photo candidates through GitHub when this machine cannot reach Wikimedia/Pixabay.
  python3 studio-kit/scripts/remote_media.py <episode.json> [more.json ...]
  python3 studio-kit/scripts/remote_media.py --q "gold bars" --q "old bank"
It finds every "query"/"query2" in the episode, pushes a small request file, waits for the GitHub
workflow "Media fetch" (1-3 min), then downloads the photos into ~/my-films/media_cache.
After that run the video as usual: the engines take the photos from the cache (sheets + "pick" unchanged)."""
import json, os, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import images as IM
ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=os.path.dirname(os.path.abspath(__file__)), capture_output=True, text=True).stdout.strip()
def git(*a, check=True): return subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True, check=check)
def walk(o, src, out):
    if isinstance(o, dict):
        src = o.get("source", src)
        for k in ("query", "query2"):
            if isinstance(o.get(k), str) and o[k].strip(): out.append({"q": o[k].strip(), "photos": src if src in ("auto", "wikimedia", "pixabay", "openverse") else "auto"})
        for v in o.values(): walk(v, src, out)
    elif isinstance(o, list):
        for v in o: walk(v, src, out)
def main():
    a = sys.argv[1:]
    if not a: sys.exit(__doc__)
    items = []
    while a:
        x = a.pop(0)
        if x == "--q": items.append({"q": a.pop(0), "photos": "auto"})
        else: ep = json.load(open(x)); walk(ep, ep.get("source", "auto"), items)
    seen, need = set(), []
    for it in items:
        k = IM.cache_key(it["q"], it["photos"])
        if k in seen or IM.from_cache(it["q"], it["photos"]): continue
        seen.add(k); need.append(dict(it, key=k))
    if not need: print("all photos are already in", IM.CACHE); return
    os.makedirs(os.path.join(ROOT, "media_requests"), exist_ok=True)
    name = f"media_requests/{time.strftime('%Y%m%d-%H%M%S')}.json"
    json.dump({"items": need}, open(os.path.join(ROOT, name), "w"), ensure_ascii=False, indent=1)
    branch = git("rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
    git("add", name); git("commit", "-m", f"media request ({len(need)} queries)", "--", name)
    p = git("push", "origin", f"HEAD:{branch}", check=False)
    if p.returncode: sys.exit("PUSH FAILED (the request must reach GitHub):\n" + p.stderr)
    print(f"requested {len(need)} queries on branch {branch}; waiting for GitHub (up to 12 min)...")
    keys = [n["key"] for n in need]; t0 = time.time()
    while time.time() - t0 < 720:
        time.sleep(20)
        if git("fetch", "-q", "origin", "media-cache", check=False).returncode: continue
        done = [k for k in keys if git("cat-file", "-e", f"FETCH_HEAD:{k}/credits.json", check=False).returncode == 0
                or git("cat-file", "-e", f"FETCH_HEAD:{k}/error.txt", check=False).returncode == 0]
        print(f"  {len(done)}/{len(keys)} ready", flush=True)
        if len(done) == len(keys): break
    else: sys.exit("TIMEOUT: GitHub did not finish. Check the «Media fetch» run in the repo's Actions tab, then run this command again (finished queries are kept).")
    os.makedirs(IM.CACHE, exist_ok=True)
    tar = subprocess.run(["git", "archive", "FETCH_HEAD", *keys], cwd=ROOT, capture_output=True, check=True).stdout
    subprocess.run(["tar", "-x", "-C", IM.CACHE], input=tar, check=True)
    bad = [n["q"] for n in need if not os.path.exists(os.path.join(IM.CACHE, n["key"], "credits.json"))]
    print("photos saved in", IM.CACHE)
    if bad: print("NO PHOTOS for:", " | ".join(bad), "-> change these queries (simpler English words) and run again.")
if __name__ == "__main__": main()
