cd "$(dirname "$0")"
F="/usr/bin/ffmpeg"
rm -rf frames
node render.mjs frames 1.875 0 24.9 30 2>&1 | tail -2
"$F" -v error -y -framerate 30 -i frames/f_%04d.jpg -i ../audio/plantilla-capcut.m4a -t 24.9 -vf "scale=in_range=pc:out_range=tv,format=yuv420p" -af "afade=t=in:d=0.4,afade=t=out:st=24.2:d=0.7" -c:v libx264 -crf 16 -preset medium -c:a aac -b:a 160k -shortest ad.mp4
mkdir -p "/home/user/prueba/socly-video/video/anuncios"
cp ad.mp4 "/home/user/prueba/socly-video/video/anuncios/anuncio-socly-app.mp4"
echo terminado
