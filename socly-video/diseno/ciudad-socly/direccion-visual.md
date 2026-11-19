# Ciudad Socly: dirección visual (propuesta, sin publicar)

Vídeo 9:16, 1080x1920, 30 fps, 70 s (~28 planos de ~2,5 s). Blender EEVEE, solo cubos, cilindros y materiales lisos. Personajes propios de bloques (no Roblox ni otra franquicia). Sin rótulo «Hecho con IA».
Marca (de `CONTEXTO.md` y `globals.css`): `#15140F` negro cálido, `#F7F4EE` crema, dorado de cinta `#D9A23F`, naranja zorro `#E3873F`. El logo REAL está en `diseno\ciudad-socly\logo-socly.png` (copia de `app estilista ia\design\logo.png`): una «S» blanca con una percha dentro, sobre cuadrado negro de esquinas redondeadas. Usar ESE, no la propuesta anterior.

## 1. Ciudad: «gris pero con dopamina»
Idea: edificios grises y apagados, pero cubiertos de pantallas y neones saturados. Todo lo que atrapa es chillón; lo bueno (Socly, Soclo) es limpio.

Paleta
| Uso | Hex |
|---|---|
| Edificios (cubos) | `#4A4D55`, `#5B5F69`, `#2F3138` |
| Asfalto / plaza | `#25262B` / `#8B8E96` |
| Cielo atardecer (arriba a horizonte) | `#2B2150` a `#E8637A` a `#FFB35C` |
| Neón rosa «oferta» | `#FF2E88` |
| Neón cian «pantalla» | `#18E0FF` |
| Amarillo «descuento» | `#FFE500` |
| Verde «-70 %» | `#2BFF88` |
| Ventanas encendidas | `#FFD27A` |
| Marca Socly (solo al final y en Soclo) | `#15140F`, `#F7F4EE`, `#D9A23F`, `#E3873F` |

Luz
- Hora: atardecer que se va a noche. Sol bajo `#FFB35C` fuerza 4, ángulo 8° sobre el horizonte, sombras largas. Mundo `#2B2150` fuerza 0,6.
- Neones: materiales emisivos (fuerza 8-15) + 2-3 luces de área del mismo color cerca de cámara para teñir caras. Bloom activado en EEVEE.
- Ventanas: cubitos emisivos `#FFD27A`, 30 % encendidas al azar (textura de ruido en umbral).
- Niebla suave: volumen en el mundo, densidad 0,008, color `#6A5A8A`. Hace que el skyline lejano se funda y de profundidad.
- Contraste: negros de verdad en las sombras; exposición +0,3; «Filmic/AgX» con alto contraste.

Skyline: 40-60 cubos de 2x2 a 4x14 m, alturas al azar, en tres filas (cerca `#2F3138`, medio `#4A4D55`, lejos `#5B5F69` con niebla). Algunos con cubo menor encima (azotea) y antena cilíndrica con luz roja.

Props reconocibles (7)
1. Pantalla gigante de ofertas: caja 12x7x0,5 m en un edificio, textura con «-70 %» / «¡YA!» en amarillo y rosa; parpadea (emisión alterna cada 6 f).
2. Torres de luz: cilindros finos de 18 m con corona de 6 focos emisivos cian; barren la plaza.
3. Carteles de neón en forma de flecha o de bolsa (cajas con borde emisivo), «SALE» en neón rosa.
4. Plaza con fuente seca: disco gris, cilindro central, estatua del alcalde (cubo-persona gris de 5 m) con dedo señalando.
5. Balcón del ayuntamiento: edificio con columnas (cilindros crema `#D8D2C4`), balcón y atril; donde habla el alcalde.
6. Rampa de lanzamiento: plataforma 14x14x1 m, dos torres de sujeción rojas `#C8372D`, rampa de cubos escalonados, en la azotea de un edificio o al borde de la plaza. Pintada con franjas amarillo/negro.
7. Marquesinas con pantallas: cajas cian en las paradas; peatones-bloque mirando abajo (cabeza inclinada 40°).
8. Sistemas de ruido: cables de cubos finos cruzando la calle con banderines de «OFERTA» (rosa/amarillo).

Cambio final (se llena de color): los edificios pasan de grises a colores cálidos suaves (`#F2A65A`, `#7AC7B8`, `#F4D35E`, `#E58B8B`), las pantallas de ofertas muestran logos y looks de Socly, los neones bajan a la mitad, amanece (sol `#FFD9A0` fuerza 5, cielo `#7EC8F0` a `#FFE3B3`), niebla casi 0, guirnaldas y globos (esferas) en la plaza. Se hace con un único interruptor: valor de mezcla 0 a 1 que anima color de edificios, cielo y luz.

## 2. Personajes (bloques)
Todos miden 6 cubos de alto: cabeza cubo 1x1x1, torso 1,2x1,4x0,7, brazos y piernas 0,4x1,3x0,4, pies cubo 0,45. Bordes biselados 0,03 (modificador Bevel) para que cojan luz. Cabeza ligeramente más grande (1,1) para que se lea la cara de lejos. Piel en 4 tonos: `#F2C9A0`, `#D9A06F`, `#A8683F`, `#6B4226`.

Cara con cubos (todos planos finos sobre la cara frontal, 0,02 de grosor)
- Ojos: dos cubos 0,18x0,22 negros `#15140F`; brillo: cubito blanco 0,06 arriba derecha. Normal; feliz = parte inferior cortada (ojo en arco) con cubo de piel encima; sorpresa = ojos 0,26x0,3 con brillo; enfadado = ojos 0,18x0,14.
- Cejas: cubos 0,3x0,06. Neutral horizontal; enfado en V (rotar 20°); sorpresa altas 0,08; tristeza en V al revés.
- Boca: cubo 0,35x0,07 oscuro `#5C2A2A`; sonrisa = 3 cubitos en arco; abierta = cubo 0,3x0,2 con lengua `#E88A7A`; grito = 0,3x0,35. Para hablar: alternar entre cerrada y abierta cada 4-6 f.
- Se cambian las caras ocultando/mostrando grupos (6 caras guardadas como colecciones por personaje).

**Soclo (protagonista)**
- Piel `#D9A06F`. Pelo: cubo recto 1,15x0,35 en la parte superior + flequillo lateral (cubo 0,5x0,5 inclinado 15°), color `#2A1B12`. Ojos felices, ceja izquierda más alta (su seña de confianza).
- Accesorio firma: cinta métrica `#D9A23F` colgando del cuello (dos cilindros planos 0,2x1,6 con marcas = textura de rayas) y percha dorada diminuta prendida al pecho. Enlaza con el zorro de la marca.
- Look A «diario»: chaqueta bomber crema `#F7F4EE`, camiseta negra `#15140F`, vaqueros `#3B4A63`, zapatillas blancas con suela `#D9A23F`.
- Look B «noche»: abrigo largo marrón `#5C3A28`, jersey de cuello alto `#E3873F`, pantalón negro, botas negras.
- Look C «confrontación»: americana negra sobre camiseta crema, pantalón beige `#C9B79C`, mocasines marrones; en el cuello, la cinta. Es el que lleva al exponer al alcalde.
- Móvil: cubo 0,5x0,9x0,06 negro con pantalla emisiva `#F7F4EE`; muestra el logo.

**El alcalde**
- Piel `#F2C9A0`, más alto (6,5 cubos), torso ancho. Pelo canoso `#CFCFD4` peinado hacia atrás (cubo con borde frontal levantado), bigote cubo 0,5x0,1 `#CFCFD4`.
- Aspecto elegante: traje azul noche `#1F2A4D` de tres piezas (chaleco `#3A4670` visible), corbata burdeos `#7A1F2B`, pañuelo crema en bolsillo, pantalón con raya (cubo fino claro), zapatos negros brillantes (rugosidad 0,1), reloj dorado `#D9A23F`, banda de alcalde cruzada (cubo fino inclinado 45°, `#E3C25A`) con medallón.
- Lado ridículo-autoritario: sombrero de copa de cilindro 1x1,1 demasiado alto, ceja en V permanente, dedo señalando enorme, atril con micrófono, el móvil siempre tapado en el bolsillo interior (pista: cubo emisivo asomando y cinta métrica dorada saliendo, la que Soclo reconoce). Cuando miente, sonrisa de 5 cubitos y sudor (cubo azul claro).

**6 vecinos ridículos** (todos mirando abajo o con pantallas)
1. «Cuadros»: camisa de cuadros naranja `#FF7A00` + pantalón de lunares rosas `#FF2E88`, calcetines un verde `#2BFF88` y un morado `#8A3CFF` (altos, sobre el zapato).
2. «Neón»: chaleco amarillo fluorescente `#FFE500` sobre camiseta de rayas cian y blancas, shorts naranjas, gafas de sol cuadradas de 3 cubos.
3. «Doble»: dos sombreros apilados (copa roja + gorra azul), camiseta con la frase «-70 %» (textura), mallas verdes, chanclas con calcetines blancos hasta la rodilla.
4. «Bolsas»: lleva 6 bolsas de compra de colores en brazos y cabeza, jersey de Navidad en pleno verano `#C8372D` con renos, falda tableada de cuadros.
5. «Pijama»: pijama de rayas azul y blanco con zapatillas de felpa, abrigo de piel falsa `#E58B8B` encima, gorro de dormir con borla (esfera).
6. «Bloque»: look de colores que chocan: pantalón rojo, camisa amarilla, chaqueta verde, corbata rosa, cinturón sobre la camiseta, un zapato rojo y otro azul.

**6 looks finales «cada uno con su estilo»** (mismos 6 vecinos, misma cabeza, ahora con paleta armónica)
1. Clásico: blazer gris `#7A7F8A`, camisa blanca, pantalón negro, mocasines.
2. Deportivo: chándal `#2B6CB0` con franja blanca, zapatillas blancas, gorra.
3. Punk: chaqueta negra con 4 púas (conos) `#C0C0C0`, camiseta roja, vaqueros rotos (cubos de piel visibles), botas con suela gruesa, pelo en cresta `#FF2E88`.
4. Minimal: todo en beige `#D8CBB6` y crema, línea limpia, sin estampado, sneakers blancas.
5. Vintage: falda midi `#B5543A`, blusa crema, gafas redondas (cilindros), bolso marrón `#5C3A28`, pelo con ondas (cubos).
6. Streetwear: sudadera oversize `#E3873F`, cargo verde oliva `#6B7A3A`, gorro negro, zapatillas altas.
El cambio se muestra con barrido de luz: el look viejo se sustituye por el nuevo con un flash blanco de 3 fotogramas.

**8 poses clave** (rig simple: pivotes en hombros, caderas y cuello, sin huesos si hace falta)
1. Neutro mirando al móvil (cabeza -35°, hombros encogidos).
2. Soclo caminando con confianza (paso de 15° en caderas, brazo contrario adelante).
3. Soclo se detiene y señala con el dedo (brazo a 80°).
4. Soclo sorprendido (manos a la cara, ojos grandes, cuerpo hacia atrás 10°).
5. Alcalde hablando en el balcón (brazo alzado, dedo erguido).
6. Alcalde asustado (rodillas hacia dentro, manos arriba, ojos 0,26).
7. Multitud celebrando (brazos arriba, saltito de 0,3 m).
8. Pose final de pasarela (una mano en la cadera, mirada a cámara, por turnos).

## 3. Logo de Socly Style y cohete
LOGO REAL (decidido por el dueño): usar la imagen `logo-socly.png` como textura emisiva en móviles, cohete y pantallas. Lo que sigue era la propuesta anterior, ya descartada: cuadrado de esquinas redondeadas `#15140F` con una «S» crema `#F7F4EE` en serif (la serif de titulares de la app, Instrument Serif) y una percha dorada `#D9A23F` pequeña en el palo superior de la S (un cilindro curvo fino con gancho). Debajo, «Socly Style» en una línea.
Cómo reproducirlo: un solo plano (la textura se genera en HTML/Chrome a 1024x1024 con PNG transparente y se pega en un cubo plano). La S se puede extruir (curva de texto con fuente serif, extrusión 0,05) y la percha es una curva con bisel `#D9A23F`. En la app (móvil de Soclo) se ve como icono sobre pantalla crema.
Variante cohete: logo en grande en los costados (4 repeticiones, 3 m de lado) y fondo del cuerpo crema.

Cohete
- Tamaño: 22 m alto, 5 m de diámetro, cuerpo cilindro `#F7F4EE`; cono de morro rojo `#C8372D` (cono 5 m); 3 aletas cubos finos `#15140F`; ventana redonda (cilindro) `#18E0FF` con el alcalde asomado (cabeza + sombrero aplastado).
- Detalles: franja dorada `#D9A23F` bajo el morro, ristra de logos pequeños, la cinta métrica enroscada en espiral desde el morro hasta la base.
- Humo: esferas blancas y grises `#E6E6EA`/`#9C9CA4` (20-30) que crecen al salir y suben; fuego: 3 conos apilados `#FFE500`, `#FF7A00`, `#FF2E88`, escalas animadas con ruido. Chispas: 40 cubitos emisivos dorados que salen disparados.
- Al despegar: temblor de cámara, polvo en la plaza, luz naranja cálida sobre la multitud.
- Marte: esfera `#B5543A` con cráteres (esferas hundidas) para el plano final del alcalde.

## 4. Cámaras y planos
Dos cámaras: «cámara A» (lente 35 mm, general y acción) y «cámara B» (lente 85 mm, caras). Sensor vertical 9:16 (1080x1920). Mano temblorosa con modificador Noise (amplitud 0,03 m, 12 f).
Diez tipos de plano (cada uno ~2,5 s, 75 fotogramas)
1. Primer plano de cara: 85 mm, a la altura de los ojos, empuje lento (dolly in 0,3 m).
2. Plano general de la ciudad: 24 mm, vista aérea desde 40 m, giro lento 10° (orbit).
3. Detalle de pantalla o mano con móvil: 50 mm, ligeramente picado, ligero temblor.
4. Contrapicado del alcalde en el balcón: 28 mm, cámara en el suelo mirando a 25°, dolly in.
5. Seguimiento de Soclo caminando: 35 mm, lateral, dolly lateral a su velocidad.
6. Zoom rápido a la cara: 35 a 85 mm en 10 f (efecto «sorpresa»), con temblor.
7. Explosión de chispas: 35 mm, fija, flash blanco de 2 f, cubos emisivos disparados.
8. Plano holandés (inclinado 15°) para la revelación y el conflicto.
9. Plano de multitud: 28 mm, picado 20°, empuje hacia el centro, mucha gente.
10. Plano cenital de la plaza: 24 mm desde arriba, giro lento 90°, cambio de color.
Más: whip pan (giro rápido con desenfoque) entre escenas, slow-mo en el despegue (30 a 12 fps equivalentes en 1 s), plano subjetivo del móvil.
Subtítulos: una palabra, amarillo `#FFE500` con borde negro `#000` 10 px, sans bold de 130-150 px, centrado, y 1500-1620 (arriba de los botones de redes; nada importante entre y 1700 y 1920).

## 5. Prueba primero (barata)
Construir solo: Soclo (look A) + un trozo de plaza: suelo gris, 3 edificios cubos detrás (`#4A4D55`), una pantalla gigante `#FF2E88`/`#FFE500` y una torre de luz.
- Cámara B: 85 mm, a 2,2 m de Soclo, a la altura del pecho, mirando hacia arriba 5° (contrapicado ligero). Soclo ligeramente girado 20°.
- Luces: sol `#FFB35C` fuerza 4 desde detrás-izquierda (contraluz cálido), luz de área rosa `#FF2E88` fuerza 300 a la derecha, luz de área cian `#18E0FF` fuerza 200 a la izquierda, luz de relleno crema tenue de frente. Niebla suave y bloom.
- Un solo fotograma 1080x1920 (EEVEE, 64 muestras, ~1 min). Se enseña al dueño antes de seguir con el resto.
- Solo si gusta: caras, 6 vecinos, alcalde, rampa y cohete, en ese orden.
