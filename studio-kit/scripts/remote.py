"""GitHub as a helper when this sandbox blocks a site (photos: Wikimedia/Pixabay, voice: edge-tts).
request(kind, items): pushes remote_requests/<kind>-<time>.json, waits for the workflow «Remote fetch»
(.github/workflows/remote.yml), then copies <key>/... from branch <kind>-cache into cache_dir.
Each item needs a unique "key". Finished keys stay on the cache branch, so asking again is instant."""
import json, os, subprocess, sys, time
KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); ROOT = os.path.dirname(KIT)
def git(*a, check=True): return subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True, check=check)
def blocked(url, timeout=6):
    """True when this machine cannot open url (firewall, DNS, TLS cut)."""
    import urllib.request
    try: urllib.request.urlopen(urllib.request.Request(url, method="HEAD", headers={"User-Agent": "studio-kit"}), timeout=timeout); return False
    except Exception as e: return not hasattr(e, "code")   # an HTTP error code means the site answered
def _have(branch, k): return any(git("cat-file", "-e", f"FETCH_HEAD:{k}/{f}", check=False).returncode == 0 for f in ("done", "error.txt"))
def request(kind, items, cache_dir, wait=720):
    os.makedirs(cache_dir, exist_ok=True)
    need = [it for it in items if not os.path.exists(os.path.join(cache_dir, it["key"], "done"))]
    if not need: return []
    branch = f"{kind}-cache"; keys = [n["key"] for n in need]
    if git("fetch", "-q", "origin", branch, check=False).returncode == 0 and all(_have(branch, k) for k in keys): pass
    else:
        os.makedirs(os.path.join(ROOT, "remote_requests"), exist_ok=True)
        name = f"remote_requests/{kind}-{time.strftime('%Y%m%d-%H%M%S')}.json"
        json.dump({"kind": kind, "items": need}, open(os.path.join(ROOT, name), "w"), ensure_ascii=False, indent=1)
        cur = git("rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
        git("add", name); git("commit", "-q", "-m", f"{kind} request ({len(need)})", "--", name)
        p = git("push", "-q", "origin", f"HEAD:{cur}", check=False)
        if p.returncode: sys.exit(f"PUSH FAILED: GitHub must receive the {kind} request.\n{p.stderr[-400:]}")
        print(f"{kind}: this machine cannot reach the site, GitHub is fetching {len(need)} item(s) (1-3 min)...", flush=True)
        t0 = time.time()
        while True:
            time.sleep(15)
            if git("fetch", "-q", "origin", branch, check=False).returncode == 0:
                n = sum(_have(branch, k) for k in keys); print(f"  {n}/{len(keys)} ready", flush=True)
                if n == len(keys): break
            if time.time() - t0 > wait: sys.exit(f"TIMEOUT: GitHub did not finish the {kind} request. Open the repo's Actions tab («Remote fetch»), then run again.")
    tar = subprocess.run(["git", "archive", "FETCH_HEAD", *keys], cwd=ROOT, capture_output=True, check=True).stdout
    subprocess.run(["tar", "-x", "-C", cache_dir], input=tar, check=True)
    return [n for n in need if os.path.exists(os.path.join(cache_dir, n["key"], "error.txt"))]
