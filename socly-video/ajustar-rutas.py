"""Adapta el kit a ESTE ordenador (Windows, Linux o Mac).

Uso, en la carpeta donde descomprimiste el kit:
    python ajustar-rutas.py [carpeta_raiz]  [--ver]

Qué hace (se puede ejecutar más de una vez):
  1. Pasa los finales de línea a LF (los .sh con CRLF fallan en bash).
  2. Cambia la raíz del proyecto del PC original por la carpeta actual.
  3. Cambia la ruta de ffmpeg por la de este ordenador.
  4. Cambia la ruta de Chrome/Chromium.
  5. Cambia las carpetas temporales de trabajo antiguas por <raiz>/trabajo/<nombre>.
  6. Detecta Blender 5.x y crea un atajo «blender» (blender.cmd en Windows).
  7. Cambia las fuentes de Windows (C:/Windows/Fonts/...) por una equivalente si no estás en Windows.
Con --ver solo cuenta lo que cambiaría, sin escribir nada.
"""
import json, os, re, shutil, subprocess, sys

VER = "--ver" in sys.argv
args = [a for a in sys.argv[1:] if not a.startswith("--")]
BL_ARG = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--blender=")), None)
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(args[0]) if args else AQUI
WIN = os.name == "nt"

VIEJO = r"C:\Users\pm221\OneDrive\Documentos\ESTILISTA IA APP"
FF_VIEJO = "C:/Users/pm221/AppData/Local/Packages/PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0/LocalCache/local-packages/Python313/site-packages/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe"
CHROME_VIEJO = "C:/Program Files/Google/Chrome/Application/chrome.exe"
TEMP_RE = re.compile(r"C:/Users/pm221/AppData/Local/Temp/claude/[^/\"']+/[^/\"']+/scratchpad/([^/\"'\s]+)")
FUENTE_RE = re.compile(r"C:/Windows/Fonts/([A-Za-z0-9_\-]+\.ttf)")


def buscar_ffmpeg():
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe().replace("\\", "/")
    except Exception:
        pass
    p = shutil.which("ffmpeg")
    return p.replace("\\", "/") if p else None


def buscar_chrome():
    candidatos = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/opt/pw-browsers/chromium/chrome",
    ]
    for c in candidatos:
        if os.path.exists(c):
            return c.replace("\\", "/")
    for n in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome"):
        p = shutil.which(n)
        if p:
            return p
    return None


def buscar_blender():
    """Blender 5.x: instalaciones típicas, Steam y PATH. Prefiere la 5.2."""
    cands = []
    for base in (os.environ.get("ProgramFiles"), os.environ.get("ProgramFiles(x86)"), r"C:\Program Files"):
        if base:
            d = os.path.join(base, "Blender Foundation")
            if os.path.isdir(d):
                for v in sorted(os.listdir(d), reverse=True):
                    cands.append(os.path.join(d, v, "blender.exe"))
    for base in (r"C:\Program Files (x86)\Steam\steamapps\common\Blender",
                 r"C:\Program Files\Steam\steamapps\common\Blender"):
        cands.append(os.path.join(base, "blender.exe"))
    cands += ["/Applications/Blender.app/Contents/MacOS/Blender"]
    p = shutil.which("blender")
    if p:
        cands.append(p)
    existentes = [c for c in cands if os.path.exists(c)]
    pref = [c for c in existentes if "5.2" in c]
    sel = (pref or existentes or [None])[0]
    return sel.replace("\\", "/") if sel else None


def fuente_equivalente(nombre):
    """Fuente de reemplazo fuera de Windows (negrita si el nombre lo sugiere)."""
    if WIN:
        return None
    n = nombre.lower()
    estilo = "sans:bold" if any(k in n for k in ("blk", "bold", "georgiab", "georgiaz")) else "sans"
    if "georgia" in n:
        estilo = "serif:bold" if estilo.endswith("bold") else "serif"
    try:
        f = subprocess.run(["fc-match", "-f", "%{file}", estilo], capture_output=True, text=True).stdout.strip()
        return f.replace("\\", "/") or None
    except Exception:
        return None


ff = buscar_ffmpeg()
chrome = buscar_chrome()
blender = (BL_ARG.replace("\\", "/") if BL_ARG else buscar_blender())
if not blender:
    print("AVISO: no encuentro Blender (se esperaba Blender 5.2). Si está instalado en otra ruta, pásala con --blender=RUTA.")
if not ff:
    print("AVISO: no encuentro ffmpeg. Instala imageio-ffmpeg (pip install imageio-ffmpeg) o ffmpeg del sistema y repite.")
if not chrome:
    print("AVISO: no encuentro Chrome/Chromium. Instálalo y repite.")

fijos = [
    (VIEJO, RAIZ),
    (VIEJO.replace("\\", "/"), RAIZ.replace("\\", "/")),
    (VIEJO.replace("\\", "\\\\"), RAIZ.replace("\\", "\\\\")),
]
if ff:
    fijos.append((FF_VIEJO, ff))
if chrome:
    fijos.append((CHROME_VIEJO, chrome))

# Rutas aplicadas en una ejecución anterior (para poder re-adaptar el kit en otro ordenador)
MARCA = os.path.join(AQUI, ".rutas-aplicadas.json")
try:
    prev = json.load(open(MARCA, encoding="utf-8"))
except Exception:
    prev = {}
for k, nuevo in (("raiz", RAIZ.replace("\\", "/")), ("ffmpeg", ff), ("chrome", chrome)):
    if prev.get(k) and nuevo and prev[k] != nuevo:
        fijos.append((prev[k], nuevo))

EXT = (".py", ".sh", ".mjs", ".js", ".html", ".json", ".md", ".txt", ".bat")
cambiados = lf = 0
for raiz, dirs, files in os.walk(AQUI):
    dirs[:] = [d for d in dirs if d not in ("node_modules", ".git", "__pycache__", "trabajo")]
    for f in files:
        p = os.path.join(raiz, f)
        if not f.lower().endswith(EXT) or p == os.path.abspath(__file__):
            continue
        try:
            with open(p, encoding="utf-8", newline="") as fh:
                t = fh.read()
        except Exception:
            continue
        n = t.replace("\r\n", "\n")
        if n != t:
            lf += 1
        for a, b in fijos:
            n = n.replace(a, b)
        n = TEMP_RE.sub(lambda m: RAIZ.replace("\\", "/") + "/trabajo/" + m.group(1), n)
        def _f(m):
            alt = fuente_equivalente(m.group(1))
            return alt or m.group(0)
        n = FUENTE_RE.sub(_f, n)
        if n != t:
            cambiados += 1
            if not VER:
                with open(p, "w", encoding="utf-8", newline="") as fh:
                    fh.write(n)

print(("[solo ver] " if VER else "") + "Archivos modificados: %d (con CRLF pasados a LF: %d)" % (cambiados, lf))
print("Raíz:  ", RAIZ)
print("ffmpeg:", ff or "(no encontrado)")
print("Chrome:", chrome or "(no encontrado)")
print("Blender:", blender or "(no encontrado)")
if not VER:
    os.makedirs(os.path.join(RAIZ, "trabajo"), exist_ok=True)
    if blender:
        # Atajo «blender» para que funcionen los comandos de los guiones (blender -b --python ...)
        if WIN:
            with open(os.path.join(RAIZ, "blender.cmd"), "w", newline="\r\n") as fh:
                fh.write('@echo off\r\n"%s" %%*\r\n' % blender.replace("/", "\\"))
        else:
            sh = os.path.join(RAIZ, "blender")
            with open(sh, "w", newline="\n") as fh:
                fh.write('#!/bin/sh\nexec "%s" "$@"\n' % blender)
            os.chmod(sh, 0o755)
        print("Atajo creado: usa  blender -b --python ...  desde la raíz del kit (o añade la raíz al PATH).")
    json.dump({"raiz": RAIZ.replace("\\", "/"), "ffmpeg": ff, "chrome": chrome}, open(MARCA, "w", encoding="utf-8"))
