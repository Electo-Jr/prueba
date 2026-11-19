"""Genera el guion del zorro con voces neuronales gratuitas (edge-tts).
Uso: PYTHONUTF8=1 python voces.py            -> voces/voz-<nombre>.mp3 con 3 voces masculinas
     PYTHONUTF8=1 python voces.py <voz> <salida.wav> -> una sola voz, a wav listo para audio.py"""
import asyncio
import os
import subprocess
import sys

import edge_tts

TEXTO = (
    "Alerta: tu armario te está mintiendo. Tienes ropa de sobra. Aquí la subes, y yo la mido. Con la cinta. "
    "Te monto looks con tus prendas. Yo cuelgo, tú eliges. "
    "Vista puesta: ves el look puesto antes de salir de casa. Primera prueba gratis. "
    "Tus amigos votan sin cuenta. Yo no voto: soy un zorro. "
    "Entra en Socly Style. Gratis, sin tarjeta."
)
VOCES = {
    "alvaro": ("es-ES-AlvaroNeural", "+6%", "+4Hz"),
    "jorge": ("es-MX-JorgeNeural", "+4%", "+3Hz"),
    "tomas": ("es-AR-TomasNeural", "+4%", "+3Hz"),
}
FF = "/usr/bin/ffmpeg"


async def hacer(nombre, salida):
    voz, rate, pitch = VOCES[nombre]
    await edge_tts.Communicate(TEXTO, voz, rate=rate, pitch=pitch).save(salida)


async def main():
    if len(sys.argv) >= 3:
        mp3 = sys.argv[2] + ".mp3"
        await hacer(sys.argv[1], mp3)
        subprocess.run([FF, "-loglevel", "error", "-y", "-i", mp3, "-ar", "44100", "-ac", "1", sys.argv[2]], check=True)
        return
    os.makedirs("voces", exist_ok=True)
    for n in VOCES:
        await hacer(n, f"voces/voz-{n}.mp3")
        print("ok", n)


asyncio.run(main())
