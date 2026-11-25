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

LANDS = {"desert": ("#d9a85a", "#c98f45", "#a86d30"), "green": ("#8fcf6a", "#6fb04a", "#4a8a3a"), "snow": ("#e8f4ff", "#cfe4f5", "#b0d0ea"), "autumn": ("#e8a050", "#d07a30", "#a85a20"),
         "ocean": ("#5ab0e0", "#3a90c8", "#2a70a8"), "rock": ("#b0a090", "#8a7a6a", "#6a5a4a"), "jungle": ("#4fae5a", "#2f8a3a", "#1f6a2a"), "pink": ("#f0b0c8", "#e090b0", "#c07090"), "night": ("#2c2b52", "#24234a", "#191a38")}
TIMES = {"day": (("#cfe7f2", "#9ccbe0"), (820, 460, "#fffbe8")), "dawn": (("#ffd9b0", "#f7b0a0"), (300, 760, "#fff1c4")), "noon": (("#f7d79b", "#f2b46b"), (780, 420, "#fff1c4")),
         "sunset": (("#f5c27a", "#e2793f"), (540, 820, "#ffd27a")), "dusk": (("#7a5aa8", "#e28a6a"), (540, 900, "#ffb07a")), "night": (("#1b2347", "#3b3f75"), (820, 420, "#f4f1d0"))}
def P(pts, c): return f'<polygon points="{pts}" fill="{c}" filter="url(#ps)"/>'
def lm_mountains(c1, c2): return P("-100,1240 200,700 420,1240", c2) + P("200,1240 560,560 900,1240", c1) + P("560,1240 860,780 1180,1240", c2) + P("515,640 560,560 610,650 575,630 545,665", "#fff")
def lm_city(c1, c2): return "".join(f'<rect x="{x}" y="{1240-h}" width="{w}" height="{h}" fill="{c1 if k%2 else c2}" filter="url(#ps)"/>' + "".join(f'<rect x="{x+16+cc*44}" y="{1240-h+30+rr*70}" width="22" height="34" fill="#fff3b0" opacity=".8"/>' for rr in range(int((h-60)/70)) for cc in range(int((w-20)/44))) for k, (x, w, h) in enumerate(((60, 160, 420), (230, 130, 620), (370, 180, 360), (560, 150, 700), (720, 190, 460), (920, 140, 560))))
def lm_castle(c1, c2): return (f'<rect x="300" y="820" width="480" height="420" fill="{c1}" filter="url(#ps)"/>' + "".join(f'<rect x="{x}" y="660" width="120" height="580" fill="{c2}" filter="url(#ps)"/><polygon points="{x-20},660 {x+60},520 {x+140},660" fill="#c0392b" filter="url(#ps)"/>' for x in (240, 720)) +
                               f'<path d="M480,1240 V1080 a60,60 0 0,1 120,0 V1240Z" fill="#5a3a22"/>' + "".join(f'<rect x="{300+k*60}" y="790" width="34" height="34" fill="{c1}"/>' for k in range(8)))
def lm_mosque(c1, c2): return (f'<rect x="270" y="960" width="540" height="280" fill="{c1}" filter="url(#ps)"/><path d="M380,960 C380,760 700,760 700,960Z" fill="{c2}" filter="url(#ps)"/><path d="M540,790 v-60" stroke="#f2c94c" stroke-width="10"/><circle cx="540" cy="718" r="14" fill="#f2c94c"/>'
                               + "".join(f'<rect x="{x}" y="620" width="54" height="620" fill="{c1}" filter="url(#ps)"/><polygon points="{x},620 {x+27},520 {x+54},620" fill="{c2}" filter="url(#ps)"/>' for x in (180, 846)) + "".join(f'<path d="M{x},1240 v-90 a35,35 0 0,1 70,0 v90Z" fill="#5a3a22" opacity=".6"/>' for x in (330, 505, 680)))
def lm_lighthouse(c1, c2): return (P("200,1240 860,1240 760,1150 300,1150", "#8a7a6a") + f'<polygon points="470,1150 610,1150 590,640 490,640" fill="#fff" filter="url(#ps)"/>' + "".join(f'<polygon points="{478+k*5},{1060-k*140} {602-k*5},{1060-k*140} {598-k*5},{1000-k*140} {482+k*5},{1000-k*140}" fill="#e5322d"/>' for k in range(3))
                                   + '<rect x="480" y="560" width="120" height="80" fill="#fff3b0" filter="url(#ps)"/><polygon points="470,560 540,490 610,560" fill="#e5322d"/><polygon id="beam" points="600,600 1100,520 1100,680" fill="#fff8c0" opacity=".45"/>')
def lm_windmill(c1, c2): return f'<polygon points="470,1240 610,1240 580,820 500,820" fill="{c1}" filter="url(#ps)"/><polygon points="490,820 540,740 590,820" fill="#c0392b"/><g id="blade" transform="translate(540 820)">' + "".join(f'<rect x="-22" y="-300" width="44" height="300" fill="#fbf3e0" filter="url(#ps)" transform="rotate({a})"/>' for a in (0, 90, 180, 270)) + '</g>'
def lm_volcano(c1, c2): return P("60,1240 420,640 660,640 1020,1240", c1) + P("420,640 470,560 540,620 610,550 660,640", "#ff5a1a") + "".join(f'<circle class="smk" cx="{540+R(k)*60:.0f}" cy="{500-k*70}" r="{50+k*10}" fill="#6a6a6a" opacity=".5"/>' for k in range(5))
def lm_bridge(c1, c2): return f'<rect x="-50" y="1100" width="1180" height="40" fill="{c2}" filter="url(#ps)"/>' + "".join(f'<rect x="{x}" y="700" width="50" height="540" fill="{c1}" filter="url(#ps)"/>' for x in (260, 770)) + f'<path d="M-50,1100 Q285,780 285,700 Q540,1060 795,700 Q795,780 1130,1100" fill="none" stroke="{c1}" stroke-width="14"/>'
def lm_tower(c1, c2): return f'<polygon points="380,1240 700,1240 560,560 520,560" fill="{c1}" filter="url(#ps)"/><path d="M430,1240 Q540,1000 650,1240" fill="#cfe7f2"/><rect x="450" y="980" width="180" height="24" fill="{c2}"/><rect x="490" y="780" width="100" height="20" fill="{c2}"/><path d="M540,560 V480" stroke="{c1}" stroke-width="10"/>'
def lm_temple(c1, c2): return P("240,820 840,820 540,680", c2) + f'<rect x="240" y="820" width="600" height="40" fill="{c1}" filter="url(#ps)"/>' + "".join(f'<rect x="{x}" y="860" width="50" height="340" fill="#fbf3e0" filter="url(#ps)"/>' for x in range(270, 800, 100)) + f'<rect x="220" y="1200" width="640" height="40" fill="{c1}" filter="url(#ps)"/>'
def lm_forest(c1, c2): return "".join(f'<polygon points="{x},{1240-h} {x-h*.35:.0f},1240 {x+h*.35:.0f},1240" fill="{c1 if k%2 else c2}" filter="url(#ps)"/>' for k, (x, h) in enumerate(((100, 420), (260, 560), (420, 380), (560, 640), (720, 460), (880, 580), (1010, 400))))
def lm_village(c1, c2): return "".join(f'<rect x="{x}" y="{1240-h}" width="{w}" height="{h}" fill="{c1}" filter="url(#ps)"/><polygon points="{x-20},{1240-h} {x+w/2:.0f},{1240-h-90} {x+w+20},{1240-h}" fill="#c0392b" filter="url(#ps)"/><rect x="{x+w/2-25:.0f}" y="{1170}" width="50" height="70" fill="#5a3a22"/>' for x, w, h in ((90, 200, 200), (380, 240, 260), (720, 220, 190)))
def lm_oasis(c1, c2): return '<ellipse cx="540" cy="1230" rx="360" ry="50" fill="#3f8fc0" filter="url(#ps)"/>' + "".join(f'<path d="M{x},1230 Q{x+20},1000 {x+40},900" stroke="#7a4a24" stroke-width="22" fill="none"/>' + "".join(f'<path d="M{x+40},900 q{dx},-60 {dx*2},{20}" stroke="#2f8a3a" stroke-width="30" fill="none" stroke-linecap="round"/>' for dx in (-90, -50, 50, 90)) for x in (240, 640, 780))
def lm_igloo(c1, c2): return '<path d="M300,1240 A240,240 0 0,1 780,1240Z" fill="#fff" filter="url(#ps)"/>' + "".join(f'<path d="M{330+k*20},{1240-k*60} H{750-k*20}" stroke="#bfd8ee" stroke-width="5"/>' for k in range(1, 4)) + '<path d="M480,1240 v-60 a60,60 0 0,1 120,0 v60Z" fill="#3a5a7a"/>'
def lm_ship(c1, c2): return P("200,1180 880,1180 800,1260 280,1260", "#6e4424") + '<path d="M540,1180 V700" stroke="#5a3a22" stroke-width="16"/><path d="M540,720 Q760,900 540,1130Z" fill="#fbf3e0" filter="url(#ps)"/><path d="M540,760 Q360,920 540,1120Z" fill="#f4e3c4" filter="url(#ps)"/>'
def lm_wall(c1, c2): return P("-100,1240 -100,1000 200,940 500,1000 800,930 1180,1010 1180,1240", c2) + "".join(f'<rect x="{x}" y="{y}" width="90" height="140" fill="{c1}" filter="url(#ps)"/>' for x, y in ((180, 860), (480, 880), (780, 850)))
LANDMARKS = {"pyramids": None, "mountains": lm_mountains, "city": lm_city, "castle": lm_castle, "mosque": lm_mosque, "lighthouse": lm_lighthouse, "windmill": lm_windmill, "volcano": lm_volcano, "bridge": lm_bridge,
             "tower": lm_tower, "temple": lm_temple, "forest": lm_forest, "village": lm_village, "oasis": lm_oasis, "igloo": lm_igloo, "ship": lm_ship, "great_wall": lm_wall, "none": lambda a, b: ""}
def bird(x, y, s=1): return f'<path transform="translate({x} {y}) scale({s})" d="M-40,0 q20,-24 40,0 q20,-24 40,0" stroke="#3a2412" stroke-width="7" fill="none"/>'
EXTRAS = {
 "camels": lambda: camel(-200, 1560, .9) + camel(-450, 1580, .8) + camel(-680, 1570, .85),
 "birds": lambda: "".join(bird(-100 - k * 90, 500 + (k % 2) * 40, .9) for k in range(5)),
 "balloon": lambda: '<g transform="translate(-150 700)"><path d="M0,-180 C110,-180 120,-40 30,40 H-30 C-120,-40 -110,-180 0,-180Z" fill="#e5322d" filter="url(#ps)"/><rect x="-30" y="70" width="60" height="50" fill="#8a5a33"/><path d="M-30,40 L-30,70 M30,40 L30,70" stroke="#3a2412" stroke-width="4"/></g>',
 "cars": lambda: "".join(f'<g transform="translate({-200-k*320} 1600)"><rect x="-90" y="-60" width="180" height="60" rx="18" fill="{c}" filter="url(#ps)"/><path d="M-50,-60 l20,-40 h60 l20,40z" fill="{c}"/><circle cx="-50" cy="0" r="20" fill="#222"/><circle cx="50" cy="0" r="20" fill="#222"/></g>' for k, c in enumerate(("#e5322d", "#2b8be0", "#ffd21f"))),
 "train": lambda: '<g transform="translate(-900 1560)">' + "".join(f'<rect x="{k*230}" y="-110" width="210" height="110" rx="12" fill="{"#c0392b" if k == 3 else "#24456b"}" filter="url(#ps)"/><circle cx="{k*230+50}" cy="0" r="22" fill="#222"/><circle cx="{k*230+160}" cy="0" r="22" fill="#222"/>' for k in range(4)) + '</g>',
 "sheep": lambda: "".join(f'<g transform="translate({-150-k*200} 1600)"><ellipse rx="70" ry="46" fill="#fff" filter="url(#ps)"/><circle cx="66" cy="-14" r="24" fill="#3a3a3a"/></g>' for k in range(4)),
 "plane": lambda: '<g transform="translate(-300 560)"><path d="M-120,0 h220 q30,0 30,20 q0,20 -30,20 h-220z" fill="#fbf3e0" filter="url(#ps)"/><path d="M0,0 l-40,-70 h30 l60,70z" fill="#e8dcc0"/></g>',
 "kite": lambda: '<g transform="translate(-150 640)"><polygon points="0,-90 60,0 0,110 -60,0" fill="#ffd21f" filter="url(#ps)"/><path d="M0,110 q40,80 0,160 q-40,80 0,160" stroke="#c0392b" stroke-width="5" fill="none"/></g>',
 "boats": lambda: "".join(f'<g transform="translate({-200-k*380} 1300)"><path d="M-100,0 h200 l-30,40 h-140z" fill="#6e4424" filter="url(#ps)"/><path d="M0,0 V-150 L80,-20Z" fill="#fbf3e0"/></g>' for k in range(2)),
 "people": lambda: "".join(f'<g transform="translate({-100-k*160} 1610)"><circle cy="-120" r="24" fill="#3a2412"/><path d="M-26,-90 h52 l10,90 h-72z" fill="{c}"/></g>' for k, c in enumerate(("#c0392b", "#24456b", "#2f8a3a"))),
 "snowfall": lambda: "".join(f'<circle class="sf" cx="{(R(k)+1)*540:.0f}" cy="{(R(k+20)+1)*500:.0f}" r="{5+abs(R(k+3))*6:.0f}" fill="#fff"/>' for k in range(60)),
 "leaves": lambda: "".join(f'<ellipse class="sf" cx="{(R(k)+1)*540:.0f}" cy="{(R(k+20)+1)*500:.0f}" rx="14" ry="7" fill="{["#e8a050", "#c0392b", "#ffd21f"][k%3]}"/>' for k in range(30)),
}

def scene(i, b, s, e, c0, c1):
    D = c1 - c0; js = []; k = b.get("k", "scene"); tm = b.get("time", "night" if k == "night" else "noon"); night = tm == "night" or k == "night"
    (g1, g2), sun = b.get("sky") and (b["sky"], b.get("sun") or TIMES[tm][1]) or TIMES[tm]; b = dict(b); b["sun"] = b.get("sun") or sun
    land = LANDS["night"] if night else LANDS.get(b.get("land", ep.get("land", "desert")), LANDS["desert"]); lmk = b.get("landmark", ep.get("landmark", "pyramids"))
    sv = f'<svg class="full" width="1080" height="1920" viewBox="0 0 1080 1920">{DEFS}<linearGradient id="sk{i}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{g1}"/><stop offset="1" stop-color="{g2}"/></linearGradient><rect width="1080" height="1920" fill="url(#sk{i})"/>'
    if night: sv += "".join(f'<circle class="tw{i}" cx="{(R(k2)+1)*540:.0f}" cy="{(R(k2+50)+1)*500:.0f}" r="{3+abs(R(k2+9))*4:.1f}" fill="#fff"/>' for k2 in range(60))
    sx, sy, sc = b["sun"]
    sv += f'<g id="sun{i}"><circle cx="{sx}" cy="{sy}" r="{110 if not night else 80}" fill="{sc}" filter="url(#ps)"/></g>'
    sv += f'<g id="cl{i}" fill="#fff" opacity="{.25 if night else .9}" filter="url(#ps)"><ellipse cx="200" cy="640" rx="150" ry="44"/><ellipse cx="300" cy="610" rx="100" ry="50"/><ellipse cx="860" cy="760" rx="130" ry="36"/></g>'
    far, mid, near = land
    sv += f'<g id="L1{i}">{dune(1180, 40, i, far)}</g>'
    pyrs = (pyr(560, 1230, 420) + pyr(260, 1260, 230, "#d9ab5a", "#a87a36") + pyr(840, 1270, 180, "#d9ab5a", "#a87a36")) if not night else (pyr(560, 1230, 420, "#3a3970", "#2a2958") + pyr(260, 1260, 230, "#34336a", "#26254f"))
    if lmk != "pyramids": pyrs = LANDMARKS[lmk](near if not night else "#3a3970", mid if not night else "#2a2958")
    if k == "build": pyrs = f'<g id="pb{i}">' + "".join(f'<rect class="blk{i}" x="{560-380+ (r_*35) + c*70:.0f}" y="{1230-(r_+1)*70}" width="68" height="68" fill="{["#e3b765","#d6a656"][(r_+c)%2]}" stroke="#a87a36" stroke-width="3"/>' for r_ in range(10) for c in range(max(0, 11-r_))) + "</g>"
    if k == "river": pyrs = pyr(760, 1180, 260) + f'<rect x="-100" y="1240" width="1300" height="200" fill="#3f8fc0" filter="url(#ps)"/><g id="bt{i}"><path d="M0,1250 h300 l-40,60 h-220 z" fill="#6e4424"/><rect x="80" y="1150" width="140" height="100" fill="#cfa25a" stroke="#8a6230" stroke-width="5"/><path d="M150,1250 V1000 L260,1150 Z" fill="#fbf3e0"/></g>'
    sv += f'<g id="L2{i}">{pyrs}</g><g id="L3{i}">{dune(1420, 60, i+3, mid)}</g>'
    ex = b.get("extras", ["camels"] if k in ("intro", "tall", "end") and lmk == "pyramids" else [])
    for n_, x_ in enumerate(ex): sv += f'<g id="ex{i}_{n_}">{EXTRAS[x_]()}</g>' 
    if k == "tall": sv += f'<g id="ruler{i}" opacity="0"><path d="M60,1230 V810" stroke="#c0392b" stroke-width="10"/><path d="M30,810 h60 M30,1230 h60" stroke="#c0392b" stroke-width="10"/><text x="90" y="1000" text-anchor="end" font-size="64" font-weight="900" fill="#c0392b" font-family="Cairo">{b.get("measure","")}</text></g>'
    sv += f'<g id="L4{i}">{dune(1660, 70, i+7, near)}</g><rect width="1080" height="1920" filter="url(#gr)"/></svg>'
    h = sv + f'<div class="cap" id="cp{i}" style="opacity:0"><span>{b["cap"]}</span></div>'
    js.append(f'tl.fromTo("#cp{i}",{{opacity:0,y:-200,rotation:-6}},{{opacity:1,y:0,rotation:-2,duration:.6,ease:"back.out(1.5)"}},{s:.2f});')
    for L, d in (("L1", 40), ("L2", 90), ("L3", 160), ("L4", 280), ("cl", 120)):   # paper parallax: nearer layers move more
        js.append(f'tl.fromTo("#{L}{i}",{{x:{d/2}}},{{x:{-d/2},duration:{D:.2f},ease:"none"}},{c0:.2f});')
    if i == 0: js += [f'tl.fromTo("#L4{i}",{{y:500}},{{y:0,duration:1,ease:"power3.out"}},0);', f'tl.fromTo("#L3{i}",{{y:400}},{{y:0,duration:1.1,ease:"power3.out"}},.15);', f'tl.fromTo("#L2{i}",{{y:600}},{{y:0,duration:1.2,ease:"back.out(1.2)"}},.3);', f'tl.fromTo("#sun{i}",{{y:300}},{{y:0,duration:1.5,ease:"power2.out"}},0);']
    for n_, x_ in enumerate(ex):
        if x_ in ("snowfall", "leaves"): js.append(f'tl.fromTo("#ex{i}_{n_} .sf",{{y:-400}},{{y:1600,duration:4,repeat:{int(D/4)+1},ease:"none",stagger:.05}},{c0:.2f});')
        else: js.append(f'tl.fromTo("#ex{i}_{n_}",{{x:0}},{{x:{1500 if x_ != "train" else 2200},duration:{D:.2f},ease:"none"}},{c0:.2f});')
    if lmk == "windmill": js.append(f'tl.fromTo("#S{i} #blade",{{rotation:0}},{{rotation:360,svgOrigin:"540 820",duration:{D:.2f},ease:"none"}},{c0:.2f});')
    if lmk == "volcano": js.append(f'tl.fromTo("#S{i} .smk",{{y:0,opacity:.5}},{{y:-300,opacity:0,duration:2,repeat:{int(D/2)},stagger:.3}},{c0:.2f});')
    if k == "build": js.append(f'tl.fromTo(".blk{i}",{{y:-1400}},{{y:0,duration:.25,ease:"bounce.out",stagger:{min(.06,(e-s-.6)/65):.3f}}},{s+.2:.2f});')
    if k == "river": js.append(f'tl.fromTo("#bt{i}",{{x:-400}},{{x:500,duration:{D:.2f},ease:"none"}},{c0:.2f});')
    if k == "tall": js += [f'tl.fromTo("#ruler{i}",{{opacity:0,scaleY:0,svgOrigin:"60 1230"}},{{opacity:1,scaleY:1,duration:.6}},{s+1:.2f});', f'tl.fromTo("#sun{i}",{{y:0}},{{y:500,duration:{D:.2f},ease:"none"}},{c0:.2f});']
    if night: js.append(f'tl.fromTo(".tw{i}",{{opacity:.3}},{{opacity:1,duration:.5,stagger:{{each:.05,repeat:-1,yoyo:true}}}},{c0:.2f});')
    return h, js
run("paper", B, scene, css=CSS, bg="#f2b46b", bed="drone", rate="-3%")
