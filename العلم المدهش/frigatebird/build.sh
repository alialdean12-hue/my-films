#!/bin/sh
# Offline rebuild from committed photos, masks and selected voice; dependencies in README.md.
set -eu
cd "$(dirname "$0")"; P=$(pwd); export PYTHONDONTWRITEBYTECODE=1 PRODUCER_LOW_MEMORY_MODE=1 RENDER_SLOTS=1
T=$(mktemp -d); trap 'rm -rf "$T"' EXIT
mkdir -p out
python3 tools/art.py
python3 tools/subtitles.py
python3 tools/compose.py --stage "$T"
python3 tools/score.py
hyperframes lint "$T" > out/lint.txt
hyperframes render --fps 24 --workers 1 -q delivery --crf 20 -o "$P/out/silent.mp4" "$T"
python3 tools/master.py
node tools/covers.cjs
python3 tools/finish_covers.py
node tools/layout.cjs
python3 tools/check_master.py
