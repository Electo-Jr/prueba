import subprocess, os, sys, shutil
D = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
FF = r"/usr/bin/ffmpeg"
TR = r"C:/Users/pm221/.claude/projects/C--Users-pm221-OneDrive-Documentos-ESTILISTA-IA-APP-app-estilista-ia/1d523e8f-d204-47bc-920b-faa4c149ebb0/tool-results/mcp-Claude_Browser-blob-"
SRC = {
    'H1': '1791493911062-90aylf', 'H2': '1791493911062-8inybm', 'H3': '1791493911062-q3z6hj',
    'ARM1': '1791493929014-qongcl', 'ARM2': '1791493929015-blbqqe', 'OUT': '1791493929015-9bljed',
    'MAL': '1791493929015-d09v22', 'EST': '1791493894802-3qb6gw', 'SOC': '1791493894802-oh3v0h',
}
AUDIO = D + '/../ref/ref-audio.m4a'
FONT = "ariblk.ttf"
FONTB = "arialbd.ttf"
W, H, FPS = 576, 1024, 30
OUTFILE = sys.argv[1] if len(sys.argv) > 1 else D + '/final.mp4'
ONLY = sys.argv[2] if len(sys.argv) > 2 else None


def run(args):
    r = subprocess.run([FF, '-v', 'error', '-y'] + args, capture_output=True, text=True, cwd=D)
    if r.returncode:
        print(r.stderr[:900])
        raise SystemExit(1)


ENC = ['-c:v', 'libx264', '-crf', '15', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-r', str(FPS)]

# 1) pantallazos recortados a 576x1024 (la zona util del pantallazo es 491x873)
os.makedirs(D + '/stills', exist_ok=True)
for k, v in SRC.items():
    out = f'{D}/stills/{k}.png'
    vf = f'crop=491:873:0:0,delogo=x=10:y=818:w=48:h=48,scale={W}:{H}:flags=lanczos'
    if k == 'SOC':
        # nombres de otras personas: se difuminan (fila de avatares y "lo que se pone tu gente")
        fcx = ('crop=491:873:0:0,delogo=x=10:y=818:w=48:h=48,split=3[a][b][c];'
               '[b]crop=491:95:0:50,boxblur=14:3[bb];[c]crop=491:170:0:480,boxblur=14:3[cc];'
               f'[a][bb]overlay=0:50[t];[t][cc]overlay=0:480,scale={W}:{H}:flags=lanczos')
        run(['-i', TR + v + '.jpg', '-filter_complex', fcx, '-frames:v', '1', out])
    else:
        run(['-i', TR + v + '.jpg', '-vf', vf, '-frames:v', '1', out])


def still(k):
    return ['-loop', '1', '-framerate', str(FPS), '-i', f'{D}/stills/{k}.png']


def zp(n, z0, z1, fx, fy):
    z = f"{z0}+({z1}-{z0})*on/{max(1, n - 1)}"
    return (f"scale={W*3}:{H*3}:flags=lanczos,zoompan=z='{z}':"
            f"x='(iw-iw/zoom)*{fx}':y='(ih-ih/zoom)*{fy}':d={n}:s={W}x{H}:fps={FPS}")


segs = []


def seg(name, inputs, vf, n, complex_=False):
    path = f'{D}/seg_{name}.mp4'
    args = []
    for i in inputs:
        args += i
    if complex_:
        args += ['-filter_complex', vf, '-map', '[v]']
    else:
        args += ['-vf', vf]
    args += ['-frames:v', str(n)] + ENC + [path]
    run(args)
    segs.append(path)


# 2) intro 0-223 (7,43 s)
N0 = 223
fc = (
    f"[0:v]scale={W*2}:{H*2},boxblur=28:4,eq=brightness=-0.42:saturation=0.8,"
    f"zoompan=z='1.0+0.06*on/{N0}':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d={N0}:s={W}x{H}:fps={FPS}[bg];"
    "[bg][2:v]overlay=x='-60+330*t':y='700-520*t':enable='lt(t,1.4)'[o1];"
    "[o1][3:v]overlay=x='520-380*t':y='250+160*t':enable='between(t,0.1,1.5)'[o2];"
    "[o2][4:v]overlay=x='80+260*t':y='160+430*t':enable='between(t,0.25,1.6)'[o3];"
    "[o3][2:v]overlay=x='460-300*t':y='820-300*t':enable='between(t,0.4,1.7)'[o4];"
    "[o4][4:v]overlay=x='-40+300*t':y='520-110*t':enable='between(t,0.5,1.8)'[o5];"
    "[o5][1:v]overlay=x=38:y=482:enable='gte(t,1.5)'[o6];"
)
txt = 'SOCLY.STYLE'
prev = 'o6'
for i in range(1, len(txt) + 1):
    t0 = 2.4 + 0.19 * (i - 1)
    t1 = 2.4 + 0.19 * i if i < len(txt) else 99
    sub = txt[:i].replace('.', '\\.')
    nxt = f'tx{i}'
    fc += (f"[{prev}]drawtext=fontfile={FONTB}:text='{sub}':fontsize=34:fontcolor=0x111111:x=100:y=500:"
           f"enable='between(t,{t0:.2f},{t1:.2f})'[{nxt}];")
    prev = nxt
fc += (f"[{prev}][5:v]overlay=x='if(lt(t,5.0),600,if(lt(t,6.2),330-(t-5.0)*190,102))':"
       f"y='if(lt(t,5.0),600,if(lt(t,6.2),640-(t-5.0)*110,508))':enable='gte(t,5.0)'[v]")
seg('0', [still('H1'), ['-i', D + '/pill.png'], ['-i', D + '/bar1.png'], ['-i', D + '/bar2.png'],
          ['-i', D + '/bar3.png'], ['-i', D + '/cursor.png']], fc, N0, True)
if ONLY == 'intro':
    shutil.copy(segs[0], OUTFILE)
    raise SystemExit(0)

# 3) destellos 223-292 (8 clips)
flash_cuts = [8, 9, 9, 8, 9, 9, 8, 9]
flash_src = ['H1', 'ARM1', 'OUT', 'EST', 'H2', 'MAL', 'ARM2', 'SOC']
foc = [(0.5, 0.2), (0.3, 0.1), (0.5, 0.3), (0.5, 0.2), (0.6, 0.5), (0.5, 0.3), (0.4, 0.6), (0.5, 0.3)]
for i, (k, n) in enumerate(zip(flash_src, flash_cuts)):
    vf = (zp(n, 1.15, 1.35, *foc[i]) + ",rgbashift=rh=-10:bh=10:gh=0,"
          "eq=brightness='0.22*max(0,1-n/3)':saturation=1.25:eval=frame")
    seg(f'f{i}', [still(k)], vf, n)

# 4) clips largos
clips = [
    ('A', 'H1', 55, 1.00, 1.14, 0.5, 0.35, ',fade=t=in:st=0:d=0.33:color=black'),
    ('B', 'ARM1', 29, 1.05, 1.22, 0.35, 0.15, ''),
    ('C', 'H3', 30, 1.20, 1.00, 0.5, 0.4, ''),
    ('D', 'ARM2', 18, 1.00, 1.25, 0.5, 0.2, ''),
    ('E', 'MAL', 16, 1.25, 1.05, 0.4, 0.2, ''),
    ('F', 'OUT', 8, 1.10, 1.25, 0.5, 0.15, ''),
]
for name, k, n, z0, z1, fx, fy, extra in clips:
    seg(name, [still(k)], zp(n, z0, z1, fx, fy) + extra, n)

# barrido (G): movimiento de cámara. La pantalla desenfocada en horizontal y con un destello cálido
seg('G', [still('H3')],
    zp(11, 1.15, 1.6, 0.5, 0.3) + ",gblur=sigma=70:sigmaV=1,"
    "eq=brightness='0.10+0.10*sin(n/3)':saturation=1.35:contrast=1.05,colorbalance=rs=0.12:bs=-0.12:rm=0.08:bm=-0.08", 11)

# 5) plano final 459-615 (156 fotogramas): tarjeta arriba, degradado a oscuro y la fecha en serif fina
NH = 156
GOLD = '0xC9A178'
ramp = lambda n0, d=12: f"min(1,max(0,(n-{n0})/{d}))"


def label(text, size, font, color, n0, ybase, rise=14, extra=''):
    return (f"drawtext=fontfile={font}:text='{text}':fontsize={size}:fontcolor={color}:"
            f"x=(w-text_w)/2:y='{ybase}+(1-{ramp(n0)})*{rise}':alpha='{ramp(n0)}':"
            f"shadowcolor=black@0.45:shadowx=0:shadowy=3{extra}")


fin = (f"[0:v]{zp(NH, 1.0, 1.06, 0.5, 0.0)},eq=brightness=-0.04[b];[b][1:v]overlay=0:0[g];[g]"
       + label('D I S P O N I B L E   D E S D E   E L', 21, 'seguisb.ttf', GOLD, 45, 676) + ","
       + label('8/10/2026', 90, 'GeorgiaPro-Light.ttf', 'white', 51, 716) + ","
       + f"drawbox=x=258:y=846:w=60:h=2:color={GOLD}@0.9:t=fill:enable='gte(n,62)',"
       + label('S O C L Y   S T Y L E', 22, 'seguisb.ttf', 'white@0.85', 66, 868))
for a in (111, 117, 123, 129, 144, 150):
    fin += f",drawbox=x=0:y={(a*7)%700}:w=576:h=260:color=0xff8a1f@0.5:t=fill:enable='between(n,{a},{a+2})'"
for a in (114, 120, 126, 147):
    fin += f",drawbox=x=0:y=0:w=576:h=1024:color=0xffb347@0.35:t=fill:enable='between(n,{a},{a+1})'"
fin += "[v]"
seg('H', [still('EST'), ['-i', D + '/grad.png']], fin, NH, True)

# 6) negro con anillo (615-629)
fcr = (f"color=c=black:s={W}x{H}:r={FPS}[bk];[bk][0:v]overlay=x=(W-w)/2:y=(H-h)/2-30:format=auto,"
       f"fade=t=in:st=0:d=0.3[v]")
seg('Z', [['-loop', '1', '-framerate', str(FPS), '-i', D + '/ring.png']], fcr, 14, True)

# 7) unir y poner el sonido
lst = D + '/list.txt'
open(lst, 'w').write(''.join(f"file '{p}'\n" for p in segs))
run(['-f', 'concat', '-safe', '0', '-i', lst, '-i', AUDIO, '-map', '0:v', '-map', '1:a',
     '-c:v', 'copy', '-c:a', 'aac', '-b:a', '128k', '-shortest', OUTFILE])
print('listo', OUTFILE)
