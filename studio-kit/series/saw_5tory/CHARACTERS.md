# شخصيات saw_5tory

صورة كل الشخصيات الجاهزة: `CHARACTERS.jpg`. الكود: `people.py` (يستخدمه `props.person`).

## 1. شخصية جاهزة (الأسرع)
```json
{"type": "person", "id": "reem", "x": 560, "y": 1540, "name": "ريم", "cast": "artist_f", "expression": "nervous"}
```
أي مفتاح تضيفه يغيّر الشخصية الجاهزة (مثلًا `"coat": "#2f5a7a"` أو `"pose": "crossed"`).

| cast | الوصف |
|---|---|
| young_man | شاب بمعطف |
| businessman | رجل أعمال، وجه مربع، لحية خفيفة، ساعة |
| sheikh | شيخ كبير، ثوب وشماغ، لحية بيضاء، عصا |
| gulf_youth | شاب خليجي، ثوب وشماغ، يتكلم بالهاتف |
| guard | حارس كبير، بطن، شارب، زي رسمي |
| chef | طاهٍ، وجه دائري، مريلة |
| student | طالب، شعر مجعد، سماعات، حقيبة |
| mechanic | ميكانيكي، عريض، لحية، ذراعان متشابكتان |
| doctor_f | طبيبة، معطف أبيض، يدان في الجيب |
| hijabi_young | شابة بحجاب وسترة |
| hijabi_pro | موظفة بحجاب وبدلة |
| abaya_lady | سيدة بعباءة سوداء وحقيبة |
| grandma | جدة، شعر أبيض، قلادة |
| artist_f | فنانة، شعر مموج أحمر، أقراط، وشاح |
| maid | عاملة منزل، ذيل حصان، مريلة |
| athlete_f | رياضية، ضفيرة، قبعة |
| professor | أستاذ كبير، أصلع، نظارة، صدرية |
| bodybuilder | رياضي ضخم، شعر موهوك |
| taxi_driver | سائق أجرة، بطن، قبعة |
| nurse | ممرضة بحجاب وكمامة |
| teen_gamer | مراهق، هودي، سماعات، هاتف |
| fisherman | صياد كبير، قبعة صوف، لحية |
| detective_f | امرأة بمعطف وقبعة فيدورا |
| child | طفل (شاهد فقط، لا يُتهم ولا يُؤذى) |

## 2. شخصية جديدة من الصفر (تركيب الأشكال)
| المفتاح | القيم |
|---|---|
| `gender` | m · f |
| `age` | child · young · adult · old |
| `face` | oval · round · square · long · heart · wide · diamond |
| `eyes` | normal · round · narrow · big · droopy · sharp (`iris` لون القزحية مع big) |
| `nose` | line · button · long · wide · hook |
| `brows` | thin · normal · thick · bushy |
| `hair_style` | spiky · short · side_part · buzz · curly · long · wavy · ponytail · braid · bun · bald · receding · mohawk · hijab · shemagh |
| `hair` | لون الشعر |
| `facial` | beard · mustache · stubble |
| `outfit` | coat · suit · thobe · abaya · uniform · sweater · hoodie · dress · apron · labcoat · vest · tshirt |
| `coat` / `accent` | لون اللباس / لون ثانوي (ربطة، حجاب، وشاح، قبعة) |
| `skin` | pale · light · medium · tan · brown · dark أو لون |
| `build` | normal · broad · slim · stocky · pear · belly |
| `body` | tall · short (الطول) |
| `pose` | down · crossed · pockets · hip · phone · point |
| `expression` | neutral · nervous · smug · scared · angry · happy |
| `accessories` | cap · fedora · beanie · headphones · earrings · scarf · necklace · watch · cane · bag · badge · mask_medical · glasses |
| حالات الدليل | `wet` (مبلل كله) · `shoes`: wet / mud · `glasses` + `fog` |

عدد التركيبات بالآلاف. **قاعدة:** لا تكرر نفس الوجه + الشعر + اللباس لمتهم في قضيتين متتاليتين، وسجّل الهيئة في `SAW_HISTORY.md`. لا تجعل التعبير يفضح الحل (الكاذب ليس دائمًا «nervous»). الطفل لا يكون متهمًا ولا ضحية.
