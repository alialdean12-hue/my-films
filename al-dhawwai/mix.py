"""«الضوّاي» — score (1930s symphonic-jazz torch ballad, 84 BPM, D minor → F) + foley from window.EV + narration → out/mix.wav
Run: $LIB/.venv/bin/python mix.py   (LIB = the Lemo-Opuscar library folder)"""
import os, sys, json, numpy as np, soundfile as sf, soxr
HERE = os.path.dirname(os.path.abspath(__file__))
LIB = os.environ.get('LIB') or os.path.abspath(os.path.join(HERE, '../..'))
sys.path.insert(0, LIB)
from core.audio.sfx import SR, bp, lp, hp, noise, norm, t_, env_exp, brown, whoosh, thump, step, ding, add, limit, compress
from core.audio import sampler as S

E = json.load(open(os.path.join(HERE, 'events.json'))); EV = E['ev']; DUR = E['dur']
GRID = next(e for e in EV if e['type'] == 'grid'); SEC = GRID['sections']; BPM = GRID['bpm']; BT = 60 / BPM
Z0, Z1, WORD = GRID['zoom0'], GRID['zoom1'], GRID['word']
N = int((DUR + 1.5) * SR)
S.seed(7)
def st(): return np.zeros((N, 2), np.float32)
def bt(n): return n * BT
def fit(x):
    y = np.zeros((N, 2), np.float32); y[:min(N, len(x))] = x[:N]; return y

# ================= score =================
ev = []   # (t, inst, pitch, dur, vel, pan[, gain])
def chord(t, inst, pitches, d, v, pan=0, g=1, strum=0):
    for i, p in enumerate(pitches): ev.append((t + i * strum, inst, p, d, v, pan, g))
DM, BB, GM, A7 = ['D4', 'F4', 'A4'], ['D4', 'F4', 'Bb4'], ['D4', 'G4', 'Bb4'], ['C#4', 'E4', 'G4', 'A4']
ROOT = {'Dm': 'D2', 'Bb': 'Bb1', 'Gm': 'G2', 'A7': 'A1', 'F': 'F2', 'C': 'C2'}
VOX = {'Dm': DM, 'Bb': BB, 'Gm': GM, 'A7': A7, 'F': ['C4', 'F4', 'A4'], 'C': ['C4', 'E4', 'G4']}
PROG = ['Dm', 'Bb', 'Gm', 'A7']

# 1 · hook: a harp glissando and a glockenspiel chord on the ignition; a low string bed
ign = next(e['t'] for e in EV if e['type'] == 'ignite')
for i, p in enumerate(['D3', 'F3', 'A3', 'D4', 'F4', 'A4', 'D5', 'F5', 'A5', 'D6']): ev.append((ign - .32 + i * .035, 'harp', p, 2.5, .45 + i * .03, -.3 + i * .06, .9))
chord(ign, 'glockenspiel', ['D6', 'F6', 'A6'], 3, .5, .2, .8)
ev.append((ign, 'cellos', 'D3', bt(9), .35, -.2, .8)); ev.append((ign, 'violas', 'A3', bt(9), .3, .2, .7))
# 2 · title: strings swell + soft trombone chord
t0 = SEC['title'][0]
chord(t0, 'trombone', ['D3', 'A3', 'F3'], bt(4), .45, 0, .7)
chord(t0, 'violins', ['F4', 'A4', 'D5'], bt(6), .45, .1, .8)
ev.append((t0, 'cellos', 'D3', bt(6), .45, -.2, .8))
for i, p in enumerate(['A4', 'D5', 'F5', 'A5']): ev.append((t0 + .1 + i * .06, 'glockenspiel', p, 1.5, .5, .2, .6))
# 3 · street + clock: stride piano (bass on 1&3, chords on 2&4), pizz bass, brushes; a glock note per lamp
def stride(b0, b1, vel=.55, lamp=True):
    for bar in range(int(b0) // 4, int(np.ceil(b1 / 4))):
        c = PROG[bar % 4]
        for k in range(4):
            bb = bar * 4 + k
            if bb < b0 or bb >= b1: continue
            t = bt(bb)
            if k % 2 == 0: ev.append((t, 'piano', ROOT[c].replace('1', '2') if k == 0 else ROOT[c].replace('2', '3').replace('1', '2'), BT * .9, vel, -.25, .9)); ev.append((t, 'contrabass_pizz', ROOT[c], BT, vel + .1, -.1, 1))
            else: chord(t, 'piano', VOX[c], BT * .6, vel * .8, .15, .8)
            ev.append((t + BT * .5, 'snare', None, None, .12, .3, .25))
stride(16, 29)
for e in EV:
    if e['type'] == 'ignite' and SEC['street'][0] < e['t'] < SEC['clock'][0] and e.get('pan', 0) < 0:
        ev.append((e['t'], 'glockenspiel', ['A5', 'D6', 'F6', 'A6', 'D7'][int(e['t'] * 7) % 5], 1.2, .45, -.2, .55))
# 4 · the wrong order: clarinet motif in fragments, pizz "wrong" notes on each skipped lamp
stride(29, 43, .45)
MOTIF = [(0, 'A4', 1), (1, 'D5', 1), (2, 'F5', 1.5), (3.5, 'E5', .5), (4, 'D5', 2), (6, 'C5', 1), (7, 'A4', 1)]
for (o, p, d) in MOTIF[:4]: ev.append((bt(30 + o), 'clarinet', p, bt(d) * .95, .55, .2, .9))
for (o, p, d) in MOTIF[:3]: ev.append((bt(38 + o), 'clarinet', p, bt(d) * .95, .5, .2, .85))
wrong = ['G#4', 'Eb5', 'B4', 'F#5', 'C#5', 'Ab4', 'E5', 'Bb4', 'G5', 'D#5']
for e in EV:
    if e['type'] == 'skip': ev.append((e['t'], 'violins_pizz', wrong[e['n'] - 1], .4, .5, -.2 + e['n'] * .04, .7))
for e in EV:
    if e['type'] == 'ignite' and SEC['skip'][0] < e['t'] < SEC['tele'][0]: chord(e['t'], 'glockenspiel', ['D6', 'A6'], 1.5, .55, 0, .7)
# 5 · telegram: muted trumpet comments over string tremolo
t5 = SEC['tele'][0]
for c, b0 in zip(['Dm', 'Gm', 'A7'], [43, 47, 51]):
    chord(bt(b0), 'violins_trem', VOX[c], bt(4), .32, .2, .7); ev.append((bt(b0), 'cellos', ROOT[c].replace('1', '2').replace('2', '3') if c != 'A7' else 'A2', bt(4), .35, -.2, .7))
for (o, p, d) in [(1, 'D5', .5), (1.5, 'E5', .5), (2, 'F5', 2), (5, 'E5', .5), (5.5, 'D5', .5), (6, 'C#5', 2.5), (9, 'A4', 1), (10, 'D5', 1)]:
    ev.append((bt(43 + o), 'trumpet_mute', p, bt(d) * .95, .45, .25, .8))
# 6 · the face: piano alone, then silence (43.0 → 45.5)
for (b_, p) in [(54, 'D4'), (55, 'F4'), (56, 'A4'), (57.5, 'C5'), (58.5, 'Bb4')]: ev.append((bt(b_), 'piano', p, bt(1.5), .45, .1, .8))
ev.append((bt(54), 'piano', 'D3', bt(4), .4, -.2, .8))
# 7 · the reveal: from the silence, strings rise; the full theme in F on the word
tc = 45.5
ev.append((tc, 'timpani', None, None, .25, 0, .5))
for i, c in enumerate(['Dm', 'Bb', 'C']):
    t = tc + i * bt(3.6)
    chord(t, 'violins', [p.replace('4', '5') for p in VOX[c]], bt(3.6), .38 + i * .08, .2, .8); ev.append((t, 'cellos', ROOT[c].replace('1', '2').replace('2', '3'), bt(3.6), .4 + i * .05, -.2, .8))
    ev.append((t, 'contrabass', ROOT[c].replace('1', '2'), bt(3.6), .35, 0, .6))
for i, p in enumerate(['F3', 'A3', 'C4', 'F4', 'A4', 'C5', 'F5', 'A5', 'C6', 'F6', 'A6']): ev.append((WORD - .45 + i * .04, 'harp', p, 3, .5 + i * .03, -.4 + i * .08, .9))
THEME = [(0, 'A4', 1), (1, 'C5', 1), (2, 'F5', 1.5), (3.5, 'E5', .5), (4, 'F5', 2), (6, 'G5', 1), (7, 'A5', 3)]
for (o, p, d) in THEME:
    ev.append((WORD + bt(o), 'clarinet', p, bt(d) * .95, .6, .15, .9)); ev.append((WORD + bt(o), 'violins', p, bt(d) * .95, .42, -.15, .7))
for i, c in enumerate(['F', 'Dm', 'Bb', 'C', 'F']):
    t = WORD + bt(i * 2)
    chord(t, 'violins', VOX[c], bt(2), .35, .2, .55); ev.append((t, 'cellos', ROOT[c].replace('1', '2').replace('2', '3'), bt(2), .45, -.2, .75))
    chord(t, 'trombone', [ROOT[c].replace('1', '2').replace('2', '3')], bt(2), .3, 0, .4)
chord(WORD, 'glockenspiel', ['F6', 'A6', 'C7'], 3, .55, .3, .7)
ev.append((WORD, 'sus_cymbal', None, None, .35, 0, .5))
# 8 · Noor: strings settle, glock sparkle on the tear
for e in EV:
    if e['type'] == 'sparkle': chord(e['t'], 'glockenspiel', ['A6', 'D7'], 2, .45, .2, .6)
# 9 · ending: piano alone, a descending note on each pair of lamps going out; the clarinet holds the last note
endt = SEC['end'][0]
chord(endt, 'piano', ['D3', 'A3', 'F4'], bt(4), .4, 0, .8)
desc = ['A5', 'G5', 'F5', 'E5', 'D5', 'C5', 'Bb4', 'A4', 'G4', 'F4']
offs = sorted(e['t'] for e in EV if e['type'] == 'off' and e['pan'] > 0 and e['t'] < SEC['card'][0])
for i, t in enumerate(offs): ev.append((t, 'piano', desc[i % len(desc)], BT * 1.2, .4, .1, .8))
ev.append((63.6, 'clarinet', 'A4', 2.6, .45, .15, .85)); ev.append((66.0, 'clarinet', 'D5', 5.0, .42, .15, .85))
chord(63.6, 'cellos', ['D3'], 7.5, .3, -.2, .7); chord(63.6, 'violas', ['A3', 'F3'], 7.5, .25, .2, .6)
# 10 · card: final chord, D major (a warm turn), tubular bell
tc = SEC['card'][0]
chord(tc + .2, 'piano', ['D3', 'A3', 'D4', 'F#4', 'A4'], 4, .4, 0, .8, strum=.04)
chord(tc + .2, 'violins', ['F#4', 'A4', 'D5'], 4, .3, .2, .6)
ev.append((tc + .2, 'tubular_bells', 'D5', 5, .45, 0, .6))
chord(tc + .25, 'glockenspiel', ['D6', 'F#6', 'A6'], 3, .45, .2, .5)

def safe_render(events):
    out = st(); bad = set()
    for e in events:
        t, inst = e[0], e[1]
        try:
            x = S.note(inst, e[2], e[3], vel=e[4]) if e[2] is not None else S.hit(inst, None, e[4], dur=e[3])
        except Exception as ex:
            if inst not in bad: print('  skip instrument', inst, '·', str(ex)[:80]); bad.add(inst)
            continue
        add(out, x.astype(np.float32), max(0, t), e[6] if len(e) > 6 else 1, e[5])
    return out
music = safe_render(ev)
music = music * .7 + S.room(music, size=.62, mix=1.0) * .3

# ================= foley =================
fx = st()
R = np.random.default_rng(1937)
def lamp_on(v=1):     # brass switch click + gas "whump" + filament hum
    k = bp(noise(.03), 2500, 9000) * env_exp(.03, .006) * .8
    w = lp(noise(.35), 900) * env_exp(.35, .09) * .6
    h = np.sin(2 * np.pi * 100 * t_(.6)) * env_exp(.6, .25) * .08
    y = np.zeros(int(.6 * SR)); y[:len(k)] += k; y[:len(w)] += w; y += h; return norm(y, .8 * v)
def lamp_off(v=1):
    k = bp(noise(.04), 1200, 6000) * env_exp(.04, .008)
    y = np.zeros(int(.3 * SR)); y[:len(k)] += k; y[:int(.25 * SR)] += lp(noise(.25), 500) * env_exp(.25, .05) * .4; return norm(y, .7 * v)
def tick(v=1): return norm(bp(noise(.02), 2500, 7000) * env_exp(.02, .003), .6 * v)
def tele(v=1): return norm(bp(noise(.025), 1500, 5000) * env_exp(.025, .004) + .3 * np.sin(2 * np.pi * 900 * t_(.025)) * env_exp(.025, .006), .5 * v)
def shutter(v=1): return norm(lp(noise(.18), 1800) * env_exp(.18, .04) + bp(noise(.18), 300, 900) * env_exp(.18, .07), .6 * v)
def leaf(v=1):        # lacquered doors sliding, then a felt clunk
    d = .4; y = bp(noise(d), 200, 2500) * np.sin(np.linspace(0, np.pi, int(round(d * SR)))) * .5; return norm(y, .5 * v)
def clunk(v=1): return norm(lp(noise(.2), 300) * env_exp(.2, .04) + np.sin(2 * np.pi * 80 * t_(.2)) * env_exp(.2, .05), .8 * v)
for e in EV:
    t, ty, gn, pan = e['t'], e['type'], e.get('gain', 1), e.get('pan', 0)
    if ty == 'ignite': add(fx, lamp_on(gn), t, .9, pan)
    elif ty == 'off': add(fx, lamp_off(gn), t, .8, pan)
    elif ty == 'tick': add(fx, tick(gn), t, .8, .1)
    elif ty == 'step': add(fx, step(gn) * .5, t, .6, R.uniform(-.1, .1))
    elif ty == 'tele': add(fx, tele(gn), t, .7, .1)
    elif ty == 'shutter': add(fx, shutter(gn), t, .7, pan)
    elif ty in ('leaf', 'leafopen'): add(fx, leaf(gn), t, .7, 0)
    elif ty in ('seam', 'clunk'): add(fx, clunk(gn), t, .8, 0)
    elif ty == 'whoosh': add(fx, whoosh(.8, gn), t, .8, 0)
    elif ty == 'blink': add(fx, ding(.25), t, .4, .3)
    elif ty == 'prop':      # a far propeller: low pulsing drone, rising, J-cut before the tower shot
        d = e['t1'] - t; tt = t_(d)
        y = lp(noise(d), 260) * (1 + .6 * np.sin(2 * np.pi * 22 * tt)) * np.interp(tt, [0, d * .3, d * .85, d], [0, .5, 1, 0])
        add(fx, norm(y, .5 * gn), t, 1, np.interp(.0, [0, 1], [.4, -.4]))
# ambience beds
amb = st()
city = lp(brown(DUR + 1), 400) * .06; city = np.stack([city, np.roll(city, 1200)], 1)
amb[:len(city)] += city[:N]
wind = bp(noise(DUR + 1), 300, 1500) * .03
wenv = np.interp(np.arange(len(wind)) / SR, [0, 44, 46, 55, 56, DUR + 1], [.5, .5, 1.6, 1.6, .5, .5])
amb[:len(wind), 0] += wind * wenv; amb[:len(wind), 1] += np.roll(wind, 900) * wenv
# silences: drop music and beds in the hook's first moment and before the reveal
def gate(pts): return np.interp(np.arange(N) / SR, [p[0] for p in pts], [p[1] for p in pts]).astype(np.float32)[:, None]
mg = gate([(0, 1), (42.6, 1), (43.0, .0), (45.4, .0), (45.6, 1), (DUR + 2, 1)])
ag = gate([(0, .2), (.7, 1), (42.8, 1), (43.0, .25), (45.4, .25), (45.6, 1), (DUR - 1, 1), (DUR + .5, 0), (DUR + 2, 0)])

# ================= narration =================
lines = json.load(open(os.path.join(HERE, 'lines.json')))
voice = st()
for e in EV:
    if e['type'] != 'vo': continue
    x, sr = sf.read(os.path.join(HERE, 'voice', e['id'] + '.wav'), dtype='float32')
    if x.ndim > 1: x = x.mean(1)
    if sr != SR: x = soxr.resample(x, sr, SR)
    x = compress(norm(hp(x, 80), .8), thr=.3, ratio=3).astype(np.float32)
    add(voice, x, e['t'], 1, 0)
voice = voice + S.room(voice, size=.3, mix=1.0) * .08
# duck music under the voice (~-9 dB)
venv = np.abs(voice).max(1)
from scipy.ndimage import maximum_filter1d, uniform_filter1d
vk = uniform_filter1d(maximum_filter1d((venv > .02).astype(np.float32), int(.35 * SR)), int(.25 * SR))
duck = (1 - .65 * vk)[:, None]

def rms(x): return float(np.sqrt(np.mean(x ** 2)) + 1e-9)
mus = music * mg * duck
# balance by RMS: voice ≈ 10 dB above the music
vr = rms(voice[np.abs(voice).max(1) > .02]); mr = rms(music[np.abs(music).max(1) > .005])
mus *= (vr / mr) * 10 ** (-10 / 20) * 1.25
mix = voice + mus + fx * .9 * (vr / max(rms(fx[np.abs(fx).max(1) > .01]), 1e-6)) * .35 + amb * ag
mix = mix[:int(DUR * SR)]
mix = limit(mix.astype(np.float32), .95)
os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
sf.write(os.path.join(HERE, 'out/mix.wav'), mix, SR)
sf.write(os.path.join(HERE, 'out/music.wav'), (mus[:int(DUR * SR)]).astype(np.float32), SR)
print('mix', mix.shape[0] / SR, 's · peak', float(np.abs(mix).max()))
