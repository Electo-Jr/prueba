#!/bin/bash
# Segundo vídeo del jardín (clips IMG_7256 e IMG_7257, grabados desde arriba): los une en orden,
# pasa el HDR del iPhone a SDR, limpia el ruido (versión «suave») y nivela el volumen. Sin añadidos.
# Desde esta carpeta: bash go-pov.sh   Salida: video\anuncios\jardin-pov\jardin-pov.mp4
set -e
FF="/usr/bin/ffmpeg"
HERE="$(cd "$(dirname "$0")" && pwd)"
SRC="$HERE/../../fotos-propias/jardin2/original"
W="/home/user/prueba/socly-video/trabajo/jardin-pov"
OUT="$HERE/../../anuncios/jardin-pov"
mkdir -p "$W" "$OUT"
cd "$HERE"

VF="zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p,scale=1080:1920,fps=30"
AF="highpass=f=90,arnndn=m=modelo/bd.rnnn:mix=0.75,equalizer=f=250:t=q:w=1:g=-2,equalizer=f=3500:t=q:w=1:g=2,acompressor=threshold=-24dB:ratio=2.5:attack=15:release=250:makeup=2,aresample=48000"

seg() { # nombre entrada inicio fin
  "$FF" -y -loglevel error -ss "$3" -to "$4" -i "$SRC/$2" -vf "$VF" -af "$AF" \
    -c:v libx264 -crf 20 -preset medium -pix_fmt yuv420p -c:a aac -b:a 192k -ar 48000 "$W/$1.mp4"
}
seg p1 1-IMG_7256.mov 2.00 20.35   # sin el inicio en el que se prepara la cámara apuntando al suelo
seg p2 2-IMG_7257.mov 0.30 8.70    # sin el final en el que el móvil se cae hacia el suelo

"$FF" -y -loglevel error -i "$W/p1.mp4" -i "$W/p2.mp4" \
  -filter_complex "[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[v][a0];[a0]loudnorm=I=-16:TP=-1.5:LRA=11[a]" \
  -map "[v]" -map "[a]" -c:v libx264 -crf 22 -preset slow -pix_fmt yuv420p -c:a aac -b:a 192k -ar 48000 -movflags +faststart "$OUT/jardin-pov.mp4"
echo "listo: $OUT/jardin-pov.mp4"
