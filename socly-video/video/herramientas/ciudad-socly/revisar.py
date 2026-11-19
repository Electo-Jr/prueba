"""Hojas de revisión: 4 momentos (fotogramas 0, 25, 50, 74) de cada plano, 4 planos por hoja -> revision\\hoja-N.png
Uso: PYTHONUTF8=1 python revisar.py [primero ultimo]"""
import os, subprocess, sys
BASE = r"/home/user/prueba/socly-video\video\herramientas\ciudad-socly"
FF = r"/usr/bin/ffmpeg"
os.makedirs(os.path.join(BASE, "revision"), exist_ok=True)
a = int(sys.argv[1]) if len(sys.argv) > 1 else 1
b = int(sys.argv[2]) if len(sys.argv) > 2 else 28
FR = (0, 25, 50, 74)
for h0 in range(a, b + 1, 4):
    planos = list(range(h0, min(h0 + 4, b + 1)))
    ins, filt = [], []
    k = 0
    for p in planos:
        for f in FR:
            ins += ["-i", os.path.join(BASE, "planos", "s%02d" % p, "f_%04d.png" % f)]
            filt.append("[%d:v]scale=240:-1[t%d]" % (k, k)); k += 1
    rows = []
    for r in range(len(planos)):
        rows.append("".join("[t%d]" % (r * 4 + c) for c in range(4)) + "hstack=inputs=4[r%d]" % r)
    graf = ";".join(filt + rows + ["".join("[r%d]" % r for r in range(len(planos))) + "vstack=inputs=%d" % len(planos)])
    out = os.path.join(BASE, "revision", "hoja-%02d-%02d.png" % (planos[0], planos[-1]))
    subprocess.run([FF, "-v", "error", "-y"] + ins + ["-filter_complex", graf, out], check=True)
    print(out)
