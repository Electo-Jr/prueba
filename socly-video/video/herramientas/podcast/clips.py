"""Monta un clip vertical (1080x1920) del podcast de Socly.
Uso: PYTHONUTF8=1 python clips.py <n> [mic]     (n = número de clip de CLIPS; «mic» pone micrófonos decorativos)
Entrada: los .MOV originales (SRC), palabras de `video\\podcast\\medium\\clipN.json` (+ correcciones).
Salida: `video\\podcast\\clips\\clipNN.mp4`.
Estructura: fondo oscuro, título arriba, vídeo cuadrado en el centro (plano abierto con fondo
desenfocado o zoom a quien habla, según `plan`), subtítulos palabra a palabra abajo, efectos de
`video\\podcast\\sonidos\\` mezclados con la voz. HDR (HLG) pasado a color normal."""
import json
import os
import subprocess
import sys

FF = "/usr/bin/ffmpeg"
ROOT = "/home/user/prueba/socly-video/video/podcast"
SRC = "/home/user/prueba/socly-video/trabajo/podcast/"
WORK = "/home/user/prueba/socly-video/trabajo/clipwork"
FONT = "C:/Windows/Fonts/ArialNova-Bold.ttf"

TM = "zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p"
# recortes cuadrados (880x880) sobre el original 1920x1080: izquierda, derecha; «abierto» = plano completo
MICS = "mic" in sys.argv[2:]
CROP = {"L": (110, 200), "R": (900, 200)}

# n: vídeo, inicio, fin, título (2 líneas), plan [(t_inicio_relativo, modo)], efectos [(t_relativo, archivo, vol)],
#    bn = (t0, t1) relativos en blanco y negro (opcional), fix = correcciones de palabras
CLIPS = {
    10: dict(video="IMG_7540", t0=361.4, t1=392.2,
             title=["¿POR QUÉ ELECTO", "ES TAN GUAPO?"],
             plan=[(0, "W"), (1.0, "L"), (8.4, "R"), (22.6, "W"), (25.8, "L")],
             sfx=[(7.0, "bruh-movie", 0.7), (16.2, "rimshot", 0.7)],
             fix={}),
    # extra (2026-11-11, 2.ª tanda): 15 = «el entrevistado viene suelto», 16 = blooper del nombre, 17 = final y salida
    15: dict(video="IMG_7540", t0=19.9, t1=57.3,
             title=["EL ENTREVISTADO", "VIENE SUELTO"],
             cuts=[(32.3, 34.2), (39.8, 43.3), (49.0, 51.5)],
             plan=[(0, "W"), (0.2, "L"), (4.0, "W"), (5.5, "L"), (11.8, "R"), (13.4, "W"), (18.8, "L"), (22.4, "R"),
                   (23.7, "L"), (26.0, "R"), (28.3, "L")],
             sfx=[(11.6, "mario-coin", 0.4), (15.7, "rimshot", 0.6), (28.4, "ding", 0.4)],
             fix={}, fixat={48.24: "buenas", 48.48: "", 48.66: "tardes"}),
    16: dict(video="IMG_7540", t0=276.2, t1=321.8,
             title=["EL NOMBRE DE SOCLY", "Y EL FALLO"],
             cuts=[(302.4, 304.7), (318.6, 320.3)],
             plan=[(0, "W"), (0.2, "L"), (2.6, "R"), (11.2, "L"), (13.0, "R"), (23.2, "W"), (26.4, "L"), (37.6, "W"), (40.1, "L")],
             sfx=[(23.4, "crickets", 0.5), (26.4, "wrong-buzzer", 0.5), (38.2, "sheesh", 0.5), (41.2, "rimshot", 0.6)],
             fix={}, fixat={288.2: "cuéntanos", 309.24: "social,", 310.1: "social", 305.76: "¿No", 305.82: "viene", 306.16: "eso?"}),
    17: dict(video="IMG_7541", t0=304.6, t1=325.0,
             title=["EL FINAL DE", "LA ENTREVISTA"],
             cuts=[(306.6, 309.4), (318.2, 320.7)],
             plan=[(0, "W"), (2.0, "R"), (8.4, "W")],
             sfx=[(1.0, "ding", 0.4), (12.0, "fah", 0.6), (14.7, "rimshot", 0.6)],
             fix={}, fixat={305.81: "fíjate"}),
    # extra (2026-11-11): 13 = «petando en YouTube», 14 = falsos arranques (palabras del Whisper «small» en medium\clip14.json)
    13: dict(video="IMG_7541", t0=21.0, t1=41.0,
             title=["«ESTÁ PETANDO EN", "YOUTUBE Y SPOTIFY»"],
             cuts=[(36.7, 39.5)],
             plan=[(0, "W"), (0.2, "L"), (1.9, "R"), (5.0, "W"), (6.5, "R"), (9.7, "L"), (13.2, "W"), (14.4, "L"), (15.7, "R")],
             sfx=[(5.8, "ding", 0.5), (8.2, "airhorn", 0.4), (15.4, "rimshot", 0.6)],
             fix={}, fixat={29.54: "", 29.66: "", 32.94: "improvisemos", 33.34: ""}),
    14: dict(video="IMG_7541", t0=52.3, t1=70.6,
             title=["COMO NO EMPEZAR", "UNA ENTREVISTA"],
             cuts=[(63.5, 64.6), (65.0, 66.6)],
             plan=[(0, "W"), (0.2, "L"), (2.4, "R"), (2.9, "L"), (5.5, "W"), (7.0, "L"), (9.8, "R"), (11.2, "L"), (13.8, "R"), (14.3, "L")],
             sfx=[(10.1, "bruh-movie", 0.6), (14.1, "rimshot", 0.6)],
             fix={}, fixat={54.71: "Sí", 68.78: "Sí", 62.32: "¡Qué", 62.48: "pesado"}),
    2: dict(video="IMG_7540", t0=112.8, t1=173.2,
            title=["EL DISEÑO DE SOCLY", "Y SUS NOVEDADES"],
            cuts=[(120.4, 121.1), (151.2, 153.2), (163.9, 165.8)],  # pausas (~4,7 s)
            plan=[(0, "W"), (0.2, "L"), (5.2, "R"), (11.0, "W"), (13.0, "R"), (19.0, "W"), (21.0, "R"),
                  (30.0, "W"), (32.0, "R"), (44.0, "W"), (46.0, "R"), (54.2, "L")],
            sfx=[(12.8, "ding", 0.5), (14.8, "ding", 0.4), (17.9, "record-scratch", 0.5), (34.3, "mario-coin", 0.4),
                 (37.3, "ding", 0.6), (40.5, "anime-wow", 0.5), (47.6, "fah", 0.5), (53.2, "ding", 0.5), (54.6, "sheesh", 0.5)],
            fix={}, fixat={113.24: "surgió", 128.3: "Louis", 166.94: "sorpresas,", 167.36: "", 167.66: "", 167.92: "", 169.92: "de activar"}),
    3: dict(video="IMG_7540", t0=174.6, t1=224.9,
            title=["CAMPAÑA SECRETA", "Y UN MONO"],
            cuts=[(187.6, 189.6), (197.8, 199.3), (203.2, 210.7), (216.1, 217.6)],  # silencios (~13 s)
            plan=[(0, "W"), (0.2, "L"), (5.7, "R"), (8.0, "R"), (13.0, "L"), (16.5, "W"), (18.5, "L"), (20.4, "R"),
                  (26.0, "W"), (28.0, "R"), (30.5, "L"), (31.8, "R"), (34.4, "L")],
            bn=(8.0, 13.0),  # blanco y negro en el gag «si quieres te la digo, pero lo cortas»
            sfx=[(8.0, "record-scratch", 0.6), (12.9, "rimshot", 0.7), (29.0, "vine-boom", 0.6), (36.0, "bruh-movie", 0.5)],
            fix={}, fixat={219.78: "", 219.96: "", 219.6: "mono,", 220.88: "oyes."}),
    4: dict(video="IMG_7540", t0=228.8, t1=268.4,
            title=["¿POR QUÉ EL ICONO", "ES UNA PERCHA?"],
            cuts=[(247.15, 249.6), (252.1, 253.5), (255.5, 258.0)],  # silencios del gag del pinganillo (~7 s)
            plan=[(0, "W"), (0.3, "L"), (4.2, "R"), (10.1, "L"), (13.0, "W"), (14.8, "L"), (16.9, "R"),
                  (24.0, "W"), (26.0, "R"), (27.6, "L"), (28.65, "R"), (31.8, "L")],
            sfx=[(11.7, "fah", 0.5), (14.4, "ding", 0.5), (21.0, "oh-no", 0.5), (29.4, "ding", 0.6), (31.9, "sheesh", 0.5)],
            fix={}),
    5: dict(video="IMG_7541", t0=92.5, t1=127.9,
            title=["¿DE DÓNDE VIENE", "EL NOMBRE SOCLY?"],
            plan=[(0, "W"), (0.2, "L"), (3.9, "R"), (12.0, "W"), (14.0, "R"), (29.5, "W"), (31.5, "R")],
            sfx=[(17.4, "ding", 0.5), (22.9, "fah", 0.6), (29.7, "ding", 0.5), (35.0, "rimshot", 0.6)],
            fix={}, fixat={114.74: "Be"}),
    1: dict(video="IMG_7540", t0=69.0, t1=108.6,
            title=["LA CAMPAÑA QUE DIO LA", "VUELTA AL MUNDO"],
            plan=[(0, "W"), (0.2, "L"), (5.5, "R"), (22.4, "L"), (33.4, "R"), (35.4, "L")],
            sfx=[(10.9, "vine-boom", 0.6), (15.6, "bruh-movie", 0.6), (21.3, "mario-coin", 0.4), (32.5, "ding", 0.5), (39.0, "rimshot", 0.6)],
            pop=[dict(img="llados.png", t0=10.9, t1=13.3), dict(img="llados.png", t0=15.5, t1=17.4)],
            fix={}, fixat={80.1: "croissant", 80.64: "with", 81.02: "coffee", 84.68: "Llados", 86.64: "surgió"}),
    6: dict(video="IMG_7540", t0=402.0, t1=437.0,
            title=["MILLONARIOS A LOS", "17 Y 18 AÑOS"],
            plan=[(0, "W"), (0.3, "L"), (8.0, "R"), (17.5, "W"), (19.5, "R"), (23.2, "L")],
            sfx=[(13.9, "vine-boom", 0.6), (14.0, "airhorn", 0.4), (22.7, "sad-trombone", 0.45), (24.0, "airhorn", 0.5),
                 (31.0, "record-scratch", 0.5), (34.0, "rimshot", 0.7)],
            pop=[dict(img="lujo.png", t0=13.9, t1=16.2), dict(img="lambos.png", t0=24.0, t1=26.2)],
            fix={}, fixat={425.66: "llegar", 425.84: "en", 426.98: "a la", 428.0: "a", 430.68: "nos", 435.82: "contaminar"}),
    7: dict(video="IMG_7541", t0=208.2, t1=238.9,
            title=["¿CUÁNTO HAY", "EN EL BOLSILLO?"],
            plan=[(0, "W"), (0.3, "L"), (2.5, "R"), (10.1, "L"), (13.2, "R"), (22.0, "W"), (25.8, "R"), (29.4, "L")],
            sfx=[(16.9, "mario-coin", 0.5), (23.4, "airhorn", 0.5), (23.5, "vine-boom", 0.6), (29.6, "sheesh", 0.5)],
            pop=dict(img="lambos.png", t0=23.4, t1=25.7),
            fix={}),
    8: dict(video="IMG_7541", t0=164.45, t1=195.2,
            title=["¿CUÁNTAS VECES MIRAS", "SOCLY AL DÍA?"],
            plan=[(0, "W"), (1.0, "L"), (2.9, "R"), (8.5, "L"), (14.45, "R"), (22.0, "W"), (24.5, "R")],
            sfx=[(19.0, "ding", 0.5), (29.2, "airhorn", 0.45)],
            fix={"escuelas": "descargas"}),
    # opcionales (el dueño quiso hacerlos antes del 8): 11 = «mi novio Electo», 12 = Bomberos de Benson
    11: dict(video="IMG_7541", t0=72.7, t1=90.4,
             title=["«MI NOVIO ELECTO...»", "PERDÓN"],
             plan=[(0, "W"), (1.0, "L"), (11.1, "R"), (12.0, "L")],
             sfx=[(4.5, "vine-boom", 0.7), (13.1, "record-scratch", 0.6), (17.3, "rimshot", 0.7)],
             fix={"electo": "Electo"}),
    12: dict(video="IMG_7541", t0=276.7, t1=304.0,
             title=["¿DE QUÉ EQUIPO", "ERES?"],
             plan=[(0, "W"), (1.0, "L"), (6.3, "R"), (15.0, "W"), (18.0, "R"), (26.6, "L")],
             sfx=[(8.3, "airhorn", 0.5), (17.6, "sheesh", 0.5), (26.9, "rimshot", 0.7)],
             fix={}),
    9: dict(video="IMG_7541", t0=249.4, t1=270.4,
            title=["¿POR QUÉ PABLO", "VISTE TAN BIEN?"],
            plan=[(0, "W"), (0.8, "L"), (4.2, "R"), (8.8, "W"), (10.8, "L"), (16.0, "W"), (17.6, "L")],
            sfx=[(6.0, "fah", 0.7), (9.8, "ding", 0.5), (19.4, "sheesh", 0.5)],
            fix={}),
}


def run(args):
    r = subprocess.run([FF, "-loglevel", "error", "-y"] + args, capture_output=True, text=True)
    if r.returncode:
        print(r.stderr[-1500:])
        raise SystemExit(1)


def ass_time(t):
    h, rem = divmod(t, 3600)
    m, s = divmod(rem, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"


def build(n):
    c = CLIPS[n]
    os.makedirs(WORK, exist_ok=True)
    os.makedirs(f"{ROOT}/clips", exist_ok=True)
    # tramos conservados (se pueden quitar silencios con c["cuts"] = [(inicio_abs, fin_abs), ...])
    keeps, cur = [], c["t0"]
    for ca, cb in sorted(c.get("cuts", [])):
        if ca > cur:
            keeps.append((cur, ca))
        cur = max(cur, cb)
    if cur < c["t1"]:
        keeps.append((cur, c["t1"]))
    offs, acc = [], 0.0
    for ks, ke in keeps:
        offs.append(acc)
        acc += ke - ks
    dur = round(acc, 2)
    src = f"{SRC}{c['video']}.MOV"

    def s2o(ts):
        for (ks, ke), o in zip(keeps, offs):
            if ks - 0.001 <= ts <= ke + 0.001:
                return o + max(0.0, ts - ks)
        return None
    # 1) segmentos de vídeo cuadrados 1080x1080
    segs = []
    plan = c["plan"] + [(dur, "END")]
    for i in range(len(plan) - 1):
        a, mode = plan[i]
        b = plan[i + 1][0]
        if mode == "W":
            rest = ("split[a][b];[a]crop=1500:920:200:160,scale=1080:662,setsar=1[fg];"
                    "[b]crop=1080:1080:420:0,boxblur=60:8,eq=brightness=-0.4:saturation=0.8,setsar=1[bg];[bg][fg]overlay=0:(H-h)/2")
        else:
            x, y = CROP[mode]
            rest = f"crop=880:880:{x}:{y},scale=1080:1080:flags=lanczos,setsar=1"
        if c.get("bn") and c["bn"][0] <= a < c["bn"][1]:
            rest += ",hue=s=0"
        # partir el tramo donde cambia de trozo conservado
        cuts_at = [o for o in offs[1:] if a < o < b]
        edges = [a] + cuts_at + [b]
        for j in range(len(edges) - 1):
            x0, x1 = edges[j], edges[j + 1]
            k = max(m for m, o in enumerate(offs) if o <= x0 + 1e-6)
            src_t = keeps[k][0] + (x0 - offs[k])
            f = f"{WORK}/c{n}_s{i}_{j}.mp4"
            ins = ["-ss", f"{src_t:.3f}", "-i", src]
            if MICS:
                ins += ["-loop", "1", "-i", f"{ROOT}/../herramientas/podcast/mics.png"]
                graph = f"[0:v]{TM}[t];[t][1:v]overlay=0:0:format=auto,format=yuv420p,{rest}"
            else:
                graph = f"[0:v]{TM},{rest}"
            run(ins + ["-t", f"{x1 - x0:.3f}", "-an", "-r", "30", "-filter_complex", graph,
                       "-c:v", "libx264", "-crf", "16", "-preset", "veryfast", "-pix_fmt", "yuv420p", f])
            segs.append(f)
    with open(f"{WORK}/c{n}_list.txt", "w") as fh:
        fh.write("\n".join(f"file '{s}'" for s in segs))
    run(["-f", "concat", "-safe", "0", "-i", f"{WORK}/c{n}_list.txt", "-c", "copy", f"{WORK}/c{n}_video.mp4"])
    # imagen humorística que salta encima (zoom suave) entre p0 y p1
    pops = c.get("pop")
    if pops:
        pops = pops if isinstance(pops, list) else [pops]
        ins, fcs, last = ["-i", f"{WORK}/c{n}_video.mp4"], [], "[0:v]"
        for i, p in enumerate(pops, start=1):
            ins += ["-loop", "1", "-framerate", "30", "-i", f"{ROOT}/imagenes/{p['img']}"]
            fcs.append(f"[{i}:v]setpts=PTS+{p['t0']}/TB,format=rgba,scale=w='trunc(980*(1+0.14*min(1,max(0,t-{p['t0']})/({p['t1']}-{p['t0']})))/2)*2':h=-2:eval=frame[im{i}]")
            fcs.append(f"{last}[im{i}]overlay=x=(W-w)/2:y=(H-h)/2+8*sin(40*t):enable='between(t,{p['t0']},{p['t1']})':eof_action=pass[o{i}]")
            last = f"[o{i}]"
        run(ins + ["-filter_complex", ";".join(fcs) + f";{last}format=yuv420p[v]",
                   "-map", "[v]", "-t", f"{dur}", "-r", "30", "-c:v", "libx264", "-crf", "16", "-preset", "veryfast", f"{WORK}/c{n}_video_pop.mp4"])
        os.replace(f"{WORK}/c{n}_video_pop.mp4", f"{WORK}/c{n}_video.mp4")

    # 2) subtítulos y título (ASS)
    words = [w for w in json.load(open(f"{ROOT}/medium/clip{n}.json", encoding="utf-8")) if c["t0"] - 0.05 <= w["s"] < c["t1"]]
    for w in words:
        core = w["w"].strip("¿?¡!.,")
        if core.lower() in c["fix"]:
            w["w"] = w["w"].replace(core, c["fix"][core.lower()], 1)
    for t_abs, txt in c.get("fixat", {}).items():  # correcciones por tiempo exacto de la palabra
        for w in words:
            if abs(w["s"] - t_abs) < 0.015:
                core = w["w"].strip("¿?¡!.,")
                if not txt:
                    w["w"] = ""
                elif txt.endswith(("?", "!")):
                    w["w"] = txt  # sustituye la palabra entera, con su puntuación
                else:
                    w["w"] = w["w"].replace(core, txt, 1)
    kept = []
    for w in words:
        S = s2o(w["s"])
        if S is None or not w["w"].strip():
            continue
        w["S"], w["E"] = S, S + (w["e"] - w["s"])
        kept.append(w)
    words = kept
    lines = []
    hdr = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Sub,Arial Nova,74,&H0040E0FF,&H00FFFFFF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,6,0,5,60,60,0,1
Style: Title,Arial Nova,84,&H00F1F4F4,&H00F1F4F4,&H00000000,&H00000000,-1,0,0,0,100,100,2,0,1,0,0,8,40,40,0,1
Style: Tag,Arial Nova,34,&H0090A0A8,&H0090A0A8,&H00000000,&H00000000,-1,0,0,0,100,100,6,0,1,0,0,8,40,40,0,1

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
"""
    lines.append(f"Dialogue: 0,{ass_time(0)},{ass_time(dur)},Tag,,0,0,150,,SOCLY STYLE PODCAST")
    lines.append(f"Dialogue: 0,{ass_time(0)},{ass_time(dur)},Title,,0,0,215,,{c['title'][0]}\\N{c['title'][1]}")
    # grupos de hasta 3 palabras, con la palabra activa resaltada
    groups, cur = [], []
    for w in words:
        cur.append(w)
        if len(cur) == 3 or w["w"].endswith((".", "?", "!")):
            groups.append(cur)
            cur = []
    if cur:
        groups.append(cur)
    for gi, g in enumerate(groups):
        g_start = g[0]["S"]
        g_end = groups[gi + 1][0]["S"] if gi + 1 < len(groups) else min(dur, g[-1]["E"] + 0.4)
        g_end = min(g_end, g[-1]["E"] + 1.0)
        txt = ""
        for w in g:
            k = max(1, round((w["e"] - w["s"]) * 100))
            txt += f"{{\\k{k}}}{w['w']} "
        lines.append(f"Dialogue: 0,{ass_time(max(0, g_start))},{ass_time(g_end)},Sub,,0,0,1530,,{{\\an8}}{txt.strip()}")
    with open(f"{WORK}/c{n}.ass", "w", encoding="utf-8") as fh:
        fh.write(hdr + "\n".join(lines))

    # 3) audio con efectos
    inputs = ["-i", src]
    parts = "".join(f"[0:a:0]atrim=start={ks:.3f}:end={ke:.3f},asetpts=PTS-STARTPTS[p{m}];" for m, (ks, ke) in enumerate(keeps))
    cat = "".join(f"[p{m}]" for m in range(len(keeps)))
    fc = f"{parts}{cat}concat=n={len(keeps)}:v=0:a=1,loudnorm=I=-16:TP=-1.5:LRA=11,volume=1.0[v]"
    labels = "[v]"
    for i, (t, name, vol) in enumerate(c["sfx"]):
        inputs += ["-i", f"{ROOT}/sonidos/{name}.mp3"]
        fc += f";[{i + 1}:a]adelay={int(t * 1000)}|{int(t * 1000)},volume={vol}[e{i}]"
        labels += f"[e{i}]"
    fc += f";{labels}amix=inputs={1 + len(c['sfx'])}:normalize=0:dropout_transition=0,alimiter=limit=0.95[aout]"
    run(inputs + ["-filter_complex", fc, "-map", "[aout]", "-ac", "2", "-ar", "48000", "-c:a", "aac", "-b:a", "192k", f"{WORK}/c{n}_audio.m4a"])

    # 4) composición final: fondo, vídeo en el centro, subtítulos (ass con fuentes de la carpeta)
    os.makedirs(WORK + "/fonts", exist_ok=True)
    if not os.path.exists(WORK + "/fonts/ArialNova-Bold.ttf"):
        import shutil
        shutil.copy(FONT, WORK + "/fonts/ArialNova-Bold.ttf")
    out = f"{ROOT}/clips/clip{n:02d}{'-mic' if MICS else ''}.mp4"
    cwd = os.getcwd()
    os.chdir(WORK)
    try:
        run(["-f", "lavfi", "-i", f"color=c=0x15140F:s=1080x1920:r=30:d={dur}", "-i", f"c{n}_video.mp4", "-i", f"c{n}_audio.m4a",
             "-filter_complex", f"[0][1]overlay=0:420:shortest=1[bg];[bg]ass=c{n}.ass:fontsdir=fonts[v]",
             "-map", "[v]", "-map", "2:a", "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p",
             "-c:a", "copy", "-shortest", "-movflags", "+faststart", out])
    finally:
        os.chdir(cwd)
    print("OK", out, dur, "s")


if __name__ == "__main__":
    build(int(sys.argv[1]))
