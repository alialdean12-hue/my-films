"""Wars & big events for style 3 (cine.py): real-border maps, armies, vehicles, explosions, flags, war places.
Map beat:  "map": {"region": "gulf|middle_east|arab_world|levant|europe|world" or [lon1, lat1, lon2, lat2],
                   "color": {"IRQ": "#c62a30"}, "labels": ["IRQ", "KWT"], "flags": ["IRQ", "KWT"],
                   "arrows": [{"from": "IRQ", "to": "KWT", "at": 1.0, "color": "#c62a30"}],
                   "take": [{"iso": "KWT", "color": "#c62a30", "at": 2.0}],
                   "pins": [{"lon": 47.98, "lat": 29.37, "label": "الكويت", "at": .5}]}
Codes are ISO-3 (IRQ KWT IRN SAU SYR JOR EGY ARE QAT BHR OMN YEM ISR PSX LBN TUR USA RUS GBR FRA …)."""
import json, math, os
K = "#16131c"
HERE = os.path.dirname(os.path.abspath(__file__))
_C = None
def countries():
    global _C
    if _C is None: _C = json.load(open(os.path.join(HERE, "data", "countries.json")))
    return _C
REGIONS = {"gulf": [38, 22, 61, 38], "middle_east": [24, 11, 64, 42], "arab_world": [-18, 6, 64, 40], "levant": [32, 28.5, 44, 38],
           "europe": [-12, 34, 46, 62], "world": [-170, -56, 190, 78], "asia": [60, 0, 150, 55], "egypt": [24, 21, 37, 32.5]}
AR = {"PSX": "فلسطين", "ISR": "إسرائيل", "ARE": "الإمارات", "USA": "أمريكا", "GBR": "بريطانيا", "RUS": "روسيا", "SAU": "السعودية"}

class Proj:
    def __init__(self, box, x0=40, y0=380, w=1000, h=1160):
        l1, a1, l2, a2 = box; self.k = math.cos(math.radians((a1 + a2) / 2))
        sx = w / ((l2 - l1) * self.k); sy = h / (a2 - a1); self.s = min(sx, sy)
        self.ox = x0 + (w - (l2 - l1) * self.k * self.s) / 2 - l1 * self.k * self.s
        self.oy = y0 + (h - (a2 - a1) * self.s) / 2 + a2 * self.s
    def __call__(self, lon, lat): return self.ox + lon * self.k * self.s, self.oy - lat * self.s

def centroid(code, P=None):
    rs = countries()[code]["r"]; r = max(rs, key=len); a = cx = cy = 0
    for i in range(len(r)):
        x0, y0 = r[i - 1]; x1, y1 = r[i]; c = x0 * y1 - x1 * y0; a += c; cx += (x0 + x1) * c; cy += (y0 + y1) * c
    lon, lat = (cx / (3 * a), cy / (3 * a)) if a else r[0]
    return P(lon, lat) if P else (lon, lat)

def flag(code, w=90):
    """simple flag drawings (h = 2/3 w). Unknown code -> plain white."""
    h = w * 2 / 3; r = lambda y, hh, c: f'<rect x="0" y="{y:.1f}" width="{w}" height="{hh:.1f}" fill="{c}"/>'
    t = h / 3
    F = {
     "IRQ": r(0, t, "#ce1126") + r(t, t, "#fff") + r(2*t, t, "#111") + f'<path d="M{w*.3},{h*.55} q{w*.06},-{h*.1} {w*.12},0 M{w*.46},{h*.42} v{h*.16} M{w*.54},{h*.55} q{w*.08},-{h*.12} {w*.16},0" stroke="#007a3d" stroke-width="{w*.035:.1f}" fill="none" stroke-linecap="round"/>',
     "KWT": r(0, t, "#007a3d") + r(t, t, "#fff") + r(2*t, t, "#ce1126") + f'<path d="M0,0 L{w*.25},{t} L{w*.25},{2*t} L0,{h}Z" fill="#111"/>',
     "IRN": r(0, t, "#239f40") + r(t, t, "#fff") + r(2*t, t, "#da0000") + f'<circle cx="{w/2}" cy="{h/2}" r="{t*.3}" fill="#da0000"/>',
     "SAU": r(0, h, "#006c35") + f'<path d="M{w*.25},{h*.62} L{w*.75},{h*.62}" stroke="#fff" stroke-width="{w*.03}"/><path d="M{w*.3},{h*.42} q{w*.2},-{h*.12} {w*.4},0" stroke="#fff" stroke-width="{w*.04}" fill="none"/>',
     "EGY": r(0, t, "#ce1126") + r(t, t, "#fff") + r(2*t, t, "#111") + f'<circle cx="{w/2}" cy="{h/2}" r="{t*.32}" fill="#c09300"/>',
     "SYR": r(0, t, "#007a3d") + r(t, t, "#fff") + r(2*t, t, "#111") + "".join(f'<circle cx="{w*x}" cy="{h/2}" r="{t*.22}" fill="#ce1126"/>' for x in (.33, .5, .67)),
     "JOR": r(0, t, "#111") + r(t, t, "#fff") + r(2*t, t, "#007a3d") + f'<path d="M0,0 L{w*.45},{h/2} L0,{h}Z" fill="#ce1126"/>',
     "ARE": r(0, t, "#00732f") + r(t, t, "#fff") + r(2*t, t, "#111") + f'<rect x="0" y="0" width="{w*.25}" height="{h}" fill="#ff0000"/>',
     "QAT": r(0, h, "#8a1538") + f'<path d="M0,0 H{w*.3} L{w*.38},{h*.05} L{w*.3},{h*.11} L{w*.38},{h*.16} L{w*.3},{h*.22} L{w*.38},{h*.27} L{w*.3},{h*.33} L{w*.38},{h*.38} L{w*.3},{h*.44} L{w*.38},{h*.5} L{w*.3},{h*.55} L{w*.38},{h*.61} L{w*.3},{h*.66} L{w*.38},{h*.72} L{w*.3},{h*.77} L{w*.38},{h*.83} L{w*.3},{h*.88} L{w*.38},{h*.94} L{w*.3},{h} H0Z" fill="#fff"/>',
     "LBN": r(0, h*.25, "#ed1c24") + r(h*.25, h*.5, "#fff") + r(h*.75, h*.25, "#ed1c24") + f'<path d="M{w/2},{h*.3} L{w*.62},{h*.68} H{w*.38}Z" fill="#00a651"/>',
     "PSX": r(0, t, "#111") + r(t, t, "#fff") + r(2*t, t, "#007a3d") + f'<path d="M0,0 L{w*.4},{h/2} L0,{h}Z" fill="#ce1126"/>',
     "YEM": r(0, t, "#ce1126") + r(t, t, "#fff") + r(2*t, t, "#111"),
     "OMN": r(0, t, "#fff") + r(t, t, "#db161b") + r(2*t, t, "#008000") + f'<rect width="{w*.28}" height="{h}" fill="#db161b"/>',
     "BHR": r(0, h, "#ce1126") + f'<path d="M0,0 H{w*.3} L{w*.4},{h*.1} L{w*.3},{h*.2} L{w*.4},{h*.3} L{w*.3},{h*.4} L{w*.4},{h*.5} L{w*.3},{h*.6} L{w*.4},{h*.7} L{w*.3},{h*.8} L{w*.4},{h*.9} L{w*.3},{h} H0Z" fill="#fff"/>',
     "LBY": r(0, h*.25, "#e70013") + r(h*.25, h*.5, "#111") + r(h*.75, h*.25, "#239e46") + f'<circle cx="{w/2}" cy="{h/2}" r="{h*.13}" fill="#fff"/>',
     "TUR": r(0, h, "#e30a17") + f'<circle cx="{w*.4}" cy="{h/2}" r="{h*.25}" fill="#fff"/><circle cx="{w*.45}" cy="{h/2}" r="{h*.2}" fill="#e30a17"/>',
     "USA": "".join(r(i*h/13, h/13, "#b22234" if i % 2 == 0 else "#fff") for i in range(13)) + f'<rect width="{w*.4}" height="{h*.54}" fill="#3c3b6e"/>',
     "RUS": r(0, t, "#fff") + r(t, t, "#0039a6") + r(2*t, t, "#d52b1e"),
     "GBR": r(0, h, "#012169") + f'<path d="M0,0 L{w},{h} M{w},0 L0,{h}" stroke="#fff" stroke-width="{h*.2}"/><path d="M{w/2},0 V{h} M0,{h/2} H{w}" stroke="#fff" stroke-width="{h*.33}"/><path d="M{w/2},0 V{h} M0,{h/2} H{w}" stroke="#c8102e" stroke-width="{h*.2}"/>',
     "FRA": f'<rect width="{w/3}" height="{h}" fill="#0055a4"/><rect x="{w/3}" width="{w/3}" height="{h}" fill="#fff"/><rect x="{2*w/3}" width="{w/3}" height="{h}" fill="#ef4135"/>',
     "DEU": r(0, t, "#111") + r(t, t, "#dd0000") + r(2*t, t, "#ffce00"),
     "JPN": r(0, h, "#fff") + f'<circle cx="{w/2}" cy="{h/2}" r="{h*.3}" fill="#bc002d"/>',
     "ISR": r(0, h, "#fff") + r(h*.1, h*.12, "#0038b8") + r(h*.78, h*.12, "#0038b8") + f'<path d="M{w/2},{h*.3} L{w*.58},{h*.62} L{w*.42},{h*.62}Z M{w/2},{h*.7} L{w*.42},{h*.38} L{w*.58},{h*.38}Z" fill="none" stroke="#0038b8" stroke-width="3"/>',
     "CHN": r(0, h, "#de2910") + f'<circle cx="{w*.2}" cy="{h*.28}" r="{h*.12}" fill="#ffde00"/>',
     "AFG": f'<rect width="{w/3}" height="{h}" fill="#111"/><rect x="{w/3}" width="{w/3}" height="{h}" fill="#be0000"/><rect x="{2*w/3}" width="{w/3}" height="{h}" fill="#009900"/>',
    }
    return f'<g><rect x="-2" y="-2" width="{w+4}" height="{h+4}" fill="{K}"/>{F.get(code, r(0, h, "#fff"))}</g>'

def flag_pole(code, x, y, i, k, w=150):
    """flag on a pole (y = ground), waving."""
    return (f'<g transform="translate({x} {y})"><path d="M0,0 V-420" stroke="#5a4a3a" stroke-width="12"/><circle cy="-424" r="10" fill="#c9a24a"/>'
            f'<g id="fg{i}_{k}" transform="translate(6 -414)">{flag(code, w)}</g></g>')

# ------------------------------------------------------------------ map
def map_svg(i, m, s, J):
    box = m.get("region", "middle_east"); box = REGIONS.get(box, box) if isinstance(box, str) else box
    P = Proj(box); C = countries(); col = m.get("color", {})
    l1, a1, l2, a2 = box; pad = 8
    out = [f'<rect x="-300" y="-300" width="1680" height="2520" fill="#2a5a7a"/>'
           + "".join(f'<path d="M-300,{y} q80,-14 160,0 t160,0 t160,0 t160,0 t160,0 t160,0 t160,0 t160,0 t160,0 t160,0" stroke="#3a6a8a" stroke-width="4" fill="none"/>' for y in range(200, 1800, 90))]
    for code, c in C.items():
        rings = [r for r in c["r"] if any(l1 - pad < x < l2 + pad and a1 - pad < y < a2 + pad for x, y in r[::3])]
        if not rings: continue
        d = " ".join("M" + " L".join(f"{P(x, y)[0]:.1f},{P(x, y)[1]:.1f}" for x, y in r) + "Z" for r in rings)
        out.append(f'<path id="cn{i}_{code}" d="{d}" fill="{col.get(code, "#e6d6b0")}" stroke="#5a4a3a" stroke-width="3" stroke-linejoin="round"/>')
    for t in m.get("take", []):
        J(f'tl.to("#cn{i}_{t["iso"]}",{{attr:{{fill:"{t.get("color", "#c62a30")}"}},duration:.6,ease:"power1.inOut"}},{s + t.get("at", 1):.2f});')
        J(f'tl.fromTo("#cn{i}_{t["iso"]}",{{attr:{{"stroke-width":3}}}},{{attr:{{"stroke-width":10}},duration:.3,yoyo:true,repeat:3}},{s + t.get("at", 1):.2f});')
    labels = list(dict.fromkeys(m.get("labels", []) + list(col) + [t["iso"] for t in m.get("take", [])]))
    if m.get("pins"): labels = [c for c in labels if c not in m.get("hide_labels", [])]
    for code in m.get("flags", []):
        if code not in C: continue
        x, y = centroid(code, P); out.append(f'<g transform="translate({x - 45:.0f} {y - 110:.0f})">{flag(code, 90)}</g>')
    for code in labels:
        if code not in C: continue
        x, y = centroid(code, P); name = AR.get(code, C[code]["ar"])
        fs = 44 if len(name) < 8 else 36
        out.append(f'<text x="{x:.0f}" y="{y + 16:.0f}" text-anchor="middle" font-size="{fs}" font-weight="900" fill="#fff" stroke="{K}" stroke-width="10" paint-order="stroke" font-family="Cairo">{name}</text>')
    for k, a in enumerate(m.get("arrows", [])):
        x1, y1 = centroid(a["from"], P) if isinstance(a["from"], str) else P(*a["from"])
        x2, y2 = centroid(a["to"], P) if isinstance(a["to"], str) else P(*a["to"])
        dx, dy = x2 - x1, y2 - y1; L = math.hypot(dx, dy) or 1; nx, ny = -dy / L, dx / L; bend = a.get("bend", .25) * L
        cx, cy = (x1 + x2) / 2 + nx * bend, (y1 + y2) / 2 + ny * bend
        ex, ey = x2 - dx / L * 30, y2 - dy / L * 30; c = a.get("color", "#c62a30"); ln = L * 1.25
        ang = math.degrees(math.atan2(ey - cy, ex - cx))
        out.append(f'<path id="ar{i}_{k}" d="M{x1:.0f},{y1:.0f} Q{cx:.0f},{cy:.0f} {ex:.0f},{ey:.0f}" fill="none" stroke="{K}" stroke-width="34" stroke-linecap="round" stroke-dasharray="{ln:.0f}" stroke-dashoffset="{ln:.0f}"/>'
                   f'<path id="ai{i}_{k}" d="M{x1:.0f},{y1:.0f} Q{cx:.0f},{cy:.0f} {ex:.0f},{ey:.0f}" fill="none" stroke="{c}" stroke-width="22" stroke-linecap="round" stroke-dasharray="{ln:.0f}" stroke-dashoffset="{ln:.0f}"/>'
                   f'<g id="ah{i}_{k}" opacity="0" transform="translate({ex:.0f} {ey:.0f}) rotate({ang:.0f})"><path d="M-10,-38 L48,0 L-10,38Z" fill="{c}" stroke="{K}" stroke-width="7" stroke-linejoin="round"/></g>')
        at = s + a.get("at", .8)
        J(f'tl.to("#ar{i}_{k}, #ai{i}_{k}",{{attr:{{"stroke-dashoffset":0}},duration:1.1,ease:"power2.inOut"}},{at:.2f});tl.to("#ah{i}_{k}",{{opacity:1,duration:.15}},{at + 1.0:.2f});')
    for k, p in enumerate(m.get("pins", [])):
        x, y = P(p["lon"], p["lat"])
        out.append(f'<g id="pn{i}_{k}" transform="translate({x:.0f} {y:.0f}) scale(0)"><circle r="22" fill="#ffd23f" stroke="{K}" stroke-width="6"/><circle r="8" fill="{K}"/>'
                   + (f'<text y="-40" text-anchor="middle" font-size="40" font-weight="900" fill="#fff" stroke="{K}" stroke-width="9" paint-order="stroke" font-family="Cairo">{p["label"]}</text>' if p.get("label") else "") + '</g>')
        J(f'tl.to("#pn{i}_{k}",{{attr:{{transform:"translate({x:.0f} {y:.0f}) scale(1)"}},duration:.4,ease:"back.out(2.5)"}},{s + p.get("at", .5):.2f});')
    return "".join(out)

# ------------------------------------------------------------------ military
def soldier(col="#5a6a3a", helmet="#4a5a2a"):
    return (f'<g><circle cx="0" cy="-150" r="30" fill="#e8c398" stroke="{K}" stroke-width="5"/><path d="M-34,-156 Q0,-196 34,-156Z" fill="{helmet}" stroke="{K}" stroke-width="5"/>'
            f'<path d="M-26,-118 L26,-118 L30,-50 L-30,-50Z" fill="{col}" stroke="{K}" stroke-width="5"/><path d="M-14,-50 L-18,0 M14,-50 L18,0" stroke="{col}" stroke-width="18" stroke-linecap="round"/>'
            f'<path d="M-14,-50 L-18,0 M14,-50 L18,0" stroke="{K}" stroke-width="4" fill="none" opacity=".4"/><path d="M20,-110 L60,-150" stroke="#2a2a2a" stroke-width="10" stroke-linecap="round"/></g>')
def tank(col="#6a7a4a"):
    return (f'<g><rect x="-150" y="-60" width="300" height="60" rx="30" fill="#3a3a3a" stroke="{K}" stroke-width="6"/>'
            + "".join(f'<circle cx="{x}" cy="-30" r="20" fill="#5a5a5a" stroke="{K}" stroke-width="4"/>' for x in (-110, -55, 0, 55, 110))
            + f'<path d="M-140,-60 L-120,-110 L130,-110 L150,-60Z" fill="{col}" stroke="{K}" stroke-width="6"/><path d="M-60,-110 Q-50,-170 20,-170 Q70,-170 70,-110Z" fill="{col}" stroke="{K}" stroke-width="6"/>'
            + f'<path class="barrel" d="M60,-145 L230,-150" stroke="{K}" stroke-width="20" stroke-linecap="round"/><path d="M60,-145 L230,-150" stroke="{col}" stroke-width="10" stroke-linecap="round"/></g>')
def jet(col="#8a96a6"):
    return (f'<g><path d="M-160,0 Q-120,-22 130,-10 Q170,0 130,10 Q-120,22 -160,0Z" fill="{col}" stroke="{K}" stroke-width="5"/>'
            f'<path d="M-20,-6 L-90,-110 L-50,-110 L50,-6Z M-20,6 L-90,110 L-50,110 L50,6Z M-140,-4 L-180,-60 L-150,-60 L-110,-4Z" fill="{col}" stroke="{K}" stroke-width="5"/>'
            f'<ellipse cx="90" cy="-8" rx="30" ry="9" fill="#9ad0ff" stroke="{K}" stroke-width="3"/></g>')
def warship(col="#7a8290"):
    return (f'<g><path d="M-260,0 L260,0 L220,70 L-230,70Z" fill="{col}" stroke="{K}" stroke-width="6"/><path d="M-120,0 L-100,-70 L80,-70 L100,0Z" fill="{col}" stroke="{K}" stroke-width="6"/>'
            f'<path d="M-40,-70 L-30,-150 L20,-150 L30,-70Z" fill="{col}" stroke="{K}" stroke-width="6"/><path d="M110,-30 L230,-46" stroke="{K}" stroke-width="12"/></g>')
def explosion(i, k, x, y, sc, at, J):
    J(f'tl.fromTo("#ex{i}_{k}",{{attr:{{transform:"translate({x} {y}) scale(0)"}},opacity:1}},{{attr:{{transform:"translate({x} {y}) scale({sc})"}},duration:.35,ease:"power3.out"}},{at:.2f});'
      f'tl.to("#ex{i}_{k}",{{opacity:0,duration:.9,ease:"power1.in"}},{at + .5:.2f});')
    return (f'<g id="ex{i}_{k}" transform="translate({x} {y}) scale(0)"><path d="M0,-150 L40,-60 L140,-90 L80,-10 L160,50 L50,50 L40,150 L-20,60 L-120,120 L-80,20 L-160,-20 L-60,-50Z" fill="#ffb020" stroke="{K}" stroke-width="6"/>'
            f'<path d="M0,-80 L22,-30 L80,-46 L44,0 L90,30 L26,28 L20,80 L-12,34 L-70,64 L-44,10 L-90,-12 L-34,-28Z" fill="#fff3a0"/></g>')

def unit(kind, col):
    return {"soldiers": soldier(col or "#5a6a3a"), "tanks": tank(col or "#6a7a4a"), "jets": jet(col or "#8a96a6"), "ships": warship(col or "#7a8290")}[kind]

def force(i, k, f, s, dur, J):
    """rows of soldiers / tanks / jets / ships moving across: {"kind":"army","units":"soldiers|tanks|jets|ships","n":6,"from":-300,"to":700,"y":1600,"color":..,"flag":"IRQ","dir":1}"""
    u = f.get("units", "soldiers"); n = f.get("n", {"soldiers": 8, "tanks": 3, "jets": 3, "ships": 2}[u]); y = f.get("y", {"jets": 600, "ships": 1330}.get(u, 1600))
    gap = {"soldiers": 150, "tanks": 380, "jets": 300, "ships": 560}[u]; sc = f.get("scale", {"soldiers": 1.7, "tanks": 1.0, "jets": .8, "ships": .7}[u])
    d = f.get("dir", 1); x0, x1 = f.get("from", -400 if d > 0 else 1480), f.get("to", 500 if d > 0 else 580)
    flip = "" if d > 0 else " scale(-1 1)"
    body = "".join(f'<g transform="translate({-j * gap * d} {(j % 2) * (14 if u == "soldiers" else 0) + (j % 3) * (60 if u == "jets" else 0)}) scale({sc}){flip}">{unit(u, f.get("color"))}</g>' for j in range(n))
    fl = f'<g transform="translate({-30*d} {-420*sc if u == "soldiers" else -260})"><path d="M0,0 V200" stroke="#5a4a3a" stroke-width="8"/><g transform="translate({4 if d > 0 else -94} 0)">{flag(f["flag"], 90)}</g></g>' if f.get("flag") else ""
    J(f'tl.fromTo("#fo{i}_{k}",{{attr:{{transform:"translate({x0} {y})"}}}},{{attr:{{transform:"translate({x1} {y})"}},duration:{max(.8, dur):.2f},ease:"{f.get("ease", "power2.out")}"}},{s + f.get("at", 0):.2f});')
    if u == "soldiers": J(f'tl.fromTo("#fo{i}_{k} > g > g",{{y:0}},{{y:-10,duration:.18,yoyo:true,repeat:{int(dur/.18)},ease:"sine.inOut"}},{s:.2f});')
    if u == "tanks": J(f'tl.fromTo("#fo{i}_{k}",{{y:0}},{{y:3,duration:.08,yoyo:true,repeat:{int(dur/.08)},ease:"none"}},{s:.2f});')
    return f'<g id="fo{i}_{k}" transform="translate({x0} {y})">{fl}{body}</g>'

# ------------------------------------------------------------------ places
def place(i, p, t, sky, ground, R):
    if p == "battlefield":
        return (sky(i, "dark" if t != "night" else "night") + f'<path d="M-300,1250 L1380,1250 L1380,2300 L-300,2300Z" fill="#8a6a4a" stroke="{K}" stroke-width="5"/>'
                + "".join(f'<ellipse cx="{R(k+5)*1080:.0f}" cy="{1320+R(k+6)*500:.0f}" rx="{60+R(k)*60:.0f}" ry="{14+R(k+1)*10:.0f}" fill="#5a4030" stroke="{K}" stroke-width="4"/>' for k in range(7))
                + "".join(f'<circle cx="{R(k+30)*1080:.0f}" cy="{1180-R(k+31)*80:.0f}" r="{70+R(k+32)*60:.0f}" fill="#4a4040" opacity=".55"/>' for k in range(6))
                + f'<path d="M-300,1500 ' + " ".join(f"L{-300+k*60},{1500 + (k % 2)*16}" for k in range(30)) + f'" stroke="#3a3a3a" stroke-width="4" fill="none"/>')
    if p == "trenches":
        return (sky(i, t) + f'<path d="M-300,1250 L1380,1250 L1380,2300 L-300,2300Z" fill="#c8a070" stroke="{K}" stroke-width="5"/>'
                + f'<path d="M-300,1500 L1380,1500 L1380,1580 L-300,1580Z" fill="#6a4a2a" stroke="{K}" stroke-width="5"/>'
                + "".join(f'<rect x="{-260+k*120}" y="1440" width="100" height="60" rx="16" fill="#d8c090" stroke="{K}" stroke-width="4"/>' for k in range(12)))
    if p == "palace":
        return (f'<rect x="-300" y="-300" width="1680" height="2520" fill="#e8dcc0"/>' + "".join(f'<g transform="translate({x} 0)"><rect x="-40" y="300" width="80" height="1250" fill="#f6eed8" stroke="{K}" stroke-width="6"/><rect x="-60" y="280" width="120" height="40" fill="#d8c8a0" stroke="{K}" stroke-width="5"/></g>' for x in (120, 960))
                + f'<path d="M180,300 Q540,40 900,300" fill="none" stroke="#c9a24a" stroke-width="20"/><path d="M-300,1500 L1380,1500 L1380,2300 L-300,2300Z" fill="#7a2a2a" stroke="{K}" stroke-width="5"/>'
                + f'<path d="M250,1500 L830,1500 L900,1900 L180,1900Z" fill="#a83a3a" stroke="#c9a24a" stroke-width="10"/><g transform="translate(540 760)"><path d="M-160,-200 Q0,-280 160,-200 L160,40 L-160,40Z" fill="#c9a24a" stroke="{K}" stroke-width="6"/></g>')
    if p == "war_room":
        return (f'<rect x="-300" y="-300" width="1680" height="2520" fill="#1a1e26"/><rect x="90" y="380" width="900" height="560" rx="16" fill="#0e2a3a" stroke="#4a5a6a" stroke-width="14"/>'
                + f'<g opacity=".85"><path d="M200,500 Q300,460 420,520 Q520,560 600,500 Q700,450 820,540 L860,760 Q700,820 560,780 Q420,740 300,800 L220,760Z" fill="#2a6a4a" stroke="#6ad0a0" stroke-width="5"/>'
                + f'<path d="M380,640 L620,600" stroke="#ff4a3a" stroke-width="12" stroke-dasharray="20 14"/><circle cx="640" cy="598" r="16" fill="#ff4a3a"/></g>'
                + f'<path d="M-300,1450 L1380,1450 L1380,2300 L-300,2300Z" fill="#2a2e36" stroke="{K}" stroke-width="5"/><path d="M60,1380 L1020,1380 L1080,1460 L0,1460Z" fill="#5a3e24" stroke="{K}" stroke-width="6"/>'
                + f'<circle cx="540" cy="300" r="60" fill="#ffe8a0" opacity=".25"/><path d="M540,-300 V250" stroke="#333" stroke-width="6"/>')
    if p == "arab_city":
        return (sky(i, t) + "".join(f'<rect x="{-200+k*170}" y="{900+R(k+3)*250:.0f}" width="140" height="{700-R(k+3)*250:.0f}" fill="{["#e0cfa8", "#cdb890", "#e8dcc0"][k % 3]}" stroke="{K}" stroke-width="5"/>'
                                        + "".join(f'<rect x="{-180+k*170+c*44}" y="{960+R(k+3)*250+r*80:.0f}" width="24" height="34" fill="#5a7a9a"/>' for c in range(3) for r in range(4)) for k in range(9))
                + f'<g transform="translate(820 900)"><rect x="-26" y="-500" width="52" height="560" fill="#f0e6d0" stroke="{K}" stroke-width="5"/><path d="M-40,-500 L0,-600 L40,-500Z" fill="#2fa84f" stroke="{K}" stroke-width="5"/><rect x="-36" y="-380" width="72" height="24" fill="#d8c8a0" stroke="{K}" stroke-width="4"/></g>'
                + f'<g transform="translate(400 860)"><path d="M-150,40 Q0,-160 150,40Z" fill="#2fa84f" stroke="{K}" stroke-width="5"/><rect x="-160" y="40" width="320" height="160" fill="#f0e6d0" stroke="{K}" stroke-width="5"/></g>'
                + "".join(f'<g transform="translate({x} 1530)"><path d="M0,0 Q-6,-120 4,-220" stroke="#6b4a2e" stroke-width="18" fill="none"/>' + "".join(f'<path d="M4,-220 q{dx},-30 {dx*2},10" stroke="#2f7a3a" stroke-width="16" fill="none" stroke-linecap="round"/>' for dx in (-60, -30, 30, 60)) + '</g>' for x in (90, 980))
                + ground("#c8b890", "#a89870"))
    return None
PLACES = ["battlefield", "trenches", "palace", "war_room", "arab_city", "map"]
