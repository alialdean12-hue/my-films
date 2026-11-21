# Style engines (styles 1, 3, 4, 5, 6, 7, 8, 9)

One JSON → narrated vertical video (1080×1920) with voice (edge-tts), music bed, sound effects. Same quality as the approved samples.

**First time on a machine:** `sh ~/my-films/studio-kit/scripts/doctor.sh` (checks and installs everything; must end with READY).
**One command for every style:** `python3 ~/my-films/studio-kit/make.py <style 1-10> video.json ~/out/<name> [--preview]`.

Every finished run gives: `video.mp4` (master), **`video_phone.mp4` (send this)**, `video_16x9.mp4` (YouTube horizontal), `video_1x1.mp4` (square), `cover.jpg` + `cover_check.jpg` (safe-area check), `CAPTION.md` (4 copy blocks: YouTube title, YouTube description, Instagram, TikTok).
- **Quality check (automatic):** before rendering, every beat is checked; text outside the frame or too long stops the render and prints exactly which caption to fix (`--force` renders anyway, `"qa": false` turns it off).
- **Music:** `"music"`: epic mystery calm sad happy tech kids horror news islamic suspense inspire none (default chosen per style), `"music_gain"` (default 0.16).
- **Cover:** `"cover": {"text": "سؤال [y]مثير[/y]؟", "tag": "شرح", "beat": 1, "size": 136, "color": "#ffd21f"}`; the background is a clean frame of that beat.
- **Caption doc:** `"caption_doc": {"title", "description", "question", "hashtags"}` (defaults come from the lines) and `"tags": ["كلمة", ...]`.
- **Voice blocked?** If edge-tts cannot connect (ClientConnectorError), make the narration with your own TTS: one file per beat `b0.wav`, `b1.wav`… (wav/mp3/flac), same text as each `line`, clear Arabic male voice, put them in a folder and add `"voice_files": "<folder>"` to the json. Timing follows those files.
- **Series (account identity):** add `"series": "<name>"` to the json and the look, music, cover tag and hashtags come from `engines/series/<name>.json` (anything in the video json wins). Add `"handle": "@your_account"` to show the account name small at the bottom of every frame.

| series | style | what it is |
|---|---|---|
| `animal_facts` | 9 | عالم الحيوان: شخصية القطة تقدّم حيوانًا جديدًا كل مرة (غيّر character في كل مشهد) |
| `anime_stories` | 8 | قصص أنمي قصيرة: نفس البطلة (شعر وردي، عيون بنفسجية) في كل حلقة |
| `daily_facts` | 9 | هل تعلم يوميًا: شخصية الحوت، معلومة واحدة مدهشة، 30 ث |
| `explained` | 3 | اشرح لي: Vox رسوم بورق كريمي |
| `history_tales` | 6 | حكايات التاريخ: ورق مقصوص، وقت الغروب |
| `life_tips` | 7 | نصائح الحياة: رجل العود بالبدلة، أماكن عمل وبيت |
| `money_rules` | 4 | قواعد المال: ثيم ذهبي ثابت، نصوص متحركة |
| `mysteries` | 1 | ألغاز التاريخ الحقيقية: وثائقي بلون أبيض وأسود وعناوين خبرية |
| `space_wonders` | 5 | عجائب الفضاء: مجسمات ثلاثية الأبعاد، سماء عميقة |
| `what_if` | 7 | ماذا تفعل لو: رجل العود نفسه (man) في كل حلقة، خطوات مرقمة |
| `wisdom` | 4 | حكم وأقوال: ثيم إسلامي هادئ |

- **Delivery folder:** every run also makes `deliver/<Drive folder>/<title>/` with `<title>.mp4`, `<title> - أفقي.mp4`, `<title> - مربع.mp4`, `غلاف.jpg`, `وصف.txt` — upload that folder to Google Drive as it is (Drive folder per style: وثائقي، Vox، رسوم Vox، نصوص متحركة، ثلاثي الأبعاد، ورق مقصوص، رجل العود، أنمي، هل تعلم؛ change with `"drive_folder"`).
- `"formats": false` skips the 16:9 and 1:1 files.

```sh
cd ~/my-films/studio-kit/engines
python3 <engine>.py examples/<engine>.json ~/out/<name> --preview   # look at sheet.jpg first
python3 <engine>.py examples/<engine>.json ~/out/<name>             # video.mp4 + video_phone.mp4
```
Behind a TLS proxy set `SSL_CERT_FILE`. **Always copy an example JSON and change it** (each style has 3: `examples/<style>.json`, `<style>_2.json`, `<style>_3.json`), never start from empty.
Common keys: `title`, `beats` (5–7 beats, one spoken `line` each, ≤ 14 words), optional `voice: {name, rate}`, `duration` (default 30; grows if the voice is longer). In captions `[y]..[/y]` = yellow, `[r]..[/r]` = red, `<br/>` = new line.

| Style | Engine | Beat keys |
|---|---|---|
| 1 وثائقي | `doc.py` | `line`, `query` (English Pixabay search, needs `PIXABAY_KEY`) **or** `img` (file path), `cap`, `date` (gold tag), optional `cam` [scaleFrom, scaleTo, dx, dy], `route: true` (red dashed route on a map photo), `flash: true` (impact flash + shake) |
| 3 Vox رسوم | `voxflat.py` | `line`, `k` + its keys: `q` (`title`, wallet losing bills) · `word` (`word`, `sub`: big slammed word) · `basket` (`title`, `left`/`right` = [label, value], `change`) · `print` (`title`, `machine`, `result`) · `chart` (`title`, `labels` ×7, rising line) · `end` (`title`, `symbol`: coin + growth) |
| 4 نصوص متحركة | `kinetic.py` | `line`, `w` (2–3 words shown one after another; a 1–2 character word is shown huge), `bg` colour |
| 5 ثلاثي الأبعاد | `threed.py` | top level `bands` (7 colours), `rings` (true/false). Beats: `line`, `cap`, `sub`, `k`: `intro` (zoom in) · `ring` (fly along the rings) · `water` (drops into water and floats) · `spin` (fast rotation) · `moons` (orbiting moons) · `end` |
| 6 ورق مقصوص | `paper.py` | `line`, `cap`, `sky` [top, bottom colour], `sun` [x, y, colour], `k`: `intro` (layers rise, caravan) · `build` (blocks stack into a pyramid) · `river` (boat on the Nile) · `tall` (sunset + `measure` ruler) · `night` (stars) · `end` |
| 7 رجل أعواد | `stick.py` | `line`, `cap` (`<span class='n'>1</span><br/>` = numbered step), `place`: elevator house kitchen street forest sea office car, `people`: list of {`look`: man woman hijab boy girl old worker doctor police chef, `x` (120–900), `pose`: stand panic phone press point sit wave breathe no think cheer run drive carry fall sad, `face`: ok happy fear calm sad angry wow, optional `walk_to` (x), `flip`, `colors` {shirt, pants, skin, hair}}, `fx` list: fire smoke rain idea question exclaim heart zzz sweat check cross phone bell clock air money shake open, optional `fx_at` [x, y] |
| 8 أنمي | `anime.py` | `line`, `sub`, `k`: establish back closeup tear run sky rain sakura title, top level `character` {hair, eyes, gender}, `sky` (see CATALOG.md) |
| 9 كرتون «هل تعلم؟» | `cartoon.py` | top level `character`: whale cat octopus bee penguin kid (each has its own home background), optional `bg`: ocean garden ice room space, `tag`. Beats: `line`, `cap`, `k`: `intro` · `compare` (`a`/`b` = [icon, label], `sign`) · `rings` · `swarm` (`icon`, `n`, `icon_scale`: icons fly into the character) · `flyby` (`icon` crosses + shake) · `grow` (`icon` rises beside it, character grows) · `count` (`number`, `unit`: counting number) · `end`. Icons: heart car plane dino house bus star apple fish drop brain clock moon leaf eye dot. A beat may change `character`/`bg`. |

**Full list of every option (places, looks, poses, characters, icons, themes, landmarks, grades…): `CATALOG.md`.** The table below is a summary; the catalog wins.

Rules: one idea per beat; vary scenes (different place / kind / animation every beat); captions 2–5 words; last beat = question or «تابعنا». Look at `sheet.jpg` before rendering: no text cut off, nothing over the caption.
Style 2 (Vox with real photos) uses `../collage/`, style 8 (anime) `../anime/`, style 10 `../series/saw_5tory/`.
