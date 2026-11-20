"""Style 9 · cartoon «هل تعلم؟»: 6 characters, 5 backgrounds, 8 scene kinds, 16 icons. JSON -> video. See README.md."""
from lib import *
CSS = ('.cap{position:absolute;left:70px;right:70px;top:210px;text-align:center;font-weight:900;font-size:96px;line-height:1.15;color:#fff;-webkit-text-stroke:14px #0b2a4a;paint-order:stroke fill}'
       '.tag{position:absolute;left:50%;top:90px;transform:translateX(-50%);background:#ffd21f;color:#0b2a4a;font-weight:900;font-size:58px;padding:0 36px 10px;border-radius:40px;border:7px solid #0b2a4a;white-space:nowrap}'
       '.num{position:absolute;left:0;right:0;top:1420px;text-align:center;font-weight:900;font-size:220px;color:#ffd21f;-webkit-text-stroke:16px #0b2a4a;paint-order:stroke fill}')
K = "#0b2a4a"; SW = 'stroke="#0b2a4a" stroke-width="10"'
def eyes(i, xs=(-60, 60), y=-40, r=34):
    return f'<g class="eye{i}">' + "".join(f'<ellipse cx="{x}" cy="{y}" rx="{r}" ry="{r*1.15:.0f}" fill="#fff" {SW}/><circle cx="{x+6}" cy="{y+4}" r="{r*.5:.0f}" fill="{K}"/><circle cx="{x+12}" cy="{y-4}" r="{r*.18:.0f}" fill="#fff"/>' for x in xs) + "</g>"
def mouth(i, x=0, y=40, w=60): return f'<path id="mo{i}" d="M{x-w},{y} Q{x},{y+70} {x+w},{y}" fill="#e85a6a" {SW}/>'
# each character: body around (0,0), size ~ 650 wide; "#wb" bob group, "#tl" wiggle part, eye{i} blink, mo{i} talk
def ch_whale(i):
    return (f'<g id="tl{i}" transform="translate(300 -20) rotate(0)"><path d="M0,0 C80,-40 120,-140 200,-160 C170,-80 180,-30 220,20 C150,10 80,40 0,40Z" fill="#3d8be0" {SW}/></g>'
            f'<path d="M-320,-20 C-320,-200 -60,-250 140,-210 C300,-180 340,-60 320,40 C300,160 120,200 -60,190 C-250,180 -320,120 -320,-20Z" fill="#4aa3f0" stroke="{K}" stroke-width="12"/>'
            '<path d="M-300,60 C-200,170 100,190 300,80 C260,160 120,200 -60,190 C-220,180 -290,130 -300,60Z" fill="#dff1ff"/>' + eyes(i, (-150,), -40) + mouth(i, -160, 40, 90) + '<ellipse cx="-90" cy="20" rx="34" ry="18" fill="#ff9aa8" opacity=".7"/>')
def ch_cat(i):
    return (f'<g id="tl{i}" transform="translate(170 140) rotate(0)"><path d="M0,0 C120,-20 160,-140 120,-240" stroke="{K}" stroke-width="44" fill="none" stroke-linecap="round"/><path d="M0,0 C120,-20 160,-140 120,-240" stroke="#ff9a3a" stroke-width="26" fill="none" stroke-linecap="round"/></g>'
            f'<ellipse cx="0" cy="170" rx="190" ry="150" fill="#ff9a3a" {SW}/><path d="M-210,-180 L-170,-330 L-60,-230Z M210,-180 L170,-330 L60,-230Z" fill="#ff9a3a" {SW}/><path d="M-180,-200 L-165,-290 L-100,-235Z M180,-200 L165,-290 L100,-235Z" fill="#ffc2c2"/>'
            f'<ellipse cx="0" cy="-60" rx="240" ry="200" fill="#ff9a3a" {SW}/><path d="M-60,-250 l20,60 M0,-258 v66 M60,-250 l-20,60" stroke="#c96a1a" stroke-width="14" stroke-linecap="round"/>'
            + eyes(i, (-90, 90), -70, 40) + f'<path d="M-20,10 h40 l-20,22z" fill="#ff6a8a"/>' + mouth(i, 0, 40, 46) +
            f'<path d="M-120,20 h-130 M-120,40 l-120,30 M120,20 h130 M120,40 l120,30" stroke="{K}" stroke-width="6"/>')
def ch_octopus(i):
    legs = "".join(f'<path class="leg{i}" d="M{x},60 C{x+dx},180 {x-dx},260 {x+dx*1.4},340" stroke="{K}" stroke-width="58" fill="none" stroke-linecap="round"/><path d="M{x},60 C{x+dx},180 {x-dx},260 {x+dx*1.4},340" stroke="#c45adb" stroke-width="40" fill="none" stroke-linecap="round"/>' for x, dx in ((-190, -60), (-110, -30), (-30, 20), (50, -20), (130, 40), (200, 60)))
    return (f'<g id="tl{i}" transform="translate(0 0) rotate(0)">{legs}</g><path d="M-240,40 C-280,-280 280,-280 240,40 C160,110 -160,110 -240,40Z" fill="#c45adb" stroke="{K}" stroke-width="12"/>'
            + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#e6a0f0"/>' for x, y, r in ((-120, -170, 26), (100, -200, 18), (150, -120, 22))) + eyes(i, (-80, 80), -40, 40) + mouth(i, 0, 30, 50))
def ch_bee(i):
    return (f'<g id="tl{i}" transform="translate(0 -170) rotate(0)"><ellipse cx="-120" cy="-60" rx="110" ry="160" fill="#dff4ff" fill-opacity=".85" {SW} transform="rotate(-30 -120 -60)"/><ellipse cx="120" cy="-60" rx="110" ry="160" fill="#dff4ff" fill-opacity=".85" {SW} transform="rotate(30 120 -60)"/></g>'
            f'<ellipse cx="0" cy="40" rx="260" ry="200" fill="#ffd21f" stroke="{K}" stroke-width="12"/><clipPath id="bc{i}"><ellipse cx="0" cy="40" rx="255" ry="195"/></clipPath><g clip-path="url(#bc{i})"><rect x="-90" y="-200" width="70" height="480" fill="{K}"/><rect x="60" y="-200" width="70" height="480" fill="{K}"/><rect x="200" y="-200" width="70" height="480" fill="{K}"/></g>'
            f'<path d="M260,40 l70,0 l-70,30z" fill="{K}"/><path d="M-160,-130 q-30,-120 -80,-140 M-60,-150 q10,-120 40,-150" stroke="{K}" stroke-width="10" fill="none"/><circle cx="-240" cy="-270" r="18" fill="{K}"/><circle cx="-20" cy="-300" r="18" fill="{K}"/>'
            f'<circle cx="-150" cy="0" r="120" fill="#ffd21f" {SW}/>' + eyes(i, (-200, -100), -20, 32) + mouth(i, -150, 50, 40))
def ch_penguin(i):
    return (f'<g id="tl{i}" transform="translate(-220 40) rotate(0)"><path d="M0,-80 C-80,-20 -90,120 -40,180 C0,100 20,0 0,-80Z" fill="#1f2a3a" {SW}/></g><path d="M220,-40 C300,20 300,160 250,220 C220,140 200,40 220,-40Z" fill="#1f2a3a" {SW}/>'
            f'<ellipse cx="0" cy="40" rx="240" ry="320" fill="#1f2a3a" stroke="{K}" stroke-width="12"/><ellipse cx="0" cy="90" rx="170" ry="250" fill="#fff"/><ellipse cx="0" cy="-130" rx="170" ry="130" fill="#fff"/>'
            f'<ellipse cx="-80" cy="360" rx="80" ry="30" fill="#ff9a3a" {SW}/><ellipse cx="80" cy="360" rx="80" ry="30" fill="#ff9a3a" {SW}/>'
            + eyes(i, (-70, 70), -150, 34) + f'<path d="M-50,-80 L0,-40 L50,-80 Q0,-110 -50,-80Z" fill="#ff9a3a" {SW}/><path id="mo{i}" d="M-40,-60 Q0,-20 40,-60" fill="#e85a6a" stroke="{K}" stroke-width="6"/>')
def ch_kid(i):
    return (f'<rect x="-70" y="200" width="60" height="200" rx="30" fill="#2b3a55" {SW}/><rect x="10" y="200" width="60" height="200" rx="30" fill="#2b3a55" {SW}/><ellipse cx="-50" cy="405" rx="55" ry="25" fill="{K}"/><ellipse cx="50" cy="405" rx="55" ry="25" fill="{K}"/>'
            f'<path d="M-140,0 Q0,-30 140,0 L120,230 H-120Z" fill="#2fbf6a" {SW}/><rect x="-200" y="20" width="60" height="180" rx="30" fill="#2fbf6a" {SW} transform="rotate(15 -170 30)"/>'
            f'<g id="tl{i}" transform="translate(140 30) rotate(0)"><rect x="0" y="-20" width="60" height="180" rx="30" fill="#2fbf6a" {SW} transform="rotate(-150 30 0)"/><circle cx="60" cy="-150" r="34" fill="#f1c7a0" {SW}/></g>'
            f'<circle cx="0" cy="-200" r="190" fill="#f1c7a0" stroke="{K}" stroke-width="12"/><path d="M-190,-200 Q-200,-400 0,-390 Q200,-400 190,-200 Q150,-320 0,-300 Q-150,-320 -190,-200Z" fill="#3a2414" {SW}/>'
            + eyes(i, (-70, 70), -200, 36) + mouth(i, 0, -110, 50) + '<ellipse cx="-120" cy="-140" rx="30" ry="16" fill="#ff9aa8" opacity=".7"/><ellipse cx="120" cy="-140" rx="30" ry="16" fill="#ff9aa8" opacity=".7"/>')
CHARS = {"whale": ch_whale, "cat": ch_cat, "octopus": ch_octopus, "bee": ch_bee, "penguin": ch_penguin, "kid": ch_kid}
HOME = {"whale": "ocean", "octopus": "ocean", "cat": "room", "bee": "garden", "penguin": "ice", "kid": "garden"}
def bg(name, i):
    if name == "ocean":
        return (f'<linearGradient id="oc{i}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3fb6ff"/><stop offset="1" stop-color="#0a3d7a"/></linearGradient><rect width="1080" height="1920" fill="url(#oc{i})"/>'
                + "".join(f'<path d="M{-100+k*260},0 L{60+k*260},0 L{-200+k*260},1300 L{-360+k*260},1300Z" fill="#fff" opacity=".07"/>' for k in range(6))
                + '<path d="M0,1780 q270,-60 540,0 t540,0 V1920 H0Z" fill="#e8c98a"/><path d="M120,1780 q10,-120 -20,-200 M150,1780 q30,-90 10,-160 M900,1790 q-20,-140 20,-230" stroke="#2f9a6a" stroke-width="18" fill="none" stroke-linecap="round"/>'), "#bfe6ff"
    if name == "garden":
        return ('<rect width="1080" height="1920" fill="#9fe0ff"/><circle cx="880" cy="520" r="110" fill="#ffe27a"/><ellipse cx="250" cy="640" rx="160" ry="50" fill="#fff"/><ellipse cx="330" cy="610" rx="100" ry="50" fill="#fff"/>'
                '<path d="M0,1500 Q540,1380 1080,1500 V1920 H0Z" fill="#6fcf4f" stroke="#0b2a4a" stroke-width="10"/>' + "".join(f'<g transform="translate({x} {y})"><path d="M0,0 V-110" stroke="#2f9a3a" stroke-width="10"/>' + "".join(f'<circle cx="{30*math.cos(a)}" cy="{-110+30*math.sin(a)}" r="24" fill="{c}" stroke="#0b2a4a" stroke-width="5"/>' for a in [k*1.2566 for k in range(5)]) + f'<circle cy="-110" r="20" fill="#ffd21f"/></g>' for x, y, c in ((120, 1660, "#ff6a8a"), (300, 1760, "#fff"), (820, 1700, "#c45adb"), (980, 1800, "#ff6a8a")))), "#ffffff"
    if name == "ice":
        return ('<linearGradient id="ic%d" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#cfefff"/><stop offset="1" stop-color="#7cc6ff"/></linearGradient><rect width="1080" height="1920" fill="url(#ic%d)"/>' % (i, i) +
                '<path d="M-50,1100 L200,700 L380,1000 L560,620 L800,1050 L1000,760 L1150,1100Z" fill="#f4fbff" stroke="#0b2a4a" stroke-width="8"/><rect y="1100" width="1080" height="820" fill="#2b8be0"/><path d="M0,1500 Q540,1420 1080,1500 V1920 H0Z" fill="#f4fbff" stroke="#0b2a4a" stroke-width="10"/>'
                + "".join(f'<circle class="sn{i}" cx="{(R(k)+1)*540:.0f}" cy="{(R(k+40)+1)*700:.0f}" r="{6+abs(R(k+3))*8:.0f}" fill="#fff"/>' for k in range(40))), "#ffffff"
    if name == "room":
        return ('<rect width="1080" height="1920" fill="#ffd9a8"/>' + "".join(f'<rect x="{k*120}" y="0" width="60" height="1500" fill="#ffcf98"/>' for k in range(9)) +
                '<rect y="1500" width="1080" height="420" fill="#c98f45" stroke="#0b2a4a" stroke-width="10"/><rect x="680" y="560" width="300" height="340" fill="#bfe3f5" stroke="#0b2a4a" stroke-width="10"/><path d="M830,560 V900 M680,730 H980" stroke="#0b2a4a" stroke-width="8"/>'
                '<rect x="80" y="700" width="300" height="24" fill="#8a5a33" stroke="#0b2a4a" stroke-width="6"/><rect x="110" y="620" width="40" height="80" fill="#e5322d"/><rect x="160" y="600" width="40" height="100" fill="#2b8be0"/><rect x="210" y="630" width="40" height="70" fill="#2fbf6a"/>'), "#fff3d6"
    return ('<rect width="1080" height="1920" fill="#0b0f2a"/>' + "".join(f'<circle cx="{(R(k)+1)*540:.0f}" cy="{(R(k+70)+1)*960:.0f}" r="{2+abs(R(k+5))*4:.1f}" fill="#fff"/>' for k in range(120)) +
            '<circle cx="880" cy="1650" r="260" fill="#ff8a5a" stroke="#0b2a4a" stroke-width="10"/><circle cx="800" cy="1580" r="40" fill="#e0703f"/><circle cx="950" cy="1720" r="60" fill="#e0703f"/>'), "#bfd0ff"
ICON = {
 "heart": '<path d="M0,60 C-160,-40 -120,-180 0,-110 C120,-180 160,-40 0,60Z" fill="#ff4d6d" {sw}/>',
 "car": '<rect x="-150" y="-80" width="300" height="110" rx="30" fill="#e5322d" {sw}/><path d="M-90,-80 L-50,-150 H60 L100,-80Z" fill="#ffd9d9" {sw}/><circle cx="-80" cy="40" r="38" fill="#333" {sw}/><circle cx="80" cy="40" r="38" fill="#333" {sw}/>',
 "plane": '<path d="M-150,-25 h260 q40,0 40,25 q0,25 -40,25 h-260z" fill="#e8eef5" {sw}/><path d="M-30,-25 l-60,-90 h40 l80,90z M-30,25 l-60,90 h40 l80,-90z" fill="#c9d4e0" {sw}/>',
 "dino": '<path d="M-160,0 C-160,-120 -60,-160 40,-140 L120,-300 C140,-330 190,-320 190,-290 L170,-170 C220,-120 220,0 160,30 L-180,40 C-260,40 -320,20 -380,-20 C-300,-10 -220,0 -160,0Z" fill="#7fbf3f" {sw}/><circle cx="150" cy="-280" r="10" fill="#0b2a4a"/>',
 "house": '<path d="M-150,-40 L0,-170 L150,-40Z" fill="#e5322d" {sw}/><rect x="-120" y="-40" width="240" height="180" fill="#ffd9a8" {sw}/><rect x="-30" y="40" width="60" height="100" fill="#8a5a33" {sw}/>',
 "bus": '<rect x="-180" y="-110" width="360" height="190" rx="24" fill="#ffd21f" {sw}/><rect x="-150" y="-80" width="300" height="70" fill="#bfe3f5" {sw}/><circle cx="-100" cy="90" r="36" fill="#333" {sw}/><circle cx="100" cy="90" r="36" fill="#333" {sw}/>',
 "star": '<path d="M0,-120 L35,-35 L125,-35 L55,20 L80,110 L0,55 L-80,110 L-55,20 L-125,-35 L-35,-35Z" fill="#ffd21f" {sw}/>',
 "apple": '<path d="M0,-70 C-120,-130 -150,40 -60,110 C-30,130 30,130 60,110 C150,40 120,-130 0,-70Z" fill="#e5322d" {sw}/><path d="M0,-70 q10,-50 40,-70" stroke="#0b2a4a" stroke-width="10" fill="none"/>',
 "fish": '<path d="M-130,0 C-60,-90 80,-90 120,0 C80,90 -60,90 -130,0Z M120,0 L190,-60 V60Z" fill="#ff9a3a" {sw}/><circle cx="-70" cy="-10" r="12" fill="#0b2a4a"/>',
 "drop": '<path d="M0,-130 C60,-40 100,20 100,60 A100,100 0 0,1 -100,60 C-100,20 -60,-40 0,-130Z" fill="#4aa3f0" {sw}/>',
 "brain": '<path d="M-130,30 C-170,-60 -100,-140 -20,-120 C20,-170 130,-140 130,-60 C190,-20 160,90 80,100 C40,140 -60,140 -90,100 C-150,100 -170,60 -130,30Z" fill="#ffb3c6" {sw}/><path d="M0,-110 V110 M-80,-40 q40,20 0,60 M80,-40 q-40,20 0,60" stroke="#0b2a4a" stroke-width="7" fill="none"/>',
 "clock": '<circle r="120" fill="#fff" {sw}/><path d="M0,0 V-80 M0,0 L60,30" stroke="#0b2a4a" stroke-width="12" stroke-linecap="round"/>',
 "moon": '<mask id="mm"><rect x="-200" y="-200" width="400" height="400" fill="#fff"/><circle cx="60" cy="-40" r="100" fill="#000"/></mask><circle r="120" fill="#ffe27a" {sw} mask="url(#mm)"/>',
 "leaf": '<path d="M-120,100 C-120,-60 40,-140 140,-120 C140,0 60,140 -120,100Z" fill="#6fcf4f" {sw}/><path d="M-120,100 L100,-90" stroke="#0b2a4a" stroke-width="8"/>',
 "eye": '<path d="M-150,0 Q0,-120 150,0 Q0,120 -150,0Z" fill="#fff" {sw}/><circle r="55" fill="#2b8be0" {sw}/><circle r="22" fill="#0b2a4a"/>',
 "dot": '<path d="M-40,0 q40,-28 80,0 q-40,28 -80,0" fill="#ff8a5a"/>',
}
def icon(n, sc=1): return f'<g transform="scale({sc})">' + ICON[n].replace("{sw}", SW) + "</g>"
def bubbles(i, col): return "".join(f'<circle class="bu{i}" cx="{(R(i*20+k)+1)*540:.0f}" cy="{1900+k*40}" r="{10+abs(R(k+i))*26:.0f}" fill="none" stroke="{col}" stroke-width="5" opacity=".8"/>' for k in range(16))
CX, CY = 560, 1180
def scene(i, b, s, e, c0, c1):
    ep_ch = ep.get("character", "whale"); ch = b.get("character", ep_ch); k = b["k"]; D = c1 - c0; js = []
    back, bub = bg(b.get("bg", ep.get("bg", HOME[ch])), i)
    sv = f'<svg class="full" width="1080" height="1920" viewBox="0 0 1080 1920">{back}{bubbles(i, bub)}'
    cs = b.get("scale", .85 if ch not in ("kid", "penguin") else .75)
    if k == "compare":
        (ia, la), (ib, lb) = b["a"], b["b"]
        sv += (f'<g transform="translate(270 1620)"><g id="ia{i}" transform="scale(0)">{icon(ia, .9)}<text y="190" text-anchor="middle" font-size="60" font-weight="900" fill="#fff" stroke="{K}" stroke-width="10" paint-order="stroke" font-family="Cairo">{la}</text></g></g>'
               f'<text id="eq{i}" x="540" y="1650" font-size="130" font-weight="900" fill="#fff" stroke="{K}" stroke-width="10" paint-order="stroke" text-anchor="middle" opacity="0">{b.get("sign", "=")}</text>'
               f'<g transform="translate(810 1620)"><g id="ib{i}" transform="scale(0)">{icon(ib, .9)}<text y="190" text-anchor="middle" font-size="60" font-weight="900" fill="#fff" stroke="{K}" stroke-width="10" paint-order="stroke" font-family="Cairo">{lb}</text></g></g>')
        cs *= .8
    if k == "rings": sv += "".join(f'<circle class="rw{i}" cx="{CX}" cy="{CY}" r="300" fill="none" stroke="#fff" stroke-width="10" opacity="0"/>' for _ in range(4))
    if k == "swarm": sv += "".join(f'<g class="kr{i}" transform="translate({140 + (n%6)*40} {820 + (n//6)*90 + R(n)*40:.0f})">{icon(b.get("icon", "dot"), b.get("icon_scale", .5))}</g>' for n in range(int(b.get("n", 24))))
    if k == "flyby": sv += f'<g id="fb{i}" transform="translate(-400 640)">{icon(b.get("icon", "plane"))}</g>'
    if k == "grow": sv += f'<g id="gr{i}" transform="translate(840 2300) scale(.6)">{icon(b.get("icon", "dino"), b.get("icon_scale", 1))}</g>'
    sv += f'<g id="wh{i}" transform="translate({CX} {CY}) scale({cs})"><g id="wb{i}" transform="translate(0 0) rotate(0)">{CHARS[ch](i)}</g></g></svg>'
    h = sv + f'<div class="tag">{ep.get("tag", "هل تعلم؟")}</div><div class="cap" id="cp{i}" style="opacity:0">{b["cap"]}</div>'
    if k == "count": h += f'<div class="num" id="nm{i}" style="opacity:0">0</div>'
    js.append(f'tl.fromTo("#cp{i}",{{opacity:0,scale:.3,rotation:-8}},{{opacity:1,scale:1,rotation:0,duration:.45,ease:"elastic.out(1,.5)"}},{s:.2f});')
    js.append(f'tl.fromTo("#S{i} .bu{i}",{{y:0}},{{y:-2100,duration:{D:.2f},stagger:{D/20:.2f},ease:"none"}},{c0:.2f});')
    js.append(f'tl.fromTo("#wb{i}",{{attr:{{transform:"translate(0 -20) rotate(-3)"}}}},{{attr:{{transform:"translate(0 20) rotate(3)"}},duration:1.1,yoyo:true,repeat:{int(D/1.1)},ease:"sine.inOut"}},{c0:.2f});')
    js.append(f'tl.fromTo("#tl{i}",{{rotation:-12}},{{rotation:12,svgOrigin:"0 0",duration:.45,yoyo:true,repeat:{int(D/.45)},ease:"sine.inOut"}},{c0:.2f});' if ch in ("octopus", "kid", "bee") else
              f'tl.fromTo("#tl{i}",{{rotation:-14}},{{rotation:14,duration:.45,yoyo:true,repeat:{int(D/.45)},ease:"sine.inOut",transformOrigin:"0% 50%"}},{c0:.2f});')
    for t in range(int(D / 2.3)): js.append(f'tl.to("#S{i} .eye{i}",{{scaleY:.1,transformOrigin:"50% 50%",duration:.07,yoyo:true,repeat:1}},{c0+1+t*2.3:.2f});')
    js.append(f'tl.fromTo("#mo{i}",{{scaleY:1}},{{scaleY:.5,transformOrigin:"50% 0%",duration:.13,yoyo:true,repeat:{int((e-s)/.13)}}},{s:.2f});')
    if k == "intro" or i == 0: js.append(f'tl.fromTo("#wh{i}",{{attr:{{transform:"translate(1600 {CY}) scale({cs})"}}}},{{attr:{{transform:"translate({CX} {CY}) scale({cs})"}},duration:1,ease:"back.out(1.2)"}},{c0:.2f});')
    if k == "compare": js += [f'tl.to("#ia{i}",{{attr:{{transform:"scale(1)"}},duration:.5,ease:"back.out(2)"}},{s+.8:.2f});', f'tl.to("#eq{i}",{{opacity:1,duration:.2}},{s+1.4:.2f});', f'tl.to("#ib{i}",{{attr:{{transform:"scale(1)"}},duration:.5,ease:"back.out(2)"}},{s+1.6:.2f});', f'tl.to("#ia{i}",{{attr:{{transform:"scale(1.12)"}},duration:.18,yoyo:true,repeat:7}},{s+2.2:.2f});']
    if k == "rings": js.append(f'tl.fromTo("#S{i} .rw{i}",{{attr:{{r:120}},opacity:.9}},{{attr:{{r:900}},opacity:0,duration:1.4,stagger:.7,repeat:1,ease:"power1.out"}},{s+.3:.2f});')
    if k == "swarm": js += [f'tl.to("#S{i} .kr{i}",{{x:{CX-300},y:{CY-850},scale:.2,duration:.6,stagger:.06,ease:"power2.in"}},{s+.6:.2f});', f'tl.to("#S{i} .kr{i}",{{opacity:0,duration:.1,stagger:.06}},{s+1.2:.2f});']
    if k == "flyby": js += [f'tl.fromTo("#fb{i}",{{attr:{{transform:"translate(-400 640)"}}}},{{attr:{{transform:"translate(1500 560)"}},duration:2.4,ease:"none"}},{s+.2:.2f});', f'tl.fromTo("#S{i} svg",{{x:0}},{{x:10,duration:.04,yoyo:true,repeat:15}},{s+1:.2f});']
    if k == "grow": js += [f'tl.to("#gr{i}",{{attr:{{transform:"translate(840 1700) scale(.6)"}},duration:.6,ease:"back.out(1.6)"}},{s+.6:.2f});', f'tl.fromTo("#wh{i}",{{attr:{{transform:"translate({CX} {CY}) scale({cs})"}}}},{{attr:{{transform:"translate({CX-80} {CY-60}) scale({cs*1.3:.2f})"}},duration:1.2,ease:"back.out(1.4)"}},{s+1.4:.2f});']
    if k == "count":
        n = b.get("number", 100)
        js += [f'tl.to("#nm{i}",{{opacity:1,duration:.2}},{s+.4:.2f});', f'const o{i}={{v:0}};tl.to(o{i},{{v:{n},duration:1.6,ease:"power2.out",onUpdate:()=>{{document.getElementById("nm{i}").textContent=Math.round(o{i}.v).toLocaleString("en")+"{b.get("unit", "")}"}}}},{s+.4:.2f});']
    if k == "end": js.append(f'tl.fromTo("#cp{i}",{{scale:1}},{{scale:1.12,duration:.3,yoyo:true,repeat:6}},{s+.6:.2f});')
    return h, js
if __name__ == "__main__":
    ep = load(); B = ep["beats"]
    run("cartoon", B, scene, css=CSS, bg="#0a3d7a", rate="+5%",
        extra_sfx=lambda sch: [{"file": "sfx/bell.wav", "at": round(s + .1, 2), "gain": .12} for s, e in sch])
