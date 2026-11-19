"""Despegue del cohete (2,5 s a 30 fps = 75 fotogramas). Se carga con exec tras lib.py.
Variables esperadas: F0, F1 (rango de fotogramas a renderizar)."""
import bpy, math, random, time
sc = bpy.data.scenes["Cohete"]; bpy.context.window.scene = sc
O = bpy.data.objects
RX, RY = 0.0, 14.0
rk = O["Cohete"]
fire = sorted([o for o in O if o.name.startswith("fuego") and o.users_scene], key=lambda o: o.name)
smoke = sorted([o for o in O if o.name.startswith("humo") and o.users_scene], key=lambda o: o.name)
people = [O["Publico%d" % i] for i in range(4)]
cam = sc.camera
FIRE_H = [1.6, 1.9, 2.3]

# guardar posiciones base la primera vez
for o in smoke + people + [cam]:
    if "base" not in o:
        o["base"] = list(o.location)
        o["bscale"] = list(o.scale)
if "Fuego luz" not in O:
    d = bpy.data.lights.new("Fuego luz", 'POINT'); d.color = (1.0, 0.45, 0.1); d.energy = 0
    lo = bpy.data.objects.new("Fuego luz", d); bpy.data.collections["Cohete col"].objects.link(lo)
lo = O["Fuego luz"]

A = 19.0  # aceleracion
def set_frame(f):
    t = f / 30.0
    rz = 1.0 + 0.5 * A * t * t
    rk.location.z = rz
    rnd = random.Random(f * 7 + 1)
    s = 1.0 + t * 2.2
    for i, o in enumerate(fire):
        k = s * (0.85 + 0.3 * rnd.random())
        o.scale = (1 + 0.1 * rnd.random(), 1 + 0.1 * rnd.random(), k)
        o.location = (RX, RY, rz + 0.25 - FIRE_H[i] * k / 2)
    lo.location = (RX, RY - 1.5, rz - 1.0)
    lo.data.energy = 60000 * (0.7 + 0.5 * rnd.random()) * min(1.0, 0.4 + t)
    for i, o in enumerate(smoke):
        b = o["base"]; bs = o["bscale"]; g = 1 + 0.9 * min(t / 1.5, 1)
        ang = math.atan2(b[1] - RY, b[0] - RX)
        o.location = (b[0] + math.cos(ang) * 1.1 * t, b[1] + math.sin(ang) * 1.1 * t, b[2] + 0.6 * t * ((i % 3) + 1) / 3)
        o.scale = (bs[0] * g, bs[1] * g, bs[2] * g)
    for i, o in enumerate(people):
        b = o["base"]; jump = abs(math.sin(t * 9 + i)) * 0.5 if t > 0.2 else 0
        o.location = (b[0], b[1], b[2] + jump)
    # camara: sigue al cohete con tope de inclinacion; temblor que sube y baja
    tz = rz * 0.55 + 4
    pitch = min(90 + math.degrees(math.atan2(tz - 1.6, 22)), 122)
    amp = min(1.0, t / 0.5) * (1.0 if t < 1.8 else max(0.25, 1 - (t - 1.8) * 1.2))
    cam.location = (amp * 0.16 * (rnd.random() - 0.5) * 2, -22 + amp * 0.1 * (rnd.random() - 0.5) * 2, 1.6 + amp * 0.12 * (rnd.random() - 0.5) * 2)
    cam.rotation_euler = (math.radians(pitch + amp * 0.5 * (rnd.random() - 0.5) * 2), 0, math.radians(amp * 0.4 * (rnd.random() - 0.5) * 2))

r = sc.render; r.engine = 'BLENDER_EEVEE'; r.resolution_x = 1080; r.resolution_y = 1920; r.resolution_percentage = 50
sc.eevee.taa_render_samples = 24
os.makedirs(OUT + r"\despegue", exist_ok=True)
t0 = time.time()
for f in range(F0, F1 + 1):
    set_frame(f)
    r.filepath = OUT + r"\despegue\f_%04d.png" % f
    bpy.ops.render.render(write_still=True)
print("fotogramas", F0, "a", F1, "en", round(time.time() - t0, 1), "s")
