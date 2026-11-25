"""Style 8 · anime: code-drawn anime shots (sky, city, close-up faces, back view, running, rain, petals). JSON -> video. See README.md / CATALOG.md."""
from lib import *
CSS = ('.sub{position:absolute;left:70px;right:70px;top:1500px;text-align:center;font-weight:800;font-size:64px;line-height:1.35;color:#fff;text-shadow:0 0 12px #000,0 4px 0 #000}'
       '.ttl{position:absolute;left:60px;right:60px;top:760px;text-align:center;font-weight:900;font-size:150px;line-height:1.1;color:#fff;text-shadow:0 0 40px #ff4d6d,0 6px 0 #000}')
SKIES = {"night": ("#0b0820", "#2a1650", "#5a2a6a"), "sunset": ("#2a1a4a", "#c8456a", "#ffb07a"), "day": ("#3a8ad8", "#8fd0ff", "#e8f6ff"), "dawn": ("#2a3a7a", "#e88aa0", "#ffd9b0"),
         "storm": ("#101018", "#2a2a3a", "#4a4a5a"), "dusk": ("#141a3a", "#4a3a8a", "#e07a6a"), "space": ("#000005", "#0a0a2a", "#1a1040")}
HAIR = {"black": ("#1a1020", "#3a2a4a"), "brown": ("#4a2a18", "#7a4a2a"), "blonde": ("#e8c070", "#fff0b0"), "pink": ("#ff7ab6", "#ffc0dc"), "blue": ("#2a4ad0", "#7aa8ff"), "silver": ("#b8c0d8", "#ffffff"), "red": ("#c0302a", "#ff7a6a"), "green": ("#2a8a5a", "#7ae0a8")}
EYES = {"brown": "#7a4a2a", "blue": "#2a7ae0", "green": "#2aa86a", "red": "#e0303a", "gold": "#e8a820", "purple": "#8a4ae0"}
def defs(i, sky):
    a, b, c = SKIES.get(sky, SKIES["night"])
    return (f'<defs><linearGradient id="sk{i}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{a}"/><stop offset=".6" stop-color="{b}"/><stop offset="1" stop-color="{c}"/></linearGradient>'
            f'<radialGradient id="gl{i}"><stop offset="0" stop-color="#fff" stop-opacity=".9"/><stop offset=".3" stop-color="#ffe7c0" stop-opacity=".35"/><stop offset="1" stop-color="#ffe7c0" stop-opacity="0"/></radialGradient>'
            f'<linearGradient id="lk{i}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ff9a6a" stop-opacity=".5"/><stop offset=".5" stop-color="#ff4d6d" stop-opacity="0"/></linearGradient></defs>')
def sky(i, kind):
    s = f'<rect width="1080" height="1920" fill="url(#sk{i})"/>'
    if kind in ("night", "dusk", "space", "dawn"): s += "".join(f'<circle class="tw{i}" cx="{(R(k)+1)*540:.0f}" cy="{(R(k+77)+1)*600:.0f}" r="{1+abs(R(k+3))*3:.1f}" fill="#fff" opacity="{.4+abs(R(k+9))*.6:.2f}"/>' for k in range(140))
    if kind in ("night", "dusk", "space"): s += f'<circle cx="780" cy="480" r="300" fill="url(#gl{i})"/><circle cx="780" cy="480" r="120" fill="#fff4dc"/>'
    if kind in ("sunset", "dawn", "day"): s += f'<circle cx="540" cy="{1000 if kind != "day" else 420}" r="420" fill="url(#gl{i})"/><circle cx="540" cy="{1000 if kind != "day" else 420}" r="150" fill="#fff2d0"/>'
    if kind in ("day", "sunset", "dawn"): s += "".join(f'<g class="cd{i}" opacity=".85"><ellipse cx="{x}" cy="{y}" rx="{w}" ry="{w*.3:.0f}" fill="#fff"/><ellipse cx="{x+w*.4:.0f}" cy="{y-w*.15:.0f}" rx="{w*.6:.0f}" ry="{w*.35:.0f}" fill="#fff"/></g>' for x, y, w in ((200, 560, 180), (820, 380, 220), (480, 720, 140)))
    return s
def city(i, col="#120a20", lit="#ffd27a"):
    s = ""
    for k, (x, w, h) in enumerate(((0, 140, 420), (130, 110, 600), (230, 160, 360), (380, 120, 700), (490, 180, 480), (660, 120, 640), (770, 150, 400), (910, 170, 560))):
        s += f'<rect x="{x}" y="{1500-h}" width="{w}" height="{h+420}" fill="{col}"/>' + "".join(f'<rect x="{x+12+cc*30}" y="{1500-h+30+rr*46}" width="14" height="20" fill="{lit}" opacity="{.25 + abs(R(k*31+rr*7+cc))*.75:.2f}"/>' for rr in range(int(h/46)-1) for cc in range(int((w-20)/30)) if R(k*13+rr*5+cc) > -.2)
    return s + f'<path d="M0,1500 H1080 V1920 H0Z" fill="{col}"/>'
def hills(i, col):
    return f'<path d="M0,1450 Q270,1300 540,1420 T1080,1380 V1920 H0Z" fill="{col}"/><path d="M0,1600 Q360,1500 700,1580 T1080,1560 V1920 H0Z" fill="#000" opacity=".35"/>'
def face(i, c, cx=540, cy=1050, sc=1.0, mid=""):  # anime close-up, ~760 wide at sc=1
    h1, h2 = HAIR.get(c.get("hair", "black"), HAIR["black"]); ey = EYES.get(c.get("eyes", "brown"), "#7a4a2a"); sk = c.get("skin", "#ffe0cf"); emo = c.get("emotion", "calm"); long_ = c.get("long", c.get("gender", "girl") == "girl")
    back = f'<path d="M-330,-60 Q-380,420 -250,640 L250,640 Q380,420 330,-60Z" fill="{h1}"/>' if long_ else ""
    s = f'<g transform="translate({cx} {cy}) scale({sc})">{back}<path d="M-120,300 L-110,460 Q0,500 110,460 L120,300Z" fill="{sk}"/><path d="M-330,640 Q-300,470 -120,440 Q0,500 120,440 Q300,470 330,640Z" fill="{c.get("shirt", "#24304a")}"/>'
    s += f'<path d="M-270,-80 Q-280,240 -120,330 Q0,400 120,330 Q280,240 270,-80 Q0,-140 -270,-80Z" fill="{sk}"/>'
    blush = '<ellipse cx="-170" cy="150" rx="60" ry="22" fill="#ff8aa0" opacity=".45"/><ellipse cx="170" cy="150" rx="60" ry="22" fill="#ff8aa0" opacity=".45"/>'
    eye = lambda x, sx: (f'<g class="ey{i}" transform="translate({x} 40)"><path d="M-80,-10 Q0,-90 80,-10 Q70,70 0,80 Q-70,70 -80,-10Z" fill="#fff"/><ellipse cx="0" cy="12" rx="56" ry="70" fill="{ey}"/><ellipse cx="0" cy="22" rx="32" ry="42" fill="#140c1c"/>'
                         f'<ellipse cx="-18" cy="-14" rx="18" ry="24" fill="#fff"/><circle cx="20" cy="44" r="9" fill="#fff" opacity=".8"/><path d="M-92,-6 Q0,-110 92,-6" stroke="#140c1c" stroke-width="14" fill="none" stroke-linecap="round"/>'
                         + (f'<path d="M-70,-120 L60,-90" stroke="#140c1c" stroke-width="10" transform="scale({sx} 1)"/>' if emo in ("determined", "angry") else (f'<path d="M-60,-110 Q0,-130 70,-104" stroke="#140c1c" stroke-width="9" fill="none" transform="scale({sx} 1)"/>' if emo != "sad" else f'<path d="M-60,-96 L60,-120" stroke="#140c1c" stroke-width="9" transform="scale({sx} 1)"/>')) + '</g>')
    s += blush + eye(-125, 1) + eye(125, -1)
    s += f'<g id="mo{i}{mid}">' + {"calm": '<path d="M-30,210 Q0,222 30,210" stroke="#a04050" stroke-width="7" fill="none" stroke-linecap="round"/>', "happy": '<path d="M-50,195 Q0,260 50,195Z" fill="#a03040"/>',
          "sad": '<path d="M-34,224 Q0,206 34,224" stroke="#a04050" stroke-width="7" fill="none"/>', "surprised": '<ellipse cx="0" cy="220" rx="20" ry="26" fill="#a03040"/>',
          "determined": '<path d="M-36,214 H36" stroke="#a04050" stroke-width="8" stroke-linecap="round"/>', "angry": '<path d="M-40,224 Q0,200 40,224" stroke="#a04050" stroke-width="9" fill="none"/>'}.get(emo, "") + "</g>"
    s += '<path d="M-6,140 l-8,40 h18" stroke="#d8a090" stroke-width="5" fill="none"/>'
    s += (f'<g id="hr{i}{mid}"><path d="M-300,-40 Q-320,-330 0,-340 Q320,-330 300,-40 Q250,-120 190,-60 Q170,-170 80,-110 Q40,-200 -40,-110 Q-120,-190 -170,-70 Q-240,-140 -300,-40Z" fill="{h1}"/>'
          f'<path d="M-200,-270 Q-60,-320 60,-300" stroke="{h2}" stroke-width="20" fill="none" stroke-linecap="round" opacity=".7"/>'
          f'<path d="M-300,-40 Q-330,140 -280,260 L-250,40Z M300,-40 Q330,140 280,260 L250,40Z" fill="{h1}"/></g>')
    if emo == "sad" or c.get("tear"): s += f'<path id="te{i}{mid}" d="M-110,120 q-10,40 0,70 q10,-30 0,-70" fill="#bfe6ff" opacity="0"/>'
    return s + "</g>"
def back_view(i, c, x=540, y=1500, sc=1.0):
    h1, _ = HAIR.get(c.get("hair", "black"), HAIR["black"])
    return (f'<g transform="translate({x} {y}) scale({sc})"><g id="bv{i}"><path d="M-120,0 Q-130,-260 -70,-330 H70 Q130,-260 120,0Z" fill="{c.get("shirt", "#24304a")}"/><rect x="-70" y="-10" width="50" height="230" fill="#1a1a2a"/><rect x="20" y="-10" width="50" height="230" fill="#1a1a2a"/>'
            f'<circle cy="-410" r="95" fill="{h1}"/>' + (f'<path d="M-90,-420 Q-110,-200 -60,-140 H60 Q110,-200 90,-420Z" fill="{h1}"/>' if c.get("long", c.get("gender", "girl") == "girl") else "") + '</g></g>')
def petals(i, col="#ffc0dc", n=40): return "".join(f'<path class="pt{i}" transform="translate({(R(k)+1)*540:.0f} {(R(k+40)+1)*500-300:.0f}) rotate({R(k+2)*180:.0f})" d="M0,0 q14,-14 28,0 q-14,14 -28,0" fill="{col}"/>' for k in range(n))
def rain(i, n=90): return "".join(f'<path class="rn{i}" d="M{(R(k)+1)*560:.0f},{(R(k+30)+1)*900-900:.0f} l-18,70" stroke="#bfd8ff" stroke-width="3" opacity=".6"/>' for k in range(n))
def speed(i): return "".join(f'<path d="M540,960 L{540+math.cos(a)*1400:.0f},{960+math.sin(a)*1400:.0f}" stroke="#fff" stroke-width="{3+abs(R(k))*8:.0f}" opacity=".25"/>' for k, a in enumerate([j*math.pi/36 for j in range(72)]))
def scene(i, b, s, e, c0, c1):
    D = c1 - c0; js = []; k = b.get("k", "establish"); c = dict(ep.get("character", {})); c.update(b.get("character", {})); sk = b.get("sky", ep.get("sky", "night"))
    sv = f'<svg class="full" width="1080" height="1920" viewBox="0 0 1080 1920">{defs(i, sk)}<g id="cam{i}">{sky(i, sk)}'
    if k in ("establish", "back", "rain", "sakura", "title", "sky", "together"):
        sv += city(i) if b.get("place", ep.get("place", "city")) == "city" else hills(i, {"night": "#140c24", "sunset": "#3a1a3a", "day": "#3a7a4a", "dawn": "#2a2a5a"}.get(sk, "#140c24"))
    if k == "back": sv += back_view(i, c, 540, 1560, 1.1)
    if k in ("closeup", "tear"): sv += f'<rect width="1080" height="1920" fill="#000" opacity=".25"/>' + face(i, dict(c, emotion=b.get("emotion", "sad" if k == "tear" else c.get("emotion", "calm")), tear=k == "tear"))
    c2 = dict(ep.get("character2", {"hair": "black", "eyes": "brown", "gender": "boy", "shirt": "#3a2a1a"})); c2.update(b.get("character2", {}))
    if k == "duo": sv += f'<rect width="1080" height="1920" fill="#000" opacity=".2"/>' + face(i, dict(c, emotion=b.get("emotion", "calm")), 300, 1120, .62, "a") + face(i, dict(c2, emotion=b.get("emotion2", "calm")), 790, 1080, .62, "b")
    if k == "talk2": sv += f'<rect width="1080" height="1920" fill="#000" opacity=".25"/>' + face(i, dict(c2, emotion=b.get("emotion", "calm"), tear=False), mid="b")
    if k == "together": sv += back_view(i, c, 420, 1560, 1.0).replace(f'id="bv{i}"', f'id="bv{i}"') + back_view(i, c2, 680, 1560, 1.1).replace(f'id="bv{i}"', f'id="bw{i}"')
    if k == "run": sv += speed(i) + f'<g id="rn{i}">' + back_view(i, c, 540, 1500, 1.4).replace(f'id="bv{i}"', f'id="rv{i}"') + "</g>"
    if k == "sky": sv += "".join(f'<path class="ss{i}" d="M{200+n*220},{200+n*60} l-260,140" stroke="#fff" stroke-width="6" stroke-linecap="round" opacity="0"/>' for n in range(4))
    if k == "sakura" or b.get("petals"): sv += petals(i)
    if k == "rain" or b.get("rain"): sv += rain(i)
    sv += f'</g><rect width="1080" height="1920" fill="url(#lk{i})"/><rect width="1080" height="140" fill="#000"/><rect y="1780" width="1080" height="140" fill="#000"/></svg>'
    h = sv
    if k == "title": h += f'<div class="ttl" id="tt{i}" style="opacity:0">{b.get("title", ep.get("title", ""))}</div>'
    if b.get("sub", b.get("cap")): h += f'<div class="sub" id="sb{i}" style="opacity:0">{b.get("sub", b.get("cap"))}</div>'
    # camera + life
    zm = {"duo": (1.0, 1.06), "talk2": (1.06, 1.16), "together": (1.1, 1.0), "establish": (1.0, 1.12), "closeup": (1.06, 1.16), "tear": (1.0, 1.2), "back": (1.1, 1.0), "run": (1.0, 1.08), "sky": (1.0, 1.1), "rain": (1.05, 1.15), "sakura": (1.0, 1.1), "title": (1.15, 1.0)}.get(k, (1, 1.1))
    js.append(f'tl.fromTo("#cam{i}",{{scale:{zm[0]},transformOrigin:"50% 55%"}},{{scale:{zm[1]},duration:{D:.2f},ease:"none"}},{c0:.2f});')
    js.append(f'tl.fromTo("#S{i}",{{opacity:0}},{{opacity:1,duration:.5}},{c0:.2f});' if i else "")
    if k in ("establish", "back", "sky", "title", "sakura", "rain"): js.append(f'tl.fromTo("#S{i} .tw{i}",{{opacity:.3}},{{opacity:1,duration:.4,stagger:{{each:.02,repeat:-1,yoyo:true}}}},{c0:.2f});')
    if k in ("closeup", "tear", "duo", "talk2"):
        spk = {"duo": "a" if b.get("speaker", 1) == 1 else "b", "talk2": "b"}.get(k, "")
        js.append(f'tl.fromTo("#mo{i}{spk}",{{scaleY:1}},{{scaleY:.4,transformOrigin:"50% 30%",duration:.12,yoyo:true,repeat:{int((e-s)/.12)}}},{s:.2f});')
        for t in range(int(D / 2.6)): js.append(f'tl.to("#S{i} .ey{i}",{{scaleY:.08,transformOrigin:"50% 40%",duration:.06,yoyo:true,repeat:1}},{c0+.9+t*2.6:.2f});')
        for hid in (["a", "b"] if k == "duo" else (["b"] if k == "talk2" else [""])): js.append(f'tl.fromTo("#hr{i}{hid}",{{rotation:-1}},{{rotation:1.2,svgOrigin:"0 -300",duration:1.6,yoyo:true,repeat:{int(D/1.6)},ease:"sine.inOut"}},{c0:.2f});')
        if k == "tear": js.append(f'tl.fromTo("#te{i}",{{opacity:0,y:0}},{{opacity:1,y:160,duration:2.2,ease:"power1.in"}},{s+.8:.2f});')
    if k == "run": js.append(f'tl.fromTo("#rv{i}",{{y:0}},{{y:-30,duration:.18,yoyo:true,repeat:{int(D/.18)},ease:"sine.inOut"}},{c0:.2f});')
    if k == "sky": js.append(f'tl.fromTo("#S{i} .ss{i}",{{opacity:0,x:0,y:0}},{{opacity:1,x:-500,y:270,duration:.7,stagger:.6,ease:"power2.in"}},{s+.3:.2f});')
    if k == "sakura" or b.get("petals"): js.append(f'tl.fromTo("#S{i} .pt{i}",{{x:0,y:0}},{{x:-300,y:1900,rotation:"+=360",duration:5,repeat:{int(D/5)+1},ease:"none",stagger:.08}},{c0:.2f});')
    if k == "rain" or b.get("rain"): js.append(f'tl.fromTo("#S{i} .rn{i}",{{y:0}},{{y:1000,duration:.6,repeat:{int(D/.6)+1},ease:"none",stagger:.01}},{c0:.2f});')
    if k == "together": js += [f'tl.fromTo("#bv{i}",{{y:0}},{{y:-6,duration:1.4,yoyo:true,repeat:{int(D/1.4)},ease:"sine.inOut"}},{c0:.2f});', f'tl.fromTo("#bw{i}",{{y:-4}},{{y:4,duration:1.6,yoyo:true,repeat:{int(D/1.6)},ease:"sine.inOut"}},{c0:.2f});']
    if k == "back": js.append(f'tl.fromTo("#bv{i}",{{y:0}},{{y:-6,duration:1.4,yoyo:true,repeat:{int(D/1.4)},ease:"sine.inOut"}},{c0:.2f});')
    if k == "title": js.append(f'tl.fromTo("#tt{i}",{{opacity:0,scale:1.3,filter:"blur(20px)"}},{{opacity:1,scale:1,filter:"blur(0px)",duration:1.2,ease:"power2.out"}},{s:.2f});')
    if b.get("sub", b.get("cap")): js.append(f'tl.fromTo("#sb{i}",{{opacity:0,y:20}},{{opacity:1,y:0,duration:.5}},{s+.1:.2f});')
    return h, [j for j in js if j]
if __name__ == "__main__":
    ep = load(); B = ep["beats"]
    run("anime", B, scene, css=CSS, bg="#000", rate=ep.get("voice", {}).get("rate", "-5%"))
