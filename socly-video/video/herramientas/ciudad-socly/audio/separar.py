"""Separa voz y música del audio de referencia con demucs (gratis, en el PC).
PYTHONPATH=C:/pp python separar.py   ->  audio\\ref-musica.wav y audio\\ref-voz.wav"""
import sys, os
sys.path.insert(0, "C:/pp")
import numpy as np, soundfile as sf, torch
from demucs.pretrained import get_model
from demucs.apply import apply_model

A = r"/home/user/prueba/socly-video\video\herramientas\ciudad-socly\audio"
x, sr = sf.read(os.path.join(A, "ref.wav"), dtype="float32")
if x.ndim == 1: x = np.stack([x, x], 1)
print("audio", x.shape, sr, flush=True)
model = get_model("htdemucs"); model.eval()
wav = torch.from_numpy(x.T.copy())[None]
ref = wav.mean(0)
wav = (wav - ref.mean()) / (ref.std() + 1e-8)
with torch.no_grad():
    out = apply_model(model, wav, device="cpu", split=True, overlap=0.25, progress=False)[0]
out = out * (ref.std() + 1e-8) + ref.mean()
iv = model.sources.index("vocals")
voz = out[iv]
musica = sum(out[i] for i in range(len(model.sources)) if i != iv)
sf.write(os.path.join(A, "ref-voz.wav"), voz.numpy().T, sr)
sf.write(os.path.join(A, "ref-musica.wav"), musica.numpy().T, sr)
print("listo", model.sources, flush=True)
