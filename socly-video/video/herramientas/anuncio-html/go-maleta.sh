#!/bin/bash
# Vídeo «Maleta de cabina»: renderiza maleta.html y codifica con audio de la plantilla y sin audio.
# Uso: bash go-maleta.sh   (≈3-4 min). Las fotos salen de ..\..\fotos-propias\maleta\procesadas\
cd "$(dirname "$0")"
F="/usr/bin/ffmpeg"
OUT="../../anuncios"
DUR=15.4
rm -rf frames-maleta
PAGE=maleta.html node render.mjs frames-maleta 1.875 0 $DUR 30 2>&1 | tail -2
VF="scale=in_range=pc:out_range=tv,format=yuv420p"
"$F" -v error -y -framerate 30 -i frames-maleta/f_%04d.jpg -i ../audio/plantilla-capcut.m4a -t $DUR \
  -vf "$VF" -af "afade=t=in:d=0.3,afade=t=out:st=14.6:d=0.8" \
  -c:v libx264 -crf 17 -preset medium -c:a aac -b:a 160k -shortest "$OUT/maleta-de-cabina.mp4"
"$F" -v error -y -framerate 30 -i frames-maleta/f_%04d.jpg -t $DUR \
  -vf "$VF" -c:v libx264 -crf 17 -preset medium -an "$OUT/maleta-de-cabina-sin-audio.mp4"
rm -rf frames-maleta
echo terminado
