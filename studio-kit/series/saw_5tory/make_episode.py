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
import props, host

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
    r = ep["room"]; parts = [props.room_shell(r.get("wall", "#0c1628"), r.get("wall2", "#1a2a44"), r.get("floor_y", 1380))]
    for o in r["objects"]:
        o = dict(o); kind = o.pop("type")
        if kind == "person": o["id_"] = o.pop("id", "p1")
        if kind == "door" and "open" in o: o["open_"] = o.pop("open")
        o.pop("note", None)
        parts.append(props.PROPS[kind](**o))
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
    first = beats[0]["scene"]
    js.append(f'tl.set("#HOST",{{opacity:{1 if first=="host" else 0}}},0);tl.set("#ROOM",{{opacity:{0 if first=="host" else 1}}},0);')
    for i in range(1, len(beats)):
        if beats[i]["scene"] != beats[i-1]["scene"]:
            t = sch[i][0] - 0.3
            js.append(f'tl.to("#dip",{{opacity:1,duration:.18,ease:"power2.in"}},{t-0.2:.2f});tl.set("#HOST",{{opacity:{1 if beats[i]["scene"]=="host" else 0}}},{t:.2f});'
                      f'tl.set("#ROOM",{{opacity:{0 if beats[i]["scene"]=="host" else 1}}},{t:.2f});tl.to("#dip",{{opacity:0,duration:.3}},{t+0.02:.2f});')
    # ambience (whole film)
    js.append(f'if(document.querySelector("#rain"))tl.fromTo("#rain",{{y:0}},{{y:{2*520/2},duration:.6,ease:"none",repeat:{int(D/0.6)}}},0);')
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
            pos = b.get("caption_pos", "bottom" if b["scene"] == "host" else "top")
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
        else:
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
</style><script src="gsap.min.js"></script></head><body>
<div id="root" data-composition-id="ep" data-start="0" data-duration="{D}" data-width="1080" data-height="1920">
 <div id="ROOM" class="clip" data-start="0" data-duration="{D}" data-track-index="1"><svg class="full" width="1080" height="1920" viewBox="0 0 1080 1920">{H["defs"]}<g id="cam">{room}{rings}</g></svg><div class="shade"></div></div>
 <div id="HOST" class="clip" data-start="0" data-duration="{D}" data-track-index="2"><svg class="full" width="1080" height="1920" viewBox="0 0 1080 1920">{H["defs"]}{H["bg"]}{pup}</svg></div>
 <div id="CAPS" class="clip" data-start="0" data-duration="{D}" data-track-index="3">{"".join(caps)}</div>
 <div id="dip" class="clip" data-start="0" data-duration="{D}" data-track-index="4"></div>
</div>
<script>{"".join(js)}</script></body></html>'''
    open(os.path.join(P, "index.html"), "w").write(html)

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
    json.dump({"duration": D, "target_lufs": -14, "items": it}, open(os.path.join(P, "mix.json"), "w"))
    os.makedirs(os.path.join(P, "out"), exist_ok=True)
    sh([sys.executable, os.path.join(KIT, "scripts", "mix.py"), "mix.json", "out/mix.wav"], cwd=P, stdout=subprocess.DEVNULL)

# ------------------------------------------------------------------ thumbnail
def thumbnail(ep, P, OUT):
    th = ep.get("thumb", {}); H = host.parts(); T = os.path.join(P, "thumb"); os.makedirs(T, exist_ok=True)
    for f in ("gsap.min.js",): shutil.copy(os.path.join(P, f), T)
    shutil.copytree(os.path.join(P, "fonts"), os.path.join(T, "fonts"), dirs_exist_ok=True)
    x, y, s = th.get("focus", [540, 960, 1.2]); part = ep.get("part", 1)
    badge = th.get("badge", "الجزء 1: اللغز" if part == 1 else "الجزء 2: الحل")
    html = f'''<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><title>thumb</title><style>
@font-face{{font-family:"Cairo";src:url("fonts/cairo-ar.woff2") format("woff2");font-weight:200 1000;font-display:block;unicode-range:U+0600-06FF,U+0750-077F,U+FB50-FDFF,U+FE70-FEFC,U+200C-200E;}}
@font-face{{font-family:"Cairo";src:url("fonts/cairo-latin.woff2") format("woff2");font-weight:200 1000;font-display:block;}}
html,body{{margin:0}}#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#020309;font-family:"Cairo",sans-serif;direction:rtl}}
.clip{{position:absolute;inset:0;overflow:hidden}}
.big{{position:absolute;left:40px;right:40px;top:150px;text-align:center;font-weight:900;font-size:150px;line-height:1.15;color:#fff;-webkit-text-stroke:12px #020309;paint-order:stroke fill;text-shadow:0 10px 30px #000}}
.r{{color:#ff3b3b}}.b{{color:#7cc6ff}}.y{{color:#ffd21f}}
.badge{{position:absolute;bottom:200px;left:50%;transform:translateX(-50%);background:#ffd21f;color:#111;font-weight:900;font-size:70px;padding:4px 50px 16px;border-radius:999px;white-space:nowrap;box-shadow:0 10px 40px #000}}
.brand{{position:absolute;bottom:110px;left:0;right:0;text-align:center;color:#7cc6ff;font-weight:900;font-size:48px;letter-spacing:2px;direction:ltr}}
.vig{{background:radial-gradient(ellipse at 50% 50%,#0000 35%,#000d 100%)}}
</style></head><body>
<div id="root" data-composition-id="thumb" data-start="0" data-duration="1" data-width="1080" data-height="1920">
<div id="a" class="clip" data-start="0" data-duration="1" data-track-index="1">
<svg width="1080" height="1920" viewBox="0 0 1080 1920" style="position:absolute;inset:0">{H["defs"]}<g transform="translate({540-x*s} {960-y*s}) scale({s})">{room_svg(ep)}</g><rect width="1080" height="1920" fill="#020309" opacity=".35"/>
<g transform="translate(470 560) scale(.78)">{H["puppet"]}{H["head"]}</g></svg>
<div class="clip vig"></div><div class="big">{markup(th.get("text", "هل تكشف [r]الكذبة[/r]؟"))}</div><div class="badge">{badge}</div><div class="brand">saw_5tory</div></div></div>
<script src="gsap.min.js"></script><script>const tl=gsap.timeline({{paused:true}});tl.to({{}},{{duration:1}},0);window.__timelines={{thumb:tl}};</script></body></html>'''
    open(os.path.join(T, "index.html"), "w").write(html)
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
