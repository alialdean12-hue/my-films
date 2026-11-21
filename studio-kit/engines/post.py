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
    text = c.get("text", ep.get("title", "")); text = re.sub(r"\[y\](.*?)\[/y\]", r'<span class="y">\1</span>', text).replace("\n", "<br/>")
    text = re.sub(r"\[r\](.*?)\[/r\]", r'<span class="r">\1</span>', text)
    tag = c.get("tag", ep.get("tag", "")); col = c.get("color", "#ffd21f")
    html = f'''<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><title>cover</title><style>
@font-face{{font-family:"Cairo";src:url("fonts/cairo-ar.woff2") format("woff2");font-weight:200 1000;font-display:block;unicode-range:U+0600-06FF,U+0750-077F,U+FB50-FDFF,U+FE70-FEFC,U+200C-200E;}}
@font-face{{font-family:"Cairo";src:url("fonts/cairo-latin.woff2") format("woff2");font-weight:200 1000;font-display:block;}}
@font-face{{font-family:"F2";src:url("fonts/{c.get("font_file", {"amiri": "amiri", "tajawal": "tajawal", "kufi": "reemkufi", "lalezar": "lalezar", "naskh": "notonaskharabic", "marhey": "marhey", "lemonada": "lemonada"}.get(ep.get("font", ""), "cairo"))}-ar.woff2") format("woff2");font-weight:100 1000;font-display:block;}}
html,body{{margin:0}}#root{{position:relative;width:1080px;height:1920px;overflow:hidden;font-family:"F2","Cairo",sans-serif;direction:rtl;background:#111}}.clip{{position:absolute;inset:0}}
.bg{{position:absolute;inset:0;background:url(bg.png) center/cover;filter:saturate(1.15) contrast(1.05)}}.sh{{position:absolute;inset:0;background:linear-gradient(#0000 22%,#000b 40%,#000b 72%,#0000 88%)}}
.t{{position:absolute;left:110px;right:110px;top:{c.get("top", 700)}px;text-align:center;font-weight:900;font-size:{c.get("size", 136)}px;line-height:1.15;color:#fff;-webkit-text-stroke:16px #000;paint-order:stroke fill}}
.y{{color:{col}}}.r{{color:#ff3b3b}}.tag{{position:absolute;top:1360px;left:50%;transform:translateX(-50%);background:#e5322d;color:#fff;font-weight:900;font-size:60px;padding:0 40px 12px;border-radius:14px;white-space:nowrap}}
</style><script src="gsap.min.js"></script></head><body><div id="root" data-composition-id="cv" data-start="0" data-duration="1" data-width="1080" data-height="1920"><div id="a" class="clip" data-start="0" data-duration="1" data-track-index="1">
<div class="bg"></div><div class="sh"></div><div class="t">{text}</div>{f'<div class="tag">{tag}</div>' if tag else ''}</div></div>
<script>const tl=gsap.timeline({{paused:true}});tl.to({{}},{{duration:1}},0);window.__timelines={{cv:tl}};</script></body></html>'''
    open(os.path.join(T, "index.html"), "w").write(html)
    shutil.rmtree(os.path.join(T, "snap"), ignore_errors=True)
    subprocess.run(["npx", "hyperframes", "snapshot", "--at", "0.5", "--no-end", "-o", "snap", "."], cwd=T, capture_output=True)
    png = [f for f in os.listdir(os.path.join(T, "snap")) if f.startswith("frame-")][0]
    sh(["ffmpeg", "-y", "-loglevel", "error", "-i", os.path.join(T, "snap", png), "-q:v", "2", os.path.join(OUT, "cover.jpg")])
    sh([sys.executable, os.path.join(KIT, "scripts", "cover_check.py"), os.path.join(OUT, "cover.jpg")])

# ------------------------------------------------------------------ 3. caption document (4 copy blocks)
TAGS = {"doc": "#وثائقي #قصة #تاريخ #هل_تعلم", "voxflat": "#شرح #معلومة #اقتصاد #تعلم", "kinetic": "#تحفيز #نصائح #اقتباسات #تطوير_الذات", "threed": "#فضاء #علوم #هل_تعلم #معلومة",
        "paper": "#تاريخ #حضارة #أماكن #قصة", "stick": "#نصائح #ماذا_تفعل #سلامة #معلومة", "cartoon": "#هل_تعلم #حيوانات #معلومات #أطفال", "collage": "#شرح #معلومة #لماذا #تعلم"}
def caption(ep, OUT, style):
    c = ep.get("caption_doc", {}); lines = [b["line"] for b in ep["beats"]]
    title = c.get("title", re.sub(r"\[/?[yr]\]|<[^>]+>|\n", " ", ep.get("cover", {}).get("text", ep.get("title", ""))).strip())
    desc = c.get("description", " ".join(lines[:2]))
    q = c.get("question", lines[-1] if "؟" in lines[-1] else "ما رأيك؟ اكتب في التعليقات 👇")
    tags = c.get("hashtags", TAGS.get(style, "#معلومة #هل_تعلم")) + (" " + " ".join("#" + t.replace(" ", "_") for t in ep.get("tags", [])) if ep.get("tags") else "")
    sep = "━━━━━━━━━━"
    doc = f"""▼ انسخ: عنوان يوتيوب
{title} #shorts
{sep}
▼ انسخ: وصف يوتيوب
{desc}
{q}
{tags}
{sep}
▼ انسخ: انستجرام
{title}
{" ".join(lines[:3])}
{q}
احفظه وشاركه مع من يحتاجه.
{tags}
{sep}
▼ انسخ: تيك توك
{title} {q} {tags}
"""
    open(os.path.join(OUT, "CAPTION.md"), "w").write(doc)

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
DRIVE = {"doc": "وثائقي", "collage": "Vox", "voxflat": "رسوم Vox", "kinetic": "نصوص متحركة", "threed": "ثلاثي الأبعاد", "paper": "ورق مقصوص", "stick": "رجل العود", "anime": "أنمي", "cartoon": "هل تعلم", "saw": "الغاز saw"}
def deliver_saw(ep, OUT):
    """puzzle parts: الغاز saw/<title>/<title> - اللغز.mp4 | - الحل.mp4, غلاف اللغز.jpg | غلاف الحل.jpg (+ wide/square)"""
    t = re.sub(r'[\\/:*?"<>|\n]', " ", ep.get("title", "لغز")).strip(); part = "اللغز" if int(ep.get("part", 1)) == 1 else "الحل"
    d = os.path.join(OUT, "deliver", "الغاز saw", t); os.makedirs(d, exist_ok=True)
    for src, dst in (("video.mp4", f"{t} - {part}.mp4"), ("thumb.jpg", f"غلاف {part}.jpg")) + ((("video_16x9.mp4", f"{t} - {part} - أفقي.mp4"), ("video_1x1.mp4", f"{t} - {part} - مربع.mp4")) if ep.get("formats") else ()):
        if os.path.exists(os.path.join(OUT, src)): shutil.copy(os.path.join(OUT, src), os.path.join(d, dst))
    print("DELIVER", d); return d
def deliver(ep, OUT, style):
    """OUT/deliver/<Drive folder>/<title>/ with ONLY: <title>.mp4, غلاف.jpg, الوصف.txt (captions + sources + photo credits at the end).
    Wide/square videos only when "formats": true. Nothing else goes to Drive."""
    t = re.sub(r'[\\/:*?"<>|\n]', " ", re.sub(r"\[/?[yr]\]|<[^>]+>", "", ep.get("title", "video"))).strip() or "video"
    d = os.path.join(OUT, "deliver", ep.get("drive_folder", DRIVE.get(style, "فيديوهات")), t)
    shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
    pairs = [("video_phone.mp4", f"{t}.mp4"), ("cover.jpg", "غلاف.jpg")]
    if ep.get("formats"): pairs += [("video_16x9.mp4", f"{t} - أفقي.mp4"), ("video_1x1.mp4", f"{t} - مربع.mp4")]
    for src, dst in pairs:
        if os.path.exists(os.path.join(OUT, src)): shutil.copy(os.path.join(OUT, src), os.path.join(d, dst))
    txt = open(os.path.join(OUT, "CAPTION.md")).read() if os.path.exists(os.path.join(OUT, "CAPTION.md")) else ""
    for f in ("SOURCES.txt", "CREDITS.txt"):
        if os.path.exists(os.path.join(OUT, f)): txt += "\n━━━━━━━━━━\n" + open(os.path.join(OUT, f)).read()
    open(os.path.join(d, "الوصف.txt"), "w").write(txt)
    print("DELIVER", d, "(upload exactly these files, nothing else)")
    return d
