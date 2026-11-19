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
    tilt = {"neutral": (4, 0), "nervous": (-6, 2), "smug": (0, 4), "scared": (-8, -4), "angry": (10, 0), "happy": (-2, 2)}[expression]
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


# ====================================================================== EXTENSION: more outfits, accessories, professions
def _hands(build, pose, face_shape):
    """(left_hand, right_hand) positions, None when hidden."""
    sw, hw, hem, t, belly = BUILDS[build]; bx = belly * 0.6
    L = (CX - sw - 18 - bx, 1192); R = (CX + sw + 18 + bx, 1192)
    if pose == "crossed": return (CX + 46, 1080), (CX - 46, 1096)
    if pose == "pockets": return None, None
    if pose == "hip": return L, (CX + hw - 10, 1186)
    if pose == "phone": return L, None
    if pose == "point": return L, (CX + sw + 178, 956)
    return L, R

def _outfit2(outfit, build, coat, accent, skin):
    """New outfits. Returns svg or None if unknown."""
    sw, hw, hem, t, belly = BUILDS[build]; tp = _torso_path(build)
    L = f'stroke="{LINE}" stroke-width="5" stroke-linejoin="round"'
    base = lambda c: f'<path d="{tp}" fill="{c}" {L}/>'
    long_ = lambda c, y=1494, extra=0: f'<path d="M{CX-sw+6},960 Q{CX},934 {CX+sw-6},960 L{CX+hw+10+extra},{y} L{CX-hw-10-extra},{y} Z" fill="{c}" {L}/>'
    collar = lambda c="#f2f4f8": f'<path d="M{CX-30},950 L{CX},990 L{CX+30},950 L{CX+16},946 L{CX},972 L{CX-16},946 Z" fill="{c}"/>'
    buttons = lambda n=4, x=CX, c="#c9ccd4": "".join(f'<circle cx="{x}" cy="{1000+k*60}" r="5" fill="{c}"/>' for k in range(n))
    belt = lambda c="#111", y=None: f'<rect x="{CX-hw+4}" y="{(y or hem-60)}" width="{2*hw-8}" height="20" fill="{c}"/><rect x="{CX-12}" y="{(y or hem-60)-2}" width="24" height="24" fill="none" stroke="#c9a24a" stroke-width="4"/>'
    pocket = lambda x, y, c="#000": f'<rect x="{x}" y="{y}" width="46" height="40" fill="none" stroke="{c}" stroke-opacity=".35" stroke-width="3"/><path d="M{x},{y} h46 v10 h-46 Z" fill="{c}" fill-opacity=".15"/>'
    star = lambda x, y, c="#ffd21f", r=14: f'<path d="M{x},{y-r} l{r*.3:.1f},{r*.6:.1f} l{r*.7:.1f},{r*.1:.1f} l{-r*.5:.1f},{r*.5:.1f} l{r*.15:.1f},{r*.75:.1f} l{-r*.65:.1f},{-r*.35:.1f} l{-r*.65:.1f},{r*.35:.1f} l{r*.15:.1f},{-r*.75:.1f} l{-r*.5:.1f},{-r*.5:.1f} l{r*.7:.1f},{-r*.1:.1f} Z" fill="{c}"/>'
    bands = lambda c="#e8e8e8": f'<rect x="{CX-hw+4}" y="1120" width="{2*hw-8}" height="18" fill="{c}"/><rect x="{CX-hw+4}" y="1200" width="{2*hw-8}" height="18" fill="{c}"/>'
    o = None
    if outfit == "police":      o = base(coat or "#1f2d4d") + collar("#16203a") + pocket(CX-70, 1000) + pocket(CX+24, 1000) + star(CX+48, 990, "#ffd21f", 16) + belt() + buttons(3)
    elif outfit == "firefighter": o = base(coat or "#6b5a2a") + bands("#ffd21f") + bands("#e8e8e8").replace("1120", "1104").replace("1200", "1184") + f'<path d="M{CX},960 V{hem}" stroke="#2a2210" stroke-width="5"/>'
    elif outfit == "pilot":     o = base(coat or "#f2f4f8") + f'<path d="M{CX-6},960 L{CX+6},960 L{CX+10},1050 L{CX},1066 L{CX-10},1050 Z" fill="#111"/>' + "".join(f'<rect x="{x}" y="962" width="44" height="14" fill="#111"/><path d="M{x+6},966 h32 M{x+6},972 h32" stroke="#e8c34a" stroke-width="3"/>' for x in (CX-sw+12, CX+sw-56)) + f'<path d="M{CX+30},1010 l40,0 l-6,8 l-28,0 Z M{CX+50},1004 v20" stroke="#e8c34a" stroke-width="4" fill="#e8c34a"/>' + buttons(4)
    elif outfit == "soldier":   o = base(coat or "#4a5a32") + "".join(f'<ellipse cx="{CX-hw+20+(k*47)%(2*hw-30)}" cy="{990+(k*61)%(hem-1000)}" rx="{18+k%3*6}" ry="{10+k%2*6}" fill="{["#3a4628","#6a6a3a","#2a3018"][k%3]}"/>' for k in range(14)) + belt("#2a2a1a") + pocket(CX-70, 1010, "#000") + pocket(CX+24, 1010, "#000")
    elif outfit == "scrubs":    o = base(coat or "#2f8a8a") + f'<path d="M{CX-34},950 L{CX},1010 L{CX+34},950" fill="none" stroke="#1f6a6a" stroke-width="8"/>' + pocket(CX+20, 1020, "#000")
    elif outfit == "chef_coat": o = base(coat or "#f4f6f8") + buttons(4, CX-26, "#9aa4b2") + buttons(4, CX+26, "#9aa4b2") + f'<path d="M{CX-36},946 Q{CX},966 {CX+36},946 L{CX+30},972 Q{CX},986 {CX-30},972 Z" fill="{accent}"/>'
    elif outfit == "judge":     o = long_(coat or "#111") + f'<path d="M{CX-14},950 L{CX-8},1020 L{CX},1010 L{CX+8},1020 L{CX+14},950 Z" fill="#f4f6f8"/><path d="M{CX-sw+20},990 L{CX-hw-6},1490 M{CX+sw-20},990 L{CX+hw+6},1490" stroke="#2a2a2a" stroke-width="10"/>'
    elif outfit == "graduate":  o = long_(coat or "#111") + f'<path d="M{CX-40},950 L{CX-40},1300 L{CX-14},1300 L{CX-14},990 Z M{CX+40},950 L{CX+40},1300 L{CX+14},1300 L{CX+14},990 Z" fill="{accent}"/>'
    elif outfit == "karate":    o = base(coat or "#f4f4f4") + f'<path d="M{CX-40},950 L{CX+30},1100 M{CX+40},950 L{CX-10},1040" stroke="#c9ccd4" stroke-width="6" fill="none"/>' + f'<rect x="{CX-hw+4}" y="{hem-90}" width="{2*hw-8}" height="22" fill="{accent if accent!="#2f6bd8" else "#111"}"/><path d="M{CX-10},{hem-70} l-14,60 M{CX+10},{hem-70} l14,60" stroke="{accent if accent!="#2f6bd8" else "#111"}" stroke-width="14"/>'
    elif outfit == "jersey":    o = base(coat or "#c4262e") + f'<text x="{CX}" y="1130" text-anchor="middle" font-family="Cairo" font-weight="900" font-size="110" fill="#fff" opacity=".9">{(sum(map(ord, coat or "a")) % 30) + 1}</text>' + f'<path d="M{CX-sw},962 L{CX-sw+30},1000 M{CX+sw},962 L{CX+sw-30},1000" stroke="#fff" stroke-width="8"/>'
    elif outfit == "overalls":  o = base(accent if accent != "#2f6bd8" else "#c4262e") + f'<path d="M{CX-hw+10},1060 L{CX+hw-10},1060 L{CX+hw},{hem} L{CX-hw},{hem} Z" fill="{coat or "#3a5a8a"}" {L}/><rect x="{CX-54}" y="1060" width="108" height="80" fill="{coat or "#3a5a8a"}"/><path d="M{CX-50},1060 L{CX-sw+20},966 M{CX+50},1060 L{CX+sw-20},966" stroke="{coat or "#3a5a8a"}" stroke-width="18"/><rect x="{CX-24}" y="1080" width="48" height="36" fill="none" stroke="#000" stroke-opacity=".35" stroke-width="3"/>'
    elif outfit == "hivis":     o = base(accent if accent != "#2f6bd8" else "#5a5a5a") + f'<path d="M{CX-sw+20},966 L{CX-30},960 L{CX-20},1100 L{CX+20},1100 L{CX+30},960 L{CX+sw-20},966 L{CX+hw-6},{hem} L{CX-hw+6},{hem} Z" fill="{coat or "#ff8a1a"}"/>' + bands("#e8e8e8")
    elif outfit == "raincoat":  o = long_(coat or "#e8c51a", 1400) + buttons(5, CX, "#8a7a1a") + f'<path d="M{CX-30},950 L{CX},1000 L{CX+30},950" fill="#c9a81a"/>'
    elif outfit == "trench":    o = long_(coat or "#b89a6a", 1420) + f'<path d="M{CX-36},948 L{CX},1080 L{CX-60},1020 L{CX-66},966 Z M{CX+36},948 L{CX},1080 L{CX+60},1020 L{CX+66},966 Z" fill="{coat or "#b89a6a"}" stroke="#000" stroke-opacity=".3" stroke-width="3"/>' + belt("#8a6a3a", 1180) + buttons(3, CX-30, "#5a4a2a") + buttons(3, CX+30, "#5a4a2a")
    elif outfit == "leather":   o = base(coat or "#151515") + f'<path d="M{CX+8},960 L{CX-6},{hem}" stroke="#c9ccd4" stroke-width="4"/><path d="M{CX-sw+10},962 L{CX-30},950 L{CX-50},1010 Z M{CX+sw-10},962 L{CX+30},950 L{CX+50},1010 Z" fill="#2a2a2a"/>'
    elif outfit == "puffer":    o = base(coat or "#2f5a9a") + "".join(f'<path d="M{CX-hw+2},{1000+k*56} Q{CX},{1020+k*56} {CX+hw-2},{1000+k*56}" stroke="#000" stroke-opacity=".3" stroke-width="5" fill="none"/>' for k in range(5)) + f'<path d="M{CX},960 V{hem}" stroke="#c9ccd4" stroke-width="4"/>'
    elif outfit == "blazer":    o = base(coat or "#5a4a7a") + f'<path d="M{CX-30},950 L{CX},1030 L{CX+30},950 Z" fill="{accent if accent!="#2f6bd8" else "#f2f4f8"}"/>' + f'<path d="M{CX-34},948 L{CX},1080 L{CX-56},1010 L{CX-62},966 Z M{CX+34},948 L{CX},1080 L{CX+56},1010 L{CX+62},966 Z" fill="{coat or "#5a4a7a"}" stroke="#000" stroke-opacity=".3" stroke-width="3"/>'
    elif outfit == "polo":      o = base(coat or "#2f8a5a") + f'<path d="M{CX-34},950 L{CX},966 L{CX+34},950 L{CX+26},980 L{CX},972 L{CX-26},980 Z" fill="{coat or "#2f8a5a"}" stroke="#000" stroke-opacity=".35" stroke-width="3"/><path d="M{CX},966 V1030" stroke="#000" stroke-opacity=".35" stroke-width="3"/>' + "".join(f'<circle cx="{CX}" cy="{986+k*20}" r="4" fill="#fff"/>' for k in range(2))
    elif outfit == "tank":      o = base(coat or "#e8e8e8") + f'<path d="M{CX-sw+24},962 Q{CX},1010 {CX+sw-24},962" fill="{skin}"/>'
    elif outfit == "waiter":    o = base("#f4f6f8") + f'<path d="M{CX-sw+24},966 L{CX-24},960 L{CX},1120 L{CX+24},960 L{CX+sw-24},966 L{CX+hw-8},{hem} L{CX-hw+8},{hem} Z" fill="{coat or "#111"}"/>' + buttons(3, CX, "#c9ccd4")
    elif outfit == "butler":    o = base(coat or "#111") + f'<path d="M{CX-30},950 L{CX},1060 L{CX+30},950 Z" fill="#f4f6f8"/><path d="M{CX-hw+10},{hem} L{CX-hw-10},{hem+150} L{CX-hw+40},{hem} M{CX+hw-10},{hem} L{CX+hw+10},{hem+150} L{CX+hw-40},{hem}" fill="{coat or "#111"}" stroke="{LINE}" stroke-width="4"/>'
    elif outfit == "postal":    o = base(coat or "#5a7a9a") + collar("#4a6a8a") + pocket(CX-70, 1000) + pocket(CX+24, 1000) + f'<rect x="{CX+30}" y="1004" width="34" height="22" fill="#e8c34a"/>'
    elif outfit == "delivery":  o = base(coat or "#d8321e") + f'<rect x="{CX-40}" y="1040" width="80" height="60" rx="8" fill="#fff"/><path d="M{CX-24},1060 h48 M{CX-24},1080 h30" stroke="{coat or "#d8321e"}" stroke-width="6"/>' + f'<path d="M{CX},960 V{hem}" stroke="#000" stroke-opacity=".3" stroke-width="4"/>'
    elif outfit == "astronaut": o = base(coat or "#eef0f2") + f'<rect x="{CX-50}" y="1000" width="100" height="70" rx="10" fill="#c9ccd4" stroke="#8592a8" stroke-width="3"/><circle cx="{CX-22}" cy="1034" r="8" fill="#c4262e"/><circle cx="{CX+4}" cy="1034" r="8" fill="#2f6bd8"/><circle cx="{CX+28}" cy="1034" r="8" fill="#3a8a4a"/>' + belt("#8592a8") + f'<rect x="{CX+44}" y="980" width="34" height="22" fill="#2f6bd8"/>'
    elif outfit == "patient":   o = long_(coat or "#bfdcf0", 1380) + "".join(f'<circle cx="{CX-hw+20+(k*41)%(2*hw-30)}" cy="{990+(k*53)%380}" r="4" fill="#5a8ab0"/>' for k in range(22))
    elif outfit == "prisoner":  o = base(coat or "#e8761e") + f'<rect x="{CX-50}" y="1010" width="100" height="40" fill="#fff"/><text x="{CX}" y="1042" text-anchor="middle" font-family="Cairo" font-weight="900" font-size="34" fill="#111">{(sum(map(ord, accent)) % 9000) + 1000}</text>' + collar("#c8601a")
    elif outfit == "tracksuit": o = base(coat or "#1d2a5a") + f'<path d="M{CX-hw+14},970 V{hem} M{CX+hw-14},970 V{hem}" stroke="#fff" stroke-width="8"/><path d="M{CX+6},960 V{hem}" stroke="#c9ccd4" stroke-width="4"/>'
    elif outfit == "cardigan":  o = base(accent if accent != "#2f6bd8" else "#e8e2d0") + f'<path d="M{CX-sw+6},962 L{CX-30},960 L{CX-14},{hem} L{CX-hw},{hem} Z M{CX+sw-6},962 L{CX+30},960 L{CX+14},{hem} L{CX+hw},{hem} Z" fill="{coat or "#7a5a3a"}" {L}/>' + buttons(4, CX-22, "#3a2a1a")
    elif outfit == "turtleneck": o = base(coat or "#2a2a2a") + f'<rect x="{CX-26}" y="920" width="52" height="46" rx="14" fill="{coat or "#2a2a2a"}" {L}/>'
    elif outfit == "shirt_tie": o = base(coat or "#e8eef6") + collar("#d0d8e2") + f'<path d="M{CX-6},962 L{CX+6},962 L{CX+10},1060 L{CX},1074 L{CX-10},1060 Z" fill="{accent}"/>' + pocket(CX+26, 1010, "#000")
    elif outfit == "bisht":     o = long_("#eef0f2") + f'<path d="M{CX-sw-6},962 Q{CX-sw+20},950 {CX-30},950 L{CX-50},1500 L{CX-hw-30},1500 Z M{CX+sw+6},962 Q{CX+sw-20},950 {CX+30},950 L{CX+50},1500 L{CX+hw+30},1500 Z" fill="{coat or "#2a1e14"}" {L}/><path d="M{CX-30},950 L{CX-50},1500 M{CX+30},950 L{CX+50},1500" stroke="#e8c34a" stroke-width="7"/>'
    elif outfit == "galabeya":  o = long_(coat or "#5a7a8a") + f'<path d="M{CX-30},950 L{CX},1030 L{CX+30},950" fill="none" stroke="{accent if accent!="#2f6bd8" else "#e8c34a"}" stroke-width="7"/>'
    elif outfit == "lab_tech":  o = base("#f4f6f8") + f'<path d="M{CX},960 L{CX},{hem}" stroke="#b9c0c8" stroke-width="4"/>' + pocket(CX+26, 1010, "#000") + pocket(CX-70, 1160, "#000")
    return o

LONG_OUTFITS = ("thobe", "abaya", "judge", "graduate", "bisht", "galabeya")
ARM_COLOUR = {"tank": "SKIN", "pilot": "#f2f4f8", "waiter": "#f4f6f8", "overalls": "ACCENT", "hivis": "ACCENT", "cardigan": "COAT", "lab_tech": "#f4f6f8", "bisht": "COAT", "chef_coat": "#f4f6f8", "astronaut": "#eef0f2"}
DEFAULT_COAT2 = {"police": "#1f2d4d", "firefighter": "#6b5a2a", "pilot": "#f2f4f8", "soldier": "#4a5a32", "scrubs": "#2f8a8a", "chef_coat": "#f4f6f8", "judge": "#111", "graduate": "#111",
                 "karate": "#f4f4f4", "jersey": "#c4262e", "overalls": "#3a5a8a", "hivis": "#ff8a1a", "raincoat": "#e8c51a", "trench": "#b89a6a", "leather": "#151515", "puffer": "#2f5a9a",
                 "blazer": "#5a4a7a", "polo": "#2f8a5a", "tank": "#e8e8e8", "waiter": "#111", "butler": "#111", "postal": "#5a7a9a", "delivery": "#d8321e", "astronaut": "#eef0f2",
                 "patient": "#bfdcf0", "prisoner": "#e8761e", "tracksuit": "#1d2a5a", "cardigan": "#7a5a3a", "turtleneck": "#2a2a2a", "shirt_tie": "#e8eef6", "bisht": "#2a1e14",
                 "galabeya": "#5a7a8a", "lab_tech": "#f4f6f8"}

HEAD_ACC = ("police_cap", "pilot_cap", "chef_hat", "hard_hat", "fire_helmet", "grad_cap", "beret", "turban", "kufi", "top_hat", "cowboy_hat", "bandana", "nurse_cap",
            "headscarf", "hairclip", "flower_hair", "sweatband", "goggles_head", "straw_hat", "sailor_cap", "crown_paper",
            "sunglasses", "eyepatch", "monocle", "scar", "freckles", "mole", "bandage_face", "earpiece", "nose_ring", "makeup", "round_glasses", "sunglasses_head")
BODY_ACC = ("bow_tie", "tie", "stethoscope", "lanyard", "medal", "whistle", "camera", "pin", "suspenders", "toolbelt", "backpack", "wristband", "gloves",
            "apron_half", "name_tag", "sash")
HAND_ACC = ("briefcase", "clipboard", "wrench", "magnifier", "coffee", "book_hand", "keys", "umbrella_hand", "walkie", "microphone", "paintbrush", "broom",
            "shopping_bag", "newspaper_hand", "misbaha", "flowers", "laptop", "tray", "ball", "measuring_tape", "comb", "scissors", "trophy", "lantern", "map", "tablet")

def _acc_head(kind, shape, skin, accent):
    hw, top, cy, chin, _ = FACES[shape]; l, r = CX - hw, CX + hw; ey = cy + 30
    A = accent
    d = {
        "police_cap": f'<path d="M{l-6},{top+40} Q{CX},{top-30} {r+6},{top+40} Z" fill="#1f2d4d" stroke="{LINE}" stroke-width="3"/><rect x="{l-4}" y="{top+30}" width="{2*hw+8}" height="18" fill="#111"/><path d="M{l+10},{top+48} Q{CX},{top+74} {r-10},{top+48}" fill="#111"/>' + f'<circle cx="{CX}" cy="{top+20}" r="9" fill="#ffd21f"/>',
        "pilot_cap":  f'<path d="M{l-6},{top+40} Q{CX},{top-30} {r+6},{top+40} Z" fill="#111" stroke="{LINE}" stroke-width="3"/><rect x="{l-4}" y="{top+30}" width="{2*hw+8}" height="16" fill="#111"/><path d="M{l+10},{top+46} Q{CX},{top+72} {r-10},{top+46}" fill="#111"/><path d="M{CX-22},{top+20} h44" stroke="#e8c34a" stroke-width="6"/>',
        "chef_hat":   f'<rect x="{l+6}" y="{top-10}" width="{2*hw-12}" height="40" fill="#f4f6f8" stroke="#c9ccd4" stroke-width="3"/>' + "".join(f'<circle cx="{CX+k*28}" cy="{top-40}" r="34" fill="#f4f6f8" stroke="#c9ccd4" stroke-width="3"/>' for k in (-1, 0, 1)),
        "hard_hat":   f'<path d="M{l-10},{top+44} Q{l},{top-26} {CX},{top-28} Q{r},{top-26} {r+10},{top+44} Z" fill="#ffc21f" stroke="{LINE}" stroke-width="3"/><rect x="{l-20}" y="{top+36}" width="{2*hw+40}" height="14" rx="6" fill="#ffc21f" stroke="{LINE}" stroke-width="3"/><path d="M{CX},{top-26} V{top+36}" stroke="#d8a010" stroke-width="8"/>',
        "fire_helmet": f'<path d="M{l-12},{top+44} Q{l},{top-30} {CX},{top-32} Q{r},{top-30} {r+12},{top+44} Z" fill="#c4262e" stroke="{LINE}" stroke-width="3"/><path d="M{l-30},{top+44} L{r+40},{top+44} L{r+60},{top+60} L{l-20},{top+56} Z" fill="#a01e1e"/><rect x="{CX-18}" y="{top-6}" width="36" height="34" rx="6" fill="#ffd21f"/>',
        "grad_cap":   f'<rect x="{l+6}" y="{top+6}" width="{2*hw-12}" height="34" fill="#111"/><path d="M{l-30},{top+6} L{CX},{top-24} L{r+30},{top+6} L{CX},{top+30} Z" fill="#111" stroke="#333" stroke-width="2"/><path d="M{r+20},{top+6} V{top+70}" stroke="{A}" stroke-width="5"/><circle cx="{r+20}" cy="{top+74}" r="7" fill="{A}"/>',
        "beret":      f'<ellipse cx="{CX-10}" cy="{top+14}" rx="{hw+18}" ry="30" fill="{A}" stroke="{LINE}" stroke-width="3"/><circle cx="{CX-10}" cy="{top-16}" r="6" fill="{A}"/>',
        "turban":     f'<ellipse cx="{CX}" cy="{top+16}" rx="{hw+14}" ry="44" fill="{A if A!="#2f6bd8" else "#f2f2f2"}" stroke="{LINE}" stroke-width="3"/><path d="M{l-6},{top+20} Q{CX},{top-20} {r+6},{top+28} M{l},{top+40} Q{CX},{top} {r},{top+44}" stroke="#000" stroke-opacity=".18" stroke-width="5" fill="none"/>',
        "kufi":       f'<path d="M{l+2},{top+40} Q{l+4},{top-12} {CX},{top-14} Q{r-4},{top-12} {r-2},{top+40} Z" fill="{A if A!="#2f6bd8" else "#f2f2f2"}" stroke="{LINE}" stroke-width="3"/><path d="M{l+8},{top+20} H{r-8}" stroke="#c9ccd4" stroke-width="3" stroke-dasharray="6 4"/>',
        "top_hat":    f'<rect x="{l+4}" y="{top-80}" width="{2*hw-8}" height="120" fill="#111" stroke="#333" stroke-width="3"/><rect x="{l+4}" y="{top+12}" width="{2*hw-8}" height="14" fill="{A}"/><ellipse cx="{CX}" cy="{top+40}" rx="{hw+34}" ry="12" fill="#111"/>',
        "cowboy_hat": f'<path d="M{l-60},{top+36} Q{CX},{top+66} {r+60},{top+36} Q{r+40},{top+50} {CX},{top+52} Q{l-40},{top+50} {l-60},{top+36} Z" fill="#8a5a2a" stroke="{LINE}" stroke-width="3"/><path d="M{l+4},{top+40} Q{l+6},{top-36} {CX},{top-20} Q{r-6},{top-36} {r-4},{top+40} Z" fill="#9a6a3a" stroke="{LINE}" stroke-width="3"/>',
        "bandana":    f'<path d="M{l-4},{top+44} Q{CX},{top-10} {r+4},{top+44} L{r},{top+60} Q{CX},{top+36} {l},{top+60} Z" fill="{A if A!="#2f6bd8" else "#c4262e"}"/><path d="M{r},{top+50} l30,10 l-20,16 Z" fill="{A if A!="#2f6bd8" else "#c4262e"}"/>',
        "nurse_cap":  f'<path d="M{CX-40},{top+10} L{CX+40},{top+10} L{CX+30},{top-24} L{CX-30},{top-24} Z" fill="#f4f6f8" stroke="#c9ccd4" stroke-width="3"/><path d="M{CX},{top-18} v20 M{CX-10},{top-8} h20" stroke="#c4262e" stroke-width="5"/>',
        "headscarf":  f'<path d="M{l-8},{top+60} Q{l},{top-20} {CX},{top-20} Q{r},{top-20} {r+8},{top+60} Q{CX},{top+20} {l-8},{top+60} Z" fill="{A}"/><path d="M{r},{top+56} l24,30 l-30,6 Z" fill="{A}"/>',
        "hairclip":   f'<rect x="{r-30}" y="{top+30}" width="30" height="12" rx="5" fill="{A}"/>',
        "flower_hair": f'<g transform="translate({r-14} {top+30})">' + "".join(f'<circle cx="{10*__import__("math").cos(k*1.256):.1f}" cy="{10*__import__("math").sin(k*1.256):.1f}" r="8" fill="#ff7aa2"/>' for k in range(5)) + '<circle r="6" fill="#ffd21f"/></g>',
        "sweatband":  f'<rect x="{l-2}" y="{top+44}" width="{2*hw+4}" height="18" rx="8" fill="{A}"/>',
        "goggles_head": f'<rect x="{l}" y="{top+20}" width="{2*hw}" height="10" fill="#333"/><circle cx="{CX-24}" cy="{top+26}" r="18" fill="#9fd0ff" stroke="#333" stroke-width="5"/><circle cx="{CX+24}" cy="{top+26}" r="18" fill="#9fd0ff" stroke="#333" stroke-width="5"/>',
        "straw_hat":  f'<ellipse cx="{CX}" cy="{top+40}" rx="{hw+70}" ry="18" fill="#e8c87a" stroke="#8a6a2a" stroke-width="3"/><path d="M{l+6},{top+40} Q{l+10},{top-20} {CX},{top-22} Q{r-10},{top-20} {r-6},{top+40} Z" fill="#e8c87a" stroke="#8a6a2a" stroke-width="3"/><rect x="{l+8}" y="{top+18}" width="{2*hw-16}" height="14" fill="{A}"/>',
        "sailor_cap": f'<ellipse cx="{CX}" cy="{top+36}" rx="{hw+6}" ry="18" fill="#f4f6f8" stroke="#c9ccd4" stroke-width="3"/><path d="M{l+6},{top+36} Q{CX},{top-6} {r-6},{top+36}" fill="#f4f6f8" stroke="#c9ccd4" stroke-width="3"/><rect x="{l+6}" y="{top+30}" width="{2*hw-12}" height="10" fill="#1f2d4d"/>',
        "crown_paper": f'<path d="M{l+6},{top+30} L{l+6},{top-10} L{CX-30},{top+10} L{CX},{top-20} L{CX+30},{top+10} L{r-6},{top-10} L{r-6},{top+30} Z" fill="#ffd21f" stroke="#c9a21f" stroke-width="3"/>',
        "sunglasses": f'<g><path d="M{CX-46},{ey-12} h36 q4,26 -18,28 q-20,-2 -18,-28 Z M{CX+10},{ey-12} h36 q2,26 -18,28 q-22,-2 -18,-28 Z" fill="#111"/><path d="M{CX-10},{ey-8} h20" stroke="#111" stroke-width="5"/></g>',
        "sunglasses_head": f'<path d="M{CX-46},{top+28} h36 q4,20 -18,22 q-20,-2 -18,-22 Z M{CX+10},{top+28} h36 q2,20 -18,22 q-22,-2 -18,-22 Z" fill="#111"/>',
        "eyepatch":   f'<path d="M{l-2},{ey-30} L{r+2},{ey+10}" stroke="#111" stroke-width="5"/><ellipse cx="{CX-24}" cy="{ey}" rx="22" ry="18" fill="#111"/>',
        "monocle":    f'<circle cx="{CX+24}" cy="{ey}" r="20" fill="none" stroke="#c9a24a" stroke-width="5"/><path d="M{CX+42},{ey+10} q20,40 0,80" stroke="#c9a24a" stroke-width="3" fill="none"/>',
        "scar":       f'<path d="M{CX+28},{ey-30} L{CX+44},{ey+30}" stroke="#a0525a" stroke-width="5"/><path d="M{CX+30},{ey-16} l10,-4 M{CX+34},{ey} l10,-4 M{CX+38},{ey+16} l10,-4" stroke="#a0525a" stroke-width="3"/>',
        "freckles":   "".join(f'<circle cx="{CX+s*(20+k*9)}" cy="{ey+30+(k%2)*6}" r="2.5" fill="#a0602a"/>' for s in (-1, 1) for k in range(4)),
        "mole":       f'<circle cx="{CX+30}" cy="{ey+56}" r="4" fill="#3a1a14"/>',
        "bandage_face": f'<rect x="{CX+16}" y="{ey+20}" width="44" height="18" rx="6" fill="#f2e2c8" transform="rotate(-20 {CX+38} {ey+29})"/>',
        "earpiece":   f'<circle cx="{r+2}" cy="{cy+28}" r="7" fill="#111"/><path d="M{r+2},{cy+34} q6,50 -10,80" stroke="#c9ccd4" stroke-width="3" fill="none"/>',
        "nose_ring":  f'<circle cx="{CX+9}" cy="{cy+64}" r="5" fill="none" stroke="#e8c34a" stroke-width="3"/>',
        "makeup":     f'<ellipse cx="{CX-36}" cy="{ey+30}" rx="16" ry="8" fill="#ff7a8a" opacity=".45"/><ellipse cx="{CX+36}" cy="{ey+30}" rx="16" ry="8" fill="#ff7a8a" opacity=".45"/>',
        "round_glasses": f'<g stroke="#5a3a1a" stroke-width="4" fill="none"><circle cx="{CX-24}" cy="{ey}" r="15"/><circle cx="{CX+24}" cy="{ey}" r="15"/><path d="M{CX-9},{ey} h18"/></g>',
    }
    return d.get(kind, "")

def _acc_body(kind, build, accent, outfit):
    sw, hw, hem, t, belly = BUILDS[build]; A = accent
    d = {
        "bow_tie":   f'<path d="M{CX},960 l-26,-14 v28 Z M{CX},960 l26,-14 v28 Z" fill="{A if A!="#2f6bd8" else "#111"}"/><circle cx="{CX}" cy="960" r="6" fill="{A if A!="#2f6bd8" else "#111"}"/>',
        "tie":       f'<path d="M{CX-6},962 L{CX+6},962 L{CX+10},1060 L{CX},1074 L{CX-10},1060 Z" fill="{A}"/>',
        "stethoscope": f'<path d="M{CX-34},952 Q{CX-40},1060 {CX},1070 Q{CX+40},1060 {CX+34},952" stroke="#333" stroke-width="5" fill="none"/><circle cx="{CX}" cy="1080" r="12" fill="#c9ccd4" stroke="#333" stroke-width="4"/>',
        "lanyard":   f'<path d="M{CX-30},952 L{CX},1060 L{CX+30},952" stroke="{A}" stroke-width="5" fill="none"/><rect x="{CX-22}" y="1060" width="44" height="58" rx="5" fill="#f4f6f8" stroke="#8592a8" stroke-width="3"/><rect x="{CX-14}" y="1068" width="28" height="22" fill="#8592a8"/>',
        "medal":     f'<path d="M{CX-14},952 L{CX},1030 L{CX+14},952" stroke="{A}" stroke-width="8" fill="none"/><circle cx="{CX}" cy="1044" r="18" fill="#e8c34a" stroke="#a8832a" stroke-width="3"/>',
        "whistle":   f'<path d="M{CX-26},952 L{CX},1040 L{CX+26},952" stroke="#c4262e" stroke-width="3" fill="none"/><rect x="{CX-12}" y="1036" width="30" height="16" rx="6" fill="#c9ccd4" stroke="#555" stroke-width="2"/>',
        "camera":    f'<path d="M{CX-sw+20},966 L{CX+30},1090" stroke="#222" stroke-width="5"/><rect x="{CX+10}" y="1080" width="70" height="46" rx="6" fill="#222"/><circle cx="{CX+45}" cy="1103" r="14" fill="#555" stroke="#999" stroke-width="3"/>',
        "pin":       f'<circle cx="{CX-50}" cy="1000" r="10" fill="{A}" stroke="#fff" stroke-width="3"/>',
        "suspenders": f'<path d="M{CX-40},960 L{CX-36},{hem} M{CX+40},960 L{CX+36},{hem}" stroke="{A if A!="#2f6bd8" else "#7a2f2f"}" stroke-width="10"/>',
        "toolbelt":  f'<rect x="{CX-hw+2}" y="{hem-60}" width="{2*hw-4}" height="26" fill="#6b4a2a"/>' + "".join(f'<rect x="{CX-hw+14+k*((2*hw-40)//3)}" y="{hem-40}" width="34" height="44" fill="#5a3a1a"/>' for k in range(4)),
        "backpack":  f'<path d="M{CX-sw+20},966 L{CX-sw+24},1180 M{CX+sw-20},966 L{CX+sw-24},1180" stroke="{A}" stroke-width="12"/><rect x="{CX+sw-30}" y="990" width="40" height="160" rx="12" fill="{A}" opacity=".9"/>',
        "wristband": f'<rect x="{CX-sw-36}" y="1160" width="34" height="16" rx="6" fill="{A}"/>',
        "gloves":    "",  # handled with hands
        "apron_half": f'<path d="M{CX-hw+14},{hem-100} L{CX+hw-14},{hem-100} L{CX+hw},{hem+90} L{CX-hw},{hem+90} Z" fill="{A if A!="#2f6bd8" else "#f4f4f4"}" stroke="#999" stroke-width="3"/>',
        "name_tag":  f'<rect x="{CX+30}" y="1000" width="64" height="24" rx="4" fill="#f4f6f8" stroke="#8592a8" stroke-width="2"/><path d="M{CX+38},1012 h46" stroke="#8592a8" stroke-width="4"/>',
        "sash":      f'<path d="M{CX-sw+10},966 L{CX+hw-6},{hem-20} L{CX+hw-30},{hem} L{CX-sw-10},990 Z" fill="{A}" opacity=".9"/>',
    }
    return d.get(kind, "")

def _acc_hand(kind, pos, accent):
    if not pos: return ""
    x, y = pos; A = accent
    d = {
        "briefcase": f'<rect x="{x-44}" y="{y+16}" width="88" height="66" rx="8" fill="#5a3a22" stroke="#2a1a10" stroke-width="4"/><path d="M{x-16},{y+16} v-10 h32 v10" stroke="#2a1a10" stroke-width="5" fill="none"/>',
        "clipboard": f'<rect x="{x-36}" y="{y-60}" width="72" height="96" rx="6" fill="#8a6a3a"/><rect x="{x-28}" y="{y-50}" width="56" height="78" fill="#f4f6f8"/><path d="M{x-20},{y-36} h40 M{x-20},{y-22} h40 M{x-20},{y-8} h30" stroke="#8592a8" stroke-width="3"/>',
        "wrench":    f'<path d="M{x},{y} L{x+6},{y+90}" stroke="#9aa4b2" stroke-width="12" stroke-linecap="round"/><path d="M{x-10},{y+90} a16,16 0 1,0 30,0" stroke="#9aa4b2" stroke-width="10" fill="none"/>',
        "magnifier": f'<path d="M{x},{y} L{x+30},{y-60}" stroke="#5a3a22" stroke-width="10" stroke-linecap="round"/><circle cx="{x+44}" cy="{y-88}" r="30" fill="#bfe3ff" fill-opacity=".45" stroke="#c9a24a" stroke-width="8"/>',
        "coffee":    f'<path d="M{x-18},{y-40} L{x+18},{y-40} L{x+14},{y+6} L{x-14},{y+6} Z" fill="#f4f6f8" stroke="#8a6a3a" stroke-width="3"/><rect x="{x-18}" y="{y-46}" width="36" height="8" fill="#5a3a22"/>',
        "book_hand": f'<rect x="{x-30}" y="{y-20}" width="60" height="80" rx="4" fill="{A}" stroke="#2a1a10" stroke-width="3"/><rect x="{x+20}" y="{y-20}" width="8" height="80" fill="#f4efe2"/>',
        "keys":      f'<circle cx="{x}" cy="{y+30}" r="12" fill="none" stroke="#c9ccd4" stroke-width="4"/><path d="M{x+6},{y+40} l10,30 M{x-4},{y+42} l-6,28" stroke="#c9a24a" stroke-width="5"/>',
        "umbrella_hand": f'<path d="M{x},{y} L{x},{y+300}" stroke="#c9a24a" stroke-width="7"/><path d="M{x},{y+30} Q{x+26},{y+170} {x+6},{y+300} L{x-6},{y+300} Q{x-26},{y+170} {x},{y+30} Z" fill="{A if A!="#2f6bd8" else "#0b0f1a"}" stroke="#2f4470" stroke-width="3"/>',
        "walkie":    f'<rect x="{x-14}" y="{y-60}" width="28" height="64" rx="5" fill="#222"/><path d="M{x+6},{y-60} v-24" stroke="#222" stroke-width="5"/><rect x="{x-8}" y="{y-50}" width="16" height="14" fill="#3ddc84"/>',
        "microphone": f'<path d="M{x},{y} L{x+10},{y-70}" stroke="#222" stroke-width="10" stroke-linecap="round"/><circle cx="{x+12}" cy="{y-84}" r="18" fill="#555" stroke="#222" stroke-width="3"/>',
        "paintbrush": f'<path d="M{x},{y+10} L{x+18},{y-80}" stroke="#8a5a2a" stroke-width="8" stroke-linecap="round"/><path d="M{x+14},{y-74} l10,-34 l8,2 l-4,34 Z" fill="{A}"/>',
        "broom":     f'<path d="M{x},{y-80} L{x+20},{y+300}" stroke="#8a5a2a" stroke-width="9"/><path d="M{x-14},{y+290} L{x+56},{y+290} L{x+70},{y+340} L{x-30},{y+340} Z" fill="#c9a24a"/>',
        "shopping_bag": f'<rect x="{x-36}" y="{y+20}" width="72" height="84" rx="4" fill="{A}"/><path d="M{x-16},{y+20} q16,-30 32,0" stroke="{A}" stroke-width="5" fill="none"/>',
        "newspaper_hand": f'<rect x="{x-40}" y="{y-30}" width="80" height="100" fill="#f4efe2" stroke="#8a7a5a" stroke-width="3" transform="rotate(-10 {x} {y})"/><path d="M{x-28},{y-10} h56 M{x-28},{y+10} h56 M{x-28},{y+30} h40" stroke="#8a7a5a" stroke-width="4" transform="rotate(-10 {x} {y})"/>',
        "misbaha":   f'<path d="M{x},{y+8} q-14,60 0,90 q14,-30 0,-90" stroke="{A if A!="#2f6bd8" else "#7a3a1a"}" stroke-width="7" stroke-dasharray="1 8" stroke-linecap="round" fill="none"/>',
        "flowers":   f'<path d="M{x},{y} l-10,-60 M{x},{y} l4,-70 M{x},{y} l16,-56" stroke="#3a8a4a" stroke-width="4"/>' + "".join(f'<circle cx="{x+dx}" cy="{y+dy}" r="12" fill="{c}"/>' for dx, dy, c in ((-10, -66, "#ff7aa2"), (4, -78, "#ffd21f"), (18, -62, "#c4262e"))),
        "laptop":    f'<rect x="{x-60}" y="{y-20}" width="120" height="80" rx="6" fill="#c9ccd4" stroke="#555" stroke-width="3"/><circle cx="{x}" cy="{y+20}" r="8" fill="#fff"/>',
        "tray":      f'<ellipse cx="{x}" cy="{y-30}" rx="60" ry="10" fill="#c9ccd4" stroke="#555" stroke-width="3"/><rect x="{x-20}" y="{y-70}" width="18" height="40" fill="#f4f6f8"/><rect x="{x+8}" y="{y-60}" width="16" height="30" fill="#c4262e" opacity=".7"/>',
        "ball":      f'<circle cx="{x}" cy="{y+30}" r="32" fill="#f4f4f4" stroke="#222" stroke-width="3"/><path d="M{x-10},{y+18} l20,0 l6,18 l-16,12 l-16,-12 Z" fill="#222"/>',
        "measuring_tape": f'<path d="M{x},{y} q-40,80 -10,160" stroke="#ffd21f" stroke-width="10" fill="none"/>',
        "comb":      f'<rect x="{x-6}" y="{y-60}" width="12" height="70" fill="#222"/>' + "".join(f'<path d="M{x+6},{y-56+k*8} h12" stroke="#222" stroke-width="3"/>' for k in range(8)),
        "scissors":  f'<circle cx="{x-8}" cy="{y+8}" r="9" fill="none" stroke="#555" stroke-width="4"/><circle cx="{x+12}" cy="{y+8}" r="9" fill="none" stroke="#555" stroke-width="4"/><path d="M{x-4},{y} L{x+14},{y-50} M{x+8},{y} L{x-6},{y-50}" stroke="#9aa4b2" stroke-width="5"/>',
        "trophy":    f'<path d="M{x-26},{y-80} h52 v20 q0,36 -26,40 q-26,-4 -26,-40 Z" fill="#e8c34a" stroke="#a8832a" stroke-width="3"/><rect x="{x-6}" y="{y-20}" width="12" height="20" fill="#e8c34a"/><rect x="{x-22}" y="{y}" width="44" height="12" fill="#5a3a22"/>',
        "lantern":   f'<path d="M{x},{y} v20" stroke="#333" stroke-width="4"/><rect x="{x-22}" y="{y+20}" width="44" height="60" rx="8" fill="#ffd27a" stroke="#5a4a2a" stroke-width="4"/>',
        "map":       f'<path d="M{x-50},{y-30} l34,10 l34,-10 l34,10 v80 l-34,-10 l-34,10 l-34,-10 Z" fill="#e8dcb0" stroke="#8a7a5a" stroke-width="3"/><path d="M{x-30},{y} q20,20 50,0" stroke="#c4262e" stroke-width="3" stroke-dasharray="6 4" fill="none"/>',
        "tablet":    f'<rect x="{x-40}" y="{y-50}" width="80" height="110" rx="8" fill="#111"/><rect x="{x-32}" y="{y-42}" width="64" height="92" fill="#0e2a55"/>',
    }
    return d.get(kind, "")

# 100 ready professions: key -> (arabic label, look)
P = lambda **k: k
PROFESSIONS = {
 "police_officer": ("شرطي", P(outfit="police", face="square", hair_style="short", accessories=["police_cap", "walkie"], pose="hip")),
 "police_f": ("شرطية", P(gender="f", outfit="police", hair_style="hijab", accent="#1f2d4d", accessories=["walkie"], face="oval")),
 "firefighter": ("رجل إطفاء", P(outfit="firefighter", face="square", facial="stubble", accessories=["fire_helmet"], build="broad")),
 "pilot": ("طيار", P(outfit="pilot", face="long", hair_style="side_part", accessories=["pilot_cap", "sunglasses"])),
 "flight_attendant_f": ("مضيفة طيران", P(gender="f", outfit="blazer", coat="#8a1e2e", hair_style="bun", accessories=["scarf", "name_tag"], accent="#e8c34a", face="heart")),
 "soldier": ("جندي", P(outfit="soldier", face="square", hair_style="buzz", accessories=["beret"], accent="#5a2a2a", build="broad")),
 "surgeon": ("جرّاح", P(outfit="scrubs", face="oval", accessories=["mask_medical", "bandana"], accent="#2f8a8a")),
 "nurse_m": ("ممرض", P(outfit="scrubs", coat="#2f6bd8", face="round", hair_style="short", accessories=["stethoscope"])),
 "pharmacist_f": ("صيدلانية", P(gender="f", outfit="labcoat", hair_style="hijab", accent="#3a8a6a", accessories=["name_tag", "round_glasses"])),
 "dentist": ("طبيب أسنان", P(outfit="labcoat", face="oval", accessories=["mask_medical", "goggles_head"], hair_style="receding")),
 "paramedic": ("مسعف", P(outfit="hivis", coat="#3a8a4a", accent="#2a2a2a", face="square", hair_style="short", accessories=["stethoscope"])),
 "doctor_m": ("طبيب", P(outfit="labcoat", face="long", facial="beard", accessories=["stethoscope", "clipboard"], skin="tan")),
 "vet_f": ("طبيبة بيطرية", P(gender="f", outfit="scrubs", coat="#5a8a3a", hair_style="ponytail", accessories=["stethoscope"], face="round")),
 "baker": ("خبّاز", P(outfit="chef_coat", accent="#c9a24a", face="round", build="belly", facial="mustache", accessories=["chef_hat"])),
 "chef_f": ("طاهية", P(gender="f", outfit="chef_coat", accent="#c4262e", hair_style="bun", accessories=["chef_hat"], face="heart")),
 "waiter": ("نادل", P(outfit="waiter", face="long", hair_style="side_part", accessories=["bow_tie", "tray"])),
 "butler": ("خادم قصر", P(outfit="butler", age="old", face="long", hair_style="receding", hair="#d0d0d0", accessories=["bow_tie", "gloves"], expression="smug")),
 "barista_f": ("باريستا", P(gender="f", outfit="tshirt", coat="#3a3a3a", hair_style="ponytail", accessories=["apron_half", "coffee"], accent="#6b4a32")),
 "judge": ("قاضٍ", P(outfit="judge", age="old", face="square", hair_style="receding", hair="#d0d0d0", accessories=["round_glasses"], expression="angry")),
 "lawyer_f": ("محامية", P(gender="f", outfit="blazer", coat="#1d2230", hair_style="hijab", accent="#5a5a6a", accessories=["briefcase"], face="diamond")),
 "lawyer_m": ("محامٍ", P(outfit="suit", face="long", hair_style="side_part", accessories=["briefcase"], accent="#2f4a7a")),
 "teacher_f": ("معلمة", P(gender="f", outfit="cardigan", coat="#5a7a5a", hair_style="hijab", accent="#7a5a3a", accessories=["book_hand", "round_glasses"])),
 "teacher_m": ("معلم", P(outfit="shirt_tie", accent="#7a2f2f", face="oval", hair_style="short", accessories=["clipboard"], glasses=True)),
 "graduate_f": ("خرّيجة", P(gender="f", outfit="graduate", hair_style="hijab", accent="#e8c34a", accessories=["grad_cap"], expression="happy")),
 "scientist": ("عالم", P(outfit="labcoat", age="old", face="long", hair_style="curly", hair="#e0e0e0", accessories=["goggles_head", "tablet"])),
 "astronaut": ("رائد فضاء", P(outfit="astronaut", face="square", hair_style="buzz", accessories=["medal"], accent="#2f6bd8")),
 "engineer": ("مهندس", P(outfit="hivis", accent="#2f6bd8", face="oval", hair_style="short", accessories=["hard_hat", "tablet"], glasses=True)),
 "construction": ("عامل بناء", P(outfit="hivis", face="square", facial="beard", accessories=["hard_hat", "toolbelt"], build="stocky", skin="brown")),
 "electrician": ("كهربائي", P(outfit="overalls", coat="#2f4a6a", accent="#e8c34a", face="round", accessories=["toolbelt", "goggles_head"])),
 "plumber": ("سبّاك", P(outfit="overalls", coat="#3a5a8a", face="wide", facial="mustache", accessories=["wrench", "cap"], accent="#c4262e", build="belly")),
 "farmer": ("مزارع", P(outfit="overalls", coat="#5a6a3a", accent="#c4262e", age="old", face="square", accessories=["straw_hat"], skin="tan")),
 "sailor": ("بحّار", P(outfit="sweater", coat="#f4f6f8", face="oval", facial="beard", accessories=["sailor_cap"], hair="#5a3a1a")),
 "ship_captain": ("قبطان", P(outfit="pilot", age="old", face="square", facial="beard", hair="#e0e0e0", accessories=["sailor_cap", "medal"])),
 "photographer": ("مصوّر", P(outfit="vest", coat="#8a7a5a", accent="#3a3a3a", face="oval", hair_style="side_part", accessories=["camera", "beanie"])),
 "journalist_f": ("صحفية", P(gender="f", outfit="blazer", coat="#2f5a7a", hair_style="wavy", accessories=["microphone", "lanyard"], accent="#c4262e")),
 "tv_anchor": ("مذيع", P(outfit="suit", face="square", hair_style="side_part", accent="#2f6bd8", accessories=["earpiece"], expression="happy")),
 "painter": ("رسّام", P(outfit="overalls", coat="#e8e2d0", accent="#2f5a7a", face="heart", hair_style="wavy", accessories=["beret", "paintbrush"])),
 "musician": ("موسيقي", P(outfit="leather", face="long", hair_style="long", hair="#2a1a10", accessories=["headphones", "sunglasses_head"])),
 "singer_f": ("مطربة", P(gender="f", outfit="dress", coat="#5a1e4a", hair_style="wavy", accessories=["microphone", "earrings", "makeup"])),
 "dj": ("دي جي", P(outfit="hoodie", coat="#111", face="round", accessories=["headphones", "cap", "sunglasses"], accent="#ff3b8a")),
 "footballer": ("لاعب كرة", P(outfit="jersey", coat="#2f6bd8", face="oval", hair_style="mohawk", accessories=["ball", "wristband"], accent="#ffffff", build="slim")),
 "karate_master": ("مدرّب كاراتيه", P(outfit="karate", accent="#111", face="square", hair_style="buzz", pose="crossed", expression="smug")),
 "referee": ("حكم", P(outfit="jersey", coat="#111", face="wide", hair_style="bald", accessories=["whistle"], build="belly")),
 "coach": ("مدرّب", P(outfit="tracksuit", face="square", facial="stubble", accessories=["whistle", "clipboard", "cap"], accent="#c4262e")),
 "lifeguard": ("منقذ", P(outfit="tank", coat="#c4262e", face="square", hair_style="spiky", accessories=["whistle", "sunglasses"], build="broad", skin="tan")),
 "fitness_trainer_f": ("مدرّبة لياقة", P(gender="f", outfit="tank", coat="#2a2a2a", hair_style="ponytail", accessories=["wristband", "sweatband"], accent="#ff3b8a", build="slim")),
 "bus_driver": ("سائق حافلة", P(outfit="shirt_tie", coat="#cfd8e2", accent="#1f2d4d", face="wide", facial="mustache", build="belly", accessories=["sailor_cap"])),
 "delivery": ("عامل توصيل", P(outfit="delivery", face="oval", hair_style="short", accessories=["cap", "backpack"], accent="#d8321e")),
 "postman": ("ساعي بريد", P(outfit="postal", face="round", hair_style="receding", accessories=["bag", "sailor_cap"], accent="#5a3a22")),
 "security": ("حارس أمن", P(outfit="suit", coat="#111", face="square", hair_style="buzz", accessories=["earpiece", "sunglasses"], build="broad", pose="crossed")),
 "prisoner": ("سجين", P(outfit="prisoner", face="long", hair_style="buzz", facial="stubble", expression="angry")),
 "patient": ("مريض", P(outfit="patient", face="oval", hair_style="short", accessories=["bandage_face"], expression="scared")),
 "elderly_patient": ("مريضة مسنّة", P(gender="f", outfit="patient", age="old", hair_style="bun", hair="#e6e6e6", accessories=["cane"])),
 "librarian_f": ("أمينة مكتبة", P(gender="f", outfit="cardigan", coat="#7a5a7a", hair_style="bun", accessories=["round_glasses", "book_hand"], age="old")),
 "banker": ("مصرفي", P(outfit="suit", coat="#2a2e3a", accent="#2f6bd8", face="long", hair_style="side_part", accessories=["briefcase", "watch"])),
 "ceo_f": ("مديرة شركة", P(gender="f", outfit="suit", coat="#2a2a2a", hair_style="bun", accent="#c4262e", accessories=["earrings", "tablet"], expression="smug", pose="crossed")),
 "secretary": ("سكرتير", P(outfit="shirt_tie", accent="#2f6bd8", face="oval", hair_style="side_part", glasses=True, accessories=["clipboard"])),
 "receptionist_f": ("موظفة استقبال", P(gender="f", outfit="blazer", coat="#2f4a7a", hair_style="hijab", accent="#e8e2d0", accessories=["name_tag", "earpiece"])),
 "hotel_manager": ("مدير فندق", P(outfit="suit", coat="#3a2a4a", accent="#e8c34a", face="square", hair_style="receding", facial="mustache", accessories=["name_tag"])),
 "cleaner": ("عامل نظافة", P(outfit="overalls", coat="#2f6a5a", accent="#e8e8e8", face="round", accessories=["broom", "gloves"])),
 "cleaner_f": ("عاملة نظافة", P(gender="f", outfit="apron", coat="#5a7a8a", hair_style="headscarf" if False else "ponytail", accessories=["headscarf", "broom"], accent="#c4262e")),
 "gardener": ("بستاني", P(outfit="overalls", coat="#5a6a3a", accent="#e8e2d0", age="old", face="round", accessories=["straw_hat", "gloves"], skin="brown")),
 "tailor": ("خيّاط", P(outfit="vest", coat="#e8e2d0", accent="#5a3a22", age="old", face="long", hair_style="bald", accessories=["measuring_tape", "round_glasses"])),
 "barber": ("حلّاق", P(outfit="tshirt", coat="#2a2a2a", face="oval", hair_style="mohawk", facial="beard", accessories=["comb", "apron_half"], accent="#111")),
 "shopkeeper": ("صاحب دكان", P(outfit="galabeya", coat="#7a6a5a", face="wide", facial="mustache", accessories=["keys", "kufi"], build="belly")),
 "jeweler": ("صائغ", P(outfit="vest", coat="#f2f4f8", accent="#2a2a3a", age="old", face="long", accessories=["monocle", "magnifier"], hair_style="receding")),
 "detective_m": ("محقق", P(outfit="trench", face="square", facial="stubble", accessories=["fedora", "magnifier"], expression="smug")),
 "spy": ("جاسوس", P(outfit="trench", coat="#2a2a2a", face="long", hair_style="side_part", accessories=["sunglasses", "earpiece"], pose="pockets")),
 "investigator_f": ("محققة خاصة", P(gender="f", outfit="trench", coat="#5a4a3a", hair_style="hijab", accent="#2a2a2a", accessories=["clipboard"])),
 "psychologist": ("طبيب نفسي", P(outfit="cardigan", coat="#5a4a3a", age="old", face="oval", facial="beard", hair="#d0d0d0", accessories=["round_glasses", "clipboard"])),
 "tourist": ("سائح", P(outfit="polo", coat="#e8a33a", face="round", skin="pale", accessories=["camera", "straw_hat", "backpack"], accent="#2f6bd8", build="belly")),
 "hiker_f": ("متسلّقة", P(gender="f", outfit="puffer", coat="#c4262e", hair_style="braid", accessories=["beanie", "backpack", "map"], accent="#2f5a3a")),
 "rich_heir": ("وريث ثري", P(outfit="bisht", coat="#1a120c", hair_style="shemagh", facial="stubble", accessories=["sunglasses", "watch"], expression="smug")),
 "old_merchant": ("تاجر عجوز", P(outfit="galabeya", coat="#4a5a6a", age="old", face="long", facial="beard", hair="#e0e0e0", accessories=["misbaha", "kufi"])),
 "villager": ("قروي", P(outfit="galabeya", coat="#6a5a4a", face="square", facial="mustache", accessories=["turban"], skin="brown")),
 "bedouin": ("بدوي", P(outfit="thobe", coat="#c9b48a", hair_style="shemagh", face="long", facial="beard", accessories=["misbaha"], skin="tan")),
 "gulf_dad": ("أب خليجي", P(outfit="thobe", hair_style="shemagh", face="round", facial="beard", build="belly", accessories=["round_glasses", "keys"])),
 "grandpa": ("جدّ", P(outfit="cardigan", coat="#6a5a4a", accent="#e8e2d0", age="old", face="round", hair_style="bald", accessories=["cane", "round_glasses"])),
 "influencer_f": ("مؤثرة", P(gender="f", outfit="tshirt", coat="#ff7aa2", hair_style="wavy", hair="#c98a4a", pose="phone", accessories=["sunglasses_head", "makeup", "earrings"])),
 "streamer": ("صانع محتوى", P(outfit="hoodie", coat="#5a2f7a", face="round", hair_style="curly", accessories=["headphones", "microphone"])),
 "programmer": ("مبرمج", P(outfit="hoodie", coat="#2a2a2a", face="oval", hair_style="side_part", glasses=True, accessories=["laptop", "lanyard"], build="slim")),
 "architect_f": ("مهندسة معمارية", P(gender="f", outfit="turtleneck", coat="#2a2a2a", hair_style="bun", accessories=["map", "round_glasses"])),
 "fashion_designer": ("مصمم أزياء", P(outfit="turtleneck", coat="#7a2f5a", face="diamond", hair_style="side_part", accessories=["measuring_tape", "beret"], accent="#111")),
 "magician": ("ساحر", P(outfit="butler", face="long", facial="mustache", accessories=["top_hat", "gloves", "bow_tie"], accent="#c4262e", expression="smug")),
 "actor": ("ممثل", P(outfit="leather", coat="#5a1e1e", face="square", hair_style="wavy", accessories=["scarf", "sunglasses"], accent="#e8c34a")),
 "cashier_f": ("كاشيرة", P(gender="f", outfit="polo", coat="#c4262e", hair_style="hijab", accent="#5a2a2a", accessories=["name_tag"])),
 "car_salesman": ("بائع سيارات", P(outfit="blazer", coat="#2f5a9a", accent="#f2f4f8", face="wide", hair_style="side_part", accessories=["keys", "tie"], expression="happy")),
 "realtor_f": ("وسيطة عقارات", P(gender="f", outfit="blazer", coat="#c9a24a", hair_style="long", accessories=["keys", "tablet"])),
 "park_ranger": ("حارس محمية", P(outfit="police", coat="#5a6a3a", face="square", accessories=["cowboy_hat", "walkie"])),
 "zookeeper_f": ("حارسة حديقة الحيوان", P(gender="f", outfit="overalls", coat="#6a7a3a", accent="#e8e2d0", hair_style="braid", accessories=["gloves", "keys"])),
 "museum_guard": ("حارس متحف", P(outfit="uniform", coat="#3a2a4a", age="old", face="long", facial="mustache", accessories=["walkie", "police_cap"])),
 "train_conductor": ("مفتّش قطار", P(outfit="postal", coat="#2a3a5a", face="oval", facial="mustache", accessories=["whistle", "pilot_cap"])),
 "courier_biker": ("سائق دراجة", P(outfit="leather", face="square", facial="stubble", accessories=["gloves", "backpack", "bandana"], accent="#2a2a2a")),
 "nanny_f": ("مربية", P(gender="f", outfit="cardigan", coat="#c98a8a", accent="#f2f4f8", hair_style="ponytail", accessories=["bag"], face="round", expression="happy")),
 "neighbor_f": ("جارة", P(gender="f", outfit="abaya", age="old", hair_style="hijab", accent="#111", accessories=["shopping_bag"])),
 "lab_tech_f": ("فنية مختبر", P(gender="f", outfit="lab_tech", hair_style="hijab", accent="#2f8a8a", accessories=["goggles_head", "gloves", "tablet"])),
 "forensic": ("خبير أدلة جنائية", P(outfit="lab_tech", face="long", hair_style="buzz", accessories=["gloves", "magnifier", "mask_medical"])),
 "rookie_detective": ("محقق مبتدئ", P(outfit="blazer", coat="#3a4a5a", accent="#e8eef6", age="young", face="heart", hair_style="spiky", accessories=["lanyard", "clipboard"], expression="nervous")),
 "street_vendor": ("بائع متجول", P(outfit="galabeya", coat="#8a6a3a", face="wide", accessories=["bandana", "tray"], skin="brown", accent="#c4262e")),
 "night_watchman": ("حارس ليلي", P(outfit="puffer", coat="#2a3a2a", age="old", face="square", facial="beard", hair="#c0c0c0", accessories=["beanie", "lantern"])),
 "taxi_f": ("سائقة أجرة", P(gender="f", outfit="vest", coat="#e8e8e8", accent="#e8b33a", hair_style="hijab", accessories=["keys", "sunglasses_head"])),
 "student_f": ("طالبة جامعية", P(gender="f", age="young", outfit="hoodie", coat="#5a7a9a", hair_style="ponytail", accessories=["backpack", "book_hand"], accent="#c4262e")),
 "pharmacist_m": ("صيدلي", P(outfit="labcoat", face="round", hair_style="side_part", facial="mustache", accessories=["name_tag", "round_glasses"])),
 "mayor": ("عمدة", P(outfit="suit", coat="#1d2230", age="old", face="wide", hair_style="receding", hair="#d0d0d0", accessories=["sash", "medal"], accent="#c4262e", build="belly")),
 "chess_player": ("لاعب شطرنج", P(outfit="turtleneck", coat="#2a2a3a", face="long", hair_style="receding", accessories=["round_glasses", "trophy"], expression="smug")),
}

for _k, (_ar, _look) in PROFESSIONS.items():
    CAST.setdefault(_k, _look)
CAST_AR = {k: v[0] for k, v in PROFESSIONS.items()}


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
    coat = coat or default_coat.get(outfit) or DEFAULT_COAT2.get(outfit, "#6b4a32")
    scale = {"tall": 1.08, "short": 0.9}.get(body, 1.0) * (0.72 if age == "child" else 1.0)
    head_k = 1.22 if age == "child" else 1.0
    o = [f'<g id="{id_}" transform="translate({x} {y}) scale({scale:.3f}) translate(-490 -1520)"><g id="{id_}_body">']
    hair_back = _hair(hair_style, hair, accent, face, "back")
    o.append(f'<g transform="translate(490 940) scale({head_k}) translate(-490 -940)">{hair_back}</g>')
    # legs
    long_robe = outfit in LONG_OUTFITS
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
    o2 = _outfit2(outfit, build, coat, accent, skin)
    o.append(o2 if o2 is not None else _outfit(outfit, build, coat, accent, skin, wet))
    arm_col = ("#3a2a1e" if wet and outfit in ("coat", "sweater", "hoodie") else coat)
    ac = ARM_COLOUR.get(outfit)
    if ac: arm_col = {"SKIN": skin, "ACCENT": accent if accent != "#2f6bd8" else "#c4262e", "COAT": coat}.get(ac, ac)
    hand_col = "#f4f6f8" if ("gloves" in accessories and outfit in ("butler",)) else ("#3a3a3a" if "gloves" in accessories else skin)
    o.append(_arms(build, pose, arm_col, hand_col, face))
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
        elif acc in HEAD_ACC: head.append(_acc_head(acc, face, skin, accent))
    o.append(f'<g {hk}>{"".join(head)}</g>')
    for acc in accessories:
        if acc in BODY_ACC: o.append(_acc_body(acc, build, accent, outfit)); continue
        if acc in HAND_ACC:
            lh, rh = _hands(build, pose, face); o.append(_acc_hand(acc, lh, accent)); continue
        if acc == "watch" and pose in ("pockets", "crossed"): continue
        if acc in ("scarf", "necklace", "watch", "cane", "bag", "badge"): o.append(_accessory(acc, face, skin, accent, build, gender))
    if wet: o.append(f'<g fill="#9fd0ff"><circle cx="{CX-70}" cy="1100" r="5"/><circle cx="{CX+70}" cy="1150" r="5"/><circle cx="{CX-20}" cy="1230" r="5"/><circle cx="{CX+110}" cy="1240" r="6"/></g><ellipse cx="{CX}" cy="1526" rx="120" ry="14" fill="#7cc6ff" opacity=".45"/>')
    o.append('</g></g>')
    if name:
        top_base = 940 - (940 - 690) * head_k
        o.append(_tag(id_, x, int(y - (1520 - top_base) * scale - 40), name))
    return "".join(o)
