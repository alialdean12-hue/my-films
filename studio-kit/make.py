"""ONE command for every style.
  python3 make.py <style> video.json OUTDIR [--preview] [--force]
style = number or name:
  1 doc · 2 collage (Vox real photos) · 3 voxflat · 4 kinetic · 5 threed · 6 paper · 7 stick · 8 anime · 9 cartoon · 10 saw (puzzle part json)
Output (styles 1,3–9): video.mp4, video_phone.mp4 (send this one), video_16x9.mp4, video_1x1.mp4, cover.jpg, cover_check.jpg, CAPTION.md.
Run  sh scripts/doctor.sh  once per machine first."""
import os, shutil, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
STYLES = {"1": "doc", "2": "collage", "3": "voxflat", "4": "kinetic", "5": "threed", "6": "paper", "7": "stick", "8": "anime", "9": "cartoon", "10": "saw"}
def main():
    if len(sys.argv) < 4: sys.exit(__doc__)
    st = STYLES.get(sys.argv[1], sys.argv[1]); js, out = os.path.abspath(sys.argv[2]), os.path.abspath(sys.argv[3]); extra = sys.argv[4:]
    if st in ("doc", "voxflat", "kinetic", "threed", "paper", "stick", "cartoon", "anime"):
        cmd = [sys.executable, os.path.join(HERE, "engines", st + ".py"), js, out] + extra; cwd = os.path.join(HERE, "engines")
    elif st == "collage":
        cmd = [sys.executable, os.path.join(HERE, "collage", "make_collage.py"), js, out] + extra; cwd = os.path.join(HERE, "collage")
    elif st == "saw":
        cmd = [sys.executable, os.path.join(HERE, "series", "saw_5tory", "make_episode.py"), js, out] + extra; cwd = os.path.join(HERE, "series", "saw_5tory")
    else: sys.exit(f"unknown style {sys.argv[1]}\n" + __doc__)
    r = subprocess.run(cmd, cwd=cwd).returncode
    if r == 0 and st == "collage" and "--preview" not in extra:   # give collage the same extras as the engines
        sys.path.insert(0, os.path.join(HERE, "engines")); import json, post
        ep = json.load(open(js)); post.caption(ep, out, "collage"); (post.formats(out) if ep.get("formats") else None); shutil.copy(os.path.join(out, "video.mp4"), os.path.join(out, "video_phone.mp4")); post.deliver(ep, out, "collage")
    if r == 0 and st == "saw" and "--preview" not in extra:   # wide/square versions + Drive folder with the series file names
        sys.path.insert(0, os.path.join(HERE, "engines")); import json, post
        ep = json.load(open(js)); (post.formats(out) if ep.get("formats") else None); post.deliver_saw(ep, out)
    sys.exit(r)
if __name__ == "__main__":
    main()
