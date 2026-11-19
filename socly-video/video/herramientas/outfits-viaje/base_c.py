"""Decorados de la fase 6: años 60, 2010 y vuelta a casa (se carga con exec tras base.py y base_b.py)."""


def car(ctx, loc, hexc, rot=0.0):
    r = empty(ctx, "Coche", loc, (0, 0, rot))
    box(ctx, "carroceria", (0, 0, 0.9), (2.2, 4.2, 0.9), hexc, 0.4, parent=r, bevel=True)
    box(ctx, "cabina", (0, -0.2, 1.7), (1.9, 2.2, 0.8), hexc, 0.4, parent=r, bevel=True)
    box(ctx, "cristales", (0, -0.2, 1.72), (1.94, 2.0, 0.5), "#9AD0E8", 0.2, parent=r)
    for sx in (-1, 1):
        for sy in (-1, 1): cyl(ctx, "rueda", (1.15 * sx, 1.4 * sy, 0.5), 0.5, 0.3, "#15140F", 0.6, rot=(0, rad(90), 0), parent=r, verts=12)
        box(ctx, "faro", (0.7 * sx, -2.12, 1.0), (0.4, 0.06, 0.3), "#FFE9A0", 0.3, 3, parent=r)
    return r


def calle60_decor(ctx):
    fondo(ctx, "#BFE8FF", 1.0)
    box(ctx, "Suelo", (0, 20, -0.25), (200, 120, 0.5), "#8A8A92", 0.9)
    box(ctx, "Calzada", (0, 20, 0.0), (12, 120, 0.04), "#5E5E66", 0.95)
    for k in range(10): box(ctx, "Raya", (0, -2 + k * 6, 0.03), (0.3, 2.5, 0.02), "#F4F1EA", 0.8)
    cols = ["#F2A65A", "#7AC7B8", "#F4D35E", "#E58B8B", "#9AA7E8"]
    for sx in (-1, 1):
        for k in range(5):
            y = 3 + k * 8.0; h = 9 + (k % 3) * 2; c = cols[(k + (1 if sx > 0 else 0)) % 5]
            box(ctx, "Edificio", (sx * 12, y, h / 2), (9, 7.5, h), c, 0.9)
            for fz in (3.2, 6.4):
                for fy in (-2.2, 0, 2.2): box(ctx, "Ventana", (sx * (12 - 4.55), y + fy, fz), (0.06, 1.2, 1.7), "#F4F1EA", 0.4, 0.3)
            cyl(ctx, "Flor", (sx * (12 - 4.6), y, h - 1.4), 0.9, 0.06, ["#FF2E88", "#FFE500", "#FF7A00"][k % 3], 0.5, 0.6, rot=(0, rad(90), 0))
    luz(ctx, "Sol", 'SUN', (10, -10, 25), 3.4, "#FFF1D0", rot=(55, 0, 20))
    luz(ctx, "Relleno", 'AREA', (0, -12, 7), 2600, "#FFFFFF", rot=(80, 0, 0), size=14)


def chica60(ctx, name, loc, rot, tela, skin=None, pelo="#2A1B12"):
    """Persona con minifalda y botas blancas."""
    sk = skin or S[0]
    r = person(ctx, name, loc, rot_z=rot, skin=sk, hair=pelo, hairstyle="long", top=tela, sleeve=tela, pants=sk, shoe_l="#F7F4EE", shorts=True,
               face_kind="happy", extras=lambda c, rr: (box(c, "minifalda", (0, 0, 1.85), (1.45, 0.95, 0.5), "#15140F" if tela != "#15140F" else "#F4F1EA", 0.8, parent=rr, bevel=True),
                                                         box(c, "diadema", (0, 0.0, 4.5), (1.2, 1.2, 0.08), "#FF2E88", 0.6, parent=rr)))
    r["rig"] = name
    return r


def calle2010_decor(ctx):
    fondo(ctx, "#CFE6F5", 1.0)
    box(ctx, "Suelo", (0, 20, -0.25), (200, 120, 0.5), "#7D8085", 0.9)
    box(ctx, "Calzada", (0, 20, 0.0), (12, 120, 0.04), "#4A4C52", 0.95)
    for k in range(10): box(ctx, "Raya", (0, -2 + k * 6, 0.03), (0.3, 2.5, 0.02), "#F4F1EA", 0.8)
    rnd = random.Random(8)
    for sx in (-1, 1):
        for k in range(5):
            y = 3 + k * 8.0; h = 12 + (k % 3) * 3
            box(ctx, "Edificio", (sx * 12, y, h / 2), (9, 7.5, h), rnd.choice(["#C9D6E2", "#D9DDE3", "#BFC9D6"]), 0.5)
            for fz in range(3, int(h) - 1, 3):
                box(ctx, "Cristal", (sx * (12 - 4.55), y, fz + 0.4), (0.06, 6.4, 1.8), "#7FB2D6", 0.15, 0.25)
    luz(ctx, "Sol", 'SUN', (10, -10, 25), 3.2, "#FFF6E0", rot=(55, 0, 20))
    luz(ctx, "Relleno", 'AREA', (0, -12, 7), 2600, "#FFFFFF", rot=(80, 0, 0), size=14)


def reloj(ctx, loc, r=1.25, hora=8, minuto=5):
    cyl(ctx, "reloj aro", loc, r + 0.12, 0.14, "#15140F", 0.4, rot=(rad(90), 0, 0))
    cyl(ctx, "reloj", (loc[0], loc[1] - 0.02, loc[2]), r, 0.14, "#F7F4EE", 0.6, rot=(rad(90), 0, 0))
    for k in range(12):
        a = rad(k * 30); box(ctx, "marca", (loc[0] + math.sin(a) * r * 0.85, loc[1] - 0.1, loc[2] + math.cos(a) * r * 0.85), (0.08, 0.04, 0.2), "#15140F", 0.5, rot=(0, -a, 0))
    pvs = []
    for ln, ang, w in ((r * 0.55, hora * 30 + minuto * 0.5, 0.12), (r * 0.8, minuto * 6, 0.08)):
        pv = empty(ctx, "aguja pivote", (loc[0], loc[1] - 0.1, loc[2]), (0, rad(ang), 0)); pvs.append(pv)
        box(ctx, "aguja", (0, 0, ln / 2), (w, 0.05, ln), "#15140F", 0.5, parent=pv)
    box(ctx, "reloj centro", (loc[0], loc[1] - 0.13, loc[2]), (0.2, 0.06, 0.2), "#E3873F", 0.4)
    return pvs


def corazon(ctx, loc, s, hexc="#FF2E88"):
    r = empty(ctx, "corazon", loc)
    for sx in (-1, 1): box(ctx, "lado", (0.22 * s * sx, 0, 0.2 * s), (0.5 * s, 0.12 * s, 0.5 * s), hexc, 0.4, 2.0, rot=(0, rad(45), 0), parent=r)
    box(ctx, "punta", (0, 0, -0.12 * s), (0.52 * s, 0.12 * s, 0.52 * s), hexc, 0.4, 2.0, rot=(0, rad(45), 0), parent=r)
    return r


# ------------------------------------------------------------------ extras de la fase 6 (mejoras)
def translucido(ctx, nombre, loc, w, h, hexc="#FFFFFF", k=0.15, rot=(0, 0, 0), emision=6, parent=None):
    """Plano translúcido luminoso en XZ (mira a -Y). Devuelve (objeto, nodo de mezcla: .inputs[0].default_value = k)."""
    m = bpy.data.materials.new(nombre); m.use_nodes = True; nt = m.node_tree
    for n in list(nt.nodes): nt.nodes.remove(n)
    em = nt.nodes.new("ShaderNodeEmission"); em.inputs["Strength"].default_value = emision; em.inputs["Color"].default_value = lin(hexc)
    tr = nt.nodes.new("ShaderNodeBsdfTransparent"); mx = nt.nodes.new("ShaderNodeMixShader"); o = nt.nodes.new("ShaderNodeOutputMaterial")
    nt.links.new(tr.outputs[0], mx.inputs[1]); nt.links.new(em.outputs[0], mx.inputs[2]); nt.links.new(mx.outputs[0], o.inputs[0])
    mx.inputs[0].default_value = k
    me = bpy.data.meshes.new(nombre); hw, hh = w / 2, h / 2
    me.from_pydata([(-hw, 0, -hh), (hw, 0, -hh), (hw, 0, hh), (-hw, 0, hh)], [], [(0, 1, 2, 3)]); me.materials.append(m)
    ob = bpy.data.objects.new(nombre, me); ctx.col.objects.link(ob); ob.location = loc; ob.rotation_euler = rot
    if parent: ob.parent = parent
    return ob, mx


def cuadro(ctx, loc, tipo, rotulo):
    """Cuadro dorado con un icono claro: 'rey', 'ley' o 'revista'. Devuelve la raíz."""
    r = empty(ctx, "cuadro " + tipo, loc)
    box(ctx, "marco", (0, 0.1, 0), (2.5, 0.16, 3.2), "#D9A23F", 0.3, 0.3, parent=r, bevel=True)
    box(ctx, "lienzo", (0, 0.0, 0), (2.2, 0.1, 2.9), {"rey": "#2A3A6B", "ley": "#E8D9B0", "revista": "#F4F1EA"}[tipo], 0.7, 0.2, parent=r)
    if tipo == "rey":
        box(ctx, "capa", (0, -0.1, -0.5), (1.4, 0.06, 1.4), "#B5231F", 0.6, parent=r)
        box(ctx, "cuello piel", (0, -0.12, 0.25), (1.1, 0.06, 0.25), "#F4F1EA", 0.8, parent=r)
        box(ctx, "cabeza", (0, -0.12, 0.65), (0.6, 0.06, 0.6), "#F0CFA8", 0.6, parent=r)
        for i in range(3): box(ctx, "pico corona", (-0.25 + 0.25 * i, -0.13, 1.1 + (0.1 if i == 1 else 0.0)), (0.17, 0.06, 0.3), "#FFD24A", 0.3, 1.0, parent=r)
        box(ctx, "banda corona", (0, -0.13, 0.95), (0.7, 0.06, 0.14), "#FFD24A", 0.3, 1.0, parent=r)
    elif tipo == "ley":
        for i in range(5): box(ctx, "linea", (0, -0.08, 0.95 - i * 0.35), (1.5 - 0.15 * (i % 2), 0.05, 0.1), "#4A3524", 0.9, parent=r)
        box(ctx, "sello", (0, -0.1, -0.85), (0.5, 0.06, 0.5), "#B5231F", 0.5, 0.6, rot=(0, rad(45), 0), parent=r)
    else:
        box(ctx, "portada", (0, -0.08, 0.0), (1.9, 0.05, 2.5), "#E3873F", 0.7, parent=r)
        text(ctx, "moda", "MODA", (0, -0.14, 0.95), 0.55, "#15140F", emit=0.2, extrude=0.03, parent=r)
        box(ctx, "mini cabeza", (0, -0.12, 0.2), (0.45, 0.05, 0.45), "#F0CFA8", 0.6, parent=r)
        box(ctx, "mini torso", (0, -0.12, -0.5), (0.8, 0.05, 1.0), "#1F2A4D", 0.8, parent=r)
    text(ctx, "rotulo", rotulo, (0, -0.2, -2.0), 0.5, "#FFE27A", emit=3, extrude=0.04, parent=r)
    return r


def flecha(ctx, loc):
    """Cursor de ratón (flecha) blanco con borde oscuro. Devuelve la raíz."""
    r = empty(ctx, "cursor", loc)
    box(ctx, "borde", (0, 0, -0.1), (0.75, 0.05, 1.45), "#15140F", 0.5, rot=(0, rad(-18), 0), parent=r)
    box(ctx, "cuerpo", (0, -0.03, -0.1), (0.55, 0.05, 1.25), "#FFFFFF", 0.4, 0.8, rot=(0, rad(-18), 0), parent=r)
    box(ctx, "cola", (0.3, -0.03, -0.75), (0.25, 0.05, 0.6), "#FFFFFF", 0.4, 0.8, rot=(0, rad(-18), 0), parent=r)
    return r
