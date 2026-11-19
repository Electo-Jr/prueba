"""Une vídeo subtitulado + voz (+ música si existe audio\\musica.wav) -> prueba\\ciudad-socly-final.mp4
Uso: PYTHONUTF8=1 python final.py"""
import os, subprocess
BASE = r"/home/user/prueba/socly-video\video\herramientas\ciudad-socly"
FF = r"/usr/bin/ffmpeg"
V = os.path.join(BASE, "prueba", "ciudad-socly-subtitulado.mp4")
VOZ = os.path.join(BASE, "audio", "voz.wav")
MUS = os.path.join(BASE, "audio", "musica.wav")
OUTF = os.path.join(BASE, "prueba", "ciudad-socly-final.mp4")
if os.path.exists(MUS):
    cmd = [FF, "-v", "error", "-y", "-i", V, "-i", VOZ, "-i", MUS, "-filter_complex",
           "[1:a]volume=1.0,apad=whole_dur=70[v];[2:a]atrim=0:70,volume=1.0,afade=t=in:d=0.5,afade=t=out:st=68:d=2[m];"
           "[v][m]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[a]",
           "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-t", "70", OUTF]
else:
    cmd = [FF, "-v", "error", "-y", "-i", V, "-i", VOZ, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-t", "70", OUTF]
r = subprocess.run(cmd, capture_output=True, text=True)
print(r.stderr[-600:] or ("ok con música" if os.path.exists(MUS) else "ok sin música"))
