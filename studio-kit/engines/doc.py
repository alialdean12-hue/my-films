from lib import *
CSS = ('.ph{position:absolute;inset:-6%;background-size:cover;background-position:center}.vg{position:absolute;inset:0;background:radial-gradient(ellipse at 50% 45%,transparent 40%,#000c 100%),linear-gradient(transparent 55%,#000e)}'
       '.cap{position:absolute;left:80px;right:80px;top:1240px;text-align:center;font-weight:900;font-size:84px;line-height:1.25;color:#fff;text-shadow:0 6px 24px #000}.dt{position:absolute;left:0;right:0;top:300px;text-align:center}.dt span{background:#c9a24a;color:#111;font-weight:900;font-size:62px;padding:2px 30px 10px}'
       '.bar{position:absolute;left:300px;right:300px;top:1215px;height:8px;background:#c9a24a}')
ep = load(); B = ep["beats"]
def scene(i, b, s, e, c0, c1):
    D = c1 - c0; js = []; a, z, dx, dy = b.get("cam", [(1.0, 1.18, -40, 0), (1.2, 1.0, 0, 30), (1.0, 1.15, 30, -20), (1.15, 1.0, 0, -30)][i % 4])
    h = f'<div class="ph" id="ph{i}" style="background-image:url(img/{i}.jpg);filter:sepia(.35) contrast(1.1) saturate(.8) brightness(.85)"></div><div class="vg"></div>'
    if b.get("route"):
        h += '<svg class="full" width="1080" height="1920" viewBox="0 0 1080 1920"><path id="rt%d" d="M260,820 C420,700 640,720 860,900" fill="none" stroke="#e5322d" stroke-width="12" stroke-dasharray="26 16"/><circle cx="260" cy="820" r="20" fill="#e5322d"/><circle id="dot%d" cx="860" cy="900" r="22" fill="#e5322d" opacity="0"/></svg>' % (i, i)
    if b.get("date"): h += f'<div class="dt" id="dt{i}" style="opacity:0"><span>{b["date"]}</span></div>'
    h += f'<div class="bar" id="br{i}"></div><div class="cap" id="cp{i}" style="opacity:0">{b["cap"]}</div>'
    if b.get("flash"): h += f'<div id="fl{i}" style="position:absolute;inset:0;background:#fff;opacity:0"></div>'
    js += [f'tl.fromTo("#ph{i}",{{scale:{a},x:{dx},y:{dy}}},{{scale:{z},x:{-dx},y:{-dy},duration:{D:.2f},ease:"none"}},{c0:.2f});',
           f'tl.fromTo("#S{i}",{{opacity:0}},{{opacity:1,duration:.45}},{c0:.2f});' if i else "",
           f'tl.fromTo("#br{i}",{{scaleX:0}},{{scaleX:1,duration:.5,ease:"power2.out"}},{s+.1:.2f});',
           f'tl.fromTo("#cp{i}",{{opacity:0,y:30}},{{opacity:1,y:0,duration:.6,ease:"power2.out"}},{s+.3:.2f});']
    if b.get("date"): js.append(f'tl.fromTo("#dt{i}",{{opacity:0,scaleX:1.4}},{{opacity:1,scaleX:1,duration:.6}},{s:.2f});')
    if b.get("route"): js += [f'tl.fromTo("#rt{i}",{{strokeDashoffset:900}},{{strokeDashoffset:0,duration:2,ease:"none"}},{s+.3:.2f});', f'tl.to("#dot{i}",{{opacity:1,duration:.2}},{s+2.3:.2f});']
    if b.get("flash"): js += [f'tl.fromTo("#fl{i}",{{opacity:.9}},{{opacity:0,immediateRender:false,duration:.5}},{s+.9:.2f});', f'tl.fromTo("#S{i}",{{x:0}},{{x:14,duration:.05,yoyo:true,repeat:9}},{s+.9:.2f});']
    return h, [j for j in js if j]
def images():
    """each beat: "img": path (relative to the json) or "query": English Pixabay search (needs PIXABAY_KEY)."""
    out = os.path.abspath(sys.argv[2]) + "/project/img"; os.makedirs(out, exist_ok=True)
    for i, b in enumerate(B):
        dst = f"{out}/{i}.jpg"
        if os.path.exists(dst): continue
        src = b.get("img")
        if src and not os.path.isabs(src): src = os.path.join(ep["_dir"], src)
        if not src:
            tmp = f"{out}/q{i}"; os.makedirs(tmp, exist_ok=True)
            sh([sys.executable, KIT + "/scripts/pixabay.py", "photos", b["query"], tmp, "--n", "1"], stdout=subprocess.DEVNULL)
            src = tmp + "/" + sorted(os.listdir(tmp))[0]
        sh(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-vf", "scale=-2:2100", "-q:v", "3", dst])
images()
run("1_doc", B, scene, css=CSS, bg="#000", bed="drone", rate="+3%",
    extra_sfx=lambda sch: [{"file": "sfx/hit.wav", "at": round(sch[3][0] + .9, 2), "gain": .35}, {"file": "sfx/riser.wav", "at": round(sch[3][0] - .2, 2), "gain": .15}])
