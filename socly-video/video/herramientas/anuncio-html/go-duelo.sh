#!/bin/bash
# Vídeo «Afina tu estilo / Esto o esto»: renderiza duelo.html y lo codifica dos veces
# (con el audio de la plantilla y sin audio, para poner el sonido de la propia red social).
# Uso: bash go-duelo.sh   (≈3 min)
cd "$(dirname "$0")"
F="/usr/bin/ffmpeg"
OUT="../../anuncios"
DUR=15.8
rm -rf frames-duelo
PAGE=duelo.html node render.mjs frames-duelo 1.875 0 $DUR 30 2>&1 | tail -2
VF="scale=in_range=pc:out_range=tv,format=yuv420p"
"$F" -v error -y -framerate 30 -i frames-duelo/f_%04d.jpg -i ../audio/plantilla-capcut.m4a -t $DUR \
  -vf "$VF" -af "afade=t=in:d=0.3,afade=t=out:st=15.0:d=0.8" \
  -c:v libx264 -crf 17 -preset medium -c:a aac -b:a 160k -shortest "$OUT/novedad-afina-tu-estilo.mp4"
"$F" -v error -y -framerate 30 -i frames-duelo/f_%04d.jpg -t $DUR \
  -vf "$VF" -c:v libx264 -crf 17 -preset medium -an "$OUT/novedad-afina-tu-estilo-sin-audio.mp4"
rm -rf frames-duelo
echo terminado
