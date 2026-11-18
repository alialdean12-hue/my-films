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
import wave

VOICE = 'ar-SA-HamedNeural'
KIT = Path(__file__).resolve().parents[2]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def spec(ep):
    v = ep['voice']
    if (v['name'], v['rate']) != (VOICE, '-3%'):
        raise ValueError('The studio export must use its approved Hamed voice and rate.')
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
    if 'flac_sha256' in manifest:
        archive = src / 'hamed.flac'
        if sha(archive.read_bytes()) != manifest['flac_sha256']:
            raise ValueError('Unexpected Hamed archive checksum.')
        pcm = subprocess.check_output(['ffmpeg','-nostdin','-v','error','-i',str(archive),'-ac','1','-ar','48000','-f','s16le','pipe:1'])
        counts = manifest['samples_per_line']
        if (len(counts) != len(ep['beats']) or any(type(n) is not int or n <= 0 for n in counts)
            or sum(counts)*2 != len(pcm) or sha(pcm) != manifest['pcm_sha256']):
            raise ValueError('Invalid PCM or line boundaries in the recorded narration.')
        offset = 0
        for i,n in enumerate(counts):
            with wave.open(str(dest / f'b{i}.wav'),'wb') as f:
                f.setparams((1,2,48000,0,'NONE','not compressed')); f.writeframes(pcm[offset:offset+2*n]); offset+=2*n
        return
    for i in range(len(ep['beats'])):
        f = f'b{i}.wav'; data = (src / f).read_bytes()
        if manifest['files'].get(f) != sha(data) or len(data) <= 1000:
            raise ValueError('Invalid cached narration: ' + f)
        if (src/f).resolve() != (dest/f).resolve(): shutil.copyfile(src/f, dest/f)


def pack(ep, raw, directory):
    raw, out = Path(raw), Path(directory); out.mkdir(parents=True,exist_ok=True)
    materialize(ep,raw,raw)  # refuse partial, wrong-voice or stale recordings
    blocks=[]; counts=[]
    for i in range(len(ep['beats'])):
        with wave.open(str(raw/f'b{i}.wav'),'rb') as f:
            if (f.getnchannels(),f.getsampwidth(),f.getframerate())!=(1,2,48000): raise ValueError('Unexpected Hamed wave format')
            block=f.readframes(f.getnframes()); counts.append(len(block)//2); blocks.append(block)
    pcm=b''.join(blocks); f=out/'hamed.flac'
    subprocess.run(['ffmpeg','-y','-v','error','-f','s16le','-ar','48000','-ac','1','-i','pipe:0','-c:a','flac','-compression_level','8',str(f)],input=pcm,check=True)
    manifest={**spec(ep),'samples_per_line':counts,'pcm_sha256':sha(pcm),'flac_sha256':sha(f.read_bytes())}
    (out/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')


def main():
    ep = json.loads(Path(sys.argv[1]).read_text()); out = Path(sys.argv[2]).resolve(); out.mkdir(parents=True,exist_ok=True)
    info = spec(ep)
    lines = [{'id': f'b{i}', 'text': line} for i,line in enumerate(info['lines'])]
    (out/'lines.json').write_text(json.dumps(lines,ensure_ascii=False))
    subprocess.run([sys.executable,str(KIT/'scripts/tts_edge.py'), str(out/'lines.json'), str(out), '--voice',VOICE,'--rate=-3%'],check=True)
    write_manifest(ep,out)


if __name__ == '__main__':
    if len(sys.argv)==5 and sys.argv[1]=='pack': pack(json.loads(Path(sys.argv[2]).read_text()),sys.argv[3],sys.argv[4])
    else: main()
