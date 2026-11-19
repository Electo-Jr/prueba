"""Crea las «cartas» humorísticas (1672x941) que saltan en los clips del podcast, con emojis a color.
Uso: PYTHONUTF8=1 python cartas.py   → `video\\podcast\\imagenes\\carta-*.png` (hechas con Chrome sin interfaz, gratis)."""
import os
import subprocess

CHROME = "/usr/bin/google-chrome"
OUT = "/home/user/prueba/socly-video/video/podcast/imagenes"
TMP = "/home/user/prueba/socly-video/trabajo/cartas"
os.makedirs(TMP, exist_ok=True)

BASE = """<!doctype html><meta charset="utf-8"><style>
html,body{margin:0;width:1672px;height:941px;overflow:hidden;font-family:'Arial Black','Segoe UI Black','Arial',sans-serif}
.c{width:1672px;height:941px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;position:relative}
.e{font-family:'Segoe UI Emoji','Noto Color Emoji',sans-serif;line-height:1}
</style>"""

CARDS = {
    "apple": """<div class="c" style="background:radial-gradient(circle at 50% 40%,#2b2b2e,#000 70%);color:#fff">
<div style="font-size:70px;letter-spacing:4px;color:#a1a1a6;font-family:Arial,sans-serif;font-weight:300">ONE MORE THING…</div>
<div class="e" style="font-size:430px;margin:10px 0">🍎</div>
<div style="font-size:120px;letter-spacing:-2px">Apple</div></div>""",
    "lv": """<div class="c" style="background:repeating-linear-gradient(45deg,#3a2112 0 60px,#46291a 60px 120px);color:#e8c36a">
<div class="e" style="font-size:330px">👜</div>
<div style="font-size:118px;letter-spacing:6px;font-family:Georgia,serif;margin-top:20px;text-shadow:0 4px 0 #1d0f07">LOUIS VUITTON</div>
<div style="font-size:52px;font-family:Arial,sans-serif;color:#f1e3b8;margin-top:12px">(nada barato)</div></div>""",
    "android": """<div class="c" style="background:#3ddc84;color:#073042">
<div class="e" style="font-size:430px">🤖</div>
<div style="font-size:150px;letter-spacing:-2px;margin-top:10px">ANDROID</div></div>""",
    "colores": """<div class="c" style="flex-direction:row">
<div style="flex:1;height:100%;background:#0f0f12;color:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center"><div class="e" style="font-size:330px">🌙</div><div style="font-size:100px;margin-top:20px">OSCURO</div></div>
<div style="flex:1;height:100%;background:#f4f1ea;color:#15140f;display:flex;flex-direction:column;align-items:center;justify-content:center"><div class="e" style="font-size:330px">☀️</div><div style="font-size:100px;margin-top:20px">CLARO</div></div></div>""",
    "maniqui": """<div class="c" style="background:linear-gradient(160deg,#f4f1ea,#d9d2c3);color:#15140f">
<div class="e" style="font-size:420px">👗</div>
<div style="font-size:120px;letter-spacing:-2px;margin-top:14px">EL MANIQUÍ</div>
<div style="font-size:54px;font-family:Arial,sans-serif;color:#6b6558;margin-top:6px">(pack premium)</div></div>""",
    "notif": """<div class="c" style="background:#15140f;color:#f4f1ea">
<div style="position:relative"><div class="e" style="font-size:400px">🔔</div><div style="position:absolute;top:10px;right:-70px;background:#ff3b30;color:#fff;border-radius:80px;font-size:84px;padding:6px 36px">99+</div></div>
<div style="font-size:92px;letter-spacing:-1px;margin-top:20px">ACTIVA LAS NOTIFICACIONES</div></div>""",
}

for name, body in CARDS.items():
    html = f"{TMP}/{name}.html"
    open(html, "w", encoding="utf-8").write(BASE + body)
    out = f"{OUT}/carta-{name}.png"
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                    "--window-size=1672,941", f"--screenshot={out}", "file:///" + html.replace("\\", "/")],
                   check=True, capture_output=True, timeout=120)
    print("ok", out)
