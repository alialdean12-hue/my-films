from lib import *
ep = load(); B = ep["beats"]
def scene(i, b, s, e, c0, c1):
    dark = b["bg"] in ("#0b0b0f", "#e5322d", "#2b6cff"); fg = "#fff" if dark else "#0b0b0f"; acc = "#ffc933" if b["bg"] != "#ffc933" else "#e5322d"
    n = len(b["w"]); step = (e - s + .3) / n; h = f'<div style="position:absolute;inset:0;background:{b["bg"]}"></div>'
    h += f'<div id="bar{i}" style="position:absolute;left:0;top:0;height:1920px;width:60px;background:{acc};opacity:.9"></div>'
    js = [f'tl.fromTo("#bar{i}",{{x:0}},{{x:-1080+60,duration:{c1-c0:.2f},ease:"none"}},{c0:.2f});']
    for k, w in enumerate(b["w"]):
        num = len(w) <= 2; size = 520 if num else (300 if len(w) <= 4 else 220); col = acc if (k == 0 and i and i < 6) or num else fg
        y = 700 + (k - (n - 1) / 2) * 0
        st = "background:" + fg + ";color:" + b["bg"] + ";padding:0 40px 30px;" if (k == n - 1 and i % 2) else ""
        h += f'<div id="w{i}_{k}" style="position:absolute;left:0;right:0;top:{y}px;text-align:center;font-weight:900;font-size:{size}px;line-height:1;color:{col};opacity:0"><span style="{st}">{w}</span></div>'
        t = s - .05 + k * step; a = [(3.2, -10), (.2, 12), (1, 0)][k % 3]
        js.append(f'tl.fromTo("#w{i}_{k}",{{scale:{a[0]},rotation:{a[1]},opacity:0,x:{0 if k%3!=2 else 700}}},{{scale:1,rotation:0,opacity:1,x:0,duration:.24,ease:"back.out(1.7)"}},{t:.2f});')
        js.append(f'tl.to("#w{i}_{k}",{{scale:1.08,duration:{step-.3:.2f},ease:"none"}},{t+.24:.2f});')
        if k < n - 1: js.append(f'tl.to("#w{i}_{k}",{{opacity:0,y:-120,duration:.12}},{t+step-.12:.2f});')
    h += f'<div id="ln{i}" style="position:absolute;left:180px;right:180px;top:1230px;height:28px;background:{acc}"></div>'
    js.append(f'tl.fromTo("#ln{i}",{{scaleX:0}},{{scaleX:1,duration:.3,ease:"power3.out"}},{s+(n-1)*step+.2:.2f});')
    return h, js
run("4_kinetic", B, scene, bed="beat", rate="+5%",
    extra_sfx=lambda sch: [{"file": "sfx/hit.wav", "at": round(s, 2), "gain": .25} for s, e in sch])
