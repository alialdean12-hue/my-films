"""Deterministic sea, paper Foley and an original brief plucked motif. No wildlife field recordings."""
from pathlib import Path
import json,math,subprocess,sys,wave
import numpy as np
from scipy.signal import butter,sosfilt
P=Path(__file__).resolve().parents[1];KIT=P.parents[1]/'studio-kit';sys.path.insert(0,str(KIT/'scripts'));import sfx_lib as S
sr=48000;ep=json.loads((P/'video.json').read_text());tl=json.loads((P/'timeline.json').read_text());ls=json.loads((P/'lines.json').read_text());D=ep['duration'];F=ep['fps'];N=D*sr;t=np.arange(N)/sr;rng=np.random.default_rng(12468);SD=P/'sfx';SD.mkdir(exist_ok=True);(P/'out').mkdir(exist_ok=True)
def wav(name,a):
 with wave.open(str(SD/name),'wb') as w:
  w.setparams((a.shape[1] if a.ndim>1 else 1,2,sr,0,'NONE','not compressed'));w.writeframes((np.clip(a,-.98,.98)*32767).astype('<i2').tobytes())
def filt(x,low,high):return sosfilt(butter(2,[low,high],btype='band',fs=sr,output='sos'),x)
def bell(f,d):
 tt=np.arange(round(d*sr))/sr;return (np.sin(2*np.pi*f*tt)+.34*np.sin(2*np.pi*f*2*tt)*np.exp(-4.3*tt)+.13*np.sin(2*np.pi*f*3*tt)*np.exp(-6*tt))*np.exp(-3.4*tt)*np.minimum(1,tt/.016)*np.minimum(1,(d-tt)/.1)
bed=np.zeros((N,2),'float32');mask=1-.58*np.exp(-((t-44)/7.1)**4)
for ch in range(2):
 n=filt(rng.normal(0,1,N),65,630+90*ch);bed[:,ch]=n*.20*(.63+.33*np.sin(2*np.pi*(t/8+ch*.1)))*mask
# Wide soft open fifths, moving sparsely, then two bright notes at the reveal.
for base,stop,root in [(0,16,146.83),(16,32.95,130.81),(32.95,39.17,164.81),(39.17,46.08,146.83),(46.08,55.42,174.61),(55.42,60,146.83)]:
 for i in range(math.ceil((stop-base)/.88)):
  if i%8 in (3,6,7):continue
  ti=base+i*.88+.09;f=root*[1,1.5,2,2,1.25,1.5,2,1][i%8];j=round(ti*sr);tone=bell(f,1.36)*(.045 if base<39 or base>=49 else .027);k=min(len(tone),N-j)
  if k>0:bed[j:j+k,:]+=tone[:k,None]*np.array([.85 if i%2 else 1,1 if i%2 else .85])
bed*=np.minimum(1,t/.08)[:,None]*np.minimum(1,(D-t)/.62)[:,None];wav('sea-score.wav',bed)
noise=lambda dur,lo,hi: filt(rng.normal(0,1,round(dur*sr)),lo,hi)
x=noise(.19,380,4100);wav('swish.wav',S.norm(x,.14)*np.sin(np.linspace(0,np.pi,len(x)))**1.3);x=noise(.30,520,4800);env=np.interp(np.arange(len(x)),np.arange(0,len(x)+288,288),rng.uniform(.15,1,len(np.arange(0,len(x)+288,288))));wav('rip.wav',S.norm(x,.18)*env*np.sin(np.linspace(0,np.pi,len(x))))
x=noise(.37,780,3450);wav('pencil.wav',S.norm(x,.11)*(.70+.3*np.sin(np.linspace(0,6*np.pi,len(x))))*np.sin(np.linspace(0,np.pi,len(x))))
wav('tap.wav',.205*S.hit(.115)*np.minimum(1,np.arange(5520)/120));wav('ink-note.wav',bell(523.25,.74)*.085);wav('answer.wav',(bell(523.25,1.2)+.64*bell(659.25,1.2))*.086)
items=[dict(file='sfx/sea-score.wav',at=0,gain=.31)];
for l in ls:items.append(dict(file=l['file'],at=l['startFrame']/F,gain=1.0))
for i,(shot,b) in enumerate(zip(tl['shots'],ep['beats'])):
 st=shot['start']/F
 if i:items.extend([dict(file='sfx/'+('rip.wav' if b['transition']=='tear' else 'swish.wav'),at=max(0,st-.16),gain=.41),dict(file='sfx/tap.wav',at=st+.01,gain=.32)])
 for obj in b['items']:
  if obj['type'] in ('sweep','circle','arrow'):items.append(dict(file='sfx/pencil.wav',at=round(st+obj['at'],3),gain=.35))
 if i in (7,12,14,16):items.append(dict(file='sfx/'+('answer.wav' if i in (14,16) else 'ink-note.wav'),at=round(st+.59,3),gain=.43))
(P/'mix.json').write_text(json.dumps(dict(duration=D,target_lufs=-14,items=items),ensure_ascii=False,indent=2)+'\n')
subprocess.run([sys.executable,str(KIT/'scripts/mix.py'),'mix.json','out/mix.wav'],cwd=P,check=True)
