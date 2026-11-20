from lib import *
CSS = '.t{position:absolute;left:90px;right:90px;text-align:center;font-weight:900;color:#151515;line-height:1.25}.hl{background:linear-gradient(#ffd21f,#ffd21f) no-repeat 100% 88%/0% 40%;padding:0 10px}'
def title(i, txt, y=300, size=96):
    t = re.sub(r"\[y\](.*?)\[/y\]", rf'<span class="hl" id="hl{i}">\1</span>', txt)
    return f'<div class="t" id="tt{i}" style="top:{y}px;font-size:{size}px;opacity:0">{t}</div>'
def tjs(i, s): return [f'tl.fromTo("#tt{i}",{{opacity:0,y:30}},{{opacity:1,y:0,duration:.35,ease:"power3.out"}},{s:.2f});', f'tl.to("#hl{i}",{{backgroundSize:"100% 40%",duration:.4}},{s+.4:.2f});']
def bg(): return '<div style="position:absolute;inset:0;background:#f1ead8"></div><svg class="full" width="1080" height="1920"><defs><pattern id="g" width="60" height="60" patternUnits="userSpaceOnUse"><path d="M60 0H0V60" fill="none" stroke="#000" stroke-opacity=".05" stroke-width="2"/></pattern></defs><rect width="1080" height="1920" fill="url(#g)"/></svg>'
ep = load(); B = ep["beats"]
def coin(x, y, r=70, lab="$"): return f'<g transform="translate({x} {y})"><circle r="{r}" fill="#f2c94c" stroke="#151515" stroke-width="7"/><circle r="{r*.72}" fill="none" stroke="#c99a1e" stroke-width="5"/><text y="{r*.35}" text-anchor="middle" font-size="{r}" font-weight="900" fill="#151515" font-family="Cairo">{lab}</text></g>'
def scene(i, b, s, e, c0, c1):
    k = b["k"]; h = bg(); js = []
    if k == "q":
        h += title(i, b.get("title",""), 300, 110).replace("\n", "<br/>")
        h += '<svg class="full" width="1080" height="1920">' + f'<g id="wal{i}" transform="translate(540 1150)"><rect x="-260" y="-170" width="520" height="340" rx="40" fill="#8a5a33" stroke="#151515" stroke-width="8"/><rect x="40" y="-60" width="240" height="120" rx="30" fill="#6e4424" stroke="#151515" stroke-width="8"/><circle cx="120" r="20" fill="#f2c94c"/></g>'
        for n in range(5): h += f'<g id="bill{i}{n}" opacity="0"><rect x="{430+n*12}" y="900" width="220" height="110" rx="10" fill="#7fbf7f" stroke="#151515" stroke-width="6" transform="rotate({-10+n*5} 540 950)"/></g>'
        h += '</svg>'
        js += tjs(i, s); js.append(f'tl.fromTo("#wal{i}",{{attr:{{transform:"translate(540 1600)"}}}},{{attr:{{transform:"translate(540 1150)"}},duration:.5,ease:"back.out(1.5)"}},{s+.3:.2f});')
        for n in range(5): js.append(f'tl.fromTo("#bill{i}{n}",{{opacity:1,y:0}},{{opacity:0,y:-500,x:{(n-2)*120},rotation:{n*20},duration:.9,ease:"power2.in"}},{s+1.2+n*.25:.2f});')
    elif k == "word":
        h += f'<div class="t" id="big{i}" style="top:760px;font-size:230px;opacity:0"><span style="background:#151515;color:#ffd21f;padding:0 40px 40px">{b.get("word","")}</span></div>'
        h += f'<div class="t" id="sub{i}" style="top:1180px;font-size:56px;color:#555;opacity:0">{b.get("sub","")}</div>'
        js += [f'tl.fromTo("#big{i}",{{opacity:0,scale:2.5}},{{opacity:1,scale:1,duration:.3,ease:"power4.in"}},{s+.9:.2f});', f'tl.fromTo("#S{i}",{{x:0}},{{x:12,duration:.05,yoyo:true,repeat:5}},{s+1.2:.2f});', f'tl.fromTo("#sub{i}",{{opacity:0}},{{opacity:1,duration:.4}},{s+1.6:.2f});']
    elif k == "basket":
        h += title(i, b.get("title",""), 260)
        h += '<svg class="full" width="1080" height="1920">'
        for j, (x, yr, p) in enumerate(((290, *b.get("left", ["قبل", "100"])), (790, *b.get("right", ["بعد", "160"])))):
            h += (f'<g id="bk{i}{j}" opacity="0"><rect x="{x-200}" y="640" width="400" height="640" rx="30" fill="#fff" stroke="#151515" stroke-width="8"/><text x="{x}" y="740" text-anchor="middle" font-size="70" font-weight="900" font-family="Cairo">{yr}</text>'
                  f'<path d="M{x-130},900 h260 l-40,170 h-180 z" fill="#d8a04a" stroke="#151515" stroke-width="7"/><circle cx="{x-60}" cy="880" r="40" fill="#e5322d" stroke="#151515" stroke-width="6"/><circle cx="{x+30}" cy="870" r="44" fill="#7fbf3f" stroke="#151515" stroke-width="6"/><rect x="{x-20}" y="800" width="40" height="90" fill="#f4e3b0" stroke="#151515" stroke-width="6"/>'
                  f'<text id="pr{i}{j}" x="{x}" y="1210" text-anchor="middle" font-size="110" font-weight="900" font-family="Cairo" fill="{"#151515" if j==0 else "#e5322d"}">{p}</text></g>')
        h += f'<path id="ar{i}" d="M500,960 L580,960" stroke="#151515" stroke-width="16" stroke-linecap="round" opacity="0"/><text id="pct{i}" x="540" y="1460" text-anchor="middle" font-size="120" font-weight="900" font-family="Cairo" fill="#e5322d" opacity="0">{b.get("change","")}</text></svg>'
        js += tjs(i, s) + [f'tl.fromTo("#bk{i}0",{{opacity:0,y:60}},{{opacity:1,y:0,duration:.4,ease:"back.out(1.6)"}},{s+.4:.2f});', f'tl.fromTo("#bk{i}1",{{opacity:0,y:60}},{{opacity:1,y:0,duration:.4,ease:"back.out(1.6)"}},{s+1.6:.2f});',
               f'tl.to("#ar{i}",{{opacity:1,duration:.2}},{s+1.4:.2f});', f'tl.fromTo("#pct{i}",{{opacity:0,scale:2}},{{opacity:1,scale:1,duration:.3,ease:"back.out(2)",transformOrigin:"50% 50%"}},{s+2.6:.2f});']
    elif k == "print":
        h += title(i, b.get("title",""), 260)
        h += '<svg class="full" width="1080" height="1920">' + f'<g transform="translate(540 820)"><rect x="-230" y="-150" width="460" height="300" rx="24" fill="#5d6b7a" stroke="#151515" stroke-width="8"/><rect x="-180" y="120" width="360" height="40" fill="#151515"/><circle id="gear{i}" cx="-120" cy="-40" r="60" fill="#9aa8b6" stroke="#151515" stroke-width="7" stroke-dasharray="20 12"/><text x="80" y="10" font-size="70" font-weight="900" fill="#fff" text-anchor="middle" font-family="Cairo">{b.get("machine","طباعة")}</text></g>'
        for n in range(6): h += f'<rect id="pb{i}{n}" x="420" y="960" width="240" height="120" rx="10" fill="#7fbf7f" stroke="#151515" stroke-width="6" opacity="0"/>'
        h += f'<g id="sc{i}" transform="translate(540 1500)"><rect x="-330" y="-20" width="660" height="40" fill="#151515" id="beam{i}"/><path d="M0,0 L-40,200 H40 Z" fill="#151515"/></g><text id="v{i}" x="540" y="1780" text-anchor="middle" font-size="80" font-weight="900" fill="#e5322d" font-family="Cairo" opacity="0">{b.get("result","")}</text></svg>'
        js += tjs(i, s) + [f'tl.to("#gear{i}",{{rotation:720,svgOrigin:"-120 -40",duration:{e-s:.2f},ease:"none"}},{s:.2f});']
        for n in range(6): js.append(f'tl.fromTo("#pb{i}{n}",{{opacity:1,y:0,x:0}},{{opacity:1,y:{300+n*30},x:{(n-2.5)*90},rotation:{(n-2.5)*12},duration:.5,ease:"power2.in"}},{s+.6+n*.35:.2f});')
        js += [f'tl.fromTo("#v{i}",{{opacity:0}},{{opacity:1,duration:.3}},{s+2.8:.2f});']
    elif k == "chart":
        h += title(i, b.get("title",""), 260)
        h += '<svg class="full" width="1080" height="1920"><path d="M140,1500 H960 M140,1500 V700" stroke="#151515" stroke-width="8"/>'
        pts = [(200 + j * 120, 1420 - j * j * 14 - j * 40) for j in range(7)]
        d = "M" + " L".join(f"{x},{y}" for x, y in pts)
        h += f'<path id="ln{i}" d="{d}" fill="none" stroke="#e5322d" stroke-width="16" stroke-linecap="round" stroke-dasharray="1600" stroke-dashoffset="1600"/>'
        for j, (x, y) in enumerate(pts): h += f'<circle id="d{i}{j}" cx="{x}" cy="{y}" r="16" fill="#151515" opacity="0"/><text x="{x}" y="1560" text-anchor="middle" font-size="36" font-weight="800" font-family="Cairo" fill="#555">{(b.get("labels") or [""]*7)[j] if j < len(b.get("labels") or []) else ""}</text>'
        h += '</svg>'
        js += tjs(i, s) + [f'tl.to("#ln{i}",{{strokeDashoffset:0,duration:{e-s-.3:.2f},ease:"none"}},{s+.3:.2f});']
        for j in range(7): js.append(f'tl.to("#d{i}{j}",{{opacity:1,duration:.1}},{s+.3+(e-s-.3)*j/6:.2f});')
    else:
        h += title(i, b.get("title",""), 300, 104)
        h += '<svg class="full" width="1080" height="1920">' + f'<g transform="translate(540 1050)"><g id="ci{i}" transform="scale(0.01)">{coin(0, 0, 170, b.get("symbol", "$"))}</g></g><g id="mt{i}" opacity="0"><path d="M300,1300 Q540,1420 780,1300" stroke="#2f9a46" stroke-width="22" fill="none" stroke-linecap="round"/><path d="M720,1250 L790,1300 L720,1360" stroke="#2f9a46" stroke-width="22" fill="none" stroke-linecap="round"/></g>'
        for n in range(4): h += f'<g id="cc{i}{n}" opacity="0">{coin(260+n*190, 1560, 60, "+")}</g>'
        h += '</svg>'
        js += tjs(i, s) + [f'tl.to("#ci{i}",{{attr:{{transform:"scale(1)"}},duration:.4,ease:"back.out(2)"}},{s+.4:.2f});', f'tl.to("#mt{i}",{{opacity:1,duration:.3}},{s+1.6:.2f});']
        for n in range(4): js.append(f'tl.fromTo("#cc{i}{n}",{{opacity:0,y:-80}},{{opacity:1,y:0,duration:.35,ease:"bounce.out"}},{s+2+n*.3:.2f});')
    return h, js
run("3_voxflat", B, scene, css=CSS, bg="#f1ead8", rate="+0%")
