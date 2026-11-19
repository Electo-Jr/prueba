"""Dibuja el micrófono de podcast (falso, solo decorativo) y los coloca sobre un lienzo 1920x1080 transparente.
Uso: python mic.py   → `video\\podcast\\sonidos\\..\\mics.png` (herramientas\\podcast\\mics.png)"""
from PIL import Image, ImageDraw, ImageFilter

S = 4  # supersampling
W, H = 130, 360  # tamaño del micro en px de salida


def gradient_h(w, h, c1, c2, c3):
    """Degradado horizontal cilíndrico: c1 borde, c2 centro-luz, c3 borde oscuro."""
    img = Image.new("RGB", (w, h))
    px = img.load()
    for x in range(w):
        t = x / (w - 1)
        if t < 0.35:
            k = t / 0.35
            c = tuple(int(c1[i] + (c2[i] - c1[i]) * k) for i in range(3))
        else:
            k = (t - 0.35) / 0.65
            c = tuple(int(c2[i] + (c3[i] - c2[i]) * k) for i in range(3))
        for y in range(h):
            px[x, y] = c
    return img


def mic():
    w, h = W * S, H * S
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx = w // 2
    # base y pie
    d.ellipse([cx - 55 * S, h - 26 * S, cx + 55 * S, h - 4 * S], fill=(24, 24, 28, 255))
    d.ellipse([cx - 55 * S, h - 30 * S, cx + 55 * S, h - 12 * S], fill=(48, 48, 54, 255))
    # tallo
    stem = gradient_h(14 * S, 110 * S, (60, 60, 66), (150, 150, 158), (28, 28, 32))
    im.paste(stem, (cx - 7 * S, h - 140 * S))
    # cuerpo del micro
    body_w, body_h = 78 * S, 150 * S
    body = gradient_h(body_w, body_h, (50, 50, 56), (120, 120, 128), (18, 18, 22)).convert("RGBA")
    mask = Image.new("L", (body_w, body_h), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, body_w - 1, body_h - 1], radius=14 * S, fill=255)
    im.paste(body, (cx - body_w // 2, h - 250 * S), mask)
    # anillo crema
    d.rounded_rectangle([cx - body_w // 2, h - 205 * S, cx + body_w // 2, h - 195 * S], radius=4 * S, fill=(244, 241, 234, 255))
    # cabeza con rejilla
    head_w, head_h = 100 * S, 130 * S
    head = gradient_h(head_w, head_h, (70, 70, 76), (150, 150, 158), (30, 30, 34)).convert("RGBA")
    hm = Image.new("L", (head_w, head_h), 0)
    ImageDraw.Draw(hm).rounded_rectangle([0, 0, head_w - 1, head_h - 1], radius=44 * S, fill=255)
    hd = ImageDraw.Draw(head)
    for k in range(-head_h, head_w + head_h, 9 * S):
        hd.line([(k, 0), (k + head_h, head_h)], fill=(20, 20, 24, 150), width=S)
        hd.line([(k, head_h), (k + head_h, 0)], fill=(20, 20, 24, 150), width=S)
    im.paste(head, (cx - head_w // 2, h - 360 * S + 4 * S), hm)
    # brillo
    d.rounded_rectangle([cx - 34 * S, h - 340 * S, cx - 24 * S, h - 270 * S], radius=5 * S, fill=(255, 255, 255, 70))
    im = im.resize((W, H), Image.LANCZOS)
    return im


def sheet(positions):
    """positions: lista de (x_centro, y_base, ángulo). Devuelve un lienzo 1920x1080."""
    canvas = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    m = mic()
    for x, yb, ang in positions:
        r = m.rotate(ang, resample=Image.BICUBIC, expand=True)
        shadow = Image.new("RGBA", r.size, (0, 0, 0, 0))
        shadow.paste((0, 0, 0, 90), mask=r.split()[3])
        shadow = shadow.filter(ImageFilter.GaussianBlur(10))
        canvas.alpha_composite(shadow, (int(x - r.width / 2 + 10), int(yb - r.height + 6)))
        canvas.alpha_composite(r, (int(x - r.width / 2), int(yb - r.height)))
    return canvas


if __name__ == "__main__":
    # micro izquierdo inclinado hacia la izquierda (hacia su persona), derecho hacia la derecha
    sheet([(640, 1005, 8), (1340, 1000, -8)]).save("/home/user/prueba/socly-video/video/herramientas/podcast/mics.png")
    print("ok")
