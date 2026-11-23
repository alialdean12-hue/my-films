# studio-kit
- `ملف صناعة الفيديوهات.md` : الصقه في تعليمات الـ Agent (9 أساليب).
- `engines/` : محرّكات جاهزة للأساليب 1 و3 و4 و5 و6 و7 و9 (ملف JSON → فيديو). اقرأ `engines/README.md`.
- `styles/<style>/` : قوالب جاهزة تعمل كما هي (انسخها ثم عدّل النص والتوقيت).
- `scripts/` : tts_edge.py (صوت) · sfx_lib.py (مؤثرات) · mix.py (دمج) · pixabay.py (لقطات) · render.sh (إخراج).
- `anime/` : مولّد الأنمي ومؤثراته.
ضع المجلد في `~/my-films/studio-kit/`. يحتاج: node 22+، ffmpeg، pip install edge-tts numpy.
قالب vox-real يحتاج لقطة (assets/v1c.mp4) وصورة (img/p1.jpg): ولّدهما بـ pixabay.py.

## اختبار البحث في Pixabay

- احفظ المفتاح في **Repository secrets** باسم `PIXABAY_KEY`. لا تلصقه في ملف البحث أو وصف المهمة.
- مهمة **Remote fetch** على GitHub تجلب الصور (ويكيميديا وPixabay) والصوت (edge-tts) تلقائيًا حين تحجبها بيئة الـ Agent: المحركات تطلبها بنفسها وتنتظر 1-3 دقائق. الملفات: `scripts/remote.py` و`scripts/voice.py` و`.github/workflows/remote.yml`.
- في ملخّص التشغيل تجد روابط صفحات Pixabay، لا المفتاح ولا روابط الملفات المؤقتة. الاختبار يقرأ بداية معاينة واحدة من كل نوع ولا ينشر ملفات الوسائط في المستودع. النتائج تُعاد من الذاكرة المؤقتة لمدة 24 ساعة، ويُذكر صراحةً إن لم يُختبر المفتاح مجددًا.
