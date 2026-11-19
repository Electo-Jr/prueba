"""Busca momentos con energía en el audio (risas, subidas de voz) para encontrar clips.
Uso: PYTHONUTF8=1 python energia.py <video.MOV>  → imprime los picos por ventanas de 1 s (mm:ss, nivel)."""
import subprocess
import sys

import numpy as np

FF = "/usr/bin/ffmpeg"
raw = subprocess.run([FF, "-loglevel", "error", "-i", sys.argv[1], "-vn", "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], capture_output=True, check=True).stdout
a = np.frombuffer(raw, dtype=np.float32)
n = len(a) // 16000
rms = np.array([np.sqrt(np.mean(a[i * 16000:(i + 1) * 16000] ** 2)) for i in range(n)])
db = 20 * np.log10(rms + 1e-6)
print("mediana", round(float(np.median(db)), 1), "dB; máx", round(float(db.max()), 1))
# picos: segundos por encima de mediana + 6 dB, agrupados
thr = np.median(db) + 6
runs, cur = [], []
for i, v in enumerate(db):
    if v >= thr:
        cur.append(i)
    elif cur:
        runs.append(cur)
        cur = []
if cur:
    runs.append(cur)
for r in runs:
    pk = max(r, key=lambda i: db[i])
    print(f"{r[0] // 60:02d}:{r[0] % 60:02d}-{r[-1] // 60:02d}:{r[-1] % 60:02d}  pico {db[pk]:.1f} dB en {pk // 60:02d}:{pk % 60:02d}")
