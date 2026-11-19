"""Mezcla: voz (narracion.wav) + música sintetizada desde cero (sin derechos) + efectos.
Uso: python audio.py <duracion_s> <salida.wav>"""
import sys
import numpy as np, soundfile as sf

SR = 24000
D = float(sys.argv[1])
N = int(SR * D)
rng = np.random.default_rng(7)
tt = np.arange(N) / SR

def env_exp(n, tau):
    return np.exp(-np.arange(n) / SR / tau)

def lowpass(x, k):  # media móvil simple, suficiente para suavizar
    k = max(1, int(k))
    c = np.cumsum(np.insert(x, 0, 0.0))
    y = (c[k:] - c[:-k]) / k
    return np.concatenate([np.zeros(k - 1), y])

# --- música: base oscura (La menor) + arpegio suave + hi-hat muy bajo
pad = sum(np.sin(2 * np.pi * f * tt + p) * a for f, p, a in [(55, 0, .5), (110, 1, .35), (164.8, 2, .22), (261.6, 3, .12)])
pad *= 0.75 + 0.25 * np.sin(2 * np.pi * 0.18 * tt)
music = pad * 0.5
step = 60 / 100 / 2  # corcheas a 100 BPM
notes = [220.0, 261.6, 329.6, 440.0, 329.6, 261.6, 392.0, 329.6]
i = 0
while i * step < D:
    t0 = i * step
    f = notes[i % len(notes)]
    n = int(SR * 0.9)
    s0 = int(t0 * SR)
    seg = np.sin(2 * np.pi * f * np.arange(n) / SR) * env_exp(n, 0.16) + 0.4 * np.sin(2 * np.pi * 2 * f * np.arange(n) / SR) * env_exp(n, 0.08)
    e = min(N, s0 + n)
    music[s0:e] += seg[: e - s0] * 0.22
    if i % 2 == 1:  # hi-hat en contratiempo
        m = int(SR * 0.05)
        h = rng.standard_normal(m) * env_exp(m, 0.012)
        h = h - lowpass(h, 6)
        e2 = min(N, s0 + m)
        music[s0:e2] += h[: e2 - s0] * 0.10
    i += 1
# eco simple
echo = np.zeros(N)
d1 = int(SR * 0.3)
echo[d1:] += music[:-d1] * 0.35
music = music + echo
music *= np.minimum(1, tt / 1.0) * np.minimum(1, (D - tt) / 1.6)
music /= np.max(np.abs(music)) + 1e-9
music *= 0.06  # muy por debajo de la voz

# --- efectos
def whoosh(dur, rise=True):
    n = int(SR * dur)
    x = rng.standard_normal(n)
    sweep = np.linspace(0, 1, n)
    k = (np.linspace(40, 4, n) if rise else np.linspace(4, 40, n)).astype(int)
    y = np.zeros(n)
    for a in range(0, n, 256):
        b = min(n, a + 256)
        kk = max(1, int(k[a]))
        y[a:b] = (x[max(0, a - kk):b].mean()) if kk > 1 else x[a:b]
    y = y - lowpass(y, 200)
    shape = np.sin(np.pi * sweep) ** 2
    y = x * 0.0 + y
    y = y / (np.max(np.abs(y)) + 1e-9)
    return y * shape

def pop(f0=720, f1=240, dur=0.16):
    n = int(SR * dur)
    f = np.linspace(f0, f1, n)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * env_exp(n, 0.045)

sfx = np.zeros(N)
ANC = [[0,0],[1.0,1.1],[3.06,2.32],[3.9,2.7],[4.55,3.12],[5.7,3.86],[7.98,5.32],[10.3,7.66],[13.3,11.8],[13.81,12.16],[15.17,13.64],[16.64,14.86],[18.4,17.0]]
def nuevo(o):
    for (o0,n0),(o1,n1) in zip(ANC,ANC[1:]):
        if o<=o1:
            return n0+(n1-n0)*max(0,(o-o0)/(o1-o0))
    return ANC[-1][1]+(o-ANC[-1][0])

def put(x, t, g):
    t = nuevo(t)
    s0 = int(t * SR)
    e = min(N, s0 + len(x))
    if s0 < N:
        sfx[s0:e] += x[: e - s0] * g

put(whoosh(0.9), 3.55, 0.5)            # sube el móvil
put(pop(), 4.55, 0.35); put(pop(), 5.7, 0.35); put(pop(), 7.98, 0.35)   # cambios de pantalla
put(whoosh(0.7, False), 10.15, 0.45)   # el móvil se va
put(pop(900, 300), 10.4, 0.45); put(pop(1000, 340), 10.6, 0.45)         # tarjetas
put(whoosh(0.8), 13.0, 0.55)           # inundación naranja
put(pop(1100, 380, 0.2), 16.6, 0.45)   # botón final

voz, sr = sf.read(sys.argv[3] if len(sys.argv) > 3 else 'narracion.wav')
assert sr == SR
if voz.ndim > 1:
    voz = voz[:, 0]
v = np.zeros(N)
v[: min(N, len(voz))] = voz[:N]
v *= 1.0 / (np.max(np.abs(v)) + 1e-9) * 0.9

mix = v + music + sfx * 0.55
mix /= max(1.0, np.max(np.abs(mix)) / 0.95)
sf.write(sys.argv[2], mix.astype(np.float32), SR)
print('ok', round(D, 2), 's')
