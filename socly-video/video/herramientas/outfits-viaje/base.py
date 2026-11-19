"""Utilidades y decorados de «¿De dónde vienen los outfits?» (se carga con exec tras lib.py y trajes.py)."""
import bpy, math, random, os
from mathutils import Vector

rad = math.radians
smooth = lambda u: u * u * (3 - 2 * u)
lerp = lambda a, b, u: a + (b - a) * u


def fondo(ctx, hexc, fuerza=1.0):
    w = bpy.data.worlds.new("Fondo"); ctx.sc.world = w; w.use_nodes = True
    bg = w.node_tree.nodes["Background"]
    bg.inputs["Color"].default_value = lin(hexc); bg.inputs["Strength"].default_value = fuerza


def luz(ctx, nombre, tipo, loc, energia, hexc, rot=None, size=None):
    d = bpy.data.lights.new(nombre, tipo); d.energy = energia; d.color = lin(hexc)[:3]
    if size: d.size = size
    o = bpy.data.objects.new(nombre, d); o.location = loc
    if rot: o.rotation_euler = tuple(rad(a) for a in rot)
    ctx.col.objects.link(o); return o


def cam_rig(ctx, a, b=None, foco=None, f=2.8):
    """a, b = (loc, rot_deg, lens). foco = punto enfocado (desenfoque de fondo con apertura f). Devuelve (cam, upd(u, look=None))."""
    cam = camera(ctx, a[0], a[1], a[2]); b = b or a
    if foco is not None:
        cam.data.dof.use_dof = True; cam.data.dof.aperture_fstop = f
    def upd(u, look=None):
        k = smooth(u)
        cam.location = tuple(lerp(a[0][i], b[0][i], k) for i in range(3))
        cam.rotation_euler = tuple(rad(lerp(a[1][i], b[1][i], k)) for i in range(3))
        cam.data.lens = lerp(a[2], b[2], k)
        if look is not None: mira(cam, look)
        if foco is not None: cam.data.dof.focus_distance = max(0.5, (cam.location - Vector(foco)).length)
    return cam, upd


def mira(cam, target):
    cam.rotation_euler = (Vector(target) - cam.location).to_track_quat('-Z', 'Y').to_euler()


def bob(root, t, base_z=0.0, a=0.1, sp=4.0, ph=0.0):
    root.location.z = base_z + abs(math.sin(t * sp + ph)) * a


def brazo(nombre, lado, grados, extra=0.0):
    """Levanta un brazo: lado 'i' (izquierdo del personaje, sale hacia +X) o 'd'. grados: 0 = colgando, 90 = horizontal, 180 = arriba."""
    i = 0 if lado == "i" else 1
    pv = RIG[nombre if isinstance(nombre, str) else nombre["rig"]]["arm"][i]
    if pv is not None: pv.rotation_euler.y = rad((-1 if lado == "i" else 1) * (grados + extra))


def estrella(ctx, loc, s, hexc="#FFE27A", emit=5):
    """Destello de 4 puntas: dos barras en cruz y un rombo central (raíz vacía: se escala y gira como un solo objeto)."""
    r = empty(ctx, "estrella", loc)
    box(ctx, "e1", (0, 0, 0), (s, s * 0.14, s * 0.14), hexc, 0.4, emit, parent=r)
    box(ctx, "e2", (0, 0, 0), (s * 0.14, s * 0.14, s), hexc, 0.4, emit, parent=r)
    box(ctx, "e3", (0, 0, 0), (s * 0.34, s * 0.2, s * 0.34), "#FFFFFF", 0.4, emit, rot=(0, rad(45), 0), parent=r)
    for sx in (-1, 1):
        box(ctx, "e4", (0.5 * s * 0.5 * sx, 0, 0.5 * s * 0.5), (s * 0.2, s * 0.1, s * 0.2), hexc, 0.4, emit * 0.8, rot=(0, rad(45), 0), parent=r)
    return r


# ------------------------------------------------------------------ destello de cambio de época
class Destello:
    """Plano blanco delante de la cámara; set(k) con k de 0 (nada) a 1 (pantalla blanca)."""
    def __init__(self, ctx, cam):
        m = bpy.data.materials.new("destello"); m.use_nodes = True; nt = m.node_tree
        for n in list(nt.nodes): nt.nodes.remove(n)
        em = nt.nodes.new("ShaderNodeEmission"); em.inputs["Strength"].default_value = 9
        tr = nt.nodes.new("ShaderNodeBsdfTransparent"); mx = nt.nodes.new("ShaderNodeMixShader"); o = nt.nodes.new("ShaderNodeOutputMaterial")
        nt.links.new(tr.outputs[0], mx.inputs[1]); nt.links.new(em.outputs[0], mx.inputs[2]); nt.links.new(mx.outputs[0], o.inputs[0])
        self.mx = mx
        me = bpy.data.meshes.new("destello"); me.from_pydata([(-4, -4, 0), (4, -4, 0), (4, 4, 0), (-4, 4, 0)], [], [(0, 1, 2, 3)]); me.materials.append(m)
        self.o = bpy.data.objects.new("destello", me); ctx.col.objects.link(self.o)
        self.o.parent = cam; self.o.location = (0, 0, -0.6)
    def set(self, k):
        k = max(0.0, min(1.0, k)); self.mx.inputs[0].default_value = k; self.o.hide_render = k <= 0.001


# ------------------------------------------------------------------ decorados
def casa_decor(ctx, muro_y):
    """Habitación de Soclo: suelo de madera, una pared al fondo (muro_y), alfombra y luz de mañana."""
    fondo(ctx, "#CBBFA6", 0.8)
    box(ctx, "Suelo", (0, 0, -0.2), (40, 40, 0.4), "#9B7650", 0.6)
    s = 1 if muro_y > 0 else -1
    box(ctx, "Muro", (0, muro_y + s * 0.2, 6), (40, 0.4, 12), "#D8C7A5", 0.9)
    box(ctx, "Rodapie", (0, muro_y - s * 0.05, 0.3), (40, 0.12, 0.6), "#F4F1EA", 0.7)
    for sx in (-1, 1): box(ctx, "Muro lado", (13 * sx, 0, 6), (0.4, 40, 12), "#CDBB98", 0.9)
    box(ctx, "Alfombra", (0, muro_y - s * 5.5, 0.02), (8, 7, 0.05), "#C0593B", 0.95)
    luz(ctx, "Sol manana", 'AREA', (-9, -3 * s, 9), 5000, "#FFE2B0", rot=(60, 0, 50), size=8)
    luz(ctx, "Relleno", 'AREA', (0, -s * 10 * -1, 7), 3000, "#FFF4E0", rot=(80, 0, 0 if s > 0 else 180), size=14)


def armario(ctx, loc, rot_z=0.0, glow=0.0, uniforme=None):
    """Armario lleno de ropa, con las dos puertas abiertas. Frente hacia -Y (local). Devuelve (raíz, material_del_fondo_luminoso)."""
    r = empty(ctx, "Armario", loc, (0, 0, rot_z))
    W = "#7A5230"; cols = ["#E3873F", "#6B8F71", "#F4F1EA", "#1F2A4D", "#D9A23F", "#A5560F", "#C9C3B5", "#8A5A2B", "#7A1F2B"]
    for sx in (-1, 1): box(ctx, "lado", (3.3 * sx, 0, 4.6), (0.4, 2.4, 9.2), W, 0.7, parent=r)
    box(ctx, "techo", (0, 0, 9.3), (7.0, 2.4, 0.4), W, 0.7, parent=r)
    box(ctx, "base", (0, 0, 0.2), (7.0, 2.4, 0.4), W, 0.7, parent=r)
    fondo_o = box(ctx, "fondo armario", (0, 0.95, 4.6), (6.2, 0.2, 8.8), "#F7F4EE", 0.6, glow, parent=r)
    if glow:
        fondo_o.data.materials[0] = fondo_o.data.materials[0].copy()
    box(ctx, "barra", (0, -0.1, 8.3), (6.2, 0.12, 0.12), "#D9A23F", 0.3, parent=r)
    rnd = random.Random(5)
    for i in range(8):
        x = -2.7 + i * 0.77
        box(ctx, "percha", (x, -0.1, 8.15), (0.5, 0.05, 0.1), "#D9A23F", 0.3, parent=r)
        box(ctx, "prenda", (x, -0.05, 6.9), (0.62, 0.35, 2.4 - rnd.random() * 0.7), uniforme or rnd.choice(cols), 0.85, parent=r, bevel=True)
    box(ctx, "estante", (0, 0, 4.2), (6.2, 2.0, 0.15), W, 0.7, parent=r)
    box(ctx, "estante2", (0, 0, 2.2), (6.2, 2.0, 0.15), W, 0.7, parent=r)
    for j, z in enumerate((4.4, 2.4)):
        for i in range(5):
            box(ctx, "pila", (-2.4 + i * 1.2, -0.15, z + 0.3 + (0.2 if (i + j) % 2 else 0)), (1.0, 1.4, 0.45 + 0.25 * ((i + j) % 3)), rnd.choice(cols), 0.9, parent=r, bevel=True)
    for i in range(4):
        box(ctx, "zapato", (-2.4 + i * 1.5, -0.2, 0.7), (0.5, 1.0, 0.5), rnd.choice(cols), 0.5, parent=r, bevel=True)
    for sx in (-1, 1):  # puertas abiertas hacia fuera
        pv = empty(ctx, "pivote puerta", (3.3 * sx, -1.2, 4.6), (0, 0, rad(-105 * sx)), r)
        box(ctx, "puerta", (-1.6 * sx, 0, 0), (3.2, 0.25, 8.8), "#8A5E38", 0.6, parent=pv, bevel=True)
        box(ctx, "tirador", (-2.9 * sx, -0.2, 0), (0.15, 0.15, 0.7), "#D9A23F", 0.3, parent=pv)
    return r, fondo_o


def cueva_decor(ctx):
    fondo(ctx, "#15110E", 0.6)
    box(ctx, "Suelo", (0, 8, -0.25), (60, 40, 0.5), "#5A4A3A", 0.95)
    box(ctx, "Pared fondo", (0, 18, 7), (40, 3, 14), "#4A4038", 0.95)
    box(ctx, "Pared izq", (-12, 8, 7), (5, 20, 14), "#3A322C", 0.95)
    box(ctx, "Pared der", (12, 8, 7), (5, 20, 14), "#3A322C", 0.95)
    box(ctx, "Techo", (0, 8, 14), (30, 22, 3), "#2E2824", 0.95)
    for (x, h) in [(-8, 2.4), (-3, 1.6), (4, 2.0), (9, 2.8)]:
        cyl(ctx, "Estalactita", (x, 11, 12.3 - h / 2), 0.7, h, "#4A4038", 0.9, r2=0.05, rot=(math.pi, 0, 0), verts=6)
    for (x, z, s) in [(-6, 6, 1.0), (-4.2, 6.4, 0.7), (-2.6, 5.8, 0.9), (5, 7, 1.1), (7, 6.2, 0.8)]:
        box(ctx, "Pintura", (x, 16.4, z), (s * 1.6, 0.1, s), "#B5743A", 0.9, 0.3)
        box(ctx, "Pintura", (x + 0.3 * s, 16.38, z + 0.6 * s), (s * 0.3, 0.1, s * 0.5), "#B5743A", 0.9, 0.3)
    for rz in (0, 60, 120): box(ctx, "Tronco", (0, 7.5, 0.25), (2.2, 0.4, 0.4), "#3B2616", 0.9, rot=(0, 0, rad(rz)))
    llamas = [box(ctx, "Llama", (dx, 7.5, 0.5 + h / 2), (0.55, 0.55, h), "#FF8A1F", 0.5, 7) for dx, h in [(-0.4, 1.4), (0.0, 2.1), (0.4, 1.2)]]
    luz(ctx, "Fuego", 'POINT', (0, 6.5, 2.5), 2200, "#FF8A2E")
    luz(ctx, "Frente", 'AREA', (0, -12, 7), 2600, "#FFE6C8", rot=(80, 0, 0), size=12)
    return llamas


def llamear(llamas, t):
    for i, f in enumerate(llamas): f.scale.z = 1 + 0.25 * math.sin(t * 17 + i * 2.1); f.scale.x = f.scale.y = 1 + 0.1 * math.sin(t * 13 + i)


def egipto_decor(ctx):
    fondo(ctx, "#9ED4EE", 1.0)
    box(ctx, "Arena", (0, 20, -0.25), (200, 120, 0.5), "#E0B76B", 0.95)
    for (x, y, r, h) in [(-16, 55, 15, 13), (14, 70, 22, 19)]:
        cyl(ctx, "Piramide", (x, y, h / 2), r, h, "#D9A85A", 0.9, r2=0.0, verts=4, rot=(0, 0, rad(45)))
    sphere(ctx, "Sol", (18, 60, 26), 3, "#FFF3C0", 0.5, 6)
    for (x, y, w, h) in [(-11, 14, 6, 6), (-6, 18, 5, 4.5), (12, 15, 7, 5.5), (7, 19, 4, 4)]:
        box(ctx, "Casa", (x, y, h / 2), (w, 5, h), "#D8B98A", 0.95)
        box(ctx, "Puerta", (x, y - 2.55, 1.1), (1.4, 0.1, 2.2), "#6B4A2A", 0.9)
    cyl(ctx, "Palmera tronco", (-9, 8, 3.5), 0.4, 7, "#8A6B3A", 0.9)
    for a in range(6):
        box(ctx, "Hoja", (-9 + 1.8 * math.cos(a), 8 + 1.8 * math.sin(a), 7.1), (3.2, 0.5, 0.18), "#3A8A3A", 0.8, rot=(0, 0, a * rad(60)))
    luz(ctx, "Sol", 'SUN', (10, -10, 25), 3.5, "#FFF1D0", rot=(50, 0, 20))
    luz(ctx, "Relleno", 'AREA', (0, -12, 7), 2500, "#FFFFFF", rot=(80, 0, 0), size=14)
    # gente de fondo: lino blanco y UNA persona de verde (la del gag)
    gente = [era(ctx, "E1", "egipto", (-3.6, 9.0, 0), rad(10), "neutral", skin=S[1]),
             era(ctx, "E2", "egipto", (0.4, 13.0, 0), rad(-8), "happy", skin=S[2]),
             era(ctx, "E4", "egipto", (4.0, 12.0, 0), rad(-10), "happy", skin=S[1])]
    verde = era(ctx, "Verde", "egipto", (2.0, 7.5, 0), 0, "happy", skin=S[3], tela="#2E9E5B", top="#2E9E5B")
    return gente, verde
