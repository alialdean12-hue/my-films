"""Two-pass loudness, AAC + stream copy. Embed attribution off screen in the actual movie."""
import json,re,subprocess as sp
from pathlib import Path
p=Path(__file__).resolve().parents[1];out=p/'out';d=json.loads((p/'timeline.json').read_text())['duration'];audio=out/'mix.wav'
base='loudnorm=I=-14:TP=-1.5:LRA=11'
probe=sp.run(['ffmpeg','-nostats','-i',str(audio),'-af',base+':print_format=json','-f','null','-'],capture_output=True,text=True,check=True).stderr
q=json.loads(re.findall(r'\{[^{}]*"input_i"[^{}]*\}',probe)[-1]);keys={'measured_I':'input_i','measured_LRA':'input_lra','measured_TP':'input_tp','measured_thresh':'input_thresh','offset':'target_offset'}
f=base+''.join(f':{k}={q[v]}' for k,v in keys.items())+':linear=true,aresample=48000,apad'
credit=(p/'CREDITS').read_text()  # Fail closed if attribution is missing.
sp.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(out/'silent.mp4'),'-i',str(audio),'-map','0:v:0','-map','1:a:0','-map_metadata','-1','-af',f,'-c:v','copy','-c:a','aac','-b:a','192k','-ac','2','-ar','48000','-t',str(d),'-metadata','title=قناع الوركاء: وجه خرج من التراب مرتين','-metadata','comment='+credit,'-movflags','+faststart',str(p/'warka-mask.mp4')],check=True)
