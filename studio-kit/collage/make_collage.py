"""Vox-style CUT-OUT COLLAGE builder: one json -> narrated vertical video + cover.
  python3 make_collage.py video.json OUTDIR [--preview]
Photos are cut out automatically (cutout.py: rembg) into paper stickers, or used as torn photo cards with tape.
Every item pops / drops / slides in, «boils» like stop-motion paper, and scenes change with a paper-tear wipe.
Json format: README.md in this folder, example: examples/gold.json. Needs python3 (rembg, pillow, numpy), ffmpeg, node>=22."""
import json, math, os, re, shutil, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); KIT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(KIT, "scripts"))
import cutout

PAPER = {"cream": "#efe6d2", "kraft": "#c9a77a", "dark": "#1d1f24", "blue": "#24456b", "red": "#a8322e", "white": "#f6f4ee", "green": "#2f5a46", "yellow": "#f2c94c",
         "pink": "#f3c6cf", "mint": "#cfeadb", "sky": "#bcdcf0", "lilac": "#d9cdf0", "orange": "#e8913a", "teal": "#1f5f63", "navy": "#14213d", "purple": "#4a2a6a", "olive": "#6b6b3a", "sand": "#e3cfa4", "grey": "#9a9a9a", "black": "#0e0e10", "newspaper": "#e9e4d8", "brown": "#5a3a22"}
DARK_BG = {"dark", "blue", "red", "green", "teal", "navy", "purple", "olive", "black", "brown", "orange"}
W, H = 1080, 1920

def sh(cmd, **kw): return subprocess.run(cmd, check=True, **kw)
def dur(p): return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]))
def rnd(seed):  # deterministic pseudo-random in [-1, 1]
    x = math.sin(seed * 12.9898 + 78.233) * 43758.5453
    return (x - math.floor(x)) * 2 - 1
def markup(s, marker="#ffd21f"):
    s = s.replace("\n", "<br/>")
    s = re.sub(r"\[y\](.*?)\[/y\]", r'<span class="mk">\1</span>', s)
    s = re.sub(r"\[r\](.*?)\[/r\]", r'<span class="rd">\1</span>', s)
    return s

def torn(w, h, seed, jag=10, step=26):
    """jagged rectangle path centred on 0,0 (torn paper)."""
    pts = []
    for side in range(4):
        n = int((w if side % 2 == 0 else h) / step)
        for k in range(n):
            t = k / n
            if side == 0: x, y = -w/2 + w*t, -h/2
            elif side == 1: x, y = w/2, -h/2 + h*t
            elif side == 2: x, y = w/2 - w*t, h/2
            else: x, y = -w/2, h/2 - h*t
            j = rnd(seed + side * 101 + k) * jag
            if side % 2 == 0: y += j
            else: x += j
            pts.append(f"{x:.1f},{y:.1f}")
    return "M" + " L".join(pts) + " Z"

# ------------------------------------------------------------------ assets / voice / timing
USED, USED_FILES = set(), set()
def check_repeats(ep):
    """no repetition ever: each asset may appear in ONE item of ONE scene only."""
    seen = {}
    for i, b in enumerate(ep["beats"]):
        for it in b.get("items", []):
            for a in ([it["asset"]] if it.get("asset") else []) + list(it.get("assets", [])):
                if a in seen and not ep.get("allow_repeat"): sys.exit(f"REPEATED MEDIA: asset «{a}» is used in scene {seen[a]} and again in scene {i+1}. Use a different photo/video for every appearance.")
                seen[a] = i + 1
def prepare_assets(ep, P):
    A = {}; ad = os.path.join(P, "assets"); os.makedirs(ad, exist_ok=True)
    for name, a in ep.get("assets", {}).items():
        if a.get("video_query") or a.get("video"):   # moving footage card (Pixabay videos): candidates/<name>.jpg, choose with "pick"
            sys.path.insert(0, os.path.join(KIT, "scripts")); import images as IM
            vs = a.get("video")
            if vs: vs = vs if os.path.isabs(vs) else os.path.join(ep["_dir"], vs)
            else:
                cd = os.path.join(os.path.dirname(P), "candidates", name); meta = os.path.join(cd, "credits.json")
                if os.path.exists(meta): res = json.load(open(meta))
                else:
                    res = IM.fetch_videos(a["video_query"], cd, 6); json.dump(res, open(meta, "w"), ensure_ascii=False)
                    IM.sheet([r["thumb"] for r in res], os.path.join(os.path.dirname(P), "candidates", name + ".jpg"))
                r = res[max(1, min(int(a.get("pick", 1)), len(res))) - 1]; vs = r["file"]
                open(os.path.join(os.path.dirname(P), "CREDITS.txt"), "a").write(f"{name} (فيديو): {r['title'][:60]} — {r['author']} — {r['license']} — {r['page']}\n")
            out = os.path.join(ad, name + ".mp4")
            if not os.path.exists(out):
                subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-stream_loop", "-1", "-ss", str(a.get("start", 1)), "-i", vs, "-t", str(a.get("dur", 12)), "-an",
                                "-vf", "scale=960:720:force_original_aspect_ratio=increase,crop=960:720,fps=30", "-c:v", "libx264", "-preset", "fast", "-crf", "21", "-pix_fmt", "yuv420p", out], check=True)
            A[name] = dict(file="assets/" + name + ".mp4", size=(960, 720), cut=False, video=True); continue
        if "query" in a and not a.get("src"):   # candidates sheet OUT/candidates/<name>.jpg: PHOTO/VIDEO + source, choose with "pick"
            sys.path.insert(0, os.path.join(KIT, "scripts")); import images as IM
            cd = os.path.join(os.path.dirname(P), "candidates", name); os.makedirs(cd, exist_ok=True); meta = os.path.join(cd, "credits.json")
            if os.path.exists(meta): res = json.load(open(meta))
            else:
                res = IM.fetch_mixed(a["query"], cd, n_vid=0, photos=a.get("source", ep.get("source", "auto")))
                json.dump(res, open(meta, "w"), ensure_ascii=False)
            fresh = [r for r in res if (r.get("page") or r["file"]) not in USED]
            if not fresh: sys.exit(f"NO NEW MEDIA for asset «{name}»: every candidate is already used by another asset. Change its query.")
            try: IM.mixed_sheet(fresh, os.path.join(os.path.dirname(P), "candidates", name + ".jpg"))
            except Exception as e: print("  (candidate sheet skipped:", type(e).__name__, ")")
            r = fresh[max(1, min(int(a.get("pick", 1)), len(fresh))) - 1]; USED.add(r.get("page") or r["file"])
            open(os.path.join(os.path.dirname(P), "CREDITS.txt"), "a").write(f"{name} ({'فيديو' if r['kind'] == 'video' else 'صورة'}): {r['title'][:60]} — {r['author']} — {r['license']} — {r['page']}\n")
            if r["kind"] == "video": a = dict(a, video=r["file"]); a.pop("query", None)
            else: a = dict(a, src=r["file"])
        if a.get("video") and not a.get("video_query"):
            vs = a["video"] if os.path.isabs(a["video"]) else os.path.join(ep["_dir"], a["video"]); out = os.path.join(ad, name + ".mp4")
            if not os.path.exists(out):
                subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-stream_loop", "-1", "-ss", str(a.get("start", 1)), "-i", vs, "-t", str(a.get("dur", 12)), "-an",
                                "-vf", "scale=960:720:force_original_aspect_ratio=increase,crop=960:720,fps=30", "-c:v", "libx264", "-preset", "fast", "-crf", "21", "-pix_fmt", "yuv420p", out], check=True)
            A[name] = dict(file="assets/" + name + ".mp4", size=(960, 720), cut=False, video=True); continue
        if a.get("src"):
            k_ = os.path.abspath(a["src"] if os.path.isabs(a["src"]) else os.path.join(ep["_dir"], a["src"]))
            if k_ in USED_FILES: sys.exit(f"REPEATED MEDIA: asset «{name}» uses the same file as another asset. Every photo must be different.")
            USED_FILES.add(k_)
        src = a["src"] if os.path.isabs(a["src"]) else os.path.join(ep["_dir"], a["src"])
        if a.get("cut"):
            out = os.path.join(ad, name + ".png")
            if not os.path.exists(out): cutout.sticker(src, out, a.get("outline", 14))
        else:
            out = os.path.join(ad, name + ".jpg")
            if not os.path.exists(out): cutout.card(src, out, vintage=a.get("vintage", False))
        from PIL import Image
        A[name] = dict(file="assets/" + os.path.basename(out), size=Image.open(out).size, cut=bool(a.get("cut")))
    return A

def voice(ep, P):
    vd = os.path.join(P, "voice"); os.makedirs(vd, exist_ok=True); v = ep.get("voice", {})
    lines = [{"id": f"b{i}", "text": b["line"]} for i, b in enumerate(ep["beats"])]
    json.dump(lines, open(os.path.join(P, "lines.json"), "w"), ensure_ascii=False)
    vf = ep.get("voice_files")   # a folder with b0.mp3/b0.wav ... made by another TTS (works when edge-tts is blocked)
    if vf:
        vf = vf if os.path.isabs(vf) else os.path.join(ep["_dir"], vf)
        for i in range(len(lines)):
            src = next((os.path.join(vf, f"b{i}.{x}") for x in ("wav", "mp3", "flac", "ogg", "m4a") if os.path.exists(os.path.join(vf, f"b{i}.{x}"))), None)
            if not src: sys.exit(f"voice_files: missing b{i}.wav (or .mp3) in {vf}")
            sh(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-ac", "1", "-ar", "48000", os.path.join(vd, f"b{i}.wav")])
    else:
        sh([sys.executable, os.path.join(KIT, "scripts", "tts_edge.py"), os.path.join(P, "lines.json"), vd, "--voice", v.get("name", "ar-SA-HamedNeural"), f"--rate={v.get('rate', '+0%')}"], stdout=subprocess.DEVNULL)
    return [dur(os.path.join(vd, f"b{i}.wav")) for i in range(len(lines))]

def schedule(ep, durs):
    t, out = 0.35, []
    for d in durs:
        out.append([round(t, 2), round(t + d, 2)]); t += d + ep.get("gap", 0.45)
    MIN = float(ep.get("min_duration", 50)); D = round(out[-1][1] + 1.3, 2)   # length follows the narration, never under MIN (default 50 s)
    if D < MIN and "--preview" not in sys.argv:
        words = sum(len(b["line"].split()) for b in ep["beats"]); add = int(words * (MIN / D - 1)) + 3
        sys.exit(f"TOO SHORT: the narration lasts {D:.1f} s but every video must be at least {MIN:.0f} s. Explain the topic more: add about {add} words. Video not rendered.")
    if D > float(ep.get("max_duration", 180)): sys.exit(f"TOO LONG: {D:.1f} s; Shorts/Reels allow at most {ep.get('max_duration', 180)} s. Shorten the lines.")
    for i in range(len(out)): out[i].append(round(out[i+1][0] - 0.05, 2) if i + 1 < len(out) else D)
    return out, D

# ------------------------------------------------------------------ items
import motions as M
SIZES = {"hero": .62, "main": .45, "small": .32, "icon": .13}   # share of the frame width

def fit(it, w0, h0, dflt_h):
    if it.get("size") in SIZES:
        ww = W * SIZES[it["size"]]; hh = h0 * ww / w0
        if hh > 1150: hh = 1150; ww = w0 * hh / h0
        return ww, hh
    hh = it.get("h", dflt_h); ww = w0 * hh / h0
    if "w" in it: ww = it["w"]; hh = h0 * ww / w0 if "h" not in it else it["h"]
    return ww, hh

def content(it, A, iid, seed):
    """the drawn item around 0,0 -> (svg, w, h)."""
    k = it["type"]
    if k == "cutout":
        a = A[it["asset"]]; ww, hh = fit(it, *a["size"], 800)
        return f'<image href="{a["file"]}" x="{-ww/2:.0f}" y="{-hh/2:.0f}" width="{ww:.0f}" height="{hh:.0f}" filter="url(#shd)"/>', ww, hh
    if k == "photo":
        a = A[it["asset"]]; w0, h0 = a["size"]
        ww = W * SIZES[it["size"]] if it.get("size") in SIZES else it.get("w", 760); hh = it.get("h", h0 * ww / w0)
        inner, outer = torn(ww, hh, seed, 8), torn(ww + 40, hh + 40, seed + 7, 12)
        tp = M.tape(ww, hh, seed) if it.get("tape", True) else ""
        return (f'<path d="{outer}" fill="#fbf8f0" filter="url(#shd)"/><clipPath id="ph{iid}"><path d="{inner}"/></clipPath>'
                f'<image href="{a["file"]}" x="{-ww/2:.0f}" y="{-hh/2:.0f}" width="{ww:.0f}" height="{hh:.0f}" preserveAspectRatio="xMidYMid slice" clip-path="url(#ph{iid})"/><path d="{inner}" fill="url(#ht)"/>{tp}'), ww, hh
    if k == "montage":   # 73 fast cuts between photos
        ww = W * SIZES.get(it.get("size", "main"), .45) if "w" not in it else it["w"]; hh = it.get("h", ww * 1.25)
        imgs = "".join(f'<image class="mt" href="{A[n]["file"]}" x="{-ww/2:.0f}" y="{-hh/2:.0f}" width="{ww:.0f}" height="{hh:.0f}" preserveAspectRatio="xMidYMid slice" opacity="{1 if j==0 else 0}"/>' for j, n in enumerate(it["assets"]))
        return f'<rect x="{-ww/2-18:.0f}" y="{-hh/2-18:.0f}" width="{ww+36:.0f}" height="{hh+36:.0f}" fill="#fbf8f0" filter="url(#shd)"/>{imgs}', ww, hh
    if k == "pin":
        return M.pin_svg() + '<path d="M0,22 V64" stroke="#111" stroke-width="5"/>', 44, 44
    return "", 0, 0

VIDS = []; CUR = {}
def video_card(it, A, bid, k, s, js):
    """moving footage inside a torn paper card: the paper is drawn in the scene, the <video> sits above it (clip-path = torn edge)."""
    iid = f"i{bid}_{k}"; x, y = it.get("x", 540), it.get("y", 960); ww = W * SIZES[it["size"]] if it.get("size") in SIZES else it.get("w", 700); hh = ww * .75
    at = s + it.get("at", 0.15 + 0.4 * k); seed = bid * 13 + k; tilt = it.get("tilt", rnd(bid * 31 + k) * 3)
    outer = torn(ww + 44, hh + 44, seed + 7, 12)
    pts = []
    for side in range(4):
        n = int((ww if side % 2 == 0 else hh) / 26)
        for q in range(n):
            t = q / n; px, py = [(ww*t, 0), (ww, hh*t), (ww - ww*t, hh), (0, hh - hh*t)][side]; j = rnd(seed + side * 101 + q) * 8
            if side % 2 == 0: py += j
            else: px += j
            pts.append(f"{px/ww*100:.1f}% {py/hh*100:.1f}%")
    t0, t1 = CUR["c0"], CUR["c1"]
    VIDS.append(f'<video id="vv{iid}" src="{A[it["asset"]]["file"]}" data-start="{max(t0, at-.05):.2f}" data-duration="{t1-max(t0, at-.05):.2f}" data-track-index="{5 + k}" muted playsinline '
                f'style="position:absolute;left:{x-ww/2:.0f}px;top:{y-hh/2:.0f}px;width:{ww:.0f}px;height:{hh:.0f}px;object-fit:cover;clip-path:polygon({",".join(pts)});opacity:0"></video>')
    js.append(f'tl.fromTo("#vv{iid}",{{opacity:0,scale:.2,rotation:{tilt-25:.1f}}},{{opacity:1,scale:1,rotation:{tilt:.1f},duration:.5,ease:"back.out(1.6)"}},{at:.2f});')
    js.append(f'tl.fromTo("#pv{iid}",{{attr:{{transform:"translate({x} {y}) rotate({tilt-25:.1f}) scale(0.2)"}},opacity:0}},{{attr:{{transform:"translate({x} {y}) rotate({tilt:.1f}) scale(1)"}},opacity:1,duration:.5,ease:"back.out(1.6)"}},{at:.2f});')
    tp = "".join(f'<rect x="{cx-70}" y="{-hh/2-34}" width="140" height="46" fill="#f4e8b0" fill-opacity=".85" transform="rotate({r} {cx} {-hh/2-11})"/>' for cx, r in ((-ww/2+60, -18), (ww/2-60, 14))) if it.get("tape", True) else ""
    return f'<g id="pv{iid}" transform="translate({x} {y}) rotate({tilt:.1f}) scale(1)" opacity="0"><path d="{outer}" fill="#fbf8f0" filter="url(#shd)"/>{tp}</g>'
def item_svg(it, A, bid, k, bg_dark, s, js):
    """svg item: translate(x y) > #iid (enter/exit) > #iidL (loop) > effect(content). appends its js."""
    if it["type"] == "video" or (it.get("asset") in A and A[it["asset"]].get("video") and it["type"] in ("photo", "cutout")): return video_card(it, A, bid, k, s, js)
    kind = it["type"]; iid = f"i{bid}_{k}"; x, y = it.get("x", 540), it.get("y", 960); seed = bid * 13 + k
    at = s + it.get("at", 0.15 + 0.4 * k)
    if kind in ("circle", "arrow", "underline"):   # 52 53 54 hand-drawn marks (absolute coords)
        js.append(f'tl.to("#{iid} .draw",{{strokeDashoffset:0,duration:.55,ease:"power2.inOut",stagger:.08}},{at:.2f});')
        if kind == "arrow": js.append(f'tl.to("#{iid} .head",{{opacity:1,duration:.1}},{at+0.5:.2f});')
        return old_mark(it, iid, x, y, bg_dark)
    if kind in ("map", "timeline", "chart", "clock", "calendar", "check", "cross", "strike", "string"):
        body, ij, w, h = M.info_item(it, iid, at, seed); js += ij
        tilt = it.get("tilt", 0)
    else:
        body, w, h = content(it, A, iid, seed); tilt = it.get("tilt", rnd(bid * 31 + k) * 4 if kind != "pin" else 0)
        if kind == "montage":
            n = len(it["assets"]); per = it.get("every", .3)
            js.append(f'for(let t={at+.3:.2f},j=1;t<{s+it.get("until",6):.2f};t+={per},j++){{const q=j%{n};tl.set("#{iid} .mt",{{opacity:0}},t);tl.set(document.querySelectorAll("#{iid} .mt")[q],{{opacity:1}},t);}}')
    if it.get("effect"):
        body, ej = M.effect(it["effect"], iid, body, w, h, s + it.get("effect_at", it.get("at", .15 + .4 * k) + 1.0), it.get("fx", {}), seed); js += ej
    en = it.get("enter", "pop" if kind == "cutout" else "drop")
    extra = ""
    if en == "pin":   # 22 dropped, then a pin is pushed in
        extra = f'<g id="P{iid}" transform="translate(0 {-h/2+20:.0f}) scale(0)">{M.pin_svg()}</g>'
        js.append(f'tl.to("#P{iid}",{{attr:{{transform:"translate(0 {-h/2+20:.0f}) scale(1)"}},duration:.25,ease:"back.out(3)"}},{at+.5:.2f});'); en = "drop"
    if en == "tape":  # 21 laid down, tape slapped on
        js.append(f'tl.fromTo("#{iid} .tp",{{opacity:0}},{{opacity:1,duration:.08,stagger:.18}},{at+.4:.2f});'); en = "pop"
    js += M.enter(en, f"#{iid}", at, tilt, it)
    if it.get("loop"):
        js += M.loop(it["loop"], f"#{iid}L", at + .9, s + it.get("until", 8), seed, it)
    if it.get("exit"):
        js += M.exit_(it["exit"], f"#{iid}", s + it["exit_at"], tilt)
    return (f'<g transform="translate({x} {y})"><g id="{iid}" transform="{M.T(0,0,tilt)}"><g id="{iid}L" transform="{M.T()}">{body}</g>{extra}</g></g>')

def old_mark(it, iid, x, y, bg_dark):
    kind = it["type"]
    if kind == "circle":
        r = it.get("r", 150); rx, ry = r * it.get("sx", 1.15), r
        p1 = f"M{x+rx},{y} A{rx},{ry} 0 1,1 {x+rx-1},{y-6}"; p2 = f"M{x+rx-10},{y+12} A{rx+8},{ry-6} 0 1,1 {x+rx},{y-14}"
        L = int(6.4 * rx)
        return f'<g id="{iid}"><path class="draw" d="{p1}" fill="none" stroke="{it.get("color", "#e5322d")}" stroke-width="11" stroke-linecap="round" stroke-dasharray="{L}" stroke-dashoffset="{L}"/><path class="draw" d="{p2}" fill="none" stroke="{it.get("color", "#e5322d")}" stroke-width="6" stroke-linecap="round" stroke-dasharray="{L}" stroke-dashoffset="{L}" opacity=".7"/></g>'
    if kind == "arrow":
        (x1, y1), (x2, y2) = it["from"], it["to"]; cx_, cy_ = (x1 + x2) / 2 + (y2 - y1) * 0.25, (y1 + y2) / 2 - (x2 - x1) * 0.25
        L = int(math.hypot(x2 - x1, y2 - y1) * 1.3); ang = math.atan2(y2 - cy_, x2 - cx_)
        hx1, hy1 = x2 - 46 * math.cos(ang - 0.45), y2 - 46 * math.sin(ang - 0.45); hx2, hy2 = x2 - 46 * math.cos(ang + 0.45), y2 - 46 * math.sin(ang + 0.45)
        col = it.get("color", "#111" if not bg_dark else "#fbf8f0")
        return f'<g id="{iid}"><path class="draw" d="M{x1},{y1} Q{cx_:.0f},{cy_:.0f} {x2},{y2}" fill="none" stroke="{col}" stroke-width="10" stroke-linecap="round" stroke-dasharray="{L}" stroke-dashoffset="{L}"/><path class="head" d="M{hx1:.0f},{hy1:.0f} L{x2},{y2} L{hx2:.0f},{hy2:.0f}" fill="none" stroke="{col}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" opacity="0"/></g>'
    w = it.get("w", 400); pts = " ".join(f"{x-w/2+j*w/12:.0f},{y+(8 if j%2 else -8)}" for j in range(13))
    return f'<g id="{iid}"><polyline class="draw" points="{pts}" fill="none" stroke="{it.get("color", "#e5322d")}" stroke-width="9" stroke-linecap="round" stroke-dasharray="{w*1.6:.0f}" stroke-dashoffset="{w*1.6:.0f}"/></g>'

def item_html(it, bid, k, bg_dark, s, js):
    """text items are HTML (crisp Arabic). enter: pop | slam (11 stamp) | type (67 typewriter) | stick (59 sticky note) | slide."""
    iid = f"i{bid}_{k}"; x, y = it.get("x", 540), it.get("y", 300); st = it.get("style", "big"); size = it.get("size", 104)
    at = s + it.get("at", 0.15 + 0.4 * k); fg = "#fbf8f0" if bg_dark else "#151515"
    en = it.get("enter", {"stamp": "slam", "note": "stick"}.get(st, "pop"))
    txt = markup(it["text"])
    if en == "type":
        parts = re.split(r"(<[^>]+>)", txt); out = []
        for p_ in parts:
            out.append(p_ if p_.startswith("<") else re.sub(r"(\S+)", r'<span class="wd" style="opacity:0">\1</span>', p_))
        txt = "".join(out)
    css = f"position:absolute;left:{x-470}px;width:940px;top:{y-size}px;text-align:center;font-weight:900;font-size:{size}px;line-height:1.25;opacity:0;"
    if st == "label":   body = f'<span style="background:#151515;color:#fbf8f0;padding:4px 28px 14px;box-shadow:8px 8px 0 #e5322d">{txt}</span>'; css += ""
    elif st == "stamp": body = f'<span style="display:inline-block;border:12px solid #e5322d;padding:0 30px 14px;border-radius:14px;transform:rotate(-8deg)">{txt}</span>'; css += "color:#e5322d;"
    elif st == "note":  body = f'<span style="display:inline-block;background:#f7e27a;color:#151515;padding:26px 34px 34px;box-shadow:0 18px 30px #0006;transform:rotate(-3deg);font-size:{int(size*0.75)}px">{txt}</span>'
    elif st == "typed": body = f'<span style="display:inline-block;background:#fbf8f0;color:#151515;padding:18px 30px;font-family:monospace,Cairo;font-size:{int(size*.7)}px;box-shadow:0 12px 24px #0005">{txt}</span>'
    else: body = txt; css += f"color:{fg};"
    sel = f"#{iid}"
    if en == "slam":
        js.append(f'tl.fromTo("{sel}",{{opacity:0,scale:3.2}},{{opacity:1,scale:1,duration:.22,ease:"power4.in"}},{at:.2f});')
        js += M.camera("shake", f"#K{bid}", None, at + .22)
    elif en == "stick":
        js.append(f'tl.fromTo("{sel}",{{opacity:0,rotation:-25,x:300,y:-200,scale:.6}},{{opacity:1,rotation:0,x:0,y:0,scale:1,duration:.5,ease:"back.out(1.6)"}},{at:.2f});')
    elif en == "type":
        js.append(f'tl.set("{sel}",{{opacity:1}},{at:.2f});tl.to("{sel} .wd",{{opacity:1,duration:.01,stagger:{it.get("speed",.16)}}},{at:.2f});')
    elif en == "slide":
        js.append(f'tl.fromTo("{sel}",{{opacity:0,x:-900}},{{opacity:1,x:0,duration:.45,ease:"power3.out"}},{at:.2f});')
    else:
        js.append(f'tl.fromTo("{sel}",{{opacity:0,y:40,scale:1.15}},{{opacity:1,y:0,scale:1,duration:.35,ease:"back.out(2)"}},{at:.2f});')
    js.append(f'tl.fromTo("{sel} .mk",{{backgroundSize:"0% 42%"}},{{backgroundSize:"100% 42%",duration:.4,ease:"power2.out"}},{at+0.4:.2f});')   # 56 marker
    if it.get("exit"): js.append(f'tl.to("{sel}",{{opacity:0,duration:.3}},{s+it["exit_at"]:.2f});')
    return f'<div id="{iid}" style="{css}">{body}</div>'

# ------------------------------------------------------------------ html
def build(ep, A, sch, D, P):
    beats = ep["beats"]; clips, js = [], ['const tl=gsap.timeline({paused:true});']; overlays = []
    for i, b in enumerate(beats):
        s, e, w = sch[i]; c0 = 0 if i == 0 else s - 1.0; c1 = sch[i+1][0] + 0.5 if i + 1 < len(beats) else D
        CUR.update(c0=c0, c1=min(c1, sch[i+1][0] + .3) if i + 1 < len(beats) else D)
        bg = b.get("bg", ep.get("paper", "cream")); dark = bg in DARK_BG; col = PAPER.get(bg, bg)
        svg_items, html_items = [], []
        for k, it in enumerate(b.get("items", [])):
            if it["type"] == "text": html_items.append(item_html(it, i, k, dark, s, js))
            else: svg_items.append(item_svg(it, A, i, k, dark, s, js))
        css = ""
        if i > 0:
            kind = b.get("transition", M.TRANSITIONS[(i - 1) % len(M.TRANSITIONS)])
            css, tj, ov = M.transition(kind, f"#B{i}", f"#K{i-1}", s, col, *b.get("transition_at", [540, 900])); js += tj
            if ov and ov.split('"')[1] not in "".join(overlays): overlays.append(ov)
        halftone = '<rect width="1080" height="1920" fill="url(#ht)"/>' if b.get("halftone", ep.get("halftone", True)) else ""
        clips.append(f'<div id="B{i}" class="clip" style="--paper:{col};{css}" data-start="{c0:.2f}" data-duration="{c1-c0:.2f}" data-track-index="{1 + i % 2}"><div id="K{i}" class="cam">'
                     f'<svg class="full" width="1080" height="1920" viewBox="0 0 1080 1920"><rect width="1080" height="1920" fill="{col}"/><rect width="1080" height="1920" filter="url(#grain)" opacity="{".5" if dark else "1"}"/>{halftone}'
                     f'<g id="cam{i}">{"".join(svg_items)}</g></svg>{"".join(html_items)}</div></div>')
        js.append(f'tl.fromTo("#cam{i}",{{scale:1}},{{scale:{b.get("zoom", 1.06)},duration:{c1-c0:.2f},ease:"none",transformOrigin:"50% 50%"}},{c0:.2f});')
        for cm in b.get("camera", []):   # 68-72
            cm = {"kind": cm} if isinstance(cm, str) else cm
            js += M.camera(cm["kind"], f"#K{i}", None, s + cm.get("at", .5), cm)
    js.append(f'tl.to({{}},{{duration:.01}},{D-0.01});window.__timelines=window.__timelines||{{}};window.__timelines["c"]=tl;')
    wipe = torn(1300, 2100, 999, 30, 40); sheet = torn(1240, 2080, 555, 26, 40)
    html = f'''<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><title>{ep.get("title","collage")}</title><style>
@font-face{{font-family:"Cairo";src:url("fonts/cairo-ar.woff2") format("woff2");font-weight:200 1000;font-display:block;unicode-range:U+0600-06FF,U+0750-077F,U+FB50-FDFF,U+FE70-FEFC,U+200C-200E;}}
@font-face{{font-family:"Cairo";src:url("fonts/cairo-latin.woff2") format("woff2");font-weight:200 1000;font-display:block;}}
html,body{{margin:0;background:#111}}#root{{position:relative;width:1080px;height:1920px;overflow:hidden;font-family:"Cairo",sans-serif;direction:rtl}}
.clip{{position:absolute;inset:0;overflow:hidden}}.cam{{position:absolute;inset:0}}svg.full{{position:absolute;inset:0}}
.mk{{background:linear-gradient(#ffd21f,#ffd21f) no-repeat 100% 88%/0% 42%;padding:0 8px;color:inherit}}.rd{{color:#e5322d}}
#flash{{position:absolute;inset:0;background:#fff}}#spot{{position:absolute;inset:0;background:#000c;--sx:540px;--sy:900px;-webkit-mask-image:radial-gradient(circle 300px at var(--sx) var(--sy),transparent 92%,#000 100%);mask-image:radial-gradient(circle 300px at var(--sx) var(--sy),transparent 92%,#000 100%)}}
</style><script src="gsap.min.js"></script></head><body>
<div id="root" data-composition-id="c" data-start="0" data-duration="{D}" data-width="1080" data-height="1920">
<svg width="0" height="0" style="position:absolute"><defs>
<filter id="grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="2" seed="4"/><feColorMatrix type="saturate" values="0"/><feComponentTransfer><feFuncA type="table" tableValues="0 .10"/></feComponentTransfer></filter>
<pattern id="ht" width="12" height="12" patternUnits="userSpaceOnUse"><circle cx="6" cy="6" r="1.6" fill="#000" opacity=".09"/></pattern>
<filter id="glow" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="14"/></filter>
<linearGradient id="rollgrad" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity=".1"/><stop offset=".5" stop-color="#fff" stop-opacity=".4"/><stop offset="1" stop-color="#000" stop-opacity=".5"/></linearGradient>
<filter id="shd" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="10" dy="16" stdDeviation="7" flood-opacity=".42"/></filter></defs></svg>
{"".join(clips)}{"".join(VIDS)}
<div id="W" class="clip" data-start="0" data-duration="{D}" data-track-index="3"><svg class="full" width="1080" height="1920" viewBox="0 0 1080 1920">{"".join(overlays)}<g id="sheetfall" transform="translate(0 -2100) rotate(0 540 960)"><g transform="translate(540 960)"><path d="{sheet}" fill="#efe6d2" filter="url(#shd)"/></g></g><g id="wipe" transform="translate(1250 0)"><g transform="translate(650 960)"><path d="{wipe}" fill="#efe6d2" filter="url(#shd)"/></g></g></svg>
<div id="spot" style="opacity:0"></div><div id="flash" style="opacity:0"></div></div>
</div><script>gsap.set("#flash,#spot",{{opacity:0}});{"".join(js)}</script></body></html>'''
    open(os.path.join(P, "index.html"), "w").write(html)

# ------------------------------------------------------------------ sound
def sound(ep, sch, D, P):
    import numpy as np
    sys.path.insert(0, os.path.join(KIT, "scripts")); import sfx_lib as S
    sd = os.path.join(P, "sfx"); os.makedirs(sd, exist_ok=True)
    S.save(os.path.join(sd, "whoosh.wav"), S.whoosh(0.35)); S.save(os.path.join(sd, "pop.wav"), S.hit(0.18)); S.save(os.path.join(sd, "scr.wav"), S.whoosh(0.5) * 0.5)
    rng = np.random.default_rng(7); sr = 48000
    def noise(d, lo, hi, gr=None):
        n = rng.standard_normal(int(sr * d)); n = S.lp(n, lo) - S.lp(n, hi) if hi else S.lp(n, lo)
        env = np.ones_like(n) if gr is None else (rng.random(len(n) // 400 + 1) > gr).repeat(400)[:len(n)] * 1.0
        return S.norm(n * env * np.linspace(1, .2, len(n)), .6)
    S.save(os.path.join(sd, "rip.wav"), noise(.45, .5, .05, .35)); S.save(os.path.join(sd, "crum.wav"), noise(.8, .4, .03, .6))
    S.save(os.path.join(sd, "snip.wav"), noise(.12, .7, .2)); S.save(os.path.join(sd, "thud.wav"), S.hit(0.4))
    notes = [220.0, 261.63, 293.66, 329.63, 392.0]
    for n, f in enumerate(notes): S.save(os.path.join(sd, f"n{n}.wav"), S.pluck(f, 1.2))
    it = [{"file": f"voice/b{i}.wav", "at": sch[i][0]} for i in range(len(sch))]
    t, k = 0.2, 0
    while t < D - 1:  # light pizzicato bed
        it.append({"file": f"sfx/n{[0,2,4,2,1,3,4,3][k%8]}.wav", "at": round(t, 2), "gain": 0.07}); t += 0.5; k += 1
    for i, b in enumerate(ep["beats"]):
        s = sch[i][0]
        if i: it.append({"file": "sfx/whoosh.wav", "at": round(s - 0.45, 2), "gain": 0.22})
        for k2, x in enumerate(b.get("items", [])):
            at = s + x.get("at", 0.15 + 0.4 * k2)
            if x["type"] in ("circle", "arrow", "underline", "strike", "check", "cross", "string"): it.append({"file": "sfx/scr.wav", "at": round(at, 2), "gain": 0.1})
            elif x.get("enter") in ("left", "right", "top", "bottom", "slide", "toss", "spin", "string"): it.append({"file": "sfx/whoosh.wav", "at": round(at, 2), "gain": 0.15})
            elif x.get("enter") == "slam" or x.get("style") == "stamp": it.append({"file": "sfx/thud.wav", "at": round(at + .22, 2), "gain": 0.3})
            elif x["type"] != "text": it.append({"file": "sfx/pop.wav", "at": round(at, 2), "gain": 0.16})
            if x.get("effect"):
                ea = s + x.get("effect_at", x.get("at", 0.15 + 0.4 * k2) + 1.0)
                f = {"tear": "rip", "strip": "rip", "shred_out": "rip", "shatter": "rip", "hole": "rip", "shredder": "rip", "crumple": "crum", "uncrumple": "crum", "scissors": "snip"}.get(x["effect"], "scr")
                it.append({"file": f"sfx/{f}.wav", "at": round(ea, 2), "gain": 0.22})
        for cm in b.get("camera", []):
            cm = {"kind": cm} if isinstance(cm, str) else cm
            if cm["kind"] in ("flash", "shake", "snap_zoom"): it.append({"file": "sfx/thud.wav" if cm["kind"] != "flash" else "sfx/pop.wav", "at": round(s + cm.get("at", .5), 2), "gain": 0.25})
    json.dump({"duration": D, "target_lufs": -14, "items": it}, open(os.path.join(P, "mix.json"), "w"))
    os.makedirs(os.path.join(P, "out"), exist_ok=True)
    sh([sys.executable, os.path.join(KIT, "scripts", "mix.py"), "mix.json", "out/mix.wav"], cwd=P, stdout=subprocess.DEVNULL)

# ------------------------------------------------------------------ cover
def cover(ep, A, P, OUT):
    c = ep.get("cover", {}); bg = c.get("bg", ep.get("paper", "cream")); dark = bg in DARK_BG
    T = os.path.join(P, "cover"); os.makedirs(T, exist_ok=True)
    for f in ("gsap.min.js",): shutil.copy(os.path.join(P, f), T)
    shutil.copytree(os.path.join(P, "fonts"), os.path.join(T, "fonts"), dirs_exist_ok=True); shutil.copytree(os.path.join(P, "assets"), os.path.join(T, "assets"), dirs_exist_ok=True)
    hero = ""
    if c.get("asset"):
        a = A[c["asset"]]; w0, h0 = a["size"]; hh = 540; ww = w0 * hh / h0
        if ww > 780: ww = 780; hh = h0 * ww / w0
        hero = f'<g transform="translate(540 1050) rotate(-3)"><image href="{a["file"]}" x="{-ww/2:.0f}" y="{-hh/2:.0f}" width="{ww:.0f}" height="{hh:.0f}" filter="url(#shd)"/></g>'
    fg = "#fbf8f0" if dark else "#151515"
    html = f'''<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><title>cover</title><style>
@font-face{{font-family:"Cairo";src:url("fonts/cairo-ar.woff2") format("woff2");font-weight:200 1000;font-display:block;unicode-range:U+0600-06FF,U+0750-077F,U+FB50-FDFF,U+FE70-FEFC,U+200C-200E;}}
html,body{{margin:0}}#root{{position:relative;width:1080px;height:1920px;overflow:hidden;font-family:"Cairo",sans-serif;direction:rtl}}.clip{{position:absolute;inset:0}}
.t{{position:absolute;left:110px;right:110px;top:470px;text-align:center;font-weight:900;font-size:{c.get("size",100)}px;line-height:1.2;color:{fg}}}
.mk{{background:linear-gradient(#ffd21f,#ffd21f) no-repeat 0 88%/100% 42%;padding:0 8px}}.rd{{color:#e5322d}}
.tag{{position:absolute;top:1330px;left:50%;transform:translateX(-50%);background:#e5322d;color:#fff;font-weight:900;font-size:56px;padding:0 34px 10px}}
</style></head><body><div id="root" data-composition-id="cv" data-start="0" data-duration="1" data-width="1080" data-height="1920"><div id="a" class="clip" data-start="0" data-duration="1" data-track-index="1">
<svg width="1080" height="1920" viewBox="0 0 1080 1920" style="position:absolute;inset:0"><defs><filter id="grain"><feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="2" seed="4"/><feColorMatrix type="saturate" values="0"/><feComponentTransfer><feFuncA type="table" tableValues="0 .10"/></feComponentTransfer></filter>
<pattern id="ht" width="12" height="12" patternUnits="userSpaceOnUse"><circle cx="6" cy="6" r="1.6" fill="#000" opacity=".09"/></pattern><filter id="shd" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="12" dy="18" stdDeviation="8" flood-opacity=".45"/></filter></defs>
<rect width="1080" height="1920" fill="{PAPER.get(bg,bg)}"/><rect width="1080" height="1920" filter="url(#grain)"/><rect width="1080" height="1920" fill="url(#ht)"/>{hero}</svg>
<div class="t">{markup(c.get("text", ep.get("title","")))}</div><div class="tag">{c.get("tag","شرح")}</div></div></div>
<script src="gsap.min.js"></script><script>const tl=gsap.timeline({{paused:true}});tl.to({{}},{{duration:1}},0);window.__timelines={{cv:tl}};</script></body></html>'''
    open(os.path.join(T, "index.html"), "w").write(html)
    shutil.rmtree(os.path.join(T, "snap"), ignore_errors=True)
    sh(["npx", "hyperframes", "snapshot", "--at", "0.5", "--no-end", "-o", "snap", "."], cwd=T, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    png = [f for f in os.listdir(os.path.join(T, "snap")) if f.startswith("frame-")][0]
    sh(["ffmpeg", "-y", "-loglevel", "error", "-i", os.path.join(T, "snap", png), "-q:v", "2", os.path.join(OUT, "cover.jpg")])

def main():
    path = os.path.abspath(sys.argv[1]); ep = json.load(open(path)); ep["_dir"] = os.path.dirname(path)
    OUT = os.path.abspath(sys.argv[2]); P = os.path.join(OUT, "project"); os.makedirs(P, exist_ok=True)
    tpl = os.path.join(KIT, "styles", "kinetic"); shutil.copy(os.path.join(tpl, "gsap.min.js"), P); shutil.copytree(os.path.join(tpl, "fonts"), os.path.join(P, "fonts"), dirs_exist_ok=True)
    check_repeats(ep)
    print("1/5 cut-outs..."); A = prepare_assets(ep, P)
    print("2/5 voice..."); durs = voice(ep, P); sch, D = schedule(ep, durs)
    print("3/5 html..."); build(ep, A, sch, D, P)
    lint = subprocess.run(["npx", "hyperframes", "lint"], cwd=P, capture_output=True, text=True).stdout
    if "✗" in lint: print(lint); sys.exit("LINT ERRORS")
    sys.path.insert(0, os.path.join(KIT, "engines")); import post
    if ep.get("qa", True):
        probs = post.qa(P, sch, D, prefix="B")
        if probs:
            print("QA PROBLEMS (fix the JSON: shorter text / smaller size / move x):\n  " + "\n  ".join(probs[:20]))
            if "--preview" not in sys.argv and "--force" not in sys.argv: sys.exit("QA FAILED: video not rendered. Fix and run again (or add --force).")
        else: print("QA OK")
    times = ",".join(f"{min(w-0.1, s+1.6):.1f}" for s, e, w in sch)
    subprocess.run(["npx", "hyperframes", "snapshot", "--at", times, "--no-end", "-o", "snaps", "."], cwd=P, capture_output=True)
    for k, f in enumerate(sorted(f for f in os.listdir(os.path.join(P, "snaps")) if f.startswith("contact"))): shutil.copy(os.path.join(P, "snaps", f), os.path.join(OUT, f"sheet{k+1}.jpg"))
    if "--preview" in sys.argv: print("preview: look at", OUT); return
    print("4/5 sound + render..."); sound(ep, sch, D, P)
    sh(["sh", os.path.join(KIT, "scripts", "render.sh"), ".", "out/mix.wav", os.path.join(OUT, "video.mp4"), "24"], cwd=P, stdout=subprocess.DEVNULL)
    print("5/5 cover..."); cover(ep, A, P, OUT)
    print("DONE", os.path.join(OUT, "video.mp4"), os.path.join(OUT, "cover.jpg"))

if __name__ == "__main__":
    main()
