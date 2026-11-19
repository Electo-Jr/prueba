"""Planos 14 y 15 con la grabación REAL de la app dentro de un móvil, sobre el vestidor en 3D (fondo desenfocado).
Se ejecuta tras montar.sh (necesita planos\\s14.mp4 y s15.mp4 renderizados). Salida: planos\\s14-app.mp4 y s15-app.mp4.
Uso: PYTHONUTF8=1 python app_planos.py"""
import os, subprocess
BASE = r"/home/user/prueba/socly-video\video\herramientas\ciudad-socly"
REC = r"/home/user/prueba/socly-video\video\fotos-propias\grabacion-app-zorro\original\grabacion-app.mp4"
FF = r"/usr/bin/ffmpeg"

R = 64  # esquina del móvil (a 1080x1920)
MARCO = (
    "crop=iw:ih*0.93:0:ih*0.07,scale=620:-2,pad=iw+36:ih+36:18:18:0x3b3b44,format=yuva420p,"
    "geq=lum='lum(X,Y)':cb='cb(X,Y)':cr='cr(X,Y)':"
    "a='if(gt(abs(W/2-X)-(W/2-%d),0)*gt(abs(H/2-Y)-(H/2-%d),0)*gt(hypot(abs(W/2-X)-(W/2-%d),abs(H/2-Y)-(H/2-%d)),%d),0,255)'" % (R, R, R, R, R)
)
FONDO = "[0:v]boxblur=30:2,eq=brightness=-0.35:saturation=0.8[bg]"

def hacer(plano, tramos):
    """tramos = [(inicio_s, fin_s), ...] de la grabación, en orden."""
    n = len(tramos)
    partes = []
    for i, (a, b) in enumerate(tramos):
        partes.append("[1:v]trim=start=%.3f:end=%.3f,setpts=PTS-STARTPTS,fps=30[c%d]" % (a, b, i))
    cat = "".join("[c%d]" % i for i in range(n)) + "concat=n=%d:v=1:a=0[rec]" % n if n > 1 else "[c0]null[rec]"
    graf = ";".join([FONDO] + partes + [cat, "[rec]%s[ph]" % MARCO, "[bg][ph]overlay=(W-w)/2:(H-h)/2:shortest=1,format=yuv420p[v]"])
    gf = os.path.join(BASE, "app-grafo-%d.txt" % plano)
    open(gf, "w", encoding="utf-8").write(graf)
    cmd = [FF, "-v", "error", "-y", "-i", os.path.join(BASE, "planos", "s%02d.mp4" % plano), "-i", REC, "-filter_complex_script", gf,
           "-map", "[v]", "-t", "2.5", "-r", "30", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20",
           os.path.join(BASE, "planos", "s%02d-app.mp4" % plano)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    print(plano, r.stderr[-500:] or "ok")

hacer(14, [(6.0, 8.5)])                                   # «Y en su móvil, Socly Style»: Inicio con el look
hacer(15, [(12.0, 12.84), (7.3, 8.14), (17.0, 17.84)])    # prendas subidas / look montado / Vista puesta
