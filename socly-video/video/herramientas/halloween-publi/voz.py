"""Narración con em_alex. Las palabras en inglés ({en:...}) se dicen con fonemas ingleses.
Uso: python voz.py guion.txt salida.wav [velocidad]
Escribe también salida.json con el inicio/fin de cada frase."""
import json, re, sys, os
import numpy as np, soundfile as sf
from kokoro_onnx import Kokoro

root = os.path.expanduser('~/.cache/hyperframes/tts')
k = Kokoro(f'{root}/models/kokoro-v1.0.onnx', f'{root}/voices/voices-v1.0.bin')
VOICE = 'em_alex'
speed = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
lines = [l.strip() for l in open(sys.argv[1], encoding='utf-8') if l.strip()]
SR = 24000
gap = lambda s: np.zeros(int(SR * s), dtype=np.float32)

def say(text, lang):
    a, sr = k.create(text, voice=VOICE, speed=speed, lang=lang)
    assert sr == SR
    return a

out, marks, t, words = [], [], 0.0, []
for line in lines:
    parts = re.split(r'(\{en:[^}]+\})', line)
    chunks, pos = [], t
    for p in parts:
        p = p.strip()
        if not p:
            continue
        en = p.startswith('{en:')
        txt = p[4:-1] if en else p
        a = say(txt, 'en-us' if en else 'es')
        ws = txt.split()
        tot = sum(len(w) + 1 for w in ws)
        dur = len(a) / SR
        acc = pos
        for w in ws:
            d = dur * (len(w) + 1) / tot
            words.append({'w': w, 'a': round(acc, 2), 'b': round(acc + d, 2), 'en': en})
            acc += d
        chunks.append(a)
        pos += dur + 0.06
    seg = np.concatenate([np.concatenate([c, gap(0.06)]) for c in chunks])
    marks.append({'texto': re.sub(r'\{en:([^}]+)\}', r'\1', line), 'inicio': round(t, 2), 'fin': round(t + len(seg) / SR, 2)})
    out += [seg, gap(0.35)]
    t += len(seg) / SR + 0.35
sf.write(sys.argv[2], np.concatenate(out), SR)
json.dump({'frases': marks, 'palabras': words}, open(os.path.splitext(sys.argv[2])[0] + '.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(json.dumps(marks, ensure_ascii=False, indent=1))
print('total', round(t, 2), 's')
