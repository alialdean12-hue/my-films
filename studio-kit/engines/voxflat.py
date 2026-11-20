from lib import *
import math
from icons import icon
CSS = '.t{position:absolute;left:90px;right:90px;text-align:center;font-weight:900;color:#151515;line-height:1.25}.hl{background:linear-gradient(#ffd21f,#ffd21f) no-repeat 100% 88%/0% 40%;padding:0 10px}'
def title(i, txt, y=300, size=96):
    t = re.sub(r"\[y\](.*?)\[/y\]", rf'<span class="hl" id="hl{i}">\1</span>', txt)
    return f'<div class="t" id="tt{i}" style="top:{y}px;font-size:{size}px;opacity:0">{t}</div>'
def tjs(i, s): return [f'tl.fromTo("#tt{i}",{{opacity:0,y:30}},{{opacity:1,y:0,duration:.35,ease:"power3.out"}},{s:.2f});', f'tl.to("#hl{i}",{{backgroundSize:"100% 40%",duration:.4}},{s+.4:.2f});']
PAPERS = {'cream': '#f1ead8', 'white': '#fbfbf7', 'blue': '#dbe8f5', 'mint': '#dff3e8', 'pink': '#fbe3e8', 'yellow': '#fff3c4', 'grey': '#e6e6e6', 'kraft': '#e3c9a0', 'lilac': '#ece3fb', 'peach': '#ffe2cc'}
def bg(): return f'<div style="position:absolute;inset:0;background:{PAPERS.get(ep.get("paper", "cream"), ep.get("paper", "#f1ead8"))}"></div><svg class="full" width="1080" height="1920"><defs><pattern id="g" width="60" height="60" patternUnits="userSpaceOnUse"><path d="M60 0H0V60" fill="none" stroke="#000" stroke-opacity=".05" stroke-width="2"/></pattern></defs><rect width="1080" height="1920" fill="url(#g)"/></svg>'
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
    elif k == "icons":   # 2-4 icons with labels pop in one by one
        h += title(i, b.get("title", ""), 280); items = b["items"]; n = len(items)
        h += '<svg class="full" width="1080" height="1920">'
        for j, (ic, lab) in enumerate(items):
            x = 540 + (j - (n - 1) / 2) * (900 / max(n, 2)) if n > 1 else 540; y = 1050 if n <= 3 else 950 + (j % 2) * 380
            if n == 4: x = 300 + (j % 2) * 480
            h += f'<g transform="translate({x:.0f} {y})"><g id="it{i}{j}" transform="scale(0)">{icon(ic, .85 if n < 4 else .7, "#151515")}<text y="210" text-anchor="middle" font-size="58" font-weight="900" font-family="Cairo" fill="#151515">{lab}</text></g></g>'
            js.append(f'tl.to("#it{i}{j}",{{attr:{{transform:"scale(1)"}},duration:.45,ease:"back.out(2)"}},{s+.4+j*(e-s-.6)/n:.2f});')
        h += '</svg>'; js += tjs(i, s)
    elif k == "versus":
        (ia, la), (ib, lb) = b["a"], b["b"]; h += title(i, b.get("title", ""), 280)
        h += (f'<svg class="full" width="1080" height="1920"><rect id="la{i}" x="0" y="700" width="540" height="900" fill="#2b8be0" opacity=".15"/><rect id="lb{i}" x="540" y="700" width="540" height="900" fill="#e5322d" opacity=".15"/>'
              f'<g transform="translate(270 1100)"><g id="va{i}" transform="scale(0)">{icon(ia, .9, "#151515")}<text y="220" text-anchor="middle" font-size="64" font-weight="900" font-family="Cairo">{la}</text></g></g>'
              f'<g transform="translate(810 1100)"><g id="vb{i}" transform="scale(0)">{icon(ib, .9, "#151515")}<text y="220" text-anchor="middle" font-size="64" font-weight="900" font-family="Cairo">{lb}</text></g></g>'
              f'<g transform="translate(540 1100)"><g id="vs{i}" transform="scale(0)"><circle r="90" fill="#151515"/><text y="30" text-anchor="middle" font-size="84" font-weight="900" fill="#ffd21f" font-family="Cairo">VS</text></g></g></svg>')
        js += tjs(i, s) + [f'tl.to("#va{i}",{{attr:{{transform:"scale(1)"}},duration:.45,ease:"back.out(2)"}},{s+.4:.2f});', f'tl.to("#vs{i}",{{attr:{{transform:"scale(1)"}},duration:.3,ease:"back.out(3)"}},{s+1:.2f});', f'tl.to("#vb{i}",{{attr:{{transform:"scale(1)"}},duration:.45,ease:"back.out(2)"}},{s+1.3:.2f});']
        if b.get("win") in (0, 1): js.append(f'tl.to("#{"la" if b["win"]==0 else "lb"}{i}",{{opacity:.45,duration:.4}},{s+2:.2f});')
    elif k == "bars":
        vals, labs = b["values"], b.get("labels", [""] * len(b["values"])); n = len(vals); mx = max(vals); h += title(i, b.get("title", ""), 260)
        cols = b.get("colors", ["#2b8be0", "#e5322d", "#2fbf6a", "#ffd21f", "#7a4fd1", "#ff8a2a"]); bw = 760 / n * .62
        h += '<svg class="full" width="1080" height="1920"><path d="M140,1560 H940" stroke="#151515" stroke-width="10"/>'
        for j, v in enumerate(vals):
            x = 160 + 760 * (j + .5) / n; bh = 700 * v / mx
            h += f'<g transform="translate(0 1560)"><g id="br{i}{j}" transform="scale(1 0.01)"><rect x="{x-bw/2:.0f}" y="{-bh:.0f}" width="{bw:.0f}" height="{bh:.0f}" fill="{cols[j%len(cols)]}" stroke="#151515" stroke-width="7"/></g></g>'
            h += f'<text x="{x:.0f}" y="1630" text-anchor="middle" font-size="48" font-weight="900" font-family="Cairo">{labs[j]}</text><text id="bv{i}{j}" x="{x:.0f}" y="{1530-bh:.0f}" text-anchor="middle" font-size="56" font-weight="900" font-family="Cairo" opacity="0">{v}{b.get("unit","")}</text>'
            js += [f'tl.to("#br{i}{j}",{{attr:{{transform:"scale(1 1)"}},duration:.6,ease:"back.out(1.3)"}},{s+.4+j*.3:.2f});', f'tl.to("#bv{i}{j}",{{opacity:1,duration:.2}},{s+.9+j*.3:.2f});']
        h += '</svg>'; js += tjs(i, s)
    elif k == "pie":
        p = b.get("percent", 70); h += title(i, b.get("title", ""), 260); C = 2 * math.pi * 230
        h += (f'<svg class="full" width="1080" height="1920"><circle cx="540" cy="1080" r="320" fill="#fff" stroke="#151515" stroke-width="10"/><circle cx="540" cy="1080" r="230" fill="none" stroke="#e8e2d0" stroke-width="180"/>'
              f'<circle id="pc{i}" cx="540" cy="1080" r="230" fill="none" stroke="{b.get("color", "#e5322d")}" stroke-width="180" stroke-dasharray="{C:.0f}" stroke-dashoffset="{C:.0f}" transform="rotate(-90 540 1080)"/>'
              f'<text x="540" y="1520" text-anchor="middle" font-size="150" font-weight="900" font-family="Cairo" fill="#151515">{p}%</text><text x="540" y="1620" text-anchor="middle" font-size="56" font-weight="800" font-family="Cairo" fill="#555">{b.get("label","")}</text></svg>')
        js += tjs(i, s) + [f'tl.to("#pc{i}",{{strokeDashoffset:{C*(1-p/100):.0f},duration:1.2,ease:"power2.out"}},{s+.4:.2f});']
    elif k == "list":
        items = b["items"]; h += title(i, b.get("title", ""), 260)
        for j, t in enumerate(items):
            h += f'<div class="t" id="li{i}{j}" style="top:{620+j*220}px;font-size:66px;text-align:right;opacity:0"><span style="display:inline-block;background:#151515;color:#ffd21f;border-radius:50%;width:110px;height:110px;line-height:100px;text-align:center;margin-left:30px">{j+1}</span>{t}</div>'
            js.append(f'tl.fromTo("#li{i}{j}",{{opacity:0,x:200}},{{opacity:1,x:0,duration:.4,ease:"power3.out"}},{s+.4+j*(e-s-.5)/len(items):.2f});')
        js += tjs(i, s)
    elif k == "counter":
        h += title(i, b.get("title", ""), 300) + f'<div class="t" id="cn{i}" style="top:820px;font-size:230px;color:{b.get("color", "#e5322d")}">0</div><div class="t" style="top:1140px;font-size:64px;color:#555">{b.get("label","")}</div>'
        if b.get("icon"): h += f'<svg class="full" width="1080" height="1920"><g transform="translate(540 1500)">{icon(b["icon"], .8, "#151515")}</g></svg>'
        js += tjs(i, s) + [f'const o{i}={{v:0}};tl.to(o{i},{{v:{b.get("number",100)},duration:{max(1, e-s-.8):.2f},ease:"power2.out",onUpdate:()=>{{document.getElementById("cn{i}").textContent=Math.round(o{i}.v).toLocaleString("en")+"{b.get("unit","")}"}}}},{s+.4:.2f});']
    elif k == "timeline":
        ev = b["events"]; n = len(ev); h += title(i, b.get("title", ""), 260)
        h += f'<svg class="full" width="1080" height="1920"><path id="tl{i}" d="M540,600 V1700" stroke="#151515" stroke-width="12" stroke-dasharray="1100" stroke-dashoffset="1100"/>'
        for j, (yr, lab) in enumerate(ev):
            y = 660 + j * 1000 / max(1, n - 1) if n > 1 else 1100; side = 1 if j % 2 else -1
            h += f'<g id="ev{i}{j}" opacity="0"><circle cx="540" cy="{y:.0f}" r="34" fill="#ffd21f" stroke="#151515" stroke-width="8"/><text x="{540+side*70}" y="{y-10:.0f}" text-anchor="{"end" if side>0 else "start"}" font-size="64" font-weight="900" font-family="Cairo">{yr}</text><text x="{540+side*70}" y="{y+60:.0f}" text-anchor="{"end" if side>0 else "start"}" font-size="46" font-weight="800" fill="#555" font-family="Cairo">{lab}</text></g>'
            js.append(f'tl.to("#ev{i}{j}",{{opacity:1,duration:.3}},{s+.4+j*(e-s-.6)/n:.2f});')
        h += '</svg>'; js += tjs(i, s) + [f'tl.to("#tl{i}",{{strokeDashoffset:0,duration:{e-s-.4:.2f},ease:"none"}},{s+.3:.2f});']
    elif k == "steps":
        items = b["items"]; n = len(items); h += title(i, b.get("title", ""), 260) + '<svg class="full" width="1080" height="1920">'
        for j, (ic, lab) in enumerate(items):
            y = 650 + j * 1050 / max(1, n - 1) if n > 1 else 1100
            h += f'<g transform="translate(400 {y:.0f})"><g id="st{i}{j}" transform="scale(0)">{icon(ic, .5, "#151515")}</g></g><text id="sl{i}{j}" x="560" y="{y+20:.0f}" font-size="60" font-weight="900" font-family="Cairo" opacity="0" text-anchor="end">{lab}</text>'
            if j < n - 1: h += f'<path id="sa{i}{j}" d="M400,{y+110:.0f} V{y+1050/max(1,n-1)-110:.0f}" stroke="#e5322d" stroke-width="12" stroke-dasharray="14 12" opacity="0"/>'
            t = s + .4 + j * (e - s - .6) / n
            js += [f'tl.to("#st{i}{j}",{{attr:{{transform:"scale(1)"}},duration:.4,ease:"back.out(2)"}},{t:.2f});', f'tl.to("#sl{i}{j}",{{opacity:1,duration:.3}},{t+.2:.2f});'] + ([f'tl.to("#sa{i}{j}",{{opacity:1,duration:.2}},{t+.4:.2f});'] if j < n - 1 else [])
        h += '</svg>'; js += tjs(i, s)
    elif k == "grid":   # e.g. 7 out of 10 people
        tot, hit = b.get("total", 10), b.get("hit", 7); cols = 5 if tot <= 10 else 10; h += title(i, b.get("title", ""), 260) + '<svg class="full" width="1080" height="1920">'
        sz = 860 / cols
        for j in range(tot):
            x = 110 + sz * (j % cols + .5); y = 800 + sz * 1.3 * (j // cols)
            c = b.get("color", "#e5322d") if j < hit else "#c9c2b0"
            h += f'<g id="gd{i}{j}" opacity="0" transform="translate({x:.0f} {y:.0f})"><circle cy="-{sz*.32:.0f}" r="{sz*.18:.0f}" fill="{c}" stroke="#151515" stroke-width="5"/><path d="M{-sz*.28:.0f},{sz*.35:.0f} Q0,{-sz*.15:.0f} {sz*.28:.0f},{sz*.35:.0f}Z" fill="{c}" stroke="#151515" stroke-width="5"/></g>'
            js.append(f'tl.to("#gd{i}{j}",{{opacity:1,duration:.15}},{s+.4+j*.08:.2f});')
        h += f'</svg><div class="t" style="top:1580px;font-size:90px;color:{b.get("color", "#e5322d")}">{hit} من {tot}</div>'; js += tjs(i, s)
    elif k == "progress":
        p = b.get("percent", 60); h += title(i, b.get("title", ""), 300)
        h += f'<div style="position:absolute;left:120px;right:120px;top:1000px;height:120px;border:10px solid #151515;border-radius:70px;background:#fff;overflow:hidden"><div id="pg{i}" style="width:100%;height:100%;background:{b.get("color", "#2fbf6a")};transform-origin:100% 50%"></div></div><div class="t" style="top:1180px;font-size:120px">{p}%</div>'
        js += tjs(i, s) + [f'tl.fromTo("#pg{i}",{{scaleX:0}},{{scaleX:{p/100},duration:1.4,ease:"power2.out"}},{s+.4:.2f});']
    elif k == "big_icon":
        h += title(i, b.get("title", ""), 280) + f'<svg class="full" width="1080" height="1920"><g transform="translate(540 1150)"><g id="bi{i}" transform="scale(0)">{icon(b.get("icon", "star"), 1.8, "#151515")}</g></g></svg>'
        js += tjs(i, s) + [f'tl.to("#bi{i}",{{attr:{{transform:"scale(1)"}},duration:.6,ease:"elastic.out(1,.5)"}},{s+.4:.2f});', f'tl.to("#bi{i}",{{attr:{{transform:"scale(1.06)"}},duration:.5,yoyo:true,repeat:{int((e-s)/.5)}}},{s+1.1:.2f});']
    elif k == "quote":
        h += f'<div class="t" style="top:520px;font-size:260px;color:#e5322d;line-height:1">“</div><div class="t" id="qt{i}" style="top:800px;font-size:76px;opacity:0">{b.get("text","")}</div><div class="t" style="top:1420px;font-size:52px;color:#555">— {b.get("who","")}</div>'
        js.append(f'tl.fromTo("#qt{i}",{{opacity:0,y:40}},{{opacity:1,y:0,duration:.6}},{s+.2:.2f});')
    elif k == "map":
        h += title(i, b.get("title", ""), 260) + f'<svg class="full" width="1080" height="1920"><g transform="translate(540 1100)">{icon("map", 2.6, "#151515")}</g>'
        for j, (x, y, lab) in enumerate(b.get("pins", [[440, 1060, ""]])):
            h += f'<g transform="translate({x} {y})"><g id="mp{i}{j}" transform="translate(0 -600)">{icon("pin", .35, "#151515")}<text y="110" text-anchor="middle" font-size="48" font-weight="900" font-family="Cairo">{lab}</text></g></g>'
            js.append(f'tl.to("#mp{i}{j}",{{attr:{{transform:"translate(0 0)"}},duration:.5,ease:"bounce.out"}},{s+.5+j*.4:.2f});')
        h += '</svg>'; js += tjs(i, s)
    else:
        h += title(i, b.get("title",""), 300, 104)
        h += '<svg class="full" width="1080" height="1920">' + f'<g transform="translate(540 1050)"><g id="ci{i}" transform="scale(0.01)">{coin(0, 0, 170, b.get("symbol", "$"))}</g></g><g id="mt{i}" opacity="0"><path d="M300,1300 Q540,1420 780,1300" stroke="#2f9a46" stroke-width="22" fill="none" stroke-linecap="round"/><path d="M720,1250 L790,1300 L720,1360" stroke="#2f9a46" stroke-width="22" fill="none" stroke-linecap="round"/></g>'
        for n in range(4): h += f'<g id="cc{i}{n}" opacity="0">{coin(260+n*190, 1560, 60, "+")}</g>'
        h += '</svg>'
        js += tjs(i, s) + [f'tl.to("#ci{i}",{{attr:{{transform:"scale(1)"}},duration:.4,ease:"back.out(2)"}},{s+.4:.2f});', f'tl.to("#mt{i}",{{opacity:1,duration:.3}},{s+1.6:.2f});']
        for n in range(4): js.append(f'tl.fromTo("#cc{i}{n}",{{opacity:0,y:-80}},{{opacity:1,y:0,duration:.35,ease:"bounce.out"}},{s+2+n*.3:.2f});')
    return h, js
run("3_voxflat", B, scene, css=CSS, bg="#f1ead8", rate="+0%")
