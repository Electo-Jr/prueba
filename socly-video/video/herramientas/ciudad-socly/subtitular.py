"""Subtitulos de una palabra (amarillo, borde negro) con tiempos aproximados por plano.
Cuando exista la voz real se sustituirá por la alineación con Whisper.
Uso: PYTHONUTF8=1 python subtitular.py"""
import os, subprocess

BASE = r"/home/user/prueba/socly-video\video\herramientas\ciudad-socly"
FF = r"/usr/bin/ffmpeg"
FONT = "C\\:/Windows/Fonts/impact.ttf"
FRASES = [
    "En esta ciudad nadie sabía vestirse.", "Nadie. Bueno, nadie menos uno.", "Soclo: impecable, con estilo propio.",
    "Una ciudad de neones, fuentes y confeti.", "Y su gente, vestida como un accidente.", "Pero había otro que también vestía genial.",
    "El alcalde. ¿Su secreto? Ni idea.", "Y los tenía a todos enganchados.", "Pantallas gigantes, ofertas sin fin, anuncios.",
    "Rebajas eternas, sorteos, notificaciones sin parar.", "Nadie miraba su propio armario.", "Soclo sospechó y lo siguió.",
    "Tras una puerta secreta, un vestidor.", "Y en su móvil, Socly Style.", "Prendas subidas, looks montados, Vista puesta.",
    "Qué generoso, alcalde.", "Pantallas para ellos. Espejo para ti.", "Furioso, el alcalde intentó callarlo.",
    "Soclo reunió a toda la ciudad.", "Su elegancia no es talento: es una app.", "Todos miraron sus pintas. Después, al alcalde.",
    "Cuenta atrás: tres, dos, uno.", "Y el alcalde salió rumbo a Marte.", "En un cohete de Socly Style.",
    "Entonces todos se bajaron la app.", "Y cada uno se vistió a su manera.", "No tengo cuello, pero la bufanda me queda de lujo.",
    "Entra en Socly Style. Tu estilo manda.",
]
import json
TJ = os.path.join(BASE, "audio", "tiempos.json")
TIEMPOS = json.load(open(TJ, encoding="utf-8")) if os.path.exists(TJ) else None
partes = []
for i, fr in enumerate(FRASES):
    palabras = fr.split()
    if TIEMPOS:  # tiempos reales de la voz: cada palabra dura según su longitud
        t0, dur = TIEMPOS[i]["inicio"], TIEMPOS[i]["fin"] - TIEMPOS[i]["inicio"] + 0.12
    else:
        t0, dur = i * 2.5, 2.5
    total_c = sum(len(w) + 1 for w in palabras); acum = 0.0
    for j, w in enumerate(palabras):
        a = t0 + dur * acum / total_c; acum += len(w) + 1; b = t0 + dur * acum / total_c
        P = TIEMPOS[i].get("palabras") if TIEMPOS else None
        if P and len(P) == len(palabras):  # tiempo real de cada palabra (Whisper)
            a = P[j]["a"]; b = P[j + 1]["a"] if j + 1 < len(P) else P[j]["b"] + 0.15
        txt = w.replace("\\", "").replace("'", "").replace(":", "\\:").replace("%", "\\%")
        partes.append("drawtext=fontfile='%s':text='%s':fontsize=150:fontcolor=0xFFE500:borderw=10:bordercolor=black:"
                      "x=(w-text_w)/2:y=1540:enable='between(t,%.3f,%.3f)'" % (FONT, txt, a, b - 0.001))
filtro = "scale=1080:1920:flags=lanczos," + ",".join(partes)
fs = os.path.join(BASE, "subs-filtro.txt")
open(fs, "w", encoding="utf-8").write(filtro)
cmd = [FF, "-v", "error", "-y", "-i", os.path.join(BASE, "prueba", "ciudad-socly-completo.mp4"), "-filter_script:v", fs,
       "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", os.path.join(BASE, "prueba", "ciudad-socly-subtitulado.mp4")]
print(subprocess.run(cmd, capture_output=True, text=True).stderr[-800:] or "ok")
