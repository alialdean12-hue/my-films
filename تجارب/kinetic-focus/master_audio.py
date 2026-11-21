"""Level this demo's measured PCM mix once, without rendering any picture again."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile


def ffmpeg(*args):
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', *args], check=True)


def finish(output):
    duration = str(json.loads((output / 'project/schedule.json').read_text())['D'])
    # For the seven locked takes. Mix measured -17.73 LUFS-I; the limiter
    # guards short peaks before AAC. Do not use this gain for other stories.
    filters = ('volume=4.32dB,aresample=192000,'
               'alimiter=limit=0.782:attack=5:release=60:level=0:latency=true,'
               'aresample=48000,apad')
    with tempfile.TemporaryDirectory(dir=output) as temp:
        temp = Path(temp)
        for rate, names in ((128, ['video_phone.mp4']),
                            (192, ['video.mp4', 'video_16x9.mp4', 'video_1x1.mp4'])):
            audio = temp / f'{rate}.m4a'
            ffmpeg('-i', output / 'project/out/mix.wav', '-af', filters, '-t', duration,
                   '-ac', '2', '-ar', '48000', '-c:a', 'aac', '-b:a', f'{rate}k', audio)
            for name in names:
                film = output / name
                if not film.exists():
                    continue
                ffmpeg('-i', film, '-i', audio, '-map', '0:v:0', '-map', '1:a:0',
                       '-c', 'copy', '-metadata:s:a:0', 'language=ara',
                       '-movflags', '+faststart', temp / name)
                (temp / name).replace(film)


if __name__ == '__main__':
    finish(Path(sys.argv[1]).expanduser().resolve())
