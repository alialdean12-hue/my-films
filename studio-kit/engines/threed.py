from lib import *
CSS = '.cap{position:absolute;left:80px;right:80px;top:230px;text-align:center;font-weight:900;font-size:96px;line-height:1.2;color:#fff;text-shadow:0 0 40px #f2c94c88}.sub{position:absolute;left:80px;right:80px;top:1560px;text-align:center;font-weight:800;font-size:62px;color:#cfd8ff}'
def stars(seed):
    return "".join(f'<circle cx="{(R(seed+k)+1)*540:.0f}" cy="{(R(seed+k+300)+1)*960:.0f}" r="{1.5+abs(R(seed+k+7))*3:.1f}" fill="#fff" opacity="{.3+abs(R(seed+k+9))*.7:.2f}"/>' for k in range(140))
def planet(i, r=300, tilt=-18):
    bands = "".join(f'<rect x="-{r*3}" y="{-r + k*r*2/14:.0f}" width="{r*14}" height="{r*2/14+1:.0f}" fill="{ep.get("bands", ["#e8c98a","#d9b070","#f0dcae","#c9985a","#e2bf80","#b8864a","#efd6a2"])[k%7]}"/>' for k in range(14))
    swirl = "".join(f'<ellipse cx="{(R(i*9+k)*r*2.5):.0f}" cy="{R(i*9+k+40)*r*.8:.0f}" rx="{60+abs(R(k))*80:.0f}" ry="14" fill="#fff" opacity=".18"/>' for k in range(10))
    ring = lambda half: f'<path d="{"M" if half else "M"}{-r*2.1},0 A{r*2.1},{r*.55} 0 0,{0 if half else 1} {r*2.1},0" fill="none" stroke="url(#rg)" stroke-width="{r*.42:.0f}" opacity=".95"/>'
    return (f'<g id="pl{i}" transform="rotate({tilt})">{ring(0) if ep.get("rings", True) else ""}<clipPath id="cp{i}"><circle r="{r}"/></clipPath><g clip-path="url(#cp{i})"><g id="tex{i}">{bands}{swirl}</g><circle r="{r}" fill="url(#shade)"/></g>'
            f'<circle r="{r}" fill="none" stroke="#fff3" stroke-width="3"/>{ring(1) if ep.get("rings", True) else ""}</g>')
DEFS = ('<defs><radialGradient id="shade" cx="35%" cy="30%" r="75%"><stop offset="0" stop-color="#fff" stop-opacity=".35"/><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".85"/></radialGradient>'
        '<linearGradient id="rg" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#cdb98f"/><stop offset=".3" stop-color="#f5e6c4"/><stop offset=".5" stop-color="#8a7754"/><stop offset=".7" stop-color="#e8d6b0"/><stop offset="1" stop-color="#a8946c"/></linearGradient>'
        '<radialGradient id="glo"><stop offset="0" stop-color="#f2c94c" stop-opacity=".35"/><stop offset="1" stop-color="#f2c94c" stop-opacity="0"/></radialGradient></defs>')
ep = load(); B = ep["beats"]
def scene(i, b, s, e, c0, c1):
    k = b["k"]; js = []; D = c1 - c0
    sv = f'<svg class="full" width="1080" height="1920" viewBox="0 0 1080 1920">{DEFS}<rect width="1080" height="1920" fill="#05060f"/><g id="st{i}">{stars(i*50)}</g><circle cx="540" cy="1000" r="700" fill="url(#glo)"/>'
    r = {"intro": 300, "ring": 240, "water": 150, "spin": 300, "moons": 190, "end": 260}[k]
    if k == "water":
        sv += f'<rect x="90" y="1060" width="900" height="420" rx="40" fill="#1d5fa8" opacity=".85"/><path id="wv{i}" d="M90,1060 q75,-30 150,0 t150,0 t150,0 t150,0 t150,0 t150,0" stroke="#9fd8ff" stroke-width="10" fill="none"/>'
    sv += f'<g id="cam{i}" transform="translate(540 1000) scale(1)"><g id="bob{i}" transform="translate(0 0)">{planet(i, r)}</g></g>'
    if k == "moons":
        for m in range(8):
            rr = 330 + m * 38; sv += f'<g transform="translate(540 1000) scale(1 .35)"><g id="mo{i}{m}" transform="rotate({m*47})"><circle cx="{rr}" r="{10+m%3*5}" fill="#cfd3dc"/></g></g>'
    sv += "</svg>"
    h = sv + f'<div class="cap" id="cp{i}" style="opacity:0">{b["cap"]}</div>' + (f'<div class="sub" id="sb{i}" style="opacity:0">{b["sub"]}</div>' if b["sub"] else "")
    js += [f'tl.fromTo("#cp{i}",{{opacity:0,y:40}},{{opacity:1,y:0,duration:.5,ease:"power3.out"}},{s:.2f});']
    if b["sub"]: js.append(f'tl.fromTo("#sb{i}",{{opacity:0}},{{opacity:1,duration:.5}},{s+.7:.2f});')
    spd = 5 if k == "spin" else 1
    js.append(f'tl.fromTo("#tex{i}",{{x:0}},{{x:{-r*(1.5 if spd==1 else 9):.0f},duration:{D:.2f},ease:"none"}},{c0:.2f});')
    js.append(f'tl.fromTo("#st{i}",{{x:0}},{{x:-60,duration:{D:.2f},ease:"none"}},{c0:.2f});')
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
