"""Human-written captions: split the recorded script at its recognised phrase boundaries."""
from pathlib import Path
import json,textwrap
p=Path(__file__).resolve().parents[1];ls=json.loads((p/'lines.json').read_text());words=json.loads((p/'voice/words.json').read_text());splits=[[(0,0),(7,7)],[(0,0),(8,9)],[(0,0),(3,3),(6,6)],[(0,0),(6,6),(9,9)],[(0,0),(3,3),(8,8)],[(0,0),(3,3)],[(0,0),(3,3),(8,8)],[(0,0),(3,3)]]
def ts(t):
 n=round(t*1000);return f'{n//3600000:02d}:{n//60000%60:02d}:{n//1000%60:02d},{n%1000:03d}'
cues=[]
for l,spl in zip(ls,splits):
 ww=words[l['id']];v=l['text'].split();at=l['startFrame']/24;dur=l['samples']/l['sampleRate'];sp=spl+[(len(v),None)];texts=[]
 for (a,ia),(b,ib) in zip(sp,sp[1:]):
  s=at+ww[ia]['s'];e=at+(ww[ib]['s'] if ib is not None else dur);text=' '.join(v[a:b]);texts.append(text);chunks=textwrap.wrap(text,width=40,break_long_words=False);cues.append(f'{len(cues)+1}\n{ts(s)} --> {ts(e)}\n'+'\n'.join(chunks));assert .55<e-s<6.5
 assert ' '.join(texts)==l['text']
(p/'frigatebird.srt').write_text('\n\n'.join(cues)+'\n')
