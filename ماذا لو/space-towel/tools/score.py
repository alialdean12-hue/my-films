"""Original stereo chamber score & foley for the actual exposure sheet. The kit's Karplus–Strong
pluck and inharmonic bells are revoiced in D pentatonic. No stock clips, music models or samples.
"""
from pathlib import Path
import json,math,wave
import numpy as np
P=Path(__file__).resolve().parents[1];OUT=P/'out';OUT.mkdir(exist_ok=True);rng=np.random.default_rng(240413);SR=48000;D=60;N=SR*D
music=np.zeros((N,2),'float32'); foley=np.zeros_like(music);timeline=json.loads((P/'timeline.json').read_text());F=1/24
T={x['key']:x['start']*F for x in timeline['shots']}; q=lambda n:440*2**((n-69)/12)

def add(track,data,sec,gain,pan=0,echo=False):
    start=round(sec*SR); n=min(len(data),N-start); assert start>=0
    if n<=0:return
    sig=np.asarray(data[:n],dtype='float32')*gain
    l=math.cos((pan+1)*math.pi/4);r=math.sin((pan+1)*math.pi/4)
    track[start:start+n,0]+=sig*l;track[start:start+n,1]+=sig*r
    if echo:
        for dt,amp,pp in [(.119,.16,-pan*.8),(.238,.079,-pan),(.362,.035,pan)]:add(track,data,sec+dt,gain*amp,pp)

def pluck(f,dur=1.45):
    # Decaying string with position-dependent excitation, plus a soft fundamental (wooden soundboard).
    count=int(SR/f); buf=rng.uniform(-1,1,count);buf=(buf+np.roll(buf,1)+np.roll(buf,2))*.33; ns=int(SR*dur);v=np.empty(ns);dd=.997 if f<260 else .993
    j=0
    for ix in range(ns):
        y=buf[j];nj=(j+1)%count;v[ix]=y;buf[j]=dd*(.5*y+.5*buf[nj]);j=nj
    t=np.arange(ns)/SR;return (v*.66+np.sin(2*np.pi*f*t)*np.exp(-4*t)*.30)*np.minimum(1,t/.005)*np.minimum(1,(dur-t)/.09)

def mallet(f,d=1.7,metal=False):
    t=np.arange(int(SR*d))/SR
    return (np.sin(2*np.pi*f*t)*np.exp(-2.9*t)+(.26 if metal else .15)*np.sin(2*np.pi*f*(2.76 if metal else 2)*t)*np.exp(-6*t)+.1*np.sin(2*np.pi*f*3.98*t)*np.exp(-10*t))*np.minimum(1,t/.008)*np.minimum(1,(d-t)/.13)

def bednotes(start,end,notes,level):
    t=np.arange(round((end-start)*SR))/SR;env=(1-np.exp(-t/.42))*np.minimum(1,(end-start-t)/.48);y=0
    for j,n in enumerate(notes):
        f=q(n);p=2*np.pi*f*t+.09*np.sin(2*np.pi*(.37+j*.13)*t);v=(np.sin(p)+.20*np.sin(2*p+.6)+.07*np.sin(3*p+.1))*(.72+.12*np.sin(2*np.pi*.21*t+j));add(music,v*env,start,level/(j+1)**.4,(-.51,.35,.1)[j%3])

for seg in [(0,6.3,[50,57,65],.13),(6.1,12.6,[48,55,62],.125),(12.2,18.6,[53,60,67],.125),(18.15,24.55,[50,57,62],.13),(24.15,29.36,[45,52,62],.12),(30.45,33.99,[45,57,64],.153),(33.7,40.05,[53,60,69],.135),(39.8,46.42,[48,55,62],.145),(46.14,52.95,[43,55,62],.13),(52.55,56.7,[45,57,65],.125),(56.3,59.99,[50,57,62],.108)]:bednotes(*seg)
# Score in short call/answer phrases rather than a continuous repeated stock loop.
phrases=[(0.10,[62,69,67,74],[0,.51,1.1,1.88]),(3.48,[65,62,57],[0,.71,1.54]),(6.70,[60,67,74,72],[0,.48,1.30,1.99]),(9.55,[69,67,65],[0,.65,1.8]),(12.52,[65,69,72,69,67],[0,.36,.76,1.50,2.05]),(15.43,[62,57,65],[0,.93,1.84]),(18.55,[57,62,67,69],[0,.60,1.27,2.06]),(21.5,[69,65,62],[0,.82,1.64]),(24.5,[62,60,57],[0,.57,1.54]),(27.5,[55,50],[0,.9]),(30.32,[45,50],[0,.54]),(34.25,[74,69,65],[0,.72,1.5]),(37.05,[67,74,77],[0,.62,1.64]),(40.04,[62,69,67,74],[0,.45,1.03,1.85]),(43.34,[65,67,69],[0,.81,1.75]),(46.68,[67,62],[0,1.18]),(49.66,[55,62,67,69],[0,.55,1.31,2.22]),(53.0,[57,65,62],[0,.6,1.5]),(56.30,[69,65],[0,.36]),(59.40,[62],[0])]
cache={}
for group,(start,notes,ds) in enumerate(phrases):
    for idx,(n,dt) in enumerate(zip(notes,ds)):
        if n not in cache:cache[n]=pluck(q(n))
        add(music,cache[n],start+dt,.48 if idx==0 else .32,(-.34,.23,-.08,.39)[(idx+group)%4],True)
    if 6<start<27 or 33<start<56:add(music,mallet(q(notes[0]-12),1.1),start+.04,.13,-.1)
for dt,n in zip([1.06,1.28,1.5,1.80],[69,74,77,81]):add(music,mallet(q(n),1.7,True),T['wring']+dt,.19 if dt<1.5 else .13,.1+dt*.2,True)

def noise(d):return rng.normal(0,1,int(d*SR))
def texture(d,f=2000):
    t=np.arange(int(d*SR))/SR;x=noise(d);width=max(3,int(SR/f));low=np.convolve(x,np.ones(width)/width,'same');return low*np.sin(np.pi*t/d)**2

def drip(d=.30,base=700):
    t=np.arange(int(d*SR))/SR;phase=2*np.pi*(base*t+270*(1-np.exp(-26*t))/26);return np.sin(phase)*np.exp(-18*t)*np.minimum(1,t/.006)
for i,s in enumerate(timeline['shots'][1:]):
    cut=s['start']*F;add(foley,texture(.25,1700),cut-.155,.065,.30*(-1)**i);add(foley,mallet(q(43 if i%2 else 50),.43),cut,.045)
for st in [.84,1.83,2.76]:add(foley,drip(.39,690),T['sink']+st,.29,.13,True)
for st in [.30,.76,1.34,1.94]:add(foley,texture(.19,4200),T['notebook']+st,.135,-.28)
for st in [T['puck']+.95,T['open']+.84,T['open']+1.85,T['pouch']+.81]:add(foley,texture(.35,6000),st,.21,.10)
for st in [T['pouch']+1.88,T['soak']+.54,T['soak']+1.78,T['fingers']+1.00,T['letgo']+.88,T['cohesion']+1.78]:add(foley,drip(.28,480),st,.22,.3,True)
add(foley,texture(.58,5400),T['wring']+.96,.6,-.20);add(foley,drip(.36,520),T['wring']+1.42,.36,-.1,True)
for t0,note in [(T['few']+.5,78),(T['few']+1.55,74)]:add(foley,mallet(q(note),.85,True),t0,.16,.4,True)
t=np.arange(N)/SR; v=timeline['voiceAt'];du=timeline['voiceDuration'];dampen=np.interp(t,[0,v-.47,v-.05,v+du-.03,v+du+.37,60],[1,1,.17,.17,.72,.72]);tail=np.clip((60-t)/.32,0,1);music*=((dampen*tail)[:,None]);foley*=tail[:,None]

def wav(file,data,target):
    data=data*(target/max(1e-8,np.max(np.abs(data))));
    with wave.open(str(file),'wb') as w:w.setparams((2,2,SR,0,'NONE','not compressed'));w.writeframes(np.round(data*32767).astype('<i2').tobytes())
wav(OUT/'score.wav',music,.86);wav(OUT/'foley.wav',foley,.82)
config={'duration':60,'target_lufs':-14,'items':[{'file':'out/score.wav','at':0,'gain':.42},{'file':'out/foley.wav','at':0,'gain':.37},{'file':'voice/l1.flac','at':v,'gain':1.0}]};(P/'mix.json').write_text(json.dumps(config,indent=2)+'\n')
