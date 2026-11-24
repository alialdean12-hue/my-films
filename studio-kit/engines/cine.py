"""Style 3 · cinematic stick story (رجل العود السينمائي). Characters are built from a description (characters.py),
placed in illustrated places with effects, camera moves and big captions. JSON -> video.
  python3 cine.py story.json OUTDIR [--preview]
Story json:
  "characters": {"name": {spec of characters.py: sex, age, build, height, skin, hair, beard, head, wear, outer, hold, ...}}
  "beats": [{"line": spoken text, "cap": "big caption with [y]..[/y] / [r]..[/r]", "place": PLACE, "time": "day|sunset|night",
             "cast": [{"who": name, "x": 300, "pose": "stand|walk|kneel|sit", "face": "calm|tired|curious|shock|joy|sad|angry",
                       "flip": false, "scale": 1, "to": 600, "pose2": .., "face2": .., "at": 1.5, "window": 2}],
             "fx": [{"kind": "mushroom|flash|shake|plane|smoke|petals|rain|rays|glint|birds|stars", "x":.., "y":.., "at":.., "scale":..}],
             "cam": "push|zoom|pan|still", "view": "harbor|hills|desert" (office/room window)}]
See README.md (style 3) and CATALOG.md for every name."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import characters as C
import war as W
from lib import run, load, mk, R
ep = load(); B = ep["beats"]; CAST = ep.get("characters", {})
K = C.K; G = 1600
PLACES = W.PLACES + ["city", "ruins", "office", "room", "train", "garden", "night_garden", "desert", "desert_night", "sea", "street_night", "plain"]
FX = ["army", "explosion", "flag", "mushroom", "flash", "shake", "plane", "smoke", "petals", "rain", "rays", "glint", "birds", "stars"]

# ------------------------------------------------------------------ drawing helpers
SKY = {"day": ("#8ac0e8", "#f6e6c8"), "sunset": ("#5a3a6a", "#f0a060"), "night": ("#070b1f", "#3b3f6e"), "dark": ("#3a1e1a", "#c86a3a")}
def sky(i, time="day", top=None, bot=None):
    a, b = SKY.get(time, SKY["day"]); a, b = top or a, bot or b
    return (f'<defs><linearGradient id="sk{i}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient></defs>'
            f'<rect x="-300" y="-300" width="1680" height="2520" fill="url(#sk{i})"/>')
def sun_moon(time):
    if time == "night": return f'<circle cx="840" cy="620" r="150" fill="#fff8dc" opacity=".15"/><circle cx="840" cy="620" r="64" fill="#fff4d2" stroke="{K}" stroke-width="5"/>'
    if time == "sunset": return '<circle cx="860" cy="1000" r="120" fill="#ffb060" opacity=".9"/>'
    return '<circle cx="880" cy="620" r="70" fill="#fff2b0"/>'
def stars(i, n=60):
    return "".join(f'<circle class="st{i}" cx="{R(k)*1080:.0f}" cy="{R(k+40)*1000:.0f}" r="{1.5+R(k+80)*2.5:.1f}" fill="#fff"/>' for k in range(n))
def mountains(y, col, seed):
    pts = " ".join(f"{-300 + k*140},{y - 120 - R(seed+k)*160:.0f}" for k in range(13))
    return f'<polygon points="-300,{y+40} {pts} 1500,{y+40}" fill="{col}" stroke="{K}" stroke-width="5"/>'
def ground(col, line="#6a6050"):
    return (f'<path d="M-300,{G-80} L1380,{G-80} L1380,2300 L-300,2300Z" fill="{col}" stroke="{K}" stroke-width="5"/>'
            + "".join(f'<path d="M{-200+k*160},{G+40+R(k)*200:.0f} q30,-6 60,0" stroke="{line}" stroke-width="5" fill="none"/>' for k in range(10)))
def house(x, y, w, h, wall="#e8dcc0", roof="#3a3a44"):
    return (f'<g transform="translate({x} {y})"><rect x="{-w/2}" y="{-h}" width="{w}" height="{h}" fill="{wall}" stroke="{K}" stroke-width="5"/>'
            + "".join(f'<path d="M{-w/2 + k*w/4},{-h} V0" stroke="#8a6a4a" stroke-width="5"/>' for k in range(1, 4))
            + f'<rect x="{-w/6}" y="{-h*.6}" width="{w/3}" height="{h*.35}" fill="#f6eed8" stroke="{K}" stroke-width="4"/>'
            + f'<path d="M{-w/2-40},{-h} Q{-w/2},{-h-20} {-w/2+10},{-h-50} L{w/2-10},{-h-50} Q{w/2},{-h-20} {w/2+40},{-h}Z" fill="{roof}" stroke="{K}" stroke-width="5"/></g>')
def town(i, ruined=False):
    s = mountains(1150, "#6a7a8a" if not ruined else "#4a3a38", 3)
    for r, (y, sc) in enumerate([(1250, .7), (1420, .85)]):
        for k in range(7):
            x = -200 + k * 230 + r * 110
            if ruined:
                s += f'<g transform="translate({x} {y}) scale({sc})"><path d="M-90,0 L-90,-{60+R(k+r*9)*80:.0f} L-40,-{30+R(k+5)*40:.0f} L10,-{90+R(k+7)*60:.0f} L60,-{20+R(k+3)*50:.0f} L90,0Z" fill="#3a2a2a" stroke="{K}" stroke-width="5"/></g>'
            else:
                s += f'<g transform="translate({x*(1-sc):.0f} {y*(1-sc):.0f}) scale({sc})">{house(x, y, 170 + R(k+r)*60, 120 + R(k+r*3)*40)}</g>'
    if not ruined:
        s += "".join(f'<path d="M{x},1560 V1160 M{x-40},1190 H{x+40}" stroke="#4a3a2a" stroke-width="10"/>' for x in (120, 760))
        s += '<path d="M120,1195 Q440,1240 760,1195 M120,1215 Q440,1262 760,1215" stroke="#2a2a2a" stroke-width="3" fill="none"/>'
    return s + ground("#8a8070" if not ruined else "#4a3a34", "#6a6050" if not ruined else "#2a1e1a")
def interior(i, view="hills", wall="#c8b48a"):
    s = f'<rect x="-300" y="-300" width="1680" height="2520" fill="{wall}"/><rect x="-300" y="1500" width="1680" height="800" fill="#7a5a3a" stroke="{K}" stroke-width="5"/>'
    s += "".join(f'<path d="M{-300+k*120},1500 L{-400+k*160},2300" stroke="#5a3e24" stroke-width="5"/>' for k in range(16))
    s += f'<g id="win{i}"><rect x="560" y="420" width="420" height="560" fill="#9ac8e8" stroke="{K}" stroke-width="10"/>'
    if view == "harbor":
        s += '<path d="M560,780 L980,780 L980,980 L560,980Z" fill="#3a7aa8"/><path d="M600,760 L760,760 L740,800 L620,800Z" fill="#4a4a5a"/>'
    if view == "desert": s += '<path d="M560,760 Q700,700 980,740 L980,980 L560,980Z" fill="#e0b070"/>'
    else: s += '<path d="M560,700 Q700,640 980,700 L980,780 L560,780Z" fill="#6a8a6a"/>'
    return s + f'<path d="M770,420 V980 M560,700 H980" stroke="#5a3e24" stroke-width="12"/></g><rect x="590" y="400" width="360" height="30" fill="#5a3e24"/>'
def dunes(i, night):
    c1, c2, c3 = ("#4a4370", "#6a5878", "#9a7a6a") if night else ("#e0b070", "#d89a58", "#e8c088")
    d = lambda y, a, c, sd: f'<path d="M-400,{y} ' + " ".join(f"Q{-400+(k+1)*275-137:.0f},{y-a*(.4+R(sd+k)):.0f} {-400+(k+1)*275:.0f},{y+(R(sd+k+9)-.5)*a*.4:.0f}" for k in range(8)) + f' V2200 H-400Z" fill="{c}" stroke="{K}" stroke-width="5"/>'
    return d(1150, 160, c1, 3) + d(1320, 190, c2, 21) + d(G - 40, 60, c3, 31)
def sakura(x, y):
    return (f'<g transform="translate({x} {y})"><path d="M0,0 Q-20,-200 10,-420 M0,-260 Q-80,-320 -160,-330 M6,-330 Q90,-380 170,-370" stroke="#4a2e22" stroke-width="26" fill="none" stroke-linecap="round"/>'
            + "".join(f'<circle cx="{(R(k+90)-.5)*460:.0f}" cy="{-380+(R(k+91)-.5)*220:.0f}" r="{60+R(k+92)*40:.0f}" fill="#f6b6c8" stroke="{K}" stroke-width="4"/>' for k in range(12)) + '</g>')
def train(i):
    s = f'<g id="tr{i}"><rect x="-200" y="1150" width="1500" height="330" rx="30" fill="#2a3a2a" stroke="{K}" stroke-width="7"/><rect x="-200" y="1150" width="1500" height="50" fill="#1a241a"/>'
    s += "".join(f'<rect x="{-150 + k*240}" y="1230" width="170" height="140" rx="12" fill="#f6dca0" stroke="{K}" stroke-width="6"/>' for k in range(6))
    return s + "".join(f'<circle cx="{-120+k*190}" cy="1500" r="55" fill="#2a2a2a" stroke="{K}" stroke-width="6"/><circle cx="{-120+k*190}" cy="1500" r="14" fill="#888"/>' for k in range(9)) + '</g>'
def sea(i, time):
    w = "#2a5a8a" if time != "night" else "#1a2a4a"
    return (f'<path d="M-300,1250 L1380,1250 L1380,2300 L-300,2300Z" fill="{w}" stroke="{K}" stroke-width="5"/>'
            + f'<g id="wv{i}">' + "".join(f'<path d="M{-300+k*180},{1320+r*120} q45,-24 90,0 t90,0" stroke="#9ac8e8" stroke-width="5" fill="none" opacity=".6"/>' for r in range(7) for k in range(11)) + '</g>'
            + f'<g transform="translate(760 1270)"><path d="M-160,0 L160,0 L120,60 L-120,60Z" fill="#6b4a2e" stroke="{K}" stroke-width="6"/><path d="M0,0 V-260" stroke="{K}" stroke-width="8"/><path d="M0,-250 Q120,-150 0,-30Z" fill="#f6f0dc" stroke="{K}" stroke-width="5"/></g>')

def place(i, b, s=0, J=None):
    p = b.get("place", "plain"); t = b.get("time", "day")
    if p == "map" or "map" in b: return W.map_svg(i, b.get("map", {}), s, J)
    wp = W.place(i, p, t, sky, ground, R)
    if wp: return wp
    if p == "city": return sky(i, t) + sun_moon(t) + (stars(i) if t == "night" else "") + town(i)
    if p == "ruins": return sky(i, "dark" if t == "day" else t) + town(i, ruined=True)
    if p == "office": return interior(i, b.get("view", "hills"))
    if p == "room": return interior(i, b.get("view", "hills"), "#d8c8b0")
    if p == "train": return sky(i, t) + f'<g id="hl{i}">{mountains(1150, "#6a9a6a", 9)}{mountains(1250, "#4a8a4a", 19)}</g>' + train(i)
    if p == "garden": return sky(i, t, "#bfe0f6", "#fff0f0") + mountains(1250, "#9ab8c8", 5) + ground("#8ab86a", "#6a9a4a") + sakura(860, G - 70)
    if p == "night_garden": return sky(i, "night", "#1a1e3a", "#4a3a5a") + stars(i, 30) + sakura(860, G - 70)
    if p in ("desert", "desert_night"):
        n = p == "desert_night" or t == "night"
        return sky(i, "night" if n else t) + (stars(i) if n else "") + sun_moon("night" if n else t) + dunes(i, n)
    if p == "sea": return sky(i, t) + sun_moon(t) + sea(i, t)
    if p == "street_night": return sky(i, "night") + stars(i, 30) + town(i)
    return sky(i, t, b.get("top"), b.get("bottom"))

def mushroom(i, k, x, y, sc):
    puffs = "".join(f'<circle cx="{(R(j+50)-.5)*360:.0f}" cy="{-520 + (R(j+60)-.5)*160:.0f}" r="{90+R(j+70)*70:.0f}" fill="url(#mg{i})" stroke="{K}" stroke-width="5"/>' for j in range(9))
    return (f'<defs><radialGradient id="mg{i}" cx="40%" cy="35%"><stop offset="0" stop-color="#ffe0a0"/><stop offset=".5" stop-color="#e8904a"/><stop offset="1" stop-color="#7a5a5a"/></radialGradient></defs>'
            f'<g id="m{i}_{k}" transform="translate({x} {y}) scale({sc})"><path d="M-70,0 Q-40,-260 -60,-440 L60,-440 Q40,-260 70,0Z" fill="url(#mg{i})" stroke="{K}" stroke-width="5"/>'
            f'<ellipse cx="0" cy="-300" rx="170" ry="40" fill="url(#mg{i})" stroke="{K}" stroke-width="5"/>{puffs}</g>')
def plane_svg(i, k, x, y, sc):
    return (f'<g id="pl{i}_{k}" transform="translate({x} {y}) scale({sc})"><path d="M-120,0 Q-80,-14 120,-6 Q140,0 120,6 Q-80,14 -120,0Z" fill="#c8ccd4" stroke="{K}" stroke-width="4"/>'
            f'<path d="M-10,-4 L-60,-90 L-30,-90 L40,-4Z M-10,4 L-60,90 L-30,90 L40,4Z M-110,-2 L-140,-40 L-120,-40 L-90,-2Z" fill="#aab0ba" stroke="{K}" stroke-width="4"/></g>')

# ------------------------------------------------------------------ scene
def scene(i, b, s, e, c0, c1):
    js = []; J = js.append; dur = c1 - c0
    back, front = [place(i, b, s, J)], []
    for k, f in enumerate(b.get("fx", [])):
        kind = f.get("kind"); at = s + f.get("at", 0)
        if kind not in FX: print(f"WARNING beat {i+1}: unknown fx {kind} (use {FX})")
        if kind == "army":
            (front if f.get("front") else back).append(W.force(i, k, f, s, f.get("dur", e - s), J)); continue
        if kind == "explosion":
            front.append(W.explosion(i, k, f.get("x", 540), f.get("y", 1300), f.get("scale", 1.0), at, J)); continue
        if kind == "flag":
            back.append(W.flag_pole(f.get("code", "IRQ"), f.get("x", 200), f.get("y", G - 60), i, k, f.get("w", 150)))
            J(f'tl.fromTo("#fg{i}_{k}",{{skewY:0}},{{skewY:5,duration:.6,yoyo:true,repeat:{int(dur/.6)},ease:"sine.inOut"}},{c0:.2f});'); continue
        if kind == "mushroom":
            x, y, sc = f.get("x", 760), f.get("y", 1250), f.get("scale", 1.0)
            back.append(mushroom(i, k, x, y, sc))
            J(f'tl.fromTo("#m{i}_{k}",{{attr:{{transform:"translate({x} {y}) scale(0)"}}}},{{attr:{{transform:"translate({x} {y}) scale({sc})"}},duration:2.2,ease:"power3.out"}},{at:.2f});')
        elif kind == "flash":
            front.append(f'<rect id="fl{i}_{k}" x="-300" y="-300" width="1680" height="2520" fill="#fffdf0" opacity="0"/>')
            J(f'tl.fromTo("#fl{i}_{k}",{{opacity:1}},{{opacity:0,duration:1.5,ease:"power2.in"}},{at:.2f});')
        elif kind == "shake":
            for j in range(8): J(f'tl.to("#W{i}",{{x:{(R(j+30+k)-.5)*40:.0f},y:{(R(j+31+k)-.5)*40:.0f},duration:.05}},{at+j*.05:.2f});')
            J(f'tl.to("#W{i}",{{x:0,y:0,duration:.1}},{at+.45:.2f});')
        elif kind == "plane":
            y = f.get("y", 640); back.append(plane_svg(i, k, -200, y, f.get("scale", .9)))
            J(f'tl.fromTo("#pl{i}_{k}",{{attr:{{transform:"translate(-200 {y}) scale({f.get("scale", .9)})"}}}},{{attr:{{transform:"translate(1300 {y-80}) scale({f.get("scale", .9)})"}},duration:{dur+.5:.2f},ease:"none"}},{c0:.2f});')
        elif kind == "smoke":
            col = f.get("color", "#3a3030"); y = f.get("y", 1300)
            back.append("".join(f'<circle class="sm{i}_{k}" cx="{R(j+i*11)*1080:.0f}" cy="{y}" r="{50+R(j+3)*60:.0f}" fill="{col}" opacity=".6"/>' for j in range(8)))
            J(f'tl.fromTo("#S{i} .sm{i}_{k}",{{y:0,opacity:.7}},{{y:-700,opacity:0,duration:{max(2, dur):.2f},stagger:.3,ease:"none"}},{c0:.2f});')
        elif kind == "petals":
            front.append("".join(f'<ellipse class="pt{i}" cx="{R(j+i)*1080:.0f}" cy="{-50 - R(j+40)*300:.0f}" rx="12" ry="8" fill="#f8b8c8" stroke="#c86a88" stroke-width="2"/>' for j in range(26)))
            J(f'tl.fromTo("#S{i} .pt{i}",{{y:0,x:0,rotation:0}},{{y:2100,x:-260,rotation:360,duration:5,stagger:.2,ease:"none"}},{c0:.2f});')
        elif kind == "rain":
            front.append(f'<g id="rn{i}">' + "".join(f'<line x1="{R(j+200)*1180-50:.0f}" y1="{R(j+250)*1920-1920:.0f}" x2="{R(j+200)*1180-60:.0f}" y2="{R(j+250)*1920-1850:.0f}" stroke="#c9d6e2" stroke-width="3" opacity=".6"/>' for j in range(140)) + '</g>')
            J(f'tl.fromTo("#rn{i}",{{y:0}},{{y:1920,duration:1,ease:"none",repeat:{int(dur)+1}}},{c0:.2f});')
        elif kind == "rays":
            back.append('<g opacity=".25">' + "".join(f'<path d="M880,200 L{200+j*160},1900 L{280+j*160},1900Z" fill="#fff6c8"/>' for j in range(5)) + '</g>')
        elif kind == "glint":
            x, y = f.get("x", 700), f.get("y", G - 14)
            front.append(f'<g id="gl{i}_{k}" transform="translate({x} {y}) scale(0)"><path d="M0,-40 L8,-8 L40,0 L8,8 L0,40 L-8,8 L-40,0 L-8,-8Z" fill="#fff6c8"/></g>')
            J(f'tl.fromTo("#gl{i}_{k}",{{attr:{{transform:"translate({x} {y}) scale(0) rotate(0)"}}}},{{attr:{{transform:"translate({x} {y}) scale(1.4) rotate(45)"}},duration:.35,ease:"back.out(3)",yoyo:true,repeat:3}},{at:.2f});')
        elif kind == "birds":
            back.append(f'<g id="bd{i}">' + "".join(f'<path d="M{-100-j*90},{500+R(j)*200:.0f} q20,-20 40,0 q20,-20 40,0" stroke="{K}" stroke-width="5" fill="none"/>' for j in range(6)) + '</g>')
            J(f'tl.fromTo("#bd{i}",{{x:0}},{{x:1500,duration:{dur:.2f},ease:"none"}},{c0:.2f});')
        elif kind == "stars":
            back.append(stars(i))
    if b.get("place") == "train":
        J(f'tl.fromTo("#hl{i}",{{x:0}},{{x:-500,duration:{dur:.2f},ease:"none"}},{c0:.2f});')
        J(f'tl.fromTo("#tr{i}",{{y:0}},{{y:4,duration:.12,yoyo:true,repeat:{int(dur/.12)},ease:"none"}},{c0:.2f});')
    if b.get("place") == "sea": J(f'tl.fromTo("#wv{i}",{{x:0}},{{x:-180,duration:{dur:.2f},ease:"none"}},{c0:.2f});')
    if b.get("time") == "night" or b.get("place") in ("desert_night", "night_garden", "street_night"):
        J(f'tl.fromTo("#S{i} .st{i}",{{opacity:1}},{{opacity:.25,duration:.8,yoyo:true,repeat:{int(dur/.8)+1},stagger:{{each:.05,from:"random"}},ease:"sine.inOut"}},{c0:.2f});')
    # characters
    people = []
    for k, c in enumerate(b.get("cast", [])):
        spec = CAST.get(c.get("who"))
        if spec is None: sys.exit(f'beat {i+1}: unknown character «{c.get("who")}»: define it in "characters"')
        if "window" in c:   # head in a train / house window
            x = -150 + int(c["window"]) * 240 + 85
            people.append(f'<g transform="translate({x} 1335) scale(.5)">{C.head(spec, c.get("face", "calm"))}</g>'); continue
        x = c.get("x", 540); sc = c.get("scale", 1.0); flip = " scale(-1 1)" if c.get("flip") else ""
        pose, face = c.get("pose", "stand"), c.get("face", "calm")
        drawings = [(pose, face)] + ([(c.get("pose2", pose), c.get("face2", face))] if ("pose2" in c or "face2" in c) else [])
        moving = "to" in c
        if moving and pose == "walk": drawings.append(("stand", face))      # walk cycle: stride + passing drawing
        g = "".join(f'<g id="c{i}_{k}_{j}" opacity="{1 if j == 0 else 0}">{C.character(spec, p, f)}</g>' for j, (p, f) in enumerate(drawings))
        inner = '<g transform="scale(-1 1)">' if c.get("flip") else "<g>"
        people.append(f'<g id="ch{i}_{k}" transform="translate({x} {G}) scale({sc})">{inner}<ellipse rx="170" ry="18" fill="#000" opacity=".28"/>{g}</g></g>')
        if moving:
            J(f'tl.to("#ch{i}_{k}",{{attr:{{transform:"translate({c["to"]} {G}) scale({sc})"}},duration:{max(.5, e - s):.2f},ease:"none"}},{s:.2f});')
            if pose == "walk":
                t, n = s, 0; last = len(drawings) - 1
                while t < e:
                    a, bb = (0, last) if n % 2 == 0 else (last, 0)
                    J(f'tl.set("#c{i}_{k}_{a}",{{opacity:0}},{t:.2f});tl.set("#c{i}_{k}_{bb}",{{opacity:1}},{t:.2f});'); t += .3; n += 1
        if ("pose2" in c or "face2" in c):
            t2 = s + c.get("at", (e - s) / 2)
            J(f'tl.set("#c{i}_{k}_0",{{opacity:0}},{t2:.2f});tl.set("#c{i}_{k}_1",{{opacity:1}},{t2:.2f});')
    # camera
    cam = b.get("cam", "push")
    if cam == "push": J(f'tl.fromTo("#V{i}",{{attr:{{transform:"translate(0 0) scale(1)"}}}},{{attr:{{transform:"translate({-540*.07:.0f} {-1150*.07:.0f}) scale(1.07)"}},duration:{dur:.2f},ease:"none"}},{c0:.2f});')
    elif cam == "zoom":
        fx, fy = b.get("focus", [540, 1050])
        J(f'tl.fromTo("#V{i}",{{attr:{{transform:"translate(0 0) scale(1)"}}}},{{attr:{{transform:"translate({540 - 1.6*fx:.0f} {960 - 1.6*fy:.0f}) scale(1.6)"}},duration:{min(1.2, dur):.2f},ease:"power2.inOut"}},{s+.3:.2f});')
    elif cam == "pan": J(f'tl.fromTo("#V{i}",{{attr:{{transform:"translate(60 0) scale(1.1)"}}}},{{attr:{{transform:"translate(-160 0) scale(1.1)"}},duration:{dur:.2f},ease:"none"}},{c0:.2f});')
    cap = f'<div class="cap" id="cp{i}">{mk(b.get("cap", ""))}</div>' if b.get("cap") else ""
    if b.get("date"):
        cap += f'<div class="date" id="dt{i}">{b["date"]}</div>'
        J(f'tl.fromTo("#dt{i}",{{scale:2.2,opacity:0,rotation:-14}},{{scale:1,opacity:1,rotation:-6,duration:.35,ease:"power3.in"}},{s+.4:.2f});')
    if cap: J(f'tl.fromTo("#cp{i}",{{y:40,opacity:0}},{{y:0,opacity:1,duration:.35,ease:"back.out(2)"}},{s+.15:.2f});')
    html = (f'<svg class="full" viewBox="0 0 1080 1920" width="1080" height="1920"><g id="W{i}"><g id="V{i}">{"".join(back)}{"".join(people)}{"".join(front)}</g></g>'
            f'<rect width="1080" height="1920" fill="url(#vigC)"/></svg>{cap}')
    return html, js

CSS = (".date{position:absolute;left:70px;top:470px;padding:6px 26px;border:8px solid #d0202a;color:#d0202a;background:rgba(255,248,230,.92);font-weight:900;font-size:56px;transform-origin:50% 50%}"
       ".cap{position:absolute;left:70px;right:70px;top:240px;text-align:center;font-weight:900;font-size:92px;line-height:1.25;color:#fff;"
       "paint-order:stroke fill;-webkit-text-stroke:14px #111;text-shadow:0 8px 0 rgba(0,0,0,.35)}")
OVER = (f'<svg width="0" height="0" style="position:absolute"><defs>{C.DEFS}<radialGradient id="vigC" cx="50%" cy="50%" r="72%"><stop offset=".55" stop-color="#000" stop-opacity="0"/>'
        f'<stop offset="1" stop-color="#000" stop-opacity=".7"/></radialGradient></defs></svg>')
def sfx(sch):
    out = []
    for k, b in enumerate(B):
        for f in b.get("fx", []):
            if f.get("kind") == "flash": out += [{"file": "sfx/hit.wav", "at": round(sch[k][0] + f.get("at", 0), 2), "gain": .9}, {"file": "sfx/riser.wav", "at": round(max(0, sch[k][0] + f.get("at", 0) - 1), 2), "gain": .35}]
            if f.get("kind") == "shake": out.append({"file": "sfx/hit.wav", "at": round(sch[k][0] + f.get("at", 0), 2), "gain": .5})
    return out
run("cine", B, scene, css=CSS, bg="#000", bed="drone", extra_sfx=sfx, overlay=OVER)
