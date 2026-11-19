"""Música house suave («chill house») generada desde cero: sin derechos de nadie.
Uso: PYTHONUTF8=1 python musica.py <salida.wav> [segundos]
122 BPM, bombo a negro, palmas en 2 y 4, hi-hat a contratiempo, bajo, acordes tipo piano eléctrico y colchón suave.
"""
import sys
import wave
import numpy as np

SR = 48000
BPM = 122
DUR = float(sys.argv[2]) if len(sys.argv) > 2 else 5.6
out = sys.argv[1]
rng = np.random.default_rng(7)
n = int(SR * DUR)
beat = 60 / BPM
t_all = np.arange(n) / SR


def lp(x, fc):
    a = 1 - np.exp(-2 * np.pi * fc / SR)
    y = np.empty_like(x)
    acc = 0.0
    for i, v in enumerate(x):
        acc += a * (v - acc)
        y[i] = acc
    return y


def hp(x, fc):
    return x - lp(x, fc)


def add(buf, start, sig, gain=1.0):
    i = int(start * SR)
    if i >= len(buf):
        return
    j = min(len(buf), i + len(sig))
    buf[i:j] += sig[: j - i] * gain


def hz(note):  # nota MIDI -> Hz
    return 440 * 2 ** ((note - 69) / 12)


# --- sonidos sueltos
def kick():
    t = np.arange(int(SR * 0.34)) / SR
    f = 45 + 95 * np.exp(-t * 32)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t * 9) * 1.0


def clap():
    t = np.arange(int(SR * 0.22)) / SR
    x = hp(rng.standard_normal(len(t)), 900)
    x = lp(x, 6500)
    env = np.exp(-t * 26) + 0.55 * np.exp(-np.maximum(t - 0.012, 0) * 40) * (t > 0.012)
    return x * env * 0.5


def hat(open_=False):
    t = np.arange(int(SR * (0.16 if open_ else 0.05))) / SR
    x = hp(rng.standard_normal(len(t)), 7000)
    return x * np.exp(-t * (22 if open_ else 80)) * 0.32


def epiano(note, length):
    t = np.arange(int(SR * length)) / SR
    f = hz(note)
    x = (np.sin(2 * np.pi * f * t) + 0.45 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t * 6)
         + 0.2 * np.sin(2 * np.pi * 3.01 * f * t) * np.exp(-t * 10))
    att = np.minimum(t / 0.008, 1)
    return x * att * np.exp(-t * 2.6) * 0.5


def pad(note, length):
    t = np.arange(int(SR * length)) / SR
    f = hz(note)
    x = sum(np.sin(2 * np.pi * f * (1 + d) * t) for d in (-0.004, 0.0, 0.004))
    x = x + 0.5 * np.sin(2 * np.pi * f * 2 * t)
    return x * np.minimum(t / 0.5, 1) * np.minimum((length - t) / 0.4, 1) * 0.22


def bass(note, length):
    t = np.arange(int(SR * length)) / SR
    f = hz(note)
    x = np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * 2 * f * t)
    return x * np.minimum(t / 0.006, 1) * np.exp(-t * 4.5) * 0.7


# --- armonía: Fmaj7 | Em7 | Dm9 | Cmaj7  (una por compás)
CHORDS = [
    (41, [60, 64, 69, 72]),   # F A C E  (Fmaj7)
    (40, [59, 62, 67, 71]),   # Em7
    (38, [60, 62, 65, 69]),   # Dm9
    (36, [59, 64, 67, 72]),   # Cmaj7
]
bar = beat * 4

drums = np.zeros(n)
music = np.zeros(n)
duck = np.ones(n)

nb = int(DUR / beat) + 1
k = kick()
for b in range(nb):
    ts = b * beat
    add(drums, ts, k, 0.95)
    # el bombo "agacha" el resto un instante (efecto de compresión típico del house)
    i0 = int(ts * SR)
    L = int(0.22 * SR)
    seg = np.arange(min(L, n - i0))
    if len(seg):
        duck[i0 : i0 + len(seg)] = np.minimum(duck[i0 : i0 + len(seg)], 0.35 + 0.65 * (seg / L) ** 1.4)
    if b % 2 == 1:
        add(drums, ts, clap(), 0.8)
    add(drums, ts + beat / 2, hat(), 1.0)
    if b % 4 == 3:
        add(drums, ts + beat / 2, hat(True), 0.8)
    add(drums, ts + beat * 0.75, hat(), 0.35)

for c in range(int(DUR / bar) + 1):
    root, notes = CHORDS[c % 4]
    tb = c * bar
    for nt in notes:
        add(music, tb, pad(nt, bar + 0.15), 0.9)
        add(music, tb + beat * 0.75, epiano(nt, beat * 1.2), 0.55)       # golpe de acorde sincopado
        add(music, tb + beat * 2.5, epiano(nt, beat * 1.2), 0.45)
    for e in range(8):                                                   # bajo a corcheas, a contratiempo
        if e % 2 == 1 or e == 0:
            add(music, tb + e * beat / 2, bass(root, beat * 0.45), 1.0)

music = lp(music, 5200) * duck
mix = drums + music * 0.95

# fundido de entrada/salida y nivel
fade_in = np.minimum(t_all / 0.35, 1)
fade_out = np.minimum((DUR - t_all) / 0.9, 1)
mix = mix * fade_in * fade_out
mix = mix / np.max(np.abs(mix)) * 0.8

# estéreo suave: la mitad más aguda se retrasa unos milisegundos en un canal
d = int(0.012 * SR)
right = mix.copy()
right[d:] = 0.8 * mix[d:] + 0.2 * mix[:-d]
st = np.stack([mix, right], axis=1)
pcm = (np.clip(st, -1, 1) * 32767).astype("<i2")
with wave.open(out, "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print("ok", out, f"{DUR:.1f}s")
