"""saw_5tory prop library: every object of a case scene, drawn in code (SVG).
Each function returns an SVG string. Coordinates are in the 1080x1920 frame.
Anchor = the point you pass as x,y (noted per prop). Colours follow the series palette.
Use ONLY these props (or extend this file in the same style); never generated images."""
import math

INK = "#05070d"; LINE = "#2a1a12"; BLUE = "#7cc6ff"; RED = "#ff3b3b"; GOLD = "#ffd21f"

def _t(x, y, size, text, fill="#111", anchor="middle", weight=900, rtl=True):
    d = ' direction="rtl"' if rtl else ''
    return f'<text x="{x}" y="{y}" font-family="Cairo" font-weight="{weight}" font-size="{size}" fill="{fill}" text-anchor="{anchor}"{d}>{text}</text>'

# ---------------------------------------------------------------- room shell
def room_shell(wall="#0c1628", wall2="#1a2a44", floor_y=1380):
    return f'''<defs><linearGradient id="wallg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{wall}"/><stop offset="1" stop-color="{wall2}"/></linearGradient>
<linearGradient id="floorg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2b1e17"/><stop offset="1" stop-color="#120c09"/></linearGradient>
<radialGradient id="lampg" cx="20%" cy="55%" r="45%"><stop offset="0" stop-color="#ffb35c" stop-opacity=".35"/><stop offset="1" stop-color="#ffb35c" stop-opacity="0"/></radialGradient></defs>
<rect width="1080" height="1920" fill="url(#wallg)"/><rect y="{floor_y}" width="1080" height="{1920-floor_y}" fill="url(#floorg)"/>
<g stroke="#000" stroke-opacity=".35" stroke-width="3"><path d="M0,{floor_y+80}H1080M0,{floor_y+180}H1080M0,{floor_y+300}H1080M0,{floor_y+440}H1080"/><path d="M200,{floor_y}v80M640,{floor_y+80}v100M380,{floor_y+180}v120M820,{floor_y+300}v140"/></g>
<rect id="lamp" width="1080" height="1920" fill="url(#lampg)"/>'''

def shade():  # last layer of the room: mood darkening
    return '<rect width="1080" height="1920" fill="#000" opacity=".18"/>'

# ---------------------------------------------------------------- wall items
def window(x=640, y=300, rain=True, broken=False, day=False, w=320, h=520):
    """anchor: top-left of the glass. rain -> animated rain (#rain); day -> daylight sky; broken -> crack + hole."""
    sky = "#9fd3ff" if day else "#0b2042"
    out = f'<rect x="{x-14}" y="{y-14}" width="{w+28}" height="{h+28}" fill="#070b14" rx="6"/><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{sky}"/>'
    if day:
        out += f'<circle cx="{x+w*0.7}" cy="{y+h*0.25}" r="44" fill="#fff3b0"/>'
    if rain and not day:
        streaks = "".join(f'<path d="M{x+(i*53)%w},{(i*137)%(2*h)} l-14,70"/>' for i in range(80))
        out += f'<clipPath id="winclip"><rect x="{x}" y="{y}" width="{w}" height="{h}"/></clipPath><g clip-path="url(#winclip)"><g transform="translate(0 {y-h})"><g id="rain" stroke="#9fd0ff" stroke-width="3" opacity=".7">{streaks}</g></g></g>'
    if broken:
        cx, cy = x + w*0.35, y + h*0.62
        out += f'<path d="M{cx},{cy} l60,-120 M{cx},{cy} l-80,-60 M{cx},{cy} l90,70 M{cx},{cy} l-40,110 M{cx},{cy} l110,-20" stroke="#dfeaff" stroke-width="3"/><path d="M{cx-34},{cy-20} l40,-26 l34,30 l-18,40 l-44,-6 Z" fill="#02040a"/>'
    out += f'<rect id="flash" x="{x}" y="{y}" width="{w}" height="{h}" fill="#dbeaff" opacity="0"/>'
    out += f'<path d="M{x+w/2},{y}V{y+h}M{x},{y+h/2}H{x+w}" stroke="#070b14" stroke-width="14"/><rect x="{x-30}" y="{y+h+10}" width="{w+60}" height="22" fill="#070b14"/>'
    return out

def clock(x=300, y=430, time="11:40"):
    """anchor: centre. analog wall clock."""
    hh, mm = [int(v) for v in time.split(":")]
    ha = (hh % 12) * 30 + mm * 0.5; ma = mm * 6
    ticks = "".join(f'<path d="M0,-58 v10" transform="rotate({k*30})"/>' for k in range(12))
    return (f'<g transform="translate({x} {y})"><circle r="78" fill="#0a0f1a" stroke="#5a6b8a" stroke-width="8"/><circle r="66" fill="#d9e2ee"/>'
            f'<g stroke="#0a0f1a" stroke-width="5">{ticks}</g><path d="M0,0 L0,-34" stroke="#0a0f1a" stroke-width="8" stroke-linecap="round" transform="rotate({ha})"/>'
            f'<path d="M0,0 L0,-54" stroke="#0a0f1a" stroke-width="5" stroke-linecap="round" transform="rotate({ma})"/><circle r="6" fill="#c23"/></g>')

def digital_clock(x=760, y=1210, text="12:00", blink=True):
    """anchor: centre. Blinking 12:00 = power came back after a cut (id dclock_text blinks)."""
    i = ' id="dclock"' if blink else ''
    return (f'<g transform="translate({x} {y})"><rect x="-90" y="-40" width="180" height="80" rx="12" fill="#050608" stroke="#3a4560" stroke-width="4"/>'
            f'<g{i}>{_t(0, 22, 56, text, "#ff3b3b", rtl=False)}</g></g>')

def calendar(x=880, y=420, month="مارس", day="14"):
    """anchor: centre. wall calendar showing a day."""
    return (f'<g transform="translate({x} {y})"><rect x="-80" y="-90" width="160" height="180" rx="10" fill="#f2f4f8" stroke="#0a0f1a" stroke-width="4"/>'
            f'<rect x="-80" y="-90" width="160" height="50" rx="10" fill="#c23"/>{_t(0,-54,34,month,"#fff")}{_t(0,60,90,day,"#111",rtl=False)}</g>')

def photo_frame(x=860, y=520, shadow="long"):
    """anchor: centre. A framed photo: a person, the sun high (short shadow) or low (long shadow)."""
    sun_y = -60 if shadow == "short" else 20
    sh = '<ellipse cx="18" cy="70" rx="22" ry="6" fill="#000" opacity=".5"/>' if shadow == "short" else '<path d="M8,70 L120,78 L118,86 L6,76 Z" fill="#000" opacity=".5"/>'
    return (f'<g transform="translate({x} {y})"><rect x="-110" y="-90" width="220" height="180" fill="#5a3a22" stroke="#2a1a12" stroke-width="5"/>'
            f'<rect x="-96" y="-76" width="192" height="152" fill="#bfe3ff"/><rect x="-96" y="40" width="192" height="36" fill="#d8c08a"/>'
            f'<circle cx="-50" cy="{sun_y}" r="16" fill="#ffd21f"/>{sh}<path d="M0,70 L0,30 M-10,50 L10,50 M0,30 L-8,70 M0,30 L8,70" stroke="#222" stroke-width="5"/><circle cx="0" cy="20" r="9" fill="#222"/></g>')

def door(x=40, y=700, chain=False, open_=False):
    """anchor: top-left. chain=True draws a door chain hooked from inside."""
    out = (f'<rect x="{x}" y="{y}" width="300" height="690" fill="#0a0e18" stroke="#2f4470" stroke-width="5"/>'
           f'<path d="M{x+20},{y+20} L{x+260},{y+40} L{x+260},{y+670} L{x+20},{y+680} Z" fill="#141c2e"/><circle cx="{x+230}" cy="{y+360}" r="10" fill="#c9a24a"/>')
    if chain:
        out += f'<path d="M{x+250},{y+300} q30,22 60,4" stroke="#c9ccd4" stroke-width="7" fill="none" stroke-dasharray="10 5"/><rect x="{x+300}" y="{y+288}" width="16" height="30" fill="#c9a24a"/>'
    return out

def doormat(x=205, y=1468, wet=False, mud=False):
    """anchor: centre."""
    fill = "#3b2a22" if wet else "#5a3a2a"
    out = f'<rect x="{x-135}" y="{y-28}" width="270" height="56" rx="8" fill="{fill}" stroke="#2a1a12" stroke-width="4"/>'
    if wet: out += f'<ellipse cx="{x}" cy="{y+40}" rx="150" ry="14" fill="#7cc6ff" opacity=".35"/>'
    if mud: out += "".join(f'<ellipse cx="{x-80+i*40}" cy="{y-6+(i%2)*14}" rx="16" ry="9" fill="#4a3018"/>' for i in range(5))
    return out

# ---------------------------------------------------------------- floor / furniture
def table(x=820, y=1300, w=300):
    """anchor: top-centre of the table top. put small props on y-? (top surface = y)."""
    return (f'<rect x="{x-w/2}" y="{y}" width="{w}" height="24" rx="4" fill="#5a3a26" stroke="#2a1a12" stroke-width="3"/>'
            f'<rect x="{x-w/2+16}" y="{y+24}" width="18" height="200" fill="#4a2f1f"/><rect x="{x+w/2-34}" y="{y+24}" width="18" height="200" fill="#4a2f1f"/>')

def chair_over(x=780, y=1560, padded=False):
    cushion = ('<rect x="-85" y="-126" width="160" height="59" rx="9" fill="#703949" stroke="#bd9170" stroke-width="5"/>'
               '<path d="M-76 -13H79" stroke="#bb956e" stroke-width="9" stroke-linecap="round"/>') if padded else ''
    return (f'<g transform="translate({x} {y}) rotate(-78)"><rect x="-90" y="-10" width="180" height="22" fill="#4a3022" stroke="#1a0f0a" stroke-width="3"/><rect x="-80" y="-170" width="18" height="160" fill="#4a3022"/>'
            f'<rect x="62" y="-170" width="18" height="160" fill="#4a3022"/><rect x="-80" y="12" width="16" height="140" fill="#3a251a"/><rect x="64" y="12" width="16" height="140" fill="#3a251a"/>{cushion}</g>')

def outline(x=700, y=1610, name=""):
    """chalk outline on the floor (no body is ever shown). anchor: centre. name -> hidden tag id tag_outline."""
    out = (f'<g transform="translate({x-700} {y-1610})"><g fill="none" stroke="#e8eef6" stroke-width="6" stroke-dasharray="14 10" opacity=".75">'
           '<path d="M640,1620 q30,-40 80,-30 l120,-10 q40,-4 60,20 l60,10 l-6,26 l-70,-6 q-30,30 -80,26 l-90,0 l-60,40 l-16,-22 l40,-34 q-36,-6 -38,-20 Z"/><circle cx="612" cy="1612" r="34"/></g></g>')
    if name: out += tag("outline", x + 120, y - 110, name)
    return out

def umbrella(x=372, y=1170, wet=False):
    """anchor: handle top. closed umbrella leaning on a wall. wet -> drops + puddle."""
    out = (f'<g transform="translate({x} {y}) rotate(6)"><path d="M0,0 L0,330" stroke="#c9a24a" stroke-width="8"/><path d="M0,30 Q30,170 8,320 L-8,320 Q-30,170 0,30 Z" fill="#0b0f1a" stroke="#2f4470" stroke-width="3"/>'
           f'<path d="M0,0 q-24,-6 -26,-30" stroke="#c9a24a" stroke-width="10" fill="none" stroke-linecap="round"/><path d="M-4,60 L4,300" stroke="#2f4470" stroke-width="2"/>')
    if wet: out += '<g fill="#9fd0ff"><circle cx="12" cy="120" r="5"/><circle cx="-10" cy="200" r="5"/><circle cx="8" cy="260" r="6"/></g><ellipse cx="10" cy="338" rx="70" ry="12" fill="#7cc6ff" opacity=".45"/>'
    return out + '</g>'

def cup_broken(x=560, y=1690):
    return f'<ellipse cx="{x}" cy="{y+10}" rx="90" ry="22" fill="#3a2214" opacity=".9"/><path d="M{x-40},{y} l30,-30 l20,24 Z" fill="#e8eef6"/><path d="M{x+30},{y+10} l24,-14 l8,18 Z" fill="#e8eef6"/>'

def cup(x=820, y=1300, steam=False, lipstick=False, skin=False, empty=False):
    """anchor: bottom-centre (sits on a table top y). steam -> animated wisps id steam."""
    out = f'<path d="M{x-34},{y-80} L{x+34},{y-80} L{x+28},{y} L{x-28},{y} Z" fill="#eef2f7" stroke="#8592a8" stroke-width="3"/><path d="M{x+34},{y-64} q26,0 24,26 q-2,22 -28,20" stroke="#eef2f7" stroke-width="8" fill="none"/>'
    if not empty: out += f'<ellipse cx="{x}" cy="{y-80}" rx="32" ry="8" fill="{"#c8b49a" if skin else "#4a2a16"}"/>'
    if lipstick: out += f'<path d="M{x-24},{y-82} q8,6 16,0" stroke="#d61f4a" stroke-width="7" stroke-linecap="round"/>'
    if steam: out += f'<g id="steam" stroke="#e8eef6" stroke-width="5" fill="none" opacity=".7" stroke-linecap="round"><path d="M{x-10},{y-96} q-14,-24 0,-48 q14,-24 0,-48"/><path d="M{x+12},{y-96} q-14,-24 0,-48 q14,-24 0,-48"/></g>'
    return out

def ice_glass(x=760, y=1300, ice=True):
    """anchor: bottom-centre. ice -> big unmelted cubes; else plain water."""
    out = f'<path d="M{x-40},{y-130} L{x+40},{y-130} L{x+32},{y} L{x-32},{y} Z" fill="#bfe3ff" fill-opacity=".35" stroke="#dfeaff" stroke-width="4"/><rect x="{x-34}" y="{y-95}" width="68" height="92" fill="#7cc6ff" opacity=".25"/>'
    if ice: out += f'<g fill="#f4fbff" stroke="#9fd0ff" stroke-width="3"><rect x="{x-28}" y="{y-110}" width="30" height="30" rx="4" transform="rotate(-10 {x-13} {y-95})"/><rect x="{x+2}" y="{y-96}" width="28" height="28" rx="4" transform="rotate(12 {x+16} {y-82})"/><rect x="{x-20}" y="{y-66}" width="28" height="28" rx="4"/></g>'
    return out

def candle(x=700, y=1300, height=0.9, lit=True, smoke=False):
    """anchor: bottom-centre on a table. height 0..1 (1 = new). smoke -> just blown out (id smoke)."""
    h = 40 + 150 * height
    out = f'<ellipse cx="{x}" cy="{y-4}" rx="46" ry="12" fill="#c9a24a"/><rect x="{x-18}" y="{y-h}" width="36" height="{h}" fill="#f4ecd8" stroke="#c9b48a" stroke-width="2"/><path d="M{x},{y-h} v-14" stroke="#222" stroke-width="3"/>'
    if lit: out += f'<path id="flame" d="M{x},{y-h-50} q14,22 0,36 q-14,-14 0,-36 Z" fill="#ffd27a"/>'
    if smoke: out += f'<g id="smoke" stroke="#9aa6b8" stroke-width="5" fill="none" opacity=".75" stroke-linecap="round"><path d="M{x},{y-h-16} q-16,-30 0,-60 q16,-30 0,-60"/></g>'
    return out

def phone(x=900, y=1290, battery=95, screen="", lit=True):
    """anchor: bottom-centre, lying-up phone seen from the front. screen: short text (Arabic or time)."""
    scr = "#0e2a55" if lit else "#050608"
    out = f'<rect x="{x-50}" y="{y-180}" width="100" height="180" rx="16" fill="#111" stroke="#3a4560" stroke-width="4"/><rect x="{x-42}" y="{y-168}" width="84" height="156" rx="8" fill="{scr}"/>'
    if lit:
        bw = 30 * battery / 100; col = "#3ddc84" if battery > 20 else "#ff3b3b"
        out += f'<rect x="{x+4}" y="{y-160}" width="32" height="14" rx="3" fill="none" stroke="#dfeaff" stroke-width="2"/><rect x="{x+5}" y="{y-159}" width="{bw:.0f}" height="12" fill="{col}"/>' + _t(x-14, y-148, 14, f"{battery}%", "#dfeaff", rtl=False)
        if screen: out += _t(x, y-80, 26, screen, "#fff")
    return out

def paper(x=540, y=1300, kind="ticket", title="", lines=(), rot=-6):
    """anchor: centre. kind: ticket | receipt | newspaper | note. lines: up to 3 short strings (dates/times in Western digits)."""
    w, h = {"ticket": (300, 150), "receipt": (180, 260), "newspaper": (320, 240), "note": (240, 180)}[kind]
    out = f'<g transform="translate({x} {y}) rotate({rot})"><rect x="{-w/2}" y="{-h/2}" width="{w}" height="{h}" fill="#f4efe2" stroke="#8a7a5a" stroke-width="3"/>'
    if kind == "ticket": out += f'<path d="M{w/2-70},{-h/2} V{h/2}" stroke="#8a7a5a" stroke-width="3" stroke-dasharray="8 6"/>'
    if kind == "newspaper": out += "".join(f'<rect x="{-w/2+20}" y="{-h/2+80+i*30}" width="{w-40}" height="10" fill="#c9c2b0"/>' for i in range(4))
    if title: out += _t(0, -h/2 + 46, 34, title, "#111")
    for i, ln in enumerate(lines[:3]): out += _t(0, -h/2 + 92 + i*40 + (60 if kind == "newspaper" else 0), 30, ln, "#222")
    return out + '</g>'

def plant(x=960, y=1380, wet=False, wilted=False):
    """anchor: bottom-centre of the pot. wet -> dark wet soil + drops (watered recently)."""
    soil = "#2a1a10" if wet else "#8a6a48"
    leaves = "#3f8a4a" if not wilted else "#8a8a4a"
    lv = "".join(f'<path d="M{x},{y-150} q{a},{-80 if not wilted else 10} {a*1.6},{-40 if not wilted else 60}" stroke="{leaves}" stroke-width="18" fill="none" stroke-linecap="round"/>' for a in (-60, -25, 25, 60))
    out = lv + f'<path d="M{x-60},{y-150} L{x+60},{y-150} L{x+46},{y} L{x-46},{y} Z" fill="#b5543a" stroke="#5a2a1a" stroke-width="4"/><ellipse cx="{x}" cy="{y-150}" rx="58" ry="12" fill="{soil}"/>'
    if wet: out += f'<g fill="#9fd0ff"><circle cx="{x-20}" cy="{y-150}" r="4"/><circle cx="{x+16}" cy="{y-148}" r="4"/></g><ellipse cx="{x}" cy="{y+6}" rx="60" ry="8" fill="#7cc6ff" opacity=".35"/>'
    if not wet: out += f'<path d="M{x-30},{y-152} l14,6 l10,-6 M{x+10},{y-150} l12,5" stroke="#5a4028" stroke-width="2"/>'
    return out

def dusty_box(x=820, y=1500, handprint=True):
    """anchor: bottom-centre. dusty box; handprint -> a clean hand shape on the dusty lid (it was touched)."""
    out = f'<rect x="{x-110}" y="{y-150}" width="220" height="150" fill="#6b5236" stroke="#2a1a12" stroke-width="4"/><path d="M{x-110},{y-150} L{x-80},{y-190} L{x+140},{y-190} L{x+110},{y-150} Z" fill="#8a8476"/>'
    out += "".join(f'<circle cx="{x-90+(i*37)%210}" cy="{y-186+(i*13)%34}" r="2.5" fill="#b8b2a2"/>' for i in range(40))
    if handprint: out += f'<g fill="#6b5236"><ellipse cx="{x+20}" cy="{y-168}" rx="20" ry="12"/><path d="M{x+4},{y-176} l-10,-12 M{x+14},{y-180} l-4,-14 M{x+26},{y-180} l2,-14 M{x+36},{y-176} l8,-12" stroke="#6b5236" stroke-width="7" stroke-linecap="round"/></g>'
    return out

def shoes(x=200, y=1530, mud=False, wet=False):
    """anchor: centre between the two shoes (on the floor)."""
    col = "#3a2414" if mud else "#0a0a0d"
    out = f'<path d="M{x-80},{y} L{x-20},{y} L{x-14},{y+26} L{x-86},{y+26} Z" fill="{col}" stroke="#2f4470" stroke-width="2"/><path d="M{x+10},{y} L{x+70},{y} L{x+76},{y+26} L{x+4},{y+26} Z" fill="{col}" stroke="#2f4470" stroke-width="2"/>'
    if mud: out += "".join(f'<circle cx="{x-60+i*24}" cy="{y+30}" r="7" fill="#5a3a1a"/>' for i in range(6))
    if wet: out += f'<ellipse cx="{x}" cy="{y+32}" rx="100" ry="10" fill="#7cc6ff" opacity=".4"/>'
    return out

def footprints(x1=300, y1=1700, x2=640, y2=1460, kind="wet", n=6):
    """a trail of prints from (x1,y1) to (x2,y2). kind: wet | mud | sand."""
    col = {"wet": "#7cc6ff", "mud": "#4a3018", "sand": "#c9a46a"}[kind]
    out = ""
    for i in range(n):
        t = i / (n - 1); px = x1 + (x2 - x1) * t + (14 if i % 2 else -14); py = y1 + (y2 - y1) * t
        ang = math.degrees(math.atan2(y2 - y1, x2 - x1)) + 90
        out += f'<ellipse cx="{px:.0f}" cy="{py:.0f}" rx="13" ry="24" fill="{col}" opacity=".7" transform="rotate({ang:.0f} {px:.0f} {py:.0f})"/>'
    return out

def glass_shards(x=540, y=1500, n=9):
    return "".join(f'<path d="M{x-120+(i*53)%240},{y-10+(i*29)%40} l{12+(i%3)*6},-{10+(i%4)*6} l{8+(i%2)*6},{14+(i%3)*4} Z" fill="#dfeaff" opacity=".85"/>' for i in range(n))

def book(x=540, y=1300, page="3"):
    """anchor: bottom-centre, open book with a bookmark and the page number."""
    return (f'<path d="M{x-120},{y-20} Q{x-60},{y-60} {x},{y-30} Q{x+60},{y-60} {x+120},{y-20} L{x+120},{y} Q{x+60},{y-30} {x},{y} Q{x-60},{y-30} {x-120},{y} Z" fill="#f4efe2" stroke="#8a7a5a" stroke-width="3"/>'
            f'<path d="M{x+60},{y-46} v60" stroke="#c23" stroke-width="10"/>' + _t(x+60, y-8, 22, page, "#222", rtl=False))

def dog(x=860, y=1640, asleep=True):
    """anchor: bottom-centre. a sleeping guard dog (zzz)."""
    out = (f'<ellipse cx="{x}" cy="{y-40}" rx="110" ry="46" fill="#7a5a3a" stroke="#2a1a12" stroke-width="4"/><circle cx="{x-100}" cy="{y-70}" r="40" fill="#7a5a3a" stroke="#2a1a12" stroke-width="4"/>'
           f'<path d="M{x-126},{y-100} l-20,-30 l30,10 Z" fill="#5a3e26"/><path d="M{x-112},{y-72} q10,6 20,0" stroke="#2a1a12" stroke-width="4" fill="none"/>')
    if asleep: out += _t(x-40, y-130, 40, "z z", "#dfeaff", rtl=False)
    return out

def tag(id_, x, y, name):
    """yellow name tag (hidden; the builder shows it with "tags":[id])."""
    w = 60 + 34 * len(name)
    return f'<g id="tag_{id_}" opacity="0"><rect x="{x-w/2}" y="{y-34}" width="{w}" height="64" rx="32" fill="{GOLD}"/>' + _t(x, y + 11, 40, name) + '</g>'

# ---------------------------------------------------------------- people
def person(id_="p1", x=490, y=1520, name="", coat="#6b4a32", hair="#14121a", skin="#f0c9ad", wet=False, glasses=False, fog=False):
    """anchor: x = body centre, y = feet. Animated by the builder: breathing (id_body), blinking (id_open/id_shut), glancing (id_pup).
    wet -> soaked coat and hair, drops, puddle. glasses / fog (fogged lenses)."""
    dx, dy = x - 490, y - 1520
    coat2 = "#3a2a1e" if wet else coat
    o = [f'<g id="{id_}" transform="translate({dx} {dy})"><g id="{id_}_body">']
    o.append('<path d="M440,1250 L430,1500 L470,1500 L480,1260 Z" fill="#1d1a22"/><path d="M500,1260 L510,1500 L550,1500 L540,1250 Z" fill="#17141b"/>')
    o.append('<path d="M420,1490 L478,1490 L480,1520 L414,1520 Z" fill="#0a0a0d"/><path d="M502,1490 L560,1490 L566,1520 L500,1520 Z" fill="#0a0a0d"/>')
    o.append(f'<path d="M400,960 Q490,930 580,960 L600,1280 L380,1280 Z" fill="{coat2}" stroke="{LINE}" stroke-width="5" stroke-linejoin="round"/>')
    o.append(f'<path d="M490,960 L490,1280" stroke="{LINE}" stroke-width="4"/><path d="M455,950 L490,1040 L525,950" fill="#e8eef6" stroke="{LINE}" stroke-width="3"/>')
    o.append(f'<path d="M580,970 L600,1170" stroke="{coat2}" stroke-width="44" stroke-linecap="round"/><path d="M402,970 L384,1170" stroke="{coat2}" stroke-width="44" stroke-linecap="round"/>')
    o.append(f'<circle cx="602" cy="1190" r="22" fill="{skin}"/><circle cx="382" cy="1190" r="22" fill="{skin}"/><rect x="472" y="880" width="36" height="70" fill="{skin}"/>')
    o.append(f'<path d="M430,800 C430,720 550,720 550,800 C550,870 520,912 490,916 C460,912 430,870 430,800 Z" fill="{skin}" stroke="{LINE}" stroke-width="4"/>')
    o.append(f'<path d="M424,800 Q420,720 490,712 Q560,716 556,800 L540,770 L526,800 L508,766 L490,802 L470,768 L452,800 L440,776 Z" fill="{hair}"/>')
    if wet: o.append(f'<path d="M440,790 l-6,40 M470,796 l-4,36 M520,794 l4,34" stroke="{hair}" stroke-width="6" stroke-linecap="round"/>')
    o.append(f'<g id="{id_}_open"><ellipse cx="468" cy="830" rx="12" ry="9" fill="#f6f3ee"/><ellipse cx="514" cy="830" rx="12" ry="9" fill="#f6f3ee"/>'
             f'<g id="{id_}_pup"><circle cx="470" cy="831" r="6" fill="{LINE}"/><circle cx="516" cy="831" r="6" fill="{LINE}"/></g></g>'
             f'<path id="{id_}_shut" d="M456,832 Q468,838 480,832 M502,832 Q514,838 526,832" stroke="{LINE}" stroke-width="4" fill="none" opacity="0"/>')
    o.append(f'<path d="M454,814 L482,818 M500,818 L528,814" stroke="{hair}" stroke-width="5" stroke-linecap="round"/><path d="M480,880 Q492,874 504,880" stroke="#7a3a2a" stroke-width="4" fill="none" stroke-linecap="round"/>')
    if glasses:
        lens = "#eef4fb" if fog else "none"; op = ".85" if fog else "1"
        o.append(f'<g stroke="#111" stroke-width="4"><circle cx="468" cy="830" r="18" fill="{lens}" fill-opacity="{op}"/><circle cx="514" cy="830" r="18" fill="{lens}" fill-opacity="{op}"/><path d="M486,830 h10"/></g>')
    if wet:
        o.append('<g fill="#9fd0ff"><circle cx="420" cy="1100" r="5"/><circle cx="560" cy="1150" r="5"/><circle cx="470" cy="1230" r="5"/><circle cx="600" cy="1240" r="6"/></g><ellipse cx="490" cy="1526" rx="120" ry="14" fill="#7cc6ff" opacity=".45"/>')
    o.append('</g></g>')
    if name: o.append(tag(id_, x, y - 860, name))
    return "".join(o)

# ----------------------------------------------------------- backstage (case 002)
def stage_wings():
    """A single practical-lit theatre wing, with burgundy velvet and two touring trunks."""
    wing = ['''<defs>
<linearGradient id="velvet002"><stop stop-color="#211321"/><stop offset=".24" stop-color="#7f3241"/><stop offset=".50" stop-color="#431d32"/><stop offset=".8" stop-color="#702b3d"/><stop offset="1" stop-color="#241d32"/></linearGradient>
<linearGradient id="wood002" x2="0" y2="1"><stop stop-color="#805142"/><stop offset=".45" stop-color="#54403c"/><stop offset="1" stop-color="#221e2c"/></linearGradient>
<radialGradient id="worklight002" cx=".73" cy=".12" r=".88"><stop stop-color="#e8c68f" stop-opacity=".23"/><stop offset=".56" stop-color="#8a8d9f" stop-opacity=".08"/><stop offset="1" stop-color="#161828" stop-opacity="0"/></radialGradient>
<linearGradient id="metal002"><stop stop-color="#829099"/><stop offset=".22" stop-color="#cad3cd"/><stop offset=".33" stop-color="#536475"/><stop offset="1" stop-color="#2d394a"/></linearGradient>
</defs>
<rect x="0" y="0" width="1080" height="1380" fill="url(#worklight002)"/>
<path d="M155 240H1000M135 255H1035" fill="none" stroke="#161a2a" stroke-width="12"/>
<path d="M350 250Q524 456 722 251M505 249Q624 341 640 252" fill="none" stroke="#242532" stroke-width="7"/>
<path d="M171 305V1358M358 305V1358M546 305V1358M734 305V1358M922 305V1358" fill="none" stroke="#8791a0" stroke-opacity=".13" stroke-width="3"/>
<path d="M0 1238H1080M0 1345H1080" stroke="#171b25" stroke-width="11"/>
<path d="M0 1376H1080V1920H0Z" fill="url(#wood002)"/>
<path d="M0 1438H1080M0 1515H1080M0 1611H1080M0 1736H1080M0 1880H1080" stroke="#251f2b" stroke-width="5"/>
<path d="M231 1378v59m399 0v78m-462 0v95m687 0v126m-348 1v145" fill="none" stroke="#302b32" stroke-width="4"/>''']
    # One painted wing on each side; asymmetric so the room reads in close-ups as well.
    for tr in ['', 'translate(1080 0) scale(-.67 .96)']:
        wing.append(f'''<g transform="{tr}"><path d="M-10 60H248Q243 443 122 842Q91 988 90 1072Q128 1240 169 1498Q87 1530 -10 1506Z" fill="url(#velvet002)" stroke="#261a29" stroke-width="6"/>''')
        for i in range(6):
            z=23+i*39
            wing.append(f'<path d="M{z} 74 Q{int(z*1.03)} 510 {int(z*.42)} 1040 Q{int(z*.55)} 1240 {int(z*.64)} 1497" fill="none" stroke="{"#ae5b5d" if i%2 else "#271829"}" stroke-opacity=".48" stroke-width="{5 if i%2 else 10}"/>')
        wing.append('<path d="M-10 1046Q45 1084 100 1051M-10 1060Q43 1098 100 1063" fill="none" stroke="#c09960" stroke-width="9"/><path d="M88 1061q18 37 8 72" fill="none" stroke="#a77b4f" stroke-width="6"/><path d="M94 1125l-7 31 18 0-6-31Z" fill="#bb925a"/></g>')
    wing.append('''<path d="M0 0H1080V164Q980 236 873 166Q720 277 529 165Q348 270 186 160Q74 230 0 156Z" fill="url(#velvet002)" stroke="#331c2b" stroke-width="6"/>
<path d="M0 152Q72 217 186 157Q347 260 529 162Q713 267 873 162Q978 229 1080 158" fill="none" stroke="#ae8656" stroke-width="7"/>
<rect x="644" y="305" width="283" height="92" rx="10" fill="#191e2a" stroke="#ac8a63" stroke-width="4"/>
<g fill="#d2b28a"><circle cx="662" cy="324" r="4"/><circle cx="907" cy="378" r="4"/></g>''')
    wing.append(_t(785,366,44,'الكواليس','#e9d6b5'))
    # A shaded stage weight at left and a wheeled road case under the video monitor.
    for x,y,w,h in [(42,1351,305,172),(588,1092,414,352)]:
        wing.append(f'''<g transform="translate({x} {y})"><ellipse cx="{w/2+3}" cy="{h+21}" rx="{w*.55}" ry="19" fill="#141720" opacity=".48"/><rect x="13" y="{h-3}" width="28" height="28" rx="10" fill="#14151f"/><rect x="{w-44}" y="{h-3}" width="28" height="28" rx="10" fill="#14151f"/><rect x="0" y="0" width="{w}" height="{h}" rx="9" fill="#2b3540" stroke="#171c26" stroke-width="7"/><path d="M2 3H{w-2}M2 48H{w-2}M2 {h-3}H{w-2}" stroke="url(#metal002)" stroke-width="9"/><rect x="{w/2-36}" y="{h*.58}" width="72" height="25" rx="7" fill="#1a202c" stroke="#78818a" stroke-width="4"/>''')
        for xx in [30,w-55]:
            wing.append(f'<rect x="{xx}" y="32" width="26" height="33" rx="4" fill="#c7ab77" stroke="#534c4d" stroke-width="3"/><path d="M{xx+6} 47h14" stroke="#4d494b" stroke-width="4"/>')
        wing.append('</g>')
    return ''.join(wing)


def stage_ticket(x=221,y=1310):
    """A torn ivory theatre ticket, visibly in two pieces, not a second solution."""
    return f'''<g transform="translate({x} {y}) rotate(-9)"><ellipse cx="0" cy="43" rx="135" ry="17" fill="#101620" opacity=".48"/>
<path d="M-127 -59H57l-9 15 9 14-9 15 8 14-10 16 7 15-10 24H-127Z" fill="#f5e2ac" stroke="#896745" stroke-width="5"/>
<path d="M69 -65l-9 15 9 14-9 15 8 14-10 16 7 15-10 24h61V-65Z" fill="#ddbf84" stroke="#896745" stroke-width="5"/>
<path d="M-121 -45H38M-121 51H31" stroke="#b25c50" stroke-width="6"/>
{_t(-38,17,37,'تذكرة','#612c37')}
<path d="M79 -48v80m7-80v80m8-80v80" stroke="#62484a" stroke-width="4"/></g>'''


def file_monitor(x=791,y=855):
    """Editor showing the original clip's properties. Zero counts tracks; it is NOT mute.
    Rows have equal visual weight. The separate part-two ring belongs to the episode.
    """
    return f'''<g transform="translate({x} {y})"><path d="M-26 109v99l-79 12v13H107v-13l-79-12v-99Z" fill="#333e4a" stroke="#141926" stroke-width="6"/>
<rect x="-219" y="-133" width="438" height="266" rx="17" fill="#111924" stroke="#879599" stroke-width="6"/>
<rect x="-205" y="-118" width="410" height="232" rx="6" fill="#223449"/>
<path d="M-204 -116h408v55h-408Z" fill="#34505d"/>
{_t(0,-79,33,'الملف الأصلي','#f8ecd2')}
<path d="M-178 25h356" stroke="#8babb0" opacity=".6" stroke-width="2"/>
<g id="file-properties-002">{_t(43,0,37,'مسارات الصورة','#f7f2e8')}{_t(-156,0,46,'1','#f7f2e8',rtl=False)}
{_t(42,81,38,'مسارات الصوت','#f7f2e8')}{_t(-156,81,46,'0','#f7f2e8',rtl=False)}</g>
<circle cx="183" cy="122" r="3" fill="#c9ad84"/></g>'''


PROPS = dict(stage_wings=stage_wings, stage_ticket=stage_ticket, file_monitor=file_monitor, window=window, clock=clock, digital_clock=digital_clock, calendar=calendar, photo_frame=photo_frame, door=door, doormat=doormat,
             table=table, chair_over=chair_over, outline=outline, umbrella=umbrella, cup_broken=cup_broken, cup=cup, ice_glass=ice_glass,
             candle=candle, phone=phone, paper=paper, plant=plant, dusty_box=dusty_box, shoes=shoes, footprints=footprints,
             glass_shards=glass_shards, book=book, dog=dog, person=person)
