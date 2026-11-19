"""Genera build_v2.py (versión de 20 s, con el gancho primero) a partir de build.py. Uso: python gen_v2.py"""
import io
s = io.open("build.py", encoding="utf-8").read()


def between(a, b, new):
    global s
    i = s.index(a)
    j = s.index(b, i)
    s = s[:i] + new + s[j:]


def rep(a, b):
    global s
    assert a in s, a[:60]
    s = s.replace(a, b, 1)


rep('Vídeo «Cómo subir tu ropa bien» (9:16', 'VERSIÓN 2 (≈20 s, gancho primero) de «Cómo subir tu ropa bien» (9:16')
rep('subir-bien"\n', 'subir-bien-v2"\n') if False else None
rep('/scratchpad/subir-bien"', '/scratchpad/subir-bien-v2"')
between("SEGS = [", "t0 = 0.0", '''SEGS = [
    dict(n="bad1",  f="08-IMG_7450.mov", a=0.0, b=1.66, v=1.0, kind="cam", vol=0.35, bw=True, hold=0.4),
    dict(n="bad2",  f="09-IMG_7452.mov", a=0.0, b=1.80, v=1.0, kind="cam", vol=0.35, bw=True, hold=0.3),
    dict(n="unfold", f="03-IMG_7448.mov", a=0.90, b=5.30, v=3.6, kind="cam", vol=None),
    dict(n="shoot", f="04-IMG_7449.mov", a=0.0, b=2.3, v=1.0, kind="cam", vol=0.5),
    dict(n="app1",  f="05-ScreenRecording_11-04-2026_20-01-31_1.mov", a=0.4, b=2.9, v=1.0, kind="scr", vol=None),
    dict(n="app2",  f="06-ScreenRecording_11-04-2026_20-01-31_1.mov", a=0.0, b=25.0, v=15.0, kind="scr", vol=None),
    dict(n="clean", f="07-ScreenRecording_11-04-2026_20-01-31_1.mov", a=0.0, b=1.0, v=1.0, kind="scr", vol=None, hold=1.2),
    dict(n="good2", f="10-IMG_7454.mov", a=0.0, b=0.70, v=0.5, kind="cam", vol=0.5, hold=1.2, zoom=True),
    dict(n="end",   f=None, a=0, b=2.4, v=1.0, kind="end", vol=None),
]

''')
between("# cuándo suena cada cosa", "mix = voice + sfx", '''# cuándo suena cada cosa (tiempos absolutos)
CHECK_APP = T["app1"] + 1.3
BAD1, BAD2 = T["bad1"] + 0.03, T["bad2"] + 0.03
GOOD2 = T["good2"] + 0.15
put(buzz(), BAD1, 0.6)
put(buzz(), BAD2, 0.55)
put(whoosh(0.45), T["unfold"] - 0.15, 0.5)
put(pop(), T["app1"] + 0.5, 0.35)          # al hacer la foto
put(ding(), CHECK_APP, 0.5)
put(whoosh(0.3), T["app2"] - 0.1, 0.35)
put(pop(), T["clean"] + 0.1, 0.4)
put(whoosh(0.4), T["good2"] - 0.2, 0.4)
put(ding(), GOOD2, 0.55)
put(whoosh(0.5), T["end"] - 0.25, 0.5)
put(pop(), T["end"] + 0.35, 0.35)
''')
between("ICONS = [", "icon(\"ok\"), icon(\"no\")", '''ICONS = [  # archivo, inicio, duración, centro y, ancho, alto
    ("titulo", 0.0, D["bad1"], 310, 828, 342),
    ("no", BAD1, 1.5, 700, 223, 223),
    ("no", BAD2, 1.6, 640, 223, 223),
    ("asi", T["unfold"], T["app1"] - T["unfold"], 310, 640, 300),
    ("ok", CHECK_APP, 1.1, 430, 223, 223),
    ("ok", GOOD2, 2.2, 640, 223, 223),
]
''')
between("def titulo():", "# --- 4) subtítulos", '''def titulo():
    """Tarjetas de título: cristal oscuro, filete dorado, Arial Black."""
    from PIL import ImageFont

    def card(name, Wd, Ht, small, lines):
        im = Image.new("RGBA", (Wd, Ht), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle((6, 6, Wd - 6, Ht - 6), radius=44, fill=(10, 10, 10, 168), outline=(242, 184, 75, 255), width=5)
        f2 = ImageFont.truetype("C:/Windows/Fonts/ariblk.ttf", 34)
        d.text((Wd / 2, 58), small, font=f2, fill=(242, 184, 75, 255), anchor="mt")
        y = 135
        for parts, size in lines:
            f = ImageFont.truetype("C:/Windows/Fonts/ariblk.ttf", size)
            tot = sum(d.textlength(t, font=f) for t, _ in parts)
            x = (Wd - tot) / 2
            for t, col in parts:
                d.text((x, y), t, font=f, fill=col, anchor="lt")
                x += d.textlength(t, font=f)
            y += int(size * 1.18)
        im.save(f"{W}/icon-{name}.png")

    WH, GO, RD = (255, 255, 255, 255), (242, 184, 75, 255), (255, 86, 86, 255)
    card("titulo", 920, 380, "SOCLY STYLE · GUÍA RÁPIDA",
         [([("ESTÁS SUBIENDO", WH)], 80), ([("TU ROPA ", WH), ("MAL", RD)], 84)])
    card("asi", 700, 330, "SOCLY STYLE · GUÍA RÁPIDA", [([("ASÍ ", WH), ("SÍ", GO)], 130)])


titulo()

''')
between("h = T[\"hook\"] - 0.55", "head = f", r'''cap(T["bad1"] + 0.1, T["bad1"] + D["bad1"], "VARIAS PRENDAS\\NEN UNA FOTO", mv=300)
cap(T["bad2"] + 0.1, T["bad2"] + D["bad2"], "CON AMIGOS O\\NGENTE DETRÁS", mv=300)
cap(T["shoot"] + 0.1, T["shoot"] + D["shoot"], GOLD + "UNA" + WHITE + " PRENDA POR FOTO")
cap(T["app1"] + 0.1, T["app1"] + D["app1"] - 0.1, "ENTERA, SOBRE UNA\\NSUPERFICIE LISA", mv=300)
cap(T["app2"] + 0.05, T["app2"] + D["app2"], GOLD + "RELLENAR POR MÍ", mv=300)
cap(T["clean"] + 0.1, T["clean"] + D["clean"], r"{\an8\fs60}Y QUEDA " + GOLD + r"COMO EN\NUNA TIENDA", mv=250)
cap(T["good2"] + 0.1, T["good2"] + D["good2"], GOLD + "TÚ SOLO" + WHITE + r", EN EL ESPEJO\NCUERPO ENTERO", mv=300)
# tarjeta final: pregunta para comentar
EV.append((T["end"] + 0.25, T["end"] + D["end"], r"{\an5\pos(540,1050)\fs62}" + "¿CUÁL DE ESTAS", 0, "Tik"))
EV.append((T["end"] + 0.50, T["end"] + D["end"], r"{\an5\pos(540,1150)\fs62}" + GOLD + "HACES TÚ?", 0, "Tik"))
EV.append((T["end"] + 1.1, T["end"] + D["end"], r"{\an5\pos(540,1480)\fs44}" + "ENLACE EN LA BIO", 0, "Tik"))

''')
rep('subir-bien.mp4"', 'subir-bien-v2.mp4"')
rep("{ts(b)}", "{ts(max(a + 0.05, b - 0.04))}")
io.open("build_v2.py", "w", encoding="utf-8", newline="").write(s)
print("build_v2.py generado")
