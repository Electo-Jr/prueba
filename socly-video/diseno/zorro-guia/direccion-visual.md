# Zorro guía: dirección visual y de animación (propuesta, sin publicar)

Lienzo 1080x1920, 30 fps (900 fotogramas), fotograma a fotograma con HTML + Chrome + ffmpeg. Base: `mascota\zorro-3d\zorro-transparente.png` (1200x1500; trae una sombra horneada en el suelo: recortar el cuerpo sin ella y dibujar la sombra en CSS).

## 1. Cómo se ve
- Fondo: `#15140F` liso con un degradado radial muy suave (`#2A2218` al 40 % de opacidad detrás del móvil). Sin partículas.
- Grabación: a pantalla casi completa, SIN marco de móvil (el marco gasta ancho y la app ya es el protagonista). Ancho 960 px (margen 60 a cada lado), esquinas redondeadas 56 px, sombra `0 40px 90px #000a`. Si la grabación es 9:19,5, alto ~1.940: recortar a 960x1.700 (arriba: quitar barra de estado; abajo: dejar la zona del zorro). Posición: x 60, y 110. Zona segura de redes: nada importante en los 250 px de arriba ni en los 340 de abajo (texto y zorro dentro de y 250-1580 siempre que se pueda).
- Zorro "compañero": alto 380 px (cuerpo ~ 1/5 de la pantalla). Vive en las esquinas inferiores SOBRE el borde del móvil, medio fuera (pisa el margen de 60 px y se solapa hasta 120 px sobre la app), esquina inferior derecha por defecto, izquierda cuando el contenido está a la derecha. Nunca tapa el botón o prenda que señala.
- Zorro "protagonista": alto 900-1.100 px, solo en gancho (0-3 s), reacción al resultado estrella (1 momento, ~2 s) y despedida (últimos 3 s). La grabación baja a 70 % de opacidad y 0,94 de escala con desenfoque 6 px mientras tanto.
- Transiciones entre estados: 12 fotogramas, ease-out con rebote leve; nunca cortes secos del zorro.

## 2. Movimiento creíble con pocas poses
Regla: el zorro nunca se mueve en línea recta ni a velocidad constante. Todo es "anticipo, acción, asiento".
- Respirar (siempre): escala Y 1 a 1,02 y X 1 a 0,99, ciclo 90 fotogramas, ancla en los pies. Cola: rotar ±3° alrededor de su base (recorte aparte, ver §4).
- Salto de A a B (24 fotogramas): anticipo 5 f (escala 1,10 x 0,88, baja 12 px); despegue 3 f (0,88 x 1,14); vuelo 10 f por arco parabólico (altura = 25 % de la distancia, mín 80 px), rotación ±6° hacia el destino; aterrizaje 3 f (1,12 x 0,86); asiento 3 f hasta 1. Sombra: elipse `#000` 35 %, se encoge a 60 % y se aclara en el aire. Ancla de la escala: los pies.
- Giro: espejo horizontal (`scaleX(-1)`) pasando por scaleX 0,15 en 4 fotogramas con un salto pequeño. La percha y la cinta quedan al otro lado: aceptable; si molesta, usar el espejo solo cuando no se vea la percha (de espaldas o recorte).
- Llega: entra por abajo o desde fuera de pantalla con un salto, 2 saltitos de rebote decreciente.
- Señala un botón: (1) salto/giro hacia el lado del botón; (2) la CINTA MÉTRICA sale del bufanda y se estira en línea curva hasta el botón: trazo SVG 14 px, color `#D9A23F`, con marcas cada 24 px (patrón repetido), crece con `stroke-dashoffset` en 10 f, termina en una percha dorada pequeña que "engancha" el botón y hace un pulso (anillo `#D9A23F` de 0,9 a 1,25 de escala, 2 pulsos). La cinta tiembla ±2 px mientras habla y se recoge en 8 f. Es el gesto de marca: sustituye flechas y estelas.
- Reacciona a un resultado: el zorro salta al centro-bajo, se agranda a protagonista parcial (700 px) con squash fuerte (0,85 x 1,18) y vuelve; ojos ya son felices, así que la emoción va en el cuerpo (salto doble, brazo arriba = pose actual) y en un pulso del propio resultado (escala 1 a 1,04 de la tarjeta). Sin confeti.
- Habla: boca = recorte de 2-3 estados según volumen (ver §4); más un "rebote" del cuerpo escala Y +1,5 % por sílaba fuerte. Mover la cabeza ±2° con el volumen suaviza una boca limitada.
- Se despide: salta al centro, protagonista, saluda con la pata (la pose actual) con balanceo ±8° de la pata, mantiene 2 s y baja con anticipo.
- Globos de diálogo: solo para frases cortas o dudas visuales; los subtítulos van aparte. Globo crema `#F8EBD6`, texto marrón `#5C3A28`, Inter 600 38 px, radio 36 px, cola hacia la boca, aparece con escala 0,6 a 1,04 a 1 en 8 f. Máx 6 palabras. Si hay subtítulos, no duplicar.
- Sombra: siempre en el suelo del zorro (también sobre la app, a pie del zorro): elipse blur 8 px.
- Cruces con el contenido: el zorro puede pasar por delante pero la pausa (donde habla) siempre en zona libre.

## 3. Efectos
Mantener: sombra de suelo; squash/stretch; cinta métrica que señala; pulso de anillo dorado en el botón; atenuar y desenfocar la grabación en los momentos de protagonista; una estrella o brillo de 1 solo punto dorado (8 f) en el resultado final. Máx 1 brillo por plano.
Quitar: destellos de fondo, emojis, pegatinas sobre el zorro, confeti, flechas genéricas, rótulos sobre el zorro, marcos de móvil, nombres/precios no decididos, texto "Hecho con IA".
Subtítulos: palabra a palabra con la palabra activa en `#D9A23F` (resto `#F8EBD6`), Inter 800 54 px, interlineado 1,15, máx 2 líneas de 22 caracteres, sombra `0 4px 18px #000b`, sin fondo. Posición: centrado, y 1.420-1.540 (por encima de la zona de botones de redes). Si el zorro está en esa franja, el zorro usa la esquina opuesta y se sube; los subtítulos nunca se mueven.

## 4. Recursos extra mínimos (de menos a más trabajo)
Todo sale de recortar el PNG existente o de Blender solo con fotogramas sueltos (EEVEE, ~1 min cada uno en gráfica integrada). Los cuatro primeros resuelven el 90 %.
1. Capas separadas del PNG actual (Python/Pillow, 20 min): cuerpo, pata saludando, cola, cabeza (con orejas). Permite respirar, balancear la pata y mover la cola. Prioridad 1.
2. Boca: 3 estados dibujados encima del recorte de la cara en SVG: cerrada (actual), pequeña abierta, grande abierta (óvalo `#5C3A28` con lengua `#E88A7A`). Se cambian por volumen (umbral 0,15 y 0,45). Prioridad 1. Sin renders.
3. Pose "señalando": render Blender con el brazo del saludo extendido a un lado (rotar el hueso/objeto del brazo ~70°). Un fotograma, de lado y su espejo. Prioridad 2. Fallback sin Blender: rotar la pata recortada 50-70°.
4. Pose "de espaldas/tres cuartos mirando a la pantalla": para cuando el zorro mira al móvil y no a cámara. Un render girando 140° en Y (muestra la cola grande). Prioridad 2; fallback: espejo y escala.
5. Pose "sorprendido/celebra": ambos brazos arriba, un render. Prioridad 3 (sin ella, usar la pose actual con salto doble).
6. Percha sola (recorte de la que sostiene) para el final de la cinta. Prioridad 2, 10 min.
Todo con sombras sin hornear: renderizar con el suelo oculto o el alfa limpio. Las poses nuevas, un único fotograma de prueba, visto antes de seguir.

## 5. Gancho: 0-3 s (90 fotogramas)
Capas, de abajo a arriba: (1) fondo `#15140F` con halo; (2) grabación, pantalla de entrada, a 0,94 de escala, 60 % de opacidad y desenfoque 6 px; (3) sombra de suelo; (4) zorro protagonista (cuerpo, cola, pata); (5) cinta métrica; (6) subtítulos.
- f0-6: negro con la grabación ya detrás; el zorro cae desde arriba con 1,10 x 0,88... golpea a y 1.150 en f6 con squash (1,14 x 0,86), sombra marca el impacto. Sonido: el primer fonema ya en f6.
- f6-18: asiento y respiro; saluda con la pata (f6, balanceo 2 veces, 12 f); boca animada; el halo sube 30 %.
- f18-30 (1 s): el zorro salta a la esquina inferior derecha (25 f, protagonista a compañero: 1.000 a 380 px), la grabación sube a 100 % y escala 1, sin desenfoque. Sombras y cola con retardo de 3 f.
- f30-60: el zorro mira a la app; la cinta señala el primer botón o elemento de la pantalla 1 (10 f) y pulso (2).
- f60-90: primer subtítulo palabra a palabra; primera pantalla de la app ya en movimiento; el zorro hace un saltito de giro hacia el lado contrario del contenido. Frase de gancho (de Marketing) dicha entre f6 y f70 como máximo.
Prueba barata: renderizar solo f0, f6, f12, f30, f60 y enseñárselos al dueño antes de montar el resto.

## Qué decide el dueño
Si la app va con o sin marco (propuesto: sin); si merece la pena generar 2 poses nuevas en Blender (señalar y de espaldas); que el color/estilo de cinta como gesto de marca le encaje.
