"""Voces de «Ciudad Socly» con edge-tts (gratis): narrador + Soclo. Cada frase se ajusta a su plano de 2,5 s.
Uso: PYTHONUTF8=1 python voces.py   ->  audio\\voz.wav y audio\\tiempos.json"""
import asyncio, json, os, subprocess, wave
import numpy as np
import edge_tts

BASE = r"/home/user/prueba/socly-video\video\herramientas\ciudad-socly"
AUD = os.path.join(BASE, "audio")
FF = r"/usr/bin/ffmpeg"
NARRADOR = os.environ.get("VOZ_NARRADOR", "es-MX-JorgeNeural")
SOCLO = os.environ.get("VOZ_SOCLO", "es-US-AlonsoNeural")
SR = 44100
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
SOCLO_PLANOS = {16, 17, 20, 27}  # frases que dice Soclo

def dur(path):
    r = subprocess.run([FF, "-i", path], capture_output=True, text=True).stderr
    h = r.split("Duration:")[1].split(",")[0].strip().split(":")
    return int(h[0]) * 3600 + int(h[1]) * 60 + float(h[2])

def leer(path):
    with wave.open(path) as w:
        a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    return a

async def generar():
    for i, fr in enumerate(FRASES, 1):
        voz = SOCLO if i in SOCLO_PLANOS else NARRADOR
        await edge_tts.Communicate(fr, voz, rate="+6%").save(os.path.join(AUD, "v%02d.mp3" % i))

asyncio.run(generar())
total = np.zeros(int(70.5 * SR), dtype=np.float32)
tiempos = []
for i, fr in enumerate(FRASES, 1):
    mp3 = os.path.join(AUD, "v%02d.mp3" % i); wav = os.path.join(AUD, "v%02d.wav" % i)
    d = dur(mp3)
    tempo = min(1.5, max(1.0, d / 2.38))
    subprocess.run([FF, "-v", "error", "-y", "-i", mp3, "-af", "atempo=%.3f" % tempo, "-ac", "1", "-ar", str(SR), wav], check=True)
    a = leer(wav)
    pico = np.abs(a) > 0.02
    idx = np.where(pico)[0]
    ini, fin = (idx[0], idx[-1]) if len(idx) else (0, len(a) - 1)
    a = a[ini:fin + 1]
    t0 = (i - 1) * 2.5 + 0.05
    n0 = int(t0 * SR)
    total[n0:n0 + len(a)] += a[:max(0, len(total) - n0)]
    tiempos.append({"plano": i, "frase": fr, "inicio": round(t0, 3), "fin": round(t0 + len(a) / SR, 3), "tempo": round(tempo, 2),
                    "voz": "soclo" if i in SOCLO_PLANOS else "narrador"})
    print(i, "%.2fs -> %.2fs (x%.2f)" % (d, len(a) / SR, tempo))
total = np.clip(total * 0.95, -1, 1)
with wave.open(os.path.join(AUD, "voz.wav"), "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((total * 32767).astype(np.int16).tobytes())
json.dump(tiempos, open(os.path.join(AUD, "tiempos.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok")
