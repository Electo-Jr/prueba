# Socly Style · vídeo (paquete para el socio)

Socly Style es una PWA en español para organizar el armario y recibir looks con IA. La llevan Electo y Pablo. Esta carpeta es el kit de **vídeo**: herramientas, contexto y guiones.

## Cómo trabajar
1. Al empezar, lee solo este archivo.
2. Para cualquier tarea de vídeo, lee `video\CONTEXTO.md` (dónde está cada cosa, herramientas y lecciones) y trabaja con eso. No releas carpetas enteras.
3. Los guiones están en `marketing\guiones\`; la dirección visual de los vídeos 3D en `diseno\`.
4. Preguntas sueltas: contesta y ya. Cambios grandes: coméntalos antes.

## Reglas (siempre)
- Responder en español y **corto**. Lo importante primero.
- **Nunca publicar, enviar ni postear nada sin permiso explícito.** Los vídeos los sube la persona a mano.
- Todo debe ser **gratis**: no gastar créditos ni IA de pago sin preguntar.
- Secretos: nunca pedir ni mostrar claves en el chat; van en `.env.local`.
- En vídeos y capturas, tapar datos personales (contactos, apps instaladas, nombres de otras personas).
- **Nunca poner el rótulo «Hecho con IA»** en vídeos ni imágenes.
- Texto de cara al público: lenguaje neutro («amigos», «personas»), directo, nada sentimental.
- No afirmar cifras ni tiempos que no estén medidos; solo lo que la app hace de verdad.
- Quiere todo «perfecto»: comprobar el resultado (un fotograma, una hoja de contacto) antes de darlo por bueno.
- Al terminar algo, apunta una línea arriba del «Registro reciente» de `video\CONTEXTO.md`: `- AAAA-MM-DD: qué se hizo y dónde está` (máximo 10 líneas; lo viejo se resume).

## Trucos del PC (Windows)
- Bash con heredocs largos falla («unexpected EOF»): crear los scripts con la herramienta de escribir archivos.
- Python: poner `PYTHONUTF8=1`. Python en Windows no usa `/tmp`.
- ffmpeg viene de `pip install imageio-ffmpeg` (`ajustar-rutas.py` pone su ruta en los scripts).
- Chrome: `/usr/bin/google-chrome`.
- Sin GPU potente: nada de modelos locales de IA. Blender se usa con EEVEE.
- En los vídeos de bloques: enseña un fotograma de cada plano (`SOCLY_FRAMES=40`) antes de renderizar los clips completos, y avisa cuando algo vaya a tardar.
