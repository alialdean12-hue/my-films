"""Subtitle cues for the .srt, with the same timing as the burned-in cards (main.js: VO starts, voice length + 0.6 s, at least 1.8 s, no overlap)."""
import os, json
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
lines = json.load(open(os.path.join(HERE, 'lines.json'))); dur = json.load(open(os.path.join(HERE, 'voice/dur.json')))
VO = {e['id']: e['t'] for e in json.load(open(os.path.join(HERE, 'events.json')))['ev'] if e['type'] == 'vo'}
cues = [{'t0': VO[L['id']], 't1': max(VO[L['id']] + 1.8, VO[L['id']] + dur[L['id']] + .6), 'text': L['text'].replace('...', '…')} for L in lines]
for a, b in zip(cues, cues[1:]): a['t1'] = min(a['t1'], b['t0'] - .35)
os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
json.dump(cues, open(os.path.join(HERE, 'out/cues.json'), 'w'), ensure_ascii=False, indent=1)
print(len(cues), 'cues')
