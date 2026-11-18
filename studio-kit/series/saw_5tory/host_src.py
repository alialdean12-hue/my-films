"""Draws the saw_5tory narrator: a masked marionette host (SVG). Do not edit the look."""
import math
def spiral(cx,cy,turns=2.4,r0=2,r1=24,n=140):
    p=[]
    for i in range(n+1):
        t=i/n;a=t*turns*2*math.pi;r=r0+(r1-r0)*t;p.append(f"{cx+r*math.cos(a):.1f},{cy+r*math.sin(a):.1f}")
    return "M"+" L".join(p)
def limb(a,b,w1,w2,fill,stroke="#22314f",sw=3):
    (x1,y1),(x2,y2)=a,b;dx,dy=x2-x1,y2-y1;L=math.hypot(dx,dy);nx,ny=-dy/L,dx/L
    pts=[(x1+nx*w1/2,y1+ny*w1/2),(x2+nx*w2/2,y2+ny*w2/2),(x2-nx*w2/2,y2-ny*w2/2),(x1-nx*w1/2,y1-ny*w1/2)]
    return f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x,y in pts)}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"/><circle cx="{x2}" cy="{y2}" r="{w2/2}" fill="{fill}"/>'
def joint(x,y,r=11): return f'<circle cx="{x}" cy="{y}" r="{r}" fill="#1b2438" stroke="#7cc6ff" stroke-width="2"/>'
def glove(x,y,rot,point=False):
    f='<path d="M0,-30 L0,-92" stroke="#f4f6fa" stroke-width="15" stroke-linecap="round"/><path d="M-14,-6 Q-30,4 -26,22" stroke="#f4f6fa" stroke-width="13" stroke-linecap="round" fill="none"/>' if point else '<path d="M-16,30 L-18,58 M-4,34 L-5,66 M9,34 L10,64 M21,28 L24,52" stroke="#f4f6fa" stroke-width="12" stroke-linecap="round"/>'
    return f'<g transform="translate({x} {y}) rotate({rot})"><path d="M-22,-34 L22,-34 L24,-14 L-24,-14 Z" fill="#dfe5ee"/>{f}<rect x="-24" y="-30" width="48" height="60" rx="22" fill="#f4f6fa" stroke="#9aa7bb" stroke-width="2.5"/></g>'
B="#2f8cff";G="#7cc6ff";INK="#05070d"
s=[]
s.append(f'''<defs>
<radialGradient id="bg" cx="50%" cy="38%" r="78%"><stop offset="0" stop-color="#0d2350"/><stop offset=".5" stop-color="#060c1f"/><stop offset="1" stop-color="#020309"/></radialGradient>
<linearGradient id="cone" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6fb6ff" stop-opacity=".26"/><stop offset="1" stop-color="#6fb6ff" stop-opacity="0"/></linearGradient>
<radialGradient id="face" cx="40%" cy="30%" r="80%"><stop offset="0" stop-color="#ffffff"/><stop offset=".55" stop-color="#e7edf4"/><stop offset="1" stop-color="#97a6b9"/></radialGradient>
<linearGradient id="suit" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#1a2236"/><stop offset=".55" stop-color="#0c111d"/><stop offset="1" stop-color="#04060b"/></linearGradient>
<linearGradient id="pant" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#141b2b"/><stop offset="1" stop-color="#05070c"/></linearGradient>
<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="soft"><feGaussianBlur stdDeviation="18"/></filter></defs>
<rect width="1080" height="1920" fill="url(#bg)"/><polygon points="440,0 640,0 960,1780 120,1780" fill="url(#cone)"/>
<ellipse cx="540" cy="1780" rx="300" ry="40" fill="{B}" opacity=".2" filter="url(#soft)"/><ellipse cx="540" cy="1782" rx="150" ry="16" fill="#000" opacity=".7" filter="url(#soft)"/>
<g filter="url(#glow)"><rect x="300" y="60" width="480" height="16" rx="8" fill="#1a2a4a" stroke="{G}" stroke-width="3"/><rect x="532" y="14" width="16" height="130" rx="8" fill="#1a2a4a" stroke="{G}" stroke-width="3"/></g>''')
# strings
s.append(f'<g stroke="{G}" stroke-width="2.2" opacity=".85" filter="url(#glow)"><path d="M540,144 L540,262"/><path d="M308,68 L352,1078"/><path d="M772,68 L906,380"/><path d="M430,68 L478,1352"/><path d="M650,68 L608,1352"/></g>')
# legs (dangling)
s.append(limb((500,1090),(478,1352),74,58,"url(#pant)")); s.append(limb((478,1352),(470,1620),58,46,"url(#pant)"))
s.append(limb((580,1090),(608,1352),74,58,"url(#pant)")); s.append(limb((608,1352),(620,1620),58,46,"#06080e"))
s.append(joint(478,1352)); s.append(joint(608,1352))
s.append('<path d="M446,1608 L496,1608 L500,1640 Q492,1712 462,1710 Q440,1690 446,1608 Z" fill="#000" stroke="#2f4470" stroke-width="3"/>')
s.append('<path d="M596,1608 L646,1608 L650,1690 Q630,1714 606,1708 Q590,1670 596,1608 Z" fill="#000" stroke="#2f4470" stroke-width="3"/>')
# left arm (down) behind torso
s.append('<g id="larm">')
s.append(limb((372,712),(330,905),70,58,"#111827")); s.append(limb((330,905),(352,1060),58,48,"#0d1220")); s.append(joint(330,905))
s.append(glove(354,1092,-8)); s.append('</g>')
# torso
s.append('<path d="M352,700 Q540,668 728,700 Q742,760 716,830 L676,960 Q690,1030 700,1104 L380,1104 Q390,1030 404,960 L364,830 Q338,760 352,700 Z" fill="url(#suit)" stroke="#22314f" stroke-width="4" stroke-linejoin="round"/>')
s.append('<path d="M716,830 L676,960 Q690,1030 700,1104 L672,1104 Q664,1010 652,960 Z" fill="#000" opacity=".35"/>')
s.append(f'<path d="M728,700 Q742,760 716,830" stroke="{G}" stroke-width="3" fill="none" opacity=".6"/>')
s.append('<path d="M500,690 L540,820 L580,690 Z" fill="#eef2f7"/>')
s.append(f'<path d="M528,712 L552,712 L558,748 L548,880 L540,900 L532,880 L522,748 Z" fill="{B}" stroke="#0a3a8a" stroke-width="2" filter="url(#glow)"/><path d="M524,694 L556,694 L552,714 L528,714 Z" fill="#1e6bdf"/>')
s.append('<path d="M478,684 L540,880 L452,830 L430,742 L462,700 Z" fill="#141b2c" stroke="#2f4470" stroke-width="3" stroke-linejoin="round"/>')
s.append('<path d="M602,684 L540,880 L628,830 L650,742 L618,700 Z" fill="#0b101b" stroke="#2f4470" stroke-width="3" stroke-linejoin="round"/>')
s.append('<path d="M540,880 L540,1104" stroke="#2f4470" stroke-width="3"/><circle cx="552" cy="940" r="7" fill="#2f4470"/><circle cx="552" cy="1010" r="7" fill="#2f4470"/>')
s.append(f'<path d="M600,770 L640,760 L636,774 Z" fill="{B}"/>')
# right arm raised, in front
s.append('<g id="rarm">')
s.append(limb((706,712),(808,575),70,58,"#0f1524")); s.append(limb((808,575),(880,418),58,48,"#0a0e18")); s.append(joint(808,575))
s.append(glove(890,392,22,True)); s.append('</g>')
# neck
s.append('<rect x="516" y="606" width="48" height="90" rx="12" fill="#2b3346" stroke="#11182a" stroke-width="3"/>')
# head (smaller)
s.append(f'''<g transform="rotate(-8 540 470)">
<path d="M540,350 C462,350 430,416 430,478 C430,556 474,612 540,626 C606,612 650,556 650,478 C650,416 618,350 540,350 Z" fill="url(#face)" stroke="#0a1224" stroke-width="6"/>
<path d="M540,350 C600,350 640,398 648,460 C620,412 584,388 540,384 Z" fill="#fff" opacity=".55"/>
<path d="M432,490 C440,560 480,612 540,626 C492,590 462,548 452,496 Z" fill="#0a1224" opacity=".18"/>
<path d="M462,540 Q480,560 500,548" stroke="#a6b2c4" stroke-width="3" fill="none"/><path d="M580,548 Q600,560 618,540" stroke="#a6b2c4" stroke-width="3" fill="none"/>
<path d="{spiral(540,418)}" fill="none" stroke="{B}" stroke-width="4" stroke-linecap="round" filter="url(#glow)"/>
<path d="M466,480 C478,456 514,454 524,482 C516,506 476,508 466,480 Z" fill="{INK}"/>
<path d="M556,482 C566,454 602,456 614,480 C604,508 564,506 556,482 Z" fill="{INK}"/>
<g id="eyes"><circle cx="495" cy="482" r="5" fill="{G}" filter="url(#glow)"/><circle cx="585" cy="482" r="5" fill="{G}" filter="url(#glow)"/></g>
<path d="M540,500 L534,548 L546,548" fill="none" stroke="#8592a8" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M508,584 Q540,592 572,584" fill="none" stroke="#0a1224" stroke-width="4.5" stroke-linecap="round"/>
<path d="M436,470 L432,510" stroke="#7d8aa0" stroke-width="2.5"/><path d="M644,470 L648,510" stroke="#7d8aa0" stroke-width="2.5"/>
<ellipse cx="540" cy="372" rx="138" ry="22" fill="#04060c" stroke="#2f4470" stroke-width="3"/>
<path d="M466,372 C464,300 494,262 540,262 C586,262 616,300 614,372 Z" fill="#070a12" stroke="#2f4470" stroke-width="3"/>
<path d="M467,344 L613,344 L614,362 L466,362 Z" fill="{B}" opacity=".85"/>
<path d="M506,280 Q540,268 574,280" stroke="#2f4470" stroke-width="3" fill="none"/>
</g>''')
svg='<svg width="1080" height="1920" viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg">'+"".join(s)+'</svg>'

