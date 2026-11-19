# Uso: bash go.sh   (desde guia/; necesita base.mp4, ../voz-knox.wav y ../datos.js hechos con audio.py)
cd "$(dirname "$0")"
F="/usr/bin/ffmpeg"
END=27.6
rm -rf fr chrome-profile
node render-png.mjs fr 1.875 0 $END 30 2>&1 | tail -2
"$F" -v error -y -i base.mp4 -framerate 30 -i fr/f_%04d.png -i ../voz-knox.wav \
  -filter_complex "[0:v][1:v]overlay=0:0:format=auto,format=yuv420p[v];[2:a]apad,afade=t=out:st=27.0:d=0.6[a]" \
  -map "[v]" -map "[a]" -t $END -c:v libx264 -crf 17 -preset medium -c:a aac -b:a 192k zorro-guia.mp4
mkdir -p ../../../anuncios/zorro-guia && cp zorro-guia.mp4 ../../../anuncios/zorro-guia/zorro-guia.mp4
echo terminado
