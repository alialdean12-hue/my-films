from lib import *
CSS = '.cap{position:absolute;left:80px;right:80px;top:250px;text-align:center;font-weight:900;font-size:92px;line-height:1.2;color:#151515}.n{display:inline-block;background:#e5322d;color:#fff;border-radius:60px;padding:0 34px 10px;margin-bottom:14px;font-size:80px}'
# stick figure: poses as angles (deg) for [larm_up, larm_lo, rarm_up, rarm_lo, lleg_up, lleg_lo, rleg_up, rleg_lo]; 0 = straight down
POSE = {
 "stand": [15, 0, -15, 0, 8, 0, -8, 0], "panic": [150, 30, -150, -30, 20, 10, -20, -10], "phone": [40, 140, -15, 0, 8, 0, -8, 0],
 "press": [10, 0, -80, -10, 8, 0, -8, 0], "sit": [30, 40, -30, -40, 80, -80, -80, 80], "wave": [15, 0, -125, -40, 8, 0, -8, 0],
 "breathe": [60, 90, -60, -90, 8, 0, -8, 0], "no": [100, 60, -100, -60, 8, 0, -8, 0],
}
def seg(id_, x, y, a, L):  # a = angle from straight down (deg)
    return f'<g id="{id_}" transform="translate({x} {y}) rotate({a})"><path d="M0,0 V{L}" stroke="#151515" stroke-width="16" stroke-linecap="round"/>'
def man(i, x, y, pose, face=":)"):
    p = POSE[pose]; s = ""
    s += f'<g id="man{i}" transform="translate({x} {y})">'
    s += '<circle cx="0" cy="-260" r="62" fill="#fff" stroke="#151515" stroke-width="14"/>'
    s += {"ok": '<circle cx="-20" cy="-270" r="7"/><circle cx="20" cy="-270" r="7"/><path d="M-22,-240 Q0,-222 22,-240" stroke="#151515" stroke-width="7" fill="none"/>',
          "fear": '<circle cx="-20" cy="-272" r="9"/><circle cx="20" cy="-272" r="9"/><ellipse cx="0" cy="-232" rx="14" ry="18" fill="#151515"/>',
          "calm": '<path d="M-30,-270 h20 M10,-270 h20" stroke="#151515" stroke-width="7"/><path d="M-18,-240 Q0,-230 18,-240" stroke="#151515" stroke-width="7" fill="none"/>'}[face]
    s += '<path d="M0,-198 V0" stroke="#151515" stroke-width="16" stroke-linecap="round"/>'
    for side, (ux, uy) in enumerate(((0, -170), (0, -170))):
        a1, a2 = p[side*2], p[side*2+1]
        s += seg(f"a{side}u{i}", 0, -170, a1, 95) + seg(f"a{side}l{i}", 0, 95, a2, 90) + "</g></g>"
    for side in range(2):
        a1, a2 = p[4+side*2], p[5+side*2]
        s += seg(f"l{side}u{i}", 0, 0, a1, 110) + seg(f"l{side}l{i}", 0, 110, a2, 110) + "</g></g>"
    return s + "</g>"
def to_pose(i, pose, at, d=.35):
    p = POSE[pose]; ids = ["a0u", "a0l", "a1u", "a1l", "l0u", "l0l", "l1u", "l1l"]; js = []
    base = {"a0u": (0, -170), "a0l": (0, 95), "a1u": (0, -170), "a1l": (0, 95), "l0u": (0, 0), "l0l": (0, 110), "l1u": (0, 0), "l1l": (0, 110)}
    for k, n in enumerate(ids):
        bx, by = base[n]; js.append(f'tl.to("#{n}{i}",{{attr:{{transform:"translate({bx} {by}) rotate({p[k]})"}},duration:{d},ease:"back.out(1.6)"}},{at:.2f});')
    return js
def lift(inner):  # elevator interior
    return ('<svg class="full" width="1080" height="1920" viewBox="0 0 1080 1920"><rect width="1080" height="1920" fill="#f4f1ea"/>'
            '<rect x="150" y="560" width="780" height="1180" fill="#dcd6c8" stroke="#151515" stroke-width="12"/><path d="M540,560 V1740" stroke="#151515" stroke-width="6" stroke-dasharray="20 14"/>'
            '<rect x="820" y="900" width="80" height="260" rx="14" fill="#fff" stroke="#151515" stroke-width="8"/>' + "".join(f'<circle cx="860" cy="{940+k*60}" r="18" fill="{"#e5322d" if k==3 else "#fff"}" stroke="#151515" stroke-width="5"/>' for k in range(4)) + inner + "</svg>")
ep = load(); B = ep["beats"]
def scene(i, b, s, e, c0, c1):
    js = []; extra = ""
    fx = b["fx"]
    if fx == "air": extra = "".join(f'<circle class="air{i}" cx="{300+k*120}" cy="1500" r="{20+k%3*8}" fill="none" stroke="#7ab0c8" stroke-width="6" opacity="0"/>' for k in range(5))
    if fx == "bell": extra = f'<g id="bl{i}" transform="translate(700 760)" opacity="0"><path d="M-50,40 Q-50,-50 0,-60 Q50,-50 50,40 Z" fill="#f2c94c" stroke="#151515" stroke-width="7"/><path d="M-80,-60 q-20,30 0,60 M80,-60 q20,30 0,60" stroke="#151515" stroke-width="7" fill="none"/></g>'
    if fx == "cross": extra = f'<g id="cx{i}" opacity="0"><path d="M440,700 L640,900 M640,700 L440,900" stroke="#e5322d" stroke-width="30" stroke-linecap="round"/></g>'
    if fx == "clock": extra = f'<g transform="translate(700 760)"><circle r="80" fill="#fff" stroke="#151515" stroke-width="8"/><path id="hd{i}" d="M0,0 V-60" stroke="#151515" stroke-width="8" stroke-linecap="round" transform="rotate(0)"/></g>'
    if fx == "open": extra = f'<rect id="dl{i}" x="150" y="560" width="390" height="1180" fill="#b8b2a4" stroke="#151515" stroke-width="8"/><rect id="dr{i}" x="540" y="560" width="390" height="1180" fill="#b8b2a4" stroke="#151515" stroke-width="8"/>'
    y = 1560 if b["pose"] != "sit" else 1660
    body = lift((extra if fx != "open" else "") + man(i, 420, y, "stand", b["face"]) + (extra if fx == "open" else ""))
    h = body + f'<div class="cap" id="cp{i}" style="opacity:0">{b["cap"]}</div>'
    js.append(f'tl.fromTo("#cp{i}",{{opacity:0,scale:.6}},{{opacity:1,scale:1,duration:.35,ease:"back.out(2)"}},{s:.2f});')
    js += to_pose(i, b["pose"], s + .3)
    if b["pose"] == "sit": js.append(f'tl.fromTo("#man{i}",{{attr:{{transform:"translate(420 1560)"}}}},{{attr:{{transform:"translate(420 1660)"}},duration:.4}},{s+.3:.2f});')
    if fx == "shake": js.append(f'tl.fromTo("#S{i} svg",{{x:0}},{{x:16,duration:.05,yoyo:true,repeat:11}},{s+.2:.2f});'); js += to_pose(i, "no", s + 1.2, .2) + to_pose(i, "panic", s + 1.5, .2)
    if fx == "air": js.append(f'tl.fromTo(".air{i}",{{opacity:.9,y:0}},{{opacity:0,y:-600,duration:2,stagger:.3,ease:"none"}},{s+.5:.2f});'); js += to_pose(i, "stand", s + 1.6, .8) + to_pose(i, "breathe", s + 2.6, .8)
    if fx == "bell": js.append(f'tl.fromTo("#bl{i}",{{opacity:1,rotation:-15}},{{rotation:15,duration:.1,yoyo:true,repeat:13,svgOrigin:"700 700"}},{s+.8:.2f});'); js += to_pose(i, "phone", s + 2.4)
    if fx == "cross": js.append(f'tl.fromTo("#cx{i}",{{opacity:0,scale:2}},{{opacity:1,scale:1,duration:.25,ease:"back.out(2)",svgOrigin:"540 800"}},{s+.9:.2f});')
    if fx == "clock": js.append(f'tl.to("#hd{i}",{{attr:{{transform:"rotate(720)"}},duration:{e-s:.2f},ease:"none"}},{s:.2f});')
    if fx == "open": js += [f'tl.fromTo("#dl{i}",{{x:0}},{{x:-380,duration:.8,ease:"power2.inOut"}},{s+.3:.2f});', f'tl.fromTo("#dr{i}",{{x:0}},{{x:380,duration:.8,ease:"power2.inOut"}},{s+.3:.2f});']
    # walk-bounce
    js.append(f'tl.fromTo("#S{i} .cap",{{y:0}},{{y:-8,duration:.6,yoyo:true,repeat:{int((c1-c0)/.6)}}},{s+.4:.2f});')
    return h, js
run("7_stick", B, scene, css=CSS, bg="#f4f1ea", rate="+0%",
    extra_sfx=lambda sch: [{"file": "sfx/bell.wav", "at": round(sch[2][0] + .8, 2), "gain": .2}, {"file": "sfx/hit.wav", "at": round(sch[3][0] + .9, 2), "gain": .25}])
