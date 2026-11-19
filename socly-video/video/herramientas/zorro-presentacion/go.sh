# Uso: bash go.sh <voz.wav> [escala]   (escala 1.875 = 1080x1920; 1.25 = borrador 720p)
cd "$(dirname "$0")"
VOZ="${1:-voz-knox.wav}"
SC="${2:-1.875}"
F="/usr/bin/ffmpeg"
# 1) datos de la voz (boca, subtítulos, efectos)
PYTHONUTF8=1 python audio.py "$VOZ" || exit 1
D=$(node -e "const fs=require('fs');const w={};new Function('window',fs.readFileSync('datos.js','utf8'))(w);console.log((Math.max(w.DATA.dur,w.DATA.words.at(-1).e)+0.9).toFixed(2))")
echo "duración del vídeo: $D s"
# 2) fotogramas
rm -rf frames
node render.mjs frames "$SC" 0 "$D" 30 2>&1 | tail -2
# 3) unir con la voz
OUT="zorro-presentacion.mp4"
"$F" -v error -y -framerate 30 -i frames/f_%04d.jpg -i "$VOZ" -t "$D" -vf "scale=in_range=pc:out_range=tv,format=yuv420p" -af "apad,afade=t=out:st=$(node -e "console.log(($D-0.5).toFixed(2))"):d=0.5" -c:v libx264 -crf 17 -preset medium -c:a aac -b:a 192k -shortest "$OUT"
mkdir -p "../../anuncios/zorro-presentacion" && cp "$OUT" "../../anuncios/zorro-presentacion/$OUT"
echo terminado
