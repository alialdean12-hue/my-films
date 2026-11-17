"""Colour script and separations for seven ORIGINAL illustrated plates; never imports archive footage.
Source WebPs are the lossless studio paintings. All plates used on screen are indexed to this palette.
"""
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
P=Path(__file__).resolve().parents[1]
COLORS=['#101a32','#263653','#486886','#99ced2','#51cbd3','#f3eee1','#ea8253','#f2bd96','#b97972','#f7cf76']
INK,NAVY,SLATE,ICE,AQUA,IVORY,CORAL,SKIN,ROSE,GOLD=COLORS
pal=[[int(c[i:i+2],16) for i in (1,3,5)] for c in COLORS]
def read(name):return Image.open(P/'assets/paint'/f'{name}.webp').convert('RGB')
def remap(im,mask=None,limit=None):
    src=np.array(im,dtype='float32'); idx=np.empty(src.shape[:2],dtype='uint8'); tone=np.array(pal,dtype='float32'); weight=np.array([.95,1.1,.94],dtype='float32')
    for top in range(0,len(src),96):
        a=src[top:top+96]; dd=((a[:,:,None,:]-tone[None,None,:,:])*weight)**2;dd=dd.sum(axis=-1)
        if limit:
            for k in set(range(10))-set(limit): dd[:,:,k]=1e9
        idx[top:top+96]=np.argmin(dd,axis=-1)
    if mask is not None:idx[np.array(mask)<128]=10
    out=Image.fromarray(idx).convert('P');out.putpalette([v for e in pal for v in e]+[0]*(768-3*len(pal)))
    if mask is not None:out.info['transparency']=10
    return out
def save(name,im,mask=None,limit=None):remap(im,mask,limit).save(P/'img'/f'{name}.png',optimize=True,bits=4)
def solid(m,seed):
    # Keep only the contiguous object. Fill enclosed ink details rather than keying the fabric ink away.
    a=m.copy(); ImageDraw.floodfill(a,seed,127); b=Image.fromarray(np.where(np.array(a)==127,255,0).astype('uint8'))
    pad=Image.new('L',(b.width+2,b.height+2));pad.paste(b,(1,1));ImageDraw.floodfill(pad,(0,0),127)
    return Image.fromarray(np.where(np.array(pad)[1:-1,1:-1]==127,0,255).astype('uint8'))
def main():
    for name in ['cabin','earth','desk','sink']:save(name,read(name))
    for source,name in [('character','astronaut'),('observe','observe')]:
        c=read(source); a=np.array(c,dtype='int16'); r,g,b=a.transpose(2,0,1); mask=Image.fromarray((~((g-r>24)&(g-b>18)) * 255).astype('uint8'));save(name,c,mask,[0,1,2,3,5,7,8,9]);
    h=read('wring'); a=np.array(h,dtype='int16');r,g,b=a.transpose(2,0,1); skin=(r>g+12)&(r>b+14)&(r>103)
    # Trim each grip to the actual ink silhouette, keeping the thumb and negative space.
    for name,box,poly in [('grip-left',(0,531,249,880),[(0,572),(47,556),(67,537),(118,544),(125,555),(178,543),(196,566),(226,632),(223,716),(241,742),(246,779),(229,815),(170,843),(137,832),(130,797),(94,791),(63,842),(0,878)]),('grip-right',(497,543,768,932),[(501,736),(521,626),(538,584),(577,555),(600,554),(614,565),(644,558),(670,567),(687,567),(768,588),(768,932),(729,907),(643,892),(577,869),(527,819),(508,785)] )]:
        region=Image.new('L',h.size); ImageDraw.Draw(region).polygon(poly,fill=255); m=(skin&(np.array(region)>0)).astype('uint8')*255
        m=Image.fromarray(m).filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.MinFilter(5)); save(name,h.crop(box),solid(m,(100,668) if name.endswith("left") else (680,700)).crop(box),[0,1,2,5,7,8,9]);
    # Clean separation of the reference folds + water sleeve (only the object, no torso or faces).
    reg=Image.new('L',h.size); ImageDraw.Draw(reg).polygon([(193,627),(261,595),(315,624),(366,594),(419,596),(475,622),(533,604),(582,618),(622,679),(632,748),(619,773),(545,759),(493,753),(466,768),(422,781),(348,768),(304,779),(237,769),(200,781)],fill=255)
    m=(((b>=r-12)&(g>=r-12)&(g>104)) & (np.array(reg)>0)).astype('uint8')*255
    m=Image.fromarray(m).filter(ImageFilter.MaxFilter(7)).filter(ImageFilter.MinFilter(3));box=(193,590,634,786); save('wet-folds',h.crop(box),solid(m,(395,699)).crop(box),[0,1,2,3,4,5]);
if __name__=='__main__':main()
