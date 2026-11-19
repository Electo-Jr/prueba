"""Correcciones tras la revisión (solapes, atravesar paredes, armario, puertas). Se carga desde escenas.py tras planos2.py."""

def scatter(n, xr, yr, mind, seed, hole=None, avoid=()):
    """Puntos al azar sin solaparse (distancia mínima `mind`); `hole`=(cx,cy,r) deja un hueco libre."""
    rnd = random.Random(seed); pts = []; tries = 0
    while len(pts) < n and tries < 8000:
        tries += 1
        x = rnd.uniform(*xr); y = rnd.uniform(*yr)
        if hole and (x - hole[0]) ** 2 + (y - hole[1]) ** 2 < hole[2] ** 2: continue
        if all((x - a) ** 2 + (y - b) ** 2 >= mind * mind for a, b in pts + list(avoid)): pts.append((x, y))
    return pts

def mira_a(px, py, cx, cy):
    """Giro en Z para que un personaje (que mira a -Y) mire hacia (cx, cy)."""
    return math.atan2(cy - py, cx - px) + math.pi / 2

def p01(ctx):  # plaza llena de bloques con looks absurdos, cenital que baja (sin solapes)
    city(ctx, "gris"); ppl = []
    for i, (x, y) in enumerate(scatter(14, (-9, 9), (-3, 11), 2.8, 4)):
        ppl.append(vecino(ctx, i, (x, y, 0), random.Random(i).uniform(-2.8, 2.8), name="a%d" % i))
    cam, up = cam_rig(ctx, ((0, -5, 32), (38, 0, 0), 32), ((0, -15, 8), (74, 0, 0), 40))
    def upd(f, t, u):
        up(u)
        for i, p in enumerate(ppl): bob(p, t, 0, 0.08, 5, i)
    return upd
def p02(ctx):  # travelling lateral junto a la gente (más separados)
    city(ctx, "gris"); ppl = []
    for i in range(8): ppl.append(vecino(ctx, i, (-11.2 + i * 3.2, 0, 0), 0.25 * (-1) ** i, name="b%d" % i))
    cam, up = cam_rig(ctx, ((-11, -13, 2.8), (90, 0, -8), 45), ((10, -13, 2.8), (90, 0, 8), 45))
    return lambda f, t, u: (up(u), [bob(p, t, 0, 0.06, 4, i) for i, p in enumerate(ppl)])
def p04(ctx):  # aereo: ciudad de neones, fuentes y confeti (orbita)
    city(ctx, "gris"); conf = confeti(ctx, 150, 8, ((-16, 16), (-6, 20), (2, 22)))
    for i, (x, y, c) in enumerate(((-8, 6, "#FF2E88"), (-3, 9, "#18E0FF"), (3, 5, "#FFE500"), (8, 8, "#2BFF88"))): globo(ctx, (x, y, 5 + i % 2), c)
    for i, (x, y) in enumerate(scatter(10, (-9, 9), (-2, 12), 2.8, 3)): vecino(ctx, i, (x, y, 0), random.Random(i).uniform(-3, 3), name="d%d" % i)
    cam, up = cam_rig(ctx, ((-24, -34, 30), (0, 0, 0), 28), ((24, -34, 30), (0, 0, 0), 28))
    def upd(f, t, u):
        up(u, look=(0, 14, 5)); confeti_update(conf, t)
    return upd
def p06(ctx):  # el alcalde de espaldas cruza una puerta de verdad (fachada con hueco), solo se ve el traje
    city(ctx, "gris")
    for sx in (-1, 1): box(ctx, "fachada", (sx * 8.0, 9.5, 5), (11, 1.0, 10), "#5B5F69", 0.8)
    box(ctx, "dintel", (0, 9.5, 8.6), (5, 1.0, 2.8), "#5B5F69", 0.8)
    for sx in (-1, 1): box(ctx, "jamba", (sx * 2.2, 9.5, 3.6), (0.4, 1.2, 7.2), "#D9A23F", 0.4)
    box(ctx, "luz interior", (0, 12.5, 3.6), (4.2, 0.1, 7.2), "#FFC86B", 0.4, 3.0)
    box(ctx, "umbral", (0, 11.0, 0.02), (4.2, 4.0, 0.06), "#E8C77A", 0.5, 0.6)
    a = alcalde(ctx, (0, 0, 0), math.radians(180), "smug", 8, hat=False)
    cam, up = cam_rig(ctx, ((0.8, -10, 3.2), (92, 0, 0), 50), ((0.3, -3.5, 3.2), (92, 0, 0), 50))
    def upd(f, t, u):
        up(u); a.location.y = lerp(0, 10.3, smooth(u)); walk("Alcalde", a, t, 2.4, 22); bob(a, t, 0, 0.08, 4.8)
    return upd
def p08(ctx):  # la gente hipnotizada mirando la pantalla gigante (sin solapes)
    city(ctx, "gris")
    for i, (x, y) in enumerate(scatter(12, (-7, 7), (-1, 9), 2.6, 2)):
        vecino(ctx, i, (x, y, 0), math.radians(180) + random.Random(i).uniform(-0.3, 0.3), name="g%d" % i, face="neutral")
    cam, up = cam_rig(ctx, ((0, 17, 2.6), (92, 0, 180), 40), ((0, 14, 3.0), (95, 0, 180), 50))
    d = bpy.data.lights.new("luz pantalla", 'AREA'); d.energy = 12000; d.size = 10; d.color = lin("#18E0FF")[:3]
    o = bpy.data.objects.new("luz pantalla", d); o.location = (3, 20, 6); o.rotation_euler = (math.radians(80), 0, math.radians(180)); ctx.col.objects.link(o)
    return lambda f, t, u: up(u)

def armario(ctx, x, y):
    """Armario de madera mirando a -Y: cuerpo, estante, barra con perchas vacías, telarañas y puertas abiertas con bisagra."""
    W, D, H = 4.4, 2.0, 8.0; mad, mad2 = "#6B4A32", "#7A5638"
    box(ctx, "fondo", (x, y + D / 2 - 0.08, H / 2), (W, 0.16, H), "#3A281A", 0.9)
    for sx in (-1, 1): box(ctx, "lado", (x + sx * (W / 2 - 0.1), y, H / 2), (0.2, D, H), mad, 0.8)
    box(ctx, "techo", (x, y, H - 0.1), (W, D, 0.2), mad, 0.8); box(ctx, "base", (x, y, 0.3), (W, D, 0.6), mad, 0.8)
    box(ctx, "estante", (x, y + 0.1, 5.3), (W - 0.4, D - 0.3, 0.14), mad2, 0.8)
    cyl(ctx, "barra", (x, y, 7.1), 0.07, W - 0.4, "#D9A23F", 0.3, rot=(0, math.radians(90), 0))
    for k in range(3): box(ctx, "percha", (x - 1.0 + k * 1.0, y, 6.75), (0.55, 0.05, 0.4), "#D9A23F", 0.3, rot=(0, 0, 0))
    for k, (dx, dz, ln, ang) in enumerate(((0.0, 0.0, 1.2, 0.0), (0.0, 0.0, 1.0, 0.8), (0.0, 0.0, 1.0, -0.8), (0.4, -0.3, 0.8, 0.4))):
        box(ctx, "tela", (x - W / 2 + 0.35 + dx + math.sin(ang) * ln / 2, y - D / 2 + 0.3, H - 0.4 + dz - math.cos(ang) * ln / 2), (0.025, 0.02, ln), "#F7F4EE", 0.8, rot=(0, ang, 0))
    for sx in (-1, 1):  # puertas abiertas hacia fuera, pivotando en el borde delantero
        piv = empty(ctx, "bisagra", (x + sx * W / 2, y - D / 2, 0), (0, 0, math.radians(-65 * sx)))
        box(ctx, "puerta", (-sx * 1.1, -0.0, H / 2), (2.2, 0.16, H - 0.1), mad2, 0.8, parent=piv)
        box(ctx, "tirador", (-sx * 1.9, -0.14, H / 2), (0.1, 0.1, 0.5), "#D9A23F", 0.3, parent=piv)
def p11(ctx):  # armario abierto, vacío y con telarañas; nadie lo mira (gente separada del armario)
    city(ctx, "gris"); armario(ctx, 0.8, 3.0)
    p = vecino(ctx, 2, (-3.4, -1.5, 0), math.radians(-15), name="i0", face="neutral")
    moth = box(ctx, "polilla", (0.8, 2.0, 6.0), (0.3, 0.05, 0.2), "#CFCFD4", 0.6)
    cam, up = cam_rig(ctx, ((-1.0, -16, 3.8), (91, 0, 0), 34), ((-0.6, -12.5, 4.0), (91, 0, 0), 36))
    def upd(f, t, u):
        up(u); moth.location = (0.8 + math.sin(t * 3) * 1.2, 1.9, 6.2 + math.cos(t * 4) * 0.6); moth.scale = (1, 1, 1 + 0.9 * math.sin(t * 40))
        bob(p, t, 0, 0.03, 3, 0)
    return upd
def p12(ctx):  # de noche: el alcalde sale con gabardina; Soclo lo sigue pegado a una pared que NO atraviesan
    city(ctx, "noche"); box(ctx, "pared", (0, 6.0, 4), (36, 0.6, 8), "#3A3D47", 0.8)
    s = soclo(ctx, (-9, 4.7, 0), math.radians(0), "A", "neutral", phone=False)
    a = alcalde(ctx, (-9, 1.2, 0), math.radians(-90), "smug", 8, hat=True); box(ctx, "gabardina", (0, 0.05, 2.0), (1.45, 0.9, 2.5), "#A0845C", 0.8, parent=a)
    d = bpy.data.lights.new("farola", 'POINT'); d.energy = 9000; d.color = lin("#FFD27A")[:3]
    o = bpy.data.objects.new("farola", d); o.location = (0, 2, 7); ctx.col.objects.link(o)
    cam, up = cam_rig(ctx, ((0, -13, 2.8), (92, 0, 0), 35))
    def upd(f, t, u):
        mx = lerp(-7, 7, u); a.location.x = mx; walk("Alcalde", a, t, 2.2, 22); bob(a, t, 0, 0.08, 4.4)
        s.location.x = mx - 5.0; walk("Soclo", s, t, 1.6, 10)
        cam.location = (mx * 0.5 - 2, -13, 2.8); cam.rotation_euler = (Vector((mx * 0.5 - 2, 3, 3.2)) - cam.location).to_track_quat('-Z', 'Y').to_euler()
    return upd
def p13(ctx):  # puerta secreta tras la estatua: el alcalde entra al vestidor por un hueco real
    city(ctx, "gris"); vestidor(ctx, 34)
    for sx in (-1, 1): box(ctx, "muro", (sx * 9.7, 25, 6), (10.6, 0.8, 12), "#2F3138", 0.7)
    box(ctx, "dintel", (0, 25, 10.5), (8.8, 0.8, 3), "#2F3138", 0.7)
    l = box(ctx, "puerta I", (-2.1, 24.3, 4.2), (4.2, 0.4, 8.4), "#4A4D55", 0.6); r_ = box(ctx, "puerta D", (2.1, 24.3, 4.2), (4.2, 0.4, 8.4), "#4A4D55", 0.6)
    person(ctx, "estatua", (-9, 16, 0), rot_z=math.radians(15), skin="#8B8E96", top="#8B8E96", pants="#8B8E96", shoe_l="#8B8E96", hair="#8B8E96", hairstyle="slick", face_kind="smug", arm_r=160, scale=2.2)
    a = alcalde(ctx, (0, 15, 0), math.radians(180), "smug", 8, hat=False)
    cam, up = cam_rig(ctx, ((0, 6, 3.8), (92, 0, 0), 38))
    def upd(f, t, u):
        k = smooth(min(1, max(0, (f - 14) / 16.0))); l.location.x = -2.1 - 4.2 * k; r_.location.x = 2.1 + 4.2 * k
        my = lerp(15, 37, smooth(min(1, f / 72.0))); a.location.y = my; walk("Alcalde", a, t, 2.2, 20)
        cam.location = (0, my - 9.0, 3.8); cam.rotation_euler = (math.radians(92), 0, 0)
    return upd
def p16(ctx):  # Soclo asoma tras el alcalde, mirada de poker (zoom brusco a su cara)
    city(ctx, "gris"); vestidor(ctx, 34)
    alcalde(ctx, (-1.8, 27.5, 0), math.radians(180), "smug", 8, hat=True)
    soclo(ctx, (1.6, 30.5, 0), math.radians(-8), "C", "neutral", phone=False)
    cam, up = cam_rig(ctx, ((0.6, 18, 4.0), (91, 0, 0), 42), ((0.6, 18, 4.0), (91, 0, 0), 95))
    def upd(f, t, u):
        k = smooth(min(1, f / 12.0)); cam.data.lens = lerp(42, 95, k)
        tgt = Vector((lerp(0.4, 1.6, k), 30.5, lerp(3.4, 4.2, k)))
        cam.location = (0.6, 18, 4.0); cam.rotation_euler = (tgt - cam.location).to_track_quat('-Z', 'Y').to_euler(); shake(cam, f, 0.5 if f < 12 else 0.08)
    return upd
def p17(ctx):  # plano y contraplano en un solo encuadre: Soclo señala el espejo del alcalde
    city(ctx, "gris"); vestidor(ctx, 34)
    box(ctx, "espejo marco", (1.9, 33.3, 4.2), (5.0, 0.3, 8.0), "#D9A23F", 0.3); box(ctx, "espejo", (1.9, 33.1, 4.2), (4.4, 0.1, 7.4), "#BFEFFF", 0.1, 0.9)
    soclo(ctx, (-1.5, 27.0, 0), math.radians(12), "C", "neutral", point=95)
    alcalde(ctx, (1.9, 30.6, 0), math.radians(180), "smug", 8, hat=True)
    cam, up = cam_rig(ctx, ((0.2, 19.5, 3.9), (92, 0, 0), 32), ((0.4, 20.5, 3.9), (92, 0, 0), 36))
    return lambda f, t, u: up(u)
def p18(ctx):  # el alcalde, rojo de rabia, mirando a camara, pulsa el boton: confeti de ofertas y alarma
    city(ctx, "gris"); vestidor(ctx, 34)
    a = alcalde(ctx, (0, 27, 0), 0.0, "angry", 45, hat=True)
    box(ctx, "consola", (2.0, 25.6, 1.3), (1.6, 1.2, 1.2), "#2F3138", 0.5); cyl(ctx, "boton", (2.0, 25.6, 2.0), 0.35, 0.2, "#D62828", 0.3, emit=2)
    conf = confeti(ctx, 160, 3, ((-6, 6), (22, 30), (2, 14)), cols=("#FFE500", "#FF2E88", "#2BFF88"))
    d = bpy.data.lights.new("alarma", 'POINT'); d.color = (1, 0.05, 0.05); d.energy = 0
    lo = bpy.data.objects.new("alarma", d); lo.location = (0, 24, 9); ctx.col.objects.link(lo)
    cam, up = cam_rig(ctx, ((0.2, 18, 4.2), (91, 0, 0), 50), ((0.4, 19.4, 4.2), (91, 0, 0), 58))
    def upd(f, t, u):
        up(u); shake(cam, f, 0.9); lo.data.energy = 120000 * (0.5 + 0.5 * math.sin(t * 22)) ** 2
        confeti_update(conf, t * 1.6, 0.3, 14); a.location.z = abs(math.sin(t * 14)) * 0.12
    return upd
def p19(ctx):  # Soclo sobre la fuente con megafono; la ciudad se agolpa a su alrededor (orbita alta)
    city(ctx, "gris")
    cyl(ctx, "fuente", (0, 5, 1.0), 3.4, 2.0, "#D8D2C4", 0.5); cyl(ctx, "fuente2", (0, 5, 2.4), 2.0, 0.8, "#BFEFFF", 0.2)
    for i, (x, y) in enumerate(scatter(20, (-11, 11), (-4, 14), 2.6, 5, hole=(0, 5, 5.0))):
        vecino(ctx, i, (x, y, 0), mira_a(x, y, 0, 5), name="m%d" % i, face="shock")
    soclo(ctx, (0, 5, 2.8), math.radians(0), "C", "happy", point=150)
    cyl(ctx, "megafono", (-0.1, 4.1, 6.0), 0.5, 0.9, "#D9A23F", 0.3, rot=(math.radians(90), 0, 0), r2=0.15)
    cam, up = cam_rig(ctx, ((-15, -9, 8), (0, 0, 0), 32), ((15, -9, 8), (0, 0, 0), 32))
    return lambda f, t, u: up(u, look=(0, 5, 4.6))
def p22(ctx):  # la multitud empuja al alcalde por un pasillo libre hacia la rampa; cuenta atras
    city(ctx, "gris"); rk, fire = cohete(ctx, 0, 16)
    a = alcalde(ctx, (0, -3, 0), 0.0, "scared", 150, hat=True)
    ppl = []; base = []
    for i, (x, y) in enumerate(scatter(12, (-9, 9), (-12, -3.5), 2.8, 6, hole=(0, -3.5, 3.4))):
        ppl.append(vecino(ctx, i, (x, y, 0), math.radians(180), name="q%d" % i, face="shock")); base.append(y)
    nums = [text(ctx, "cuenta " + ch, ch, (0, -3.0, 9.0), 6.0, "#FFE500", emit=6, extrude=0.5) for ch in ("3", "2", "1")]
    cam, up = cam_rig(ctx, ((0, -22, 2.2), (96, 0, 0), 28), ((0, -22, 2.2), (96, 0, 0), 30))
    def upd(f, t, u):
        up(u); shake(cam, f, u * 1.2); a.location.y = lerp(-3, 5, u); walk("Alcalde", a, t, 2.0, 16)
        for p, b in zip(ppl, base): p.location.y = b + lerp(0, 7, u)
        for k, n in enumerate(nums): n.hide_render = not (int(f // 25) == k)
    return upd
def p25(ctx):  # la ciudad celebra: todos con el movil y el logo (sin solapes)
    city(ctx, "color"); cf = confeti(ctx, 140, 4, ((-12, 12), (-4, 14), (2, 20))); ppl = []
    for i, (x, y) in enumerate(scatter(12, (-8, 8), (-2, 10), 2.7, 5)):
        ppl.append(vecino(ctx, i, (x, y, 0), random.Random(i).uniform(-0.5, 0.5), "logo", name="s%d" % i, face="happy"))
    cam, up = cam_rig(ctx, ((0, -13, 4.4), (90, 0, 0), 38), ((0, -9, 3.8), (92, 0, 0), 42))
    def upd(f, t, u):
        up(u); confeti_update(cf, t, 0.2, 20)
        for i, p in enumerate(ppl): bob(p, t, 0, 0.3, 8, i)
    return upd
def p28(ctx):  # ciudad con looks variados y el logo; el boton queda por encima de las cabezas
    city(ctx, "color"); cf = confeti(ctx, 120, 9, ((-12, 12), (-4, 12), (2, 18))); ppl = []
    for i in range(6): ppl.append(final(ctx, i, (-6.5 + i * 2.6, 0, 0), 0.2 * (-1) ** i, name="z%d" % i))
    lg = logo_plane(ctx, "logo final", (0, 3, 13.0), 7.0, strength=2.2)
    bt = box(ctx, "boton", (0, 2.5, 7.4), (11.0, 0.4, 2.0), "#F7F4EE", 0.4, 0.5)
    tx = text(ctx, "Entra", "Entra en Socly Style", (0, 2.2, 7.4), 1.15, "#15140F", emit=0, extrude=0.05)
    cam, up = cam_rig(ctx, ((0, -22, 6.5), (90, 0, 0), 38), ((0, -18, 6.5), (90, 0, 0), 38))
    def upd(f, t, u):
        up(u); confeti_update(cf, t, 0.2, 18); k = smooth(min(1, max(0, (f - 18) / 18.0)))
        lg.scale = (k, k, k); bt.scale = (k, 1, k); tx.scale = (k, k, k)
        for i, p in enumerate(ppl): bob(p, t, 0, 0.12, 6, i)
    return upd

SHOTS.update({1: p01, 2: p02, 4: p04, 6: p06, 8: p08, 11: p11, 12: p12, 13: p13, 16: p16, 17: p17, 18: p18, 19: p19, 22: p22, 25: p25, 28: p28})
