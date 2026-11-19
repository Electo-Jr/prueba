#!/bin/bash
# Limpia los dos clips nuevos del cartel de ESIC (tú delante del cartel + tu socio en la escalera):
# vídeo a 1080x1920 SDR a 30 fps y sonido con el ruido reducido (mismo ajuste «suave» del jardín) y volumen igualado.
# Desde esta carpeta: bash limpiar-esic.sh   Salida: video\fotos-propias\match\esic\limpio\
set -e
FF="/usr/bin/ffmpeg"
HERE="$(cd "$(dirname "$0")" && pwd)"
SRC="$HERE/../../fotos-propias/match/esic"
OUT="$SRC/limpio"
mkdir -p "$OUT"
cd "$HERE/../jardin"   # el modelo de ruido está en herramientas\jardin\modelo

HDR="zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p,scale=1080:1920:flags=lanczos,fps=30"
SDR="scale=1080:1920:flags=lanczos,unsharp=5:5:0.6,fps=30,format=yuv420p"
AF="highpass=f=80,arnndn=m=modelo/bd.rnnn:mix=0.6,afftdn=nr=8,loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000"

"$FF" -y -loglevel error -i "$SRC/1-IMG_3623.mov" -vf "$HDR" -af "$AF" -c:v libx264 -crf 15 -preset medium -c:a aac -b:a 192k -ar 48000 "$OUT/1-cartel-limpio.mp4"
"$FF" -y -loglevel error -i "$SRC/2-socio.mov"    -vf "$SDR" -af "$AF" -c:v libx264 -crf 15 -preset medium -c:a aac -b:a 192k -ar 48000 "$OUT/2-socio-limpio.mp4"
echo "listo: $OUT"
