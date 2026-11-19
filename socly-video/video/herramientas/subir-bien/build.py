"""Vídeo «Cómo subir tu ropa bien» (9:16, 1080x1920, 30 fps, sin voz: subtítulos + sonidos).
Uso: PYTHONUTF8=1 python build.py [--preview]   (salida: video/anuncios/subir-bien/subir-bien.mp4)
Clips originales en video/fotos-propias/subir-bien/original (01..10, en el orden en que los subió el dueño).
Cada segmento se saca con un nº EXACTO de fotogramas (dur*30) y su audio con 1600 muestras por fotograma,
así vídeo, audio, iconos y subtítulos no se desfasan."""
import os
import shutil
import subprocess
import sys

import numpy as np
import soundfile as sf

FF = "/usr/bin/ffmpeg"
HERE = os.path.dirname(os.path.abspath(__file__))
VIDEO = os.path.abspath(os.path.join(HERE, "..", ".."))
SRC = os.path.join(VIDEO, "fotos-propias", "subir-bien", "original")
OUT_DIR = os.path.join(VIDEO, "anuncios", "subir-bien")
LOGO = os.path.join(VIDEO, "herramientas", "halloween-publi", "logo-blanco.png")
DENOISE = os.path.join(VIDEO, "herramientas", "jardin", "modelo", "bd.rnnn")
W = "/home/user/prueba/socly-video/trabajo/subir-bien"
FPS, SR = 30, 48000
os.makedirs(W, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)
shutil.copy("C:/Windows/Fonts/ariblk.ttf", W)
shutil.copy(DENOISE, f"{W}/bd.rnnn")

HDR = ("zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,"
       "zscale=t=bt709:m=bt709:r=tv,format=yuv420p,scale=1080:1920")
# grabación de pantalla (1170x2532): encaja a todo el alto sobre su propio fondo desenfocado
SCR = ("split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=60:6,eq=brightness=-0.38:saturation=0.6[bg];"
       "[b]scale=-2:1920[fg];[bg][fg]overlay=(W-w)/2:0,scale=in_range=pc:out_range=tv,format=yuv420p")
BW = "hue=s=0,eq=contrast=1.12:brightness=-0.04"


def run(*args):
    # cwd = carpeta de trabajo: en los filtros los «C:/» rompen las rutas, así que se usan nombres relativos
    subprocess.run([FF, "-y", "-loglevel", "error", *args], check=True, cwd=W)


# --- segmentos: nombre, clip, inicio, fin, velocidad, vf extra, congelar al final (s), audio (None = silencio), tipo
SEGS = [
    dict(n="hook",  f="01-IMG_7446.mov", a=0.55, b=5.95, v=1.0, kind="cam", vol=1.0),
    dict(n="door",  f="02-IMG_7447.mov", a=0.15, b=2.05, v=1.0, kind="cam", vol=0.5),
    dict(n="unfold", f="03-IMG_7448.mov", a=0.90, b=5.30, v=1.8, kind="cam", vol=None),
    dict(n="shoot", f="04-IMG_7449.mov", a=0.0, b=2.5, v=1.0, kind="cam", vol=0.5),
    dict(n="app1",  f="05-ScreenRecording_11-04-2026_20-01-31_1.mov", a=0.0, b=3.2, v=1.0, kind="scr", vol=None),
    dict(n="app2",  f="06-ScreenRecording_11-04-2026_20-01-31_1.mov", a=0.0, b=25.0, v=12.0, kind="scr", vol=None),
    dict(n="clean", f="07-ScreenRecording_11-04-2026_20-01-31_1.mov", a=0.0, b=1.0, v=1.0, kind="scr", vol=None, hold=1.6),
    dict(n="bad1",  f="08-IMG_7450.mov", a=0.0, b=1.66, v=0.8, kind="cam", vol=0.35, bw=True),
    dict(n="bad2",  f="09-IMG_7452.mov", a=0.0, b=1.80, v=0.8, kind="cam", vol=0.35, bw=True),
    dict(n="good2", f="10-IMG_7454.mov", a=0.0, b=0.70, v=0.5, kind="cam", vol=0.5, hold=1.2, zoom=True),
    dict(n="end",   f=None, a=0, b=2.6, v=1.0, kind="end", vol=None),
]

t0 = 0.0
for s in SEGS:
    s["dur"] = round(((s["b"] - s["a"]) / s["v"] + s.get("hold", 0)) * FPS) / FPS
    s["t0"] = t0
    t0 += s["dur"]
TOTAL = t0
print("duración total", round(TOTAL, 2), "s")
T = {s["n"]: s["t0"] for s in SEGS}
D = {s["n"]: s["dur"] for s in SEGS}

# --- 1) segmentos de vídeo y de audio
audio_parts = []
for s in SEGS:
    nfr = round(s["dur"] * FPS)
    out = f"{W}/{s['n']}.mp4"
    if s["kind"] == "end":
        run("-f", "lavfi", "-i", f"color=c=black:s=1080x1920:r={FPS}", "-frames:v", str(nfr),
            "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", out)
    else:
        base = HDR if s["kind"] == "cam" else SCR
        sp = f"setpts=PTS/{s['v']}," if s["v"] != 1 else ""
        vf = f"{base},{sp}fps={FPS}"
        if s.get("bw"):
            vf += f",{BW}"
        if s.get("hold"):
            vf += f",tpad=stop_mode=clone:stop_duration={s['hold']}"
        if s.get("zoom"):
            # empuje suave sobre la persona del espejo (está pequeña y a la izquierda del encuadre)
            vf += (f",scale=w='1080*(1.15+0.30*min(t/{s['dur']},1))':h='1920*(1.15+0.30*min(t/{s['dur']},1))':eval=frame,"
                   "crop=1080:1920:x='min(max(0.39*iw-540,0),iw-1080)':y='min(max(0.40*ih-960,0),ih-1920)'")
        run("-ss", str(s["a"]), "-to", str(s["b"]), "-i", f"{SRC}/{s['f']}", "-vf", vf, "-an", "-frames:v", str(nfr),
            "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", out)
    # audio del segmento
    n = nfr * (SR // FPS)
    if s.get("vol") is None:
        a = np.zeros((n, 2), dtype=np.float32)
    else:
        wav = f"{W}/{s['n']}.wav"
        af = f"highpass=f=90,arnndn=m=bd.rnnn:mix=0.75,aresample={SR}"
        if s["v"] != 1:
            af = f"atempo={s['v']}," + af
        run("-ss", str(s["a"]), "-to", str(s["b"]), "-i", f"{SRC}/{s['f']}", "-vn", "-af", af, "-ac", "2", "-ar", str(SR), wav)
        raw, _ = sf.read(wav, dtype="float32")
        a = np.zeros((n, 2), dtype=np.float32)
        m = min(n, len(raw))
        a[:m] = raw[:m] * s["vol"]
    audio_parts.append(a)
voice = np.concatenate(audio_parts)
N = int(round(TOTAL * FPS)) * (SR // FPS)
voice = voice[:N] if len(voice) >= N else np.pad(voice, ((0, N - len(voice)), (0, 0)))

# --- 2) sonidos sintetizados (sin derechos)
rng = np.random.default_rng(3)
sfx = np.zeros((N, 2), dtype=np.float32)


def put(x, t, g=1.0):
    s0 = int(t * SR)
    e = min(N, s0 + len(x))
    if s0 < N and e > s0:
        sfx[s0:e, 0] += x[: e - s0] * g
        sfx[s0:e, 1] += x[: e - s0] * g


def env(n, tau):
    return np.exp(-np.arange(n) / SR / tau)


def ding():
    n = int(SR * 0.9)
    t = np.arange(n) / SR
    a = np.sin(2 * np.pi * 1046.5 * t) * env(n, 0.22)
    b = np.zeros(n)
    k = int(SR * 0.09)
    b[k:] = (np.sin(2 * np.pi * 1568.0 * t[: n - k]) * env(n - k, 0.30))
    return (a * 0.6 + b * 0.8 + 0.25 * np.sin(2 * np.pi * 2093 * t) * env(n, 0.12))


def buzz():
    n = int(SR * 0.5)
    t = np.arange(n) / SR
    sq = np.sign(np.sin(2 * np.pi * 120 * t)) + np.sign(np.sin(2 * np.pi * 127 * t))
    thud = np.sin(2 * np.pi * 70 * t) * env(n, 0.07) * 2.0
    gate = np.where((t < 0.19) | ((t > 0.24) & (t < 0.46)), 1.0, 0.0)
    gate = np.convolve(gate, np.ones(60) / 60, mode="same")
    return (sq * 0.35 * gate * env(n, 0.5) + thud) * 0.9


def whoosh(dur=0.5):
    n = int(SR * dur)
    x = rng.standard_normal(n)
    # filtro paso banda que sube y baja
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
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.04)


# cuándo suena cada cosa (tiempos absolutos)
CHECK_APP = T["app1"] + 1.9
BAD1, BAD2 = T["bad1"] + 0.05, T["bad2"] + 0.05
GOOD2 = T["good2"] + 0.15
put(whoosh(0.45), T["door"] - 0.2, 0.5)
put(whoosh(0.45), T["app1"] - 0.25, 0.5)
put(pop(), T["app1"] + 1.0, 0.35)          # al hacer la foto
put(ding(), CHECK_APP, 0.5)
put(pop(), T["clean"] + 0.1, 0.4)
put(whoosh(0.4), T["bad1"] - 0.2, 0.45)
put(buzz(), BAD1, 0.55)
put(buzz(), BAD2, 0.55)
put(whoosh(0.4), T["good2"] - 0.2, 0.4)
put(ding(), GOOD2, 0.55)
put(whoosh(0.5), T["end"] - 0.25, 0.5)
put(pop(), T["end"] + 0.35, 0.35)
mix = voice + sfx
mix /= max(1.0, np.max(np.abs(mix)) / 0.95)
sf.write(f"{W}/mezcla.wav", mix, SR)

# --- 3) iconos ✓ / ✗ (PNG con transparencia, se animan al superponerlos)
from PIL import Image, ImageDraw  # noqa: E402

SZ = 360


def icon(kind):
    im = Image.new("RGBA", (SZ, SZ), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    col = (46, 184, 114, 255) if kind == "ok" else (232, 62, 62, 255)
    d.ellipse((8, 8, SZ - 8, SZ - 8), fill=col, outline=(255, 255, 255, 255), width=14)
    wd = 34
    if kind == "ok":
        pts = [(98, 190), (155, 247), (265, 123)]
        d.line(pts, fill=(255, 255, 255, 255), width=wd, joint="curve")
        for p in (pts[0], pts[2]):
            d.ellipse((p[0] - wd / 2, p[1] - wd / 2, p[0] + wd / 2, p[1] + wd / 2), fill=(255, 255, 255, 255))
    else:
        for p, q in (((112, 112), (248, 248)), ((248, 112), (112, 248))):
            d.line([p, q], fill=(255, 255, 255, 255), width=wd)
            for e in (p, q):
                d.ellipse((e[0] - wd / 2, e[1] - wd / 2, e[0] + wd / 2, e[1] + wd / 2), fill=(255, 255, 255, 255))
    path = f"{W}/icon-{kind}.png"
    im.save(path)
    return path


ICONS = [  # archivo, inicio, duración, centro y, ancho, alto
    ("titulo", T["door"], T["shoot"] - T["door"], 310, 828, 342),
    ("ok", CHECK_APP, 1.1, 430, 223, 223),
    ("no", BAD1, 1.9, 640, 223, 223),
    ("no", BAD2, 2.0, 640, 223, 223),
    ("ok", GOOD2, 2.2, 640, 223, 223),
]
icon("ok"), icon("no")


def titulo():
    """Tarjeta de título: cristal oscuro, filete dorado y dos líneas en Arial Black."""
    from PIL import ImageFont
    Wd, Ht = 920, 380
    im = Image.new("RGBA", (Wd, Ht), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((6, 6, Wd - 6, Ht - 6), radius=44, fill=(10, 10, 10, 168), outline=(242, 184, 75, 255), width=5)
    f = ImageFont.truetype("C:/Windows/Fonts/ariblk.ttf", 84)
    f2 = ImageFont.truetype("C:/Windows/Fonts/ariblk.ttf", 34)
    d.text((Wd / 2, 58), "SOCLY STYLE · GUÍA RÁPIDA", font=f2, fill=(242, 184, 75, 255), anchor="mt")
    d.text((Wd / 2, 135), "CÓMO SUBIR", font=f, fill=(255, 255, 255, 255), anchor="mt")
    w1 = d.textlength("TU ROPA ", font=f)
    w2 = d.textlength("BIEN", font=f)
    x0 = (Wd - (w1 + w2)) / 2
    d.text((x0, 245), "TU ROPA ", font=f, fill=(255, 255, 255, 255), anchor="lt")
    d.text((x0 + w1, 245), "BIEN", font=f, fill=(242, 184, 75, 255), anchor="lt")
    im.save(f"{W}/icon-titulo.png")


titulo()

# --- 4) subtítulos (ASS): estilo del resto de vídeos (Arial Black, mayúsculas, borde)
GOLD, WHITE = r"{\c&H004BB8F2&}", r"{\c&H00FFFFFF&}"
pop_tag = r"{\fscx84\fscy84\t(0,90,\fscx107\fscy107)\t(90,170,\fscx100\fscy100)}"


def ts(t):
    return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"


EV = []  # (inicio, fin, texto, margenV, estilo)


def cap(a, b, text, mv=470, style="Tik"):
    EV.append((a, b, pop_tag + text, mv, style))


h = T["hook"] - 0.55  # el tiempo de la fuente 0.55 s es el 0 del segmento
cap(h + 0.96, h + 2.40, "PERDONA, ¿ME COBRAS<br>LA SUDADERA?".replace("<br>", r"\N"))
cap(h + 2.48, h + 3.80, "CLARO, 3,99 €")
cap(h + 4.00, h + 5.95, r"¡QUÉ BARATO!\NCOMO EL " + GOLD + "PLAN DE SOCLY")
cap(T["shoot"] + 0.15, T["shoot"] + D["shoot"], GOLD + "UNA" + WHITE + " PRENDA POR FOTO")
cap(T["app1"] + 0.1, T["app1"] + D["app1"] - 0.1, "ENTERA, SOBRE UNA\\NSUPERFICIE LISA", mv=300)
cap(T["app2"] + 0.1, T["app2"] + D["app2"] - 0.1, GOLD + "RELLENAR POR MÍ", mv=300)
cap(T["clean"] + 0.1, T["clean"] + D["clean"], r"{\an8\fs60}Y QUEDA " + GOLD + r"COMO EN\NUNA TIENDA", mv=250)
cap(T["bad1"] + 0.1, T["bad1"] + D["bad1"], "VARIAS PRENDAS\\NEN UNA FOTO", mv=300)
cap(T["bad2"] + 0.1, T["bad2"] + D["bad2"], "CON AMIGOS O\\NGENTE DETRÁS", mv=300)
cap(T["good2"] + 0.1, T["good2"] + D["good2"], GOLD + "TÚ SOLO" + WHITE + r", EN EL ESPEJO\NCUERPO ENTERO", mv=300)
# etiquetas de sección arriba
EV.append((T["shoot"], T["bad2"], r"{\an8\fs50\c&H004BB8F2&}PRENDA SUELTA", 170, "Tik"))
EV.append((T["bad2"], T["end"], r"{\an8\fs50\c&H004BB8F2&}OUTFIT", 170, "Tik"))
# tarjeta final
EV.append((T["end"] + 0.25, T["end"] + D["end"], r"{\an5\pos(540,1050)\fs64}" + "UNA PRENDA POR FOTO.", 0, "Tik"))
EV.append((T["end"] + 0.55, T["end"] + D["end"], r"{\an5\pos(540,1160)\fs64}" + "TÚ SOLO EN EL ESPEJO.", 0, "Tik"))
EV.append((T["end"] + 1.2, T["end"] + D["end"], r"{\an5\pos(540,1480)\fs44\c&H004BB8F2&}ENLACE EN LA BIO", 0, "Tik"))

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
    for a, b, text, mv, style in EV:
        fh.write(f"Dialogue: 0,{ts(a)},{ts(b)},{style},,0,0,{mv},,{WHITE}{text}\n")

# --- 5) unir todo: vídeo + logo final + iconos con rebote + subtítulos + audio
with open(f"{W}/lista.txt", "w") as fh:
    for s in SEGS:
        fh.write(f"file '{W}/{s['n']}.mp4'\n")
run("-f", "concat", "-safe", "0", "-i", f"{W}/lista.txt", "-c", "copy", f"{W}/base.mp4")

inputs = ["-i", f"{W}/base.mp4", "-loop", "1", "-i", LOGO]
fc = ["[1:v]scale=420:-1,format=rgba[logo]",
      f"[0:v][logo]overlay=x=(W-w)/2:y=640:enable='between(t,{T['end'] + 0.1},{TOTAL})'[v0]"]
last = "v0"
for i, (kind, a, d, cy, bw, bh) in enumerate(ICONS):
    inputs += ["-loop", "1", "-t", f"{a + d:.2f}", "-i", f"{W}/icon-{kind}.png"]
    k = i + 2
    # rebote: crece de 0 a 1,15 en 0,16 s y se asienta en 1,0; desaparece al final
    sc = f"if(lt(t-{a},0.16),1.15*(t-{a})/0.16,if(lt(t-{a},0.30),1.15-0.15*(t-{a}-0.16)/0.14,1))"
    fc.append(f"[{k}:v]setpts=PTS-STARTPTS+{a}/TB,scale=w='max(2,{bw}*({sc}))':h='max(2,{bh}*({sc}))':eval=frame[ic{i}]")
    fc.append(f"[{last}][ic{i}]overlay=x='(W-w)/2':y='{cy}-h/2':enable='between(t,{a},{a + d})':eof_action=pass[v{i + 1}]")
    last = f"v{i + 1}"
fc.append(f"[{last}]subtitles=subs.ass:fontsdir=.[vf]")
final = f"{OUT_DIR}/subir-bien.mp4"
run(*inputs, "-i", f"{W}/mezcla.wav", "-filter_complex", ";".join(fc), "-map", "[vf]", "-map", f"{inputs.count('-i')}:a",
    "-t", f"{TOTAL:.3f}", "-c:v", "libx264", "-crf", "17", "-preset", "medium", "-pix_fmt", "yuv420p",
    "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", final)
print("listo:", final)
