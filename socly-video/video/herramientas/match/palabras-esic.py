"""Palabras con su tiempo (ya dentro del recorte de cada clip) para subtitular los dos clips del cartel de ESIC.
El texto lo dictó el dueño (Whisper no lo saca bien); los tiempos salen de la voz (energía del audio limpio).
Uso: python palabras-esic.py <carpeta_de_salida>"""
import json
import sys

out = sys.argv[1]

# Clip 1 (dueño ante el cartel): se recorta desde 0.35 s
A0 = 0.35
a = [
    ("Madrid", 0.58, 0.98), ("está", 0.98, 1.18), ("lleno", 1.18, 1.34), ("de", 1.34, 1.38),
    ("carteles", 1.38, 1.66), ("match,", 1.66, 2.02),
    ("a", 2.44, 2.6), ("ver", 2.6, 2.64), ("cuándo", 2.64, 2.82), ("sacan", 2.82, 3.1),
    ("ya", 3.1, 3.24), ("esta", 3.24, 3.4), ("aplicación.", 3.4, 3.84),
]
# Clip 2 (socio en la escalera): se recorta desde 0.55 s
B0 = 0.55
b = [
    ("Nosotros", 0.84, 1.30), ("sí", 1.50, 1.62), ("sabemos", 1.62, 1.95), ("cómo", 1.95, 2.15),
    ("hacer", 2.15, 2.30), ("un", 2.30, 2.38), ("buen", 2.38, 2.52), ("match,", 2.52, 2.72),
    ("pero", 2.90, 3.05), ("antes,", 3.05, 3.25), ("habiendo", 3.30, 3.50), ("usado", 3.50, 3.68),
    ("Socly", 3.70, 4.00), ("Style.", 4.00, 4.22),
]
for name, words, t0 in (("a", a, A0), ("b", b, B0)):
    json.dump([{"w": w, "s": round(s - t0, 2), "e": round(e - t0, 2)} for w, s, e in words],
              open(f"{out}/{name}.json", "w", encoding="utf-8"), ensure_ascii=False)
print("ok")
