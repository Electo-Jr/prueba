#!/bin/bash
# Vídeo «el motor aprende tu estilo» (swipe y duelos): une los 4 clips en el orden en que se subieron,
# HDR del iPhone a SDR, ruido limpiado («suave»), cortes directos, y en la escena 3 pone la grabación de
# pantalla del swipe (en pequeño, mientras gira los dedos) y las dos tarjetas del duelo sobre sus manos.
# Con y sin subtítulos (estilo TikTok, palabra dicha en dorado).
# Desde esta carpeta: bash go.sh   Salida: video\anuncios\estilo-swipe\estilo-swipe[-subtitulado].mp4
set -e
FF="/usr/bin/ffmpeg"
HERE="$(cd "$(dirname "$0")" && pwd)"
SRC="$HERE/../../fotos-propias/estilo-swipe"
OUT="$HERE/../../anuncios/estilo-swipe"
W="/home/user/prueba/socly-video/trabajo/estilo-swipe"
export PYTHONUTF8=1
mkdir -p "$OUT" "$W"

VF="zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p,scale=1080:1920:flags=lanczos,fps=30"
AF="highpass=f=90,arnndn=m=modelo/bd.rnnn:mix=0.75,equalizer=f=250:t=q:w=1:g=-2,equalizer=f=3500:t=q:w=1:g=2,acompressor=threshold=-24dB:ratio=2.5:attack=15:release=250:makeup=2,aresample=48000"

# 1) los cuatro clips (recortes: sin el silencio de antes y de después de hablar)
seg() { # nombre entrada inicio fin
  local len
  len=$(python -c "print(round($4-$3-0.015,3))")
  (cd "$HERE/../jardin" && "$FF" -y -loglevel error -ss "$3" -to "$4" -i "$SRC/original/$2" -vf "$VF" \
    -af "$AF,afade=t=in:d=0.015,afade=t=out:st=$len:d=0.015" \
    -c:v libx264 -crf 15 -preset medium -pix_fmt yuv420p -c:a aac -b:a 192k -ar 48000 "$W/$1.mp4")
}
seg s1 1-IMG_7340.mov 0.00 5.85
seg s2 2-IMG_7352.mov 0.55 5.60
seg s3 3-IMG_7349.mov 0.00 14.10   # sin recortar el principio: los tiempos de las tarjetas son los del clip
seg s4 4-IMG_7364.mov 0.00 5.54

# 2) la grabación de pantalla: 2,4 s del swipe sin la barra de arriba (hora y punto rojo de grabar)
rm -rf "$W/rec" && mkdir -p "$W/rec"
"$FF" -y -loglevel error -ss 0.6 -t 2.4 -i "$SRC/original/pantalla-swipe.mov" \
  -vf "crop=1170:2412:0:120,scale=360:-2:flags=lanczos,fps=30" -q:v 2 "$W/rec/r_%03d.jpg"

# 3) fotogramas transparentes: móvil del swipe (7,45-10,05 s) y tarjetas del duelo (11,35-14,0 s)
node "$HERE/render-overlays.mjs" "$W/ov-swipe" "$W/rec" 7.45 10.05 30
node "$HERE/render-overlays.mjs" "$W/ov-duelo" "$W/rec" 11.35 14.0 30

# 4) subtítulos
python "$HERE/palabras.py" "$W/palabras.json"
echo '{}' > "$W/fix.json"
python "$HERE/../jardin/subtitulos.py" "$W/palabras.json" "$W/fix.json" "$W/estilo-swipe.ass"
cp C:/Windows/Fonts/ariblk.ttf "$W/"

# 5) montaje: overlays sobre la escena 3, cortes directos, volumen nivelado
montar() { # salida con_subtitulos(0|1)
  local sub=""
  [ "$2" = 1 ] && sub=",subtitles=estilo-swipe.ass:fontsdir=."
  (cd "$W" && "$FF" -y -loglevel error -i s1.mp4 -i s2.mp4 -i s3.mp4 -i s4.mp4 \
    -itsoffset 7.45 -framerate 30 -i ov-swipe/s_%04d.png -itsoffset 11.35 -framerate 30 -i ov-duelo/s_%04d.png \
    -filter_complex "[2:v][4:v]overlay=eof_action=pass:format=auto[a];[a][5:v]overlay=eof_action=pass:format=auto[s3o];
[0:v][0:a][1:v][1:a][s3o][2:a][3:v][3:a]concat=n=4:v=1:a=1[v0][a0];
[v0]format=yuv420p${sub}[v];[a0]loudnorm=I=-16:TP=-1.5:LRA=11[a]" \
    -map "[v]" -map "[a]" -c:v libx264 -crf 16 -preset slow -pix_fmt yuv420p -c:a aac -b:a 192k -ar 48000 -movflags +faststart "$1")
  echo "listo: $1"
}
montar "$OUT/estilo-swipe.mp4" 0
montar "$OUT/estilo-swipe-subtitulado.mp4" 1
