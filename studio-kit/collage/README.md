# Vox cut-out collage (style S2)

Real photos (Pixabay / Wikimedia) become **paper stickers**: the subject is cut out automatically (rembg), gets a white sticker border and a shadow; other photos become **torn photo cards with tape**. Everything pops / drops / slides in, «boils» like stop-motion paper (12 fps jitter), sits on textured paper with halftone, and scenes change with a **paper-tear wipe**. Hand-drawn red circles, arrows and underlines draw themselves; key words get a yellow marker.

**73 motions** (enter, paper effects, tears, loops, annotations, info graphics, transitions, camera): see `MOTIONS.md`. Boil only on characters (`"loop":"boil"`).

```sh
pip install "rembg[cpu]" pillow numpy      # once; first cut downloads the u2net model (~170 MB)
# photos: give each asset a "query" (English); the engine shows a numbered sheet candidates/<asset>.jpg, choose with "pick"
python3 ~/my-films/studio-kit/collage/make_collage.py video.json OUT --preview    # look at OUT/sheet1.jpg
python3 ~/my-films/studio-kit/collage/make_collage.py video.json OUT              # OUT/video.mp4 + OUT/cover.jpg
python3 ~/my-films/studio-kit/scripts/cover_check.py OUT/cover.jpg               # safe-area check
```
Example: `examples/gold.json` (download its four photos into `media/` first; each asset has the `query` used).

## json
- `title`, `paper` (default background: cream · kraft · white · dark · blue · red · green · yellow), `voice` `{name, rate}`, optional `duration` (default: fits the voice), `gap`.
- `assets`: `{"name": {"src": "media/x.jpg", "cut": true}}` → sticker; without `cut` → photo card (`"vintage": true` = sepia print).
- `beats` (one spoken `line` each, 4–8 beats for 25–45 s): `bg` (paper colour), `zoom` (slow push, default 1.06), `items`:
  - `cutout` `{asset, x, y, h|w, tilt, size: hero|main|small|icon, enter, effect, loop, exit, at} (keys in MOTIONS.md)`
  - `photo` `{asset, x, y, w, tilt, tape, enter, at}` (torn edges automatic)
  - `text` `{text, x, y, size, style: big|label|stamp|note, at}`: `[y]..[/y]` yellow marker, `[r]..[/r]` red, `\n` new line
  - `circle` `{x, y, r, sx}` · `arrow` `{from:[x,y], to:[x,y]}` · `underline` `{x, y, w}` · `pin` `{x, y}`
  - `at` = seconds after the line starts (stagger items 0.4–0.8 s, land each on the word it illustrates).
- `cover`: `{asset, text, bg, tag}` (tag default «شرح»).

## Rules that make it look like the big channels
- 1 hero cut-out per scene + at most 1 photo card + 1–2 texts + 1 drawn mark. Never a slideshow of full photos.
- Cut-outs only from photos with a clear subject (person, object, building) on a simple background; check the sticker in the sheet: if the cut is ragged, choose another photo.
- Alternate paper colours scene to scene (kraft → cream → dark …). Keep text inside x 90–990 and away from faces.
- People: real public figures only from public-domain/CC archive photos; never generated faces of real people.

## Moving footage cards
Asset `{"video_query": "ocean waves"}` (Pixabay videos, needs PIXABAY_KEY; candidates in `candidates/<asset>.jpg`, choose with `"pick"`; `"start"`, `"dur"`) and item `{"type": "video", "asset": "sea", "x": 540, "y": 1050, "size": "hero"}`: the footage plays inside a torn paper card with tape. Example: `examples/video_demo.json`.
