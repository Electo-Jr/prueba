"""Transcribe SOLO las ventanas de los clips con Whisper «medium» (más fiel que «small»).
Uso: PYTHONUTF8=1 python transcribir_ventanas.py <carpeta-salida>
Guarda <salida>/<clip>.json con palabras y tiempos ABSOLUTOS del vídeo de origen."""
import json
import subprocess
import sys

import numpy as np
from faster_whisper import WhisperModel

FF = "/usr/bin/ffmpeg"
SRC = "/home/user/prueba/socly-video/trabajo/podcast/"
out = sys.argv[1]
# clip: (vídeo, inicio, fin) con 1,5 s de margen
V = {
    10: ("IMG_7540", 359, 393), 9: ("IMG_7541", 245, 272), 8: ("IMG_7541", 162, 195),
    7: ("IMG_7541", 206, 240), 6: ("IMG_7540", 391, 441), 5: ("IMG_7541", 91, 128),
    4: ("IMG_7540", 227, 268), 3: ("IMG_7540", 172, 226), 2: ("IMG_7540", 110, 176),
    1: ("IMG_7540", 67, 112),
    15: ("IMG_7540", 14, 58), 16: ("IMG_7540", 266, 323), 17: ("IMG_7541", 300, 327),  # extra: suelto, blooper del nombre, final
    13: ("IMG_7541", 9, 56), 14: ("IMG_7541", 50, 76),  # extra: «petando en YouTube» y falsos arranques
    11: ("IMG_7541", 64, 93), 12: ("IMG_7541", 275, 306),  # opcionales: «mi novio Electo» y Bomberos de Benson
}
solo = [int(x) for x in sys.argv[2:]]  # opcional: solo estos clips
model = WhisperModel("medium", device="cpu", compute_type="int8")
for n, (v, a, b) in V.items():
    if solo and n not in solo:
        continue
    raw = subprocess.run([FF, "-loglevel", "error", "-ss", str(a), "-to", str(b), "-i", SRC + v + ".MOV", "-vn", "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], capture_output=True, check=True).stdout
    audio = np.frombuffer(raw, dtype=np.float32)
    segs, _ = model.transcribe(audio, language="es", word_timestamps=True, vad_filter=True,
                               initial_prompt="Podcast de Socly Style, la app de armario con inteligencia artificial. Electo y Pablo. Pregunta y respuesta en tono de humor.")
    words = [{"w": w.word.strip(), "s": round(w.start + a, 2), "e": round(w.end + a, 2)} for s in segs for w in (s.words or [])]
    json.dump(words, open(f"{out}/clip{n}.json", "w", encoding="utf-8"), ensure_ascii=False)
    print(n, " ".join(w["w"] for w in words), flush=True)
