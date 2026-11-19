#!/bin/bash
# Subtitula los vídeos del jardín: transcribe con Whisper (local), aplica las correcciones y los quema.
# Desde esta carpeta: bash go-subtitulos.sh jardin|pov   (correcciones en fix-*.json de esta carpeta)
set -e
FF="/usr/bin/ffmpeg"
HERE="$(cd "$(dirname "$0")" && pwd)"
V="$HERE/../../anuncios"
W="/home/user/prueba/socly-video/trabajo/sub"
export PYTHONUTF8=1 HF_HUB_OFFLINE=1
case "$1" in
  jardin) IN="$V/jardin-escenas/jardin-escenas-suave.mp4"; OUT="$V/jardin-escenas/jardin-escenas-suave-subtitulado.mp4" ;;
  pov)    IN="$V/jardin-pov/jardin-pov.mp4";               OUT="$V/jardin-pov/jardin-pov-subtitulado.mp4" ;;
  *) echo "uso: bash go-subtitulos.sh jardin|pov"; exit 1 ;;
esac
mkdir -p "$W"; cp /usr/share/fonts/opentype/inter/Inter-Bold.otf "$W/"
[ -f "$W/$1.json" ] || python "$HERE/transcribir.py" "$IN" "$W/$1.json"
python "$HERE/subtitulos.py" "$W/$1.json" "$HERE/fix-$1.json" "$W/$1.ass"
cd "$W"
"$FF" -y -loglevel error -i "$IN" -vf "subtitles=$1.ass:fontsdir=." -c:v libx264 -crf 20 -preset medium -pix_fmt yuv420p -c:a copy -movflags +faststart "$OUT"
echo "listo: $OUT"
