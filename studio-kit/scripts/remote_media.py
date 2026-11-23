"""Fetch the photos of an episode in advance (all queries in one go; through GitHub if this sandbox blocks the sites).
  python3 studio-kit/scripts/remote_media.py <episode.json> [--force-remote]
The engines do this by themselves; this command is only to prepare photos early."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import images as IM, remote
def walk(o, src, out):
    if isinstance(o, dict):
        src = o.get("source", src)
        for k in ("query", "query2"):
            if isinstance(o.get(k), str) and o[k].strip(): out.append((o[k].strip(), src if src in ("auto", "wikimedia", "pixabay", "openverse") else "auto"))
        for v in o.values(): walk(v, src, out)
    elif isinstance(o, list):
        for v in o: walk(v, src, out)
def queries(ep):
    out = []; walk(ep, ep.get("source", "auto"), out); return out
if __name__ == "__main__":
    if len(sys.argv) < 2: sys.exit(__doc__)
    ep = json.load(open(sys.argv[1])); qs = queries(ep)
    if "--force-remote" in sys.argv: remote.blocked = lambda *a, **k: True
    IM.ensure(qs); print(sum(bool(IM.from_cache(q, p)) for q, p in qs), "/", len(qs), "queries have photos in", IM.CACHE)
