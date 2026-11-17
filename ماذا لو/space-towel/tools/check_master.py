"""Checks the exported bytes: streams + R128 + actual decoded samples, exposure sheet, palette and SRT."""
import hashlib,io,json,re,subprocess as sp
from pathlib import Path
from PIL import Image,ImageDraw,ImageChops,ImageStat
from paint import COLORS
p=Path(__file__).resolve().parents[1];f=p/'space-towel.mp4';out=p/'out';qa=p/'qa';qa.mkdir(exist_ok=True);sheet=json.loads((p/'timeline.json').read_text());nframe=int(sheet['duration']*sheet['fps']);layout=json.loads((out/'layout.json').read_text())
def data(args):return sp.check_output(args)
probe=json.loads(data(['ffprobe','-v','error','-show_entries','format=duration,size:format_tags=title,comment:stream=codec_type,codec_name,width,height,r_frame_rate,nb_frames,channels,sample_rate,duration','-of','json',str(f)]));assert probe['format']['tags'].pop('comment')==(p/'CREDITS').read_text();v,a=probe['streams'];assert (v['codec_name'],v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))==('h264',1080,1920,'24/1',1440);assert(a['codec_name'],a['channels'],a['sample_rate'])==('aac',2,'48000');assert all(abs(float(x['duration'])-60)<.001 for x in [v,a,probe['format']]);log=sp.run(['ffmpeg','-hide_banner','-nostats','-i',str(f),'-vf','blackdetect=d=0.04:pix_th=0.025:pic_th=0.985','-af','loudnorm=I=-14:TP=-1.2:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True,check=True).stderr
lev=json.loads(re.findall(r'\{[^{}]*"input_i"[^{}]*\}',log)[-1]);blacks=re.findall(r'black_start:[^\n]+',log);assert not blacks,blacks; assert abs(float(lev['input_i'])+14)<.7 and float(lev['input_tp'])<=-1.0,lev
w,h,off=153,272,14;raw=data(['ffmpeg','-v','error','-i',str(f),'-an','-vf',f"select='eq(mod(n,24),{off})',scale={w}:{h}:flags=lanczos,format=rgb24",'-fps_mode','passthrough','-f','rawvideo','-pix_fmt','rgb24','pipe:1']);bf=w*h*3; assert len(raw)==60*bf
imgs=[Image.frombytes('RGB',(w,h),raw[i*bf:(i+1)*bf]) for i in range(60)];means=[round(sum(ImageStat.Stat(ImageChops.difference(x,y)).mean)/3,2) for x,y in zip(imgs,imgs[1:])]
for ix in range(3):
 im=Image.new('RGB',((w+6)*5,(h+20)*4),(44,49,61));d=ImageDraw.Draw(im)
 for j in range(20):
  x=j%5*(w+6);y=j//5*(h+20);im.paste(imgs[ix*20+j],(x,y));d.text((x+4,y+h+2),f'{ix*20+j+off/24:.2f} s',fill='white')
 im.save(qa/f'encoded-{ix+1}.jpg',quality=91)
# Check the actual source palette, not anti-aliased H.264 samples or intentionally interpolated colour dips.
page=(p/'index.html').read_text();palette=sorted(set(re.findall(r'#[\da-fA-F]{6}\b',page)));assert set(palette)==set(COLORS);plates={}
for file in (p/'img').glob('*.png'):
 im=Image.open(file);assert im.mode=='P';table=im.getpalette();cols={tuple(table[3*idx:3*idx+3]) for _,idx in im.getcolors() if idx!=im.info.get('transparency')};actual={'#%02x%02x%02x'%c for c in cols};assert actual<=set(COLORS);plates[file.name]=len(actual)
sak=[s['key'] for s in sheet['shots'] if s['mode']=='sakuga'];assert sak==['wring'];assert all(48<=s['end']-s['start']<=96 and (s['drawings']==(8 if s['key']=='wring' else 3)) and all(x[1]%2==0 for x in s['keys']) and s['end']-s['start']-s['keys'][-1][1]>=12 for s in sheet['shots']);assert not layout['bad'] and not layout['externalMedia'];assert layout['minimumContrast']>=4.5
srt=(p/'space-towel.srt').read_text().strip().split('\n\n');assert len(srt)==19
stamps=lambda t:int(t[0:2])*3600000+int(t[3:5])*60000+int(t[6:8])*1000+int(t[9:12]);prev=0
for i,c in enumerate(srt):
 num,tm,*txt=c.splitlines();a1,b1=map(stamps,tm.split(' --> '));assert int(num)==i+1 and txt and prev<=a1<b1<=60000;prev=b1
fb=f.read_bytes();checks={'container':probe,'md5':hashlib.md5(fb).hexdigest(),'sha256':hashlib.sha256(fb).hexdigest(),'lufs':float(lev['input_i']),'truePeak_dBTP':float(lev['input_tp']),'lra_LU':float(lev['input_lra']),'black_intervals':blacks,'duration_seconds':60,'shots':len(sheet['shots']),'painted_cels':sum(s['drawings'] for s in sheet['shots']),'source_palette':palette,'plate_colours':plates,'sakuga':sak,'captions_measured':len(layout['measured']),'caption_ink_limits':[min(x['ext'][0] for x in layout['measured']),min(x['ext'][1] for x in layout['measured']),max(x['ext'][2] for x in layout['measured']),max(x['ext'][3] for x in layout['measured'])],'minimum_contrast':layout['minimumContrast'],'srt_cues':len(srt),'decoded_review_frames':len(imgs),'decoded_frame_offset':off,'sequential_mean_abs_pixel_difference':means};(qa/'checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in checks.items() if k not in ['sequential_mean_abs_pixel_difference','source_palette','plate_colours']},ensure_ascii=False));print('identical adjacent integer-second samples:',[i for i,x in enumerate(means) if x<.02]);
