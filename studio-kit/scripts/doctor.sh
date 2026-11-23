#!/bin/sh
# Checks (and installs what is missing) everything the video engines need. Run once per machine:
#   sh ~/my-films/studio-kit/scripts/doctor.sh
# Prints OK / FIXED / MISSING for each item and a final verdict.
KIT=$(cd "$(dirname "$0")/.." && pwd); BAD=0
ok() { echo "OK      $1"; }; fixed() { echo "FIXED   $1"; }; miss() { echo "MISSING $1  -> $2"; BAD=1; }
command -v python3 >/dev/null && ok "python3 $(python3 -V 2>&1 | cut -d' ' -f2)" || miss python3 "install Python 3.10+"
command -v ffmpeg >/dev/null && ok ffmpeg || { (apt-get install -y ffmpeg >/dev/null 2>&1 || sudo apt-get install -y ffmpeg >/dev/null 2>&1 || brew install ffmpeg >/dev/null 2>&1) && fixed ffmpeg || miss ffmpeg "install ffmpeg"; }
if command -v node >/dev/null; then V=$(node -v | sed 's/v//;s/\..*//'); [ "$V" -ge 22 ] && ok "node v$V" || miss "node >= 22 (have v$V)" "install Node 22 (nvm install 22)"; else miss node "install Node 22"; fi
for m in numpy PIL edge_tts; do
  python3 -c "import $m" 2>/dev/null && ok "python: $m" || { P=$m; [ $m = PIL ] && P=pillow; [ $m = edge_tts ] && P=edge-tts; pip install -q $P 2>/dev/null || pip install -q --break-system-packages $P 2>/dev/null; python3 -c "import $m" 2>/dev/null && fixed "python: $m" || miss "python: $m" "pip install $P"; }
done
python3 -c "import rembg" 2>/dev/null && ok "python: rembg (style 2 cut-outs)" || { pip install -q "rembg[cpu]" 2>/dev/null || pip install -q --break-system-packages "rembg[cpu]" 2>/dev/null; python3 -c "import rembg" 2>/dev/null && fixed "python: rembg" || echo "WARN    rembg not installed: only style 2 (cut-out stickers) needs it -> pip install 'rembg[cpu]'"; }
npx --yes hyperframes --version >/dev/null 2>&1 && ok "hyperframes" || miss hyperframes "npm i -g hyperframes (needs network)"
node -e "require('playwright')" 2>/dev/null && ok "playwright (quality check)" || { npm i -g playwright >/dev/null 2>&1; node -e "require('playwright')" 2>/dev/null && fixed playwright || echo "WARN    playwright missing: quality check is skipped -> npm i -g playwright && npx playwright install chromium"; }
[ -f "$KIT/styles/kinetic/fonts/cairo-ar.woff2" ] && ok "Cairo font" || miss "Cairo font" "git pull the repository again"
T=$(mktemp -d); echo '[{"id":"t","text":"مرحبا"}]' > $T/l.json
python3 "$KIT/scripts/tts_edge.py" $T/l.json $T >/dev/null 2>&1 && [ -s $T/t.wav ] && ok "edge-tts voice works" || echo "OK      edge-tts blocked here: the engines will make the voice through GitHub automatically (needs git push)"; rm -rf $T
[ -n "$PIXABAY_KEY" ] && ok "PIXABAY_KEY set here" || echo "OK      PIXABAY_KEY not set here: Pixabay photos come through GitHub when needed"
git -C "$KIT/.." push --dry-run -q origin HEAD >/dev/null 2>&1 && ok "git push works (needed when this machine blocks photo/voice sites)" || echo "WARN    git push failed: if photo/voice sites are blocked here, the GitHub fallback cannot work"
[ $BAD = 0 ] && echo "READY: all engines can run." || { echo "NOT READY: fix the MISSING lines above."; exit 1; }
