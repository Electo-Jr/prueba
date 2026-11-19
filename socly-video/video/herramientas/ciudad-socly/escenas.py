"""«Ciudad Socly»: plano a plano. Se ejecuta en segundo plano:
  blender -b --python escenas.py -- 1 14      (renderiza los planos 1 a 14)
Cada plano: 75 fotogramas (2,5 s, 30 fps) en despegue\\..\\planos\\sNN\\f_0000.png"""
import sys, math, random, time, os
import bpy
from mathutils import Vector
exec(open(r"/home/user/prueba/socly-video\video\herramientas\ciudad-socly\lib.py", encoding="utf-8").read())
S = SKINS
PLANOS = OUT + r"\planos"
N = 75
smooth = lambda u: u * u * (3 - 2 * u)
lerp = lambda a, b, u: a + (b - a) * u

# ------------------------------------------------------------------ reparto
def _cuadros(c, r, sc): phone_arm(c, r, "#FF7A00", S[1], sc); [box(c, "cuadro", (-0.4 + i * 0.4, -0.37, 2.0 + j * 0.45), (0.2, 0.03, 0.2), "#B84F00", 0.7, parent=r) for i in range(3) for j in range(3)]
def _neon(c, r, sc):
    phone_arm(c, r, "#18E0FF", S[2], sc)
    for k in range(3): box(c, "raya", (0, -0.37, 2.1 + k * 0.45), (1.22, 0.03, 0.14), "#FFFFFF", 0.6, parent=r)
    for sx in (-1, 1): box(c, "chaleco", (0.42 * sx, -0.38, 2.55), (0.4, 0.04, 1.25), "#FFE500", 0.6, 1.5, parent=r)
    box(c, "gafas", (0, -0.6, 4.02), (0.95, 0.05, 0.24), "#15140F", 0.2, parent=r)
def _doble(c, r, sc):
    phone_arm(c, r, "#FFFFFF", S[0], sc); cyl(c, "copa roja", (0, 0, 5.0), 0.5, 0.8, "#D62828", 0.5, parent=r)
    box(c, "gorra azul", (0, 0, 5.5), (1.2, 1.2, 0.3), "#2B6CB0", 0.6, parent=r, bevel=True)
    text(c, "-70%", "-70%", (0, -0.38, 2.6), 0.55, "#FF2E88", emit=2, parent=r)
def _bolsas(c, r, sc):
    phone_arm(c, r, "#C8372D", S[3], sc); box(c, "falda", (0, 0, 1.45), (1.55, 0.95, 0.75), "#1F8A4C", 0.8, parent=r, bevel=True)
    for (x, z, col) in ((-1.0, 1.9, "#FF2E88"), (-1.15, 1.3, "#FFE500"), (1.35, 1.7, "#18E0FF")): box(c, "bolsa", (x, -0.1, z), (0.7, 0.45, 0.8), col, 0.6, parent=r)
    box(c, "bolsa cabeza", (0, 0, 5.1), (0.9, 0.5, 0.8), "#8A3CFF", 0.6, rot=(0, 0, 0.15), parent=r)
def _pijama(c, r, sc):
    phone_arm(c, r, "#FFFFFF", S[1], sc)
    for k in range(4): box(c, "raya", (0, -0.37, 1.95 + k * 0.38), (1.22, 0.03, 0.13), "#3B6FD9", 0.7, parent=r)
    box(c, "abrigo piel", (0, 0.03, 2.8), (1.45, 0.9, 0.95), "#E58B8B", 0.95, parent=r, bevel=True)
    cyl(c, "gorro", (0, 0, 5.15), 0.6, 1.0, "#3B6FD9", 0.7, parent=r, r2=0.12); sphere(c, "borla", (0, 0, 5.75), 0.2, "#FFFFFF", 0.9, parent=r)
def _bloque(c, r, sc):
    phone_arm(c, r, "#2BFF88", S[2], sc)
    for sx in (-1, 1): box(c, "chaqueta", (0.52 * sx, -0.38, 2.5), (0.4, 0.04, 1.3), "#2BFF88", 0.7, parent=r)
    box(c, "corbata", (0, -0.4, 2.55), (0.17, 0.03, 0.95), "#FF2E88", 0.6, parent=r)
VEC = [
 (dict(skin=S[1], top="#FF7A00", pants="#FF2E88", shoe_l="#5C3A28", hair="#2A1B12", hairstyle="flat"), _cuadros),
 (dict(skin=S[2], top="#18E0FF", pants="#FF7A00", shoe_l="#F7F4EE", hair="#15140F", hairstyle="flat", shorts=True), _neon),
 (dict(skin=S[0], top="#15140F", sleeve="#FFFFFF", pants="#2BFF88", shoe_l="#D9C7A0", hair="#7A4A22", hairstyle="none"), _doble),
 (dict(skin=S[3], top="#C8372D", pants=S[3], shoe_l="#15140F", hair="#15140F", hairstyle="long"), _bolsas),
 (dict(skin=S[1], top="#FFFFFF", pants="#FFFFFF", shoe_l="#F4A6B8", hair="#A8683F", hairstyle="flat"), _pijama),
 (dict(skin=S[0], top="#FFE500", pants="#D62828", shoe_l="#E63946", shoe_r="#2B6CB0", hair="#FF2E88", hairstyle="crest"), _bloque),
]
def vecino(ctx, i, loc, rot=0.0, screen="ad", name=None, face="happy"):
    kw, fn = VEC[i % 6]
    return person(ctx, name or "vec%d_%d" % (i, random.randrange(10**6)), loc, rot_z=rot, face_kind=face, arm_r=None,
                  extras=lambda c, r: fn(c, r, screen), **kw)

def _f_clasico(c, r): phone_arm(c, r, "#7A7F8A", S[1], "logo"); box(c, "camisa", (0, -0.37, 2.9), (0.5, 0.03, 0.6), "#FFFFFF", 0.6, parent=r)
def _f_depor(c, r): phone_arm(c, r, "#2B6CB0", S[2], "logo"); box(c, "gorra", (0, 0, 4.62), (1.2, 1.2, 0.3), "#2B6CB0", 0.6, parent=r, bevel=True)
def _f_punk(c, r): phone_arm(c, r, "#15140F", S[0], "logo"); box(c, "camiseta roja", (0, -0.37, 2.4), (0.55, 0.03, 1.1), "#D62828", 0.6, parent=r)
def _f_min(c, r): phone_arm(c, r, "#D8CBB6", S[3], "logo")
def _f_vint(c, r): phone_arm(c, r, "#F3E9D2", S[1], "logo"); box(c, "falda midi", (0, 0, 1.4), (1.45, 0.9, 1.2), "#B5543A", 0.85, parent=r, bevel=True)
def _f_street(c, r): phone_arm(c, r, "#E3873F", S[0], "logo"); box(c, "sudadera", (0, 0, 2.5), (1.55, 0.85, 1.5), "#E3873F", 0.9, parent=r, bevel=True); box(c, "gorro", (0, 0, 4.65), (1.2, 1.2, 0.5), "#15140F", 0.9, parent=r, bevel=True)
FIN = [
 (dict(skin=S[1], top="#7A7F8A", pants="#15140F", shoe_l="#1B1B1F", hair="#2A1B12", hairstyle="flat"), _f_clasico),
 (dict(skin=S[2], top="#2B6CB0", pants="#2B6CB0", shoe_l="#F7F4EE", hair="#15140F", hairstyle="none"), _f_depor),
 (dict(skin=S[0], top="#15140F", pants="#3B4A63", shoe_l="#15140F", hair="#FF2E88", hairstyle="crest"), _f_punk),
 (dict(skin=S[3], top="#D8CBB6", pants="#EFE6D4", shoe_l="#F7F4EE", hair="#15140F", hairstyle="flat"), _f_min),
 (dict(skin=S[1], top="#F3E9D2", pants=S[1], shoe_l="#5C3A28", hair="#7A4A22", hairstyle="long"), _f_vint),
 (dict(skin=S[0], top="#6B7A3A", pants="#6B7A3A", shoe_l="#F7F4EE", hair="#2A1B12", hairstyle="none"), _f_street),
]
def final(ctx, i, loc, rot=0.0, name=None, face="happy"):
    kw, fn = FIN[i % 6]
    return person(ctx, name or "fin%d_%d" % (i, random.randrange(10**6)), loc, rot_z=rot, face_kind=face, arm_r=None, extras=fn, **kw)

def soclo(ctx, loc, rot=0.0, look="A", face="happy", phone=True, name="Soclo"):
    def ex(c, r):
        if phone: phone_arm(c, r, "#F7F4EE" if look == "A" else "#15140F", S[1], "logo")
        if look == "A":
            for sx in (-1, 1): box(c, "bomber", (0.44 * sx, -0.4, 2.5), (0.42, 0.05, 1.2), "#F7F4EE", 0.7, parent=r)
            box(c, "bomber cintura", (0, 0.02, 1.88), (1.36, 0.84, 0.18), "#D9D5CC", 0.7, parent=r)
        for sx in (-1, 1): box(c, "cinta", (0.2 * sx - 0.35, -0.46, 2.3), (0.14, 0.04, 1.2), "#D9A23F", 0.35, parent=r)
    if look == "A":
        kw = dict(top="#15140F", sleeve="#F7F4EE", pants="#3B4A63", shoe_l="#F7F4EE", sole="#D9A23F")
    else:  # C: americana negra sobre camiseta crema, pantalon beige, mocasines
        kw = dict(top="#15140F", sleeve="#15140F", pants="#C9B79C", shoe_l="#5C3A28")
    return person(ctx, name, loc, rot_z=rot, skin=S[1], hair="#2A1B12", hairstyle="flat", face_kind=face, arm_r=None, extras=ex, **kw)

def alcalde(ctx, loc, rot=0.0, face="smug", arm_r=8, hat=True):
    return make_alcalde(ctx, loc, rot_z=rot, face_kind=face, arm_r=arm_r, with_hat=hat)

def walk(name, root, t, speed=2.4, amp=28):
    rig = RIG.get(name)
    if not rig: return
    s = math.sin(t * speed * 2)
    rig["hip"][0].rotation_euler.x = math.radians(amp) * s
    rig["hip"][1].rotation_euler.x = -math.radians(amp) * s
    if rig["arm"][0]: rig["arm"][0].rotation_euler.x = -math.radians(amp * 0.8) * s

def bob(root, t, base_z=0.0, a=0.1, sp=4.0, ph=0.0):
    root.location.z = base_z + abs(math.sin(t * sp + ph)) * a

# ------------------------------------------------------------------ props
def confeti(ctx, n, seed, area, cols=("#FF2E88", "#FFE500", "#18E0FF", "#2BFF88", "#FF7A00")):
    rnd = random.Random(seed); out = []
    for i in range(n):
        o = box(ctx, "confeti", (rnd.uniform(*area[0]), rnd.uniform(*area[1]), rnd.uniform(*area[2])), (0.25, 0.04, 0.4), rnd.choice(cols), 0.5, 2.0)
        out.append((o, rnd.uniform(1.5, 4.0), rnd.uniform(-6, 6), rnd.uniform(-1, 1)))
    return out
def confeti_update(items, t, zmin=0.2, zmax=22):
    for o, vz, spin, dx in items:
        b = o.get("b0")
        if b is None: o["b0"] = list(o.location); b = o["b0"]
        z = b[2] - vz * t
        z = zmin + ((z - zmin) % (zmax - zmin))
        o.location = (b[0] + dx * t, b[1], z); o.rotation_euler = (spin * t, spin * t * 0.5, 0)

def globo(ctx, loc, hexc, r=0.9):
    sphere(ctx, "globo", loc, r, hexc, 0.3); cyl(ctx, "cuerda", (loc[0], loc[1], loc[2] - r - 1.2), 0.02, 2.4, "#F7F4EE", 0.5)

def poste_pantalla(ctx, loc, hexc="#FF2E88", s="OFERTA"):
    cyl(ctx, "poste", (loc[0], loc[1], 3.0), 0.18, 6, "#2F3138", 0.5)
    box(ctx, "pant marco", (loc[0], loc[1] - 0.1, 5.4), (3.2, 0.3, 3.8), "#15140F", 0.4)
    box(ctx, "pant", (loc[0], loc[1] - 0.28, 5.4), (2.9, 0.06, 3.5), hexc, 0.4, 1.3)
    text(ctx, "pant txt", s, (loc[0], loc[1] - 0.36, 5.4), 0.7, "#FFE500", emit=1.5)

def vestidor(ctx, y0=30.0):
    # el vestidor ocupa el hueco de la ciudad: se quitan los edificios, ventanas y carteles que estaban dentro
    for o in list(ctx.col.objects):
        if o.name.startswith(("Edificio", "Ventana", "Neon")) and abs(o.location.x) < 19 and (y0 - 12) < o.location.y < (y0 + 16):
            bpy.data.objects.remove(o, do_unlink=True)
    box(ctx, "v suelo", (0, y0, -0.05), (30, 18, 0.1), "#6A4A2A", 0.5)
    box(ctx, "v fondo", (0, y0 + 9, 6), (30, 0.3, 12), "#C9A24F", 0.4, 0.25)
    box(ctx, "v techo", (0, y0, 12), (30, 18, 0.3), "#3A2A1A", 0.7)
    for sx in (-1, 1): box(ctx, "v pared", (15 * sx, y0, 6), (0.3, 18, 12), "#B08A3E", 0.5, 0.1)
    cols = ["#FF2E88", "#18E0FF", "#FFE500", "#2BFF88", "#FF7A00", "#8A3CFF", "#F7F4EE", "#1F2A4D"]
    rnd = random.Random(2)
    for row, yy in enumerate((y0 + 6, y0 + 1)):
        box(ctx, "barra", (0, yy, 7.2), (24, 0.2, 0.2), "#D9A23F", 0.3)
        for i in range(14):
            x = -11 + i * 1.7
            box(ctx, "prenda", (x, yy, 5.7), (0.9, 0.18, 2.4), rnd.choice(cols), 0.8, parent=None)
            box(ctx, "percha", (x, yy, 7.0), (0.8, 0.06, 0.12), "#D9A23F", 0.3)
    d = bpy.data.lights.new("v luz", 'AREA'); d.energy = 16000; d.size = 18; d.color = lin("#FFC86B")[:3]
    o = bpy.data.objects.new("v luz", d); o.location = (0, y0 + 2, 11); o.rotation_euler = (0, 0, 0); ctx.col.objects.link(o)
    d2 = bpy.data.lights.new("v luz entrada", 'POINT'); d2.energy = 9000; d2.color = lin("#FFD9A0")[:3]
    o2 = bpy.data.objects.new("v luz entrada", d2); o2.location = (3, y0 - 12, 9); ctx.col.objects.link(o2)

# ------------------------------------------------------------------ ciudad y cámara
def city(ctx, mode="gris"):
    if mode == "color":
        build_city(ctx, seed=11, color_mix=0.7); lights(ctx, rosa=450, cian=350, relleno=700, sol=4.5, fachadas=30000); sky(ctx, 1.3)
        for o in list(ctx.col.objects):
            if o.name.startswith(("Pantalla fondo", "Pantalla franja", "Pantalla texto")): bpy.data.objects.remove(o, do_unlink=True)
        box(ctx, "Pantalla negra", (3.0, 23.65, 10.5), (12.2, 0.1, 6.8), "#15140F", 0.4)
        logo_plane(ctx, "Pantalla logo", (3.0, 23.55, 10.5), 6.2, strength=2.2)
    elif mode == "noche":
        build_city(ctx, seed=11); lights(ctx, rosa=250, cian=300, relleno=120, sol=0.2, fachadas=5000); sky(ctx, 0.35)
    else:
        build_city(ctx, seed=11); lights(ctx, rosa=700, cian=700, relleno=500, sol=3.0, fachadas=25000); sky(ctx, 1.1)
    box(ctx, "Plaza delantera", (0, -12, 0.02), (80, 34, 0.06), "#8B8E96", 0.7)

def cam_rig(ctx, a, b=None, lens=None):
    """a, b = (loc, rot_deg, lens). Devuelve función update(u) que mueve la cámara (u de 0 a 1, suavizado)."""
    cam = camera(ctx, a[0], a[1], a[2])
    cam.data.sensor_fit = 'HORIZONTAL'; cam.data.sensor_width = 36
    cam.data.sensor_fit = 'VERTICAL'
    b = b or a
    def upd(u, look=None):
        k = smooth(u)
        cam.location = tuple(lerp(a[0][i], b[0][i], k) for i in range(3))
        cam.rotation_euler = tuple(math.radians(lerp(a[1][i], b[1][i], k)) for i in range(3))
        cam.data.lens = lerp(a[2], b[2], k)
        if look is not None:
            cam.rotation_euler = (Vector(look) - cam.location).to_track_quat('-Z', 'Y').to_euler()
    return cam, upd

def shake(cam, f, amp, ph=0):
    r = random.Random(f * 13 + ph)
    cam.location.x += amp * 0.12 * (r.random() - 0.5) * 2; cam.location.z += amp * 0.1 * (r.random() - 0.5) * 2
    cam.rotation_euler.x += math.radians(amp * 0.5 * (r.random() - 0.5) * 2); cam.rotation_euler.z += math.radians(amp * 0.4 * (r.random() - 0.5) * 2)

def flash(ctx, f, frames=3):
    """Flash blanco: sube la intensidad del cielo los primeros fotogramas."""
    w = ctx.sc.world
    if w and w.use_nodes:
        bg = [n for n in w.node_tree.nodes if n.type == 'BACKGROUND'][0]
        bg.inputs["Strength"].default_value = 12.0 if f < frames else (bg.get("base_s", 1.1))

# ------------------------------------------------------------------ planos 1 a 14
def p01(ctx):  # plaza llena de bloques con looks absurdos, cenital que baja
    city(ctx, "gris"); rnd = random.Random(4); ppl = []
    for i in range(18):
        ppl.append(vecino(ctx, i, (rnd.uniform(-9, 9), rnd.uniform(-3, 11), 0), rnd.uniform(-2.5, 2.5), name="a%d" % i))
    cam, up = cam_rig(ctx, ((0, -5, 32), (38, 0, 0), 32), ((0, -15, 8), (74, 0, 0), 40))
    def upd(f, t, u):
        up(u)
        for i, p in enumerate(ppl): bob(p, t, 0, 0.08, 5, i)
    return upd
def p02(ctx):  # travelling lateral junto a la gente, cada uno peor
    city(ctx, "gris"); ppl = []
    for i in range(8): ppl.append(vecino(ctx, i, (-9 + i * 2.7, 0, 0), 0.25 * (-1) ** i, name="b%d" % i))
    cam, up = cam_rig(ctx, ((-9, -13, 2.8), (90, 0, -8), 45), ((8, -13, 2.8), (90, 0, 8), 45))
    return lambda f, t, u: (up(u), [bob(p, t, 0, 0.06, 4, i) for i, p in enumerate(ppl)])
def p03(ctx):  # Soclo cruza la plaza con su look, contrapicado en camara lenta
    city(ctx, "gris"); s = soclo(ctx, (-5, 0, 0), math.radians(70), "A")
    cam, up = cam_rig(ctx, ((-1, -9.5, 0.7), (101, 0, -3), 40), ((1, -9.5, 0.9), (99, 0, 3), 58))
    def upd(f, t, u):
        up(u); s.location.x = lerp(-5, 5, u); walk("Soclo", s, t * 0.6, 2.4, 24); bob(s, t * 0.6, 0, 0.1, 4.8)
    return upd
def p04(ctx):  # aereo: ciudad de neones, fuentes y confeti (orbita)
    city(ctx, "gris"); conf = confeti(ctx, 150, 8, ((-16, 16), (-6, 20), (2, 22)))
    for i, (x, y, c) in enumerate(((-8, 6, "#FF2E88"), (-3, 9, "#18E0FF"), (3, 5, "#FFE500"), (8, 8, "#2BFF88"))): globo(ctx, (x, y, 5 + i % 2), c)
    for i in range(10): vecino(ctx, i, (random.Random(i).uniform(-9, 9), random.Random(i + 9).uniform(-2, 12), 0), random.Random(i).uniform(-3, 3), name="d%d" % i)
    cam, up = cam_rig(ctx, ((-24, -34, 30), (0, 0, 0), 28), ((24, -34, 30), (0, 0, 0), 28))
    def upd(f, t, u):
        up(u, look=(0, 14, 5)); confeti_update(conf, t)
    return upd
def p05(ctx):  # bloques con looks ridiculos mirando a camara, cortes rapidos
    city(ctx, "gris"); ppl = [vecino(ctx, i, (-6.5 + i * 2.6, 0, 0), 0.0, name="e%d" % i, face="happy") for i in range(6)]
    cuts = [(0, 25, ((-4.2, -8, 3.4), (92, 0, 0), 55), 0), (25, 50, ((0.3, -8, 3.6), (92, 0, 0), 55), 2), (50, 75, ((3.8, -8, 3.4), (92, 0, 0), 55), 3)]
    cam, up = cam_rig(ctx, cuts[0][2])
    def upd(f, t, u):
        for (a, b, c, i) in cuts:
            if a <= f < b:
                cam.location = c[0]; cam.rotation_euler = tuple(math.radians(v) for v in c[1]); cam.data.lens = c[2] + (f - a) * 0.3
        for i, p in enumerate(ppl): bob(p, t, 0, 0.1, 6, i)
    return upd
def p06(ctx):  # el alcalde de espaldas, traje a medida, cruza una puerta
    city(ctx, "gris"); box(ctx, "marco puerta", (0, 9, 3.5), (5, 0.6, 7), "#2F3138", 0.5)
    box(ctx, "hueco puerta", (0, 9.2, 3.0), (3.4, 0.4, 6), "#FFC86B", 0.4, 2.0)
    a = alcalde(ctx, (0, 0, 0), math.radians(180), "smug", 8, hat=False)
    cam, up = cam_rig(ctx, ((0.8, -10, 3.2), (92, 0, 0), 50), ((0.2, -5.5, 3.2), (92, 0, 0), 50))
    def upd(f, t, u):
        up(u); a.location.y = lerp(0, 6.2, smooth(u)); walk("Alcalde", a, t, 2.4, 22); bob(a, t, 0, 0.08, 4.8)
    return upd
def p07(ctx):  # se gira: es el alcalde, guiña
    city(ctx, "gris"); a = alcalde(ctx, (0, 0, 0), math.radians(180), "smug", 8, hat=True)
    cam, up = cam_rig(ctx, ((0, -6.2, 4.6), (91, 0, 0), 85), ((0, -4.6, 4.6), (91, 0, 0), 85))
    eyes = [o for o in a.children_recursive if o.name.startswith("ojo")]
    def upd(f, t, u):
        up(u); k = smooth(min(1, f / 18)); a.rotation_euler.z = math.radians(lerp(180, 345, k))
        flash(ctx, f, 3)
        w = 1.0 if 46 <= f < 58 else 0.0
        for e in eyes:
            if e.location.x > 0: e.scale = (1, 1, 0.15 if w else 1)
    return upd
def p08(ctx):  # la gente hipnotizada mirando la pantalla gigante
    city(ctx, "gris"); rnd = random.Random(2)
    for i in range(14): vecino(ctx, i, (rnd.uniform(-7, 7), rnd.uniform(-1, 9), 0), math.radians(180) + rnd.uniform(-0.3, 0.3), name="g%d" % i, face="neutral")
    cam, up = cam_rig(ctx, ((0, 17, 2.6), (92, 0, 180), 40), ((0, 14, 3.0), (95, 0, 180), 50))
    d = bpy.data.lights.new("luz pantalla", 'AREA'); d.energy = 12000; d.size = 10; d.color = lin("#18E0FF")[:3]
    o = bpy.data.objects.new("luz pantalla", d); o.location = (3, 20, 6); o.rotation_euler = (math.radians(80), 0, math.radians(180)); ctx.col.objects.link(o)
    return lambda f, t, u: up(u)
def p09(ctx):  # montaje: pantallas en farolas, carteles de oferta, anuncios en autobuses
    city(ctx, "gris")
    poste_pantalla(ctx, (-5, 4), "#FF2E88", "SUPER OFERTA"); poste_pantalla(ctx, (5, 6), "#18E0FF", "-50%")
    box(ctx, "bus", (0, 10, 2.0), (14, 4.5, 4), "#2B6CB0", 0.5); box(ctx, "bus anuncio", (0, 7.7, 2.2), (11, 0.1, 2.4), "#FFE500", 0.4, 2.2)
    text(ctx, "bus txt", "TODO AL 70%", (0, 7.6, 2.2), 1.0, "#D62828", emit=1.5)
    cuts = [(0, 25, ((-5, -3, 5.2), (92, 0, 0), 55)), (25, 50, ((5, -2, 5.2), (92, 0, 8), 55)), (50, 75, ((0, 0, 2.4), (92, 0, -6), 40))]
    cam, up = cam_rig(ctx, cuts[0][2])
    def upd(f, t, u):
        for (a, b, c) in cuts:
            if a <= f < b:
                k = (f - a) / (b - a); cam.location = (c[0][0] + (k - 0.5) * 0.8, c[0][1] + k * 0.8, c[0][2]); cam.rotation_euler = tuple(math.radians(v) for v in c[1]); cam.data.lens = c[2]
    return upd
def p10(ctx):  # cupones, ruleta y notificaciones sobre las cabezas
    city(ctx, "gris"); ppl = [vecino(ctx, i, (-3.4 + i * 3.4, 0, 0), 0.0, name="h%d" % i, face="happy") for i in range(3)]
    cup = confeti(ctx, 90, 5, ((-8, 8), (-2, 4), (3, 20)), cols=("#FFE500", "#FF2E88", "#2BFF88"))
    bub = []
    for i in range(6):
        b = box(ctx, "notif", (-4 + i * 1.6, -0.8, 6.8 + (i % 2)), (1.0, 0.1, 0.6), "#FFFFFF", 0.4, 0.6); sphere(ctx, "punto", (-3.55 + i * 1.6, -0.88, 7.1 + (i % 2)), 0.18, "#D62828", 0.4, 1.5); bub.append(b)
    cam, up = cam_rig(ctx, ((0, -11, 4.2), (92, 0, 0), 45), ((0, -8.5, 4.4), (92, 0, 0), 55))
    def upd(f, t, u):
        up(u); confeti_update(cup, t, 0.3, 20)
        for i, b in enumerate(bub): b.location.z = 6.8 + (i % 2) + 0.25 * math.sin(t * 5 + i)
        for i, p in enumerate(ppl): bob(p, t, 0, 0.1, 6, i)
    return upd
def p11(ctx):  # armario abierto, vacio y con telarañas; nadie lo mira
    city(ctx, "gris"); box(ctx, "armario", (3.2, 3, 4), (4.2, 2.2, 8), "#5C3A28", 0.7)
    box(ctx, "interior", (3.2, 1.95, 4), (3.6, 0.1, 7.4), "#2A1B12", 0.9)
    for sx in (-1, 1): box(ctx, "puerta", (3.2 + sx * 2.9, 0.9, 4), (0.15, 2.2, 7.6), "#6B4A32", 0.7, rot=(0, 0, math.radians(35 * sx)))
    box(ctx, "barra", (3.2, 2.4, 7), (3.6, 0.1, 0.1), "#D9A23F", 0.3)
    for i in range(7): box(ctx, "tela", (1.6 + i * 0.5, 1.9, 7.3 - i * 0.3), (0.04, 0.02, 1.5 - i * 0.1), "#F7F4EE", 0.8, rot=(0, 0.4, 0))
    p = vecino(ctx, 2, (-1.2, -1.0, 0), math.radians(-20), name="i0", face="neutral")
    moth = box(ctx, "polilla", (3.0, 1.8, 5.0), (0.3, 0.05, 0.2), "#CFCFD4", 0.6)
    cam, up = cam_rig(ctx, ((-1, -15, 3.6), (91, 0, 0), 45), ((1.5, -10.5, 3.9), (91, 0, 0), 50))
    def upd(f, t, u):
        up(u); moth.location = (3.0 + math.sin(t * 3) * 1.4, 1.7, 5.0 + math.cos(t * 4) * 0.8); moth.scale = (1, 1, 1 + 0.9 * math.sin(t * 40))
    return upd
def p12(ctx):  # de noche: el alcalde sale con gabardina, Soclo lo sigue pegado a la pared
    city(ctx, "noche"); box(ctx, "pared", (-3.2, 3, 4), (0.6, 14, 8), "#3A3D47", 0.8)
    s = soclo(ctx, (-2.4, 4.6, 0), math.radians(-90), "A", "neutral", phone=False)
    a = alcalde(ctx, (-8, 0.5, 0), math.radians(90), "smug", 8, hat=True); box(ctx, "gabardina", (0, 0.05, 2.0), (1.45, 0.9, 2.5), "#A0845C", 0.8, parent=a)
    d = bpy.data.lights.new("farola", 'POINT'); d.energy = 9000; d.color = lin("#FFD27A")[:3]
    o = bpy.data.objects.new("farola", d); o.location = (-1, 1, 7); ctx.col.objects.link(o)
    cam, up = cam_rig(ctx, ((2, -8, 2.4), (92, 0, 8), 40), ((2.6, -8, 2.5), (92, 0, 14), 46))
    def upd(f, t, u):
        up(u); a.location.x = lerp(-8, 8, u); walk("Alcalde", a, t, 2.2, 22); bob(a, t, 0, 0.08, 4.4)
    return upd
def p13(ctx):  # puerta secreta tras la estatua: dentro, un vestidor enorme
    city(ctx, "gris"); vestidor(ctx, 34)
    for sx in (-1, 1): box(ctx, "muro", (sx * 9.7, 18, 6), (10.6, 0.8, 12), "#2F3138", 0.7)
    box(ctx, "dintel", (0, 18, 10.5), (9, 0.8, 3), "#2F3138", 0.7); l = box(ctx, "puerta I", (-2.2, 17.5, 4), (4.4, 0.5, 8), "#4A4D55", 0.6); r_ = box(ctx, "puerta D", (2.2, 17.5, 4), (4.4, 0.5, 8), "#4A4D55", 0.6)
    st = person(ctx, "estatua", (-9, 12, 0), rot_z=math.radians(10), skin="#8B8E96", top="#8B8E96", pants="#8B8E96", shoe_l="#8B8E96", hair="#8B8E96", hairstyle="slick", face_kind="smug", arm_r=160, scale=2.2)
    a = alcalde(ctx, (0, 12, 0), math.radians(180), "smug", 8, hat=False)
    cam, up = cam_rig(ctx, ((0, 4, 3.8), (92, 0, 0), 38))
    def upd(f, t, u):
        k = smooth(min(1, max(0, f / 16.0))); l.location.x = -2.2 - 4.4 * k; r_.location.x = 2.2 + 4.4 * k
        my = lerp(12, 44, smooth(min(1, f / 70.0))); a.location.y = my; walk("Alcalde", a, t, 2.2, 20)
        cam.location = (0, my - 8.5, 3.8); cam.rotation_euler = (math.radians(92), 0, 0)
    return upd
def p14(ctx):  # el movil del alcalde: Socly Style (sustituible por la grabacion real)
    city(ctx, "gris"); vestidor(ctx, 34)
    box(ctx, "movil", (0, 12, 4), (2.4, 0.2, 4.6), "#15140F", 0.3); logo_plane(ctx, "logo movil", (0, 11.88, 4), 2.1, strength=2.2)
    cam, up = cam_rig(ctx, ((0, 4, 4), (90, 0, 0), 50), ((0, 6.5, 4), (90, 0, 0), 50))
    return lambda f, t, u: up(u)

SHOTS = {1: p01, 2: p02, 3: p03, 4: p04, 5: p05, 6: p06, 7: p07, 8: p08, 9: p09, 10: p10, 11: p11, 12: p12, 13: p13, 14: p14}

exec(open(OUT + r"\planos2.py", encoding="utf-8").read())
exec(open(OUT + r"\planos3.py", encoding="utf-8").read())

def run(i):
    random.seed(i)
    ctx = Ctx("plano%02d" % i)
    upd = SHOTS[i](ctx)
    r = ctx.sc.render; r.engine = 'BLENDER_EEVEE'; r.resolution_x = 1080; r.resolution_y = 1920; r.resolution_percentage = 50
    ctx.sc.eevee.taa_render_samples = 20
    ctx.sc.view_settings.view_transform = 'AgX'; ctx.sc.view_settings.look = 'AgX - High Contrast'; ctx.sc.view_settings.exposure = 0.1
    d = PLANOS + "\\s%02d" % i; os.makedirs(d, exist_ok=True)
    t0 = time.time()
    frames = [int(x) for x in os.environ["SOCLY_FRAMES"].split(",")] if os.environ.get("SOCLY_FRAMES") else range(N)
    for f in frames:
        upd(f, f / 30.0, f / (N - 1))
        r.filepath = d + "\\f_%04d.png" % f
        bpy.ops.render.render(write_still=True)
    print("PLANO", i, "listo en", round(time.time() - t0), "s", flush=True)

if __name__ == "__main__":
    args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else ["1", "1"]
    a, b = int(args[0]), int(args[-1])
    for i in range(a, b + 1): run(i)
