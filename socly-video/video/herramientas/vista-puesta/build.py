"""Vídeo «Vista puesta» (9:16, 1080x1920, 30 fps, voz del propio clip + subtítulos + sonidos).
Uso: PYTHONUTF8=1 python build.py   (salida: video/anuncios/vista-puesta/vista-puesta.mp4, ~4 min)
Clips originales: video/anuncios/vista-puesta/clips (IMG_3911, 3913, 3914). Animaciones: vista-puesta.html/.js
(se renderizan con render.mjs). Cada segmento sale con un nº EXACTO de fotogramas (dur*30)."""
import os
import shutil
import subprocess
import sys

import numpy as np
import soundfile as sf

FF = "/usr/bin/ffmpeg"
HERE = os.path.dirname(os.path.abspath(__file__))
VIDEO = os.path.abspath(os.path.join(HERE, "..", ".."))
SRC = os.path.join(VIDEO, "anuncios", "vista-puesta", "clips")
OUT_DIR = os.path.join(VIDEO, "anuncios", "vista-puesta")
LOGO = os.path.join(VIDEO, "herramientas", "halloween-publi", "logo-blanco.png")
DENOISE = os.path.join(VIDEO, "herramientas", "jardin", "modelo", "bd.rnnn")
W = "/home/user/prueba/socly-video/trabajo/vista-puesta"
FPS, SR = 30, 48000
SKIP_RENDER = "--no-render" in sys.argv
os.makedirs(W, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)
shutil.copy("C:/Windows/Fonts/ariblk.ttf", W)
shutil.copy(DENOISE, f"{W}/bd.rnnn")

HDR = ("zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,"
       "zscale=t=bt709:m=bt709:r=tv,format=yuv420p,scale=1080:1920")


def run(*args):
    subprocess.run([FF, "-y", "-loglevel", "error", *args], check=True, cwd=W)


# --- segmentos. kind: cam (clip del móvil) | anim (animación HTML: t0 de render) | end
#     aud = (clip, inicio, fin) del audio; el vídeo de las animaciones (coche, caminando) usa el audio del hook
SEGS = [
    dict(n="hook", kind="cam", f="IMG_3911.mov", a=2.9, b=8.7),
    dict(n="car", kind="anim", r0=0.0, dur=1.6),
    dict(n="walk", kind="anim", r0=2.0, dur=1.7),
    dict(n="intro", kind="cam", f="IMG_3913.MOV", a=8.6, b=13.0),
    dict(n="func", kind="anim", r0=4.0, dur=9.3),
    dict(n="galeria", kind="anim", r0=15.0, dur=8.3),
    dict(n="end", kind="end", dur=2.6),
]
# audio continuo por bloques: (clip, inicio, fin)
AUDIO = [("IMG_3911.mov", 2.9, 12.0), ("IMG_3913.MOV", 8.6, 14.2), ("IMG_3913.MOV", 17.1, 25.2), ("IMG_3914.MOV", 4.6, 12.9)]

t0 = 0.0
for s in SEGS:
    if s["kind"] == "cam":
        s["dur"] = round((s["b"] - s["a"]) * FPS) / FPS
    s["dur"] = round(s["dur"] * FPS) / FPS
    s["t0"] = t0
    t0 += s["dur"]
TOTAL = t0
T = {s["n"]: s["t0"] for s in SEGS}
D = {s["n"]: s["dur"] for s in SEGS}
print("duración total", round(TOTAL, 2), "s")

# --- 1) animaciones: se renderizan fotograma a fotograma en Chrome
for s in SEGS:
    if s["kind"] != "anim":
        continue
    d = f"{W}/fr-{s['n']}"
    if not SKIP_RENDER or not os.path.isdir(d):
        shutil.rmtree(d, ignore_errors=True)
        env = dict(os.environ, PAGE="vista-puesta.html")
        subprocess.run(["node", "render.mjs", d, "1.875", str(s["r0"]), str(s["r0"] + s["dur"]), str(FPS)],
                       check=True, cwd=HERE, env=env, stdout=subprocess.DEVNULL)
    got = len([f for f in os.listdir(d) if f.endswith('.jpg')])
    assert got >= round(s['dur'] * FPS), f"{s['n']}: solo {got} fotogramas (el render falló)"

# --- 2) segmentos de vídeo
for s in SEGS:
    nfr = round(s["dur"] * FPS)
    out = f"{W}/{s['n']}.mp4"
    if s["kind"] == "end":
        run("-f", "lavfi", "-i", f"color=c=black:s=1080x1920:r={FPS}", "-frames:v", str(nfr),
            "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", out)
    elif s["kind"] == "anim":
        run("-framerate", str(FPS), "-i", f"fr-{s['n']}/f_%04d.jpg", "-frames:v", str(nfr),
            "-vf", "scale=in_range=pc:out_range=tv,format=yuv420p", "-c:v", "libx264", "-crf", "16", "-preset", "medium", out)
    else:
        run("-ss", str(s["a"]), "-to", str(s["b"]), "-i", f"{SRC}/{s['f']}", "-vf", f"{HDR},fps={FPS}", "-an",
            "-frames:v", str(nfr), "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", out)

# --- 3) voz: limpia, nivelada y encadenada
voice_parts = []
for i, (clip, a, b) in enumerate(AUDIO):
    wav = f"{W}/voz{i}.wav"
    run("-ss", str(a), "-to", str(b), "-i", f"{SRC}/{clip}", "-vn",
        "-af", f"highpass=f=90,arnndn=m=bd.rnnn:mix=0.75,aresample={SR}", "-ac", "2", "-ar", str(SR), wav)
    x, _ = sf.read(wav, dtype="float32")
    n = int(round((b - a) * FPS)) * (SR // FPS)
    x = x[:n] if len(x) >= n else np.pad(x, ((0, n - len(x)), (0, 0)))
    # nivel: la voz (frames por encima del ruido) a ~ -19 dBFS de RMS
    env = np.abs(x).mean(axis=1)
    thr = np.percentile(env, 70) * 0.5
    voiced = x[env > thr]
    rms = float(np.sqrt((voiced ** 2).mean())) if len(voiced) else 0.1
    gain = min(0.1122 / max(rms, 1e-4), 6.0)
    x = x * gain
    f = int(SR * 0.02)
    x[:f] *= np.linspace(0, 1, f)[:, None]
    x[-f:] *= np.linspace(1, 0, f)[:, None]
    print(f"voz {i}: rms {rms:.3f} -> ganancia {gain:.2f}")
    voice_parts.append(x)
voice = np.concatenate(voice_parts + [np.zeros((int(round(D["end"] * FPS)) * (SR // FPS), 2), dtype=np.float32)])
N = int(round(TOTAL * FPS)) * (SR // FPS)
voice = voice[:N] if len(voice) >= N else np.pad(voice, ((0, N - len(voice)), (0, 0)))

# --- 4) sonidos sintetizados (sin derechos)
rng = np.random.default_rng(5)
sfx = np.zeros((N, 2), dtype=np.float32)


def put(x, t, g=1.0):
    s0 = int(t * SR)
    e = min(N, s0 + len(x))
    if s0 < N and e > s0:
        sfx[s0:e, 0] += x[: e - s0] * g
        sfx[s0:e, 1] += x[: e - s0] * g


def env_(n, tau):
    return np.exp(-np.arange(n) / SR / tau)


def whoosh(dur=0.5):
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
    return out / (np.max(np.abs(out)) + 1e-9) * 0.7


def pop():
    n = int(SR * 0.14)
    f = np.linspace(720, 240, n)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env_(n, 0.04)


def tap():
    n = int(SR * 0.08)
    t = np.arange(n) / SR
    return np.sin(2 * np.pi * 180 * t) * env_(n, 0.02) * 0.9 + np.sin(2 * np.pi * 900 * t) * env_(n, 0.008) * 0.3


def ding():
    n = int(SR * 0.9)
    t = np.arange(n) / SR
    a = np.sin(2 * np.pi * 1046.5 * t) * env_(n, 0.22)
    b = np.zeros(n)
    k = int(SR * 0.09)
    b[k:] = np.sin(2 * np.pi * 1568.0 * t[: n - k]) * env_(n - k, 0.30)
    return a * 0.6 + b * 0.8 + 0.25 * np.sin(2 * np.pi * 2093 * t) * env_(n, 0.12)


def sparkle():
    n = int(SR * 0.7)
    t = np.arange(n) / SR
    out = np.zeros(n)
    for i, f in enumerate([1318, 1760, 2093, 2637]):
        s0 = int(SR * 0.06 * i)
        out[s0:] += np.sin(2 * np.pi * f * t[: n - s0]) * env_(n - s0, 0.18) * 0.3
    return out


put(whoosh(0.4), T["car"] - 0.15, 0.55)
put(whoosh(0.35), T["walk"] - 0.1, 0.5)
put(whoosh(0.45), T["intro"] - 0.15, 0.5)
F = T["func"] + 1.2
put(whoosh(0.4), T["func"] - 0.12, 0.45)
put(pop(), T["func"] + 0.4, 0.3)
put(tap(), F + 2.3, 0.7)
put(whoosh(0.35), F + 2.4, 0.35)
put(sparkle(), F + 3.95, 0.7)
put(pop(), F + 6.5, 0.4)
G = T["galeria"]
put(whoosh(0.4), G - 0.12, 0.45)
put(tap(), G + 1.1, 0.7)
put(whoosh(0.35), G + 1.2, 0.35)
for k in range(3):
    put(whoosh(0.25), G + 2.28 + 0.55 * k, 0.3)
put(pop(), G + 3.75, 0.4)
put(whoosh(0.4), G + 6.7, 0.45)
put(ding(), G + 7.5, 0.55)
put(whoosh(0.5), T["end"] - 0.25, 0.5)
put(pop(), T["end"] + 0.35, 0.35)
mix = voice + sfx
mix /= max(1.0, np.max(np.abs(mix)) / 0.95)
sf.write(f"{W}/mezcla.wav", mix, SR)

# --- 5) subtítulos (ASS): Arial Black, mayúsculas, borde. Tiempos de la transcripción con Whisper.
GOLD, WHITE = r"{\c&H004BB8F2&}", r"{\c&H00FFFFFF&}"
pop_tag = r"{\fscx84\fscy84\t(0,90,\fscx107\fscy107)\t(90,170,\fscx100\fscy100)}"


def ts(t):
    return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"


EV = []


def cap(a, b, text, mv=330):
    EV.append((a, b, pop_tag + text, mv))


H = lambda c: T["hook"] + (c - 2.9)        # tiempo del clip 3911 -> tiempo del vídeo
I = lambda c: T["intro"] + (c - 8.6)       # clip 3913 (presentación)
Fn = lambda c: T["func"] + 1.2 + (c - 17.1)      # clip 3913 (voz sobre la animación)
Gl = lambda c: T["galeria"] + (c - 4.6)    # clip 3914
cap(H(3.18), H(4.28), "Y SI TE DIJERA", 420)
cap(H(4.28), H(6.10), "QUE HEMOS CREADO\\NUNA " + GOLD + "APLICACIÓN", 420)
cap(H(6.10), H(8.20), "CON LA QUE PUEDES\\NVER " + GOLD + "TUS OUTFITS", 420)
cap(H(8.46), H(10.30), "YA SEA DESDE\\N" + GOLD + "TU COCHE", 330)
cap(H(10.50), H(12.00), GOLD + "CAMINANDO" + WHITE + "\\NCON TUS AMIGOS", 330)
cap(I(8.82), I(10.96), "LA APLICACIÓN SE LLAMA\\N" + GOLD + "SOCLY STYLE", 420)
cap(I(10.96), I(12.46), "Y HEMOS AÑADIDO UNA\\N" + GOLD + "NUEVA FUNCIONALIDAD", 420)
cap(I(12.46), I(14.20), "QUE TE VA\\NA ENCANTAR", 300)
cap(Fn(17.28), Fn(18.54), "CON ESTA\\NFUNCIONALIDAD", 300)
cap(Fn(18.54), Fn(21.22), "LO QUE PUEDES ES\\NVER TU OUTFIT", 300)
cap(Fn(21.22), Fn(22.72), "COMO SI FUESE\\NUN " + GOLD + "MANIQUÍ", 300)
cap(Fn(22.72), Fn(24.02), "UN POCO\\NMÁS MODERNO", 300)
cap(Fn(24.02), Fn(25.20), "UN MANIQUÍ\\N" + GOLD + "INVISIBLE", 300)
cap(Gl(4.87), Gl(6.10), "Y ASÍ TE PUEDES\\NIMAGINAR TÚ", 300)
cap(Gl(6.10), Gl(8.27), "DE FORMA MÁS\\N" + GOLD + "FÁCIL Y EFICIENTE", 300)
cap(Gl(8.27), Gl(10.95), "CÓMO ES TU OUTFIT\\NANTES DE " + GOLD + "TU EVENTO", 300)
cap(Gl(11.43), Gl(12.90), GOLD + "TÚ COMPARAS" + WHITE + "\\NCÓMO TE QUEDA", 300)
E = T["end"]
EV.append((E + 0.25, E + D["end"], r"{\an5\pos(540,1010)\fs58}" + "VISTA PUESTA", 0))
EV.append((E + 0.50, E + D["end"], r"{\an5\pos(540,1100)\fs44}" + GOLD + "TU OUTFIT, ANTES DE SALIR", 0))
EV.append((E + 1.2, E + D["end"], r"{\an5\pos(540,1560)\fs44\c&H004BB8F2&}" + "ENLACE EN LA BIO", 0))

head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Tik,Arial Black,70,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,0,0,0,0,100,100,0,0,1,7,2,2,60,60,470,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
with open(f"{W}/subs.ass", "w", encoding="utf-8") as fh:
    fh.write(head)
    for a, b, text, mv in EV:
        fh.write(f"Dialogue: 0,{ts(a)},{ts(max(a + 0.05, b - 0.04))},Tik,,0,0,{mv},,{WHITE}{text}\n")

# --- 6) unir todo
with open(f"{W}/lista.txt", "w") as fh:
    for s in SEGS:
        fh.write(f"file '{W}/{s['n']}.mp4'\n")
run("-f", "concat", "-safe", "0", "-i", f"{W}/lista.txt", "-c", "copy", f"{W}/base.mp4")
fc = ["[1:v]scale=420:-1,format=rgba[logo]",
      f"[0:v][logo]overlay=x=(W-w)/2:y=560:enable='between(t,{E + 0.1},{TOTAL})'[v0]",
      "[v0]subtitles=subs.ass:fontsdir=.[vf]"]
final = f"{OUT_DIR}/vista-puesta.mp4"
run("-i", f"{W}/base.mp4", "-loop", "1", "-i", LOGO, "-i", f"{W}/mezcla.wav", "-filter_complex", ";".join(fc),
    "-map", "[vf]", "-map", "2:a", "-t", f"{TOTAL:.3f}", "-c:v", "libx264", "-crf", "17", "-preset", "medium",
    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", final)
print("listo:", final)
