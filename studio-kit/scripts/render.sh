#!/bin/sh
# Render one HyperFrames project and mux its mixed audio. Paths after cd are project-relative.
#   sh render.sh <project_dir> <mix.wav|-> <out.mp4> [fps]
set -eu
P="$1"; AUD="$2"; OUT="$3"; FPS="${4:-24}"
cd "$P"
TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
hf() { if command -v hyperframes >/dev/null 2>&1; then hyperframes "$@"; else npx hyperframes "$@"; fi; }
if ! hf lint >"$TMP/lint.txt" 2>&1; then cat "$TMP/lint.txt" >&2; exit 1; fi
tail -5 "$TMP/lint.txt"
if grep -q '✗' "$TMP/lint.txt"; then echo 'LINT ERRORS - fix first' >&2; exit 1; fi
hf render --fps "$FPS" --workers "${RENDER_SLOTS:-1}" -q delivery -o "$TMP/silent.mp4" .
if [ "$AUD" = '-' ]; then cp "$TMP/silent.mp4" "$OUT"; else
  ffmpeg -y -loglevel error -i "$TMP/silent.mp4" -i "$AUD" -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart "$OUT"
fi
ffprobe -v error -show_entries format=duration,size -of compact "$OUT"
