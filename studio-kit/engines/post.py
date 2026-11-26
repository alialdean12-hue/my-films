"""After-render steps shared by all engines: quality check (qa), cover, caption document, extra formats.
Each step can also be run alone:  python3 post.py qa|cover|caption|formats video.json OUTDIR"""
import json, os, re, shutil, subprocess, sys
KIT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
def sh(c, **k): return subprocess.run(c, check=True, **k)

# ------------------------------------------------------------------ 1. quality check (text inside the frame, nothing cut)
QA_JS = r"""
const {chromium} = require('playwright');
(async () => {
  const [file, times] = [process.argv[2], JSON.parse(process.argv[3])];
  const b = await chromium.launch(); const p = await b.newPage({viewport: {width: 1080, height: 1920}});
  await p.goto('file://' + file); await p.waitForTimeout(800);
  const out = await p.evaluate((times) => {
    const tl = window.__timelines && (window.__timelines.c || Object.values(window.__timelines)[0]); const issues = [];
    const vis = (el) => { let o = 1; for (let e = el; e && e.id !== 'root'; e = e.parentElement) { const cs = getComputedStyle(e); if (cs.display === 'none' || cs.visibility === 'hidden') return 0; o *= parseFloat(cs.opacity); } return o; };
    for (const [t, clip] of times) {
      tl.seek(t, false);
      const scope = document.getElementById(clip) || document;
      const els = [...scope.querySelectorAll('div,span,text')].filter(e => [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim().length > 1));
      for (const e of els) {
        if (vis(e) < 0.5) continue;
        const rg = document.createRange(); rg.selectNodeContents(e); const r = rg.getBoundingClientRect(); if (r.width < 2) continue;
        const txt = e.textContent.trim().slice(0, 30);
        if (r.left < 20 || r.right > 1060) issues.push(`${t.toFixed(1)}s «${txt}» goes outside the frame sideways (x ${Math.round(r.left)}–${Math.round(r.right)})`);
        if (r.top < 40 || r.bottom > 1880) issues.push(`${t.toFixed(1)}s «${txt}» goes outside the frame top/bottom (y ${Math.round(r.top)}–${Math.round(r.bottom)})`);
        if (e.tagName === 'DIV' && e.scrollWidth > e.clientWidth + 6 && getComputedStyle(e).overflow !== 'visible') issues.push(`${t.toFixed(1)}s «${txt}» is too long for its box`);
      }
    }
    return [...new Set(issues)];
  }, times);
  console.log(JSON.stringify(out)); await b.close();
})();
"""
def qa(P, sch, D, prefix="S"):
    """returns list of problems (empty = OK). Checks every beat when its animation has settled."""
    times = [[min(s + 1.9, (sch[i+1][0] - .3) if i + 1 < len(sch) else D - .2), f"{prefix}{i}"] for i, (s, e, *_) in enumerate(sch)]
    js = os.path.join(P, "_qa.js"); open(js, "w").write(QA_JS)
    r = subprocess.run(["node", js, os.path.join(P, "index.html"), json.dumps(times)], capture_output=True, text=True, cwd=P)
    try: return json.loads(r.stdout.strip().splitlines()[-1])
    except Exception: return [f"QA could not run: {r.stderr[-300:]}"]

# ------------------------------------------------------------------ 1b. automatic text contrast (text colour opposite to the background behind it)
CONTRAST_JS = r"""
const {chromium} = require('playwright');
(async () => {
  const [file, times] = [process.argv[2], JSON.parse(process.argv[3])];
  const b = await chromium.launch(); const p = await b.newPage({viewport: {width: 1080, height: 1920}});
  await p.goto('file://' + file); await p.waitForTimeout(800);
  const hasT = (e) => [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim().length > 1);
  const out = {};
  for (const [t, clip] of times) {
    const boxes = await p.evaluate(([t, clip]) => {
      const tl = window.__timelines && (window.__timelines.c || Object.values(window.__timelines)[0]); if (tl) tl.seek(t, false);
      document.querySelectorAll('[data-start][data-duration]').forEach(c => { if (c.id === 'root' || c.hasAttribute('data-composition-id')) return;
        const a = parseFloat(c.dataset.start), d = parseFloat(c.dataset.duration); c.style.visibility = (t >= a && t < a + d) ? '' : 'hidden'; });
      const all = [...document.querySelectorAll('div,span,text')].filter(e => [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim().length > 1));
      const vis = (el) => { let o = 1; for (let e = el; e && e.id !== 'root'; e = e.parentElement) { const cs = getComputedStyle(e); if (cs.display === 'none' || cs.visibility === 'hidden') return 0; o *= parseFloat(cs.opacity); } return o; };
      const scope = clip ? document.getElementById(clip) : document; const res = [];
      all.forEach((e, i) => { if (scope && scope !== document && !scope.contains(e)) return; if (vis(e) < .5) return;
        const rg = document.createRange(); rg.selectNodeContents(e); const r = rg.getBoundingClientRect(); if (r.width < 4 || r.height < 4) return;
        res.push([i, Math.max(0, r.left), Math.max(0, r.top), Math.min(1080, r.right), Math.min(1920, r.bottom)]); });
      let st = document.getElementById('__hideTxt'); if (!st) { st = document.createElement('style'); st.id = '__hideTxt'; document.head.appendChild(st); }
      st.textContent = 'div,span,text{color:transparent!important;-webkit-text-stroke-color:transparent!important;text-shadow:none!important;fill:transparent!important;stroke:transparent!important}';
      return res; }, [t, clip]);
    for (const [i, x1, y1, x2, y2] of boxes) {
      if (out[i] !== undefined || x2 - x1 < 4 || y2 - y1 < 4) continue;
      const buf = await p.screenshot({clip: {x: x1, y: y1, width: x2 - x1, height: y2 - y1}});
      out[i] = buf.toString('base64');
    }
    await p.evaluate(() => { const st = document.getElementById('__hideTxt'); if (st) st.textContent = ''; });
  }
  console.log(JSON.stringify(out)); await b.close();
})();
"""
CONTRAST_CSS = (".onlight{color:#141414!important;-webkit-text-stroke-color:#ffffff!important;text-shadow:0 5px 0 rgba(255,255,255,.45)!important}"
    "text.onlight{fill:#141414!important;stroke:#ffffff!important}"
    ".onlight .kw,.kw.onlight,.onlight .y,.onlight .r{color:#b0001c!important}"
    ".ondark{color:#ffffff!important;-webkit-text-stroke-color:#111111!important;text-shadow:0 6px 0 rgba(0,0,0,.4)!important}"
    "text.ondark{fill:#ffffff!important;stroke:#111111!important}")
def contrast(P, times, html="index.html"):
    """measures the real background behind every visible text at the given times [[t, clip_id|None]] and
    makes the text dark on light backgrounds, white on dark ones (key words: yellow on dark, deep red on light)."""
    import base64, io
    from PIL import Image
    js = os.path.join(P, "_contrast.js"); open(js, "w").write(CONTRAST_JS)
    r = subprocess.run(["node", js, os.path.join(P, html), json.dumps(times)], capture_output=True, text=True, cwd=P)
    try: shots = json.loads(r.stdout.strip().splitlines()[-1])
    except Exception: print("contrast skipped:", r.stderr[-200:]); return {}
    mode = {}
    for i, b64 in shots.items():
        im = Image.open(io.BytesIO(base64.b64decode(b64))).convert("RGB").resize((24, 24))
        px = list(im.getdata()); lum = sum(.2126*a + .7152*b + .0722*c for a, b, c in px) / len(px) / 255
        if lum > .58: mode[i] = "onlight"
        elif lum < .42: mode[i] = "ondark"
    idx = os.path.join(P, html); s = open(idx).read()
    s = re.sub(r"<style id=\"__contrast\">.*?</script>", "", s, flags=re.S)
    inj = (f'<style id="__contrast">{CONTRAST_CSS}</style><script>(function(){{var M={json.dumps(mode)};'
           'var A=[].slice.call(document.querySelectorAll("div,span,text")).filter(function(e){return [].some.call(e.childNodes,function(n){return n.nodeType===3&&n.textContent.trim().length>1})});'
           '[].forEach.call(document.querySelectorAll("span"),function(e){if(e.style&&e.style.color)e.classList.add("kw");});for(var k in M){var e=A[k];if(!e)continue;if(M[k]==="ondark"&&e.style&&e.style.color)continue;e.classList.add(M[k]);}})();</script>')
    s = s.replace("</body>", inj + "</body>", 1)
    open(idx, "w").write(s)
    print(f"CONTRAST: {sum(v == 'onlight' for v in mode.values())} texts made dark (light background), {sum(v == 'ondark' for v in mode.values())} white (dark background)")
    return mode

# ------------------------------------------------------------------ 2. cover (frame of the video + big title inside the safe area)
def cover(ep, P, OUT, sch, D):
    c = ep.get("cover", {}); at = c.get("at", min(sch[0][0] + 1.8, D - .5) if len(sch) == 1 else sch[min(c.get("beat", 1), len(sch) - 1)][0] + 1.8)
    snap = os.path.join(P, "cover_snap"); shutil.rmtree(snap, ignore_errors=True)
    idx = os.path.join(P, "index.html"); orig = open(idx).read()
    open(idx, "w").write(orig.replace("</style>", ".cap,.tag,.t,.num,.sub,.dt,.bar,#hdl,[id^=cp],[id^=tt]{display:none!important}</style>", 1))   # clean frame: no video captions
    try: subprocess.run(["npx", "hyperframes", "snapshot", "--at", f"{at:.2f}", "--no-end", "-o", "cover_snap", "."], cwd=P, capture_output=True)
    finally: open(idx, "w").write(orig)
    pngs = [f for f in os.listdir(snap) if f.startswith("frame-")] if os.path.isdir(snap) else []
    T = os.path.join(P, "cover"); os.makedirs(T, exist_ok=True)
    shutil.copy(os.path.join(P, "gsap.min.js"), T); shutil.copytree(os.path.join(P, "fonts"), os.path.join(T, "fonts"), dirs_exist_ok=True)
    if pngs: shutil.copy(os.path.join(snap, pngs[0]), os.path.join(T, "bg.png"))
    raw = c.get("text", ep.get("title", "")); plain = re.sub(r"\[/?[yr]\]|<[^>]+>", "", raw).replace("\n", " ")
    n = len(plain); size = c.get("size", 176 if n <= 10 else 150 if n <= 16 else 128 if n <= 24 else 108)
    text = re.sub(r"\[y\](.*?)\[/y\]", r'<span class="y">\1</span>', raw).replace("\n", "<br/>")
    text = re.sub(r"\[r\](.*?)\[/r\]", r'<span class="r">\1</span>', text)
    tag = c.get("tag", ep.get("tag", "")); col = c.get("color", "#ffd21f"); label = c.get("label", "")
    fx, fy = c.get("focus", [540, 960]); zoom = c.get("zoom", 1.25); style = c.get("style", "bold")
    arrow = (f'<svg width="1080" height="1920" style="position:absolute;inset:0"><path d="M{c.get("arrow_from", [940, 1330])[0]},{c.get("arrow_from", [940, 1330])[1]} Q{(fx+880)/2+120:.0f},{(fy+640)/2:.0f} {fx+60},{fy-40}" fill="none" stroke="#ff2a2a" stroke-width="22" stroke-linecap="round"/>'
             f'<circle cx="{fx}" cy="{fy}" r="{c.get("circle_r", 170)}" fill="none" stroke="#ff2a2a" stroke-width="16"/></svg>') if c.get("arrow") else ""
    band = style == "split"
    html = f'''<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><title>cover</title><style>
@font-face{{font-family:"Cairo";src:url("fonts/cairo-ar.woff2") format("woff2");font-weight:200 1000;font-display:block;unicode-range:U+0600-06FF,U+0750-077F,U+FB50-FDFF,U+FE70-FEFC,U+200C-200E;}}
@font-face{{font-family:"Cairo";src:url("fonts/cairo-latin.woff2") format("woff2");font-weight:200 1000;font-display:block;}}
@font-face{{font-family:"F2";src:url("fonts/{c.get("font_file", {"amiri": "amiri", "tajawal": "tajawal", "kufi": "reemkufi", "lalezar": "lalezar", "naskh": "notonaskharabic", "marhey": "marhey", "lemonada": "lemonada"}.get(ep.get("font", ""), "cairo"))}-ar.woff2") format("woff2");font-weight:100 1000;font-display:block;}}
html,body{{margin:0}}#root{{position:relative;width:1080px;height:1920px;overflow:hidden;font-family:"F2","Cairo",sans-serif;direction:rtl;background:#111}}.clip{{position:absolute;inset:0}}
.bg{{position:absolute;inset:0;background:url(bg.png) {fx/10.8:.0f}% {fy/19.2:.0f}%/cover;transform:scale({zoom});transform-origin:{fx}px {fy}px;filter:saturate(1.3) contrast(1.12) brightness(.95)}}
.vg{{position:absolute;inset:0;background:radial-gradient(ellipse at {fx}px {fy}px,#0000 25%,#000c 85%)}}
.band{{position:absolute;left:0;right:0;top:440px;height:520px;background:{c.get("band", "#111")};opacity:.92}}
.t{{position:absolute;left:96px;right:96px;top:{c.get("top", 520 if band else 600)}px;text-align:center;font-weight:900;font-size:{size}px;line-height:1.42;color:#fff;-webkit-text-stroke:{max(10, size//10)}px #000;paint-order:stroke fill;text-shadow:0 12px 30px #000c}}
.y{{display:inline-block;color:#111;-webkit-text-stroke:0;background:{col};padding:0 24px 14px;margin:6px 0;border-radius:18px;line-height:1.15;text-shadow:none;transform:rotate(-2deg)}}.r{{color:#ff3b3b}}
.lab{{position:absolute;top:470px;left:50%;transform:translateX(-50%);background:#fff;color:#111;font-weight:900;font-size:46px;padding:0 30px 8px;border-radius:40px;white-space:nowrap}}
.tag{{position:absolute;top:1370px;left:50%;transform:translateX(-50%);background:#e5322d;color:#fff;font-weight:900;font-size:58px;padding:0 40px 12px;border-radius:14px;white-space:nowrap;box-shadow:0 10px 0 #7a0f0f}}
</style><script src="gsap.min.js"></script></head><body><div id="root" data-composition-id="cv" data-start="0" data-duration="1" data-width="1080" data-height="1920"><div id="a" class="clip" data-start="0" data-duration="1" data-track-index="1">
<div class="bg"></div><div class="vg"></div>{'<div class="band"></div>' if band else ''}{arrow}{f'<div class="lab">{label}</div>' if label else ''}<div class="t">{text}</div>{f'<div class="tag">{tag}</div>' if tag else ''}</div></div>
<script>const tl=gsap.timeline({{paused:true}});tl.to({{}},{{duration:1}},0);window.__timelines={{cv:tl}};</script></body></html>'''
    open(os.path.join(T, "index.html"), "w").write(html)
    shutil.rmtree(os.path.join(T, "snap"), ignore_errors=True)
    contrast(T, [[0.5, None]])
    subprocess.run(["npx", "hyperframes", "snapshot", "--at", "0.5", "--no-end", "-o", "snap", "."], cwd=T, capture_output=True)
    png = [f for f in os.listdir(os.path.join(T, "snap")) if f.startswith("frame-")][0]
    sh(["ffmpeg", "-y", "-loglevel", "error", "-i", os.path.join(T, "snap", png), "-q:v", "2", os.path.join(OUT, "cover.jpg")])
    sh([sys.executable, os.path.join(KIT, "scripts", "cover_check.py"), os.path.join(OUT, "cover.jpg")])

# ------------------------------------------------------------------ 3. caption document (4 copy blocks)
TAGS = {  # niche tags per style (Arabic first); broad tags are added from BROAD
 "doc": ["#قصة_حقيقية", "#وثائقي", "#تاريخ", "#غموض", "#ألغاز"], "collage": ["#لماذا", "#شرح", "#معلومة", "#اقتصاد", "#ثقافة"],
 "voxflat": ["#معلومة", "#إحصائيات", "#شرح", "#اقتصاد", "#تعلم"], "kinetic": ["#تطوير_الذات", "#نصائح", "#تحفيز", "#حكمة", "#نجاح"],
 "threed": ["#فضاء", "#علوم", "#الكون", "#ماذا_لو", "#معلومة"], "paper": ["#تاريخ", "#حضارات", "#قصص", "#آثار", "#تراث"],
 "cine": ["#قصة_حقيقية", "#قصص", "#تاريخ", "#قصة_قصيرة", "#عبرة"], "stick": ["#ماذا_تفعل", "#نصائح", "#سلامة", "#مواقف", "#معلومة_مفيدة"], "anime": ["#أنمي", "#قصة_قصيرة", "#قصص", "#مشاعر", "#عبرة"],
 "cartoon": ["#هل_تعلم", "#حيوانات", "#معلومات_غريبة", "#عالم_الحيوان", "#معلومة"], "saw": ["#لغز", "#ألغاز", "#جريمة", "#تحقيق", "#فكر"]}
BROAD = ["#معلومات", "#قصص", "#هل_تعلم", "#ثقافة_عامة", "#عرب"]
def _clean(t): return re.sub(r"\[/?[yr]\]|<[^>]+>|\n", " ", t or "").strip()
def caption(ep, OUT, style):
    """CAPTION.md: a different title/description/hashtags for YouTube, TikTok and Instagram (each platform rewards different things)."""
    c = ep.get("caption_doc", {}); lines = [b["line"] for b in ep["beats"]]
    hook = c.get("hook", lines[0]); title = c.get("title", _clean(ep.get("title", "")))
    cover_words = _clean(ep.get("cover", {}).get("text", title))
    q = c.get("question", lines[-1] if "؟" in lines[-1] else "ما رأيك؟ اكتب في التعليقات 👇")
    niche = c.get("hashtags") or ep.get("hashtags") or TAGS.get(style, ["#معلومة"])
    if isinstance(niche, str): niche = niche.split()
    if ep.get("no_facts"): niche = [t for t in niche if "حقيقي" not in t] + ["#قصة"]
    own = ["#" + t.replace(" ", "_").lstrip("#") for t in ep.get("tags", [])]
    cover_words = re.sub(r"\s+", " ", cover_words)
    def cut(t, n=60):   # never cut a word in half
        t = t.strip(); return t if len(t) <= n else t[:n].rsplit(" ", 1)[0].rstrip("،,.… ") + "…"
    yt_title = cut(c.get("youtube_title") or (title if len(title) >= 6 else hook))
    uniq = lambda xs: list(dict.fromkeys(xs))
    tiktok_tags = uniq(own + niche)[:3] + BROAD[:1]
    yt_tags = uniq(own + niche)[:3]
    ig_tags = list(dict.fromkeys(own + niche + BROAD))[:12]
    story = " ".join(lines[1:4])
    sep = "━━━━━━━━━━"
    doc = f"""▼ انسخ: عنوان يوتيوب
{yt_title} #shorts
{sep}
▼ انسخ: وصف يوتيوب
{hook}
{story}
{q}
{" ".join(yt_tags)}
{sep}
▼ انسخ: تيك توك
{hook[:90]} {q} {" ".join(tiktok_tags)}
{sep}
▼ انسخ: انستجرام
{hook}

{story}

{q}
احفظ الفيديو وأرسله لصديق يحب {c.get("audience", "هذه القصص")} 📌
.
{" ".join(ig_tags)}
{sep}
(للنشر، لا تنسخ: انشر النسخة الأصلية النظيفة في كل منصة بلا شعار منصة أخرى. أوقات مقترحة للمنطقة العربية: تيك توك 8–11 مساءً · يوتيوب 6–9 مساءً · إنستغرام 7–9 مساءً. نص الغلاف: «{cover_words}».)
"""
    open(os.path.join(OUT, "CAPTION.md"), "w").write(doc)
    # one copy-ready text per platform (see deliver): clean hashtags, digits, no separators inside
    parts = {"1 عنوان يوتيوب": f"{yt_title} #shorts",
             "2 وصف يوتيوب": f"{hook}\n{story}\n\n{q}\n\n{' '.join(yt_tags)}",
             "3 تيك توك": f"{cut(hook, 90)} {q} {' '.join(tiktok_tags)}",
             "4 انستجرام": f"{hook}\n\n{story}\n\n{q}\nاحفظ الفيديو وأرسله لصديق يحب {c.get('audience', 'هذه القصص')} 📌\n.\n{' '.join(ig_tags)}"}
    parts = {k: re.sub(r"[ \t]+", " ", re.sub(r"\\([#_*])", r"\1", v)).strip() + "\n" for k, v in parts.items()}
    notes = (f"أوقات نشر مقترحة للمنطقة العربية: تيك توك 8–11 مساءً · يوتيوب 6–9 مساءً · إنستغرام 7–9 مساءً.\n"
             f"انشر النسخة الأصلية النظيفة في كل منصة بلا شعار منصة أخرى.\nنص الغلاف: «{cover_words}».\n")
    json.dump({"parts": parts, "notes": notes}, open(os.path.join(OUT, "captions.json"), "w"), ensure_ascii=False, indent=1)

# ------------------------------------------------------------------ 4. extra formats: 16:9 (YouTube) and 1:1 (square), blurred background fill
def formats(OUT, src="video.mp4"):
    v = os.path.join(OUT, src)
    for name, W, H in (("video_16x9.mp4", 1920, 1080), ("video_1x1.mp4", 1080, 1080)):
        fc = f"[0]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=30:3,eq=brightness=-0.15[bg];[0]scale=-2:{H}[fg];[bg][fg]overlay=(W-w)/2:0"
        sh(["ffmpeg", "-y", "-loglevel", "error", "-i", v, "-filter_complex", fc, "-c:v", "libx264", "-crf", "22", "-preset", "fast", "-c:a", "copy", "-movflags", "+faststart", os.path.join(OUT, name)])

if __name__ == "__main__":
    step, js, OUT = sys.argv[1], sys.argv[2], os.path.abspath(sys.argv[3]); ep = json.load(open(js)); P = os.path.join(OUT, "project")
    if step == "formats": formats(OUT)
    elif step == "caption": caption(ep, OUT, sys.argv[4] if len(sys.argv) > 4 else "")
    else:
        sch = json.load(open(os.path.join(P, "schedule.json"))); D = sch["D"]; sch = sch["sch"]
        if step == "qa": print("\n".join(qa(P, sch, D)) or "QA OK")
        if step == "cover": cover(ep, P, OUT, sch, D)

# ------------------------------------------------------------------ 5. delivery folder (ready to upload to Google Drive as it is)
CATEGORY = {"1": "جرائم حقيقية عربية", "2": "حروب ومخابرات وأسرار", "3": "قصص تحوّل الحياة والعبرة"}   # Drive: أفلامي/<category>/<title>/
DRIVE = {"doc": "وثائقي", "collage": "Vox", "voxflat": "رسوم Vox", "kinetic": "نصوص متحركة", "threed": "ثلاثي الأبعاد", "paper": "ورق مقصوص", "stick": "رجل العود", "cine": "رجل العود", "anime": "أنمي", "cartoon": "هل تعلم", "saw": "الغاز saw"}
def deliver_saw(ep, OUT):
    """puzzle parts: الغاز saw/<title>/<title> - اللغز.mp4 | - الحل.mp4, غلاف اللغز.jpg | غلاف الحل.jpg (+ wide/square)"""
    t = re.sub(r'[\\/:*?"<>|\n]', " ", ep.get("title", "لغز")).strip(); part = "اللغز" if int(ep.get("part", 1)) == 1 else "الحل"
    d = os.path.join(OUT, "deliver", "أفلامي", "الغاز saw", t); os.makedirs(d, exist_ok=True)
    for src, dst in (("video.mp4", f"{t} - {part}.mp4"), ("thumb.jpg", f"غلاف {part}.jpg")) + ((("video_16x9.mp4", f"{t} - {part} - أفقي.mp4"), ("video_1x1.mp4", f"{t} - {part} - مربع.mp4")) if ep.get("formats") else ()):
        if os.path.exists(os.path.join(OUT, src)): shutil.copy(os.path.join(OUT, src), os.path.join(d, dst))
    print("DELIVER", d); return d
def deliver(ep, OUT, style):
    """OUT/deliver/<Drive folder>/<title>/ with ONLY: <title>.mp4, غلاف.jpg and 5 plain-text files (1 عنوان يوتيوب, 2 وصف يوتيوب, 3 تيك توك, 4 انستجرام, 5 مصادر وملاحظات).
    Wide/square videos only when "formats": true. Nothing else goes to Drive."""
    t = re.sub(r'[\\/:*?"<>|\n]', " ", re.sub(r"\[/?[yr]\]|<[^>]+>", "", ep.get("title", "video"))).strip() or "video"
    d = os.path.join(OUT, "deliver", "أفلامي", ep.get("drive_folder") or CATEGORY.get(str(ep.get("category", "")), "أخرى"), t)
    shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
    pairs = [("video_phone.mp4", f"{t}.mp4"), ("cover.jpg", "غلاف.jpg")]
    if ep.get("formats"): pairs += [("video_16x9.mp4", f"{t} - أفقي.mp4"), ("video_1x1.mp4", f"{t} - مربع.mp4")]
    for src, dst in pairs:
        if os.path.exists(os.path.join(OUT, src)): shutil.copy(os.path.join(OUT, src), os.path.join(d, dst))
    cj = os.path.join(OUT, "captions.json")
    if os.path.exists(cj):   # one plain-text file per platform: open it in Drive, Select all, Copy
        C = json.load(open(cj))
        for name, txt in C["parts"].items(): open(os.path.join(d, f"{name}.txt"), "w", encoding="utf-8-sig").write(txt)
        notes = C["notes"]
    else: notes = ""
    for f in ("SOURCES.txt", "CREDITS.txt"):
        if os.path.exists(os.path.join(OUT, f)): notes += "\n" + open(os.path.join(OUT, f)).read()
    open(os.path.join(d, "5 مصادر وملاحظات.txt"), "w", encoding="utf-8-sig").write(notes)
    print("DELIVER", d, "(upload exactly these files, nothing else)")
    return d
