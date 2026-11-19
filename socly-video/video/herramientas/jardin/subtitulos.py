"""Crea subtítulos .ass estilo TikTok (mayúsculas, 2-3 palabras, la palabra que se dice en dorado).
Uso: PYTHONUTF8=1 python subtitulos.py <palabras.json> <correcciones.json> <salida.ass>
`correcciones.json`: {"indice": "texto"} para cambiar lo que Whisper entendió mal ("" = quitar la palabra)."""
import json
import os
import re
import sys

words_file, fix_file, out = sys.argv[1:4]
# EMPH=1: las palabras de KEYS (separadas por comas) crecen al decirse
EMPH = os.environ.get("EMPH") == "1"
KEYS = {k.strip().lower() for k in os.environ.get("KEYS", "").split(",") if k.strip()}
words = json.load(open(words_file, encoding="utf-8"))
fixes = json.load(open(fix_file, encoding="utf-8"))
for i, w in enumerate(words):
    if str(i) in fixes:
        w["w"] = fixes[str(i)]
words = [w for w in words if w["w"]]

GOLD = r"{\c&H004BB8F2&}"
WHITE = r"{\c&H00FFFFFF&}"


def clean(t):
    return re.sub(r"[,.;:]+$", "", t).upper()


# grupos de hasta 3 palabras: se corta antes si hay pausa, signo de cierre o demasiadas letras
groups, cur = [], []
for i, w in enumerate(words):
    if cur:
        gap = w["s"] - cur[-1]["e"]
        ends = re.search(r"[.?!]$", cur[-1]["w"])
        chars = sum(len(x["w"]) + 1 for x in cur) + len(w["w"])
        if len(cur) >= 3 or gap > 0.35 or ends or chars > 22:
            groups.append(cur)
            cur = []
    cur.append(w)
if cur:
    groups.append(cur)


def ts(t):
    h, m, s = int(t // 3600), int(t % 3600 // 60), t % 60
    return f"{h}:{m:02d}:{s:05.2f}"


head = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Tik,Arial Black,78,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,0,0,0,0,100,100,0,0,1,7,2,2,60,60,660,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
lines = []
for gi, g in enumerate(groups):
    nxt = groups[gi + 1][0]["s"] if gi + 1 < len(groups) else g[-1]["e"] + 0.4
    for k, w in enumerate(g):
        start = g[k]["s"] if k == 0 else g[k - 1].get("_end", g[k]["s"])
        # la palabra se queda hasta que empieza la siguiente; la última del grupo aguanta un poco
        end = g[k + 1]["s"] if k + 1 < len(g) else min(g[-1]["e"] + 0.3, nxt)
        end = max(end, start + 0.05)
        def piece(j, x):
            word = clean(x["w"])
            if j == k and EMPH and re.sub(r"[^0-9a-záéíóúñ%]", "", x["w"].lower()) in KEYS:
                # palabra clave: aparece más pequeña, crece de golpe y se queda un poco más grande mientras se dice
                return GOLD + r"{\fscx86\fscy86\t(0,90,\fscx126\fscy126)\t(90,180,\fscx118\fscy118)}" + word + r"{\fscx100\fscy100}"
            return (GOLD if j == k else WHITE) + word

        text = " ".join(piece(j, x) for j, x in enumerate(g))
        # POP=1: al entrar cada grupo, un pequeño rebote (se encoge y crece en 0,17 s)
        if os.environ.get("POP") == "1" and k == 0:
            text = r"{\fscx84\fscy84\t(0,90,\fscx107\fscy107)\t(90,170,\fscx100\fscy100)}" + text
        w["_end"] = end
        lines.append(f"Dialogue: 0,{ts(start)},{ts(end)},Tik,,0,0,0,,{text}")

open(out, "w", encoding="utf-8").write(head + "\n".join(lines) + "\n")
print(len(groups), "grupos,", len(lines), "líneas")
