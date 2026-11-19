"""Une las palabras de los 4 clips en una sola línea de tiempo (ya con los recortes), con las correcciones a mano.
Uso: python palabras.py <salida.json>
Las transcripciones de Whisper están en palabras\\ (salen de herramientas\\jardin\\transcribir.py)."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
out = sys.argv[1]

# (archivo, inicio del recorte, fin del recorte, {indice: texto}) — "" quita la palabra
CLIPS = [
    ("1-IMG_7340", 0.0, 5.85, {}),
    ("2-IMG_7352", 0.55, 5.60, {}),
    # «va a aprender»: Whisper oyó «va a prender»
    ("3-IMG_7349", 0.0, 14.10, {12: "aprender", 24: "qué"}),
    ("4-IMG_7364", 0.0, 5.54, {3: "haces,"}),
]

words = []
offset = 0.0
for name, t0, t1, fix in CLIPS:
    for i, w in enumerate(json.load(open(os.path.join(HERE, "palabras", name + ".json"), encoding="utf-8"))):
        text = fix.get(i, w["w"])
        if not text or w["e"] <= t0 or w["s"] >= t1:
            continue
        # «va a aprender»: la «a» suelta de Whisper y «prender» comparten sonido
        s, e = w["s"], w["e"]
        words.append({"w": text, "s": round(max(s, t0) - t0 + offset, 2), "e": round(min(e, t1) - t0 + offset, 2)})
    offset += t1 - t0

json.dump(words, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(words), "palabras; duración total", round(offset, 2), "s")
