# studio-kit
- `ملف صناعة الفيديوهات.md` (في جذر المستودع): تعليمات الـ Agent (4 أساليب).
- `make.py`: أمر واحد لكل الأساليب: 1 وثائقي · 2 Vox كولاج · 3 رجل العود السينمائي · 4 ألغاز saw.
- `engines/`: محرّكا الأسلوبين 1 و3، ومُركِّب الشخصيات `characters.py`. اقرأ `engines/README.md` و`engines/CATALOG.md`.
- `collage/`: محرّك الأسلوب 2. · `series/saw_5tory/`: الأسلوب 4.
- `topics/`: مجالات الحساب الثابتة (`ACCOUNT.md`) والقنوات والحسابات المرجعية (`channels.json`، `social.md`).
- `scripts/`: الصوت (`voice.py`، `tts_edge.py`)، الصور (`images.py`)، الموسيقى والمؤثرات والدمج، `trends.py` (مشاهدات حقيقية)، `remote.py` (الجلب عن طريق GitHub)، `doctor.sh`.
- `assets/`: الخطوط ومكتبة الحركة المشتركة.

مهمة **Remote fetch** على GitHub تجلب الصور والصوت ومشاهدات يوتيوب تلقائيًا حين تحجبها بيئة الـ Agent. مفتاح Pixabay محفوظ في **Repository secrets** باسم `PIXABAY_KEY`، ولا يُكتب في أي ملف.
