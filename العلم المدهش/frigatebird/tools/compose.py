"""Run the studio's S2 collage engine with recorded, word-addressable cuts.
Print plates extend the normal photo/cutout items; never synthesise EEG values.
"""
from contextlib import ExitStack
from pathlib import Path
from unittest.mock import patch
import html,json,math,os,re,shutil,subprocess,sys,tempfile
from PIL import Image
P=Path(__file__).resolve().parents[1]; KIT=P.parents[1]/'studio-kit';sys.path.insert(0,str(KIT/'collage'))
import make_collage as C, motions as M
E=json.loads((P/'video.json').read_text()); lines=json.loads((P/'lines.json').read_text()); words=json.loads((P/'voice/words.json').read_text())
F=E['fps'];D=E['duration']; END=F*D
PAP={'cream':'#f3e7cb','oat':'#e0caa4','sea':'#b8d3ca','blue':'#1d434c','night':'#192d33','white':'#f6f1de','yellow':'#f4c954'}
INK='#15383d';CORAL='#c84434';YEL='#ffce36'
A={k:{'file':v['src'],'size':Image.open(P/v['src']).size,'cut':v.get('cut',False)} for k,v in E['assets'].items()}
L={v['id']:v for v in lines}
def frame(cue):
    if cue=='start':return 0
    id,ix,delta=cue;return round(L[id]['startFrame']+(words[id][ix]['s']+delta)*F)
cuts=[frame(b['cue']) for b in E['beats']]+[END]
assert all(2*F<=b-a<=4*F for a,b in zip(cuts,cuts[1:])),cuts
sch=[(c/F,e/F,e/F) for c,e in zip(cuts,cuts[1:])];timeline={'duration':D,'fps':F,'shots':[]}

def bgart(i,bg,theme):
    # A sheet of screen-printed field-notebook paper, not a rotating UI or a photo backdrop.
    col=PAP[bg];dark=bg in ('blue','night'); penc='#e5e0bc' if dark else '#396061';ink='#0b252b' if dark else '#6a8a7f';r=[]
    r+=[f'<defs><pattern id="pg{i}" width="256" height="256" patternUnits="userSpaceOnUse"><image href="assets/paper-{bg}.jpg" width="256" height="256"/></pattern><pattern id="pht{i}" width="14" height="14" patternUnits="userSpaceOnUse" patternTransform="rotate(-18)"><circle cx="6" cy="6" r="2.9" fill="{penc}" opacity=".3"/></pattern></defs><rect width="1080" height="1920" fill="url(#pg{i})"/>']
    # A few broad, quiet off-register marks outside the reading area.
    if theme in ('sun','air','wind','nightwind','specimen'):
        cx,cy,rad={'sun':(610,925,322),'air':(370,808,296),'wind':(410,914,286),'nightwind':(545,873,364),'specimen':(450,975,268)}[theme]
        r+=[f'<circle cx="{cx+18}" cy="{cy+18}" r="{rad+11}" fill="url(#pht{i})"/><circle cx="{cx}" cy="{cy}" r="{rad}" fill="{YEL if not dark else "#588884"}" opacity="{.89 if not dark else .71}"/>']
        for k in range(3):r+=[f'<path d="M{-80+k*42} {1340+k*44} Q340 {1270+k*45} 559 {1110+k*27} T1200 {850+k*34}" fill="none" stroke="{penc}" stroke-opacity=".20" stroke-width="3"/>']
    elif theme in ('chart','draft','proof','fold','day'):
        # Fine cartographic contours (decorative, never represented as a route).
        cx,cy=(1010,1470) if i%2 else (-72,460)
        for k in range(8):
            rx=95+29*k;ry=rx*1.38;r+=[f'<path d="M{cx-rx},{cy} c{-rx*.18:.1f},{-ry*.54:.1f} {rx*.46:.1f},{-ry*1.25:.1f} {rx:.1f},{-ry:.1f} s{rx*1.21:.1f},{ry*.7:.1f} {rx:.1f},{ry:.1f} s{-rx*.55:.1f},{ry*1.09:.1f} {-rx:.1f},{ry:.1f} s{-rx*1.11:.1f},{-ry*.52:.1f} {-rx:.1f},{-ry:.1f}Z" fill="none" stroke="{penc}" stroke-opacity=".18" stroke-width="3"/>']
        if theme=='proof':r+=[f'<path d="M0 511l1080 -245v38L0 553Z" fill="url(#pht{i})" opacity=".55"/>']
    # A torn, contrasting print edge bleeds off the paper; deliberately not a banner.
    pts=' '.join(f'{x},{1734+int(54*math.sin((x+170*i)/410)+12*M.R(i+x))}' for x in range(-30,1121,27));r+=[f'<polygon points="-35,1950 {pts} 1140,1950" fill="{ink}" opacity=".18"/><g opacity=".20" stroke="{penc}" stroke-width="3"><path d="M887 -38l233 181 M925 -32l198 149 M960 -28l163 125"/></g>']
    return ''.join(r)

base_content=C.content

def rectplate(w,h,seed,iid,taped=True):
    d=C.torn(w,h,seed,4,23);edge=C.torn(w+20,h+18,seed+67,5,25)
    return f'<path d="{edge}" fill="#e4dac1" filter="url(#shd)"/><path d="{d}" fill="#faf6e6"/>'+(M.tape(w,h,seed) if taped else '')

def plate(it,A,iid,seed):
    if it['type']!='print':return base_content(it,A,iid,seed)
    w,h=it['w'],it['h'];key=it['plate'];s=''
    if key in ('uni','bi'):
        s=rectplate(w,h,seed,iid);focus=it['focus']
        for row,lab,dy in [(0,'الأيسر',-88),(1,'الأيمن',88)]:
            yy=dy-56;colored=(focus=='both' or (focus=='top' and row==0)); selected=colored or (focus=='lower' and row==1)
            # Labels name the EEG lead. Absolute signal scale stays identical across conditions.
            if selected:
                s+=f'<path d="{C.torn(760,123,seed+row,3,20)}" transform="translate(0 {dy})" fill="{"#f4d66a" if colored else "#bfdbcd"}"/>'
            for x in range(-367,212,42):s+=f'<path d="M{x} {yy}v114" stroke="#b7b3a2" stroke-width="1.6" opacity=".42"/>'
            s+=f'<svg x="-371" y="{yy}" width="580" height="112" viewBox="0 {64*row} 338 64" preserveAspectRatio="none" overflow="hidden"><image href="assets/eeg-{key}.png" x="0" y="0" width="338" height="128"/></svg><text class="axis" direction="rtl" text-anchor="middle" x="295" y="{dy+17}" font-family="Cairo" font-weight="850" font-size="49" fill="{INK}">{lab}</text>'
        s+='<path d="M-369 0 H360" stroke="#bab5a5" stroke-dasharray="7 8" stroke-width="2"/>'
    elif key=='skull':
        s=rectplate(w,h,seed,iid)+f'<image href="assets/skull.png" x="{-w*.48}" y="{-h*.43}" width="{w*.96}" height="{h*.86}"/>'
    elif key=='compare':
        s=rectplate(w,h,seed,iid)+f'<image href="assets/tracks.png" x="-390" y="-177" width="332" height="325"/><path d="M-21 -166l13 324" stroke="#d1bfa0" stroke-width="4" stroke-dasharray="10 13"/><image href="assets/eeg-uni.png" x="38" y="-110" width="346" height="220"/><path d="M-170 170 Q0 218 193 171" fill="none" stroke="{CORAL}" stroke-width="5" stroke-linecap="round"/> '
    elif key=='scraps':
        for j,(xx,yy,ang) in enumerate([(-283,15,-6),(-95,-15,8),(91,10,-8),(287,-16,6)]):
            s+=f'<g transform="translate({xx} {yy}) rotate({ang})"><g class="scrap"><path d="{C.torn(133,65,31+j,5,15)}" fill="{["#fff5d9",YEL,"#cb6749","#f8e59e"][j]}" filter="url(#shd)"/><path d="M-43 6 q29 -17 80 -4" stroke="{INK}" opacity=".55" stroke-width="4" fill="none"/></g></g>'
    elif key=='share':
        r=w*.41;circ=2*math.pi*r;s+=f'<circle r="{r+36}" fill="#1c3c43"/><circle r="{r}" stroke="#658a84" stroke-width="48" fill="none"/><circle r="{r}" stroke="{YEL}" stroke-width="48" fill="none" stroke-dasharray="{circ*.69/24:.3f} {circ*(1-.69/24):.3f}" transform="rotate(-90)"/>'
        for j in range(24):s+=f'<path d="M0 {-r+36:.1f}v{19 if j%6==0 else 8}" stroke="#c1cfc1" opacity=".82" stroke-width="3" transform="rotate({j*15})"/>'
    return s,w,h

base_enter=M.enter;base_loop=M.loop;base_svg=C.item_svg

def enter(kind,sel,at,tilt=0.,p=None):
    if kind=='park':return []
    return base_enter(kind,sel,at,tilt,p)
def loop(kind,sel,t0,t1,seed=0,p=None):
    if kind=='glide':return [M.tw(sel,M.T(23,13,2),M.T(-29,-24,-1),t0-.76,max(.4,t1-t0+.73),'sine.inOut')]
    if kind=='boil': # subtle 8-Hz print jitter; only the real bird gets it
        return [f'tl.set("{sel}",{{attr:{{transform:"{M.T(M.R(seed+j)*1.7,M.R(seed+93+j)*1.9,M.R(seed+41+j)*.48)}"}}}},{t0+j/8:.3f});' for j in range(max(1,int((t1-t0)*8)))]
    return base_loop(kind,sel,t0,t1,seed,p)

sweeps={'glide':('M877 1204 Q663 1332 338 1289 Q237 1279 192 1222',False),'query':('M189 1373 Q120 1224 237 1153 l-48 8 m48 -8 l-19 43',False),'wing':('M161 809 Q216 701 329 716 l-34 -22 m34 22 l-45 13',False),'flightpath':('M176 1369 Q611 1475 882 1144',False),'spiral':('M238 1390 C808 1455 934 1134 452 1129 C163 1126 205 1357 604 1210 C889 1094 803 923 488 948 C294 971 357 1097 595 989 Q764 902 699 790 m-7 39 l7 -39 l33 29',False),'mapbracket':('M231 801 L204 802 199 937 M201 1102 L205 1175 272 1178',False),'brace':('M147 980 Q119 975 132 1023 Q148 1072 108 1092 Q148 1111 133 1173 Q125 1211 151 1215',False),'share':('M823 675 Q771 554 610 644 l36 -1 m-36 1 l15 -35',False)}

def svg(it,A,bid,k,dark,s,js):
    if it['type']=='paper':return bgart(bid,E['beats'][bid]['bg'],E['beats'][bid]['motif'])
    if it['type']=='sweep':
        iid=f'i{bid}_{k}';t=s+it['at'];d=sweeps[it['shape']][0];color='#f5d363' if dark else CORAL
        js+=[f'tl.to("#{iid}",{{attr:{{"stroke-dashoffset":0}},duration:.86,ease:"power1.inOut"}},{t:.3f});'];return f'<path id="{iid}" d="{d}" pathLength="1" stroke-dasharray="1.01" stroke-dashoffset="1.01" fill="none" stroke="{color}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>'
    res=base_svg(it,A,bid,k,dark,s,js)
    if it.get('plate')=='scraps':js.append(f'tl.fromTo("#i{bid}_{k} .scrap",{{opacity:0,y:-44}},{{opacity:1,y:0,duration:.32,stagger:.25,ease:"back.out(1.2)"}},{s+.45:.2f});')
    return res

def text(it,bid,k,dark,s,js):
    iid=f'i{bid}_{k}';t=s+it.get('at',0);st=it['style'];msg=C.markup(html.escape(it['text']));darkfg='#fff2d2' if dark else INK;park=st in ('first','numberdark')
    if not park:js.append(f'tl.fromTo("#{iid}",{{opacity:0,y:25}},{{opacity:1,y:0,duration:.28,ease:"power3.out"}},{t:.3f});')
    elif st=='numberdark':js.append(f'tl.set("#{iid}",{{opacity:1}},{t:.3f});')
    if '[y]' in it['text']:js.append(f'tl.fromTo("#{iid} .mk",{{backgroundSize:"0% 43%"}},{{backgroundSize:"100% 43%",duration:.48,ease:"power2.inOut"}},{t+.25:.3f});')
    return f'<div class="headline {st}" id="{iid}" style="top:{it["y"]}px;font-size:{it["size"]}px;text-align:{it.get("align","center")};color:{darkfg};opacity:{1 if st=="first" else 0}"><span class="word">{msg}</span></div>'

def create():
    # C.build handles the two alternating tracks, native torn-paper transitions, SVG items,
    # locally loaded GSAP and the HyperFrames timeline. Only film-specific print types differ.
    for i,b in enumerate(E['beats']):
        st,e,_=sch[i]; b['items'].insert(0,{'type':'paper'});b['halftone']=False
        for it in b['items']:it['until']=e-st
        timeline['shots'].append(dict(start=cuts[i],end=cuts[i+1],cue=b['cue'],bg=b['bg'],transition=b['transition'],note=b['direction']))
    with ExitStack() as ctx:
        for obj,prop,val in [(M,'enter',enter),(M,'loop',loop),(C,'item_svg',svg),(C,'item_html',text),(C,'content',plate),(C,'PAPER',PAP),(C,'DARK_BG',{'blue','night'})]:ctx.enter_context(patch.object(obj,prop,val))
        C.build(E,A,sch,D,str(P))
    p=P/'index.html';h=p.read_text();h=re.sub(r'<rect width="1080" height="1920" filter="url\(#grain\)" opacity="[^"]+"/>','',h)
    css='''.headline{position:absolute;left:95px;right:95px;line-height:1.39;white-space:nowrap;direction:rtl;font-weight:900}.headline .word{display:inline-block;padding:0 3px}.headline .mk{background-position:100% 83%;padding:0 6px}.headline.label .word,.headline.bright .word,.headline.strip .word,.headline.numberdark .word{padding:1px 27px 9px;line-height:1.36}.headline.label .word{background:#193a3c;color:#fff4d5;box-shadow:9px 11px 0 #ca5136}.headline.bright .word{background:#ffce36;color:#17343a;box-shadow:9px 9px 0 #0d242a}.headline.strip .word{background:#fbf5dd;color:#18373a;box-shadow:7px 8px 0 #3c5c5450}.headline.numberdark .word{color:#ffd141}.headline.light{color:#fff4d9}.axis{font-family:Cairo,sans-serif}.first .word{font-weight:950}''';h=h.replace('</style>',css+'</style>');h=h.replace('font-weight:200 1000;font-display:block;}','font-weight:200 1000;font-display:block;unicode-range:U+0000-00FF,U+2000-206F;}');p.write_text(h)
    (P/'timeline.json').write_text(json.dumps(timeline,ensure_ascii=False,indent=2)+'\n')

def stage(dest):
    q=Path(dest);q.mkdir(exist_ok=True,parents=True)
    for v in ['index.html','gsap.min.js']:shutil.copy2(P/v,q/v)
    for v in ['assets','fonts']:shutil.copytree(P/v,q/v,dirs_exist_ok=True)

def preview():
    out=P/'out';out.mkdir(exist_ok=True);times=','.join(f'{s+(e-s)*.7:.3f}' for s,e,_ in sch)
    with tempfile.TemporaryDirectory() as t:
        stage(t);subprocess.run(['hyperframes','lint',t],check=True);subprocess.run(['hyperframes','snapshot','--at',times,'--no-end','-o',str(out/'snaps'),t],check=True)
    sheets=sorted((out/'snaps').glob('contact*'));[shutil.copy(f,out/f'sheet{k+1}.jpg') for k,f in enumerate(sheets)]
if __name__=='__main__':
    create();print('shot frames:',cuts,flush=True)
    if '--stage' in sys.argv:stage(sys.argv[sys.argv.index('--stage')+1])
    if '--preview' in sys.argv:preview()
