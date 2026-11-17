"""Two independent cover layouts, not screenshots with an arbitrary timestamp overlay."""
from pathlib import Path
from cels import *
P=Path(__file__).resolve().parents[1];out=P/'out';out.mkdir(exist_ok=True)
a=img('cabin',0,-25,600,1110,True)+rect(0,0,600,1067,I,'opacity=".12"')+portrait(-147,-24,1.16,watch=True,tilt=-3)+pair(302,610,1.04,-9,1,1,True)+bead(490,413,15,-13)
a+=p('M-20 754 Q104 727 258 728 Q468 733 626 690 L626 1080 L-20 1080Z',I)+p('M-5 753 Q121 727 240 730 M479 726Q550 711 604 697','none',B,2.4)
b=img('cabin',-360,-330,1230,1650,True)+rect(0,0,600,1067,I,'opacity=".62"')
b+=p('M0 0H600V343 Q416 308 284 344 Q101 395 0 368Z',I)+p('M0 367 Q102 397 272 350','none',W,2)+pair(178,622,1.36,-22,1,1,True)+bead(149,433,36,-18)+bead(457,800,20,20)+shine(150,415,.75)
base='''@font-face{font-family:Cairo;src:url('fonts/cairo-ar.woff2');font-weight:200 1000;font-display:block}*{box-sizing:border-box}html,body{margin:0;width:1080px;height:1920px;overflow:hidden}body{position:relative;background:%s;font-family:Cairo,sans-serif;direction:rtl}svg{width:1080px;height:1920px}.headline{position:absolute;left:40px;right:40px;text-align:center;font-weight:900;line-height:1.13;white-space:nowrap;color:%s;-webkit-text-stroke:10px %s;paint-order:stroke fill}.a .headline{top:1338px;font-size:124px}.b .headline{top:398px;font-size:124px}.headline b{color:%s}.b b{color:%s}'''%(I,C,I,G,G)
for name,kind,world,title in [('thumbnail','a',a,'أين ذهب <b>الماء؟</b>'),('thumbnail-b','b',b,'غلافٌ من <b>ماء!</b>')]:
    (out/(name+'.html')).write_text(f'<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><base href="../"><style>{base}</style></head><body class="{kind}"><svg xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none" viewBox="0 0 600 1066.667">{world}</svg><div class="headline">{title}</div></body></html>')
