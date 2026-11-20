"""Human-corrected Arabic, segmented at phrase onsets from voice/words.json (seconds)."""
from pathlib import Path
import json, textwrap, re
p=Path(__file__).resolve().parents[1];ls=json.loads((p/'lines.json').read_text());cues=[[(None,'هذا الوجه السومري خرج من تحت التراب مرتين.'),(4.44,'في المرة الثانية، لم تكن حفرية آثار.')],[(None,'انظر إلى العينين الفارغتين.'),(11.26,'هذا قناع الوركاء،'),(13.05,'نُحت قبل نحو خمسة آلاف سنة.')],[(None,'في ثلاثينيات القرن الماضي،'),(19.08,'اكتشفت بعثة تنقيب القناع في أوروك،'),(21.97,'جنوب العراق.')],[(None,'وبقي في المتحف العراقي في بغداد'),(26.12,'حتى نيسان عام ألفين وثلاثة.'),(29.37,'نُهب المتحف، واختفى القناع.')],[(None,'بعد شهور، دخل عراقيّ المتحف'),(35.55,'بمعلومة عن آثار مخبّأة.'),(37.92,'لم يذكر القناع.')],[(None,'قاد البلاغ المحقّقين إلى مزرعة شماليّ بغداد.'),(43.52,'وهناك، دلّهم صاحبها على موضع خلف المزرعة.')],[(None,'تحت التراب، كان الوجه سليمًا.'),(50.62,'وفي أيلول من العام نفسه، عاد إلى المتحف.')],[(None,'خرج من تحت التراب مرتين.'),(56.92,'أيّ الاكتشافين أدهشك أكثر؟')]]
def ts(x):
 n=round(x*1000);return f'{n//3600000:02d}:{n//60000%60:02d}:{n//1000%60:02d},{n%1000:03d}'
ss=[]
for row,tt in zip(ls,cues):
 assert ' '.join(q for _,q in tt)==row['text']; end=row['at']+row['duration'];
 for j,(st,q) in enumerate(tt):
  st=row['at'] if st is None else st;et=tt[j+1][0] if j+1<len(tt) else end;assert 0<et-st<7
  lines=textwrap.wrap(q, width=41, break_long_words=False, break_on_hyphens=False)
  if len(lines)==2 and len(lines[-1])<11:
   ww=q.split();k=min(range(1,len(ww)),key=lambda z:abs(len(' '.join(ww[:z]))-len(' '.join(ww[z:])))); lines=[' '.join(ww[:k]),' '.join(ww[k:])]
  ss.append(f'{len(ss)+1}\n{ts(st)} --> {ts(et)}\n'+'\n'.join(lines))
(p/'warka-mask.srt').write_text('\n\n'.join(ss)+'\n')
