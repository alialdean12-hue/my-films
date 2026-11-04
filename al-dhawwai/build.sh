#!/bin/sh
# One command: picture → events → score/foley/voice mix → master.  sh build.sh
# The narration in voice/ is already generated and checked (tools/tts_edge.py + asr_check.py, see README below).
set -e
LIB=${LIB:-/root/lemo-opuscar}
HERE=$(cd "$(dirname "$0")" && pwd)
export LIB
[ -f "$LIB/core/render/video.mjs" ] || { echo "set LIB to the Lemo-Opuscar library folder"; exit 1; }
cd "$LIB"
node core/render/events.mjs "$HERE" --size 1080x1920
node core/render/video.mjs "$HERE" --fps 24 --workers 4 --size 1080x1920 --out "$HERE/out/video.mp4"
"$LIB/.venv/bin/python" "$HERE/mix.py"
"$LIB/.venv/bin/python" "$HERE/tools/make_srt.py"
"$LIB/.venv/bin/python" core/render/srt.py "$HERE/out/cues.json" "$HERE/al-dhawwai.srt"
sh core/render/mux.sh "$HERE/out/video.mp4" "$HERE/out/mix.wav" "$HERE/al-dhawwai.mp4" 24 1
node core/render/still.mjs "$HERE" 53.8 --size 1080x1920 --out "$HERE/out" --prefix poster_ && cp "$HERE/out/poster_53.8.jpg" "$HERE/poster.jpg"

# Regenerate the narration (needs a network connection to Microsoft's speech service):
#   SSL_CERT_FILE=... $LIB/.venv/bin/python tools/tts_edge.py lines.json voice --voice ar-IQ-BasselNeural --rate=-8%
#   $LIB/.venv/bin/python $LIB/core/tts/asr_check.py lines.json voice --lang ar --model medium
