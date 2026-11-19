# Socly Style · paquete de vídeo para Claude Code

Aquí está todo lo que usamos Electo y Pablo para hacer vídeos con Claude Code: las herramientas (scripts), el contexto, los guiones y las reglas. No lleva vídeos ni renders (pesan gigas): se regeneran con los scripts.

## 1. Primeros pasos (10 minutos)
1. Descomprime el zip en una carpeta sin espacios raros, por ejemplo `C:\socly-video`.
2. Instala lo necesario (más abajo).
3. Abre una terminal en esa carpeta y ejecuta: `python ajustar-rutas.py`. Cambia las rutas de nuestro PC (`C:\Users\pm221\...`) por las de la carpeta donde lo has descomprimido y por tu ffmpeg.
4. Abre Claude Code en la carpeta y dile: «Lee CLAUDE.md y video\CONTEXTO.md y dime qué herramientas hay». Desde ahí trabaja como nosotros: le pides el vídeo y él usa las herramientas.

> **Linux/Mac:** `python3 ajustar-rutas.py` detecta ffmpeg y Chrome/Chromium del sistema y cambia las fuentes de Windows por otras equivalentes (el aspecto de algunos textos puede variar). Los scripts `.sh` y `.mjs` funcionan igual. Blender: instala el tuyo y pon su ruta si un script la pide. Las rutas que nombran carpetas no incluidas en el zip (`anuncios\`, `fotos-propias\`) se crean o se rellenan con tus propios archivos.

## 2. Qué hay que instalar (todo gratis)
- **Python 3.13** y estas librerías: `pip install numpy pillow soundfile imageio-ffmpeg faster-whisper edge-tts gradio_client opencv-python segno`
- **Node.js** (sin paquetes extra: los scripts `.mjs` solo usan lo que trae Node).
- **Google Chrome** (renderiza los anuncios en HTML sin ventana).
- **Blender 5.2** (los vídeos de bloques tipo Roblox). Ruta esperada: `C:\Program Files\Blender Foundation\Blender 5.2\blender.exe`.
- Solo para separar música de una referencia: `torch` y `demucs` instalados en `C:\pp` (`pip install --target C:\pp demucs`), porque la ruta corta evita un límite de Windows.

## 3. Cómo se hace cada tipo de vídeo
| Tipo | Carpeta | Cómo |
|---|---|---|
| **Historia 3D de bloques (estilo Roblox)**: «Ciudad Socly» y «¿De dónde vienen los outfits?» | `video\herramientas\ciudad-socly\` y `outfits-viaje\` | Guion con escenas de 2,5 s → cada plano es una función de Blender (`planos2.py`, `planos3.py`, `app_planos.py`, personajes y decorados en `lib.py` / `base*.py` / `trajes.py`) → `blender -b --python planos_a.py -- 1 12` renderiza fotogramas → `montar_final.py` (outfits) o `montar.sh` + `subtitular.py` + `final.py` (ciudad) une los planos, los ajusta a la voz con Whisper, subtitula y mezcla música. Se prueba primero un fotograma con `SOCLY_FRAMES=40`. |
| **Anuncios y reels animados en HTML** | `anuncio-html\`, `mercadillo\`, `vista-puesta\`, `halloween-publi\`, `subir-bien\`, `presentacion-*` | `ad.html` + `ad.js` (escenas y cámara con fotogramas clave) se renderizan en Chrome fotograma a fotograma (`render.mjs`) y `go.sh` o `build.py` unen audio y codifican con ffmpeg. |
| **Zorro (mascota)** | `zorro-presentacion\` | Animación 2.5D con poses PNG, boca según el volumen, subtítulos por palabra. `bash go.sh <voz.wav>`. |
| **Podcast en clips** | `podcast\` | `clips.py <n>` corta cada clip con subtítulos palabra a palabra (Whisper), `transcribir.py` y `energia.py` ayudan a elegir momentos. Plan en `marketing\podcast\`. |
| **Fotos con IA** | `imagenes-ia\` | `gen.py` con el Space gratis `Tongyi-MAI/Z-Image-Turbo` de Hugging Face (límite diario sin cuenta). |
| **Plantilla CapCut** | `plantilla-capcut\` | Ejemplo de réplica de plantilla; no se ejecuta tal cual. |

## 4. Reglas de la casa (Claude Code las sigue si le dices que lea CLAUDE.md)
- Nada se publica ni se envía sin permiso. Los vídeos se suben a mano.
- Todo gratis: si algo gasta créditos o pide una clave de pago, se pregunta antes.
- Tapar datos personales en vídeos y capturas (contactos, apps instaladas, nombres).
- Nunca poner el rótulo «Hecho con IA» en vídeos ni imágenes.
- Texto de cara al público: lenguaje neutro, directo, nada sentimental.
- Las claves van en `.env.local` o en la web de cada servicio, nunca por el chat.

## 5. Voces y música
- **Voz**: AI Studio (`aistudio.google.com/generate-speech`), voz **Fenrir** para narrador, gratis con una cuenta de Google. Alternativa sin cuenta: `edge-tts` (voces `es-MX-JorgeNeural`, etc.).
- **Música**: para Ciudad Socly se separó la música de un audio de referencia con demucs; **puede tener derechos**. Antes de subir, mejor una pista libre de derechos.
- Los efectos de sonido del podcast venían de myinstants.com (de terceros): no van en el paquete.

## 6. Lo que NO va en el zip
Vídeos y renders, fotogramas, `.blend`, voces y audios, música, fotos y grabaciones personales, perfiles de navegador, claves y la carpeta `privado\`. Si falta algo, se genera con los scripts o te lo pasamos aparte.

## 7. Para trabajar bien
- Un cambio importante, coméntalo antes con quien lo lleve (Pablo o Electo).
- Cada vez que acabes algo, apunta una línea en el `CONTEXTO.md` de su carpeta (`- AAAA-MM-DD: qué se hizo y dónde está`, máximo 10 líneas).
- Los scripts largos se crean con la herramienta de escribir archivos de Claude Code, no con «heredocs» en bash (en Windows fallan).
- Ejecutar Python con `PYTHONUTF8=1`.

## 8. Transcripciones
Las transcripciones de grabaciones personales (`IMG_*.json`, `estilo-swipe/palabras/`) no van en el repositorio. Se regeneran con Whisper (`transcribir.py` / `palabras.py`) a partir de tus propios vídeos.
