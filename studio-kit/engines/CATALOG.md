# Catalog: every option of every engine

Use these names in the JSON keys. Mix freely. Engines: see README.md.

## Shared icons (95) · used by cartoon (`icon`, `a`/`b`), voxflat (`icon`, `items`), kinetic (`icon`), stick (`fx`)
`alien`, `apple`, `arrow_down`, `arrow_up`, `atom`, `bag`, `ball`, `banana`, `basketball`, `battery`, `bike`, `bolt`, `bone`, `book`, `brain`, `bread`, `bulb`, `bus`, `cake`, `calendar`, `camera`, `car`, `carrot`, `cart`, `chart`, `check`, `cheese`, `clock`, `cloud`, `coffee`, `coin`, `cross`, `crown`, `diamond`, `dino`, `dna`, `dot`, `drop`, `earth`, `egg`, `exclaim`, `eye`, `factory`, `fire`, `fish`, `flag`, `flower`, `ghost`, `gift`, `heart`, `hospital`, `hourglass`, `house`, `key`, `laptop`, `leaf`, `lock`, `magnet`, `map`, `medal`, `milk`, `money`, `moon`, `mosque`, `mountain`, `music`, `pencil`, `phone`, `pie`, `pill`, `pin`, `pizza`, `plane`, `pyramid`, `question`, `rain`, `robot`, `rocket`, `school`, `ship`, `skull`, `snow`, `star`, `sun`, `syringe`, `tooth`, `tower`, `train`, `tree`, `trophy`, `tv`, `volcano`, `warning`, `water`, `wifi`

## 7 · Stick people (`stick.py`)
- **place** (46): `elevator`, `house`, `kitchen`, `street`, `forest`, `sea`, `office`, `car`, `bedroom`, `living_room`, `classroom`, `school_yard`, `hospital`, `clinic`, `supermarket`, `market`, `restaurant`, `cafe`, `office2`, `meeting`, `bank`, `library`, `gym`, `lab`, `bathroom`, `garage`, `airport`, `station`, `park`, `playground`, `stadium`, `desert`, `mountain`, `camp`, `snow`, `farm`, `village`, `mosque`, `space`, `underwater`, `rooftop`, `night_street`, `beach_night`, `court`, `prison`, `studio`
- **look** (45): `man`, `woman`, `hijab`, `boy`, `girl`, `old`, `worker`, `doctor`, `police`, `chef`, `student`, `teacher`, `businessman`, `businesswoman`, `nurse`, `firefighter`, `soldier`, `pilot`, `farmer`, `athlete`, `gamer`, `scientist`, `grandma`, `grandma_hijab`, `baby`, `teen`, `thobe`, `abaya`, `thief`, `judge`, `mechanic`, `waiter`, `astronaut`, `superhero`, `robot`, `man2`, `man3`, `man4`, `woman2`, `woman3`, `hijab2`, `hijab3`, `boy2`, `girl2`, `girl_hijab` (override any colour with `colors: {shirt, pants, skin, hair}`)
- **pose** (42): `stand`, `panic`, `phone`, `press`, `point`, `sit`, `wave`, `breathe`, `no`, `think`, `cheer`, `run`, `walk1`, `walk2`, `drive`, `carry`, `fall`, `sad`, `shrug`, `hands_hips`, `pray`, `read`, `type`, `eat`, `drink`, `kick`, `jump`, `dance1`, `dance2`, `cry`, `scared`, `stop`, `thumbs`, `lift`, `lie`, `kneel`, `hug`, `climb`, `swim`, `bow`, `sleep`, `angry_point`
- **face** (15): `ok`, `happy`, `fear`, `calm`, `sad`, `angry`, `sleepy`, `wink`, `laugh`, `cry`, `think`, `sick`, `love`, `cool`, `wow`
- **fx** (16 animated + any icon name): `fire`, `rain`, `idea`, `question`, `exclaim`, `heart`, `zzz`, `sweat`, `check`, `cross`, `phone`, `bell`, `clock`, `smoke`, `air`, `money`, `shake`, `open`
- per person: `x`, `walk_to`, `flip`, `scale`; per beat: `fx_at` [x, y]

## 9 · Cartoon (`cartoon.py`)
- **character** (55): `whale`, `cat`, `octopus`, `bee`, `penguin`, `kid`, `dog`, `puppy`, `rabbit`, `bear`, `panda`, `polar_bear`, `koala`, `lion`, `tiger`, `fox`, `wolf`, `mouse`, `hamster`, `pig`, `cow`, `sheep`, `goat`, `horse`, `camel`, `elephant`, `giraffe`, `zebra`, `monkey`, `gorilla`, `frog`, `turtle`, `owl`, `chick`, `chicken`, `duck`, `parrot`, `eagle`, `bat`, `dolphin`, `shark`, `seal`, `crab`, `ladybug`, `butterfly`, `ant`, `snail`, `dragon`, `unicorn`, `robot`, `alien`, `monster`, `teacher`, `scientist`, `grandpa`
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

## 1 · Documentary (`doc.py`)
- **grade**: `sepia`, `bw`, `cold`, `warm`, `noir`, `vivid`, `faded`, `green`, `red`, `night`, `old_film`, `clean`
- **cam**: `in`, `out`, `left`, `right`, `up`, `down`, `still`, `fast_in` or [scaleFrom, scaleTo, dx, dy]
- **caption**: `gold`, `box`, `lower`, `news`, `type`, `big`, `top`, `red`
- **transition**: `fade`, `cut`, `slide`, `up`, `zoom`, `blur`, `flash`, `glitch`
- **overlay** (list): `circle` (at [x,y,r]), `arrow` (arrow [[x1,y1],[x2,y2]]), `route`, `zoombox` (box [x,y,w]), `redact`, `film`, `letterbox`, `vhs`, `counter` (number, unit), `stamp` (stamp), `quote` (quote), `split` (img2 or query2)
- per beat: `img` or `query`, `cap`, `date`, `flash`
