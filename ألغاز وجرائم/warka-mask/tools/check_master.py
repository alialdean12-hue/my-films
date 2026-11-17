"""Check the exported container, levels and black frames; write 1 actual frame per second as contact sheets."""
import json,re,subprocess as sp
from pathlib import Path
from PIL import Image,ImageDraw
p=Path(__file__).resolve().parents[1]; f=p/'warka-mask.mp4';out=p/'out'; t=json.loads((p/'timeline.json').read_text());d=t['duration'];frames=t['frames']
def data(args):return sp.check_output(args)
probe=json.loads(data(['ffprobe','-v','error','-show_entries','format=duration,size:stream=codec_type,codec_name,width,height,r_frame_rate,nb_frames,channels,sample_rate,duration','-of','json',str(f)]));v=next(x for x in probe['streams'] if x['codec_type']=='video');a=next(x for x in probe['streams'] if x['codec_type']=='audio');assert (v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))==(1080,1920,'24/1',frames);assert v['codec_name']=='h264' and a['codec_name']=='aac' and a['channels']==2 and abs(float(probe['format']['duration'])-d)<=.05
r=sp.run(['ffmpeg','-hide_banner','-nostats','-i',str(f),'-vf','blackdetect=d=0.04:pix_th=0.025:pic_th=0.985','-af','loudnorm=I=-14:TP=-1.2:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True,check=True).stderr
stat=json.loads(re.findall(r'\{[^{}]*"input_i"[^{}]*\}',r)[-1]); blacks=re.findall(r'black_start:[^\n]+',r);assert not blacks,blacks
assert abs(float(stat['input_i'])+14)<.8 and float(stat['input_tp'])<=-1.0,stat
# Read from the encoded file itself: at 24 fps select frames 8, 32, 56, …
w,h=153,272;fpsf="select='eq(mod(n,24),8)',scale=153:272:flags=lanczos,format=rgb24";raw=data(['ffmpeg','-v','error','-i',str(f),'-an','-vf',fpsf,'-fps_mode','passthrough','-f','rawvideo','-pix_fmt','rgb24','pipe:1']);n=len(raw)//(w*h*3);assert n==int(d)
for start in range(0,n,20):
 sheet=Image.new('RGB',((w+6)*5,(h+22)*4),'#53534e');pen=ImageDraw.Draw(sheet)
 for i in range(start,min(n,start+20)):
  tmp=Image.frombytes('RGB',(w,h),raw[i*w*h*3:(i+1)*w*h*3]);j=i-start;x=(j%5)*(w+6);y=(j//5)*(h+22);sheet.paste(tmp,(x,y));pen.text((x+4,y+h+2),f'{i+8/24:.2f} s',fill='#fffbef')
 sheet.save(out/f'final-sheet-{start//20+1}.jpg',quality=91)
q=dict(container=probe,lufs=float(stat['input_i']),true_peak_dbtp=float(stat['input_tp']),lra_lu=float(stat['input_lra']),black_intervals=blacks,review_frames=n);(out/'master-check.json').write_text(json.dumps(q,indent=2)+'\n');print(json.dumps(q))
