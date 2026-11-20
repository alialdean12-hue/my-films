"""Inspect timing/transcription locally: python tools/asr.py AUDIO WHISPER_MODEL_DIR OUTPUT_JSON."""
import os, sys, json
from pathlib import Path
from faster_whisper import WhisperModel
m=WhisperModel(sys.argv[2],device='cpu', compute_type='int8', cpu_threads=int(os.getenv('ASR_THREADS','2')),local_files_only=True)
segments,_=m.transcribe(sys.argv[1],language='ar',word_timestamps=True,beam_size=4,condition_on_previous_text=False,initial_prompt='قناع الوركاء. أوروك. بغداد. نيسان وأيلول.')
words=[dict(word=w.word.strip(),start=round(w.start,3),end=round(w.end,3)) for s in segments for w in s.words];Path(sys.argv[3]).write_text(json.dumps(words,ensure_ascii=False,indent=2)+'\n')
print(' '.join(w['word'] for w in words))
