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

# ---------------------------------------------------------------- parametric animals (one builder, many species)
def ch_animal(spec):
    c, c2 = spec["c"], spec.get("c2", "#ffffff"); ears = spec.get("ears", "round"); tail = spec.get("tail", "none"); pat = spec.get("pat", "")
    def f(i):
        s = ""
        tl = {"none": "", "curl": f'<path d="M0,0 C110,-10 140,-110 90,-150 C60,-170 40,-130 70,-120" stroke="{K}" stroke-width="40" fill="none" stroke-linecap="round"/><path d="M0,0 C110,-10 140,-110 90,-150" stroke="{c}" stroke-width="24" fill="none" stroke-linecap="round"/>',
              "long": f'<path d="M0,0 C120,-20 160,-140 120,-240" stroke="{K}" stroke-width="44" fill="none" stroke-linecap="round"/><path d="M0,0 C120,-20 160,-140 120,-240" stroke="{c}" stroke-width="26" fill="none" stroke-linecap="round"/>',
              "puff": f'<circle cx="40" cy="-20" r="60" fill="{c2}" {SW}/>', "fan": f'<path d="M0,0 L160,-140 L200,-40Z" fill="{c}" {SW}/>',
              "fin": f'<path d="M0,0 C80,-40 120,-140 200,-160 C170,-80 180,-30 220,20 C150,10 80,40 0,40Z" fill="{c}" {SW}/>'}[tail]
        s += f'<g id="tl{i}" transform="translate(180 140) rotate(0)">{tl}</g>'
        if spec.get("legs", True): s += "".join(f'<rect x="{x-38}" y="220" width="76" height="120" rx="34" fill="{c}" {SW}/>' for x in (-110, 110))
        body = f'<ellipse cx="0" cy="170" rx="{spec.get("bw", 200)}" ry="150" fill="{c}" {SW}/><ellipse cx="0" cy="200" rx="{spec.get("bw", 200)*.6:.0f}" ry="100" fill="{c2}"/>'
        if spec.get("wings"): body += f'<path d="M-190,120 C-320,40 -300,240 -170,230Z M190,120 C320,40 300,240 170,230Z" fill="{spec.get("wc", c)}" {SW}/>'
        s += body
        if spec.get("neck"): s += f'<rect x="-75" y="-330" width="150" height="460" rx="60" fill="{c}" {SW}/>' + "".join(f'<circle cx="{x}" cy="{y}" r="24" fill="{spec.get("pc", "#c96a1a")}"/>' for x, y in ((-30, -200), (30, -80), (-20, 40))) + '<g transform="translate(0 -330)">'
        lift_end = "</g>" if spec.get("neck") else ""
        er = {"round": lambda sx: f'<circle cx="{sx*170}" cy="-210" r="70" fill="{c}" {SW}/><circle cx="{sx*170}" cy="-210" r="38" fill="{c2}"/>',
              "cat": lambda sx: f'<path d="M{sx*210},-180 L{sx*170},-330 L{sx*60},-230Z" fill="{c}" {SW}/>',
              "long": lambda sx: f'<ellipse cx="{sx*90}" cy="-330" rx="50" ry="150" fill="{c}" {SW}/><ellipse cx="{sx*90}" cy="-320" rx="24" ry="110" fill="#ffc2c2"/>',
              "floppy": lambda sx: f'<ellipse cx="{sx*230}" cy="-60" rx="60" ry="140" fill="{spec.get("ec", c)}" {SW} transform="rotate({-sx*20} {sx*230} -60)"/>',
              "horn": lambda sx: f'<path d="M{sx*120},-200 Q{sx*190},-330 {sx*110},-360 Q{sx*120},-280 {sx*60},-220Z" fill="#f4e3b0" {SW}/>',
              "big": lambda sx: f'<ellipse cx="{sx*250}" cy="-70" rx="130" ry="170" fill="{c}" {SW}/><ellipse cx="{sx*250}" cy="-70" rx="80" ry="120" fill="#ffc2c2"/>',
              "tuft": lambda sx: f'<path d="M{sx*150},-210 L{sx*200},-320 L{sx*80},-240Z" fill="{c}" {SW}/>',
              "none": lambda sx: ""}[ears]
        s += er(-1) + er(1)
        if spec.get("bwings"): s += "".join(f'<ellipse cx="{sx*190}" cy="{dy}" rx="170" ry="{r_}" fill="{spec["bwings"]}" {SW} transform="rotate({sx*20} {sx*190} {dy})"/>' for sx in (-1, 1) for dy, r_ in ((-120, 200), (160, 130)))
        if spec.get("shell"): s += f'<path d="M-260,220 A260,260 0 0,1 260,220Z" fill="{spec["shell"]}" {SW}/>' + "".join(f'<path d="M{x},220 Q{x+40},40 {x+90},220" stroke="{K}" stroke-width="6" fill="none"/>' for x in (-200, -80, 40))
        if spec.get("wool"): s += "".join(f'<circle cx="{x}" cy="{y}" r="{r_}" fill="{spec["wool"]}" {SW}/>' for x, y, r_ in ((-200, 120, 110), (0, 90, 130), (200, 120, 110), (-110, 260, 110), (110, 260, 110), (-150, -220, 70), (0, -270, 80), (150, -220, 70)))
        if spec.get("mane"): s += f'<circle cx="0" cy="-60" r="300" fill="{spec["mane"]}" {SW}/>'
        s += f'<ellipse cx="0" cy="-60" rx="{spec.get("hw", 240)}" ry="{spec.get("hh", 200)}" fill="{c}" stroke="{K}" stroke-width="12"/>'
        if pat == "spots": s += "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{spec.get("pc", "#151515")}" opacity=".85"/>' for x, y, r in ((-150, -140, 30), (140, -10, 26), (-170, 30, 20), (120, -170, 22)))
        if pat == "stripes": s += "".join(f'<path d="M{x},-255 l{d},70" stroke="{spec.get("pc", "#151515")}" stroke-width="18" stroke-linecap="round"/>' for x, d in ((-60, 20), (0, 0), (60, -20)))
        if pat == "mask": s += f'<ellipse cx="-90" cy="-60" rx="70" ry="60" fill="{spec.get("pc", "#151515")}"/><ellipse cx="90" cy="-60" rx="70" ry="60" fill="{spec.get("pc", "#151515")}"/>'
        if pat == "comb": s += f'<path d="M-60,-250 q30,-90 60,-10 q30,-90 60,0 q30,-80 50,10Z" fill="#e5322d" {SW}/>'
        mz = spec.get("muzzle", "small")
        if mz == "small": s += f'<ellipse cx="0" cy="20" rx="80" ry="55" fill="{c2}"/><path d="M-20,-10 h40 l-20,24z" fill="{spec.get("nc", "#ff6a8a")}"/>'
        if mz == "big": s += f'<ellipse cx="0" cy="40" rx="130" ry="80" fill="{c2}" {SW}/><ellipse cx="0" cy="10" rx="36" ry="24" fill="{K}"/>'
        if mz == "beak": s += f'<path d="M-50,0 L0,70 L50,0 Q0,-30 -50,0Z" fill="#ff9a3a" {SW}/>'
        if mz == "snout": s += f'<ellipse cx="0" cy="30" rx="80" ry="58" fill="{spec.get("nc", "#ffb3c6")}" {SW}/><circle cx="-26" cy="30" r="12" fill="{K}"/><circle cx="26" cy="30" r="12" fill="{K}"/>'
        if mz == "trunk": s += f'<path d="M-40,0 C-40,160 40,220 90,200 C60,180 40,140 40,0Z" fill="{c}" {SW}/>'
        s += eyes(i, (-90, 90), -90, spec.get("er", 40)) + (f'<path id="mo{i}" d="M-40,90 Q0,140 40,90" fill="#e85a6a" {SW}/>' if mz != "beak" else f'<path id="mo{i}" d="M-30,70 Q0,100 30,70" fill="#e85a6a" stroke="{K}" stroke-width="6"/>')
        if spec.get("whisk"): s += f'<path d="M-100,30 h-140 M-100,50 l-130,30 M100,30 h140 M100,50 l130,30" stroke="{K}" stroke-width="6"/>'
        if spec.get("glasses"): s += f'<circle cx="-90" cy="-90" r="60" fill="none" stroke="{K}" stroke-width="10"/><circle cx="90" cy="-90" r="60" fill="none" stroke="{K}" stroke-width="10"/><path d="M-30,-90 H30" stroke="{K}" stroke-width="10"/>'
        if spec.get("antenna"): s += f'<path d="M-60,-240 Q-100,-380 -160,-400 M60,-240 Q100,-380 160,-400" stroke="{K}" stroke-width="12" fill="none"/><circle cx="-160" cy="-400" r="22" fill="{K}"/><circle cx="160" cy="-400" r="22" fill="{K}"/>'
        if spec.get("unihorn"): s += f'<path d="M-30,-250 L0,-460 L30,-250Z" fill="#ffd21f" {SW}/>'
        if spec.get("hat"): s += f'<path d="M-150,-230 H150 L120,-260 H-120Z M-90,-260 V-380 H90 V-260Z" fill="{spec["hat"]}" {SW}/>'
        return s + lift_end
    return f
ANIMALS = {
 "dog": dict(c="#c98f45", c2="#f4e3c4", ears="floppy", ec="#8a5a33", tail="curl", muzzle="big"),
 "puppy": dict(c="#f4e3c4", c2="#fff", ears="floppy", ec="#c98f45", tail="curl", muzzle="big", pat="spots", pc="#c98f45"),
 "rabbit": dict(c="#f2f2f2", c2="#ffd9e0", ears="long", tail="puff", muzzle="small", whisk=True),
 "bear": dict(c="#8a5a33", c2="#d9b48a", ears="round", muzzle="big"),
 "panda": dict(c="#fff", c2="#fff", ears="round", muzzle="big", pat="mask", pc="#151515"),
 "polar_bear": dict(c="#f4f8ff", c2="#fff", ears="round", muzzle="big"),
 "koala": dict(c="#9aa8b6", c2="#e8eef5", ears="big", muzzle="big"),
 "lion": dict(c="#f2b24c", c2="#ffe7b0", ears="round", mane="#c96a1a", tail="long", muzzle="small", nc="#8a4a2a"),
 "tiger": dict(c="#ff9a3a", c2="#fff", ears="cat", pat="stripes", tail="long", muzzle="small", whisk=True),
 "fox": dict(c="#ff7a2a", c2="#fff", ears="cat", tail="puff", muzzle="small", nc="#151515"),
 "wolf": dict(c="#8a9ab0", c2="#e8eef5", ears="cat", tail="puff", muzzle="big"),
 "mouse": dict(c="#b8b8c8", c2="#ffd9e0", ears="big", tail="long", muzzle="small", whisk=True, er=34),
 "hamster": dict(c="#f2b24c", c2="#fff", ears="round", muzzle="small", hw=280),
 "pig": dict(c="#ffb3c6", c2="#ffd9e0", ears="cat", tail="curl", muzzle="snout"),
 "cow": dict(c="#fff", c2="#ffd9e0", ears="horn", pat="spots", pc="#151515", muzzle="snout", nc="#ffb3c6"),
 "sheep": dict(c="#3a3a3a", c2="#5a5a5a", ears="floppy", ec="#3a3a3a", muzzle="none", wool="#f4f4f4", hw=170, hh=180),
 "goat": dict(c="#e8dcc8", c2="#fff", ears="horn", muzzle="big"),
 "horse": dict(c="#8a5a33", c2="#c98f45", ears="cat", tail="long", muzzle="snout", nc="#c98f45", hh=230),
 "camel": dict(c="#d9a85a", c2="#f4e3c4", ears="round", muzzle="big", tail="long"),
 "elephant": dict(c="#9aa8b6", c2="#c9d4e0", ears="big", muzzle="trunk"),
 "giraffe": dict(c="#ffd27a", c2="#fff", ears="horn", pat="spots", pc="#c96a1a", muzzle="snout", nc="#f4e3c4", neck=True, hw=190, hh=160),
 "zebra": dict(c="#fff", c2="#fff", ears="cat", pat="stripes", pc="#151515", muzzle="snout", nc="#3a3a3a"),
 "monkey": dict(c="#8a5a33", c2="#f1c7a0", ears="round", tail="curl", muzzle="big"),
 "gorilla": dict(c="#3a3a40", c2="#6a6a70", ears="round", muzzle="big", bw=260),
 "frog": dict(c="#6fcf4f", c2="#c8f0b0", ears="none", muzzle="none", er=58, legs=False),
 "turtle": dict(c="#6fcf4f", c2="#6fcf4f", ears="none", muzzle="none", legs=True, shell="#3f8a3a", hw=170, hh=150),
 "owl": dict(c="#8a5a33", c2="#f4e3c4", ears="tuft", muzzle="beak", er=60, wings=True),
 "chick": dict(c="#ffd21f", c2="#fff3b0", ears="none", muzzle="beak", wings=True, legs=False),
 "chicken": dict(c="#fff", c2="#fff", ears="none", muzzle="beak", pat="comb", wings=True, tail="fan"),
 "duck": dict(c="#fff", c2="#fff", ears="none", muzzle="beak", wings=True, legs=False),
 "parrot": dict(c="#2fbf6a", c2="#ffd21f", ears="none", muzzle="beak", wings=True, wc="#e5322d", tail="fan"),
 "eagle": dict(c="#5a3a22", c2="#fff", ears="none", muzzle="beak", wings=True, hw=220),
 "bat": dict(c="#4a3a5a", c2="#7a6a8a", ears="cat", muzzle="small", wings=True, wc="#3a2a4a", legs=False),
 "dolphin": dict(c="#7cb6e0", c2="#e8f4ff", ears="none", muzzle="big", tail="fin", legs=False),
 "shark": dict(c="#8a9ab0", c2="#fff", ears="none", muzzle="big", tail="fin", legs=False, pat=""),
 "seal": dict(c="#9aa8b6", c2="#c9d4e0", ears="none", muzzle="small", whisk=True, tail="fin", legs=False),
 "crab": dict(c="#e5322d", c2="#ff8a7a", ears="none", muzzle="none", legs=True, er=46),
 "ladybug": dict(c="#e5322d", c2="#151515", ears="none", pat="spots", pc="#151515", muzzle="none", legs=False),
 "butterfly": dict(c="#c45adb", c2="#ffd21f", ears="none", bwings="#ffd21f", muzzle="none", legs=False, hw=150, hh=150, bw=90),
 "ant": dict(c="#3a2a2a", c2="#5a4a4a", ears="none", muzzle="none", legs=True, antenna=True, hw=180, hh=170),
 "snail": dict(c="#c8e090", c2="#c8e090", ears="none", muzzle="none", legs=False, shell="#d98f45", hw=170, hh=160),
 "dragon": dict(c="#2fbf6a", c2="#ffd21f", ears="horn", wings=True, wc="#2f8a3a", tail="long", muzzle="big"),
 "unicorn": dict(c="#fff", c2="#ffd9f0", ears="cat", tail="long", muzzle="snout", nc="#ffd9f0", unihorn=True, mane="#c4a8ff"),
 "robot": dict(c="#9aa8b6", c2="#dff1ff", ears="none", muzzle="none", legs=True, er=46),
 "alien": dict(c="#7fdf6f", c2="#c8f0b0", ears="long", muzzle="none", er=60),
 "monster": dict(c="#7a4fd1", c2="#c4a8ff", ears="horn", muzzle="big", pat="spots", pc="#5a2fb1"),
 "teacher": dict(c="#f1c7a0", c2="#f1c7a0", ears="round", muzzle="none", glasses=True, legs=True),
 "scientist": dict(c="#f1c7a0", c2="#fff", ears="none", muzzle="none", glasses=True, mane="#ddd"),
 "grandpa": dict(c="#e9b98f", c2="#fff", ears="round", muzzle="none", glasses=True, hat="#5a3a22"),
}
for _n, _sp in ANIMALS.items():
    CHARS.setdefault(_n, ch_animal(_sp))
for _n in ANIMALS: HOME.setdefault(_n, {"dolphin": "ocean", "shark": "ocean", "seal": "ice", "crab": "beach", "polar_bear": "ice", "camel": "desert", "lion": "savanna", "giraffe": "savanna", "zebra": "savanna", "elephant": "savanna",
    "monkey": "jungle", "gorilla": "jungle", "parrot": "jungle", "frog": "pond", "turtle": "pond", "duck": "pond", "cow": "farm", "pig": "farm", "sheep": "farm", "goat": "farm", "horse": "farm", "chicken": "farm", "chick": "farm",
    "owl": "night", "bat": "night", "wolf": "night", "eagle": "mountain", "robot": "lab", "scientist": "lab", "alien": "space", "dragon": "mountain", "teacher": "classroom", "grandpa": "room", "unicorn": "garden"}.get(_n, "garden"))


# ---------------------------------------------------------------- 4 body templates: side-view quadrupeds, birds, sea creatures, bugs
def _mouth(i, x, y, w=34): return f'<path id="mo{i}" d="M{x-w},{y} Q{x},{y+34} {x+w},{y}" fill="#e85a6a" stroke="{K}" stroke-width="7"/>'
def ch_quad(sp):
    c, c2 = sp["c"], sp.get("c2", "#fff"); bw = sp.get("bw", 230); leg = sp.get("leg", 130); nk = sp.get("neck", 0)
    def f(i):
        hx, hy = -bw + 10, -70 - nk
        s = ""
        tail = {"thin": f'<path d="M0,0 C60,-20 80,-90 60,-140" stroke="{K}" stroke-width="26" fill="none" stroke-linecap="round"/><path d="M0,0 C60,-20 80,-90 60,-140" stroke="{c}" stroke-width="12" fill="none" stroke-linecap="round"/>',
                "fluffy": f'<path d="M0,0 C80,-30 150,-20 170,-90 C120,-60 60,-60 0,-30Z" fill="{sp.get("tc", c)}" {SW}/>', "tuft": f'<path d="M0,0 C70,10 110,-40 120,-90" stroke="{K}" stroke-width="20" fill="none"/><circle cx="122" cy="-100" r="30" fill="{sp.get("tc", "#8a4a1a")}" {SW}/>',
                "short": f'<circle cx="16" cy="-6" r="26" fill="{c}" {SW}/>', "curl": f'<path d="M0,0 C50,0 60,-60 30,-60 C10,-60 14,-34 34,-36" stroke="{K}" stroke-width="16" fill="none"/>', "long": f'<path d="M0,0 C120,40 170,-40 230,-10" stroke="{K}" stroke-width="40" fill="none" stroke-linecap="round"/><path d="M0,0 C120,40 170,-40 230,-10" stroke="{c}" stroke-width="24" fill="none" stroke-linecap="round"/>',
                "none": ""}[sp.get("tail", "thin")]
        s += f'<g id="tl{i}" transform="translate({bw-20} -10) rotate(0)">{tail}</g>'
        for k, x in enumerate((-bw + 70, -bw + 140, bw - 140, bw - 70)):
            s += f'<rect x="{x-28}" y="60" width="56" height="{leg}" rx="24" fill="{c if k % 2 else sp.get("lc", c)}" {SW}/><rect x="{x-30}" y="{40+leg}" width="60" height="26" rx="10" fill="{sp.get("hoof", K)}"/>'
        s += f'<ellipse cx="0" cy="20" rx="{bw}" ry="{sp.get("bh", 120)}" fill="{c}" stroke="{K}" stroke-width="12"/>'
        if sp.get("belly", True): s += f'<ellipse cx="0" cy="{60}" rx="{bw*.7:.0f}" ry="{sp.get("bh", 120)*.5:.0f}" fill="{c2}"/>'
        if sp.get("humps"): s += "".join(f'<path d="M{x-90},-70 Q{x},-260 {x+90},-70Z" fill="{c}" {SW}/>' for x in ([0] if sp["humps"] == 1 else [-70, 90]))
        pat = sp.get("pat")
        if pat == "spots": s += "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{sp.get("pc", "#151515")}" opacity=".85"/>' for x, y, r in ((-80, -10, 34), (60, 40, 30), (150, -20, 26), (-10, 70, 22), (-150, 40, 24)))
        if pat == "stripes": s += "".join(f'<path d="M{x},-90 q-20,60 0,130" stroke="{sp.get("pc", "#151515")}" stroke-width="22" fill="none" stroke-linecap="round"/>' for x in (-120, -50, 20, 90, 160))
        if pat == "shell": s += f'<path d="M{-bw+20},20 A{bw-20},{sp.get("bh",120)+40} 0 0,1 {bw-20},20Z" fill="{sp.get("pc", "#3f8a3a")}" {SW}/>' + "".join(f'<path d="M{x},20 Q{x+50},-90 {x+100},20" stroke="{K}" stroke-width="6" fill="none"/>' for x in (-150, -50, 50))
        if pat == "wool": s += "".join(f'<circle cx="{x}" cy="{y}" r="70" fill="{sp.get("pc", "#f4f4f4")}" {SW}/>' for x, y in ((-140, 0), (-50, -40), (50, -40), (140, 0), (-90, 60), (0, 70), (90, 60)))
        if nk: s += f'<path d="M{-bw+60},-40 L{hx+20},{hy+40} L{hx+100},{hy+60} L{-bw+170},-50Z" fill="{c}" {SW}/>' + ("".join(f'<circle cx="{-bw+80 - k*25}" cy="{-80 - k*nk/4:.0f}" r="20" fill="{sp.get("pc", "#c96a1a")}"/>' for k in range(3)) if pat == "spots" else "")
        if sp.get("mane") == "neck": s += f'<path d="M{-bw+160},-60 L{hx+80},{hy-10} L{hx+120},{hy+20} L{-bw+190},-50Z" fill="{sp.get("mc", "#3a2414")}"/>'
        if sp.get("mane") == "ring": s += f'<circle cx="{hx}" cy="{hy}" r="{sp.get("hr", 110)+60}" fill="{sp.get("mc", "#c96a1a")}" {SW}/>'
        ears = sp.get("ears", "point"); hr = sp.get("hr", 110)
        E = {"point": lambda: f'<path d="M{hx+20},{hy-hr+30} L{hx+50},{hy-hr-60} L{hx+90},{hy-hr+50}Z" fill="{c}" {SW}/>', "round": lambda: f'<circle cx="{hx+50}" cy="{hy-hr+10}" r="40" fill="{c}" {SW}/>',
             "floppy": lambda: f'<ellipse cx="{hx+70}" cy="{hy-10}" rx="40" ry="90" fill="{sp.get("ec", c)}" {SW} transform="rotate(20 {hx+70} {hy-10})"/>', "long": lambda: f'<ellipse cx="{hx+40}" cy="{hy-hr-60}" rx="34" ry="110" fill="{c}" {SW}/>',
             "big": lambda: f'<ellipse cx="{hx+90}" cy="{hy-10}" rx="110" ry="140" fill="{c}" {SW}/><ellipse cx="{hx+90}" cy="{hy-10}" rx="70" ry="100" fill="#ffc2c2"/>',
             "horns": lambda: f'<path d="M{hx+10},{hy-hr+20} Q{hx-10},{hy-hr-90} {hx+40},{hy-hr-110} Q{hx+30},{hy-hr-40} {hx+50},{hy-hr+20}Z" fill="#f4e3b0" {SW}/><path d="M{hx+50},{hy-hr+20} Q{hx+60},{hy-hr-80} {hx+110},{hy-hr-90} Q{hx+90},{hy-hr-30} {hx+90},{hy-hr+30}Z" fill="#f4e3b0" {SW}/>',
             "antlers": lambda: f'<path d="M{hx+30},{hy-hr+20} V{hy-hr-90} M{hx+30},{hy-hr-40} L{hx-30},{hy-hr-90} M{hx+30},{hy-hr-70} L{hx+90},{hy-hr-120}" stroke="#8a5a33" stroke-width="18" stroke-linecap="round"/>',
             "ossicones": lambda: f'<path d="M{hx+20},{hy-hr+20} V{hy-hr-50} M{hx+70},{hy-hr+20} V{hy-hr-50}" stroke="{K}" stroke-width="14"/><circle cx="{hx+20}" cy="{hy-hr-55}" r="16" fill="#8a4a1a"/><circle cx="{hx+70}" cy="{hy-hr-55}" r="16" fill="#8a4a1a"/>', "none": lambda: ""}
        s += E.get(ears, E["point"])() if ears != "floppy" else ""
        snout = sp.get("snout", "short")
        s += f'<ellipse cx="{hx}" cy="{hy}" rx="{hr*1.05:.0f}" ry="{hr}" fill="{c}" stroke="{K}" stroke-width="12"/>'
        if ears == "floppy": s += E["floppy"]()
        if snout == "long": s += f'<ellipse cx="{hx-hr*.8:.0f}" cy="{hy+30}" rx="{hr*.75:.0f}" ry="{hr*.5:.0f}" fill="{sp.get("sc", c2)}" {SW}/><circle cx="{hx-hr*1.4:.0f}" cy="{hy+10}" r="14" fill="{K}"/>' + _mouth(i, hx - hr * .9, hy + 55, 40)
        elif snout == "croc": s += f'<path d="M{hx-30},{hy-20} L{hx-hr*2.6:.0f},{hy+10} Q{hx-hr*2.7:.0f},{hy+40} {hx-hr*2.5:.0f},{hy+50} L{hx-30},{hy+50}Z" fill="{c}" {SW}/>' + "".join(f'<path d="M{hx-60-k*45},{hy+48} l12,-22 l12,22" fill="#fff"/>' for k in range(5)) + _mouth(i, hx - 120, hy + 62, 60)
        elif snout == "trunk": s += f'<path d="M{hx-hr*.7:.0f},{hy} C{hx-hr*1.6:.0f},{hy+40} {hx-hr*1.6:.0f},{hy+200} {hx-hr*1.1:.0f},{hy+250} C{hx-hr*1.25:.0f},{hy+190} {hx-hr*1.1:.0f},{hy+80} {hx-hr*.5:.0f},{hy+60}Z" fill="{c}" {SW}/><path d="M{hx-40},{hy+70} q-60,40 -40,90" stroke="#fffbe8" stroke-width="20" fill="none" stroke-linecap="round"/>' + _mouth(i, hx - 10, hy + 70, 26)
        elif snout == "pig": s += f'<ellipse cx="{hx-hr*.95:.0f}" cy="{hy+20}" rx="40" ry="50" fill="{sp.get("sc", "#ffb3c6")}" {SW}/><circle cx="{hx-hr*.95:.0f}" cy="{hy+5}" r="9" fill="{K}"/><circle cx="{hx-hr*.95:.0f}" cy="{hy+35}" r="9" fill="{K}"/>' + _mouth(i, hx - 40, hy + 70, 26)
        else: s += f'<ellipse cx="{hx-hr*.6:.0f}" cy="{hy+30}" rx="{hr*.5:.0f}" ry="{hr*.38:.0f}" fill="{sp.get("sc", c2)}"/><ellipse cx="{hx-hr*.95:.0f}" cy="{hy+10}" rx="16" ry="12" fill="{K}"/>' + _mouth(i, hx - hr * .6, hy + 52, 26)
        s += eyes(i, (hx - 10,), hy - 30, sp.get("er", 34))
        if sp.get("whisk"): s += f'<path d="M{hx-hr*.9:.0f},{hy+30} h-90 M{hx-hr*.9:.0f},{hy+45} l-80,25" stroke="{K}" stroke-width="5"/>'
        if sp.get("tusk"): s += f'<path d="M{hx-50},{hy+60} q-40,60 -100,50" stroke="#fffbe8" stroke-width="18" fill="none"/>'
        if ears in E and ears not in ("floppy",) and sp.get("ears2", True) and ears in ("point", "round"): s += ""
        if sp.get("uni"): s += f'<path d="M{hx-10},{hy-hr+10} L{hx-30},{hy-hr-130} L{hx+20},{hy-hr+10}Z" fill="#ffd21f" {SW}/>'
        return s
    return f
def ch_bird(sp):
    c, c2 = sp["c"], sp.get("c2", "#fff"); legl = sp.get("leg", 90)
    def f(i):
        s = f'<path d="M110,40 L240,{sp.get("tail_y", -10)} L230,90Z" fill="{sp.get("tc", c)}" {SW}/>'
        s += "".join(f'<path d="M{x},180 V{180+legl} M{x},{180+legl} l-30,20 M{x},{180+legl} l10,24" stroke="#ff9a3a" stroke-width="12" stroke-linecap="round"/>' for x in (-30, 40))
        nk = sp.get("neck", 0)
        s += f'<ellipse cx="20" cy="60" rx="{sp.get("bw", 160)}" ry="{sp.get("bh", 150)}" fill="{c}" stroke="{K}" stroke-width="12"/><ellipse cx="-20" cy="100" rx="{sp.get("bw", 160)*.6:.0f}" ry="{sp.get("bh",150)*.6:.0f}" fill="{c2}"/>'
        hx, hy, hr = -90, -110 - nk, sp.get("hr", 100)
        if nk: s += f'<path d="M-60,-20 Q-150,{hy+80} {hx},{hy+40} L{hx+60},{hy+60} Q-60,{hy+120} 10,-30Z" fill="{c}" {SW}/>'
        s += f'<circle cx="{hx}" cy="{hy}" r="{hr}" fill="{sp.get("hc", c)}" stroke="{K}" stroke-width="12"/>'
        if sp.get("crest") == "comb": s += f'<path d="M{hx-50},{hy-hr+20} q20,-80 50,-10 q30,-80 50,0 q30,-70 40,20Z" fill="#e5322d" {SW}/>'
        if sp.get("crest") == "tuft": s += f'<path d="M{hx-60},{hy-hr+30} L{hx-90},{hy-hr-50} L{hx-20},{hy-hr+10}Z M{hx+60},{hy-hr+30} L{hx+90},{hy-hr-50} L{hx+20},{hy-hr+10}Z" fill="{c}" {SW}/>'
        if sp.get("crest") == "feathers": s += "".join(f'<path d="M{hx+10},{hy-hr+10} Q{hx+dx},{hy-hr-90} {hx+dx+30},{hy-hr-60}" stroke="{sp.get("cc", "#ffd21f")}" stroke-width="16" fill="none" stroke-linecap="round"/>' for dx in (-20, 20, 60))
        b = sp.get("beak", "cone")
        if b == "cone": s += f'<path d="M{hx-hr+10},{hy-10} L{hx-hr-60},{hy+10} L{hx-hr+10},{hy+30}Z" fill="#ff9a3a" {SW}/>'
        if b == "hook": s += f'<path d="M{hx-hr+10},{hy-30} Q{hx-hr-80},{hy-30} {hx-hr-60},{hy+50} Q{hx-hr-40},{hy+10} {hx-hr+20},{hy+30}Z" fill="{sp.get("bc", "#ffd21f")}" {SW}/>'
        if b == "flat": s += f'<path d="M{hx-hr+10},{hy-5} Q{hx-hr-110},{hy-20} {hx-hr-100},{hy+25} Q{hx-hr-40},{hy+40} {hx-hr+20},{hy+30}Z" fill="#ff9a3a" {SW}/>'
        if b == "long": s += f'<path d="M{hx-hr+10},{hy-10} L{hx-hr-170},{hy+30} L{hx-hr+10},{hy+30}Z" fill="{sp.get("bc", "#3a3a3a")}" {SW}/>'
        s += f'<path id="mo{i}" d="M{hx-hr+5},{hy+28} q-10,6 0,10" fill="none" stroke="{K}" stroke-width="4"/>'
        s += eyes(i, (hx - 20,), hy - 20, sp.get("er", 32))
        if sp.get("mask"): s += f'<path d="M{hx-80},{hy-50} H{hx+40}" stroke="{K}" stroke-width="16"/>'
        s += f'<g id="tl{i}" transform="translate(40 20) rotate(0)"><path d="M0,0 C120,-30 190,40 140,140 C80,120 20,90 0,0Z" fill="{sp.get("wc", c)}" {SW}/></g>'
        return s
    return f
def ch_sea(sp):
    c, c2 = sp["c"], sp.get("c2", "#fff"); kind = sp.get("kind", "fish")
    def f(i):
        if kind == "jelly":
            s = f'<g id="tl{i}" transform="translate(0 60) rotate(0)">' + "".join(f'<path d="M{x},0 q30,80 0,160 q-30,80 0,160" stroke="{c}" stroke-width="18" fill="none" stroke-linecap="round"/>' for x in (-120, -60, 0, 60, 120)) + '</g>'
            s += f'<path d="M-200,60 C-220,-220 220,-220 200,60 Q150,90 100,60 Q50,90 0,60 Q-50,90 -100,60 Q-150,90 -200,60Z" fill="{c}" fill-opacity=".9" stroke="{K}" stroke-width="12"/>'
            return s + eyes(i, (-60, 60), -40, 32) + _mouth(i, 0, 20, 30)
        if kind == "crab":
            s = "".join(f'<path d="M{sx*120},40 l{sx*90},60 l{sx*30},70" stroke="{K}" stroke-width="16" fill="none" stroke-linecap="round"/>' for sx in (-1, 1) for _ in (0,))
            s += "".join(f'<path d="M{sx*100},{30+k*30} l{sx*120},{40+k*10}" stroke="{c}" stroke-width="14" stroke-linecap="round"/>' for sx in (-1, 1) for k in range(3))
            s += f'<g id="tl{i}" transform="translate(0 0) rotate(0)"><path d="M-170,-40 L-260,-170 M170,-40 L260,-170" stroke="{c}" stroke-width="30" stroke-linecap="round"/><path d="M-260,-170 l-60,-40 l40,-50 l40,50 l-20,-60 l60,40Z M260,-170 l60,-40 l-40,-50 l-40,50 l20,-60 l-60,40Z" fill="{c}" {SW}/></g>'
            s += f'<ellipse cx="0" cy="40" rx="210" ry="130" fill="{c}" stroke="{K}" stroke-width="12"/><path d="M-50,-80 V-150 M50,-80 V-150" stroke="{K}" stroke-width="12"/>'
            return s + eyes(i, (-50, 50), -170, 30) + _mouth(i, 0, 60, 40)
        if kind == "star":
            pts = " ".join(f"{(220 if k % 2 == 0 else 95) * math.cos(math.pi/2 + k*math.pi/5):.0f},{-(220 if k % 2 == 0 else 95) * math.sin(math.pi/2 + k*math.pi/5):.0f}" for k in range(10))
            return f'<g id="tl{i}" transform="translate(0 0) rotate(0)"><polygon points="{pts}" fill="{c}" stroke="{K}" stroke-width="12" stroke-linejoin="round"/></g>' + eyes(i, (-45, 45), -20, 28) + _mouth(i, 0, 40, 28)
        if kind == "seahorse":
            s = f'<path d="M0,-200 C120,-220 140,-80 60,-20 C140,40 120,180 20,200 C-40,210 -60,260 -20,290 C-100,280 -80,180 0,160 C60,140 60,60 -20,40 C-80,30 -90,-60 -40,-110 L-160,-110 L-160,-150 L-40,-170Z" fill="{c}" stroke="{K}" stroke-width="12"/>'
            s += f'<g id="tl{i}" transform="translate(70 0) rotate(0)"><path d="M0,0 C60,-40 90,20 40,60Z" fill="{c2}" {SW}/></g>'
            return s + eyes(i, (-10,), -150, 30) + _mouth(i, -150, -130, 14)
        # fish-like: fish, dolphin, shark
        bw = sp.get("bw", 260); s = ""
        s += f'<g id="tl{i}" transform="translate({bw-30} 0) rotate(0)"><path d="M0,0 L110,-110 Q80,0 110,110Z" fill="{c}" {SW}/></g>'
        if sp.get("fin", True): s += f'<path d="M-20,{-sp.get("bh",120)+10} Q40,{-sp.get("bh",120)-130} 110,{-sp.get("bh",120)+20}Z" fill="{c}" {SW}/>'
        s += f'<path d="M{-bw},10 C{-bw+20},{-sp.get("bh",120)*1.4:.0f} {bw*.6:.0f},{-sp.get("bh",120)*1.2:.0f} {bw},0 C{bw*.6:.0f},{sp.get("bh",120)*1.2:.0f} {-bw+20},{sp.get("bh",120)*1.2:.0f} {-bw},10Z" fill="{c}" stroke="{K}" stroke-width="12"/>'
        s += f'<path d="M{-bw+30},40 C{-bw/2:.0f},{sp.get("bh",120)} {bw*.4:.0f},{sp.get("bh",120)*.9:.0f} {bw*.7:.0f},30 C{bw*.3:.0f},60 {-bw/2:.0f},70 {-bw+30},40Z" fill="{c2}"/>'
        if kind == "dolphin": s += f'<path d="M{-bw+10},0 Q{-bw-70},10 {-bw-60},40 Q{-bw-20},40 {-bw+20},30Z" fill="{c}" {SW}/>'
        if kind == "shark": s += "".join(f'<path d="M{-bw+40+k*28},40 l12,24 l12,-24" fill="#fff" stroke="{K}" stroke-width="3"/>' for k in range(5)) + "".join(f'<path d="M{-80+k*30},-20 q-10,30 0,60" stroke="{K}" stroke-width="6" fill="none"/>' for k in range(3))
        if kind == "fish": s += "".join(f'<path d="M{x},-70 q-30,70 0,140" stroke="{sp.get("pc", "#fff")}" stroke-width="22" fill="none" opacity=".8"/>' for x in (-40, 60))
        s += f'<path d="M-60,40 Q-10,120 50,50" fill="{c}" {SW}/>'
        return s + eyes(i, (-bw + 90,), -30, sp.get("er", 30)) + _mouth(i, -bw + 50, 40, 22)
    return f
def ch_bug(sp):
    c, c2 = sp["c"], sp.get("c2", "#151515"); kind = sp.get("kind", "ant")
    def f(i):
        legs = "".join(f'<path d="M{x},40 l{-40 if x < 0 else 40},90 l{-20 if x < 0 else 20},40" stroke="{K}" stroke-width="12" fill="none" stroke-linecap="round"/>' for x in (-90, 0, 90))
        ant = f'<path d="M-160,-110 Q-200,-220 -260,-230 M-120,-130 Q-120,-240 -80,-270" stroke="{K}" stroke-width="10" fill="none"/><circle cx="-260" cy="-230" r="16" fill="{K}"/><circle cx="-80" cy="-270" r="16" fill="{K}"/>'
        if kind == "ladybug":
            s = legs + f'<g id="tl{i}" transform="translate(0 0) rotate(0)"><path d="M-170,40 A190,190 0 0,1 210,40Z" fill="{c}" stroke="{K}" stroke-width="12"/><path d="M20,-150 V40" stroke="{K}" stroke-width="10"/>' + "".join(f'<circle cx="{x}" cy="{y}" r="28" fill="{K}"/>' for x, y in ((-80, -60), (110, -60), (-30, -5), (80, -5), (40, -110))) + '</g>'
            return s + f'<circle cx="-170" cy="-20" r="90" fill="{K}"/>' + ant.replace("-110", "-80") + eyes(i, (-200, -130), -40, 26) + _mouth(i, -170, 30, 26)
        if kind == "butterfly":
            s = f'<g id="tl{i}" transform="translate(0 0) rotate(0)">' + "".join(f'<ellipse cx="{sx*170}" cy="{dy}" rx="160" ry="{r_}" fill="{c if dy < 0 else sp.get("c3", c2)}" {SW} transform="rotate({sx*25} {sx*170} {dy})"/><circle cx="{sx*190}" cy="{dy}" r="40" fill="#fff" opacity=".7"/>' for sx in (-1, 1) for dy, r_ in ((-120, 190), (160, 120))) + '</g>'
            return s + f'<rect x="-36" y="-160" width="72" height="360" rx="36" fill="#3a2a2a" {SW}/>' + f'<circle cx="0" cy="-230" r="80" fill="#3a2a2a" {SW}/>' + ant.replace("-160,-110", "-30,-290").replace("-120,-130", "30,-290") + eyes(i, (-30, 30), -240, 26) + _mouth(i, 0, -190, 22)
        if kind == "spider":
            s = "".join(f'<path d="M0,0 L{sx*200},{dy} L{sx*260},{dy+120}" stroke="{K}" stroke-width="16" fill="none" stroke-linejoin="round"/>' for sx in (-1, 1) for dy in (-160, -60, 40, 140))
            return f'<g id="tl{i}" transform="translate(0 0) rotate(0)">{s}</g><circle r="170" fill="{c}" stroke="{K}" stroke-width="12"/>' + eyes(i, (-60, 60), -40, 36) + _mouth(i, 0, 60, 34)
        if kind == "caterpillar":
            s = "".join(f'<circle cx="{x}" cy="{40 + (k%2)*-30}" r="80" fill="{c if k % 2 else sp.get("c3", c)}" {SW}/>' for k, x in enumerate((260, 160, 60, -40, -140)))
            return f'<g id="tl{i}" transform="translate(0 0) rotate(0)">{s}</g><circle cx="-240" cy="-20" r="110" fill="{c}" {SW}/>' + ant.replace("-160,-110", "-280,-110").replace("-120,-130", "-200,-120") + eyes(i, (-280, -200), -40, 28) + _mouth(i, -240, 40, 30)
        if kind == "snail":
            s = f'<path d="M-280,160 Q-300,40 -220,40 L240,140 Q260,190 200,190 H-280Z" fill="{c2}" {SW}/><path d="M-220,60 L-250,-90 M-180,60 L-170,-100" stroke="{K}" stroke-width="10"/><circle cx="-250" cy="-100" r="14" fill="{K}"/><circle cx="-170" cy="-110" r="14" fill="{K}"/>'
            s += f'<g id="tl{i}" transform="translate(40 30) rotate(0)"><circle r="170" fill="{c}" stroke="{K}" stroke-width="12"/><path d="M0,0 m-20,0 a20,20 0 1,1 40,0 a60,60 0 1,1 -120,0 a100,100 0 1,1 200,0 a140,140 0 1,1 -280,0" stroke="{K}" stroke-width="8" fill="none"/></g>'
            return s + eyes(i, (-260,), 90, 26) + _mouth(i, -250, 140, 24)
        # ant / beetle / mosquito: 3 segments
        wings = f'<path d="M-20,-60 C-80,-260 120,-260 60,-60Z M40,-60 C60,-250 240,-200 120,-50Z" fill="#dff4ff" fill-opacity=".8" {SW}/>' if kind in ("mosquito", "fly", "beetle") else ""
        s = legs + f'<g id="tl{i}" transform="translate(0 0) rotate(0)">{wings}</g>'
        s += f'<ellipse cx="170" cy="20" rx="{140 if kind != "mosquito" else 170}" ry="{100 if kind != "mosquito" else 60}" fill="{c}" stroke="{K}" stroke-width="12"/><ellipse cx="10" cy="10" rx="80" ry="70" fill="{c}" stroke="{K}" stroke-width="12"/>'
        if kind == "beetle": s += f'<path d="M170,-80 V120" stroke="{K}" stroke-width="8"/>'
        s += f'<circle cx="-150" cy="-30" r="100" fill="{c}" stroke="{K}" stroke-width="12"/>' + ant
        if kind == "mosquito": s += f'<path d="M-240,0 L-340,40" stroke="{K}" stroke-width="10"/>'
        return s + eyes(i, (-190, -120), -50, 28) + _mouth(i, -150, 20, 26)
    return f
NEW = {
 "dog": (ch_quad, dict(c="#c98f45", c2="#f4e3c4", ears="floppy", ec="#8a5a33", tail="thin", snout="long")),
 "puppy": (ch_quad, dict(c="#f4e3c4", c2="#fff", ears="floppy", ec="#c98f45", tail="short", snout="long", pat="spots", pc="#c98f45", leg=100)),
 "wolf": (ch_quad, dict(c="#8a9ab0", c2="#e8eef5", ears="point", tail="fluffy", snout="long")),
 "fox": (ch_quad, dict(c="#ff7a2a", c2="#fff", ears="point", tail="fluffy", tc="#ff7a2a", snout="long", hoof="#3a2414")),
 "lion": (ch_quad, dict(c="#f2b24c", c2="#ffe7b0", ears="round", tail="tuft", mane="ring", mc="#c96a1a", snout="short")),
 "tiger": (ch_quad, dict(c="#ff9a3a", c2="#fff", ears="round", tail="long", pat="stripes", snout="short", whisk=True)),
 "horse": (ch_quad, dict(c="#8a5a33", c2="#a87048", ears="point", tail="fluffy", tc="#3a2414", neck=170, mane="neck", snout="long", sc="#c98f45", leg=170, hr=95)),
 "zebra": (ch_quad, dict(c="#fff", c2="#fff", ears="point", tail="tuft", tc="#151515", neck=150, mane="neck", mc="#151515", snout="long", sc="#3a3a3a", pat="stripes", leg=160, hr=90)),
 "camel": (ch_quad, dict(c="#d9a85a", c2="#f4e3c4", ears="round", tail="thin", neck=160, humps=2, snout="long", leg=190, hr=85)),
 "giraffe": (ch_quad, dict(c="#ffd27a", c2="#fff3d0", ears="ossicones", tail="tuft", neck=360, pat="spots", pc="#c96a1a", snout="long", leg=200, hr=80, bw=200)),
 "elephant": (ch_quad, dict(c="#9aa8b6", c2="#b8c4d0", ears="big", tail="thin", snout="trunk", tusk=True, leg=150, hr=130, bw=260, bh=150)),
 "cow": (ch_quad, dict(c="#fff", c2="#ffd9e0", ears="horns", tail="tuft", pat="spots", snout="pig", sc="#ffc2d0")),
 "pig": (ch_quad, dict(c="#ffb3c6", c2="#ffd9e0", ears="point", tail="curl", snout="pig", leg=90)),
 "sheep": (ch_quad, dict(c="#3a3a3a", c2="#3a3a3a", ears="floppy", ec="#3a3a3a", tail="short", pat="wool", snout="short", belly=False, leg=110)),
 "goat": (ch_quad, dict(c="#e8dcc8", c2="#fff", ears="horns", tail="short", snout="long", leg=130)),
 "deer": (ch_quad, dict(c="#b8753a", c2="#f4e3c4", ears="antlers", tail="short", snout="long", pat="spots", pc="#fff", neck=80, leg=170, hr=90)),
 "crocodile": (ch_quad, dict(c="#4f9a4a", c2="#c8e090", ears="none", tail="long", snout="croc", leg=60, bh=90, bw=280, hr=90)),
 "turtle": (ch_quad, dict(c="#6fcf4f", c2="#6fcf4f", ears="none", tail="short", pat="shell", pc="#3f8a3a", snout="short", leg=70, belly=False)),
 "rhino": (ch_quad, dict(c="#8a9ab0", c2="#a8b4c0", ears="point", tail="thin", snout="long", uni=True, leg=110, bw=260, bh=140, hr=120)),
 "unicorn": (ch_quad, dict(c="#fff", c2="#ffd9f0", ears="point", tail="fluffy", tc="#c4a8ff", neck=170, mane="neck", mc="#c4a8ff", snout="long", sc="#ffd9f0", uni=True, leg=170, hr=95)),
 "owl": (ch_bird, dict(c="#8a5a33", c2="#f4e3c4", beak="hook", bc="#ff9a3a", crest="tuft", er=46, hr=120)),
 "chick": (ch_bird, dict(c="#ffd21f", c2="#fff3b0", beak="cone", bw=140, bh=130)),
 "chicken": (ch_bird, dict(c="#fff", c2="#fff", beak="cone", crest="comb", tc="#e5322d")),
 "duck": (ch_bird, dict(c="#fff", c2="#fff", beak="flat", hc="#2f8a3a", leg=50)),
 "parrot": (ch_bird, dict(c="#2fbf6a", c2="#ffd21f", beak="hook", bc="#3a3a3a", wc="#e5322d", tc="#2b8be0", crest="feathers")),
 "eagle": (ch_bird, dict(c="#5a3a22", c2="#7a5a3a", hc="#fff", beak="hook", bc="#ffd21f", wc="#4a2a12", mask=False)),
 "flamingo": (ch_bird, dict(c="#ff8ab0", c2="#ffb3cc", beak="long", bc="#3a3a3a", neck=200, leg=260, bw=140, bh=110, hr=80)),
 "crow": (ch_bird, dict(c="#2a2a3a", c2="#3a3a4a", beak="long", bc="#151515", leg=90)),
 "penguin2": (ch_bird, dict(c="#1f2a3a", c2="#fff", beak="cone", leg=30, bw=170, bh=200)),
 "peacock": (ch_bird, dict(c="#2b5ad0", c2="#2fbf6a", beak="cone", crest="feathers", cc="#2b5ad0", tc="#2fbf6a")),
 "dolphin": (ch_sea, dict(c="#7cb6e0", c2="#e8f4ff", kind="dolphin")),
 "shark": (ch_sea, dict(c="#8a9ab0", c2="#fff", kind="shark", bw=290)),
 "fish": (ch_sea, dict(c="#ff9a3a", c2="#ffd9a8", kind="fish", pc="#fff", fin=True, bw=220, bh=140)),
 "goldfish": (ch_sea, dict(c="#ffb02e", c2="#ffe7b0", kind="fish", pc="#ff7a2a", bw=200, bh=150)),
 "jellyfish": (ch_sea, dict(c="#c4a8ff", kind="jelly")),
 "crab": (ch_sea, dict(c="#e5322d", kind="crab")),
 "starfish": (ch_sea, dict(c="#ff8a5a", kind="star")),
 "seahorse": (ch_sea, dict(c="#ffb02e", c2="#ffe7b0", kind="seahorse")),
 "ant": (ch_bug, dict(c="#3a2a2a", kind="ant")),
 "beetle": (ch_bug, dict(c="#2a6a4a", kind="beetle")),
 "mosquito": (ch_bug, dict(c="#5a5a6a", kind="mosquito")),
 "ladybug": (ch_bug, dict(c="#e5322d", kind="ladybug")),
 "butterfly": (ch_bug, dict(c="#c45adb", c3="#ffd21f", kind="butterfly")),
 "spider": (ch_bug, dict(c="#3a2a4a", kind="spider")),
 "caterpillar": (ch_bug, dict(c="#7fdf4f", c3="#4fbf3f", kind="caterpillar")),
 "snail": (ch_bug, dict(c="#d98f45", c2="#c8e090", kind="snail")),
}
for _n, (_t, _sp) in NEW.items():
    CHARS[_n] = _t(_sp)
for _n in NEW: HOME.setdefault(_n, {"dolphin": "ocean", "shark": "ocean", "fish": "ocean", "goldfish": "ocean", "jellyfish": "ocean", "crab": "beach", "starfish": "beach", "seahorse": "ocean", "crocodile": "pond", "flamingo": "pond",
    "deer": "jungle", "rhino": "savanna", "crow": "night", "peacock": "garden", "penguin2": "ice", "beetle": "garden", "mosquito": "pond", "caterpillar": "garden", "spider": "garden"}.get(_n, HOME.get(_n, "garden")))

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
    SCENE = {  # name: (sky top, sky bottom, ground, decoration icons [(name,x,y,scale)], bubble colour)
     "desert": ("#ffd27a", "#ffb35a", "#e8c070", [("sun", 820, 520, .8), ("pyramid", 260, 1420, 1.1), ("pyramid", 520, 1460, .7)], "#fff3d0"),
     "savanna": ("#ffcf7a", "#ffa64a", "#d9b050", [("sun", 540, 1250, 1.6), ("tree", 200, 1400, 1.2), ("tree", 900, 1430, .9)], "#fff3d0"),
     "jungle": ("#7fd36a", "#2f8a3a", "#3f7a2a", [("leaf", 120, 500, 1.3), ("leaf", 960, 640, 1.2), ("tree", 160, 1380, 1.3), ("tree", 940, 1400, 1.4), ("flower", 820, 1700, .5)], "#d8ffd0"),
     "pond": ("#9fe0ff", "#c8f0ff", "#6fcf4f", [("water", 540, 1640, 3.5), ("leaf", 300, 1640, .6), ("flower", 820, 1620, .5), ("cloud", 260, 560, .9)], "#ffffff"),
     "farm": ("#9fe0ff", "#dff4ff", "#8fd35a", [("house", 860, 1300, 1.2), ("tree", 160, 1350, 1.2), ("sun", 860, 500, .8), ("cloud", 300, 560, .8)], "#ffffff"),
     "night": ("#0b1a3a", "#2b2f6a", "#1f3a2a", [("moon", 820, 520, .9), ("star", 220, 420, .3), ("star", 420, 700, .2), ("star", 640, 380, .25), ("tree", 160, 1400, 1.2)], "#bfd0ff"),
     "mountain": ("#9fd4ff", "#e8f4ff", "#7aa860", [("mountain", 260, 1300, 2.2), ("mountain", 820, 1340, 1.8), ("cloud", 700, 520, .9)], "#ffffff"),
     "beach": ("#8fd3ff", "#dff4ff", "#f2d79a", [("sun", 820, 500, .8), ("water", 540, 1430, 3.5), ("cloud", 260, 580, .8)], "#ffffff"),
     "city": ("#9fd4ff", "#dff4ff", "#9aa8b6", [("tower", 200, 1250, 1.6), ("factory", 860, 1350, 1.3), ("bus", 820, 1700, .7)], "#ffffff"),
     "lab": ("#dff4ff", "#bfe0ff", "#9aa8b6", [("atom", 200, 560, .9), ("dna", 900, 620, .9), ("laptop", 820, 1600, .8)], "#ffffff"),
     "classroom": ("#ffe7b0", "#ffd98a", "#c98f45", [("book", 200, 600, .8), ("pencil", 880, 620, .7), ("clock", 540, 500, .6)], "#fff3d6"),
     "kitchen": ("#fff3e0", "#ffe0c0", "#c9d6e0", [("cake", 220, 1600, .7), ("coffee", 880, 1600, .6), ("pizza", 860, 560, .6)], "#ffffff"),
     "rain": ("#7a8ea8", "#a8b8cc", "#5a7a5a", [("rain", 260, 520, 1), ("rain", 800, 640, .9), ("bolt", 540, 700, .6)], "#dfe8ff"),
     "snow": ("#cfe0f0", "#f4f8ff", "#ffffff", [("snow", 200, 500, .4), ("snow", 820, 620, .3), ("tree", 900, 1400, 1.2)], "#ffffff"),
     "stage": ("#3a1a4a", "#7a2a5a", "#5a2a1a", [("star", 200, 500, .5), ("star", 880, 500, .5), ("music", 540, 600, .6)], "#ffd0f0"),
     "hospital": ("#e8f4ff", "#ffffff", "#bfd0e0", [("hospital", 820, 1350, 1.1), ("pill", 220, 600, .6), ("syringe", 880, 560, .6)], "#ffffff"),
    }
    if name in SCENE:
        t, b2, g, deco, bub = SCENE[name]
        return (f'<linearGradient id="sk{i}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{t}"/><stop offset="1" stop-color="{b2}"/></linearGradient><rect width="1080" height="1920" fill="url(#sk{i})"/>'
                f'<path d="M0,1520 Q540,1420 1080,1520 V1920 H0Z" fill="{g}" stroke="{K}" stroke-width="10"/>' + "".join(f'<g transform="translate({x} {y})">{icon(n, min(sc * 1.4, 3.6))}</g>' for n, x, y, sc in deco)), bub
    return ('<rect width="1080" height="1920" fill="#0b0f2a"/>' + "".join(f'<circle cx="{(R(k)+1)*540:.0f}" cy="{(R(k+70)+1)*960:.0f}" r="{2+abs(R(k+5))*4:.1f}" fill="#fff"/>' for k in range(120)) +
            '<circle cx="880" cy="1650" r="260" fill="#ff8a5a" stroke="#0b2a4a" stroke-width="10"/><circle cx="800" cy="1580" r="40" fill="#e0703f"/><circle cx="950" cy="1720" r="60" fill="#e0703f"/>'), "#bfd0ff"
from icons import ICONS as ICON, icon as _icon
def icon(n, sc=1): return _icon(n, sc)
def bubbles(i, col): return "".join(f'<circle class="bu{i}" cx="{(R(i*20+k)+1)*540:.0f}" cy="{1900+k*40}" r="{10+abs(R(k+i))*26:.0f}" fill="none" stroke="{col}" stroke-width="5" opacity=".8"/>' for k in range(16))
CX, CY = 560, 1180
def scene(i, b, s, e, c0, c1):
    ep_ch = ep.get("character", "whale"); ch = b.get("character", ep_ch); k = b["k"]; D = c1 - c0; js = []
    back, bub = bg(b.get("bg", ep.get("bg", HOME[ch])), i)
    sv = f'<svg class="full" width="1080" height="1920" viewBox="0 0 1080 1920">{back}{bubbles(i, bub)}'
    cs = b.get("scale", 1.15 if ch in NEW else (.85 if ch not in ("kid", "penguin") else .75))
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
