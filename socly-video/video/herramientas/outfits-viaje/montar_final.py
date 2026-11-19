"""Fase 7 de «¿De dónde vienen los outfits?»: monta los 34 planos, los ajusta a la voz (Whisper), subtitula y mezcla la música de Ciudad Socly.
Uso: PYTHONUTF8=1 python montar_final.py            (todo)
     PYTHONUTF8=1 python montar_final.py sin-subs   (solo vídeo + audio, para probar el ritmo)
Salida: video\\anuncios\\de-donde-vienen-los-outfits\\de-donde-vienen-los-outfits.mp4 (+ -ligero.mp4 en 720p)"""
import sys, os, re, json, difflib, subprocess
import numpy as np

HERE = r"/home/user/prueba/socly-video\video\herramientas\outfits-viaje"
ROOT = r"/home/user/prueba/socly-video\video"
FF = r"/usr/bin/ffmpeg"
VOZ = HERE + r"\voz-fenrir.wav"
MUS_REF = ROOT + r"\herramientas\ciudad-socly\audio\ref-musica.wav"
MUS_OK = ROOT + r"\herramientas\ciudad-socly\audio\musica.wav"
PLANOS = HERE + r"\planos"
TMP = HERE + r"\montaje"
SALIDA = ROOT + r"\anuncios\de-donde-vienen-los-outfits"
FONT = "C\\:/Windows/Fonts/impact.ttf"
os.makedirs(TMP, exist_ok=True); os.makedirs(SALIDA, exist_ok=True)

FRASES = [
    "¿De dónde vienen los outfits?", "Soclo se lo preguntó ante su armario.", "Abrió la puerta… y se cayó dentro.",
    "Hace decenas de miles de años.", "Hace frío. Aquí nadie elige: se abriga.", "Alguien inventó la aguja de hueso.",
    "Y ya llevaban collares de conchas.", "Adornarse es casi tan viejo como abrigarse.", "Egipto. Calor, lino y ropa blanca.",
    "Y mira ese: va de verde.", "El verde era el color de la vida.", "Joyas, pelucas, maquillaje: ya había look.",
    "Roma. El púrpura costaba una fortuna.", "Solo los poderosos podían llevarlo.", "El color ya decía quién eras.",
    "Edad Media. Había leyes sobre qué ponerte.", "Según tu clase, ciertas telas estaban prohibidas.", "Soclo ni podía mirar ese terciopelo.",
    "1852. Aparece una palabra nueva.", "Outfit. Ya no era equipamiento: era tu ropa.", "Un modisto puso su nombre en sus vestidos.",
    "Y las revistas dijeron qué combinar.", "Años 60. La calle empieza a mandar.", "Los jóvenes inventan su propio estilo.",
    "Y llegan los blogs de street style.", "2010. Llega Instagram.", "Por fin se ve el conjunto entero.",
    "Se populariza el hashtag OOTD: el outfit del día.", "Soclo vuelve a casa.", "Antes decidía una ley o una revista.",
    "Hoy decides tú cada mañana…", "…y muchas veces acabas con lo mismo.", "En Socly lo decides con tu ropa.", "Entra en Socly Style.",
]
assert len(FRASES) == 34
ROTULOS = {4: "PREHISTORIA", 9: "EGIPTO", 13: "ROMA", 16: "EDAD MEDIA", 19: "1852", 23: "AÑOS 60", 26: "2010", 29: "HOY"}


def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, **kw)
    return r


def pcm(path, sr):
    r = run([FF, "-v", "error", "-i", path, "-f", "f32le", "-ac", "1", "-ar", str(sr), "-"])
    return np.frombuffer(r.stdout, dtype=np.float32)


def norm(w):
    return re.sub(r"[^a-záéíóúüñ0-9]", "", w.lower().replace("socly", "soclo"))


def palabras_whisper(audio16):
    from faster_whisper import WhisperModel
    m = WhisperModel("small", device="cpu", compute_type="int8")
    segs, _ = m.transcribe(audio16, language="es", word_timestamps=True, vad_filter=False, beam_size=5)
    return [(w.word.strip(), w.start, w.end) for s in segs for w in s.words]


def mapear(frases, hip):
    ref = [(i, w) for i, f in enumerate(frases) for w in f.split()]
    rn = [norm(w) for _, w in ref]; hn = [norm(h[0]) for h in hip]
    sm = difflib.SequenceMatcher(None, rn, hn, autojunk=False)
    tim = [None] * len(ref)
    for tag, a0, a1, b0, b1 in sm.get_opcodes():
        if tag == "equal" or (tag == "replace" and a1 - a0 == b1 - b0):
            for k in range(a1 - a0): tim[a0 + k] = (hip[b0 + k][1], hip[b0 + k][2])
    for k in range(len(tim)):
        if tim[k] is None:
            l = next((j for j in range(k - 1, -1, -1) if tim[j]), None); r = next((j for j in range(k + 1, len(tim)) if tim[j]), None)
            if l is not None and r is not None:
                n = r - l; tim[k] = (tim[l][1] + (tim[r][0] - tim[l][1]) * (k - l) / n, tim[l][1] + (tim[r][0] - tim[l][1]) * (k - l + 1) / n)
            elif l is not None: tim[k] = (tim[l][1], tim[l][1] + 0.25)
            elif r is not None: tim[k] = (max(0, tim[r][0] - 0.25), tim[r][0])
            else: tim[k] = (0, 0.25)
    por = {}
    for (i, w), t in zip(ref, tim): por.setdefault(i, []).append((w, t[0], t[1]))
    return por


def duracion(path):
    r = run([FF, "-i", path]); m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", r.stderr.decode("utf-8", "ignore"))
    return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))


# ------------------------------------------------------------------ 1. clips de cada plano
for i in range(1, 35):
    d = "%s\\s%02d" % (PLANOS, i); out = d + ".mp4"
    n = len([f for f in os.listdir(d) if f.endswith(".png")])
    assert n >= 75, "FALTA plano %d (%d fotogramas)" % (i, n)
    if not os.path.exists(out) or os.path.getmtime(out) < os.path.getmtime(d + "\\f_0074.png"):
        r = run([FF, "-v", "error", "-y", "-framerate", "30", "-i", d + "\\f_%04d.png", "-vf", "scale=1080:1920:flags=lanczos", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", out])
        if r.returncode: print(r.stderr.decode()[-300:]); sys.exit(1)
print("clips ok", flush=True)

# ------------------------------------------------------------------ 2. alineación con la voz
TJ = TMP + r"\tiempos.json"
if os.path.exists(TJ) and os.path.getmtime(TJ) > os.path.getmtime(VOZ):
    por = {int(k): v for k, v in json.load(open(TJ, encoding="utf-8")).items()}
else:
    print("Whisper...", flush=True)
    por = mapear(FRASES, palabras_whisper(pcm(VOZ, 16000)))
    json.dump(por, open(TJ, "w", encoding="utf-8"), ensure_ascii=False)
vdur = duracion(VOZ)
inicio = [0.0] + [max(0.0, por[i][0][1] - 0.10) for i in range(1, 34)]
total = vdur + 0.6
dur = [inicio[i + 1] - inicio[i] for i in range(33)] + [total - inicio[33]]
print("Voz %.2f s, vídeo %.2f s" % (vdur, total))
for i, d in enumerate(dur, 1):
    flag = "  <-- AVISO" if d / 2.5 > 2.0 or d / 2.5 < 0.55 else ""
    print("plano %2d  %.2f s  x%.2f%s" % (i, d, d / 2.5, flag))

# ------------------------------------------------------------------ 3. retemporizar y unir
lista = TMP + r"\lista.txt"
with open(lista, "w", encoding="utf-8") as fl:
    for i, d in enumerate(dur, 1):
        out = "%s\\r%02d.mp4" % (TMP, i)
        r = run([FF, "-v", "error", "-y", "-i", "%s\\s%02d.mp4" % (PLANOS, i), "-vf", "setpts=PTS*%.5f,fps=30" % (d / 2.5), "-t", "%.3f" % d,
                 "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-an", out])
        if r.returncode: print(r.stderr.decode()[-300:]); sys.exit(1)
        fl.write("file '%s'\n" % out.replace("\\", "/"))
MUDO = TMP + r"\mudo.mp4"
r = run([FF, "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lista, "-c", "copy", MUDO]); print(r.stderr.decode()[-300:] or "unido", flush=True)

# ------------------------------------------------------------------ 4. subtítulos (una palabra, amarillo) y rótulos de época
partes = []
for i in range(34):
    ws = por[i]
    for j, (w, a, b) in enumerate(ws):
        fin = ws[j + 1][1] if j + 1 < len(ws) else b + 0.15
        if j + 1 == len(ws) and i < 33: fin = min(fin, inicio[i + 1] + 0.05)
        t = re.sub(r"[¿?¡!…,.;:]", "", w)
        if not t: continue
        t = t.replace("\\", "").replace("'", "").replace("%", "\\%")
        partes.append("drawtext=fontfile='%s':text='%s':fontsize=150:fontcolor=0xFFE500:borderw=10:bordercolor=black:x=(w-text_w)/2:y=1540:enable='between(t,%.3f,%.3f)'" % (FONT, t, a, max(a + 0.08, fin - 0.001)))
    if (i + 1) in ROTULOS:
        partes.append("drawtext=fontfile='%s':text='%s':fontsize=110:fontcolor=white:borderw=8:bordercolor=black:x=(w-text_w)/2:y=170:enable='between(t,%.3f,%.3f)'" % (FONT, ROTULOS[i + 1], inicio[i] + 0.1, inicio[i] + 1.9))
SUBS = TMP + r"\subs-filtro.txt"
open(SUBS, "w", encoding="utf-8").write(",".join(partes))
CON = TMP + r"\subtitulado.mp4"
if len(sys.argv) > 1 and sys.argv[1] == "sin-subs":
    CON = MUDO
else:
    r = run([FF, "-v", "error", "-y", "-i", MUDO, "-filter_script:v", SUBS, "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", CON])
    if r.returncode: print(r.stderr.decode()[-500:]); sys.exit(1)
    print("subtítulos ok", flush=True)

# ------------------------------------------------------------------ 5. música de Ciudad Socly bajo la voz
def media_db(args):
    r = run([FF, "-i"] + args + ["-af", "volumedetect", "-f", "null", "-"])
    m = re.search(r"mean_volume: (-?[\d.]+) dB", r.stderr.decode("utf-8", "ignore")); return float(m.group(1)) if m else -20.0
objetivo = media_db([MUS_OK])
MUS = TMP + r"\musica.wav"
run([FF, "-v", "error", "-y", "-ss", "30", "-t", "%.2f" % (total + 1), "-i", MUS_REF, MUS])
gan = objetivo - media_db([MUS])
print("música: ganancia %.1f dB (igual que Ciudad Socly)" % gan, flush=True)
FINAL = SALIDA + r"\de-donde-vienen-los-outfits.mp4"
fc = ("[1:a]aresample=44100,apad=whole_dur=%.2f[v];[2:a]atrim=0:%.2f,volume=%.2fdB,afade=t=in:d=0.6,afade=t=out:st=%.2f:d=2.5[m];"
      "[v][m]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[a]") % (total, total, gan, total - 2.5)
r = run([FF, "-v", "error", "-y", "-i", CON, "-i", VOZ, "-i", MUS, "-filter_complex", fc, "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-t", "%.2f" % total, FINAL])
print(r.stderr.decode()[-500:] or "final ok", flush=True)
LIG = SALIDA + r"\de-donde-vienen-los-outfits-ligero.mp4"
r = run([FF, "-v", "error", "-y", "-i", FINAL, "-vf", "scale=720:1280:flags=lanczos", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "27", "-c:a", "aac", "-b:a", "128k", LIG])
print(r.stderr.decode()[-300:] or "ligero ok")
for f in (FINAL, LIG): print(f, "%.1f MB" % (os.path.getsize(f) / 1e6))
