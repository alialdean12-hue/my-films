# 002 · همسة خلف الستار

An original fictional backstage case. Salma is represented only by a chalk outline. The puppet is the unchanged series host, and all scenery, the ticket, and the file monitor are original SVG props. No film clips, external photographs, generated pictures, or third-party music were used.

**The contradiction:** Younes claims to have heard Salma call Nader *in the original clip*. Its properties show one picture track and **zero audio tracks**. This disproves the claimed source of the name, not who caused Salma’s death. Private reference: [MDN, AudioTrackList.length](https://developer.mozilla.org/en-US/docs/Web/API/AudioTrackList/length): “A value of 0 indicates that there are no audio tracks in the media.” A mute button would not prove the same thing.

**Picture review:** Inspected the kit's pre-render sheets for each part and corrected a competing camera tween, name-tag/title overlap, a stamp that was too large, centring of the red ring, and the framing on Salma's outline. In part 1 the chair, monitor and ticket are each toured for the same 2.203-second slot at 1.95×. The clue stays uncircled and unnamed in dialogue. The ring in part 2 singles out the 0, not the whole screen. Both local Cairo fonts loaded; the eight caption/stamp/reveal elements measured per part were in bounds at their midpoints. Each final file was sampled at 0.5, 1.5, …, 49.5 seconds and visually reviewed. No identical adjacent samples and no detected sustained black interval. Both final thumbnails were reviewed at 320 px (see `covers-320.jpg`). The solution is not printed on either cover.

**Sound:** Authentic `ar-SA-HamedNeural`, −3%, seven lines per part. Decoded checksummed, lossless takes are trimmed at sample boundaries, then the original puppet treatment from `make_episode.py` is applied without changing the reference host or the approved filter. Removed only the redundant first sentence of the fourth take in part 2 (161,280 samples, through the pause) to fit 50 s; no speed-up. A low studio drone and synthesized cues sit below the narrator. Final level is set from the PCM mix using measured two-pass loudness; the picture is not recompressed during that pass.

**Final encoded masters:** H.264 1080×1920, 24 fps, 1200 frames each; stereo 48 kHz AAC. Container, picture and sound each measure 50.000 s in both files. Last spoken beat ends at 47.89 s and 47.87 s respectively. HyperFrames 0.9.64 on local Chromium: 0 errors, 5 warnings per episode (reviewed). Unprompted multilingual Whisper on all 14 **encoded** spoken beats recognized the underlying lines, including «يا نادر» and «مسارات الصوت صفر», with some word/spelling differences. This is a technical/ASR check, **not a human listening review**.

| Part | MP4 bytes | Integrated LUFS | dBTP | Master SHA-256 |
|---|---:|---:|---:|---|
| 1 | 23,650,417 | -14.03 | -3.04 | `6870724e59b3c171197c356f2a3eb40c36fc8be2de33b34e647c27b7b347179f` |
| 2 | 22,212,021 | -14.03 | -2.91 | `eedee3dcdd82525032fcc792fa1eab4353cdbc0e2d67371736101e3d1d71f2fe` |

**Delivery:** Drive contained exactly two MP4s, two JPEGs and two native Google Docs, one description per part. The four binary sizes and MD5s matched the local versions. Both Docs were exported back as text to check YouTube Shorts, Instagram and TikTok content. Part 1 contains a comment prompt and no solution. The folder link is in `SAW_HISTORY.md`.
