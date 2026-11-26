# studio-kit
- `ملف صناعة الفيديوهات.md` (في جذر المستودع): تعليمات الـ Agent (10 أساليب).
- `make.py`: أمر واحد لكل الأساليب: 1 وثائقي · 2 Vox كولاج · 3 Vox رسوم · 4 نصوص متحركة · 5 ثلاثي الأبعاد · 6 ورق مقصوص · 7 رجل العود السينمائي · 8 أنمي · 9 كرتون · 10 ألغاز saw.
- `engines/`: محرّكات الأساليب 1 و3–9، ومُركِّب الشخصيات `characters.py`، والخرائط والجيوش `war.py`. اقرأ `engines/README.md` و`engines/CATALOG.md`.
- `collage/`: محرّك الأسلوب 2. · `series/saw_5tory/`: الأسلوب 10.
- `topics/`: مجالات الحساب الثابتة (`ACCOUNT.md`) والقنوات والحسابات المرجعية (`channels.json`، `social.md`).
- `scripts/`: الصوت (`voice.py`، `tts_edge.py`)، الصور (`images.py`)، الموسيقى والمؤثرات والدمج، `trends.py` (مشاهدات حقيقية)، `remote.py` (الجلب عن طريق GitHub)، `doctor.sh`.
- `assets/`: الخطوط ومكتبة الحركة المشتركة.

مهمة **Remote fetch** على GitHub تجلب الصور والصوت ومشاهدات يوتيوب تلقائيًا حين تحجبها بيئة الـ Agent. مفتاح Pixabay محفوظ في **Repository secrets** باسم `PIXABAY_KEY`، ولا يُكتب في أي ملف.
