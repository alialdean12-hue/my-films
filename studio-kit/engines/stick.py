"""Style 7 · stick people WITH bodies (clothes, skin, hair) in 8 places. JSON -> video. See README.md."""
from lib import *
CSS = ('.cap{position:absolute;left:80px;right:80px;top:170px;text-align:center;font-weight:900;font-size:88px;line-height:1.2;color:#151515}'
       '.cap .bx{display:inline-block;background:#fbf8f0;padding:4px 34px 16px;border-radius:26px;box-shadow:0 10px 0 #0002}'
       '.n{display:inline-block;background:#e5322d;color:#fff;border-radius:60px;padding:0 34px 10px;margin-bottom:10px;font-size:76px}')
K = "#151515"; FLOOR = 1720
# joint angles (deg, 0 = straight down): [back arm up, back arm low, front arm up, front arm low, back leg up, back leg low, front leg up, front leg low]
POSE = {
 "stand": [12, 0, -12, 0, 6, 0, -6, 0], "panic": [150, 30, -150, -30, 20, 10, -20, -10], "phone": [40, 140, -12, 0, 6, 0, -6, 0],
 "press": [10, 0, -80, -10, 6, 0, -6, 0], "point": [12, 0, -95, 0, 6, 0, -6, 0], "sit": [30, 40, -30, -40, 80, -80, 80, -80],
 "wave": [12, 0, -125, -40, 6, 0, -6, 0], "breathe": [60, 90, -60, -90, 6, 0, -6, 0], "no": [100, 60, -100, -60, 6, 0, -6, 0],
 "think": [12, 0, -40, -150, 6, 0, -6, 0], "cheer": [160, 10, -160, -10, 10, 0, -10, 0], "run": [60, 80, -70, -90, 45, -70, -40, -20],
 "walk1": [30, 20, -30, -20, 25, -10, -25, -5], "walk2": [-30, -20, 30, 20, -25, -5, 25, -10], "drive": [70, 40, -70, -40, 80, -80, 80, -80],
 "carry": [80, 70, -80, -70, 6, 0, -6, 0], "fall": [120, 30, -60, -20, 40, 20, -30, -30], "sad": [8, 0, -8, 0, 4, 0, -4, 0],
}
LOOKS = {  # ready outfits
 "man": dict(shirt="#e5322d", pants="#2b3a55", skin="#f1c7a0", hair="#3a2414", hs="short"),
 "woman": dict(shirt="#7a4fd1", pants="#2b3a55", skin="#f1c7a0", hair="#5a3418", hs="long", dress="#7a4fd1"),
 "hijab": dict(shirt="#2f9a6a", pants="#2b3a55", skin="#e9b98f", hair="#1f4a3a", hs="hijab", dress="#2f9a6a"),
 "boy": dict(shirt="#2b8be0", pants="#4a4a4a", skin="#f1c7a0", hair="#151515", hs="short", scale=.78),
 "girl": dict(shirt="#ff8a3a", pants="#2b3a55", skin="#e9b98f", hair="#3a2414", hs="long", dress="#ff8a3a", scale=.74),
 "old": dict(shirt="#8a6a4a", pants="#4a4a4a", skin="#e9b98f", hair="#d8d8d8", hs="bald", beard="#d8d8d8"),
 "worker": dict(shirt="#f2c94c", pants="#2b3a55", skin="#c98c5a", hair="#151515", hs="cap", cap="#f2c94c"),
 "doctor": dict(shirt="#ffffff", pants="#4f8ac9", skin="#f1c7a0", hair="#3a2414", hs="short"),
 "police": dict(shirt="#24456b", pants="#1a2a40", skin="#c98c5a", hair="#151515", hs="cap", cap="#1a2a40"),
 "chef": dict(shirt="#ffffff", pants="#151515", skin="#f1c7a0", hair="#3a2414", hs="chef"),
}
def cap_(w, L, col, extra=""): return f'<rect x="{-w/2}" y="{-w/2}" width="{w}" height="{L+w}" rx="{w/2}" fill="{col}" stroke="{K}" stroke-width="9"/>{extra}'
def limb(pid, n, x, y, a1, a2, L, w, c1, c2, end):
    return (f'<g id="{n}u{pid}" transform="translate({x} {y}) rotate({a1})">{cap_(w, L, c1)}'
            f'<g id="{n}l{pid}" transform="translate(0 {L}) rotate({a2})">{cap_(w-4, L-8, c2)}<g transform="translate(0 {L-8})">{end}</g></g></g>')
FACE = {
 "ok": '<circle cx="-26" cy="0" r="9"/><circle cx="26" cy="0" r="9"/><path d="M-24,34 Q0,52 24,34" stroke="#151515" stroke-width="7" fill="none" stroke-linecap="round"/>',
 "happy": '<path d="M-36,0 q10,-14 20,0 M16,0 q10,-14 20,0" stroke="#151515" stroke-width="7" fill="none"/><path d="M-30,28 Q0,66 30,28 Z" fill="#7a1a1a"/>',
 "fear": '<circle cx="-26" cy="-4" r="12" fill="#fff" stroke="#151515" stroke-width="5"/><circle cx="26" cy="-4" r="12" fill="#fff" stroke="#151515" stroke-width="5"/><circle cx="-26" cy="-2" r="5"/><circle cx="26" cy="-2" r="5"/><ellipse cx="0" cy="40" rx="14" ry="18"/>',
 "calm": '<path d="M-36,0 h22 M14,0 h22" stroke="#151515" stroke-width="7"/><path d="M-18,34 Q0,44 18,34" stroke="#151515" stroke-width="7" fill="none"/>',
 "sad": '<circle cx="-26" cy="4" r="9"/><circle cx="26" cy="4" r="9"/><path d="M-22,46 Q0,30 22,46" stroke="#151515" stroke-width="7" fill="none"/><path d="M-40,-20 l22,8 M40,-20 l-22,8" stroke="#151515" stroke-width="6"/>',
 "angry": '<circle cx="-26" cy="6" r="9"/><circle cx="26" cy="6" r="9"/><path d="M-44,-16 l30,12 M44,-16 l-30,12" stroke="#151515" stroke-width="8"/><path d="M-22,42 h44" stroke="#151515" stroke-width="7"/>',
 "wow": '<circle cx="-26" cy="-4" r="10"/><circle cx="26" cy="-4" r="10"/><circle cx="0" cy="40" r="14"/>',
}
def hair(L, hs):
    c = L["hair"]
    if hs == "short": return f'<path d="M-82,-8 Q-80,-100 0,-96 Q80,-100 82,-8 Q60,-58 0,-54 Q-60,-58 -82,-8Z" fill="{c}" stroke="{K}" stroke-width="8"/>', ""
    if hs == "long": return f'<path d="M-82,-8 Q-80,-100 0,-96 Q80,-100 82,-8 Q60,-58 0,-54 Q-60,-58 -82,-8Z" fill="{c}" stroke="{K}" stroke-width="8"/>', f'<path d="M-86,-20 Q-110,90 -70,140 L-40,60 M86,-20 Q110,90 70,140 L40,60" fill="{c}" stroke="{K}" stroke-width="8"/>'
    if hs == "hijab": return f'<path d="M-96,10 Q-100,-110 0,-108 Q100,-110 96,10 Q96,90 60,120 Q0,140 -60,120 Q-96,90 -96,10Z M-70,0 Q-70,70 0,82 Q70,70 70,0 Q70,-66 0,-70 Q-70,-66 -70,0Z" fill="{c}" fill-rule="evenodd" stroke="{K}" stroke-width="8"/>', f'<path d="M-90,60 Q-120,170 -70,200 H70 Q120,170 90,60 Q0,130 -90,60Z" fill="{c}" stroke="{K}" stroke-width="8"/>'
    if hs == "cap": return f'<path d="M-84,-14 Q-80,-104 0,-100 Q80,-104 84,-14Z" fill="{L.get("cap", c)}" stroke="{K}" stroke-width="8"/><path d="M-20,-24 H120 Q120,-6 84,-6 H-20Z" fill="{L.get("cap", c)}" stroke="{K}" stroke-width="8"/>', ""
    if hs == "chef": return f'<path d="M-70,-40 Q-120,-150 -40,-150 Q0,-210 40,-150 Q120,-150 70,-40Z" fill="#fff" stroke="{K}" stroke-width="8"/>', ""
    return f'<path d="M-82,10 Q-90,-30 -70,-40 M82,10 Q90,-30 70,-40" stroke="{c}" stroke-width="16" fill="none" stroke-linecap="round"/>', ""
def person(pid, p):
    L = dict(LOOKS.get(p.get("look", "man"), LOOKS["man"])); L.update(p.get("colors", {}))
    a = POSE[p.get("pose", "stand")]; sc = p.get("scale", L.get("scale", 1)) * (-1 if p.get("flip") else 1)
    sk, sh_, pa = L["skin"], L["shirt"], L["pants"]
    hand = f'<circle r="24" fill="{sk}" stroke="{K}" stroke-width="8"/>'; shoe = f'<ellipse cx="14" cy="10" rx="40" ry="20" fill="{K}"/>'
    legs = limb(pid, "l0", -26, 0, a[4], a[5], 110, 54, pa, pa, shoe) + limb(pid, "l1", 26, 0, a[6], a[7], 110, 54, pa, pa, shoe)
    back_arm = limb(pid, "a0", -64, -178, a[0], a[1], 96, 46, sh_, sh_, hand); front_arm = limb(pid, "a1", 64, -178, a[2], a[3], 96, 46, sh_, sh_, hand)
    dress = f'<path d="M-66,-60 L-100,90 Q0,110 100,90 L66,-60Z" fill="{L["dress"]}" stroke="{K}" stroke-width="9"/>' if L.get("dress") else ""
    torso = f'<path d="M-76,-206 Q0,-224 76,-206 L68,12 Q0,22 -68,12Z" fill="{sh_}" stroke="{K}" stroke-width="9"/>'
    if p.get("look") == "doctor": torso += '<path d="M0,-200 V8" stroke="#151515" stroke-width="5"/><rect x="20" y="-170" width="36" height="40" fill="#e5322d"/>'
    if p.get("look") == "police": torso += '<path d="M-30,-160 l10,30 l20,-10 l20,10 l10,-30 z" fill="#f2c94c" stroke="#151515" stroke-width="4"/>'
    hf, hb = hair(L, L["hs"]); beard = f'<path d="M-60,30 Q0,120 60,30 Q0,70 -60,30Z" fill="{L["beard"]}" stroke="{K}" stroke-width="6"/>' if L.get("beard") else ""
    head = f'<g id="hd{pid}" transform="translate(0 -290)">{hb}<circle r="84" fill="{sk}" stroke="{K}" stroke-width="9"/><g fill="#151515">{FACE[p.get("face", "ok")]}</g>{beard}{hf}</g>'
    x = p.get("x", 540); y = p.get("y", FLOOR - 230 * abs(sc))
    return f'<g transform="translate({x} {y})"><g id="pp{pid}" transform="translate(0 0) scale({sc} {abs(sc)})">{back_arm}{legs}{dress}{torso}{front_arm}{head}</g></g>'
BASE = {"a0u": (-64, -178), "a0l": (0, 96), "a1u": (64, -178), "a1l": (0, 96), "l0u": (-26, 0), "l0l": (0, 110), "l1u": (26, 0), "l1l": (0, 110)}
def to_pose(pid, pose, at, d=.35, ease="back.out(1.6)"):
    p = POSE[pose]; js = []
    for k, n in enumerate(["a0u", "a0l", "a1u", "a1l", "l0u", "l0l", "l1u", "l1l"]):
        bx, by = BASE[n]; js.append(f'tl.to("#{n}{pid}",{{attr:{{transform:"translate({bx} {by}) rotate({p[k]})"}},duration:{d},ease:"{ease}"}},{at:.2f});')
    return js
# ------------------------------------------------------------------ places (1080x1920, floor at y 1720)
def place(name, i):
    s = ""
    if name == "elevator":
        s = ('<rect width="1080" height="1920" fill="#f4f1ea"/><rect x="150" y="560" width="780" height="1180" fill="#dcd6c8" stroke="#151515" stroke-width="12"/><path d="M540,560 V1740" stroke="#151515" stroke-width="6" stroke-dasharray="20 14"/>'
             '<rect x="820" y="900" width="80" height="260" rx="14" fill="#fff" stroke="#151515" stroke-width="8"/>' + "".join(f'<circle cx="860" cy="{940+k*60}" r="18" fill="{"#e5322d" if k==3 else "#fff"}" stroke="#151515" stroke-width="5"/>' for k in range(4)))
    elif name == "house":
        s = ('<rect width="1080" height="1920" fill="#f3e2c4"/><rect y="1720" width="1080" height="200" fill="#b98552"/>' + "".join(f'<path d="M{k*180},1720 v200" stroke="#9a6a3c" stroke-width="5"/>' for k in range(7)) +
             '<rect x="620" y="640" width="320" height="380" fill="#bfe3f5" stroke="#151515" stroke-width="10"/><path d="M780,640 V1020 M620,830 H940" stroke="#151515" stroke-width="8"/><path d="M600,620 Q640,840 600,1060 H660 Q690,840 660,620Z M960,620 Q920,840 960,1060 H900 Q870,840 900,620Z" fill="#e5322d" stroke="#151515" stroke-width="6"/>'
             '<rect x="110" y="1440" width="560" height="200" rx="40" fill="#5a7fbf" stroke="#151515" stroke-width="10"/><rect x="90" y="1360" width="600" height="120" rx="40" fill="#6a8fcf" stroke="#151515" stroke-width="10"/><rect x="140" y="1630" width="30" height="90" fill="#151515"/><rect x="610" y="1630" width="30" height="90" fill="#151515"/>'
             '<rect x="200" y="700" width="220" height="160" fill="#fff" stroke="#151515" stroke-width="8"/><path d="M220,840 l60,-70 l40,40 l40,-60 l40,90z" fill="#7fbf3f"/><path d="M880,1720 V1200" stroke="#151515" stroke-width="10"/><path d="M820,1200 h120 l-30,-110 h-60z" fill="#f2c94c" stroke="#151515" stroke-width="8"/>')
    elif name == "kitchen":
        s = ('<rect width="1080" height="1920" fill="#fdf6ea"/>' + "".join(f'<rect x="{c*90}" y="{900+r*90}" width="90" height="90" fill="{"#dff1ff" if (r+c)%2 else "#fff"}" stroke="#c9d6e0" stroke-width="3"/>' for r in range(6) for c in range(12)) +
             '<rect y="1720" width="1080" height="200" fill="#9aa8b6"/><rect x="0" y="1300" width="700" height="420" fill="#c98f45" stroke="#151515" stroke-width="10"/><rect x="0" y="1270" width="720" height="40" fill="#e8e2d0" stroke="#151515" stroke-width="8"/>'
             '<rect x="300" y="1340" width="300" height="260" fill="#3a3e44" stroke="#151515" stroke-width="8"/><rect x="330" y="1370" width="240" height="160" fill="#151515"/><rect x="330" y="1210" width="200" height="70" rx="10" fill="#9aa8b6" stroke="#151515" stroke-width="8"/>'
             '<rect x="820" y="1000" width="230" height="720" rx="20" fill="#e8eef5" stroke="#151515" stroke-width="10"/><path d="M820,1300 h230 M850,1100 v120 M850,1340 v160" stroke="#151515" stroke-width="8"/>'
             '<rect x="40" y="620" width="620" height="220" fill="#c98f45" stroke="#151515" stroke-width="10"/><path d="M350,620 v220" stroke="#151515" stroke-width="8"/>')
    elif name == "street":
        s = ('<rect width="1080" height="1920" fill="#9fd4f5"/>' + "".join(f'<rect x="{x}" y="{y}" width="{w}" height="{1500-y}" fill="{c}" stroke="#151515" stroke-width="8"/>' + "".join(f'<rect x="{x+20+cc*60}" y="{y+30+rr*90}" width="34" height="50" fill="#fbe9a8"/>' for rr in range(int((1450-y)/90)) for cc in range(int((w-30)/60)))
              for x, y, w, c in ((-20, 700, 300, "#c98f45"), (280, 520, 260, "#8a9ab0"), (540, 820, 240, "#d9a85a"), (780, 600, 320, "#b86a5a"))) +
             '<rect y="1500" width="1080" height="120" fill="#cfcfcf" stroke="#151515" stroke-width="6"/><rect y="1620" width="1080" height="300" fill="#4a4e55"/>' + "".join(f'<rect class="rl{i}" x="{k*240}" y="1760" width="130" height="18" fill="#fff"/>' for k in range(6)) +
             '<path d="M960,1500 V1050 q0,-40 -60,-40" stroke="#151515" stroke-width="14" fill="none"/><ellipse cx="890" cy="1015" rx="40" ry="16" fill="#f2c94c" stroke="#151515" stroke-width="6"/>')
    elif name == "forest":
        s = ('<rect width="1080" height="1920" fill="#bfe6c4"/><rect y="1500" width="1080" height="420" fill="#6fbf4f"/><path d="M380,1920 Q520,1650 560,1500 H640 Q640,1650 760,1920Z" fill="#d9b070"/>' +
             "".join(f'<g class="tr{i}" transform="translate({x} {y}) scale({sc})"><rect x="-22" y="-20" width="44" height="260" fill="#7a4a24" stroke="#151515" stroke-width="7"/><circle cy="-120" r="150" fill="{c}" stroke="#151515" stroke-width="8"/><circle cx="-90" cy="-40" r="100" fill="{c}" stroke="#151515" stroke-width="8"/><circle cx="90" cy="-40" r="100" fill="{c}" stroke="#151515" stroke-width="8"/></g>'
                     for x, y, sc, c in ((120, 1300, .8, "#3f9a4a"), (920, 1280, .9, "#2f8a3a"), (330, 1180, .55, "#4fae5a"), (760, 1160, .5, "#4fae5a"), (60, 1600, 1.0, "#2f8a3a"), (1010, 1620, 1.0, "#3f9a4a"))))
    elif name == "sea":
        s = ('<rect width="1080" height="1920" fill="#8fd3ff"/><circle cx="820" cy="560" r="110" fill="#ffe27a"/><rect y="1050" width="1080" height="500" fill="#2b8be0"/>' +
             "".join(f'<path class="wv{i}" d="M{-200+k*0},{1100+r*90} q90,-30 180,0 t180,0 t180,0 t180,0 t180,0 t180,0 t180,0" stroke="#bfe6ff" stroke-width="10" fill="none"/>' for r, k in ((0, 0), (1, 1), (2, 2), (3, 3))) +
             '<path d="M0,1500 Q540,1440 1080,1500 V1920 H0Z" fill="#f2d79a"/><path d="M820,1720 V1300" stroke="#151515" stroke-width="12"/><path d="M620,1320 Q820,1140 1020,1320Z" fill="#e5322d" stroke="#151515" stroke-width="9"/>')
    elif name == "office":
        s = ('<rect width="1080" height="1920" fill="#e8eef5"/><rect y="1720" width="1080" height="200" fill="#8a9ab0"/><rect x="120" y="560" width="840" height="520" fill="#bfe3f5" stroke="#151515" stroke-width="10"/>' +
             "".join(f'<rect x="{150+k*130}" y="{760+(k%3)*60}" width="100" height="{320-(k%3)*60}" fill="#8a9ab0"/>' for k in range(6)) + '<path d="M540,560 V1080" stroke="#151515" stroke-width="8"/>'
             '<rect x="360" y="1380" width="640" height="40" fill="#c98f45" stroke="#151515" stroke-width="8"/><rect x="390" y="1420" width="30" height="300" fill="#151515"/><rect x="940" y="1420" width="30" height="300" fill="#151515"/>'
             '<rect x="560" y="1160" width="300" height="200" rx="10" fill="#3a3e44" stroke="#151515" stroke-width="8"/><rect x="580" y="1180" width="260" height="150" fill="#7cc6ff"/><rect x="690" y="1360" width="40" height="22" fill="#151515"/>'
             '<path d="M120,1720 l30,-200 h120 l30,200z" fill="#c98f45" stroke="#151515" stroke-width="8"/><path d="M210,1520 q-90,-120 -40,-220 q30,90 40,0 q40,90 60,0 q60,110 -60,220" fill="#3f9a4a" stroke="#151515" stroke-width="7"/>')
    elif name == "car":
        s = ('<rect width="1080" height="1920" fill="#8fd3ff"/><rect y="980" width="1080" height="400" fill="#6fbf4f"/><path d="M380,980 L-200,1500 H1280 L700,980Z" fill="#4a4e55"/>' +
             "".join(f'<path class="cl{i}" d="M540,{1010+k*120} v60" stroke="#fff" stroke-width="{10+k*8}"/>' for k in range(4)) +
             '<path d="M0,500 H1080 V1380 H0Z M70,560 Q540,500 1010,560 L960,1300 H120Z" fill="#2b2f36" fill-rule="evenodd"/><rect y="1380" width="1080" height="540" fill="#3a3e44"/>'
             '<rect y="1340" width="1080" height="120" fill="#24282e" stroke="#151515" stroke-width="8"/><circle cx="820" cy="1400" r="40" fill="#151515" stroke="#7cc6ff" stroke-width="6"/>')
    return s
FX = {
 "fire": lambda x, y, i: f'<g class="fx{i}" transform="translate({x} {y})">' + "".join(f'<path class="fl{i}" d="M{dx},0 Q{dx-60},-120 {dx},-{h} Q{dx+60},-120 {dx},0Z" fill="{c}" stroke="#151515" stroke-width="5"/>' for dx, h, c in ((-50, 170, "#ff8a2a"), (40, 220, "#e5322d"), (0, 150, "#f2c94c"))) + '</g>',
 "rain": lambda x, y, i: "".join(f'<path class="rn{i}" d="M{(R(k)+1)*540:.0f},{(R(k+30)+1)*700:.0f} l-20,60" stroke="#2b8be0" stroke-width="7" stroke-linecap="round"/>' for k in range(50)),
 "idea": lambda x, y, i: f'<g class="fx{i}" transform="translate({x} {y})"><circle r="56" fill="#ffe27a" stroke="#151515" stroke-width="8"/><rect x="-26" y="50" width="52" height="40" fill="#9aa8b6" stroke="#151515" stroke-width="7"/><path d="M-90,-70 l-26,-26 M90,-70 l26,-26 M0,-90 v-36" stroke="#f2c94c" stroke-width="10"/></g>',
 "question": lambda x, y, i: f'<text class="fx{i}" x="{x}" y="{y}" font-size="190" font-weight="900" fill="#2b8be0" stroke="#151515" stroke-width="6" text-anchor="middle" font-family="Cairo">؟</text>',
 "exclaim": lambda x, y, i: f'<text class="fx{i}" x="{x}" y="{y}" font-size="200" font-weight="900" fill="#e5322d" stroke="#151515" stroke-width="6" text-anchor="middle" font-family="Cairo">!</text>',
 "heart": lambda x, y, i: f'<path class="fx{i}" transform="translate({x} {y})" d="M0,50 C-130,-30 -100,-150 0,-90 C100,-150 130,-30 0,50Z" fill="#ff4d6d" stroke="#151515" stroke-width="8"/>',
 "zzz": lambda x, y, i: f'<text class="fx{i}" x="{x}" y="{y}" font-size="110" font-weight="900" fill="#7a4fd1" font-family="Cairo">Z z z</text>',
 "sweat": lambda x, y, i: f'<path class="fx{i}" transform="translate({x-170} {y+80})" d="M0,0 Q-30,50 0,70 Q30,50 0,0Z" fill="#7cc6ff" stroke="#151515" stroke-width="5"/>',
 "check": lambda x, y, i: f'<path class="fx{i}" d="M{x-70},{y} l50,50 l100,-110" stroke="#2f9a46" stroke-width="30" fill="none" stroke-linecap="round" stroke-linejoin="round"/>',
 "cross": lambda x, y, i: f'<path class="fx{i}" d="M{x-80},{y-80} L{x+80},{y+80} M{x+80},{y-80} L{x-80},{y+80}" stroke="#e5322d" stroke-width="30" stroke-linecap="round"/>',
 "phone": lambda x, y, i: f'<g class="fx{i}" transform="translate({x} {y})"><rect x="-50" y="-90" width="100" height="180" rx="16" fill="#3a3e44" stroke="#151515" stroke-width="8"/><rect x="-36" y="-72" width="72" height="130" fill="#7cc6ff"/><path d="M70,-60 q30,40 0,80 M100,-80 q50,60 0,120" stroke="#151515" stroke-width="8" fill="none"/></g>',
 "bell": lambda x, y, i: f'<g class="fx{i}" transform="translate({x} {y})"><path d="M-50,40 Q-50,-50 0,-60 Q50,-50 50,40 Z" fill="#f2c94c" stroke="#151515" stroke-width="7"/><path d="M-80,-60 q-20,30 0,60 M80,-60 q20,30 0,60" stroke="#151515" stroke-width="7" fill="none"/></g>',
 "clock": lambda x, y, i: f'<g transform="translate({x} {y})"><circle r="80" fill="#fff" stroke="#151515" stroke-width="8"/><path class="hand{i}" d="M0,0 V-60" stroke="#151515" stroke-width="8" stroke-linecap="round"/></g>',
 "smoke": lambda x, y, i: "".join(f'<circle class="sm{i}" cx="{x+R(k)*60:.0f}" cy="{y}" r="{50+k*8}" fill="#8a8a8a" opacity=".55"/>' for k in range(6)),
 "air": lambda x, y, i: "".join(f'<circle class="sm{i}" cx="{x-200+k*100}" cy="{y+300}" r="{20+k%3*8}" fill="none" stroke="#7ab0c8" stroke-width="6"/>' for k in range(5)),
 "money": lambda x, y, i: "".join(f'<rect class="mn{i}" x="{x-60+R(k)*120:.0f}" y="{y-400-k*90}" width="120" height="60" rx="8" fill="#7fbf7f" stroke="#151515" stroke-width="5"/>' for k in range(8)),
}
def fx_js(kind, i, s, e):
    if kind == "fire": return [f'tl.fromTo("#S{i} .fl{i}",{{scaleY:.8,transformOrigin:"50% 100%"}},{{scaleY:1.15,duration:.18,yoyo:true,repeat:{int((e-s+1)/.18)},stagger:.06}},{s:.2f});']
    if kind == "rain": return [f'tl.fromTo("#S{i} .rn{i}",{{y:-200}},{{y:1500,duration:1,repeat:{int(e-s+2)},ease:"none",stagger:.02}},{s-.3:.2f});']
    if kind in ("smoke", "air"): return [f'tl.fromTo("#S{i} .sm{i}",{{y:0,opacity:.7}},{{y:-500,opacity:0,duration:2,stagger:.25,ease:"none"}},{s+.3:.2f});']
    if kind == "money": return [f'tl.fromTo("#S{i} .mn{i}",{{y:-300,rotation:0}},{{y:900,rotation:180,duration:1.6,stagger:.15,ease:"none"}},{s+.3:.2f});']
    if kind == "clock": return [f'tl.to("#S{i} .hand{i}",{{rotation:720,svgOrigin:"0 0",duration:{e-s:.2f},ease:"none"}},{s:.2f});']
    if kind in ("bell", "phone"): return [f'tl.fromTo("#S{i} .fx{i}",{{rotation:-12}},{{rotation:12,duration:.09,yoyo:true,repeat:15,transformOrigin:"50% 0%"}},{s+.6:.2f});']
    return [f'tl.fromTo("#S{i} .fx{i}",{{opacity:0,scale:.2,transformOrigin:"50% 50%"}},{{opacity:1,scale:1,duration:.35,ease:"back.out(2.2)"}},{s+.7:.2f});']
def scene(i, b, s, e, c0, c1):
    js = []; pl = b.get("place", "elevator")
    people = b.get("people") or [{"look": b.get("look", "man"), "x": b.get("x", 420), "pose": b.get("pose", "stand"), "face": b.get("face", "ok")}]
    fxs = b.get("fx", []); fxs = [fxs] if isinstance(fxs, str) else fxs
    over = ""
    p0 = people[0]; hx, hy = p0.get("x", 420) + 190, 1050
    for f in fxs:
        if f in ("shake", "open", "walk"): continue
        svg = FX[f](*(b.get("fx_at") or ((p0.get("x", 420), 1700) if f in ("fire", "smoke") else (hx, hy))), i)
        over += svg
        js += fx_js(f, i, s, e)
    doors = ""
    if "open" in fxs and pl == "elevator":
        doors = f'<rect id="dl{i}" x="150" y="560" width="390" height="1180" fill="#b8b2a4" stroke="#151515" stroke-width="8"/><rect id="dr{i}" x="540" y="560" width="390" height="1180" fill="#b8b2a4" stroke="#151515" stroke-width="8"/>'
        js += [f'tl.fromTo("#dl{i}",{{x:0}},{{x:-380,duration:.8,ease:"power2.inOut"}},{s+.3:.2f});', f'tl.fromTo("#dr{i}",{{x:0}},{{x:380,duration:.8,ease:"power2.inOut"}},{s+.3:.2f});']
    figs = ""
    for n, p in enumerate(people):
        pid = f"{i}_{n}"; final = p.get("pose", "stand"); p2 = dict(p); p2["pose"] = "stand" if final not in ("sit", "drive") else final
        if pl == "car" and "x" not in p: p2["x"] = 380; p2["y"] = 1560
        figs += person(pid, p2)
        if final not in ("sit", "drive"): js += to_pose(pid, final, s + .3 + n * .15)
        if p.get("walk_to") is not None:
            x0 = p2.get("x", 540); sc = p2.get("scale", 1)
            js.append(f'tl.fromTo("#pp{pid}",{{x:0}},{{x:{p["walk_to"]-x0},duration:{max(1, e-s-.6):.2f},ease:"none"}},{s:.2f});')
            for k in range(int(max(1, e - s - .6) / .3)): js += to_pose(pid, "walk1" if k % 2 == 0 else "walk2", s + k * .3, .3, "sine.inOut")
            js += to_pose(pid, final, s + max(1, e - s - .6))
        js.append(f'tl.fromTo("#hd{pid}",{{rotation:-3}},{{rotation:3,svgOrigin:"0 -210",duration:.5,yoyo:true,repeat:{int((c1-c0)/.5)},ease:"sine.inOut"}},{c0:.2f});')
    if pl == "street": js.append(f'tl.fromTo("#S{i} .rl{i}",{{x:0}},{{x:-240,duration:.8,repeat:{int((c1-c0)/.8)},ease:"none"}},{c0:.2f});')
    if pl == "car": js.append(f'tl.fromTo("#S{i} .cl{i}",{{y:0,opacity:1}},{{y:400,opacity:0,duration:.7,repeat:{int((c1-c0)/.7)},ease:"power1.in",stagger:.17}},{c0:.2f});')
    if pl == "sea": js.append(f'tl.fromTo("#S{i} .wv{i}",{{x:0}},{{x:-180,duration:1.2,repeat:{int((c1-c0)/1.2)},ease:"none"}},{c0:.2f});')
    if pl == "forest": js.append(f'tl.fromTo("#S{i} .tr{i}",{{rotation:-1.5}},{{rotation:1.5,transformOrigin:"50% 100%",duration:1.4,yoyo:true,repeat:{int((c1-c0)/1.4)},ease:"sine.inOut"}},{c0:.2f});')
    car_front = '<path d="M0,1460 H1080 V1920 H0Z" fill="#3a3e44"/><g transform="translate(380 1420)"><circle r="150" fill="none" stroke="#151515" stroke-width="34"/><path d="M-150,0 H150 M0,0 V150" stroke="#151515" stroke-width="26"/></g>' if pl == "car" else ""
    h = f'<svg class="full" width="1080" height="1920" viewBox="0 0 1080 1920"><g id="bg{i}">{place(pl, i)}</g>{figs}{car_front}{doors}{over}</svg>'
    h += f'<div class="cap" id="cp{i}" style="opacity:0"><span class="bx">{b["cap"]}</span></div>'
    js.append(f'tl.fromTo("#cp{i}",{{opacity:0,scale:.6}},{{opacity:1,scale:1,duration:.35,ease:"back.out(2)"}},{s:.2f});')
    if "shake" in fxs: js.append(f'tl.fromTo("#S{i} svg",{{x:0}},{{x:16,duration:.05,yoyo:true,repeat:11}},{s+.2:.2f});')
    js.append(f'tl.fromTo("#bg{i}",{{scale:1}},{{scale:1.04,transformOrigin:"50% 60%",duration:{c1-c0:.2f},ease:"none"}},{c0:.2f});')
    return h, js
if __name__ == "__main__":
    ep = load(); B = ep["beats"]
    def sfx(sch):
        out = []
        for k, b in enumerate(B):
            f = b.get("fx", []); f = [f] if isinstance(f, str) else f
            if "bell" in f or "phone" in f: out.append({"file": "sfx/bell.wav", "at": round(sch[k][0] + .6, 2), "gain": .2})
            if set(f) & {"cross", "exclaim", "shake"}: out.append({"file": "sfx/hit.wav", "at": round(sch[k][0] + .7, 2), "gain": .25})
        return out
    run("stick", B, scene, css=CSS, bg="#f4f1ea", rate="+0%", extra_sfx=sfx)
