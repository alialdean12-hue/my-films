"""Drawing layouts for the 2013 washcloth reenactment. Coordinates: 600 × 840 camera aperture.
Props are original SVG drawings. Character and grip layers are registered to the studio model sheet.
"""
from math import sin,cos,pi
from paint import INK as I,NAVY as N,SLATE as S,ICE as B,AQUA as W,IVORY as C,CORAL as O,SKIN as K,ROSE as R,GOLD as G

def g(s,trans='',attr=''):return f'<g transform="{trans}" {attr}>{s}</g>' if trans else f'<g {attr}>{s}</g>'
def p(d,c='none',line='none',w=1,extra=''):return f'<path d="{d}" fill="{c}" stroke="{line}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" {extra}/>'
def el(x,y,rx,ry,c,line='none',w=1,extra=''):return f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{c}" stroke="{line}" stroke-width="{w}" {extra}/>'
def rect(x,y,w,h,c,extra=''):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{c}" {extra}/>'
def img(name,x,y,w,h,slice=False):return f'<image href="img/{name}.png" x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="'+('xMidYMid slice' if slice else 'none')+'"/>'
def at(s,x,y,z=1,a=0):return g(s,f'translate({x} {y}) rotate({a}) scale({z})')
def shine(x,y,z=1):return at(p('M0 -8 Q1 -1 7 0 Q1 1 0 9 Q-1 1 -7 0 Q-1 -1 0 -8Z',C),x,y,z)

def portrait(x,y,s,k=0,blink=False,tilt=0,watch=False):
    # Cels retain the two hand-inked catchlights, hairline and cheek rim in the base painting.
    eyes=((449,379),(550,384)) if watch else ((405,328),(511,328)); a=img('observe' if watch else 'astronaut',0,0,768,1376)
    if blink:
        for i,(cx,cy) in enumerate(eyes):
            # A skin-colour mask followed by a real drawn tapered lash (not an opacity fade).
            a+=at(p('M-29 2 Q-8 -27 17 -15 Q29 -8 27 10 Q9 21 -19 15Z',K)+p('M-29 3 Q-5 18 23 -1 Q7 13 -5 14 Q-20 13 -29 3Z',I),cx,cy,.98 if not i else .82)
    else:
        for cx,cy in eyes:a+=el(cx+4,cy-6,2.7,3.3,C)+el(cx-4,cy+4,1.55,1.55,B)
    if watch:a=g(a,'translate(-44 -51)')
    return at(g(a,f'rotate({tilt} 378 565)'),x,y,s)

def bead(x=0,y=0,r=10,k=0):
    s=p('M0 -24 C14 -26 26 -13 25 1 C26 17 16 26 0 26 C-14 26 -25 16 -25 2 C-26 -12 -15 -23 0 -24Z',B,B,1.3,'fill-opacity=".42"')+p('M-17 -1 Q-3 -6 12 -3 Q6 -5 1 -7 Q-9 -9 -17 -1Z',B)+p('M-24 3 Q-15 18 1 18 Q19 18 24 0 Q27 24 4 25 Q-19 28 -24 3Z',W)+p('M-18 -5 Q-17 -18 -3 -20 Q3 -19 -2 -15 Q-10 -15 -14 -6Z',C)+el(14,12,3.5,1.8,C)+el(7,-16,2,1.1,B)
    return at(s,x,y,r/25,k)

def cuff(k=0):
    # A facecloth opened from its compressed puck. Broad soft folds, a ribbed woven hem, loose corner.
    drift=(-7,0,9)[k%3]
    a=p(f'M-182 -86 Q-144 -119 -102 -83 Q-77 -69 -41 -88 Q-12 -102 26 -92 Q67 -66 117 -79 Q158 -95 187 -73 L{173+drift} -39 Q154 11 181 75 Q190 109 161 138 Q142 161 168 198 Q130 228 82 201 Q43 184 4 209 Q-58 232 -95 201 Q-123 184 -153 207 Q-199 189 -179 142 Q-156 100 -179 45 Q-200 -6 -174 -49Z',C,I,3)
    a+=p('M-179 -79 Q-142 -115 -106 -79 Q-74 -54 -36 -81 Q-61 -42 -99 -43 Q-141 -71 -174 -39Z',B)+p('M45 -85 Q87 -47 130 -70 Q143 -77 166 -76 Q135 -58 120 -36 Q96 -26 65 -52Z',B)
    a+=p('M-153 200 Q-165 141 -145 108 Q-139 89 -148 57 Q-121 84 -132 125 Q-149 166 -122 197Z',B)+p('M3 205 Q31 193 42 151 Q64 106 45 62 Q80 93 66 131 Q54 172 80 200 Q42 183 3 205Z',B)
    a+=p('M161 137 Q131 154 120 174 Q137 158 151 166 Q151 186 166 198 Q147 201 129 199 Q103 179 115 154Z',S)
    for ix in (0,1,2):
        a+=p(f'M-163 {151+ix*5} Q-136 {142+ix*5} -109 {155+ix*5} T-47 {167+ix*5} T17 {161+ix*5} T85 {154+ix*5} T155 {159+ix*5}', 'none',S,1.1)
    for j in range(25):
        xx=-156+j*13;yy=166+9*sin(j/3);a+=p(f'M{xx} {yy}l3 7','none',B,.9)
    a+=p('M-89 -63 Q-51 -60 -33 -84 M-95 -40 Q-67 -37 -49 -58 M22 -73 Q52 -52 61 -35 M-141 119 Q-131 99 -137 86 M129 106 Q146 89 134 65','none',S,1.15)
    return a

def puck(k=0):
    a=p('M-103 -16 Q-105 -49 -11 -58 Q90 -67 106 -31 L107 13 Q111 47 21 60 Q-75 72 -97 42Z',B,I,3)
    a+=p('M-101 -16 Q-113 -46 -22 -60 Q70 -78 102 -45 Q125 -20 65 2 Q-41 38 -101 -16Z',C,I,2.3)
    for j in range(4):
        y=7+j*8
        a+=p(f'M-93 {y-5}q18 8 31 10t26 3q19 9 33 2t25 -2q31 1 64 -20','none',S,1.4)
    a+=p('M-89 -30q19 -14 39 -13t35 -6q17 -7 29 -4q-14 6 -19 14q-14 9 -35 6t-49 3Z',B)+p('M-69 -16q21 -8 43 -5t51 -10q-9 12 -26 15t-37 3t-31 -3Z',B)+p('M18 -12q19 -22 43 -23q-18 5 -26 19Z',S)
    for j in range(16):a+=p(f'M{-80+j*10} {24+6*sin(j/3)}l-1 5','none',S,.9)
    if k:a+=p('M53 -49 Q64 -74 87 -77 L99 -61 Q79 -49 71 -38Z',C,I,1.5)
    return a

def pouch(k=0):
    a=p('M-161 -103 Q-93 -88 -42 -113 L68 -101 L89 -37 L67 -5 L78 73 Q1 82 -46 99 L-172 74 L-152 33Z',B,I,3)
    a+=p('M-156 -98 L-115 -54 L31 -54 L62 -93 L-39 -106Z',C)+p('M-155 -94 L-136 36 L-164 67 L-121 52 L-112 -41Z',S)+p('M-113 47 L-36 67 L62 51 L68 68 L-46 91 L-159 70Z',S)+p('M34 -51 L64 -83 L73 -40 L60 1 L69 38Z',C)
    a+=p('M-141 -72 L-118 -49 M-120 -32 L-122 -9 M-96 47 Q-37 69 40 47 M-146 62 L-74 78 M43 -90 L26 -70 M-76 -77 L-35 -82','none',I,1.5)
    a+=p('M64 2 L93 4 L99 17 L81 26 L64 19Z',C,I,2.7)+p('M89 8 Q106 11 117 30 Q131 46 149 46 L149 54 Q126 55 111 35 Q101 20 90 18Z',B,I,2.2)+p('M144 43 L157 44 L158 57 L145 57Z',C,I,2)
    a+=p('M-107 -31 Q-68 -42 -32 -37 Q-57 -32 -76 -20 L-99 -12Z',C)+p('M-18 -29 Q8 -36 33 -32 L20 -27 Q4 -26 -18 -22Z',C)+p('M-104 29 Q-69 38 -37 35 M21 26 Q41 20 47 11','none',S,1.6)+el(-83,-52,6,5,N)+el(-81,-54,2,2,C)
    return a

def twisting(t):
    """A new contour and new fold paths at each key, not a rotation of a dry still."""
    h=66-27*t; end=76-16*t;sl=44+73*t; out=p(f'M-225 {-end} Q-168 {-end-10} -135 {-h+6} Q-53 {-h+17} -3 {-h-3} Q61 {-h-25} 114 {-h+6} Q151 {-h+14} 219 {-end} Q245 -9 227 {end} Q177 {end-6} 140 {h-8} Q73 {h-24} 16 {h+3} Q-49 {h+28} -123 {h-9} Q-157 {h-23} -225 {end} Q-249 -4 -225 {-end}Z',C,I,3)
    for i,x in enumerate((-218,-142,-56,30,113)):
        yy=-h+12*sin(i*1.4+.6); hh=h+10*sin(i*2.2)
        out+=p(f'M{x} {hh} Q{x+sl*.66} {hh*.2} {x+sl*.6} {yy*.3} Q{x+sl*.75} {yy} {x+sl} {yy-2} Q{x+sl*.65} {yy+14} {x+sl*.6} 7 Q{x+sl*.65} {hh*.72} {x+12} {hh-1}Z',B)
        out+=p(f'M{x-7} {hh-6} Q{x+sl*.58} {hh*.5} {x+sl*.6} 0 Q{x+sl*.63} {yy*.76} {x+sl-7} {yy+6}','none',S,2.1)
    for j in range(8): out+=p(f'M{-212+2*j} {-37+9*j}q13 -4 20 -2 M{189-j} {-30+7*j}l18 -5','none',S,1)
    return out

def fingerwet(amount,side):
    if amount<=0:return ''
    d=('M539 662 Q542 636 554 619 Q563 595 580 585 Q599 578 612 595 Q622 581 638 585 Q658 586 675 598 Q686 602 695 617 Q670 603 651 605 Q632 603 626 618 Q618 625 606 610 Q591 596 577 618 Q569 632 566 650 Q564 663 551 670Z' if side=='r' else 'M221 686 Q217 666 211 660 Q207 647 196 643 Q179 634 168 645 Q183 640 191 649 Q203 656 202 676 Q203 687 213 691Z')
    glow=('M554 646 Q561 618 581 611' if side=='r' else 'M210 671 Q206 649 190 645')
    s=p(d,W,B,1.2, 'fill-opacity=".53"')+p(glow,'none',C,3.8)
    if side=='r' and amount>.55:s+=el(620,605,3.8,2,C)+p('M568 651 Q574 641 575 636','none',B,1.5)
    if side=='l' and amount>.55:s+=el(174,647,3,1.7,C)
    ax,ay=(543,660) if side=='r' else (220,687)
    return g(s,f'translate({ax} {ay}) scale({amount}) translate({-ax} {-ay})')

def pair(x,y,z=1,a=0,t=.9,wet=.7,paint=False,left=0,right=0):
    """Pair registered in layout units. Cropped wrists continue into/off the camera edges."""
    s='';ang=(1-t)*-13
    if paint:s+=img('wet-folds',193,590,441,196)
    else:
        if wet>0:
            s+=g(p('M-213 -53 Q-177 -76 -140 -54 Q-64 -34 -18 -57 Q42 -85 115 -52 Q166 -18 215 -57 L218 53 Q172 73 120 52 Q61 26 -1 60 Q-75 86 -132 53 Q-178 32 -214 67Z',W,B,2,'fill-opacity=".65"')+p('M-159 57 Q-109 81 -70 66 M35 -63 Q65 -72 90 -58','none',C,4),f'translate(385 691) scale(1 {1+wet*.21})')
        s+=g(twisting(t),f'translate(385 689) scale(1 {1.08-t*.09})')
    if wet>0:
        # Exterior meniscus is a continuous, partly transparent sleeve. Keep the white textile distinctly visible inside.
        film=p('M200 646 Q211 613 248 607 C304 600 331 620 386 611 Q463 588 523 607 Q554 611 578 620 L618 729 Q618 755 598 764 Q572 775 535 763 Q473 764 424 778 Q341 801 279 776 Q230 770 198 750Z',W,B,2.8,'fill-opacity=".14"')
        film+=p('M212 643Q225 619 253 616 M268 614Q288 613 304 617 M409 611Q460 600 485 603 M486 762Q445 768 422 777 M346 782Q326 783 310 780','none',C,4.2)
        film+=p('M239 761 Q264 764 284 770 M509 609 Q531 610 541 615','none',B,2)
        s+=g(film,f'translate(0 692) scale(1 {max(.55,wet)}) translate(0 -692)', f'opacity="{min(1,wet*1.3):.2f}"')
    s+=g(img('grip-left',0,531,249,349)+fingerwet(wet,'l'),f'translate({left} {2+6*(1-t)}) rotate({ang} 183 689)')
    s+=g(img('grip-right',497,543,271,389)+fingerwet(wet,'r'),f'translate({right} {-5*(1-t)}) rotate({-ang*.8} 580 689)')
    return at(g(s,'translate(-384 -694)'),x,y,z,a)

def station(k=0):
    # Stylized 2013-era truss, four pairs of photovoltaic wings; no later rolled-out arrays.
    a=''
    for cx in (-162,-120,117,159):
        a+=p(f'M{cx-3} -49 L{cx+4} -49 L{cx+4} 42 L{cx-3} 42Z',B,I,1.4)
        for sign in (-1,1):
            y=sign*82; h=107; a+=rect(cx-16,y-h/2,32,h,R,f'stroke="{I}" stroke-width="2"');a+=rect(cx-14,y-h/2+3,27,h-6,O)
            for row in range(10):a+=p(f'M{cx-15} {y-50+row*10.5}h30','none',N,1.9)
            a+=p(f'M{cx} {y-52}v104','none',I,2)+p(f'M{cx+13} {y-53}v105','none',G,2)
    a+=p('M-208 -11 L204 -11 L211 -7 L208 8 L-206 8Z',B,I,2)+p('M-206 -11 L200 -11 L206 -7 L-209 -6Z',C)
    for t in range(-202,201,17):a+=p(f'M{t} 5l8 -10l8 10','none',S,1.5)
    for dx,dy,rot,length in [(-15,-14,0,47),(13,2,0,46),(-4,28,88,45),(-57,4,0,47),(-5,-37,87,43),(36,36,55,47)]:
        shell=p(f'M{-length/2} -10 Q-5 -16 {length/2} -9V8 Q8 14 {-length/2} 9Z',C,I,1.8)+p(f'M{-length/2} 3 Q0 11 {length/2} 1V8Q0 15 {-length/2} 9Z',S)+el(length/2,-1,3,9,B,I,1)+p(f'M{-length/2+7} -9v19 M{length/2-7} -10v18','none',S,1)
        a+=at(shell,dx,dy,1,rot)
    a+=p('M56 -12 L70 -47 L43 -61 L37 -79','none',I,4)+p('M56 -12 L70 -47 L43 -61 L37 -79','none',C,2)
    for dx in (-61,51):a+=at(p('M-10 -25 L9 -25 L10 23 L-10 23Z',C,I,1.2)+p('M-10 -15h18 M-10 -5h18M-10 5h18 M-10 15h18','none',S,1.6),dx,-33,1,-8)
    return a

def bg(name,shade=0,x=0,y=0,z=1):return img(name,x,y,600*z,840*z,True)+(rect(0,0,600,840,I,f'opacity="{shade}"') if shade else '')
def orbit(x,y,k,sc=1):return at(station(k),x+4*k,y-k*3,sc,-22+k*.4)

def notebook(k):
    # Diagrammatic marks drawn onto the imaginary notebook, not a replica of the girls' writing.
    a=g(p('M0 10 q20 -19 43 -8 t45 -3 l5 38 q-27 17 -57 2 q-15 -7 -32 2Z','none',S,2.3)+p('M13 33q14 -12 31 -5t38 -2 M10 5q22 -9 34 0 M21 8l-6 17 M64 9l-9 12','none',S,1.4), 'translate(278 185) rotate(-6)')
    if k>=1:
        a+=p('M317 249 Q302 266 312 280 Q325 287 328 272 Q326 262 317 249Z','none',S,2.3)+p('M278 297 Q315 313 355 295 M272 302 Q313 324 359 303','none',S,1.5)
    if k>=2:
        a+=g(p('M0 9 Q4 -8 18 -7 Q34 -7 37 7 Q40 15 23 26 Q15 32 16 41','none',S,5)+el(16,54,3.3,3.3,S),'translate(320 480) rotate(8)')
    return a

def dropsim(k=0):
    # Visual shorthand for cohesive water, not a molecular-scale claim or a second wringing sequence.
    s=p('M-222 21 Q-141 -64 -60 -4 Q5 39 59 -5 Q141 -62 216 9 Q167 80 75 57 Q6 40 -67 57 Q-162 80 -222 21Z',B,S,3) if k==2 else ''
    return s
