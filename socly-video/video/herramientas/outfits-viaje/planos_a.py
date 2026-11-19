"""Fase 4: planos 1-12 de «¿De dónde vienen los outfits?» (casa, prehistoria, Egipto). 75 fotogramas por plano (2,5 s a 30 fps).
  blender -b --python planos_a.py -- 1 12                 (renderiza los planos 1 a 12 a planos\\sNN\\)
  SOCLY_FRAMES=40 blender -b --python planos_a.py -- 1 12  (solo ese fotograma de cada plano, a prueba\\pNN.png)"""
import sys, time
HERE = r"/home/user/prueba/socly-video\video\herramientas\outfits-viaje"
exec(open(r"/home/user/prueba/socly-video\video\herramientas\ciudad-socly\lib.py", encoding="utf-8").read())
exec(open(HERE + r"\trajes.py", encoding="utf-8").read())
exec(open(HERE + r"\base.py", encoding="utf-8").read())
N = 75
PLANOS = HERE + r"\planos"


def entrada(ctx, cam):  # llegada de un salto: parte de blanco
    d = Destello(ctx, cam); return lambda f: d.set(max(0.0, 1 - f / 10.0))


def salida_blanca(ctx, cam):  # salto a otra época: acaba en blanco
    d = Destello(ctx, cam); return lambda f: d.set(max(0.0, (f - 62) / 12.0))


def bocanadas(ctx, n=3):
    return [box(ctx, "vaho", (0, 0, 0), (0.2, 0.2, 0.2), "#F4F1EA", 0.9, 0.4) for _ in range(n)]


def vaho(ps, t, origen):
    for i, p in enumerate(ps):
        ph = (t * 1.1 + i / len(ps)) % 1.0
        p.location = (origen[0] + 0.45 + 0.9 * ph * (1 if i % 2 else 0.4), origen[1] - 0.7 - 0.3 * ph, origen[2] - 0.25 + 0.5 * ph)
        p.scale = (0.4 + 0.9 * ph,) * 3


# ------------------------------------------------------------------ casa
def p01(ctx):  # Soclo de espaldas ante su armario lleno
    casa_decor(ctx, -4.6); armario(ctx, (0, -3.4, 0), math.pi)
    s = era(ctx, "Soclo", "casa", (0, 1.4, 0), 0, "neutral")
    cam, up = cam_rig(ctx, ((0, 15, 6.0), (79, 0, 180), 40), ((0, 12.5, 5.6), (80, 0, 180), 40))
    def upd(f, t, u):
        up(u); bob(s, t, 0, 0.04, 3); s.rotation_euler.z = 0.1 * math.sin(t * 2.4)
    return upd


def p02(ctx):  # Soclo de frente, se rasca la cabeza con el armario detrás
    casa_decor(ctx, 5.6); armario(ctx, (0, 4.2, 0), 0)
    s = era(ctx, "Soclo", "casa", (0, 0, 0), 0, "neutral")
    cam, up = cam_rig(ctx, ((0, -15, 5.2), (84, 0, 0), 40), ((0, -12, 4.8), (85, 0, 0), 40))
    def upd(f, t, u):
        up(u); brazo("Soclo", "i", 150, 12 * math.sin(t * 10)); bob(s, t, 0, 0.03, 3)
    return upd


def p03(ctx):  # entra en el armario: luz blanca, cae dentro, destello
    casa_decor(ctx, -4.6); _, g = armario(ctx, (0, -3.4, 0), math.pi, glow=3)
    s = era(ctx, "Soclo", "casa", (0, 1.4, 0), 0, "shock")
    cam, up = cam_rig(ctx, ((0, 12, 5.6), (80, 0, 180), 40), ((0, 8.5, 4.8), (82, 0, 180), 40))
    fl = salida_blanca(ctx, cam)
    def upd(f, t, u):
        up(u); k = max(0.0, (u - 0.35) / 0.65)
        s.location.y = lerp(1.4, -3.2, smooth(min(1, u / 0.8))); s.location.z = -2.2 * k * k
        s.rotation_euler.x = 0.9 * k; s.scale = (1 - 0.7 * k,) * 3
        g.data.materials[0].node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = 3 + 40 * u
        fl(f)
    return upd


# ------------------------------------------------------------------ prehistoria
def _cuevagente(ctx):
    return [era(ctx, "C1", "prehistoria", (-3.4, 9.0, 0), rad(15), "neutral", skin=S[2], tela="#6B4A2A"),
            era(ctx, "C2", "prehistoria", (3.2, 9.5, 0), rad(-15), "happy", skin=S[3], tela="#A5683A"),
            era(ctx, "C3", "prehistoria", (4.4, 4.6, 0), rad(-30), "neutral", skin=S[0], tela="#7A5230")]


def p04(ctx):  # Soclo cae en la cueva
    ll = cueva_decor(ctx); gente = _cuevagente(ctx)
    s = era(ctx, "Soclo", "prehistoria", (-1.8, 0, 0), 0, "shock")
    cam, up = cam_rig(ctx, ((0, -20, 4.4), (87, 0, 0), 50), ((0, -17.5, 4.0), (87, 0, 0), 50))
    fl = entrada(ctx, cam)
    def upd(f, t, u):
        up(u); llamear(ll, t)
        tl = 0.65
        s.location.z = 9 - 9 * (t / tl) ** 2 if t < tl else max(0.0, 1.1 * math.sin((t - tl) * 8) * math.exp(-(t - tl) * 3))
        for i, g in enumerate(gente): bob(g, t, 0, 0.05, 3, i)
        fl(f)
    return upd


def p05(ctx):  # hace frío: Soclo tirita y echa vaho
    ll = cueva_decor(ctx); gente = _cuevagente(ctx)
    s = era(ctx, "Soclo", "prehistoria", (-0.5, 0, 0), 0, "scared"); pv = bocanadas(ctx)
    cam, up = cam_rig(ctx, ((0, -13, 3.8), (88, 0, 0), 50), ((0, -11, 3.6), (88, 0, 0), 50))
    def upd(f, t, u):
        up(u); llamear(ll, t)
        s.location.x = -0.5 + 0.06 * math.sin(t * 70); brazo("Soclo", "i", 35); brazo("Soclo", "d", 35)
        vaho(pv, t, (s.location.x, s.location.y, 3.7))
        for i, g in enumerate(gente): brazo(g, "i", 60 + 10 * math.sin(t * 5 + i)); bob(g, t, 0, 0.04, 3, i)
    return upd


def p06(ctx):  # primer plano: una persona de la cueva cose una piel con una aguja de hueso
    ll = cueva_decor(ctx)
    c = era(ctx, "Cose", "prehistoria", (0, 0, 0), 0, "happy", skin=S[2], tela="#6B4A2A")
    for pv in RIG["Cose"]["arm"]:
        if pv is not None: pv.scale = (0.001, 0.001, 0.001)
    for sx in (-1, 1):  # brazos doblados hacia delante, con los dos antebrazos y las manos
        box(ctx, "brazo", (0.88 * sx, 0, 2.85), (0.42, 0.45, 0.8), S[2], 0.6, parent=c, bevel=True)
        box(ctx, "antebrazo", (0.7 * sx, -0.5, 2.55), (0.4, 1.0, 0.4), S[2], 0.6, parent=c, bevel=True)
        box(ctx, "mano", (0.5 * sx, -1.05, 2.55), (0.42, 0.42, 0.42), S[2], 0.6, parent=c, bevel=True)
    box(ctx, "piel cosida", (-0.45, -1.15, 2.1), (1.4, 0.25, 1.0), "#8A5A2B", 0.95, parent=c, bevel=True)
    box(ctx, "piel cosida borde", (-0.45, -1.15, 1.62), (1.45, 0.27, 0.12), "#E8DCC0", 0.95, parent=c)
    aguja = box(ctx, "aguja", (0.5, -1.2, 2.7), (0.1, 0.1, 1.1), "#F4F1EA", 0.45, 1.0, rot=(0, rad(35), 0), parent=c)
    hilo = box(ctx, "hilo", (0.2, -1.2, 2.2), (0.04, 0.04, 0.8), "#E3B25A", 0.8, 0.5, parent=c)
    est = [estrella(ctx, p, 0.3) for p in ((1.6, -1.6, 3.4), (-1.6, -1.2, 3.9))]
    cam, up = cam_rig(ctx, ((0, -8.5, 3.0), (89, 0, 0), 40), ((0, -6.6, 2.9), (89, 0, 0), 40))
    def upd(f, t, u):
        up(u); llamear(ll, t); d = 0.35 * math.sin(t * 7.5)
        aguja.location = (0.5, -1.2, 2.7 + d); hilo.location = (0.2, -1.2, 2.2 + d * 0.5); bob(c, t, 0, 0.03, 3)
        for i, e in enumerate(est): e.scale = (0.2 + 0.9 * abs(math.sin(t * 5 + i * 2)),) * 3; e.rotation_euler.y = t * 2 + i
    return upd


def p07(ctx):  # una persona con collar de conchas; Soclo la señala
    ll = cueva_decor(ctx)
    s = era(ctx, "Soclo", "prehistoria", (-0.9, 0, 0), rad(-12), "happy")
    c = era(ctx, "Collar", "prehistoria", (1.6, 4.0, 0), rad(-8), "happy", skin=S[3], tela="#7A5230"); c.scale = (1.25,) * 3
    conchas = [box(ctx, "concha gr", (-0.45 + 0.15 * i, -0.45, 3.0 - abs(i - 3) * 0.1), (0.17, 0.07, 0.17), "#F4F1EA", 0.4, 1.2, parent=c) for i in range(7)]
    cam, up = cam_rig(ctx, ((0, -15.5, 3.8), (88, 0, 0), 50), ((0.2, -13, 3.8), (88, 0, 0), 50))
    def upd(f, t, u):
        up(u); llamear(ll, t); brazo("Soclo", "i", 85, 6 * math.sin(t * 6)); bob(s, t, 0, 0.04, 3)
        for i, o in enumerate(conchas): o.scale = (1 + 0.25 * math.sin(t * 8 + i),) * 3
    return upd


def p08(ctx):  # Soclo se prueba el collar y sonríe; salto
    ll = cueva_decor(ctx)
    s = era(ctx, "Soclo", "prehistoria", (0, 0, 0), 0, "happy")
    for i in range(7): box(ctx, "concha gr", (-0.45 + 0.15 * i, -0.45, 3.0 - abs(i - 3) * 0.1), (0.17, 0.07, 0.17), "#F4F1EA", 0.4, 1.0, parent=s)
    est = [estrella(ctx, p, 0.35) for p in ((-1.5, -1.2, 3.6), (1.6, -1.0, 4.4), (0.2, -1.3, 5.2))]
    cam, up = cam_rig(ctx, ((0, -9, 3.9), (88, 0, 0), 50), ((0, -7, 3.9), (88, 0, 0), 50))
    fl = salida_blanca(ctx, cam)
    def upd(f, t, u):
        up(u); llamear(ll, t); bob(s, t, 0, 0.08, 5); brazo("Soclo", "i", 30); s.rotation_euler.z = 0.12 * math.sin(t * 4)
        for i, e in enumerate(est): e.scale = (0.3 + abs(math.sin(t * 6 + i * 2)),) * 3; e.rotation_euler.y = t * 3 + i
        fl(f)
    return upd


# ------------------------------------------------------------------ Egipto
def p09(ctx):  # Egipto: calor, lino y ropa blanca
    gente, verde = egipto_decor(ctx)
    s = era(ctx, "Soclo", "egipto", (-1.1, 0, 0), rad(-10), "happy")
    cam, up = cam_rig(ctx, ((0, -15, 3.6), (88, 0, 0), 50), ((0, -12.5, 3.5), (88, 0, 0), 50))
    fl = entrada(ctx, cam)
    def upd(f, t, u):
        up(u); bob(s, t, 0, 0.05, 3)
        for i, g in enumerate(gente + [verde]): bob(g, t, 0, 0.04, 3, i)
        fl(f)
    return upd


def p10(ctx):  # «mira ese: va de verde»: Soclo señala y la cámara se acerca al del verde
    gente, verde = egipto_decor(ctx)
    s = era(ctx, "Soclo", "egipto", (0.2, -1.0, 0), rad(10), "happy")
    cam, up = cam_rig(ctx, ((0.9, -13, 3.8), (88, 0, 0), 50), ((0.9, -10.8, 3.8), (88, 0, 0), 50))
    def upd(f, t, u):
        up(u, look=(1.0, 7.5, 3.6)); brazo("Soclo", "i", 85, 6 * math.sin(t * 6)); bob(s, t, 0, 0.04, 3)
        for i, g in enumerate(gente): bob(g, t, 0, 0.03, 3, i)
    return upd


def p11(ctx):  # primer plano del del verde: sombra de ojos de malaquita que brilla
    gente, verde = egipto_decor(ctx)
    sh = [box(ctx, "malaquita", (2.0 + 0.26 * sx, 7.5 - 0.6, 4.2), (0.34, 0.03, 0.1), "#2EE07A", 0.4, 3) for sx in (-1, 1)]
    est = [estrella(ctx, (2.0 + dx, 7.0, 4.0 + dz), 0.25, "#9CFFC4") for dx, dz in ((-0.9, 0.5), (0.9, 0.6), (0.0, 0.9))]
    cam, up = cam_rig(ctx, ((2.0, 2.6, 4.0), (90, 0, 0), 75), ((2.0, 3.6, 4.0), (90, 0, 0), 95))
    def upd(f, t, u):
        up(u, look=(2.0, 7.5, 3.95)); bob(verde, t, 0, 0.02, 3)
        for o in sh: o.data.materials[0].node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = 0.6 + 0.8 * abs(math.sin(t * 5))
        for i, e in enumerate(est): e.scale = (0.2 + abs(math.sin(t * 5 + i * 2)),) * 3; e.rotation_euler.y = t * 3 + i
    return upd


def p12(ctx):  # joyas, pelucas, maquillaje: Soclo posa y la cámara gira; salto
    gente, verde = egipto_decor(ctx)
    s = era(ctx, "Soclo", "egipto", (0, 0, 0), 0, "happy")
    est = [estrella(ctx, p, 0.4) for p in ((-1.2, -1.0, 3.2), (1.3, -1.0, 4.6), (0.0, -1.2, 5.3))]
    cam, up = cam_rig(ctx, ((0, -10, 3.8), (88, 0, 0), 50))
    fl = salida_blanca(ctx, cam)
    def upd(f, t, u):
        a = rad(lerp(-38, 38, smooth(u))); cam.location = (10 * math.sin(a), -10 * math.cos(a), 3.8); mira(cam, (0, 0, 3.4))
        brazo("Soclo", "i", 35); brazo("Soclo", "d", 35); bob(s, t, 0, 0.06, 4)
        for i, e in enumerate(est): e.scale = (0.15 + 0.45 * abs(math.sin(t * 6 + i * 2)),) * 3
        for i, g in enumerate(gente + [verde]): bob(g, t, 0, 0.03, 3, i)
        fl(f)
    return upd


SHOTS = {1: p01, 2: p02, 3: p03, 4: p04, 5: p05, 6: p06, 7: p07, 8: p08, 9: p09, 10: p10, 11: p11, 12: p12}


def run(i):
    random.seed(i)
    ctx = Ctx("plano%02d" % i)
    upd = SHOTS[i](ctx)
    r = ctx.sc.render; r.engine = 'BLENDER_EEVEE'; r.resolution_x = 1080; r.resolution_y = 1920; r.resolution_percentage = 50
    ctx.sc.eevee.taa_render_samples = 24
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
    args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else ["1", "1"]
    a, b = int(args[0]), int(args[-1])
    for i in range(a, b + 1): run(i)
