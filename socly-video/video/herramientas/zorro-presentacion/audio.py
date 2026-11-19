"""Prepara los datos del vídeo del zorro a partir de la voz.
Uso: PYTHONUTF8=1 python audio.py <voz.wav>
Escribe datos.js con: duración, envolvente de volumen por fotograma (para mover la boca) y las
palabras con sus tiempos (Whisper local, gratis) para los subtítulos y los efectos."""
import json
import subprocess
import sys

import numpy as np
from faster_whisper import WhisperModel

wav = sys.argv[1]
FF = "/usr/bin/ffmpeg"
FPS = 30

raw = subprocess.run([FF, "-loglevel", "error", "-i", wav, "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], capture_output=True, check=True).stdout
audio = np.frombuffer(raw, dtype=np.float32)
dur = len(audio) / 16000

# Envolvente: RMS por ventana de 1/FPS s, suavizada y normalizada (0..1).
win = 16000 // FPS
n = len(audio) // win
rms = np.sqrt(np.mean(audio[: n * win].reshape(n, win) ** 2, axis=1))
rms = np.convolve(rms, np.array([0.25, 0.5, 0.25]), mode="same")
top = np.percentile(rms, 95) or 1.0
env = np.clip(rms / top, 0, 1)
env[env < 0.08] = 0.0  # silencios: boca cerrada

model = WhisperModel("small", device="cpu", compute_type="int8")
segments, _ = model.transcribe(
    audio,
    language="es",
    word_timestamps=True,
)
words = []
for seg in segments:
    for w in seg.words or []:
        words.append({"w": w.word.strip(), "s": round(w.start, 2), "e": round(w.end, 2)})

# Los subtítulos usan el texto del guion (Whisper oye «Soclistahil»): se alinea por orden y, donde
# Whisper falla, se reparte el tiempo entre las palabras vecinas que sí reconoció.
import difflib
import re
import unicodedata


def norm(t):
    t = unicodedata.normalize("NFD", t.lower())
    return re.sub(r"[^a-z0-9]", "", "".join(c for c in t if unicodedata.category(c) != "Mn"))


script = open("guion.txt", encoding="utf-8").read().split()
heard = [w for w in words if norm(w["w"])]
sm = difflib.SequenceMatcher(None, [norm(w) for w in script], [norm(w["w"]) for w in heard], autojunk=False)
start = [None] * len(script)
end = [None] * len(script)
for blk in sm.get_matching_blocks():
    for k in range(blk.size):
        start[blk.a + k] = heard[blk.b + k]["s"]
        end[blk.a + k] = heard[blk.b + k]["e"]
# Huecos: interpolar entre el ancla anterior y la siguiente.
i = 0
while i < len(script):
    if start[i] is not None:
        i += 1
        continue
    j = i
    while j < len(script) and start[j] is None:
        j += 1
    t0 = end[i - 1] if i > 0 else 0.0
    t1 = start[j] if j < len(script) else dur
    step = (t1 - t0) / (j - i)
    for k in range(i, j):
        start[k] = round(t0 + step * (k - i), 2)
        end[k] = round(t0 + step * (k - i + 1), 2)
    i = j
aligned = [{"w": script[k], "s": start[k], "e": end[k]} for k in range(len(script))]

data = {"fps": FPS, "dur": round(dur, 2), "env": [round(float(x), 2) for x in env], "words": aligned}
open("datos.js", "w", encoding="utf-8").write("window.DATA = " + json.dumps(data, ensure_ascii=False) + ";" + chr(10))
print("duración", round(dur, 2), "s;", len(aligned), "palabras")
print(" ".join(f"{w['w']}@{w['s']}" for w in aligned))
