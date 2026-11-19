#!/bin/sh
# Animate a geographical close-up over the real ASTER still; NOT historical footage of the discovery.
set -eu
cd "$(dirname "$0")/.."
ffmpeg -y -hide_banner -loglevel error -i img/uruk-aster.jpg -vf "scale=1800:-1,zoompan=z='1.0+0.0015*on':x='iw*(.50+.08*on/96)-iw/zoom/2':y='ih*.46-ih/zoom/2':d=96:s=960x840:fps=24,setsar=1" -frames:v 96 -c:v libx264 -threads 2 -crf 19 -preset fast -pix_fmt yuv420p -movflags +faststart assets/uruk-atlas.mp4
