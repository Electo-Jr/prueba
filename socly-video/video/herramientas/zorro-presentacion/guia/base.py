"""Base del vídeo guiado: los trozos de la grabación ya recortados (c_*.mp4) se ajustan a la duración
de cada escena, se unen y se colocan sobre el fondo oscuro con la pantalla de esquinas redondeadas.
Uso: PYTHONUTF8=1 python base.py   (lee escenas.json -> base.mp4, 1080x1920, sin audio)"""
import json
import subprocess

from PIL import Image, ImageDraw

FF = "/usr/bin/ffmpeg"
SRC = "../../../fotos-propias/grabacion-app-zorro/original/grabacion-app.mp4"
W, H, PW, PH, PX, PY = 1080, 1920, 960, 1630, 60, 60
ESC = json.load(open("escenas.json", encoding="utf-8"))


def run(*args):
    subprocess.run([FF, "-v", "error", "-y", *args], check=True)


# Máscara de esquinas redondeadas
m = Image.new("L", (PW * 2, PH * 2), 0)
ImageDraw.Draw(m).rounded_rectangle((0, 0, PW * 2 - 1, PH * 2 - 1), radius=88, fill=255)
m.resize((PW, PH), Image.LANCZOS).save("mascara.png")

# 1) cada escena: sus trozos, ajustados a la duración exacta
partes = []
for i, e in enumerate(ESC):
    dur = e["dur"]
    if e.get("freeze") is not None:  # imagen fija de la grabación
        run("-ss", str(e["freeze"]), "-i", SRC, "-frames:v", "1", "-vf", "crop=1170:1986:0:140,scale=960:1630", f"f_{i}.png")
        run("-loop", "1", "-framerate", "30", "-t", str(dur), "-i", f"f_{i}.png", "-vf", "format=yuv420p", "-c:v", "libx264", "-crf", "16", f"s_{i}.mp4")
    else:
        lista = "".join(f"file '{c}'\n" for c in e["clips"])
        open(f"l_{i}.txt", "w").write(lista)
        run("-f", "concat", "-safe", "0", "-i", f"l_{i}.txt", "-vf", f"tpad=stop_mode=clone:stop_duration=3,trim=duration={dur},setpts=PTS-STARTPTS,fps=30,format=yuv420p", "-c:v", "libx264", "-crf", "16", f"s_{i}.mp4")
    partes.append(f"s_{i}.mp4")
open("todo.txt", "w").write("".join(f"file '{p}'\n" for p in partes))
run("-f", "concat", "-safe", "0", "-i", "todo.txt", "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", "pantalla.mp4")

# 2) pantalla con esquinas redondeadas sobre el fondo
total = sum(e["dur"] for e in ESC)
run(
    "-f", "lavfi", "-i", f"color=c=0x15140F:s={W}x{H}:r=30:d={total}",
    "-i", "pantalla.mp4", "-loop", "1", "-i", "mascara.png",
    "-filter_complex", f"[1:v][2:v]alphamerge[p];[0:v][p]overlay={PX}:{PY}:shortest=1,format=yuv420p",
    "-t", str(total), "-c:v", "libx264", "-crf", "16", "base.mp4",
)
print("base.mp4", round(total, 2), "s")
