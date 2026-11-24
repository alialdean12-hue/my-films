"""Character builder: a character is described by a spec (dict) and drawn in any pose.
spec keys (all optional):
  sex: m|f   age: child|young|adult|old   build: thin|avg|heavy   height: short|avg|tall
  skin: light|medium|tan|brown|dark|#hex
  hair: short|bald|curly|long|none   hair_color   beard: none|stubble|short|full|long|goatee   beard_color   glasses: true
  head: shemagh|ghutra|kumma|massar|turban|taqiyah|hijab|niqab|cap|hard_hat|police_cap|beret|none   head_color   agal: true|false
  wear: thobe|dishdasha|jalabiya|abaya|suit|shirt|lab|military|police|work   color   pants_color
  outer: bisht|none   outer_color
  hold: {"right": "cane|coin|book|phone|beads|lantern|bag", "left": ...}   khanjar: true
poses: stand, walk, kneel, sit.   faces: calm, tired, curious, shock, joy, sad, angry.
"""
import math
K = "#16131c"
SKINS = {"light": "#f3d9b8", "medium": "#e8c398", "tan": "#d6a676", "brown": "#b07a4f", "dark": "#7a4e30"}
SHADE = "#5a3050"
DEFS = '''<pattern id="shm" width="22" height="22" patternUnits="userSpaceOnUse"><rect width="22" height="22" fill="#f6f4ee"/><path d="M0,11 H22 M11,0 V22" stroke="#c62a30" stroke-width="5"/><rect x="8" y="8" width="6" height="6" fill="#8e1a20"/></pattern>
<pattern id="camo" width="80" height="80" patternUnits="userSpaceOnUse"><rect width="80" height="80" fill="#6b7a4a"/><path d="M5,10 q20,-10 30,6 q-10,14 -30,-6Z M44,40 q24,-6 30,14 q-20,10 -30,-14Z M10,56 q14,-4 18,10 q-12,8 -18,-10Z" fill="#4a5634"/><path d="M50,8 q10,4 6,14 q-10,-2 -6,-14Z M24,34 q10,0 8,10 q-10,0 -8,-10Z" fill="#8f9a66"/></pattern>
<pattern id="dashiki" width="60" height="60" patternUnits="userSpaceOnUse"><rect width="60" height="60" fill="#e8742a"/><path d="M0,30 L15,15 L30,30 L45,15 L60,30 M0,52 L60,52" stroke="#1c1a22" stroke-width="5" fill="none"/><circle cx="30" cy="44" r="5" fill="#ffd23f"/></pattern>
<pattern id="stripes" width="24" height="24" patternUnits="userSpaceOnUse"><rect width="24" height="24" fill="#ffffff"/><rect y="12" width="24" height="10" fill="#1c3a7a"/></pattern>
<pattern id="checker" width="20" height="20" patternUnits="userSpaceOnUse"><rect width="20" height="20" fill="#fff"/><rect width="10" height="10" fill="#222"/><rect x="10" y="10" width="10" height="10" fill="#222"/></pattern>
<pattern id="fur" width="30" height="30" patternUnits="userSpaceOnUse"><rect width="30" height="30" fill="#8a6a4a"/><path d="M4,8 l6,8 M16,4 l4,10 M24,16 l4,8 M8,22 l6,6" stroke="#5a3e24" stroke-width="4"/></pattern>
<pattern id="ermine" width="26" height="26" patternUnits="userSpaceOnUse"><rect width="26" height="26" fill="#fbfbf6"/><path d="M13,8 l-3,8 h6Z" fill="#111"/></pattern>
<linearGradient id="metal" x1="0" x2="1"><stop offset="0" stop-color="#7a8290"/><stop offset=".5" stop-color="#d6dbe2"/><stop offset="1" stop-color="#7a8290"/></linearGradient>
<pattern id="nemes" width="20" height="26" patternUnits="userSpaceOnUse"><rect width="20" height="26" fill="#f2c94c"/><rect y="13" width="20" height="13" fill="#2a4aa8"/></pattern>
<clipPath id="hc"><circle r="112"/></clipPath>
<linearGradient id="bishtG" x1="0" x2="1"><stop offset="0" stop-color="#3a2618"/><stop offset=".5" stop-color="#5a3c24"/><stop offset="1" stop-color="#3a2618"/></linearGradient>'''

# ------------------------------------------------------------------ skeletons (origin = feet on the ground, facing right)
# hip, shoulder y, legs (back L, front R): hip -> knee -> foot, arms (back L / front R): shoulder x, angles (upper, fore)
POSES = {
 "stand": dict(sh=-480, hip=-250, legs=[((-22, -250), (-22, -125), (-20, -8)), ((22, -250), (24, -125), (26, -8))],
               arms=[(-70, 6, -2), (70, -6, 2)], lean=0),
 "walk":  dict(sh=-476, hip=-246, legs=[((-20, -246), (-28, -125), (-66, -22)), ((20, -246), (52, -128), (96, -8))],
               arms=[(-62, 22, 8), (66, -24, -14)], lean=2),
 "kneel": dict(sh=-355, hip=-125, legs=[((-20, -125), (-34, -8), (-158, -10)), ((26, -125), (150, -125), (156, -8))],
               arms=[(-66, -40, -40), (70, -55, -30)], lean=4),
 "sit":   dict(sh=-262, hip=-36, legs=[((-24, -36), (88, -150), (150, -8)), ((10, -36), (112, -150), (176, -8))],
               arms=[(-66, -30, -60), (70, -70, 40)], lean=0),
}
ROBE = {   # one-piece long garment outline per pose (shoulders to hem)
 "stand": "M-64,-480 Q0,-498 64,-480 L74,-28 Q0,-20 -74,-28Z",
 "walk":  "M-64,-476 Q0,-494 64,-476 L74,-256 Q104,-140 124,-30 L-58,-22 Q-74,-150 -70,-256Z",
 "kneel": "M-60,-355 Q2,-371 62,-353 L68,-135 Q110,-160 162,-132 Q172,-70 164,-14 L120,-12 Q40,-8 -40,-6 Q-120,-4 -176,-4 Q-184,-28 -150,-40 Q-96,-56 -74,-92 Q-66,-112 -64,-135Z",
 "sit":   "M-60,-262 Q-2,-278 60,-258 L62,-120 Q96,-176 140,-160 Q182,-120 188,-14 L-108,-12 Q-124,-44 -92,-80 Q-70,-100 -64,-130Z",
}
ROBE_SH = {
 "stand": "M-64,-480 L-74,-28 L-40,-26 L-34,-470Z",
 "walk":  "M-64,-476 L-70,-256 Q-74,-150 -58,-22 L-28,-22 Q-40,-160 -34,-466Z",
 "kneel": "M-60,-355 L-64,-135 Q-66,-112 -74,-92 Q-96,-56 -150,-40 L-110,-30 Q-60,-70 -40,-140 L-30,-345Z",
 "sit":   "M-60,-262 L-64,-130 Q-70,-100 -92,-80 Q-124,-44 -108,-12 L-60,-12 Q-80,-90 -40,-140 L-30,-252Z",
}
BISHT_BACK = {
 "stand": "M-80,-484 Q0,-502 80,-484 L108,-18 L-108,-18Z",
 "walk":  "M-80,-480 Q0,-498 80,-480 L128,-26 L-104,-34Z",
 "kneel": "M-80,-362 Q0,-380 80,-358 L70,-130 Q-40,-40 -190,-6 L-236,-6 Q-170,-130 -80,-362Z",
 "sit":   "M-80,-268 Q0,-286 80,-264 L70,-100 Q-40,-40 -150,-8 L-196,-8 Q-150,-120 -80,-268Z",
}

def _sk(spec): return SKINS.get(spec.get("skin", "medium"), spec.get("skin", "#e8c398"))

# ------------------------------------------------------------------ face + hair + headwear
def face(kind, spec):
    f = spec.get("sex", "m") == "f"; old = spec.get("age") == "old"; child = spec.get("age") == "child"
    E = f'<circle cx="4" cy="4" r="{11 if child else 10}" fill="{K}"/><circle cx="66" cy="4" r="{11 if child else 10}" fill="{K}"/>'
    lash = f'<path d="M-8,-6 l-10,-8 M58,-6 l-6,-10 M78,-6 l8,-10" stroke="{K}" stroke-width="4"/>' if f else ""
    m = {"calm": (E, "M-14,-24 L18,-26 M50,-26 L84,-24", f'<path d="M22,58 Q36,64 52,58" stroke="{K}" stroke-width="7" fill="none" stroke-linecap="round"/>'),
         "tired": (f'<path d="M-12,6 Q4,14 20,6" stroke="{K}" stroke-width="7" fill="none"/><path d="M50,6 Q66,14 82,6" stroke="{K}" stroke-width="7" fill="none"/>', "M-14,-20 L18,-14 M50,-14 L84,-20", f'<path d="M22,62 Q36,56 52,62" stroke="{K}" stroke-width="7" fill="none" stroke-linecap="round"/>'),
         "curious": (f'<circle cx="10" cy="10" r="10" fill="{K}"/><circle cx="72" cy="10" r="10" fill="{K}"/>', "M-14,-18 L18,-18 M50,-32 Q66,-42 84,-30", f'<circle cx="38" cy="62" r="9" fill="none" stroke="{K}" stroke-width="6"/>'),
         "shock": (f'<circle cx="4" cy="2" r="20" fill="#fff" stroke="{K}" stroke-width="5"/><circle cx="66" cy="2" r="20" fill="#fff" stroke="{K}" stroke-width="5"/><circle cx="8" cy="6" r="8" fill="{K}"/><circle cx="70" cy="6" r="8" fill="{K}"/>', "M-16,-30 Q4,-44 22,-30 M48,-30 Q66,-44 86,-30", f'<path d="M22,46 Q38,38 54,46 Q58,82 38,84 Q18,82 22,46Z" fill="#5a1e1e" stroke="{K}" stroke-width="6"/>'),
         "joy": (f'<path d="M-12,8 Q4,-8 20,8" stroke="{K}" stroke-width="7" fill="none"/><path d="M50,8 Q66,-8 82,8" stroke="{K}" stroke-width="7" fill="none"/>', "M-14,-24 Q4,-34 20,-24 M50,-24 Q66,-34 84,-24", f'<path d="M10,44 Q38,50 68,44 Q62,84 38,86 Q14,84 10,44Z" fill="#5a1e1e" stroke="{K}" stroke-width="6"/><path d="M20,48 Q38,52 58,48" stroke="#fff" stroke-width="7"/>'),
         "sad": (E, "M-14,-14 L18,-28 M50,-28 L84,-14", f'<path d="M20,66 Q36,52 54,66" stroke="{K}" stroke-width="7" fill="none" stroke-linecap="round"/>'),
         "angry": (E, "M-14,-30 L20,-14 M48,-14 L84,-30", f'<path d="M20,62 L54,58" stroke="{K}" stroke-width="7" fill="none" stroke-linecap="round"/>')}[kind]
    eyes, brows, mouth = m
    bc = spec.get("beard_color", "#e8e4dc" if old else "#2a1d18")
    bw = {"none": 0, "stubble": 1, "short": 2, "full": 3, "long": 4, "goatee": 5, "mustache": 6}[spec.get("beard", "none" if f or child else "short")]
    beard = ""
    if bw == 1: beard = f'<path d="M0,64 Q38,98 84,62 Q80,92 42,100 Q8,96 0,64Z" fill="{bc}" opacity=".35"/>'
    if bw in (2, 3, 4):
        low = {2: 114, 3: 132, 4: 176}[bw]
        beard = f'<path d="M-4,60 Q38,96 86,58 Q84,{low-20} 42,{low} Q4,{low-20} -4,60Z" fill="{bc}" stroke="{K}" stroke-width="4"/>'
    if bw == 5: beard = f'<path d="M24,74 Q38,84 54,74 Q52,104 38,110 Q26,104 24,74Z" fill="{bc}" stroke="{K}" stroke-width="4"/>'
    must = (f'<path d="M14,58 Q38,44 68,58 Q60,68 38,62 Q20,68 14,58Z" fill="{bc}" stroke="{K}" stroke-width="3"/>' if bw == 6 else
            f'<path d="M18,56 Q38,48 64,56" stroke="{bc}" stroke-width="9" fill="none" stroke-linecap="round"/>' if bw >= 2 else "")
    wr = (f'<path d="M-30,-58 Q4,-66 40,-58 M-24,-44 Q4,-50 34,-44" stroke="{K}" stroke-width="3" fill="none" opacity=".5"/>'
          f'<path d="M-6,28 Q-14,40 -8,52 M86,28 Q94,40 88,52" stroke="{K}" stroke-width="3" fill="none" opacity=".5"/>') if old else ""
    gl = (f'<g fill="none" stroke="{K}" stroke-width="5"><circle cx="4" cy="4" r="24"/><circle cx="66" cy="4" r="24"/><path d="M28,2 Q35,-4 42,2 M-20,0 L-60,-8"/></g>') if spec.get("glasses") else ""
    if old: brows_col = "#d8d4cc"
    else: brows_col = K
    cheek = f'<ellipse cx="-6" cy="38" rx="14" ry="8" fill="#ff7a7a" opacity=".35"/><ellipse cx="86" cy="38" rx="12" ry="8" fill="#ff7a7a" opacity=".35"/>' if (f or child) else ""
    return f'{wr}{cheek}{beard}{must}{eyes}{lash}<path d="{brows}" stroke="{brows_col}" stroke-width="{5 if f else 7}" fill="none" stroke-linecap="round"/>{mouth}{gl}'

def hair(spec):
    hc = spec.get("hair_color", "#d8d4cc" if spec.get("age") == "old" else "#2a1d18")
    h = spec.get("hair", "long" if spec.get("sex") == "f" else "short")
    if h == "short": return f'<path d="M-112,-6 Q-120,-116 -10,-120 Q92,-122 112,-36 Q70,-70 20,-62 Q-50,-56 -80,-20 Q-96,-2 -100,20Z" fill="{hc}" stroke="{K}" stroke-width="6"/>', ""
    if h == "curly": return "".join(f'<circle cx="{x}" cy="{y}" r="34" fill="{hc}" stroke="{K}" stroke-width="5"/>' for x, y in ((-80, -60), (-40, -96), (10, -108), (60, -94), (94, -60), (-100, -10))), ""
    if h == "bald": return f'<path d="M-112,10 Q-118,-40 -100,-56 L-90,-20 Q-96,0 -100,30Z" fill="{hc}" stroke="{K}" stroke-width="5"/>', ""
    if h == "long":
        back = f'<path d="M-118,-20 Q-150,120 -120,250 L60,250 Q30,140 40,80 Z" fill="{hc}" stroke="{K}" stroke-width="6"/>'
        return f'<path d="M-114,10 Q-124,-122 0,-122 Q110,-122 116,-30 Q60,-80 0,-70 Q-60,-60 -90,0 Q-100,40 -104,90Z" fill="{hc}" stroke="{K}" stroke-width="6"/>', back
    if h == "ponytail":
        return (f'<path d="M-112,-6 Q-120,-116 -10,-120 Q92,-122 112,-36 Q70,-70 20,-62 Q-50,-56 -80,-20 Q-96,-2 -100,20Z" fill="{hc}" stroke="{K}" stroke-width="6"/>',
                f'<path d="M-100,-60 Q-190,-20 -170,120 Q-150,60 -110,10Z" fill="{hc}" stroke="{K}" stroke-width="6"/>')
    if h == "bun":
        return (f'<path d="M-112,-6 Q-120,-116 -10,-120 Q92,-122 112,-36 Q70,-70 20,-62 Q-50,-56 -80,-20 Q-96,-2 -100,20Z" fill="{hc}" stroke="{K}" stroke-width="6"/><circle cx="-40" cy="-132" r="40" fill="{hc}" stroke="{K}" stroke-width="6"/>', "")
    if h == "braids":
        return (f'<path d="M-114,10 Q-124,-122 0,-122 Q110,-122 116,-30 Q60,-80 0,-70 Q-60,-60 -90,0 Q-100,40 -104,90Z" fill="{hc}" stroke="{K}" stroke-width="6"/>',
                "".join(f'<ellipse cx="-112" cy="{70+k*34}" rx="20" ry="20" fill="{hc}" stroke="{K}" stroke-width="5"/>' for k in range(5)))
    return "", ""

def headwear(spec):
    """returns (behind_head, over_head)"""
    hw = spec.get("head", "none"); col = spec.get("head_color")
    if hw in ("shemagh", "ghutra"):
        fill = "url(#shm)" if hw == "shemagh" else (col or "#f6f4ee"); fold = "#8e1a20" if hw == "shemagh" else "#d6d0c4"
        back = (f'<path d="M-60,40 C-100,80 -110,150 -96,220 L-20,214 C-26,150 -10,90 -10,40Z" fill="{fill}" stroke="{K}" stroke-width="6"/>'
                f'<path d="M-124,0 C-150,-170 150,-170 124,0 C130,60 146,110 150,150 Q0,182 -146,166 C-140,110 -128,60 -124,0Z" fill="{fill}" stroke="{K}" stroke-width="6"/>'
                f'<path d="M-124,0 C-150,-170 150,-170 124,0 C130,60 146,110 150,150 Q0,182 -146,166 C-140,110 -128,60 -124,0Z" fill="#000" opacity=".10"/>')
        over = (f'<path d="M-118,40 C-132,-100 -60,-150 8,-150 C80,-150 126,-104 120,-42 Q100,-60 72,-46 L30,-54 Q-30,-60 -70,-30 Q-96,-10 -100,60 Z" fill="{fill}" stroke="{K}" stroke-width="6"/>'
                f'<path d="M120,-42 Q132,40 118,150 L96,150 Q108,40 100,-40Z" fill="{fill}" stroke="{K}" stroke-width="5"/>'
                f'<path d="M-70,-110 Q-30,-70 -50,-24 M10,-136 Q30,-96 14,-56" stroke="{fold}" stroke-width="5" fill="none" opacity=".55"/>')
        if spec.get("agal", True):
            over += (f'<ellipse cx="0" cy="-108" rx="104" ry="26" transform="rotate(-5)" fill="none" stroke="{K}" stroke-width="16"/>'
                     f'<ellipse cx="0" cy="-90" rx="108" ry="26" transform="rotate(-5)" fill="none" stroke="{K}" stroke-width="16"/>'
                     f'<path d="M-84,-118 Q0,-138 84,-124" stroke="#555" stroke-width="4" fill="none"/>')
        return back, over
    if hw in ("hijab", "niqab"):
        c = col or "#1c1a22"; hl = "#3a3644" if c == "#1c1a22" else "#ffffff"
        back = f'<path d="M-130,-10 C-150,-170 150,-170 130,-10 C140,70 150,130 160,190 Q0,226 -160,200 C-150,130 -140,70 -130,-10Z" fill="{c}" stroke="{K}" stroke-width="6"/>'
        over = (f'<path d="M-120,30 C-130,-110 -50,-150 6,-150 C80,-150 128,-104 124,-30 Q126,40 112,100 Q90,130 40,138 L40,124 Q86,116 98,80 Q112,20 100,-40 Q70,-80 6,-80 Q-60,-80 -88,-30 Q-104,10 -104,60Z" fill="{c}" stroke="{K}" stroke-width="6"/>'
                f'<path d="M-70,-120 Q-30,-120 10,-130" stroke="{hl}" stroke-width="5" fill="none" opacity=".35"/>')
        if hw == "niqab":
            over += (f'<g clip-path="url(#hc)"><path d="M-120,22 L130,22 L130,150 L-120,150Z" fill="{c}"/></g>'
                     f'<path d="M-104,22 L118,22" stroke="{K}" stroke-width="5"/>')
        return back, over
    if hw == "kumma":
        c = col or "#f2ead8"
        return "", (f'<path d="M-104,-50 Q-110,-130 0,-134 Q110,-130 104,-50 Q0,-74 -104,-50Z" fill="{c}" stroke="{K}" stroke-width="6"/>'
                    + "".join(f'<circle cx="{x}" cy="{-92 + abs(x)/8:.0f}" r="5" fill="#3a6aa8"/>' for x in range(-80, 90, 26))
                    + f'<path d="M-96,-66 Q0,-86 96,-66" stroke="#3a6aa8" stroke-width="5" fill="none"/>')
    if hw in ("massar", "turban"):
        c = col or ("#c9b8e8" if hw == "massar" else "#f6f4ee")
        over = (f'<path d="M-116,-40 Q-124,-150 0,-152 Q124,-150 116,-40 Q60,-70 0,-68 Q-60,-70 -116,-40Z" fill="{c}" stroke="{K}" stroke-width="6"/>'
                f'<path d="M-104,-90 Q0,-130 108,-70 M-110,-60 Q0,-104 112,-48" stroke="{K}" stroke-width="4" fill="none" opacity=".5"/>')
        if hw == "massar": over += f'<path d="M-100,-90 Q-60,-110 -30,-130 L-20,-110 Q-60,-90 -90,-70Z" fill="#7a4a9a" opacity=".5"/>'
        return "", over
    if hw == "taqiyah":
        return "", f'<path d="M-100,-56 Q-104,-124 0,-126 Q104,-124 100,-56 Q0,-80 -100,-56Z" fill="{col or "#ffffff"}" stroke="{K}" stroke-width="6"/>' + "".join(f'<circle cx="{x}" cy="-96" r="3" fill="#d6d0c4"/>' for x in range(-70, 80, 18))
    if hw == "cap":
        c = col or "#2a5a9a"
        return "", f'<path d="M-104,-50 Q-104,-132 0,-132 Q104,-132 104,-50Z" fill="{c}" stroke="{K}" stroke-width="6"/><path d="M80,-56 Q160,-60 176,-40 Q140,-30 80,-38Z" fill="{c}" stroke="{K}" stroke-width="6"/>'
    if hw == "hard_hat":
        c = col or "#ffc21a"
        return "", f'<path d="M-110,-40 Q-110,-150 0,-150 Q110,-150 110,-40Z" fill="{c}" stroke="{K}" stroke-width="6"/><path d="M-130,-40 L140,-40 L140,-24 L-130,-24Z" fill="{c}" stroke="{K}" stroke-width="6"/><path d="M0,-148 L0,-44" stroke="{K}" stroke-width="5" opacity=".4"/>'
    if hw == "police_cap":
        c = col or "#1c2a4a"
        return "", f'<path d="M-110,-70 Q-120,-130 0,-140 Q130,-134 120,-70Z" fill="{c}" stroke="{K}" stroke-width="6"/><path d="M-100,-70 L110,-70 L110,-50 L-100,-50Z" fill="#111" stroke="{K}" stroke-width="5"/><path d="M60,-52 Q120,-50 150,-34 L70,-38Z" fill="#111"/><circle cx="20" cy="-96" r="12" fill="#ffd23f" stroke="{K}" stroke-width="4"/>'
    if hw == "beret":
        c = col or "#7a1e26"
        return "", f'<path d="M-112,-50 Q-140,-130 -20,-140 Q110,-140 118,-70 Q40,-60 -112,-50Z" fill="{c}" stroke="{K}" stroke-width="6"/><circle cx="60" cy="-86" r="10" fill="#ffd23f" stroke="{K}" stroke-width="3"/>'
    if hw == "crown":
        c = col or "#ffcf3a"
        return "", f'<path d="M-90,-80 L-96,-160 L-50,-120 L0,-176 L50,-120 L96,-160 L90,-80Z" fill="{c}" stroke="{K}" stroke-width="6"/>' + "".join(f'<circle cx="{x}" cy="-104" r="9" fill="{g}" stroke="{K}" stroke-width="3"/>' for x, g in ((-50, "#c62a30"), (0, "#2a6ac8"), (50, "#2fa84f")))
    if hw == "pharaoh":
        back = '<path d="M-130,-40 Q-150,120 -150,200 L-60,200 Q-60,120 -40,40Z" fill="url(#nemes)" stroke="' + K + '" stroke-width="6"/>'
        over = (f'<path d="M-124,30 Q-140,-150 0,-150 Q140,-150 124,30 L100,40 Q104,-60 0,-70 Q-104,-60 -100,40Z" fill="url(#nemes)" stroke="{K}" stroke-width="6"/>'
                f'<path d="M100,40 L118,160 L80,160 L86,40Z" fill="url(#nemes)" stroke="{K}" stroke-width="5"/><path d="M-6,-150 q8,-26 20,0" fill="#ffcf3a" stroke="{K}" stroke-width="4"/>')
        return back, over
    if hw == "roman_helmet":
        return "", (f'<path d="M-112,-20 Q-118,-140 0,-142 Q118,-140 112,-20 L90,-24 Q86,-90 0,-92 Q-86,-90 -90,-24Z" fill="url(#metal)" stroke="{K}" stroke-width="6"/>'
                    f'<path d="M-60,-140 Q0,-230 60,-140" fill="#c62a30" stroke="{K}" stroke-width="5"/><path d="M-112,-20 L-118,60 L-90,60 L-90,-24Z" fill="url(#metal)" stroke="{K}" stroke-width="5"/>')
    if hw == "viking_helmet":
        return "", (f'<path d="M-110,-40 Q-110,-150 0,-150 Q110,-150 110,-40Z" fill="url(#metal)" stroke="{K}" stroke-width="6"/><path d="M-110,-40 L110,-40" stroke="#6b4a2e" stroke-width="14"/>'
                    f'<path d="M-104,-90 Q-170,-110 -160,-190 Q-130,-130 -96,-120Z M104,-90 Q170,-110 160,-190 Q130,-130 96,-120Z" fill="#f4ead2" stroke="{K}" stroke-width="5"/><path d="M40,-44 L44,30 L54,30 L52,-44Z" fill="url(#metal)" stroke="{K}" stroke-width="4"/>')
    if hw == "knight_helmet":
        return "", (f'<path d="M-120,90 Q-130,-150 0,-152 Q130,-150 120,90Z" fill="url(#metal)" stroke="{K}" stroke-width="6"/>'
                    f'<path d="M-10,-10 L124,-10 M-10,14 L124,14" stroke="{K}" stroke-width="8"/><path d="M0,-152 Q20,-220 60,-210 Q30,-180 20,-150Z" fill="#c62a30" stroke="{K}" stroke-width="4"/>')
    if hw == "topknot":
        return "", f'<path d="M-112,-6 Q-120,-116 -10,-120 Q92,-122 112,-36 Q70,-70 20,-62 Q-50,-56 -80,-20 Q-96,-2 -100,20Z" fill="{col or "#1a1a1a"}" stroke="{K}" stroke-width="6"/><ellipse cx="-10" cy="-136" rx="26" ry="20" fill="{col or "#1a1a1a"}" stroke="{K}" stroke-width="5"/>'
    if hw == "pirate":
        return "", (f'<path d="M-104,-60 Q-104,-130 0,-130 Q104,-130 104,-60Z" fill="#c62a30" stroke="{K}" stroke-width="6"/><path d="M-150,-70 Q0,-40 150,-70 Q120,-200 0,-170 Q-120,-200 -150,-70Z" fill="#1c1a22" stroke="{K}" stroke-width="6"/>'
                    f'<path d="M-20,-130 l10,-12 l10,12 l-10,10Z" fill="#fff"/><path d="M-30,0 L100,-20" stroke="{K}" stroke-width="5"/><ellipse cx="66" cy="22" rx="24" ry="20" fill="{K}"/>')
    if hw == "cowboy":
        c = col or "#8a5a33"
        return "", f'<path d="M-180,-60 Q0,-20 180,-60 Q160,-40 120,-44 Q100,-160 0,-150 Q-100,-160 -120,-44 Q-160,-40 -180,-60Z" fill="{c}" stroke="{K}" stroke-width="6"/><path d="M-112,-70 Q0,-50 112,-70" stroke="#3a2618" stroke-width="10" fill="none"/>'
    if hw == "astronaut":
        back = '<circle r="160" fill="#e8eef6" stroke="' + K + '" stroke-width="8"/>'
        return back, f'<circle r="150" fill="#9ad0ff" opacity=".25" stroke="{K}" stroke-width="6"/><path d="M-90,-110 Q-40,-140 20,-136" stroke="#fff" stroke-width="12" fill="none" opacity=".8"/>'
    if hw == "diver":
        return "", f'<path d="M-108,-30 Q-112,-140 0,-142 Q112,-140 108,-30Z" fill="#1c1a22" stroke="{K}" stroke-width="6"/><rect x="-30" y="-24" width="150" height="70" rx="26" fill="#9ad0ff" opacity=".7" stroke="{K}" stroke-width="7"/><path d="M-110,0 L-30,0" stroke="{K}" stroke-width="10"/><path d="M60,70 Q110,90 130,40" stroke="#ffc21a" stroke-width="12" fill="none"/>'
    if hw == "explorer":
        return "", f'<path d="M-150,-48 Q0,-20 150,-48 Q100,-170 0,-160 Q-100,-170 -150,-48Z" fill="#d8c08a" stroke="{K}" stroke-width="6"/><path d="M-108,-60 Q0,-44 108,-60" stroke="#6b4a2e" stroke-width="10" fill="none"/>'
    if hw == "chef":
        return "", f'<path d="M-80,-70 L80,-70 L84,-140 Q120,-170 90,-210 Q60,-250 20,-220 Q0,-260 -30,-226 Q-80,-250 -100,-200 Q-120,-160 -84,-140Z" fill="#fff" stroke="{K}" stroke-width="6"/>'
    if hw in ("pilot_cap", "sailor_cap"):
        c = col or ("#1c2a4a" if hw == "pilot_cap" else "#ffffff")
        return "", f'<path d="M-110,-70 Q-120,-130 0,-140 Q130,-134 120,-70Z" fill="{c}" stroke="{K}" stroke-width="6"/><path d="M-100,-70 L110,-70 L110,-50 L-100,-50Z" fill="#111" stroke="{K}" stroke-width="5"/><path d="M60,-52 Q120,-50 150,-34 L70,-38Z" fill="#111"/>' + (f'<path d="M-10,-104 l30,0 l-15,-14Z" fill="#ffd23f"/>' if hw == "pilot_cap" else "")
    if hw == "rice_hat":
        return "", f'<path d="M-200,-40 L0,-190 L200,-40 Q0,-20 -200,-40Z" fill="#d8b86a" stroke="{K}" stroke-width="6"/><path d="M-120,-80 L0,-170 L60,-110" stroke="#a8864a" stroke-width="4" fill="none"/>'
    if hw == "headband":
        return "", f'<path d="M-112,-40 Q0,-80 112,-40 L112,-18 Q0,-58 -112,-18Z" fill="{col or "#c62a30"}" stroke="{K}" stroke-width="5"/><path d="M-110,-30 Q-150,0 -160,40 M-110,-26 Q-140,20 -136,60" stroke="{col or "#c62a30"}" stroke-width="12" fill="none"/>'
    return "", ""

BANDAGE = (f'<path d="M-112,-40 Q0,-86 112,-40 L114,-12 Q0,-58 -114,-12Z" fill="#fbfbf6" stroke="{K}" stroke-width="4"/>'
           f'<path d="M-104,-30 Q0,-70 104,-30" stroke="#d8d0c0" stroke-width="3" fill="none"/><path d="M-110,30 L-60,40 L-64,70 L-112,62Z" fill="#fbfbf6" stroke="{K}" stroke-width="4"/>'
           f'<path d="M-40,-40 l14,10" stroke="#c84a3a" stroke-width="5" opacity=".6"/>')
def head(spec, kind="calm"):
    hb, ho = headwear(spec)
    if spec.get("head", "none") in ("none", "cap", "beret", "hard_hat", "police_cap", "kumma", "taqiyah", "crown", "cowboy", "headband", "pilot_cap", "sailor_cap", "explorer", "chef", "rice_hat", "pirate", "roman_helmet", "viking_helmet"):
        hf, hbk = hair(spec) if spec.get("head", "none") == "none" else ((lambda hh: (hh[0], hh[1] if spec.get("hair") in ("long", "ponytail", "braids") else ""))(hair(dict(spec, hair=spec.get("hair", "short")))) if spec.get("hair", "short") != "bald" else ("", ""))
    else:
        hf, hbk = "", ""
    sk = _sk(spec)
    ear = f'<ellipse cx="-96" cy="10" rx="18" ry="26" fill="{sk}" stroke="{K}" stroke-width="6"/>' if spec.get("head", "none") not in ("shemagh", "ghutra", "hijab", "niqab", "pharaoh", "knight_helmet", "astronaut", "diver") and spec.get("hair") != "long" else ""
    return (f'{hbk}{hb}{ear}<circle r="112" fill="{sk}" stroke="{K}" stroke-width="8"/>'
            f'<g clip-path="url(#hc)"><circle cx="-62" cy="22" r="108" fill="{SHADE}" opacity=".18"/></g>'
            f'<g transform="translate(0 18)">{face(kind, spec)}</g>{hf}{ho}' + (BANDAGE if spec.get("bandage") else ""))

# ------------------------------------------------------------------ body parts
def held(item, rot):
    """object in a hand; drawn upright whatever the arm angle."""
    if not item: return ""
    g = lambda s: f'<g transform="rotate({-rot})">{s}</g>'
    return g({
        "cane": f'<path d="M0,-40 L0,250" stroke="#6b4a2e" stroke-width="12" stroke-linecap="round"/><path d="M0,-40 Q0,-70 30,-66" stroke="#6b4a2e" stroke-width="12" fill="none" stroke-linecap="round"/>',
        "coin": f'<g transform="translate(0 -30)"><circle r="26" fill="#ffcf3a" stroke="{K}" stroke-width="5"/><circle r="14" fill="none" stroke="#c98d10" stroke-width="4"/></g>',
        "book": f'<rect x="-10" y="-10" width="70" height="90" rx="6" fill="#7a2f35" stroke="{K}" stroke-width="5"/><path d="M0,0 L0,70" stroke="#d8a93a" stroke-width="4"/>',
        "phone": f'<rect x="-14" y="-40" width="36" height="66" rx="8" fill="#222" stroke="{K}" stroke-width="5"/><rect x="-8" y="-32" width="24" height="44" fill="#7cc6ff"/>',
        "beads": "".join(f'<circle cx="{8*math.sin(k/2):.0f}" cy="{14+k*9}" r="6" fill="#8a3a2a" stroke="{K}" stroke-width="2"/>' for k in range(9)),
        "bag": f'<path d="M-10,10 L-40,60 L60,60 L40,10" fill="none" stroke="{K}" stroke-width="6"/><rect x="-46" y="60" width="112" height="80" rx="12" fill="#8a5a33" stroke="{K}" stroke-width="5"/>',
        "lantern": f'<path d="M0,0 L0,24" stroke="{K}" stroke-width="4"/><rect x="-28" y="24" width="56" height="16" rx="4" fill="#3a2a1a" stroke="{K}" stroke-width="4"/><rect x="-24" y="40" width="48" height="60" rx="10" fill="#ffd77a" stroke="{K}" stroke-width="5"/><path d="M0,52 C10,64 10,80 0,88 C-10,80 -10,64 0,52Z" fill="#ff8a1c"/><rect x="-30" y="98" width="60" height="12" rx="4" fill="#3a2a1a" stroke="{K}" stroke-width="4"/>',
    }.get(item, ""))

def arm(x, y, a1, a2, col, sk, item="", wide=False):
    r1, r2 = math.radians(a1), math.radians(a1 + a2)
    ex, ey = -105*math.sin(r1), 105*math.cos(r1); wx, wy = ex - 96*math.sin(r2), ey + 96*math.cos(r2)
    d = f"M0,0 L{ex:.1f},{ey:.1f} L{wx:.1f},{wy:.1f}"; w = 50 if wide else 42
    sl = (f'<path d="{d}" stroke="{K}" stroke-width="{w}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
          f'<path d="{d}" stroke="{col}" stroke-width="{w-13}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
          f'<path d="M-7,10 L{ex-7:.1f},{ey:.1f} L{wx-7:.1f},{wy-8:.1f}" stroke="#000" stroke-width="6" fill="none" stroke-linecap="round" stroke-linejoin="round" opacity=".12"/>')
    hand = (f'<g transform="translate({wx:.1f} {wy:.1f}) rotate({a1+a2})"><path d="M-{w/2-6},-6 L{w/2-6},-6 L{w/2-5},8 L-{w/2-5},8Z" fill="{col}" stroke="{K}" stroke-width="5" stroke-linejoin="round"/>'
            f'<ellipse cx="0" cy="20" rx="15" ry="17" fill="{sk}" stroke="{K}" stroke-width="5"/><g transform="translate(0 22)">{held(item, a1+a2)}</g></g>')
    return f'<g transform="translate({x} {y})">{sl}{hand}</g>'

def leg(pts, col, shoe):
    (hx, hy), (kx, ky), (fx, fy) = pts
    d = f"M{hx},{hy} L{kx},{ky} L{fx},{fy}"
    return (f'<path d="{d}" stroke="{K}" stroke-width="50" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{d}" stroke="{col}" stroke-width="37" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
            + shoe_at(fx, fy, shoe))

def shoe_at(x, y, kind, r=0):
    if kind == "sandal":
        return f'<g transform="translate({x} {y+4}) rotate({r})"><path d="M-22,-4 Q-24,10 -8,10 L34,10 Q46,8 40,-4 Z" fill="#7a4a24" stroke="{K}" stroke-width="5"/><path d="M-8,-4 Q8,-14 22,-4" stroke="#4a2a12" stroke-width="6" fill="none"/></g>'
    c = {"boot": "#3a2a1a", "shoe": "#1a1a1a", "sneaker": "#f0f0f0"}.get(kind, "#1a1a1a")
    return f'<g transform="translate({x} {y+4}) rotate({r})"><path d="M-26,-22 L18,-22 Q54,-16 54,6 L-26,8Z" fill="{c}" stroke="{K}" stroke-width="5" stroke-linejoin="round"/></g>'

ROBES = {"thobe": "#f6f4ee", "dishdasha": "#f6f4ee", "jalabiya": "#3a6aa8", "abaya": "#1c1a22", "kimono": "#c62a4a", "sari": "#e8742a", "toga": "#f6f4ee", "egypt": "#f6f0dc", "dress": "#3a8ac8", "hanfu": "#2a8a7a", "royal": "#8a1e2e"}
PANTS = {"suit": ("#2a2f3a", "#2a2f3a", "shoe"), "shirt": ("#5a8ac8", "#3a3f4a", "shoe"), "lab": ("#9ac0e8", "#3a3f4a", "shoe"),
         "military": ("url(#camo)", "url(#camo)", "boot"), "police": ("#2a3a5a", "#1c2438", "shoe"), "work": ("#f07a1c", "#f07a1c", "boot"),
         "jeans": ("#e8e2d6", "#3a5a8a", "sneaker"), "dashiki": ("url(#dashiki)", "#e8742a", "sandal"), "cowboy": ("#a83a2a", "#3a5a8a", "boot"),
         "knight": ("url(#metal)", "url(#metal)", "boot"), "viking": ("#6b4a2e", "#8a7a5a", "boot"), "roman": ("#b8282e", "SKIN", "sandal"),
         "samurai": ("#2a3a5a", "#1c1a22", "sandal"), "pirate": ("#f6f4ee", "#3a2a1a", "boot"), "astronaut": ("#f0f2f6", "#f0f2f6", "boot"),
         "diver": ("#1c1a22", "#1c1a22", "sneaker"), "chef": ("#ffffff", "url(#checker)", "shoe"), "pilot": ("#1c2a4a", "#1c2a4a", "shoe"),
         "sailor": ("url(#stripes)", "#1c2a4a", "shoe"), "explorer": ("#c9b48a", "#a8936a", "boot"), "coat": ("#e8e2d6", "#3a3f4a", "shoe")}

def body(spec, pose, kind="calm", hs=(1, 1)):
    P = POSES[pose]; sk = _sk(spec); wear = spec.get("wear", "abaya" if spec.get("sex") == "f" else "thobe")
    hold = dict(spec.get("hold", {})); sh = P["sh"]
    if pose in ("kneel", "sit"): hold = {k: v for k, v in hold.items() if v != "cane"}   # the cane is laid aside
    out_back, out_front, front_arm, back_arm = [], [], "", ""
    (bx, ba1, ba2), (fx, fa1, fa2) = P["arms"]
    if wear in ROBES:
        col = spec.get("color", ROBES[wear]); wide = wear in ("abaya", "jalabiya", "kimono", "hanfu", "royal")
        sleeve = col
        out_back.append(f'<path d="{ROBE[pose]}" fill="{col}" stroke="{K}" stroke-width="7" stroke-linejoin="round"/><path d="{ROBE_SH[pose]}" fill="{SHADE}" opacity=".13"/>')
        feet = [p[2] for p in P["legs"]]
        if pose != "kneel": shoes = "".join(shoe_at(x + (8 if k else 0), y if y > -30 else -4, "sandal" if spec.get("sex") != "f" or wear in ("sari", "toga", "egypt") else "shoe") for k, (x, y) in enumerate(feet))
        else: shoes = shoe_at(feet[1][0] + 10, -4, "sandal" if spec.get("sex") != "f" or wear in ("sari", "toga", "egypt") else "shoe")
        out_back.insert(0, shoes)
        nx = 0
        if wear in ("thobe", "dishdasha"):
            out_back.append(f'<path d="M-24,{sh-2} Q0,{sh-12} 24,{sh-2} L24,{sh+16} Q0,{sh+8} -24,{sh+16}Z" fill="{col}" stroke="{K}" stroke-width="5"/><path d="M6,{sh+14} L6,{sh+100}" stroke="#d6d0c4" stroke-width="6"/>'
                            + "".join(f'<circle cx="14" cy="{sh+30+k*26}" r="4" fill="#d6d0c4"/>' for k in range(3)))
            if wear == "dishdasha": out_back.append(f'<path d="M10,{sh+16} Q14,{sh+90} 8,{sh+150}" stroke="#c9b48a" stroke-width="6" fill="none"/><path d="M0,{sh+150} L16,{sh+150} L12,{sh+176} L4,{sh+176}Z" fill="#c9b48a" stroke="{K}" stroke-width="3"/>')
        if wear == "jalabiya": out_back.append(f'<path d="M-26,{sh} L4,{sh+70} L34,{sh}" fill="none" stroke="#d8a93a" stroke-width="7"/>')
        if wear == "kimono": out_back.append(f'<path d="M-30,{sh} L20,{sh+150} M40,{sh} L4,{sh+90}" stroke="#fff" stroke-width="8" fill="none"/><rect x="-70" y="{P["hip"]-40}" width="140" height="44" fill="#ffd23f" stroke="{K}" stroke-width="5"/>')
        if wear == "sari": out_back.append(f'<path d="M-64,{sh+20} Q0,{sh+40} 70,{P["hip"]-20} L70,{P["hip"]+30} Q0,{sh+90} -64,{sh+70}Z" fill="#c9302a" stroke="{K}" stroke-width="5"/><path d="M-64,{sh+20} Q0,{sh+40} 70,{P["hip"]-20}" stroke="#ffd23f" stroke-width="7" fill="none"/>')
        if wear == "toga": out_back.append(f'<path d="M-60,{sh} Q20,{sh+120} 70,{P["hip"]+20} L50,{P["hip"]+40} Q0,{sh+150} -64,{sh+40}Z" fill="#e8e2d0" stroke="{K}" stroke-width="5"/><path d="M-50,{sh+30} Q10,{sh+140} 56,{P["hip"]+20}" stroke="#b8282e" stroke-width="8" fill="none"/>')
        if wear == "egypt": out_back.append(f'<path d="M-60,{sh-4} Q0,{sh+70} 64,{sh-4} L60,{sh+30} Q0,{sh+100} -60,{sh+30}Z" fill="#2a4aa8" stroke="{K}" stroke-width="5"/><path d="M-56,{sh+12} Q0,{sh+80} 60,{sh+12}" stroke="#ffcf3a" stroke-width="8" fill="none"/><rect x="-68" y="{P["hip"]-20}" width="136" height="22" fill="#ffcf3a" stroke="{K}" stroke-width="4"/>')
        if wear == "dress": out_back.append(f'<path d="M-66,{P["hip"]-30} L66,{P["hip"]-30}" stroke="#fff" stroke-width="10"/>')
        if wear == "hanfu": out_back.append(f'<path d="M-40,{sh} L30,{sh+170}" stroke="#f6f4ee" stroke-width="10" fill="none"/><rect x="-70" y="{P["hip"]-34}" width="140" height="30" fill="#c62a30" stroke="{K}" stroke-width="5"/>')
        if wear == "royal": out_back.append(f'<path d="M-30,{sh} L-30,{-30 if pose in ("stand", "walk") else -20} M34,{sh} L34,{-30 if pose in ("stand", "walk") else -20}" stroke="#ffcf3a" stroke-width="8"/>')
        if wear == "abaya": out_back.append(f'<path d="M4,{sh+10} L6,{-30 if pose in ("stand", "walk") else -20}" stroke="#3a3644" stroke-width="5"/>')
    else:
        top, pants, shoe = PANTS[wear]; top = spec.get("color", top); pants = spec.get("pants_color", sk if pants == "SKIN" else pants)
        sleeve = top; wide = False
        legs = "".join(leg(l, pants, shoe) for l in P["legs"])
        hip = P["hip"]; lean = P["lean"]
        torso = f'<path d="M-64,{sh} Q0,{sh-18} 64,{sh} L68,{hip+16} L-68,{hip+16}Z" fill="{top}" stroke="{K}" stroke-width="7" stroke-linejoin="round"/><path d="M-64,{sh} L-68,{hip+16} L-36,{hip+16} L-32,{sh+4}Z" fill="{SHADE}" opacity=".13"/>'
        belt = f'<path d="M-68,{hip+6} L68,{hip+6}" stroke="#2a1d18" stroke-width="12"/><rect x="-6" y="{hip-2}" width="22" height="16" fill="#c9a24a" stroke="{K}" stroke-width="3"/>'
        det = ""
        if wear == "suit":
            det = (f'<path d="M-20,{sh-6} L4,{sh+40} L28,{sh-6}" fill="#fff" stroke="{K}" stroke-width="4"/><path d="M4,{sh+20} L-6,{sh+120} L4,{sh+140} L14,{sh+120}Z" fill="#9a1e26" stroke="{K}" stroke-width="3"/>'
                   f'<path d="M-30,{sh-4} L-10,{sh+110} M38,{sh-4} L18,{sh+110}" stroke="{K}" stroke-width="5"/>'); belt = ""
        if wear == "police": det = f'<path d="M30,{sh+40} l12,-8 l12,8 l-4,18 h-16Z" fill="#ffd23f" stroke="{K}" stroke-width="3"/><path d="M-60,{sh+10} L60,{sh+10}" stroke="#111" stroke-width="8"/>'
        if wear == "work": det = f'<path d="M-40,{sh} L-40,{hip} M44,{sh} L44,{hip}" stroke="#c45a10" stroke-width="10"/><rect x="-36" y="{sh+60}" width="80" height="60" fill="#c45a10" opacity=".5"/>'
        if wear == "jeans": det = ""; belt = belt
        if wear == "cowboy": det = f'<path d="M-64,{sh} L-50,{hip} L-10,{hip} L-20,{sh+20}Z M64,{sh} L50,{hip} L16,{hip} L26,{sh+20}Z" fill="#3a2618" stroke="{K}" stroke-width="5"/><path d="M-20,{sh} L4,{sh+30} L28,{sh}" fill="#e8742a" stroke="{K}" stroke-width="4"/>'
        if wear == "knight": det = f'<path d="M-60,{sh+40} Q0,{sh+20} 60,{sh+40} M-62,{sh+90} Q0,{sh+70} 62,{sh+90}" stroke="#5a626e" stroke-width="5" fill="none"/><path d="M-20,{sh+20} L28,{sh+20} L28,{hip-40} L4,{hip-10} L-20,{hip-40}Z" fill="#c62a30" stroke="{K}" stroke-width="4"/><path d="M4,{sh+30} L4,{hip-30} M-12,{sh+70} L20,{sh+70}" stroke="#ffcf3a" stroke-width="6"/>'
        if wear == "viking": det = f'<path d="M-66,{sh} L-60,{hip} L-20,{hip} L-30,{sh+10}Z M66,{sh} L60,{hip} L26,{hip} L34,{sh+10}Z" fill="url(#fur)" stroke="{K}" stroke-width="5"/>'
        if wear == "roman": det = f'<path d="M-62,{sh+10} L62,{sh+10} L66,{hip-20} L-66,{hip-20}Z" fill="url(#metal)" stroke="{K}" stroke-width="5"/>' + "".join(f'<path d="M{x},{hip-20} L{x},{hip+50}" stroke="#6b4a2e" stroke-width="12"/>' for x in (-50, -25, 0, 25, 50))
        if wear == "samurai": det = f'<path d="M-30,{sh} L20,{sh+150} M40,{sh} L4,{sh+90}" stroke="#f6f4ee" stroke-width="8" fill="none"/><path d="M-70,{sh+30} L-90,{sh+90} L-50,{sh+90}Z M70,{sh+30} L90,{sh+90} L50,{sh+90}Z" fill="#8a1e2e" stroke="{K}" stroke-width="5"/><rect x="-70" y="{hip-30}" width="140" height="30" fill="#c9a24a" stroke="{K}" stroke-width="5"/>'
        if wear == "pirate": det = f'<path d="M-64,{sh} L-56,{hip} L-14,{hip} L-24,{sh+20}Z M64,{sh} L56,{hip} L20,{hip} L28,{sh+20}Z" fill="#7a1e26" stroke="{K}" stroke-width="5"/><path d="M-70,{hip+4} L70,{hip+4}" stroke="#c62a30" stroke-width="16"/>'; belt = ""
        if wear == "astronaut": det = f'<rect x="-40" y="{sh+40}" width="80" height="60" rx="8" fill="#c8ccd4" stroke="{K}" stroke-width="5"/><circle cx="-16" cy="{sh+70}" r="8" fill="#c62a30"/><circle cx="16" cy="{sh+70}" r="8" fill="#2a6ac8"/>'; belt = ""
        if wear == "diver": det = f'<path d="M-64,{sh+20} L64,{sh+20}" stroke="#ffc21a" stroke-width="10"/>'; belt = ""
        if wear == "chef": det = "".join(f'<circle cx="{x}" cy="{sh+40+k*40}" r="6" fill="#ccc" stroke="{K}" stroke-width="2"/>' for x in (-20, 30) for k in range(3)) + f'<path d="M-24,{sh-4} L-20,{sh+20} L28,{sh+20} L32,{sh-4}" fill="none" stroke="{K}" stroke-width="4"/>'; belt = ""
        if wear == "pilot": det = f'<path d="M-20,{sh-6} L4,{sh+40} L28,{sh-6}" fill="#fff" stroke="{K}" stroke-width="4"/><path d="M4,{sh+20} L-6,{sh+110} L4,{sh+124} L14,{sh+110}Z" fill="#111"/><path d="M30,{sh+50} l40,0" stroke="#ffcf3a" stroke-width="8"/>'; belt = ""
        if wear == "explorer": det = f'<rect x="-50" y="{sh+40}" width="40" height="34" fill="#a8936a" stroke="{K}" stroke-width="4"/><rect x="20" y="{sh+40}" width="40" height="34" fill="#a8936a" stroke="{K}" stroke-width="4"/>'
        if wear == "coat": det = f'<path d="M-72,{sh} L-82,{hip+140 if pose == "stand" else hip+60} L-6,{hip+140 if pose == "stand" else hip+60} L-6,{sh+20}Z M72,{sh} L82,{hip+140 if pose == "stand" else hip+60} L10,{hip+140 if pose == "stand" else hip+60} L10,{sh+20}Z" fill="{spec.get("outer_color", "#6b4a2e")}" stroke="{K}" stroke-width="6"/>'
        if wear == "lab": det = (f'<path d="M-72,{sh} L-80,{hip+130 if pose == "stand" else hip+60} L-20,{hip+130 if pose == "stand" else hip+60} L-6,{sh+30}Z M72,{sh} L80,{hip+130 if pose == "stand" else hip+60} L26,{hip+130 if pose == "stand" else hip+60} L14,{sh+30}Z" fill="#fbfbfb" stroke="{K}" stroke-width="6"/>')
        out_back.append(legs + torso + belt + det)
        if wear == "lab": sleeve = "#fbfbfb"
        if wear == "coat": sleeve = spec.get("outer_color", "#6b4a2e")
        if wear == "knight": sleeve = "url(#metal)"
    if spec.get("khanjar"):
        y = (P["hip"] - 40) if wear not in ROBES else (P["sh"] + 200)
        out_back.append(f'<path d="M-50,{y} L60,{y}" stroke="#c9b48a" stroke-width="10"/><path d="M0,{y} Q-6,{y+40} 20,{y+70} Q40,{y+76} 36,{y+50} Q20,{y+30} 24,{y}Z" fill="#d8c08a" stroke="{K}" stroke-width="4"/>')
    if spec.get("outer") == "cape":
        oc = spec.get("outer_color", "#8a1e2e")
        out_back.insert(0, f'<path d="{BISHT_BACK[pose]}" fill="{oc}" stroke="{K}" stroke-width="6"/>')
        out_front.append(f'<path d="M-80,{sh-6} Q0,{sh+40} 80,{sh-6} L84,{sh+20} Q0,{sh+70} -84,{sh+20}Z" fill="url(#ermine)" stroke="{K}" stroke-width="5"/>')
    if spec.get("outer") == "bisht":
        oc = spec.get("outer_color", "url(#bishtG)")
        out_back.insert(0, f'<path d="{BISHT_BACK[pose]}" fill="{oc}" stroke="{K}" stroke-width="6"/>')
        if pose in ("stand", "walk"):
            y2 = -18 if pose == "stand" else -30; dx = 0 if pose == "stand" else 14
            out_front.append("".join(f'<path d="M{s*76},{sh-2} Q{s*92},{sh+100} {s*96+dx},{y2} L{s*60+dx},{y2} Q{s*52},{sh+100} {s*30},{sh+2}Z" fill="{oc}" stroke="{K}" stroke-width="6"/><path d="M{s*30},{sh+2} Q{s*52},{sh+100} {s*60+dx},{y2}" stroke="#d8a93a" stroke-width="8" fill="none"/>' for s in (-1, 1)))
        else:
            hp = P["hip"] - 10
            out_front.append(f'<path d="M-76,{sh-8} Q-84,{sh+100} -70,{hp} L-40,{hp} Q-50,{sh+100} -30,{sh-6}Z" fill="{oc}" stroke="{K}" stroke-width="6"/><path d="M-30,{sh-6} Q-50,{sh+100} -40,{hp}" stroke="#d8a93a" stroke-width="8" fill="none"/>')
    back_arm = arm(bx, sh + 24, ba1, ba2, sleeve, sk, hold.get("left", ""), wide)
    front_arm = arm(fx, sh + 24, fa1, fa2, sleeve, sk, hold.get("right", ""), wide)
    hx = 12 + (12 if pose == "kneel" else 0); hy = sh - 120; tilt = {"walk": 3, "kneel": 8}.get(pose, 0)
    hd = f'<g transform="translate({hx} {hy}) rotate({tilt}) scale({hs[0]:.3f} {hs[1]:.3f})">{head(spec, kind)}</g>'
    return back_arm + "".join(out_back) + "".join(out_front) + hd + front_arm

def character(spec, pose="stand", kind="calm"):
    """full character with size by age/build/height. Returns svg group markup (origin = feet)."""
    age = spec.get("age", "adult")
    sx = {"thin": .88, "avg": 1.0, "heavy": 1.22}[spec.get("build", "avg")]
    sy = {"short": .9, "avg": 1.0, "tall": 1.08}[spec.get("height", "avg")]
    s = {"child": .68, "young": .97, "adult": 1.0, "old": .97}[age]
    if spec.get("sex") == "f": sx *= .94; sy *= .96
    hunch = ' rotate(4)' if age == "old" and pose in ("stand", "walk") else ''
    hk = 1.28 if age == "child" else 1.0
    return f'<g transform="scale({s*sx:.3f} {s*sy:.3f}){hunch}">{body(spec, pose, kind, (hk*sy/sx, hk))}</g>'
