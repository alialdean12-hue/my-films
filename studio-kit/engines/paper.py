from lib import *
CSS = '.cap{position:absolute;left:90px;right:90px;top:200px;text-align:center;font-weight:900;font-size:90px;line-height:1.2;color:#3a2412}.cap span{background:#fbf3e0;padding:6px 30px 16px;box-shadow:8px 10px 0 #0003;display:inline-block}'
DEFS = ('<defs><filter id="ps" x="-10%" y="-10%" width="120%" height="130%"><feDropShadow dx="0" dy="-10" stdDeviation="8" flood-opacity=".35"/></filter>'
        '<filter id="gr" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="3"/><feColorMatrix type="saturate" values="0"/><feComponentTransfer><feFuncA type="table" tableValues="0 .12"/></feComponentTransfer></filter></defs>')
def dune(y, amp, seed, col, w=3000):
    pts = " ".join(f"{-600+k*100},{y+math.sin(k*.5+seed)*amp+R(seed+k)*12:.0f}" for k in range(int(w/100)+1))
    return f'<polygon points="-600,1920 {pts} {w-600},1920" fill="{col}" filter="url(#ps)"/>'
def pyr(x, y, s, c1="#e3b765", c2="#b8863e"):
    return f'<g filter="url(#ps)"><polygon points="{x},{y-s} {x-s*1.1},{y} {x},{y}" fill="{c1}"/><polygon points="{x},{y-s} {x+s*1.1},{y} {x},{y}" fill="{c2}"/></g>'
def camel(x, y, sc=1):
    return (f'<g transform="translate({x} {y}) scale({sc})" fill="#4a2e18"><ellipse cx="0" cy="-60" rx="70" ry="38"/><ellipse cx="-10" cy="-95" rx="30" ry="26"/><path d="M60,-70 q40,-30 40,-90 h22 q4,70 -40,110z"/><ellipse cx="112" cy="-162" rx="22" ry="14"/>'
            + "".join(f'<rect x="{lx}" y="-40" width="12" height="62"/>' for lx in (-50, -30, 30, 48)) + "</g>")
ep = load(); B = ep["beats"]
def scene(i, b, s, e, c0, c1):
    D = c1 - c0; js = []; k = b["k"]; night = k == "night"
    g1, g2 = b["sky"]
    sv = f'<svg class="full" width="1080" height="1920" viewBox="0 0 1080 1920">{DEFS}<linearGradient id="sk{i}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{g1}"/><stop offset="1" stop-color="{g2}"/></linearGradient><rect width="1080" height="1920" fill="url(#sk{i})"/>'
    if night: sv += "".join(f'<circle class="tw{i}" cx="{(R(k2)+1)*540:.0f}" cy="{(R(k2+50)+1)*500:.0f}" r="{3+abs(R(k2+9))*4:.1f}" fill="#fff"/>' for k2 in range(60))
    sx, sy, sc = b["sun"]
    sv += f'<g id="sun{i}"><circle cx="{sx}" cy="{sy}" r="{110 if not night else 80}" fill="{sc}" filter="url(#ps)"/></g>'
    sv += f'<g id="cl{i}" fill="#fff" opacity="{.25 if night else .9}" filter="url(#ps)"><ellipse cx="200" cy="640" rx="150" ry="44"/><ellipse cx="300" cy="610" rx="100" ry="50"/><ellipse cx="860" cy="760" rx="130" ry="36"/></g>'
    far = "#d9a85a" if not night else "#2c2b52"; mid = "#c98f45" if not night else "#24234a"; near = "#a86d30" if not night else "#191a38"
    sv += f'<g id="L1{i}">{dune(1180, 40, i, far)}</g>'
    pyrs = (pyr(560, 1230, 420) + pyr(260, 1260, 230, "#d9ab5a", "#a87a36") + pyr(840, 1270, 180, "#d9ab5a", "#a87a36")) if not night else (pyr(560, 1230, 420, "#3a3970", "#2a2958") + pyr(260, 1260, 230, "#34336a", "#26254f"))
    if k == "build": pyrs = f'<g id="pb{i}">' + "".join(f'<rect class="blk{i}" x="{560-380+ (r_*35) + c*70:.0f}" y="{1230-(r_+1)*70}" width="68" height="68" fill="{["#e3b765","#d6a656"][(r_+c)%2]}" stroke="#a87a36" stroke-width="3"/>' for r_ in range(10) for c in range(max(0, 11-r_))) + "</g>"
    if k == "river": pyrs = pyr(760, 1180, 260) + f'<rect x="-100" y="1240" width="1300" height="200" fill="#3f8fc0" filter="url(#ps)"/><g id="bt{i}"><path d="M0,1250 h300 l-40,60 h-220 z" fill="#6e4424"/><rect x="80" y="1150" width="140" height="100" fill="#cfa25a" stroke="#8a6230" stroke-width="5"/><path d="M150,1250 V1000 L260,1150 Z" fill="#fbf3e0"/></g>'
    sv += f'<g id="L2{i}">{pyrs}</g><g id="L3{i}">{dune(1420, 60, i+3, mid)}</g>'
    if k in ("intro", "tall", "end"): sv += f'<g id="cv{i}">' + camel(-200, 1560, .9) + camel(-450, 1580, .8) + camel(-680, 1570, .85) + "</g>"
    if k == "tall": sv += f'<g id="ruler{i}" opacity="0"><path d="M60,1230 V810" stroke="#c0392b" stroke-width="10"/><path d="M30,810 h60 M30,1230 h60" stroke="#c0392b" stroke-width="10"/><text x="90" y="1000" font-size="64" font-weight="900" fill="#c0392b" font-family="Cairo">{b.get("measure","")}</text></g>'
    sv += f'<g id="L4{i}">{dune(1660, 70, i+7, near)}</g><rect width="1080" height="1920" filter="url(#gr)"/></svg>'
    h = sv + f'<div class="cap" id="cp{i}" style="opacity:0"><span>{b["cap"]}</span></div>'
    js.append(f'tl.fromTo("#cp{i}",{{opacity:0,y:-200,rotation:-6}},{{opacity:1,y:0,rotation:-2,duration:.6,ease:"back.out(1.5)"}},{s:.2f});')
    for L, d in (("L1", 40), ("L2", 90), ("L3", 160), ("L4", 280), ("cl", 120)):   # paper parallax: nearer layers move more
        js.append(f'tl.fromTo("#{L}{i}",{{x:{d/2}}},{{x:{-d/2},duration:{D:.2f},ease:"none"}},{c0:.2f});')
    if i == 0: js += [f'tl.fromTo("#L4{i}",{{y:500}},{{y:0,duration:1,ease:"power3.out"}},0);', f'tl.fromTo("#L3{i}",{{y:400}},{{y:0,duration:1.1,ease:"power3.out"}},.15);', f'tl.fromTo("#L2{i}",{{y:600}},{{y:0,duration:1.2,ease:"back.out(1.2)"}},.3);', f'tl.fromTo("#sun{i}",{{y:300}},{{y:0,duration:1.5,ease:"power2.out"}},0);']
    if k in ("intro", "tall", "end"): js.append(f'tl.fromTo("#cv{i}",{{x:0}},{{x:1500,duration:{D:.2f},ease:"none"}},{c0:.2f});')
    if k == "build": js.append(f'tl.fromTo(".blk{i}",{{y:-1400}},{{y:0,duration:.25,ease:"bounce.out",stagger:{min(.06,(e-s-.6)/65):.3f}}},{s+.2:.2f});')
    if k == "river": js.append(f'tl.fromTo("#bt{i}",{{x:-400}},{{x:500,duration:{D:.2f},ease:"none"}},{c0:.2f});')
    if k == "tall": js += [f'tl.fromTo("#ruler{i}",{{opacity:0,scaleY:0,svgOrigin:"60 1230"}},{{opacity:1,scaleY:1,duration:.6}},{s+1:.2f});', f'tl.fromTo("#sun{i}",{{y:0}},{{y:500,duration:{D:.2f},ease:"none"}},{c0:.2f});']
    if night: js.append(f'tl.fromTo(".tw{i}",{{opacity:.3}},{{opacity:1,duration:.5,stagger:{{each:.05,repeat:-1,yoyo:true}}}},{c0:.2f});')
    return h, js
run("6_paper", B, scene, css=CSS, bg="#f2b46b", bed="drone", rate="-3%")
