"""saw_5tory things: moving objects & vehicles, animals, plants, atmospheres. All drawn in code and animated.
Animation is declared with classes the builder reads (no code needed in the episode json):
  a-spin  data-o="x y" data-s=turns/sec      a-sway data-o="x y" data-a=deg data-p=sec
  a-bob   data-d=px data-p=sec               a-blink data-p=sec (closes for 0.12 s)
  a-flashA / a-flashB (alternate, police)     a-drift data-x0 data-x1 data-p (moves across, loops)
  a-fall  data-h=px data-p=sec (falls & loops) a-flicker (candle-like opacity)
Anchor of every object = bottom-centre on the floor unless noted. Use scale `s` to resize."""
import math

LINE = "#1a120c"

def _g(inner, x, y, s=1.0, flip=False):
    return f'<g transform="translate({x} {y}) scale({-s if flip else s} {s})">{inner}</g>'

def _wheel(cx, cy, r, spin=False, tyre="#111", hub="#9aa4b2"):
    spokes = "".join(f'<path d="M0,0 L{r*0.7*math.cos(k*1.047):.1f},{r*0.7*math.sin(k*1.047):.1f}" stroke="{hub}" stroke-width="{max(2,r*0.1):.0f}"/>' for k in range(6))
    cls = f' class="a-spin" data-o="{cx} {cy}" data-s="1.2"' if spin else ""
    return f'<g transform="translate({cx} {cy})"><circle r="{r}" fill="{tyre}"/><g{cls}>{spokes}</g><circle r="{r*0.28:.1f}" fill="{hub}"/></g>' if not spin else \
           f'<g transform="translate({cx} {cy})"><circle r="{r}" fill="{tyre}"/></g><g{cls}><g transform="translate({cx} {cy})">{spokes}<circle r="{r*0.28:.1f}" fill="{hub}"/></g></g>'

def _moving(svg, x, moving, period=6, x0=-500, x1=1600):
    return f'<g class="a-drift" data-x0="{x0-x}" data-x1="{x1-x}" data-p="{period}">{svg}</g>' if moving else svg

# =========================================================== vehicles & moving objects
def vehicle(x=540, y=1540, kind="sedan", color=None, s=1.0, flip=False, moving=False, lights=True):
    """kind: sedan · taxi · police · ambulance · pickup · truck · bus · van. moving=True drives across the frame (wheels spin)."""
    col = color or {"sedan": "#8a1e2e", "taxi": "#e8b33a", "police": "#f4f6f8", "ambulance": "#f4f6f8", "pickup": "#2f5a7a", "truck": "#c4562e", "bus": "#2f8a5a", "van": "#c9ccd4"}[kind]
    w = {"bus": 900, "truck": 760, "van": 560, "pickup": 560}.get(kind, 480)
    h = {"bus": 380, "truck": 360, "van": 300}.get(kind, 180)
    o = []; txt = []
    if kind in ("bus", "van", "truck"):
        o.append(f'<rect x="{-w/2}" y="{-h-20}" width="{w}" height="{h}" rx="26" fill="{col}" stroke="{LINE}" stroke-width="6"/>')
        nwin = 5 if kind == "bus" else (2 if kind == "van" else 1)
        o.append("".join(f'<rect x="{-w/2+30+k*(w-60)/nwin}" y="{-h+10}" width="{(w-60)/nwin-20}" height="{h*0.35}" rx="10" fill="#9fc6e8" stroke="{LINE}" stroke-width="3"/>' for k in range(nwin)))
        if kind == "truck": o.append(f'<rect x="{w/2-200}" y="{-h+10}" width="180" height="{h*0.4}" rx="10" fill="#9fc6e8" stroke="{LINE}" stroke-width="3"/><rect x="{-w/2}" y="{-h-20}" width="{w-230}" height="{h}" fill="#e8e2d0" stroke="{LINE}" stroke-width="6"/>')
        if kind == "bus": txt.append(f'<text x="0" y="{-60}" text-anchor="middle" font-family="Cairo" font-weight="900" font-size="48" fill="#fff" direction="rtl">خط 12</text>')
    else:
        o.append(f'<path d="M{-w/2},-40 L{-w/2+20},-120 Q{-w/2+80},-{h} {-60},-{h} L60,-{h} Q{w/2-110},-{h-10} {w/2-70},-110 L{w/2},-90 L{w/2+10},-30 L{-w/2},-30 Z" fill="{col}" stroke="{LINE}" stroke-width="5"/>')
        o.append(f'<path d="M{-w/2+50},-120 Q{-w/2+100},-{h-12} -50,-{h-12} L-50,-116 Z M-30,-{h-12} L50,-{h-12} Q{w/2-130},-{h-20} {w/2-100},-116 L-30,-116 Z" fill="#9fc6e8" stroke="{LINE}" stroke-width="3"/>')
        if kind == "pickup": o.append(f'<rect x="{-w/2}" y="-120" width="{w*0.45}" height="90" fill="{col}" stroke="{LINE}" stroke-width="5"/>')
    if lights: o.append(f'<rect x="{w/2-30}" y="-96" width="26" height="16" fill="#ffe8a8"/><rect x="{-w/2+4}" y="-96" width="18" height="16" fill="#c4262e"/>')
    if kind == "taxi": o.append(f'<rect x="-50" y="-{h+28}" width="100" height="28" rx="6" fill="#111"/>'); txt.append(f'<text x="0" y="-{h+6}" text-anchor="middle" font-family="Cairo" font-weight="900" font-size="22" fill="#e8b33a" direction="rtl">أجرة</text>')
    if kind == "police":
        o.append(f'<rect x="{-w/2+10}" y="-100" width="{w-20}" height="24" fill="#1f2d4d"/>'); txt.append('<text x="0" y="-82" text-anchor="middle" font-family="Cairo" font-weight="900" font-size="22" fill="#fff" direction="rtl">شرطة</text>')
        o.append(f'<rect class="a-flashA" x="-40" y="-{h+24}" width="36" height="22" rx="5" fill="#ff3b3b"/><rect class="a-flashB" x="4" y="-{h+24}" width="36" height="22" rx="5" fill="#3b7bff"/>')
    if kind == "ambulance":
        o.append(f'<rect x="-30" y="-{h-30}" width="60" height="16" fill="#c4262e"/><rect x="-8" y="-{h-8}" width="16" height="60" fill="#c4262e" transform="translate(0 -30)"/><rect class="a-flashA" x="-20" y="-{h+24}" width="40" height="22" rx="5" fill="#ff3b3b"/>')
    rr = 46 if kind in ("bus", "truck") else 42
    for wx in ((-w/2+110, w/2-110) if kind != "bus" else (-w/2+140, w/2-140)):
        o.append(_wheel(wx, -28, rr, spin=moving))
    return _moving(_g("".join(o), x, y, s, flip) + _g("".join(txt), x, y, s), x, moving, 5)

def motorcycle(x=540, y=1540, color="#c4262e", s=1.0, flip=False, moving=False):
    o = _wheel(-130, -50, 50, moving) + _wheel(130, -50, 50, moving)
    o += f'<path d="M-130,-50 L-40,-140 L80,-140 L130,-50" stroke="{LINE}" stroke-width="10" fill="none"/><path d="M-60,-150 Q0,-200 70,-150 Z" fill="{color}" stroke="{LINE}" stroke-width="4"/><rect x="-110" y="-170" width="90" height="22" rx="8" fill="#222"/><path d="M90,-150 l40,-60 M110,-210 h40" stroke="#222" stroke-width="10"/>'
    return _moving(_g(o, x, y, s, flip), x, moving, 4)

def bicycle(x=540, y=1540, color="#2f6bd8", s=1.0, flip=False, moving=False):
    o = _wheel(-110, -60, 60, moving, "#222", "#c9ccd4") + _wheel(110, -60, 60, moving, "#222", "#c9ccd4")
    o += f'<path d="M-110,-60 L-20,-60 L50,-150 L-50,-150 Z M-20,-60 L-50,-170 M50,-150 L110,-60 M50,-150 L40,-190" stroke="{color}" stroke-width="10" fill="none" stroke-linejoin="round"/><rect x="-80" y="-182" width="60" height="14" rx="6" fill="#111"/><path d="M20,-196 h44" stroke="#111" stroke-width="10"/>'
    return _moving(_g(o, x, y, s, flip), x, moving, 7)

def shopping_cart(x=540, y=1540, s=1.0, moving=False, full=False):
    o = f'<path d="M-120,-300 L-90,-300 L-60,-120 L120,-120 L140,-260 L-80,-260" stroke="#9aa4b2" stroke-width="8" fill="none"/>' + "".join(f'<path d="M{-60+k*30},-250 L{-48+k*30},-130" stroke="#9aa4b2" stroke-width="3"/>' for k in range(7))
    if full: o += "".join(f'<rect x="{-50+k*44}" y="-{220+(k%2)*30}" width="38" height="{80+(k%2)*30}" rx="6" fill="{c}"/>' for k, c in enumerate(("#c4262e", "#e8b33a", "#2f6bd8", "#3a8a4a")))
    o += _wheel(-40, -30, 24, moving) + _wheel(100, -30, 24, moving)
    return _moving(_g(o, x, y, s), x, moving, 8)

def wheelchair(x=540, y=1540, s=1.0, flip=False, moving=False):
    o = _wheel(-40, -120, 110, moving, "#333", "#c9ccd4") + _wheel(120, -34, 34, moving)
    o += f'<path d="M-90,-420 L-60,-200 L110,-200 L130,-120 M-60,-200 L-40,-120" stroke="#555" stroke-width="12" fill="none"/><rect x="-70" y="-230" width="190" height="40" rx="10" fill="#2f4a7a"/><rect x="-100" y="-420" width="40" height="200" rx="10" fill="#2f4a7a"/>'
    return _moving(_g(o, x, y, s, flip), x, moving, 9)

def suitcase(x=540, y=1540, color="#7a2f35", s=1.0, moving=False):
    o = f'<rect x="-80" y="-280" width="160" height="250" rx="22" fill="{color}" stroke="{LINE}" stroke-width="5"/><path d="M-80,-200 H80 M-80,-120 H80" stroke="#000" stroke-opacity=".25" stroke-width="5"/><path d="M-30,-280 V-360 H30 V-280" stroke="#555" stroke-width="10" fill="none"/>' + _wheel(-50, -18, 16, moving) + _wheel(50, -18, 16, moving)
    return _moving(_g(o, x, y, s), x, moving, 9)

def stroller(x=540, y=1540, color="#5a7a9a", s=1.0, moving=False):
    o = f'<path d="M-140,-180 Q-140,-330 0,-330 L0,-180 Z" fill="{color}" stroke="{LINE}" stroke-width="5"/><rect x="-140" y="-200" width="260" height="70" rx="30" fill="{color}" stroke="{LINE}" stroke-width="5"/><path d="M120,-180 L190,-330" stroke="#555" stroke-width="10"/>' + _wheel(-90, -50, 40, moving) + _wheel(80, -50, 40, moving)
    return _moving(_g(o, x, y, s), x, moving, 10)

def ceiling_fan(x=540, y=0, s=1.0, on=True):
    """anchor: ceiling point (top). Blades spin when on."""
    blades = "".join(f'<path d="M0,0 L{200*math.cos(k*1.571):.0f},{40*math.sin(k*1.571):.0f}" stroke="#5a3a22" stroke-width="30" stroke-linecap="round"/>' for k in range(4))
    cls = ' class="a-spin" data-o="0 0" data-s="0.8"' if on else ""
    return _g(f'<path d="M0,0 V160" stroke="#222" stroke-width="10"/><g transform="translate(0 170) scale(1 .35)"><g{cls}>{blades}</g></g><circle cy="170" r="30" fill="#c9a24a"/>', x, y, s)

def desk_fan(x=540, y=1300, s=1.0, on=True):
    blades = "".join(f'<ellipse cx="{50*math.cos(k*2.094):.0f}" cy="{50*math.sin(k*2.094):.0f}" rx="44" ry="18" transform="rotate({k*120} {50*math.cos(k*2.094):.0f} {50*math.sin(k*2.094):.0f})" fill="#9fc6e8"/>' for k in range(3))
    cls = ' class="a-spin" data-o="0 0" data-s="3"' if on else ""
    return _g(f'<path d="M0,-170 V-20" stroke="#555" stroke-width="12"/><ellipse cy="-10" rx="70" ry="16" fill="#555"/><g transform="translate(0 -230)"><circle r="110" fill="none" stroke="#9aa4b2" stroke-width="5"/><g{cls}>{blades}</g><circle r="18" fill="#555"/></g>', x, y, s)

def pendulum_clock(x=540, y=1500, s=1.0, time="11:40"):
    hh, mm = [int(v) for v in time.split(":")]
    face = f'<circle cy="-680" r="70" fill="#f4efe2" stroke="#c9a24a" stroke-width="8"/><path d="M0,-680 L0,-720" stroke="#111" stroke-width="7" transform="rotate({(hh%12)*30+mm*0.5} 0 -680)"/><path d="M0,-680 L0,-740" stroke="#111" stroke-width="4" transform="rotate({mm*6} 0 -680)"/>'
    pend = '<g class="a-sway" data-o="0 -600" data-a="14" data-p="1"><path d="M0,-600 V-260" stroke="#c9a24a" stroke-width="6"/><circle cy="-250" r="34" fill="#c9a24a"/></g>'
    return _g(f'<rect x="-110" y="-800" width="220" height="800" rx="20" fill="#5a3a22" stroke="#2a1a10" stroke-width="6"/><rect x="-80" y="-580" width="160" height="440" rx="10" fill="#1a0f08"/>{pend}{face}', x, y, s)

def swinging_lamp(x=540, y=0, s=1.0):
    return _g('<g class="a-sway" data-o="0 0" data-a="8" data-p="2.2"><path d="M0,0 V260" stroke="#222" stroke-width="5"/><path d="M-70,320 L70,320 L36,260 L-36,260 Z" fill="#2a2a2a"/><polygon points="-70,320 70,320 360,1600 -360,1600" fill="#ffd27a" fill-opacity=".08"/><circle cy="322" r="14" fill="#ffe8a8"/></g>', x, y, s)

def rocking_chair(x=540, y=1540, s=1.0, color="#6b4a32"):
    return _g(f'<g class="a-sway" data-o="0 0" data-a="6" data-p="1.6"><path d="M-160,-10 Q0,30 160,-10" stroke="{color}" stroke-width="14" fill="none"/><rect x="-110" y="-230" width="200" height="24" fill="{color}"/><path d="M-100,-230 L-140,-560 M80,-230 L60,-560 M-120,-480 L70,-480 M-120,-400 L70,-400" stroke="{color}" stroke-width="16"/><path d="M-100,-206 L-130,-10 M80,-206 L110,-10" stroke="{color}" stroke-width="14"/></g>', x, y, s)

def ball(x=540, y=1540, color="#c4262e", s=1.0, moving=False):
    o = f'<g class="a-spin" data-o="0 -50" data-s="1.5"><circle cy="-50" r="50" fill="{color}" stroke="{LINE}" stroke-width="4"/><path d="M-50,-50 H50 M0,-100 V0" stroke="#fff" stroke-width="5"/></g>'
    return _moving(_g(o, x, y, s), x, moving, 6)

def passing_train(y=1320, s=1.0, color="#c9ccd4"):
    """a train crossing the far background (use behind people, e.g. on a platform)."""
    cars = "".join(f'<rect x="{k*560}" y="-300" width="540" height="270" rx="30" fill="{color}" stroke="{LINE}" stroke-width="6"/>' + "".join(f'<rect x="{k*560+30+j*120}" y="-260" width="90" height="80" rx="10" fill="#9fc6e8"/>' for j in range(4)) + f'<rect x="{k*560}" y="-140" width="540" height="20" fill="#c4262e"/>' for k in range(4))
    return f'<g class="a-drift" data-x0="1200" data-x1="-2400" data-p="5"><g transform="translate(0 {y}) scale({s})">{cars}</g></g>'

def flag(x=540, y=1380, color="#2f6bd8", s=1.0, text=""):
    t = f'<text x="110" y="-470" text-anchor="middle" font-family="Cairo" font-weight="900" font-size="40" fill="#fff" direction="rtl">{text}</text>' if text else ""
    return _g(f'<rect x="-8" y="-700" width="16" height="700" fill="#888"/><g class="a-sway" data-o="0 -560" data-a="5" data-p="0.9"><path d="M8,-690 Q100,-720 220,-680 L220,-440 Q100,-480 8,-450 Z" fill="{color}"/>{t}</g>', x, y, s)

def windmill(x=540, y=1380, s=1.0):
    blades = "".join(f'<g transform="rotate({k*90})"><path d="M0,-8 L250,-8 L250,-56 L40,-40 Z" fill="#f4f0e8" stroke="#8a7a5a" stroke-width="4"/><path d="M60,-10 V-44 M120,-10 V-48 M180,-10 V-52" stroke="#8a7a5a" stroke-width="3"/></g>' for k in range(4))
    return _g(f'<path d="M-60,0 L-30,-600 L30,-600 L60,0 Z" fill="#e8e2d0" stroke="#8a7a5a" stroke-width="5"/><g transform="translate(0 -620)"><g class="a-spin" data-o="0 0" data-s="0.25">{blades}</g><circle r="20" fill="#5a3a22"/></g>', x, y, s)

def washing_machine(x=540, y=1500, s=1.0, on=True):
    cls = ' class="a-spin" data-o="0 -190" data-s="2"' if on else ""
    return _g(f'<rect x="-140" y="-340" width="280" height="340" rx="16" fill="#eef2f6" stroke="#8592a8" stroke-width="5"/><rect x="-140" y="-340" width="280" height="60" fill="#d8dee6"/><circle cy="-170" r="96" fill="#9aa4b2"/><g{cls}><circle cy="-170" r="76" fill="#5a7a9a"/><path d="M-50,-170 h100" stroke="#fff" stroke-width="12"/></g>', x, y, s)

def record_player(x=540, y=1300, s=1.0, on=True):
    cls = ' class="a-spin" data-o="0 -50" data-s="0.6"' if on else ""
    return _g(f'<rect x="-160" y="-60" width="320" height="60" rx="8" fill="#5a3a22"/><g{cls}><ellipse cy="-62" rx="120" ry="30" fill="#111"/><ellipse cy="-62" rx="30" ry="8" fill="#c4262e"/></g><path d="M130,-90 L60,-60" stroke="#c9ccd4" stroke-width="8"/>', x, y, s)

def door_creak(x=40, y=700, s=1.0, color="#3a2a1e"):
    """a door that keeps swinging a little (anchor: top-left of the frame)."""
    return _g(f'<rect width="300" height="690" fill="#05070c" stroke="#2f4470" stroke-width="5"/><g class="a-sway" data-o="0 0" data-a="7" data-p="2.6"><path d="M0,0 L250,30 L250,670 L0,690 Z" fill="{color}" stroke="#111" stroke-width="4"/><circle cx="220" cy="360" r="10" fill="#c9a24a"/></g>', x, y, s)

def curtain_blow(x=640, y=290, w=340, h=560, color="#c9b8e8"):
    """curtains moving with the wind over a window (anchor: top-left of the window)."""
    return f'<g class="a-sway" data-o="{x} {y}" data-a="5" data-p="1.8"><path d="M{x},{y} L{x+w*0.35},{y} Q{x+w*0.25},{y+h*0.5} {x+w*0.4},{y+h} L{x},{y+h} Z" fill="{color}" opacity=".9"/></g><g class="a-sway" data-o="{x+w} {y}" data-a="-5" data-p="2.1"><path d="M{x+w},{y} L{x+w*0.65},{y} Q{x+w*0.75},{y+h*0.5} {x+w*0.6},{y+h} L{x+w},{y+h} Z" fill="{color}" opacity=".9"/></g>'

# =========================================================== animals
def cat(x=540, y=1540, color="#5a4a3a", s=1.0, flip=False, state="awake"):
    """state: awake · asleep · wet (dripping, small puddle) · arched (scared)."""
    eyes = '<g class="a-blink" data-p="3.1"><ellipse cx="-30" cy="-215" rx="9" ry="12" fill="#c9e84a"/><ellipse cx="10" cy="-215" rx="9" ry="12" fill="#c9e84a"/><ellipse cx="-30" cy="-215" rx="3" ry="10" fill="#111"/><ellipse cx="10" cy="-215" rx="3" ry="10" fill="#111"/></g>' if state != "asleep" else '<path d="M-40,-214 q10,6 20,0 M0,-214 q10,6 20,0" stroke="#111" stroke-width="4" fill="none"/>'
    body = f'<path d="M-60,0 Q-90,-120 -40,-170 L40,-170 Q80,-120 60,0 Z" fill="{color}" stroke="{LINE}" stroke-width="4"/>' if state != "arched" else f'<path d="M-90,0 Q-70,-200 0,-200 Q70,-200 90,0 Z" fill="{color}" stroke="{LINE}" stroke-width="4"/>'
    head = f'<circle cx="-10" cy="-205" r="58" fill="{color}" stroke="{LINE}" stroke-width="4"/><path d="M-60,-240 L-52,-300 L-20,-258 Z M0,-258 L32,-300 L40,-240 Z" fill="{color}" stroke="{LINE}" stroke-width="4"/><path d="M-14,-190 l4,6 l4,-6 Z" fill="#e88a9a"/><path d="M-30,-180 l-50,-4 M-30,-176 l-48,8 M10,-180 l50,-4 M10,-176 l48,8" stroke="#ddd" stroke-width="2"/>'
    tail = f'<g class="a-sway" data-o="55 -20" data-a="18" data-p="1.4"><path d="M55,-20 Q150,-40 130,-160" stroke="{color}" stroke-width="22" fill="none" stroke-linecap="round"/></g>'
    wet = '<g fill="#9fd0ff"><circle cx="-40" cy="-60" r="5"/><circle cx="30" cy="-100" r="5"/><circle cx="0" cy="-20" r="5"/></g><ellipse cy="6" rx="90" ry="10" fill="#7cc6ff" opacity=".45"/>' if state == "wet" else ""
    zz = '<text x="60" y="-280" font-size="40" fill="#dfeaff" font-family="sans-serif">z z</text>' if state == "asleep" else ""
    return _g(f'<g class="a-bob" data-d="3" data-p="2">{tail}{body}{head}{eyes}{wet}{zz}</g>', x, y, s, flip)

def dog(x=540, y=1540, breed="guard", s=1.0, flip=False, state="awake", asleep=None):
    """breed: guard (big, dark) · small (light) · saluki (thin, tall) · spotted. state: awake · asleep · barking · muddy."""
    if asleep: state = "asleep"
    col, sc = {"guard": ("#3a2a1e", 1.0), "small": ("#e8d0a8", 0.6), "saluki": ("#d8c09a", 0.9), "spotted": ("#f4f4f4", 0.85)}.get(breed, ("#7a5a3a", 1.0))
    if state == "asleep":
        o = f'<ellipse cy="-50" rx="150" ry="55" fill="{col}" stroke="{LINE}" stroke-width="4"/><circle cx="-130" cy="-70" r="50" fill="{col}" stroke="{LINE}" stroke-width="4"/><path d="M-150,-72 q12,8 24,0" stroke="#111" stroke-width="4" fill="none"/><path d="M-160,-110 l-20,-40 l40,14 Z" fill="#000" opacity=".4"/><text x="-60" y="-140" font-size="40" fill="#dfeaff" font-family="sans-serif">z z</text>'
        o += f'<g class="a-bob" data-d="4" data-p="2.4"><ellipse cy="-60" rx="140" ry="8" fill="none"/></g>'
    else:
        o = f'<g class="a-sway" data-o="120 -200" data-a="22" data-p="0.5"><path d="M120,-200 Q190,-260 200,-320" stroke="{col}" stroke-width="20" fill="none" stroke-linecap="round"/></g>'
        o += f'<rect x="-120" y="-260" width="260" height="120" rx="60" fill="{col}" stroke="{LINE}" stroke-width="4"/>'
        o += "".join(f'<rect x="{lx}" y="-170" width="30" height="170" rx="12" fill="{col}" stroke="{LINE}" stroke-width="4"/>' for lx in (-110, -60, 60, 100))
        o += f'<g class="a-bob" data-d="4" data-p="1.6"><circle cx="-150" cy="-300" r="62" fill="{col}" stroke="{LINE}" stroke-width="4"/><path d="M-196,-300 Q-210,-220 -170,-230" fill="{col}" stroke="{LINE}" stroke-width="4"/><ellipse cx="-206" cy="-286" rx="26" ry="20" fill="{col}" stroke="{LINE}" stroke-width="4"/><circle cx="-226" cy="-292" r="9" fill="#111"/><g class="a-blink" data-p="2.7"><circle cx="-160" cy="-318" r="8" fill="#111"/></g>'
        if state == "barking": o += '<path d="M-232,-268 q-20,10 -6,24" fill="#c4262e"/><path d="M-280,-330 l-30,-20 M-286,-300 l-36,0 M-280,-270 l-30,20" stroke="#fff" stroke-width="5"/>'
        o += '</g>'
        if breed == "spotted": o += '<g fill="#111"><circle cx="-40" cy="-220" r="18"/><circle cx="60" cy="-190" r="14"/><circle cx="-160" cy="-330" r="12"/></g>'
        if state == "muddy": o += '<g fill="#4a3018"><circle cx="-95" cy="-20" r="14"/><circle cx="75" cy="-20" r="14"/><circle cx="20" cy="-160" r="12"/></g>'
    return _g(o, x, y, s * sc, flip)

def bird(x=540, y=1200, kind="sparrow", s=1.0, flip=False, flying=False):
    """kind: sparrow · crow · parrot · pigeon · falcon · owl. flying=True flaps and crosses the frame."""
    col, wing, beak = {"sparrow": ("#8a6a42", "#5a4228", "#e8a33a"), "crow": ("#151515", "#2a2a2a", "#333"), "parrot": ("#3ab84a", "#c4262e", "#e8c34a"),
                       "pigeon": ("#8a96a8", "#6a7488", "#e88a5a"), "falcon": ("#8a6a42", "#4a3424", "#e8c34a"), "owl": ("#8a6a42", "#6a4a2a", "#e8a33a")}[kind]
    if kind == "owl":
        o = (f'<ellipse cy="-90" rx="70" ry="90" fill="{col}" stroke="{LINE}" stroke-width="4"/><path d="M-60,-170 l-6,-40 l30,22 Z M60,-170 l6,-40 l-30,22 Z" fill="{col}"/>'
             '<g class="a-blink" data-p="2.3"><circle cx="-28" cy="-130" r="24" fill="#f4e08a"/><circle cx="28" cy="-130" r="24" fill="#f4e08a"/><circle cx="-28" cy="-130" r="10" fill="#111"/><circle cx="28" cy="-130" r="10" fill="#111"/></g>'
             f'<path d="M-8,-110 l8,16 l8,-16 Z" fill="{beak}"/><path d="M-40,-40 q40,20 80,0" stroke="{wing}" stroke-width="6" fill="none"/>')
        return _g(f'<g class="a-bob" data-d="3" data-p="2.2">{o}</g>', x, y, s, flip)
    wing_svg = f'<g class="a-sway" data-o="0 -60" data-a="{40 if flying else 8}" data-p="{0.25 if flying else 2}"><path d="M0,-60 Q-60,-120 -110,-80 Q-60,-70 0,-50 Z" fill="{wing}"/></g>'
    body = f'<ellipse cy="-55" rx="70" ry="40" fill="{col}" stroke="{LINE}" stroke-width="4"/><circle cx="60" cy="-95" r="32" fill="{col}" stroke="{LINE}" stroke-width="4"/><path d="M88,-98 l30,8 l-30,8 Z" fill="{beak}"/><g class="a-blink" data-p="3.3"><circle cx="70" cy="-104" r="6" fill="#111"/></g><path d="M-60,-50 l-50,-14 l4,24 Z" fill="{wing}"/>'
    legs = '' if flying else '<path d="M-10,-18 v18 M20,-18 v18" stroke="#e8a33a" stroke-width="5"/>'
    if kind == "parrot": body += '<path d="M-60,-40 l-60,40 l20,6 Z" fill="#2f6bd8"/>'
    o = f'<g class="a-bob" data-d="{8 if flying else 2}" data-p="{0.5 if flying else 1.2}">{legs}{body}{wing_svg}</g>'
    g = _g(o, x, y, s, flip)
    return f'<g class="a-drift" data-x0="{1300-x}" data-x1="{-300-x}" data-p="6">{g}</g>' if flying else g

def horse(x=540, y=1540, color="#6b4228", s=1.0, flip=False):
    o = (f'<g class="a-sway" data-o="230 -560" data-a="10" data-p="1.8"><path d="M230,-560 Q300,-500 280,-330" stroke="#2a1a10" stroke-width="26" fill="none"/></g>'
         f'<ellipse cy="-560" rx="250" ry="130" fill="{color}" stroke="{LINE}" stroke-width="5"/>'
         + "".join(f'<rect x="{lx}" y="-480" width="44" height="480" rx="16" fill="{color}" stroke="{LINE}" stroke-width="5"/><rect x="{lx}" y="-30" width="44" height="30" fill="#222"/>' for lx in (-200, -130, 120, 180))
         + f'<path d="M-200,-620 L-300,-860 L-210,-900 L-130,-640 Z" fill="{color}" stroke="{LINE}" stroke-width="5"/><g class="a-bob" data-d="6" data-p="1.7"><path d="M-300,-860 L-420,-780 L-400,-730 L-260,-800 Z" fill="{color}" stroke="{LINE}" stroke-width="5"/><g class="a-blink" data-p="3"><circle cx="-300" cy="-830" r="8" fill="#111"/></g><path d="M-280,-900 l-10,-40 l26,30 Z" fill="{color}"/></g>'
         f'<path d="M-260,-880 Q-200,-760 -140,-640" stroke="#2a1a10" stroke-width="20" fill="none"/>')
    return _g(o, x, y, s * 0.8, flip)

def camel(x=540, y=1540, s=1.0, flip=False, sitting=False):
    col = "#c9a26a"
    if sitting:
        o = f'<ellipse cy="-150" rx="260" ry="150" fill="{col}" stroke="{LINE}" stroke-width="5"/><path d="M-60,-280 Q0,-420 60,-280 Z" fill="{col}" stroke="{LINE}" stroke-width="5"/>'
    else:
        o = "".join(f'<rect x="{lx}" y="-520" width="40" height="520" rx="14" fill="{col}" stroke="{LINE}" stroke-width="5"/>' for lx in (-190, -120, 110, 170))
        o += f'<ellipse cy="-600" rx="250" ry="130" fill="{col}" stroke="{LINE}" stroke-width="5"/><path d="M-60,-710 Q0,-860 70,-710 Z" fill="{col}" stroke="{LINE}" stroke-width="5"/>'
    base = -150 if sitting else -600
    o += f'<path d="M-230,{base} Q-330,{base-60} -330,{base-260}" stroke="{col}" stroke-width="60" fill="none" stroke-linecap="round"/><g class="a-bob" data-d="5" data-p="2"><ellipse cx="-370" cy="{base-280}" rx="80" ry="44" fill="{col}" stroke="{LINE}" stroke-width="5"/><g class="a-blink" data-p="3.5"><circle cx="-380" cy="{base-296}" r="8" fill="#111"/></g><path d="M-440,{base-270} l-10,6" stroke="#111" stroke-width="5"/></g>'
    o += f'<g class="a-sway" data-o="240 {base}" data-a="8" data-p="2"><path d="M240,{base} q30,60 10,140" stroke="#8a6a3a" stroke-width="14" fill="none"/></g>'
    return _g(o, x, y, s * 0.75, flip)

def fish_tank(x=540, y=1300, s=1.0):
    """anchor: bottom-centre on a table/cabinet."""
    fish = "".join(f'<g class="a-drift" data-x0="{-150+k*60}" data-x1="{150-k*40}" data-p="{4+k}"><g transform="translate(0 {-180+k*50})"><ellipse rx="26" ry="14" fill="{c}"/><path d="M22,0 l20,-12 v24 Z" fill="{c}"/><circle cx="-12" cy="-3" r="3" fill="#111"/></g></g>' for k, c in enumerate(("#ff8a2a", "#e8c34a", "#ff3b8a")))
    return _g(f'<defs><clipPath id="tankclip"><rect x="-200" y="-300" width="400" height="290"/></clipPath></defs><rect x="-210" y="-310" width="420" height="310" rx="10" fill="#5ab8e8" fill-opacity=".35" stroke="#9fd3ff" stroke-width="6"/><g clip-path="url(#tankclip)">{fish}<path d="M-120,-10 q10,-80 0,-140 M100,-10 q-14,-60 6,-110" stroke="#3a8a4a" stroke-width="10" fill="none"/></g><rect x="-210" y="-20" width="420" height="20" fill="#c9a26a"/>', x, y, s)

def mouse(x=540, y=1540, s=1.0, flip=False):
    return _g('<g class="a-bob" data-d="2" data-p=".4"><ellipse cy="-30" rx="50" ry="30" fill="#9a9a9a" stroke="#111" stroke-width="3"/><circle cx="-50" cy="-40" r="22" fill="#9a9a9a" stroke="#111" stroke-width="3"/><circle cx="-44" cy="-64" r="14" fill="#e8b0b0"/><circle cx="-64" cy="-42" r="4" fill="#111"/><path d="M50,-26 Q110,-20 120,-60" stroke="#c99" stroke-width="5" fill="none"/></g>', x, y, s, flip)

def snake(x=540, y=1540, color="#5a8a3a", s=1.0, flip=False):
    return _g(f'<ellipse cy="-30" rx="130" ry="34" fill="{color}" stroke="{LINE}" stroke-width="4"/><ellipse cy="-70" rx="96" ry="28" fill="{color}" stroke="{LINE}" stroke-width="4"/><g class="a-sway" data-o="-40 -90" data-a="10" data-p="1.4"><path d="M-40,-90 Q-80,-200 -20,-230" stroke="{color}" stroke-width="40" fill="none" stroke-linecap="round"/><circle cx="-10" cy="-238" r="6" fill="#111"/><g class="a-blink" data-p=".9"><path d="M-2,-226 l30,4 l8,-8 M28,-222 l8,6" stroke="#c4262e" stroke-width="4" fill="none"/></g></g>', x, y, s, flip)

def goat(x=540, y=1540, color="#f4f0e8", s=1.0, flip=False, sheep=False):
    if sheep:
        body = "".join(f'<circle cx="{cx}" cy="{cy}" r="50" fill="#f4f0e8" stroke="#bbb" stroke-width="3"/>' for cx, cy in ((-90, -220), (-30, -250), (40, -250), (100, -220), (-60, -180), (60, -180), (0, -200)))
        head = '<ellipse cx="-160" cy="-250" rx="44" ry="56" fill="#3a3a3a"/>'
    else:
        body = f'<ellipse cy="-220" rx="150" ry="80" fill="{color}" stroke="{LINE}" stroke-width="4"/>'
        head = f'<ellipse cx="-170" cy="-290" rx="40" ry="56" fill="{color}" stroke="{LINE}" stroke-width="4"/><path d="M-170,-340 q-10,-50 30,-70 M-150,-340 q20,-40 50,-50" stroke="#8a7a5a" stroke-width="8" fill="none"/><path d="M-180,-240 q4,40 14,50" stroke="{color}" stroke-width="16"/>'
    legs = "".join(f'<rect x="{lx}" y="-170" width="24" height="170" fill="#3a3a3a"/>' for lx in (-110, -60, 60, 100))
    return _g(f'{legs}{body}<g class="a-bob" data-d="4" data-p="1.8">{head}<g class="a-blink" data-p="2.9"><circle cx="-180" cy="-300" r="6" fill="#111"/></g></g>', x, y, s * 0.8, flip)

def chicken(x=540, y=1540, s=1.0, flip=False):
    return _g('<g class="a-bob" data-d="6" data-p=".7"><ellipse cy="-90" rx="70" ry="60" fill="#f4f0e8" stroke="#111" stroke-width="3"/><circle cx="-60" cy="-160" r="34" fill="#f4f0e8" stroke="#111" stroke-width="3"/><path d="M-80,-196 q10,-20 20,0 q10,-20 20,0" fill="#c4262e"/><path d="M-94,-158 l-22,6 l22,6 Z" fill="#e8a33a"/><circle cx="-66" cy="-166" r="5" fill="#111"/><path d="M60,-110 l40,-40 l6,50 Z" fill="#e8e2d0"/></g><path d="M-20,-30 v30 M20,-30 v30" stroke="#e8a33a" stroke-width="6"/>', x, y, s, flip)

def rabbit(x=540, y=1540, color="#e8e2d8", s=1.0, flip=False):
    return _g(f'<g class="a-bob" data-d="3" data-p="1"><ellipse cy="-70" rx="80" ry="64" fill="{color}" stroke="#111" stroke-width="3"/><circle cx="-60" cy="-130" r="40" fill="{color}" stroke="#111" stroke-width="3"/><g class="a-sway" data-o="-60 -160" data-a="10" data-p="1.6"><ellipse cx="-74" cy="-220" rx="14" ry="56" fill="{color}" stroke="#111" stroke-width="3"/><ellipse cx="-44" cy="-214" rx="14" ry="56" fill="{color}" stroke="#111" stroke-width="3"/></g><circle cx="-76" cy="-134" r="5" fill="#111"/><circle cx="80" cy="-60" r="18" fill="#fff"/></g>', x, y, s, flip)

def turtle(x=540, y=1540, s=1.0, flip=False):
    return _g('<g class="a-drift" data-x0="0" data-x1="-80" data-p="20"><ellipse cy="-40" rx="110" ry="60" fill="#5a7a3a" stroke="#111" stroke-width="4"/><path d="M-60,-60 l40,-30 l40,0 l40,30 M-80,-30 h160" stroke="#3a5a2a" stroke-width="5" fill="none"/><g class="a-bob" data-d="4" data-p="2"><ellipse cx="-130" cy="-40" rx="34" ry="24" fill="#8a9a5a" stroke="#111" stroke-width="3"/><circle cx="-146" cy="-46" r="4" fill="#111"/></g></g>', x, y, s, flip)

def bat(x=540, y=300, s=1.0, hanging=True):
    if hanging:
        return _g('<path d="M0,0 v20" stroke="#222" stroke-width="4"/><g class="a-sway" data-o="0 0" data-a="4" data-p="2.5"><path d="M-40,20 Q0,120 40,20 Q20,40 0,30 Q-20,40 -40,20 Z" fill="#1a1a1a"/><circle cx="0" cy="110" r="22" fill="#1a1a1a"/><circle cx="-8" cy="112" r="3" fill="#ff3b3b"/><circle cx="8" cy="112" r="3" fill="#ff3b3b"/></g>', x, y, s)
    g = _g('<circle r="18" fill="#111"/><g class="a-sway" data-o="0 0" data-a="30" data-p=".25"><path d="M0,0 Q-50,-40 -90,0 Q-70,-6 -60,10 Q-40,0 -30,14 Q-10,4 0,0 Z" fill="#111"/></g><g class="a-sway" data-o="0 0" data-a="-30" data-p=".25"><path d="M0,0 Q50,-40 90,0 Q70,-6 60,10 Q40,0 30,14 Q10,4 0,0 Z" fill="#111"/></g>', x, y, s)
    return f'<g class="a-drift" data-x0="{-200-x}" data-x1="{1300-x}" data-p="5">{g}</g>'

def butterfly(x=540, y=900, s=1.0, color="#ff8a2a"):
    g = _g(f'<g class="a-sway" data-o="0 0" data-a="35" data-p=".3"><path d="M0,0 Q-50,-60 -60,-10 Q-50,30 0,0 Z" fill="{color}"/></g><g class="a-sway" data-o="0 0" data-a="-35" data-p=".3"><path d="M0,0 Q50,-60 60,-10 Q50,30 0,0 Z" fill="{color}"/></g><rect x="-3" y="-20" width="6" height="40" fill="#222"/>', x, y, s)
    return f'<g class="a-bob" data-d="30" data-p="1.5">{g}</g>'

# =========================================================== plants
def tree(x=540, y=1380, kind="round", s=1.0, color=None):
    """kind: round · pine · palm · olive · dead · birch · cypress. Leaves sway."""
    c = color or {"round": "#2f6a32", "pine": "#1f4a2a", "olive": "#6a8a5a", "birch": "#5a9a4a", "cypress": "#1f4a2a"}.get(kind, "#2f6a32")
    if kind == "palm":
        fr = "".join(f'<path d="M0,-560 q{dx},-70 {dx*2},{dy}" stroke="#2f7a2a" stroke-width="26" fill="none" stroke-linecap="round"/>' for dx, dy in ((-110, 50), (110, 50), (-70, -20), (80, -30), (0, -80), (-130, 110), (130, 110)))
        return _g(f'<path d="M0,0 q-30,-280 0,-560" stroke="#8a6a3a" stroke-width="34" fill="none"/><g class="a-sway" data-o="0 -560" data-a="4" data-p="3">{fr}<circle cx="-10" cy="-540" r="14" fill="#5a3a1a"/><circle cx="12" cy="-536" r="14" fill="#5a3a1a"/></g>', x, y, s)
    if kind == "dead":
        return _g('<path d="M0,0 L-10,-300 L-80,-460 M-10,-300 L40,-420 L110,-480 M40,-420 L30,-520 M-50,-390 L-120,-400" stroke="#4a3424" stroke-width="22" fill="none" stroke-linecap="round"/>', x, y, s)
    if kind == "pine":
        return _g(f'<rect x="-14" y="-90" width="28" height="90" fill="#4a2f1f"/><g class="a-sway" data-o="0 -90" data-a="2" data-p="3.4">' + "".join(f'<path d="M0,{-240-k*130} L{150-k*30},{-90-k*130} L{-150+k*30},{-90-k*130} Z" fill="{c}"/>' for k in range(4)) + '</g>', x, y, s)
    if kind == "cypress":
        return _g(f'<rect x="-12" y="-60" width="24" height="60" fill="#4a2f1f"/><g class="a-sway" data-o="0 -60" data-a="2" data-p="3"><path d="M0,-700 Q90,-400 60,-60 L-60,-60 Q-90,-400 0,-700 Z" fill="{c}"/></g>', x, y, s)
    trunk = "#d8d8d0" if kind == "birch" else "#5a3a22"
    marks = '<path d="M-10,-80 h14 M4,-160 h12 M-12,-240 h16" stroke="#222" stroke-width="5"/>' if kind == "birch" else ""
    blobs = ((-90, -380, 110), (90, -370, 110), (0, -470, 130), (-40, -300, 90), (60, -300, 90)) if kind != "olive" else ((-110, -340, 80), (100, -340, 80), (0, -420, 100), (-50, -290, 70), (60, -280, 70))
    leaves = "".join(f'<circle cx="{bx}" cy="{by}" r="{r}" fill="{c}"/>' for bx, by, r in blobs)
    if kind == "olive": leaves += "".join(f'<circle cx="{-80+k*40}" cy="{-380+(k%3)*40}" r="7" fill="#3a3a2a"/>' for k in range(5))
    return _g(f'<path d="M-20,0 Q-10,-150 -30,-300 L30,-300 Q10,-150 20,0 Z" fill="{trunk}"/>{marks}<g class="a-sway" data-o="0 -300" data-a="2.5" data-p="3.2">{leaves}</g>', x, y, s)

def cactus(x=540, y=1380, s=1.0, flower=False):
    o = '<path d="M-40,0 V-420 Q0,-470 40,-420 V0 Z" fill="#3a7a3a" stroke="#1f4a1f" stroke-width="5"/><path d="M-40,-220 H-110 V-340 Q-80,-370 -70,-330 V-260 H-40" fill="#3a7a3a" stroke="#1f4a1f" stroke-width="5"/><path d="M40,-160 H100 V-300 Q130,-320 140,-290 V-200 H40" fill="#3a7a3a" stroke="#1f4a1f" stroke-width="5"/>'
    o += "".join(f'<path d="M{-30+(k%3)*30},{-60-k*40} l-8,-6 M{-30+(k%3)*30},{-60-k*40} l8,-6" stroke="#e8e2c0" stroke-width="2"/>' for k in range(9))
    if flower: o += '<circle cy="-440" r="20" fill="#ff5a8a"/>'
    return _g(o, x, y, s)

def flowers(x=540, y=1540, s=1.0, color="#ff5a8a", wilted=False):
    """a small flower bed / bunch on the ground. wilted -> drooping, brown."""
    out = ""
    for k in range(7):
        fx = -150 + k * 50; h = 120 + (k * 37) % 70
        if wilted:
            out += f'<path d="M{fx},0 Q{fx+10},{-h*0.6} {fx+40},{-h*0.5}" stroke="#7a7a3a" stroke-width="6" fill="none"/><circle cx="{fx+42}" cy="{-h*0.45}" r="12" fill="#8a6a4a"/>'
        else:
            out += f'<path d="M{fx},0 V{-h}" stroke="#3a7a3a" stroke-width="6"/>' + "".join(f'<circle cx="{fx+14*math.cos(j*1.256):.0f}" cy="{-h+14*math.sin(j*1.256):.0f}" r="10" fill="{color if k%2 else "#ffd21f"}"/>' for j in range(5)) + f'<circle cx="{fx}" cy="{-h}" r="7" fill="#e8a33a"/>'
    cls = '' if wilted else ' class="a-sway" data-o="0 0" data-a="3" data-p="2.2"'
    return _g(f'<g{cls}>{out}</g>', x, y, s)

def bush(x=540, y=1540, s=1.0, color="#3a6a32", berries=False):
    o = "".join(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}"/>' for cx, cy, r in ((-110, -70, 80), (0, -110, 100), (110, -70, 80), (-50, -50, 70), (60, -50, 70)))
    if berries: o += "".join(f'<circle cx="{-120+k*40}" cy="{-80-(k*31)%80}" r="9" fill="#c4262e"/>' for k in range(7))
    return _g(f'<g class="a-sway" data-o="0 0" data-a="1.5" data-p="2.6">{o}</g>', x, y, s)

def tall_grass(x=540, y=1540, s=1.0, color="#6a8a3a", w=400):
    blades = "".join(f'<path d="M{-w/2+k*14},0 q{6-(k%3)*6},-80 {(k%5)-2},-{140+(k*29)%80}" stroke="{color}" stroke-width="6" fill="none"/>' for k in range(int(w / 14)))
    return _g(f'<g class="a-sway" data-o="0 0" data-a="4" data-p="1.8">{blades}</g>', x, y, s)

def potted(x=540, y=1500, kind="monstera", s=1.0, wet=False, wilted=False):
    """house plants. kind: monstera · ficus · succulent · bonsai · bamboo · sunflower · rose · hanging (anchor: ceiling point)."""
    pot = f'<path d="M-70,-140 L70,-140 L54,0 L-54,0 Z" fill="#b5543a" stroke="#5a2a1a" stroke-width="4"/><ellipse cy="-140" rx="68" ry="12" fill="{"#2a1a10" if wet else "#8a6a48"}"/>' + ('<ellipse cy="6" rx="70" ry="8" fill="#7cc6ff" opacity=".35"/>' if wet else "")
    g = "#8a8a4a" if wilted else "#2f7a3a"
    if kind == "hanging":
        vines = "".join(f'<path d="M{-40+k*20},40 q{10-(k%2)*20},120 {(k%3)*10-10},{180+(k*23)%80}" stroke="{g}" stroke-width="10" fill="none"/>' for k in range(5))
        return _g(f'<path d="M0,0 V-200 M-60,-60 L0,-200 L60,-60" stroke="#8a7a5a" stroke-width="3" fill="none" transform="scale(1 -1)"/><path d="M-60,0 h120 l-20,60 h-80 Z" fill="#e8e2d0"/><g class="a-sway" data-o="0 40" data-a="4" data-p="2.5">{vines}</g>', x, y, s)
    if kind == "monstera":
        top = "".join(f'<g transform="rotate({a} 0 -140)"><path d="M0,-140 Q-10,-260 0,-360" stroke="{g}" stroke-width="6" fill="none"/><ellipse cx="0" cy="-380" rx="60" ry="46" fill="{g}"/><path d="M-30,-380 h20 M10,-370 h22" stroke="#1f4a1f" stroke-width="6"/></g>' for a in ((-40, 0, 40) if not wilted else (-70, 60)))
    elif kind == "ficus":
        top = f'<path d="M0,-140 V-380" stroke="#5a3a22" stroke-width="12"/>' + "".join(f'<ellipse cx="{(k*47)%160-80}" cy="{-260-(k*37)%170}" rx="18" ry="11" fill="{g}" transform="rotate({k*40} {(k*47)%160-80} {-260-(k*37)%170})"/>' for k in range(26 if not wilted else 8))
    elif kind == "succulent":
        top = "".join(f'<ellipse cx="0" cy="-170" rx="14" ry="44" fill="#6a9a7a" transform="rotate({k*45} 0 -150)"/>' for k in range(8))
    elif kind == "bonsai":
        top = f'<path d="M0,-140 Q-40,-200 20,-240 Q60,-270 30,-300" stroke="#5a3a22" stroke-width="14" fill="none"/>' + "".join(f'<ellipse cx="{cx}" cy="{cy}" rx="60" ry="28" fill="{g}"/>' for cx, cy in ((-40, -230), (50, -300), (10, -260)))
    elif kind == "bamboo":
        top = "".join(f'<path d="M{dx},-140 V{-480+dx}" stroke="#7aa84a" stroke-width="14"/>' + "".join(f'<path d="M{dx-8},{-200-j*80} h16" stroke="#4a7a2a" stroke-width="4"/>' for j in range(4)) for dx in (-30, 0, 30))
    elif kind == "sunflower":
        top = f'<path d="M0,-140 V-460" stroke="{g}" stroke-width="10"/><g transform="translate(0 -470)">' + "".join(f'<ellipse cx="{40*math.cos(k*0.524):.0f}" cy="{40*math.sin(k*0.524):.0f}" rx="22" ry="10" fill="{"#ffd21f" if not wilted else "#8a6a2a"}" transform="rotate({k*30} {40*math.cos(k*0.524):.0f} {40*math.sin(k*0.524):.0f})"/>' for k in range(12)) + '<circle r="30" fill="#5a3a1a"/></g>'
    else:  # rose
        top = "".join(f'<path d="M{dx},-140 V{-300-abs(dx)}" stroke="{g}" stroke-width="6"/><circle cx="{dx}" cy="{-310-abs(dx)}" r="20" fill="{"#c4262e" if not wilted else "#6a3a2a"}"/>' for dx in (-30, 0, 30))
    cls = '' if wilted else ' class="a-sway" data-o="0 -140" data-a="2" data-p="2.8"'
    return _g(f'<g{cls}>{top}</g>{pot}', x, y, s)

def ivy(x=0, y=0, w=400, h=700, s=1.0):
    """ivy climbing a wall from (x,y) top-left."""
    leaves = "".join(f'<path d="M{(k*53)%w},{(k*97)%h} q8,-14 16,0 q-8,14 -16,0 Z" fill="#2f6a32"/>' for k in range(60))
    return _g(f'<path d="M{w*0.3},{h} Q{w*0.5},{h*0.5} {w*0.2},0 M{w*0.7},{h} Q{w*0.9},{h*0.4} {w*0.6},0" stroke="#3a4a2a" stroke-width="6" fill="none"/>{leaves}', x, y, s)

def mushrooms(x=540, y=1540, s=1.0, color="#c4262e"):
    return _g("".join(f'<rect x="{dx-8}" y="{-h}" width="16" height="{h}" fill="#f4efe2"/><path d="M{dx-40},{-h} Q{dx},{-h-60} {dx+40},{-h} Z" fill="{color}"/><circle cx="{dx-10}" cy="{-h-20}" r="6" fill="#fff"/>' for dx, h in ((-50, 60), (10, 90), (60, 50))), x, y, s)

# =========================================================== atmospheres (full-frame overlays, last layer of the scene)
def atmosphere(kind, x=540, y=900):
    """fog · sandstorm · wind_leaves · smoke · sunset · dawn · blackout (x,y = candle/torch light) · police_lights · moonbeam · storm · heat · dust"""
    if kind == "fog":
        return "".join(f'<g class="a-drift" data-x0="{-200+k*80}" data-x1="{200-k*60}" data-p="{12+k*3}"><ellipse cx="{(k*263)%1080}" cy="{1100+(k*137)%600}" rx="520" ry="110" fill="#dfe8f0" opacity=".22"/></g>' for k in range(8)) + '<rect width="1080" height="1920" fill="#c8d4dc" opacity=".18"/>'
    if kind == "sandstorm":
        dots = "".join(f'<circle cx="{(k*67)%1080}" cy="{(k*131)%1920}" r="{2+(k%3)}" fill="#e8c88a"/>' for k in range(160))
        return f'<rect width="1080" height="1920" fill="#c99a5a" opacity=".35"/><g class="a-drift" data-x0="-200" data-x1="200" data-p="1.2">{dots}</g><g class="a-drift" data-x0="100" data-x1="-300" data-p="2.5"><ellipse cx="540" cy="900" rx="700" ry="300" fill="#b8884a" opacity=".2"/></g>'
    if kind == "wind_leaves":
        return "".join(f'<g class="a-drift" data-x0="{1200}" data-x1="{-300}" data-p="{3+(k%4)}"><g class="a-spin" data-o="{(k*97)%1080} {(k*173)%1600+100}" data-s=".8"><path d="M{(k*97)%1080},{(k*173)%1600+100} q14,-18 28,0 q-14,18 -28,0 Z" fill="{["#c97a2a","#a8642a","#e8a33a"][k%3]}"/></g></g>' for k in range(18))
    if kind == "smoke":
        return "".join(f'<g class="a-fall" data-h="-700" data-p="{4+k%3}"><circle cx="{x-60+(k*37)%120}" cy="{y+k*40}" r="{60+k*12}" fill="#8a8e96" opacity=".2"/></g>' for k in range(7))
    if kind == "sunset":
        return '<defs><linearGradient id="atm_sunset" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ff7a3a" stop-opacity=".35"/><stop offset="1" stop-color="#5a1e4a" stop-opacity=".25"/></linearGradient></defs><rect width="1080" height="1920" fill="url(#atm_sunset)"/>'
    if kind == "dawn":
        return '<defs><linearGradient id="atm_dawn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffb8c8" stop-opacity=".3"/><stop offset="1" stop-color="#9fc6e8" stop-opacity=".2"/></linearGradient></defs><rect width="1080" height="1920" fill="url(#atm_dawn)"/>'
    if kind == "blackout":
        return (f'<defs><radialGradient id="atm_bo" cx="{x/1080:.2f}" cy="{y/1920:.2f}" r=".45"><stop offset="0" stop-color="#000" stop-opacity="0"/><stop offset=".5" stop-color="#000" stop-opacity=".55"/><stop offset="1" stop-color="#000" stop-opacity=".88"/></radialGradient></defs>'
                f'<rect class="a-flicker" width="1080" height="1920" fill="url(#atm_bo)"/><circle class="a-flicker" cx="{x}" cy="{y}" r="200" fill="#ffb35c" fill-opacity=".12"/>')
    if kind == "police_lights":
        return '<rect class="a-flashA" width="1080" height="1920" fill="#ff2a2a" fill-opacity=".16"/><rect class="a-flashB" width="1080" height="1920" fill="#2a5aff" fill-opacity=".16"/>'
    if kind == "moonbeam":
        return f'<polygon points="{x-120},0 {x+120},0 {x+520},1920 {x+80},1920" fill="#cfe0ff" opacity=".12"/>' + "".join(f'<g class="a-fall" data-h="-200" data-p="{5+k}"><circle cx="{x+60+(k*41)%300}" cy="{400+(k*197)%1300}" r="3" fill="#fff" opacity=".5"/></g>' for k in range(14))
    if kind == "storm":
        return '<rect width="1080" height="1920" fill="#0a1020" opacity=".35"/><rect class="a-flashA" width="1080" height="1920" fill="#dbeaff" fill-opacity=".06"/>'
    if kind == "heat":
        return '<rect width="1080" height="1920" fill="#ffb35c" opacity=".12"/>' + "".join(f'<g class="a-bob" data-d="8" data-p="{0.8+k*0.2}"><path d="M0,{1300+k*40} q135,-12 270,0 t270,0 t270,0 t270,0" stroke="#fff" stroke-opacity=".08" stroke-width="10" fill="none"/></g>' for k in range(5))
    if kind == "dust":
        return "".join(f'<g class="a-bob" data-d="20" data-p="{3+k%4}"><circle cx="{(k*89)%1080}" cy="{(k*157)%1700+100}" r="3" fill="#fff3d0" opacity=".45"/></g>' for k in range(40))
    return ""

ATMOSPHERES = ["fog", "sandstorm", "wind_leaves", "smoke", "sunset", "dawn", "blackout", "police_lights", "moonbeam", "storm", "heat", "dust"]

THINGS = dict(vehicle=vehicle, motorcycle=motorcycle, bicycle=bicycle, shopping_cart=shopping_cart, wheelchair=wheelchair, suitcase=suitcase, stroller=stroller,
              ceiling_fan=ceiling_fan, desk_fan=desk_fan, pendulum_clock=pendulum_clock, swinging_lamp=swinging_lamp, rocking_chair=rocking_chair, ball=ball,
              passing_train=passing_train, flag=flag, windmill=windmill, washing_machine=washing_machine, record_player=record_player, door_creak=door_creak, curtain_blow=curtain_blow,
              cat=cat, dog=dog, bird=bird, horse=horse, camel=camel, fish_tank=fish_tank, mouse=mouse, snake=snake, goat=goat, chicken=chicken, rabbit=rabbit,
              turtle=turtle, bat=bat, butterfly=butterfly,
              tree=tree, cactus=cactus, flowers=flowers, bush=bush, tall_grass=tall_grass, potted=potted, ivy=ivy, mushrooms=mushrooms)
