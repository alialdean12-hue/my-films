"""saw_5tory people v3: characters built from different SHAPES (face, eyes, nose, brows, build, pose, hair, accessories),
not only different colours. person(...) keeps the ids the builder animates: <id>_body, <id>_open, <id>_shut, <id>_pup, tag_<id>.
Use cast="<name>" for a ready character from CAST, then override any key."""

LINE = "#2a1a12"
SKINS = {"light": "#f3d2b8", "medium": "#e2b48e", "tan": "#c98f62", "brown": "#9a6640", "dark": "#6b4429", "pale": "#f6e0d2"}
CX = 490

FACES = {  # half width, top, cheek y, chin y, jaw style
    "oval":   (60, 720, 800, 916, "curve"),
    "round":  (68, 726, 812, 904, "round"),
    "square": (64, 722, 806, 908, "square"),
    "long":   (54, 712, 800, 932, "curve"),
    "heart":  (64, 722, 798, 918, "point"),
    "wide":   (74, 732, 816, 900, "round"),
    "diamond": (62, 716, 812, 922, "point"),
}

def _face_path(shape):
    hw, top, cy, chin, jaw = FACES[shape]
    l, r = CX - hw, CX + hw
    head = f"M{l},{cy} C{l},{top} {r},{top} {r},{cy}"
    if jaw == "square":
        return head + f" L{r},{cy+64} Q{r},{chin-4} {CX+40},{chin} L{CX-40},{chin} Q{l},{chin-4} {l},{cy+64} Z"
    if jaw == "round":
        return head + f" C{r},{cy+70} {CX+50},{chin} {CX},{chin} C{CX-50},{chin} {l},{cy+70} {l},{cy} Z"
    if jaw == "point":
        return head + f" C{r},{cy+50} {CX+20},{chin-12} {CX},{chin} C{CX-20},{chin-12} {l},{cy+50} {l},{cy} Z"
    return head + f" C{r},{cy+70} {CX+30},{chin-4} {CX},{chin} C{CX-30},{chin-4} {l},{cy+70} {l},{cy} Z"

def _eyes(id_, shape, kind, expression, iris):
    hw, top, cy, chin, _ = FACES[shape]
    ey = cy + 30; dx = max(22, int(hw * 0.38))
    xs = (CX - dx, CX + dx)
    if expression == "scared": kind = "round"
    if expression == "smug" and kind in ("normal", "round"): kind = "narrow"
    o = [f'<g id="{id_}_open">']
    for x in xs:
        if kind == "round":
            o.append(f'<ellipse cx="{x}" cy="{ey}" rx="12" ry="12" fill="#f6f3ee"/>')
        elif kind == "narrow":
            o.append(f'<ellipse cx="{x}" cy="{ey}" rx="13" ry="5" fill="#f6f3ee"/>')
        elif kind == "big":
            o.append(f'<ellipse cx="{x}" cy="{ey}" rx="15" ry="13" fill="#f6f3ee"/><path d="M{x-16},{ey-6} Q{x},{ey-18} {x+16},{ey-6}" stroke="{LINE}" stroke-width="4" fill="none"/>')
        elif kind == "sharp":
            o.append(f'<path d="M{x-15},{ey+2} Q{x-4},{ey-10} {x+15},{ey-4} Q{x+4},{ey+8} {x-15},{ey+2} Z" fill="#f6f3ee"/>')
        else:  # normal / droopy
            o.append(f'<ellipse cx="{x}" cy="{ey}" rx="12" ry="9" fill="#f6f3ee"/>')
    pr = {"narrow": 4, "big": 9, "round": 7}.get(kind, 6)
    o.append(f'<g id="{id_}_pup">' + "".join(
        (f'<circle cx="{x+2}" cy="{ey+1}" r="{pr}" fill="{iris}"/><circle cx="{x+2}" cy="{ey+1}" r="{max(3,pr-4)}" fill="{LINE}"/><circle cx="{x+5}" cy="{ey-3}" r="2.5" fill="#fff"/>'
         if kind == "big" else f'<circle cx="{x+2}" cy="{ey+1}" r="{pr}" fill="{LINE}"/>') for x in xs) + '</g>')
    if kind == "droopy":
        o.append("".join(f'<path d="M{x-14},{ey-1} Q{x},{ey-12} {x+14},{ey-1} Z" fill="SKIN"/><path d="M{x-14},{ey-1} Q{x},{ey-6} {x+14},{ey-1}" stroke="{LINE}" stroke-width="3" fill="none"/>' for x in xs))
    o.append('</g>')
    o.append(f'<path id="{id_}_shut" d="' + " ".join(f"M{x-12},{ey+2} Q{x},{ey+8} {x+12},{ey+2}" for x in xs) + f'" stroke="{LINE}" stroke-width="4" fill="none" opacity="0"/>')
    return "".join(o), xs, ey

def _brows(shape, xs, ey, expression, kind, color):
    w = {"thin": 4, "thick": 7, "bushy": 11}.get(kind, 5)
    y = ey - 16
    tilt = {"neutral": (4, 0), "nervous": (-6, 2), "smug": (0, 4), "scared": (-8, -4), "angry": (10, 0)}[expression]
    l, r = xs
    return (f'<path d="M{l-14},{y-tilt[1]} L{l+14},{y+tilt[0]-tilt[1]} M{r-14},{y+tilt[0]-tilt[1]} L{r+14},{y-tilt[1]}" '
            f'stroke="{color}" stroke-width="{w}" stroke-linecap="round"/>')

def _nose(shape, kind, skin_dark):
    hw, top, cy, chin, _ = FACES[shape]
    y = cy + 44
    d = {"line": f'<path d="M{CX-2},{y} l-6,22 l10,2" stroke="{skin_dark}" stroke-width="3.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>',
         "button": f'<path d="M{CX-9},{y+20} q9,10 18,0" stroke="{skin_dark}" stroke-width="4" fill="none" stroke-linecap="round"/>',
         "long": f'<path d="M{CX},{y-14} l-10,40 l14,4" stroke="{skin_dark}" stroke-width="3.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>',
         "wide": f'<path d="M{CX-16},{y+18} q16,12 32,0" stroke="{skin_dark}" stroke-width="4" fill="none"/><circle cx="{CX-8}" cy="{y+22}" r="2.5" fill="{skin_dark}"/><circle cx="{CX+8}" cy="{y+22}" r="2.5" fill="{skin_dark}"/>',
         "hook": f'<path d="M{CX+2},{y-12} q-18,30 -6,40 q8,2 14,-3" stroke="{skin_dark}" stroke-width="3.5" fill="none" stroke-linecap="round"/>'}
    return d.get(kind, d["line"])

def _mouth(shape, expression, gender, lips):
    hw, top, cy, chin, _ = FACES[shape]
    y = min(cy + 80, chin - 26)
    m = {"neutral": f"M{CX-12},{y} Q{CX},{y-6} {CX+12},{y}", "nervous": f"M{CX-14},{y+2} Q{CX-7},{y-4} {CX},{y+2} Q{CX+7},{y-4} {CX+14},{y+2}",
         "smug": f"M{CX-14},{y-2} Q{CX+4},{y+8} {CX+16},{y-8}", "scared": f"M{CX-9},{y-4} Q{CX},{y+16} {CX+9},{y-4} Z", "angry": f"M{CX-14},{y+4} Q{CX},{y-6} {CX+14},{y+4}",
         "happy": f"M{CX-16},{y-4} Q{CX},{y+12} {CX+16},{y-4}"}[expression]
    col = lips or ("#b0444a" if gender == "f" else "#7a3a2a")
    return f'<path d="{m}" stroke="{col}" stroke-width="4" fill="{"#3a1a14" if expression=="scared" else "none"}" stroke-linecap="round"/>', y

# ---------------------------------------------------------------- hair (drawn in "oval" space then fitted to the face)
def _fit(shape):
    hw, top, cy, chin, _ = FACES[shape]
    return f'transform="translate({CX} {top-720}) scale({hw/60:.3f} 1) translate({-CX} 0)"'

BACK_HAIR = {
    "long": '<path d="M426,780 Q420,700 490,698 Q562,700 556,780 L566,1010 Q490,1040 414,1010 Z" fill="H"/>',
    "wavy": '<path d="M422,780 Q416,696 490,694 Q566,696 560,780 Q586,860 560,930 Q584,990 556,1030 Q490,1050 424,1030 Q396,990 420,930 Q394,860 422,780 Z" fill="H"/>',
    "ponytail": '<path d="M540,730 Q600,760 590,860 Q584,930 600,990 Q560,960 556,880 Q560,800 530,760 Z" fill="H"/>',
    "braid": '<g fill="H"><circle cx="560" cy="880" r="16"/><circle cx="566" cy="912" r="15"/><circle cx="570" cy="942" r="14"/><circle cx="572" cy="970" r="13"/><circle cx="572" cy="996" r="11"/></g>',
}
FRONT_HAIR = {
    "spiky": '<path d="M424,800 Q420,720 490,712 Q560,716 556,800 L540,770 L526,800 L508,766 L490,802 L470,768 L452,800 L440,776 Z" fill="H"/>',
    "short": '<path d="M428,796 Q426,716 490,712 Q556,716 552,796 Q540,758 490,756 Q440,758 428,796 Z" fill="H"/>',
    "side_part": '<path d="M428,800 Q424,714 492,710 Q558,716 554,800 Q546,766 520,752 Q470,746 452,772 Q440,786 428,800 Z" fill="H"/><path d="M470,716 Q478,736 470,756" stroke="#000" stroke-opacity=".25" stroke-width="3" fill="none"/>',
    "buzz": '<path d="M432,792 Q430,720 490,716 Q552,720 548,792 Q540,760 490,758 Q440,760 432,792 Z" fill="H" fill-opacity=".55"/>',
    "curly": '<g fill="H"><circle cx="430" cy="752" r="22"/><circle cx="450" cy="742" r="22"/><circle cx="470" cy="752" r="22"/><circle cx="490" cy="742" r="22"/><circle cx="510" cy="752" r="22"/><circle cx="530" cy="742" r="22"/><circle cx="550" cy="752" r="22"/><circle cx="436" cy="792" r="16"/><circle cx="546" cy="792" r="16"/></g>',
    "long": '<path d="M426,812 Q428,712 490,708 Q556,712 556,812 Q540,764 500,752 Q468,776 438,812 Z" fill="H"/>',
    "wavy": '<path d="M424,814 Q426,710 490,706 Q558,710 558,814 Q546,770 520,756 Q500,780 476,762 Q452,780 438,812 Z" fill="H"/>',
    "ponytail": '<path d="M428,800 Q426,716 490,712 Q556,716 552,800 Q540,756 490,752 Q440,756 428,800 Z" fill="H"/>',
    "braid": '<path d="M428,800 Q426,716 490,712 Q556,716 552,800 Q540,756 490,752 Q440,756 428,800 Z" fill="H"/>',
    "bun": '<circle cx="490" cy="700" r="30" fill="H"/><path d="M428,800 Q426,716 490,712 Q556,716 552,800 Q540,756 490,752 Q440,756 428,800 Z" fill="H"/>',
    "bald": '<path d="M430,806 q-2,-22 8,-30 M550,806 q2,-22 -8,-30" stroke="H" stroke-width="12" stroke-linecap="round" fill="none"/><path d="M462,734 Q490,726 518,734" stroke="#fff" stroke-opacity=".35" stroke-width="5" fill="none"/>',
    "receding": '<path d="M428,800 Q426,750 446,736 L452,780 Q440,790 428,800 Z M552,800 Q554,750 534,736 L528,780 Q540,790 552,800 Z" fill="H"/><path d="M466,726 Q490,720 514,726" stroke="H" stroke-width="6" fill="none"/>',
    "mohawk": '<path d="M476,740 L470,690 L486,712 L490,680 L498,712 L512,690 L506,740 Z" fill="H"/><path d="M432,792 Q430,730 490,724 Q550,730 548,792" fill="none" stroke="H" stroke-opacity=".4" stroke-width="10"/>',
}

def _hair(style, color, accent, shape, layer):
    fit = _fit(shape)
    if style == "hijab":
        if layer == "back": return f'<g {fit}><path d="M418,800 Q414,690 490,686 Q566,690 562,800 L590,1000 Q490,1040 390,1000 Z" fill="{accent}"/></g>'
        return f'<g {fit}><path d="M428,806 Q426,712 490,708 Q554,712 552,806" fill="none" stroke="{accent}" stroke-width="18"/><path d="M432,860 Q440,930 490,946 Q540,930 548,860 L560,980 L420,980 Z" fill="{accent}"/></g>'
    if style == "shemagh":
        if layer == "back": return f'<g {fit}><path d="M412,790 Q410,690 490,684 Q570,690 568,790 L600,1010 L380,1010 Z" fill="#f2f2f2"/></g>'
        return f'<g {fit}><path d="M424,806 Q426,712 490,708 Q554,712 556,806" fill="none" stroke="#f2f2f2" stroke-width="18"/><path d="M424,748 Q490,724 556,748" stroke="#111" stroke-width="12" fill="none"/><path d="M426,764 Q490,740 554,764" stroke="#111" stroke-width="8" fill="none"/></g>'
    src = (BACK_HAIR if layer == "back" else FRONT_HAIR).get(style, "")
    return f'<g {fit}>' + src.replace('"H"', f'"{color}"') + '</g>' if src else ""

# ---------------------------------------------------------------- body
BUILDS = {  # shoulder half-width, hem half-width, hem y, arm thickness, belly
    "normal": (90, 110, 1280, 44, 0), "broad": (114, 100, 1280, 52, 0), "slim": (74, 84, 1280, 36, 0),
    "stocky": (104, 118, 1290, 52, 0), "pear": (80, 132, 1290, 42, 0), "belly": (96, 112, 1290, 50, 60),
}

def _torso_path(build):
    sw, hw, hem, _, belly = BUILDS[build]
    if belly:
        return f"M{CX-sw},960 Q{CX},930 {CX+sw},960 Q{CX+sw+belly},1130 {CX+hw},{hem} L{CX-hw},{hem} Q{CX-sw-belly},1130 {CX-sw},960 Z"
    return f"M{CX-sw},960 Q{CX},930 {CX+sw},960 L{CX+hw},{hem} L{CX-hw},{hem} Z"

def _arms(build, pose, color, skin, face_shape):
    sw, hw, hem, t, belly = BUILDS[build]
    L_, R_ = (CX - sw + 10, 975), (CX + sw - 10, 975)
    hand = lambda x, y: f'<circle cx="{x}" cy="{y}" r="{t*0.5:.0f}" fill="{skin}"/>'
    seg = lambda pts: (f'<polyline points="{" ".join(f"{x},{y}" for x, y in pts)}" fill="none" stroke="{LINE}" stroke-width="{t+7}" stroke-linecap="round" stroke-linejoin="round"/>'
                       f'<polyline points="{" ".join(f"{x},{y}" for x, y in pts)}" fill="none" stroke="{color}" stroke-width="{t}" stroke-linecap="round" stroke-linejoin="round"/>')
    bx = belly * 0.6
    if pose == "crossed":
        return (seg([L_, (CX - sw + 4, 1090), (CX + 34, 1080)]) + seg([R_, (CX + sw - 4, 1090), (CX - 34, 1096)]) + hand(CX + 46, 1080) + hand(CX - 46, 1096))
    if pose == "pockets":
        return (seg([L_, (CX - sw - 6 - bx, 1080), (CX - hw + 30, 1180)]) + seg([R_, (CX + sw + 6 + bx, 1080), (CX + hw - 30, 1180)])
                + f'<path d="M{CX-hw+14},1176 h36 M{CX+hw-50},1176 h36" stroke="#000" stroke-opacity=".4" stroke-width="5"/>')
    if pose == "hip":
        return (seg([L_, (CX - sw - 16 - bx, 1170)]) + hand(CX - sw - 18 - bx, 1192) + seg([R_, (CX + sw + 60 + bx, 1080), (CX + hw - 6, 1186)]) + hand(CX + hw - 10, 1186))
    if pose == "phone":
        fw = FACES[face_shape][0]
        return (seg([L_, (CX - sw - 16 - bx, 1170)]) + hand(CX - sw - 18 - bx, 1192) + seg([R_, (CX + sw + 30, 1070), (CX + fw + 22, 860)]) + hand(CX + fw + 22, 846)
                + f'<rect x="{CX+fw+8}" y="{800}" width="20" height="56" rx="5" fill="#111" stroke="#3a4560" stroke-width="3"/>')
    if pose == "point":
        return (seg([L_, (CX - sw - 16 - bx, 1170)]) + hand(CX - sw - 18 - bx, 1192) + seg([R_, (CX + sw + 80, 1010), (CX + sw + 170, 960)]) + hand(CX + sw + 178, 956)
                + f'<path d="M{CX+sw+186},952 l30,-8" stroke="{skin}" stroke-width="10" stroke-linecap="round"/>')
    return (seg([L_, (CX - sw - 16 - bx, 1170)]) + seg([R_, (CX + sw + 16 + bx, 1170)]) + hand(CX - sw - 18 - bx, 1192) + hand(CX + sw + 18 + bx, 1192))

def _outfit(outfit, build, coat, accent, skin, wet):
    sw, hw, hem, t, belly = BUILDS[build]
    tp = _torso_path(build); L = f'stroke="{LINE}" stroke-width="5" stroke-linejoin="round"'
    col = "#3a2a1e" if wet and outfit in ("coat", "sweater", "hoodie") else coat
    o = []
    if outfit == "thobe":
        o.append(f'<path d="M{CX-sw+6},960 Q{CX},934 {CX+sw-6},960 L{CX+hw+10},1494 L{CX-hw-10},1494 Z" fill="{col}" {L}/><path d="M{CX},960 L{CX},1100" stroke="#b9c0c8" stroke-width="4"/><circle cx="{CX}" cy="980" r="5" fill="#b9c0c8"/>')
    elif outfit == "dress":
        o.append(f'<path d="M{CX-sw+10},960 Q{CX},934 {CX+sw-10},960 L{CX+hw+12},1400 L{CX-hw-12},1400 Z" fill="{col}" {L}/><path d="M{CX-50},1120 Q{CX},1140 {CX+50},1120" stroke="#000" stroke-opacity=".25" stroke-width="4" fill="none"/>')
    elif outfit == "abaya":
        o.append(f'<path d="M{CX-sw+6},960 Q{CX},934 {CX+sw-6},960 L{CX+hw+16},1500 L{CX-hw-16},1500 Z" fill="{col}" {L}/><path d="M{CX-sw+20},990 L{CX-hw},1490 M{CX+sw-20},990 L{CX+hw},1490" stroke="{accent}" stroke-width="6" opacity=".7"/>')
    else:
        o.append(f'<path d="{tp}" fill="{col}" {L}/>')
        if outfit == "coat":
            o.append(f'<path d="M{CX},960 L{CX},{hem}" stroke="{LINE}" stroke-width="4"/><path d="M{CX-35},950 L{CX},1040 L{CX+35},950" fill="#e8eef6" stroke="{LINE}" stroke-width="3"/>')
        elif outfit == "suit":
            o.append(f'<path d="M{CX-28},950 L{CX},1060 L{CX+28},950 Z" fill="#f2f4f8"/><path d="M{CX-6},960 L{CX+6},960 L{CX+10},1040 L{CX},1056 L{CX-10},1040 Z" fill="{accent}"/>'
                     f'<path d="M{CX-34},948 L{CX},1070 L{CX-52},1010 L{CX-60},966 Z M{CX+34},948 L{CX},1070 L{CX+52},1010 L{CX+60},966 Z" fill="{col}" stroke="#000" stroke-opacity=".35" stroke-width="3"/>')
        elif outfit == "uniform":
            o.append(f'<rect x="{CX-hw+6}" y="{hem-100}" width="{2*hw-12}" height="22" fill="#111"/><rect x="{CX-12}" y="{hem-104}" width="24" height="30" fill="#c9a24a"/>'
                     f'<path d="M{CX+48},1010 l8,16 l18,2 l-13,12 l4,18 l-17,-9 l-16,9 l4,-18 l-13,-12 l18,-2 Z" fill="#ffd21f"/>')
        elif outfit == "sweater":
            o.append(f'<path d="M{CX-32},950 Q{CX},980 {CX+32},950" stroke="#000" stroke-opacity=".3" stroke-width="10" fill="none"/>' + "".join(f'<path d="M{CX-hw+4},{1040+k*60} H{CX+hw-4}" stroke="#000" stroke-opacity=".12" stroke-width="6"/>' for k in range(4)))
        elif outfit == "hoodie":
            o.append(f'<path d="M{CX-50},950 Q{CX},1010 {CX+50},950" stroke="#000" stroke-opacity=".35" stroke-width="12" fill="none"/><path d="M{CX-20},990 L{CX-24},1060 M{CX+20},990 L{CX+24},1060" stroke="#ddd" stroke-width="4"/><rect x="{CX-60}" y="1160" width="120" height="60" rx="14" fill="#000" opacity=".2"/>')
        elif outfit == "apron":
            o.append(f'<path d="M{CX-50},1000 L{CX+50},1000 L{CX+70},{hem+10} L{CX-70},{hem+10} Z" fill="#f4f4f4" stroke="#999" stroke-width="3"/><path d="M{CX-50},1000 L{CX-20},950 M{CX+50},1000 L{CX+20},950" stroke="#f4f4f4" stroke-width="8"/>')
        elif outfit == "labcoat":
            o.append(f'<path d="{tp}" fill="#f4f6f8" {L}/><path d="M{CX},960 L{CX},{hem}" stroke="#b9c0c8" stroke-width="4"/><path d="M{CX-30},950 L{CX},1030 L{CX+30},950" fill="{accent}"/><rect x="{CX+34}" y="1010" width="40" height="50" fill="none" stroke="#b9c0c8" stroke-width="3"/><path d="M{CX+44},1004 v20" stroke="#2f6bd8" stroke-width="4"/>')
        elif outfit == "vest":
            o.append(f'<path d="M{CX-sw+20},966 L{CX-30},960 L{CX},1080 L{CX+30},960 L{CX+sw-20},966 L{CX+hw-10},{hem} L{CX-hw+10},{hem} Z" fill="{accent}" opacity=".9"/>')
        elif outfit == "tshirt":
            o.append(f'<path d="M{CX-30},950 Q{CX},972 {CX+30},950" stroke="#000" stroke-opacity=".3" stroke-width="6" fill="none"/>')
    return "".join(o)

def _accessory(kind, shape, skin, accent, build, gender):
    hw, top, cy, chin, _ = FACES[shape]; sw, bhw, hem, t, belly = BUILDS[build]
    if kind == "cap":
        return f'<path d="M{CX-hw-4},{top+56} Q{CX-hw},{top-6} {CX},{top-8} Q{CX+hw},{top-6} {CX+hw+4},{top+56} Z" fill="{accent}" stroke="{LINE}" stroke-width="3"/><path d="M{CX+hw-10},{top+52} Q{CX+hw+60},{top+50} {CX+hw+70},{top+66} L{CX+hw-6},{top+66} Z" fill="{accent}" stroke="{LINE}" stroke-width="3"/>'
    if kind == "fedora":
        return f'<ellipse cx="{CX}" cy="{top+40}" rx="{hw+44}" ry="14" fill="#3a2a1e" stroke="{LINE}" stroke-width="3"/><path d="M{CX-hw+4},{top+40} Q{CX-hw+10},{top-36} {CX},{top-20} Q{CX+hw-10},{top-36} {CX+hw-4},{top+40} Z" fill="#4a3424" stroke="{LINE}" stroke-width="3"/><rect x="{CX-hw+6}" y="{top+22}" width="{2*hw-12}" height="12" fill="#1a120c"/>'
    if kind == "beanie":
        return f'<path d="M{CX-hw-2},{top+50} Q{CX-hw},{top-24} {CX},{top-26} Q{CX+hw},{top-24} {CX+hw+2},{top+50} Z" fill="{accent}" stroke="{LINE}" stroke-width="3"/><rect x="{CX-hw-4}" y="{top+34}" width="{2*hw+8}" height="22" rx="8" fill="{accent}" stroke="{LINE}" stroke-width="3"/><circle cx="{CX}" cy="{top-28}" r="12" fill="{accent}"/>'
    if kind == "headphones":
        return f'<path d="M{CX-hw-6},{cy} Q{CX-hw},{top-30} {CX},{top-30} Q{CX+hw},{top-30} {CX+hw+6},{cy}" stroke="#222" stroke-width="10" fill="none"/><rect x="{CX-hw-18}" y="{cy-10}" width="22" height="46" rx="10" fill="#222"/><rect x="{CX+hw-4}" y="{cy-10}" width="22" height="46" rx="10" fill="#222"/>'
    if kind == "earrings":
        return f'<circle cx="{CX-hw+2}" cy="{cy+56}" r="6" fill="#e8c34a"/><circle cx="{CX+hw-2}" cy="{cy+56}" r="6" fill="#e8c34a"/>'
    if kind == "scarf":
        return f'<path d="M{CX-46},946 Q{CX},972 {CX+46},946 L{CX+44},972 Q{CX},998 {CX-44},972 Z" fill="{accent}"/><path d="M{CX+20},972 L{CX+34},1080 L{CX+12},1080 Z" fill="{accent}"/>'
    if kind == "necklace":
        return f'<path d="M{CX-30},958 Q{CX},1000 {CX+30},958" stroke="#e8c34a" stroke-width="4" fill="none"/><circle cx="{CX}" cy="992" r="7" fill="#e8c34a"/>'
    if kind == "watch":
        hx = CX - sw - 18 - belly * 0.6
        return f'<rect x="{hx-15:.0f}" y="1150" width="30" height="20" rx="4" fill="#c9ccd4" stroke="#222" stroke-width="3"/>'
    if kind == "cane":
        return f'<path d="M{CX+sw+22},1190 L{CX+sw+40},1520" stroke="#5a3a22" stroke-width="10" stroke-linecap="round"/><path d="M{CX+sw+22},1190 q-4,-26 22,-26" stroke="#5a3a22" stroke-width="10" fill="none" stroke-linecap="round"/>'
    if kind == "bag":
        return f'<path d="M{CX+sw-20},966 L{CX-bhw+10},1200" stroke="#5a3a22" stroke-width="8"/><rect x="{CX-bhw-40}" y="1190" width="90" height="70" rx="10" fill="#7a4a2a" stroke="#3a2214" stroke-width="4"/>'
    if kind == "badge":
        return f'<rect x="{CX+30}" y="1000" width="56" height="40" rx="6" fill="#eef2f7" stroke="#8592a8" stroke-width="3"/><rect x="{CX+36}" y="1006" width="16" height="18" fill="#8592a8"/>'
    if kind == "mask_medical":
        ey = cy + 54
        return f'<path d="M{CX-hw+10},{ey} Q{CX},{ey-12} {CX+hw-10},{ey} L{CX+hw-16},{ey+52} Q{CX},{ey+70} {CX-hw+16},{ey+52} Z" fill="#cfe6f7" stroke="#8fb4cc" stroke-width="3"/>'
    return ""

def _tag(id_, x, y, name):
    w = 60 + 34 * len(name)
    return (f'<g id="tag_{id_}" opacity="0"><rect x="{x-w/2}" y="{y-34}" width="{w}" height="64" rx="32" fill="#ffd21f"/>'
            f'<text x="{x}" y="{y+11}" font-family="Cairo" font-weight="900" font-size="40" fill="#111" text-anchor="middle" direction="rtl">{name}</text></g>')

# ---------------------------------------------------------------- ready characters
CAST = {
    "young_man":      dict(gender="m", face="oval", eyes="normal", nose="line", hair_style="spiky", outfit="coat"),
    "businessman":    dict(gender="m", face="square", eyes="sharp", nose="long", brows="thick", hair_style="side_part", outfit="suit", coat="#1d2230", accent="#c4262e", facial="stubble", accessories=["watch"]),
    "sheikh":         dict(gender="m", age="old", face="long", eyes="droopy", nose="hook", hair_style="shemagh", facial="beard", hair="#e0e0e0", outfit="thobe", skin="tan", accessories=["cane"]),
    "gulf_youth":     dict(gender="m", face="oval", eyes="sharp", nose="line", hair_style="shemagh", facial="stubble", outfit="thobe", skin="medium", pose="phone"),
    "guard":          dict(gender="m", age="old", face="wide", eyes="narrow", nose="wide", brows="bushy", hair_style="buzz", hair="#9a9a9a", facial="mustache", outfit="uniform", build="belly", pose="hip"),
    "chef":           dict(gender="m", face="round", eyes="round", nose="button", hair_style="buzz", outfit="apron", coat="#eef0f2", build="belly", facial="mustache", skin="brown"),
    "student":        dict(gender="m", age="young", face="heart", eyes="big", nose="button", hair_style="curly", outfit="hoodie", coat="#3a5a3a", build="slim", accessories=["headphones", "bag"], skin="dark"),
    "mechanic":       dict(gender="m", face="square", eyes="narrow", nose="wide", brows="bushy", hair_style="receding", outfit="tshirt", coat="#3a4a5a", build="broad", facial="beard", pose="crossed"),
    "doctor_f":       dict(gender="f", face="oval", eyes="sharp", nose="line", hair_style="bun", outfit="labcoat", accent="#2f6bd8", accessories=["badge"], pose="pockets"),
    "hijabi_young":   dict(gender="f", age="young", face="heart", eyes="big", nose="button", hair_style="hijab", accent="#7a2f5a", outfit="sweater", coat="#3a5a7a", skin="medium"),
    "hijabi_pro":     dict(gender="f", face="oval", eyes="sharp", nose="line", hair_style="hijab", accent="#1d2230", outfit="suit", coat="#3a3a4a", accent2="#ffffff", accessories=["badge"], pose="crossed"),
    "abaya_lady":     dict(gender="f", face="long", eyes="normal", nose="line", hair_style="hijab", accent="#111", outfit="abaya", coat="#111", accessories=["bag"]),
    "grandma":        dict(gender="f", age="old", face="round", eyes="droopy", nose="button", hair_style="bun", hair="#e6e6e6", outfit="sweater", coat="#7a4a5a", build="pear", accessories=["necklace"]),
    "artist_f":       dict(gender="f", face="diamond", eyes="big", nose="line", hair_style="wavy", hair="#7a3a1a", outfit="tshirt", coat="#d9a441", accessories=["earrings", "scarf"], accent="#2f6bd8"),
    "maid":           dict(gender="f", face="round", eyes="normal", nose="button", hair_style="ponytail", outfit="apron", coat="#2f4a6a", skin="tan"),
    "athlete_f":      dict(gender="f", age="young", face="oval", eyes="sharp", nose="button", hair_style="braid", hair="#14121a", outfit="tshirt", coat="#c4262e", build="slim", skin="brown", accessories=["cap"], accent="#111"),
    "professor":      dict(gender="m", age="old", face="long", eyes="normal", nose="long", hair_style="bald", hair="#bdbdbd", facial="beard", outfit="vest", coat="#e8e2d0", accent="#5a3a22", glasses=True, build="slim"),
    "bodybuilder":    dict(gender="m", face="square", eyes="narrow", nose="wide", brows="thick", hair_style="mohawk", outfit="tshirt", coat="#111", build="broad", pose="crossed", skin="tan"),
    "taxi_driver":    dict(gender="m", face="wide", eyes="round", nose="wide", hair_style="receding", facial="mustache", outfit="vest", coat="#e8e8e8", accent="#e8b33a", build="belly", accessories=["cap"]),
    "nurse":          dict(gender="f", face="heart", eyes="normal", nose="button", hair_style="hijab", accent="#5aa0d8", outfit="labcoat", accessories=["mask_medical"], pose="pockets"),
    "teen_gamer":     dict(gender="m", age="young", face="round", eyes="big", nose="button", hair_style="side_part", hair="#5a3a1a", outfit="hoodie", coat="#5a2f7a", accessories=["headphones"], skin="light", pose="phone"),
    "fisherman":      dict(gender="m", age="old", face="square", eyes="droopy", nose="hook", hair_style="buzz", hair="#c9c9c9", facial="beard", outfit="sweater", coat="#2f4a5a", accessories=["beanie"], accent="#7a2f2f", build="stocky"),
    "detective_f":    dict(gender="f", face="diamond", eyes="sharp", nose="long", hair_style="long", hair="#14121a", outfit="coat", coat="#5a4a3a", accessories=["fedora"], pose="hip"),
    "child":          dict(gender="m", age="child", face="round", eyes="big", nose="button", hair_style="curly", outfit="tshirt", coat="#e8b33a", skin="medium"),
}

def person(id_="p1", x=490, y=1520, name="", cast=None, gender="m", age="adult", face=None, eyes=None, nose=None, brows=None,
           hair_style=None, hair="#14121a", facial=None, outfit="coat", coat=None, accent="#2f6bd8", skin="#f0c9ad",
           body="normal", build=None, pose="down", expression="neutral", accessories=(), iris="#5a3a22", lips=None,
           wet=False, shoes=None, glasses=False, fog=False, **_ignored):
    """See module doc. Old keys (hair_style, outfit, body, expression, wet, shoes, glasses, fog) keep working."""
    if cast:
        base = dict(CAST[cast]); loc = dict(gender=gender, age=age, face=face, eyes=eyes, nose=nose, brows=brows, hair_style=hair_style,
            facial=facial, outfit=outfit, coat=coat, accent=accent, skin=skin, build=build, pose=pose, expression=expression,
            accessories=accessories, glasses=glasses, hair=hair)
        defaults = dict(gender="m", age="adult", outfit="coat", accent="#2f6bd8", skin="#f0c9ad", pose="down", expression="neutral", accessories=(), glasses=False, hair="#14121a")
        for k, v in loc.items():
            if v is not None and not (k in defaults and v == defaults[k]): base[k] = v
        base.pop("accent2", None)
        return person(id_=id_, x=x, y=y, name=name, body=body, iris=iris, lips=lips, wet=wet, shoes=shoes, fog=fog, **base)
    skin = SKINS.get(skin, skin)
    skin_dark = "#00000055"
    face = face or ("heart" if gender == "f" else "oval"); eyes = eyes or "normal"; nose = nose or ("button" if gender == "f" else "line")
    brows = brows or ("thin" if gender == "f" else "normal")
    if hair_style is None: hair_style = "long" if gender == "f" else "spiky"
    if age == "old" and hair == "#14121a": hair = "#d9d9d9"
    build = build or {"heavy": "belly", "thin": "slim"}.get(body, "normal")
    default_coat = {"thobe": "#eef0f2", "uniform": "#22325a", "suit": "#1d2230", "dress": "#7a2f35", "apron": "#8a3a3a", "hoodie": "#3a3a4a",
                    "sweater": "#3a5a7a", "abaya": "#111", "labcoat": "#f4f6f8", "vest": "#e8e2d0", "tshirt": "#3a4a5a"}
    coat = coat or default_coat.get(outfit, "#6b4a32")
    scale = {"tall": 1.08, "short": 0.9}.get(body, 1.0) * (0.72 if age == "child" else 1.0)
    head_k = 1.22 if age == "child" else 1.0
    o = [f'<g id="{id_}" transform="translate({x} {y}) scale({scale:.3f}) translate(-490 -1520)"><g id="{id_}_body">']
    hair_back = _hair(hair_style, hair, accent, face, "back")
    o.append(f'<g transform="translate(490 940) scale({head_k}) translate(-490 -940)">{hair_back}</g>')
    # legs
    long_robe = outfit in ("thobe", "abaya")
    leg = {"uniform": "#1a2440"}.get(outfit, "#1d1a22")
    if outfit == "dress": leg = skin
    sw, hw, hem, t, belly = BUILDS[build]
    if not long_robe:
        lw = 20 if build in ("broad", "stocky", "belly") else (16 if build == "slim" else 18)
        o.append(f'<path d="M{CX-hw+30},{hem-30} L{CX-60},1500 L{CX-60+2*lw},1500 L{CX-4},{hem-20} Z" fill="{leg}"/><path d="M{CX+4},{hem-20} L{CX+60-2*lw},1500 L{CX+60},1500 L{CX+hw-30},{hem-30} Z" fill="{leg if outfit=="dress" else "#17141b"}"/>')
    shoe = {"mud": "#4a3018"}.get(shoes, "#0a0a0d") if not long_robe else "#5a3a22"
    o.append(f'<path d="M{CX-70},1490 L{CX-12},1490 L{CX-10},1520 L{CX-76},1520 Z" fill="{shoe}"/><path d="M{CX+12},1490 L{CX+70},1490 L{CX+76},1520 L{CX+10},1520 Z" fill="{shoe}"/>')
    if shoes == "wet": o.append(f'<g fill="#9fd0ff"><circle cx="{CX-60}" cy="1484" r="4"/><circle cx="{CX+62}" cy="1486" r="4"/></g><ellipse cx="{CX}" cy="1528" rx="100" ry="10" fill="#7cc6ff" opacity=".45"/>')
    if shoes == "mud": o.append("".join(f'<circle cx="{CX-66+k*44}" cy="1517" r="7" fill="#5a3a1a"/>' for k in range(4)))
    o.append(_outfit(outfit, build, coat, accent, skin, wet))
    arm_col = ("#3a2a1e" if wet and outfit in ("coat", "sweater", "hoodie") else coat) if outfit not in ("tshirt",) else coat
    o.append(_arms(build, pose, arm_col if outfit != "tshirt" else coat, skin, face))
    if outfit == "tshirt" and pose in ("down", "hip", "point", "phone"):  # bare forearms
        pass
    # neck + head
    hk = f'transform="translate(490 940) scale({head_k}) translate(-490 -940)"'
    head = []
    if hair_style not in ("hijab", "shemagh"): head.append(f'<rect x="{CX-18}" y="880" width="36" height="70" fill="{skin}"/>')
    fh = FACES[face]
    if hair_style not in ("hijab", "shemagh", "long", "wavy"):
        head.append(f'<ellipse cx="{CX-fh[0]+2}" cy="{fh[2]+28}" rx="10" ry="18" fill="{skin}" stroke="{LINE}" stroke-width="3"/><ellipse cx="{CX+fh[0]-2}" cy="{fh[2]+28}" rx="10" ry="18" fill="{skin}" stroke="{LINE}" stroke-width="3"/>')
    head.append(f'<path d="{_face_path(face)}" fill="{skin}" stroke="{LINE}" stroke-width="4"/>')
    if age == "old": head.append(f'<path d="M{CX-30},{fh[1]+52} h60 M{CX-24},{fh[1]+64} h48" stroke="#000" stroke-opacity=".25" stroke-width="3"/>')
    eyes_svg, xs, ey = _eyes(id_, face, eyes, expression, iris)
    head.append(eyes_svg.replace('fill="SKIN"', f'fill="{skin}"'))
    if age == "old": head.append(f'<path d="M{xs[0]-20},{ey+4} l-8,5 M{xs[1]+20},{ey+4} l8,5" stroke="#000" stroke-opacity=".3" stroke-width="3"/>')
    if gender == "f": head.append(f'<path d="M{xs[0]-14},{ey-6} l-6,-6 M{xs[1]+14},{ey-6} l6,-6" stroke="{LINE}" stroke-width="3"/>')
    head.append(_nose(face, nose, skin_dark))
    m, my = _mouth(face, expression, gender, lips); head.append(m)
    if facial == "beard":
        head.append(f'<path d="M{CX-fh[0]+4},{fh[2]+40} Q{CX-fh[0]+10},{fh[3]-6} {CX},{fh[3]+10} Q{CX+fh[0]-10},{fh[3]-6} {CX+fh[0]-4},{fh[2]+40} Q{CX+fh[0]-14},{my+16} {CX},{my+18} Q{CX-fh[0]+14},{my+16} {CX-fh[0]+4},{fh[2]+40} Z" fill="{hair}"/><path d="M{CX-22},{my-10} Q{CX},{my-20} {CX+22},{my-10} Q{CX},{my-4} {CX-22},{my-10} Z" fill="{hair}"/>')
    if facial == "mustache": head.append(f'<path d="M{CX-24},{my-8} Q{CX},{my-22} {CX+24},{my-8} Q{CX},{my-2} {CX-24},{my-8} Z" fill="{hair}"/>')
    if facial == "stubble": head.append(f'<path d="M{CX-fh[0]+10},{fh[2]+44} Q{CX-fh[0]+16},{fh[3]-10} {CX},{fh[3]+2} Q{CX+fh[0]-16},{fh[3]-10} {CX+fh[0]-10},{fh[2]+44}" stroke="{hair}" stroke-opacity=".35" stroke-width="16" fill="none" stroke-dasharray="2 4"/>')
    head.append(_hair(hair_style, hair, accent, face, "front"))
    head.append(_brows(face, xs, ey, expression, brows, hair if hair_style not in ("hijab", "shemagh") else LINE))
    if expression == "nervous": head.append(f'<path d="M{CX+fh[0]-6},{fh[2]-14} q8,14 0,22 q-8,-8 0,-22 Z" fill="#9fd0ff"/>')
    if glasses or "glasses" in accessories:
        lens = "#eef4fb" if fog else "none"; op = ".85" if fog else "1"
        head.append(f'<g stroke="#111" stroke-width="4"><circle cx="{xs[0]}" cy="{ey}" r="18" fill="{lens}" fill-opacity="{op}"/><circle cx="{xs[1]}" cy="{ey}" r="18" fill="{lens}" fill-opacity="{op}"/><path d="M{xs[0]+18},{ey} H{xs[1]-18}"/></g>')
    for acc in accessories:
        if acc in ("cap", "fedora", "beanie", "headphones", "earrings", "mask_medical"): head.append(_accessory(acc, face, skin, accent, build, gender))
    o.append(f'<g {hk}>{"".join(head)}</g>')
    for acc in accessories:
        if acc == "watch" and pose in ("pockets", "crossed"): continue
        if acc in ("scarf", "necklace", "watch", "cane", "bag", "badge"): o.append(_accessory(acc, face, skin, accent, build, gender))
    if wet: o.append(f'<g fill="#9fd0ff"><circle cx="{CX-70}" cy="1100" r="5"/><circle cx="{CX+70}" cy="1150" r="5"/><circle cx="{CX-20}" cy="1230" r="5"/><circle cx="{CX+110}" cy="1240" r="6"/></g><ellipse cx="{CX}" cy="1526" rx="120" ry="14" fill="#7cc6ff" opacity=".45"/>')
    o.append('</g></g>')
    if name:
        top_base = 940 - (940 - 690) * head_k
        o.append(_tag(id_, x, int(y - (1520 - top_base) * scale - 40), name))
    return "".join(o)
