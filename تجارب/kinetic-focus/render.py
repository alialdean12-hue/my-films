"""Run the shipped style-4 engine on the demo, with the archived alternative voice.
Usage: python3 render.py ~/out/test [--preview]. No network speech service required.
"""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import tempfile

from master_audio import finish

project = Path(__file__).resolve().parent
studio = project.parents[1] / 'studio-kit'
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('output', type=Path)
parser.add_argument('--preview', action='store_true')
args = parser.parse_args()
recipe = json.loads((project / 'kinetic.json').read_text())
# 11f3b22 supports absolute voice_files paths; its relative-path code expects
# an internal _dir field. Resolve here rather than editing the shared engine.
recipe['voice_files'] = str((project / recipe['voice_files']).resolve())
with tempfile.TemporaryDirectory() as temp:
    source = Path(temp) / 'kinetic.json'
    source.write_text(json.dumps(recipe, ensure_ascii=False))
    command = [sys.executable, str(studio / 'make.py'), '4', str(source), str(args.output.expanduser().resolve())]
    subprocess.run(command + (['--preview'] if args.preview else []), check=True)

if not args.preview:
    finish(args.output.expanduser().resolve())
