#!/bin/bash
# Monta los 28 planos en un mp4 mudo de 1080x1920: bash montar.sh
# Los planos 14 y 15 llevan la grabación real de la app (app_planos.py).
cd "/home/user/prueba/socly-video/video/herramientas/ciudad-socly"
FF="/usr/bin/ffmpeg"
rm -f lista.txt
for i in $(seq -w 1 28); do
  n=$(ls planos/s$i 2>/dev/null | wc -l)
  if [ "$n" -lt 75 ]; then echo "FALTA plano $i ($n fotogramas)"; exit 1; fi
  "$FF" -v error -y -framerate 30 -i planos/s$i/f_%04d.png -vf "scale=1080:1920:flags=lanczos" -c:v libx264 -pix_fmt yuv420p -crf 18 planos/s$i.mp4
done
PYTHONUTF8=1 python app_planos.py
for i in $(seq -w 1 28); do
  if [ "$i" = "14" ] || [ "$i" = "15" ]; then echo "file 'planos/s$i-app.mp4'" >> lista.txt; else echo "file 'planos/s$i.mp4'" >> lista.txt; fi
done
"$FF" -v error -y -f concat -safe 0 -i lista.txt -c copy prueba/ciudad-socly-completo.mp4
rm -f lista.txt
ls -la prueba/ciudad-socly-completo.mp4
