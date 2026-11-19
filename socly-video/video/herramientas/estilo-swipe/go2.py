"""Versión 2 del vídeo «el motor aprende tu estilo»: más ritmo, sin parecer barato.

Qué añade a la versión 1 (go.sh):
  1. Gancho en pantalla en el primer segundo.
  2. Pausas largas recortadas (y el silencio de antes de hablar).
  3. Zoom de énfasis: se alterna plano normal y plano cerrado en cada frase (con un empuje lento).
  4. Subtítulos con un pequeño «pop» al entrar.
  5. Sonidos sutiles (pop y whoosh generados aquí, sin derechos) al aparecer el gancho, el móvil y las tarjetas.
  6. Un «VS» entre las dos tarjetas del duelo.
Cortes directos entre escenas (nada de transiciones).

Uso: python go2.py      (necesita antes `bash go.sh`: deja en la carpeta de trabajo los clips s1-s4 y la grabación)
Salida: video\\anuncios\\estilo-swipe\\estilo-swipe-v2[-subtitulado][-25mb].mp4
"""
import json
import math
import os
import shutil
import subprocess
import struct
import wave

import numpy as np

FF = "/usr/bin/ffmpeg"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, "..", "..", "anuncios", "estilo-swipe"))
W = "/home/user/prueba/socly-video/trabajo/estilo-swipe"
V2 = os.path.join(W, "v2")
os.makedirs(V2, exist_ok=True)
os.environ["PYTHONUTF8"] = "1"


def run(cmd, cwd=None):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        raise SystemExit(f"falló: {' '.join(cmd)[:300]}\n{r.stderr[-1500:]}")
    return r


# ---------------------------------------------------------------------------
# 1) Plan: tramos que se conservan de cada clip y el zoom de cada tramo
#    (clip, desde, hasta, zoom_inicial, zoom_final, rampa): tiempos del propio clip (s1..s4.mp4).
#    rampa > 0: el zoom pasa suave desde el del tramo anterior en esos segundos; 0 = corte seco.
# ---------------------------------------------------------------------------
Z_OUT = (1.00, 1.015)  # plano normal con un empuje muy lento
Z_IN = (1.05, 1.065)   # plano cerrado, leve
GAP = 0.035            # al recortar una pausa se deja este margen a cada lado

SEGS = [
    (1, 0.30, 2.13, *Z_OUT, 0),
    (1, 2.13, 3.51, *Z_IN, 0.18),
    (1, 3.51, 5.85, *Z_OUT, 0.18),
    # el clip 2 empieza en 0,55 s del original: sus tiempos van restados
    # clip 2: él camina con la cámara en la mano; sin zoom para no sumar movimiento
    (2, 0.20, 5.05, 1.0, 1.0, 0),
    # el clip 3: pausas recortadas (4,63-4,92 · 6,94-7,29 · 10,14-10,48 · 12,54-12,76)
    (3, 0.00, 4.634 + GAP, *Z_OUT, 0),
    (3, 4.917 - GAP, 6.943 + GAP, *Z_IN, 0),
    (3, 7.294 - GAP, 10.135 + GAP, *Z_OUT, 0),
    (3, 10.482 - GAP, 12.540 + GAP, *Z_IN, 0),
    (3, 12.764 - GAP, 14.10, *Z_OUT, 0),
    # el clip 4 (el despertar) se queda como está: sus pausas son el chiste
    (4, 0.00, 5.54, 1.0, 1.0, 0),
]
# Todos los cortes caen en un fotograma exacto (30 fps): si no, cada tramo pierde o gana un fotograma y el
# vídeo se adelanta o se atrasa respecto al audio, hasta 0,3 s al final.
FPS = 30
# Los clips s1..s4.mp4 tienen estos fotogramas (el último tramo no puede pedir más: si lo pide, el plan se adelanta al vídeo real)
CLIP_FRAMES = {1: 175, 2: 151, 3: 422, 4: 165}
SEGS = [(c, round(a * FPS) / FPS, min(round(b * FPS), CLIP_FRAMES[c]) / FPS, z0, z1, r) for (c, a, b, z0, z1, r) in SEGS]
CLIP_START_IN_ORIGINAL = {1: 0.0, 2: 0.55, 3: 0.0, 4: 0.0}   # para pasar las palabras de Whisper al tiempo del clip
NAMES = {1: "1-IMG_7340", 2: "2-IMG_7352", 3: "3-IMG_7349", 4: "4-IMG_7364"}

# línea de tiempo global: dónde empieza cada tramo
starts = []
t = 0.0
for c, a, b, *_ in SEGS:
    starts.append(t)
    t += b - a
TOTAL = t


def to_global(clip, tc):
    """Tiempo de un clip -> tiempo del vídeo final (lo que cae en una pausa recortada se queda en el borde)."""
    best = None
    for (c, a, b, *_), g in zip(SEGS, starts):
        if c != clip:
            continue
        if a <= tc <= b:
            return g + (tc - a)
        if tc < a and best is None:
            best = g
        if tc > b:
            best = g + (b - a)
    return best if best is not None else 0.0


# ---------------------------------------------------------------------------
# 2) Palabras (Whisper + correcciones) en el tiempo del vídeo final
# ---------------------------------------------------------------------------
FIX = {3: {12: "aprender", 24: "qué"}, 4: {3: "haces,"}}
words = []
for clip in (1, 2, 3, 4):
    data = json.load(open(os.path.join(HERE, "palabras", NAMES[clip] + ".json"), encoding="utf-8"))
    for i, w in enumerate(data):
        text = FIX.get(clip, {}).get(i, w["w"])
        s = w["s"] - CLIP_START_IN_ORIGINAL[clip]
        e = w["e"] - CLIP_START_IN_ORIGINAL[clip]
        if clip == 1 and i == 0:
            s = 0.44  # Whisper pone la primera palabra al principio del todo; el audio empieza a los 0,44 s
        if e <= 0:
            continue
        words.append({"w": text, "s": round(to_global(clip, max(s, 0.0)), 3), "e": round(to_global(clip, e), 3)})
json.dump(words, open(os.path.join(V2, "palabras.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# ---------------------------------------------------------------------------
# 3) Tiempos de las capas (los de los gestos del clip 3, pasados al vídeo final)
# ---------------------------------------------------------------------------
g3 = lambda t: to_global(3, t)
plan = {
    "swipeIn": g3(7.45), "swipeOut": g3(10.05), "recStart": g3(7.55), "recFrames": 72,
    "dlIn": g3(11.35), "drIn": g3(11.75), "vsIn": g3(12.0), "duelOut": g3(14.0),
}
json.dump(plan, open(os.path.join(V2, "plan.json"), "w"), indent=1)
print("duración final", round(TOTAL, 2), "s ·", {k: round(v, 2) for k, v in plan.items() if k != "recFrames"})

# ---------------------------------------------------------------------------
# 4) Sonidos (pop y whoosh) — síntesis propia, sin derechos
# ---------------------------------------------------------------------------
SR = 48000


def write_wav(name, data):
    data = np.clip(data, -1, 1)
    with wave.open(os.path.join(V2, name), "wb") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(SR)
        f.writeframes((data * 32767).astype("<i2").tobytes())


def pop(f0, f1, dur=0.11, peak=0.55):
    n = int(SR * dur)
    x = np.arange(n) / SR
    freq = f1 + (f0 - f1) * np.exp(-x * 38)
    ph = 2 * np.pi * np.cumsum(freq) / SR
    env = np.exp(-x * 34) * np.minimum(1, x / 0.004)
    return peak * np.sin(ph) * env


def whoosh(dur=0.42, peak=0.5):
    n = int(SR * dur)
    rng = np.random.default_rng(7)
    noise = rng.standard_normal(n)
    x = np.arange(n) / SR
    # filtro de paso de banda que sube (barrido): media móvil exponencial con coeficiente variable
    out = np.zeros(n)
    lp1 = lp2 = 0.0
    for i in range(n):
        fc = 400 + 5200 * (x[i] / dur) ** 1.6
        a = 1 - math.exp(-2 * math.pi * fc / SR)
        lp1 += a * (noise[i] - lp1)
        lp2 += a * (lp1 - lp2)
        out[i] = lp1 - lp2
    env = np.sin(np.pi * x / dur) ** 1.8
    out = out * env
    return peak * out / (np.max(np.abs(out)) + 1e-9)


write_wav("pop1.wav", pop(1100, 380))
write_wav("pop2.wav", pop(1500, 520, 0.1, 0.5))
write_wav("whoosh.wav", whoosh())
SFX = [("pop1.wav", plan["swipeIn"] + 0.04), ("pop1.wav", plan["dlIn"] + 0.04),
       ("pop1.wav", plan["drIn"] + 0.04), ("pop2.wav", plan["vsIn"] + 0.04),
       ("pop2.wav", TOTAL + 0.1)]  # el logo de la pantalla final

# ---------------------------------------------------------------------------
# 5) Grabación de pantalla (72 fotogramas) y capas transparentes
# ---------------------------------------------------------------------------
if not os.path.isdir(os.path.join(W, "rec")):
    raise SystemExit("falta la grabación: ejecuta antes bash go.sh")

for name, a, b in (("ov-swipe", plan["swipeIn"], plan["swipeOut"]), ("ov-duelo", plan["dlIn"], plan["duelOut"])):
    shutil.rmtree(os.path.join(V2, name), ignore_errors=True)
    run(["node", os.path.join(HERE, "render-overlays.mjs"), os.path.join(V2, name), os.path.join(W, "rec"),
         f"{a:.3f}", f"{b:.3f}", "30", os.path.join(V2, "plan.json")])

# pantalla final: fondo negro, logo blanco, «Socly Style» y «enlace en la bio» (2 s, 60 fotogramas)
CARD_FRAMES = 60
shutil.rmtree(os.path.join(V2, "endcard"), ignore_errors=True)
subprocess.run(["node", os.path.join(HERE, "render-overlays.mjs"), os.path.join(V2, "endcard"), os.path.join(W, "rec"), "0",
                f"{(CARD_FRAMES - 1) / 30:.4f}", "30", os.path.join(V2, "plan.json")],
               check=True, env=dict(os.environ, PAGE="endcard.html", OPAQUE="1"))

# ---------------------------------------------------------------------------
# 6) Subtítulos
# ---------------------------------------------------------------------------
json.dump({}, open(os.path.join(V2, "fix.json"), "w"))
env = dict(os.environ, EMPH="1", KEYS="17,100%,swipe,duelo,tinder,estilo,aprender")
subprocess.run(["python", os.path.join(HERE, "..", "jardin", "subtitulos.py"), os.path.join(V2, "palabras.json"),
                os.path.join(V2, "fix.json"), os.path.join(V2, "estilo-swipe.ass")], check=True, env=env)
shutil.copy("C:/Windows/Fonts/ariblk.ttf", V2)

# ---------------------------------------------------------------------------
# 7) Montaje
# ---------------------------------------------------------------------------
inputs = []
for k in (1, 2, 3, 4):
    inputs += ["-i", os.path.join(W, f"s{k}.mp4")]
n_clips = 4
overlay_inputs = [("ov-swipe", plan["swipeIn"]), ("ov-duelo", plan["dlIn"])]
for name, off in overlay_inputs:
    inputs += ["-itsoffset", f"{off:.3f}", "-framerate", "30", "-i", os.path.join(V2, name, "s_%04d.png")]
inputs += ["-framerate", "30", "-i", os.path.join(V2, "endcard", "s_%04d.png")]
card_idx = n_clips + len(overlay_inputs)
sfx_first = card_idx + 1
for name, _ in SFX:
    inputs += ["-i", os.path.join(V2, name)]

f = []
prev_end = {}
labels_v, labels_a = [], []
for idx, (clip, a, b, z0, z1, ramp) in enumerate(SEGS):
    dur = b - a
    vin = f"[{clip - 1}:v]"
    chain = f"{vin}trim=start_frame={round(a * FPS)}:end_frame={round(b * FPS)},setpts=PTS-STARTPTS"
    if z0 != 1.0 or z1 != 1.0:
        zprev = prev_end.get(clip, z0) if ramp > 0 else z0
        base = f"({z0}+({z1}-{z0})*t/{dur:.3f})"
        if ramp > 0:
            r = f"min(1,t/{ramp})"
            sm = f"({r}*{r}*(3-2*{r}))"
            Z = f"({zprev}+({base}-{zprev})*{sm})"
        else:
            Z = base
        # se sube a 2x, se hace el zoom ahí (el redondeo a píxeles pesa la mitad) y se baja otra vez
        chain += (f",scale=2160:3840:flags=lanczos,scale=w='trunc(2160*{Z}/2)*2':h='trunc(3840*{Z}/2)*2':eval=frame:flags=bicubic"
                  f",crop=2160:3840:x='(iw-2160)/2':y='(ih-3840)*0.3',scale=1080:1920:flags=lanczos")
    prev_end[clip] = z1
    f.append(f"{chain},setsar=1[v{idx}]")
    fade = 0.01
    f.append(f"[{clip - 1}:a]atrim={round(a * FPS) / FPS:.4f}:{round(b * FPS) / FPS:.4f},asetpts=PTS-STARTPTS,afade=t=in:d={fade},afade=t=out:st={max(dur - fade, 0):.3f}:d={fade},aresample=48000[a{idx}]")
    labels_v.append(f"[v{idx}]")
    labels_a.append(f"[a{idx}]")

n = len(SEGS)
f.append("".join(labels_v) + f"concat=n={n}:v=1:a=0[vc]")
f.append("".join(labels_a) + f"concat=n={n}:v=0:a=1[ac]")
f.append(f"[vc][{n_clips}:v]overlay=eof_action=pass:format=auto[o1]")
f.append(f"[o1][{n_clips + 1}:v]overlay=eof_action=pass:format=auto[o2]")
f.append("[ac]loudnorm=I=-16:TP=-1.5:LRA=11,aformat=channel_layouts=stereo,apad=pad_dur=2.0[dial]")
mix_in = "[dial]"
for j, (name, at) in enumerate(SFX):
    ms = int(at * 1000)
    f.append(f"[{sfx_first + j}:a]aformat=sample_rates=48000:channel_layouts=stereo,adelay={ms}|{ms},volume=0.42[x{j}]")
    mix_in += f"[x{j}]"
f.append(f"{mix_in}amix=inputs={len(SFX) + 1}:normalize=0:duration=first[amix]")
graph_base = ";\n".join(f)


def render(out_name, subtitles):
    sub = f",subtitles=estilo-swipe.ass:fontsdir=." if subtitles else ""
    graph = graph_base + f";\n[o2]format=yuv420p{sub}[vmain];\n[{card_idx}:v]format=yuv420p,setsar=1[card];\n[vmain][card]concat=n=2:v=1:a=0[vfinal]"
    out = os.path.join(OUT, out_name)
    run([FF, "-y", "-loglevel", "error", *inputs, "-filter_complex", graph, "-map", "[vfinal]", "-map", "[amix]",
         "-t", f"{TOTAL + CARD_FRAMES / 30:.3f}", "-c:v", "libx264", "-crf", "16", "-preset", "slow", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", out], cwd=V2)
    print("listo:", out)
    return out


render("estilo-swipe-v2.mp4", False)
big = render("estilo-swipe-v2-subtitulado.mp4", True)

# copia de unos 25 MB (2 pasadas)
small = os.path.join(OUT, "estilo-swipe-v2-subtitulado-25mb.mp4")
run([FF, "-y", "-loglevel", "error", "-i", big, "-c:v", "libx264", "-b:v", "6100k", "-preset", "slow", "-pass", "1",
     "-passlogfile", "p25", "-an", "-f", "null", "NUL"], cwd=V2)
run([FF, "-y", "-loglevel", "error", "-i", big, "-c:v", "libx264", "-b:v", "6100k", "-preset", "slow", "-pass", "2",
     "-passlogfile", "p25", "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", small], cwd=V2)
print("listo:", small, round(os.path.getsize(small) / 1e6, 1), "MB")
