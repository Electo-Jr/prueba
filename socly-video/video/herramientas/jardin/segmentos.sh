#!/bin/bash
# Recorta los 4 clips del jardín, los pasa de HDR (iPhone) a SDR y limpia el ruido de fondo.
# Salida: $OUT/s1.mp4 … s4a.mp4 (persona) y s4b.mp4 (jardín, para el móvil encima).
FF="/usr/bin/ffmpeg"
SRC="/home/user/prueba/socly-video/video/fotos-propias/jardin/original"
OUT="$1"
mkdir -p "$OUT"

VF="zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p,scale=1080:1920,fps=30"
# audio: la versión llega en $AF (go.sh la define); por defecto, la suave
cd "$(dirname "$0")"
AF="${AF:-highpass=f=90,arnndn=m=modelo/bd.rnnn:mix=0.75,aresample=48000}"

seg() { # nombre entrada inicio fin
  "$FF" -y -loglevel error -ss "$3" -to "$4" -i "$SRC/$2" -vf "$VF" -af "$AF" \
    -c:v libx264 -crf 16 -preset medium -pix_fmt yuv420p -c:a aac -b:a 192k -ar 48000 "$OUT/$1.mp4"
  echo "$1 listo"
}

seg s1  1-IMG_7248.mov 1.50 6.95
seg s2  2-IMG_7249.mov 0.55 3.00
seg s3  3-IMG_7251.mov 0.80 4.85
seg s4a 4-IMG_7255.mov 0.70 3.00
seg s4b 4-IMG_7255.mov 3.00 8.60
