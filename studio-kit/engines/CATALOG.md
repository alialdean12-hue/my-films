# Catalog: every option of every engine

Use these names in the JSON keys. Mix freely. Engines: see README.md.

## 1 · Documentary (`doc.py`)
- **grade** (default `natural` = the photo as it is; the others darken it): `natural`, `sepia`, `bw`, `cold`, `warm`, `noir`, `vivid`, `faded`, `green`, `red`, `night`, `old_film`, `clean`
- **cam**: `in`, `out`, `left`, `right`, `up`, `down`, `still`, `fast_in` or [scaleFrom, scaleTo, dx, dy]
- **caption**: `paper`, `gold`, `box`, `lower`, `news`, `type`, `big`, `top`, `red`
- **transition**: `fade`, `cut`, `slide`, `up`, `zoom`, `blur`, `flash`, `glitch`
- **overlay** (list): `circle` (at [x,y,r]), `arrow` (arrow [[x1,y1],[x2,y2]]), `route`, `zoombox` (box [x,y,w]), `redact`, `film`, `letterbox`, `vhs`, `counter` (number, unit), `stamp` (stamp), `quote` (quote), `split` (img2 or query2)
- per beat: `img` or `query` (+ `wiki`: English Wikipedia article title, or `ar:<title>`, for real photos of real people/events), `cap`, `date`, `flash`
- **style 11 (`hybrid.py`) adds:** `sticker` {`query` | `img`, `pick`, `x`, `y`, `size`, `rotate`, `outline`} = cut-out of a person/object popping over the photo · caption `paper` (default in style 11): torn paper strip with tape, `[y]` yellow marker, `[r]` red marker

## 7 · رجل العود السينمائي (`cine.py` + `characters.py`)
- **place** (12): `city`, `ruins`, `office`, `room`, `train`, `garden`, `night_garden`, `desert`, `desert_night`, `sea`, `street_night`, `plain` · **time**: `day`, `sunset`, `night` · **view** (office/room window): `hills`, `harbor`, `desert`
- **fx** (11): `mushroom`, `flash`, `shake`, `plane`, `smoke`, `petals`, `rain`, `rays`, `glint`, `birds`, `stars` (keys: `x`, `y`, `at` seconds after the line starts, `scale`, `color`)
- **pose** (4): `stand`, `walk` (with `to` = walks across), `kneel`, `sit` · **face** (7): `calm`, `tired`, `curious`, `shock`, `joy`, `sad`, `angry` · change mid-line with `pose2`/`face2` + `at`
- **cam**: `push` (default), `zoom` (+ `focus: [x, y]`), `pan`, `still` · `window: 0-5` puts a character's head in a train window
- **character spec**: `sex` m/f · `age` child/young/adult/old · `build` thin/avg/heavy · `height` short/avg/tall · `skin` light/medium/tan/brown/dark/#hex
  - `hair`: short, bald, curly, long, ponytail, bun, braids · `hair_color` · `beard`: none, stubble, short, full, long, goatee · `beard_color` · `glasses` · `bandage`
  - `head` (28): `astronaut`, `beret`, `cap`, `chef`, `cowboy`, `crown`, `diver`, `explorer`, `ghutra`, `hard_hat`, `headband`, `hijab`, `knight_helmet`, `kumma`, `massar`, `niqab`, `pharaoh`, `pilot_cap`, `pirate`, `police_cap`, `rice_hat`, `roman_helmet`, `sailor_cap`, `shemagh`, `taqiyah`, `topknot`, `turban`, `viking_helmet` · `head_color` · `agal` (with shemagh/ghutra)
  - `wear` (32): `thobe`, `dishdasha`, `jalabiya`, `abaya`, `kimono`, `sari`, `toga`, `egypt`, `dress`, `hanfu`, `royal`, `suit`, `shirt`, `lab`, `military`, `police`, `work`, `jeans`, `dashiki`, `cowboy`, `knight`, `viking`, `roman`, `samurai`, `pirate`, `astronaut`, `diver`, `chef`, `pilot`, `sailor`, `explorer`, `coat` · `color`, `pants_color`
  - `outer`: `bisht`, `cape` · `outer_color` · `khanjar` · `hold` {"right"/"left": `cane`, `coin`, `book`, `phone`, `beads`, `bag`, `lantern`}
- **War & big events** (`war.py`):
  - **place** also: `map`, `battlefield`, `trenches`, `palace`, `war_room`, `arab_city` · beat `"date": "2 أغسطس 1990"` = red stamp
  - **map** (with `"place": "map"`): `region` `gulf`, `middle_east`, `arab_world`, `levant`, `europe`, `world`, `asia`, `egypt` or `[lon1, lat1, lon2, lat2]` · `color` {ISO: colour} · `labels` [ISO…] (Arabic names) · `flags` [ISO…] · `arrows` [{from, to (ISO or [lon, lat]), at, color, bend}] · `take` [{iso, color, at}] (country changes colour) · `pins` [{lon, lat, label, at}] · `hide_labels`. Real borders of every country (ISO-3 codes: IRQ KWT IRN SAU SYR JOR EGY ARE QAT BHR OMN YEM LBN PSX ISR TUR USA RUS GBR FRA DEU CHN JPN AFG …).
  - **fx** also: `army` {`units`: soldiers/tanks/jets/ships, `n`, `from`, `to`, `y`, `dir` 1/-1, `flag`: ISO, `color`, `scale`, `front`} · `explosion` {x, y, at, scale} · `flag` {code, x} (waving flag on a pole)
  - **flags** drawn: IRQ KWT IRN SAU EGY SYR JOR ARE QAT LBN PSX YEM OMN BHR LBY TUR USA RUS GBR FRA DEU JPN ISR CHN AFG
  - character `beard: "mustache"` · leaders: one character entry per person (e.g. a general in `military` + `beret`, an emir in `thobe` + `ghutra` + `bisht`)
- Design rule: robes (thobe, abaya…) are drawn per pose so they fall with the body; no joints are visible. Make one character entry per look (e.g. `ali` and `ali_hurt` with `bandage`).

## Shared icons (207) · used by cartoon (`icon`, `a`/`b`), voxflat (`icon`, `items`), kinetic (`icon`), stick (`fx`). Unknown names print a WARNING.
`abacus`, `alien`, `ambulance`, `anchor`, `angry_face`, `apple`, `arrow_down`, `arrow_up`, `atom`, `baby`, `backpack`, `bag`, `ball`, `banana`, `bank`, `basketball`, `battery`, `bee`, `bike`, `bird`, `bolt`, `bone`, `book`, `box`, `brain`, `bread`, `bridge`, `bulb`, `bus`, `butterfly`, `cactus`, `cake`, `calendar`, `camel`, `camera`, `car`, `carrot`, `cart`, `castle`, `cat`, `certificate`, `chart`, `check`, `cheese`, `chocolate`, `city`, `clock`, `cloud`, `coffee`, `coin`, `compass`, `cow`, `crab`, `credit_card`, `crescent`, `cross`, `crown`, `diamond`, `dino`, `dna`, `dog`, `dot`, `drop`, `earth`, `egg`, `elephant`, `exclaim`, `eye`, `factory`, `family`, `film`, `fire`, `fish`, `flag`, `flag_iraq`, `flask`, `flower`, `food`, `footprint`, `game`, `gas`, `gear`, `ghost`, `gift`, `globe`, `gold`, `graduation`, `guitar`, `hand`, `handshake`, `headphones`, `heart`, `heartbeat`, `helicopter`, `honey`, `horse`, `hospital`, `hourglass`, `house`, `house_key`, `ice_cream`, `idea`, `kaaba`, `key`, `lantern`, `laptop`, `leaf`, `lion`, `lock`, `lungs`, `magnet`, `mail`, `map`, `medal`, `megaphone`, `microscope`, `milk`, `money`, `money_bag`, `moon`, `mosque`, `mountain`, `mouse`, `muscle`, `mushroom`, `music`, `newspaper`, `octopus`, `oil`, `paint`, `palm`, `paw`, `pencil`, `people`, `person`, `phone`, `photo`, `pie`, `pill`, `pin`, `pizza`, `plane`, `planet`, `police_car`, `pray`, `pyramid`, `question`, `rabbit`, `rain`, `rainbow`, `recycle`, `robot`, `rocket`, `rocket2`, `running`, `sad_face`, `salt`, `satellite`, `scale`, `school`, `search`, `shark`, `shield`, `ship`, `skull`, `sleep`, `smile`, `snake`, `snow`, `solar`, `speech`, `spider`, `star`, `statue`, `stocks`, `stomach`, `sugar`, `sun`, `sword`, `syringe`, `target`, `telescope`, `thermometer`, `thought`, `thumbs_up`, `time`, `tools`, `tooth`, `tornado`, `tower`, `train`, `trash`, `tree`, `trophy`, `truck`, `turtle`, `tv`, `virus`, `volcano`, `warning`, `water`, `water_glass`, `wave`, `whale`, `wifi`, `wind_turbine`, `zzz`

## 7 (old) · Stick people (`stick.py`, name `stick`)
- **place** (46): `elevator`, `house`, `kitchen`, `street`, `forest`, `sea`, `office`, `car`, `bedroom`, `living_room`, `classroom`, `school_yard`, `hospital`, `clinic`, `supermarket`, `market`, `restaurant`, `cafe`, `office2`, `meeting`, `bank`, `library`, `gym`, `lab`, `bathroom`, `garage`, `airport`, `station`, `park`, `playground`, `stadium`, `desert`, `mountain`, `camp`, `snow`, `farm`, `village`, `mosque`, `space`, `underwater`, `rooftop`, `night_street`, `beach_night`, `court`, `prison`, `studio`
- **look** (45): `man`, `woman`, `hijab`, `boy`, `girl`, `old`, `worker`, `doctor`, `police`, `chef`, `student`, `teacher`, `businessman`, `businesswoman`, `nurse`, `firefighter`, `soldier`, `pilot`, `farmer`, `athlete`, `gamer`, `scientist`, `grandma`, `grandma_hijab`, `baby`, `teen`, `thobe`, `abaya`, `thief`, `judge`, `mechanic`, `waiter`, `astronaut`, `superhero`, `robot`, `man2`, `man3`, `man4`, `woman2`, `woman3`, `hijab2`, `hijab3`, `boy2`, `girl2`, `girl_hijab` (override any colour with `colors: {shirt, pants, skin, hair}`)
- **pose** (42): `stand`, `panic`, `phone`, `press`, `point`, `sit`, `wave`, `breathe`, `no`, `think`, `cheer`, `run`, `walk1`, `walk2`, `drive`, `carry`, `fall`, `sad`, `shrug`, `hands_hips`, `pray`, `read`, `type`, `eat`, `drink`, `kick`, `jump`, `dance1`, `dance2`, `cry`, `scared`, `stop`, `thumbs`, `lift`, `lie`, `kneel`, `hug`, `climb`, `swim`, `bow`, `sleep`, `angry_point`
- **face** (15): `ok`, `happy`, `fear`, `calm`, `sad`, `angry`, `sleepy`, `wink`, `laugh`, `cry`, `think`, `sick`, `love`, `cool`, `wow`
- **fx** (16 animated + any icon name): `fire`, `rain`, `idea`, `question`, `exclaim`, `heart`, `zzz`, `sweat`, `check`, `cross`, `phone`, `bell`, `clock`, `smoke`, `air`, `money`, `shake`, `open`
- per person: `x`, `walk_to`, `flip`, `scale`; per beat: `fx_at` [x, y]
- **action** (two people, they face each other automatically): `handshake`, `give` (+ `item`: any icon), `hug`, `argue`, `high_five`, `talk`, `help`, `bow`, `dance`, `teach`

## 9 · Cartoon (`cartoon.py`)
- **character** (71): `alien`, `ant`, `bat`, `bear`, `bee`, `beetle`, `butterfly`, `camel`, `cat`, `caterpillar`, `chick`, `chicken`, `cow`, `crab`, `crocodile`, `crow`, `deer`, `dog`, `dolphin`, `dragon`, `duck`, `eagle`, `elephant`, `fish`, `flamingo`, `fox`, `frog`, `giraffe`, `goat`, `goldfish`, `gorilla`, `grandpa`, `hamster`, `horse`, `jellyfish`, `kid`, `koala`, `ladybug`, `lion`, `monkey`, `monster`, `mosquito`, `mouse`, `octopus`, `owl`, `panda`, `parrot`, `peacock`, `penguin`, `penguin2`, `pig`, `polar_bear`, `puppy`, `rabbit`, `rhino`, `robot`, `scientist`, `seahorse`, `seal`, `shark`, `sheep`, `snail`, `spider`, `starfish`, `teacher`, `tiger`, `turtle`, `unicorn`, `whale`, `wolf`, `zebra`
  (side-view animals, birds, sea creatures and bugs have their own body shapes; whale cat octopus bee penguin kid are the original six)
- **bg** (21): `ocean`, `garden`, `ice`, `room`, `space`, `desert`, `savanna`, `jungle`, `pond`, `farm`, `night`, `mountain`, `beach`, `city`, `lab`, `classroom`, `kitchen`, `rain`, `snow`, `stage`, `hospital` (each character has a default home)
- **k**: `intro`, `compare` (a, b, sign), `rings`, `swarm` (icon, n, icon_scale), `flyby` (icon), `grow` (icon, icon_scale), `count` (number, unit), `end`

## 4 · Kinetic text (`kinetic.py`)
- **theme** (24): `classic`, `mono`, `paper`, `neon`, `sunset`, `ocean`, `forest`, `candy`, `gold`, `fire`, `ice`, `royal`, `mint`, `coffee`, `sport`, `news`, `tech`, `retro`, `pastel`, `islamic`, `horror`, `kids`, `luxury`, `bw_red`
- **anim** (16, list = cycle per word): `slam`, `pop`, `drop`, `rise`, `left`, `right`, `spin`, `blur`, `stretch`, `squash`, `flipx`, `flipy`, `zoomout`, `tilt`, `fade`, `shake`
- **style**: `solid`, `outline`, `box`, `shadow`, `underline`, `glow`, `highlight`, `italic`
- **layout**: `one`, `stack`, `zigzag`, `top`, `bottom` · **bgfx**: `bar`, `none`, `circle`, `stripes`, `grid`, `burst`, `dots`, `frame`, `split`, `noise` · **emph**: `grow`, `wobble`, `pulse`, `shake`, `none`
- per beat: `w` (words), `hl` (indexes in accent), `icon`, `bg`, `color`, `accent`, `size`

## 3 · Vox drawings (`voxflat.py`)
- **paper**: `cream`, `white`, `blue`, `mint`, `pink`, `yellow`, `grey`, `kraft`, `lilac`, `peach` (or any colour)
- **k**: `icons` (items [[icon,label]×2–4]), `versus` (a, b, win), `bars` (values, labels, unit), `pie` (percent, label, color), `list` (items), `counter` (number, unit, label, icon), `timeline` (events [[year,label]]), `steps` (items), `grid` (total, hit), `progress` (percent), `big_icon` (icon), `quote` (text, who), `map` (pins [[x,y,label]]), `word` (word, sub), `basket` (left, right, change), `print` (machine, result), `chart` (labels), `q`, `end` (symbol). Every kind takes `title` with `[y]..[/y]`.

## 5 · 3D (`threed.py`)
- **object**: `saturn`, `jupiter`, `earth`, `mars`, `venus`, `mercury`, `uranus`, `neptune`, `pluto`, `moon`, `sun`, `ice_planet`, `lava_planet`, `candy_planet`, `coin` (`label`), `gem`, `cube`, `gold_bar`, `ball`, `heart`, `atom`, `dice`, `pyramid`, `bulb`
- **sky**: `space`, `deep`, `studio`, `blue`, `sunset`, `white`, `green`
- **k**: `intro`, `ring`, `water`, `spin`, `moons`, `end` · custom planet: top-level `bands` (7 colours) + `rings`

## 6 · Paper cut-out (`paper.py`)
- **landmark**: `pyramids`, `mountains`, `city`, `castle`, `mosque`, `lighthouse`, `windmill`, `volcano`, `bridge`, `tower`, `temple`, `forest`, `village`, `oasis`, `igloo`, `ship`, `great_wall`, `none`
- **time**: `day`, `dawn`, `noon`, `sunset`, `dusk`, `night` · **land**: `desert`, `green`, `snow`, `autumn`, `ocean`, `rock`, `jungle`, `pink`, `night`
- **extras** (list): `camels`, `birds`, `balloon`, `cars`, `train`, `sheep`, `plane`, `kite`, `boats`, `people`, `snowfall`, `leaves`
- **k**: `scene`, `intro`, `build` (pyramid stacks), `river` (boat), `tall` (ruler `measure`), `night`, `end`

## 8 · Anime (`anime.py`)
- top level `character`: {`hair`: black brown blonde pink blue silver red green, `eyes`: brown blue green red gold purple, `gender`: girl/boy, `long` (hair), `shirt`, `skin`}, `sky`, `place`: city / hills
- **k**: `establish` (city or hills under the sky), `back` (character from behind), `closeup` (face; `emotion`: calm happy sad surprised determined angry), `tear` (close-up with a falling tear), `run` (speed lines), `sky` (shooting stars), `rain`, `sakura` (falling petals), `title` (big glowing title `title`)
- **sky**: night sunset day dawn storm dusk space · per beat: `sub` (subtitle), `petals: true`, `rain: true`
- **two characters**: top level `character2`; kinds `duo` (`speaker`: 1 or 2, `emotion`, `emotion2`), `talk2`, `together`

## Shared options (every engine)
- **font**: `cairo` (default), `amiri` (classic), `naskh`, `tajawal` (clean), `kufi` (Reem Kufi titles), `lalezar` (bold display), `marhey` (playful), `lemonada` (rounded)
- **music**: epic mystery calm sad happy tech kids horror news islamic suspense inspire none · `music_gain`
- **say** (per beat): what the voice reads if it must differ from `line` (e.g. spell a name). Numbers and the names in `scripts/pronounce.json` are converted to Arabic words automatically.
- **sources**: list of sources (required for styles 1, 3, 5, 6, 7, 9; `"no_facts": true` for pure fiction) → `مصادر المعلومات.txt` in the delivery folder
- **photos** (styles 1 and 2): `query` + `source` (`auto` = Wikimedia → Pixabay → Openverse, or one of them) + `pick` (number from `candidates/beatN.jpg`; collage: `candidates/<asset>.jpg`). Credits → `مصادر الصور.txt`.
- **series**, **handle**, **cover**, **caption_doc**, **tags**, **formats**, **qa**, **voice**, **voice_files**, **drive_folder**: see README.md
