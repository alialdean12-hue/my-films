# شخصيات saw_5tory

صور الشخصيات: `CHARACTERS.jpg` (24 شخصية) و`PROFESSIONS_1.jpg` … `PROFESSIONS_3.jpg` (105 مهن). الكود: `people.py` (يستخدمه `props.person`).

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
| `outfit` (45) | abaya · apron · astronaut · bisht · blazer · butler · cardigan · chef_coat · coat · delivery · dress · firefighter · galabeya · graduate · hivis · hoodie · jersey · judge · karate · lab_tech · labcoat · leather · overalls · patient · pilot · police · polo · postal · prisoner · puffer · raincoat · scrubs · shirt_tie · soldier · suit · sweater · tank · thobe · tracksuit · trench · tshirt · turtleneck · uniform · vest · waiter |
| `coat` / `accent` | لون اللباس / لون ثانوي (ربطة، حجاب، وشاح، قبعة) |
| `skin` | pale · light · medium · tan · brown · dark أو لون |
| `build` | normal · broad · slim · stocky · pear · belly |
| `body` | tall · short (الطول) |
| `pose` | down · crossed · pockets · hip · phone · point |
| `expression` | neutral · nervous · smug · scared · angry · happy |
| `accessories` (88) | cap · fedora · beanie · headphones · earrings · mask_medical · glasses · scarf · necklace · watch · cane · bag · badge · police_cap · pilot_cap · chef_hat · hard_hat · fire_helmet · grad_cap · beret · turban · kufi · top_hat · cowboy_hat · bandana · nurse_cap · headscarf · hairclip · flower_hair · sweatband · goggles_head · straw_hat · sailor_cap · crown_paper · sunglasses · eyepatch · monocle · scar · freckles · mole · bandage_face · earpiece · nose_ring · makeup · round_glasses · sunglasses_head · bow_tie · tie · stethoscope · lanyard · medal · whistle · camera · pin · suspenders · toolbelt · backpack · wristband · apron_half · name_tag · sash · briefcase · clipboard · wrench · magnifier · coffee · book_hand · keys · umbrella_hand · walkie · microphone · paintbrush · broom · shopping_bag · newspaper_hand · misbaha · flowers · laptop · tray · ball · measuring_tape · comb · scissors · trophy · lantern · map · tablet · gloves |

الأشياء المحمولة باليد (مثل briefcase, magnifier, coffee, broom, microphone…) تظهر فقط مع الوضعيات down / hip / phone / point.
| حالات الدليل | `wet` (مبلل كله) · `shoes`: wet / mud · `glasses` + `fog` |

عدد التركيبات بالآلاف. **قاعدة:** لا تكرر نفس الوجه + الشعر + اللباس لمتهم في قضيتين متتاليتين، وسجّل الهيئة في `SAW_HISTORY.md`. لا تجعل التعبير يفضح الحل (الكاذب ليس دائمًا «nervous»). الطفل لا يكون متهمًا ولا ضحية.


## 3. المهن الجاهزة (105)
استخدمها مثل الشخصيات الجاهزة: `"cast": "police_officer"`.

| cast | المهنة |
|---|---|
| police_officer | شرطي |
| police_f | شرطية |
| firefighter | رجل إطفاء |
| pilot | طيار |
| flight_attendant_f | مضيفة طيران |
| soldier | جندي |
| surgeon | جرّاح |
| nurse_m | ممرض |
| pharmacist_f | صيدلانية |
| dentist | طبيب أسنان |
| paramedic | مسعف |
| doctor_m | طبيب |
| vet_f | طبيبة بيطرية |
| baker | خبّاز |
| chef_f | طاهية |
| waiter | نادل |
| butler | خادم قصر |
| barista_f | باريستا |
| judge | قاضٍ |
| lawyer_f | محامية |
| lawyer_m | محامٍ |
| teacher_f | معلمة |
| teacher_m | معلم |
| graduate_f | خرّيجة |
| scientist | عالم |
| astronaut | رائد فضاء |
| engineer | مهندس |
| construction | عامل بناء |
| electrician | كهربائي |
| plumber | سبّاك |
| farmer | مزارع |
| sailor | بحّار |
| ship_captain | قبطان |
| photographer | مصوّر |
| journalist_f | صحفية |
| tv_anchor | مذيع |
| painter | رسّام |
| musician | موسيقي |
| singer_f | مطربة |
| dj | دي جي |
| footballer | لاعب كرة |
| karate_master | مدرّب كاراتيه |
| referee | حكم |
| coach | مدرّب |
| lifeguard | منقذ |
| fitness_trainer_f | مدرّبة لياقة |
| bus_driver | سائق حافلة |
| delivery | عامل توصيل |
| postman | ساعي بريد |
| security | حارس أمن |
| prisoner | سجين |
| patient | مريض |
| elderly_patient | مريضة مسنّة |
| librarian_f | أمينة مكتبة |
| banker | مصرفي |
| ceo_f | مديرة شركة |
| secretary | سكرتير |
| receptionist_f | موظفة استقبال |
| hotel_manager | مدير فندق |
| cleaner | عامل نظافة |
| cleaner_f | عاملة نظافة |
| gardener | بستاني |
| tailor | خيّاط |
| barber | حلّاق |
| shopkeeper | صاحب دكان |
| jeweler | صائغ |
| detective_m | محقق |
| spy | جاسوس |
| investigator_f | محققة خاصة |
| psychologist | طبيب نفسي |
| tourist | سائح |
| hiker_f | متسلّقة |
| rich_heir | وريث ثري |
| old_merchant | تاجر عجوز |
| villager | قروي |
| bedouin | بدوي |
| gulf_dad | أب خليجي |
| grandpa | جدّ |
| influencer_f | مؤثرة |
| streamer | صانع محتوى |
| programmer | مبرمج |
| architect_f | مهندسة معمارية |
| fashion_designer | مصمم أزياء |
| magician | ساحر |
| actor | ممثل |
| cashier_f | كاشيرة |
| car_salesman | بائع سيارات |
| realtor_f | وسيطة عقارات |
| park_ranger | حارس محمية |
| zookeeper_f | حارسة حديقة الحيوان |
| museum_guard | حارس متحف |
| train_conductor | مفتّش قطار |
| courier_biker | سائق دراجة |
| nanny_f | مربية |
| neighbor_f | جارة |
| lab_tech_f | فنية مختبر |
| forensic | خبير أدلة جنائية |
| rookie_detective | محقق مبتدئ |
| street_vendor | بائع متجول |
| night_watchman | حارس ليلي |
| taxi_f | سائقة أجرة |
| student_f | طالبة جامعية |
| pharmacist_m | صيدلي |
| mayor | عمدة |
| chess_player | لاعب شطرنج |
