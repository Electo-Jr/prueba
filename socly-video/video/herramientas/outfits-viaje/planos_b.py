"""Fase 5: planos 13-22 de «¿De dónde vienen los outfits?» (Roma, Edad Media, 1852). 75 fotogramas por plano (2,5 s a 30 fps).
  blender -b --python planos_b.py -- 13 22
  SOCLY_FRAMES=40 blender -b --python planos_b.py -- 13 22   (solo ese fotograma de cada plano, a prueba\\pNN_f40.png)"""
import sys, time
HERE = r"/home/user/prueba/socly-video\video\herramientas\outfits-viaje"
exec(open(r"/home/user/prueba/socly-video\video\herramientas\ciudad-socly\lib.py", encoding="utf-8").read())
exec(open(HERE + r"\trajes.py", encoding="utf-8").read())
exec(open(HERE + r"\base.py", encoding="utf-8").read())
exec(open(HERE + r"\base_b.py", encoding="utf-8").read())
N = 75
PLANOS = HERE + r"\planos"


def entrada(ctx, cam):
    d = Destello(ctx, cam); return lambda f: d.set(max(0.0, 1 - f / 10.0))


def salida_blanca(ctx, cam):
    d = Destello(ctx, cam); return lambda f: d.set(max(0.0, (f - 62) / 12.0))


def bobs(gs, t, a=0.04):
    for i, g in enumerate(gs): bob(g, t, 0, a, 3, i)


# ------------------------------------------------------------------ Roma
def p13(ctx):  # Roma: mercado de telas; el vendedor enseña una tela púrpura
    roma_decor(ctx)
    puesto_telas(ctx, 2.6, 6.5, ["#F4F1EA", "#6B2D8A", "#C9B79C", "#8A5A2B"]); puesto_telas(ctx, -4.2, 11.0, ["#E3873F", "#F4F1EA", "#1F2A4D", "#F4F1EA"])
    s = era(ctx, "Soclo", "roma", (-1.2, 0, 0), rad(15), "happy")
    v = era(ctx, "Vendedor", "roma", (2.6, 8.1, 0), 0, "happy", skin=S[2])
    tela = box(ctx, "Tela purpura", (2.6, 7.0, 3.6), (1.7, 0.1, 1.5), "#6B2D8A", 0.5, 0.7)
    clientes = [era(ctx, "Cli1", "roma", (-3.4, 4.5, 0), rad(20), "neutral", skin=S[3]), era(ctx, "Cli2", "roma", (0.8, 12.5, 0), rad(-10), "happy", skin=S[1], tela="#C9B79C")]
    cam, up = cam_rig(ctx, ((0, -18.5, 4.2), (87, 0, 0), 50), ((0, -15.5, 4.0), (87, 0, 0), 50)); fl = entrada(ctx, cam)
    def upd(f, t, u):
        up(u); bobs([s, v] + clientes, t); brazo("Vendedor", "i", 110, 8 * math.sin(t * 6)); brazo("Vendedor", "d", 110, -8 * math.sin(t * 6))
        tela.rotation_euler.x = 0.06 * math.sin(t * 5); fl(f)
    return upd


def p14(ctx):  # el senador con toga púrpura, guardias; el pueblo mira de lejos
    roma_decor(ctx)
    sen = era_purpura(ctx, "Senador", (0, 6.0, 0), 0, "smug")
    g1 = era(ctx, "G1", "roma", (-2.5, 5.0, 0), 0, "neutral", skin=S[3], tela="#C9B79C"); g2 = era(ctx, "G2", "roma", (2.5, 5.0, 0), 0, "neutral", skin=S[2], tela="#C9B79C")
    lanza(ctx, (-3.4, 4.6, 2.3)); lanza(ctx, (3.4, 4.6, 2.3))
    pueblo = [era(ctx, "P%d" % i, "roma", (-4 + i * 1.6, 13.5 + (i % 2) * 1.5, 0), rad(-5 + i * 2), "happy", skin=S[i % 4], tela="#E8DFC9") for i in range(6)]
    s = era(ctx, "Soclo", "roma", (-1.0, -1.5, 0), rad(-15), "neutral")
    cam, up = cam_rig(ctx, ((0, -17, 4.2), (87, 0, 0), 50), ((0, -14.5, 4.0), (87, 0, 0), 50))
    def upd(f, t, u):
        up(u); bobs([sen, g1, g2, s] + pueblo, t, 0.03); brazo("Senador", "i", 45, 6 * math.sin(t * 3))
    return upd


def p15(ctx):  # Soclo compara su toga blanca con la del poderoso; salto
    roma_decor(ctx)
    sen = era_purpura(ctx, "Senador", (1.5, 0.5, 0), rad(-12), "smug"); sen.scale = (1.1,) * 3
    s = era(ctx, "Soclo", "roma", (-1.3, 0, 0), rad(12), "neutral")
    cam, up = cam_rig(ctx, ((0, -14.5, 4.0), (88, 0, 0), 50), ((0, -12.5, 3.9), (88, 0, 0), 50)); fl = salida_blanca(ctx, cam)
    def upd(f, t, u):
        up(u); s.rotation_euler.x = 0.18 * smooth(min(1, u * 2)); brazo("Soclo", "i", 35); bobs([sen], t, 0.02); fl(f)
    return upd


# ------------------------------------------------------------------ Edad Media
def p16(ctx):  # Edad Media: calle de piedra, carretas, gente con ropa de lana
    medieval_decor(ctx); carreta(ctx, (-5.5, 9.0, 0), rad(10)); carreta(ctx, (6.5, 16.0, 0), rad(-8))
    s = era(ctx, "Soclo", "medieval", (-0.6, 0, 0), rad(10), "happy")
    gente = [era(ctx, "M1", "medieval", (2.4, 6.0, 0), rad(-10), "neutral", skin=S[2], tela="#8B6F47"), era(ctx, "M2", "medieval", (-3.0, 9.5, 0), rad(15), "happy", skin=S[0], tela="#6B7A3A"),
             era(ctx, "M3", "medieval", (3.4, 11.5, 0), rad(-5), "neutral", skin=S[3], tela="#7A5A5A")]
    cam, up = cam_rig(ctx, ((0, -15, 3.8), (88, 0, 0), 50), ((0, -12.5, 3.7), (88, 0, 0), 50)); fl = entrada(ctx, cam)
    def upd(f, t, u):
        up(u); bobs([s] + gente, t); fl(f)
    return upd


def p17(ctx):  # cartel con la ley: telas y colores tachados; pasa un noble
    medieval_decor(ctx)
    box(ctx, "Poste cartel", (0.4, 3.6, 2.6), (0.3, 0.3, 5.2), "#4A3524", 0.9)
    box(ctx, "Tablon", (0.4, 3.35, 5.0), (3.4, 0.2, 4.2), "#7A5230", 0.9, bevel=True)
    box(ctx, "Pergamino", (0.4, 3.2, 5.0), (3.0, 0.08, 3.8), "#E8D9B0", 0.9)
    cols = ["#6B2D8A", "#7A1F2B", "#D9A23F", "#1F2A4D", "#2E9E5B", "#E3873F"]
    for k, c in enumerate(cols):
        zz = 6.4 - k * 0.55
        box(ctx, "muestra", (-0.65, 3.14, zz), (0.9, 0.06, 0.34), c, 0.7)
        box(ctx, "linea", (0.9, 3.14, zz), (1.2, 0.06, 0.1), "#4A3524", 0.9)
        if k % 2 == 0:
            for sg in (-1, 1): box(ctx, "tachon", (-0.65, 3.1, zz), (1.2, 0.06, 0.08), "#D62828", 0.6, 0.6, rot=(0, rad(35 * sg), 0))
    s = era(ctx, "Soclo", "medieval", (-1.2, 0, 0), rad(-18), "neutral")
    noble = era(ctx, "Noble", "medieval", (6.0, 1.5, 0), rad(90), "smug", skin=S[0], tela="#5B1F7A")
    cam, up = cam_rig(ctx, ((0, -14.5, 4.4), (88, 0, 0), 50), ((0, -12, 4.5), (88, 0, 0), 50))
    def upd(f, t, u):
        up(u); noble.location.x = lerp(6.0, -4.0, u); anda(noble, t); bobs([s], t, 0.03); brazo("Soclo", "i", 80, 6 * math.sin(t * 5))
    return upd


def p18(ctx):  # Soclo mira por la ventana el terciopelo de un noble, sin poder tocarlo; un guardia le tapa los ojos; salto
    fondo(ctx, "#B9C6D0", 0.9)
    box(ctx, "Suelo", (0, 5, -0.25), (60, 40, 0.5), "#77716A", 0.95)
    # muro de cara a la cámara (plano y=3.2) con una ventana a la derecha
    box(ctx, "Muro bajo", (1.0, 3.2, 1.1), (30, 0.4, 2.2), "#D8C7A5", 0.95)
    box(ctx, "Muro alto", (1.0, 3.2, 7.6), (30, 0.4, 4.8), "#D8C7A5", 0.95)
    box(ctx, "Muro izq", (-6.9, 3.2, 3.8), (14.2, 0.4, 3.0), "#D8C7A5", 0.95)
    box(ctx, "Muro der", (9.9, 3.2, 3.8), (11.6, 0.4, 3.0), "#D8C7A5", 0.95)
    box(ctx, "Marco abajo", (2.2, 3.0, 2.25), (3.0, 0.5, 0.2), "#4A3524", 0.9); box(ctx, "Marco arriba", (2.2, 3.0, 5.35), (3.0, 0.5, 0.2), "#4A3524", 0.9)
    box(ctx, "Interior suelo", (2.2, 8.0, 0.02), (14, 10, 0.06), "#6A4A2A", 0.6)
    box(ctx, "Interior fondo", (2.2, 12.5, 5), (14, 0.4, 10), "#7A3A2A", 0.8)
    luz(ctx, "Sol", 'SUN', (10, -10, 25), 2.8, "#FFF1D0", rot=(55, 0, 20))
    luz(ctx, "Relleno", 'AREA', (0, -12, 7), 2600, "#FFFFFF", rot=(80, 0, 0), size=14)
    luz(ctx, "Interior", 'AREA', (2.2, 7, 9), 5000, "#FFE0B0", rot=(0, 0, 0), size=6)
    noble = era(ctx, "Noble", "medieval", (2.2, 6.2, 0), 0, "smug", skin=S[0], tela="#5B1F7A")
    s = era(ctx, "Soclo", "medieval", (-0.8, 1.2, 0), rad(55), "happy")
    guardia = era(ctx, "Guardia", "medieval", (-2.2, 2.2, 0), rad(55), "neutral", skin=S[3], tela="#6A6F78")
    cyl(ctx, "casco", (0, 0, 4.72), 0.7, 0.8, "#9AA0AA", 0.3, parent=guardia, r2=0.55)
    cara = Vector((-0.8 + 0.82 * 0.55, 1.2 - 0.57 * 0.55, 3.95)); perp = Vector((0.57, 0.82, 0)); atras = Vector((-0.82, 0.57, 0))
    manos = [box(ctx, "mano guardia", (0, 0, 0), (0.5, 0.5, 0.5), S[3], 0.6, bevel=True) for _ in (0, 1)]
    mangas = [box(ctx, "manga guardia", (0, 0, 0), (0.45, 0.45, 0.9), "#6A6F78", 0.7, bevel=True) for _ in (0, 1)]
    est = [estrella(ctx, p, 0.3, "#E7C8FF") for p in ((1.2, 2.6, 4.6), (3.4, 2.6, 3.4))]
    cam, up = cam_rig(ctx, ((0.6, -11, 4.2), (88, 0, 0), 50), ((0.6, -9, 4.1), (88, 0, 0), 50)); fl = salida_blanca(ctx, cam)
    def upd(f, t, u):
        up(u); k = smooth(max(0.0, min(1.0, (f - 30) / 20.0)))
        s.rotation_euler.z = rad(55) + 0.1 * math.sin(t * 4) * (1 - k); bobs([noble], t, 0.02)
        s.rotation_euler.x = 0.0
        RIG["Soclo"]["arm"][0].rotation_euler = (rad(-80) * (1 - 0.7 * k), 0, 0)
        for sg, m, b in zip((-1, 1), manos, mangas):
            end = cara + perp * 0.3 * sg; start = cara + atras * 1.4 + perp * 0.9 * sg + Vector((0, 0, -0.3))
            pos = start.lerp(end, k); m.location = pos; b.location = pos + atras * 0.6 + Vector((0, 0, -0.3))
        for i, e in enumerate(est): e.scale = (0.2 + 0.7 * abs(math.sin(t * 5 + i)),) * 3
        fl(f)
    return upd


# ------------------------------------------------------------------ 1852
def p19(ctx):  # calle de París 1852, levitas y vestidos largos
    paris_decor(ctx)
    s = era(ctx, "Soclo", "1852", (-0.9, 0, 0), rad(8), "happy")
    gente = [era(ctx, "H1", "1852", (2.4, 6.0, 0), rad(-12), "neutral", skin=S[2], tela="#2B3A5C"), era(ctx, "H2", "1852", (-3.2, 10.0, 0), rad(10), "happy", skin=S[0], tela="#4A3A2A"),
             dama(ctx, "D1", (0.6, 8.6, 0), rad(5), "#C97A9A"), dama(ctx, "D2", (3.6, 12.0, 0), rad(-8), "#4F8A9A", skin=S[1])]
    cam, up = cam_rig(ctx, ((0, -15, 3.8), (88, 0, 0), 50), ((0, -12.5, 3.7), (88, 0, 0), 50)); fl = entrada(ctx, cam)
    def upd(f, t, u):
        up(u); bobs([s] + gente, t); fl(f)
    return upd


def p20(ctx):  # la palabra OUTFIT cae sobre un maniquí con un conjunto completo
    fondo(ctx, "#1F2A3A", 0.8)
    box(ctx, "Suelo", (0, 5, -0.25), (60, 40, 0.5), "#2C3E50", 0.5)
    box(ctx, "Fondo", (0, 14, 7), (40, 0.4, 14), "#26374B", 0.8)
    maniqui(ctx, (0, 6.0, 0.3), True)
    luz(ctx, "Foco", 'SPOT', (0, -2, 14), 90000, "#FFF4DD", rot=(75, 0, 0)); luz(ctx, "Frente", 'AREA', (0, -12, 7), 2500, "#FFFFFF", rot=(80, 0, 0), size=14)
    s = era(ctx, "Soclo", "1852", (-1.4, 1.5, 0), rad(-20), "happy")
    texto = text(ctx, "OUTFIT", "OUTFIT", (0, 4.6, 12.0), 1.4, "#FFE27A", emit=3.5, extrude=0.5)
    est = [estrella(ctx, p, 0.5) for p in ((-2.6, 4.2, 7.6), (2.7, 4.2, 8.2), (0.2, 4.0, 9.2))]
    cam, up = cam_rig(ctx, ((0, -11, 4.6), (88, 0, 0), 50), ((0, -9.5, 4.6), (88, 0, 0), 50))
    def upd(f, t, u):
        up(u); tl = 0.55; z0 = 12.0; zf = 8.0
        texto.location.z = z0 - (z0 - zf) * (t / tl) ** 2 if t < tl else zf + max(0.0, 0.7 * math.sin((t - tl) * 9) * math.exp(-(t - tl) * 3.5))
        for i, e in enumerate(est): e.scale = (0.05 if t < tl else 0.2 + 0.8 * abs(math.sin((t - tl) * 6 + i * 2)),) * 3; e.rotation_euler.y = t * 2 + i
        bobs([s], t, 0.03)
    return upd


def p21(ctx):  # taller de costura: un modisto cose una etiqueta con su nombre en un vestido
    mesa = taller_decor(ctx)
    box(ctx, "vestido", (0.4, 5.4, 1.35), (2.2, 1.2, 0.2), "#7A1F2B", 0.8, bevel=True)
    box(ctx, "etiqueta", (-0.1, 5.1, 1.5), (0.9, 0.5, 0.06), "#F7F4EE", 0.7)
    box(ctx, "firma", (-0.1, 5.1, 1.54), (0.6, 0.05, 0.02), "#15140F", 0.9)
    m = era(ctx, "Modisto", "1852", (0, 7.4, 0), 0, "happy", skin=S[0], hair="#CFCFD4", tela="#4A4A55")
    aguja = box(ctx, "aguja", (0.1, 5.0, 1.8), (0.06, 0.06, 0.9), "#F4F1EA", 0.4, 0.8, rot=(rad(20), 0, 0))
    s = era(ctx, "Soclo", "1852", (3.6, 0.5, 0), rad(25), "happy")
    est = [estrella(ctx, p, 0.3) for p in ((-0.6, 4.6, 2.4), (0.8, 4.6, 2.2))]
    cam, up = cam_rig(ctx, ((0.3, -6.5, 3.8), (80, 0, 0), 45), ((0.2, -5.0, 3.6), (78, 0, 0), 45))
    def upd(f, t, u):
        up(u); d = 0.3 * abs(math.sin(t * 6)); aguja.location.z = 1.7 + d; bobs([s], t, 0.03); bob(m, t, 0, 0.02, 3)
        for i, e in enumerate(est): e.scale = (0.2 + 0.7 * abs(math.sin(t * 6 + i * 2)),) * 3
    return upd


def p22(ctx):  # Soclo hojea una revista con looks; salto
    paris_decor(ctx)
    s = era(ctx, "Soclo", "1852", (0, 0, 0), 0, "happy")
    r, pv = revista(ctx, (0, -1.0, 2.5), 1.05)
    est = [estrella(ctx, p, 0.35) for p in ((-2.0, -1.5, 5.0), (2.1, -1.5, 4.2))]
    cam, up = cam_rig(ctx, ((0, -11, 3.9), (88, 0, 0), 50), ((0, -8.5, 3.8), (88, 0, 0), 50)); fl = salida_blanca(ctx, cam)
    def upd(f, t, u):
        up(u); pv.rotation_euler.z = math.pi * smooth(max(0.0, min(1.0, (f - 15) / 35.0))); bob(s, t, 0, 0.03, 3)
        for i, e in enumerate(est): e.scale = (0.2 + 0.7 * abs(math.sin(t * 6 + i * 2)),) * 3
        fl(f)
    return upd


SHOTS = {13: p13, 14: p14, 15: p15, 16: p16, 17: p17, 18: p18, 19: p19, 20: p20, 21: p21, 22: p22}


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
    args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else ["13", "13"]
    a, b = int(args[0]), int(args[-1])
    for i in range(a, b + 1): run(i)
