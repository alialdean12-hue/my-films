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
SKINS = {"light": "#f3d2b8", "medium": "#e2b48e", "tan": "#c98f62", "brown": "#9a6640", "dark": "#6b4429"}

def person(id_="p1", x=490, y=1520, name="", gender="m", age="adult", hair_style=None, hair="#14121a",
           facial=None, outfit="coat", coat="#6b4a32", accent="#2f6bd8", skin="#f0c9ad", body="normal",
           expression="neutral", wet=False, shoes=None, glasses=False, fog=False):
    """A suspect / witness. anchor: x = body centre, y = feet (floor y 1500-1540).
    gender: m | f · age: young | adult | old (old -> grey/white hair, wrinkles)
    hair_style: short | spiky | long | bun | bald | hijab | shemagh | curly (default: spiky for m, long for f)
    facial: None | beard | mustache | stubble · outfit: coat | suit | thobe | uniform | sweater | dress | apron | hoodie
    coat = main outfit colour, accent = tie / hijab / scarf colour · skin: hex or light|medium|tan|brown|dark
    body: normal | tall | short | heavy | thin · expression: neutral | nervous | smug | scared | angry
    wet: soaked clothes+hair · shoes: None | wet | mud (only the shoes, with a small puddle/mud) · glasses / fog.
    Animated by the builder: breathing (id_body), blinking (id_open / id_shut), glancing (id_pup)."""
    skin = SKINS.get(skin, skin)
    if hair_style is None: hair_style = "long" if gender == "f" else "spiky"
    if age == "old" and hair == "#14121a": hair = "#d9d9d9"
    if coat == "#6b4a32": coat = {"thobe": "#eef0f2", "uniform": "#22325a", "suit": "#1d2230", "dress": "#7a2f35", "apron": "#8a3a3a", "hoodie": "#3a3a4a", "sweater": "#3a5a7a"}.get(outfit, coat)
    out_col = "#3a2a1e" if wet and outfit in ("coat", "sweater", "hoodie") else coat
    sx = {"heavy": 1.22, "thin": 0.86}.get(body, 1.0); sy = {"tall": 1.08, "short": 0.9}.get(body, 1.0)
    o = [f'<g id="{id_}" transform="translate({x} {y}) scale({sy}) translate(-490 -1520)"><g id="{id_}_body">']
    W = f'transform="translate(490 0) scale({sx} 1) translate(-490 0)"'
    long_robe = outfit in ("thobe", "dress")
    # back hair / hijab (behind everything)
    if hair_style == "long":
        o.append(f'<path d="M426,780 Q420,700 490,698 Q562,700 556,780 L566,1010 Q490,1040 414,1010 Z" fill="{hair}"/>')
    if hair_style == "hijab":
        o.append(f'<path d="M418,800 Q414,690 490,686 Q566,690 562,800 L590,1000 Q490,1040 390,1000 Z" fill="{accent}"/>')
    if hair_style == "shemagh":
        o.append('<path d="M412,790 Q410,690 490,684 Q570,690 568,790 L600,1010 L380,1010 Z" fill="#f2f2f2"/>')
    o.append(f'<g {W}>')
    # legs + shoes
    leg = "#1d1a22" if outfit != "uniform" else "#1a2440"
    if not long_robe or outfit == "dress":
        o.append(f'<path d="M440,1250 L430,1500 L470,1500 L480,1260 Z" fill="{leg if outfit!="dress" else skin}"/><path d="M500,1260 L510,1500 L550,1500 L540,1250 Z" fill="{"#17141b" if outfit!="dress" else skin}"/>')
    shoe = {"mud": "#4a3018"}.get(shoes, "#0a0a0d") if outfit != "thobe" else "#5a3a22"
    o.append(f'<path d="M420,1490 L478,1490 L480,1520 L414,1520 Z" fill="{shoe}"/><path d="M502,1490 L560,1490 L566,1520 L500,1520 Z" fill="{shoe}"/>')
    if shoes == "wet": o.append('<g fill="#9fd0ff"><circle cx="430" cy="1484" r="4"/><circle cx="552" cy="1486" r="4"/></g><ellipse cx="490" cy="1528" rx="100" ry="10" fill="#7cc6ff" opacity=".45"/>')
    if shoes == "mud": o.append('<g fill="#5a3a1a"><circle cx="424" cy="1516" r="7"/><circle cx="470" cy="1518" r="6"/><circle cx="512" cy="1517" r="7"/><circle cx="556" cy="1518" r="6"/></g>')
    # torso by outfit
    L = f'stroke="{LINE}" stroke-width="5" stroke-linejoin="round"'
    if outfit == "coat":
        o.append(f'<path d="M400,960 Q490,930 580,960 L600,1280 L380,1280 Z" fill="{out_col}" {L}/><path d="M490,960 L490,1280" stroke="{LINE}" stroke-width="4"/><path d="M455,950 L490,1040 L525,950" fill="#e8eef6" stroke="{LINE}" stroke-width="3"/>')
    elif outfit == "suit":
        o.append(f'<path d="M400,960 Q490,930 580,960 L594,1260 L386,1260 Z" fill="{coat}" {L}/><path d="M462,950 L490,1060 L518,950 Z" fill="#f2f4f8"/><path d="M484,960 L496,960 L500,1040 L490,1056 L480,1040 Z" fill="{accent}"/>'
                 f'<path d="M456,948 L490,1070 L438,1010 L430,966 Z M524,948 L490,1070 L542,1010 L550,966 Z" fill="{coat}" stroke="#000" stroke-opacity=".35" stroke-width="3"/>')
    elif outfit == "thobe":
        o.append(f'<path d="M404,960 Q490,934 576,960 L604,1494 L376,1494 Z" fill="{coat}" {L}/><path d="M490,960 L490,1100" stroke="#b9c0c8" stroke-width="4"/><circle cx="490" cy="980" r="5" fill="#b9c0c8"/>')
    elif outfit == "dress":
        o.append(f'<path d="M410,960 Q490,934 570,960 L612,1400 L368,1400 Z" fill="{coat}" {L}/><path d="M440,1120 Q490,1140 540,1120" stroke="#000" stroke-opacity=".25" stroke-width="4" fill="none"/>')
    elif outfit == "uniform":
        o.append(f'<path d="M400,960 Q490,930 580,960 L594,1270 L386,1270 Z" fill="{coat}" {L}/><rect x="392" y="1180" width="196" height="22" fill="#111"/><rect x="478" y="1176" width="24" height="30" fill="#c9a24a"/>'
                 f'<path d="M538,1010 l8,16 l18,2 l-13,12 l4,18 l-17,-9 l-16,9 l4,-18 l-13,-12 l18,-2 Z" fill="#ffd21f"/>')
    elif outfit == "sweater":
        o.append(f'<path d="M400,960 Q490,930 580,960 L596,1280 L384,1280 Z" fill="{out_col}" {L}/><path d="M458,950 Q490,980 522,950" stroke="#000" stroke-opacity=".3" stroke-width="10" fill="none"/>'
                 + "".join(f'<path d="M392,{1040+k*60} H588" stroke="#000" stroke-opacity=".12" stroke-width="6"/>' for k in range(4)))
    elif outfit == "hoodie":
        o.append(f'<path d="M400,960 Q490,930 580,960 L596,1280 L384,1280 Z" fill="{out_col}" {L}/><path d="M440,950 Q490,1010 540,950" stroke="#000" stroke-opacity=".35" stroke-width="12" fill="none"/><path d="M470,990 L466,1060 M510,990 L514,1060" stroke="#ddd" stroke-width="4"/><rect x="430" y="1160" width="120" height="60" rx="14" fill="#000" opacity=".2"/>')
    elif outfit == "apron":
        o.append(f'<path d="M400,960 Q490,930 580,960 L596,1280 L384,1280 Z" fill="{coat}" {L}/><path d="M440,1000 L540,1000 L560,1290 L420,1290 Z" fill="#f4f4f4" stroke="#999" stroke-width="3"/><path d="M440,1000 L470,950 M540,1000 L510,950" stroke="#f4f4f4" stroke-width="8"/>')
    arm = out_col
    o.append(f'<path d="M580,970 L600,1170" stroke="{arm}" stroke-width="44" stroke-linecap="round"/><path d="M402,970 L384,1170" stroke="{arm}" stroke-width="44" stroke-linecap="round"/>')
    o.append(f'<circle cx="602" cy="1190" r="22" fill="{skin}"/><circle cx="382" cy="1190" r="22" fill="{skin}"/>')
    o.append('</g>')
    # neck + head
    if hair_style not in ("hijab", "shemagh"): o.append(f'<rect x="472" y="880" width="36" height="70" fill="{skin}"/>')
    o.append(f'<path d="M430,800 C430,720 550,720 550,800 C550,870 520,912 490,916 C460,912 430,870 430,800 Z" fill="{skin}" stroke="{LINE}" stroke-width="4"/>')
    if age == "old": o.append(f'<path d="M456,770 h56 M462,782 h44 M446,846 l-8,6 M534,846 l8,6" stroke="#000" stroke-opacity=".28" stroke-width="3" fill="none"/>')
    # front hair
    if hair_style == "spiky":
        o.append(f'<path d="M424,800 Q420,720 490,712 Q560,716 556,800 L540,770 L526,800 L508,766 L490,802 L470,768 L452,800 L440,776 Z" fill="{hair}"/>')
    elif hair_style == "short":
        o.append(f'<path d="M428,796 Q426,716 490,712 Q556,716 552,796 Q540,758 490,756 Q440,758 428,796 Z" fill="{hair}"/>')
    elif hair_style == "curly":
        o.append(f'<g fill="{hair}">' + "".join(f'<circle cx="{430+k*20}" cy="{752+(k%2)*10}" r="22"/>' for k in range(7)) + '<circle cx="436" cy="792" r="16"/><circle cx="546" cy="792" r="16"/></g>')
    elif hair_style == "long":
        o.append(f'<path d="M426,812 Q428,712 490,708 Q556,712 556,812 Q540,764 500,752 Q468,776 438,812 Z" fill="{hair}"/>')
    elif hair_style == "bun":
        o.append(f'<circle cx="490" cy="700" r="30" fill="{hair}"/><path d="M428,800 Q426,716 490,712 Q556,716 552,800 Q540,756 490,752 Q440,756 428,800 Z" fill="{hair}"/>')
    elif hair_style == "bald":
        o.append(f'<path d="M430,806 q-2,-22 8,-30 M550,806 q2,-22 -8,-30" stroke="{hair}" stroke-width="12" stroke-linecap="round" fill="none"/><path d="M462,734 Q490,726 518,734" stroke="#fff" stroke-opacity=".35" stroke-width="5" fill="none"/>')
    elif hair_style == "hijab":
        o.append(f'<path d="M428,806 Q426,712 490,708 Q554,712 552,806" fill="none" stroke="{accent}" stroke-width="18"/><path d="M432,860 Q440,930 490,946 Q540,930 548,860 L560,980 L420,980 Z" fill="{accent}"/>')
    elif hair_style == "shemagh":
        o.append('<path d="M424,806 Q426,712 490,708 Q554,712 556,806" fill="none" stroke="#f2f2f2" stroke-width="18"/><path d="M424,748 Q490,724 556,748" stroke="#111" stroke-width="12" fill="none"/><path d="M426,764 Q490,740 554,764" stroke="#111" stroke-width="8" fill="none"/>')
    # brows by expression
    brow = {"neutral": "M454,814 L482,818 M500,818 L528,814", "nervous": "M454,812 L482,804 M500,804 L528,812", "smug": "M454,818 L482,814 M500,810 L528,816",
            "scared": "M454,808 L482,800 M500,800 L528,808", "angry": "M454,806 L482,818 M500,818 L528,806"}[expression]
    o.append(f'<path d="{brow}" stroke="{hair if hair_style not in ("hijab","shemagh") else "#2a1a12"}" stroke-width="5" stroke-linecap="round"/>')
    ry = 6 if expression == "smug" else (11 if expression == "scared" else 9)
    o.append(f'<g id="{id_}_open"><ellipse cx="468" cy="830" rx="12" ry="{ry}" fill="#f6f3ee"/><ellipse cx="514" cy="830" rx="12" ry="{ry}" fill="#f6f3ee"/>'
             f'<g id="{id_}_pup"><circle cx="470" cy="831" r="{5 if ry<7 else 6}" fill="{LINE}"/><circle cx="516" cy="831" r="{5 if ry<7 else 6}" fill="{LINE}"/></g></g>'
             f'<path id="{id_}_shut" d="M456,832 Q468,838 480,832 M502,832 Q514,838 526,832" stroke="{LINE}" stroke-width="4" fill="none" opacity="0"/>')
    if gender == "f": o.append(f'<path d="M454,822 l-6,-6 M526,822 l6,-6" stroke="{LINE}" stroke-width="3"/>')
    mouth = {"neutral": "M480,880 Q492,874 504,880", "nervous": "M478,882 Q484,876 490,882 Q496,876 504,882", "smug": "M478,878 Q496,888 508,872",
             "scared": "M482,876 Q492,894 502,876 Z", "angry": "M478,884 Q492,874 506,884"}[expression]
    lip = "#b0444a" if gender == "f" else "#7a3a2a"
    o.append(f'<path d="{mouth}" stroke="{lip}" stroke-width="4" fill="{"#3a1a14" if expression=="scared" else "none"}" stroke-linecap="round"/>')
    if expression == "nervous": o.append('<path d="M548,786 q8,14 0,22 q-8,-8 0,-22 Z" fill="#9fd0ff"/>')
    if facial == "beard": o.append(f'<path d="M434,842 Q440,912 490,926 Q540,912 546,842 Q532,890 490,894 Q448,890 434,842 Z" fill="{hair}"/><path d="M470,868 Q490,858 510,868 Q490,876 470,868 Z" fill="{hair}"/>')
    if facial == "mustache": o.append(f'<path d="M466,870 Q490,856 514,870 Q490,878 466,870 Z" fill="{hair}"/>')
    if facial == "stubble": o.append(f'<path d="M440,850 Q446,906 490,918 Q534,906 540,850" stroke="{hair}" stroke-opacity=".35" stroke-width="16" fill="none" stroke-dasharray="2 4"/>')
    if hair_style == "spiky" and wet: o.append(f'<path d="M440,790 l-6,40 M470,796 l-4,36 M520,794 l4,34" stroke="{hair}" stroke-width="6" stroke-linecap="round"/>')
    if glasses:
        lens = "#eef4fb" if fog else "none"; op = ".85" if fog else "1"
        o.append(f'<g stroke="#111" stroke-width="4"><circle cx="468" cy="830" r="18" fill="{lens}" fill-opacity="{op}"/><circle cx="514" cy="830" r="18" fill="{lens}" fill-opacity="{op}"/><path d="M486,830 h10"/></g>')
    if wet:
        o.append('<g fill="#9fd0ff"><circle cx="420" cy="1100" r="5"/><circle cx="560" cy="1150" r="5"/><circle cx="470" cy="1230" r="5"/><circle cx="600" cy="1240" r="6"/></g><ellipse cx="490" cy="1526" rx="120" ry="14" fill="#7cc6ff" opacity=".45"/>')
    o.append('</g></g>')
    if name: o.append(tag(id_, x, y - int(860 * sy), name))
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


# ---------------------------------------------------------------- furniture (for room presets)
def sofa(x=880, y=1400, color="#5a2f3a"):
    """anchor: bottom-centre, against the back wall."""
    return (f'<rect x="{x-190}" y="{y-230}" width="380" height="140" rx="30" fill="{color}" stroke="#1a0f12" stroke-width="4"/><rect x="{x-200}" y="{y-120}" width="400" height="100" rx="20" fill="{color}" stroke="#1a0f12" stroke-width="4"/>'
            f'<rect x="{x-220}" y="{y-170}" width="50" height="150" rx="20" fill="{color}" stroke="#1a0f12" stroke-width="4"/><rect x="{x+170}" y="{y-170}" width="50" height="150" rx="20" fill="{color}" stroke="#1a0f12" stroke-width="4"/>'
            f'<rect x="{x-180}" y="{y-20}" width="16" height="22" fill="#1a0f12"/><rect x="{x+164}" y="{y-20}" width="16" height="22" fill="#1a0f12"/>')

def rug(x=540, y=1600, color="#6b2a2a"):
    return f'<ellipse cx="{x}" cy="{y}" rx="380" ry="90" fill="{color}" opacity=".85"/><ellipse cx="{x}" cy="{y}" rx="330" ry="66" fill="none" stroke="#e8c87a" stroke-width="5" opacity=".7"/>'

def desk(x=860, y=1300, screen="", lit=True):
    """anchor: top-centre of the desk (y = desk top). Computer monitor; screen text optional."""
    scr = "#0e2a55" if lit else "#050608"
    return (table(x, y, 340) + f'<rect x="{x-110}" y="{y-200}" width="220" height="150" rx="8" fill="#111" stroke="#3a4560" stroke-width="5"/><rect x="{x-98}" y="{y-188}" width="196" height="126" fill="{scr}"/>'
            f'<rect x="{x-12}" y="{y-50}" width="24" height="50" fill="#222"/>' + (_t(x, y - 116, 30, screen, "#fff") if screen and lit else ""))

def bookshelf(x=900, y=1380):
    """anchor: bottom-centre."""
    books = "".join(f'<rect x="{x-150+(k*37)%290}" y="{y-470+(k//8)*120}" width="26" height="{80+(k*13)%26}" fill="{["#7a2f35","#2f5a7a","#7a6a2f","#3a6a3a"][k%4]}"/>' for k in range(32))
    return f'<rect x="{x-170}" y="{y-520}" width="340" height="520" fill="#4a2f1f" stroke="#1a0f0a" stroke-width="5"/>' + "".join(f'<rect x="{x-160}" y="{y-390+i*120}" width="320" height="14" fill="#2a1a10"/>' for i in range(4)) + books

def bed(x=840, y=1420, color="#3a4a7a"):
    """anchor: bottom-centre."""
    return (f'<rect x="{x-230}" y="{y-330}" width="40" height="330" fill="#4a2f1f"/><rect x="{x-230}" y="{y-170}" width="470" height="120" rx="14" fill="#f2f2f2"/>'
            f'<rect x="{x-190}" y="{y-200}" width="110" height="50" rx="20" fill="#fff" stroke="#ccc" stroke-width="3"/><rect x="{x-110}" y="{y-180}" width="350" height="110" rx="16" fill="{color}"/><rect x="{x-230}" y="{y-50}" width="470" height="50" fill="#4a2f1f"/>')

def fridge(x=960, y=1400):
    return f'<rect x="{x-110}" y="{y-560}" width="220" height="560" rx="18" fill="#dfe5ec" stroke="#8592a8" stroke-width="5"/><path d="M{x-110},{y-360} H{x+110}" stroke="#8592a8" stroke-width="5"/><rect x="{x+70}" y="{y-500}" width="12" height="90" rx="6" fill="#8592a8"/><rect x="{x+70}" y="{y-320}" width="12" height="120" rx="6" fill="#8592a8"/>'

def counter(x=760, y=1400, w=420):
    """anchor: bottom-centre. kitchen counter, top surface at y-300 (put cups there)."""
    return f'<rect x="{x-w/2}" y="{y-300}" width="{w}" height="300" fill="#6b4a32" stroke="#2a1a12" stroke-width="5"/><rect x="{x-w/2-10}" y="{y-320}" width="{w+20}" height="26" fill="#d9d2c4"/>' + "".join(f'<rect x="{x-w/2+20+k*(w/3)}" y="{y-270}" width="{w/3-40}" height="230" fill="none" stroke="#2a1a12" stroke-width="4"/>' for k in range(3))

def painting(x=860, y=1000, kind="landscape"):
    """anchor: centre. framed painting (also good as a wall clue holder)."""
    inner = '<rect x="-96" y="-66" width="192" height="132" fill="#e8b36a"/><path d="M-96,40 L-40,-20 L10,30 L50,-10 L96,40 L96,66 L-96,66 Z" fill="#4a6a3a"/>' if kind == "landscape" else '<rect x="-96" y="-66" width="192" height="132" fill="#3a2a4a"/><circle cx="0" cy="-6" r="30" fill="#e8c8a8"/>'
    return f'<g transform="translate({x} {y})"><rect x="-112" y="-82" width="224" height="164" fill="#c9a24a" stroke="#6a4a1a" stroke-width="5"/>{inner}</g>'

def crates(x=860, y=1500, n=3):
    """anchor: bottom-centre. stacked wooden crates (warehouse)."""
    out = ""
    pos = [(-120, 0), (60, 0), (-30, -160)][:n]
    for dx, dy in pos:
        cx, cy = x + dx, y + dy
        out += f'<rect x="{cx-80}" y="{cy-160}" width="160" height="160" fill="#8a6a3a" stroke="#3a2a14" stroke-width="5"/><path d="M{cx-80},{cy-160} L{cx+80},{cy} M{cx+80},{cy-160} L{cx-80},{cy}" stroke="#3a2a14" stroke-width="5"/>'
    return out

def safe(x=880, y=1500, open_=True, empty=True):
    """anchor: bottom-centre. a wall/floor safe; open shows the inside (empty or with money)."""
    out = f'<rect x="{x-120}" y="{y-240}" width="240" height="240" rx="10" fill="#3a4250" stroke="#11151c" stroke-width="6"/><rect x="{x-96}" y="{y-216}" width="192" height="192" fill="#11151c"/>'
    if not empty: out += f'<rect x="{x-70}" y="{y-110}" width="140" height="60" fill="#3a7a4a"/><rect x="{x-60}" y="{y-150}" width="120" height="40" fill="#3a7a4a"/>'
    if open_: out += f'<path d="M{x-120},{y-240} L{x-230},{y-210} L{x-230},{y-30} L{x-120},{y}" fill="#4a5262" stroke="#11151c" stroke-width="6"/><circle cx="{x-180}" cy="{y-120}" r="22" fill="#c9ccd4" stroke="#11151c" stroke-width="4"/>'
    else: out += f'<circle cx="{x}" cy="{y-120}" r="34" fill="#c9ccd4" stroke="#11151c" stroke-width="5"/>'
    return out

def lamp_stand(x=160, y=1500, lit=True):
    out = f'<rect x="{x-6}" y="{y-420}" width="12" height="420" fill="#222"/><ellipse cx="{x}" cy="{y}" rx="50" ry="10" fill="#222"/><path d="M{x-70},{y-420} L{x+70},{y-420} L{x+40},{y-520} L{x-40},{y-520} Z" fill="{"#ffd27a" if lit else "#6a5a3a"}" stroke="#2a1a12" stroke-width="4"/>'
    return out

def blinds(x=640, y=300, w=320, h=520):
    """window blinds drawn over a window (office)."""
    return "".join(f'<rect x="{x}" y="{y+k*26}" width="{w}" height="14" fill="#c9ccd4" opacity=".55"/>' for k in range(h // 26))

def hanging_bulb(x=540, y=0, lit=True):
    return f'<path d="M{x},{y} V{y+260}" stroke="#222" stroke-width="4"/><circle cx="{x}" cy="{y+290}" r="30" fill="{"#ffe8a8" if lit else "#555"}"/>' + (f'<circle cx="{x}" cy="{y+290}" r="120" fill="#ffd27a" opacity=".12"/>' if lit else "")

def shelf_items(x=860, y=1380):
    """shop shelves with jars and boxes. anchor: bottom-centre."""
    out = f'<rect x="{x-190}" y="{y-560}" width="380" height="560" fill="#5a3e2a" stroke="#2a1a10" stroke-width="5"/>'
    for i in range(4):
        sy_ = y - 440 + i * 130
        out += f'<rect x="{x-180}" y="{sy_}" width="360" height="12" fill="#2a1a10"/>'
        out += "".join(f'<rect x="{x-170+k*58}" y="{sy_-70}" width="44" height="70" rx="8" fill="{["#c4262e","#2f6bd8","#e8b33a","#3a8a4a"][(i+k)%4]}"/>' for k in range(6))
    return out

PRESETS = {
    "living":    dict(wall="#0c1628", wall2="#1a2a44", pattern="plain", furniture=[("sofa", dict(x=880, y=1400)), ("rug", dict(x=540, y=1610))]),
    "office":    dict(wall="#1a2230", wall2="#2a3446", pattern="panels", furniture=[("desk", dict(x=860, y=1300)), ("blinds", dict(x=640, y=300))]),
    "hotel":     dict(wall="#2a1a2a", wall2="#3a2438", pattern="wallpaper", furniture=[("bed", dict(x=850, y=1420)), ("lamp_stand", dict(x=1010, y=1420))]),
    "kitchen":   dict(wall="#1c2a2a", wall2="#2a3a3a", pattern="tiles", furniture=[("counter", dict(x=720, y=1400)), ("fridge", dict(x=990, y=1400))]),
    "warehouse": dict(wall="#1a1c20", wall2="#2a2c30", pattern="metal", furniture=[("crates", dict(x=880, y=1500)), ("hanging_bulb", dict(x=540, y=0))]),
    "shop":      dict(wall="#24180f", wall2="#3a2818", pattern="plain", furniture=[("shelf_items", dict(x=880, y=1380))]),
    "none":      dict(wall="#0c1628", wall2="#1a2a44", pattern="plain", furniture=[]),
}

def wall_pattern(kind, floor_y=1380):
    if kind == "wallpaper": return '<g opacity=".12" fill="#fff">' + "".join(f'<circle cx="{40+(i%14)*80+(i//14%2)*40}" cy="{40+(i//14)*80}" r="6"/>' for i in range(14 * (floor_y // 80))) + '</g>'
    if kind == "tiles": return '<g stroke="#fff" stroke-opacity=".08" stroke-width="3">' + "".join(f'<path d="M0,{k*90}H1080"/>' for k in range(floor_y // 90)) + "".join(f'<path d="M{k*90},0V{floor_y}"/>' for k in range(13)) + '</g>'
    if kind == "metal": return '<g stroke="#000" stroke-opacity=".35" stroke-width="4">' + "".join(f'<path d="M{k*120},0V{floor_y}"/>' for k in range(10)) + '</g>'
    if kind == "panels": return '<g stroke="#000" stroke-opacity=".25" stroke-width="4"><path d="M0,1000H1080"/></g>'
    return ""

PROPS = dict(stage_wings=stage_wings, stage_ticket=stage_ticket, file_monitor=file_monitor,
             window=window, clock=clock, digital_clock=digital_clock, calendar=calendar, photo_frame=photo_frame, door=door, doormat=doormat,
             table=table, chair_over=chair_over, outline=outline, umbrella=umbrella, cup_broken=cup_broken, cup=cup, ice_glass=ice_glass,
             candle=candle, phone=phone, paper=paper, plant=plant, dusty_box=dusty_box, shoes=shoes, footprints=footprints,
             glass_shards=glass_shards, book=book, dog=dog, person=person,
             sofa=sofa, rug=rug, desk=desk, bookshelf=bookshelf, bed=bed, fridge=fridge, counter=counter, painting=painting,
             crates=crates, safe=safe, lamp_stand=lamp_stand, blinds=blinds, hanging_bulb=hanging_bulb, shelf_items=shelf_items)

# people v3 (different face / body shapes, poses, accessories, ready cast) replaces the simple person above
from people import person, SKINS, CAST  # noqa: E402
PROPS["person"] = person

# moving objects, animals, plants (things.py) — "dog" is replaced by the animated version
import things  # noqa: E402
PROPS.update(things.THINGS)
