"""Transcribe un vídeo largo con Whisper (faster-whisper «small», local y gratis).
Uso: PYTHONUTF8=1 python transcribir.py <video> <salida-base>
Guarda <base>.json (palabras con tiempos) y <base>.txt (frases con [mm:ss])."""
import json
import subprocess
import sys

import numpy as np
from faster_whisper import WhisperModel

video, base = sys.argv[1], sys.argv[2]
FF = "/usr/bin/ffmpeg"
raw = subprocess.run([FF, "-loglevel", "error", "-i", video, "-vn", "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], capture_output=True, check=True).stdout
audio = np.frombuffer(raw, dtype=np.float32)
model = WhisperModel("small", device="cpu", compute_type="int8")
segments, info = model.transcribe(
    audio,
    language="es",
    word_timestamps=True,
    vad_filter=True,
    vad_parameters={"min_silence_duration_ms": 400},
    initial_prompt="Podcast de Socly Style, la app de armario y looks con inteligencia artificial, con Electo y Pablo.",
)
words, lines = [], []
for seg in segments:
    for w in seg.words or []:
        words.append({"w": w.word.strip(), "s": round(w.start, 2), "e": round(w.end, 2)})
    m, s = divmod(int(seg.start), 60)
    lines.append(f"[{m:02d}:{s:02d}] {seg.text.strip()}")
json.dump(words, open(base + ".json", "w", encoding="utf-8"), ensure_ascii=False)
open(base + ".txt", "w", encoding="utf-8").write("\n".join(lines))
print(len(words), "palabras;", f"{len(audio) / 16000:.0f}s")
