from pathlib import Path
import subprocess as sp
from PIL import Image,ImageDraw
p=Path(__file__).resolve().parents[1];kit=p.parents[1]/'studio-kit/scripts/cover_check.py';o=p/'out';qa=p/'qa';qa.mkdir(exist_ok=True)
proof=Image.new('RGB',(2*322,592),'#244448');d=ImageDraw.Draw(proof)
for i,n in enumerate(['thumbnail','thumbnail-b']):
 im=Image.open(o/(n+'.png')).convert('RGB');assert im.size==(1080,1920);ex=Image.Exif();ex[270]=('Great frigatebird in flight. NOAA Photo Library / NOAA NMFS/PIFSC, CC BY 2.0 https://creativecommons.org/licenses/by/2.0/ plus Jon Sullivan / PDPhoto, public domain; cut out, regraded, collaged. See CREDITS.' if not i else 'Bryson Voirin photograph and Rattenborg et al. (2016) fig. 2b EEG, doi:10.1038/ncomms12468, CC BY 4.0 https://creativecommons.org/licenses/by/4.0/. Cropped, recoloured, annotated, paper collage.');im.save(p/(n+'.jpg'),quality=94,exif=ex);q=Image.open(p/(n+'.jpg'));proof.paste(q.resize((320,569),Image.Resampling.LANCZOS),(322*i,0));d.text((322*i+5,572),'B' if i else 'A',fill='white');sp.run(['python3',str(kit),str(p/(n+'.jpg'))],check=True);(p/(n+'_check.jpg')).replace(o/(n+'_check.jpg'))
proof.save(qa/'covers-320.jpg',quality=94)
