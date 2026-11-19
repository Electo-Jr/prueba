"""Trajes de Soclo por época para «¿De dónde vienen los outfits?» (se carga con exec después de lib.py de ciudad-socly).
era(ctx, nombre, epoca, loc, rot, face, skin, tela) -> personaje. Épocas: casa, prehistoria, egipto, roma, medieval, 1852, 60s, 2010.
`tela` cambia el color de la prenda principal (para gente de fondo: p. ej. el verde de Egipto)."""
import math
S = SKINS
PIEL_CLARA = "#E8DCC0"


def _casa(c, r, tela):
    phone_arm(c, r, "#F7F4EE", S[1], "logo")
    for sx in (-1, 1):
        box(c, "bomber", (0.44 * sx, -0.4, 2.5), (0.42, 0.05, 1.2), "#F7F4EE", 0.7, parent=r)
    box(c, "bomber cintura", (0, 0.02, 1.88), (1.36, 0.84, 0.18), "#D9D5CC", 0.7, parent=r)
    for sx in (-1, 1):
        box(c, "cinta", (0.2 * sx - 0.35, -0.46, 2.3), (0.14, 0.04, 1.2), "#D9A23F", 0.35, parent=r)


def _prehistoria(c, r, tela):
    box(c, "piel", (0, -0.37, 2.45), (1.28, 0.06, 1.0), tela, 0.95, parent=r, bevel=True)
    box(c, "piel borde", (0, -0.38, 1.9), (1.3, 0.07, 0.2), PIEL_CLARA, 0.95, parent=r)
    box(c, "piel hombro", (-0.62, -0.05, 3.08), (0.55, 0.95, 0.38), tela, 0.95, parent=r, bevel=True)
    box(c, "piel cintura", (0, 0, 1.78), (1.4, 0.9, 0.22), tela, 0.95, parent=r, bevel=True)
    for i in range(7):  # borde irregular de la piel
        box(c, "piel pico", (-0.55 + i * 0.185, -0.4, 1.72 - (0.1 if i % 2 else 0.0)), (0.17, 0.06, 0.22), PIEL_CLARA, 0.95, parent=r)
    box(c, "hueso", (0.1, -0.2, 4.72), (0.8, 0.14, 0.14), "#F4F1EA", 0.5, rot=(0, 0.25, 0), parent=r)
    for sx in (-1, 1):
        box(c, "hueso punta", (0.1 + 0.45 * sx, -0.2, 4.72 + 0.11 * sx), (0.22, 0.2, 0.22), "#F4F1EA", 0.5, parent=r)
    rig = RIG.get(r.name)
    if rig and rig["arm"][1] is not None:  # maza de madera
        box(c, "maza", (0, -0.25, -1.55), (0.28, 0.28, 1.5), "#6B4A2A", 0.9, parent=rig["arm"][1], bevel=True)
        box(c, "maza cabeza", (0, -0.25, -2.35), (0.55, 0.55, 0.6), "#6B4A2A", 0.9, parent=rig["arm"][1], bevel=True)
    for i in range(5):  # collar de conchas
        box(c, "concha", (-0.3 + i * 0.15, -0.4, 3.08 - abs(i - 2) * 0.07), (0.11, 0.05, 0.11), "#F4F1EA", 0.4, parent=r)


def _egipto(c, r, tela):
    box(c, "falda lino", (0, 0, 1.55), (1.5, 0.98, 0.95), tela, 0.85, parent=r, bevel=True)
    box(c, "cinturon", (0, 0, 2.0), (1.42, 0.9, 0.14), "#D9A23F", 0.3, parent=r)
    box(c, "collar", (0, -0.2, 3.1), (1.1, 0.7, 0.2), "#D9A23F", 0.3, parent=r, bevel=True)
    for i in range(5):
        box(c, "lapislazuli", (-0.4 + i * 0.2, -0.56, 3.0), (0.12, 0.05, 0.12), "#1F5FA8", 0.3, parent=r)
    # tocado a rayas
    box(c, "tocado", (0, 0.0, 4.62), (1.3, 1.3, 0.3), "#D9A23F", 0.35, parent=r, bevel=True)
    for sx in (-1, 1):
        box(c, "tocado lado", (0.66 * sx, 0.1, 4.0), (0.2, 0.9, 1.2), "#1F5FA8", 0.45, parent=r)
        box(c, "tocado raya", (0.66 * sx, 0.1, 4.2), (0.22, 0.92, 0.2), "#D9A23F", 0.35, parent=r)
    # ojos pintados
    for sx in (-1, 1):
        box(c, "kohl", (0.26 * sx, -0.58, 3.95), (0.34, 0.02, 0.06), "#15140F", 0.6, parent=r)


def _roma(c, r, tela, purpura=False):
    box(c, "toga pecho", (0, -0.37, 2.5), (1.3, 0.08, 1.4), tela, 0.85, parent=r, bevel=True)
    box(c, "toga hombro", (-0.7, 0, 3.0), (0.75, 1.0, 0.5), tela, 0.85, parent=r, bevel=True)
    box(c, "toga caida", (-0.78, -0.1, 2.0), (0.4, 0.95, 1.7), tela, 0.85, parent=r, bevel=True)
    box(c, "toga falda", (0, 0, 1.5), (1.45, 0.95, 0.9), tela, 0.85, parent=r, bevel=True)
    if purpura:
        box(c, "franja purpura", (0.1, -0.42, 2.45), (0.22, 0.04, 1.5), "#6B2D8A", 0.5, 0.4, parent=r)
        box(c, "franja purpura 2", (-0.78, -0.58, 1.9), (0.3, 0.04, 1.7), "#6B2D8A", 0.5, 0.4, parent=r)
    for i in range(8):  # corona de laurel
        a = i / 8 * 2 * math.pi
        box(c, "laurel", (0.64 * math.cos(a), 0.64 * math.sin(a), 4.82), (0.3, 0.3, 0.16), "#4F9A3A", 0.7, parent=r)


def _medieval(c, r, tela):
    box(c, "cinturon cuerda", (0, 0, 1.95), (1.34, 0.84, 0.12), "#C9B79C", 0.9, parent=r)
    box(c, "nudo", (0.35, -0.44, 1.9), (0.14, 0.06, 0.5), "#C9B79C", 0.9, parent=r)
    box(c, "tunica faldon", (0, 0, 1.45), (1.4, 0.92, 0.9), tela, 0.95, parent=r, bevel=True)
    box(c, "capucha", (0, 0.05, 4.62), (1.3, 1.25, 0.4), "#5A4A3A", 0.95, parent=r, bevel=True)
    box(c, "capucha atras", (0, 0.62, 4.0), (1.3, 0.28, 1.4), "#5A4A3A", 0.95, parent=r)
    box(c, "capa hombros", (0, 0.1, 3.3), (1.75, 1.05, 0.3), "#5A4A3A", 0.95, parent=r, bevel=True)
    box(c, "remiendo", (0.3, -0.38, 2.3), (0.3, 0.03, 0.3), "#8A6B3A", 0.9, parent=r)


def _1852(c, r, tela):
    box(c, "camisa", (0, -0.37, 2.95), (0.5, 0.03, 0.9), "#F7F4EE", 0.6, parent=r)
    box(c, "pañuelo cuello", (0, -0.4, 3.2), (0.3, 0.05, 0.2), "#7A1F2B", 0.6, parent=r)
    box(c, "chaleco", (0, -0.375, 2.2), (0.8, 0.04, 0.7), "#3A4670", 0.7, parent=r)
    box(c, "faldon frac", (0, 0.4, 1.7), (0.95, 0.28, 1.3), tela, 0.7, parent=r, bevel=True)
    for sx in (-1, 1):
        box(c, "solapa", (0.42 * sx, -0.4, 2.75), (0.22, 0.05, 0.9), tela, 0.6, rot=(0, 0.1 * sx, 0), parent=r)
    cyl(c, "ala copa", (0, 0, 4.58), 0.85, 0.08, "#15140F", 0.3, parent=r)
    cyl(c, "copa alta", (0, 0, 5.2), 0.5, 1.2, "#15140F", 0.3, parent=r)
    box(c, "cinta copa", (0, 0, 4.78), (1.02, 1.02, 0.14), "#7A1F2B", 0.4, parent=r)


def _60s(c, r, tela):
    for i in range(4):  # rayas de la camiseta
        box(c, "raya", (0, -0.375, 1.95 + i * 0.36), (1.22, 0.04, 0.12), "#F7F4EE", 0.7, parent=r)
    box(c, "cuello grande", (0, -0.3, 3.18), (0.9, 0.4, 0.14), "#F7F4EE", 0.7, rot=(0.3, 0, 0), parent=r)
    rig = RIG.get(r.name)
    if rig:  # pantalones de campana: patas anchas que caminan con la cadera
        for hp in rig["hip"]:
            box(c, "campana", (0, -0.06, 0.45 - 1.75), (0.62, 0.82, 0.55), "#6B4226", 0.8, parent=hp, bevel=True)


def _2010(c, r, tela):
    box(c, "capucha", (0, 0.55, 3.35), (1.0, 0.45, 0.5), tela, 0.9, parent=r, bevel=True)
    box(c, "bolsillo", (0, -0.4, 2.0), (0.8, 0.05, 0.4), "#58627A", 0.9, parent=r)
    for sx in (-1, 1):
        box(c, "cordon", (0.12 * sx, -0.4, 2.85), (0.05, 0.04, 0.45), "#F7F4EE", 0.6, parent=r)
        box(c, "auricular", (0.58 * sx, 0, 3.95), (0.1, 0.22, 0.22), "#F7F4EE", 0.5, parent=r)
    phone_arm(c, r, tela, S[1], "ad")
    box(c, "pantalla azul", (0.88, -1.07, 2.95), (0.54, 0.01, 1.0), "#4C7BD9", 0.4, 1.6, parent=r)
    box(c, "icono foto", (0.88, -1.08, 3.15), (0.26, 0.01, 0.26), "#F4F1EA", 0.4, 1.0, parent=r)


# epoca: (kwargs de person, extras, color de tela por defecto)
EPOCAS = {
    "casa": (dict(top="#15140F", sleeve="#F7F4EE", pants="#3B4A63", shoe_l="#F7F4EE", sole="#D9A23F", hairstyle="flat", arm_r=None), _casa, "#F7F4EE"),
    "prehistoria": (dict(top="#8A5A2B", sleeve=S[1], pants="#8A5A2B", shoe_l=S[1], hairstyle="long", shorts=True), _prehistoria, "#8A5A2B"),
    "egipto": (dict(top=S[1], sleeve=S[1], pants="#F4F1EA", shoe_l="#D9A23F", hairstyle="none", shorts=True), _egipto, "#F4F1EA"),
    "roma": (dict(top="#F4F1EA", sleeve=S[1], pants="#F4F1EA", shoe_l="#8A5A2B", hairstyle="flat", shorts=True), _roma, "#F4F1EA"),
    "medieval": (dict(top="#7B5B3A", sleeve="#7B5B3A", pants="#5A4A3A", shoe_l="#3A2A1A", hairstyle="none"), _medieval, "#7B5B3A"),
    "1852": (dict(top="#15140F", sleeve="#15140F", pants="#2B2B33", shoe_l="#0B0B0D", hairstyle="none"), _1852, "#15140F"),
    "60s": (dict(top="#E3873F", sleeve="#E3873F", pants="#6B4226", shoe_l="#F7F4EE", hairstyle="long"), _60s, "#E3873F"),
    "2010": (dict(top="#6B7A8F", sleeve="#6B7A8F", pants="#1F2A4D", shoe_l="#F7F4EE", sole="#D9D5CC", hairstyle="flat", arm_r=None), _2010, "#6B7A8F"),
}


def era(ctx, name, epoca, loc, rot=0.0, face="happy", skin=None, hair="#2A1B12", tela=None, **extra):
    kw, fn, tela0 = EPOCAS[epoca]
    kw = dict(kw)
    t = tela or tela0
    if tela:  # la tela elegida sustituye al color principal de la prenda
        for k in ("top", "sleeve", "pants"):
            if kw.get(k) == tela0:
                kw[k] = tela
    sk = skin or S[1]
    if skin:
        for k in ("top", "sleeve", "pants", "shoe_l"):
            if kw.get(k) == S[1]:
                kw[k] = skin
    kw.update(extra)
    root = person(ctx, name, loc, rot_z=rot, skin=sk, hair=hair, face_kind=face, extras=lambda c, r: fn(c, r, t), **kw)
    root["rig"] = name
    return root


def era_purpura(ctx, name, loc, rot=0.0, face="smug"):
    """Senador romano con franjas púrpura."""
    kw, _, _ = EPOCAS["roma"]
    return person(ctx, name, loc, rot_z=rot, skin=S[0], hair="#CFCFD4", face_kind=face,
                  extras=lambda c, r: _roma(c, r, "#F4F1EA", purpura=True), **kw)
