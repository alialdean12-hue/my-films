"""Vox-style CUT-OUT COLLAGE builder: one json -> narrated vertical video + cover.
  python3 make_collage.py video.json OUTDIR [--preview]
Photos are cut out automatically (cutout.py: rembg) into paper stickers, or used as torn photo cards with tape.
Every item pops / drops / slides in, «boils» like stop-motion paper, and scenes change with a paper-tear wipe.
Json format: README.md in this folder, example: examples/gold.json. Needs python3 (rembg, pillow, numpy), ffmpeg, node>=22."""
import json, math, os, re, shutil, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); KIT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(KIT, "scripts"))
import cutout

PAPER = {"cream": "#efe6d2", "kraft": "#c9a77a", "dark": "#1d1f24", "blue": "#24456b", "red": "#a8322e", "white": "#f6f4ee", "green": "#2f5a46", "yellow": "#f2c94c"}
DARK_BG = {"dark", "blue", "red", "green"}
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
def prepare_assets(ep, P):
    A = {}; ad = os.path.join(P, "assets"); os.makedirs(ad, exist_ok=True)
    for name, a in ep.get("assets", {}).items():
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
    sh([sys.executable, os.path.join(KIT, "scripts", "tts_edge.py"), os.path.join(P, "lines.json"), vd, "--voice", v.get("name", "ar-SA-HamedNeural"), f"--rate={v.get('rate', '+0%')}"], stdout=subprocess.DEVNULL)
    return [dur(os.path.join(vd, f"b{i}.wav")) for i in range(len(lines))]

def schedule(ep, durs):
    t, out = 0.35, []
    for d in durs:
        out.append([round(t, 2), round(t + d, 2)]); t += d + ep.get("gap", 0.45)
    D = ep.get("duration") or round(out[-1][1] + 1.3, 2)
    if out[-1][1] > D - 0.5: sys.exit(f"TOO LONG: voice ends at {out[-1][1]:.1f}s, duration {D}s. Shorten the lines or raise duration.")
    for i in range(len(out)): out[i].append(round(out[i+1][0] - 0.05, 2) if i + 1 < len(out) else D)
    return out, D

# ------------------------------------------------------------------ items
def item_svg(it, A, bid, k, bg_dark):
    kind = it["type"]; iid = f"i{bid}_{k}"; x, y = it.get("x", 540), it.get("y", 960); tilt = it.get("tilt", rnd(bid * 31 + k) * 4)
    boil = ' class="boil"' if it.get("boil", True) else ""
    if kind == "cutout":
        a = A[it["asset"]]; w0, h0 = a["size"]; hh = it.get("h", 800); ww = w0 * hh / h0
        if "w" in it: ww = it["w"]; hh = h0 * ww / w0
        return (f'<g transform="translate({x} {y})"><g id="{iid}" data-tilt="{tilt:.1f}" transform="translate(0 0) rotate({tilt:.1f}) scale(1 1)"><g{boil}><image href="{a["file"]}" x="{-ww/2:.0f}" y="{-hh/2:.0f}" width="{ww:.0f}" height="{hh:.0f}" filter="url(#shd)"/></g></g></g>')
    if kind == "photo":
        a = A[it["asset"]]; w0, h0 = a["size"]; ww = it.get("w", 760); hh = h0 * ww / w0
        if "h" in it: hh = it["h"]
        seed = bid * 13 + k
        inner, outer = torn(ww, hh, seed, 8), torn(ww + 40, hh + 40, seed + 7, 12)
        tape = ""
        if it.get("tape", True):
            tape = "".join(f'<rect x="{cx-70}" y="{-hh/2-36}" width="140" height="46" fill="#f4e8b0" fill-opacity=".8" transform="rotate({r} {cx} {-hh/2-13})"/>' for cx, r in ((-ww/2+60, -18), (ww/2-60, 14)))
        return (f'<g transform="translate({x} {y})"><g id="{iid}" data-tilt="{tilt:.1f}" transform="translate(0 0) rotate({tilt:.1f}) scale(1 1)"><g{boil}><path d="{outer}" fill="#fbf8f0" filter="url(#shd)"/>'
                f'<clipPath id="c{iid}"><path d="{inner}"/></clipPath><image href="{a["file"]}" x="{-ww/2:.0f}" y="{-hh/2:.0f}" width="{ww:.0f}" height="{hh:.0f}" preserveAspectRatio="xMidYMid slice" clip-path="url(#c{iid})"/>'
                f'<path d="{inner}" fill="url(#ht)"/>{tape}</g></g></g>')
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
    if kind == "underline":
        w = it.get("w", 400); pts = " ".join(f"{x-w/2+j*w/12:.0f},{y+(8 if j%2 else -8)}" for j in range(13))
        return f'<g id="{iid}"><polyline class="draw" points="{pts}" fill="none" stroke="{it.get("color", "#e5322d")}" stroke-width="9" stroke-linecap="round" stroke-dasharray="{w*1.6:.0f}" stroke-dashoffset="{w*1.6:.0f}"/></g>'
    if kind == "pin":
        return f'<g transform="translate({x} {y})"><g id="{iid}" data-tilt="0" transform="translate(0 0) rotate(0) scale(1 1)"><circle r="26" fill="#e5322d" stroke="#111" stroke-width="4"/><circle cx="-8" cy="-8" r="7" fill="#fff" opacity=".6"/><path d="M0,26 V70" stroke="#111" stroke-width="5"/></g></g>'
    return ""

def item_html(it, bid, k, bg_dark):
    """text items are HTML (crisp Arabic, marker spans)."""
    iid = f"i{bid}_{k}"; x, y = it.get("x", 540), it.get("y", 300); st = it.get("style", "big"); size = it.get("size", 104)
    fg = "#fbf8f0" if bg_dark else "#151515"
    css = f"position:absolute;left:{x-470}px;width:940px;top:{y-size}px;text-align:center;font-weight:900;font-size:{size}px;line-height:1.25;opacity:0;"
    if st == "label":
        return f'<div id="{iid}" style="{css}"><span style="background:#151515;color:#fbf8f0;padding:4px 28px 14px;box-shadow:8px 8px 0 #e5322d">{markup(it["text"])}</span></div>'
    if st == "stamp":
        return f'<div id="{iid}" style="{css}color:#e5322d;transform:rotate(-8deg)"><span style="border:12px solid #e5322d;padding:0 30px 14px;border-radius:14px">{markup(it["text"])}</span></div>'
    if st == "note":
        return f'<div id="{iid}" style="{css}"><span style="display:inline-block;background:#f7e27a;color:#151515;padding:26px 34px 34px;box-shadow:0 18px 30px #0006;transform:rotate(-3deg);font-size:{int(size*0.75)}px">{markup(it["text"])}</span></div>'
    return f'<div id="{iid}" class="tx" style="{css}color:{fg}">{markup(it["text"])}</div>'

def enter_js(sel, kind, tilt, at):
    """entrance as an attribute tween (item drawn around 0,0 inside a translated parent)."""
    T = lambda dx, dy, r, sx, sy: f"translate({dx} {dy}) rotate({r:.1f}) scale({sx} {sy})"
    end = T(0, 0, tilt, 1, 1)
    start, ease, d, op = {
        "pop":   (T(0, 0, tilt - 12, 0.02, 0.02), "back.out(2.2)", .45, 1),
        "drop":  (T(0, -380, tilt + 12, 1, 1), "back.out(1.4)", .55, 0),
        "left":  (T(-900, 0, tilt, 1, 1), "power3.out", .5, 1),
        "right": (T(900, 0, tilt, 1, 1), "power3.out", .5, 1),
        "grow":  (T(0, 0, tilt, 1, 0.02), "power3.out", .45, 1),
        "fade":  (end, "none", .4, 0),
    }[kind]
    return f'tl.fromTo("{sel}",{{attr:{{transform:"{start}"}},opacity:{op}}},{{attr:{{transform:"{end}"}},opacity:1,duration:{d},ease:"{ease}"}},{at:.2f});'

# ------------------------------------------------------------------ html
def build(ep, A, sch, D, P):
    beats = ep["beats"]; clips, js = [], ['const tl=gsap.timeline({paused:true});']
    for i, b in enumerate(beats):
        s, e, w = sch[i]; c0 = 0 if i == 0 else s - 0.15; c1 = w if i + 1 < len(beats) else D
        bg = b.get("bg", ep.get("paper", "cream")); dark = bg in DARK_BG; col = PAPER.get(bg, bg)
        svg_items, html_items = [], []
        for k, it in enumerate(b.get("items", [])):
            if it["type"] == "text": html_items.append(item_html(it, i, k, dark))
            else: svg_items.append(item_svg(it, A, i, k, dark))
        halftone = '<rect width="1080" height="1920" fill="url(#ht)"/>' if b.get("halftone", ep.get("halftone", True)) else ""
        clips.append(f'<div id="B{i}" class="clip" data-start="{c0:.2f}" data-duration="{c1-c0:.2f}" data-track-index="{1 + i % 2}">'
                     f'<svg class="full" width="1080" height="1920" viewBox="0 0 1080 1920"><rect width="1080" height="1920" fill="{col}"/><rect width="1080" height="1920" filter="url(#grain)" opacity="{".5" if dark else "1"}"/>{halftone}'
                     f'<g id="cam{i}">{"".join(svg_items)}</g></svg>{"".join(html_items)}</div>')
        js.append(f'tl.fromTo("#cam{i}",{{scale:1}},{{scale:{b.get("zoom", 1.06)},duration:{c1-c0:.2f},ease:"none",transformOrigin:"50% 50%"}},{c0:.2f});')
        for k, it in enumerate(b.get("items", [])):
            iid = f"#i{i}_{k}"; at = s + it.get("at", 0.15 + 0.4 * k)
            if it["type"] in ("circle", "arrow", "underline"):
                js.append(f'tl.to("{iid} .draw",{{strokeDashoffset:0,duration:.55,ease:"power2.inOut",stagger:.08}},{at:.2f});')
                if it["type"] == "arrow": js.append(f'tl.to("{iid} .head",{{opacity:1,duration:.1}},{at+0.5:.2f});')
                continue
            if it["type"] == "text":
                js.append(f'tl.fromTo("{iid}",{{opacity:0,y:40,scale:1.15}},{{opacity:1,y:0,scale:1,duration:.35,ease:"back.out(2)"}},{at:.2f});')
                js.append(f'tl.fromTo("{iid} .mk",{{backgroundSize:"0% 42%"}},{{backgroundSize:"100% 42%",duration:.4,ease:"power2.out"}},{at+0.35:.2f});')
                continue
            tilt = float(re.search(r'data-tilt="([-0-9.]+)"', item_svg(it, A, i, k, dark)).group(1)) if it["type"] in ("cutout", "photo", "pin") else 0
            js.append(enter_js(iid, it.get("enter", "pop" if it["type"] == "cutout" else "drop"), tilt, at))
        if i > 0:  # paper-tear wipe in the colour of this scene
            js.append(f'tl.fromTo("#wipe",{{x:1250}},{{x:-60,duration:.32,ease:"power2.in"}},{s-0.47:.2f});tl.set("#wipe path",{{attr:{{fill:"{col}"}}}},{s-0.47:.2f});tl.to("#wipe",{{x:-1400,duration:.34,ease:"power2.out"}},{s-0.13:.2f});')
    # stop-motion boil: every 1/12 s each paper item shifts a hair
    js.append(f'const DUR={D};let n=0;document.querySelectorAll(".boil").forEach((el,j)=>{{for(let t=0;t<DUR;t+=1/12){{n++;const a=Math.sin(n*12.9898+j)*43758.5453,f=a-Math.floor(a);'
              f'tl.set(el,{{attr:{{transform:`translate(${{(f*4-2).toFixed(2)}} ${{((f*7%1)*4-2).toFixed(2)}}) rotate(${{((f*13%1)*1.4-.7).toFixed(2)}})`}}}},t);}}}});')
    js.append(f'tl.to({{}},{{duration:.01}},{D-0.01});window.__timelines=window.__timelines||{{}};window.__timelines["c"]=tl;')
    wipe = torn(1300, 2100, 999, 30, 40)
    html = f'''<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><title>{ep.get("title","collage")}</title><style>
@font-face{{font-family:"Cairo";src:url("fonts/cairo-ar.woff2") format("woff2");font-weight:200 1000;font-display:block;unicode-range:U+0600-06FF,U+0750-077F,U+FB50-FDFF,U+FE70-FEFC,U+200C-200E;}}
@font-face{{font-family:"Cairo";src:url("fonts/cairo-latin.woff2") format("woff2");font-weight:200 1000;font-display:block;}}
html,body{{margin:0;background:#111}}#root{{position:relative;width:1080px;height:1920px;overflow:hidden;font-family:"Cairo",sans-serif;direction:rtl}}
.clip{{position:absolute;inset:0;overflow:hidden}}svg.full{{position:absolute;inset:0}}
.mk{{background:linear-gradient(#ffd21f,#ffd21f) no-repeat 100% 88%/0% 42%;padding:0 8px;color:inherit}}.rd{{color:#e5322d}}
.tx{{-webkit-text-stroke:0;}}
</style><script src="gsap.min.js"></script></head><body>
<div id="root" data-composition-id="c" data-start="0" data-duration="{D}" data-width="1080" data-height="1920">
<svg width="0" height="0" style="position:absolute"><defs>
<filter id="grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="2" seed="4"/><feColorMatrix type="saturate" values="0"/><feComponentTransfer><feFuncA type="table" tableValues="0 .10"/></feComponentTransfer></filter>
<pattern id="ht" width="12" height="12" patternUnits="userSpaceOnUse"><circle cx="6" cy="6" r="1.6" fill="#000" opacity=".09"/></pattern>
<filter id="shd" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="10" dy="16" stdDeviation="7" flood-opacity=".42"/></filter></defs></svg>
{"".join(clips)}
<div id="W" class="clip" data-start="0" data-duration="{D}" data-track-index="3"><svg class="full" width="1080" height="1920" viewBox="0 0 1080 1920"><g id="wipe" transform="translate(1250 0)"><g transform="translate(650 960)"><path d="{wipe}" fill="#efe6d2" filter="url(#shd)"/></g></g></svg></div>
</div><script>{"".join(js)}</script></body></html>'''
    open(os.path.join(P, "index.html"), "w").write(html)

# ------------------------------------------------------------------ sound
def sound(ep, sch, D, P):
    import numpy as np
    sys.path.insert(0, os.path.join(KIT, "scripts")); import sfx_lib as S
    sd = os.path.join(P, "sfx"); os.makedirs(sd, exist_ok=True)
    S.save(os.path.join(sd, "whoosh.wav"), S.whoosh(0.35)); S.save(os.path.join(sd, "pop.wav"), S.hit(0.18)); S.save(os.path.join(sd, "scr.wav"), S.whoosh(0.5) * 0.5)
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
            if x["type"] in ("cutout", "photo"): it.append({"file": "sfx/pop.wav", "at": round(at, 2), "gain": 0.16})
            if x["type"] in ("circle", "arrow", "underline"): it.append({"file": "sfx/scr.wav", "at": round(at, 2), "gain": 0.1})
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
    print("1/5 cut-outs..."); A = prepare_assets(ep, P)
    print("2/5 voice..."); durs = voice(ep, P); sch, D = schedule(ep, durs)
    print("3/5 html..."); build(ep, A, sch, D, P)
    lint = subprocess.run(["npx", "hyperframes", "lint"], cwd=P, capture_output=True, text=True).stdout
    if "✗" in lint: print(lint); sys.exit("LINT ERRORS")
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
