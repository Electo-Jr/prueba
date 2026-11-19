"""Vídeo «Mercadillo» (9:16, 1080x1920, 30 fps, sin voz: texto animado + música y sonidos sintetizados).
Estilo: copia la mecánica del vídeo de referencia (texto palabra a palabra con desenfoque, tarjetas apiladas, móvil que
sube inclinado, pila de mensajes que desborda, corte a negro, logo, botón «enlace en la bio», cierre que enlaza con el gancho).
Uso: PYTHONUTF8=1 python build.py [--no-render]   (salida: video/anuncios/mercadillo/mercadillo.mp4, ~6 min)
La animación es mercadillo.html (función render(t) determinista); se pinta con render.mjs fotograma a fotograma."""
import os
import shutil
import subprocess
import sys

import numpy as np
import soundfile as sf

FF = "/usr/bin/ffmpeg"
HERE = os.path.dirname(os.path.abspath(__file__))
VIDEO = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT_DIR = os.path.join(VIDEO, "anuncios", "mercadillo")
W = "/home/user/prueba/socly-video/trabajo/mercadillo-video"
FPS, SR = 30, 48000
TOTAL = 32.0
NFR = round(TOTAL * FPS)
os.makedirs(W, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)


def run(*args):
    subprocess.run([FF, "-y", "-loglevel", "error", *args], check=True, cwd=W)


# --- 1) fotogramas
fr = f"{W}/fr"
if "--no-render" not in sys.argv or not os.path.isdir(fr):
    shutil.rmtree(fr, ignore_errors=True)
    subprocess.run(["node", "render.mjs", fr, "1.875", "0", str(TOTAL - 1 / FPS), str(FPS)], check=True, cwd=HERE,
                   env=dict(os.environ, PAGE="mercadillo.html"), stdout=subprocess.DEVNULL)
got = len([f for f in os.listdir(fr) if f.endswith(".jpg")])
assert got == NFR, f"fotogramas: {got} de {NFR} (el render falló)"

# --- 2) audio sintetizado (sin derechos)
N = NFR * (SR // FPS)
rng = np.random.default_rng(11)
mus = np.zeros((N, 2), dtype=np.float32)
sfx = np.zeros((N, 2), dtype=np.float32)


def put(buf, x, t, g=1.0):
    s0 = int(t * SR)
    e = min(N, s0 + len(x))
    if 0 <= s0 < N and e > s0:
        buf[s0:e, 0] += x[: e - s0] * g
        buf[s0:e, 1] += x[: e - s0] * g


def env_(n, tau):
    return np.exp(-np.arange(n) / SR / tau)


def whoosh(dur=0.5, g=0.7):
    n = int(SR * dur)
    x = rng.standard_normal(n)
    out = np.zeros(n)
    prev = 0.0
    for i in range(n):
        a = 0.02 + 0.5 * np.sin(np.pi * i / n) ** 2
        prev += a * (x[i] - prev)
        out[i] = prev
    out -= np.convolve(out, np.ones(300) / 300, mode="same")
    out *= np.sin(np.pi * np.arange(n) / n) ** 2
    return out / (np.max(np.abs(out)) + 1e-9) * g


def pop():
    n = int(SR * 0.14)
    f = np.linspace(720, 240, n)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env_(n, 0.04)


def tap():
    n = int(SR * 0.08)
    t = np.arange(n) / SR
    return np.sin(2 * np.pi * 180 * t) * env_(n, 0.02) * 0.9 + np.sin(2 * np.pi * 900 * t) * env_(n, 0.008) * 0.3


def tick():
    n = int(SR * 0.03)
    t = np.arange(n) / SR
    return (np.sin(2 * np.pi * 2400 * t) * 0.5 + rng.standard_normal(n) * 0.25) * env_(n, 0.006)


def ding():
    n = int(SR * 1.0)
    t = np.arange(n) / SR
    a = np.sin(2 * np.pi * 1046.5 * t) * env_(n, 0.25)
    b = np.zeros(n)
    k = int(SR * 0.09)
    b[k:] = np.sin(2 * np.pi * 1568.0 * t[: n - k]) * env_(n - k, 0.32)
    return a * 0.6 + b * 0.8 + 0.25 * np.sin(2 * np.pi * 2093 * t) * env_(n, 0.12)


def sparkle():
    n = int(SR * 0.7)
    t = np.arange(n) / SR
    out = np.zeros(n)
    for i, f in enumerate([1318, 1760, 2093, 2637]):
        s0 = int(SR * 0.06 * i)
        out[s0:] += np.sin(2 * np.pi * f * t[: n - s0]) * env_(n - s0, 0.18) * 0.3
    return out


def thud():
    n = int(SR * 0.5)
    t = np.arange(n) / SR
    f = 120 * np.exp(-t * 9) + 45
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * env_(n, 0.12)
    click = rng.standard_normal(n) * env_(n, 0.006) * 0.4
    return body + click


def kick():
    n = int(SR * 0.3)
    t = np.arange(n) / SR
    f = 150 * np.exp(-t * 22) + 48
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env_(n, 0.11)


def hat():
    n = int(SR * 0.05)
    x = rng.standard_normal(n)
    x = x - np.convolve(x, np.ones(6) / 6, mode="same")
    return x * env_(n, 0.012)


def riser(dur):
    n = int(SR * dur)
    x = rng.standard_normal(n)
    out = np.zeros(n)
    prev = 0.0
    for i in range(n):
        a = 0.03 + 0.6 * (i / n) ** 2
        prev += a * (x[i] - prev)
        out[i] = prev
    out -= np.convolve(out, np.ones(200) / 200, mode="same")
    return out * (np.arange(n) / n) ** 2


def burst(dur):
    n = int(SR * dur)
    return rng.standard_normal(n) * np.where(rng.random(n) > 0.35, 1, 0.2) * np.hanning(n) * 0.9


def pad_note(freqs, dur, g):
    n = int(SR * dur)
    t = np.arange(n) / SR
    out = np.zeros(n)
    for f in freqs:
        out += np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * f * 2.003 * t) + 0.12 * np.sin(2 * np.pi * f * 3 * t)
    a = np.minimum(1, t / 0.5) * np.minimum(1, (dur - t) / 0.7)
    return out / len(freqs) * a * g


BEAT = 60 / 96
BAR = BEAT * 4
CH = [([110, 164.8, 220, 261.6], 55.0), ([87.3, 130.8, 174.6, 220], 43.65), ([130.8, 196, 261.6, 329.6], 65.4), ([98, 146.8, 196, 246.9], 49.0)]
DROP, OUTRO = 12.25, 29.25
t = 0.0
i = 0
while t < TOTAL:
    notes, root = CH[i % 4]
    gain = 0.07 if t < DROP else 0.09
    put(mus, pad_note(notes, BAR + 0.3, 1.0), t, gain * (0.6 if t < 4.5 else 1.0))
    t += BAR
    i += 1
# pulso: reloj antes del corte, bombo y bajo después
b = 0.0
while b < TOTAL:
    if b < DROP - 0.3:
        put(mus, tick(), b, 0.14 if b > 4.5 else 0.08)
    elif b < OUTRO + 1.2:
        put(mus, kick(), b, 0.30)
        root = CH[int((b - DROP) // BAR) % 4][1]
        n = int(SR * BEAT * 0.9)
        tt = np.arange(n) / SR
        put(mus, np.sin(2 * np.pi * root * 2 * tt) * env_(n, 0.25), b, 0.16)
        put(mus, hat(), b + BEAT / 2, 0.07)
    b += BEAT
fade = np.ones(N, dtype=np.float32)
k0, k1 = int(31.0 * SR), int(31.8 * SR)
fade[k0:k1] = np.linspace(1, 0, k1 - k0)
fade[k1:] = 0
mus *= fade[:, None]

# palabras que se escriben: un «tic» suave por palabra
WORDS = []
for t0, st, n in [(0.1, .27, 9), (12.3, .25, 3), (14.05, .3, 4), (15.75, .25, 3), (17.05, .22, 4), (18.3, .28, 6), (20.5, .26, 4),
                  (21.9, .26, 4), (23.5, .26, 4), (25.75, .24, 4), (26.95, .24, 4), (28.15, .22, 5), (29.7, .24, 4)]:
    WORDS += [t0 + k * st for k in range(n)]
WORDS += [4.5, 4.8, 5.1, 6.05, 6.35, 6.65, 6.9, 7.1, 7.4, 7.65]
for w in WORDS:
    put(sfx, tick(), w, 0.5)

for k, tf in enumerate([3.1, 3.45, 3.8, 4.15]):
    put(sfx, tap(), tf, 0.55)
    put(sfx, whoosh(0.18, 0.5), tf - 0.05, 0.3)
for tc in [6.1, 6.9, 7.7, 8.5]:
    put(sfx, whoosh(0.32, 0.7), tc - 0.05, 0.4)
    put(sfx, tap(), tc + 0.38, 0.35)
put(sfx, riser(2.9), 9.1, 0.35)
# mensajes: mismos tiempos que en la página (t = 9.1; hueco .42 que se acorta ×.86)
tm, gap = 9.1, .42
for i in range(22):
    put(sfx, pop(), tm, 0.10 + 0.012 * i)
    tm += gap
    gap *= .86
put(sfx, burst(0.2), 12.0, 0.45)
put(sfx, thud(), 12.22, 0.9)
for tt in [12.3, 12.55, 12.85]:
    put(sfx, tap(), tt, 0.6)
put(sfx, whoosh(0.35, 0.7), 14.0, 0.3)
put(sfx, whoosh(0.4, 0.7), 16.3, 0.3)
put(sfx, ding(), 16.5, 0.5)
put(sfx, sparkle(), 16.6, 0.4)
put(sfx, whoosh(0.5, 0.7), 17.85, 0.55)
for th in [19.75, 20.0, 20.25]:
    put(sfx, tap(), th, 0.3)
put(sfx, whoosh(0.3, 0.7), 19.45, 0.35)
put(sfx, whoosh(0.3, 0.7), 20.35, 0.4)
for tt in [18.7, 19.05, 19.3, 22.3, 24.15, 24.9]:
    put(sfx, tap(), tt, 0.55)
put(sfx, thud(), 22.45, 0.75)
put(sfx, sparkle(), 22.9, 0.5)
put(sfx, whoosh(0.5, 0.7), 25.15, 0.5)
for tt in [26.0, 26.25]:
    put(sfx, pop(), tt, 0.3)
for k in range(4):
    put(sfx, pop(), 28.45 + k * .14, 0.28)
put(sfx, ding(), 29.3, 0.55)
put(sfx, pop(), 30.0, 0.35)

mix = mus + sfx
mix /= max(1.0, np.max(np.abs(mix)) / 0.93)
sf.write(f"{W}/mezcla.wav", mix, SR)

# --- 3) unir
final = f"{OUT_DIR}/mercadillo.mp4"
run("-framerate", str(FPS), "-i", "fr/f_%04d.jpg", "-i", "mezcla.wav", "-vf", "scale=in_range=pc:out_range=tv,format=yuv420p",
    "-frames:v", str(NFR), "-c:v", "libx264", "-crf", "17", "-preset", "medium", "-c:a", "aac", "-b:a", "192k",
    "-shortest", "-movflags", "+faststart", final)
print("listo:", final)
