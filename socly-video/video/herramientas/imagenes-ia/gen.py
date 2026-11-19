"""Uso: python gen.py <archivo_prompt.txt> <salida.png> <seed> [resolucion]
Genera una imagen con Z-Image-Turbo (Space público de Hugging Face, gratis)."""
import shutil
import sys
import time

from gradio_client import Client

prompt_file, out, seed = sys.argv[1], sys.argv[2], int(sys.argv[3])
res = sys.argv[4] if len(sys.argv) > 4 else '864x1152 ( 3:4 )'
prompt = open(prompt_file, encoding='utf-8').read().strip()

t = time.time()
c = Client('Tongyi-MAI/Z-Image-Turbo', verbose=False)
r = c.predict(prompt=prompt, resolution=res, seed=seed, steps=8, shift=3.0,
              random_seed=False, gallery_images=[], api_name='/generate')
item = r[0][0]
path = item['image'] if isinstance(item['image'], str) else item['image']['path']
shutil.copy(path, out)
print('ok', out, f'{time.time() - t:.0f}s')
