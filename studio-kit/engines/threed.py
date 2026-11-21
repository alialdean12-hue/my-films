from lib import *
CSS = '.cap{position:absolute;left:80px;right:80px;top:230px;text-align:center;font-weight:900;font-size:96px;line-height:1.2;color:#fff;text-shadow:0 0 40px #f2c94c88}.sub{position:absolute;left:80px;right:80px;top:1560px;text-align:center;font-weight:800;font-size:62px;color:#cfd8ff}'
def stars(seed):
    return "".join(f'<circle cx="{(R(seed+k)+1)*540:.0f}" cy="{(R(seed+k+300)+1)*960:.0f}" r="{1.5+abs(R(seed+k+7))*3:.1f}" fill="#fff" opacity="{.3+abs(R(seed+k+9))*.7:.2f}"/>' for k in range(140))
def planet(i, r=300, tilt=-18):
    bands = "".join(f'<rect x="-{r*3}" y="{-r + k*r*2/14:.0f}" width="{r*14}" height="{r*2/14+1:.0f}" fill="{BANDS()[k%7]}"/>' for k in range(14))
    swirl = "".join(f'<ellipse cx="{(R(i*9+k)*r*2.5):.0f}" cy="{R(i*9+k+40)*r*.8:.0f}" rx="{60+abs(R(k))*80:.0f}" ry="14" fill="#fff" opacity=".18"/>' for k in range(10))
    ring = lambda half: f'<path d="{"M" if half else "M"}{-r*2.1},0 A{r*2.1},{r*.55} 0 0,{0 if half else 1} {r*2.1},0" fill="none" stroke="url(#rg)" stroke-width="{r*.42:.0f}" opacity=".95"/>'
    return (f'<g id="pl{i}" transform="rotate({tilt})">{ring(0) if RINGS() else ""}<clipPath id="cp{i}"><circle r="{r}"/></clipPath><g clip-path="url(#cp{i})"><g id="tex{i}">{bands}{swirl}</g><circle r="{r}" fill="url(#shade)"/></g>'
            f'<circle r="{r}" fill="none" stroke="#fff3" stroke-width="3"/>{ring(1) if RINGS() else ""}</g>')
DEFS = ('<defs><radialGradient id="shade" cx="35%" cy="30%" r="75%"><stop offset="0" stop-color="#fff" stop-opacity=".35"/><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".85"/></radialGradient>'
        '<linearGradient id="rg" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#cdb98f"/><stop offset=".3" stop-color="#f5e6c4"/><stop offset=".5" stop-color="#8a7754"/><stop offset=".7" stop-color="#e8d6b0"/><stop offset="1" stop-color="#a8946c"/></linearGradient>'
        '<radialGradient id="glo"><stop offset="0" stop-color="#f2c94c" stop-opacity=".35"/><stop offset="1" stop-color="#f2c94c" stop-opacity="0"/></radialGradient></defs>')
ep = load(); B = ep["beats"]

PLANETS = {  # bands (7 colours), rings
 "saturn": (["#e8c98a", "#d9b070", "#f0dcae", "#c9985a", "#e2bf80", "#b8864a", "#efd6a2"], True),
 "jupiter": (["#e8c8a0", "#c98f5a", "#f4e3c4", "#b8703a", "#e8b080", "#d9a070", "#f0d0a8"], False),
 "earth": (["#2b8be0", "#2f9a46", "#2b8be0", "#e8e0c0", "#2b8be0", "#2f9a46", "#2b70c0"], False),
 "mars": (["#c4502a", "#a8401a", "#d9703a", "#b84a22", "#c96a3a", "#8a3a1a", "#d98050"], False),
 "venus": (["#f2d29a", "#e8c080", "#f4e0b0", "#e0b070", "#f0d8a0", "#d9a860", "#f4e8c0"], False),
 "mercury": (["#9a9a9a", "#8a8a8a", "#b0b0b0", "#7a7a7a", "#a0a0a0", "#888888", "#b8b8b8"], False),
 "uranus": (["#9fe8f0", "#8fdce8", "#b0f0f4", "#80d0e0", "#a8ecf0", "#90e0e8", "#c0f4f8"], True),
 "neptune": (["#3a6ad0", "#2b5ac0", "#4a7ae0", "#2a4ab0", "#3a70d8", "#2050a8", "#5080e0"], False),
 "pluto": (["#d9c0a0", "#c0a080", "#e8d0b8", "#b09070", "#d0b898", "#a88868", "#f0dcc8"], False),
 "moon": (["#c9c9c9", "#b8b8b8", "#d0d0d0", "#a8a8a8", "#c0c0c0", "#b0b0b0", "#d8d8d8"], False),
 "sun": (["#ffd21f", "#ffb02e", "#ffe27a", "#ff9a1a", "#ffc93a", "#ffa020", "#ffe890"], False),
 "ice_planet": (["#e8f6ff", "#bfe6ff", "#ffffff", "#a8d8f8", "#d8f0ff", "#90c8f0", "#f0faff"], True),
 "lava_planet": (["#3a0a00", "#ff5a1a", "#5a1a00", "#ff8a2a", "#2a0500", "#e5322d", "#4a1000"], False),
 "candy_planet": (["#ff7ab6", "#7ad7ff", "#ffe27a", "#c4a8ff", "#9fe870", "#ff9a5a", "#ffffff"], True),
}
def OBJ(b=None): return (b or {}).get("object", ep.get("object", "saturn"))
def BANDS(): return ep.get("bands") or PLANETS.get(OBJ(CUR), PLANETS["saturn"])[0]
def RINGS(): return ep.get("rings", PLANETS.get(OBJ(CUR), PLANETS["saturn"])[1])
CUR = {}
SKY = {"space": "#05060f", "deep": "#0b0420", "studio": "#1a1a22", "blue": "#0a2a5a", "sunset": "#3a0a2a", "white": "#e8eef5", "green": "#04201a"}
def solid(i, kind, r):
    """non-planet 3D objects (shaded flat), spin via scaleX on #spin{i}."""
    if kind == "coin": return f'<g id="spin{i}"><ellipse rx="{r}" ry="{r}" fill="#c99a1e"/><ellipse rx="{r*.92:.0f}" ry="{r*.92:.0f}" fill="#f2c94c"/><circle r="{r*.7:.0f}" fill="none" stroke="#c99a1e" stroke-width="14"/><text y="{r*.3:.0f}" text-anchor="middle" font-size="{r*.9:.0f}" font-weight="900" fill="#a8780a" font-family="Cairo">{ep.get("label", "$")}</text></g>'
    if kind == "gem": return f'<g id="spin{i}"><path d="M{-r},{-r*.3} L{-r*.55},{-r*.85} H{r*.55} L{r},{-r*.3} L0,{r}Z" fill="#4ad0ff"/><path d="M{-r},{-r*.3} H{r} M{-r*.55},{-r*.85} L{-r*.3},{-r*.3} L0,{r} L{r*.3},{-r*.3} L{r*.55},{-r*.85}" stroke="#bff4ff" stroke-width="8" fill="none"/><path d="M{-r*.3},{-r*.3} L0,{-r*.85} L{r*.3},{-r*.3}" fill="#9fe8ff"/></g>'
    if kind == "cube": return f'<g id="spin{i}"><path d="M0,{-r} L{r*.87},{-r*.5} L0,0 L{-r*.87},{-r*.5}Z" fill="#7cc6ff"/><path d="M{-r*.87},{-r*.5} L0,0 V{r} L{-r*.87},{r*.5}Z" fill="#2b8be0"/><path d="M{r*.87},{-r*.5} L0,0 V{r} L{r*.87},{r*.5}Z" fill="#1d5fa8"/></g>'
    if kind == "gold_bar": return f'<g id="spin{i}"><path d="M{-r},{r*.3} L{-r*.7},{-r*.3} H{r*.7} L{r},{r*.3}Z" fill="#f2c94c"/><path d="M{-r*.7},{-r*.3} L{-r*.5},{-r*.55} H{r*.5} L{r*.7},{-r*.3}Z" fill="#ffe27a"/><path d="M{-r},{r*.3} H{r} V{r*.42} H{-r}Z" fill="#c99a1e"/></g>'
    if kind == "ball": return f'<g id="spin{i}"><circle r="{r}" fill="#fff"/><path d="M0,{-r*.35} L{r*.33},{-r*.1} L{r*.2},{r*.28} H{-r*.2} L{-r*.33},{-r*.1}Z" fill="#151515"/><circle r="{r}" fill="url(#shade)"/></g>'
    if kind == "heart": return f'<g id="spin{i}"><path d="M0,{r*.6} C{-r*1.3},{-r*.3} {-r},{-r*1.4} 0,{-r*.8} C{r},{-r*1.4} {r*1.3},{-r*.3} 0,{r*.6}Z" fill="#ff3a5a"/><path d="M{-r*.5},{-r*.6} q{r*.2},-{r*.2} {r*.4},0" stroke="#fff" stroke-opacity=".6" stroke-width="20" fill="none"/></g>'
    if kind == "atom": return f'<g id="spin{i}">' + "".join(f'<ellipse rx="{r}" ry="{r*.35:.0f}" fill="none" stroke="#7cc6ff" stroke-width="14" transform="rotate({a})"/>' for a in (0, 60, 120)) + f'<circle r="{r*.18:.0f}" fill="#e5322d"/></g>'
    if kind == "dice": return f'<g id="spin{i}"><rect x="{-r*.8:.0f}" y="{-r*.8:.0f}" width="{r*1.6:.0f}" height="{r*1.6:.0f}" rx="{r*.2:.0f}" fill="#fff"/>' + "".join(f'<circle cx="{x*r*.45:.0f}" cy="{y*r*.45:.0f}" r="{r*.13:.0f}" fill="#151515"/>' for x, y in ((-1, -1), (1, 1), (0, 0), (1, -1), (-1, 1))) + '</g>'
    if kind == "pyramid": return f'<g id="spin{i}"><path d="M0,{-r} L{-r},{r*.6} H0Z" fill="#e3b765"/><path d="M0,{-r} L{r},{r*.6} H0Z" fill="#b8863e"/></g>'
    if kind == "bulb": return f'<g id="spin{i}"><circle cy="{-r*.2:.0f}" r="{r*.8:.0f}" fill="#ffe27a"/><rect x="{-r*.35:.0f}" y="{r*.55:.0f}" width="{r*.7:.0f}" height="{r*.45:.0f}" fill="#9aa8b6"/><circle cy="{-r*.2:.0f}" r="{r*.8:.0f}" fill="url(#shade)"/></g>'
    return ""
def scene(i, b, s, e, c0, c1):
    k = b["k"]; js = []; D = c1 - c0; CUR.clear(); CUR.update(b); obj = OBJ(b)
    sv = f'<svg class="full" width="1080" height="1920" viewBox="0 0 1080 1920">{DEFS}<rect width="1080" height="1920" fill="{SKY.get(b.get("sky", ep.get("sky", "space")), "#05060f")}"/><g id="st{i}">{stars(i*50)}</g><circle cx="540" cy="1000" r="700" fill="url(#glo)"/>'
    r = {"intro": 300, "ring": 240, "water": 150, "spin": 300, "moons": 190, "end": 260}[k]
    if k == "water":
        sv += f'<rect x="90" y="1060" width="900" height="420" rx="40" fill="#1d5fa8" opacity=".85"/><path id="wv{i}" d="M90,1060 q75,-30 150,0 t150,0 t150,0 t150,0 t150,0 t150,0" stroke="#9fd8ff" stroke-width="10" fill="none"/>'
    sv += f'<g id="cam{i}" transform="translate(540 1000) scale(1)"><g id="bob{i}" transform="translate(0 0)">{planet(i, r) if obj in PLANETS else solid(i, obj, r)}</g></g>'
    if k == "moons":
        for m in range(8):
            rr = 330 + m * 38; sv += f'<g transform="translate(540 1000) scale(1 .35)"><g id="mo{i}{m}" transform="rotate({m*47})"><circle cx="{rr}" r="{10+m%3*5}" fill="#cfd3dc"/></g></g>'
    sv += "</svg>"
    h = sv + f'<div class="cap" id="cp{i}" style="opacity:0;{"color:#151515;text-shadow:none" if b.get("sky", ep.get("sky")) == "white" else ""}">{b["cap"]}</div>' + (f'<div class="sub" id="sb{i}" style="opacity:0">{b["sub"]}</div>' if b.get("sub") else "")
    js += [f'tl.fromTo("#cp{i}",{{opacity:0,y:40}},{{opacity:1,y:0,duration:.5,ease:"power3.out"}},{s:.2f});']
    if b.get("sub"): js.append(f'tl.fromTo("#sb{i}",{{opacity:0}},{{opacity:1,duration:.5}},{s+.7:.2f});')
    spd = 5 if k == "spin" else 1
    if obj in PLANETS: js.append(f'tl.fromTo("#tex{i}",{{x:0}},{{x:{-r*(1.5 if spd==1 else 9):.0f},duration:{D:.2f},ease:"none"}},{c0:.2f});')
    js.append(f'tl.fromTo("#st{i}",{{x:0}},{{x:-60,duration:{D:.2f},ease:"none"}},{c0:.2f});')
    if obj not in PLANETS: js.append(f'tl.fromTo("#spin{i}",{{scaleX:1}},{{scaleX:-1,duration:{1.2 if k != "spin" else .3},yoyo:true,repeat:{int(D/(1.2 if k != "spin" else .3))},ease:"sine.inOut",transformOrigin:"50% 50%"}},{c0:.2f});')
    if k == "intro": js.append(f'tl.fromTo("#cam{i}",{{attr:{{transform:"translate(540 1000) scale(0.2)"}}}},{{attr:{{transform:"translate(540 1000) scale(1)"}},duration:2.2,ease:"power3.out"}},{c0:.2f});')
    if k == "ring": js.append(f'tl.fromTo("#cam{i}",{{attr:{{transform:"translate(540 1000) scale(1)"}}}},{{attr:{{transform:"translate(160 1000) scale(2.6)"}},duration:{D:.2f},ease:"sine.inOut"}},{c0:.2f});')
    if k == "water":
        js.append(f'tl.fromTo("#bob{i}",{{attr:{{transform:"translate(0 -700)"}}}},{{attr:{{transform:"translate(0 40)"}},duration:1.2,ease:"bounce.out"}},{s+.3:.2f});')
        js.append(f'tl.fromTo("#bob{i}",{{attr:{{transform:"translate(0 40)"}}}},{{attr:{{transform:"translate(0 60)"}},duration:.8,yoyo:true,repeat:5,ease:"sine.inOut"}},{s+1.5:.2f});')
        js.append(f'tl.fromTo("#wv{i}",{{x:0}},{{x:-150,duration:1,repeat:6,ease:"none"}},{c0:.2f});')
    if k == "spin": js.append(f'tl.fromTo("#cam{i}",{{attr:{{transform:"translate(540 1000) scale(1)"}}}},{{attr:{{transform:"translate(540 1000) scale(1.15)"}},duration:{D:.2f},ease:"none"}},{c0:.2f});')
    if k == "moons":
        for m in range(8): js.append(f'tl.fromTo("#mo{i}{m}",{{attr:{{transform:"rotate({m*47})"}}}},{{attr:{{transform:"rotate({m*47+360*(1.4-m*.12):.0f})"}},duration:{D:.2f},ease:"none"}},{c0:.2f});')
    if k == "end": js.append(f'tl.fromTo("#cam{i}",{{attr:{{transform:"translate(540 1000) scale(1.3)"}}}},{{attr:{{transform:"translate(540 1000) scale(0.9)"}},duration:{D:.2f},ease:"sine.inOut"}},{c0:.2f});')
    return h, js
run("5_3d", B, scene, css=CSS, bg="#05060f", bed="drone", rate="-3%")
