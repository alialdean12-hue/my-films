"""Printing plates made only from the credited photographs and published figure pixels.
Native photo cut-outs are kept in assets/; --recut is optional and needs rembg/u2netp.
"""
from pathlib import Path
import math, sys
import numpy as np
from PIL import Image, ImageDraw, ImageOps, ImageFilter
from scipy.ndimage import distance_transform_edt, maximum_filter, median_filter
P=Path(__file__).resolve().parents[1]; S=P/'img/source'; A=P/'assets'; A.mkdir(exist_ok=True)
sys.path.insert(0,str(P.parents[1]/'studio-kit/collage'))
import cutout
INK='#16383e'; RED='#b94236'; YELLOW='#ffcf39'

def cut():
    cutout.sticker(S/'flight-noaa.jpg',A/'soar.png',8,1500,'u2netp')
    cutout.sticker(S/'voirin.png',A/'tagged.png',6,900,'u2netp')

def clean_sky():
    # The model leaves a small triangular pocket of blue sky BETWEEN the wings.
    # Local colour key on the photographic pixels, never a hand-painted bird.
    im=Image.open(A/'soar.png').convert('RGBA'); a=np.array(im); r,g,b=a[:,:,:3].astype('int16').transpose(2,0,1); y,x=np.indices(r.shape)
    mask=(x>98)&(x<257)&(y>260)&(y<507)&(b-r>24)&(b-g>10)&(r>65)&(g>88)&(a[:,:,3]>100)
    if mask.any():
        near=distance_transform_edt(mask);a[:,:,:3]=np.where(((near>0)&(near<6))[:,:,None],np.array([250,248,240]),a[:,:,:3]);a[:,:,3]=np.where(near>6,0,a[:,:,3])
    Image.fromarray(a).save(A/'flight.png')

def plates():
    # Regrade contextual ocean only. The documentary birds are not recoloured.
    ocean=Image.open(S/'wave.jpg').convert('RGB'); ocean=ImageOps.colorize(ImageOps.autocontrast(ImageOps.grayscale(ocean),1),'#123b49','#c6e0d8');ocean.save(A/'ocean.jpg',quality=94)
    bird=Image.open(S/'flight-noaa.jpg');bird.crop((280,55,1340,966)).save(A/'sky.jpg',quality=95)
    cutout.card(S/'genovesa.jpg',A/'colony.jpg')
    real=Image.open(S/'voirin.png').convert('RGB');real.crop((76,144,265,261)).save(A/'head.jpg',quality=98);real.crop((168,116,398,247)).save(A/'back.jpg',quality=98)
    img=Image.open(S/'figure1.jpg').convert('RGB');chart=np.array(img.crop((41,453,299,681)),dtype=float); h,w=chart.shape[:2]; y,x=np.indices((h,w));rgb=chart.max(2)-chart.min(2)
    # Isolate the actual coloured tracks. Keep the shapes and relative locations;
    # omit ridge labels and depth key instead of pretending to reproduce bathymetry.
    paths=np.clip((rgb-10)/48,0,1);paths=.82*paths+.18*maximum_filter(paths,size=2);hsv=np.array(Image.fromarray(chart.astype('uint8')).convert('HSV'))[:,:,0];warm=(hsv<62)|(hsv>185)
    coast=(x>4)&(x<78)&(y>139)&(y<216)&(x*.71+y>151); islands=np.clip((153-chart.mean(2))/99,0,1)*coast*(1-paths)
    relief=median_filter(chart.mean(2),size=11)/255
    paper=np.zeros_like(chart)+np.array([232,231,207]);paper+=(relief[:,:,None]-.48)*[22,26,23];paper-=islands[:,:,None]*[126,107,83];dark=np.zeros_like(chart)+[162,66,49]
    for lo,hi,c in [(15,45,[163,115,38]),(45,95,[44,105,68]),(95,146,[27,94,116]),(146,201,[81,75,129]),(201,241,[155,76,100])]:dark[(hsv>=lo)&(hsv<hi)]=c
    paper=paper*(1-paths[:,:,None])+dark*paths[:,:,None]
    im=Image.fromarray(np.uint8(np.clip(paper,0,255))).resize((774,684),Image.Resampling.LANCZOS); im.save(A/'tracks.png');
    skull=img.crop((15,300,340,399)).convert('L');arr=np.array(ImageOps.invert(skull)).astype(float);alpha=np.uint8(np.clip((arr-10)*1.24,0,255));out=Image.new('RGBA',skull.size,INK);out.putalpha(Image.fromarray(alpha));out.save(A/'skull.png');
    fig=Image.open(S/'figure2.jpg').convert('L');
    for key,x0 in [('uni',446),('bi',73)]:
        # Fig. 2b, 25 s excerpt. Skip coloured outlines; same scaling for ALL rows.
        z=fig.crop((x0,868,x0+338,996));density=np.array(z).astype(float);alpha=np.uint8(np.clip((250-density)*1.7,0,255));im=Image.new('RGBA',z.size,INK);im.putalpha(Image.fromarray(alpha));im.save(A/f'eeg-{key}.png')
    # Deliberately static, cheap-to-render paper: grain, sparse pulp fibres & halftone.
    rng=np.random.default_rng(2907);w=h=256;noise=rng.normal(0,4.7,(h,w));yy,xx=np.indices(noise.shape);dots=(((xx+4)%13-6)**2+((yy+1)%13-6)**2<4)*10
    for k,col in {'cream':(243,231,203),'oat':(224,202,164),'sea':(184,211,202),'blue':(29,67,76),'night':(25,45,51),'white':(246,241,222),'yellow':(244,201,84)}.items():
        data=np.uint8(np.clip(np.array(col)+(noise-dots)[:,:,None],0,255));im=Image.fromarray(data);d=ImageDraw.Draw(im);rg=np.random.default_rng(529)
        for _ in range(65):
            x,y=rg.integers(0,256,2);delta=int(rg.choice([-1,1]))*8;d.line((x,y,x+int(rg.integers(2,9)),y+1),fill=tuple(np.uint8(np.clip(np.array(col)+delta,0,255))))
        im.save(A/f'paper-{k}.jpg',quality=87)
if __name__=='__main__':
    if '--recut' in sys.argv:cut()
    clean_sky();plates()
