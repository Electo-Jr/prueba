cd "$(dirname "$0")"
F="/usr/bin/ffmpeg"
D=17.0
# 1) voz (si cambia guion.txt: PYTHONUTF8=1 python voz.py guion.txt narracion.wav 1.0 y regenerar datos.js)
PYTHONUTF8=1 python audio.py $D mezcla.wav voz-gemini.wav || exit 1
# 2) fotogramas
rm -rf frames
node render.mjs frames 1.875 0 $D 30 2>&1 | tail -2
# 3) unir
"$F" -v error -y -framerate 30 -i frames/f_%04d.jpg -i mezcla.wav -t $D -vf "scale=in_range=pc:out_range=tv,format=yuv420p" -af "afade=t=out:st=16.0:d=1.0" -c:v libx264 -crf 16 -preset medium -c:a aac -b:a 192k -shortest halloween-publi.mp4
mkdir -p "../../anuncios/halloween-publi" && cp halloween-publi.mp4 "../../anuncios/halloween-publi/halloween-publi.mp4"
echo terminado
