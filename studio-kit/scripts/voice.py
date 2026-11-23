"""Narration for every style: synth(lines, outdir, voice, rate, voice_files=None) -> outdir/<id>.wav (trimmed, 48k mono).
Order: voice_files folder (your own TTS) -> local cache -> edge-tts here -> edge-tts on GitHub (when this sandbox blocks it)."""
import hashlib, json, os, shutil, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import remote
CACHE = os.environ.get("VOICE_CACHE") or os.path.join(remote.ROOT, "voice_cache")
def key(text, voice, rate): return hashlib.sha1(f"{text}|{voice}|{rate}".encode()).hexdigest()[:16]
def _wav(src, dst): subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-ac", "1", "-ar", "48000", dst], check=True)
def synth(lines, outdir, voice="ar-SA-HamedNeural", rate="+0%", voice_files=None):
    os.makedirs(outdir, exist_ok=True)
    if voice_files:
        for ln in lines:
            src = next((f"{voice_files}/{ln['id']}.{x}" for x in ("wav", "mp3", "flac", "ogg", "m4a") if os.path.exists(f"{voice_files}/{ln['id']}.{x}")), None)
            if not src: sys.exit(f"voice_files: missing {ln['id']}.wav (or .mp3/.flac) in {voice_files}")
            _wav(src, f"{outdir}/{ln['id']}.wav")
        return
    todo = []
    for ln in lines:
        c = os.path.join(CACHE, key(ln["text"], voice, rate), "v.flac")
        if os.path.exists(c): _wav(c, f"{outdir}/{ln['id']}.wav")
        else: todo.append(ln)
    if not todo: return
    lj = os.path.join(outdir, "_todo.json"); json.dump(todo, open(lj, "w"), ensure_ascii=False)
    r = subprocess.run([sys.executable, os.path.join(HERE, "tts_edge.py"), lj, outdir, "--voice", voice, f"--rate={rate}"], capture_output=True, text=True)
    if r.returncode == 0:
        for ln in todo:   # keep a copy so the same line is never synthesised twice
            d = os.path.join(CACHE, key(ln["text"], voice, rate)); os.makedirs(d, exist_ok=True)
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{outdir}/{ln['id']}.wav", f"{d}/v.flac"]); open(f"{d}/done", "w").close()
        return
    items = [dict(key=key(ln["text"], voice, rate), text=ln["text"], voice=voice, rate=rate, raw=bool(ln.get("raw"))) for ln in todo]
    bad = remote.request("voice", items, CACHE)
    if bad: sys.exit("VOICE FAILED on GitHub too: " + open(os.path.join(CACHE, bad[0]["key"], "error.txt")).read()[:300]
                     + '\nMake the audio with your own TTS: b0.wav b1.wav ... in a folder, then add "voice_files": "<folder>" to the json.')
    for ln, it in zip(todo, items): _wav(os.path.join(CACHE, it["key"], "v.flac"), f"{outdir}/{ln['id']}.wav")
if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) < 2: sys.exit("usage: voice.py lines.json outdir [voice] [rate]")
    synth(json.load(open(a[0])), a[1], *(a[2:4]))
