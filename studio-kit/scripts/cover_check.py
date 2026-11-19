"""Cover safe-area check for every style.
  python3 cover_check.py cover.jpg      -> cover_check.jpg : [full cover + yellow safe box] [4:5 crop] [1:1 crop] [3:4 crop]
Vertical covers (9:16): safe box x 90-990, y 440-1480 on 1080x1920. Horizontal (16:9): 60 px margins + bottom-right 220x90 kept free."""
import subprocess, sys, json
src = sys.argv[1]; out = src.rsplit(".", 1)[0] + "_check.jpg"
w, h = json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=width,height", "-of", "json", src]))["streams"][0].values()
if h > w:
    k = w / 1080
    box = f"drawbox=x={int(90*k)}:y={int(440*k)}:w={int(900*k)}:h={int(1040*k)}:color=yellow@0.9:t={max(4,int(6*k))}"
    crops = [f"crop=iw:iw*5/4:0:(ih-iw*5/4)/2", "crop=iw:iw:0:(ih-iw)/2", "crop=iw:iw*4/3:0:(ih-iw*4/3)/2"]
    fc = f"[0]split=4[a][b][c][d];[a]{box},scale=-1:600[A];[b]{crops[0]},scale=-1:600[B];[c]{crops[1]},scale=-1:600[C];[d]{crops[2]},scale=-1:600[D];[A][B][C][D]hstack=4"
else:
    k = w / 1280
    fc = f"[0]drawbox=x={int(60*k)}:y={int(60*k)}:w={int(1160*k)}:h={int(600*k)}:color=yellow@0.9:t=4,drawbox=x={int(1060*k)}:y={int(630*k)}:w={int(220*k)}:h={int(90*k)}:color=red@0.6:t=fill,scale=-1:600"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-filter_complex", fc, "-q:v", "3", out], check=True)
print(out)
