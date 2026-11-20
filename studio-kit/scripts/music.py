"""Mood music, composed offline (numpy): chords + bass + melody + drums, loops cleanly.
  python music.py <mood> seconds out.wav [--bpm N] [--seed N]
moods: epic mystery calm sad happy tech kids horror news islamic suspense inspire
Every track: 48 kHz mono, fades in/out, mixed low enough to sit under a voice."""
import sys, wave, math
import numpy as np
SR = 48000
N = lambda m: 440.0 * 2 ** ((m - 69) / 12)
MOODS = {  # bpm, key root (midi), scale, progression (scale degrees), lead instrument, drums pattern, pad
 "epic":     (96, 50, [0, 2, 3, 5, 7, 8, 10], [0, 5, 3, 6], "brass", "boom", "strings"),
 "mystery":  (80, 45, [0, 2, 3, 5, 7, 8, 11], [0, 5, 0, 4], "bell", "tick", "dark"),
 "calm":     (76, 60, [0, 2, 4, 7, 9], [0, 3, 4, 2], "pluck", "soft", "warm"),
 "sad":      (70, 57, [0, 2, 3, 5, 7, 8, 10], [0, 5, 2, 6], "piano", "none", "strings"),
 "happy":    (118, 60, [0, 2, 4, 5, 7, 9, 11], [0, 4, 5, 3], "pluck", "pop", "warm"),
 "tech":     (110, 52, [0, 3, 5, 7, 10], [0, 3, 1, 4], "saw", "four", "dark"),
 "kids":     (124, 65, [0, 2, 4, 5, 7, 9, 11], [0, 3, 4, 0], "bell", "pop", "warm"),
 "horror":   (60, 41, [0, 1, 3, 6, 7, 8, 11], [0, 1, 0, 6], "bell", "heart", "dark"),
 "news":     (104, 55, [0, 2, 4, 5, 7, 9, 11], [0, 5, 3, 4], "saw", "tick", "strings"),
 "islamic":  (72, 50, [0, 1, 4, 5, 7, 8, 10], [0, 3, 0, 4], "oud", "frame", "warm"),
 "suspense": (88, 47, [0, 2, 3, 5, 7, 8, 11], [0, 0, 5, 4], "pluck", "tick", "dark"),
 "inspire":  (100, 55, [0, 2, 4, 5, 7, 9, 11], [0, 4, 5, 3], "piano", "soft", "strings"),
}
def env(n, a=.01, r=.3):
    t = np.arange(n) / SR; e = np.minimum(1, t / a) * np.exp(-t / r); return e
def osc(f, n, kind):
    t = np.arange(n) / SR
    if kind == "saw": return 2 * ((t * f) % 1) - 1
    if kind == "sq": return np.sign(np.sin(2 * np.pi * f * t))
    if kind == "tri": return 2 * np.abs(2 * ((t * f) % 1) - 1) - 1
    return np.sin(2 * np.pi * f * t)
def inst(kind, f, n):
    if kind == "piano": return (osc(f, n, "sin") + .4 * osc(2 * f, n, "sin") + .15 * osc(3 * f, n, "sin")) * env(n, .005, .9)
    if kind == "pluck": return (osc(f, n, "tri") + .3 * osc(2 * f, n, "sin")) * env(n, .003, .35)
    if kind == "bell": return (osc(f, n, "sin") + .5 * osc(f * 2.76, n, "sin") * np.exp(-np.arange(n) / SR / .2)) * env(n, .002, 1.2)
    if kind == "brass": return np.tanh(2 * osc(f, n, "saw")) * env(n, .06, .8) * .6
    if kind == "saw": return osc(f, n, "saw") * env(n, .01, .25) * .5
    if kind == "oud": return (osc(f, n, "tri") * .8 + .5 * osc(2 * f, n, "saw") * .3) * env(n, .002, .5)
    return osc(f, n, "sin") * env(n)
def lp(x, a):
    y = np.empty_like(x); s = 0.0
    for i in range(0, len(x)):
        s += a * (x[i] - s); y[i] = s
    return y
def drum(kind, n):
    t = np.arange(n) / SR; rng = np.random.default_rng(3)
    if kind == "kick": return np.sin(2 * np.pi * (110 * np.exp(-t * 18) + 40) * t) * np.exp(-t * 9)
    if kind == "snare": return (rng.normal(0, 1, n) * .7 + np.sin(2 * np.pi * 190 * t) * .4) * np.exp(-t * 18)
    if kind == "hat": x = rng.normal(0, 1, n); return (x - np.concatenate([[0], x[:-1]])) * np.exp(-t * 60) * .3
    if kind == "tom": return np.sin(2 * np.pi * (140 * np.exp(-t * 6) + 60) * t) * np.exp(-t * 6)
    return np.zeros(n)
PAT = {  # 16 steps per bar: (instrument, steps)
 "boom": [("kick", [0, 10]), ("tom", [8, 14]), ("hat", [4, 12])], "tick": [("hat", list(range(0, 16, 2))), ("kick", [0])],
 "soft": [("kick", [0, 8]), ("hat", [4, 12])], "pop": [("kick", [0, 8]), ("snare", [4, 12]), ("hat", list(range(0, 16, 2)))],
 "four": [("kick", [0, 4, 8, 12]), ("hat", [2, 6, 10, 14]), ("snare", [4, 12])], "heart": [("kick", [0, 2])], "frame": [("tom", [0, 6, 10]), ("hat", [3, 7, 12, 14])], "none": [],
}
def compose(mood, secs, bpm=None, seed=1):
    b0, root, scale, prog, lead, dr, pad = MOODS[mood]; bpm = bpm or b0
    beat = 60 / bpm; bar = 4 * beat; nb = max(2, int(math.ceil(secs / bar))); n = int(SR * nb * bar) + SR
    out = np.zeros(n); rng = np.random.default_rng(seed)
    deg = lambda d, o=0: root + scale[d % len(scale)] + 12 * (d // len(scale) + o)
    for k in range(nb):
        t0 = int(k * bar * SR); d = prog[k % len(prog)]; L = int(bar * SR)
        chord = [deg(d), deg(d + 2), deg(d + 4)]
        padw = sum((osc(N(m + 12), L, "saw" if pad == "strings" else "tri") for m in chord)) / 3
        padw = lp(padw, .05 if pad == "dark" else .12) * np.minimum(1, np.arange(L) / (SR * .4)) * np.minimum(1, (L - np.arange(L)) / (SR * .4))
        out[t0:t0 + L] += padw * (.16 if pad != "dark" else .2)
        for q in range(4):  # bass on beats
            nn = int(beat * SR * .9); s = t0 + int(q * beat * SR)
            out[s:s + nn] += osc(N(deg(d, -1)), nn, "tri") * env(nn, .01, .35) * .3
        for st in range(8):  # melody on 8ths, sparse
            if rng.random() < (.55 if mood not in ("sad", "horror", "mystery") else .3):
                m = deg(d + int(rng.choice([0, 2, 4, 1, 3, 5, 7])), 1); nn = int(beat * SR * (1.5 if lead in ("bell", "piano") else .8))
                s = t0 + int(st * beat / 2 * SR); seg = inst(lead, N(m), nn) * .16
                out[s:s + nn] += seg[: len(out[s:s + nn])]
        for kind, steps in PAT[dr]:
            for st in steps:
                nn = int(.4 * SR); s = t0 + int(st * beat / 4 * SR); x = drum(kind, nn) * (.35 if kind == "kick" else .18)
                out[s:s + nn] += x[: len(out[s:s + nn])]
    out = out[: int(secs * SR)]
    t = np.arange(len(out)) / SR; out *= np.minimum(1, t / 1.5) * np.minimum(1, (secs - t) / 2)
    out = np.tanh(out * 1.4); return out / (np.abs(out).max() + 1e-9) * .7
def save(path, x):
    w = wave.open(path, "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((x * 32767).astype(np.int16).tobytes()); w.close()
if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] not in MOODS: sys.exit(__doc__)
    bpm = int(a[a.index("--bpm") + 1]) if "--bpm" in a else None; seed = int(a[a.index("--seed") + 1]) if "--seed" in a else 1
    save(a[2], compose(a[0], float(a[1]), bpm, seed)); print("ok", a[2])
