#!/bin/bash
# Vídeo «¿Cuál me pongo?»: renderiza cual-me-pongo.html y lo codifica dos veces
# (con el audio de la plantilla y sin audio, para poner el sonido de la propia red social).
# Uso: bash go-cual-me-pongo.sh   (≈3 min)
cd "$(dirname "$0")"
F="/usr/bin/ffmpeg"
OUT="../../anuncios"
DUR=16
rm -rf frames-cual
PAGE=cual-me-pongo.html node render.mjs frames-cual 1.875 0 $DUR 30 2>&1 | tail -2
VF="scale=in_range=pc:out_range=tv,format=yuv420p"
"$F" -v error -y -framerate 30 -i frames-cual/f_%04d.jpg -i ../audio/plantilla-capcut.m4a -t $DUR \
  -vf "$VF" -af "afade=t=in:d=0.3,afade=t=out:st=15.2:d=0.8" \
  -c:v libx264 -crf 17 -preset medium -c:a aac -b:a 160k -shortest "$OUT/cual-me-pongo.mp4"
"$F" -v error -y -framerate 30 -i frames-cual/f_%04d.jpg -t $DUR \
  -vf "$VF" -c:v libx264 -crf 17 -preset medium -an "$OUT/cual-me-pongo-sin-audio.mp4"
rm -rf frames-cual
echo terminado
