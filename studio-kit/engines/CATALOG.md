# Catalog: every option of every engine

Use these names in the JSON keys. Mix freely. Engines: see README.md.

## 1 · Documentary (`doc.py`)
- **grade**: `sepia`, `bw`, `cold`, `warm`, `noir`, `vivid`, `faded`, `green`, `red`, `night`, `old_film`, `clean`
- **cam**: `in`, `out`, `left`, `right`, `up`, `down`, `still`, `fast_in` or [scaleFrom, scaleTo, dx, dy]
- **caption**: `gold`, `box`, `lower`, `news`, `type`, `big`, `top`, `red`
- **transition**: `fade`, `cut`, `slide`, `up`, `zoom`, `blur`, `flash`, `glitch`
- **overlay** (list): `circle` (at [x,y,r]), `arrow` (arrow [[x1,y1],[x2,y2]]), `route`, `zoombox` (box [x,y,w]), `redact`, `film`, `letterbox`, `vhs`, `counter` (number, unit), `stamp` (stamp), `quote` (quote), `split` (img2 or query2)
- per beat: `img` or `query`, `cap`, `date`, `flash`

## 3 · رجل العود السينمائي (`cine.py` + `characters.py`)
- **place** (12): `city`, `ruins`, `office`, `room`, `train`, `garden`, `night_garden`, `desert`, `desert_night`, `sea`, `street_night`, `plain` · **time**: `day`, `sunset`, `night` · **view** (office/room window): `hills`, `harbor`, `desert`
- **fx** (11): `mushroom`, `flash`, `shake`, `plane`, `smoke`, `petals`, `rain`, `rays`, `glint`, `birds`, `stars` (keys: `x`, `y`, `at` seconds after the line starts, `scale`, `color`)
- **pose** (4): `stand`, `walk` (with `to` = walks across), `kneel`, `sit` · **face** (7): `calm`, `tired`, `curious`, `shock`, `joy`, `sad`, `angry` · change mid-line with `pose2`/`face2` + `at`
- **cam**: `push` (default), `zoom` (+ `focus: [x, y]`), `pan`, `still` · `window: 0-5` puts a character's head in a train window
- **character spec**: `sex` m/f · `age` child/young/adult/old · `build` thin/avg/heavy · `height` short/avg/tall · `skin` light/medium/tan/brown/dark/#hex
  - `hair`: short, bald, curly, long, ponytail, bun, braids · `hair_color` · `beard`: none, stubble, short, full, long, goatee · `beard_color` · `glasses` · `bandage`
  - `head` (28): `astronaut`, `beret`, `cap`, `chef`, `cowboy`, `crown`, `diver`, `explorer`, `ghutra`, `hard_hat`, `headband`, `hijab`, `knight_helmet`, `kumma`, `massar`, `niqab`, `pharaoh`, `pilot_cap`, `pirate`, `police_cap`, `rice_hat`, `roman_helmet`, `sailor_cap`, `shemagh`, `taqiyah`, `topknot`, `turban`, `viking_helmet` · `head_color` · `agal` (with shemagh/ghutra)
  - `wear` (32): `thobe`, `dishdasha`, `jalabiya`, `abaya`, `kimono`, `sari`, `toga`, `egypt`, `dress`, `hanfu`, `royal`, `suit`, `shirt`, `lab`, `military`, `police`, `work`, `jeans`, `dashiki`, `cowboy`, `knight`, `viking`, `roman`, `samurai`, `pirate`, `astronaut`, `diver`, `chef`, `pilot`, `sailor`, `explorer`, `coat` · `color`, `pants_color`
  - `outer`: `bisht`, `cape` · `outer_color` · `khanjar` · `hold` {"right"/"left": `cane`, `coin`, `book`, `phone`, `beads`, `bag`, `lantern`}
- Design rule: robes (thobe, abaya…) are drawn per pose so they fall with the body; no joints are visible. Make one character entry per look (e.g. `ali` and `ali_hurt` with `bandage`).

## Shared options (every engine)
- **font**: `cairo` (default), `amiri` (classic), `naskh`, `tajawal` (clean), `kufi` (Reem Kufi titles), `lalezar` (bold display), `marhey` (playful), `lemonada` (rounded)
- **music**: epic mystery calm sad happy tech kids horror news islamic suspense inspire none · `music_gain`
- **say** (per beat): what the voice reads if it must differ from `line` (e.g. spell a name). Numbers and the names in `scripts/pronounce.json` are converted to Arabic words automatically.
- **sources**: list of sources (required for styles 1 and 3; `"no_facts": true` for pure fiction) → `مصادر المعلومات.txt` in the delivery folder
- **photos** (styles 1 and 2): `query` + `source` (`auto` = Wikimedia → Pixabay → Openverse, or one of them) + `pick` (number from `candidates/beatN.jpg`; collage: `candidates/<asset>.jpg`). Credits → `مصادر الصور.txt`.
- **series**, **handle**, **cover**, **caption_doc**, **tags**, **formats**, **qa**, **voice**, **voice_files**, **drive_folder**: see README.md
