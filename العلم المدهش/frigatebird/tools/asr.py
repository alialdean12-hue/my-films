"""Unprompted local ASR, one window per spoken beat, extracted from the *final encoded* AAC."""
from pathlib import Path
from difflib import SequenceMatcher
import json,re,subprocess as sp,sys
import numpy as np
from faster_whisper import WhisperModel
p=Path(__file__).resolve().parents[1];ls=json.loads((p/'lines.json').read_text());f=p/'frigatebird.mp4';m=WhisperModel(sys.argv[1],device='cpu',compute_type='int8',cpu_threads=2,local_files_only=True)
def norm(s):
 s=re.sub(r'(?<!\d)40(?!\d)','أربعين',s)
 return ''.join(c for c in s.translate(str.maketrans('أإآىة','ااايه')) if '\u0621'<=c<='\u064a' and c!='ـ')
r=[]
for line in ls:
 t=line['startFrame']/24;d=line['samples']/line['sampleRate'];pcm=sp.check_output(['ffmpeg','-v','error','-ss',str(t),'-i',str(f),'-t',str(d+.025),'-vn','-ac','1','-ar','16000','-f','f32le','pipe:1']);s,_=m.transcribe(np.frombuffer(pcm,np.float32).copy(),language='ar',beam_size=5,condition_on_previous_text=False,word_timestamps=True);ws=[dict(w=x.word.strip(),s=round(t+x.start,2),e=round(t+x.end,2)) for ss in s for x in ss.words];txt=' '.join(x['w'] for x in ws);score=round(SequenceMatcher(None,norm(line['text']),norm(txt)).ratio(),3);r.append(dict(id=line['id'],reference=line['text'],recognized=txt,similarity=score,words=ws));print(line['id'],score,txt,flush=True)
(p/'qa/final-asr.json').write_text(json.dumps(dict(source='final AAC, per beat, small INT8, ar, no prompt',beats=r),ensure_ascii=False,indent=2)+'\n');assert all(x['words'] and x['similarity']>=.86 for x in r)
