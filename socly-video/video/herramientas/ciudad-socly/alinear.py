"""Alinea las voces de AI Studio con los 28 planos: corta cada frase, la ajusta a su plano y la coloca.
Uso: PYTHONUTF8=1 python alinear.py "<narrador.wav>" ["<soclo.wav>"]
Salida: audio\\voz.wav y audio\\tiempos.json (con tiempo de cada palabra para los subtítulos)."""
import sys, os, json, re, subprocess, difflib, wave
import numpy as np

BASE = r"/home/user/prueba/socly-video\video\herramientas\ciudad-socly"
AUD = os.path.join(BASE, "audio")
FF = r"/usr/bin/ffmpeg"
SR = 44100
exec(open(os.path.join(BASE, "voces.py"), encoding="utf-8").read().split("def dur(")[0].split("FRASES = [")[0].split("import asyncio")[0]) if False else None
FRASES = [l.strip() for l in open(os.path.join(AUD, "texto-voz-knox.txt"), encoding="utf-8").read().split("TEXTO (una frase por línea, tal cual):")[1].strip().splitlines() if l.strip()]
SOCLO_PLANOS = [16, 17, 20, 27]
assert len(FRASES) == 28, len(FRASES)

def pcm(path, sr):
    r = subprocess.run([FF, "-v", "error", "-i", path, "-f", "f32le", "-ac", "1", "-ar", str(sr), "-"], capture_output=True)
    return np.frombuffer(r.stdout, dtype=np.float32)

def norm(w):
    return re.sub(r"[^a-záéíóúüñ0-9]", "", w.lower().replace("socly", "soclo"))

def palabras_whisper(audio16):
    from faster_whisper import WhisperModel
    m = WhisperModel("small", device="cpu", compute_type="int8")
    segs, _ = m.transcribe(audio16, language="es", word_timestamps=True, vad_filter=False, beam_size=5)
    out = []
    for s in segs:
        for w in s.words: out.append((w.word.strip(), w.start, w.end))
    return out

def mapear(frases, hip):
    """Asigna a cada palabra de referencia un (inicio, fin) usando difflib sobre las palabras reconocidas."""
    ref = [(i, w) for i, f in enumerate(frases) for w in f.split()]
    rn = [norm(w) for _, w in ref]; hn = [norm(h[0]) for h in hip]
    sm = difflib.SequenceMatcher(None, rn, hn, autojunk=False)
    tim = [None] * len(ref)
    for tag, a0, a1, b0, b1 in sm.get_opcodes():
        if tag == "equal" or (tag == "replace" and a1 - a0 == b1 - b0):
            for k in range(a1 - a0): tim[a0 + k] = (hip[b0 + k][1], hip[b0 + k][2])
    # interpolar los huecos
    for k in range(len(tim)):
        if tim[k] is None:
            l = next((j for j in range(k - 1, -1, -1) if tim[j]), None); r = next((j for j in range(k + 1, len(tim)) if tim[j]), None)
            if l is not None and r is not None:
                n = r - l; tim[k] = (tim[l][1] + (tim[r][0] - tim[l][1]) * (k - l) / n, tim[l][1] + (tim[r][0] - tim[l][1]) * (k - l + 1) / n)
            elif l is not None: tim[k] = (tim[l][1], tim[l][1] + 0.25)
            elif r is not None: tim[k] = (max(0, tim[r][0] - 0.25), tim[r][0])
            else: tim[k] = (0, 0.25)
    por_frase = {}
    for (i, w), t in zip(ref, tim): por_frase.setdefault(i, []).append((w, t[0], t[1]))
    return por_frase

def atempo(x, t):
    if abs(t - 1.0) < 0.02: return x
    p = subprocess.run([FF, "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af", "atempo=%.4f" % t, "-f", "f32le", "-ar", str(SR), "-ac", "1", "-"],
                       input=x.astype(np.float32).tobytes(), capture_output=True)
    return np.frombuffer(p.stdout, dtype=np.float32).copy()

archivos = sys.argv[1:]
datos = []
for p in archivos:
    a = pcm(p, SR); datos.append((p, a, len(a) / SR))
    print(os.path.basename(p), "%.1f s" % (len(a) / SR))
datos.sort(key=lambda d: -d[2])
narr = datos[0]; soc = datos[1] if len(datos) > 1 else None

print("Whisper (narrador)...", flush=True)
hn = palabras_whisper(pcm(narr[0], 16000))
mp_n = mapear(FRASES, hn)
mp_s = None
if soc:
    print("Whisper (Soclo)...", flush=True)
    frs = [FRASES[i - 1] for i in SOCLO_PLANOS]
    mp_s = mapear(frs, palabras_whisper(pcm(soc[0], 16000)))

total = np.zeros(int(70.5 * SR), dtype=np.float32); tiempos = []
for i, fr in enumerate(FRASES, 1):
    usar_soclo = soc is not None and i in SOCLO_PLANOS
    if usar_soclo: ws = mp_s[SOCLO_PLANOS.index(i)]; audio = soc[1]
    else: ws = mp_n[i - 1]; audio = narr[1]
    s0 = max(0.0, ws[0][1] - 0.04); s1 = ws[-1][2] + 0.10
    seg = audio[int(s0 * SR):int(s1 * SR)].copy()
    d = len(seg) / SR
    tempo = min(1.6, max(1.0, d / 2.36))
    seg = atempo(seg, tempo)
    n = len(seg); f = int(0.006 * SR)
    seg[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f)
    t0 = (i - 1) * 2.5 + 0.04
    n0 = int(t0 * SR); total[n0:n0 + n] += seg[:max(0, len(total) - n0)]
    pal = [{"w": w, "a": round(t0 + (a - s0) / tempo, 3), "b": round(t0 + (b - s0) / tempo, 3)} for (w, a, b) in ws]
    tiempos.append({"plano": i, "frase": fr, "inicio": round(t0, 3), "fin": round(t0 + n / SR, 3), "tempo": round(tempo, 2),
                    "voz": "soclo" if usar_soclo else "narrador", "palabras": pal})
    print(i, "%.2fs -> %.2fs (x%.2f) %s" % (d, n / SR, tempo, "SOCLO" if usar_soclo else ""))
pico = np.abs(total).max(); total = total / pico * 0.93 if pico > 0.93 else total
with wave.open(os.path.join(AUD, "voz.wav"), "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((total * 32767).astype(np.int16).tobytes())
json.dump(tiempos, open(os.path.join(AUD, "tiempos.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok")
