"""60 s extension of the studio's html-anime template and its frame-boundary swap()/dip grammar.
Only the first camera moves. All normal shots have three replacement cels; only the wring has eight.
"""
import html,json,math,subprocess
from pathlib import Path
from layouts import SHOTS,backdrop,pose,fx
from paint import COLORS,INK,IVORY,ICE,AQUA,SLATE,GOLD
P=Path(__file__).resolve().parents[1]; FPS=24;TOTAL=1440

def dump(f,x):(P/f).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def clock(t):
    n=round(t*1000);return f'{n//3600000:02d}:{n//60000%60:02d}:{n//1000%60:02d},{n%1000:03d}'

def main():
    d=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(P/'voice/l1.flac')],text=True));dump('voice/durations.json',{'l1':d}); voice=json.loads((P/'lines.json').read_text())[0]['text'];button=TOTAL-2*math.ceil((d+5/6+.5)*12);va=(button+20)/FPS
    cuts=[round(a*FPS) for _,a,*_ in SHOTS[:-1]]+[button,TOTAL]; scenes=[];drawings=[];srt=[];sheet=[]
    for i,(n,_,words,desc,sound) in enumerate(SHOTS):
        s,e=cuts[i:i+2];length=e-s;assert 48<=length<=96 and s%2==0
        times=([0,14,22,26,30,34,40,48] if n=='wring' else [0,22,44]); count=len(times)
        # A blink uses the existing open cel again before the third acting key. All swaps land on twos.
        order=list(enumerate(times));
        if n in ('chris','hook','wait','button','most','letgo','puck'):order.insert(2,(0,26))
        assert all(frame%2==0 for _,frame in order) and length-order[-1][1]>=12
        tex=''.join('<span class="'+('last' if j==len(words)-1 else 'first')+'">'+html.escape(w)+'</span>' for j,w in enumerate(words));tag=f's{i+1}';effect,mark=fx(n)
        dr=''.join(f'<g class="draw {"initial" if k==0 else ""}" id="{tag}d{k}">{pose(n,k)}</g>' for k in range(count));motion=(f'<g id="{tag}fx">{mark}</g>' if effect else '')
        if n=='sink': motion+='<g id="ripple"><ellipse cx="289" cy="535" rx="51" ry="10" fill="none" stroke="'+ICE+'" stroke-width="3"/><ellipse cx="289" cy="535" rx="23" ry="5" fill="none" stroke="'+SLATE+'" stroke-width="2"/></g>'
        drawings.append(f'<div class="clip shot" id="{tag}" data-start="{s/FPS:.6f}" data-duration="{length/FPS:.6f}" data-track-index="1"><div class="aperture"><svg xmlns="http://www.w3.org/2000/svg" class="world" id="{tag}w" viewBox="0 0 600 840" aria-hidden="true">{backdrop(n)}{dr}{motion}</svg></div><div class="caption" id="{tag}text">{tex}</div></div>')
        scenes.append(dict(id=tag,key=n,start=s,end=e,drawings=count,keys=order,fx=effect,words=words,mode='sakuga' if n=='wring' else 'held'))
        cue_s=va if n=='button' else s/FPS;cue_e=va+d if n=='button' else e/FPS; srt.append(f'{i+1}\n{clock(cue_s)} --> {clock(cue_e)}\n'+('\n'.join(words) if n!='button' else voice)+'\n'); sheet.append(f'| {i+1} | {s/FPS:g}–{e/FPS:g} | {" / ".join(words)} | {desc} | {sound} |')
    cfg=dict(fps=24,duration=60,voiceAt=va,voiceDuration=d,captionEnd=va+d,shots=scenes);dump('timeline.json',cfg)
    (P/'space-towel.srt').write_text('\n'.join(srt),encoding='utf-8'); (P/'TREATMENT.md').write_text('# منشفة في المدار — دفتر الإخراج\n\nإعادة رسم أنمي لتجربة حقيقية. موسيقى وفعل بصري، دون حوار منسوب إلى هادفيلد. سؤال الراوي الخارجي وحده مسموع. سؤال الطالبتين منقول بالمعنى. الحوض والدفتر ورسم المدار والتحام القطرتين لقطات توضيحية. الأرقام في الفيلم ثابتة.\n\n| اللقطة | الثواني | كلمات الشاشة | الصورة والفعل | الصوت |\n|---|---|---|---|---|\n'+'\n'.join(sheet)+'\n\nالتحريك على اثنين في 24 إطارًا/ث. غطسات لون أردوازي 0.25/0.35 ثانية بين اللقطات. تقريب 1→1.06 في الافتتاح وحده. جملة الخاتمة تدخل بعد عشرين إطارًا. آخر ثمانية إطارات إلى لون الحبر.\n')
    css=(P/'style.css').read_text(); script=(P/'motion.js').read_text();tmpl=(P.parents[1]/'studio-kit/styles/anime/index.html').read_text();prefix=tmpl[:tmpl.index('    <style>')].replace('<html lang="ar">','<html lang="ar" dir="rtl">').replace('Lantern — html-anime','منشفة في المدار — أنمي');page=prefix+f'''    <style>{css}</style><script src="gsap.min.js"></script>
</head><body><div id="root" data-composition-id="space-towel" data-start="0" data-duration="60" data-width="1080" data-height="1920">
'''+ '\n'.join(drawings)+'''\n<div id="dip" class="clip" data-start="0" data-duration="60" data-track-index="2"></div>
<div id="out" class="clip" data-start="0" data-duration="60" data-track-index="3"></div></div>
<script>const SHEET='''+json.dumps(cfg,ensure_ascii=False,separators=(',',':'))+';\n'+script+'\n</script></body></html>\n';(P/'index.html').write_text(page)
    import re
    assert set(re.findall(r'#[0-9a-fA-F]{6}\b',page))==set(COLORS);assert sum(s['mode']=='sakuga' for s in scenes)==1
    print('shots:',len(scenes),'cels:',sum(s['drawings'] for s in scenes),'voice at',va,'duration',d,'unique painted colours',len(COLORS))
if __name__=='__main__':main()
