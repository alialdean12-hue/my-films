# saw_5tory: سلسلة ألغاز الجرائم

The agent writes **two JSON files per case** (part 1 = the puzzle, part 2 = the solution) and runs:

```sh
cd ~/my-films/studio-kit/series/saw_5tory
python3 make_episode.py cases/<NNN>-part1.json ~/saw_out/<NNN>/p1 --preview   # look at sheet*.jpg first
python3 make_episode.py cases/<NNN>-part1.json ~/saw_out/<NNN>/p1             # video.mp4 + thumb.jpg
python3 make_episode.py cases/<NNN>-part2.json ~/saw_out/<NNN>/p2
```
Behind a TLS proxy set `SSL_CERT_FILE` (edge-tts needs it). Each run: voice → timing → HTML → lint → contact sheet → sound mix → render → thumbnail. Every video is exactly `duration` (50 s). If the lines are too long the script stops and says how many words to cut.

Working examples: `examples/001-part1.json`, `examples/001-part2.json` (copy them, never start from empty).

## JSON format

```json
{
 "slug": "001-dry-umbrella", "title": "المظلة الجافة", "part": 1, "duration": 50,
 "voice": {"name": "ar-SA-HamedNeural", "rate": "-3%"},
 "room": {"wall": "#0c1628", "objects": [ {"type": "window", "x": 640, "y": 300, "rain": true}, ... ]},
 "beats": [ {"scene": "host", "host": "enter", "line": "...", "caption": "..."}, {"scene": "room", ...}, ... ],
 "thumb": {"text": "هل تكشف\n[r]الكذبة[/r]؟", "focus": [490, 1150, 1.25]}
}
```

**Voice**: always Hamed; the builder adds the approved «doll» layer (octave-down copy at 38 % + light echo). Do not change it.

**room.objects**: props from `props.py` (one dict per prop, `"type"` = function name, other keys = its arguments; `"note"` is ignored, use it to mark the clue / red herrings):
`window(x,y,rain,broken,day)` · `clock(x,y,time)` · `digital_clock(x,y,text,blink)` · `calendar(x,y,month,day)` · `photo_frame(x,y,shadow:long|short)` · `door(x,y,chain)` · `doormat(x,y,wet,mud)` · `table(x,y,w)` · `chair_over(x,y)` · `outline(x,y,name)` · `umbrella(x,y,wet)` · `cup_broken(x,y)` · `cup(x,y,steam,lipstick,skin,empty)` · `ice_glass(x,y,ice)` · `candle(x,y,height,lit,smoke)` · `phone(x,y,battery,screen,lit)` · `paper(x,y,kind:ticket|receipt|newspaper|note,title,lines,rot)` · `plant(x,y,wet,wilted)` · `dusty_box(x,y,handprint)` · `shoes(x,y,mud,wet)` · `footprints(x1,y1,x2,y2,kind:wet|mud|sand,n)` · `glass_shards(x,y)` · `book(x,y,page)` · `dog(x,y,asleep)` · `person(id,x,y,name,coat,hair,skin,wet,glasses,fog)`.
Frame is 1080×1920; floor starts at y 1380. Standard layout that always reads well: window top-right (640,300), clock top-left (300,430), door left (40,700), people at x 380–700 with feet at y 1520, small props on a `table` (top at y 1300) or on the floor y 1460–1720. Keep 3–6 props + 1–2 people; never more than 8 objects.

**beats** (5–8 per part, one spoken line each, ≤ 14 words):
- `scene`: `host` (the puppet narrator) or `room`.
- `line`: what the voice says. `caption`: the 2–6 key words on screen; colour with `[r]..[/r]` red, `[y]..[/y]` yellow, `[b]..[/b]` blue, `\n` new line.
- host beats: `"host": "enter"` (first beat), `"talk"`, `"point"` (last beat); `"sub"`: small second caption (e.g. «اكتب جوابك في التعليقات»).
- room beats: `"cam": [x, y, scale]` (1.0 = whole room, 1.5–2.3 = close), `"tour": [[x,y,s],...]` quick equal stops (2–4), `"tags": ["<person id>", "outline"]` show name tags, `"fx": ["lightning", "flicker", "glance"]`, `"stamp": "يكذب!"` red stamp, `"caption_pos": "top"|"bottom"|"low"`, `"caption_size"`.
- part 2 only: `"ring": [x, y, r]` red circle drawn on the decisive clue, `"reveal": "المظلة [r]جافة[/r]!"` big yellow line.

**thumb**: `text` 2–4 words (part 1 asks, part 2 teases the answer without saying it), `focus` = what the background shows. Badge «الجزء 1: اللغز» / «الجزء 2: الحل» and `saw_5tory` are added automatically.

## Five case formats (rotate them: never the same format twice in a row)
| Format | Question | Scenes used | Example |
|---|---|---|---|
| **classic** | «ما الذي كشف كذبته؟» one suspect, one lie, one visible clue | title, host, room | `examples/001` |
| **lineup** | «من الكاذب؟ 1 أم 2 أم 3» three suspects, each one statement; one is contradicted by the room | title, host, room, cards | `examples/002` |
| **slip** (زلة لسان) | «ما الكلمة التي كشفته؟» the suspect says something nobody told him | title, host, room, talk | `examples/003` |
| **timeline** | «أين الخلل؟» times on a board do not fit the alibi | title, host, room, board | `examples/004` |
| **howdunit** | «كيف فعلها؟» we know who; the clue shows how | title, host, room, cards | build like 001/002 |

**Scene types**
- `title`: case card. Keys: `case` ("005"), `title`, optional `subtitle`. Always the first beat.
- `host`: the puppet. `host`: enter | talk | point; `timer: true` shows a «فكّر» ring after the line (use on the last beat of part 1).
- `room`: the scene (cam, tour, tags, fx, stamp, ring, reveal as above). A beat with `tags` puts its caption low automatically.
- `cards`: 2–3 numbered evidence cards cropped live from the room: `"cards": [[x, y, scale, "label"], ...]`; part 2 adds `"pick": index` (0-based) to light the right card and dim the others.
- `talk`: interrogation bubbles, one per beat, they stay on screen for the whole run (max 4, then a fresh page): `"say": ["detective" | <person id>, "text with [r]..[/r]"]`.
- `board`: timeline notes. Put `"board": {"title": "...", "items": [["9:00", "..."], ...]}` at the top level (max 4 items); each board beat has `"show": n` (notes visible by its end) and, in part 2, `"mark": index`.

**People (`person`)**: read `CHARACTERS.md` (24 ready characters with `"cast"`, plus thousands of combinations of face, eyes, nose, brows, hair, outfit, build, pose, expression and accessories; gallery in `CHARACTERS.jpg`). Put 2–3 people at x ≈ 320 / 560 / 790 (feet y 1530) or 1 person at x ≈ 490.

**Places**: read `PLACES.md`: 51 interior and exterior places (`"place": "bank"`, `"time"`, `"weather"`), each drawn with its own furniture and Arabic sign. Old `"preset"` rooms still work.

## Rules that keep it good
- Part 1 never circles or names the decisive clue: the `tour` visits the clue AND the red herrings equally.
- Part 2 opens by recalling the lie, shows the clue with `ring` + `reveal`, explains in 2 lines, dismisses the red herrings, ends with a question + «تابع للغز القادم».
- Look at `sheet*.jpg` before the full render: no caption on a face, no tag over a caption, the clue visible in part 1.
- No body is ever shown (chalk outline only), no blood, no weapons in close-up.
