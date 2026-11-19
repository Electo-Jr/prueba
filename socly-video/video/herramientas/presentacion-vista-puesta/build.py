"""Vídeo de presentación de «Vista puesta» (3 escenas del dueño + animación de la función + tarjeta final), 1080x1920.
Uso: PYTHONUTF8=1 python build.py     -> anuncios\\presentacion-vista-puesta\\presentacion-vista-puesta.mp4
Escenas (fotos-propias\\presentacion-vista-puesta\\original, verticales con rotación guardada): IMG_7572 (competencia),
IMG_7578 (balcón), IMG_7581 (terraza; al final mira al horizonte: ahí entra la animación de la app).
El móvil (`phone\f_0000..0204.png`, fondo transparente, 6,8 s) sale de `herramientas\vista-puesta` (vp-transparente.html + render-png.mjs; la carga va x2,2).
Sin música ni efectos: solo la voz (y el sonido ambiente de la terraza durante la animación). Sin «Hecho con IA»."""
import json, math, os, subprocess, sys
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont

FF = "/usr/bin/ffmpeg"
V = "/home/user/prueba/socly-video/video/"
SRC = V + "fotos-propias/presentacion-vista-puesta/original/"
HERE = V + "herramientas/presentacion-vista-puesta/"
DAT = HERE + "datos/"
PHONE = HERE + "phone/"
SINZOOM = "sinzoom" in sys.argv[1:]   # `python build.py sinzoom`: escenas con su encuadre original, sin zoom ni empuje
OUT = V + "anuncios/presentacion-vista-puesta/presentacion-vista-puesta" + ("-sin-zoom" if SINZOOM else "") + ".mp4"
os.makedirs(os.path.dirname(OUT), exist_ok=True)
WORK = "/home/user/prueba/socly-video/trabajo/vp/work"
os.makedirs(WORK, exist_ok=True)
W, H, FPS, SR = 1080, 1920, 30, 48000
SFXS = [("IMG_7578", 4.45, "fah", 0.55)]   # (clip, t del clip, archivo, volumen): «fah» en «no nos llegan a la altura»
FONT = "/usr/share/fonts/opentype/inter/Inter-Bold.otf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
TM = ("zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=tonemap=hable:desat=0,"
      "zscale=t=bt709:m=bt709:r=tv,format=yuv420p")

CLIPS = ["IMG_7572", "IMG_7578", "IMG_7581"]
PHONE_T0 = 9.3             # IMG_7581: desde aquí mira al horizonte y entra el móvil encima
N_PHONE = 205              # fotogramas del móvil (6,83 s)
HOLD_FIN = 0.6             # el horizonte sigue un poco tras la animación
END = 2.4
# encuadre por clip: (centro x, centro y, zoom base) sobre el fotograma vertical 1080x1920
ENC = {"IMG_7572": (480, 1240, 1.5), "IMG_7578": (585, 1050, 2.0), "IMG_7581": (510, 950, 2.0)}
# captions de la animación: (t inicio, t fin, texto, palabra resaltada)
if SINZOOM:
    ENC = {k: (540, 960, 1.0) for k in ENC}
CAPS = [(0.5, 2.3, "Eliges tu look de hoy", "look"), (2.3, 3.7, "Tocas Vista puesta", "Vista puesta"),
        (3.7, 6.8, "Y te ves con tu propia ropa", "propia ropa")]


def ff_read(args, w, h, ch=3):
    pf = ["-pix_fmt", "rgb24"] if ch == 3 else ["-pix_fmt", "gray"]
    p = subprocess.Popen([FF, "-loglevel", "error"] + args + pf + ["-f", "rawvideo", "-"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    n = w * h * ch
    while True:
        b = p.stdout.read(n)
        if len(b) < n:
            break
        yield np.frombuffer(b, np.uint8).reshape(h, w, ch)
    p.stdout.close(); p.wait()


# ---------------------------------------------------------------- segmentos (cortes en pausas)
def segmentos(small):
    segs = []
    s0 = small[0]["s"]
    for a, b in zip(small, small[1:]):
        if b["s"] - a["e"] > 0.20:
            segs.append((max(0, s0 - 0.09), a["e"] + 0.11)); s0 = b["s"]
    segs.append((max(0, s0 - 0.09), small[-1]["e"] + 0.14))
    return segs


timeline = []
out_t = 0.0
DATA = {}
for ci, c in enumerate(CLIPS):
    small = json.load(open(DAT + c + ".json", encoding="utf-8"))
    med = json.load(open(DAT + c + "-medium.json", encoding="utf-8"))
    segs = segmentos(small)
    if ci == 0:
        segs[0] = (0.12, segs[0][1])
    if c == "IMG_7581":
        segs[-1] = (segs[-1][0], PHONE_T0 + N_PHONE / FPS + HOLD_FIN)
    DATA[c] = (small, med, segs)
    for i, (a, b) in enumerate(segs):
        timeline.append(dict(clip=c, t0=a, t1=b, out0=out_t, z=1.0 if (i % 2 == 0 or SINZOOM) else 1.07))
        out_t += b - a
DUR = out_t
TOTAL = DUR + END
print(f"escenas {DUR:.1f} s + tarjeta {END} s = {TOTAL:.1f} s; segmentos {len(timeline)}")


def t_out(clip, t):
    best = None
    for s in timeline:
        if s["clip"] != clip:
            continue
        if s["t0"] <= t <= s["t1"]:
            return s["out0"] + (t - s["t0"])
        if t < s["t0"] and best is None:
            best = s["out0"]
    return best


# ---------------------------------------------------------------- subtítulos
frases = []
for c in CLIPS:
    small, med, segs = DATA[c]
    ws = []
    for w in med:
        t = t_out(c, w["s"])
        if t is not None:
            ws.append([w["w"], t])
    grupo = []
    for i, (txt, t) in enumerate(ws):
        grupo.append((txt, t))
        if (len(grupo) >= 2 and txt.endswith((",", "."))) or len(grupo) >= 4 or i == len(ws) - 1:
            frases.append(grupo); grupo = []
    if grupo:
        frases.append(grupo)
subs = []
for gi, g in enumerate(frases):
    items = [[w, t, (g[j + 1][1] if j + 1 < len(g) else None)] for j, (w, t) in enumerate(g)]
    t_fin = frases[gi + 1][0][1] if gi + 1 < len(frases) else g[-1][1] + 0.7
    t_fin = min(t_fin, g[-1][1] + 0.9)
    for it in items:
        if it[2] is None:
            it[2] = t_fin
    subs.append(dict(t0=g[0][1], t1=t_fin, words=items))

fnt = ImageFont.truetype(FONT, 80)
_cache = {}


def render_texto(palabras, activos):
    """palabras: lista de str; activos: set de índices resaltados."""
    anchos = [fnt.getlength(w + " ") for w in palabras]
    lineas, cur, ancho = [], [], 0
    for i, w in enumerate(palabras):
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
            col = (255, 214, 140, 255) if i in activos else (255, 255, 255, 255)
            d.text((x, y), palabras[i], font=fnt, fill=col, stroke_width=9, stroke_fill=(15, 12, 8, 255))
            x += anchos[i]
        y += 100
    return np.array(img)


def capa_subs(frase, activo):
    key = (id(frase), activo)
    if key not in _cache:
        _cache[key] = render_texto([w for w, _, _ in frase["words"]], {activo})
    return _cache[key]


def sub_en(t):
    for fr in subs:
        if fr["t0"] - 0.02 <= t < fr["t1"]:
            act = 0
            for i, (w, a, b) in enumerate(fr["words"]):
                if t >= a:
                    act = i
            return capa_subs(fr, act)
    return None


_capc = {}


def caption_en(t):
    for i, (a, b, txt, res) in enumerate(CAPS):
        if a <= t < b:
            if i not in _capc:
                ps = txt.split(" ")
                rs = set(res.split(" "))
                _capc[i] = render_texto(ps, {k for k, p in enumerate(ps) if p in rs})
            al = min(1.0, (t - a) / 0.2, (b - t) / 0.2)
            return _capc[i], al
    return None, 0


def poner(img, layer, y_s=1640 - 380, alpha=1.0):
    al = layer[:, :, 3:4].astype(np.float32) / 255 * alpha
    seg = img[y_s:y_s + 380].astype(np.float32)
    img[y_s:y_s + 380] = (seg * (1 - al) + layer[:, :, :3] * al).astype(np.uint8)


# ---------------------------------------------------------------- sonido (solo voz + ambiente de la terraza)
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
    act = np.abs(voz).max(axis=1) > 0.01
    rms = np.sqrt(np.mean(voz[act] ** 2)) if act.any() else 0.1
    gain = (10 ** (-17 / 20)) / max(rms, 1e-4)
    voz *= gain
    mix = np.tanh(voz * 1.2) / 1.2
    # efecto pedido por el dueño: «fah» al decir «pero no nos llegan a la altura»
    for c, tc, nm, vol in SFXS:
        to = t_out(c, tc)
        if to is not None:
            e = leer_audio("/home/user/prueba/socly-video/video/podcast/sonidos/" + nm + ".mp3")[:int(2.0 * SR)]
            i0 = int(to * SR); mix[i0:i0 + len(e)] += (e * vol)[:n - i0]
    mix = np.clip(mix, -0.98, 0.98)
    mix *= np.minimum(1, (TOTAL - np.arange(n) / SR) / 0.6)[:, None]
    wav = WORK + "/audio.wav"
    subprocess.run([FF, "-y", "-loglevel", "error", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", wav], input=mix.astype(np.float32).tobytes(), check=True)
    return wav


# ---------------------------------------------------------------- tarjeta final: logo de Socly (negro) y «Socly Style»
def tarjeta():
    img = Image.new("RGB", (W, H), (244, 238, 228))
    logo = Image.open("/home/user/prueba/socly-video/app estilista ia/design/logo.png").convert("RGBA").resize((440, 440), Image.LANCZOS)
    img.paste(logo, ((W - 440) // 2, 740), logo)
    ImageDraw.Draw(img).text((W / 2, 1300), "Socly Style", font=ImageFont.truetype(SERIF, 112), fill=(21, 20, 15), anchor="mm")
    return np.array(img)


def gradear(img):
    f = img.astype(np.float32) / 255.0
    f = np.clip((f - 0.5) * 1.07 + 0.5 + 0.02, 0, 1) ** 0.94
    g = f.mean(axis=2, keepdims=True)
    f = np.clip(g + (f - g) * 1.10, 0, 1)
    return (f * 255).astype(np.uint8)


def main():
    wav = construir_audio()
    print("audio listo")
    card = tarjeta()
    enc = subprocess.Popen([FF, "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                            "-i", wav, "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                            "-shortest", "-movflags", "+faststart", OUT], stdin=subprocess.PIPE)
    out_frame = 0
    prev_img = None
    for s in timeline:
        c = s["clip"]
        ss = max(0.0, s["t0"] - 0.3)
        stream = ff_read(["-ss", f"{ss:.3f}", "-i", SRC + c + ".mov", "-vf", f"fps={FPS},{TM},format=rgb24"], 1080, 1920)
        for k0, fr in enumerate(stream):
            tt = ss + k0 / FPS
            if tt < s["t0"] - 1e-6:
                continue
            if tt >= s["t1"]:
                break
            tout = s["out0"] + (tt - s["t0"])
            ofi = int(round(tout * FPS))
            ccx, ccy, zb = ENC[c]
            z = zb * s["z"] * (1 + (0 if SINZOOM else 0.03) * (tt - s["t0"]) / max(0.5, s["t1"] - s["t0"]))
            if c == "IMG_7581" and tt > 8.6:   # al irse, el plano se abre para enseñar el horizonte
                e = min(1.0, (tt - 8.6) / 0.8); e = e * e * (3 - 2 * e)
                z = z + (1.0 - z) * e; ccx = ccx + (540 - ccx) * e; ccy = ccy + (960 - ccy) * e
            cw = int(1080 / z); ch = int(1920 / z)
            x0 = int(min(max(ccx - cw / 2, 0), 1080 - cw)); y0 = int(min(max(ccy - ch / 2, 0), 1920 - ch))
            img = cv2.resize(fr[y0:y0 + ch, x0:x0 + cw], (W, H), interpolation=cv2.INTER_LANCZOS4)
            bl = cv2.GaussianBlur(img, (0, 0), 1.4); img = cv2.addWeighted(img, 1.5, bl, -0.5, 0)
            img = gradear(img)
            sb = sub_en(tout)
            if sb is not None:
                poner(img, sb)
            # el móvil con la función, encima del horizonte
            tp0 = t_out("IMG_7581", PHONE_T0)
            if c == "IMG_7581" and tout >= tp0:
                k = int((tout - tp0) * FPS)
                if k < N_PHONE:
                    ph = cv2.cvtColor(cv2.imread(PHONE + f"f_{k:04d}.png", cv2.IMREAD_UNCHANGED), cv2.COLOR_BGRA2RGBA)
                    ent = min(1.0, k / 9.0); ent = ent * ent * (3 - 2 * ent)
                    dy = int(90 + (1 - ent) * 70)
                    M = np.float32([[1, 0, 0], [0, 1, dy]])
                    ph = cv2.warpAffine(ph, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
                    a_ = ph[:, :, 3:4].astype(np.float32) / 255 * ent
                    img = (img.astype(np.float32) * (1 - a_) + ph[:, :, :3].astype(np.float32) * a_).astype(np.uint8)
                    layer, al = caption_en(k / FPS)
                    if layer is not None:
                        poner(img, layer, y_s=1700 - 380, alpha=al)
            if ofi < 5:
                img = (img * (ofi + 1) / 6).astype(np.uint8)
            while out_frame < ofi:
                enc.stdin.write(prev_img.tobytes()); out_frame += 1
            enc.stdin.write(img.tobytes()); out_frame += 1; prev_img = img
    # tarjeta final con fundido
    for k in range(int(END * FPS)):
        if k < 6:
            a = k / 6.0
            img = (prev_img.astype(np.float32) * (1 - a) + card.astype(np.float32) * a).astype(np.uint8)
        else:
            img = card
        enc.stdin.write(img.tobytes()); out_frame += 1
    enc.stdin.close(); enc.wait()
    print("OK", OUT, out_frame, "fotogramas")


if __name__ == "__main__":
    main()
