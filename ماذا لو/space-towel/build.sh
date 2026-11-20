#!/bin/sh
# No network needed once dependencies are installed. Run with HyperFrames 0.9.64 and Node 22+.
set -eu
cd "$(dirname "$0")"; P=$(pwd); mkdir -p out
export PYTHONDONTWRITEBYTECODE=1 RENDER_SLOTS=1 PRODUCER_LOW_MEMORY_MODE=1 HYPERFRAMES_NO_TELEMETRY=1
# The prepared limited-palette plates are included. Set REPAINT=1 to regenerate them from the editable masters.
if [ "${REPAINT:-0}" = 1 ]; then python3 tools/paint.py; fi
python3 tools/compose.py
python3 tools/score.py
python3 ../../studio-kit/scripts/mix.py mix.json out/mix.wav
STAGE=$(mktemp -d); trap 'rm -rf "$STAGE"' EXIT
cp index.html gsap.min.js "$STAGE/"; cp -R img fonts "$STAGE/"
hyperframes lint "$STAGE" >out/lint.txt
hyperframes render --fps 24 -q delivery --crf 20 --workers 1 -o "$P/out/silent.mp4" "$STAGE"
python3 tools/master.py
ffprobe -v error -show_entries format=duration,size:stream=codec_name,width,height,r_frame_rate,nb_frames -of compact space-towel.mp4
