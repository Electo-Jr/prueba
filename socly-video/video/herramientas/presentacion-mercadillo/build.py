"""Vídeo de presentación del Mercadillo Socly (4 clips del dueño hablando a cámara, 1080x1920).
Uso: PYTHONUTF8=1 python build.py con     -> anuncios\\presentacion-mercadillo\\presentacion-mercadillo-con-app.mp4
     PYTHONUTF8=1 python build.py sin     -> ...-sin-app.mp4   (igual, sin las pantallas de la app)
Pasos: HDR->SDR, recorte vertical siguiendo la cara, cortes en pausas (con zoom alterno), subtítulos
palabra a palabra, (opcional) pantallas de la app de `anuncios\\mercadillo\\mercadillo.mp4`, música suave y
efectos de `video\\podcast\\sonidos\\`, tarjeta final. Sin rótulo «Hecho con IA»."""
import json, math, os, subprocess, sys, glob
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont

MODO = sys.argv[1] if len(sys.argv) > 1 else "con"
FF = "/usr/bin/ffmpeg"
V = "/home/user/prueba/socly-video/video/"
SRC = V + "fotos-propias/presentacion-mercadillo/original/"
DAT = V + "herramientas/presentacion-mercadillo/datos/"
SFX = V + "podcast/sonidos/"
MERC = V + "anuncios/mercadillo/mercadillo.mp4"
OUT = V + "anuncios/presentacion-mercadillo/presentacion-mercadillo-" + ("con-app" if MODO == "con" else "sin-app") + ".mp4"
WORK = "/home/user/prueba/socly-video/trabajo/nuevo/work"
os.makedirs(WORK, exist_ok=True)
W, H, FPS, SR = 1080, 1920, 30, 48000
FONT = "C:/Windows/Fonts/ArialNova-Bold.ttf"
SERIF = "C:/Windows/Fonts/georgiab.ttf"
SERIF_I = "C:/Windows/Fonts/georgiaz.ttf"
TM = ("zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=tonemap=hable:desat=0,"
      "zscale=t=bt709:m=bt709:r=tv,format=yuv420p")

CLIPS = ["IMG_7563", "IMG_7564", "IMG_7566", "IMG_7568"]
# correcciones de subtítulos (la palabra tal cual la da Whisper medium -> texto final)
FIX = {"acabo": "acabó", "de,": "de", "me": "«me", "descuento": "descuento»", "Vinted": "Vinted"}
# pantallas de la app (tiempos del vídeo mercadillo.mp4): clip -> (t_inicio, t_fin del clip, t_inicio en mercadillo.mp4)
CUTAWAYS = {"IMG_7566": [(4.3, 6.9, 19.6)], "IMG_7568": [(5.7, 8.1, 22.2), (11.6, 13.8, 24.2)]}
# efectos: (clip, t del clip, archivo, volumen)
SFXS = [("IMG_7566", 3.25, "ding", 0.45)]


def ff_read(args, w, h, ch=3):
    """Devuelve un generador de fotogramas crudos de ffmpeg."""
    pf = ["-pix_fmt", "rgb24"] if ch == 3 else ["-pix_fmt", "gray"]
    p = subprocess.Popen([FF, "-loglevel", "error"] + args + pf + ["-f", "rawvideo", "-"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    n = w * h * ch
    while True:
        b = p.stdout.read(n)
        if len(b) < n:
            break
        yield np.frombuffer(b, np.uint8).reshape(h, w, ch) if ch > 1 else np.frombuffer(b, np.uint8).reshape(h, w)
    p.stdout.close(); p.wait()


# ---------------------------------------------------------------- datos de palabras y segmentos
def cargar(clip):
    small = json.load(open(DAT + clip + ".json", encoding="utf-8"))
    med = json.load(open(DAT + clip + "-medium.json", encoding="utf-8"))
    return small, med


def segmentos(small):
    segs = []
    s0, e0 = small[0]["s"], small[0]["e"]
    for a, b in zip(small, small[1:]):
        if b["s"] - a["e"] > 0.20:
            segs.append((max(0, s0 - 0.09), a["e"] + 0.11)); s0 = b["s"]
        e0 = b["e"]
    segs.append((max(0, s0 - 0.09), e0 + 0.14))
    return segs


timeline = []   # (clip, t0, t1, out0, escala)
out_t = 0.0
DATA = {}
for ci, c in enumerate(CLIPS):
    small, med = cargar(c)
    segs = segmentos(small)
    if ci == 0:
        segs[0] = (0.22, segs[0][1])   # el gancho empieza ya
    DATA[c] = (small, med, segs)
    for i, (a, b) in enumerate(segs):
        timeline.append(dict(clip=c, t0=a, t1=b, out0=out_t, z=1.0 if len(timeline) % 2 == 0 else (1.10 if c != "IMG_7563" else 1.0)))
        out_t += b - a
DUR = out_t
END = 2.4
TOTAL = DUR + END
NF = int(round(TOTAL * FPS))
print(f"segmentos {len(timeline)}; vídeo {DUR:.1f} s + tarjeta {END} s")


def t_out(clip, t):
    best = None
    for s in timeline:
        if s["clip"] != clip:
            continue
        if s["t0"] <= t <= s["t1"]:
            return s["out0"] + (t - s["t0"])
        if t < s["t0"] and best is None:
            best = s["out0"]
    return best if best is not None else None


# ---------------------------------------------------------------- subtítulos
def fixtxt(w):
    return FIX.get(w, w)


frases = []   # (out0, out1, [(palabra, out_t0, out_t1)])
for c in CLIPS:
    small, med, segs = DATA[c]
    ws = []
    for i, w in enumerate(med):
        t = t_out(c, w["s"])
        if t is None:
            continue
        ws.append([fixtxt(w["w"]), t])
    # troceado en frases de 3-4 palabras, cortando en signos
    grupo = []
    for i, (txt, t) in enumerate(ws):
        grupo.append((txt, t))
        fin = txt.endswith((",", ".", "»,", "»")) or len(grupo) >= 4
        if len(grupo) >= 2 and txt.endswith((",", ".")) or len(grupo) >= 4 or i == len(ws) - 1:
            frases.append(grupo); grupo = []
    if grupo:
        frases.append(grupo)
# tiempos de fin de cada palabra
subs = []
alls = [(w, t) for g in frases for (w, t) in g]
for gi, g in enumerate(frases):
    items = []
    for j, (w, t) in enumerate(g):
        nxt = g[j + 1][1] if j + 1 < len(g) else None
        items.append([w, t, nxt])
    # el fin de la frase: justo antes de la frase siguiente o +0.6 s
    t_fin_frase = frases[gi + 1][0][1] if gi + 1 < len(frases) else g[-1][1] + 0.7
    t_fin_frase = min(t_fin_frase, g[-1][1] + 0.9)
    for it in items:
        if it[2] is None:
            it[2] = t_fin_frase
    subs.append(dict(t0=g[0][1], t1=t_fin_frase, words=items))

fnt = ImageFont.truetype(FONT, 80)
_cache = {}


def capa_subs(frase, activo):
    key = (id(frase), activo)
    if key in _cache:
        return _cache[key]
    ws = [w for w, _, _ in frase["words"]]
    # partir en 2 líneas si es largo
    anchos = [fnt.getlength(w + " ") for w in ws]
    lineas, cur, ancho = [], [], 0
    for i, w in enumerate(ws):
        if ancho + anchos[i] > 900 and cur:
            lineas.append(cur); cur, ancho = [], 0
        cur.append(i); ancho += anchos[i]
    lineas.append(cur)
    img = Image.new("RGBA", (W, 380), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    y = 380 - (len(lineas) * 100) - 30
    for ln in lineas:
        tot = sum(anchos[i] for i in ln) - fnt.getlength(" ")
        x = (W - tot) / 2
        for i in ln:
            col = (255, 214, 140, 255) if i == activo else (255, 255, 255, 255)
            d.text((x, y), ws[i], font=fnt, fill=col, stroke_width=9, stroke_fill=(15, 12, 8, 255))
            x += anchos[i]
        y += 100
    arr = np.array(img)
    _cache[key] = arr
    return arr


def sub_en(t):
    for fr in subs:
        if fr["t0"] - 0.02 <= t < fr["t1"]:
            act = 0
            for i, (w, a, b) in enumerate(fr["words"]):
                if t >= a:
                    act = i
            return capa_subs(fr, act)
    return None


# ---------------------------------------------------------------- cara -> recorte
# centro horizontal de la cara (coordenadas 1920x1080), puntos (t del clip, x) mirados a mano en fotogramas;
# no hay detector de caras en este OpenCV y la persona se mueve y se acerca a la cámara
KEYS = {
    "IMG_7563": [(0, 860), (3, 900), (6.5, 960)],
    "IMG_7564": [(0, 870), (5, 900), (8, 780), (10, 650), (12.2, 640)],
    "IMG_7566": [(0, 1020), (3, 1040), (5, 1050), (7, 1100), (9, 1150), (11.5, 1160)],
    "IMG_7568": [(0, 960), (6, 960), (14.5, 940)],
}


def trayectoria(clip):
    pts = KEYS[clip]; N = int(15 * FPS)
    t = np.arange(N) / FPS
    x = np.interp(t, [p[0] for p in pts], [p[1] for p in pts])
    ker = np.exp(-0.5 * (np.arange(-30, 31) / 12.0) ** 2); ker /= ker.sum()
    x = np.convolve(np.pad(x, 30, mode="edge"), ker, mode="valid")
    return np.stack([x, np.zeros(N)], 1)


# ---------------------------------------------------------------- sonido
def leer_audio(path, ss=None, t=None):
    a = ["-i", path] if ss is None else ["-ss", str(ss), "-t", str(t), "-i", path]
    raw = subprocess.run([FF, "-loglevel", "error"] + a + ["-vn", "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2)


def construir_audio():
    n = int(TOTAL * SR)
    voz = np.zeros((n, 2), np.float32)
    cache = {}
    for s in timeline:
        if s["clip"] not in cache:
            cache[s["clip"]] = leer_audio(SRC + s["clip"] + ".mov")
        a = cache[s["clip"]][int(s["t0"] * SR):int(s["t1"] * SR)].copy()
        f = int(0.012 * SR)
        a[:f] *= np.linspace(0, 1, f)[:, None]; a[-f:] *= np.linspace(1, 0, f)[:, None]
        i0 = int(s["out0"] * SR); voz[i0:i0 + len(a)] += a[:n - i0]
    # normaliza la voz (RMS de las partes con voz) a -17 dBFS aprox.
    act = np.abs(voz).max(axis=1) > 0.01
    rms = np.sqrt(np.mean(voz[act] ** 2)) if act.any() else 0.1
    voz *= (10 ** (-17 / 20)) / max(rms, 1e-4)
    voz = np.tanh(voz * 1.2) / 1.2
    # música: acordes suaves
    t = np.arange(n) / SR
    mus = np.zeros(n, np.float32)
    acordes = [(261.63, 329.63, 392.0, 493.88), (220.0, 261.63, 329.63, 392.0), (174.61, 220.0, 261.63, 329.63), (196.0, 246.94, 293.66, 392.0)]
    comp = 2.0   # s por acorde
    for i in range(int(TOTAL / comp) + 1):
        a0, a1 = int(i * comp * SR), min(n, int((i + 1) * comp * SR))
        if a0 >= n:
            break
        tt = t[a0:a1] - t[a0]
        env = np.minimum(1, tt / 0.25) * np.minimum(1, (comp - tt) / 0.5)
        for fr in acordes[i % 4]:
            mus[a0:a1] += (np.sin(2 * math.pi * fr * tt) + 0.3 * np.sin(2 * math.pi * 2 * fr * tt) * np.exp(-tt * 3)) * env * 0.2
        # pulso suave de bajo
        mus[a0:a1] += np.sin(2 * math.pi * (acordes[i % 4][0] / 2) * tt) * env * 0.35
    mus *= np.minimum(1, t / 0.8) * np.minimum(1, (TOTAL - t) / 1.4)
    musv = np.stack([mus, mus], 1) * 0.045
    mix = voz + musv
    # efectos
    efs = [(c, tc, nm, vol) for c, tc, nm, vol in SFXS if vol > 0]
    for c, tc, nm, vol in efs:
        to = t_out(c, tc)
        if to is None:
            continue
        e = leer_audio(SFX + nm + ".mp3")[:int(1.5 * SR)]
        i0 = int(to * SR); mix[i0:i0 + len(e)] += (e * vol)[:n - i0]
    mix = np.clip(mix, -0.98, 0.98)
    wav = WORK + "/audio.wav"
    subprocess.run([FF, "-y", "-loglevel", "error", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", wav], input=mix.astype(np.float32).tobytes(), check=True)
    return wav


# ---------------------------------------------------------------- imágenes de la app
def cutaway_frames():
    out = {}
    if MODO != "con":
        return out
    for c, lst in CUTAWAYS.items():
        for (a, b, m0) in lst:
            n = int(round((b - a) * FPS))
            frs = list(ff_read(["-ss", str(m0), "-t", str(n / FPS + 0.1), "-i", MERC, "-vf", f"fps={FPS}"], W, H))[:n]
            out[(c, a)] = [componer_phone(f) for f in frs]
    return out


def componer_phone(f):
    # fondo: franja limpia de arriba estirada; teléfono: recorte y 480..1700 con bordes suaves
    bg = cv2.resize(f[0:50], (W, H), interpolation=cv2.INTER_LINEAR)
    bg = cv2.GaussianBlur(bg, (0, 0), 25)
    ph = f[480:1700].astype(np.float32)
    al = np.ones((ph.shape[0], 1, 1), np.float32)
    al[:70] = np.linspace(0, 1, 70)[:, None, None]; al[-70:] = np.linspace(1, 0, 70)[:, None, None]
    y0 = 160
    reg = bg[y0:y0 + 1220].astype(np.float32)
    bg[y0:y0 + 1220] = (reg * (1 - al) + ph * al).astype(np.uint8)
    return bg


# ---------------------------------------------------------------- tarjeta final
def tarjeta():
    img = Image.new("RGB", (W, H), (244, 238, 228))
    logo = Image.open("/home/user/prueba/socly-video/app estilista ia/design/logo.png").convert("RGBA").resize((440, 440), Image.LANCZOS)
    img.paste(logo, ((W - 440) // 2, 740), logo)
    d = ImageDraw.Draw(img)
    d.text((W / 2, 1300), "Socly Style", font=ImageFont.truetype(SERIF, 112), fill=(21, 20, 15), anchor="mm")
    return np.array(img)


# ---------------------------------------------------------------- render
def gradear(img):
    f = img.astype(np.float32) / 255.0
    f = np.clip((f - 0.5) * 1.07 + 0.5 + 0.02, 0, 1) ** 0.94
    g = f.mean(axis=2, keepdims=True)
    f = np.clip(g + (f - g) * 1.10, 0, 1)
    return (f * 255).astype(np.uint8)


def main():
    cuts = cutaway_frames()
    wav = construir_audio()
    print("audio listo")
    card = tarjeta()
    enc = subprocess.Popen([FF, "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                            "-i", wav, "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                            "-shortest", "-movflags", "+faststart", OUT], stdin=subprocess.PIPE)
    out_frame = 0
    prev_img = None
    for s in timeline:
        c = s["clip"]; i0 = int(round(s["t0"] * FPS)); i1 = int(round(s["t1"] * FPS))
        ss = max(0.0, s["t0"] - 0.3)
        stream = ff_read(["-ss", f"{ss:.3f}", "-i", SRC + c + ".mov", "-vf", f"fps={FPS},{TM},format=rgb24"], 1080, 1920)
        for k0, fr in enumerate(stream):
            tt_clip = ss + k0 / FPS
            idx = int(round(tt_clip * FPS))
            if tt_clip < s["t0"] - 1e-6:
                continue
            if tt_clip >= s["t1"]:
                break
            tout = s["out0"] + (tt_clip - s["t0"])
            ofi = int(round(tout * FPS))
            # encuadre: los clips ya son verticales (1080x1920); empuje lento y zoom alterno en cada corte
            z = s["z"] * (1 + 0.03 * (tt_clip - s["t0"]) / max(0.5, s["t1"] - s["t0"]))
            if c == "IMG_7563":   # persona lejos, en el escenario: acercar sobre ella
                z *= 1.5; ccx, ccy = 500, 1010
            else:
                ccx, ccy = {"IMG_7564": (580, 900), "IMG_7566": (640, 1100), "IMG_7568": (600, 1000)}[c]
            cw = int(1080 / z); ch = int(1920 / z)
            x0 = int(min(max(ccx - cw / 2, 0), 1080 - cw)); y0 = int(min(max(ccy - ch / 2, 0), 1920 - ch))
            crop = fr[y0:y0 + ch, x0:x0 + cw]
            img = cv2.resize(crop, (W, H), interpolation=cv2.INTER_LANCZOS4)
            bl = cv2.GaussianBlur(img, (0, 0), 1.4); img = cv2.addWeighted(img, 1.5, bl, -0.5, 0)
            img = gradear(img)
            # pantallas de la app
            for (cc, a), frs in cuts.items():
                if cc == c:
                    b = a + len(frs) / FPS
                    if a <= tt_clip < b:
                        k = int((tt_clip - a) * FPS); ph = frs[min(k, len(frs) - 1)]
                        al = min(1.0, (tt_clip - a) / 0.14, (b - tt_clip) / 0.14)
                        img = (img.astype(np.float32) * (1 - al) + ph.astype(np.float32) * al).astype(np.uint8)
            # subtítulos
            sb = sub_en(tout)
            if sb is not None:
                y_s = 1640 - 380
                al = sb[:, :, 3:4].astype(np.float32) / 255
                seg = img[y_s:y_s + 380].astype(np.float32)
                img[y_s:y_s + 380] = (seg * (1 - al) + sb[:, :, :3] * al).astype(np.uint8)
            # fundido de entrada del primer fotograma
            if ofi < 5:
                img = (img * (ofi + 1) / 6).astype(np.uint8)
            while out_frame < ofi:   # rellena huecos de redondeo
                enc.stdin.write(prev_img.tobytes()); out_frame += 1
            enc.stdin.write(img.tobytes()); out_frame += 1; prev_img = img
    # tarjeta final con fundido desde el último fotograma
    nfix = int(END * FPS)
    for k in range(nfix):
        a = min(1.0, k / 6.0)
        img = (prev_img.astype(np.float32) * (1 - a) + card.astype(np.float32) * a).astype(np.uint8) if k < 6 else card
        enc.stdin.write(img.tobytes()); out_frame += 1
    enc.stdin.close(); enc.wait()
    print("OK", OUT, out_frame, "fotogramas")


if __name__ == "__main__":
    main()
