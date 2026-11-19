#!/bin/bash
# Vídeo «match» con la explicación de ESIC, en cuatro versiones (la explicación al principio, en medio, al final, y al final con una tarjeta «¿Por qué?»).
# Explicación = clip del dueño ante el cartel de ESIC (con el nuestro encima) + clip del socio en la escalera,
# subtitulados al estilo TikTok. Cortes directos; solo hay fundido a negro hacia el cartel final.
# Antes: bash limpiar-esic.sh (clips limpios) y bash go.sh (trozos c1-c3 y cartel en la carpeta de trabajo).
# Desde esta carpeta: bash go-esic.sh   Salida: video\anuncios\match-socly\match-socly-esic-{inicio,medio,final,final-porque}.mp4
set -e
FF="/usr/bin/ffmpeg"
HERE="$(cd "$(dirname "$0")" && pwd)"
CLEAN="$HERE/../../fotos-propias/match/esic/limpio"
OUT="$HERE/../../anuncios/match-socly"
W="/home/user/prueba/socly-video/trabajo/match"
export PYTHONUTF8=1
mkdir -p "$OUT" "$W/esic"
cp /usr/share/fonts/opentype/inter/Inter-Bold.otf "$W/esic/"

python "$HERE/palabras-esic.py" "$W/esic"
echo '{}' > "$W/esic/fix.json"
python "$HERE/../jardin/subtitulos.py" "$W/esic/a.json" "$W/esic/fix.json" "$W/esic/a.ass"
python "$HERE/../jardin/subtitulos.py" "$W/esic/b.json" "$W/esic/fix.json" "$W/esic/b.ass"

# recorta cada clip y le quema los subtítulos; fundidos de 15 ms en el sonido para que los cortes no hagan «clic»
sub() { # nombre entrada inicio fin
  local len
  len=$(python -c "print(round($4-$3-0.015,3))")
  (cd "$W/esic" && "$FF" -y -loglevel error -ss "$3" -to "$4" -i "$CLEAN/$2" -vf "subtitles=$1.ass:fontsdir=.,fps=30,format=yuv420p" \
    -af "afade=t=in:d=0.015,afade=t=out:st=$len:d=0.015" -c:v libx264 -crf 15 -preset medium -c:a aac -b:a 192k -ar 48000 "$W/esic/$1.mp4")
}
sub a 1-cartel-limpio.mp4 0.35 4.10
sub b 2-socio-limpio.mp4  0.55 4.50

# Tarjeta «¿Por qué?» de 1 s sobre negro: puente entre «¿Qué has hecho?» y la explicación
cat > "$W/esic/q.ass" <<'ASS'
[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Q,Arial Black,150,&H004BB8F2,&H00FFFFFF,&H00000000,&H64000000,0,0,0,0,100,100,0,0,1,0,0,5,60,60,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,0:00:01.00,Q,,0,0,0,,{ad(150,150)}¿POR QUÉ?
ASS
(cd "$W/esic" && "$FF" -y -loglevel error -f lavfi -i "color=c=black:s=1080x1920:r=30:d=1" -f lavfi -i "anullsrc=r=48000:cl=stereo" -t 1   -vf "subtitles=q.ass:fontsdir=.,format=yuv420p" -c:v libx264 -crf 15 -c:a aac -b:a 192k -ar 48000 q.mp4)

dur() { "$FF" -i "$1" 2>&1 | grep -m1 Duration | sed 's/.*Duration: \([0-9:.]*\),.*/\1/' | awk -F: '{printf "%.3f", $1*3600+$2*60+$3}'; }

montar() { # nombre orden_de_trozos (c1 c2 c3 a b)
  local name=$1; shift
  local inputs="" vf="" af="" n=0 T=0 d
  for p in "$@"; do
    if [ "$p" = a ] || [ "$p" = b ] || [ "$p" = q ]; then f="$W/esic/$p.mp4"; else f="$W/$p.mp4"; fi
    inputs="$inputs -i $f"
    vf="$vf[$n:v]"; af="$af[$n:a]"
    d=$(dur "$f"); T=$(python -c "print(round($T+$d,3))")
    n=$((n+1))
  done
  local OFF TOTAL
  OFF=$(python -c "print(round($T-0.3,3))")
  TOTAL=$(python -c "print(round($T+2.6-0.3,3))")
  "$FF" -y -loglevel error $inputs -i "$W/fin.mp4" -filter_complex "
${vf}concat=n=$n:v=1:a=0,fps=30,settb=AVTB[vv];
[$n:v]fps=30,settb=AVTB[fv];
[vv][fv]xfade=transition=fadeblack:duration=0.3:offset=$OFF[v];
${af}concat=n=$n:v=0:a=1[ac];
[ac]aformat=channel_layouts=stereo,apad=pad_dur=3,loudnorm=I=-16:TP=-1.5:LRA=11[a]" \
    -map "[v]" -map "[a]" -t "$TOTAL" -c:v libx264 -crf 21 -preset slow -pix_fmt yuv420p -c:a aac -b:a 192k -ar 48000 -movflags +faststart "$OUT/match-socly-esic-$name.mp4"
  echo "listo: match-socly-esic-$name.mp4 ($TOTAL s)"
}

montar inicio a b c1 c2 c3
montar medio  c1 c2 a b c3
montar final  c1 c2 c3 a b
montar final-porque c1 c2 c3 q a b
