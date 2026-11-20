"""Style 4 · kinetic typography: 24 themes, 16 entrances, 8 layouts, 10 backgrounds, emphasis effects, icons. JSON -> video. See README.md."""
from lib import *
from icons import icon
THEMES = {  # bg cycle, text, accent
 "classic": (["#0b0b0f", "#ffc933", "#0b0b0f", "#e5322d", "#0b0b0f", "#2b6cff"], "#ffffff", "#ffc933"),
 "mono": (["#0b0b0f", "#f4f4f4"], "#ffffff", "#ffffff"), "paper": (["#f4ecd8", "#e8dcc0"], "#151515", "#e5322d"),
 "neon": (["#0a0420", "#14082e"], "#ffffff", "#39ff88"), "sunset": (["#ff5e62", "#ff9966", "#7a1fa2"], "#ffffff", "#ffe27a"),
 "ocean": (["#0a3d7a", "#1d6fb8", "#0b2a4a"], "#ffffff", "#7ce0ff"), "forest": (["#14361f", "#2f5a46"], "#f4f1d0", "#9fe870"),
 "candy": (["#ff7ab6", "#7ad7ff", "#ffe27a"], "#151515", "#ffffff"), "gold": (["#151515", "#2a2318"], "#f4e3b0", "#f2c94c"),
 "fire": (["#1a0500", "#3a0a00", "#e5322d"], "#ffffff", "#ffb02e"), "ice": (["#e8f6ff", "#bfe6ff"], "#0b2a4a", "#2b8be0"),
 "royal": (["#1b0f3a", "#3a1f7a"], "#ffffff", "#f2c94c"), "mint": (["#d8fff0", "#a8f0d8"], "#0b3a2a", "#e5322d"),
 "coffee": (["#3a2414", "#5a3a22"], "#f4e3c4", "#ffb35a"), "sport": (["#0b0b0f", "#2fbf6a"], "#ffffff", "#ffd21f"),
 "news": (["#ffffff", "#e5322d"], "#151515", "#e5322d"), "tech": (["#05101f", "#0b2340"], "#e8f4ff", "#00e0ff"),
 "retro": (["#f2d0a4", "#e07a5f", "#3d405b"], "#151515", "#81b29a"), "pastel": (["#fde2e4", "#e2ece9", "#dfe7fd"], "#3a3a3a", "#ff6a8a"),
 "islamic": (["#0b3a2a", "#14532d"], "#f4f1d0", "#f2c94c"), "horror": (["#050505", "#1a0000"], "#e8e8e8", "#ff1a1a"),
 "kids": (["#ffd21f", "#2fbf6a", "#2b8be0", "#ff6a8a"], "#151515", "#ffffff"), "luxury": (["#0b0b0b"], "#e8dcc0", "#c9a24a"),
 "bw_red": (["#ffffff", "#0b0b0f"], "#151515", "#e5322d"),
}
ENTER = {  # from-state for words
 "slam": "scale:3.2,rotation:-8,opacity:0", "pop": "scale:.2,rotation:10,opacity:0", "drop": "y:-500,opacity:0", "rise": "y:500,opacity:0",
 "left": "x:-900,opacity:0", "right": "x:900,opacity:0", "spin": "rotation:-180,scale:.2,opacity:0", "blur": "opacity:0,filter:'blur(30px)',scale:1.3",
 "stretch": "scaleX:3,scaleY:.3,opacity:0", "squash": "scaleX:.2,scaleY:2.5,opacity:0", "flipx": "rotationX:90,opacity:0", "flipy": "rotationY:90,opacity:0",
 "zoomout": "scale:6,opacity:0", "tilt": "rotation:25,x:300,opacity:0", "fade": "opacity:0", "shake": "x:40,opacity:0",
}
EASE = {"slam": "back.out(1.7)", "pop": "back.out(2.4)", "drop": "bounce.out", "rise": "back.out(1.4)", "spin": "back.out(1.5)", "stretch": "elastic.out(1,.5)", "squash": "elastic.out(1,.5)", "zoomout": "expo.out"}
BGFX = ["bar", "none", "circle", "stripes", "grid", "burst", "dots", "frame", "split", "noise"]
def bgfx(kind, i, acc, D, c0):
    js = []
    if kind == "bar": h = f'<div id="bx{i}" style="position:absolute;left:0;top:0;height:1920px;width:60px;background:{acc};opacity:.9"></div>'; js.append(f'tl.fromTo("#bx{i}",{{x:0}},{{x:1020,duration:{D:.2f},ease:"none"}},{c0:.2f});')
    elif kind == "circle": h = f'<div id="bx{i}" style="position:absolute;left:140px;top:560px;width:800px;height:800px;border-radius:50%;border:30px solid {acc};opacity:.25"></div>'; js.append(f'tl.fromTo("#bx{i}",{{scale:.6}},{{scale:1.15,duration:{D:.2f},ease:"none"}},{c0:.2f});')
    elif kind == "stripes": h = f'<div id="bx{i}" style="position:absolute;inset:-200px;background:repeating-linear-gradient(45deg,{acc}22 0 40px,transparent 40px 120px)"></div>'; js.append(f'tl.fromTo("#bx{i}",{{x:0}},{{x:-170,duration:{D:.2f},ease:"none"}},{c0:.2f});')
    elif kind == "grid": h = f'<div id="bx{i}" style="position:absolute;inset:-120px;background-image:linear-gradient({acc}22 2px,transparent 2px),linear-gradient(90deg,{acc}22 2px,transparent 2px);background-size:120px 120px"></div>'; js.append(f'tl.fromTo("#bx{i}",{{y:0}},{{y:120,duration:{D:.2f},ease:"none"}},{c0:.2f});')
    elif kind == "burst": h = f'<div id="bx{i}" style="position:absolute;left:-460px;top:-0px;width:2000px;height:2000px;background:repeating-conic-gradient({acc}26 0 10deg,transparent 10deg 20deg);border-radius:50%"></div>'; js.append(f'tl.fromTo("#bx{i}",{{rotation:0}},{{rotation:40,duration:{D:.2f},ease:"none"}},{c0:.2f});')
    elif kind == "dots": h = f'<div id="bx{i}" style="position:absolute;inset:-100px;background-image:radial-gradient({acc}44 6px,transparent 7px);background-size:70px 70px"></div>'; js.append(f'tl.fromTo("#bx{i}",{{x:0}},{{x:70,duration:{D:.2f},ease:"none"}},{c0:.2f});')
    elif kind == "frame": h = f'<div id="bx{i}" style="position:absolute;inset:60px;border:16px solid {acc}"></div>'; js.append(f'tl.fromTo("#bx{i}",{{scale:1.2,opacity:0}},{{scale:1,opacity:1,duration:.5}},{c0:.2f});')
    elif kind == "split": h = f'<div id="bx{i}" style="position:absolute;left:0;right:0;top:960px;height:960px;background:{acc};opacity:.15"></div>'; js.append(f'tl.fromTo("#bx{i}",{{scaleY:0,transformOrigin:"50% 100%"}},{{scaleY:1,duration:.5}},{c0:.2f});')
    elif kind == "noise": h = f'<svg class="full" width="1080" height="1920"><filter id="nz{i}"><feTurbulence baseFrequency=".8" numOctaves="2" seed="{i}"/><feColorMatrix type="saturate" values="0"/><feComponentTransfer><feFuncA type="table" tableValues="0 .12"/></feComponentTransfer></filter><rect width="1080" height="1920" filter="url(#nz{i})"/></svg>'
    else: h = ""
    return h, js
def scene(i, b, s, e, c0, c1):
    th = THEMES.get(ep.get("theme", "classic"), THEMES["classic"]); bgs, fg, acc = th
    bg = b.get("bg", bgs[i % len(bgs)]); fg = b.get("color", fg); acc = b.get("accent", acc)
    if bg == acc: acc = fg
    words = b["w"]; n = len(words); step = (e - s + .3) / n; lay = b.get("layout", ep.get("layout", "one"))
    anims = b.get("anim") or ep.get("anim") or ["slam", "pop", "left"]; anims = [anims] if isinstance(anims, str) else anims
    h = f'<div style="position:absolute;inset:0;background:{bg}"></div>'
    fx, js = bgfx(b.get("bgfx", ep.get("bgfx", BGFX[i % 3] if ep.get("bgfx") is None else "none")), i, acc, c1 - c0, c0); h += fx
    if b.get("icon"): h += f'<svg class="full" width="1080" height="1920"><g id="ic{i}" transform="translate(540 1500)">{icon(b["icon"], .9)}</g></svg>'; js.append(f'tl.fromTo("#ic{i}",{{scale:0,transformOrigin:"50% 50%"}},{{scale:1,duration:.4,ease:"back.out(2)"}},{s+.3:.2f});')
    for k, w in enumerate(words):
        num = len(w) <= 2; size = b.get("size") or (520 if num else (300 if len(w) <= 4 else 220 if len(w) <= 7 else 160))
        col = acc if (num or k in b.get("hl", [0 if i else -1])) else fg
        if lay == "stack": size = min(size, 200); y = 960 - n * 120 + k * 240
        elif lay == "top": y = 380
        elif lay == "bottom": y = 1100
        elif lay == "zigzag": y = 700 + (k % 2) * 260 - 130
        else: y = 700
        x0 = {"zigzag": (-180 if k % 2 == 0 else 180)}.get(lay, 0)
        style = b.get("style", ep.get("style", "solid"))
        css = {"solid": f"color:{col}", "outline": f"color:transparent;-webkit-text-stroke:10px {col}", "box": f"color:{bg};background:{col};padding:0 40px 30px",
               "shadow": f"color:{col};text-shadow:14px 14px 0 {acc if col != acc else fg}", "underline": f"color:{col};border-bottom:24px solid {acc}", "glow": f"color:{col};text-shadow:0 0 40px {col},0 0 90px {col}",
               "highlight": f"color:{col};background:linear-gradient({acc}88,{acc}88) no-repeat 0 85%/100% 35%", "italic": f"color:{col};font-style:italic"}[style if not (k == n - 1 and i % 2 and style == "solid") else "box"]
        h += f'<div id="w{i}_{k}" style="position:absolute;left:{x0}px;right:{-x0}px;top:{y}px;text-align:center;font-weight:900;font-size:{size}px;line-height:1;opacity:0"><span style="display:inline-block;{css}">{w}</span></div>'
        t = s - .05 + k * step if lay != "stack" else s + k * .25; a = anims[k % len(anims)]
        js.append(f'tl.fromTo("#w{i}_{k} span",{{{ENTER.get(a, ENTER["pop"])}}},{{x:0,y:0,scale:1,scaleX:1,scaleY:1,rotation:0,rotationX:0,rotationY:0,opacity:1,filter:"blur(0px)",duration:.28,ease:"{EASE.get(a, "power3.out")}"}},{t:.2f});')
        js.append(f'tl.set("#w{i}_{k}",{{opacity:1}},{t:.2f});')
        emph = b.get("emph", ep.get("emph", "grow"))
        if emph == "grow": js.append(f'tl.to("#w{i}_{k} span",{{scale:1.08,duration:{max(.2, step-.35):.2f},ease:"none"}},{t+.28:.2f});')
        elif emph == "wobble": js.append(f'tl.to("#w{i}_{k} span",{{rotation:4,duration:.12,yoyo:true,repeat:{int(step/.12)}}},{t+.28:.2f});')
        elif emph == "pulse": js.append(f'tl.to("#w{i}_{k} span",{{scale:1.12,duration:.2,yoyo:true,repeat:{int(step/.2)}}},{t+.28:.2f});')
        elif emph == "shake": js.append(f'tl.to("#w{i}_{k} span",{{x:8,duration:.04,yoyo:true,repeat:{int(step/.04)}}},{t+.28:.2f});')
        if lay != "stack" and k < n - 1: js.append(f'tl.to("#w{i}_{k}",{{opacity:0,y:-120,duration:.12}},{t+step-.12:.2f});')
    return h, js
if __name__ == "__main__":
    ep = load(); B = ep["beats"]
    run("kinetic", B, scene, bed=ep.get("bed", "beat"), rate="+5%", extra_sfx=lambda sch: [{"file": "sfx/hit.wav", "at": round(s, 2), "gain": .25} for s, e in sch])
