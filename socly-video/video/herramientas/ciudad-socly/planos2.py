"""Planos 15 a 28 de «Ciudad Socly». Se carga desde escenas.py (comparte sus funciones)."""

def soclo(ctx, loc, rot=0.0, look="A", face="happy", phone=True, name="Soclo", scarf=False, point=None):
    if point is not None: phone = False
    def ex(c, r):
        if phone: phone_arm(c, r, "#F7F4EE" if look == "A" else "#15140F", S[1], "logo")
        if look == "A":
            for sx in (-1, 1): box(c, "bomber", (0.44 * sx, -0.4, 2.5), (0.42, 0.05, 1.2), "#F7F4EE", 0.7, parent=r)
            box(c, "bomber cintura", (0, 0.02, 1.88), (1.36, 0.84, 0.18), "#D9D5CC", 0.7, parent=r)
        if scarf:
            box(c, "bufanda", (0, 0, 3.38), (1.15, 0.95, 0.38), "#E3873F", 0.95, parent=r, bevel=True)
            box(c, "bufanda cola", (0.28, -0.5, 2.7), (0.34, 0.1, 1.1), "#E3873F", 0.95, parent=r, bevel=True)
        for sx in (-1, 1): box(c, "cinta", (0.2 * sx - 0.35, -0.46, 2.3), (0.14, 0.04, 1.2), "#D9A23F", 0.35, parent=r)
    if look == "A":
        kw = dict(top="#15140F", sleeve="#F7F4EE", pants="#3B4A63", shoe_l="#F7F4EE", sole="#D9A23F")
    else:
        kw = dict(top="#15140F", sleeve="#15140F", pants="#C9B79C", shoe_l="#5C3A28")
    return person(ctx, name, loc, rot_z=rot, skin=S[1], hair="#2A1B12", hairstyle="flat", face_kind=face, arm_r=point, extras=ex, **kw)

def cohete(ctx, RX=0.0, RY=14.0, rampa=True, z0=1.0):
    if rampa:
        box(ctx, "Rampa", (RX, RY, 0.5), (16, 16, 1.0), "#2A2B30", 0.7)
        for i in range(16): box(ctx, "Franja", (RX - 7.5 + i, RY - 8.02, 0.5), (0.5, 0.06, 1.0), "#FFE500" if i % 2 == 0 else "#15140F", 0.6)
        for sx in (-1, 1):
            box(ctx, "Torre sujecion", (RX + 6.2 * sx, RY + 2, 9.5), (1.3, 1.3, 17), "#C8372D", 0.55, bevel=True)
            for k in range(5): box(ctx, "Travesano", (RX + 4.4 * sx, RY + 2, 3 + k * 3.2), (3.6, 0.35, 0.35), "#C8372D", 0.55)
    rk = empty(ctx, "Cohete", (RX, RY, z0))
    cyl(ctx, "cuerpo", (0, 0, 9.5), 2.5, 19, "#F7F4EE", 0.35, parent=rk, verts=40)
    cyl(ctx, "morro", (0, 0, 21.5), 2.5, 5, "#C8372D", 0.35, parent=rk, verts=40, r2=0.05)
    cyl(ctx, "franja dorada", (0, 0, 18.4), 2.53, 0.9, "#D9A23F", 0.3, parent=rk, verts=40)
    cyl(ctx, "franja negra", (0, 0, 1.1), 2.53, 1.0, "#15140F", 0.5, parent=rk, verts=40)
    for k in range(3):
        a = k * 2 * math.pi / 3 + math.pi / 2
        box(ctx, "aleta", (math.cos(a) * 3.1, math.sin(a) * 3.1, 3.2), (0.35, 3.0, 5.0), "#15140F", 0.4, rot=(0, 0, a - math.pi / 2), parent=rk)
    cyl(ctx, "ventana marco", (0, -2.2, 15.2), 1.15, 0.5, "#D9A23F", 0.3, rot=(math.radians(90), 0, 0), parent=rk)
    cyl(ctx, "ventana", (0, -2.35, 15.2), 0.95, 0.3, "#18E0FF", 0.15, emit=2.5, rot=(math.radians(90), 0, 0), parent=rk)
    box(ctx, "alcalde cabeza", (0, -2.55, 15.0), (1.0, 0.3, 1.0), "#F2C9A0", 0.6, parent=rk)
    for sx in (-1, 1): box(ctx, "ojo", (0.25 * sx, -2.72, 15.1), (0.16, 0.03, 0.2), "#15140F", 0.9, parent=rk)
    cyl(ctx, "casco", (0, -2.55, 15.55), 0.62, 0.5, "#D9A23F", 0.3, parent=rk)
    for (zz, ang) in ((11.2, 0), (6.0, 0), (11.2, 70), (11.2, -70)):
        a = math.radians(ang); logo_plane(ctx, "logo cohete", (math.sin(a) * 2.52, -math.cos(a) * 2.52, zz), 3.0, rot=(0, 0, a), parent=rk, strength=1.4)
    for i in range(70):
        a = i * 0.28 + 1.9; z = 2.4 + i * 0.2
        box(ctx, "cinta espiral", (math.cos(a) * 2.53, math.sin(a) * 2.53, z), (0.55, 0.1, 0.45), "#D9A23F", 0.3, 0.8, rot=(0, 0, a + math.pi / 2), parent=rk)
    fire = []
    for (c, r, h) in (("#FFE500", 1.9, 1.6), ("#FF7A00", 1.5, 1.9), ("#FF2E88", 1.0, 2.3)):
        fire.append((cyl(ctx, "fuego", (RX, RY, 0.4), r, h, c, 0.3, emit=2.6, rot=(math.radians(180), 0, 0), r2=0.05), h))
    return rk, fire

def p15(ctx):  # la app: armario y looks (marcador 3D de la grabacion real)
    city(ctx, "gris"); vestidor(ctx, 34)
    box(ctx, "movil", (0, 12, 4), (3.0, 0.2, 5.6), "#15140F", 0.3); box(ctx, "pant", (0, 11.88, 4), (2.7, 0.02, 5.2), "#F7F4EE", 0.5, 0.6)
    cards = [box(ctx, "tarjeta", (-0.7 + (i % 2) * 1.4, 11.84, 5.4 - (i // 2) * 1.5), (1.2, 0.02, 1.35), c, 0.6, 0.5)
             for i, c in enumerate(["#E3873F", "#3B4A63", "#F3E9D2", "#2B6CB0", "#C8372D", "#D8CBB6"])]
    cam, up = cam_rig(ctx, ((0, 4, 4.2), (90, 0, 0), 45), ((0, 7.5, 4.6), (90, 0, 0), 55))
    def upd(f, t, u):
        up(u)
        for i, c in enumerate(cards): c.location.y = 11.84 - (0.06 if f >= 12 + i * 8 else 0)
    return upd
def p16(ctx):  # Soclo asoma tras el alcalde, mirada de poker (zoom brusco)
    city(ctx, "gris"); vestidor(ctx, 34); alcalde(ctx, (-2.2, 24, 0), math.radians(180), "smug", 8, hat=True)
    soclo(ctx, (0.6, 27, 0), math.radians(-15), "C", "neutral", phone=False)
    cam, up = cam_rig(ctx, ((0.8, 18, 4.4), (91, 0, 0), 50), ((0.8, 18, 4.4), (91, 0, 0), 95))
    def upd(f, t, u):
        up(min(1, f / 12.0)); shake(cam, f, 0.6 if f < 12 else 0.1)
    return upd
def p17(ctx):  # plano y contraplano: Soclo señala la ciudad / el espejo del alcalde
    city(ctx, "gris"); vestidor(ctx, 34)
    soclo(ctx, (0, 24, 0), math.radians(10), "C", "neutral", point=95)
    box(ctx, "espejo marco", (7, 36, 5), (7.4, 0.5, 9.4), "#D9A23F", 0.3); box(ctx, "espejo", (7, 35.7, 5), (6.6, 0.1, 8.6), "#BFEFFF", 0.1, 0.9)
    alcalde(ctx, (7, 31, 0), 0.0, "smug", 8, hat=True)
    cam, up = cam_rig(ctx, ((2, 17, 3.8), (92, 0, 0), 55))
    cam2, up2 = cam_rig(ctx, ((7, 22, 3.8), (92, 0, 0), 45), ((7, 24, 3.8), (92, 0, 0), 50))
    def upd(f, t, u):
        ctx.sc.camera = cam if f < 37 else cam2
        if f < 37: cam.location = (0.1 + 0.4 * f / 37, 17, 3.8)
        else: up2((f - 37) / 38.0)
    return upd
def p18(ctx):  # el alcalde, rojo de rabia, pulsa el boton: confeti de ofertas y alarma
    city(ctx, "gris"); vestidor(ctx, 34)
    a = alcalde(ctx, (0, 26, 0), math.radians(185), "angry", 40, hat=True)
    box(ctx, "consola", (-1.6, 24.3, 1.6), (1.6, 1.2, 1.4), "#2F3138", 0.5); cyl(ctx, "boton", (-1.6, 24.3, 2.45), 0.35, 0.2, "#D62828", 0.3, emit=2)
    conf = confeti(ctx, 160, 3, ((-6, 6), (22, 30), (2, 14)), cols=("#FFE500", "#FF2E88", "#2BFF88"))
    d = bpy.data.lights.new("alarma", 'POINT'); d.color = (1, 0.05, 0.05); d.energy = 0
    lo = bpy.data.objects.new("alarma", d); lo.location = (0, 27, 9); ctx.col.objects.link(lo)
    cam, up = cam_rig(ctx, ((0.2, 18, 4.2), (91, 0, 0), 55), ((0.4, 19.6, 4.2), (91, 0, 0), 62))
    def upd(f, t, u):
        up(u); shake(cam, f, 0.9); lo.data.energy = 120000 * (0.5 + 0.5 * math.sin(t * 22)) ** 2
        confeti_update(conf, t * 1.6, 0.3, 14); a.location.z = abs(math.sin(t * 14)) * 0.12
    return upd
def p19(ctx):  # Soclo sube a la fuente con megafono; la ciudad se agolpa (orbita)
    city(ctx, "gris"); cyl(ctx, "fuente", (0, 5, 0.5), 3.2, 1.0, "#D8D2C4", 0.5); cyl(ctx, "fuente2", (0, 5, 1.4), 1.8, 0.8, "#BFEFFF", 0.2)
    rnd = random.Random(5)
    for i in range(18):
        ang = i / 18 * 2 * math.pi; r = rnd.uniform(5, 8)
        vecino(ctx, i, (math.cos(ang) * r, 5 + math.sin(ang) * r, 0), ang - math.pi / 2, name="m%d" % i, face="shock")
    soclo(ctx, (0, 5, 1.8), math.radians(180), "C", "happy", point=150)
    cyl(ctx, "megafono", (0.6, 4.1, 5.1), 0.55, 0.9, "#D9A23F", 0.3, rot=(math.radians(90), 0, 0), r2=0.15)
    cam, up = cam_rig(ctx, ((-14, -8, 4.5), (0, 0, 0), 32), ((14, -8, 4.5), (0, 0, 0), 32))
    return lambda f, t, u: up(u, look=(0, 5, 4.2))
def p20(ctx):  # primer plano: Soclo señala al alcalde con el megafono
    city(ctx, "gris"); soclo(ctx, (0, 0, 0), math.radians(-20), "C", "angry", point=130)
    cyl(ctx, "megafono", (0.55, -0.9, 3.7), 0.5, 0.9, "#D9A23F", 0.3, rot=(math.radians(90), 0, 0), r2=0.14)
    cam, up = cam_rig(ctx, ((0.2, -7.6, 3.9), (92, 0, 0), 60), ((0.3, -6.0, 3.9), (92, 0, 0), 75))
    return lambda f, t, u: up(u)
def p21(ctx):  # montaje: miran su ropa, al alcalde, se miran entre si
    city(ctx, "gris"); rnd = random.Random(8); grp = []
    for i in range(5): grp.append(vecino(ctx, i, (-4.4 + i * 2.2, 0, 0), rnd.uniform(-0.4, 0.4), name="n%d" % i, face="shock"))
    cuts = [(0, 25, ((0, -9, 2.6), (84, 0, 0), 40)), (25, 50, ((-2, -8, 3.6), (92, 0, -10), 55)), (50, 75, ((1.5, -6.5, 3.8), (92, 0, 6), 70))]
    cam, up = cam_rig(ctx, cuts[0][2])
    def upd(f, t, u):
        for (a, b, c) in cuts:
            if a <= f < b: cam.location = c[0]; cam.rotation_euler = tuple(math.radians(v) for v in c[1]); cam.data.lens = c[2]
        for i, p in enumerate(grp):
            p.rotation_euler.z = math.radians(10 * (i - 2)) if f < 25 else (math.radians(-70) if f < 50 else math.radians(60 * (1 if i % 2 else -1)))
    return upd
def p22(ctx):  # la multitud empuja al alcalde a la rampa; cuenta atras 3, 2, 1
    city(ctx, "gris"); rk, fire = cohete(ctx, 0, 16)
    a = alcalde(ctx, (0, -2, 0), math.radians(180), "scared", 150, hat=True)
    rnd = random.Random(6); ppl = []
    for i in range(10): ppl.append(vecino(ctx, i, (rnd.uniform(-5, 5), rnd.uniform(-9, -3), 0), math.radians(180), name="q%d" % i, face="shock"))
    base = [p.location.y for p in ppl]; nums = []
    for ch in ("3", "2", "1"):
        n = text(ctx, "cuenta " + ch, ch, (0, -2.5, 8.5), 6.0, "#FFE500", emit=6, extrude=0.5); nums.append(n)
    cam, up = cam_rig(ctx, ((0, -22, 2.2), (96, 0, 0), 28), ((0, -22, 2.2), (96, 0, 0), 30))
    def upd(f, t, u):
        up(u); shake(cam, f, u * 1.2); a.location.y = lerp(-2, 4, u); walk("Alcalde", a, t, 2.0, 16)
        for p, b in zip(ppl, base): p.location.y = b + lerp(0, 6, u)
        for k, n in enumerate(nums): n.hide_render = not (int(f // 25) == k)
    return upd
def p23(ctx):  # despegue con el alcalde resignado en la ventana
    city(ctx, "gris"); rk, fire = cohete(ctx, 0, 14)
    rnd = random.Random(1); smoke = []
    for i in range(30):
        ang = rnd.uniform(0, 2 * math.pi); d_ = rnd.uniform(2.5, 8.5); s_ = rnd.uniform(1.0, 2.6)
        o = sphere(ctx, "humo", (math.cos(ang) * d_, 14 - 1 + math.sin(ang) * d_ * 0.7, 1.4 + s_ * 0.4), s_, rnd.choice(["#E6E6EA", "#9C9CA4", "#F7F4EE"]), 0.95)
        o["b"] = list(o.location); smoke.append(o)
    ppl = [vecino(ctx, i, (x, -6, 0), 0.0, name="r%d" % i, face="shock") for i, x in enumerate((-6, -3, 3.5, 6.8))]
    d = bpy.data.lights.new("fuego luz", 'POINT'); d.color = (1, .45, .1); d.energy = 0
    lo = bpy.data.objects.new("fuego luz", d); ctx.col.objects.link(lo)
    cam, up = cam_rig(ctx, ((0, -22, 1.6), (101, 0, 0), 28))
    def upd(f, t, u):
        tl = max(0.0, (f - 15) / 30.0); rz = 1.0 + 0.5 * 19 * tl * tl; rk.location.z = rz
        r2 = random.Random(f * 7 + 1); s2 = 1.0 + tl * 2.2
        for i, (o, h) in enumerate(fire):
            k = s2 * (0.85 + 0.3 * r2.random()); o.scale = (1, 1, k if tl > 0 else 0.01); o.location = (0, 14, rz + 0.25 - h * k / 2)
        lo.location = (0, 12.5, rz - 1); lo.data.energy = 60000 * min(1, tl * 2)
        for i, o in enumerate(smoke):
            b = o["b"]; g = 1 + 0.9 * min(tl / 1.5, 1); ang = math.atan2(b[1] - 14, b[0])
            o.location = (b[0] + math.cos(ang) * 1.1 * tl, b[1] + math.sin(ang) * 1.1 * tl, b[2] + 0.6 * tl * ((i % 3) + 1) / 3); o.scale = (g, g, g)
        for i, p in enumerate(ppl): bob(p, t, 0, 0.45 if tl > 0 else 0.05, 9, i)
        pitch = min(90 + math.degrees(math.atan2(rz * 0.55 + 4 - 1.6, 22)), 122) if tl > 0 else 101
        cam.location = (0, -22, 1.6); cam.rotation_euler = (math.radians(pitch), 0, 0); shake(cam, f, min(1, tl * 2))
    return upd
def p24(ctx):  # el cohete de Socly Style cruza el cielo hacia Marte
    w = bpy.data.worlds.new("espacio"); ctx.sc.world = w; w.use_nodes = True
    w.node_tree.nodes["Background"].inputs["Color"].default_value = lin("#07061A"); w.node_tree.nodes["Background"].inputs["Strength"].default_value = 1.0
    rnd = random.Random(2)
    for i in range(160): sphere(ctx, "estrella", (rnd.uniform(-60, 60), 80, rnd.uniform(-40, 70)), rnd.uniform(0.1, 0.35), "#FFFFFF", 0.5, 4)
    sphere(ctx, "Marte", (22, 60, 8), 14, "#B5543A", 0.9)
    for i in range(14):
        a = rnd.uniform(0, 6.28); b = rnd.uniform(-0.6, 0.6)
        sphere(ctx, "crater", (22 + 14 * math.cos(a) * math.cos(b) * 0.99, 60 - 14 * abs(math.sin(a)) * 0.99, 8 + 14 * math.sin(b)), rnd.uniform(0.8, 1.8), "#8F3F2A", 0.95)
    rk, fire = cohete(ctx, 0, 0, rampa=False, z0=0); rk.scale = (0.35, 0.35, 0.35)
    for (o, h) in fire: o.parent = rk; o.location = (0, 0, -0.4); o.scale = (1, 1, 2.0)
    d = bpy.data.lights.new("sol espacio", 'SUN'); d.energy = 5.0; d.color = (1, .9, .8)
    lo = bpy.data.objects.new("sol espacio", d); lo.rotation_euler = (math.radians(60), 0, math.radians(30)); ctx.col.objects.link(lo)
    cam, up = cam_rig(ctx, ((0, -24, 14), (90, 0, 0), 35))
    def upd(f, t, u):
        rk.location = (lerp(-14, 12, u), 10, lerp(-10, 14, u)); rk.rotation_euler = (0, math.radians(-35), 0); up(u)
    return upd
def p25(ctx):  # la ciudad celebra: todos sacan el movil y se descargan la app
    city(ctx, "color"); cf = confeti(ctx, 140, 4, ((-12, 12), (-4, 14), (2, 20))); rnd = random.Random(5); ppl = []
    for i in range(14): ppl.append(vecino(ctx, i, (rnd.uniform(-8, 8), rnd.uniform(-2, 10), 0), rnd.uniform(-0.5, 0.5), "logo", name="s%d" % i, face="happy"))
    cam, up = cam_rig(ctx, ((0, -13, 4.4), (90, 0, 0), 38), ((0, -9, 3.8), (92, 0, 0), 42))
    def upd(f, t, u):
        up(u); confeti_update(cf, t, 0.2, 20)
        for i, p in enumerate(ppl): bob(p, t, 0, 0.3, 8, i)
    return upd
def p26(ctx):  # montaje: cada uno se viste a su manera
    city(ctx, "color")
    walls = ["#F2A65A", "#7AC7B8", "#F4D35E", "#E58B8B", "#8C8FB5"]; ppl = []
    for k in range(5):
        box(ctx, "fondo %d" % k, (60 * k, 8, 6), (14, 0.5, 12), walls[k], 0.6); box(ctx, "suelo %d" % k, (60 * k, 0, 0.01), (14, 14, 0.05), "#EDE6D8", 0.7)
        ppl.append(final(ctx, k + (1 if k > 3 else 0), (60 * k, 0, 0), 0.25 * (-1) ** k, name="u%d" % k))
    cam, up = cam_rig(ctx, ((0, -9, 3.2), (92, 0, 0), 50))
    def upd(f, t, u):
        k = min(4, int(f // 15)); cam.location = (60 * k, -9 + (f % 15) * 0.05, 3.2); cam.rotation_euler = (math.radians(92), 0, 0)
        for j, p in enumerate(ppl): p.rotation_euler.z = math.radians(15 * (-1) ** j) + (math.radians(25) * math.sin((f % 15) / 15 * math.pi) if j == k else 0)
    return upd
def p27(ctx):  # Soclo, cara seria, a camara (bufanda)
    city(ctx, "color"); soclo(ctx, (0, 0, 0), math.radians(-6), "A", "neutral", phone=True, scarf=True)
    cam, up = cam_rig(ctx, ((0.1, -8.4, 3.7), (92, 0, 0), 60), ((0.1, -8.4, 3.7), (92, 0, 0), 90))
    return lambda f, t, u: up(u)
def p28(ctx):  # ciudad con looks variados y el logo
    city(ctx, "color"); cf = confeti(ctx, 120, 9, ((-12, 12), (-4, 12), (2, 18))); ppl = []
    for i in range(6): ppl.append(final(ctx, i, (-6.5 + i * 2.6, 0, 0), 0.2 * (-1) ** i, name="z%d" % i))
    lg = logo_plane(ctx, "logo final", (0, 3, 9.5), 7.0, strength=2.2)
    bt = box(ctx, "boton", (0, 2.5, 4.6), (8.5, 0.4, 1.6), "#F7F4EE", 0.4, 0.5)
    tx = text(ctx, "Entra", "Entra en Socly Style", (0, 2.2, 4.6), 0.9, "#15140F", emit=0, extrude=0.05)
    cam, up = cam_rig(ctx, ((0, -22, 5.5), (90, 0, 0), 38), ((0, -18, 5.5), (90, 0, 0), 38))
    def upd(f, t, u):
        up(u); confeti_update(cf, t, 0.2, 18); k = smooth(min(1, max(0, (f - 18) / 18.0)))
        lg.scale = (k, k, k); bt.scale = (k, 1, k); tx.scale = (k, k, k)
        for i, p in enumerate(ppl): bob(p, t, 0, 0.12, 6, i)
    return upd

SHOTS.update({15: p15, 16: p16, 17: p17, 18: p18, 19: p19, 20: p20, 21: p21, 22: p22, 23: p23, 24: p24, 25: p25, 26: p26, 27: p27, 28: p28})
