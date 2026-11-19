"""Piezas de «Ciudad Socly» para Blender (se cargan con exec desde execute_blender_code).
Unidades: 1 = un cubo. Los personajes miran hacia -Y. Todo con cajas, cilindros y materiales lisos."""
import bpy, bmesh, math, random, os
from mathutils import Vector

ROOT = r"/home/user/prueba/socly-video"
LOGO = ROOT + r"\diseno\ciudad-socly\logo-socly.png"
OUT = ROOT + r"\video\herramientas\ciudad-socly"

def lin(h):
    h = h.lstrip('#'); r, g, b = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
    f = lambda c: c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return (f(r), f(g), f(b), 1)

_MAT = {}
def mat(hexc, rough=0.55, emit=0):
    k = (hexc, round(rough, 2), emit)
    if k in _MAT and _MAT[k].name in bpy.data.materials: return _MAT[k]
    m = bpy.data.materials.new("m" + hexc[1:] + ("e%g" % emit if emit else ""))
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = lin(hexc); b.inputs["Roughness"].default_value = rough
    if emit:
        b.inputs["Emission Color"].default_value = lin(hexc); b.inputs["Emission Strength"].default_value = emit
    _MAT[k] = m; return m

_LOGO = {}
def logo_mat(strength=1.6):
    if strength in _LOGO and _LOGO[strength].name in bpy.data.materials: return _LOGO[strength]
    img = bpy.data.images.get("logo-socly.png") or bpy.data.images.load(LOGO)
    m = bpy.data.materials.new("logo"); m.use_nodes = True; nt = m.node_tree
    for n in list(nt.nodes): nt.nodes.remove(n)
    tx = nt.nodes.new("ShaderNodeTexImage"); tx.image = img
    em = nt.nodes.new("ShaderNodeEmission"); em.inputs["Strength"].default_value = strength
    o = nt.nodes.new("ShaderNodeOutputMaterial")
    nt.links.new(tx.outputs["Color"], em.inputs["Color"]); nt.links.new(em.outputs["Emission"], o.inputs["Surface"])
    _LOGO[strength] = m; return m

class Ctx:
    """Escena + colección donde se crea todo."""
    def __init__(self, name):
        self.sc = bpy.data.scenes.new(name)
        bpy.context.window.scene = self.sc
        self.col = bpy.data.collections.new(name + " col"); self.sc.collection.children.link(self.col)

def _link(ctx, o):
    ctx.col.objects.link(o); return o

def box(ctx, name, loc, size, hexc, rough=0.55, emit=0, rot=(0, 0, 0), parent=None, bevel=False, material=None):
    me = bpy.data.meshes.new(name); bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts: v.co.x *= size[0]; v.co.y *= size[1]; v.co.z *= size[2]
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); _link(ctx, o)
    me.materials.append(material or mat(hexc, rough, emit))
    o.location = loc; o.rotation_euler = rot
    if bevel:
        md = o.modifiers.new("b", 'BEVEL'); md.width = 0.04; md.segments = 2
    if parent: o.parent = parent
    return o

def cyl(ctx, name, loc, r, h, hexc, rough=0.5, emit=0, rot=(0, 0, 0), parent=None, verts=32, r2=None):
    me = bpy.data.meshes.new(name); bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=verts, radius1=r, radius2=(r if r2 is None else r2), depth=h)
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); _link(ctx, o); me.materials.append(mat(hexc, rough, emit))
    o.location = loc; o.rotation_euler = rot
    if parent: o.parent = parent
    return o

def sphere(ctx, name, loc, r, hexc, rough=0.7, emit=0, parent=None):
    me = bpy.data.meshes.new(name); bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=20, v_segments=12, radius=r)
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); _link(ctx, o); me.materials.append(mat(hexc, rough, emit))
    o.location = loc
    if parent: o.parent = parent
    return o

def empty(ctx, name, loc=(0, 0, 0), rot=(0, 0, 0), parent=None):
    o = bpy.data.objects.new(name, None); _link(ctx, o); o.location = loc; o.rotation_euler = rot
    if parent: o.parent = parent
    return o

def text(ctx, name, s, loc, size, hexc, emit=6, rot=(math.radians(90), 0, 0), extrude=0.06, parent=None):
    cu = bpy.data.curves.new(name, 'FONT'); cu.body = s; cu.size = size; cu.extrude = extrude
    cu.align_x = 'CENTER'; cu.align_y = 'CENTER'
    o = bpy.data.objects.new(name, cu); _link(ctx, o); cu.materials.append(mat(hexc, 0.4, emit))
    o.location = loc; o.rotation_euler = rot
    if parent: o.parent = parent
    return o

def logo_plane(ctx, name, loc, size, rot=(0, 0, 0), parent=None, strength=1.6):
    me = bpy.data.meshes.new(name)
    h = size / 2
    me.from_pydata([(-h, 0, -h), (h, 0, -h), (h, 0, h), (-h, 0, h)], [], [(0, 1, 2, 3)])
    uv = me.uv_layers.new(name="UVMap")
    for i, c in enumerate([(0, 0), (1, 0), (1, 1), (0, 1)]): uv.data[i].uv = c
    me.update(); me.materials.append(logo_mat(strength))
    o = bpy.data.objects.new(name, me); _link(ctx, o); o.location = loc; o.rotation_euler = rot
    if parent: o.parent = parent
    return o

RIG = {}
SKINS = ["#F2C9A0", "#D9A06F", "#A8683F", "#6B4226"]

def face(ctx, par, kind="happy", hair="#2A1B12", y=-0.57, z0=0.0):
    """Cara con cubos planos sobre la cara frontal de la cabeza (centro en z0)."""
    eye = (0.18, 0.02, 0.22); brow_y = 0.30
    big = kind in ("scared", "shock")
    if big: eye = (0.26, 0.02, 0.30)
    if kind == "angry": eye = (0.18, 0.02, 0.14)
    for sx in (-1, 1):
        box(ctx, "ojo", (0.26 * sx, y, z0 + 0.05), eye, "#15140F", 0.95, parent=par)
        box(ctx, "brillo", (0.26 * sx + 0.04, y - 0.01, z0 + 0.12), (0.06, 0.02, 0.06), "#FFFFFF", 0.3, 2, parent=par)
        rot = 0
        if kind == "angry": rot = 0.35 * sx
        if kind in ("scared",): rot = -0.25 * sx
        box(ctx, "ceja", (0.26 * sx, y, z0 + (brow_y + (0.08 if big else 0))), (0.32, 0.02, 0.07), hair, 0.5, rot=(0, 0, rot), parent=par)
    mz = z0 - 0.33
    if kind in ("happy", "smug"):
        box(ctx, "boca", (0, y, mz), (0.2, 0.02, 0.07), "#5C2A2A", 0.4, parent=par)
        for sx in (-1, 1): box(ctx, "boca", (0.17 * sx, y, mz + 0.05 + (0.03 if kind == "smug" and sx > 0 else 0)), (0.1, 0.02, 0.07), "#5C2A2A", 0.4, parent=par)
    elif kind in ("scared", "shock"):
        box(ctx, "boca", (0, y, mz), (0.3, 0.02, 0.3), "#5C2A2A", 0.4, parent=par)
        box(ctx, "lengua", (0, y - 0.01, mz - 0.07), (0.2, 0.02, 0.1), "#E88A7A", 0.5, parent=par)
    else:  # neutral / angry
        box(ctx, "boca", (0, y, mz), (0.35, 0.02, 0.07), "#5C2A2A", 0.4, parent=par)

def arm(ctx, par, side, shoulder, length, angle_deg, sleeve, hand_hex, hand=True):
    """Brazo que cuelga de un pivote en el hombro; angle 0 = colgando, 90 = horizontal hacia fuera, 180 = arriba."""
    pv = empty(ctx, "pivote brazo", shoulder, (0, math.radians(angle_deg * side), 0), par)
    box(ctx, "brazo", (0, 0, -length / 2), (0.42, 0.45, length), sleeve, 0.7, parent=pv, bevel=True)
    if hand: box(ctx, "mano", (0, 0, -length - 0.18), (0.38, 0.4, 0.4), hand_hex, 0.6, parent=pv, bevel=True)
    return pv

def person(ctx, name, loc, rot_z=0, skin=SKINS[0], hair="#2A1B12", hairstyle="flat", top="#888888", sleeve=None,
           pants="#3B4A63", shoe_l="#F7F4EE", shoe_r=None, sole=None, face_kind="happy", arm_l=8, arm_r=8,
           scale=1.0, shorts=False, extras=None):
    """Personaje de bloques: pies en z=0. Devuelve el empty raíz (los extras reciben (ctx, root))."""
    root = empty(ctx, name, loc, (0, 0, rot_z)); root.scale = (scale,) * 3
    sleeve = sleeve or top; shoe_r = shoe_r or shoe_l
    # zapatos y piernas (cada pierna cuelga de un pivote en la cadera para poder caminar)
    hips = []
    for sx, sc_ in ((-1, shoe_l), (1, shoe_r)):
        hip = empty(ctx, "cadera", (0.42 * sx, 0, 1.75), parent=root); hips.append(hip)
        box(ctx, "zapato", (0, -0.06, 0.225 - 1.75), (0.45, 0.75, 0.45), sc_, 0.45, parent=hip, bevel=True)
        if sole: box(ctx, "suela", (0, -0.06, 0.04 - 1.75), (0.47, 0.77, 0.1), sole, 0.5, parent=hip)
        if shorts:
            box(ctx, "pierna piel", (0, 0, 0.85 - 1.75), (0.38, 0.4, 0.8), skin, 0.6, parent=hip, bevel=True)
            box(ctx, "short", (0, 0, 1.45 - 1.75), (0.44, 0.46, 0.6), pants, 0.8, parent=hip, bevel=True)
        else:
            box(ctx, "pierna", (0, 0, 1.1 - 1.75), (0.4, 0.42, 1.3), pants, 0.8, parent=hip, bevel=True)
    box(ctx, "torso", (0, 0, 2.5), (1.2, 0.7, 1.4), top, 0.75, parent=root, bevel=True)
    sh_z = 3.12
    pl = arm(ctx, root, -1, (-0.82, 0, sh_z), 1.1, arm_l, sleeve, skin)
    pr = arm(ctx, root, 1, (0.82, 0, sh_z), 1.1, arm_r, sleeve, skin) if arm_r is not None else None
    RIG[name] = {"hip": hips, "arm": [pl, pr]}
    box(ctx, "cuello", (0, 0, 3.28), (0.45, 0.45, 0.2), skin, 0.6, parent=root)
    head = box(ctx, "cabeza", (0, 0, 3.95), (1.1, 1.1, 1.1), skin, 0.55, parent=root, bevel=True)
    # pelo
    if hairstyle == "flat":
        box(ctx, "pelo", (0, 0.04, 4.55), (1.18, 1.18, 0.4), hair, 0.7, parent=root, bevel=True)
        box(ctx, "flequillo", (0.2, -0.45, 4.4), (0.62, 0.3, 0.35), hair, 0.7, rot=(0, 0, 0.26), parent=root, bevel=True)
    elif hairstyle == "crest":
        for i in range(5):
            box(ctx, "cresta", (0, 0.45 - i * 0.22, 4.7 + (0.12 if i in (1, 2, 3) else 0)), (0.2, 0.2, 0.45), hair, 0.6, parent=root)
    elif hairstyle == "long":
        box(ctx, "pelo", (0, 0.04, 4.55), (1.18, 1.18, 0.4), hair, 0.7, parent=root, bevel=True)
        box(ctx, "melena", (0, 0.5, 4.0), (1.2, 0.22, 1.0), hair, 0.7, parent=root)
    elif hairstyle == "slick":  # pelo canoso peinado hacia atrás
        box(ctx, "pelo", (0, 0.06, 4.56), (1.16, 1.14, 0.36), hair, 0.6, parent=root, bevel=True)
        box(ctx, "tupe", (0, -0.5, 4.62), (1.0, 0.18, 0.3), hair, 0.6, parent=root, bevel=True)
    # cara (hijos de la raíz, en coordenadas de la raíz)
    fholder = empty(ctx, "cara", (0, 0, 3.95), (0, 0, 0), root)
    face(ctx, fholder, face_kind, hair if hairstyle != "none" else "#2A1B12")
    if extras: extras(ctx, root)
    return root

def build_city(ctx, seed=11, neon=True, color_mix=0.0):
    """Skyline de cubos (3 filas) con ventanas, pantalla de ofertas, torre de luz y neones."""
    rnd = random.Random(seed)
    bc = ["#2F3138", "#4A4D55", "#5B5F69"]
    if color_mix > 0:  # al final de la historia se llena de color
        warm = ["#F2A65A", "#7AC7B8", "#F4D35E", "#E58B8B"]
    rows = [(30, 0, (8, 15)), (44, 1, (14, 26)), (62, 2, (20, 38))]
    win = mat("#FFD27A", 0.5, 4); win2 = mat("#18E0FF", 0.5, 5); win3 = mat("#FF2E88", 0.5, 5)
    box(ctx, "Suelo", (0, 10, -0.25), (140, 90, 0.5), "#25262B", 0.8)
    box(ctx, "Plaza", (0, 2, 0.01), (30, 22, 0.06), "#8B8E96", 0.7)
    for (yy, ci, (h0, h1)) in rows:
        x = -60
        while x < 60:
            w = rnd.uniform(6, 11); h = rnd.uniform(h0, h1); d = rnd.uniform(6, 9)
            col = rnd.choice(warm) if color_mix > 0 and rnd.random() < color_mix else bc[ci]
            box(ctx, "Edificio", (x + w / 2, yy, h / 2), (w, d, h), col, 0.8)
            if ci < 2:
                fy = yy - d / 2 - 0.03; nx = int((w - 1) // 1.6); nz = int((h - 2) // 2.4)
                for i in range(nx):
                    for j in range(nz):
                        r = rnd.random()
                        if r < 0.42:
                            m = win2 if r < 0.05 else (win3 if r < 0.09 else win)
                            box(ctx, "Ventana", (x + 1.0 + i * 1.6, fy, 1.8 + j * 2.4), (0.7, 0.05, 1.0), "#000", material=m)
                if neon and rnd.random() < 0.28 and h > 11:  # cartel de neón
                    word = rnd.choice(["SALE", "OFERTA", "-50%", "YA!", "TOP"])
                    colr = rnd.choice(["#FF2E88", "#FFE500", "#2BFF88", "#18E0FF"])
                    text(ctx, "Neon " + word, word, (x + w / 2, fy - 0.2, h * 0.62), 1.6, colr, emit=9)
            x += w + rnd.uniform(0.4, 1.4)
    # pantalla gigante de ofertas
    box(ctx, "Pantalla marco", (3.0, 24.0, 10.5), (13, 0.6, 7.6), "#15140F", 0.4)
    box(ctx, "Pantalla fondo", (3.0, 23.65, 10.5), (12.2, 0.1, 6.8), "#FF2E88", 0.4, 2.4)
    box(ctx, "Pantalla franja", (3.0, 23.58, 10.0), (9.5, 0.08, 2.4), "#FFE500", 0.4, 3.0)
    text(ctx, "Pantalla texto", "-70%", (3.0, 23.45, 10.0), 2.0, "#E8001C", emit=1.5)
    text(ctx, "Pantalla texto 2", "OFERTA YA", (3.0, 23.45, 12.5), 0.9, "#18E0FF", emit=3)
    # torre de luz
    cyl(ctx, "Torre", (-6.5, 22, 5.5), 0.35, 11, "#2F3138", 0.5)
    for i in range(3):
        for j in range(2):
            box(ctx, "Foco", (-7.4 + i * 0.9, 21.6, 11.4 + j * 0.9), (0.7, 0.2, 0.7), "#18E0FF", 0.3, 9)

def lights(ctx, rosa=700, cian=700, relleno=500, sol=3.0, fachadas=60000):
    def L(name, kind, loc, energy, hexc, rot=None, size=None):
        d = bpy.data.lights.new(name, kind); d.energy = energy; d.color = lin(hexc)[:3]
        if size: d.size = size
        o = bpy.data.objects.new(name, d); o.location = loc
        if rot: o.rotation_euler = rot
        ctx.col.objects.link(o); return o
    L("Sol", 'SUN', (0, 30, 20), sol, "#FFB35C", rot=(math.radians(100), 0, math.radians(30)))
    L("Rosa", 'AREA', (7, -6, 4), rosa, "#FF2E88", rot=(math.radians(80), 0, math.radians(55)), size=4)
    L("Cian", 'AREA', (-7, -6, 4), cian, "#18E0FF", rot=(math.radians(80), 0, math.radians(-55)), size=4)
    L("Relleno", 'AREA', (0, -9, 3), relleno, "#F7F4EE", rot=(math.radians(90), 0, 0), size=5)
    L("Fachadas", 'AREA', (0, -2, 28), fachadas, "#8C8FB5", rot=(math.radians(75), 0, 0), size=40)

def sky(ctx, strength=1.1):
    w = bpy.data.worlds.new("Cielo"); ctx.sc.world = w; w.use_nodes = True
    n = w.node_tree.nodes; l = w.node_tree.links
    for x in list(n): n.remove(x)
    out = n.new("ShaderNodeOutputWorld"); bg = n.new("ShaderNodeBackground"); bg.inputs["Strength"].default_value = strength
    ramp = n.new("ShaderNodeValToRGB"); sep = n.new("ShaderNodeSeparateXYZ"); tc = n.new("ShaderNodeTexCoord")
    ramp.color_ramp.elements[0].position = 0.35; ramp.color_ramp.elements[0].color = lin("#FFB35C")
    ramp.color_ramp.elements[1].position = 0.95; ramp.color_ramp.elements[1].color = lin("#2B2150")
    e = ramp.color_ramp.elements.new(0.62); e.color = lin("#E8637A")
    l.new(tc.outputs["Window"], sep.inputs["Vector"]); l.new(sep.outputs["Y"], ramp.inputs["Fac"])
    l.new(ramp.outputs["Color"], bg.inputs["Color"]); l.new(bg.outputs["Background"], out.inputs["Surface"])

def camera(ctx, loc, rot_deg, lens=50):
    cd = bpy.data.cameras.new("Cam"); cd.lens = lens; cd.sensor_fit = 'VERTICAL'; cd.sensor_height = 36
    c = bpy.data.objects.new("Cam", cd); ctx.col.objects.link(c); ctx.sc.camera = c
    c.location = loc; c.rotation_euler = tuple(math.radians(a) for a in rot_deg); return c

def render(ctx, filename, pct=50, samples=64, exposure=0.3):
    r = ctx.sc.render; r.engine = 'BLENDER_EEVEE'; r.resolution_x = 1080; r.resolution_y = 1920; r.resolution_percentage = pct
    ctx.sc.eevee.taa_render_samples = samples
    ctx.sc.view_settings.view_transform = 'AgX'; ctx.sc.view_settings.look = 'AgX - High Contrast'; ctx.sc.view_settings.exposure = exposure
    os.makedirs(OUT + r"\prueba", exist_ok=True)
    r.filepath = OUT + "\\prueba\\" + filename
    bpy.context.window.scene = ctx.sc
    bpy.ops.render.render(write_still=True)
    return r.filepath


def make_alcalde(ctx, loc=(0, 0, 0), rot_z=0.0, face_kind="smug", arm_r=160, with_hat=True):
    NAVY, VEST, BURG = "#1F2A4D", "#3A4670", "#7A1F2B"
    def extras(c, root):
        box(c, "camisa", (0, -0.37, 2.95), (0.42, 0.03, 0.5), "#F7F4EE", 0.6, parent=root)
        box(c, "chaleco", (0, -0.375, 2.35), (0.95, 0.04, 0.85), VEST, 0.7, parent=root)
        box(c, "corbata", (0, -0.4, 2.62), (0.17, 0.03, 0.95), BURG, 0.6, parent=root)
        box(c, "panuelo", (0.4, -0.375, 2.98), (0.2, 0.03, 0.13), "#F7F4EE", 0.6, parent=root)
        box(c, "banda", (0.0, -0.4, 2.55), (0.2, 0.05, 2.0), "#E3C25A", 0.35, rot=(0, math.radians(32), 0), parent=root)
        cyl(c, "medallon", (-0.5, -0.43, 2.0), 0.17, 0.05, "#D9A23F", 0.25, rot=(math.radians(90), 0, 0), parent=root)
        box(c, "bigote", (0, -0.58, 3.7), (0.55, 0.05, 0.1), "#CFCFD4", 0.6, parent=root)
        if with_hat:
            cyl(c, "ala", (0, 0, 4.66), 0.95, 0.09, "#15140F", 0.3, parent=root)
            cyl(c, "copa", (0, 0, 5.4), 0.58, 1.45, "#15140F", 0.3, parent=root)
            cyl(c, "cinta sombrero", (0, 0, 4.9), 0.6, 0.22, BURG, 0.4, parent=root)
        box(c, "movil", (-0.42, -0.4, 2.78), (0.34, 0.05, 0.55), "#15140F", 0.3, parent=root)
        logo_plane(c, "logo movil", (-0.42, -0.43, 2.8), 0.28, parent=root, strength=2.0)
        box(c, "cinta dorada", (-0.62, -0.4, 2.55), (0.1, 0.04, 0.5), "#D9A23F", 0.3, rot=(0, math.radians(10), 0), parent=root)
    return person(ctx, "Alcalde", loc, rot_z=rot_z, skin="#F2C9A0", hair="#CFCFD4", hairstyle="slick",
                  top=NAVY, sleeve=NAVY, pants="#181F3A", shoe_l="#0B0B0D", face_kind=face_kind,
                  arm_l=6, arm_r=arm_r, scale=1.15, extras=extras)


def phone_arm(c, root, sleeve, skin, screen="ad"):
    """Brazo derecho doblado con el móvil en la mano. screen: 'ad' (ofertas) o 'logo' (Socly Style)."""
    box(c, "brazo", (0.88, 0, 2.85), (0.42, 0.45, 0.8), sleeve, 0.7, parent=root, bevel=True)
    box(c, "antebrazo", (0.88, -0.42, 2.45), (0.42, 0.9, 0.42), sleeve, 0.7, parent=root, bevel=True)
    box(c, "mano", (0.88, -0.85, 2.45), (0.38, 0.4, 0.4), skin, 0.6, parent=root, bevel=True)
    box(c, "movil", (0.88, -1.0, 2.95), (0.6, 0.06, 1.1), "#15140F", 0.6, parent=root)
    if screen == "logo":
        logo_plane(c, "logo movil", (0.88, -1.04, 2.95), 0.54, parent=root, strength=2.0)
    else:
        box(c, "pantalla ad", (0.88, -1.04, 2.95), (0.54, 0.01, 1.0), "#FF2E88", 0.4, 2.0, parent=root)
        box(c, "pantalla ad2", (0.88, -1.05, 2.95), (0.54, 0.01, 0.3), "#FFE500", 0.4, 2.5, parent=root)
