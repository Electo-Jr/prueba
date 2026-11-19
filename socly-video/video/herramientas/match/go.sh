#!/bin/bash
# Vídeo del cartel «match»: salida por el tobogán -> llegada abajo -> pega el cartel a un desconocido
# -> su mano tapa la cámara, negro y sale el cartel. Vertical 1080x1920, 30 fps.
# Entre escenas, corte directo (sin transiciones); solo hay fundido en el negro de la mano hacia el cartel.
# Desde esta carpeta: bash go.sh   Salida: video\anuncios\match-socly\match-socly.mp4 (+ -sin-audio.mp4)
set -e
FF="/usr/bin/ffmpeg"
HERE="$(cd "$(dirname "$0")" && pwd)"
SRC="$HERE/../../fotos-propias/match"
OUT="$HERE/../../anuncios/match-socly"
W="/home/user/prueba/socly-video/trabajo/match"
mkdir -p "$OUT" "$W"
cd "$HERE/../jardin"   # el modelo de ruido está en herramientas\jardin\modelo

# Pantalla final: el cartel centrado sobre su propio fondo desenfocado
"$FF" -y -loglevel error -loop 1 -framerate 30 -t 2.6 -i "$SRC/cartel-match.png" -filter_complex \
  "[0:v]split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=45:6,eq=brightness=-0.12[bg];[b]scale=1080:-2[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2,format=yuv420p,fps=30[v]" \
  -map "[v]" -an -c:v libx264 -crf 14 "$W/fin.mp4"

# HDR del iPhone (4K) a SDR 1080x1920; los clips de 576x1024 se escalan con un poco de nitidez
HDR="zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p,scale=1080:1920:flags=lanczos,fps=30"
SDR="scale=1080:1920:flags=lanczos,unsharp=5:5:0.6,fps=30,format=yuv420p"
# ruido reducido; fundidos de 15 ms en los extremos de cada escena para que los cortes directos no hagan «clic»
AF="highpass=f=80,arnndn=m=modelo/bd.rnnn:mix=0.6,aresample=48000"

seg() { # nombre entrada inicio fin filtro_de_vídeo
  local len
  len=$(python -c "print(round($4-$3-0.015,3))")
  "$FF" -y -loglevel error -ss "$3" -to "$4" -i "$SRC/original/$2" -vf "$5" -af "$AF,afade=t=in:d=0.015,afade=t=out:st=$len:d=0.015" -c:v libx264 -crf 15 -preset medium -c:a aac -b:a 192k -ar 48000 "$W/$1.mp4"
}
seg c1 1-IMG_3605.mov 1.95 4.55 "$HDR"      # sin la cuenta atrás (es un aviso para la gente de alrededor): empieza al bajar por el tobogán
seg c2 2-escena.mov   1.25 3.47 "$SDR"      # el tobogán vacío y él llegando abajo
seg c3 3-escena.mov   0.50 6.05 "$SDR"      # pega el cartel, «¿Qué has hecho?» y acaba cuando su mano tapa la cámara

# Duración real de lo ya unido (para que el fundido al cartel caiga justo al final)
dur() { "$FF" -i "$1" 2>&1 | grep -m1 Duration | sed 's/.*Duration: \([0-9:.]*\),.*/\1/' | awk -F: '{printf "%.3f", $1*3600+$2*60+$3}'; }
T=$(python -c "print(round($(dur "$W/c1.mp4")+$(dur "$W/c2.mp4")+$(dur "$W/c3.mp4"),3))")
OFF=$(python -c "print(round($T-0.3,3))")
TOTAL=$(python -c "print(round($T+2.6-0.3,3))")

"$FF" -y -loglevel error -i "$W/c1.mp4" -i "$W/c2.mp4" -i "$W/c3.mp4" -i "$W/fin.mp4" -filter_complex "
[0:v][1:v][2:v]concat=n=3:v=1:a=0,fps=30,settb=AVTB[vv];
[3:v]fps=30,settb=AVTB[fv];
[vv][fv]xfade=transition=fadeblack:duration=0.3:offset=$OFF[v];
[0:a][1:a][2:a]concat=n=3:v=0:a=1[ac];
[ac]apad=pad_dur=3,loudnorm=I=-16:TP=-1.5:LRA=11[a]" \
  -map "[v]" -map "[a]" -t "$TOTAL" -c:v libx264 -crf 21 -preset slow -pix_fmt yuv420p -c:a aac -b:a 192k -ar 48000 -movflags +faststart "$OUT/match-socly.mp4"

# Sin audio, para poner el sonido de la propia red
"$FF" -y -loglevel error -i "$OUT/match-socly.mp4" -an -c:v copy "$OUT/match-socly-sin-audio.mp4"
echo "listo: $OUT/match-socly.mp4 ($TOTAL s)"
