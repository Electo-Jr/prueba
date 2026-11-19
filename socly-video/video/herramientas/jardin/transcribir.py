"""Transcribe un vídeo con Whisper (faster-whisper, modelo «small», en local y gratis).
Uso: PYTHONUTF8=1 python transcribir.py <video.mp4> <salida.json>
Guarda palabras con su tiempo de inicio y fin."""
import json
import subprocess
import sys

import numpy as np

from faster_whisper import WhisperModel

video, out = sys.argv[1], sys.argv[2]
FF = "/usr/bin/ffmpeg"
# el lector de audio de faster-whisper falla con esta versión de PyAV: se le pasa el audio ya decodificado
raw = subprocess.run([FF, "-loglevel", "error", "-i", video, "-vn", "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], capture_output=True, check=True).stdout
audio = np.frombuffer(raw, dtype=np.float32)
model = WhisperModel("small", device="cpu", compute_type="int8")
segments, info = model.transcribe(
    audio,
    language="es",
    word_timestamps=True,
    vad_filter=True,
    vad_parameters={"min_silence_duration_ms": 300},
    initial_prompt="Socly Style, la app de armario y looks con inteligencia artificial.",
)
words = []
for seg in segments:
    for w in seg.words or []:
        words.append({"w": w.word.strip(), "s": round(w.start, 2), "e": round(w.end, 2)})
json.dump(words, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(" ".join(w["w"] for w in words))
print(f"\n{len(words)} palabras, duración {len(audio) / 16000:.1f}s")
