"""Produce and verify the *unprocessed* Hamed stems for one approved episode.

The doll filter is applied separately by make_episode.py, exactly as in the pilot.
A cache cannot silently supply an old line, another requested voice, or a changed file.
"""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

VOICE = 'ar-SA-HamedNeural'
KIT = Path(__file__).resolve().parents[2]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def spec(ep):
    v = ep['voice']; assert v['name'] == VOICE and v['rate'] == '-3%'
    return {'voice': v['name'], 'rate': v['rate'], 'lines': [b['line'] for b in ep['beats']]}


def write_manifest(ep, out):
    pack = spec(ep)
    pack['files'] = {f'b{i}.wav': sha((out / f'b{i}.wav').read_bytes()) for i in range(len(ep['beats']))}
    (out / 'manifest.json').write_text(json.dumps(pack, ensure_ascii=False, indent=2) + '\n')


def materialize(ep, directory, dest):
    src, dest = Path(directory), Path(dest)
    manifest = json.loads((src / 'manifest.json').read_text())
    if any(manifest.get(k) != v for k,v in spec(ep).items()):
        raise ValueError('Narration cache does not match the script, rate and Hamed voice.')
    dest.mkdir(parents=True, exist_ok=True)
    for i in range(len(ep['beats'])):
        f = f'b{i}.wav'; data = (src / f).read_bytes()
        if manifest['files'].get(f) != sha(data) or len(data) <= 1000:
            raise ValueError('Invalid cached narration: ' + f)
        if (src/f).resolve() != (dest/f).resolve(): shutil.copyfile(src/f, dest/f)


def main():
    ep = json.loads(Path(sys.argv[1]).read_text()); out = Path(sys.argv[2]).resolve(); out.mkdir(parents=True,exist_ok=True)
    info = spec(ep)
    lines = [{'id': f'b{i}', 'text': line} for i,line in enumerate(info['lines'])]
    (out/'lines.json').write_text(json.dumps(lines,ensure_ascii=False))
    subprocess.run([sys.executable,str(KIT/'scripts/tts_edge.py'), str(out/'lines.json'), str(out), '--voice',VOICE,'--rate=-3%'],check=True)
    write_manifest(ep,out)


if __name__ == '__main__': main()
