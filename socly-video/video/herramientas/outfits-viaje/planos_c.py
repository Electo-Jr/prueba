"""Fase 6: planos 23-34 de «¿De dónde vienen los outfits?» (años 60, 2010, vuelta a casa y cierre). 75 fotogramas por plano.
  blender -b --python planos_c.py -- 23 34
  SOCLY_FRAMES=40 blender -b --python planos_c.py -- 23 34   (solo ese fotograma de cada plano, a prueba\\pNN_f40.png)"""
import sys, time
HERE = r"/home/user/prueba/socly-video\video\herramientas\outfits-viaje"
exec(open(r"/home/user/prueba/socly-video\video\herramientas\ciudad-socly\lib.py", encoding="utf-8").read())
exec(open(HERE + r"\trajes.py", encoding="utf-8").read())
exec(open(HERE + r"\base.py", encoding="utf-8").read())
exec(open(HERE + r"\base_b.py", encoding="utf-8").read())
exec(open(HERE + r"\base_c.py", encoding="utf-8").read())
N = 75
PLANOS = HERE + r"\planos"


def entrada(ctx, cam):
    d = Destello(ctx, cam); return lambda f: d.set(max(0.0, 1 - f / 10.0))


def salida_blanca(ctx, cam):
    d = Destello(ctx, cam); return lambda f: d.set(max(0.0, (f - 62) / 12.0))


def bobs(gs, t, a=0.04):
    for i, g in enumerate(gs): bob(g, t, 0, a, 3, i)


def cam_std(ctx, y0=-15.0, y1=-12.5, z=3.8, x=0.0, foco=None):
    return cam_rig(ctx, ((x, y0, z), (88, 0, 0), 50), ((x, y1, z - 0.1), (88, 0, 0), 50), foco=foco)


# ------------------------------------------------------------------ años 60
def p23(ctx):  # años 60: calle colorida con coches pequeños
    calle60_decor(ctx); car(ctx, (-3.5, 17, 0), "#E3873F", rad(5)); car(ctx, (3.6, 23, 0), "#2E9E5B", rad(-4))
    s = era(ctx, "Soclo", "60s", (-0.9, 0, 0), rad(8), "happy")
    gente = [chica60(ctx, "C1", (2.2, 6.0, 0), rad(-10), "#FFE500", skin=S[2]), era(ctx, "H1", "60s", (-3.0, 9.5, 0), rad(10), "happy", skin=S[3], tela="#2E9E5B"),
             chica60(ctx, "C2", (0.8, 12.0, 0), rad(5), "#FF2E88", skin=S[1], pelo="#7A4A22")]
    for sx, y in ((-1, 8.0), (1, 14.0)):  # símbolos de paz en la calle
        cyl(ctx, "paz", (sx * 6.2, y, 2.4), 1.0, 0.12, "#FFFFFF", 0.4, 0.8, rot=(rad(90), 0, 0)); cyl(ctx, "paz hueco", (sx * 6.2, y - 0.05, 2.4), 0.8, 0.12, "#7AC7B8", 0.4, 0.3, rot=(rad(90), 0, 0))
        box(ctx, "paz v", (sx * 6.2, y - 0.1, 2.4), (0.12, 0.05, 1.5), "#FFFFFF", 0.4, 0.8); box(ctx, "paz d", (sx * 6.2 + 0.3, y - 0.1, 2.0), (0.12, 0.05, 0.9), "#FFFFFF", 0.4, 0.8, rot=(0, rad(35), 0))
    cam, up = cam_std(ctx, foco=(-0.9, 0, 3.5)); fl = entrada(ctx, cam)
    def upd(f, t, u):
        up(u); bobs([s] + gente, t); fl(f)
    return upd


def p24(ctx):  # un grupo de jóvenes con ropa distinta posando; la cámara gira un poco
    calle60_decor(ctx)
    g = [era(ctx, "A", "60s", (-2.2, 4.0, 0), rad(15), "happy", skin=S[1]), chica60(ctx, "B", (-0.7, 2.0, 0), rad(5), "#2E9E5B", skin=S[2]),
         era(ctx, "Cc", "60s", (1.0, 3.0, 0), rad(-10), "happy", skin=S[3], tela="#6B2D8A"), chica60(ctx, "D", (2.5, 1.5, 0), rad(-15), "#FF7A00", skin=S[0], pelo="#C9803A"),
         era(ctx, "E", "60s", (-0.2, 6.0, 0), 0, "happy", skin=S[0], tela="#18B7D9")]
    cam, up = cam_rig(ctx, ((-2.4, -13, 3.9), (88, 0, 0), 50), ((1.4, -11, 3.9), (88, 0, 0), 50), foco=(0.3, 3.0, 3.5))
    notas = [box(ctx, "nota", (0, 0, 0), (0.25, 0.1, 0.25), "#FFE27A", 0.4, 3) for _ in range(4)]
    def upd(f, t, u):
        up(u, look=(0.3, 3.0, 3.4))
        for i, p in enumerate(g): bob(p, t, 0, 0.12, 5, i * 1.3); brazo(p, "d", 40 + 30 * abs(math.sin(t * 4 + i)))
        for i, n in enumerate(notas):
            ph = (t * 0.9 + i / 4) % 1.0; n.location = (-3 + 2 * i + math.sin(ph * 6), 1.0, 5 + 3 * ph); n.scale = (0.5 + 0.8 * math.sin(ph * math.pi),) * 3
    return upd


def p25(ctx):  # un fotógrafo de calle retrata a alguien; destello con foto que sale volando; salto
    calle60_decor(ctx)
    ft = era(ctx, "Fotografo", "2010", (-1.3, 0.5, 0), math.pi, "happy", skin=S[0], tela="#2B2B33")
    sujeto = chica60(ctx, "Modelo", (1.2, 6.5, 0), 0, "#FF2E88", skin=S[2])
    cam_b = box(ctx, "camara foto", (0, 0, 0), (0.9, 0.5, 0.6), "#15140F", 0.4)
    obj = cyl(ctx, "objetivo", (0, 0, 0), 0.28, 0.5, "#3A3F4A", 0.3, rot=(rad(90), 0, 0))
    destello = estrella(ctx, (0, 0, 0), 1.0, "#FFFFFF", 9)
    foto = empty(ctx, "polaroid", (0, 0, 0)); box(ctx, "marco foto", (0, 0, 0), (0.9, 0.06, 1.1), "#FFFFFF", 0.6, 0.3, parent=foto); box(ctx, "imagen foto", (0, -0.04, 0.12), (0.7, 0.04, 0.7), "#FF8FB5", 0.6, 0.6, parent=foto)
    cam, up = cam_std(ctx, -14, -11.5, 3.9, foco=(1.2, 6.5, 3.5)); salida = salida_blanca(ctx, cam); flash_cam = Destello(ctx, cam)
    def upd(f, t, u):
        up(u); bob(sujeto, t, 0, 0.05, 3); brazo("Modelo", "d", 50 + 20 * math.sin(t * 3))
        cam_b.location = (ft.location.x, ft.location.y + 1.0, 4.0); obj.location = (ft.location.x, ft.location.y + 1.5, 4.0)
        destello.location = (ft.location.x, ft.location.y + 2.0, 4.0); destello.scale = ((1.0 + 2.0 * (f - 28) / 4.0) if 28 <= f <= 32 else 0.001,) * 3
        flash_cam.set(0.55 if 28 <= f <= 30 else 0.0)
        q = max(0.0, (f - 32) / 28.0)
        foto.location = (lerp(ft.location.x, 2.6, smooth(q)), lerp(ft.location.y + 1.5, -5.0, q), 4.0 + 2.0 * math.sin(q * math.pi)) if f > 31 else (0, 0, -20)
        foto.rotation_euler.z = q * 7.0; salida(f)
    return upd


# ------------------------------------------------------------------ 2010
def p26(ctx):  # 2010: calle moderna, gente con móvil y corazones; Soclo con sudadera
    calle2010_decor(ctx)
    s = era(ctx, "Soclo", "2010", (-0.9, 0, 0), rad(8), "happy")
    gente = [era(ctx, "G1", "2010", (2.3, 6.0, 0), rad(-10), "neutral", skin=S[2], tela="#C0593B"), era(ctx, "G2", "2010", (-3.0, 9.5, 0), rad(10), "happy", skin=S[3], tela="#2F5D50"),
             era(ctx, "G3", "2010", (1.0, 12.0, 0), rad(3), "neutral", skin=S[0], tela="#3B4A63")]
    cor = [corazon(ctx, (0, 0, 0), 0.6) for _ in range(6)]
    cam, up = cam_std(ctx, foco=(-0.9, 0, 3.5)); fl = entrada(ctx, cam)
    bases = [(-0.2, 0.0), (2.9, 5.0), (-3.4, 8.5), (1.3, 11.0), (0.6, -0.5), (3.4, 6.0)]
    def upd(f, t, u):
        up(u); bobs([s] + gente, t); fl(f)
        for i, c in enumerate(cor):
            ph = (t * 0.7 + i / 6) % 1.0
            c.location = (bases[i][0] + 0.3 * math.sin(ph * 7), bases[i][1] - 1.0, 4.4 + 2.2 * ph); c.scale = (0.3 + 0.8 * math.sin(ph * math.pi),) * 3
    return upd


def p27(ctx):  # alguien se hace una foto de cuerpo entero frente al espejo (con reflejo)
    fondo(ctx, "#E8E4DA", 0.9)
    box(ctx, "Suelo", (0, 5, -0.2), (40, 30, 0.4), "#B9B2A3", 0.6)
    box(ctx, "Pared", (0, 16, 6), (40, 0.4, 12), "#F2EEE6", 0.9)
    for pos, size in (((0, 10.4, 7.95), (4.2, 0.3, 0.25)), ((0, 10.4, 0.05), (4.2, 0.3, 0.25)), ((-1.98, 10.4, 4.0), (0.25, 0.3, 7.6)), ((1.98, 10.4, 4.0), (0.25, 0.3, 7.6))):
        box(ctx, "Marco espejo", pos, size, "#4A3524", 0.7, bevel=True)
    box(ctx, "Fondo espejo", (0, 15.0, 4.0), (3.7, 0.1, 7.1), "#DCE9F2", 0.4, 0.5)
    luz(ctx, "Frente", 'AREA', (0, -12, 7), 3500, "#FFFFFF", rot=(80, 0, 0), size=14); luz(ctx, "Sol", 'SUN', (10, -10, 25), 2.2, "#FFF6E0", rot=(55, 0, 20))
    p = era(ctx, "Foto", "2010", (2.6, 5.5, 0), math.pi + 0.45, "happy", skin=S[1], tela="#6B7A8F")
    refl = era(ctx, "Reflejo", "2010", (0, 13.9, 0), 0, "happy", skin=S[1], tela="#6B7A8F")
    translucido(ctx, "cristal", (0, 10.3, 4.0), 3.7, 7.1, "#CFE6F5", 0.18, emision=3)
    marco = [box(ctx, "visor", pos, size, "#FFFFFF", 0.4, 3) for pos, size in
             (((0.6, 5.0, 8.4), (5.7, 0.05, 0.1)), ((0.6, 5.0, -0.1), (5.7, 0.05, 0.1)), ((-2.2, 5.0, 4.15), (0.1, 0.05, 8.6)), ((3.4, 5.0, 4.15), (0.1, 0.05, 8.6)))]
    for k in (-0.6, 0.6):  # cuadrícula del visor
        box(ctx, "rejilla v", (0.6 + k * 1.6, 5.0, 4.15), (0.04, 0.05, 8.6), "#FFFFFF", 0.4, 1.2); box(ctx, "rejilla h", (0.6, 5.0, 4.15 + k * 3), (5.7, 0.05, 0.04), "#FFFFFF", 0.4, 1.2)
    cyl(ctx, "disparador", (0.6, 5.0, 0.6), 0.32, 0.1, "#FFFFFF", 0.4, 2.5, rot=(rad(90), 0, 0)); cyl(ctx, "disparador aro", (0.6, 5.02, 0.6), 0.42, 0.08, "#15140F", 0.4, rot=(rad(90), 0, 0))
    est = [estrella(ctx, q, 0.35) for q in ((-2.0, 5.0, 8.6), (3.4, 5.0, 8.0))]
    cam, up = cam_rig(ctx, ((0.6, -15, 4.2), (88, 0, 0), 50), ((0.6, -12.5, 4.1), (88, 0, 0), 50), foco=(2.6, 5.5, 3.5)); dfl = Destello(ctx, cam)
    def upd(f, t, u):
        up(u); bob(p, t, 0, 0.04, 3); bob(refl, t, 0, 0.04, 3); brazo("Foto", "i", 120); brazo("Reflejo", "i", 120)
        for o in marco: o.scale = (1 + 0.04 * math.sin(t * 8),) * 3
        for i, e in enumerate(est): e.scale = (0.2 + 0.7 * abs(math.sin(t * 5 + i)),) * 3
        dfl.set(0.5 if 40 <= f <= 42 else 0.0)
    return upd


def p28(ctx):  # la foto en el móvil con #OOTD, «me gusta» que suben y corazones; salto
    fondo(ctx, "#1F2A3A", 0.8)
    box(ctx, "Suelo", (0, 5, -0.25), (60, 40, 0.5), "#2C3E50", 0.5)
    luz(ctx, "Frente", 'AREA', (0, -12, 7), 3000, "#FFFFFF", rot=(80, 0, 0), size=14)
    box(ctx, "movil", (0, 6.0, 4.0), (3.8, 0.35, 7.0), "#15140F", 0.3, bevel=True)
    box(ctx, "pantalla", (0, 5.8, 4.0), (3.4, 0.05, 6.5), "#F4F1EA", 0.4, 0.6)
    cyl(ctx, "avatar", (-1.15, 5.74, 6.7), 0.22, 0.04, "#E3873F", 0.5, 0.5, rot=(rad(90), 0, 0))
    box(ctx, "nombre", (0.0, 5.74, 6.75), (1.4, 0.03, 0.14), "#6B665A", 0.6); box(ctx, "nombre2", (-0.2, 5.74, 6.5), (0.9, 0.03, 0.1), "#B8B2A3", 0.6)
    box(ctx, "foto cuerpo", (0, 5.76, 4.7), (2.8, 0.04, 3.6), "#B9D8EE", 0.5, 0.4)
    box(ctx, "mini cabeza", (0, 5.72, 5.9), (0.5, 0.05, 0.5), "#F0CFA8", 0.6); box(ctx, "mini torso", (0, 5.72, 5.1), (1.0, 0.05, 1.2), "#6B7A8F", 0.8); box(ctx, "mini piernas", (0, 5.72, 3.95), (0.75, 0.05, 1.2), "#1F2A4D", 0.8)
    box(ctx, "corazon base", (-1.2, 5.74, 2.55), (0.3, 0.03, 0.3), "#FF2E88", 0.5, 1.5, rot=(0, rad(45), 0))
    me = text(ctx, "likes", "12", (-0.2, 5.7, 2.55), 0.5, "#15140F", emit=0.1, extrude=0.02)
    box(ctx, "comentario", (0.4, 5.74, 1.6), (2.2, 0.03, 0.1), "#B8B2A3", 0.6); box(ctx, "comentario2", (0.1, 5.74, 1.3), (1.7, 0.03, 0.1), "#B8B2A3", 0.6)
    texto = text(ctx, "OOTD", "#OOTD", (0, 5.5, 8.2), 1.5, "#FFE27A", emit=3.5, extrude=0.3)
    cor = [corazon(ctx, (-1.6 + 0.8 * i, 5.5, 2.0), 0.9, ["#FF2E88", "#FF5A5A", "#FF2E88"][i % 3]) for i in range(5)]
    cam, up = cam_rig(ctx, ((0, -12, 4.6), (89, 0, 0), 50), ((0, -10.2, 4.5), (89, 0, 0), 50), foco=(0, 5.8, 4.0)); fl = salida_blanca(ctx, cam)
    def upd(f, t, u):
        up(u); k = min(1.0, t / 0.45)
        texto.location.z = 8.2 + 3.0 * (1 - k) ** 2; texto.scale = (0.2 + 0.8 * smooth(k),) * 3
        me.data.body = "{:,}".format(int(12 + 1830 * smooth(min(1.0, u * 1.3)) ** 2)).replace(",", ".")
        for i, c in enumerate(cor):
            ph = (t * 0.8 + i / 5) % 1.0; c.location = (-1.8 + 0.9 * i + 0.3 * math.sin(ph * 6), 5.4, 1.5 + 6.0 * ph); c.scale = (0.4 + 0.7 * math.sin(ph * math.pi),) * 3
        fl(f)
    return upd


# ------------------------------------------------------------------ vuelta a casa
def p29(ctx):  # Soclo sale del armario mareado, entre rayos de luz y polvo
    casa_decor(ctx, 5.6); _, g = armario(ctx, (0, 4.2, 0), 0, glow=40)
    s = era(ctx, "Soclo", "casa", (0, 3.6, 0), 0, "shock")
    rayos = [translucido(ctx, "rayo", (0, 4.5, 4.6), 0.5, 10.0, "#FFF6D0", 0.18, rot=(0, rad(-80 + i * 20), 0), emision=8)[1] for i in range(9)]
    rnd = random.Random(9)
    polvo = [box(ctx, "polvo", (rnd.uniform(-3, 3), rnd.uniform(0, 3), rnd.uniform(1, 8)), (0.09, 0.09, 0.09), "#FFFFFF", 0.5, 2.0) for _ in range(16)]
    est = [estrella(ctx, (0, 0, 0), 0.3, "#FFE27A") for _ in range(3)]
    cam, up = cam_rig(ctx, ((0, -13, 5.0), (85, 0, 0), 40), ((0, -11, 4.7), (85, 0, 0), 40), foco=(0, 0, 3.5)); fl = entrada(ctx, cam)
    def upd(f, t, u):
        up(u); k = smooth(min(1.0, u / 0.7))
        s.location.y = lerp(3.6, -0.6, k); s.location.z = 0.0; s.rotation_euler.x = -0.5 * (1 - k); s.scale = (0.5 + 0.5 * k,) * 3
        g.data.materials[0].node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = max(0.0, 40 * (1 - u * 1.4))
        for mx in rayos: mx.inputs[0].default_value = max(0.0, 0.18 * (1 - u * 1.2))
        for i, d in enumerate(polvo):
            d.location.z = 1 + (random.Random(i).uniform(0, 7) + t * 0.5) % 8
        for i, e in enumerate(est):
            a = t * 5 + i * 2.09; e.location = (s.location.x + 0.9 * math.cos(a), s.location.y - 0.6 + 0.3 * math.sin(a), 5.0 + 0.1 * i)
            e.scale = (0.001 if u < 0.55 else 0.25 + 0.4 * abs(math.sin(t * 6 + i)),) * 3
        s.rotation_euler.z = 0.12 * math.sin(t * 6) * k; fl(f)
    return upd


def p30(ctx):  # «antes decidía una ley o una revista»: tres cuadros (rey, ley, revista) que se desvanecen
    casa_decor(ctx, 5.6); armario(ctx, (0, 4.2, 0), 0)
    s = era(ctx, "Soclo", "casa", (0, 0, 0), 0, "neutral")
    cuadros = [cuadro(ctx, (-2.4, -1.6, 7.4), "rey", "REY"), cuadro(ctx, (0, -1.6, 7.7), "ley", "LEY"), cuadro(ctx, (2.4, -1.6, 7.4), "revista", "REVISTA")]
    cam, up = cam_rig(ctx, ((0, -15.5, 5.4), (84, 0, 0), 40), ((0, -13.5, 5.1), (84, 0, 0), 40), foco=(0, 0, 3.5))
    def upd(f, t, u):
        up(u); k = max(0.0, 1 - max(0.0, (u - 0.5) / 0.4))
        for i, o in enumerate(cuadros): o.scale = (0.85 * k,) * 3; o.rotation_euler.z = 0.12 * math.sin(t * 2 + i * 2)
        bob(s, t, 0, 0.03, 3); s.rotation_euler.z = 0.08 * math.sin(t * 2)
    return upd


def p31(ctx):  # mañana: Soclo indeciso, el reloj marca las 8:05 y avanza, entra el sol por la ventana
    casa_decor(ctx, 5.6); armario(ctx, (0, 4.2, 0), 0); pvs = reloj(ctx, (4.4, 5.2, 7.0))
    box(ctx, "marco ventana", (-5.2, 5.3, 6.6), (2.8, 0.3, 3.8), "#F4F1EA", 0.6); translucido(ctx, "ventana", (-5.2, 5.1, 6.6), 2.4, 3.4, "#BFE3FF", 0.9, emision=3)
    for i in range(3): translucido(ctx, "rayo sol", (-3.6 + i * 0.9, 4.9, 4.2), 0.5, 7.5, "#FFE6A8", 0.1, rot=(0, rad(-28), 0), emision=6)
    s = era(ctx, "Soclo", "casa", (0, 0, 0), 0, "neutral")
    qs = [text(ctx, "interrogante", "?", (0, 0, 0), 0.9, "#FFE27A", emit=3, extrude=0.08) for _ in range(3)]
    cam, up = cam_rig(ctx, ((1.0, -14, 5.2), (84, 0, 0), 40), ((1.6, -11.5, 4.9), (84, 0, 0), 40), foco=(0, 0, 3.5))
    def upd(f, t, u):
        up(u); bob(s, t, 0, 0.03, 3); brazo("Soclo", "i", 150, 10 * math.sin(t * 9)); s.rotation_euler.z = 0.1 * math.sin(t * 2.4)
        pvs[1].rotation_euler.y = rad(30 + 25 * u); pvs[0].rotation_euler.y = rad(242.5 + 2 * u)
        for i, q in enumerate(qs):
            ph = (t * 0.8 + i / 3) % 1.0; q.location = (-0.6 + 0.6 * i, -0.7, 5.3 + 1.6 * ph); q.scale = (0.4 + 0.8 * math.sin(ph * math.pi),) * 3
    return upd


def p32(ctx):  # el armario lleno, pero Soclo saca siempre la misma prenda; calendario de la semana
    casa_decor(ctx, 5.6); armario(ctx, (0, 4.2, 0), 0, uniforme="#E3873F")
    s = era(ctx, "Soclo", "casa", (0, 0, 0), 0, "neutral")
    prenda = box(ctx, "prenda en mano", (0, 0, 0), (1.3, 0.2, 1.7), "#E3873F", 0.85, bevel=True)
    cards = []
    for i, d in enumerate("LMXJV"):
        r = empty(ctx, "dia " + d, (-1.7 + 0.85 * i, -3.6, 0.1))
        box(ctx, "tarjeta", (0, 0, 0.85), (0.8, 0.1, 1.5), "#F7F4EE", 0.7, parent=r, bevel=True)
        text(ctx, "letra", d, (0, -0.1, 1.35), 0.4, "#15140F", emit=0.1, extrude=0.03, parent=r)
        box(ctx, "camiseta", (0, -0.1, 0.7), (0.55, 0.05, 0.5), "#E3873F", 0.8, parent=r); box(ctx, "manga", (-0.35, -0.1, 0.78), (0.2, 0.05, 0.22), "#E3873F", 0.8, parent=r); box(ctx, "manga", (0.35, -0.1, 0.78), (0.2, 0.05, 0.22), "#E3873F", 0.8, parent=r)
        cards.append(r)
    for k in range(5): box(ctx, "pila", (-2.5, -1.6 - 0.1 * (k % 2), 0.2 + 0.22 * k), (1.4, 1.0, 0.2), "#E3873F", 0.9, bevel=True)
    cam, up = cam_rig(ctx, ((0, -13, 4.8), (85, 0, 0), 40), ((0, -10.5, 4.5), (85, 0, 0), 40), foco=(0, 0, 3.5))
    def upd(f, t, u):
        up(u); ph = (t * 1.6) % 1.0; arriba = 0.4 + 0.6 * math.sin(ph * math.pi)
        prenda.location = (0.9, -1.0, 2.8 + 1.0 * arriba); prenda.rotation_euler.y = 0.15 * math.sin(t * 5); bob(s, t, 0, 0.02, 3)
        for i, c in enumerate(cards):
            q = max(0.0, min(1.0, (t - (0.2 + 0.36 * i)) / 0.2))
            c.scale = (smooth(q) * (1 + 0.15 * math.sin(q * math.pi)),) * 3 if q > 0 else (0.001,) * 3
    return upd


def p33(ctx):  # pasarela: Soclo da una vuelta con su look nuevo entre focos y flashes
    fondo(ctx, "#15140F", 0.5)
    box(ctx, "Suelo", (0, 5, -0.25), (60, 40, 0.5), "#24221B", 0.4)
    box(ctx, "Pasarela", (0, 2, 0.02), (5.2, 14, 0.12), "#F4F1EA", 0.4)
    for sx in (-1, 1): box(ctx, "Luces pasarela", (2.8 * sx, 2, 0.12), (0.15, 14, 0.12), "#FFE27A", 0.3, 4)
    luz(ctx, "Foco 1", 'SPOT', (-4, -3, 14), 80000, "#FFF1D6", rot=(65, 0, -15)); luz(ctx, "Foco 2", 'SPOT', (4, -3, 14), 80000, "#FFD9F0", rot=(65, 0, 15))
    luz(ctx, "Frente", 'AREA', (0, -12, 7), 7000, "#FFFFFF", rot=(80, 0, 0), size=14)
    s = era(ctx, "Soclo", "casa", (0, 0, 0), 0, "happy", top="#E3873F", pants="#C9B79C")
    est = [estrella(ctx, p, 0.45) for p in ((-2.0, -1.0, 4.8), (2.2, -1.0, 3.6), (-1.6, -1.0, 2.2), (1.9, -1.0, 5.6))]
    cam, up = cam_rig(ctx, ((0, -11, 4.0), (88, 0, 0), 50), ((0, -8.5, 3.9), (88, 0, 0), 50), foco=(0, 0, 3.5)); dfl = Destello(ctx, cam)
    def upd(f, t, u):
        up(u); bob(s, t, 0, 0.06, 5); s.rotation_euler.z = 2 * math.pi * smooth(min(1.0, max(0.0, (u - 0.1) / 0.8)))
        for i, e in enumerate(est): e.scale = (0.2 + 0.9 * abs(math.sin(t * 5 + i * 1.7)),) * 3; e.rotation_euler.y = t * 2 + i
        dfl.set(0.28 if f in (14, 28, 41, 55, 66) else 0.0)
    return upd


def p34(ctx):  # logo con rebote, confeti y un cursor que pulsa el botón
    fondo(ctx, "#15140F", 0.6)
    box(ctx, "Suelo", (0, 5, -0.25), (60, 40, 0.5), "#24221B", 0.5)
    luz(ctx, "Frente", 'AREA', (0, -12, 8), 3000, "#FFFFFF", rot=(80, 0, 0), size=14)
    logo = logo_plane(ctx, "logo", (0, 4.0, 8.0), 4.0, strength=2.2)
    boton = box(ctx, "boton", (0, 3.8, 5.2), (5.6, 0.4, 1.3), "#E3873F", 0.4, 0.5, bevel=True)
    texto = text(ctx, "cta", "Entra en Socly Style", (0, 3.55, 5.2), 0.62, "#15140F", emit=0.4, extrude=0.05)
    brillo, _ = translucido(ctx, "brillo boton", (0, 3.4, 5.2), 0.6, 1.5, "#FFFFFF", 0.5, rot=(0, rad(20), 0), emision=5)
    s = era(ctx, "Soclo", "casa", (0, -1.0, 0), 0, "happy"); s.scale = (0.75,) * 3
    cur = flecha(ctx, (2.6, 3.2, 8.0))
    onda = cyl(ctx, "onda", (0, 3.45, 5.2), 0.5, 0.05, "#FFFFFF", 0.4, 4, rot=(rad(90), 0, 0))
    rnd = random.Random(4); cols = ["#FF2E88", "#FFE500", "#18E0FF", "#2BFF88", "#FF7A00", "#8A3CFF"]
    conf = [(box(ctx, "confeti", (0, 0, 0), (0.22, 0.04, 0.34), rnd.choice(cols), 0.5, 1.5), rnd.uniform(-3.4, 3.4), rnd.random(), rnd.uniform(-1, 1)) for _ in range(46)]
    est = [estrella(ctx, p, 0.5) for p in ((-3.6, 3.0, 8.6), (3.8, 3.0, 8.2), (3.4, 3.0, 3.8), (-3.9, 3.0, 4.4))]
    cam, up = cam_rig(ctx, ((0, -14, 4.8), (86, 0, 0), 40), ((0, -11.5, 4.8), (86, 0, 0), 40), foco=(0, 2.0, 5.0))
    def upd(f, t, u):
        up(u); pop = 1 - math.exp(-t * 7) * math.cos(t * 14); logo.scale = (max(0.05, pop),) * 3; logo.location.z = 8.0 + 0.1 * math.sin(t * 2.5)
        bob(s, t, 0, 0.06, 4); brazo("Soclo", "d", 150, 20 * math.sin(t * 8))
        q = smooth(max(0.0, min(1.0, (t - 0.7) / 0.7))); cur.location = (lerp(2.6, 0.7, q), 3.2, lerp(8.0, 4.9, q))
        click = 1.0 if 1.4 <= t <= 1.55 else 0.0; k = 1 + 0.05 * math.sin(t * 6) - 0.10 * click; boton.scale = (k, 1, k); texto.scale = (k, k, k)
        w = max(0.0, (t - 1.4) / 0.6); onda.scale = (1 + 5 * w, 1, 1 + 5 * w) if 0 < w < 1 else (0.001,) * 3
        brillo.location.x = lerp(-3.0, 3.0, ((t * 0.7) % 1.0))
        for o, x0, ph, dx in conf:
            if t < 1.4: o.scale = (0.001,) * 3; continue
            tt = (t - 1.4) * 0.5 + ph; z = 11 - ((tt % 1.0) * 13)
            o.scale = (1,) * 3; o.location = (x0 + dx * 0.6 * (tt % 1.0), 2.5, z); o.rotation_euler = (t * 4 + ph, 0, t * 3 + dx)
        for i, e in enumerate(est): e.scale = (0.2 + 0.9 * abs(math.sin(t * 4 + i * 1.7)),) * 3; e.rotation_euler.y = t * 2 + i
    return upd


SHOTS = {23: p23, 24: p24, 25: p25, 26: p26, 27: p27, 28: p28, 29: p29, 30: p30, 31: p31, 32: p32, 33: p33, 34: p34}


def run(i):
    random.seed(i)
    ctx = Ctx("plano%02d" % i)
    upd = SHOTS[i](ctx)
    r = ctx.sc.render; r.engine = 'BLENDER_EEVEE'; r.resolution_x = 1080; r.resolution_y = 1920; r.resolution_percentage = 50
    ctx.sc.eevee.taa_render_samples = 48
    ctx.sc.view_settings.view_transform = 'AgX'; ctx.sc.view_settings.look = 'AgX - High Contrast'; ctx.sc.view_settings.exposure = 0.0
    prueba = os.environ.get("SOCLY_FRAMES")
    d = PLANOS + "\\s%02d" % i
    os.makedirs(d if not prueba else HERE + r"\prueba", exist_ok=True)
    frames = [int(x) for x in prueba.split(",")] if prueba else range(N)
    t0 = time.time()
    for f in frames:
        upd(f, f / 30.0, f / (N - 1))
        r.filepath = (HERE + "\\prueba\\p%02d_f%02d.png" % (i, f)) if prueba else d + "\\f_%04d.png" % f
        bpy.ops.render.render(write_still=True)
    print("PLANO", i, "listo en", round(time.time() - t0), "s", flush=True)


if __name__ == "__main__":
    args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else ["23", "23"]
    a, b = int(args[0]), int(args[-1])
    for i in range(a, b + 1): run(i)
