from lib import *
CSS = ('.cap{position:absolute;left:70px;right:70px;top:210px;text-align:center;font-weight:900;font-size:96px;line-height:1.15;color:#fff;-webkit-text-stroke:14px #0b2a4a;paint-order:stroke fill}'
       '.tag{position:absolute;left:50%;top:90px;transform:translateX(-50%);background:#ffd21f;color:#0b2a4a;font-weight:900;font-size:58px;padding:0 36px 10px;border-radius:40px;border:7px solid #0b2a4a}')
def whale(i, mood="happy"):
    eye = '<g class="eye{0}"><ellipse cx="-150" cy="-40" rx="34" ry="40" fill="#fff" stroke="#0b2a4a" stroke-width="8"/><circle cx="-142" cy="-34" r="17" fill="#0b2a4a"/><circle cx="-136" cy="-42" r="6" fill="#fff"/></g>'.format(i)
    mouth = f'<path id="mo{i}" d="M-260,40 Q-170,{110 if mood!="wow" else 140} -60,50" fill="#e85a6a" stroke="#0b2a4a" stroke-width="9"/>'
    return (f'<g id="wh{i}" transform="translate(560 1200)"><g id="wb{i}" transform="translate(0 0) rotate(0)">'
            f'<g id="tl{i}" transform="translate(300 -20) rotate(0)"><path d="M0,0 C80,-40 120,-140 200,-160 C170,-80 180,-30 220,20 C150,10 80,40 0,40Z" fill="#3d8be0" stroke="#0b2a4a" stroke-width="10"/></g>'
            '<path d="M-320,-20 C-320,-200 -60,-250 140,-210 C300,-180 340,-60 320,40 C300,160 120,200 -60,190 C-250,180 -320,120 -320,-20Z" fill="#4aa3f0" stroke="#0b2a4a" stroke-width="12"/>'
            '<path d="M-300,60 C-200,170 100,190 300,80 C260,160 120,200 -60,190 C-220,180 -290,130 -300,60Z" fill="#dff1ff"/>'
            + "".join(f'<path d="M{-240+k*70},{110+k*4} q60,10 120,0" stroke="#9cc9ee" stroke-width="7" fill="none"/>' for k in range(5)) +
            f'{eye}{mouth}<ellipse cx="-90" cy="20" rx="34" ry="18" fill="#ff9aa8" opacity=".7"/><path d="M-20,-200 q10,-40 30,-50" stroke="#0b2a4a" stroke-width="8" fill="none"/></g></g>')
def bubbles(i): return "".join(f'<circle class="bu{i}" cx="{(R(i*20+k)+1)*540:.0f}" cy="{1900+k*40}" r="{10+abs(R(k+i))*26:.0f}" fill="none" stroke="#bfe6ff" stroke-width="5" opacity=".8"/>' for k in range(16))
def ocean(i):
    return (f'<linearGradient id="oc{i}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3fb6ff"/><stop offset="1" stop-color="#0a3d7a"/></linearGradient><rect width="1080" height="1920" fill="url(#oc{i})"/>'
            + "".join(f'<path d="M{-100+k*260},0 L{60+k*260},0 L{-200+k*260},1300 L{-360+k*260},1300Z" fill="#fff" opacity=".07"/>' for k in range(6))
            + '<path d="M0,1780 q270,-60 540,0 t540,0 V1920 H0Z" fill="#e8c98a"/><path d="M120,1780 q10,-120 -20,-200 M150,1780 q30,-90 10,-160 M900,1790 q-20,-140 20,-230" stroke="#2f9a6a" stroke-width="18" fill="none" stroke-linecap="round"/>')
ep = load(); B = ep["beats"]
def scene(i, b, s, e, c0, c1):
    k = b["k"]; D = c1 - c0; js = []
    sv = f'<svg class="full" width="1080" height="1920" viewBox="0 0 1080 1920">{ocean(i)}{bubbles(i)}'
    if k == "car": sv += f'<g id="ob{i}" transform="translate(800 1560) scale(0)"><rect x="-150" y="-80" width="300" height="110" rx="30" fill="#e5322d" stroke="#0b2a4a" stroke-width="9"/><path d="M-90,-80 L-50,-150 H60 L100,-80Z" fill="#ffd9d9" stroke="#0b2a4a" stroke-width="9"/><circle cx="-80" cy="40" r="38" fill="#333" stroke="#0b2a4a" stroke-width="8"/><circle cx="80" cy="40" r="38" fill="#333" stroke="#0b2a4a" stroke-width="8"/></g><g id="ht{i}" transform="translate(300 1560) scale(0)"><path d="M0,60 C-160,-40 -120,-180 0,-110 C120,-180 160,-40 0,60Z" fill="#ff4d6d" stroke="#0b2a4a" stroke-width="10"/></g><text id="eq{i}" x="550" y="1590" font-size="110" font-weight="900" fill="#fff" text-anchor="middle" opacity="0">=</text>'
    if k == "beat": sv += "".join(f'<circle class="rw{i}" cx="560" cy="1200" r="300" fill="none" stroke="#fff" stroke-width="10" opacity="0"/>' for _ in range(4))
    if k == "eat": sv += "".join(f'<g class="kr{i}" transform="translate({180+ (k2%6)*30} {900+ (k2//6)*90 + R(k2)*40:.0f})"><path d="M0,0 q20,-14 40,0 q-20,14 -40,0" fill="#ff8a5a"/></g>' for k2 in range(30))
    if k == "loud": sv += f'<g id="pl{i}" transform="translate(-300 650)"><path d="M0,0 h260 q40,0 40,25 q0,25 -40,25 h-260z" fill="#e8eef5" stroke="#0b2a4a" stroke-width="8"/><path d="M120,0 l-60,-90 h40 l80,90z M120,50 l-60,90 h40 l80,-90z" fill="#c9d4e0" stroke="#0b2a4a" stroke-width="7"/></g>' + "".join(f'<path class="sw{i}" d="M{300+j*0},1100 q60,100 0,200" transform="translate({-60-j*60} 0)" stroke="#ffd21f" stroke-width="14" fill="none" stroke-linecap="round" opacity="0"/>' for j in range(3))
    if k == "dino": sv += f'<g id="dn{i}" transform="translate(840 2300) scale(.6)"><path d="M-160,0 C-160,-120 -60,-160 40,-140 L120,-300 C140,-330 190,-320 190,-290 L170,-170 C220,-120 220,0 160,30 L-180,40 C-260,40 -320,20 -380,-20 C-300,-10 -220,0 -160,0Z" fill="#7fbf3f" stroke="#0b2a4a" stroke-width="10"/><circle cx="150" cy="-280" r="10" fill="#0b2a4a"/></g>'
    sv += whale(i, "wow" if k in ("car", "dino", "loud") else "happy") + "</svg>"
    h = sv + f'<div class="tag">هل تعلم؟</div><div class="cap" id="cp{i}" style="opacity:0">{b["cap"]}</div>'
    js.append(f'tl.fromTo("#cp{i}",{{opacity:0,scale:.3,rotation:-8}},{{opacity:1,scale:1,rotation:0,duration:.45,ease:"elastic.out(1,.5)"}},{s:.2f});')
    js.append(f'tl.fromTo(".bu{i}",{{y:0}},{{y:-2100,duration:{D:.2f},stagger:{D/20:.2f},ease:"none"}},{c0:.2f});')
    # whale life: swim bob, tail flap, blink, talking mouth
    js.append(f'tl.fromTo("#wb{i}",{{attr:{{transform:"translate(0 -20) rotate(-3)"}}}},{{attr:{{transform:"translate(0 20) rotate(3)"}},duration:1.1,yoyo:true,repeat:{int(D/1.1)},ease:"sine.inOut"}},{c0:.2f});')
    js.append(f'tl.fromTo("#tl{i}",{{attr:{{transform:"translate(300 -20) rotate(-14)"}}}},{{attr:{{transform:"translate(300 -20) rotate(14)"}},duration:.45,yoyo:true,repeat:{int(D/.45)},ease:"sine.inOut"}},{c0:.2f});')
    for t in range(int(D / 2.3)): js.append(f'tl.to("#S{i} .eye{i}",{{scaleY:.1,transformOrigin:"50% 50%",duration:.07,yoyo:true,repeat:1}},{c0+1+t*2.3:.2f});')
    js.append(f'tl.fromTo("#mo{i}",{{scaleY:1}},{{scaleY:.55,transformOrigin:"50% 0%",duration:.13,yoyo:true,repeat:{int((e-s)/.13)}}},{s:.2f});')
    if i == 0: js.append(f'tl.fromTo("#wh{i}",{{attr:{{transform:"translate(1500 1200)"}}}},{{attr:{{transform:"translate(560 1200)"}},duration:1,ease:"back.out(1.2)"}},0);')
    if k == "car": js += [f'tl.to("#ht{i}",{{attr:{{transform:"translate(300 1560) scale(1)"}},duration:.5,ease:"back.out(2)"}},{s+.8:.2f});', f'tl.to("#eq{i}",{{opacity:1,duration:.2}},{s+1.4:.2f});', f'tl.to("#ob{i}",{{attr:{{transform:"translate(800 1560) scale(1)"}},duration:.5,ease:"back.out(2)"}},{s+1.6:.2f});', f'tl.to("#ht{i}",{{attr:{{transform:"translate(300 1560) scale(1.15)"}},duration:.18,yoyo:true,repeat:9}},{s+2.2:.2f});']
    if k == "beat": js.append(f'tl.fromTo(".rw{i}",{{attr:{{r:120}},opacity:.9}},{{attr:{{r:900}},opacity:0,duration:1.4,stagger:.7,repeat:1,ease:"power1.out"}},{s+.3:.2f});')
    if k == "eat": js += [f'tl.to(".kr{i}",{{x:380,y:320,scale:.2,duration:.6,stagger:.06,ease:"power2.in"}},{s+.6:.2f});', f'tl.to(".kr{i}",{{opacity:0,duration:.1,stagger:.06}},{s+1.2:.2f});']
    if k == "loud": js += [f'tl.fromTo("#pl{i}",{{attr:{{transform:"translate(-300 650)"}}}},{{attr:{{transform:"translate(1200 560)"}},duration:2.4,ease:"none"}},{s+.2:.2f});', f'tl.fromTo(".sw{i}",{{opacity:1,x:0}},{{opacity:0,x:-200,duration:.6,stagger:.15,repeat:4}},{s+.8:.2f});', f'tl.fromTo("#S{i} svg",{{x:0}},{{x:10,duration:.04,yoyo:true,repeat:15}},{s+1:.2f});']
    if k == "dino": js += [f'tl.fromTo("#dn{i}",{{attr:{{transform:"translate(840 2300) scale(.6)"}}}},{{attr:{{transform:"translate(840 1700) scale(.6)"}},duration:.6,ease:"back.out(1.6)"}},{s+.6:.2f});', f'tl.fromTo("#wh{i}",{{attr:{{transform:"translate(560 1200) scale(1)"}}}},{{attr:{{transform:"translate(460 1050) scale(1.15)"}},duration:1.2,ease:"back.out(1.4)"}},{s+1.4:.2f});']
    if k == "end": js.append(f'tl.fromTo("#cp{i}",{{scale:1}},{{scale:1.12,duration:.3,yoyo:true,repeat:6}},{s+.6:.2f});')
    return h, js
run("9_cartoon", B, scene, css=CSS, bg="#0a3d7a", rate="+5%",
    extra_sfx=lambda sch: [{"file": "sfx/bell.wav", "at": round(s + .1, 2), "gain": .12} for s, e in sch])
