from lib import *
import json
CSS = ('.ph{position:absolute;inset:-6%;background-size:cover;background-position:center}.vg{position:absolute;inset:0;background:radial-gradient(ellipse at 50% 45%,transparent 55%,#0000004d 100%)}'
       '.cap{position:absolute;left:80px;right:80px;top:1240px;text-align:center;font-weight:900;font-size:84px;line-height:1.25;color:#fff;-webkit-text-stroke:12px #111;paint-order:stroke fill;text-shadow:0 6px 18px rgba(0,0,0,.45)}.dt{position:absolute;left:0;right:0;top:300px;text-align:center}.dt span{background:#c9a24a;color:#111;font-weight:900;font-size:62px;padding:2px 30px 10px}'
       '.bar{position:absolute;left:300px;right:300px;top:1215px;height:8px;background:#c9a24a}')
ep = load(); B = ep["beats"]
STYLE = globals().get("__STYLE__", "doc")   # "hybrid" = style 11: documentary photo + collage stickers and paper captions
HYB = STYLE == "hybrid"
GRADES = {"sepia": "sepia(.35) contrast(1.1) saturate(.8) brightness(.85)", "bw": "grayscale(1) contrast(1.2) brightness(.85)", "cold": "saturate(.7) hue-rotate(15deg) brightness(.85) contrast(1.1)",
          "warm": "sepia(.2) saturate(1.2) brightness(.9)", "noir": "grayscale(1) contrast(1.6) brightness(.7)", "vivid": "saturate(1.4) contrast(1.15) brightness(.9)", "faded": "saturate(.5) contrast(.85) brightness(1.05)",
          "green": "sepia(.3) hue-rotate(60deg) saturate(.9) brightness(.8)", "red": "sepia(.4) hue-rotate(-30deg) saturate(1.4) brightness(.75)", "night": "saturate(.6) hue-rotate(190deg) brightness(.6) contrast(1.2)",
          "old_film": "sepia(.8) contrast(1.3) brightness(.8)", "clean": "none", "natural": "contrast(1.05) saturate(1.05)"}
CAMS = {"in": (1.0, 1.18, 0, 0), "out": (1.2, 1.0, 0, 0), "left": (1.15, 1.15, 60, 0), "right": (1.15, 1.15, -60, 0), "up": (1.15, 1.15, 0, 60), "down": (1.15, 1.15, 0, -60), "still": (1.05, 1.05, 0, 0), "fast_in": (1.0, 1.4, 0, 0)}
CAPS = {  # caption looks
 "gold": ('top:1240px;color:#fff;text-shadow:0 6px 24px #000', True), "box": ('top:1260px;color:#111;', False), "lower": ('top:1500px;text-align:right;color:#fff;font-size:66px', False),
 "news": ('top:1300px;color:#fff;', False), "type": ('top:1280px;color:#f4ecd8;font-family:monospace,Cairo;font-size:64px', False), "big": ('top:780px;color:#fff;font-size:150px;text-shadow:0 10px 40px #000', False),
 "top": ('top:320px;color:#fff;text-shadow:0 6px 24px #000', False), "red": ('top:1260px;color:#fff;', False),
 "paper": ('top:250px;color:#141414;-webkit-text-stroke:0;text-shadow:none', False),
}
def capdiv(i, b):
    st = b.get("caption", ep.get("caption", "paper" if HYB else "gold")); css, bar = CAPS.get(st, CAPS["gold"]); t = b.get("cap", "")
    if st == "box": t = f'<span style="background:#f4ecd8;padding:6px 30px 16px;box-shadow:10px 10px 0 #c9a24a">{t}</span>'
    if st == "news": t = f'<span style="background:#c0392b;padding:6px 30px 16px">{t}</span>'
    if st == "red": t = f'<span style="background:#e5322d;padding:6px 30px 16px;transform:rotate(-2deg);display:inline-block">{t}</span>'
    if st == "paper":   # torn paper strip with tape and a yellow marker on the key word
        t = (f'<span class="tp" style="display:inline-block;background:#f6eedc;padding:20px 46px 30px;transform:rotate(-2deg);'
             f'clip-path:polygon(0 6%,4% 0,9% 5%,15% 1%,22% 6%,30% 0,38% 5%,46% 1%,55% 6%,63% 0,71% 5%,79% 1%,87% 6%,94% 0,100% 5%,98% 50%,100% 95%,94% 100%,86% 94%,78% 100%,70% 95%,61% 100%,52% 94%,44% 100%,36% 95%,27% 100%,19% 94%,11% 100%,4% 95%,0 100%,2% 50%);'
             f'box-shadow:0 14px 26px rgba(0,0,0,.35)">{t.replace("color:#ffd21f", "color:#141414;background:#ffd21f;padding:0 10px").replace("color:#ff3b3b", "color:#fff;background:#d0202a;padding:0 10px")}</span>'
             f'<span style="position:absolute;left:50%;top:-14px;width:150px;height:46px;margin-left:-75px;background:rgba(240,230,190,.75);transform:rotate(4deg)"></span>')
    if st == "lower": t = f'<span style="border-right:16px solid #c9a24a;padding-right:24px;background:linear-gradient(270deg,#000c,#0000)">{t}</span>'
    return (f'<div class="bar" id="br{i}"></div>' if bar else "") + f'<div class="cap" id="cp{i}" style="opacity:0;{css}">{t}</div>', bar
def overlay(i, b, s, e):
    o = b.get("overlay"); h, js = "", []
    if not o: return h, js
    o = [o] if isinstance(o, str) else o
    sv = ""
    for k in o:
        if k == "circle": x, y, r = b.get("at", [540, 900, 220]); L = int(6.4 * r); sv += f'<path id="oc{i}" d="M{x+r},{y} A{r},{r*.9} 0 1,1 {x+r-1},{y-6}" fill="none" stroke="#e5322d" stroke-width="12" stroke-dasharray="{L}" stroke-dashoffset="{L}"/>'; js.append(f'tl.to("#oc{i}",{{strokeDashoffset:0,duration:.7}},{s+.6:.2f});')
        if k == "arrow": (x1, y1), (x2, y2) = b.get("arrow", [[200, 600], [520, 880]]); sv += f'<path id="oa{i}" d="M{x1},{y1} L{x2},{y2}" stroke="#ffd21f" stroke-width="16" stroke-linecap="round" stroke-dasharray="900" stroke-dashoffset="900" marker-end="url(#ah{i})"/><marker id="ah{i}" markerWidth="6" markerHeight="6" refX="3" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6Z" fill="#ffd21f"/></marker>'; js.append(f'tl.to("#oa{i}",{{strokeDashoffset:0,duration:.6}},{s+.6:.2f});')
        if k == "route": sv += f'<path id="rt{i}" d="M260,820 C420,700 640,720 860,900" fill="none" stroke="#e5322d" stroke-width="12" stroke-dasharray="26 16"/><circle cx="260" cy="820" r="20" fill="#e5322d"/><circle id="dot{i}" cx="860" cy="900" r="22" fill="#e5322d" opacity="0"/>'; js += [f'tl.fromTo("#rt{i}",{{strokeDashoffset:900}},{{strokeDashoffset:0,duration:2,ease:"none"}},{s+.3:.2f});', f'tl.to("#dot{i}",{{opacity:1,duration:.2}},{s+2.3:.2f});']
        if k == "zoombox": x, y, w = b.get("box", [400, 700, 300]); sv += f'<rect id="zb{i}" x="{x}" y="{y}" width="{w}" height="{w}" fill="none" stroke="#ffd21f" stroke-width="10" opacity="0"/>'; js.append(f'tl.fromTo("#zb{i}",{{opacity:0,scale:1.6,transformOrigin:"50% 50%"}},{{opacity:1,scale:1,duration:.4}},{s+.5:.2f});')
        if k == "redact": sv += "".join(f'<rect class="rd{i}" x="{150+R(j)*40:.0f}" y="{600+j*90}" width="{500+R(j+5)*200:.0f}" height="50" fill="#111"/>' for j in range(4)); js.append(f'tl.fromTo("#S{i} .rd{i}",{{scaleX:0,transformOrigin:"0% 50%"}},{{scaleX:1,duration:.3,stagger:.2}},{s+.4:.2f});')
        if k == "film": sv += '<rect width="1080" height="1920" fill="none" stroke="#000" stroke-width="80"/>' + "".join(f'<rect x="{x}" y="{y}" width="30" height="40" rx="6" fill="#ddd"/>' for x in (10, 1040) for y in range(20, 1920, 80))
        if k == "letterbox": sv += '<rect width="1080" height="260" fill="#000"/><rect y="1660" width="1080" height="260" fill="#000"/>'
        if k == "vhs": sv += "".join(f'<rect class="vh{i}" x="0" y="{(R(j)+1)*960:.0f}" width="1080" height="{4+abs(R(j+3))*10:.0f}" fill="#fff" opacity=".12"/>' for j in range(10)) + '<text x="70" y="140" text-anchor="end" font-size="56" font-family="monospace" fill="#fff" opacity=".8">▶ PLAY</text>'; js.append(f'tl.fromTo("#S{i} .vh{i}",{{y:0}},{{y:300,duration:.5,repeat:{int((e-s)/.5)+2},ease:"none"}},{s-.3:.2f});')
        if k == "counter": h += f'<div class="cap" id="cn{i}" style="top:640px;font-size:220px;color:#ffd21f;text-shadow:0 10px 40px #000">0</div>'; js.append(f'const o{i}={{v:0}};tl.to(o{i},{{v:{b.get("number",100)},duration:1.6,ease:"power2.out",onUpdate:()=>{{document.getElementById("cn{i}").textContent=Math.round(o{i}.v).toLocaleString("en")+"{b.get("unit","")}"}}}},{s+.3:.2f});')
        if k == "stamp": h += f'<div class="cap" id="sp{i}" style="top:700px;font-size:120px;color:#e5322d"><span style="border:14px solid #e5322d;padding:0 30px 14px;display:inline-block;transform:rotate(-10deg)">{b.get("stamp","سرّي")}</span></div>'; js.append(f'tl.fromTo("#sp{i}",{{opacity:0,scale:3}},{{opacity:1,scale:1,duration:.25,ease:"power4.in"}},{s+.8:.2f});')
        if k == "quote": h += f'<div class="cap" id="qt{i}" style="top:560px;font-size:76px;color:#f4ecd8;font-style:italic">«{b.get("quote","")}»</div>'; js.append(f'tl.fromTo("#qt{i}",{{opacity:0}},{{opacity:1,duration:.8}},{s+.3:.2f});')
        if k == "split" and b.get("img2_ready"): h += f'<div id="sp2{i}" style="position:absolute;left:540px;top:0;width:540px;height:1920px;background:url(img/{i}b.jpg) center/cover;border-left:10px solid #fff;filter:{GRADES.get(b.get("grade", ep.get("grade", "sepia")))}"></div>'; js.append(f'tl.fromTo("#sp2{i}",{{x:540}},{{x:0,duration:.6,ease:"power3.out"}},{s+.5:.2f});')
    if sv: h = f'<svg class="full" width="1080" height="1920" viewBox="0 0 1080 1920">{sv}</svg>' + h
    return h, js
def scene(i, b, s, e, c0, c1):
    D = c1 - c0; js = []
    cam = b.get("cam", ep.get("cam")); a, z, dx, dy = CAMS[cam] if isinstance(cam, str) else (cam or [(1.0, 1.18, -40, 0), (1.2, 1.0, 0, 30), (1.0, 1.15, 30, -20), (1.15, 1.0, 0, -30)][i % 4])
    g = GRADES.get(b.get("grade", ep.get("grade", "natural")), GRADES["natural"])
    if b.get("_vsrc"):
        sys.path.insert(0, KIT + "/scripts"); import images as IM
        vd = os.path.abspath(sys.argv[2]) + "/project/vid"; os.makedirs(vd, exist_ok=True)
        if not os.path.exists(f"{vd}/{i}.mp4"): IM.vertical(b["_vsrc"], f"{vd}/{i}.mp4", D + .2, b.get("video_start", 1.0))
        TOP.append(f'<video id="vid{i}" src="vid/{i}.mp4" data-start="{c0:.2f}" data-duration="{D:.2f}" data-track-index="0" muted playsinline style="position:absolute;inset:0;width:1080px;height:1920px;object-fit:cover;filter:{g}"></video>')
        h = '<div class="vg"></div>'
    else: h = f'<div class="ph" id="ph{i}" style="background-image:url(img/{i}.jpg);filter:{g}"></div><div class="vg"></div>'
    if b.get("_sticker"):   # cut-out sticker of the key person/object, pops in front of the photo
        st = b.get("sticker", {}); x, y, w = st.get("x", 560), st.get("y", 1180), st.get("size", 640); rot = st.get("rotate", -4 if i % 2 else 4)
        h += (f'<img id="stk{i}" src="img/{i}s.png" style="position:absolute;left:{x - w/2:.0f}px;top:{y - w/2:.0f}px;width:{w}px;height:{w}px;object-fit:contain;'
              f'filter:drop-shadow(0 18px 18px rgba(0,0,0,.45))"/>')
        js.append(f'tl.fromTo("#stk{i}",{{scale:0,rotation:{rot*4}}},{{scale:1,rotation:{rot},duration:.5,ease:"back.out(2)"}},{s+.5:.2f});')
        js.append(f'tl.to("#stk{i}",{{rotation:{-rot*.4:.1f},duration:.5,ease:"sine.inOut",yoyo:true,repeat:{int((e-s)/.5)}}},{s+1.0:.2f});')
    oh, oj = overlay(i, b, s, e); h += oh; js += oj
    if b.get("route"): o2, j2 = overlay(i, {"overlay": "route"}, s, e); h += o2; js += j2
    if b.get("date"): h += f'<div class="dt" id="dt{i}" style="opacity:0"><span>{b["date"]}</span></div>'
    ch, bar = capdiv(i, b); h += ch
    if b.get("flash"): h += f'<div id="fl{i}" style="position:absolute;inset:0;background:#fff;opacity:0"></div>'
    tr = b.get("transition", ep.get("transition", "fade"))
    js.append(f'tl.fromTo("#{"vid" if b.get("_vsrc") else "ph"}{i}",{{scale:{a if not b.get("_vsrc") else 1.0},x:{dx if not b.get("_vsrc") else 0},y:{dy if not b.get("_vsrc") else 0}}},{{scale:{z if not b.get("_vsrc") else 1.08},x:{-dx if not b.get("_vsrc") else 0},y:{-dy if not b.get("_vsrc") else 0},duration:{D:.2f},ease:"none"}},{c0:.2f});')
    if i:
        js.append({"fade": f'tl.fromTo("#S{i}",{{opacity:0}},{{opacity:1,duration:.45}},{c0:.2f});', "cut": f'tl.fromTo("#S{i}",{{opacity:0}},{{opacity:1,duration:.05}},{c0+.3:.2f});',
                   "slide": f'tl.fromTo("#S{i}",{{x:1080}},{{x:0,duration:.45,ease:"power3.out"}},{c0:.2f});', "up": f'tl.fromTo("#S{i}",{{y:1920}},{{y:0,duration:.45,ease:"power3.out"}},{c0:.2f});',
                   "zoom": f'tl.fromTo("#S{i}",{{opacity:0,scale:1.5}},{{opacity:1,scale:1,duration:.45,ease:"power3.out"}},{c0:.2f});', "blur": f'tl.fromTo("#S{i}",{{opacity:0,filter:"blur(30px)"}},{{opacity:1,filter:"blur(0px)",duration:.5}},{c0:.2f});',
                   "flash": f'tl.fromTo("#S{i}",{{opacity:0}},{{opacity:1,duration:.05}},{c0+.3:.2f});tl.fromTo("#S{i}",{{filter:"brightness(4)"}},{{filter:"brightness(1)",duration:.4}},{c0+.3:.2f});',
                   "glitch": f'tl.fromTo("#S{i}",{{opacity:0,x:-40}},{{opacity:1,x:0,duration:.06,repeat:4,yoyo:true}},{c0+.2:.2f});'}.get(tr, ""))
    if b.get("_vsrc") and i: js.append(f'tl.fromTo("#vid{i}",{{opacity:0}},{{opacity:1,duration:.45}},{c0:.2f});')
    if bar: js.append(f'tl.fromTo("#br{i}",{{scaleX:0}},{{scaleX:1,duration:.5,ease:"power2.out"}},{s+.1:.2f});')
    if b.get("caption", ep.get("caption", "paper" if HYB else "gold")) == "paper":
        js.append(f'tl.fromTo("#cp{i}",{{opacity:0,scale:1.6,rotation:-6}},{{opacity:1,scale:1,rotation:0,duration:.35,ease:"power3.in"}},{s+.2:.2f});')
    else: js.append(f'tl.fromTo("#cp{i}",{{opacity:0,y:30}},{{opacity:1,y:0,duration:.6,ease:"power2.out"}},{s+.3:.2f});')
    if b.get("date"): js.append(f'tl.fromTo("#dt{i}",{{opacity:0,scaleX:1.4}},{{opacity:1,scaleX:1,duration:.6}},{s:.2f});')
    if b.get("flash"): js += [f'tl.fromTo("#fl{i}",{{opacity:.9}},{{opacity:0,immediateRender:false,duration:.5}},{s+.9:.2f});', f'tl.fromTo("#S{i}",{{x:0}},{{x:14,duration:.05,yoyo:true,repeat:9}},{s+.9:.2f});']
    return h, js
def images():
    """each beat: "query" (English words) -> candidates sheet candidates/beatN.jpg with Wikimedia photos + Pixabay photos + Pixabay videos;
    choose with "pick": N. Or give "img"/"video" files. "source" limits photos (auto|wikimedia|pixabay|openverse|none), "videos": 0 turns videos off.
    The same photo/video is never used in two scenes: already used items are removed from later sheets, and a repeated pick stops the run."""
    sys.path.insert(0, KIT + "/scripts"); import images as IM
    OUT = os.path.abspath(sys.argv[2]); out = OUT + "/project/img"; cand = OUT + "/candidates"; os.makedirs(out, exist_ok=True); os.makedirs(cand, exist_ok=True)
    credits, used = [], {}
    src0 = ep.get("source", "auto")   # all photo searches of the video in one go (through GitHub if this sandbox blocks the sites)
    IM.ensure([(q, b.get("source", src0), b.get("wiki")) for b in B if not (b.get("img") or b.get("video")) for q in [b.get("query") or b.get("video_query")]]
              + [(b["query2"], "auto") for b in B if b.get("query2") and not b.get("img2")]
              + [(b["sticker"]["query"], b["sticker"].get("source", "auto")) for b in B if isinstance(b.get("sticker"), dict) and b["sticker"].get("query")])
    def key(r): return r.get("page") or r["file"]
    for i, b in enumerate(B):
        tag = ""
        if b.get("img") or b.get("video"):
            src = b.get("video") or b.get("img"); src = src if os.path.isabs(src) else os.path.join(ep["_dir"], src)
            if src in used: sys.exit(f"REPEATED MEDIA: scene {i+1} uses the same file as scene {used[src]}. Every scene needs its own photo/video.")
            used[src] = i + 1
            if b.get("video"): b["_vsrc"] = src
            else: sh(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-vf", "scale=-2:2100", "-q:v", "3", f"{out}/{i}.jpg"])
            continue
        q = b.get("query") or b.get("video_query")
        cf = f"{cand}/q{i}"; meta = os.path.join(cf, "credits.json")
        if os.path.exists(meta): res = json.load(open(meta))
        else:
            nv = 0 if b.get("videos", ep.get("videos", 3)) == 0 else 3
            res = IM.fetch_mixed(q, cf, video_q=b.get("video_query"), n_vid=0, photos=b.get("source", ep.get("source", "auto")), wiki=b.get("wiki"))
            json.dump(res, open(meta, "w"), ensure_ascii=False)
        fresh = [r for r in res if key(r) not in used]          # never offer what an earlier scene already uses
        if not fresh: sys.exit(f"NO NEW MEDIA for scene {i+1} («{q}»): every candidate is already used. Change the query of this scene.")
        IM.mixed_sheet(fresh, f"{cand}/beat{i+1}.jpg")
        k = int(b.get("pick", 1))
        if k > len(fresh): k = 1
        r = fresh[k - 1]; used[key(r)] = i + 1
        if r["kind"] == "video": b["_vsrc"] = r["file"]
        else: sh(["ffmpeg", "-y", "-loglevel", "error", "-i", r["file"], "-vf", "scale=-2:2100", "-q:v", "3", f"{out}/{i}.jpg"])
        credits.append(f"مشهد {i+1} ({'فيديو' if r['kind'] == 'video' else 'صورة'}): {r['title'][:60]} — {r['author']} — {r['license']} — {r['page']}")
        if b.get("img2") or b.get("query2"):
            q2 = b.get("query2"); cf2 = f"{cand}/q{i}b"; m2 = os.path.join(cf2, "credits.json")
            if b.get("img2"): src2 = b["img2"] if os.path.isabs(b["img2"]) else os.path.join(ep["_dir"], b["img2"])
            else:
                res2 = json.load(open(m2)) if os.path.exists(m2) else IM.fetch_mixed(q2, cf2, n_vid=0)
                if not os.path.exists(m2): json.dump(res2, open(m2, "w"), ensure_ascii=False)
                f2 = [x for x in res2 if key(x) not in used] or res2; r2 = f2[max(1, min(int(b.get("pick2", 1)), len(f2))) - 1]; used[key(r2)] = i + 1; src2 = r2["file"]
            sh(["ffmpeg", "-y", "-loglevel", "error", "-i", src2, "-vf", "scale=-2:2100", "-q:v", "3", f"{out}/{i}b.jpg"]); b["img2_ready"] = True
        stk = b.get("sticker")
        if stk:
            if stk.get("img"): s_src = stk["img"] if os.path.isabs(stk["img"]) else os.path.join(ep["_dir"], stk["img"])
            else:
                cf3 = f"{cand}/q{i}s"; m3 = os.path.join(cf3, "credits.json")
                res3 = json.load(open(m3)) if os.path.exists(m3) else IM.fetch_mixed(stk["query"], cf3, n_vid=0, photos=stk.get("source", "auto"))
                if not os.path.exists(m3): json.dump(res3, open(m3, "w"), ensure_ascii=False)
                f3 = [x for x in res3 if key(x) not in used]
                if not f3: sys.exit(f"NO NEW MEDIA for the sticker of scene {i+1}: change its query.")
                IM.mixed_sheet(f3, f"{cand}/sticker{i+1}.jpg")
                r3 = f3[max(1, min(int(stk.get("pick", 1)), len(f3))) - 1]; used[key(r3)] = i + 1; s_src = r3["file"]
                credits.append(f"ملصق مشهد {i+1}: {r3['title'][:60]} — {r3['author']} — {r3['license']} — {r3['page']}")
            sys.path.insert(0, KIT + "/collage"); import cutout
            try: cutout.sticker(s_src, f"{out}/{i}s.png", stk.get("outline", 14))
            except Exception as ex:   # no rembg here: a white-framed photo card instead
                print(f"sticker cut-out failed ({type(ex).__name__}); using a photo card")
                from PIL import Image, ImageOps
                im = Image.open(s_src).convert("RGB"); im.thumbnail((900, 900)); ImageOps.expand(im, 22, "#ffffff").save(f"{out}/{i}s.png")
            b["_sticker"] = True
    open(OUT + "/CREDITS.txt", "w").write("مصادر الصور والفيديوهات وتراخيصها:\n" + "\n".join(credits) + "\n")
    print("media candidates: look at", cand, "(beatN.jpg: numbered PHOTO/VIDEO + source; items used in earlier scenes are removed), then set \"pick\": number")

images()
run(STYLE, B, scene, css=CSS, bg="#000", bed="drone", rate="+3%",
    extra_sfx=lambda sch: sum(([{"file": "sfx/hit.wav", "at": round(sch[k][0] + .9, 2), "gain": .35}, {"file": "sfx/riser.wav", "at": round(sch[k][0] - .2, 2), "gain": .15}] for k, b in enumerate(B) if b.get("flash")), []))
