"""Collage motion library: 73 motions for the Vox cut-out style.
Every motion is deterministic GSAP on SVG/HTML. Items are drawn around (0,0) inside <g transform="translate(x y)">,
the animated wrapper is <g id=IID transform="translate(dx dy) rotate(r) scale(sx sy)"> (attribute tweens).
See MOTIONS.md for the list (number -> key -> what it does)."""
import math, random

def R(seed):
    x = math.sin(seed * 12.9898 + 78.233) * 43758.5453
    return (x - math.floor(x)) * 2 - 1

def T(dx=0, dy=0, r=0.0, sx=1, sy=1):
    return f"translate({dx:.1f} {dy:.1f}) rotate({r:.1f}) scale({sx:.3f} {sy:.3f})"

def tw(sel, frm, to, at, dur, ease="power2.out", extra=""):
    return f'tl.fromTo("{sel}",{{attr:{{transform:"{frm}"}}{extra}}},{{attr:{{transform:"{to}"}},duration:{dur},ease:"{ease}"}},{at:.2f});'

def jag(w, h, seed, amp=8, step=26):
    pts = []
    for side in range(4):
        n = max(2, int((w if side % 2 == 0 else h) / step))
        for k in range(n):
            t = k / n
            x, y = [(-w/2 + w*t, -h/2), (w/2, -h/2 + h*t), (w/2 - w*t, h/2), (-w/2, h/2 - h*t)][side]
            j = R(seed + side * 97 + k) * amp
            if side % 2 == 0: y += j
            else: x += j
            pts.append((x, y))
    return pts

def pstr(pts): return " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)

# =================================================================== ENTRANCES (wrapper)
def enter(kind, sel, at, tilt=0.0, p=None):
    p = p or {}; end = T(0, 0, tilt)
    js = []
    if kind == "pop":        js.append(tw(sel, T(0, 0, tilt - 12, .02, .02), end, at, .45, "back.out(2.2)"))
    elif kind == "hop":      # 10 squash & stretch landing
        js.append(tw(sel, T(0, -700, tilt, .9, 1.1), T(0, 0, tilt, 1.25, .72), at, .42, "power2.in"))
        js.append(f'tl.to("{sel}",{{attr:{{transform:"{T(0,-160,tilt,.88,1.12)}"}},duration:.22,ease:"power2.out"}},{at+.42:.2f});tl.to("{sel}",{{attr:{{transform:"{T(0,0,tilt,1.1,.88)}"}},duration:.2,ease:"power2.in"}},{at+.64:.2f});tl.to("{sel}",{{attr:{{transform:"{end}"}},duration:.18,ease:"power1.out"}},{at+.84:.2f});')
    elif kind == "bounce":   js.append(tw(sel, T(0, -900, tilt + 8), end, at, .8, "bounce.out"))           # 13
    elif kind in ("slide", "left", "right", "top", "bottom"):                                            # 14
        d = p.get("from", kind if kind != "slide" else "left"); dx, dy = {"left": (-1100, 0), "right": (1100, 0), "top": (0, -1400), "bottom": (0, 1400)}[d]
        js.append(tw(sel, T(dx, dy, tilt), end, at, .5, "power3.out"))
    elif kind == "spin":     js.append(tw(sel, T(0, 0, tilt - 360, .1, .1), end, at, .7, "back.out(1.4)"))   # 15
    elif kind == "zoom":     js.append(tw(sel, T(0, 0, tilt, .01, .01), end, at, .5, "expo.out"))           # 16
    elif kind == "fade":     js.append(f'tl.fromTo("{sel}",{{opacity:0}},{{opacity:1,duration:.4}},{at:.2f});')
    elif kind == "toss":     # 20 thrown on the table from below, spinning
        js.append(tw(sel, T(R(at) * 300, 1300, tilt + 90 * (1 if R(at+1) > 0 else -1), 1.3, 1.3), end, at, .55, "power3.out"))
    elif kind == "string":   # 23 lowered on a string, then swings
        js.append(tw(sel, T(0, -1500, tilt), T(0, 0, tilt + 10), at, .7, "power2.out"))
        js.append(f'tl.to("{sel}",{{attr:{{transform:"{end}"}},duration:1.6,ease:"elastic.out(1,0.3)"}},{at+.7:.2f});')
    else:                    js.append(tw(sel, T(0, -380, tilt + 12), end, at, .55, "back.out(1.4)"))       # drop
    return js

def exit_(kind, sel, at, tilt=0.0):
    if kind == "fly_left":  return [tw(sel, T(0, 0, tilt), T(-1300, 0, tilt - 20), at, .45, "power2.in")]
    if kind == "fly_right": return [tw(sel, T(0, 0, tilt), T(1300, 0, tilt + 20), at, .45, "power2.in")]
    if kind == "drop":      return [tw(sel, T(0, 0, tilt), T(0, 1500, tilt + 25), at, .5, "power2.in")]
    if kind == "shrink":    return [tw(sel, T(0, 0, tilt), T(0, 0, tilt + 30, .01, .01), at, .35, "back.in(2)")]
    return [f'tl.to("{sel}",{{opacity:0,duration:.3}},{at:.2f});']

# =================================================================== LOOPS (on an inner group)
def loop(kind, sel, t0, t1, seed=0, p=None):
    p = p or {}; D = max(.5, t1 - t0)
    if kind == "boil":    # 12 stop-motion paper jitter (only characters!)
        return [f'for(let t={t0:.2f},n={seed*100};t<{t1:.2f};t+=1/8,n++){{const a=Math.sin(n*12.9898)*43758.5453,f=a-Math.floor(a);tl.set("{sel}",{{attr:{{transform:`translate(${{(f*8-4).toFixed(1)}} ${{((f*7%1)*8-4).toFixed(1)}}) rotate(${{((f*13%1)*3-1.5).toFixed(2)}}) scale(1 1)`}}}},t);}}']
    yoyo = lambda frm, to, per, ease="sine.inOut": f'tl.fromTo("{sel}",{{attr:{{transform:"{frm}"}}}},{{attr:{{transform:"{to}"}},duration:{per/2:.2f},ease:"{ease}",yoyo:true,repeat:{int(D/(per/2))}}},{t0:.2f});'
    if kind == "swing":   a = p.get("a", 8); return [yoyo(T(0, 0, -a), T(0, 0, a), 2.0)]          # 8 (pivot = item centre top via parent)
    if kind == "float":   return [yoyo(T(0, -14), T(0, 14), 3.0)]                                  # 45
    if kind == "breathe": return [yoyo(T(0, 0, 0, 1, 1), T(0, 0, 0, 1.04, 1.04), 2.4)]             # 46
    if kind == "tremble": return [yoyo(T(-4, 0, -.8), T(4, 0, .8), .12, "none")]                   # 47
    if kind == "wind":    return [yoyo(T(-10, 0, -4, 1, 1), T(14, -6, 5, .97, 1), 1.3)]            # 48
    if kind == "parallax":                                                                         # 49 (depth 0..1)
        d = p.get("depth", .5); return [f'tl.fromTo("{sel}",{{attr:{{transform:"{T(60*d,0)}"}}}},{{attr:{{transform:"{T(-60*d,0)}"}},duration:{D:.2f},ease:"none"}},{t0:.2f});']
    if kind == "spin":    return [f'tl.fromTo("{sel}",{{attr:{{transform:"{T(0,0,0)}"}}}},{{attr:{{transform:"{T(0,0,D*30)}"}},duration:{D:.2f},ease:"none"}},{t0:.2f});']  # 50
    if kind == "flicker": return [f'for(let t={t0:.2f},n=0;t<{t1:.2f};t+=.09,n++){{tl.set("{sel}",{{opacity:(Math.sin(n*7.3)>.6?.55:1)}},t);}}']                      # 51
    if kind == "wave":    return []   # 28 handled in content (displacement)
    return []

# =================================================================== CONTENT EFFECTS (one-shot, need the drawn content)
def effect(kind, iid, content, w, h, at, p, seed):
    """returns (svg, js). content is drawn around 0,0 with size w x h. kind = paper / tear / reveal effect."""
    p = p or {}; js = []; s = f"#{iid}"
    if kind in ("crumple", "uncrumple"):                                   # 2 / 3
        wr = "".join(f'<path d="M{R(seed+k)*w*.45:.0f},{R(seed+k+50)*h*.45:.0f} l{R(seed+k+9)*160:.0f},{R(seed+k+19)*160:.0f} l{R(seed+k+29)*120:.0f},{R(seed+k+39)*120:.0f}" stroke="#000" stroke-opacity=".35" stroke-width="3" fill="none"/>' for k in range(24))
        svg = (f'<filter id="f{iid}" x="-40%" y="-40%" width="180%" height="180%"><feTurbulence type="fractalNoise" baseFrequency=".02" numOctaves="3" seed="{seed%50}"/><feDisplacementMap id="d{iid}" in="SourceGraphic" scale="{0 if kind=="crumple" else 130}" xChannelSelector="R" yChannelSelector="G"/></filter>'
               f'<g id="g{iid}" transform="{T(0,0,0) if kind=="crumple" else T(0,0,200,.22,.22)}"><g filter="url(#f{iid})">{content}<g id="w{iid}" opacity="{0 if kind=="crumple" else 1}">{wr}</g></g></g>')
        if kind == "crumple":
            js += [f'tl.to("#d{iid}",{{attr:{{scale:130}},duration:.75,ease:"power2.in"}},{at:.2f});tl.to("#w{iid}",{{opacity:1,duration:.5}},{at:.2f});',
                   f'tl.to("#g{iid}",{{attr:{{transform:"{T(0,0,170,.24,.24)}"}},duration:.75,ease:"power2.in"}},{at:.2f});',
                   f'tl.to("#g{iid}",{{attr:{{transform:"{T(p.get("throw_x",-1100),400,480,.2,.2)}"}},duration:.5,ease:"power2.in"}},{at+.85:.2f});']
        else:
            js += [f'tl.to("#d{iid}",{{attr:{{scale:0}},duration:.9,ease:"power3.out"}},{at:.2f});tl.to("#w{iid}",{{opacity:.12,duration:.9}},{at:.2f});',
                   f'tl.to("#g{iid}",{{attr:{{transform:"{T(0,0,0)}"}},duration:.9,ease:"back.out(1.3)"}},{at:.2f});']
        return svg, js
    if kind == "peel":                                                       # 4
        pp = lambda q: pstr([(-w/2, -h/2), (w/2, -h/2), (w/2, h/2 - q), (w/2 - q, h/2), (-w/2, h/2)])
        fl = lambda q: pstr([(w/2, h/2 - q), (w/2 - q, h/2), (w/2 - q, h/2 - q)])
        q = min(w, h) * .9
        svg = f'<clipPath id="c{iid}"><polygon id="pc{iid}" points="{pp(0)}"/></clipPath><g id="g{iid}" transform="{T()}"><g clip-path="url(#c{iid})">{content}</g><polygon id="fl{iid}" points="{fl(0)}" fill="#f2eee2" stroke="#d6cfba" stroke-width="3"/></g>'
        js += [f'tl.to("#pc{iid}",{{attr:{{points:"{pp(q)}"}},duration:.9,ease:"power1.in"}},{at:.2f});tl.to("#fl{iid}",{{attr:{{points:"{fl(q)}"}},duration:.9,ease:"power1.in"}},{at:.2f});',
               f'tl.to("#g{iid}",{{attr:{{transform:"{T(-1000,-700,-30)}"}},duration:.45,ease:"power2.in"}},{at+.95:.2f});']
        return svg, js
    if kind in ("unfold", "fold"):                                           # 5 / 24
        th = h / 3
        clips = "".join(f'<clipPath id="c{iid}{k}"><rect x="{-w/2}" y="{-h/2+k*th}" width="{w}" height="{th+1}"/></clipPath>' for k in range(3))
        def pan(k, folded):
            hinge = -h/2 + (th if k == 0 else 2*th)
            sc = -0.02 if folded else 1
            return (f'<g id="p{k}{iid}" transform="translate(0 {hinge:.1f}) scale(1 {sc}) translate(0 {-hinge:.1f})"><g clip-path="url(#c{iid}{k})">{content}</g>'
                    f'<rect id="sh{k}{iid}" x="{-w/2}" y="{-h/2+k*th}" width="{w}" height="{th}" fill="#000" opacity="{.45 if folded else 0}"/></g>')
        start_folded = kind == "unfold"
        svg = clips + f'<g clip-path="url(#c{iid}1)">{content}</g>' + pan(0, start_folded) + pan(2, start_folded)
        for k, dt in ((0, 0), (2, .55)):
            hinge = -h/2 + (th if k == 0 else 2*th)
            a, b = ("-0.02", "1") if start_folded else ("1", "-0.02")
            js.append(f'tl.fromTo("#p{k}{iid}",{{attr:{{transform:"translate(0 {hinge:.1f}) scale(1 {a}) translate(0 {-hinge:.1f})"}}}},{{attr:{{transform:"translate(0 {hinge:.1f}) scale(1 {b}) translate(0 {-hinge:.1f})"}},duration:.55,ease:"power2.inOut"}},{at+dt:.2f});')
            js.append(f'tl.to("#sh{k}{iid}",{{opacity:{0 if start_folded else .45},duration:.55}},{at+dt:.2f});')
        return svg, js
    if kind == "flip":                                                       # 7 (p.back = svg of the back side)
        back = p.get("back_svg", f'<rect x="{-w/2}" y="{-h/2}" width="{w}" height="{h}" fill="#2f5a46"/>')
        svg = f'<g id="g{iid}" transform="{T()}"><g id="a{iid}">{content}</g><g id="b{iid}" opacity="0">{back}</g></g>'
        js += [f'tl.to("#g{iid}",{{attr:{{transform:"{T(0,0,0,.01,1)}"}},duration:.3,ease:"power2.in"}},{at:.2f});tl.set("#a{iid}",{{opacity:0}},{at+.3:.2f});tl.set("#b{iid}",{{opacity:1}},{at+.3:.2f});',
               f'tl.to("#g{iid}",{{attr:{{transform:"{T()}"}},duration:.45,ease:"back.out(1.6)"}},{at+.3:.2f});']
        return svg, js
    if kind == "origami":                                                    # 25 fold into a triangle, then a smaller triangle
        tri1 = pstr([(-w/2, -h/2), (w/2, -h/2), (w/2, h/2), (-w/2, h/2)])
        svg = (f'<clipPath id="c{iid}"><polygon id="pc{iid}" points="{tri1}"/></clipPath><g id="g{iid}" transform="{T()}"><g clip-path="url(#c{iid})">{content}</g>'
               f'<polygon id="fl{iid}" points="{pstr([(-w/2,h/2),(-w/2,h/2),(-w/2,h/2),(-w/2,h/2)])}" fill="#efe9da" stroke="#c9c0a8" stroke-width="3"/></g>')
        js += [f'tl.to("#pc{iid}",{{attr:{{points:"{pstr([(-w/2,-h/2),(w/2,-h/2),(w/2,h/2),(w/2,h/2)])}"}},duration:.5,ease:"power2.inOut"}},{at:.2f});',
               f'tl.to("#fl{iid}",{{attr:{{points:"{pstr([(-w/2,-h/2),(w/2,h/2),(w/2,-h/2+ (h-w if h>w else 0)*0),(-w/2,-h/2)])}"}},duration:.5,ease:"power2.inOut"}},{at:.2f});',
               f'tl.to("#g{iid}",{{attr:{{transform:"{T(0,0,45,.5,.5)}"}},duration:.5,ease:"power2.inOut"}},{at+.6:.2f});tl.to("#g{iid}",{{attr:{{transform:"{T(900,-900,120,.3,.3)}"}},duration:.5,ease:"power2.in"}},{at+1.2:.2f});']
        return svg, js
    if kind == "roll":                                                       # 26 rolls up into a tube
        svg = (f'<g id="g{iid}" transform="translate(0 {-h/2}) scale(1 1) translate(0 {h/2})"><g>{content}</g>'
               f'<rect id="sh{iid}" x="{-w/2}" y="{-h/2}" width="{w}" height="{h}" fill="url(#rollgrad)" opacity="0"/></g><rect id="tube{iid}" x="{-w/2-6}" y="{-h/2-30}" width="{w+12}" height="0" rx="30" fill="#e8e2d0" stroke="#bfb69e" stroke-width="3"/>')
        js += [f'tl.to("#g{iid}",{{attr:{{transform:"translate(0 {-h/2}) scale(1 0.02) translate(0 {h/2})"}},duration:.7,ease:"power2.in"}},{at:.2f});tl.to("#sh{iid}",{{opacity:.8,duration:.7}},{at:.2f});',
               f'tl.to("#tube{iid}",{{attr:{{height:60}},duration:.5}},{at+.3:.2f});']
        return svg, js
    if kind == "curl":                                                       # 27 corner lifts in the wind (loops)
        fl = lambda q: pstr([(w/2, -h/2 + q), (w/2 - q, -h/2), (w/2 - q * 1.1, -h/2 + q * 1.1)])
        cp = lambda q: pstr([(-w/2, -h/2), (w/2 - q, -h/2), (w/2, -h/2 + q), (w/2, h/2), (-w/2, h/2)])
        q = min(w, h) * .22
        svg = f'<clipPath id="c{iid}"><polygon id="pc{iid}" points="{cp(0)}"/></clipPath><g clip-path="url(#c{iid})">{content}</g><polygon id="fl{iid}" points="{fl(0)}" fill="#f2eee2" stroke="#d6cfba" stroke-width="3"/>'
        js += [f'tl.fromTo("#pc{iid}",{{attr:{{points:"{cp(4)}"}}}},{{attr:{{points:"{cp(q)}"}},duration:.8,ease:"sine.inOut",yoyo:true,repeat:5}},{at:.2f});tl.fromTo("#fl{iid}",{{attr:{{points:"{fl(4)}"}}}},{{attr:{{points:"{fl(q)}"}},duration:.8,ease:"sine.inOut",yoyo:true,repeat:5}},{at:.2f});']
        return svg, js
    if kind == "wave":                                                       # 28 paper waving in the air
        svg = (f'<filter id="f{iid}" x="-20%" y="-20%" width="140%" height="140%"><feTurbulence id="t{iid}" type="turbulence" baseFrequency="0.004 0.012" numOctaves="1" seed="{seed%40}"/><feDisplacementMap in="SourceGraphic" scale="28" xChannelSelector="R" yChannelSelector="G"/></filter><g filter="url(#f{iid})">{content}</g>')
        js.append(f'tl.fromTo("#t{iid}",{{attr:{{baseFrequency:"0.004 0.012"}}}},{{attr:{{baseFrequency:"0.006 0.02"}},duration:1.2,ease:"sine.inOut",yoyo:true,repeat:8}},{at:.2f});')
        return svg, js
    if kind == "plane":                                                      # 29 folds into a paper plane and flies away
        plane = f'<g id="pl{iid}" opacity="0" transform="{T(0,0,0,.01,.01)}"><path d="M-160,20 L170,-40 L-60,70 Z" fill="#fbf8f0" stroke="#bfb69e" stroke-width="4"/><path d="M-60,70 L170,-40 L-20,10 Z" fill="#e8e2d0" stroke="#bfb69e" stroke-width="4"/></g>'
        svg = f'<g id="g{iid}" transform="{T()}">{content}</g>{plane}'
        js += [f'tl.to("#g{iid}",{{attr:{{transform:"{T(0,0,-20,.05,.4)}"}},opacity:0,duration:.5,ease:"power2.in"}},{at:.2f});',
               f'tl.to("#pl{iid}",{{opacity:1,attr:{{transform:"{T(0,0,-10,1,1)}"}},duration:.3,ease:"back.out(2)"}},{at+.4:.2f});',
               f'tl.to("#pl{iid}",{{attr:{{transform:"{T(900,-1000,-25,.6,.6)}"}},duration:.9,ease:"power2.in"}},{at+.85:.2f});']
        return svg, js
    if kind == "tear":                                                       # 1 tear in two halves
        line = [(R(seed + k) * 22, -h/2 - 20 + (h + 40) * k / 20) for k in range(21)]
        Lp = [(-w/2 - 40, -h/2 - 40)] + line + [(-w/2 - 40, h/2 + 40)]; Rp = [(w/2 + 40, -h/2 - 40)] + line + [(w/2 + 40, h/2 + 40)]
        svg = (f'<clipPath id="l{iid}"><polygon points="{pstr(Lp)}"/></clipPath><clipPath id="r{iid}"><polygon points="{pstr(Rp)}"/></clipPath>'
               f'<g id="L{iid}" transform="{T()}"><g clip-path="url(#l{iid})">{content}</g><polyline points="{pstr(line)}" fill="none" stroke="#fbf8f0" stroke-width="7"/></g>'
               f'<g id="R{iid}" transform="{T()}"><g clip-path="url(#r{iid})">{content}</g><polyline points="{pstr(line)}" fill="none" stroke="#fbf8f0" stroke-width="7"/></g>')
        js += [f'tl.to("#L{iid}",{{attr:{{transform:"{T(-6,0,-1)}"}},duration:.1,yoyo:true,repeat:3}},{at-.45:.2f});',
               f'tl.to("#L{iid}",{{attr:{{transform:"{T(-900,140,-16)}"}},duration:.7,ease:"power2.in"}},{at:.2f});tl.to("#R{iid}",{{attr:{{transform:"{T(900,-60,14)}"}},duration:.7,ease:"power2.in"}},{at+.05:.2f});']
        return svg, js
    if kind in ("shred_in", "shred_out", "shredder"):                        # 6 / 34
        N = 8; sw = w / N
        strips = "".join(f'<clipPath id="c{iid}{k}"><rect x="{-w/2+k*sw}" y="{-h/2-10}" width="{sw-5}" height="{h+20}"/></clipPath><g id="s{k}{iid}" transform="{T(0,-1500 if kind=="shred_in" else 0)}"><g clip-path="url(#c{iid}{k})">{content}</g></g>' for k in range(N))
        svg = strips
        if kind == "shredder":
            svg = f'<g id="m{iid}"><rect x="{-w/2-40}" y="{h/2+10}" width="{w+80}" height="120" rx="16" fill="#3a3e44"/><rect x="{-w/2-20}" y="{h/2+20}" width="{w+40}" height="16" fill="#111"/></g>' + strips.replace(f'transform="{T(0,0)}"', f'transform="{T(0,0)}"')
        for k in range(N):
            if kind == "shred_in": js.append(f'tl.to("#s{k}{iid}",{{attr:{{transform:"{T(0,0)}"}},duration:.45,ease:"back.out(1.3)"}},{at+k*.07:.2f});')
            elif kind == "shred_out": js.append(f'tl.to("#s{k}{iid}",{{attr:{{transform:"{T(R(seed+k)*80,1700,R(seed+k+3)*30)}"}},duration:.55,ease:"power2.in"}},{at+((k*3)%N)*.06:.2f});')
            else: js.append(f'tl.to("#s{k}{iid}",{{attr:{{transform:"{T(0,h+60)}"}},duration:1.0,ease:"none"}},{at:.2f});tl.to("#s{k}{iid}",{{attr:{{transform:"{T(R(seed+k)*40,h+260,R(seed+k+3)*12)}"}},duration:.4,ease:"power1.in"}},{at+1.0:.2f});')
        return svg, js
    if kind == "strip":                                                      # 30 a strip is torn out of the middle
        a = [(-w/2-30, -h*.12 + R(seed+k)*10) for k in range(1)]
        top = [(-w/2-30, -h/2-30), (w/2+30, -h/2-30)] + [(w/2+30 - (w+60)*k/16, -h*.1 + R(seed+k)*14) for k in range(17)]
        bot = [(-w/2-30, h/2+30), (w/2+30, h/2+30)] + [(w/2+30 - (w+60)*k/16, h*.1 + R(seed+k+40)*14) for k in range(17)]
        mid = [(w/2+30 - (w+60)*k/16, -h*.1 + R(seed+k)*14) for k in range(17)] + [(-w/2-30 + (w+60)*k/16, h*.1 + R(seed+(16-k)+40)*14) for k in range(17)]
        svg = (f'<clipPath id="t{iid}"><polygon points="{pstr(top)}"/></clipPath><clipPath id="b{iid}"><polygon points="{pstr(bot)}"/></clipPath><clipPath id="m{iid}"><polygon points="{pstr(mid)}"/></clipPath>'
               f'<g id="T{iid}" transform="{T()}"><g clip-path="url(#t{iid})">{content}</g></g><g id="B{iid}" transform="{T()}"><g clip-path="url(#b{iid})">{content}</g></g><g id="M{iid}" transform="{T()}"><g clip-path="url(#m{iid})">{content}</g></g>')
        js += [f'tl.to("#M{iid}",{{attr:{{transform:"{T(-1300,-200,-25)}"}},duration:.6,ease:"power2.in"}},{at:.2f});tl.to("#T{iid}",{{attr:{{transform:"{T(0,-40,-2)}"}},duration:.3}},{at:.2f});tl.to("#B{iid}",{{attr:{{transform:"{T(0,40,2)}"}},duration:.3}},{at:.2f});']
        return svg, js
    if kind == "scissors":                                                   # 31 cut along a dashed line, piece falls
        cw, ch = w * .5, h * .5; cx, cy = p.get("cx", 0), p.get("cy", 0)
        rect = f"M{cx-cw/2},{cy-ch/2} H{cx+cw/2} V{cy+ch/2} H{cx-cw/2} Z"; per = 2 * (cw + ch)
        sc = '<g><ellipse cx="-30" cy="-18" rx="18" ry="12" fill="none" stroke="#e5322d" stroke-width="7"/><ellipse cx="-30" cy="18" rx="18" ry="12" fill="none" stroke="#e5322d" stroke-width="7"/><path d="M-14,-12 L40,6 M-14,12 L40,-6" stroke="#9aa4b2" stroke-width="7" stroke-linecap="round"/></g>'
        pts = [(cx-cw/2, cy-ch/2), (cx+cw/2, cy-ch/2), (cx+cw/2, cy+ch/2), (cx-cw/2, cy+ch/2), (cx-cw/2, cy-ch/2)]
        svg = (f'{content}<g id="pc{iid}" transform="{T()}"><clipPath id="cc{iid}"><path d="{rect}"/></clipPath><g clip-path="url(#cc{iid})">{content}</g></g>'
               f'<path d="{rect}" fill="none" stroke="#151515" stroke-width="5" stroke-dasharray="14 10"/><path id="cut{iid}" d="{rect}" fill="none" stroke="#fbf8f0" stroke-width="8" stroke-dasharray="{per:.0f}" stroke-dashoffset="{per:.0f}"/>'
               f'<g id="sc{iid}" transform="translate({pts[0][0]} {pts[0][1]})">{sc}</g><rect id="hole{iid}" x="{cx-cw/2}" y="{cy-ch/2}" width="{cw}" height="{ch}" fill="var(--paper)" opacity="0"/>')
        js.append(f'tl.to("#cut{iid}",{{strokeDashoffset:0,duration:1.2,ease:"none"}},{at:.2f});')
        for k in range(4):
            js.append(f'tl.to("#sc{iid}",{{attr:{{transform:"translate({pts[k+1][0]} {pts[k+1][1]})"}},duration:.3,ease:"none"}},{at+k*.3:.2f});')
        js += [f'tl.set("#hole{iid}",{{opacity:1}},{at+1.25:.2f});tl.to("#pc{iid}",{{attr:{{transform:"{T(120,1300,40)}"}},duration:.7,ease:"power2.in"}},{at+1.25:.2f});tl.to("#sc{iid}",{{opacity:0,duration:.2}},{at+1.25:.2f});']
        return svg, js
    if kind == "hole":                                                       # 32 a torn hole grows in the item
        hp = " L".join(f"{math.cos(a)*(1+R(seed+k)*.2):.3f},{math.sin(a)*(1+R(seed+k)*.2):.3f}" for k, a in enumerate([j*2*math.pi/28 for j in range(28)]))
        svg = f'<mask id="m{iid}"><rect x="{-w}" y="{-h}" width="{2*w}" height="{2*h}" fill="#fff"/><path id="hp{iid}" d="M{hp} Z" fill="#000" transform="scale(1)"/></mask><g mask="url(#m{iid})">{content}</g><path id="he{iid}" d="M{hp} Z" fill="none" stroke="#fbf8f0" stroke-width=".05" transform="scale(1)"/>'
        js.append(f'tl.fromTo(["#hp{iid}","#he{iid}"],{{attr:{{transform:"scale(1)"}}}},{{attr:{{transform:"scale({max(w,h)*.8:.0f})"}},duration:.9,ease:"power3.in"}},{at:.2f});')
        return svg, js
    if kind == "shatter":                                                    # 33 tears into many pieces that scatter
        cols, rows = 3, 3; pieces = ""
        for k in range(cols * rows):
            cx, cy = -w/2 + (k % cols + .5) * w / cols, -h/2 + (k // cols + .5) * h / rows
            poly = [(cx + (w/cols/2 + 10) * math.cos(a) * (1 + R(seed+k*7+j)*.15), cy + (h/rows/2 + 10) * math.sin(a) * (1 + R(seed+k*5+j)*.15)) for j, a in enumerate([i * math.pi / 3 for i in range(6)])]
            pieces += f'<clipPath id="c{iid}{k}"><polygon points="{pstr(poly)}"/></clipPath><g id="p{k}{iid}" transform="{T()}"><g clip-path="url(#c{iid}{k})">{content}</g></g>'
            js.append(f'tl.to("#p{k}{iid}",{{attr:{{transform:"{T(R(seed+k)*900, R(seed+k+9)*900 + 400, R(seed+k+3)*120, .7, .7)}"}},duration:.7,ease:"power2.in"}},{at + (k%3)*.04:.2f});')
        return pieces, js
    if kind == "crop_zoom":                                                  # 35 a detail is cut out and enlarged
        cx, cy, cw, ch = p.get("cx", 0), p.get("cy", 0), w * .34, h * .34; k_ = p.get("k", 2.2)
        svg = (f'{content}<rect x="{cx-cw/2}" y="{cy-ch/2}" width="{cw}" height="{ch}" fill="none" stroke="#e5322d" stroke-width="6" stroke-dasharray="12 8"/>'
               f'<clipPath id="cz{iid}"><rect x="{cx-cw/2}" y="{cy-ch/2}" width="{cw}" height="{ch}"/></clipPath>'
               f'<g id="z{iid}" transform="translate({cx} {cy}) scale(1) translate({-cx} {-cy})"><rect x="{cx-cw/2-10}" y="{cy-ch/2-10}" width="{cw+20}" height="{ch+20}" fill="#fbf8f0" filter="url(#shd)"/><g clip-path="url(#cz{iid})">{content}</g></g>')
        js.append(f'tl.to("#z{iid}",{{attr:{{transform:"translate({p.get("tx",cx+w*.15)} {p.get("ty",cy-h*.25)}) scale({k_}) translate({-cx} {-cy})"}},duration:.6,ease:"back.out(1.4)"}},{at:.2f});')
        return svg, js
    if kind == "polaroid":                                                   # 40 develops from dark
        svg = f'{content}<rect id="dv{iid}" x="{-w/2}" y="{-h/2}" width="{w}" height="{h}" fill="#141210" opacity="1"/>'
        js.append(f'tl.to("#dv{iid}",{{opacity:0,duration:1.8,ease:"power1.in"}},{at:.2f});')
        return svg, js
    if kind == "magnifier":                                                  # 57 lens moves over the item showing it 2x
        (x1, y1), (x2, y2) = p.get("path", [(-w*.25, -h*.15), (w*.25, h*.15)]); r = p.get("r", min(w, h) * .22); k_ = p.get("k", 2)
        zt = lambda x, y: f"translate({x:.1f} {y:.1f}) scale({k_}) translate({-x:.1f} {-y:.1f})"
        svg = (f'{content}<clipPath id="mc{iid}"><circle id="mcc{iid}" cx="{x1}" cy="{y1}" r="{r}"/></clipPath><g clip-path="url(#mc{iid})"><g id="mz{iid}" transform="{zt(x1,y1)}">{content}</g></g>'
               f'<g id="ml{iid}" transform="translate({x1} {y1})"><circle r="{r}" fill="none" stroke="#c9a24a" stroke-width="12"/><path d="M{r*.7:.0f},{r*.7:.0f} l{r*.6:.0f},{r*.6:.0f}" stroke="#5a3a22" stroke-width="24" stroke-linecap="round"/></g>')
        d = p.get("dur", 1.6)
        js += [f'tl.to("#mcc{iid}",{{attr:{{cx:{x2},cy:{y2}}},duration:{d},ease:"sine.inOut"}},{at:.2f});tl.to("#mz{iid}",{{attr:{{transform:"{zt(x2,y2)}"}},duration:{d},ease:"sine.inOut"}},{at:.2f});tl.to("#ml{iid}",{{attr:{{transform:"translate({x2} {y2})"}},duration:{d},ease:"sine.inOut"}},{at:.2f});']
        return svg, js
    if kind == "mask_reveal":                                                # 17 a paper flap is pulled off the item
        svg = f'{content}<g id="mr{iid}" transform="{T()}"><rect x="{-w/2-12}" y="{-h/2-12}" width="{w+24}" height="{h+24}" fill="#e8dfc8" stroke="#c9bfa4" stroke-width="3"/><text x="0" y="20" text-anchor="middle" font-family="Cairo" font-weight="900" font-size="{int(min(w,h)*.18)}" fill="#8a7a5a">؟</text></g>'
        js.append(f'tl.to("#mr{iid}",{{attr:{{transform:"{T(1200,-300,25)}"}},duration:.6,ease:"power2.in"}},{at:.2f});')
        return svg, js
    if kind in ("envelope", "folder"):                                       # 18 / 19 slides out of an envelope / folder
        ew, eh = w + 80, h * .7
        holder = (f'<rect x="{-ew/2}" y="{h/2-eh+40}" width="{ew}" height="{eh}" rx="8" fill="{"#e8d8b0" if kind=="envelope" else "#d8a64a"}" stroke="#8a7a5a" stroke-width="4"/>')
        front = (f'<path d="M{-ew/2},{h/2-eh+40} L0,{h/2-eh*0.35+40} L{ew/2},{h/2-eh+40} V{h/2+40} H{-ew/2} Z" fill="{"#f2e6c4" if kind=="envelope" else "#e8b65a"}" stroke="#8a7a5a" stroke-width="4"/>'
                 if kind == "envelope" else f'<rect x="{-ew/2}" y="{h/2-eh*0.6+40}" width="{ew}" height="{eh*0.6}" rx="8" fill="#e8b65a" stroke="#8a7a5a" stroke-width="4"/><text x="0" y="{h/2-eh*0.3+60}" text-anchor="middle" font-family="Cairo" font-weight="900" font-size="54" fill="#5a3a12" direction="rtl">سرّي</text>')
        svg = f'{holder}<g id="in{iid}" transform="{T(0, eh*.9)}">{content}</g>{front}'
        js.append(f'tl.to("#in{iid}",{{attr:{{transform:"{T(0,-eh*.25,-3)}"}},duration:.7,ease:"power2.out"}},{at:.2f});')
        return svg, js
    return content, js

# =================================================================== annotation / info content
def tape(w, h, seed):                                                        # 21 tape strips
    return "".join(f'<rect class="tp" x="{cx-70}" y="{-h/2-34}" width="140" height="46" fill="#f4e8b0" fill-opacity=".85" transform="rotate({r} {cx} {-h/2-11})"/>' for cx, r in ((-w/2+60, -18 + R(seed)*6), (w/2-60, 14 + R(seed+1)*6)))

def pin_svg(): return '<circle r="22" fill="#e5322d" stroke="#111" stroke-width="4"/><circle cx="-7" cy="-7" r="6" fill="#fff" opacity=".6"/>'

def map_svg(w, h, pins=(), route=None, seed=0):                              # 61 / 62
    land = "".join(f'<path d="M{x},{y} q{60+R(seed+k)*30},{-50} {130},{-10} q{50},{40} {20},{110} q{-40},{60} {-120},{30} q{-70},{-40} {-30},{-130} Z" fill="#d8c79a" stroke="#a8956a" stroke-width="3" transform="scale({1+R(seed+k+5)*.3:.2f})"/>'
                   for k, (x, y) in enumerate([(-w*.35, -h*.2), (w*.05, -h*.3), (w*.2, h*.05), (-w*.2, h*.2)]))
    grid = "".join(f'<path d="M{-w/2},{-h/2+k*h/6:.0f} H{w/2}" stroke="#7ab0c8" stroke-opacity=".4" stroke-width="2"/>' for k in range(1, 6)) + "".join(f'<path d="M{-w/2+k*w/6:.0f},{-h/2} V{h/2}" stroke="#7ab0c8" stroke-opacity=".4" stroke-width="2"/>' for k in range(1, 6))
    return f'<rect x="{-w/2}" y="{-h/2}" width="{w}" height="{h}" fill="#bfdce8"/>{grid}{land}<rect x="{-w/2}" y="{-h/2}" width="{w}" height="{h}" fill="none" stroke="#5a4a3a" stroke-width="6"/>'

def info_item(it, iid, at, seed):
    """map, timeline, chart, clock, calendar, check/cross, strike, string, montage → (svg, js, w, h)"""
    k = it["type"]; js = []
    if k == "map":
        w, h = it.get("w", 900), it.get("h", 640); svg = map_svg(w, h, seed=seed)
        route = it.get("route")
        if route:
            pts = [(x - it.get("x", 540), y - it.get("y", 960)) for x, y in route]
            d = "M" + " L".join(f"{x:.0f},{y:.0f}" for x, y in pts); L = sum(math.dist(pts[i], pts[i+1]) for i in range(len(pts)-1))
            svg += f'<path d="{d}" fill="none" stroke="#e5322d" stroke-width="9" stroke-dasharray="18 12"/><path id="rv{iid}" d="{d}" fill="none" stroke="#bfdce8" stroke-width="13" stroke-dasharray="{L:.0f}" stroke-dashoffset="0"/>'
            svg += f'<g id="mv{iid}" transform="translate({pts[0][0]} {pts[0][1]})">{pin_svg()}</g>'
            js.append(f'tl.to("#rv{iid}",{{strokeDashoffset:{-L:.0f},duration:1.6,ease:"none"}},{at+.4:.2f});')
            t, seg_d = at + .4, 1.6 / (len(pts) - 1)
            for x, y in pts[1:]:
                js.append(f'tl.to("#mv{iid}",{{attr:{{transform:"translate({x:.0f} {y:.0f})"}},duration:{seg_d:.2f},ease:"none"}},{t:.2f});'); t += seg_d
        for j, (x, y) in enumerate(it.get("pins", [])):
            px, py = x - it.get("x", 540), y - it.get("y", 960)
            svg += f'<g id="pn{j}{iid}" transform="translate({px} {py-600})">{pin_svg()}</g>'
            js.append(f'tl.to("#pn{j}{iid}",{{attr:{{transform:"translate({px} {py})"}},duration:.45,ease:"bounce.out"}},{at+.5+j*.35:.2f});')
        return svg, js, w, h
    if k == "timeline":                                                      # 63
        w = it.get("w", 900); ev = it.get("events", [["1900", ""], ["2000", ""]]); n = len(ev)
        svg = f'<path id="ln{iid}" d="M{-w/2},0 H{w/2}" stroke="#151515" stroke-width="10" stroke-dasharray="{w}" stroke-dashoffset="{w}"/>'
        js.append(f'tl.to("#ln{iid}",{{strokeDashoffset:0,duration:.8,ease:"power2.out"}},{at:.2f});')
        for j, (yr, lab) in enumerate(ev):
            x = -w/2 + w * (j + .5) / n; up = -1 if j % 2 == 0 else 1
            svg += (f'<g id="ev{j}{iid}" opacity="0"><circle cx="{x:.0f}" r="22" fill="#e5322d" stroke="#151515" stroke-width="5"/><text x="{x:.0f}" y="{up*70+ (18 if up>0 else 0):.0f}" text-anchor="middle" font-family="Cairo" font-weight="900" font-size="52" fill="#151515">{yr}</text>'
                    f'<text x="{x:.0f}" y="{up*130+(18 if up>0 else 0):.0f}" text-anchor="middle" font-family="Cairo" font-weight="800" font-size="36" fill="#3a3a3a" direction="rtl">{lab}</text></g>')
            js.append(f'tl.fromTo("#ev{j}{iid}",{{opacity:0,y:20}},{{opacity:1,y:0,duration:.3,ease:"back.out(2)"}},{at+.5+j*.35:.2f});')
        return svg, js, w, 300
    if k == "chart":                                                         # 64
        vals = it.get("values", [3, 5, 8]); labs = it.get("labels", [""] * len(vals)); w, h = it.get("w", 800), it.get("h", 560); n = len(vals); mx = max(vals)
        svg = f'<path d="M{-w/2},{h/2} H{w/2}" stroke="#151515" stroke-width="8"/>'
        bw = w / n * .6
        for j, v in enumerate(vals):
            x = -w/2 + w * (j + .5) / n; bh = (h - 120) * v / mx
            col = it.get("colors", ["#c9a24a", "#e5322d", "#24456b", "#2f5a46"])[j % 4]
            svg += f'<g id="br{j}{iid}" transform="translate(0 {h/2}) scale(1 0.01) translate(0 {-h/2})"><rect x="{x-bw/2:.0f}" y="{h/2-bh:.0f}" width="{bw:.0f}" height="{bh:.0f}" fill="{col}" stroke="#151515" stroke-width="5"/></g>'
            svg += f'<text x="{x:.0f}" y="{h/2+56}" text-anchor="middle" font-family="Cairo" font-weight="900" font-size="40" fill="#151515" direction="rtl">{labs[j]}</text><text id="bv{j}{iid}" opacity="0" x="{x:.0f}" y="{h/2-bh-20:.0f}" text-anchor="middle" font-family="Cairo" font-weight="900" font-size="48" fill="#151515">{v}</text>'
            js.append(f'tl.to("#br{j}{iid}",{{attr:{{transform:"translate(0 {h/2}) scale(1 1) translate(0 {-h/2})"}},duration:.6,ease:"back.out(1.3)"}},{at+j*.25:.2f});tl.to("#bv{j}{iid}",{{opacity:1,duration:.2}},{at+j*.25+.5:.2f});')
        return svg, js, w, h
    if k == "clock":                                                         # 65
        r = it.get("r", 220); h0, m0 = it.get("from", [9, 0]); h1, m1 = it.get("to", [11, 40])
        a0h, a1h = (h0 % 12) * 30 + m0 * .5, (h1 % 12) * 30 + m1 * .5 + (360 if (h1 % 12) * 30 + m1 * .5 < (h0 % 12) * 30 + m0 * .5 else 0)
        a0m, a1m = m0 * 6, m0 * 6 + (((h1 * 60 + m1) - (h0 * 60 + m0)) % 720) * 6
        ticks = "".join(f'<path d="M0,{-r*.82} v{r*.12}" stroke="#151515" stroke-width="6" transform="rotate({j*30})"/>' for j in range(12))
        svg = (f'<circle r="{r+18}" fill="#5a3a22"/><circle r="{r}" fill="#f4efe2" stroke="#151515" stroke-width="6"/>{ticks}'
               f'<path id="hh{iid}" d="M0,0 V{-r*.5}" stroke="#151515" stroke-width="14" stroke-linecap="round" transform="rotate({a0h})"/><path id="mh{iid}" d="M0,0 V{-r*.78}" stroke="#151515" stroke-width="8" stroke-linecap="round" transform="rotate({a0m})"/><circle r="12" fill="#e5322d"/>')
        js.append(f'tl.to("#hh{iid}",{{attr:{{transform:"rotate({a1h})"}},duration:1.6,ease:"power2.inOut"}},{at:.2f});tl.to("#mh{iid}",{{attr:{{transform:"rotate({a1m})"}},duration:1.6,ease:"power2.inOut"}},{at:.2f});')
        return svg, js, 2 * r, 2 * r
    if k == "calendar":                                                      # 66
        days = it.get("days", ["12", "13", "14"]); mon = it.get("month", "مارس"); w, h = 420, 480; svg = ""
        for j, d in enumerate(reversed(days)):
            idx = len(days) - 1 - j
            svg += (f'<g id="pg{idx}{iid}" transform="translate(0 {-h/2}) scale(1 1) translate(0 {h/2})"><rect x="{-w/2}" y="{-h/2}" width="{w}" height="{h}" rx="12" fill="#fbf8f0" stroke="#151515" stroke-width="5"/>'
                    f'<rect x="{-w/2}" y="{-h/2}" width="{w}" height="110" rx="12" fill="#e5322d"/><text y="{-h/2+80}" text-anchor="middle" font-family="Cairo" font-weight="900" font-size="60" fill="#fff" direction="rtl">{mon}</text>'
                    f'<text y="{h/2-90}" text-anchor="middle" font-family="Cairo" font-weight="900" font-size="200" fill="#151515">{d}</text></g>')
        for j in range(len(days) - 1):
            js.append(f'tl.to("#pg{j}{iid}",{{attr:{{transform:"translate(0 {-h/2}) scale(1 -0.05) translate(0 {h/2})"}},opacity:0,duration:.4,ease:"power2.in"}},{at+j*.55:.2f});')
        return svg, js, w, h
    if k in ("check", "cross"):                                              # 60
        s_ = it.get("s", 160)
        d = f"M{-s_*.5},0 L{-s_*.12},{s_*.4} L{s_*.6},{-s_*.5}" if k == "check" else f"M{-s_*.5},{-s_*.5} L{s_*.5},{s_*.5} M{s_*.5},{-s_*.5} L{-s_*.5},{s_*.5}"
        L = s_ * 3
        svg = f'<path id="ck{iid}" d="{d}" fill="none" stroke="{"#2f9a46" if k=="check" else "#e5322d"}" stroke-width="{s_*.16:.0f}" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="{L:.0f}" stroke-dashoffset="{L:.0f}"/>'
        js.append(f'tl.to("#ck{iid}",{{strokeDashoffset:0,duration:.45,ease:"power2.out"}},{at:.2f});')
        return svg, js, s_, s_
    if k == "strike":                                                        # 55 scribbled cross-out over something
        w = it.get("w", 500); pts = " ".join(f"{-w/2+j*w/10:.0f},{(R(seed+j)*18):.0f}" for j in range(11)); L = w * 1.3
        svg = f'<polyline id="sk{iid}" points="{pts}" fill="none" stroke="#e5322d" stroke-width="14" stroke-linecap="round" stroke-dasharray="{L:.0f}" stroke-dashoffset="{L:.0f}"/>'
        js.append(f'tl.to("#sk{iid}",{{strokeDashoffset:0,duration:.4,ease:"power1.out"}},{at:.2f});')
        return svg, js, w, 40
    if k == "string":                                                        # 58 red string between points (detective board)
        pts = [(x - it.get("x", 540), y - it.get("y", 960)) for x, y in it["points"]]; svg = ""
        for j in range(len(pts) - 1):
            (x1, y1), (x2, y2) = pts[j], pts[j+1]; L = math.dist(pts[j], pts[j+1]) * 1.05; mx, my = (x1+x2)/2, (y1+y2)/2 + 40
            svg += f'<path id="rs{j}{iid}" d="M{x1:.0f},{y1:.0f} Q{mx:.0f},{my:.0f} {x2:.0f},{y2:.0f}" fill="none" stroke="#c4262e" stroke-width="7" stroke-dasharray="{L:.0f}" stroke-dashoffset="{L:.0f}"/>'
            js.append(f'tl.to("#rs{j}{iid}",{{strokeDashoffset:0,duration:.45,ease:"power1.inOut"}},{at+j*.45:.2f});')
        svg += "".join(f'<g transform="translate({x:.0f} {y:.0f})">{pin_svg()}</g>' for x, y in pts)
        return svg, js, 0, 0
    return "", js, 0, 0

# =================================================================== scene transitions (CSS masks on the incoming scene / overlays)
TRANSITIONS = ["tear_screen", "punch", "burn", "ink", "brush", "scan", "curtain", "zoom_into", "sheet", "cut"]

def transition(kind, scene_sel, prev_sel, s, color, cx=540, cy=900):
    """incoming scene is ON TOP; returns (css for the incoming scene, js, overlay svg)."""
    a = s - .45
    if kind == "punch":   # 9 circular torn hole grows
        return (f"--r:0px;-webkit-mask-image:radial-gradient(circle at {cx}px {cy}px,#000 var(--r),transparent calc(var(--r) + 3px));mask-image:radial-gradient(circle at {cx}px {cy}px,#000 var(--r),transparent calc(var(--r) + 3px));",
                [f'tl.fromTo("{scene_sel}",{{"--r":"0px"}},{{"--r":"1300px",duration:.6,ease:"power3.in"}},{a:.2f});tl.set("{scene_sel}",{{webkitMaskImage:"none",maskImage:"none"}},{a+.62:.2f});'], "")
    if kind == "ink":     # 37 ink blots grow
        g = ",".join(f"radial-gradient(circle at {x}px {y}px,#000 calc(var(--r) * {f}),transparent calc(var(--r) * {f} + 2px))" for x, y, f in ((300, 600, 1), (760, 900, 1.2), (420, 1300, .9), (820, 1500, .8), (180, 1100, .7)))
        return (f"--r:0px;-webkit-mask-image:{g};mask-image:{g};", [f'tl.fromTo("{scene_sel}",{{"--r":"0px"}},{{"--r":"1100px",duration:.7,ease:"power2.in"}},{a:.2f});tl.set("{scene_sel}",{{webkitMaskImage:"none",maskImage:"none"}},{a+.72:.2f});'], "")
    if kind == "brush":   # 38 diagonal brush wipe
        g = "linear-gradient(115deg,#000 var(--p),transparent calc(var(--p) + 6%))"
        return (f"--p:-10%;-webkit-mask-image:{g};mask-image:{g};", [f'tl.fromTo("{scene_sel}",{{"--p":"-10%"}},{{"--p":"110%",duration:.55,ease:"power2.inOut"}},{a:.2f});tl.set("{scene_sel}",{{webkitMaskImage:"none",maskImage:"none"}},{a+.57:.2f});'], "")
    if kind == "scan":    # 39 printer line from top
        g = "linear-gradient(180deg,#000 var(--p),transparent var(--p))"
        bar = f'<rect id="scanbar" x="0" y="0" width="1080" height="14" fill="#7cc6ff" opacity="0"/>'
        return (f"--p:0%;-webkit-mask-image:{g};mask-image:{g};", [f'tl.fromTo("{scene_sel}",{{"--p":"0%"}},{{"--p":"100%",duration:.7,ease:"none"}},{a:.2f});tl.set("{scene_sel}",{{webkitMaskImage:"none",maskImage:"none"}},{a+.72:.2f});',
                f'tl.fromTo("#scanbar",{{attr:{{y:0}},opacity:.9}},{{attr:{{y:1920}},opacity:.9,immediateRender:false,duration:.7,ease:"none"}},{a:.2f});tl.set("#scanbar",{{opacity:0}},{a+.72:.2f});'], bar)
    if kind == "curtain": # 41 two paper halves part from the middle
        g = "linear-gradient(90deg,transparent calc(50% - var(--p)),#000 calc(50% - var(--p)),#000 calc(50% + var(--p)),transparent calc(50% + var(--p)))"
        return (f"--p:0%;-webkit-mask-image:{g};mask-image:{g};", [f'tl.fromTo("{scene_sel}",{{"--p":"0%"}},{{"--p":"51%",duration:.6,ease:"power2.inOut"}},{a:.2f});tl.set("{scene_sel}",{{webkitMaskImage:"none",maskImage:"none"}},{a+.62:.2f});'], "")
    if kind == "zoom_into":  # 42 dive into the previous scene, the next one opens from its centre
        return ("opacity:0;", [f'tl.to("{prev_sel}",{{scale:4,opacity:0,duration:.5,ease:"power3.in",transformOrigin:"{cx}px {cy}px"}},{a:.2f});tl.fromTo("{scene_sel}",{{opacity:0,scale:.4}},{{opacity:1,scale:1,duration:.45,ease:"power3.out",transformOrigin:"50% 50%"}},{a+.3:.2f});'], "")
    if kind == "burn":    # 36 the old scene burns away from the centre
        g = f"radial-gradient(circle at {cx}px {cy}px,#000 var(--r),transparent calc(var(--r) + 40px))"
        ring = f'<circle id="burnring" cx="{cx}" cy="{cy}" r="1" fill="none" stroke="#ff8a2a" stroke-width="40" opacity="0" filter="url(#glow)"/>'
        return (f"--r:0px;-webkit-mask-image:{g};mask-image:{g};", [f'tl.fromTo("{scene_sel}",{{"--r":"0px"}},{{"--r":"1300px",duration:.9,ease:"power2.in"}},{a-.2:.2f});tl.set("{scene_sel}",{{webkitMaskImage:"none",maskImage:"none"}},{a+.72:.2f});',
                f'tl.fromTo("#burnring",{{attr:{{r:1}},opacity:1}},{{attr:{{r:1330}},opacity:1,immediateRender:false,duration:.9,ease:"power2.in"}},{a-.2:.2f});tl.set("#burnring",{{opacity:0}},{a+.72:.2f});'], ring)
    if kind == "sheet":   # 44 a sheet of paper falls over the frame
        return ("opacity:0;", [f'tl.fromTo("#sheetfall",{{attr:{{transform:"translate(0 -2100) rotate(-8 540 960)"}}}},{{attr:{{transform:"translate(0 0) rotate(0 540 960)"}},duration:.4,ease:"power2.in"}},{a:.2f});tl.set("{scene_sel}",{{opacity:1}},{a+.4:.2f});tl.set("#sheetfall path",{{attr:{{fill:"{color}"}}}},{a:.2f});tl.to("#sheetfall",{{attr:{{transform:"translate(0 2200) rotate(10 540 960)"}},duration:.45,ease:"power2.in"}},{a+.42:.2f});'], "")
    if kind == "cut":
        return ("opacity:0;", [f'tl.set("{scene_sel}",{{opacity:1}},{s-.1:.2f});'], "")
    # 43 tear_screen (default): torn paper wipe across the frame
    return ("opacity:0;", [f'tl.set("{scene_sel}",{{opacity:1}},{a+.3:.2f});tl.set("#wipe path",{{attr:{{fill:"{color}"}}}},{a-.02:.2f});tl.fromTo("#wipe",{{attr:{{transform:"translate(1250 0)"}}}},{{attr:{{transform:"translate(-60 0)"}},duration:.3,ease:"power2.in"}},{a:.2f});tl.to("#wipe",{{attr:{{transform:"translate(-1400 0)"}},duration:.34,ease:"power2.out"}},{a+.32:.2f});'], "")

# =================================================================== camera (scene level)
def camera(kind, scene_sel, cam_sel, at, p=None):
    p = p or {}
    if kind == "flash":     return [f'tl.fromTo("#flash",{{opacity:.95}},{{opacity:0,immediateRender:false,duration:.35,ease:"power2.out"}},{at:.2f});']                                                        # 68
    if kind == "spotlight": return [f'tl.fromTo("#spot",{{opacity:0,"--sx":"{p.get("from",[200,700])[0]}px","--sy":"{p.get("from",[200,700])[1]}px"}},{{opacity:1,immediateRender:false,"--sx":"{p.get("to",[860,1200])[0]}px","--sy":"{p.get("to",[860,1200])[1]}px",duration:{p.get("dur",2):.2f},ease:"sine.inOut"}},{at:.2f});tl.to("#spot",{{opacity:0,duration:.3}},{at+p.get("dur",2):.2f});']  # 69
    if kind == "shake":     return [f'tl.fromTo("{scene_sel}",{{x:0,y:0}},{{x:14,y:-8,duration:.05,yoyo:true,repeat:7,ease:"none"}},{at:.2f});tl.set("{scene_sel}",{{x:0,y:0}},{at+.45:.2f});']   # 70
    if kind == "snap_zoom": return [f'tl.to("{scene_sel}",{{scale:{p.get("k",1.4)},duration:.18,ease:"expo.out",transformOrigin:"{p.get("x",540)}px {p.get("y",900)}px"}},{at:.2f});tl.to("{scene_sel}",{{scale:1,duration:.5,ease:"power2.inOut"}},{at+p.get("hold",1.2):.2f});']  # 71
    if kind == "focus":     return [f'tl.fromTo("{scene_sel}",{{filter:"blur(16px)"}},{{filter:"blur(0px)",duration:.8,ease:"power2.out"}},{at:.2f});']                                  # 72
    return []
