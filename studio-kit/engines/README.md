# Style engines (styles 1, 3, 4, 5, 6, 7, 9)

One JSON → narrated vertical video (1080×1920) with voice (edge-tts), music bed, sound effects. Same quality as the approved samples.

```sh
cd ~/my-films/studio-kit/engines
python3 <engine>.py examples/<engine>.json ~/out/<name> --preview   # look at sheet.jpg first
python3 <engine>.py examples/<engine>.json ~/out/<name>             # video.mp4 + video_phone.mp4
```
Behind a TLS proxy set `SSL_CERT_FILE`. **Always copy the example JSON and change it**, never start from empty.
Common keys: `title`, `beats` (5–7 beats, one spoken `line` each, ≤ 14 words), optional `voice: {name, rate}`, `duration` (default 30; grows if the voice is longer). In captions `[y]..[/y]` = yellow, `[r]..[/r]` = red, `<br/>` = new line.

| Style | Engine | Beat keys |
|---|---|---|
| 1 وثائقي | `doc.py` | `line`, `query` (English Pixabay search, needs `PIXABAY_KEY`) **or** `img` (file path), `cap`, `date` (gold tag), optional `cam` [scaleFrom, scaleTo, dx, dy], `route: true` (red dashed route on a map photo), `flash: true` (impact flash + shake) |
| 3 Vox رسوم | `voxflat.py` | `line`, `k` + its keys: `q` (`title`, wallet losing bills) · `word` (`word`, `sub`: big slammed word) · `basket` (`title`, `left`/`right` = [label, value], `change`) · `print` (`title`, `machine`, `result`) · `chart` (`title`, `labels` ×7, rising line) · `end` (`title`, `symbol`: coin + growth) |
| 4 نصوص متحركة | `kinetic.py` | `line`, `w` (2–3 words shown one after another; a 1–2 character word is shown huge), `bg` colour |
| 5 ثلاثي الأبعاد | `threed.py` | top level `bands` (7 colours), `rings` (true/false). Beats: `line`, `cap`, `sub`, `k`: `intro` (zoom in) · `ring` (fly along the rings) · `water` (drops into water and floats) · `spin` (fast rotation) · `moons` (orbiting moons) · `end` |
| 6 ورق مقصوص | `paper.py` | `line`, `cap`, `sky` [top, bottom colour], `sun` [x, y, colour], `k`: `intro` (layers rise, caravan) · `build` (blocks stack into a pyramid) · `river` (boat on the Nile) · `tall` (sunset + `measure` ruler) · `night` (stars) · `end` |
| 7 رجل أعواد | `stick.py` | `line`, `cap` (`<span class='n'>1</span><br/>` = numbered step), `place`: elevator house kitchen street forest sea office car, `people`: list of {`look`: man woman hijab boy girl old worker doctor police chef, `x` (120–900), `pose`: stand panic phone press point sit wave breathe no think cheer run drive carry fall sad, `face`: ok happy fear calm sad angry wow, optional `walk_to` (x), `flip`, `colors` {shirt, pants, skin, hair}}, `fx` list: fire smoke rain idea question exclaim heart zzz sweat check cross phone bell clock air money shake open, optional `fx_at` [x, y] |
| 9 كرتون «هل تعلم؟» | `cartoon.py` | top level `character`: whale cat octopus bee penguin kid (each has its own home background), optional `bg`: ocean garden ice room space, `tag`. Beats: `line`, `cap`, `k`: `intro` · `compare` (`a`/`b` = [icon, label], `sign`) · `rings` · `swarm` (`icon`, `n`, `icon_scale`: icons fly into the character) · `flyby` (`icon` crosses + shake) · `grow` (`icon` rises beside it, character grows) · `count` (`number`, `unit`: counting number) · `end`. Icons: heart car plane dino house bus star apple fish drop brain clock moon leaf eye dot. A beat may change `character`/`bg`. |

Rules: one idea per beat; captions 2–5 words; last beat = question or «تابعنا». Look at `sheet.jpg` before rendering: no text cut off, nothing over the caption.
Style 2 (Vox with real photos) uses `../collage/`, style 8 (anime) `../anime/`, style 10 `../series/saw_5tory/`.
