"""Score (tense documentary pulse) + hits/whooshes on every cut + narration → out/mix.wav"""
import os, sys, json, numpy as np, soundfile as sf, soxr
HERE = os.path.dirname(os.path.abspath(__file__)); LIB = os.environ.get('LIB', '/root/lemo-opuscar'); sys.path.insert(0, LIB)
from core.audio.sfx import SR, bp, lp, hp, noise, norm, t_, env_exp, whoosh, thump, add, limit, compress
from core.audio import sampler as S
E = json.load(open(os.path.join(HERE, 'events.json'))); EV = E['ev']; DUR = E['dur']; N = int((DUR + 1) * SR)
S.seed(11); BT = 60 / 100
def st(): return np.zeros((N, 2), np.float32)
ev = []
# pulse: pizz bass + cello 8ths (D minor → Bb → Gm → A), stops for the turn at 17.9, returns bigger
prog = [('D2', 'D3'), ('Bb1', 'Bb2'), ('G1', 'G2'), ('A1', 'A2')]
t = 0.0; i = 0
while t < DUR - 2:
    bar = int(t / (BT * 4)) % 4; lo, hi = prog[bar]
    if not (16.9 < t < 17.9):
        ev.append((t, 'contrabass_pizz', lo, BT, .55 if i % 2 == 0 else .4, -.1, .9))
        ev.append((t, 'cellos_spic', hi, BT * .5, .35, .15, .6))
    t += BT / 2; i += 1
for k, (a, b) in enumerate([(0, 7.3), (7.3, 13.0), (13.0, 17.4)]):
    for p in (['D4', 'F4', 'A4'], ['Bb3', 'D4', 'F4'], ['G3', 'Bb3', 'D4'])[k]: ev.append((a, 'violins_trem', p, b - a, .25 + k * .05, .2, .5))
# the turn: piano motif, then full strings for "the most famous painting"
for o, p in [(0, 'A4'), (.6, 'D5'), (1.2, 'F5'), (1.8, 'E5'), (2.4, 'D5')]: ev.append((17.9 + o, 'piano', p, .9, .5, .1, .9))
for p in ['F3', 'A3', 'C4', 'F4', 'A4', 'C5']: ev.append((20.5, 'violins' if p > 'C4' else 'cellos', p, 2.0, .45, .1, .6))
ev.append((20.5, 'timpani', None, None, .5, 0, .7))
for p in ['D3', 'A3', 'D4', 'F4']: ev.append((22.5, 'cellos' if p < 'D4' else 'violins', p, 4, .32, 0, .6))
ev.append((24.0, 'piano', 'D6', 2.5, .4, .2, .8)); ev.append((24.0, 'glockenspiel', 'A6', 2, .35, .2, .5))
music = st()
for e in ev:
    try: x = S.note(e[1], e[2], e[3], vel=e[4]) if e[2] is not None else S.hit(e[1], None, e[4])
    except Exception as ex: print('skip', e[1], ex); continue
    add(music, x.astype(np.float32), e[0], e[6], e[5])
music = music * .75 + S.room(music, size=.5, mix=1.0) * .25
fx = st()
def pop(): return norm(bp(noise(.06), 1500, 7000) * env_exp(.06, .012), .5)
def flick(): return norm(hp(noise(.15), 2500) * env_exp(.15, .03), .5)
def scratch(): d = .25; return norm(bp(noise(d), 800, 4000) * np.interp(t_(d), [0, .05, d], [0, 1, 0]), .6)
def tick(): return norm(bp(noise(.02), 2500, 7000) * env_exp(.02, .004), .6)
for e in EV:
    ty = e['type']
    if ty == 'whoosh': add(fx, whoosh(.3, .8), e['t'], .7, 0)
    elif ty == 'hit': add(fx, thump(1, 55) * .9 + norm(lp(noise(.3), 400) * env_exp(.3, .08), .5)[:len(thump(1, 55))] if False else thump(1, 55), e['t'], 1, 0)
    elif ty == 'pop': add(fx, pop(), e['t'], .6, 0)
    elif ty == 'card': add(fx, flick(), e['t'], .7, .1)
    elif ty == 'thud': add(fx, thump(1, 80), e['t'], 1, 0)
    elif ty == 'scratch': add(fx, scratch(), e['t'], .8, 0)
    elif ty == 'tick': add(fx, tick(), e['t'], .8, 0)
voice = st()
for e in EV:
    if e['type'] != 'vo': continue
    x, sr = sf.read(os.path.join(HERE, 'voice', e['id'] + '.wav'), dtype='float32')
    if x.ndim > 1: x = x.mean(1)
    x = compress(norm(hp(soxr.resample(x, sr, SR), 80), .8), thr=.3, ratio=3).astype(np.float32); add(voice, x, e['t'], 1, 0)
from scipy.ndimage import maximum_filter1d, uniform_filter1d
vk = uniform_filter1d(maximum_filter1d((np.abs(voice).max(1) > .02).astype(np.float32), int(.3 * SR)), int(.2 * SR))
def rms(x): return float(np.sqrt(np.mean(x ** 2)) + 1e-9)
vr = rms(voice[np.abs(voice).max(1) > .02]); mr = rms(music[np.abs(music).max(1) > .005]); fr = rms(fx[np.abs(fx).max(1) > .01])
mix = voice + music * (1 - .55 * vk)[:, None] * (vr / mr) * 10 ** (-9 / 20) + fx * (vr / fr) * .3
mix = limit(mix[:int(DUR * SR)].astype(np.float32), .95)
os.makedirs(os.path.join(HERE, 'out'), exist_ok=True); sf.write(os.path.join(HERE, 'out/mix.wav'), mix, SR); print('ok', len(mix) / SR)
