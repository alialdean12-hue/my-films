"""Photographic print grades of NARA 6648802, not generative upscaling or restoration.
presentation.jpg is a 257×170 crop of the 610×517 reproduction: (139,320,396,490).
It keeps the real fingers that cover parts of the stone. Never infer the hidden outline.
"""
from pathlib import Path
from PIL import Image,ImageOps,ImageFilter
import numpy as np
p=Path(__file__).resolve().parents[1]/'img';src=Image.open(p/'presentation.jpg').convert('RGB');assert src.size==(257,170)
def print_photo(image,size,name,colour):
 im=image.resize(size,Image.Resampling.LANCZOS).filter(ImageFilter.UnsharpMask(2.4,80,3));g=ImageOps.autocontrast(im.convert('L'),cutoff=.65);ink=ImageOps.colorize(g,black='#1c1b18',white='#fff5dc',mid='#a69c88');photo=Image.blend(ink,im,colour)
 # Fine screened grain on the enlarged archive print; no AI repair, added eyes, or redrawn contours.
 v=np.array(photo,dtype='float32');y,x=np.indices(v.shape[:2]);d=2.4*np.cos((.94*x+.35*y)*2*np.pi/6.3)*np.cos((-.35*x+.94*y)*2*np.pi/6.3);Image.fromarray(np.uint8(np.clip(v+d[:,:,None],0,255))).save(p/name,quality=94)
print_photo(src,(1028,680),'mask.jpg',.46)
print_photo(src.crop((69,12,203,159)),(670,735),'portrait.jpg',.50)
