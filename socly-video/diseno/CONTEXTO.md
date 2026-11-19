# Contexto: diseño y marca

## Qué hay (`diseno\`)
- `mascota\`: el gato antiguo (`gato.svg`, `gato.png`, `mascota app socly.png`, 5 poses). **Mascota nueva: ZORRO** (desde 2026-11-12, mismo estilo de arcilla suave, ojos cerrados, cinta métrica de bufanda con percha dorada): `mascota\zorro-3d\` con `zorro-hero.png`, `zorro-transparente.png`, `zorro-cara.png`, `zorro-socly.blend` y `zorro-socly.glb` (1,3 MB, para la app). Colores: naranja #E3873F, crema #F8EBD6, marrón #5C3A28, cinta #D9A23F. Pendiente: otras poses, revisión del dueño e integración en la app.
- `ideas-interfaz\`: capturas de WhatsApp del 2026-09-23 y los prompts de Claude Design del Mercadillo (v1-v3).
- `maquetas\`: `maqueta-cajon.html` (cajón tras la compra, ya en la app); `movil-3d\` (Blender 5.2, fondo #15140F: `movil-hero.png`, `socly-movil.blend`; para cambiar la pantalla, sustituir la imagen del material «Pantalla Socly»; `movil-vista-puesta.mp4` 6 s sin audio con textos `texto-a/b/c.png` regenerables con `textos-vp.html` + ffmpeg sin volver a renderizar el móvil); `pasarela-3d\` (ver abajo).
- Zips de Claude Design (los que existen en `diseno\`): `Armario digital con IA social.zip`, `ARAMRIO IA SOCIAL.zip`, `Mercadillo de Socly Style.zip` y `Mercadillo v2`/`v3`, `Inicio y Mercadillo v4`, `Rediseno app v5` (6 pantallas), `Opciones v6`, `Cual me pongo y Retos v7`. Ya programados en la app (ver `app estilista ia\CONTEXTO.md`).
- `prototipo-vista-puesta\`: prototipos de Vista puesta (ya en la app, abierta a todas). `historias-vista-puesta\`: 6 historias del teaser (jueves 12 y viernes 13, PNG 1080x1920); las `v2\` usan looks reales sin cara y .mp4 de 6 s, SIN rótulo «Hecho con IA» (el dueño no lo quiere nunca); fuente `historias2.html` + `render2.mjs`, `bash go.sh`. Sin publicar.
- Otros: `capturas\`, `planifica-semana\`, `a_hazme_este_diseño_de.png` (referencia 2026-09-24).
- **Pasarela 3D de Vista puesta** (`maquetas\pasarela-3d\`): v1 plana HECHA (`pasarela-vista-puesta.mp4`, 14 s, 720x1280, sin audio; `construir_pasarela_v1_planos.py`); el dueño la rechazó y la v2 con maniquí 3D (`maniqui.py` + `construir_pasarela.py`, pruebas en `pruebas\`) está PARADA, sin render completo. Si se retoma: fotogramas del flash en blanco, colores lavados, costuras en cintura/rodillas.
- Reglas del dueño: nada anclado, looks grandes, no diseñar página a página (las parecidas se alinean solas); en Armario el botón «Añadir» saca el desplegable actual.

## Dónde vive el diseño real
En el código de la app: variables de tema en `app/globals.css`. Colores del QR de /instalar: `#15140F` sobre `#F4F1EA`.

## Registro reciente
- 2026-11-16: logo REAL de Socly Style (S con percha, blanco sobre negro) copiado a `ciudad-socly\logo-socly.png` y puesto como el logo oficial en `ciudad-socly\direccion-visual.md` (sustituye la propuesta anterior). Prueba de render de Soclo hecha en `video\herramientas\ciudad-socly\`.
- 2026-11-16: dirección visual del vídeo «ciudad Socly» (3D de bloques, 70 s) en ciudad-socly\.
- 2026-11-15: dirección visual y de animación del vídeo «zorro guía» (1080x1920, ~30 s, sobre grabación de pantalla) en `zorro-guia\direccion-visual.md`. Sin publicar.
- 2026-11-14: contexto recortado; sin trabajo nuevo de diseño.
- 2026-11-12: pasarela v2 con maniquí 3D probada en fotogramas y PARADA por el dueño (ver cuerpo).
- 2026-11-12: pasarela v1 (`pasarela-vista-puesta.mp4`) y vídeo del móvil 3D (`movil-vista-puesta.mp4`) hechos para el lanzamiento de Vista puesta. Sin publicar.
- 2026-11-12: mascota zorro 3D (`mascota\zorro-3d\`) y maqueta del móvil con Inicio (`maquetas\movil-3d\`).
- 2026-11-11: historias del teaser de Vista puesta v1 y v2 (looks reales) en `historias-vista-puesta\`.
- 2026-11-10: zips `Opciones v6` y `Cual me pongo y Retos v7` guardados; páginas parecidas se alinean con el diseño nuevo sin diseñarlas una a una.
- 2026-11-09: zips `Rediseno app v5` e `Inicio y Mercadillo v4` aprobados (el dueño dejó «Tocar las prendas» para después, hecha el 11/11) y programados.
- 2026-11-09: Mercadillo de Claude Design v1-v3 revisado (v3 aprobada); prompts de mejora en `ideas-interfaz\`.
