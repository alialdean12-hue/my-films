# الأشياء المتحركة والحيوانات والنباتات والأجواء

صور: `THINGS_1.jpg` (مركبات وأشياء متحركة) · `THINGS_2.jpg` (حيوانات) · `THINGS_3.jpg` (نباتات) · `THINGS_4.jpg` (أجواء). الكود: `things.py`.
كل شيء يتحرك تلقائيًا (عجلات تدور، ذيل يهتز، أوراق تتمايل، رمش، أضواء شرطة…). أضفه في `room.objects` مثل أي شيء آخر.

## 1. مركبات وأشياء متحركة
| type | المفاتيح |
|---|---|
| `vehicle` | `kind`: sedan · taxi · police (أضواء تومض) · ambulance · pickup · truck · bus · van · `color` · `s` · `flip` · `moving` (تعبر الشاشة وعجلاتها تدور) |
| `motorcycle` · `bicycle` · `shopping_cart` (`full`) · `wheelchair` · `suitcase` · `stroller` | `x, y, s, flip, moving` |
| `ceiling_fan` (y = السقف) · `desk_fan` · `washing_machine` · `record_player` | `on` (يدور) |
| `pendulum_clock` (`time`) · `swinging_lamp` (y = السقف) · `rocking_chair` · `flag` (`text`, `color`) · `windmill` | تتأرجح أو تدور |
| `ball` (`moving`) · `passing_train` (`y` خلفية) · `door_creak` (x,y أعلى يسار الباب) · `curtain_blow` (x,y أعلى يسار النافذة) | |

## 2. حيوانات (كلها تتحرك وترمش)
| type | المفاتيح |
|---|---|
| `cat` | `color` · `state`: awake · asleep · wet · arched |
| `dog` | `breed`: guard · small · saluki · spotted · `state`: awake · asleep · barking · muddy |
| `bird` | `kind`: sparrow · crow · parrot · pigeon · falcon · owl · `flying` (يطير عبر الشاشة) |
| `horse` · `camel` (`sitting`) · `goat` (`sheep: true` خروف) · `chicken` · `rabbit` · `turtle` · `mouse` · `snake` | `x, y, s, flip, color` |
| `bat` (`hanging` أو يطير) · `butterfly` · `fish_tank` (أسماك تسبح) | |

## 3. نباتات (تتمايل)
| type | المفاتيح |
|---|---|
| `tree` | `kind`: round · pine · palm · olive · dead · birch · cypress |
| `cactus` (`flower`) · `bush` (`berries`) · `tall_grass` (`w`) · `flowers` (`color`, `wilted`) · `mushrooms` · `ivy` (x,y أعلى يسار) | |
| `potted` | `kind`: monstera · ficus · succulent · bonsai · bamboo · sunflower · rose · hanging (y = السقف) · `wet` (مسقية الآن) · `wilted` (ذابلة) |

## 4. الأجواء والطقس
```json
"room": {"place": "street", "weather": "rain", "atmosphere": ["fog", {"kind": "blackout", "x": 300, "y": 1200}], ...}
```
fog · sandstorm · wind_leaves · smoke · sunset · dawn · blackout · police_lights · moonbeam · storm · heat · dust
- `weather` في المكان: rain · snow (خارجي). `fx: ["lightning"]` في المشهد للبرق.
- `blackout`: إظلام مع بقعة ضوء (شمعة/فانوس) عند x,y. `police_lights`: وميض أحمر وأزرق. `moonbeam`: شعاع قمر عند x. `smoke`: دخان يتصاعد من x,y.

## أدلة جاهزة من هذه الأشياء
قط مبلل في بيت جاف · كلب حراسة نائم (لم ينبح) · كلب موحل · نبتة مسقية الآن (تركها بيت «مهجور») · زهور ذابلة («أسقيها يوميًا») · مروحة تدور (أحدهم هنا الآن) · أسطوانة تدور · ساعة بندول متوقفة أو تعمل · سيارة شرطة وصلت قبل الاتصال · طيور ليلية في «الظهيرة».
