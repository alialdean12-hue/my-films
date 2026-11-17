#!/bin/sh
# Rebuild with Node >=22, FFmpeg/ffprobe, Python + numpy, and a HyperFrames-compatible browser.
# No media or fonts are fetched by the film. Point PUPPETEER_EXECUTABLE_PATH at a local browser if needed.
set -eu
cd "$(dirname "$0")"
P=$(pwd); mkdir -p out
if command -v hyperframes >/dev/null 2>&1; then hf(){ hyperframes "$@"; }; else hf(){ npx --yes hyperframes@0.9.64 "$@"; }; fi
export PYTHONDONTWRITEBYTECODE=1 RENDER_SLOTS=1 PRODUCER_LOW_MEMORY_MODE=1 HYPERFRAMES_NO_TELEMETRY=1
[ -s assets/uruk-atlas.mp4 ] || sh assets/rebuild-atlas.sh
python3 tools/subtitles.py
python3 tools/compose.py
python3 tools/score.py
python3 ../../studio-kit/scripts/mix.py mix.json out/mix.wav
# Render from a clean input tree. Never recursively stage the master's QA frames or old renders.
STAGE=$(mktemp -d); trap 'rm -rf "$STAGE"' EXIT
cp index.html gsap.min.js "$STAGE/"; cp -R fonts img assets "$STAGE/"
hf lint "$STAGE" > out/lint.txt
hf render --fps 24 -q delivery --crf 20 --workers 1 -o "$P/out/silent.mp4" "$STAGE"
python3 tools/master.py
ffprobe -v error -show_entries stream=codec_name,width,height,r_frame_rate,nb_frames:format=duration,size -of compact warka-mask.mp4
