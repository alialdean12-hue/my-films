"""saw_5tory episode builder: ONE json -> a finished 50 s video + thumbnail.

  python3 make_episode.py episode.json OUTDIR            # voice, html, sound, render, thumbnail
  python3 make_episode.py episode.json OUTDIR --preview  # voice + html + snapshot sheet only (no render)

Writes OUTDIR/video.mp4, OUTDIR/thumb.jpg, OUTDIR/sheet.jpg (contact sheet to LOOK at), OUTDIR/project/ (html).
The json format is documented in README.md and examples/*.json. Needs: python3, ffmpeg, node>=22 (npx hyperframes), edge-tts, numpy.
"""
import json, os, re, shutil, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import props, host, places, things

GAP, SWITCH, LEAD, TAIL = 0.45, 0.35, 0.4, 2.0

def sh(cmd, **kw):
    return subprocess.run(cmd, check=True, **kw)

def dur(path):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path]))

def markup(s):
    for k, c in (("r", "r"), ("b", "b"), ("y", "y")):
        s = s.replace(f"[{k}]", f'<span class="{c}">').replace(f"[/{k}]", "</span>")
    return s.replace("\n", "<br/>")

# ------------------------------------------------------------------ voice
def voice(ep, P):
    vd = os.path.join(P, "voice"); os.makedirs(vd, exist_ok=True)
    v = ep.get("voice", {})
    lines = [{"id": f"b{i}", "text": b["line"]} for i, b in enumerate(ep["beats"])]
    json.dump(lines, open(os.path.join(P, "lines.json"), "w"), ensure_ascii=False)
    env = dict(os.environ)
    sh([sys.executable, os.path.join(KIT, "scripts", "tts_edge.py"), os.path.join(P, "lines.json"), vd,
        "--voice", v.get("name", "ar-SA-HamedNeural"), f"--rate={v.get('rate', '-3%')}"], env=env, stdout=subprocess.DEVNULL)
    low = v.get("puppet_layer", 0.38)  # the approved «doll» voice: Hamed + an octave-down copy at 38 % + light echo
    out = []
    for i in range(len(lines)):
        src, dst = os.path.join(vd, f"b{i}.wav"), os.path.join(vd, f"v{i}.wav")
        sh(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-filter_complex",
            f"[0]aresample=44100,asplit[a][b];[b]asetrate=44100*0.7,aresample=44100,atempo=1.4286,volume={low}[low];[a][low]amix=2:normalize=0,aecho=0.8:0.4:60:0.12,aresample=48000",
            "-ac", "1", dst])
        out.append(dur(dst))
    return out

# ------------------------------------------------------------------ timing
def schedule(ep, durs):
    D = ep.get("duration", 50); beats = ep["beats"]
    base = LEAD + sum(durs) + GAP * (len(beats) - 1) + sum(SWITCH for i in range(1, len(beats)) if beats[i]["scene"] != beats[i-1]["scene"]) + TAIL
    slack = D - base
    if slack < 0:
        sys.exit(f"TOO LONG by {-slack:.1f} s: shorten the lines (about {int(-slack*2.4)+1} words) and run again.")
    extra = min(slack / max(1, len(beats)), 1.2)
    t, out = LEAD, []
    for i, b in enumerate(beats):
        if i and b["scene"] != beats[i-1]["scene"]: t += SWITCH
        out.append([round(t, 2), round(t + durs[i], 2)])
        t += durs[i] + GAP + extra
    for i in range(len(out)):  # window = until the next beat starts (last: until the end)
        out[i].append(round(out[i+1][0] - 0.05, 2) if i + 1 < len(out) else D)
    return out

# ------------------------------------------------------------------ html
def room_svg(ep):
    r = ep["room"]; pre = props.PRESETS.get(r.get("preset", "none"), props.PRESETS["none"]); fy = r.get("floor_y", 1380)
    if r.get("place"):
        bg, fy = places.place(r["place"], r.get("time", "night"), r.get("weather"))
        parts = [bg]; furn = []
    else:
        parts = [props.room_shell(r.get("wall", pre["wall"]), r.get("wall2", pre["wall2"]), fy), props.wall_pattern(r.get("pattern", pre["pattern"]), fy)]
        furn = [] if r.get("no_furniture") else pre["furniture"]
    for kind, kw in furn:
        if kind != "blinds": parts.append(props.PROPS[kind](**kw))
    for o in r["objects"]:
        o = dict(o); kind = o.pop("type")
        if kind == "person": o["id_"] = o.pop("id", "p1")
        if kind == "door" and "open" in o: o["open_"] = o.pop("open")
        o.pop("note", None)
        parts.append(props.PROPS[kind](**o))
    for kind, kw in furn:
        if kind == "blinds" and any(o["type"] == "window" for o in r["objects"]):
            w = [o for o in r["objects"] if o["type"] == "window"][0]; parts.append(props.blinds(w.get("x", 640), w.get("y", 300)))
    for a in r.get("atmosphere", []):
        a = {"kind": a} if isinstance(a, str) else a
        parts.append(things.atmosphere(a["kind"], a.get("x", 540), a.get("y", 900)))
    parts.append(props.shade())
    svg = "".join(parts)
    tags = re.findall(r'<g id="tag_[^"]+" opacity="0">.*?</g>', svg)  # name tags always on top
    for t in tags: svg = svg.replace(t, "")
    return svg + "".join(tags)

def clamp(x, y, s):
    hw, hh = 540 / s, 960 / s
    return min(max(x, hw), 1080 - hw), min(max(y, hh), 1920 - hh)

def build_html(ep, sch, P):
    D = ep.get("duration", 50); beats = ep["beats"]; H = host.parts()
    caps, js = [], []
    room = room_svg(ep)
    people = [o.get("id", "p1") for o in ep["room"]["objects"] if o["type"] == "person"]
    js.append('const tl=gsap.timeline({paused:true});')
    js.append('const cam=(x,y,s,t,d,e)=>tl.to("#cam",{x:540-x*s,y:960-y*s,scale:s,duration:d,ease:e||"power2.inOut",transformOrigin:"0px 0px"},t);')
    # scene visibility
    CONT = dict(host="HOST", room="ROOM", cards="CARDS", talk="TALK", board="BOARD", title="TITLE")
    show = lambda sc, t: "".join(f'tl.set("#{c}",{{opacity:{1 if k==sc else 0}}},{t:.2f});' for k, c in CONT.items())
    js.insert(0, "".join(f'gsap.set("#{c}",{{opacity:{1 if k==beats[0]["scene"] else 0}}});' for k, c in CONT.items()))
    js.append(show(beats[0]["scene"], 0))
    for i in range(1, len(beats)):
        if beats[i]["scene"] != beats[i-1]["scene"]:
            t = sch[i][0] - 0.3
            js.append(f'tl.to("#dip",{{opacity:1,duration:.18,ease:"power2.in"}},{t-0.2:.2f});' + show(beats[i]["scene"], t) + f'tl.to("#dip",{{opacity:0,duration:.3}},{t+0.02:.2f});')
    extra = build_extra(ep, sch, js, caps)
    # ambience (whole film)
    js.append(f'if(document.querySelector("#rain"))tl.fromTo("#rain",{{y:0}},{{y:{2*520/2},duration:.6,ease:"none",repeat:{int(D/0.6)}}},0);')
    js.append("const DUR=" + str(D) + ";const Q=c=>Array.from(document.querySelectorAll(c));"
              "Q('.a-spin').forEach(el=>{const o=el.dataset.o,t=360*(+el.dataset.s||1)*DUR;tl.fromTo(el,{attr:{transform:`rotate(0 ${o})`}},{attr:{transform:`rotate(${t} ${o})`},duration:DUR,ease:'none'},0);});"
              "Q('.a-sway').forEach((el,i)=>{const o=el.dataset.o,a=+el.dataset.a||5,p=+el.dataset.p||2;tl.fromTo(el,{attr:{transform:`rotate(${-a} ${o})`}},{attr:{transform:`rotate(${a} ${o})`},duration:p/2,ease:'sine.inOut',yoyo:true,repeat:Math.ceil(DUR/(p/2))},0);});"
              "Q('.a-bob').forEach(el=>{const d=+el.dataset.d||4,p=+el.dataset.p||1.5;tl.fromTo(el,{attr:{transform:'translate(0 0)'}},{attr:{transform:`translate(0 ${-d})`},duration:p/2,ease:'sine.inOut',yoyo:true,repeat:Math.ceil(DUR/(p/2))},0);});"
              "Q('.a-drift').forEach(el=>{const a=+el.dataset.x0,b=+el.dataset.x1,p=+el.dataset.p||6;tl.fromTo(el,{attr:{transform:`translate(${a} 0)`}},{attr:{transform:`translate(${b} 0)`},duration:p,ease:'none',repeat:Math.ceil(DUR/p)},0);});"
              "Q('.a-fall').forEach(el=>{const h=+el.dataset.h||600,p=+el.dataset.p||4;tl.fromTo(el,{attr:{transform:'translate(0 0)'},opacity:1},{attr:{transform:`translate(0 ${h})`},opacity:0,duration:p,ease:'none',repeat:Math.ceil(DUR/p)},0);});"
              "Q('.a-blink').forEach((el,i)=>{const p=+el.dataset.p||3;for(let t=p*.6+i*.37;t<DUR;t+=p){tl.set(el,{opacity:0},t);tl.set(el,{opacity:1},t+.12);}});"
              "Q('.a-flashA').forEach(el=>{for(let t=0;t<DUR;t+=.8){tl.set(el,{opacity:1},t);tl.set(el,{opacity:.15},t+.4);}});"
              "Q('.a-flashB').forEach(el=>{for(let t=0;t<DUR;t+=.8){tl.set(el,{opacity:.15},t);tl.set(el,{opacity:1},t+.4);}});"
              "Q('.a-flicker').forEach(el=>{tl.fromTo(el,{opacity:1},{opacity:.82,duration:.09,ease:'none',yoyo:true,repeat:Math.ceil(DUR/.09)},0);});")
    js.append(f'if(document.querySelector("#snow"))tl.fromTo("#snow",{{y:0}},{{y:520,duration:3,ease:"none",repeat:{int(D/3)}}},0);')
    js.append(f'if(document.querySelector("#steam"))tl.fromTo("#steam",{{y:0,opacity:.7}},{{y:-14,opacity:.3,duration:1.2,ease:"sine.inOut",yoyo:true,repeat:{int(D/1.2)}}},0);')
    js.append(f'if(document.querySelector("#smoke"))tl.fromTo("#smoke",{{y:0,opacity:.75}},{{y:-20,opacity:.3,duration:1.4,ease:"sine.inOut",yoyo:true,repeat:{int(D/1.4)}}},0);')
    js.append(f'if(document.querySelector("#flame"))tl.fromTo("#flame",{{scaleY:1}},{{scaleY:.82,duration:.18,ease:"sine.inOut",yoyo:true,repeat:{int(D/0.18)},transformOrigin:"50% 100%"}},0);')
    js.append(f'if(document.querySelector("#dclock"))for(let k=0;k<{int(D)};k++){{tl.set("#dclock",{{opacity:0}},k+.5);tl.set("#dclock",{{opacity:1}},k+1);}}')
    for n, pid in enumerate(people):
        js.append(f'tl.fromTo("#{pid}_body",{{y:0}},{{y:4,duration:1.4,ease:"sine.inOut",yoyo:true,repeat:{int(D/1.4)}}},0);')
        for k in range(int(D / 3.3)):
            t = 1.7 + k * 3.3 + n * 0.9
            js.append(f'tl.set("#{pid}_open",{{opacity:0}},{t:.2f});tl.set("#{pid}_shut",{{opacity:1}},{t:.2f});tl.set("#{pid}_open",{{opacity:1}},{t+0.12:.2f});tl.set("#{pid}_shut",{{opacity:0}},{t+0.12:.2f});')
    # host idle across the film
    js.append(f'tl.fromTo("#bob",{{y:0}},{{y:-16,duration:.95,ease:"sine.inOut",yoyo:true,repeat:{int(D/0.95)}}},0);')
    js.append(f'tl.fromTo("#sway",{{rotation:-2.5}},{{rotation:2.5,duration:1.4,ease:"sine.inOut",yoyo:true,repeat:{int(D/1.4)},svgOrigin:"540 60"}},0);')
    js.append(f'tl.to("#larm",{{rotation:8,duration:.9,ease:"sine.inOut",yoyo:true,repeat:{int(D/0.9)},svgOrigin:"372 712"}},0);')
    entered = False
    for i, b in enumerate(beats):
        s, e, w = sch[i]
        cid = f"cap{i}"
        if b.get("caption"):
            pos = b.get("caption_pos", "bottom" if b["scene"] == "host" else ("low" if b.get("tags") else "top"))
            top = {"top": 120, "bottom": 1500, "low": 1620}[pos]
            fs = b.get("caption_size", 100 if b["scene"] == "host" else 92)
            caps.append(f'<div id="{cid}" class="cap" style="top:{top}px;font-size:{fs}px">{markup(b["caption"])}</div>')
            js.append(f'tl.fromTo("#{cid}",{{opacity:0,y:30}},{{opacity:1,y:0,duration:.3,ease:"power3.out"}},{s+0.1:.2f});tl.to("#{cid}",{{opacity:0,duration:.2}},{w-0.25:.2f});')
            if b.get("sub"):
                caps.append(f'<div id="{cid}s" class="cap" style="top:1700px;font-size:64px">{markup(b["sub"])}</div>')
                js.append(f'tl.fromTo("#{cid}s",{{opacity:0,y:30}},{{opacity:1,y:0,duration:.3}},{s+1.6:.2f});tl.to("#{cid}s",{{opacity:0,duration:.2}},{w-0.25:.2f});')
        if b["scene"] == "host":
            act = b.get("host", "talk")
            if not entered:
                js.append(f'tl.fromTo("#pup",{{y:-1000}},{{y:0,duration:1.0,ease:"back.out(1.3)"}},{max(0,s-0.4):.2f});'); entered = True
            js.append(f'tl.to("#hd",{{rotation:-12,duration:.4,ease:"power2.out",svgOrigin:"540 620"}},{s+0.3:.2f});tl.to("#hd",{{rotation:8,duration:.5,ease:"power2.inOut",svgOrigin:"540 620"}},{s+(e-s)*0.55:.2f});tl.to("#hd",{{rotation:0,duration:.4}},{w-0.4:.2f});')
            if act == "point":
                js.append(f'tl.to("#rarm",{{rotation:30,duration:.5,ease:"back.out(1.5)",svgOrigin:"706 712"}},{s+0.6:.2f});tl.to("#rarm",{{rotation:24,duration:.25,yoyo:true,repeat:3,svgOrigin:"706 712"}},{s+1.2:.2f});tl.to("#rarm",{{rotation:0,duration:.4,svgOrigin:"706 712"}},{w-0.4:.2f});')
            else:
                js.append(f'tl.to("#rarm",{{rotation:-14,duration:.3,ease:"sine.inOut",yoyo:true,repeat:5,svgOrigin:"706 712"}},{s+0.4:.2f});')
            js.append(f'tl.to("#eyes",{{opacity:.15,duration:.06,yoyo:true,repeat:3}},{e-0.4:.2f});')
            if b.get("timer"):
                caps.append(f'<svg id="tm{i}" class="timer" width="260" height="260" viewBox="-130 -130 260 260"><circle r="100" fill="#020309cc" stroke="#ffffff22" stroke-width="16"/><circle id="tmr{i}" r="100" fill="none" stroke="#ff3b3b" stroke-width="16" stroke-dasharray="629" stroke-dashoffset="629" transform="rotate(-90)" stroke-linecap="round"/><text y="22" text-anchor="middle" font-family="Cairo" font-weight="900" font-size="64" fill="#fff">فكّر</text></svg>')
                js.append(f'tl.fromTo("#tm{i}",{{opacity:0,scale:.6}},{{opacity:1,scale:1,duration:.3,ease:"back.out(2)"}},{e+0.1:.2f});tl.to("#tmr{i}",{{strokeDashoffset:0,duration:{max(1.0,w-e-0.6):.2f},ease:"none"}},{e+0.3:.2f});tl.to("#tm{i}",{{opacity:0,duration:.2}},{w-0.2:.2f});')
        elif b["scene"] == "room":
            if b.get("cam"):
                x, y, sc = b["cam"]; x, y = clamp(x, y, sc * 1.07)
                js.append(f'cam({x},{y},{sc},{s-0.15:.2f},.7);cam({x},{y},{sc*1.07:.3f},{s+0.55:.2f},{max(0.5,w-s-0.7):.2f},"none");')
            if b.get("tour"):
                stops = b["tour"]; t0 = s + (w - s) * 0.42; step = (w - 0.3 - t0) / len(stops)
                for k, (x, y, sc) in enumerate(stops):
                    x, y = clamp(x, y, sc)
                    js.append(f'cam({x},{y},{sc},{t0+k*step:.2f},.42);')
            for tg in b.get("tags", []):
                js.append(f'tl.to("#tag_{tg}",{{opacity:1,duration:.3}},{s+0.4:.2f});tl.to("#tag_{tg}",{{opacity:0,duration:.2}},{w-0.2:.2f});')
            for fx in b.get("fx", []):
                if fx == "lightning":
                    t = s + 0.3
                    js.append(f'if(document.querySelector("#flash")){{tl.to("#flash",{{opacity:.9,duration:.05}},{t:.2f});tl.to("#flash",{{opacity:0,duration:.25}},{t+0.08:.2f});tl.to("#flash",{{opacity:.6,duration:.05}},{t+0.4:.2f});tl.to("#flash",{{opacity:0,duration:.3}},{t+0.48:.2f});}}')
                if fx == "flicker":
                    t = (s + e) / 2
                    js.append(f'tl.to("#lamp",{{opacity:.3,duration:.05}},{t:.2f});tl.to("#lamp",{{opacity:1,duration:.12}},{t+0.1:.2f});')
                if fx == "glance":
                    for pid in people:
                        js.append(f'tl.to("#{pid}_pup",{{x:-6,duration:.25}},{s+0.5:.2f});tl.to("#{pid}_pup",{{x:5,duration:.3}},{(s+e)/2:.2f});tl.to("#{pid}_pup",{{x:0,duration:.3}},{w-0.3:.2f});')
            if b.get("stamp"):
                caps.append(f'<div id="st{i}" class="stamp"><span>{markup(b["stamp"])}</span></div>')
                js.append(f'tl.fromTo("#st{i}",{{scale:2.4,opacity:0,rotation:-14}},{{scale:1,opacity:1,rotation:-8,duration:.22,ease:"power4.in"}},{s+0.5:.2f});tl.to("#st{i}",{{opacity:0,duration:.25}},{w-0.3:.2f});')
            if b.get("ring"):
                x, y, rr = b["ring"]
                js.append(f'tl.fromTo("#ring{i}",{{opacity:0,strokeDashoffset:{int(6.3*rr)}}},{{opacity:1,strokeDashoffset:0,duration:.6,ease:"power2.inOut"}},{s+0.5:.2f});tl.to("#ring{i}",{{opacity:0,duration:.2}},{w-0.2:.2f});')
            if b.get("reveal"):
                caps.append(f'<div id="rv{i}" class="reveal">{markup(b["reveal"])}</div>')
                js.append(f'tl.fromTo("#rv{i}",{{scale:.4,opacity:0}},{{scale:1,opacity:1,duration:.35,ease:"back.out(2)"}},{s+0.9:.2f});tl.to("#rv{i}",{{opacity:0,duration:.2}},{w-0.2:.2f});')
    rings = "".join(f'<circle id="ring{i}" cx="{b["ring"][0]}" cy="{b["ring"][1]}" r="{b["ring"][2]}" fill="none" stroke="#ff3b3b" stroke-width="10" stroke-dasharray="{int(6.3*b["ring"][2])}" opacity="0" filter="url(#glow)"/>' for i, b in enumerate(beats) if b.get("ring"))
    js.append(f'tl.to("#dip",{{opacity:1,duration:.5}},{D-0.6});')
    js.append('window.__timelines=window.__timelines||{};window.__timelines["ep"]=tl;')
    pup = f'<g id="pup"><g id="bob"><g id="sway">{H["puppet"]}<g id="hd">{H["head"]}</g></g></g></g>'
    html = f'''<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><title>{ep.get("title","saw_5tory")}</title><style>
@font-face{{font-family:"Cairo";src:url("fonts/cairo-ar.woff2") format("woff2");font-weight:200 1000;font-display:block;unicode-range:U+0600-06FF,U+0750-077F,U+FB50-FDFF,U+FE70-FEFC,U+200C-200E;}}
@font-face{{font-family:"Cairo";src:url("fonts/cairo-latin.woff2") format("woff2");font-weight:200 1000;font-display:block;}}
html,body{{margin:0;background:#020309}}#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#020309;font-family:"Cairo",sans-serif;direction:rtl}}
.clip{{position:absolute;inset:0;overflow:hidden}}svg.full{{position:absolute;inset:0}}
.cap{{position:absolute;left:60px;right:60px;text-align:center;font-weight:900;line-height:1.25;color:#fff;-webkit-text-stroke:8px #020309;paint-order:stroke fill;opacity:0}}
.r{{color:#ff3b3b}}.b{{color:#7cc6ff}}.y{{color:#ffd21f}}
.shade{{position:absolute;left:0;right:0;top:0;height:440px;background:linear-gradient(#020309e6,#02030900)}}
.stamp{{position:absolute;left:0;right:0;top:820px;text-align:center;font-weight:900;font-size:180px;color:#ff3b3b;opacity:0}}
.stamp span{{display:inline-block;border:14px solid #ff3b3b;padding:0 40px 20px;border-radius:24px;background:#02030988}}
.reveal{{position:absolute;left:40px;right:40px;top:1480px;text-align:center;font-weight:900;font-size:110px;color:#ffd21f;-webkit-text-stroke:9px #020309;paint-order:stroke fill;opacity:0}}
#dip{{background:#000;opacity:0}}
.timer{{position:absolute;left:50px;top:110px;opacity:0}}
.bub{{position:absolute;width:820px;padding:18px 34px 26px;border-radius:34px;font-weight:800;font-size:54px;line-height:1.35;opacity:0;box-shadow:0 14px 40px #000a}}
.bub b{{display:block;font-size:34px;font-weight:900;margin-bottom:4px}}
.bub.d{{right:60px;background:#13284d;color:#fff;border:4px solid #7cc6ff}}.bub.d b{{color:#7cc6ff}}
.bub.s{{left:60px;background:#f3efe6;color:#111;border:4px solid #ffd21f}}.bub.s b{{color:#9a5a00}}
.note::before{{content:"";position:absolute;top:-14px;left:50%;width:28px;height:28px;margin-left:-14px;border-radius:50%;background:#c4262e;box-shadow:0 4px 8px #000}}
.note{{position:absolute;width:640px;padding:22px 30px 28px;background:#f4efe2;color:#111;font-weight:800;font-size:48px;line-height:1.3;box-shadow:0 16px 40px #000c;opacity:0}}
.note .tm{{display:block;font-size:64px;font-weight:900;color:#c4262e;direction:ltr;text-align:right}}
.note.mk{{outline:10px solid #ff3b3b;outline-offset:8px}}
.cnum{{position:absolute;width:110px;height:110px;border-radius:50%;background:#ffd21f;color:#111;font-weight:900;font-size:72px;text-align:center;line-height:104px;box-shadow:0 8px 24px #000}}
.clab{{position:absolute;left:0;right:0;text-align:center;font-weight:900;font-size:50px;color:#fff;-webkit-text-stroke:6px #020309;paint-order:stroke fill}}
.case{{position:absolute;left:0;right:0;text-align:center;font-weight:900;color:#fff}}
</style><script src="gsap.min.js"></script></head><body>
<div id="root" data-composition-id="ep" data-start="0" data-duration="{D}" data-width="1080" data-height="1920">
 <div id="ROOM" class="clip" data-start="0" data-duration="{D}" data-track-index="1"><svg class="full" width="1080" height="1920" viewBox="0 0 1080 1920">{H["defs"]}<g id="cam"><g id="roomart">{room}</g>{rings}</g></svg><div class="shade"></div></div>
 <div id="HOST" class="clip" data-start="0" data-duration="{D}" data-track-index="2"><svg class="full" width="1080" height="1920" viewBox="0 0 1080 1920">{H["defs"]}{H["bg"]}{pup}</svg></div>
 {extra}
 <div id="CAPS" class="clip" data-start="0" data-duration="{D}" data-track-index="7">{"".join(caps)}</div>
 <div id="dip" class="clip" data-start="0" data-duration="{D}" data-track-index="8"></div>
</div>
<script>{"".join(js)}</script></body></html>'''
    open(os.path.join(P, "index.html"), "w").write(html)

def build_extra(ep, sch, js, caps):
    """cards / talk / board / title scenes. Returns their container html."""
    beats = ep["beats"]; D = ep.get("duration", 50); out = []
    persons = {o.get("id", "p1"): o for o in ep["room"]["objects"] if o["type"] == "person"}
    # ---- CARDS: crops of the room (live, via <use>) numbered 1..3
    cards_html = []
    for i, b in enumerate(beats):
        if b["scene"] != "cards": continue
        s, e, w = sch[i]; cs = b["cards"]; n = len(cs)
        H_ = 440 if n == 3 else 560; tops = [330, 820, 1310] if n == 3 else [380, 1040]
        g = ""
        for k, (x, y, sc, lab) in enumerate(cs):
            vw, vh = 860 / sc, H_ / sc
            g += (f'<g id="cd{i}_{k}" opacity="0"><rect x="100" y="{tops[k]-10}" width="880" height="{H_+20}" rx="18" fill="#f4efe2"/>'
                  f'<svg x="110" y="{tops[k]}" width="860" height="{H_}" viewBox="{x-vw/2:.1f} {y-vh/2:.1f} {vw:.1f} {vh:.1f}"><use href="#roomart"/></svg>'
                  f'<rect id="cdx{i}_{k}" x="100" y="{tops[k]-10}" width="880" height="{H_+20}" rx="18" fill="none" stroke="#ff3b3b" stroke-width="14" opacity="0"/>'
                  f'<rect x="110" y="{tops[k]+H_-80}" width="860" height="80" fill="#020309" opacity=".7"/>'
                  f'<text x="540" y="{tops[k]+H_-24}" text-anchor="middle" font-family="Cairo" font-weight="900" font-size="48" fill="#fff" direction="rtl">{lab}</text>'
                  f'<circle cx="920" cy="{tops[k]+40}" r="56" fill="#ffd21f" stroke="#020309" stroke-width="6"/><text x="920" y="{tops[k]+66}" text-anchor="middle" font-family="Cairo" font-weight="900" font-size="72" fill="#111">{k+1}</text></g>')
            js.append(f'tl.fromTo("#cd{i}_{k}",{{opacity:0,y:60}},{{opacity:1,y:0,duration:.35,ease:"back.out(1.6)"}},{s+0.2+k*0.55:.2f});tl.to("#cd{i}_{k}",{{opacity:0,duration:.2}},{w-0.2:.2f});')
            if b.get("pick") is not None:
                if k == b["pick"]: js.append(f'tl.to("#cdx{i}_{k}",{{opacity:1,duration:.2}},{s+1.6:.2f});tl.to("#cdx{i}_{k}",{{opacity:.2,duration:.2,yoyo:true,repeat:3}},{s+1.9:.2f});')
                else: js.append(f'tl.to("#cd{i}_{k}",{{opacity:.28,duration:.3}},{s+1.6:.2f});')
        cards_html.append(g)
    out.append(f'<div id="CARDS" class="clip" data-start="0" data-duration="{D}" data-track-index="3" style="opacity:0;background:radial-gradient(ellipse at 50% 40%,#13284d,#020309 75%)"><svg class="full" width="1080" height="1920" viewBox="0 0 1080 1920">{"".join(cards_html)}</svg></div>')
    # ---- TALK: interrogation bubbles accumulate within a run of talk beats (max 4 on screen)
    talk = []; slot = 0; run_end = None
    for i, b in enumerate(beats):
        if b["scene"] != "talk": slot = 0; continue
        s, e, w = sch[i]
        j = i
        while j + 1 < len(beats) and beats[j+1]["scene"] == "talk": j += 1
        run_end = sch[j][2]
        if slot == 4:
            js.append(f'tl.to("#TALK .bub",{{opacity:0,duration:.2}},{s-0.1:.2f});'); slot = 0
        who, text = b["say"][0], b["say"][1]
        side = "d" if who in ("detective", "المحقق") else "s"
        name = "المحقق" if side == "d" else persons.get(who, {}).get("name", who)
        top = 250 + slot * 330
        talk.append(f'<div id="bb{i}" class="bub {side}" style="top:{top}px"><b>{name}</b>{markup(text)}</div>')
        js.append(f'tl.fromTo("#bb{i}",{{opacity:0,y:40,scale:.9}},{{opacity:1,y:0,scale:1,duration:.3,ease:"back.out(1.8)"}},{s+0.05:.2f});tl.to("#bb{i}",{{opacity:0,duration:.25}},{run_end-0.25:.2f});')
        slot += 1
    out.append(f'<div id="TALK" class="clip" data-start="0" data-duration="{D}" data-track-index="4" style="opacity:0;background:radial-gradient(ellipse at 50% 0%,#3a3020 0%,#0a0c12 55%,#020309 100%)">'
               '<svg class="full" width="1080" height="1920" viewBox="0 0 1080 1920"><path d="M540,0 V120" stroke="#222" stroke-width="6"/><path d="M470,120 L610,120 L640,170 L440,170 Z" fill="#2a2a2a"/><polygon points="440,170 640,170 1000,1920 80,1920" fill="#ffe2a0" opacity=".08"/>'
               '<rect x="0" y="1640" width="1080" height="280" fill="#1a120c"/><rect x="0" y="1630" width="1080" height="20" fill="#3a2a1a"/></svg>' + "".join(talk) + '</div>')
    # ---- BOARD: timeline notes pinned on a dark board, string between them
    bd = ep.get("board", {}); items = bd.get("items", []); notes = []; shown = 0
    for k, (tm, txt) in enumerate(items):
        top = 300 + k * 290; left = 80 if k % 2 == 0 else 360
        notes.append(f'<div id="nt{k}" class="note" style="top:{top}px;left:{left}px;transform:rotate({-2 if k%2==0 else 2}deg)"><span class="tm">{tm}</span>{markup(txt)}</div>')
    for i, b in enumerate(beats):
        if b["scene"] != "board": continue
        s, e, w = sch[i]; upto = min(b.get("show", len(items)), len(items))
        new = list(range(shown, upto)); step = max(0.6, (e - s) / max(1, len(new)))
        for n_, k in enumerate(new): js.append(f'tl.fromTo("#nt{k}",{{opacity:0,scale:1.25}},{{opacity:1,scale:1,duration:.3,ease:"power3.out"}},{s+0.1+n_*step:.2f});')
        shown = max(shown, upto)
        if b.get("mark") is not None:
            js.append(f'tl.set("#nt{b["mark"]}",{{className:"note mk"}},{s+0.8:.2f});tl.fromTo("#nt{b["mark"]}",{{scale:1}},{{scale:1.06,duration:.25,yoyo:true,repeat:3}},{s+0.8:.2f});')
    pins = "".join(f'<circle cx="{(80 if k%2==0 else 360)+320}" cy="{300+k*290+6}" r="14" fill="#c4262e"/>' for k in range(len(items)))
    string = "M" + " L".join(f'{(80 if k%2==0 else 360)+320},{300+k*290+6}' for k in range(len(items))) if items else ""
    out.append(f'<div id="BOARD" class="clip" data-start="0" data-duration="{D}" data-track-index="5" style="opacity:0;background:#2a1e14">'
               f'<svg class="full" width="1080" height="1920" viewBox="0 0 1080 1920"><g opacity=".18" fill="#000">' + "".join(f'<circle cx="{(k*97)%1080}" cy="{(k*233)%1920}" r="5"/>' for k in range(260)) + '</g>'
               + '</svg>'
               + f'<div class="case" style="top:110px;font-size:80px;-webkit-text-stroke:6px #020309;paint-order:stroke fill">{markup(bd.get("title",""))}</div>' + "".join(notes) + '</div>')
    # ---- TITLE: case card
    tt = []
    for i, b in enumerate(beats):
        if b["scene"] != "title": continue
        s, e, w = sch[i]
        tt.append(f'<div id="tc{i}" style="opacity:0"><div class="case" style="top:660px;font-size:80px;color:#ff3b3b">{"اللغز" if ep.get("part",1)==1 else "الحل"}</div>'
                  f'<div class="case" style="top:770px;font-size:150px;line-height:1.15;-webkit-text-stroke:8px #020309;paint-order:stroke fill">{markup(b.get("title", ep.get("title","")))}</div>'
                  f'<div class="case" style="top:1180px;font-size:52px;color:#7cc6ff">{markup(b.get("subtitle","saw_5tory"))}</div></div>')
        js.append(f'tl.fromTo("#tc{i}",{{opacity:0,scale:1.15}},{{opacity:1,scale:1,duration:.5,ease:"power3.out"}},{s:.2f});tl.to("#tc{i}",{{opacity:0,duration:.25}},{w-0.25:.2f});')
    out.append(f'<div id="TITLE" class="clip" data-start="0" data-duration="{D}" data-track-index="6" style="opacity:0;background:radial-gradient(ellipse at 50% 45%,#1d2f5a,#020309 70%)">' + "".join(tt) + '</div>')
    return "\n".join(out)

# ------------------------------------------------------------------ sound
def sound(ep, sch, P):
    D = ep.get("duration", 50); sd = os.path.join(P, "sfx"); os.makedirs(sd, exist_ok=True)
    py = sys.executable; lib = os.path.join(KIT, "scripts", "sfx_lib.py")
    for n in ("whoosh", "hit", "bell", "riser"): sh([py, lib, n, os.path.join(sd, n + ".wav")])
    sh(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", f"sine=f=55:d={D}", "-f", "lavfi", "-i", f"sine=f=82.4:d={D}", "-filter_complex",
        f"[0][1]amix=2,tremolo=f=0.3:d=0.4,afade=t=in:d=2,afade=t=out:st={D-2}:d=2,volume=0.6", "-ar", "48000", "-ac", "1", os.path.join(sd, "drone.wav")])
    sh(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", f"anoisesrc=c=pink:d={D}:a=0.6", "-af", f"highpass=f=900,lowpass=f=7000,afade=t=in:d=0.5,afade=t=out:st={D-1}:d=1", "-ar", "48000", "-ac", "1", os.path.join(sd, "rain.wav")])
    sh(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", "anoisesrc=c=brown:d=2.5:a=0.9", "-af", "lowpass=f=160,afade=t=in:d=0.05,afade=t=out:st=0.4:d=2.1,volume=3", "-ar", "48000", "-ac", "1", os.path.join(sd, "thunder.wav")])
    beats = ep["beats"]; it = [{"file": f"voice/v{i}.wav", "at": sch[i][0]} for i in range(len(beats))]
    it.append({"file": "sfx/drone.wav", "at": 0, "gain": 0.1})
    rainy = any(o["type"] == "window" and o.get("rain", True) and not o.get("day") for o in ep["room"]["objects"])
    if rainy: it.append({"file": "sfx/rain.wav", "at": 0, "gain": 0.07})
    for i, b in enumerate(beats):
        s, e, w = sch[i]
        if i and b["scene"] != beats[i-1]["scene"]:
            it += [{"file": "sfx/whoosh.wav", "at": round(s - 0.75, 2), "gain": 0.15}, {"file": "sfx/hit.wav", "at": round(s - 0.3, 2), "gain": 0.2}]
        if "lightning" in b.get("fx", []): it.append({"file": "sfx/thunder.wav", "at": round(s + 0.3, 2), "gain": 0.25})
        if b.get("stamp"): it.append({"file": "sfx/hit.wav", "at": round(s + 0.7, 2), "gain": 0.3})
        if b.get("tour"):
            t0 = s + (w - s) * 0.42; step = (w - 0.3 - t0) / len(b["tour"])
            it += [{"file": "sfx/bell.wav", "at": round(t0 + k * step, 2), "gain": 0.05} for k in range(len(b["tour"]))]
        if b.get("ring"): it.append({"file": "sfx/riser.wav", "at": round(s, 2), "gain": 0.12})
        if b.get("reveal"): it.append({"file": "sfx/hit.wav", "at": round(s + 0.9, 2), "gain": 0.3})
        if b["scene"] == "cards":
            it += [{"file": "sfx/hit.wav", "at": round(s + 0.25 + k * 0.55, 2), "gain": 0.12} for k in range(len(b["cards"]))]
            if b.get("pick") is not None: it += [{"file": "sfx/riser.wav", "at": round(s + 0.6, 2), "gain": 0.12}, {"file": "sfx/hit.wav", "at": round(s + 1.6, 2), "gain": 0.3}]
        if b["scene"] == "talk": it.append({"file": "sfx/bell.wav", "at": round(s + 0.05, 2), "gain": 0.04})
        if b["scene"] == "board": it.append({"file": "sfx/bell.wav", "at": round(s + 0.1, 2), "gain": 0.05})
        if b["scene"] == "title": it += [{"file": "sfx/hit.wav", "at": round(s, 2), "gain": 0.3}, {"file": "sfx/riser.wav", "at": round(max(0, s - 0.2), 2), "gain": 0.1}]
        if b.get("timer"): it.append({"file": "sfx/riser.wav", "at": round(e + 0.3, 2), "gain": 0.12})
    json.dump({"duration": D, "target_lufs": -14, "items": it}, open(os.path.join(P, "mix.json"), "w"))
    os.makedirs(os.path.join(P, "out"), exist_ok=True)
    sh([sys.executable, os.path.join(KIT, "scripts", "mix.py"), "mix.json", "out/mix.wav"], cwd=P, stdout=subprocess.DEVNULL)

# ------------------------------------------------------------------ thumbnail
def thumbnail(ep, P, OUT):
    """Cover. Design «face + clue» for single-suspect cases, «lineup» when 3 suspects (cards / format lineup).
    thumb keys: text (markup, 2-4 words), design ("face"|"lineup", optional), suspect (id), expression,
    mystery [x,y,scale] (part 1 magnifier, hidden with ?), clue [x,y,scale] (part 2 magnifier, revealed), stamp (part 2 word),
    suspects [ids] and liar (id) for lineup."""
    import people
    th = ep.get("thumb", {}); H = host.parts(); T = os.path.join(P, "thumb"); os.makedirs(T, exist_ok=True)
    shutil.copy(os.path.join(P, "gsap.min.js"), T); shutil.copytree(os.path.join(P, "fonts"), os.path.join(T, "fonts"), dirs_exist_ok=True)
    part = ep.get("part", 1); room = room_svg(ep)
    persons = [o for o in ep["room"]["objects"] if o["type"] == "person"]
    byid = {o.get("id", "p1"): o for o in persons}
    design = th.get("design") or ("lineup" if (len(persons) >= 3 and any(b["scene"] == "cards" for b in ep["beats"])) else "face")
    def head(pid, x, y, w, expression=None, dim=False):
        o = dict(byid[pid]); o.pop("type"); o.pop("note", None); o["id_"] = "th_" + o.pop("id", "p1"); o["x"] = 490; o["y"] = 1520; o.pop("name", None)
        if expression: o["expression"] = expression
        h = w * 320 / 240
        return f'<svg x="{x}" y="{y}" width="{w}" height="{h:.0f}" viewBox="370 680 240 320">{people.person(**o)}</svg>' + (f'<rect x="{x}" y="{y}" width="{w}" height="{h:.0f}" fill="#000" opacity=".55"/>' if dim else "")
    def tx(x, y, size, text, fill="#fff", stroke="#020309", sw=14):
        return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" paint-order="stroke fill" text-anchor="middle" direction="rtl" font-family="Cairo" font-weight="900">{text}</text>'
    def lines(markup_text, y0, size=140):
        cols = {"r": "#ff3b3b", "y": "#ffd21f", "b": "#7cc6ff"}; out = ""
        for k, ln in enumerate(markup_text.split("\n")):
            col = "#fff"
            for c, v in cols.items():
                if f"[{c}]" in ln: col = v
            ln = re.sub(r"\[/?[ryb]\]", "", ln)
            out += tx(540, y0 + k * size * 1.05, size if k else int(size * 0.85), ln, col)
        return out
    def badge(label, y):
        return f'<rect x="390" y="{y-80}" width="300" height="110" rx="55" fill="#ffd21f" stroke="#020309" stroke-width="6"/>' + tx(540, y, 70, label, "#111", "none", 0)
    defs = H["defs"] + '<defs><filter id="tblur"><feGaussianBlur stdDeviation="8"/></filter><radialGradient id="tred" cx=".5" cy=".45" r=".6"><stop offset="0" stop-color="#7a0e1e"/><stop offset="1" stop-color="#05060a"/></radialGradient><radialGradient id="tvig" cx=".5" cy=".5" r=".7"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".85"/></radialGradient></defs>'
    fx, fy, fs = th.get("focus", [540, 1250, 1.1])
    bg = f'<g transform="translate({540-fx*fs} {960-fy*fs}) scale({fs})" filter="url(#tblur)">{room}</g>'
    label = "اللغز" if part == 1 else "الحل"
    if design == "lineup":
        ids = th.get("suspects") or [o.get("id", "p1") for o in persons][:3]
        pick = next((b.get("pick") for b in ep["beats"] if b["scene"] == "cards" and b.get("pick") is not None), None)
        liar = th.get("liar") or (ids[pick] if pick is not None and pick < len(ids) else None)
        body = '<rect width="1080" height="1920" fill="#1a1e26"/>'
        for k in range(9):
            y = 650 + k * 100
            body += f'<path d="M0,{y} H1080" stroke="#cfd8e2" stroke-opacity=".35" stroke-width="4"/><text x="40" y="{y-10}" font-size="30" fill="#cfd8e2" opacity=".5">{200-k*10}</text>'
        for k, pid in enumerate(ids):
            x = 40 + k * 340 if len(ids) == 3 else 200 + k * 380
            is_liar = (pid == liar)
            body += head(pid, x, 640, 320, dim=(part == 2 and liar and not is_liar))
            body += f'<rect x="{x+40}" y="1085" width="240" height="90" rx="10" fill="#111" stroke="#cfd8e2" stroke-width="4"/>' + tx(x + 160, 1149, 54, byid[pid].get("name", ""), "#fff", "none", 0)
            body += f'<circle cx="{x+160}" cy="1260" r="54" fill="#ffd21f" stroke="#020309" stroke-width="6"/>' + tx(x + 160, 1285, 70, str(k + 1), "#111", "none", 0)
            if part == 2 and is_liar:
                body += f'<g transform="rotate(-14 {x+160} 870)"><rect x="{x}" y="810" width="320" height="120" rx="16" fill="#05060a" fill-opacity=".5" stroke="#ff3b3b" stroke-width="14"/>' + tx(x + 160, 902, 84, th.get("stamp", "الكاذب"), "#ff3b3b", "none", 0) + '</g>'
        body += lines(th.get("text", "من [r]الكاذب[/r]؟" if part == 1 else "[y]انكشف![/y]"), 520 if "\n" in th.get("text", "") else 590, 110)
        body += '<rect width="1080" height="1920" fill="url(#tvig)"/>' + badge(label, 1440)
    else:
        pid = th.get("suspect") or (persons[0].get("id", "p1") if persons else None)
        body = '<rect width="1080" height="1920" fill="url(#tred)"/>' + bg + '<rect width="1080" height="1920" fill="#05060a" opacity=".7"/>'
        if pid: body += head(pid, 0, 660, 520, th.get("expression", "nervous" if part == 1 else "scared"))
        ring = next((b.get("ring") for b in ep["beats"] if b.get("ring")), None)
        view = th.get("mystery", [fx, fy, 1.6]) if part == 1 else th.get("clue", [ring[0], ring[1], 1.9] if ring else [fx, fy, 1.6])
        cx, cy, r = 720, 1080, 190; vx, vy, vs = view; vw = 2 * r / vs
        body += (f'<defs><clipPath id="tmag"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath></defs><g clip-path="url(#tmag)"><rect x="{cx-r}" y="{cy-r}" width="{2*r}" height="{2*r}" fill="#05060a"/>'
                 f'<svg x="{cx-r}" y="{cy-r}" width="{2*r}" height="{2*r}" viewBox="{vx-vw/2} {vy-vw/2} {vw} {vw}">{room}</svg>'
                 + (f'<rect x="{cx-r}" y="{cy-r}" width="{2*r}" height="{2*r}" fill="#05060a" opacity=".35"/>' + tx(cx, cy + 70, 260, "؟", "#ffd21f", "#020309", 16) if part == 1 else "")
                 + f'</g><circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#ff3b3b" stroke-width="16"/><path d="M{cx+r*0.7},{cy+r*0.7} l{r*0.55},{r*0.55}" stroke="#ff3b3b" stroke-width="34" stroke-linecap="round"/>')
        if part == 2:
            body += f'<g transform="rotate(-12 720 1270)"><rect x="560" y="1220" width="320" height="100" rx="14" fill="none" stroke="#ff3b3b" stroke-width="12"/>' + tx(720, 1298, 72, th.get("stamp", "انكشف!"), "#ff3b3b", "#020309", 8) + '</g>'
        body += lines(th.get("text", "هل تكشف\n[r]الكذبة[/r]؟" if part == 1 else "الحل\n[y]هنا[/y]!"), 540, 112)
        body += '<rect width="1080" height="1920" fill="url(#tvig)"/>' + badge(label, 1450)
    html = f'''<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><title>cover</title><style>
@font-face{{font-family:"Cairo";src:url("fonts/cairo-ar.woff2") format("woff2");font-weight:200 1000;font-display:block;unicode-range:U+0600-06FF,U+0750-077F,U+FB50-FDFF,U+FE70-FEFC,U+200C-200E;}}
@font-face{{font-family:"Cairo";src:url("fonts/cairo-latin.woff2") format("woff2");font-weight:200 1000;font-display:block;}}
html,body{{margin:0}}#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#05060a}}.clip{{position:absolute;inset:0;overflow:hidden}}
</style></head><body><div id="root" data-composition-id="thumb" data-start="0" data-duration="1" data-width="1080" data-height="1920">
<div id="a" class="clip" data-start="0" data-duration="1" data-track-index="1"><svg width="1080" height="1920" viewBox="0 0 1080 1920" style="position:absolute;inset:0">{defs}{body}</svg></div></div>
<script src="gsap.min.js"></script><script>const tl=gsap.timeline({{paused:true}});tl.to({{}},{{duration:1}},0);window.__timelines={{thumb:tl}};</script></body></html>'''
    open(os.path.join(T, "index.html"), "w").write(html)
    shutil.rmtree(os.path.join(T, "snap"), ignore_errors=True)
    sh(["npx", "hyperframes", "snapshot", "--at", "0.5", "--no-end", "-o", "snap", "."], cwd=T, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    png = [f for f in os.listdir(os.path.join(T, "snap")) if f.startswith("frame-")][0]
    sh(["ffmpeg", "-y", "-loglevel", "error", "-i", os.path.join(T, "snap", png), "-q:v", "2", os.path.join(OUT, "thumb.jpg")])

# ------------------------------------------------------------------ main
def main():
    ep = json.load(open(sys.argv[1])); OUT = os.path.abspath(sys.argv[2]); preview = "--preview" in sys.argv
    P = os.path.join(OUT, "project"); os.makedirs(P, exist_ok=True)
    tpl = os.path.join(KIT, "styles", "kinetic")
    shutil.copy(os.path.join(tpl, "gsap.min.js"), P); shutil.copytree(os.path.join(tpl, "fonts"), os.path.join(P, "fonts"), dirs_exist_ok=True)
    print("1/5 voice..."); durs = voice(ep, P)
    sch = schedule(ep, durs); json.dump(sch, open(os.path.join(P, "schedule.json"), "w"))
    print("2/5 html..."); build_html(ep, sch, P)
    lint = subprocess.run(["npx", "hyperframes", "lint"], cwd=P, capture_output=True, text=True).stdout
    if "✗" in lint: print(lint); sys.exit("LINT ERRORS")
    times = ",".join(f"{(s+w)/2:.1f}" for s, e, w in sch)
    print("3/5 look..."); subprocess.run(["npx", "hyperframes", "snapshot", "--at", times, "--no-end", "-o", "snaps", "."], cwd=P, capture_output=True)
    sheets = sorted(f for f in os.listdir(os.path.join(P, "snaps")) if f.startswith("contact"))
    for k, f in enumerate(sheets): shutil.copy(os.path.join(P, "snaps", f), os.path.join(OUT, f"sheet{k+1}.jpg"))
    if preview: print("preview done: look at", OUT); return
    print("4/5 sound + render..."); sound(ep, sch, P)
    sh(["sh", os.path.join(KIT, "scripts", "render.sh"), ".", "out/mix.wav", os.path.join(OUT, "video.mp4"), "24"], cwd=P, stdout=subprocess.DEVNULL)
    print("5/5 thumbnail..."); thumbnail(ep, P, OUT)
    print("DONE:", os.path.join(OUT, "video.mp4"), os.path.join(OUT, "thumb.jpg"))

if __name__ == "__main__":
    main()
