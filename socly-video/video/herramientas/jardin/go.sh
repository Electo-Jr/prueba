#!/bin/bash
# Une los clips del jardín (en el orden en que se subieron) y pone el móvil grande sobre el jardín final.
# Desde esta carpeta: bash go.sh   (~3 min). Salida: video\anuncios\jardin-escenas\jardin-escenas-$VER.mp4
set -e
FF="/usr/bin/ffmpeg"
HERE="$(cd "$(dirname "$0")" && pwd)"
W="/home/user/prueba/socly-video/trabajo/jardin"
OUT="$HERE/../../anuncios/jardin-escenas"
mkdir -p "$OUT"

# Versión de audio: suave (por defecto) o fuerte. bash go.sh fuerte
VER="${1:-suave}"
cd "$HERE"
case "$VER" in
  suave)  export AF="highpass=f=90,arnndn=m=modelo/bd.rnnn:mix=0.75,equalizer=f=250:t=q:w=1:g=-2,equalizer=f=3500:t=q:w=1:g=2,acompressor=threshold=-24dB:ratio=2.5:attack=15:release=250:makeup=2,aresample=48000" ;;
  fuerte) export AF="highpass=f=110,arnndn=m=modelo/bd.rnnn:mix=1,arnndn=m=modelo/bd.rnnn:mix=0.6,equalizer=f=250:t=q:w=1:g=-3,equalizer=f=3500:t=q:w=1:g=3,acompressor=threshold=-26dB:ratio=3.5:attack=10:release=200:makeup=3,aresample=48000" ;;
esac
W="$W/$VER"; mkdir -p "$W"
FR="$W/../frames"

bash "$HERE/segmentos.sh" "$W"

# 1) móvil con fondo transparente (5,6 s = lo que dura el jardín)
[ -f "$FR/f_0168.png" ] || { rm -rf "$FR"; node "$HERE/render-alpha.mjs" "$FR" 1.875 0 5.6 30; }

# 2) música house suave (generada aquí, sin derechos) para el tramo del móvil
PYTHONUTF8=1 python "$HERE/musica.py" "$W/musica.wav" 5.6

# 3) móvil sobre el jardín; el sonido ambiente se sustituye por la música
"$FF" -y -loglevel error -i "$W/s4b.mp4" -framerate 30 -i "$FR/f_%04d.png" -i "$W/musica.wav"   -filter_complex "[0:v][1:v]overlay=shortest=1:format=auto,format=yuv420p[v];[2:a]volume=0.17[a]" -map "[v]" -map "[a]"   -c:v libx264 -crf 16 -preset medium -c:a aac -b:a 192k -ar 48000 -t 5.6 "$W/s4bm.mp4"

# 4) unir en orden y nivelar el volumen
"$FF" -y -loglevel error -i "$W/s1.mp4" -i "$W/s2.mp4" -i "$W/s3.mp4" -i "$W/s4a.mp4" -i "$W/s4bm.mp4" \
  -filter_complex "[0:v][0:a][1:v][1:a][2:v][2:a][3:v][3:a][4:v][4:a]concat=n=5:v=1:a=1[v][a0];[a0]loudnorm=I=-16:TP=-1.5:LRA=11[a]" \
  -map "[v]" -map "[a]" -c:v libx264 -crf 17 -preset slow -pix_fmt yuv420p -c:a aac -b:a 192k -ar 48000 -movflags +faststart "$OUT/jardin-escenas-$VER.mp4"
echo "listo: $OUT/jardin-escenas-$VER.mp4"
