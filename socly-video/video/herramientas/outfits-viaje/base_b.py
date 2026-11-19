"""Decorados de la fase 5: Roma, Edad Media, París 1852 (se carga con exec tras base.py)."""


def anda(g, t, vel=5.0, amp=26):
    rig = RIG[g["rig"]]; s = math.sin(t * vel)
    rig["hip"][0].rotation_euler.x = rad(amp) * s; rig["hip"][1].rotation_euler.x = -rad(amp) * s
    if rig["arm"][0] is not None: rig["arm"][0].rotation_euler.x = -rad(amp * 0.7) * s


def roma_decor(ctx):
    fondo(ctx, "#A8D4EE", 1.0)
    box(ctx, "Suelo", (0, 14, -0.25), (120, 70, 0.5), "#D9D2C2", 0.7)
    for i in range(10):
        for j in range(6):
            if (i + j) % 2: box(ctx, "Baldosa", (-9 + i * 2, -4 + j * 3, 0.0), (2, 3, 0.04), "#BDB5A3", 0.7)
    for x in (-10, -3.5, 3.5, 10):
        cyl(ctx, "Columna", (x, 17, 6), 1.0, 12, "#F4F0E6", 0.5)
        box(ctx, "Capitel", (x, 17, 12.2), (2.6, 2.6, 0.5), "#F4F0E6", 0.5)
    box(ctx, "Arquitrabe", (0, 17, 13.1), (26, 3.2, 1.6), "#F4F0E6", 0.5)
    box(ctx, "Escalon", (0, 14, 0.3), (28, 5, 0.6), "#E0D9C8", 0.6)
    box(ctx, "Muro fondo", (0, 26, 8), (60, 1, 16), "#C9B79C", 0.9)
    luz(ctx, "Sol", 'SUN', (10, -10, 25), 3.2, "#FFF1D0", rot=(50, 0, 20))
    luz(ctx, "Relleno", 'AREA', (0, -12, 7), 2400, "#FFFFFF", rot=(80, 0, 0), size=14)


def puesto_telas(ctx, x, y, colores):
    box(ctx, "Mostrador", (x, y, 1.0), (4.6, 1.8, 2.0), "#8A5A2B", 0.8)
    for i, c in enumerate(colores):
        box(ctx, "Tela", (x - 1.7 + i * 1.15, y - 0.95, 1.55), (1.0, 0.12, 2.0), c, 0.6, 0.4 if c.startswith("#6B2D") else 0)
    box(ctx, "Toldo", (x, y + 0.4, 4.2), (5.4, 2.6, 0.2), "#C0593B", 0.8)
    for sx in (-1, 1): box(ctx, "Palo", (x + 2.5 * sx, y - 0.7, 2.1), (0.15, 0.15, 4.2), "#6B4A2A", 0.9)


def lanza(ctx, loc, parent=None):
    box(ctx, "asta", loc, (0.12, 0.12, 4.6), "#6B4A2A", 0.9, parent=parent)
    box(ctx, "punta", (loc[0], loc[1], loc[2] + 2.4), (0.22, 0.12, 0.5), "#C9C3B5", 0.3, parent=parent)


def medieval_decor(ctx):
    fondo(ctx, "#B9C6D0", 0.9)
    box(ctx, "Suelo", (0, 20, -0.25), (200, 120, 0.5), "#77716A", 0.95)
    rnd = random.Random(3)
    for i in range(7):
        for j in range(9):
            g = rnd.choice(["#6A655E", "#85807A", "#706B64"])
            box(ctx, "Adoquin", (-6.3 + i * 2.1, -4 + j * 2.8, 0.0), (1.9, 2.6, 0.05), g, 0.95)
    for sx in (-1, 1):
        for k in range(5):
            y = 3 + k * 7.5; h = 7 + (k % 3) * 1.6
            box(ctx, "Casa", (sx * 11, y, h / 2), (8, 6.5, h), "#D8C7A5", 0.95)
            for vx in (-3.0, 0.0, 3.0): box(ctx, "Viga", (sx * (11 - 4.03), y + vx * 0.9, h / 2), (0.08, 0.35, h), "#4A3524", 0.9)
            box(ctx, "Viga h", (sx * (11 - 4.03), y, h * 0.55), (0.08, 6.5, 0.35), "#4A3524", 0.9)
            box(ctx, "Tejado", (sx * 11, y, h + 0.7), (9, 7.5, 1.4), "#8A3B2A", 0.9)
            box(ctx, "Ventana", (sx * (11 - 4.05), y - 1.8, h * 0.72), (0.06, 1.1, 1.3), "#2A3140", 0.5)
            box(ctx, "Puerta", (sx * (11 - 4.05), y + 1.8, 1.4), (0.06, 1.3, 2.8), "#5A3A22", 0.9)
    luz(ctx, "Sol", 'SUN', (10, -10, 25), 2.6, "#FFF1D0", rot=(55, 0, 20))
    luz(ctx, "Relleno", 'AREA', (0, -12, 7), 2600, "#FFFFFF", rot=(80, 0, 0), size=14)


def carreta(ctx, loc, rot=0.0):
    r = empty(ctx, "Carreta", loc, (0, 0, rot))
    box(ctx, "base", (0, 0, 1.3), (3.0, 4.2, 0.35), "#8A5A2B", 0.9, parent=r)
    for sy in (-1, 1): box(ctx, "lado", (0, 2.0 * sy, 1.8), (3.0, 0.2, 0.9), "#7A4A22", 0.9, parent=r)
    box(ctx, "paja", (0, 0, 2.0), (2.7, 3.6, 0.9), "#D9B25A", 0.95, parent=r)
    for sx in (-1, 1): cyl(ctx, "rueda", (1.7 * sx, 0, 0.95), 0.95, 0.25, "#4A3524", 0.9, rot=(0, rad(90), 0), parent=r, verts=12)
    return r


def paris_decor(ctx):
    fondo(ctx, "#D4DEE8", 1.0)
    box(ctx, "Suelo", (0, 20, -0.25), (200, 120, 0.5), "#8A8780", 0.9)
    box(ctx, "Calzada", (0, 20, 0.0), (11, 120, 0.04), "#6E6B66", 0.95)
    for sx in (-1, 1):
        for k in range(5):
            y = 3 + k * 8.5
            box(ctx, "Edificio", (sx * 12, y, 8), (9, 8, 16), "#E6DCC3", 0.9)
            box(ctx, "Mansarda", (sx * 12, y, 16.8), (9.6, 8.6, 1.8), "#59606B", 0.8)
            for fz in (3.5, 7.5, 11.5):
                for fy in (-2.4, 0, 2.4):
                    box(ctx, "Ventana", (sx * (12 - 4.55), y + fy, fz), (0.06, 1.2, 2.0), "#4A5568", 0.4)
                    box(ctx, "Contraventana", (sx * (12 - 4.6), y + fy + 0.85, fz), (0.05, 0.4, 2.0), "#3E5C54", 0.8)
                box(ctx, "Balcon", (sx * (12 - 4.8), y, fz - 1.15), (0.5, 8, 0.12), "#15140F", 0.5)
    for sx in (-1, 1):
        cyl(ctx, "Farola", (sx * 5.0, 4, 2.5), 0.12, 5, "#15140F", 0.4)
        box(ctx, "Farol", (sx * 5.0, 4, 5.3), (0.55, 0.55, 0.8), "#FFD27A", 0.4, 3)
    luz(ctx, "Sol", 'SUN', (10, -10, 25), 3.0, "#FFF1D0", rot=(55, 0, 20))
    luz(ctx, "Relleno", 'AREA', (0, -12, 7), 2600, "#FFFFFF", rot=(80, 0, 0), size=14)


def dama(ctx, name, loc, rot, tela, skin=None):
    """Persona con vestido de crinolina (1852)."""
    sk = skin or S[0]
    r = person(ctx, name, loc, rot_z=rot, skin=sk, hair="#2A1B12", hairstyle="long", top=tela, sleeve=tela, pants=tela,
               shoe_l="#2B2B33", face_kind="happy", extras=lambda c, rr: (
                   cyl(c, "crinolina", (0, 0, 1.15), 1.45, 2.1, tela, 0.8, r2=0.8, parent=rr),
                   box(c, "cinta", (0, -0.37, 2.0), (1.25, 0.05, 0.14), "#7A1F2B", 0.6, parent=rr),
                   box(c, "sombrero", (0, 0.0, 4.72), (1.4, 1.4, 0.16), "#F4F1EA", 0.7, parent=rr, bevel=True),
                   box(c, "lazo", (0.6, -0.4, 4.78), (0.3, 0.2, 0.3), "#7A1F2B", 0.6, parent=rr)))
    r["rig"] = name
    return r


def maniqui(ctx, loc, completo=True):
    r = empty(ctx, "Maniqui", loc)
    PEL = "#E9DFC9"
    cyl(ctx, "peana", (0, 0.3, 0.1), 0.9, 0.2, "#3A372D", 0.5, parent=r)
    cyl(ctx, "poste", (0, 0.3, 1.8), 0.12, 3.4, "#3A372D", 0.5, parent=r)
    box(ctx, "torso", (0, 0, 3.0), (1.2, 0.7, 1.6), PEL, 0.7, parent=r, bevel=True)
    box(ctx, "cuello", (0, 0, 3.95), (0.4, 0.4, 0.3), PEL, 0.7, parent=r)
    sphere(ctx, "cabeza", (0, 0, 4.45), 0.5, PEL, 0.7, parent=r)
    if completo:
        box(ctx, "camisa", (0, -0.02, 3.35), (1.3, 0.78, 0.95), "#F7F4EE", 0.8, parent=r, bevel=True)
        box(ctx, "chaqueta", (0, -0.03, 3.0), (1.36, 0.8, 0.7), "#E3873F", 0.8, parent=r, bevel=True)
        box(ctx, "pantalon i", (-0.32, 0, 1.55), (0.5, 0.55, 2.0), "#1F2A4D", 0.8, parent=r, bevel=True)
        box(ctx, "pantalon d", (0.32, 0, 1.55), (0.5, 0.55, 2.0), "#1F2A4D", 0.8, parent=r, bevel=True)
        for sx in (-1, 1): box(ctx, "zapato", (0.32 * sx, -0.1, 0.4), (0.5, 0.8, 0.4), "#5C3A28", 0.5, parent=r, bevel=True)
        cyl(ctx, "ala", (0, 0, 4.78), 0.75, 0.08, "#15140F", 0.3, parent=r)
        cyl(ctx, "copa", (0, 0, 5.3), 0.42, 1.0, "#15140F", 0.3, parent=r)
        box(ctx, "bufanda", (0, -0.4, 3.85), (0.8, 0.3, 0.25), "#7A1F2B", 0.8, parent=r)
    return r


def taller_decor(ctx):
    fondo(ctx, "#6E5A44", 0.7)
    box(ctx, "Suelo", (0, 5, -0.2), (40, 30, 0.4), "#7A5A3A", 0.7)
    box(ctx, "Pared", (0, 12, 6), (40, 0.4, 12), "#CDB894", 0.9)
    box(ctx, "Ventanal", (-5, 11.7, 5.5), (4, 0.1, 5), "#BFE3FF", 0.3, 1.5)
    for k, c in enumerate(["#7A1F2B", "#1F2A4D", "#E3873F", "#2E9E5B", "#F4F1EA", "#6B2D8A"]):
        cyl(ctx, "rollo tela", (4.5 + (k % 3) * 1.1, 11.0, 5.6 - (k // 3) * 1.1), 0.5, 1.8, c, 0.8, rot=(0, rad(90), 0))
    box(ctx, "Estante", (6, 11.5, 4.5), (4.5, 1.0, 0.2), "#6B4A2A", 0.8)
    box(ctx, "Estante2", (6, 11.5, 3.4), (4.5, 1.0, 0.2), "#6B4A2A", 0.8)
    mesa = box(ctx, "Mesa", (0, 6.0, 1.0), (5.0, 2.2, 0.25), "#8A5E38", 0.7)
    for sx in (-1, 1): box(ctx, "Pata", (2.1 * sx, 6.0, 0.5), (0.25, 1.8, 1.0), "#6B4A2A", 0.8)
    luz(ctx, "Ventana", 'AREA', (-5, 6, 8), 5000, "#CFE8FF", rot=(60, 0, -20), size=6)
    luz(ctx, "Calida", 'AREA', (0, -8, 6), 3000, "#FFE0B0", rot=(80, 0, 0), size=12)
    return mesa


def revista(ctx, loc, escala=1.0):
    """Revista abierta de frente con minifiguras de looks; devuelve (raíz, página que pasa)."""
    r = empty(ctx, "Revista", loc); r.scale = (escala,) * 3
    cols = [("#E3873F", "#1F2A4D"), ("#2E9E5B", "#F4F1EA"), ("#7A1F2B", "#C9B79C"), ("#6B2D8A", "#15140F"), ("#F4F1EA", "#3B4A63"), ("#D9A23F", "#6B4226")]
    def figuras(parent, off, ci):
        for a, b in ((-0.4, 0.55), (0.4, 0.55), (-0.4, -0.55), (0.4, -0.55)):
            c1, c2 = cols[ci % len(cols)]; ci += 1
            box(ctx, "mini cabeza", (a, -0.08, b + 0.5), (0.2, 0.05, 0.2), "#F0CFA8", 0.6, parent=parent)
            box(ctx, "mini torso", (a, -0.08, b + 0.2), (0.3, 0.05, 0.35), c1, 0.8, parent=parent)
            box(ctx, "mini piernas", (a, -0.08, b - 0.1), (0.26, 0.05, 0.3), c2, 0.8, parent=parent)
    box(ctx, "lomo", (0, 0.05, 0), (0.1, 0.12, 2.3), "#7A1F2B", 0.7, parent=r)
    izq = box(ctx, "pagina izq", (-0.82, 0, 0), (1.6, 0.05, 2.2), "#F7F4EE", 0.8, parent=r); figuras(izq, 0, 0)
    der = box(ctx, "pagina der", (0.82, 0, 0), (1.6, 0.05, 2.2), "#F7F4EE", 0.8, parent=r); figuras(der, 0, 2)
    pv = empty(ctx, "pivote pagina", (0, -0.03, 0), (0, 0, 0), r)
    pag = box(ctx, "pagina", (0.8, 0, 0), (1.6, 0.04, 2.2), "#FBF8F1", 0.8, parent=pv); figuras(pag, 0, 4)
    return r, pv
