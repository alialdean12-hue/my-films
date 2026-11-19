"""saw_5tory places: ~50 interior and exterior locations drawn in code.
place(name, time="night"|"day", weather=None|"rain"|"snow") -> (svg, floor_y)
People stand with feet at y 1500-1560; floor/ground starts at floor_y. Arabic signs are part of the place.
Every place keeps ids the builder animates: #rain (rain), #snow (snow), #flash (lightning, outdoor sky / windows), #lamp (flicker)."""
import math

F = "Cairo"

def _t(x, y, size, text, fill="#fff", anchor="middle", weight=900):
    return f'<text x="{x}" y="{y}" font-family="{F}" font-weight="{weight}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" direction="rtl">{text}</text>'

def _grad(id_, c1, c2, vertical=True):
    return f'<linearGradient id="{id_}" x1="0" y1="0" x2="{0 if vertical else 1}" y2="{1 if vertical else 0}"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient>'

# ---------------------------------------------------------------- primitives
def sky(time, y_end=1380, stars=True):
    if time == "day":
        g = _grad("skyg", "#5aa8e8", "#bfe3ff"); body = '<circle cx="840" cy="260" r="80" fill="#fff3b0"/>'
    elif time == "dusk":
        g = _grad("skyg", "#2a2a5a", "#e8885a"); body = '<circle cx="820" cy="900" r="90" fill="#ffb35c" opacity=".9"/>'
    else:
        g = _grad("skyg", "#020510", "#13284d"); body = '<circle cx="820" cy="300" r="70" fill="#e8eef6"/><circle cx="846" cy="286" r="62" fill="#0a1530"/>'
        if stars: body += "".join(f'<rect x="{(k*131)%1080}" y="{(k*73)%(y_end-300)}" width="4" height="4" fill="#fff" opacity=".7"/>' for k in range(40))
    return f'<defs>{g}</defs><rect width="1080" height="{y_end}" fill="url(#skyg)"/>{body}<rect id="flash" width="1080" height="{y_end}" fill="#dbeaff" opacity="0"/>'

def wall(c1, c2, y_end=1380):
    return f'<defs>{_grad("wallg2", c1, c2)}</defs><rect width="1080" height="{y_end}" fill="url(#wallg2)"/>'

def floor(kind, y=1380, c=None):
    h = 1920 - y
    if kind == "wood":
        return (f'<rect y="{y}" width="1080" height="{h}" fill="{c or "#3a2618"}"/><g stroke="#000" stroke-opacity=".35" stroke-width="3">'
                + "".join(f'<path d="M0,{y+40+k*90}H1080"/>' for k in range(h // 90)) + "".join(f'<path d="M{(k*277)%1080},{y+40+(k%6)*90}v90"/>' for k in range(12)) + '</g>')
    if kind == "tile":
        return f'<rect y="{y}" width="1080" height="{h}" fill="{c or "#c9ccd4"}"/><g stroke="#000" stroke-opacity=".18" stroke-width="3">' + "".join(f'<path d="M0,{y+k*90}H1080"/>' for k in range(h // 90 + 1)) + "".join(f'<path d="M{k*120},{y}V1920"/>' for k in range(10)) + '</g>'
    if kind == "checker":
        return f'<rect y="{y}" width="1080" height="{h}" fill="#e8e8e8"/>' + "".join(f'<rect x="{(i%9)*120}" y="{y+(i//9)*110}" width="120" height="110" fill="#222"/>' for i in range(9 * (h // 110 + 1)) if (i % 9 + i // 9) % 2 == 0)
    if kind == "carpet":
        return f'<rect y="{y}" width="1080" height="{h}" fill="{c or "#5a1e2a"}"/><rect y="{y}" width="1080" height="{h}" fill="url(#none)" opacity="0"/>' + "".join(f'<circle cx="{(k*97)%1080}" cy="{y+(k*53)%h}" r="3" fill="#000" opacity=".2"/>' for k in range(60))
    if kind == "concrete":
        return f'<rect y="{y}" width="1080" height="{h}" fill="{c or "#5a5e66"}"/><path d="M120,{y+120} l80,40 l20,80 M700,{y+300} l-60,60 M900,{y+100} l40,90" stroke="#000" stroke-opacity=".3" stroke-width="3" fill="none"/>' + "".join(f'<ellipse cx="{(k*211)%1080}" cy="{y+(k*97)%h}" rx="40" ry="10" fill="#000" opacity=".12"/>' for k in range(8))
    if kind == "grass":
        return f'<rect y="{y}" width="1080" height="{h}" fill="{c or "#2f5a2a"}"/>' + "".join(f'<path d="M{(k*37)%1080},{y+(k*71)%h} l-6,-20 M{(k*37)%1080+6},{y+(k*71)%h} l4,-22" stroke="#4a7a3a" stroke-width="4"/>' for k in range(90))
    if kind == "sand":
        return f'<rect y="{y}" width="1080" height="{h}" fill="{c or "#d8b47a"}"/><path d="M0,{y+120} Q300,{y+60} 600,{y+140} T1080,{y+100}" stroke="#b8945a" stroke-width="6" fill="none" opacity=".6"/><path d="M0,{y+320} Q400,{y+260} 800,{y+340} T1300,{y+300}" stroke="#b8945a" stroke-width="6" fill="none" opacity=".5"/>'
    if kind == "asphalt":
        return f'<rect y="{y}" width="1080" height="{h}" fill="{c or "#2a2c30"}"/><rect y="{y}" width="1080" height="40" fill="#5a5e66"/>' + "".join(f'<rect x="{k*260+40}" y="{y+240}" width="140" height="16" fill="#e8e2c0" opacity=".8"/>' for k in range(5))
    if kind == "snow":
        return f'<rect y="{y}" width="1080" height="{h}" fill="#e8f0f8"/><path d="M0,{y} Q270,{y-30} 540,{y} T1080,{y}" fill="#e8f0f8"/>' + "".join(f'<ellipse cx="{(k*157)%1080}" cy="{y+(k*83)%h}" rx="50" ry="8" fill="#c9d8e8" opacity=".6"/>' for k in range(10))
    if kind == "marble":
        return f'<rect y="{y}" width="1080" height="{h}" fill="{c or "#e8e2d8"}"/><path d="M0,{y+100} q200,40 400,-10 t500,30 M100,{y+300} q300,-50 600,20 t400,-20" stroke="#b8b0a0" stroke-width="3" fill="none"/>' + "".join(f'<path d="M0,{y+k*130}H1080" stroke="#000" stroke-opacity=".08" stroke-width="3"/>' for k in range(5))
    if kind == "deck":
        return f'<rect y="{y}" width="1080" height="{h}" fill="#8a6a42"/>' + "".join(f'<path d="M{k*90},{y}V1920" stroke="#5a4228" stroke-width="4"/>' for k in range(13))
    if kind == "metal":
        return f'<rect y="{y}" width="1080" height="{h}" fill="#4a5058"/>' + "".join(f'<path d="M{(k*60)%1080},{y+(k//18)*60+20} l20,20 M{(k*60)%1080+20},{y+(k//18)*60+20} l-20,20" stroke="#3a4048" stroke-width="3"/>' for k in range(18 * (h // 60)))
    return f'<rect y="{y}" width="1080" height="{h}" fill="{c or "#3a2618"}"/>'

def bricks(c="#6a3a2a", y_end=1380, x0=0, x1=1080):
    out = f'<rect x="{x0}" width="{x1-x0}" height="{y_end}" fill="{c}"/><g stroke="#000" stroke-opacity=".3" stroke-width="3">'
    for r in range(y_end // 50):
        out += f'<path d="M{x0},{r*50}H{x1}"/>' + "".join(f'<path d="M{x0+(k*120+(60 if r%2 else 0))},{r*50}v50"/>' for k in range((x1-x0)//120 + 1))
    return out + '</g>'

def wpattern(kind, y_end=1380):
    if kind == "wallpaper": return '<g opacity=".12" fill="#fff">' + "".join(f'<circle cx="{40+(i%14)*80+(i//14%2)*40}" cy="{40+(i//14)*80}" r="6"/>' for i in range(14 * (y_end // 80))) + '</g>'
    if kind == "panels": return '<g stroke="#000" stroke-opacity=".3" stroke-width="4">' + "".join(f'<path d="M{k*180},0V{y_end}"/>' for k in range(7)) + f'<path d="M0,{y_end-380}H1080"/></g>'
    if kind == "stone": return '<g stroke="#000" stroke-opacity=".25" stroke-width="4">' + "".join(f'<path d="M0,{r*120}H1080"/>' + "".join(f'<path d="M{(k*200+(100 if r%2 else 0))},{r*120}v120"/>' for k in range(6)) for r in range(y_end // 120)) + '</g>'
    if kind == "logs": return "".join(f'<rect y="{r*70}" width="1080" height="64" rx="30" fill="#7a5232" stroke="#4a3018" stroke-width="4"/>' for r in range(y_end // 70))
    if kind == "metal": return '<g stroke="#000" stroke-opacity=".35" stroke-width="4">' + "".join(f'<path d="M{k*120},0V{y_end}"/>' for k in range(10)) + '</g>' + "".join(f'<circle cx="{k*120+12}" cy="{r*200+20}" r="4" fill="#888"/>' for k in range(9) for r in range(y_end // 200))
    if kind == "tiles": return '<g stroke="#fff" stroke-opacity=".12" stroke-width="3">' + "".join(f'<path d="M0,{k*90}H1080"/>' for k in range(y_end // 90)) + "".join(f'<path d="M{k*90},0V{y_end}"/>' for k in range(13)) + '</g>'
    return ""

def window2(x, y, w, h, view="night", frame="#070b14", bars=False):
    v = {"night": "#0b2042", "day": "#9fd3ff", "city": "#0b1a33", "sea": "#1a4a6a", "dark": "#05070c"}[view]
    out = f'<rect x="{x-12}" y="{y-12}" width="{w+24}" height="{h+24}" fill="{frame}"/><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{v}"/>'
    if view == "city":
        out += "".join(f'<rect x="{x+k*w//6}" y="{y+h-(60+(k*53)%150)}" width="{w//6-6}" height="{60+(k*53)%150}" fill="#111a2a"/>' for k in range(6))
        out += "".join(f'<rect x="{x+10+(k*37)%(w-20)}" y="{y+h-20-(k*29)%120}" width="6" height="8" fill="#ffd27a"/>' for k in range(16))
    if view == "sea": out += f'<rect x="{x}" y="{y+h*0.55}" width="{w}" height="{h*0.45}" fill="#0e2a44"/>'
    out += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#dbeaff" opacity="0" class="wflash"/>'
    if bars: out += "".join(f'<rect x="{x+k*w//5}" y="{y}" width="8" height="{h}" fill="#333"/>' for k in range(1, 5))
    return out

def sign(x, y, text, bg="#c4262e", fg="#fff", w=None, size=56):
    w = w or (70 + size * 0.62 * len(text))
    return f'<rect x="{x-w/2}" y="{y-size}" width="{w}" height="{size*1.5}" rx="10" fill="{bg}" stroke="#000" stroke-opacity=".4" stroke-width="4"/>' + _t(x, y + size * 0.35, size, text, fg)

def neon(x, y, text, color="#ff3b8a", size=70):
    return f'<g><text x="{x}" y="{y}" font-family="{F}" font-weight="900" font-size="{size}" fill="none" stroke="{color}" stroke-width="10" opacity=".35" text-anchor="middle" direction="rtl">{text}</text>' + _t(x, y, size, text, color) + '</g>'

def ceiling_lamp(x, y=0, lit=True, col="#ffd27a"):
    return f'<path d="M{x},{y} V{y+120}" stroke="#222" stroke-width="5"/><path d="M{x-60},{y+170} L{x+60},{y+170} L{x+30},{y+120} L{x-30},{y+120} Z" fill="#2a2a2a"/>' + (f'<polygon id="lamp" points="{x-60},{y+170} {x+60},{y+170} {x+360},1920 {x-360},1920" fill="{col}" fill-opacity=".07"/>' if lit else "")

def fluorescent(y=60):
    return "".join(f'<rect x="{x}" y="{y}" width="220" height="18" rx="8" fill="#eef8ff"/><rect x="{x-40}" y="{y+18}" width="300" height="400" fill="#eef8ff" opacity=".04"/>' for x in (120, 740))

def skyline(y=1380, col="#0a1222", lit=True):
    out = ""
    for k in range(12):
        bw = 70 + (k * 37) % 80; bh = 200 + (k * 97) % 420; bx = k * 92 - 20
        out += f'<rect x="{bx}" y="{y-bh}" width="{bw}" height="{bh}" fill="{col}"/>'
        if lit: out += "".join(f'<rect x="{bx+10+(j*23)%(bw-20)}" y="{y-bh+20+(j*47)%(bh-40)}" width="8" height="12" fill="#ffd27a" opacity=".8"/>' for j in range(6))
    return out

def streetlamp(x, y=1380, lit=True):
    return (f'<rect x="{x-6}" y="{y-560}" width="12" height="560" fill="#222"/><path d="M{x},{y-560} q0,-40 60,-40" stroke="#222" stroke-width="12" fill="none"/><rect x="{x+40}" y="{y-610}" width="60" height="22" rx="6" fill="#333"/>'
            + (f'<polygon points="{x+46},{y-588} {x+94},{y-588} {x+260},{y+80} {x-120},{y+80}" fill="#ffe2a0" opacity=".1"/><circle cx="{x+70}" cy="{y-584}" r="14" fill="#ffe8a8"/>' if lit else ""))

def tree(x, y=1380, s=1.0, pine=False, col="#1f4a2a"):
    if pine:
        return f'<rect x="{x-10*s}" y="{y-60*s}" width="{20*s}" height="{60*s}" fill="#4a2f1f"/>' + "".join(f'<path d="M{x},{y-(60+k*90)*s-120*s} L{x+(110-k*20)*s},{y-(60+k*90)*s} L{x-(110-k*20)*s},{y-(60+k*90)*s} Z" fill="{col}"/>' for k in range(3))
    return f'<rect x="{x-16*s}" y="{y-260*s}" width="{32*s}" height="{260*s}" fill="#4a2f1f"/>' + "".join(f'<circle cx="{x+dx*s}" cy="{y-(300+dy)*s}" r="{r*s}" fill="{col}"/>' for dx, dy, r in ((-70, 0, 90), (70, 10, 90), (0, 80, 110), (-30, -40, 80), (40, -50, 80)))

def palm(x, y=1380, s=1.0):
    return f'<path d="M{x},{y} q{-20*s},{-200*s} {10*s},{-420*s}" stroke="#7a5a32" stroke-width="{26*s}" fill="none"/>' + "".join(f'<path d="M{x+10*s},{y-420*s} q{dx*s},{-60*s} {dx*2*s},{dy*s}" stroke="#2f6a2a" stroke-width="{22*s}" fill="none" stroke-linecap="round"/>' for dx, dy in ((-80, 40), (80, 40), (-50, -10), (60, -20), (0, -60)))

def car(x, y=1520, col="#8a1e2e", facing=1):
    return (f'<g transform="translate({x} {y}) scale({facing} 1)"><path d="M-230,-40 L-210,-120 Q-150,-170 -40,-170 L60,-170 Q130,-160 170,-110 L230,-90 L240,-30 L-230,-30 Z" fill="{col}" stroke="#111" stroke-width="5"/>'
            f'<path d="M-180,-120 Q-130,-158 -50,-158 L-50,-116 Z M-30,-158 L50,-158 Q110,-150 140,-116 L-30,-116 Z" fill="#9fc6e8" stroke="#111" stroke-width="3"/>'
            f'<circle cx="-140" cy="-28" r="42" fill="#111"/><circle cx="-140" cy="-28" r="18" fill="#9aa4b2"/><circle cx="150" cy="-28" r="42" fill="#111"/><circle cx="150" cy="-28" r="18" fill="#9aa4b2"/>'
            f'<rect x="210" y="-96" width="26" height="16" fill="#ffe8a8"/></g>')

def bench(x, y=1500, w=320):
    return f'<rect x="{x-w/2}" y="{y-110}" width="{w}" height="20" fill="#7a5232"/><rect x="{x-w/2}" y="{y-60}" width="{w}" height="22" fill="#7a5232"/><rect x="{x-w/2+20}" y="{y-40}" width="14" height="40" fill="#222"/><rect x="{x+w/2-34}" y="{y-40}" width="14" height="40" fill="#222"/>'

def shelf_wall(x0, x1, y_top, rows=4, colors=("#c4262e", "#2f6bd8", "#e8b33a", "#3a8a4a", "#e8e8e8")):
    out = f'<rect x="{x0}" y="{y_top}" width="{x1-x0}" height="{1380-y_top}" fill="#5a3e2a"/>'
    rh = (1380 - y_top) // rows
    for r in range(rows):
        yy = y_top + (r + 1) * rh
        out += f'<rect x="{x0}" y="{yy-12}" width="{x1-x0}" height="12" fill="#2a1a10"/>' + "".join(f'<rect x="{x0+10+k*46}" y="{yy-12-(50+(k*13)%30)}" width="36" height="{50+(k*13)%30}" rx="5" fill="{colors[(k+r)%len(colors)]}"/>' for k in range((x1 - x0 - 20) // 46))
    return out

def counter_(x0, x1, y_top=1180, col="#6b4a32", top="#d9d2c4"):
    return f'<rect x="{x0}" y="{y_top}" width="{x1-x0}" height="{1400-y_top}" fill="{col}" stroke="#2a1a10" stroke-width="5"/><rect x="{x0-10}" y="{y_top-20}" width="{x1-x0+20}" height="26" fill="{top}"/>'

def curtain(x0, x1, y0=0, y1=1380, col="#8a1e2e"):
    return f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" fill="{col}"/>' + "".join(f'<path d="M{x},{y0} V{y1}" stroke="#000" stroke-opacity=".25" stroke-width="10"/>' for x in range(x0 + 30, x1, 60))

def pillar(x, y_end=1380, col="#d8d0c0"):
    return f'<rect x="{x-50}" y="0" width="100" height="{y_end}" fill="{col}"/><rect x="{x-70}" y="{y_end-40}" width="140" height="40" fill="{col}" stroke="#000" stroke-opacity=".2" stroke-width="3"/><path d="M{x-30},0 V{y_end-40} M{x},0 V{y_end-40} M{x+30},0 V{y_end-40}" stroke="#000" stroke-opacity=".12" stroke-width="4"/>'

def rain_overlay():
    base = [((i * 53) % 1080, (i * 137) % 520) for i in range(40)]
    streaks = "".join(f'<path d="M{x},{y+k*520} l-14,70"/>' for k in range(5) for x, y in base)
    return f'<g transform="translate(0 -520)"><g id="rain" stroke="#9fd0ff" stroke-width="3" opacity=".55">{streaks}</g></g>'

def snow_overlay():
    base = [((i * 71) % 1080, (i * 113) % 520, 3 + (i % 3) * 2) for i in range(45)]
    flakes = "".join(f'<circle cx="{x}" cy="{y+k*520}" r="{r}"/>' for k in range(5) for x, y, r in base)
    return f'<g transform="translate(0 -520)"><g id="snow" fill="#fff" opacity=".85">{flakes}</g></g>'

# ---------------------------------------------------------------- places
def _p_street(t):   return sky(t) + skyline(1300, lit=t != "day") + floor("asphalt", 1300) + streetlamp(160, 1340, t != "day") + sign(820, 1080, "صيدلية", "#3a8a4a") + f'<rect x="620" y="1110" width="400" height="200" fill="#1a2230"/><rect x="640" y="1130" width="160" height="180" fill="{"#ffd27a" if t!="day" else "#9fd3ff"}" opacity=".6"/>', 1300
def _p_alley(t):    return sky(t, 600) + bricks("#5a2e22", 1400, 0, 300) + bricks("#4a2a20", 1400, 780, 1080) + f'<rect x="300" y="600" width="480" height="800" fill="#0a0c12"/>' + streetlamp(860, 1400, True) + floor("concrete", 1400, "#2a2c30") + f'<rect x="80" y="1260" width="200" height="160" rx="10" fill="#2f4a3a" stroke="#111" stroke-width="5"/><rect x="70" y="1240" width="220" height="30" fill="#24382c"/>', 1400
def _p_park(t):     return sky(t) + tree(140, 1340) + tree(960, 1350, 1.1) + tree(560, 1260, .6, col="#2a5a32") + floor("grass", 1340) + f'<path d="M380,1920 Q520,1600 520,1340 L620,1340 Q640,1600 760,1920 Z" fill="#c9b48a" opacity=".7"/>' + bench(820, 1520) + streetlamp(300, 1360, t != "day"), 1340
def _p_beach(t):    return sky(t, 1100) + f'<rect y="1100" width="1080" height="300" fill="{"#2a6a9a" if t=="day" else "#0e2a44"}"/><path d="M0,1180 q60,-14 120,0 t120,0 t120,0 t120,0 t120,0 t120,0 t120,0 t120,0 t120,0" stroke="#e8f4ff" stroke-width="4" fill="none" opacity=".5"/>' + floor("sand", 1360) + palm(980, 1400, .9), 1360
def _p_desert_camp(t): return sky(t, 1300) + f'<path d="M0,1300 Q260,1180 540,1260 Q800,1200 1080,1280 L1080,1400 L0,1400 Z" fill="#b8945a"/>' + floor("sand", 1380) + f'<path d="M640,1380 L840,1060 L1060,1380 Z" fill="#8a3a2a" stroke="#4a1e14" stroke-width="5"/><path d="M840,1060 L800,1380 L880,1380 Z" fill="#2a120c"/>' + f'<g transform="translate(260 1560)"><path d="M-40,0 l40,-90 l40,90 Z" fill="#ff8a2a"/><path d="M-20,0 l20,-50 l20,50 Z" fill="#ffd27a"/><rect x="-60" y="0" width="120" height="14" fill="#4a2a1a"/></g>', 1380
def _p_parking(t):  return wall("#22262c", "#2e3238") + fluorescent() + "".join(pillar(x, 1380, "#6a6e76") for x in (120, 960)) + floor("concrete", 1380, "#3a3e44") + "".join(f'<rect x="{x}" y="1400" width="14" height="300" fill="#e8e2c0" opacity=".7" transform="skewX(-20)"/>' for x in (520, 900)) + car(640, 1520, "#2f4a7a") + sign(540, 300, "P", "#2f6bd8", w=120, size=90), 1380
def _p_rooftop(t):  return sky(t, 1240) + skyline(1240, lit=t != "day") + f'<rect y="1240" width="1080" height="160" fill="#4a4e56"/>' + "".join(f'<rect x="{k*90}" y="1180" width="10" height="70" fill="#888"/>' for k in range(13)) + '<rect y="1180" width="1080" height="10" fill="#888"/>' + f'<rect x="760" y="900" width="220" height="280" fill="#6a5a4a"/><rect x="740" y="880" width="260" height="30" fill="#5a4a3a"/>' + floor("concrete", 1380, "#5a5e66"), 1380
def _p_platform(t): return wall("#2a3040", "#3a4256", 1280) + fluorescent(40) + sign(540, 360, "رصيف 3", "#1f2d4d", size=64) + f'<rect y="1280" width="1080" height="120" fill="#111"/><rect y="1300" width="1080" height="12" fill="#9aa4b2"/><rect y="1350" width="1080" height="12" fill="#9aa4b2"/>' + floor("tile", 1400, "#8a8e96") + '<rect y="1400" width="1080" height="24" fill="#ffd21f"/>' + bench(860, 1560, 260), 1400
def _p_train_cabin(t): return wall("#3a4a5a", "#2a3644", 1380) + "".join(window2(60 + k * 340, 360, 280, 260, "night" if t != "day" else "day") for k in range(3)) + "".join(f'<rect x="{40+k*340}" y="900" width="300" height="300" rx="30" fill="#2f4a7a" stroke="#1a2a4a" stroke-width="6"/>' for k in range(3)) + floor("metal", 1380) + '<rect x="530" y="0" width="20" height="1380" fill="#c9ccd4"/>', 1380
def _p_airport(t):  return wall("#cfd8e2", "#e8eef6", 1380) + window2(40, 180, 1000, 700, "day" if t == "day" else "night", "#5a6a7a") + f'<path d="M300,700 L760,640 L820,600 L860,640 L760,680 L600,720 L700,800 L660,808 L520,730 L340,750 Z" fill="#e8eef6" opacity=".9"/>' + sign(540, 1010, "البوابة 12", "#2a2e3a", "#ffd21f", size=58) + "".join(f'<rect x="{80+k*130}" y="1220" width="110" height="160" rx="12" fill="#3a4a6a"/>' for k in range(8)) + floor("marble", 1380, "#d8dce4"), 1380
def _p_hospital(t): return wall("#cfe0e8", "#e8f2f6") + window2(700, 260, 300, 360, "day" if t == "day" else "night", "#e8eef6") + f'<rect x="740" y="1100" width="320" height="200" rx="16" fill="#f4f6f8" stroke="#9aa4b2" stroke-width="5"/><rect x="740" y="1060" width="40" height="320" fill="#9aa4b2"/><rect x="60" y="560" width="200" height="140" rx="10" fill="#111"/><path d="M80,640 l40,0 l15,-40 l20,70 l15,-30 l70,0" stroke="#3ddc84" stroke-width="5" fill="none"/><path d="M300,300 V1380" stroke="#9aa4b2" stroke-width="8"/><rect x="290" y="300" width="60" height="80" rx="10" fill="#bfe3ff" opacity=".7"/>' + floor("tile", 1380, "#bcc6cc"), 1380
def _p_police(t):   return wall("#2a3446", "#3a465a") + wpattern("panels") + sign(540, 240, "قسم الشرطة", "#1f2d4d", size=60) + f'<rect x="60" y="420" width="320" height="260" fill="#c9a26a" stroke="#5a3a22" stroke-width="8"/>' + "".join(f'<rect x="{90+(k%3)*96}" y="{450+(k//3)*110}" width="80" height="90" fill="#f4efe2" transform="rotate({(k*7)%11-5} {130+(k%3)*96} {495+(k//3)*110})"/>' for k in range(6)) + counter_(620, 1080, 1160, "#3a2a1e") + floor("tile", 1380, "#5a5e66"), 1380
def _p_interrog(t): return wall("#2a2c30", "#1a1c20") + f'<rect x="640" y="300" width="380" height="260" fill="#0a0c10" stroke="#555" stroke-width="10"/><rect x="650" y="310" width="360" height="240" fill="#22262e" opacity=".8"/>' + ceiling_lamp(540) + f'<rect x="300" y="1240" width="480" height="30" fill="#4a4e56"/><rect x="330" y="1270" width="20" height="200" fill="#333"/><rect x="730" y="1270" width="20" height="200" fill="#333"/>' + floor("concrete", 1380, "#3a3c40"), 1380
def _p_court(t):    return wall("#4a2e1e", "#5a3a26") + wpattern("panels") + f'<rect x="240" y="760" width="600" height="420" fill="#6a4228" stroke="#2a1a10" stroke-width="8"/><rect x="220" y="740" width="640" height="40" fill="#7a5232"/>' + sign(540, 900, "المحكمة", "#2a1a10", "#e8c34a", size=56) + f'<rect x="900" y="1000" width="160" height="200" fill="#6a4228" stroke="#2a1a10" stroke-width="6"/>' + floor("wood", 1380, "#3a2416"), 1380
def _p_classroom(t): return wall("#e8e2c8", "#d8d0b0") + f'<rect x="120" y="260" width="840" height="440" fill="#2f4a3a" stroke="#6a4a2a" stroke-width="16"/>' + _t(540, 420, 64, "الدرس الأول", "#f4f4f4") + _t(540, 540, 48, "2 + 2 = 4", "#f4f4f4") + "".join(f'<rect x="{60+k*260}" y="1230" width="200" height="24" fill="#a07a4a"/><rect x="{80+k*260}" y="1254" width="12" height="120" fill="#555"/><rect x="{228+k*260}" y="1254" width="12" height="120" fill="#555"/>' for k in range(4)) + floor("tile", 1380, "#a8a090"), 1380
def _p_library(t):  return wall("#3a2a1e", "#2a1e14") + shelf_wall(0, 330, 200, 5, ("#7a2f35", "#2f5a7a", "#7a6a2f", "#3a6a3a")) + shelf_wall(750, 1080, 200, 5, ("#7a2f35", "#2f5a7a", "#7a6a2f", "#3a6a3a")) + ceiling_lamp(540) + f'<rect x="380" y="1180" width="320" height="24" fill="#5a3a26"/><rect x="400" y="1204" width="16" height="170" fill="#3a2a1a"/><rect x="664" y="1204" width="16" height="170" fill="#3a2a1a"/>' + floor("carpet", 1380, "#4a1e1e"), 1380
def _p_museum(t):   return wall("#e8e2d8", "#d8d0c4") + "".join(pillar(x, 1380, "#f0eae0") for x in (80, 1000)) + f'<rect x="300" y="380" width="220" height="280" fill="#c9a24a"/><rect x="316" y="396" width="188" height="248" fill="#3a2a4a"/><circle cx="410" cy="500" r="44" fill="#e8c8a8"/><rect x="600" y="420" width="240" height="180" fill="#c9a24a"/><rect x="616" y="436" width="208" height="148" fill="#4a6a3a"/>' + f'<rect x="440" y="1100" width="200" height="280" fill="#f4f0e8" stroke="#b8b0a0" stroke-width="5"/><path d="M500,1100 q-30,-80 40,-140 q70,60 40,140 Z" fill="#2f6bd8" stroke="#1a3a7a" stroke-width="4"/>' + sign(540, 230, "المتحف الوطني", "#2a2a2a", "#e8c34a", size=52) + floor("marble", 1380), 1380
def _p_bank(t):     return wall("#2a3a3a", "#3a4a4a") + wpattern("panels") + sign(540, 230, "بنك المدينة", "#1f3a2f", "#e8c34a", size=60) + counter_(0, 700, 1100, "#5a4a3a", "#c9ccd4") + f'<rect x="0" y="700" width="700" height="380" fill="#bfe3ff" opacity=".18" stroke="#9aa4b2" stroke-width="6"/><circle cx="890" cy="900" r="170" fill="#6a6e76" stroke="#3a3e44" stroke-width="14"/><circle cx="890" cy="900" r="40" fill="#3a3e44"/>' + "".join(f'<path d="M890,900 l{120*math.cos(k*0.785):.0f},{120*math.sin(k*0.785):.0f}" stroke="#3a3e44" stroke-width="10"/>' for k in range(8)) + floor("marble", 1380, "#c8c0b4"), 1380
def _p_jewelry(t):  return wall("#2a1e2a", "#3a2a3a") + "".join(f'<rect x="{60+k*340}" y="1060" width="300" height="320" fill="#3a2a3a" stroke="#c9a24a" stroke-width="5"/><rect x="{60+k*340}" y="1060" width="300" height="140" fill="#bfe3ff" opacity=".25"/><circle cx="{140+k*340}" cy="1170" r="14" fill="none" stroke="#e8c34a" stroke-width="5"/><circle cx="{210+k*340}" cy="1165" r="10" fill="#9fd3ff"/><circle cx="{270+k*340}" cy="1170" r="14" fill="none" stroke="#c9ccd4" stroke-width="5"/>' for k in range(3)) + sign(540, 300, "مجوهرات النجمة", "#3a2a3a", "#e8c34a", size=56) + ceiling_lamp(540, 0, True, "#fff3d0") + floor("marble", 1380, "#d8c8b8"), 1380
def _p_restaurant(t): return wall("#3a1e1a", "#4a2a22") + wpattern("wallpaper") + "".join(f'<ellipse cx="{x}" cy="1240" rx="150" ry="30" fill="#f4f0e8"/><rect x="{x-140}" y="1240" width="280" height="140" fill="#f4f0e8"/><rect x="{x-14}" y="1180" width="10" height="60" fill="#c9a24a"/>' for x in (240, 840)) + f'<g transform="translate(540 120)"><path d="M-120,0 h240 l-40,80 h-160 Z" fill="#c9a24a"/>' + "".join(f'<circle cx="{-100+k*50}" cy="96" r="12" fill="#ffe8a8"/>' for k in range(5)) + '</g>' + floor("checker", 1380), 1380
def _p_cafe(t):     return wall("#4a3426", "#5a4230") + f'<rect x="80" y="240" width="420" height="320" fill="#1a1a1a" stroke="#6a4a2a" stroke-width="10"/>' + _t(290, 320, 46, "القائمة", "#f4f4f4") + _t(290, 400, 36, "قهوة عربية 10", "#e8e2d0") + _t(290, 460, 36, "شاي 5", "#e8e2d0") + counter_(560, 1080, 1120, "#3a2a1e") + f'<rect x="800" y="960" width="160" height="140" rx="10" fill="#9aa4b2" stroke="#555" stroke-width="5"/>' + neon(800, 260, "مقهى", "#ffb35c", 80) + floor("wood", 1380, "#5a3a26"), 1380
def _p_market(t):   return wall("#e8eef0", "#f4f8fa") + fluorescent() + "".join(shelf_wall(x, x + 280, 300, 5) for x in (0, 400, 800)) + sign(540, 200, "سوبرماركت", "#c4262e", size=56) + floor("tile", 1380, "#d8dce0"), 1380
def _p_gas(t):      return sky(t, 1200) + f'<rect x="80" y="420" width="920" height="70" fill="#c4262e"/><rect x="200" y="490" width="30" height="760" fill="#c9ccd4"/><rect x="850" y="490" width="30" height="760" fill="#c9ccd4"/>' + _t(540, 475, 52, "محطة وقود", "#fff") + f'<rect y="1200" width="1080" height="200" fill="#3a3e44"/>' + "".join(f'<rect x="{x}" y="1020" width="110" height="260" rx="10" fill="#e8e8e8" stroke="#555" stroke-width="5"/><rect x="{x+20}" y="1050" width="70" height="50" fill="#111"/><path d="M{x+110},1120 q40,10 30,90" stroke="#111" stroke-width="8" fill="none"/>' for x in (330, 640)) + floor("asphalt", 1380), 1380
def _p_garage(t):   return wall("#3a3e44", "#2a2e34") + f'<rect x="40" y="360" width="400" height="300" fill="#5a4a3a"/>' + "".join(f'<path d="M{70+k*55},380 v{60+(k%3)*30}" stroke="#9aa4b2" stroke-width="10" stroke-linecap="round"/>' for k in range(7)) + car(700, 1480, "#c9ccd4", -1) + f'<rect x="460" y="1480" width="500" height="20" fill="#e8b33a"/>' + floor("concrete", 1380, "#4a4e54") + '<ellipse cx="300" cy="1700" rx="120" ry="24" fill="#111" opacity=".5"/>', 1380
def _p_barn(t):     return wall("#7a3a2a", "#5a2a1e") + wpattern("panels") + f'<path d="M340,200 L540,60 L740,200 Z" fill="#5a2a1e"/>' + "".join(f'<rect x="{x}" y="{y}" width="200" height="120" fill="#e8c87a" stroke="#b8944a" stroke-width="5"/>' for x, y in ((40, 1260), (240, 1260), (140, 1140), (840, 1260))) + floor("plain", 1380, "#8a6a3a"), 1380
def _p_cabin(t):    return wpattern("logs") + window2(660, 320, 300, 300, "night" if t != "day" else "day", "#4a3018") + f'<rect x="60" y="900" width="320" height="480" fill="#6a6a6a" stroke="#3a3a3a" stroke-width="8"/><rect x="120" y="1100" width="200" height="280" fill="#1a0c08"/><path d="M160,1380 l40,-110 l40,110 Z" fill="#ff8a2a"/><path d="M190,1380 l20,-60 l20,60 Z" fill="#ffd27a"/>' + floor("wood", 1380, "#4a3018"), 1380
def _p_ship_cabin(t): return wall("#5a3a22", "#4a2e1a") + wpattern("panels") + "".join(f'<circle cx="{x}" cy="500" r="110" fill="#c9a24a"/><circle cx="{x}" cy="500" r="86" fill="{"#1a4a6a" if t!="day" else "#7ab8e8"}"/>' for x in (300, 780)) + ceiling_lamp(540, 0, True) + floor("deck", 1380), 1380
def _p_ship_deck(t): return sky(t, 1100) + f'<rect y="1100" width="1080" height="200" fill="{"#0e2a44" if t!="day" else "#2a6a9a"}"/><rect x="900" y="0" width="30" height="1300" fill="#5a3a22"/><path d="M930,100 L930,900 L1080,860 Z" fill="#e8e2d0"/>' + f'<rect y="1240" width="1080" height="16" fill="#c9ccd4"/>' + "".join(f'<rect x="{k*120}" y="1240" width="10" height="140" fill="#c9ccd4"/>' for k in range(10)) + floor("deck", 1380), 1380
def _p_lobby(t):    return wall("#3a2a20", "#4a3628") + "".join(pillar(x, 1380, "#c8b89a") for x in (100, 980)) + counter_(240, 840, 1100, "#5a3a22", "#c9a24a") + sign(540, 300, "فندق الواحة", "#2a1e14", "#e8c34a", size=60) + f'<g transform="translate(540 60)"><path d="M-160,0 h320 l-60,100 h-200 Z" fill="#c9a24a"/>' + "".join(f'<circle cx="{-140+k*56}" cy="118" r="14" fill="#ffe8a8"/>' for k in range(6)) + '</g>' + floor("marble", 1380, "#d8c8b0"), 1380
def _p_elevator(t): return wall("#9aa4b2", "#6a7480", 1420) + wpattern("metal", 1420) + f'<rect x="900" y="560" width="120" height="380" rx="10" fill="#3a3e44"/>' + "".join(f'<circle cx="{930+(k%2)*60}" cy="{620+(k//2)*70}" r="20" fill="#c9ccd4"/>' + _t(930 + (k % 2) * 60, 628 + (k // 2) * 70, 22, str(k + 1), "#222") for k in range(8)) + f'<rect x="420" y="120" width="240" height="90" rx="10" fill="#111"/>' + _t(540, 190, 64, "7 ▲", "#ff3b3b") + floor("metal", 1420), 1420
def _p_corridor(t): return wall("#5a4a3a", "#4a3a2e") + f'<path d="M0,0 L380,520 L700,520 L1080,0 Z" fill="#3a2e24"/><path d="M0,1380 L380,880 L700,880 L1080,1380 Z" fill="#4a1e1e"/><rect x="380" y="520" width="320" height="360" fill="#2a1e16"/>' + "".join(f'<path d="M{x1},{y1} L{x2},{y2} L{x2},{y3} L{x1},{y4} Z" fill="#6a4a2a" stroke="#2a1a10" stroke-width="4"/>' for x1, y1, x2, y2, y3, y4 in ((60, 300, 200, 420, 980, 1180), (880, 420, 1020, 300, 1180, 980))) + _t(130, 400, 44, "304", "#e8c34a") + _t(950, 400, 44, "305", "#e8c34a") + floor("carpet", 1380, "#4a1e1e"), 1380
def _p_gym(t):      return wall("#2a2e36", "#3a3e46") + f'<rect x="60" y="300" width="960" height="500" fill="#9fb3c6" opacity=".25" stroke="#c9ccd4" stroke-width="6"/>' + f'<rect x="100" y="1180" width="360" height="20" fill="#555"/><circle cx="110" cy="1190" r="60" fill="#222"/><circle cx="450" cy="1190" r="60" fill="#222"/><rect x="700" y="1000" width="300" height="300" fill="#333"/><rect x="720" y="1300" width="260" height="60" fill="#111"/>' + neon(540, 230, "نادي القوة", "#3ddc84", 72) + floor("plain", 1380, "#222"), 1380
def _p_lockers(t):  return wall("#cfd8e2", "#e8eef6") + "".join(f'<rect x="{k*108}" y="560" width="104" height="820" fill="#2f5a8a" stroke="#1a3a5a" stroke-width="4"/><rect x="{k*108+16}" y="620" width="70" height="8" fill="#1a3a5a"/><rect x="{k*108+16}" y="640" width="70" height="8" fill="#1a3a5a"/><circle cx="{k*108+80}" cy="900" r="8" fill="#c9ccd4"/>' for k in range(10)) + bench(540, 1560, 600) + floor("tile", 1380, "#9aa4b2"), 1380
def _p_stage(t):    return curtain(0, 1080, 0, 1300, "#6a0e1e") + f'<polygon points="440,0 640,0 900,1400 180,1400" fill="#fff3d0" opacity=".12"/>' + f'<path d="M0,0 Q540,200 1080,0 L1080,140 Q540,320 0,140 Z" fill="#8a1e2e"/>' + floor("wood", 1300, "#5a3a22"), 1300
def _p_studio(t):   return wall("#111", "#1a1a22") + f'<rect x="140" y="260" width="800" height="440" fill="#13284d"/>' + neon(540, 520, "الأخبار", "#7cc6ff", 100) + f'<rect x="200" y="1100" width="680" height="200" rx="20" fill="#2a2e3a" stroke="#7cc6ff" stroke-width="4"/>' + "".join(f'<rect x="{x}" y="{y}" width="60" height="40" fill="#333"/><polygon points="{x+60},{y} {x+200},{y-60} {x+200},{y+100} {x+60},{y+40}" fill="#fff3d0" opacity=".06"/>' for x, y in ((40, 120), (980, 120))) + floor("plain", 1380, "#1a1a22"), 1380
def _p_lab(t):      return wall("#e8eef0", "#d8e2e6") + wpattern("tiles") + counter_(0, 1080, 1160, "#cfd8e2", "#3a3e44") + "".join(f'<path d="M{x},1140 l-30,0 l20,-80 l0,-60 l20,0 l0,60 l20,80 Z" fill="{c}" opacity=".8" stroke="#555" stroke-width="3"/>' for x, c in ((160, "#3ddc84"), (300, "#7cc6ff"), (780, "#ff7aa2"), (900, "#ffd21f"))) + f'<rect x="420" y="300" width="300" height="400" fill="#9aa4b2" stroke="#555" stroke-width="6"/><rect x="440" y="320" width="260" height="200" fill="#bfe3ff" opacity=".5"/>' + floor("tile", 1380, "#c8d0d4"), 1380
def _p_servers(t):  return wall("#0a0e14", "#121822") + "".join(f'<rect x="{40+k*210}" y="300" width="180" height="1080" fill="#1a1e26" stroke="#2a2e36" stroke-width="5"/>' + "".join(f'<rect x="{60+k*210}" y="{340+j*60}" width="140" height="40" fill="#22262e"/><circle cx="{80+k*210}" cy="{360+j*60}" r="5" fill="{["#3ddc84","#7cc6ff","#ff3b3b"][(j+k)%3]}"/>' for j in range(17)) for k in range(5)) + floor("metal", 1380), 1380
def _p_office_open(t): return wall("#d8dce2", "#e8ecf0") + window2(80, 200, 920, 480, "city" if t != "day" else "day", "#5a6a7a") + "".join(f'<rect x="{k*360}" y="1000" width="340" height="30" fill="#8a9aa8"/><rect x="{k*360+120}" y="860" width="140" height="110" rx="6" fill="#111"/><rect x="{k*360+184}" y="970" width="12" height="30" fill="#333"/><rect x="{k*360}" y="1030" width="340" height="340" fill="#6a7a88" opacity=".6"/>' for k in range(3)) + floor("carpet", 1380, "#3a4a5a"), 1380
def _p_bedroom(t):  return wall("#3a3a5a", "#2a2a44") + wpattern("wallpaper") + window2(120, 320, 280, 380, "night" if t != "day" else "day", "#e8e2d8") + f'<rect x="600" y="1180" width="460" height="120" rx="14" fill="#f2f2f2"/><rect x="600" y="1000" width="40" height="380" fill="#5a3a26"/><rect x="660" y="1150" width="400" height="110" rx="16" fill="#7a2f4a"/><rect x="420" y="760" width="140" height="620" fill="#6a4a32" stroke="#3a2a1a" stroke-width="5"/>' + floor("wood", 1380), 1380
def _p_souq(t):     return sky(t, 600, False) + "".join(f'<path d="M{x},600 L{x+340},600 L{x+320},700 L{x+20},700 Z" fill="{c}"/>' + f'<rect x="{x+20}" y="700" width="300" height="680" fill="#3a2a1e"/><rect x="{x+40}" y="1000" width="260" height="200" fill="{c2}"/>' for x, c, c2 in ((0, "#c4262e", "#e8b33a"), (360, "#2f6bd8", "#3a8a4a"), (720, "#e8b33a", "#c4262e"))) + "".join(f'<path d="M{x},560 v60" stroke="#333" stroke-width="3"/><rect x="{x-18}" y="620" width="36" height="50" rx="8" fill="#ffd27a"/>' for x in (180, 540, 900)) + sign(540, 480, "سوق الذهب القديم", "#5a2a14", "#e8c34a", size=50) + floor("stone_floor" if False else "plain", 1380, "#8a7a62"), 1380
def _p_majlis(t):   return wall("#e8dcc0", "#d8c8a8") + wpattern("panels") + f'<rect x="0" y="1180" width="1080" height="200" fill="#8a1e2e"/>' + "".join(f'<rect x="{k*180+10}" y="1080" width="160" height="110" rx="20" fill="#a0283a" stroke="#5a0e1a" stroke-width="4"/>' for k in range(6)) + f'<g transform="translate(540 1560)"><path d="M-30,0 q-10,-80 30,-110 q40,30 30,110 Z" fill="#c9a24a" stroke="#8a6a2a" stroke-width="4"/><path d="M30,-70 q50,-20 50,30" stroke="#c9a24a" stroke-width="8" fill="none"/></g>' + floor("carpet", 1380, "#6a1a24"), 1380
def _p_tent(t):     return f'<rect width="1080" height="1400" fill="#3a1e14"/>' + "".join(f'<path d="M{k*135},0 L540,-200 L{(k+1)*135},0 L{(k+1)*135},1400 L{k*135},1400 Z" fill="{["#7a2a1e","#e8d8b0"][k%2]}" opacity=".9"/>' for k in range(8)) + f'<path d="M540,0 V200" stroke="#222" stroke-width="4"/><rect x="510" y="200" width="60" height="80" rx="10" fill="#ffd27a"/>' + floor("carpet", 1380, "#7a1e1e") + "".join(f'<path d="M{k*120},1460 l60,-40 l60,40 l-60,40 Z" fill="#e8c34a" opacity=".5"/>' for k in range(9)), 1380
def _p_cinema(t):   return wall("#0a0a0e", "#14141a") + f'<rect x="60" y="120" width="960" height="560" fill="#cfe0f0" opacity=".85"/><polygon points="540,1920 60,680 1020,680" fill="#cfe0f0" opacity=".05"/>' + "".join(f'<rect x="{k*110}" y="{1150+r*120}" width="100" height="110" rx="14" fill="#6a0e1e" stroke="#3a0610" stroke-width="4"/>' for r in range(2) for k in range(10)) + floor("carpet", 1380, "#2a0a10"), 1380
def _p_cell(t):     return wall("#5a5e5a", "#3a3e3a") + wpattern("stone") + window2(700, 240, 200, 140, "night" if t != "day" else "day", "#333", bars=True) + f'<rect x="560" y="1180" width="480" height="40" fill="#6a6e6a"/><rect x="560" y="1140" width="480" height="50" fill="#9a9a8a"/>' + "".join(f'<rect x="{x}" y="0" width="22" height="1920" fill="#2a2a2a"/>' for x in range(30, 1080, 150)) + floor("concrete", 1380, "#4a4e4a"), 1380
def _p_mall(t):     return wall("#e8e2d8", "#d8d0c4") + "".join(f'<rect x="{k*360+20}" y="420" width="320" height="560" fill="#9fc6e8" opacity=".5" stroke="#8592a8" stroke-width="6"/>' + sign(k * 360 + 180, 380, n, c, size=40) for k, (n, c) in enumerate((("ملابس", "#c4262e"), ("ألعاب", "#2f6bd8"), ("عطور", "#7a2f5a")))) + f'<path d="M0,1380 L360,1000 L460,1000 L100,1380 Z" fill="#9aa4b2"/>' + floor("marble", 1380, "#e0d8cc"), 1380
def _p_construction(t): return sky(t, 1300) + "".join(f'<rect x="{x}" y="500" width="14" height="880" fill="#c9a21a"/>' for x in (100, 300, 500)) + "".join(f'<rect x="100" y="{y}" width="414" height="14" fill="#c9a21a"/>' for y in (600, 800, 1000, 1200)) + f'<rect x="760" y="100" width="24" height="1280" fill="#e8b31a"/><rect x="560" y="100" width="500" height="24" fill="#e8b31a"/><path d="M1000,124 V500" stroke="#333" stroke-width="4"/>' + floor("plain", 1380, "#8a7a62") + "".join(f'<path d="M{x},1560 l30,-90 l30,90 Z" fill="#ff8a1a"/><rect x="{x+10}" y="1510" width="40" height="12" fill="#fff"/>' for x in (600, 900)), 1380
def _p_subway(t):   return wall("#cfd8e2", "#b8c2cc") + "".join(window2(40 + k * 360, 340, 300, 240, "dark", "#9aa4b2") for k in range(3)) + "".join(sign(190 + k * 360, 260, a, "#ffd21f", "#111", size=34) for k, a in enumerate(("إعلان", "خصم 50%", "المحطة"))) + "".join(f'<rect x="{k*360}" y="1000" width="340" height="200" rx="20" fill="#c4262e"/>' for k in range(3)) + "".join(f'<rect x="{x}" y="0" width="18" height="1380" fill="#c9ccd4"/>' for x in (340, 700)) + floor("metal", 1380), 1380
def _p_snow_cabin(t): return sky(t, 1300) + "".join(tree(x, 1340, s, True, "#1f3a2a") for x, s in ((80, 1.0), (980, 1.2), (260, .7))) + f'<rect x="480" y="900" width="440" height="440" fill="#6a4a2e"/>' + wpattern("logs").replace('width="1080"', 'width="0"') + f'<path d="M440,900 L700,700 L960,900 Z" fill="#e8f0f8" stroke="#9fb3c6" stroke-width="5"/><rect x="560" y="1020" width="120" height="120" fill="#ffd27a"/><rect x="760" y="1060" width="110" height="280" fill="#3a2a1a"/>' + floor("snow", 1340), 1340
def _p_lighthouse(t): return sky(t, 1100) + f'<rect y="1100" width="1080" height="300" fill="#0e2a44"/><path d="M500,1380 L560,500 L700,500 L760,1380 Z" fill="#e8e8e8"/>' + "".join(f'<path d="M{510+k*12},{1300-k*200} L{750-k*12},{1300-k*200} L{745-k*12},{1220-k*200} L{515+k*12},{1220-k*200} Z" fill="#c4262e"/>' for k in range(4)) + f'<rect x="580" y="420" width="100" height="80" fill="#ffe8a8"/><polygon points="630,460 1080,300 1080,620" fill="#fff3b0" opacity=".2"/>' + f'<path d="M0,1380 Q200,1280 420,1340 Q600,1300 1080,1380 L1080,1400 L0,1400 Z" fill="#3a3e44"/>' + floor("plain", 1380, "#3a3e44"), 1380
def _p_palace(t):   return wall("#e8d8b8", "#d8c4a0") + "".join(pillar(x, 1380, "#f0e4c8") for x in (90, 370, 710, 990)) + "".join(f'<g transform="translate({x} 40)"><path d="M-100,0 h200 l-40,70 h-120 Z" fill="#c9a24a"/>' + "".join(f'<circle cx="{-80+k*40}" cy="86" r="11" fill="#ffe8a8"/>' for k in range(5)) + '</g>' for x in (230, 850)) + floor("marble", 1380, "#e8dcc8") + '<path d="M440,1380 L640,1380 L760,1920 L320,1920 Z" fill="#8a1e2e"/>', 1380
def _p_living(t):
    import props
    return wall("#0c1628", "#1a2a44") + window2(640, 300, 320, 420, "night" if t != "day" else "day") + floor("wood", 1380) + props.sofa(880, 1400) + props.rug(540, 1610) + props.painting(260, 620), 1380

PLACES = {
    # outdoor
    "street": ("شارع ليلي في المدينة", _p_street, True), "alley": ("زقاق ضيق", _p_alley, True), "park": ("حديقة عامة", _p_park, True),
    "beach": ("شاطئ", _p_beach, True), "desert_camp": ("مخيم في الصحراء", _p_desert_camp, True), "rooftop": ("سطح مبنى", _p_rooftop, True),
    "gas_station": ("محطة وقود", _p_gas, True), "ship_deck": ("سطح سفينة", _p_ship_deck, True), "construction": ("موقع بناء", _p_construction, True),
    "snow_cabin": ("كوخ في الثلج", _p_snow_cabin, True), "lighthouse": ("منارة على البحر", _p_lighthouse, True), "souq": ("سوق شعبي", _p_souq, True),
    # transport
    "parking": ("موقف سيارات تحت الأرض", _p_parking, False), "platform": ("رصيف قطار", _p_platform, False), "train_cabin": ("مقصورة قطار", _p_train_cabin, False),
    "airport_gate": ("بوابة مطار", _p_airport, False), "subway": ("عربة مترو", _p_subway, False), "elevator": ("مصعد", _p_elevator, False),
    # public
    "hospital_room": ("غرفة مستشفى", _p_hospital, False), "police_station": ("قسم شرطة", _p_police, False), "interrogation": ("غرفة استجواب", _p_interrog, False),
    "courtroom": ("قاعة محكمة", _p_court, False), "classroom": ("فصل دراسي", _p_classroom, False), "library": ("مكتبة", _p_library, False),
    "museum": ("متحف", _p_museum, False), "bank": ("بنك", _p_bank, False), "jewelry_store": ("محل مجوهرات", _p_jewelry, False),
    "restaurant": ("مطعم", _p_restaurant, False), "cafe": ("مقهى", _p_cafe, False), "supermarket": ("سوبرماركت", _p_market, False),
    "mall": ("مركز تسوق", _p_mall, False), "cinema": ("قاعة سينما", _p_cinema, False), "theatre_stage": ("خشبة مسرح", _p_stage, False),
    "tv_studio": ("استوديو أخبار", _p_studio, False), "gym": ("نادي رياضي", _p_gym, False), "locker_room": ("غرفة خزائن", _p_lockers, False),
    # work
    "garage": ("ورشة سيارات", _p_garage, False), "barn": ("حظيرة مزرعة", _p_barn, False), "lab": ("مختبر", _p_lab, False),
    "server_room": ("غرفة خوادم", _p_servers, False), "open_office": ("مكتب مفتوح", _p_office_open, False), "hotel_lobby": ("بهو فندق", _p_lobby, False),
    "corridor": ("ممر فندق", _p_corridor, False), "ship_cabin": ("قمرة سفينة", _p_ship_cabin, False), "prison_cell": ("زنزانة", _p_cell, False),
    # homes
    "bedroom": ("غرفة نوم", _p_bedroom, False), "forest_cabin": ("كوخ خشبي", _p_cabin, False), "majlis": ("مجلس عربي", _p_majlis, False),
    "bedouin_tent": ("خيمة بدوية", _p_tent, False), "palace_hall": ("قاعة قصر", _p_palace, False), "living_room": ("صالة بيت", _p_living, False),
}

def place(name, time="night", weather=None):
    label, fn, outdoor = PLACES[name]
    svg, fy = fn(time)
    if weather == "rain" and outdoor: svg += rain_overlay()
    if weather == "snow" and outdoor: svg += snow_overlay()
    if '<rect id="flash"' not in svg: svg += '<rect id="flash" width="1080" height="1920" fill="#dbeaff" opacity="0"/>'
    if 'id="lamp"' not in svg: svg += '<rect id="lamp" width="1080" height="1920" fill="none"/>'
    return svg, fy
