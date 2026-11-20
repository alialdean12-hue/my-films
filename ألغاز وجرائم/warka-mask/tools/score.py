"""Original chamber-pulse bed and Foley. Run in film root. Requires numpy and ffmpeg.
Voice timing is read from the delivered, trimmed FLAC stems, never estimated from word count.
"""
import sys,json,wave,subprocess,math
from pathlib import Path
import numpy as np
p=Path(__file__).resolve().parents[1];kit=p.parents[1]/'studio-kit'/'scripts';sys.path.insert(0,str(kit));import sfx_lib as fx
SR=48000;dur=json.loads((p/'timeline.json').read_text())['duration'];cuts=json.loads((p/'cuts.json').read_text());N=round(dur*SR);(p/'sfx').mkdir(exist_ok=True);rng=np.random.default_rng(398)
def dump(f,a):fx.save(str(p/'sfx'/f),np.asarray(a))
def place(dst,when,x,gain=1):
 j=round(when*SR); n=min(len(dst)-j,len(x));
 if n>0:dst[j:j+n]+=x[:n]*gain
bed=np.zeros(N);beat=60/96
# A plucked low D, answering fifth, and sparse alternating upper figures rather than a constant loop.
for i in range(int(dur/beat)):
 t=i*beat
 if 46.4<=t<48.95:continue
 bass=[73.42,73.42,65.41,55,73.42,77.78,65.41,55][(i//8)%8];
 if t>49:bass=[73.42,87.31,98,73.42][(i//8)%4]
 if i%2==0:
  f=bass*(1 if i%4==0 else 1.5);u=np.arange(round(.83*SR))/SR
  pl=(np.sin(2*np.pi*f*u)+.31*np.sin(4*np.pi*f*u)+.11*np.sin(6*np.pi*f*u))*np.minimum(1,u/.008)*np.exp(-u*7.3)
  place(bed,t,pl,.22 if i%4==0 else .115)
 if i%8 in (1,3,6) or t>49 and i%2==1:
  f=bass*[4,6,5.34,4,6,7.12,4.75,5.34][i%8];u=np.arange(round(.8*SR))/SR
  note=(np.sin(2*np.pi*f*u+.2*np.sin(2*np.pi*2*f*u))+np.sin(2*np.pi*f*1.002*u)*.35)*np.minimum(1,u/.006)*np.exp(-u*8.5)
  place(bed,t+.075,note,.115 if t<49 else .15)
 if i%8==0:
  u=np.arange(round(beat*8*SR))/SR
  # A restrained bowed harmonic, fades smoothly between phrases.
  swell=np.sin(np.pi*u/(beat*8))**1.5
  place(bed,t,(np.sin(2*np.pi*2*bass*u)+.34*np.sin(2*np.pi*(2*bass+.8)*u)+.14*np.sin(2*np.pi*6*bass*u))*swell,.063)
t=np.arange(N)/SR;duck=np.clip((46.8-t)/.56,0,1)+np.clip((t-48.95)/.56,0,1);bed*=np.minimum(1,duck);bed*=np.clip(t/.3,0,1)*np.clip((dur-t)/.8,0,1)
dump('score.wav',bed/np.max(np.abs(bed))*.36)
# Short, papery transitions; low hits and fine nib sounds are intentionally quieter than the spoken syllables.
u=np.arange(int(.23*SR))/SR; ws=(rng.uniform(-1,1,len(u))-rng.uniform(-.18,.18,len(u)))*np.sin(np.pi*u/.23)**3
ws=np.convolve(ws,np.ones(13)/13,'same');dump('turn.wav',fx.norm(ws,.16));dump('ink.wav',fx.hit(.21)*.21);dump('ring.wav',fx.bell(622.25,.8)*.26)
u=np.arange(int(.1*SR))/SR;tap=(np.sin(2*np.pi*870*u)+.2*np.sin(2*np.pi*1260*u))*np.exp(-70*u);dump('tick.wav',fx.norm(tap,.12))
items=[dict(file=x['file'],at=x['at'],gain=1.0) for x in json.loads((p/'lines.json').read_text())];items.append(dict(file='sfx/score.wav',at=0,gain=.30));
for i,s in enumerate(cuts):
 t=s['start'];
 if i:items.append(dict(file='sfx/turn.wav',at=round(t-.155,3),gain=.38 if i%3 else .46))
 items.append(dict(file='sfx/ink.wav',at=t,gain=.38 if i%2 else .48));
 if i in (1,3,5,7,10,12,14,15):items.append(dict(file='sfx/tick.wav',at=round(t+.66,3),gain=.35))
 if i in (4,16,19):items.append(dict(file='sfx/ring.wav',at=round(t+.25,3),gain=.39))
(p/'mix.json').write_text(json.dumps(dict(duration=dur,target_lufs=-14,items=items),ensure_ascii=False,indent=2)+'\n')
