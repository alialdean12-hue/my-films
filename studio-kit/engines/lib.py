import json, os, re, shutil, subprocess, sys, math
KIT = "/home/user/my-films/studio-kit"
sys.path.insert(0, KIT + "/scripts")

def sh(c, **k): return subprocess.run(c, check=True, **k)
def dur(p): return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]))
def R(seed):
    x = math.sin(seed * 12.9898 + 78.233) * 43758.5453
    return (x - math.floor(x)) * 2 - 1
def mk(s, hl="#ffd21f"):
    s = s.replace("\n", "<br/>")
    s = re.sub(r"\[y\](.*?)\[/y\]", rf'<span style="color:{hl}">\1</span>', s)
    return re.sub(r"\[r\](.*?)\[/r\]", r'<span style="color:#ff3b3b">\1</span>', s)

FONT = '''@font-face{font-family:"Cairo";src:url("fonts/cairo-ar.woff2") format("woff2");font-weight:200 1000;font-display:block;unicode-range:U+0600-06FF,U+0750-077F,U+FB50-FDFF,U+FE70-FEFC,U+200C-200E;}
@font-face{font-family:"Cairo";src:url("fonts/cairo-latin.woff2") format("woff2");font-weight:200 1000;font-display:block;}''' + "".join(
    f'@font-face{{font-family:"{n}";src:url("fonts/{f}-ar.woff2") format("woff2");font-weight:100 1000;font-display:block;unicode-range:U+0600-06FF,U+0750-077F,U+FB50-FDFF,U+FE70-FEFC,U+200C-200E;}}'
    for n, f in (("Amiri", "amiri"), ("Tajawal", "tajawal"), ("Reem Kufi", "reemkufi"), ("Lalezar", "lalezar"), ("Noto Naskh", "notonaskharabic"), ("Marhey", "marhey"), ("Lemonada", "lemonada")))
FONTS = {"cairo": "Cairo", "amiri": "Amiri", "tajawal": "Tajawal", "kufi": "Reem Kufi", "lalezar": "Lalezar", "naskh": "Noto Naskh", "marhey": "Marhey", "lemonada": "Lemonada"}

TOP = []   # top-level timed elements (e.g. <video>) that scenes add; drawn under the scene clips
def merge(a, b):
    out = dict(a)
    for k, v in b.items(): out[k] = merge(out[k], v) if isinstance(v, dict) and isinstance(out.get(k), dict) else v
    return out
def load():
    """reads the video json; "series": "<name>" pulls defaults from engines/series/<name>.json (the video json wins)."""
    if len(sys.argv) < 3: sys.exit("usage: python <engine>.py video.json OUTDIR [--preview]")
    ep = json.load(open(sys.argv[1]))
    if ep.get("series"):
        f = os.path.join(os.path.dirname(os.path.abspath(__file__)), "series", ep["series"] + ".json")
        if not os.path.exists(f): sys.exit(f"unknown series {ep['series']}: see engines/series/")
        pre = json.load(open(f)); pre.pop("about", None); pre.pop("style", None); ep = merge(pre, ep)
    ep["_dir"] = os.path.dirname(os.path.abspath(sys.argv[1])); return ep

def run(name, beats, scene, css="", bg="#111", voice="ar-SA-HamedNeural", rate="+0%", D=30.0, bed="pluck", extra_sfx=None, overlay="", pre_js=""):
    """beats: list of dicts with 'line'. scene(i,b,s,e,c0,c1)->(html, js list). returns video path."""
    OUT = os.path.abspath(sys.argv[2]); P = OUT + "/project"
    ep = load(); voice = ep.get("voice", {}).get("name", voice); rate = ep.get("voice", {}).get("rate", rate); D = float(ep.get("duration", D))
    os.makedirs(P + "/voice", exist_ok=True)
    shutil.copy(KIT + "/styles/kinetic/gsap.min.js", P); shutil.copytree(KIT + "/styles/kinetic/fonts", P + "/fonts", dirs_exist_ok=True)
    json.dump([{"id": f"b{i}", "text": b.get("say", b["line"])} for i, b in enumerate(beats)], open(P + "/lines.json", "w"), ensure_ascii=False)
    vf = ep.get("voice_files")   # folder with b0.wav/mp3/flac... made by another TTS (when edge-tts is blocked)
    if vf:
        vf = vf if os.path.isabs(vf) else os.path.join(ep["_dir"], vf)
        for i in range(len(beats)):
            src = next((f"{vf}/b{i}.{x}" for x in ("wav", "mp3", "flac", "ogg", "m4a") if os.path.exists(f"{vf}/b{i}.{x}")), None)
            if not src: sys.exit(f"voice_files: missing b{i}.wav (or .mp3/.flac) in {vf}")
            sh(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-ac", "1", "-ar", "48000", f"{P}/voice/b{i}.wav"])
    if not all(os.path.exists(f"{P}/voice/b{i}.wav") for i in range(len(beats))):
        r_ = subprocess.run([sys.executable, KIT + "/scripts/tts_edge.py", P + "/lines.json", P + "/voice", "--voice", voice, f"--rate={rate}"], capture_output=True, text=True)
        if r_.returncode: sys.exit("VOICE FAILED (edge-tts cannot reach its server here). Make one audio file per beat with your own TTS, Arabic male voice, "
                                   "named b0.wav b1.wav ... (one per line, same text), put them in a folder and add  \"voice_files\": \"<folder>\"  to the json. Then run again.\n" + r_.stderr[-300:])
    durs = [dur(f"{P}/voice/b{i}.wav") for i in range(len(beats))]
    # length follows the topic: the video is as long as the narration needs (no maximum), but never under "min_duration" (default 50 s).
    # A too-short narration is NOT padded with silence: the render stops and says how many words to add (previews still run).
    need = lambda t: t + .3 * (len(beats) - 1) + 1.6
    tot = sum(durs); MIN = float(ep.get("min_duration", 50))
    if need(tot) < MIN and "--preview" not in sys.argv:
        words = sum(len(b.get("say", b["line"]).split()) for b in beats); add = int(words * (MIN / need(tot) - 1)) + 3
        sys.exit(f"TOO SHORT: the narration lasts {need(tot):.1f} s but every video must be at least {MIN:.0f} s. Explain the topic more: add about {add} words (new beats or longer lines). Video not rendered.")
    D = round(max(need(tot), MIN if "--preview" not in sys.argv else min(MIN, need(tot) + 2)), 2)
    gap = min(1.0, max(.3, (D - 0.6 - 1.0 - tot) / max(1, len(beats) - 1)))
    sch, t = [], .5
    for d in durs: sch.append((round(t, 2), round(t + d, 2))); t += d + gap
    clips, js = [], ["const tl=gsap.timeline({paused:true});"]
    for i, b in enumerate(beats):
        s, e = sch[i]; c0 = 0 if i == 0 else s - .35; c1 = sch[i+1][0] + .1 if i + 1 < len(beats) else D
        h, j = scene(i, b, s, e, c0, c1); js += j
        clips.append(f'<div id="S{i}" class="clip" data-start="{c0:.2f}" data-duration="{c1-c0:.2f}" data-track-index="{1+i%2}">{h}</div>')
    handle = (f'<div id="hdl" class="clip" data-start="0" data-duration="{D}" data-track-index="9" style="pointer-events:none"><div style="position:absolute;left:0;right:0;top:1770px;text-align:center;font-weight:800;font-size:38px;color:#fff;opacity:.55;text-shadow:0 2px 6px #000;direction:ltr">{ep["handle"]}</div></div>') if ep.get("handle") else ""
    js.append(f'tl.to({{}},{{duration:.01}},{D-.01});window.__timelines=window.__timelines||{{}};window.__timelines["c"]=tl;')
    html = f'''<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><title>{name}</title><style>{FONT}
html,body{{margin:0;background:{bg}}}#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:{bg};font-family:"{FONTS.get(ep.get("font", "cairo"), "Cairo")}","Cairo",sans-serif;direction:rtl}}#root *{{font-family:inherit}}
.clip{{position:absolute;inset:0;overflow:hidden}}svg.full{{position:absolute;inset:0}}{css}</style><script src="gsap.min.js"></script></head><body>
<div id="root" data-composition-id="c" data-start="0" data-duration="{D}" data-width="1080" data-height="1920">{"".join(TOP)}{"".join(clips)}{overlay}{handle}</div><script>{pre_js}{"".join(js)}</script></body></html>'''
    open(P + "/index.html", "w").write(html)
    lint = subprocess.run(["npx", "hyperframes", "lint"], cwd=P, capture_output=True, text=True).stdout
    if "✗" in lint: print(lint); sys.exit("LINT")
    json.dump({"sch": sch, "D": D}, open(P + "/schedule.json", "w"))
    FACT = {"doc", "voxflat", "threed", "cartoon", "paper"}   # styles that state facts: every number/claim needs a source
    if name in FACT:
        src = ep.get("sources") or []
        if src: open(OUT + "/SOURCES.txt", "w").write("مصادر المعلومات:\n" + "\n".join(f"- {x}" for x in src) + "\n")
        elif "--preview" not in sys.argv and not ep.get("no_facts"):
            sys.exit('SOURCES MISSING: add "sources": ["<site or book> — <what it confirms>", ...] to the json (one per fact/number), or "no_facts": true for pure fiction. Video not rendered.')
    import post
    if ep.get("qa", True):
        probs = post.qa(P, sch, D)
        if probs:
            print("QA PROBLEMS (fix the JSON: shorter captions / smaller size / move x):\n  " + "\n  ".join(probs[:20]))
            if "--preview" not in sys.argv and "--force" not in sys.argv: sys.exit("QA FAILED: video not rendered. Fix and run again (or add --force).")
        else: print("QA OK")
    times = ",".join(f"{min(sch[i+1][0]-.4 if i+1<len(sch) else D-.3, s+1.8):.1f}" for i, (s, e) in enumerate(sch))
    shutil.rmtree(P + "/snaps", ignore_errors=True)
    subprocess.run(["npx", "hyperframes", "snapshot", "--at", times, "--no-end", "-o", "snaps", "."], cwd=P, capture_output=True)
    for f in os.listdir(P + "/snaps"):
        if f.startswith("contact"): shutil.copy(P + "/snaps/" + f, OUT + "/sheet.jpg")
    if "--preview" in sys.argv: print("sheet", OUT); return
    import sfx_lib as S
    sd = P + "/sfx"; os.makedirs(sd, exist_ok=True)
    S.save(sd + "/whoosh.wav", S.whoosh(.35)); S.save(sd + "/hit.wav", S.hit(.3)); S.save(sd + "/bell.wav", S.bell(880, .8)); S.save(sd + "/riser.wav", S.riser(1.0))
    it = [{"file": f"voice/b{i}.wav", "at": sch[i][0]} for i in range(len(beats))]
    if bed == "pluck":
        notes = [220.0, 261.63, 293.66, 329.63, 392.0]
        for n, f in enumerate(notes): S.save(f"{sd}/n{n}.wav", S.pluck(f, 1.2))
        t, k = .2, 0
        while t < D - 1: it.append({"file": f"sfx/n{[0,2,4,2,1,3,4,3][k%8]}.wav", "at": round(t, 2), "gain": .07}); t += .5; k += 1
    elif bed == "drone":
        import numpy as np
        sr = 48000; tt = np.arange(int(sr * D)) / sr
        x = .5 * np.sin(2*np.pi*55*tt) + .3 * np.sin(2*np.pi*82.4*tt) + .2*np.sin(2*np.pi*110*tt*(1+.002*np.sin(tt)))
        S.save(sd + "/bed.wav", S.norm(x * np.minimum(1, tt / 2) * np.minimum(1, (D - tt) / 2), .5)); it.append({"file": "sfx/bed.wav", "at": 0, "gain": .12})
    elif bed == "beat":
        t = .5
        while t < D - .5: it.append({"file": "sfx/hit.wav", "at": round(t, 2), "gain": .14}); t += .5
    MOOD = {"doc": "mystery", "voxflat": "inspire", "kinetic": "tech", "threed": "epic", "paper": "calm", "stick": "happy", "cartoon": "kids", "anime": "sad"}
    mood = ep.get("music", MOOD.get(name, "calm"))
    if mood and mood != "none":
        import music
        music.save(sd + "/music.wav", music.compose(mood, D, seed=len(ep.get("title", "x"))))
        it.append({"file": "sfx/music.wav", "at": 0, "gain": ep.get("music_gain", .16)})
        it = [x for x in it if not (x["file"].startswith("sfx/n") or x["file"] == "sfx/bed.wav")] if ep.get("music_only", True) else it
    for i in range(1, len(beats)): it.append({"file": "sfx/whoosh.wav", "at": round(sch[i][0] - .4, 2), "gain": .14})
    for x in (extra_sfx(sch) if extra_sfx else []): it.append(x)
    json.dump({"duration": D, "target_lufs": -14, "items": it}, open(P + "/mix.json", "w"))
    os.makedirs(P + "/out", exist_ok=True)
    sh([sys.executable, KIT + "/scripts/mix.py", "mix.json", "out/mix.wav"], cwd=P, stdout=subprocess.DEVNULL)
    sh(["sh", KIT + "/scripts/render.sh", ".", "out/mix.wav", OUT + "/video.mp4", "30"], cwd=P, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    sh(["ffmpeg", "-y", "-loglevel", "error", "-i", OUT + "/video.mp4", "-vf", "scale=720:-2", "-c:v", "libx264", "-profile:v", "main", "-crf", "26", "-preset", "fast", "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", OUT + "/video_phone.mp4"])
    real = dur(OUT + "/video.mp4")
    print(f"LENGTH {real:.2f} s" + ("" if real >= float(ep.get("min_duration", 50)) - .1 else "  WARNING: shorter than the minimum"))
    post.caption(ep, OUT, name)
    if ep.get("formats"): post.formats(OUT)
    try: post.cover(ep, P, OUT, sch, D)
    except Exception as ex: print("cover failed:", ex)
    post.deliver(ep, OUT, name)
    print("DONE", OUT, ": deliver/ (ready to upload) + video.mp4 video_phone.mp4 video_16x9.mp4 video_1x1.mp4 cover.jpg cover_check.jpg CAPTION.md")
