"""Offline recognition of the actual sole spoken line from both the stem and the end of the *encoded* film.
Pass a local CTranslate2 multilingual Whisper model directory as argv[1]. No scripted prompt is used.
"""
from pathlib import Path
import json,re,subprocess as sp,sys
import numpy as np
from difflib import SequenceMatcher
from faster_whisper import WhisperModel
p=Path(__file__).resolve().parents[1];t=json.loads((p/'timeline.json').read_text());m=WhisperModel(sys.argv[1],local_files_only=True,device='cpu',compute_type='int8',cpu_threads=2);expected=json.loads((p/'lines.json').read_text())[0]['text']
def norm(s):return ''.join(c for c in s.translate(str.maketrans('أإآىة','ااايه')) if '\u0621'<=c<='\u064a' and c!='ـ')
def words(file,at=0):
 raw=sp.check_output(['ffmpeg','-v','error','-ss',str(at),'-i',str(file),'-vn','-ac','1','-ar','16000','-f','f32le','pipe:1']);audio=np.frombuffer(raw,np.float32).copy();seg,_=m.transcribe(audio,language='ar',word_timestamps=True,beam_size=5,condition_on_previous_text=False);return [dict(word=w.word.strip(),start=round(at+float(w.start),3),end=round(at+float(w.end),3)) for s in seg for w in s.words]
r={}
for id,file,at in [('stem',p/'voice/l1.flac',0),('encodedFinalShot',p/'space-towel.mp4',t['shots'][-1]['start']/24)]:
 a=words(file,at);txt=' '.join(x['word'] for x in a);r[id]=dict(text=txt,words=a,similarity=round(SequenceMatcher(None,norm(expected),norm(txt)).ratio(),3));print(id,txt,r[id]['similarity']);
 if id=='stem':(p/'voice/words.json').write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n')
r['spokenLines']=1;r['expected']=expected;r['scope']='sole final spoken line; earlier shots contain music/foley and visual story captions, not dialogue';(p/'qa/asr.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');assert min(r['stem']['similarity'],r['encodedFinalShot']['similarity'])>=.90
