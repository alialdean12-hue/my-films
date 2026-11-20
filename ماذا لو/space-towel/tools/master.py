"""Two independent passes of EBU R128 and a stream-copy mux. The art and music are original."""
import json,re,subprocess as sp
from pathlib import Path
p=Path(__file__).resolve().parents[1]; out=p/'out';mix=out/'mix.wav';D=json.loads((p/'timeline.json').read_text())['duration'];tag=(p/'CREDITS').read_text();base='loudnorm=I=-14:TP=-1.55:LRA=11'
log=sp.run(['ffmpeg','-nostats','-i',str(mix),'-af',base+':print_format=json','-f','null','-'],capture_output=True,text=True,check=True).stderr
q=json.loads(re.findall(r'\{[^{}]*"input_i"[^{}]*\}',log)[-1]);kk={'measured_I':'input_i','measured_LRA':'input_lra','measured_TP':'input_tp','measured_thresh':'input_thresh','offset':'target_offset'};f=base+''.join(f':{k}={q[v]}' for k,v in kk.items())+':linear=true,aresample=48000,apad'
sp.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(out/'silent.mp4'),'-i',str(mix),'-map','0:v:0','-map','1:a:0','-map_metadata','-1','-af',f,'-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-ac','2','-t',str(D),'-metadata','title=منشفة في المدار — تجربة كريس هادفيلد','-metadata','comment='+tag,'-metadata:s:a:0','language=ara','-movflags','+faststart',str(p/'space-towel.mp4')],check=True)
