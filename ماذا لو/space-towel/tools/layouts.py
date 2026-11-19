"""Locked layouts and cel poses. Only the establishing shot receives a camera move."""
from cels import *
import math
# A film in three movements (student question / wring / consequence), not three repeated shorts.
SHOTS=[
 ('hook',0,['الماء يلتفّ','حول أصابعه!'],'يدان وطبقة الماء أمام وجه هادفيلد. اقتراب وحيد من الكادر.','وتر مضروب ولمعة قصيرة'),
 ('sink',3.25,['على الأرض،','يسقط الماء'],'مقارنة توضيحية فوق الحوض؛ قطرة تسقط ودوائر على سطح الماء.','قطرة في الخزف'),
 ('orbit',6.25,['محطة الفضاء الدولية','2013'],'الأرض من المدار؛ الهيكل والألواح الشمسية يعبران الأفق.','نغمة بعيدة من القرار'),
 ('chris',9.25,['كريس هادفيلد','رائد فضاء كندي'],'لقطة متوسطة داخل الوحدة وتبديل الجفون. الرسوم ليست تسجيلًا أرشيفيًا.','أوتار دافئة'),
 ('notebook',12.25,['فكرة طالبتين'],'دفتر توضيحي لا نسخة من مخطوطة: رسم منشفة وقطرة ثم سؤال.','احتكاك سنّ القلم'),
 ('puck',15.25,['منشفة مضغوطة'],'قرص القماش بين أصابعه. نرى خطوط طيّه.','طَقّة قماش خافتة'),
 ('open',18.25,['فردها بيديه'],'ثلاث حالات: مطويّة، تفتح، ثم تتّسع حدودها.','رفرفة'),
 ('pouch',21.25,['من كيس الشرب…'],'فوهة الكيس تقترب من القماش، ثم تخرج حبّة ماء.','حفيف الكيس'),
 ('soak',24.25,['بلّل المنشفة'],'لقطة مقرّبة؛ بقعة البلل تنتشر في طيّات القماش.','أثر بلل قصير'),
 ('wait',27.25,['ماذا سيحدث','إذا عصرها؟'],'لقطة قريبة للعينين، تتوسطهما حافة القماش.','وتر غليظ ثم فراغ'),
 ('wring',30.25,['لفّ طرفيها'],'لقطة الساكوغا الوحيدة: توقّف، شدّ متعاكس، طيّات جديدة، خروج الماء، استقرار.','ضربة خافتة ثم حفيف سريع وأجراس صاعدة'),
 ('sleeve',33.75,['خرج الماء من القماش'],'تفصيل من الزاوية الأخرى: غلاف وطيّات وانعكاس ضوئي على السطح.','رنّة زجاجية'),
 ('few',36.75,['تطايرت بضع قطرات'],'بؤرة اللقطة قطرتان منفصلتان فقط فوق حافة المنشفة.','رنتان متباعدتان'),
 ('most',39.75,['وبقي معظمه حولها'],'الكادر أوسع؛ الغلاف المتصل أهم من القطرات المنفصلة.','عودة لحن البداية'),
 ('fingers',43,['وامتدّ إلى يديه'],'عقد الأصابع في المقدمة وسطح الماء يمتدّ فوقها.','صوت تماس رطب'),
 ('letgo',46.25,['أفلتها… فطفَت'],'يد تنسحب والقماش المفتول يبقى أمامنا في الهواء.','وتَر وحيد وتعليق'),
 ('freefall',49.25,['المحطة وما فيها','في سقوط حرّ'],'منظر خارجي؛ القوس حول الأرض يبيّن السقوط المداري لا غياب الجاذبية.','نغمة ملساء منخفضة'),
 ('cohesion',52.75,['التوتّر السطحيّ','يُبقي الماء متماسكًا'],'رسم مقرّب لتماس قطرتين والتحامهما؛ مثال تفسيري لا حدث إضافي في التسجيل.','تقارب نغمتين'),
 ('button',56.25,['أين توقّعت','أن يذهب الماء؟'],'عودة إلى الكادر الافتتاحي. سؤال الراوي الوحيد ثم خفوت إلى الحبر.','سؤال بالفصحى وقفلة موسيقية'),
]

def backdrop(n):
    if n in ('orbit','freefall'):return bg('earth',0, -90,-90,1.17) if n=='freefall' else bg('earth')
    if n=='notebook':return bg('desk')
    if n=='sink':return bg('sink',0)
    if n in ('hook','button','chris','most','letgo','pouch'):return bg('cabin',.16)
    if n in ('wait','fingers','sleeve','few','cohesion'):return bg('cabin',.53,-280,-350,1.95)
    if n in ('wring','soak','open','puck'):return bg('cabin',.30,-120,-130,1.48)
    raise ValueError(n)

def clothfree(k):
    body=p('M-202 -42 Q-186 -65 -131 -57 Q-57 -47 -6 -59 Q61 -75 131 -48 L193 -54 Q211 -54 215 -31 L214 36 Q217 53 195 57 Q159 54 122 52 Q55 52 12 69 Q-46 90 -108 65 Q-156 49 -195 60 Q-219 46 -215 8Z',W,B,2.7,'fill-opacity=".39"')
    body+=p('M-216 -39 Q-193 -52 -156 -45 L-161 40 Q-191 37 -213 44 Q-225 15 -216 -39Z',C,I,2)+p('M162 -38 Q188 -48 206 -40 Q219 0 202 43 Q179 50 157 40Z',C,I,2)
    body+=img('wet-folds',-197,-90,398,178)
    body+=p('M-200 -38q20 -20 49 -15 M-125 -49q15 0 28 3 M70 -58q30 -4 47 4 M-51 70q32 4 50 -4','none',C,3.1)
    return at(body,326+5*k,531-13*k,1.03,-14-k*1.9)


def capillary(k):
    if k==0: return at(bead(0,0,88)+bead(168,0,59),201,383,1,-9)
    if k==1: return at(bead(0,0,86)+bead(137,0,57),225,388,1,-9)
    s=p('M-103 -6 C-105 -73 -36 -113 25 -99 C93 -91 146 -57 150 -8 C156 44 117 91 54 98 C-22 105 -102 67 -103 -6Z',B,B,3,'fill-opacity=".4"')+p('M-101 2 Q-67 73 -2 78 Q94 93 147 -2 Q154 63 78 90 Q11 114 -48 78 Q-95 51 -101 2Z',W)+p('M-77 -33 Q-68 -62 -34 -68 Q-23 -65 -36 -60 Q-63 -48 -67 -31Z',C)+p('M89 -64 Q113 -56 123 -38 M93 72 Q113 60 123 43','none',B,5)
    return at(s,272,410,1.43,-10)

def pose(n,k):
    if n in ('hook','button','most'):
        if n=='most':
            return portrait(-191,-145+(0,5,2)[k],1.08,k,k==1,(-3,-3,-1)[k],True)+pair(304,577-4*k,.94,-12+k,1,.76+.07*k,True)
        br=n=='button'; y=(-3,0,2)[k];return portrait(-119,-78+y,1.00,k,k==1,(-3,-3,-2)[k],not br or k<2)+pair(301+2*k,556+(6 if br else 0)-4*k,.88,6-.8*k,1,.79+.085*k,True)
    if n=='sink':
        # Anonymous everyday comparison, not a historical second camera angle. A wrung cloth enters above the bowl.
        return pair(278,185+3*k,.92,-7+k*.8,.72,0,False,0,0)+p(f'M{285+2*k} 225q10 14 6 25q-6 8 -10 2q-4 -7 4 -27Z',W,C,1.4)
    if n in ('orbit','freefall'):
        if n=='orbit':return orbit(287+8*k,321-2*k,k,1.02)
        path='M-54 524 Q231 185 694 288'; track=p(path,'none',B,1.9,'stroke-dasharray="13 14"')
        return track+orbit(225+18*k,344-10*k,k,.69)
    if n=='chris':return portrait(-5,22+(0,-5,0)[k],.80,k,k==1,(-4,-4,-1)[k])
    if n=='notebook':return notebook(k)
    if n=='puck':
        # Shirt/palm enter from opposite sides; a compact stack of fabric is centre stage.
        a=portrait(-284,-243,1.42,k,k==1,-5,True);a+=at(puck(k),330+5*k,500-8*k,1.39,-10+4*k);a+=g(img('grip-left',0,531,249,349),'translate(5 7) translate(241 552) rotate(-16) scale(1.05) translate(-217 -694)');return a
    if n=='open':
        wide=(.64,.92,1.2)[k];tall=(.58,.82,1.08)[k]
        s=g(cuff(k),f'translate(317 {428-k*6}) rotate({-12+4*k}) scale({wide} {tall})');s+=g(img('grip-left',0,531,249,349),f'translate({317-177*wide} {422-80*tall}) rotate(-7) scale(.95) translate(-200 -694)');s+=g(img('grip-right',497,543,271,389),f'translate({317+172*wide} {423-69*tall}) rotate(9) scale(.94) translate(-563 -694)');return s
    if n=='pouch':
        a=at(cuff(k),403,539,1.0,-9+k);a+=at(pouch(k),178+k*7,297+k*4,1.15,17+k);a+=bead(310+k*3,413+k*6,8+3*k)
        a+=g(img('grip-left',0,531,249,349),f'translate({63+3*k} {296+2*k}) rotate(9) scale(.77) translate(-195 -694)');a+=g(img('grip-right',497,543,271,389),f'translate({536-k*3} {466+2*k}) rotate(14) scale(.80) translate(-559 -694)');return a
    if n=='soak':
        a=at(cuff(k),254,446,1.72,-12);a+=at(pouch(k),-24,234,1.8,16);ax=211+k*3;ay=397-k
        a+=at(p('M-54 3 Q-44 -30 -22 -23 Q-7 -38 12 -24 Q31 -32 37 -15 Q64 -16 56 8 Q62 29 37 26 Q17 48 -3 30 Q-34 47 -40 29 Q-65 23 -54 3Z',B,'none',1,'opacity=".82"')+p('M-43 4 Q-30 -2 -14 2 Q7 7 29 -5 M-19 18 Q-3 11 15 17','none',S,1.2),ax,ay,(.38,.94,1.49)[k],-10);a+=p('M204 365 Q204 380 215 391','none',B,6)+p('M205 368 Q206 380 213 385','none',C,2);return a
    if n=='wait':return portrait(-412,-308+2*k,1.9,k,k==1,-3+k*.5,True)+at(g(cuff(k),'scale(1 .63)'),348,812-k*5,1.85,-9)
    if n=='wring':
        vals=[(.10,.0,8,0),(.03,.0,10,9),(.21,.0,7,13),(.48,.05,2,-1),(.74,.24,-3,-7),(.97,.54,-7,-11),(.95,.79,-5,-5),(1,.94,-4,-2)]
        t,w,angle,dy=vals[k]; a=portrait(-135,-190+(7 if k in (1,2) else 0),1.12,0,False,-5+k*.2,True)
        a+=pair(302,500+dy,.93,angle,t,w,k==7,2*(1-t),-2*(1-t));
        if k in (3,4,5):
            for x,y,l in [(0,349,66),(37,320,47),(10,654,59),(540,290,66),(561,316,44),(552,664,65)]:
                a+=p(f'M{x} {y}l{l} {17 if x<100 else -21}','none',B,1.9)
        return a
    if n=='sleeve':return pair(310,411-k*3,1.88,-17+.65*k,1,.75+.09*k,True)
    if n=='few':return pair(204,736-k*4,1.21,12+k*.5,1,.81,True)
    if n=='fingers':return pair(56,522-k*4,1.4,19+k*.55,1,(.22,.61,1.06)[k],True)
    if n=='letgo':
        a=portrait(-130,-152,1.12,k,k==1,2,True);a+=clothfree(k)
        # Match previous grips but withdraw the hand leftward; no arm disconnected from the edge.
        a+=g(img('grip-left',0,531,249,349),f'translate({(152,85,32)[k]} {624+k*20}) rotate(-14) scale(.93) translate(-204 -694)');return a
    if n=='cohesion': return capillary(k)
    raise ValueError(n)

def fx(n):
    # Props/background motion on ones, precisely separate from held character drawings.
    if n=='sink':return ('drop',bead(281,263,8)+bead(297,222,4.4))
    if n=='few':return ('few',bead(241,464,49,-15)+bead(403,337,22,8))
    if n in ('hook','button','most'):return ('pearl',bead(454,428,9,-15)) if n!='most' else ('pearl',bead(438,335,7,-15))
    if n in ('orbit','freefall'):return ('glint',shine(450 if n=='orbit' else 353,185 if n=='orbit' else 251,.8))
    if n=='notebook':return ('lead',at(p('M-7 0 L-6 -107 L0 -117 L6 -109 L7 0 L0 19Z',O,I,1.5)+p('M-7 0H7L0 19Z',K,I,1.3)+p('M-3 12H3L0 19Z',I)+p('M-3 -4V-105','none',G,2),361,261,1.2,37))
    if n=='pouch':return ('water',bead(317,400,5))
    if n=='letgo':return ('drift',bead(438,365,11))
    if n=='sleeve':return ('shine',shine(357,367,.75))
    if n=='fingers':return ('shine',shine(378,483,.65))
    if n=='cohesion':return ('shine',shine(201,332,1.15))
    return (None,'')
