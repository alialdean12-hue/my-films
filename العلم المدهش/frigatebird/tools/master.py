"""Normalise offline mix, copy rendered picture, add off-screen attribution and faststart."""
from pathlib import Path
import json,re,subprocess as sp
p=Path(__file__).resolve().parents[1];o=p/'out';mix=o/'mix.wav';tl=json.loads((p/'timeline.json').read_text());f='loudnorm=I=-14:TP=-1.6:LRA=11';log=sp.run(['ffmpeg','-nostats','-i',str(mix),'-af',f+':print_format=json','-f','null','-'],capture_output=True,text=True,check=True).stderr
q=json.loads(re.findall(r'\{[^{}]*"input_i"[^{}]*\}',log)[-1]);params={'measured_I':'input_i','measured_TP':'input_tp','measured_LRA':'input_lra','measured_thresh':'input_thresh','offset':'target_offset'};flt=f+''.join(f':{k}={q[v]}' for k,v in params.items())+':linear=true,aresample=48000,apad'
sp.run(['ffmpeg','-y','-v','error','-i',str(o/'silent.mp4'),'-i',str(mix),'-map','0:v','-map','1:a','-map_metadata','-1','-c:v','copy','-af',flt,'-c:a','aac','-b:a','192k','-ar','48000','-ac','2','-t',str(tl['duration']),'-metadata','title=قيلولة بلا هبوط','-metadata','comment='+(p/'CREDITS').read_text(),'-metadata:s:a:0','language=ara','-movflags','+faststart',str(p/'frigatebird.mp4')],check=True)
