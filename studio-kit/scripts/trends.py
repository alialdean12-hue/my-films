"""Real view counts of the reference channels (studio-kit/topics/channels.json): latest 15 videos each, sorted by views.
  python3 studio-kit/scripts/trends.py            -> prints the table and writes ~/my-films/TRENDS.md
Works through GitHub (workflow «Remote fetch») when this sandbox cannot reach YouTube. Use it before proposing topics."""
import json, os, re, sys, time, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import remote
CH = os.path.join(remote.KIT, "topics", "channels.json")
CACHE = os.path.join(remote.ROOT, "trends_cache")
def parse(xml):
    out = []
    for e in re.findall(r"<entry>(.*?)</entry>", xml, re.S):
        g = lambda p: (re.search(p, e, re.S) or [None, ""])[1]
        out.append(dict(title=re.sub("&quot;", '"', g(r"<title>(.*?)</title>")), views=int(g(r'views="(\d+)"') or 0),
                        date=g(r"<published>(.*?)</published>")[:10], url=g(r'<link rel="alternate" href="(.*?)"/>')))
    return out
def feed(cid):
    return urllib.request.urlopen(urllib.request.Request(f"https://www.youtube.com/feeds/videos.xml?channel_id={cid}", headers={"User-Agent": "studio-kit"}), timeout=20).read().decode()
def main():
    chans = json.load(open(CH))["channels"]; day = time.strftime("%Y%m%d"); data = {}
    if not remote.blocked("https://www.youtube.com/"):
        for c in chans:
            try: data[c["id"]] = parse(feed(c["id"]))
            except Exception as e: print("skip", c["name"], type(e).__name__)
    else:
        items = [dict(key=f'{c["id"]}-{day}', cid=c["id"]) for c in chans]
        bad = remote.request("trends", items, CACHE)
        for c in chans:
            f = os.path.join(CACHE, f'{c["id"]}-{day}', "feed.json")
            if os.path.exists(f): data[c["id"]] = json.load(open(f))
    lines = [f"# TRENDS {time.strftime('%Y-%m-%d')} (latest 15 videos per channel, by views)\n"]
    for c in chans:
        v = sorted(data.get(c["id"], []), key=lambda x: -x["views"])
        if not v: continue
        med = sorted(x["views"] for x in v)[len(v)//2]
        lines.append(f"\n## {c['name']} · {c['niche']} · median {med:,}\n")
        lines += [f"- {x['views']:,} · {x['date']} · {x['title']}" for x in v]
    txt = "\n".join(lines) + "\n"; print(txt)
    open(os.path.join(remote.ROOT, "TRENDS.md"), "w").write(txt)
if __name__ == "__main__": main()
