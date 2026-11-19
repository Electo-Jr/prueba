import numpy as np, zlib, struct, os, math
OUT = os.path.dirname(os.path.abspath(__file__))

def write_png(path, arr):
    h, w, _ = arr.shape
    raw = b''.join(b'\x00' + arr[y].tobytes() for y in range(h))
    def chunk(t, d):
        c = struct.pack('>I', len(d)) + t + d
        return c + struct.pack('>I', zlib.crc32(t + d) & 0xffffffff)
    png = b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 6, 0, 0, 0)) + chunk(b'IDAT', zlib.compress(raw, 6)) + chunk(b'IEND', b'')
    open(path, 'wb').write(png)

SS = 4  # supersampling

def finish(mask, color):
    """mask float (H*SS,W*SS) in 0..1 -> RGBA uint8 (H,W)"""
    h, w = mask.shape[0] // SS, mask.shape[1] // SS
    m = mask.reshape(h, SS, w, SS).mean(axis=(1, 3))
    out = np.zeros((h, w, 4), np.uint8)
    out[..., 0], out[..., 1], out[..., 2] = color
    out[..., 3] = (np.clip(m, 0, 1) * 255).astype(np.uint8)
    return out

def grid(w, h):
    ys, xs = np.mgrid[0:h * SS, 0:w * SS]
    return (xs + 0.5) / SS, (ys + 0.5) / SS

def rrect_mask(w, h, r, x0=0, y0=0, x1=None, y1=None):
    x, y = grid(w, h)
    x1 = w if x1 is None else x1; y1 = h if y1 is None else y1
    cx = np.clip(x, x0 + r, x1 - r); cy = np.clip(y, y0 + r, y1 - r)
    d = np.hypot(x - cx, y - cy)
    inside = (x >= x0) & (x <= x1) & (y >= y0) & (y <= y1)
    return ((d <= r) & inside).astype(float)

# --- píldora de búsqueda blanca con lupa y micro ---
def pill(w=500, h=76):
    x, y = grid(w, h)
    m = rrect_mask(w, h, h / 2)
    base = np.zeros((h, w, 4), np.uint8)
    white = finish(m, (255, 255, 255))
    # lupa
    cx, cy, r = 40, h / 2 - 2, 9
    ring = (np.abs(np.hypot(x - cx, y - cy) - r) <= 1.8).astype(float)
    # mango: segmento de (cx+r*.7, cy+r*.7) a +9
    t = np.clip(((x - (cx + r * .7)) + (y - (cy + r * .7))) / (2 * 8), 0, 1)
    px, py = cx + r * .7 + t * 8, cy + r * .7 + t * 8
    handle = (np.hypot(x - px, y - py) <= 1.8).astype(float)
    icon = finish(np.maximum(ring, handle), (70, 70, 70))
    # micro
    mx, my = w - 40, h / 2
    cap = rrect_mask(w, h, 4.5, mx - 4.5, my - 12, mx + 4.5, my + 3)
    arc = ((np.abs(np.hypot(x - mx, y - (my - 2)) - 9) <= 1.6) & (y > my - 2)).astype(float)
    stem = ((np.abs(x - mx) <= 1.5) & (y > my + 7) & (y < my + 13)).astype(float)
    mic = finish(np.maximum(np.maximum(cap, arc), stem), (70, 70, 70))
    out = white.astype(float)
    for layer in (icon, mic):
        a = layer[..., 3:4] / 255.0
        out[..., :3] = out[..., :3] * (1 - a) + layer[..., :3] * a
        out[..., 3:4] = np.maximum(out[..., 3:4], layer[..., 3:4])
    return out.astype(np.uint8)

# --- trazos blancos ---
def bar(length, thick, angle_deg):
    pad = int(length * 0.2) + 6
    w = h = int(length + pad * 2)
    x, y = grid(w, h)
    a = math.radians(angle_deg)
    u = (x - w / 2) * math.cos(a) + (y - h / 2) * math.sin(a)
    v = -(x - w / 2) * math.sin(a) + (y - h / 2) * math.cos(a)
    cu = np.clip(u, -length / 2 + thick / 2, length / 2 - thick / 2)
    d = np.hypot(u - cu, v)
    return finish((d <= thick / 2).astype(float), (255, 255, 255))

# --- cursor ---
def cursor(scale=2.0):
    pts = np.array([(0, 0), (0, 22), (5.5, 17.5), (9.5, 27), (13, 25.5), (9, 16.5), (16, 16.5)]) * scale
    w, h = int(pts[:, 0].max()) + 8, int(pts[:, 1].max()) + 8
    x, y = grid(w, h)
    def inside(P):
        n = len(P); res = np.zeros_like(x, bool)
        for i in range(n):
            x1, y1 = P[i]; x2, y2 = P[(i + 1) % n]
            cond = ((y1 > y) != (y2 > y)) & (x < (x2 - x1) * (y - y1) / (y2 - y1 + 1e-9) + x1)
            res ^= cond
        return res
    P = pts + 3
    fill = inside(P).astype(float)
    # contorno blanco: dilatar
    from itertools import product
    big = np.zeros_like(fill)
    k = int(2.2 * SS)
    for dx, dy in product(range(-k, k + 1, 2), repeat=2):
        if dx * dx + dy * dy <= k * k:
            big = np.maximum(big, np.roll(np.roll(fill, dy, 0), dx, 1))
    outline = finish(big, (255, 255, 255))
    body = finish(fill, (20, 20, 20))
    a = body[..., 3:4] / 255.0
    res = outline.astype(float)
    res[..., :3] = res[..., :3] * (1 - a) + body[..., :3] * a
    return res.astype(np.uint8)

# --- anillo de luz ---
def ring(size=360, r=58, thick=9):
    x, y = (np.mgrid[0:size, 0:size] + 0.5)[1], (np.mgrid[0:size, 0:size] + 0.5)[0]
    d = np.hypot(x - size / 2, y - size / 2)
    core = np.exp(-((d - r) ** 2) / (2 * (thick / 2) ** 2))
    glow = 0.55 * np.exp(-((d - r) ** 2) / (2 * 22 ** 2))
    a = np.clip(core + glow, 0, 1)
    out = np.zeros((size, size, 4), np.uint8)
    out[..., :3] = 255
    out[..., 3] = (a * 255).astype(np.uint8)
    return out

if __name__ == '__main__':
    write_png(f'{OUT}/pill.png', pill())
    write_png(f'{OUT}/bar1.png', bar(110, 12, -28))
    write_png(f'{OUT}/bar2.png', bar(90, 11, -10))
    write_png(f'{OUT}/bar3.png', bar(100, 12, 18))
    write_png(f'{OUT}/cursor.png', cursor())
    write_png(f'{OUT}/ring.png', ring())
    print('assets ok')
