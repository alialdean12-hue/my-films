# Style engines (style 1 وثائقي, style 3 رجل العود السينمائي)

One JSON → narrated vertical video (1080×1920) with voice (edge-tts), music bed, sound effects. Same quality as the approved samples.

**First time on a machine:** `sh ~/my-films/studio-kit/scripts/doctor.sh` (checks and installs everything; must end with READY).
**One command for every style:** `python3 ~/my-films/studio-kit/make.py <style 1-4> video.json ~/out/<name> [--preview]`.

Every finished run gives: `video.mp4` (master), **`video_phone.mp4` (send this)**, (`video_16x9.mp4`, `video_1x1.mp4` only with `"formats": true`), `cover.jpg` + `cover_check.jpg` (safe-area check), `CAPTION.md` (4 copy blocks: YouTube title, YouTube description, Instagram, TikTok).
- **Quality check (automatic):** before rendering, every beat is checked; text outside the frame or too long stops the render and prints exactly which caption to fix (`--force` renders anyway, `"qa": false` turns it off).
- **Photos (styles 1, 2):** each `query` downloads 6 candidates; look at `candidates/beatN.jpg` (numbered) after `--preview` and set `"pick": N` in that beat. `"source"`: auto (Wikimedia → Pixabay → Openverse), wikimedia (history, people, places, artworks), pixabay, openverse.
- **Sources:** styles 1 and 3 need `"sources"` (or `"no_facts": true`), else the render stops.
- **Pronunciation:** numbers become Arabic words automatically; add foreign names to `scripts/pronounce.json`, or give a beat `"say"`.
- **Font:** `"font"`: cairo amiri naskh tajawal kufi lalezar marhey lemonada.
- **Music:** `"music"`: epic mystery calm sad happy tech kids horror news islamic suspense inspire none (default chosen per style), `"music_gain"` (default 0.16).
- **Cover:** `"cover": {"text": "2–4 words, [y]keyword[/y] in a yellow box", "label": "small top pill", "tag": "red badge", "beat": 1, "focus": [x, y], "zoom": 1.25, "arrow": true, "style": "bold"|"split"}`; background = clean zoomed frame of that beat, text size adapts to its length.
- **Caption doc:** a different text per platform (YouTube title+description, TikTok, Instagram). Feed it `"caption_doc": {"hook", "title", "question", "audience", "youtube_title", "hashtags"}` and `"tags"`.
- **Same voice in a series:** when you make the narration yourself (`voice_files`), use the SAME voice every episode and write its name in the series file key `"agent_voice"`.
- **Voice blocked?** If edge-tts cannot connect (ClientConnectorError), make the narration with your own TTS: one file per beat `b0.wav`, `b1.wav`… (wav/mp3/flac), same text as each `line`, clear Arabic male voice, put them in a folder and add `"voice_files": "<folder>"` to the json. Timing follows those files.
- **Series (account identity):** add `"series": "<name>"` to the json and the look, music, cover tag and hashtags come from `engines/series/<name>.json` (anything in the video json wins). Add `"handle": "@your_account"` to show the account name small at the bottom of every frame.

| series | style | what it is |
|---|---|---|
| `mysteries` | 1 | ألغاز التاريخ الحقيقية: وثائقي بلون أبيض وأسود وعناوين خبرية |

- **Delivery folder:** every run makes `deliver/<Drive folder>/<title>/` with ONLY `<title>.mp4`, `غلاف.jpg` and 5 plain-text files, one per platform plus sources (upload as plain text, never as Google Docs; was `الوصف.txt` (captions, then sources and photo credits). Upload exactly that (the .txt becomes the Google Doc «الوصف»). `"formats": true` adds `<title> - أفقي.mp4` and `<title> - مربع.mp4`.
- `"formats": true` also makes the 16:9 and 1:1 files.

```sh
cd ~/my-films/studio-kit/engines
python3 <engine>.py examples/<engine>.json ~/out/<name> --preview   # look at sheet.jpg first
python3 <engine>.py examples/<engine>.json ~/out/<name>             # video.mp4 + video_phone.mp4
```
Behind a TLS proxy set `SSL_CERT_FILE`. **Always copy an example JSON and change it** (each style has 3: `examples/<style>.json`, `<style>_2.json`, `<style>_3.json`), never start from empty.
Common keys: `title`, `beats` (7–10 beats, one spoken `line` each, ≤ 14 words), optional `voice: {name, rate}`, length = as long as the narration needs, minimum 50 s and maximum 80 s (`min_duration`, `max_duration`); outside that range the render stops and says how many words to add or cut (previews still run). In captions `[y]..[/y]` = yellow, `[r]..[/r]` = red, `<br/>` = new line.

| Style | Engine | Beat keys |
|---|---|---|
| 1 وثائقي | `doc.py` | `line`, `query` (English Pixabay search, needs `PIXABAY_KEY`) **or** `img` (file path), `cap`, `date` (gold tag), optional `cam` [scaleFrom, scaleTo, dx, dy], `route: true` (red dashed route on a map photo), `flash: true` (impact flash + shake) |
| 3 رجل العود السينمائي | `cine.py` | قصة بمشاهد: `characters` (كل شخصية تُوصف فتُرسم: `sex age build height skin hair hair_color beard beard_color glasses head head_color agal wear color pants_color outer outer_color hold khanjar bandage`)، ولكل beat: `line`, `cap`, `place`, `time` (day/sunset/night), `cast` (`who x pose face flip scale to pose2 face2 at window`)، `fx` (`kind x y at scale`)، `cam` (push/zoom/pan/still)، `focus`، `view`. مثالان: `examples/cine.json` (قصة حقيقية بمصادر) و`examples/cine_2.json` (قصة خيالية، `no_facts`). كل الأسماء في `CATALOG.md`. |

**Full list of every option (places, looks, poses, characters, icons, themes, landmarks, grades…): `CATALOG.md`.** The table below is a summary; the catalog wins.

Rules: one idea per beat; vary scenes (different place / kind / animation every beat); captions 2–5 words; last beat = question or «تابعنا». Look at `sheet.jpg` before rendering: no text cut off, nothing over the caption.
Style 2 (Vox with real photos) uses `../collage/`, style 4 `../series/saw_5tory/`.
