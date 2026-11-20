"""Compose the Warka short from the local vox-real reference. No remote media at playback.
Run from the project directory: python3 tools/compose.py
"""
import json, math
from pathlib import Path
P=Path(__file__).resolve().parents[1]
FPS=24; W=1080; H=1920
D=json.loads((P/'timeline.json').read_text())['duration']
# Frame-locked cuts; established using voice/words.json, including space before the stresses.
F=[0,76,139,207,274,333,393,468,562,639,706,779,852,948,1036,1104,1174,1226,1310,1374,1440]
A=[v/FPS for v in F]; assert F[-1]==round(D*FPS) and max(b-a for a,b in zip(F,F[1:]))<=4*FPS
sheets=[];desc=[]

def box(x,y,w,h,cl='',css='',inner='',extra=''):
    return f'<div class="p {cl}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;{css}" {extra}>{inner}</div>'
def cap(txt,y,sz=118,x=75,w=930,al='center',cl='',delay=.13,css=''):
    return f'<div class="word align-{al} pop {cl}" data-in="{delay}" style="left:{x}px;top:{y}px;width:{w}px;font-size:{sz}px;{css}">{txt}</div>'
def chip(t,col=''):
    return f'<span class="chip {col}">{t}</span>'
def hi(t):return f'<em class="hl">{t}</em>'
def num(n):return f'<b class="num" dir="ltr">{n}</b>'
def tag(t,y=195,sz=78,al='right',cl='',delay=.12):return cap(f'<span class="tag {cl}">{t}</span>',y,sz,al=al,delay=delay)
def art(inner,cl='',z=2):return f'<svg class="art {cl}" viewBox="0 0 1080 1920" aria-hidden="true" style="z-index:{z}">{inner}</svg>'
def line(d,color='#e5322d',sw=12,delay=.45,extras=''):
    return f'<path class="draw" data-in="{delay}" pathLength="1" d="{d}" stroke="{color}" stroke-width="{sw}" fill="none" stroke-linecap="round" stroke-linejoin="round" {extras}/>'
def outline(cx,cy,rx,ry,delay=.5,color='#e5322d',sw=13):
    return line(f'M{cx-rx},{cy+6} C{cx-rx*1.08:.0f},{cy-ry*.65:.0f} {cx-rx*.57:.0f},{cy-ry*1.09:.0f} {cx+20},{cy-ry} C{cx+rx*.73:.0f},{cy-ry-8} {cx+rx+9},{cy-ry*.53:.0f} {cx+rx},{cy-8} C{cx+rx-8},{cy+ry*.9:.0f} {cx+rx*.45:.0f},{cy+ry+4} {cx-25},{cy+ry} C{cx-rx*.77:.0f},{cy+ry-3} {cx-rx-10},{cy+ry*.47:.0f} {cx-rx},{cy-12}',color,sw,delay)
def arrow(d,tip,col='#b52322',delay=.4):return line(d,col,11,delay)+line(tip,col,12,delay+.32)
def photo(f,x,y,w,h,rot=0,cl='',pos='50% 50%',dz=1.05,dy=0):
    # Rotation is applied on a wrapper that is not animated by GSAP.
    inner=f'<img class="img drift" data-zoom="{dz}" data-dy="{dy}" src="img/{f}" style="object-position:{pos}" alt=""/>'
    return box(x,y,w,h,'plate '+cl,f'transform:rotate({rot}deg);',inner)
def hatch(x,y,w,h,col='#27251b'):
    return box(x,y,w,h,'screen',f'color:{col};')
def strip(x,y,w,h,rot=0,color='var(--gold)'):
    return box(x,y,w,h,'tape',f'background:{color};transform:rotate({rot}deg);')
def add(theme,body,title,location,fx,sound='حفيف قصير ثم نبضة خافتة'):
    i=len(sheets);d=A[i+1]-A[i]
    sheets.append(f'<section id="s{i}" class="clip scene {theme}" data-start="{A[i]:.8f}" data-duration="{d:.8f}" data-track-index="2">{body}<div class="scatter"></div></section>');desc.append((title,location,fx,sound))
def contours(cx=800,cy=950,ink='#998954',n=8):
    paths=[]
    for j in range(n):
        pts=[]
        for k in range(120):
            a=2*math.pi*k/120; r=(210+39*j)*(1+.08*math.sin(a*3+.4)+.06*math.cos(a*5-.6));pts.append((cx+1.16*r*math.cos(a),cy+r*math.sin(a)))
        paths.append('<path d="M'+' L'.join(f'{x:.1f},{y:.1f}' for x,y in pts)+'Z" fill="none" stroke="'+ink+'" stroke-width="2" opacity=".55"/>')
    return art(''.join(paths),z=0)

def iraq(x,y,w,h,redpoint=True):
    a=json.loads((P/'assets/iraq.json').read_text()); lon0=38.6;lat0=37.45; sx=w/10.25;sy=h/8.6
    def pt(lon,lat):return (x+(lon-lon0)*sx,y+(lat0-lat)*sy)
    d='M'+' L'.join('%.1f,%.1f'%pt(lon,lat) for lon,lat in a)+'Z'; bx,by=pt(44.3855,33.3277);ux,uy=pt(45.6,31.3)
    points=f'<circle cx="{ux:.1f}" cy="{uy:.1f}" r="6" fill="#191916"/><circle cx="{bx:.1f}" cy="{by:.1f}" r="11" fill="#b52322" stroke="#fff9e9" stroke-width="4"/>' if redpoint else ''
    return art(f'<path d="{d}" fill="#ffd400" stroke="#26251e" stroke-width="7" stroke-linejoin="round"/>'+points)

def field(dark=False):
    # Schematic infographic. Not an aerial image or a reconstruction of the real farm.
    fill='#febf37' if dark else '#e9d9a8';ink='#4b4430';t=''
    for pts in ['175,724 483,608 579,697 268,823','286,845 595,722 680,804 374,932','392,951 700,835 786,921 483,1043','501,1060 803,945 914,1052 598,1180']:
        t+=f'<polygon points="{pts}" fill="{fill}" stroke="{ink}" stroke-width="4"/>'
    for i in range(12):
        x=184+25*i;y=725-i*9.5;t+=f'<path d="M{x},{y} l85,85 M{x+112},{y+118} l78,78 M{x+218},{y+224} l83,85 M{x+324},{y+340} l87,91" stroke="{ink}" opacity=".52" stroke-width="3"/>'
    t+='<path d="M641,566 l104,-42 98,96 -108,42 z" fill="#e5322d" stroke="#191916" stroke-width="6"/><path d="M735,662 v64 l108,-44 v-62z" fill="#b33426" stroke="#191916" stroke-width="5"/><path d="M641,566 v61 l94,99 v-64z" fill="#fff4cf" stroke="#191916" stroke-width="5"/>'
    return art(t)
# Opening: actual hands displaying the recovered mask (NARA 6648802), no reconstructed detail.
add('ink',contours(540,800,'#aa915e',11)+photo('mask.jpg',0,224,1080,1000,0,'noframe',pos='51% 51%',dz=1.08)+strip(-10,1216,1100,23,-1)+tag('الوركاء',171,92,delay=0)+cap('وجهٌ سومريّ',1285,112,al='right',cl='white',delay=0)+cap(hi('تحت التراب'),1446,133,al='right',delay=.6)+art(line('M185,1334 Q120,1269 159,1187','#ffd400',10,.9),z=4),'وجه من تحت التراب','صورة أرشيفية ممتدة إلى جانبي الكادر: عرض القناع بين الأيدي بعد الاسترداد','اقتراب مستمر؛ مسحة تظليل مع العبارة','نقرة افتتاح ونبض وتري')
add('paper',hatch(0,0,450,1920,'#5c51323a')+photo('field-left.jpg',93,405,580,735,-6,pos='50% 56%',dz=1.07)+photo('portrait.jpg',477,616,510,730,5,pos='50% 50%',dz=1.07)+cap('خرج',183,115,al='right')+cap(chip('مرّتين'),1398,151,delay=.04)+art(line('M171,1328 Q348,1375 462,1318','#b52322',12,1.05),z=5),'مرّتين','صورتا الموقع والوجه، ورق كريمي','صورتان بعمقين؛ ضربة تظليل وقوس')
add('gold',contours(970,1470,'#987d0a')+box(95,500,865,738,'note','transform:rotate(-4deg)')+box(140,552,52,621,'perf')+photo('field-right.jpg',195,620,615,460,2,'thin',dz=1.06)+cap('المرّة الثانية',165,105)+art(line('M206,1000 L799,666','#e5322d',27,.25)+line('M244,697 L769,1029','#e5322d',20,.65),z=4)+cap('<span class="stamp">ليست حفريّة</span>',1337,113,delay=.27),'ليست حفريّة','رسم بصري يشطب صورة الحفر؛ ليس توثيقًا للواقعة','خطّا نفي مرسومان وختم','طبعة ورق')
add('paper',cap('انظر إلى',180,113,al='right')+cap(hi('العينين'),315,127,al='right',delay=.35)+box(42,620,996,619,'inkbox','border:14px solid #fffaf0;box-shadow:15px 17px 0 var(--ink);overflow:hidden;', '<img class="drift" data-zoom="1.097" src="img/mask.jpg" style="width:100%;height:100%;object-fit:cover;object-position:50% 43%" alt="تفصيل العينين"/>')+art(outline(648,893,72,48,.42)+arrow('M267,1321 Q349,1189 515,1114','M493,1160 L519,1110 L463,1113'),z=4)+cap(chip('فارغتان','ivory'),1373,115,al='left',delay=.67),'عينان فارغتان','صورة الأيدي والقناع؛ تعيين موضع العين في اللقطة الحقيقية','دائرة حمراء على العين وسهم مفصلي')
add('crimson',hatch(0,1470,1080,480,'#ffc83355')+box(163,324,745,996,'arch cream')+photo('portrait.jpg',190,352,690,935,0,'porthole',dz=1.07)+strip(132,352,232,55,-15)+cap('قناع',170,100,al='right',cl='white')+cap(chip('الوركاء'),1402,141,delay=.25),'قناع الوركاء','صورة القطعة على بطاقة جرد مقوّسة','دخول اسم القطعة خلف شريط أصفر')
add('paper',box(0,825,1080,1095,'inkbox')+contours(225,1520,'#ad9550',9)+cap('عمره نحو',191,101,al='right')+cap(num('5000'),338,283,al='center',delay=.22)+cap('سنة',865,123,x=617,w=358,al='right',cl='yellow',delay=.55)+photo('portrait.jpg',107,971,528,635,-3,'round',pos='53% 51%',dz=1.08)+art(line('M146,727 Q509,706 932,714','#e5322d',18,.64)+arrow('M811,1189 Q775,1302 667,1351','M701,1309 L665,1355 L728,1350','#ffd400',1.02),z=4),'نحو 5000 سنة','لوح ورقي وفاصل حبري وصورة قياس بصرية','رقم ثابت بلا عدّاد؛ تسطير وسهم')
add('paper',hatch(480,0,600,1920,'#6f61392c')+tag('أوروك',183,80)+photo('field-right.jpg',308,520,623,686,7,pos='48% 48%',dz=1.05)+photo('field-left.jpg',89,714,546,585,-7,pos='56% 50%',dz=1.09)+strip(500,543,193,52,12)+strip(142,725,166,52,-14)+cap('حفريات',1390,109,al='right')+cap(hi('الثلاثينيات'),1521,101,al='right',delay=.36),'حفريات الثلاثينيات','صورتان أرشيفيتان للموقع؛ ليستا لحظة اكتشاف الوجه','انزلاق ألبوم ومطالعة صورتين أصليتين')
add('atlaspage',cap('الاكتشاف الأوّل',169,107,al='right')+cap(num('1939'),294,151,al='right',delay=.27)+art(outline(747,740,163,115,.58)+arrow('M210,1400 Q282,1280 423,1191','M394,1201 L427,1187 L418,1225'),z=4)+cap(chip('أوروك'),1378,120,al='right',delay=.26)+cap('جنوب العراق',1532,91,al='right',delay=.95),'أوروك • 1939','تحديد موضع أوروك على مرئية ASTER اللاحقة؛ السنة للاكتشاف لا للصورة','مسح بصري بطيء فوق المرئية ودائرة الموقع')
add('paper',photo('museum.jpg',68,456,937,835,-3,pos='54% 51%',dz=1.08)+strip(665,410,216,57,7)+tag('بغداد',175,84)+cap('المتحف',1334,128,al='right')+cap(hi('العراقي'),1488,124,al='right',delay=.44)+art(line('M153,1322 Q109,1243 147,1126','#b52322',12,.85),z=5),'المتحف العراقي','معلم المتحف في بغداد في صورة مكانية','بطاقة واجهة تميل مع قصّ قريب')
add('gold',contours(100,1420,'#a58614')+box(125,455,848,893,'inkbox','transform:rotate(3deg)')+box(96,435,848,893,'cream boxedge','transform:rotate(-2deg)')+hatch(185,502,665,110,'#ac9b673c')+cap('نيسان',670,151)+cap(num('2003'),838,231,delay=.15)+art(line('M228,1159 Q517,1183 862,1145','#b52322',17,.72),z=4)+cap('عام السرقة',1394,107),'نيسان 2003','بطاقة تاريخ طباعية، أصفر وحبر','السنة تظهر مرة وتبقى ثابتة')
# An empty outlined display place, not a purported photograph of a looted gallery.
add('ink',contours(510,890,'#648078',8)+box(176,344,719,955,'arch whiteedge')+art('<path d="M279,1130 l177,-76 364,31 -170,83z M279,1130 v76 l371,40 v-78 M650,1246 l170,-83 v-78" fill="#36352d" stroke="#d5c49a" stroke-width="6" stroke-linejoin="round"/><path d="M410,1079 v-163 l33,-30 M651,1100 v-192 l-35,-26" fill="none" stroke="#d5c49a" stroke-width="9" stroke-linecap="round"/>'+line('M541,784 C425,769 384,669 406,550 C433,427 631,422 668,545 C695,678 650,775 541,784','#ffd400',9,.24),z=3)+art(line('M111,1292 L968,1292','#f1e9d6',9,.32)+line('M389,1350 L702,1350','#ffd400',12,.8),z=4)+cap('اختفى',1368,111,cl='white')+cap('القناع',1502,128,cl='yellow',delay=.3),'اختفى القناع','حامل عرض فارغ ودائرة مرسومة، لا إعادة بناء قاعة حقيقية','يُرسَم خط الرفّ؛ تظهر مساحة الغياب','نبضة منخفضة وفراغ لحني')
add('paper',box(0,0,328,1920,'ybox')+photo('entrance.jpg',94,495,867,812,3,pos='43% 47%',dz=1.075)+cap('بعد شهور',199,117,al='right')+art(arrow('M201,1443 Q155,1343 250,1247','M207,1273 L253,1243 L252,1298'),z=4)+cap(chip('بلاغ عراقي'),1435,111,al='right',delay=.35),'بلاغ عراقي','صورة مدخل المتحف لاحقًا لا صورة المُبلّغ','سهم إلى المدخل وشريط البلاغ')
add('gold',box(122,480,842,800,'note','transform:rotate(-2.4deg)')+box(180,615,65,470,'perf')+cap('معلومة عن',557,92,al='center')+cap(hi('آثار مخبّأة'),792,125,delay=.15)+art(line('M193,1081 Q534,1097 839,1073','#e5322d',14,.55)+line('M447,1225 L540,1300 L634,1219','#191916',9,.98),z=3)+cap('لا اسم للقناع',1432,114,delay=1.23),'آثار مخبّأة','بطاقة شرح للمعلومة، لا وثيقة منسوبة إلى المُبلّغ','مسحة وتسطير ثم بيان غياب الاسم')
add('ink',photo('baghdad-iss.jpg',0,400,1080,890,0,'noframe',pos='51% 55%',dz=1.12)+iraq(92,1045,285,282)+cap('وجهة البلاغ',181,101,al='right',cl='white')+art(outline(522,898,275,171,.46,'#ffd400',12),z=4)+cap('شماليّ',1295,112,al='right',cl='white')+cap(chip('بغداد'),1502,119,al='right',delay=.35),'شماليّ بغداد','صورة فضائية لبغداد؛ الدائرة للمدينة وليست موقعًا للمزرعة','تكبير فوتوغرافي وتعيين النطاق العام')
add('paper',cap('مزرعة',179,138,al='right')+box(85,418,911,927,'farmboard','transform:rotate(-2deg)')+field()+art(arrow('M321,1173 Q322,1047 450,950','M411,967 L452,946 L438,993','#b52322',1.0),z=4)+cap(chip('رسم توضيحي','ivory'),1441,88,al='center',delay=.35),'مزرعة','مخطط حقل توضيحي؛ لا يزعم تحديد موقع أو شكل حقيقي','رسم هندسي ورأس سهم يتتبع الشرح')
# Section drawing and reveal, intentionally graphic rather than photographic re-enactment.
strata='<path d="M0,755 Q235,674 444,733 T825,702 T1080,703 V1920 H0Z" fill="#d3b884"/>'
for i in range(15):
    y=804+i*56;strata+=f'<path d="M-40,{y} C190,{y-67} 337,{y+41} 522,{y-21} S805,{y-70} 1120,{y-21}" fill="none" stroke="#{"877451" if i%3 else "514835"}" stroke-width="{3 if i%3 else 7}" opacity=".7"/>'
add('paper',cap('خلف المزرعة',201,119,al='right')+art(strata,z=1)+art(arrow('M859,480 C867,687 740,756 633,884','M635,834 L630,889 L696,861','#b52322',.26),z=3)+box(286,913,502,489,'disk inkbox','z-index:2;')+photo('portrait.jpg',368,968,337,355,0,'round lens',dz=1.065)+cap(chip('تحت التراب','ivory'),1482,101,delay=.63),'خلف المزرعة','قطاع توضيحي في الأرض مع إدراج صورة الوجه؛ ليس تصوير الحفر','خطوط التربة ثم عدسة تفتح على القناع')
add('crimson',hatch(0,0,553,1920,'#ffc87c45')+box(151,314,778,1041,'cream','transform:rotate(-3deg);box-shadow:18px 18px #191916')+photo('presentation.jpg',187,431,699,767,-3,'thin',pos='53% 51%',dz=1.07)+strip(704,311,145,46,10)+cap(chip('سليمًا'),1431,148,delay=.27)+art(line('M220,1334 Q527,1368 830,1311','#ffd400',12,.55),z=4),'سليمًا','الصورة الحقيقية للقناع','عودة الصورة إلى سياقها بالأيدي وختم السلامة','جرس قصير ووتر محلول')
add('paper',tag('23 أيلول',180,90)+photo('entrance.jpg',80,464,910,828,-3,pos='50% 50%',dz=1.08)+strip(695,441,196,52,11)+art(line('M839,1331 Q525,1282 291,1350','#b52322',12,.75),z=4)+cap('عاد إلى',1357,116,al='right')+cap(hi('المتحف'),1495,121,al='right',delay=.4),'عاد إلى المتحف','واجهة المتحف الفعلية للتعريف بالمكان؛ التاريخ للعودة وليس لالتقاط صورة الواجهة','مسحة صفراء تنتهي بصورة المؤسسة')
add('gold',box(0,960,1080,960,'cream')+cap('مرّتين',192,144)+photo('field-left.jpg',141,547,707,710,-5,pos='55% 53%',dz=1.08)+strip(168,524,178,54,-18)+cap(chip('الاكتشاف','k'),1431,118,delay=.47),'مرّتين','صورة أوروك تعيد الصلة بالجملة الافتتاحية','انزلاق الصورة ووقفة قبل البديل')
add('ink',contours(554,753,'#b39962',9)+box(202,402,680,820,'disk ybox')+photo('mask.jpg',126,400,828,828,-4,'round',pos='51% 50%',dz=1.07)+cap('أيّهما',1283,115,cl='white',delay=.04)+cap(hi('أدهشك أكثر؟'),1437,118,delay=.47)+art(line('M192,1225 Q188,1310 270,1369','#e5322d',12,.55),z=4),'أيّهما أدهشك أكثر؟','الوجه الحقيقي والتكوين الحلقي من الافتتاح','تظليل السؤال وعودة هادئة للبداية','خاتمة لحنية قصيرة')

css=(P/'design.css').read_text()+'''\n#s0{opacity:1}#root{background:#f1e9d6 url(img/grain.png)}.plate.round{border-radius:50%}.plate.porthole{border-radius:52% 52% 0 0}.plate.lens{z-index:3;border-width:8px;box-shadow:none}.scene{z-index:2}.atlaspage{background:transparent!important}#atlas{z-index:1}\n'''
video=f'<video muted playsinline preload="auto" id="atlas" data-start="{A[7]}" data-duration="{A[8]-A[7]}" data-track-index="1" src="assets/uruk-atlas.mp4" poster="img/uruk-aster.jpg" style="opacity:1"></video>'
wipe=f'<div id="wipe" class="clip" data-start="0" data-duration="{D}" data-track-index="8"></div>'
js=(P/'motion.js').read_text().replace('/*CUTS*/[]',json.dumps(A)).replace('/*DURATION*/0',str(D));
html=f'''<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><title>قناع الوركاء — وجه خرج من التراب مرتين</title><style>{css}</style><script src="gsap.min.js"></script></head><body><div id="root" data-composition-id="warka" data-start="0" data-duration="{D}" data-fps="24" data-width="1080" data-height="1920">{video}{''.join(sheets)}{wipe}</div><script>{js}</script></body></html>'''
(P/'index.html').write_text(html)
(P/'cuts.json').write_text(json.dumps([dict(frame=F[i],start=A[i],end=A[i+1],keyword=a[0]) for i,a in enumerate(desc)],ensure_ascii=False,indent=2)+'\n')
(P/'TREATMENT.md').write_text('# قناع الوركاء: خرج من التراب مرتين\n\nشورت 9:16، دقيقة واحدة، 24 إطارًا/ث. قالب Vox بلقطات وصور حقيقية (`vox-real`): حبر على ورق منقّط، أشرطة صفراء، ودوائر حمراء تربط الشرح بالدليل. المادة المرئية فوتوغرافية، لا يوجد فيلم مصوَّر لانتشال 2003 في هذا العمل. حركة مرئية ASTER حركة كاميرا فوق صورة حقيقية، لا تسجيل جوي للحدث. أصوات أصلية موضوعة بعد قياس مسارات الراوي. العبارات الكاملة في الترجمة الخارجية فقط.\n\n| الوقت بالثواني | كلمات الشاشة | المشهد / الخلفية / الصورة | الحركة | الصوت |\n|---|---|---|---|---|\n'+''.join(f'| {A[i]:.2f}–{A[i+1]:.2f} | '+ ' | '.join(s)+' |\n' for i,s in enumerate(desc)))
