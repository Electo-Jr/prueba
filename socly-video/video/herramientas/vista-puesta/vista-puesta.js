// «Vista puesta»: escenas animadas del vídeo. 576x1024 CSS px (x1.875 = 1080x1920). render(t) es determinista.
// t global: coche 0–1.7 · caminando 2–3.8 · función (D) 4–13.4 (los primeros 1,2 s suenan sobre la frase anterior) · galería y comparar (E) 15–23.4
const $ = (id) => document.getElementById(id)
const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v))
const seg = (t, a, b) => clamp((t - a) / (b - a))
const easeOut = (x) => 1 - Math.pow(1 - x, 3)
const easeInOut = (x) => (x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2)
const easeBack = (x) => { const c = 1.70158; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2) }
const lerp = (a, b, x) => a + (b - a) * x
const pop = (t, a, d = 0.35) => easeBack(seg(t, a, a + d))
const SCENES = ['car', 'walk', 'sceneD', 'sceneE']

function show(id, a) { $(id).style.opacity = a }

/* ---------- COCHE ---------- */
const BOKEH = Array.from({ length: 18 }, (_, i) => ({
  x: (i * 97) % 640, y: 250 + ((i * 53) % 300), r: 5 + ((i * 7) % 13), sp: 40 + ((i * 29) % 90),
  c: ['#ffcf8a', '#ff9d6b', '#9fd3ff', '#ffe9b0'][i % 4],
}))
function drawCar(t) {
  let s = `<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0a0f22"/><stop offset=".55" stop-color="#27264a"/><stop offset="1" stop-color="#8a5a5a"/></linearGradient>
  <radialGradient id="dg" cx=".7" cy=".1" r=".6"><stop offset="0" stop-color="#ffd79a" stop-opacity=".45"/><stop offset="1" stop-color="#ffd79a" stop-opacity="0"/></radialGradient></defs>
  <rect width="576" height="1024" fill="url(#sky)"/>`
  for (const b of BOKEH) {
    const x = (((b.x - b.sp * t * 1.6) % 640) + 640) % 640 - 32
    s += `<circle cx="${x}" cy="${b.y}" r="${b.r}" fill="${b.c}" opacity=".7"/>`
  }
  s += `<rect y="540" width="576" height="484" fill="#101119"/>`
  s += `<polygon points="262,540 314,540 760,1024 -184,1024" fill="#1a1c27"/>`
  for (let k = 0; k < 7; k++) {
    const z = ((k / 7 + t * 1.5) % 1)
    const y = 540 + z * z * 330, w = 2 + z * 22, h = 5 + z * z * 90
    s += `<rect x="${288 - w / 2}" y="${y}" width="${w}" height="${h}" fill="#efe7d4" opacity="${0.35 + z * 0.6}"/>`
  }
  for (let i = 0; i < 14; i++) {
    const ang = (i / 14) * Math.PI * 2
    if (Math.sin(ang) < 0.05) continue
    const z = ((i * 0.137 + t * 1.8) % 1)
    const r0 = 30 + z * z * 520, r1 = r0 + 12 + z * z * 120
    s += `<line x1="${288 + Math.cos(ang) * r0}" y1="${540 + Math.sin(ang) * r0 * 0.9}" x2="${288 + Math.cos(ang) * r1}" y2="${540 + Math.sin(ang) * r1 * 0.9}" stroke="#ffd29a" stroke-width="${1 + z * 3}" opacity="${0.2 + z * 0.6}" stroke-linecap="round"/>`
  }
  s += `<path d="M0 800 Q288 740 576 790 L576 1024 L0 1024Z" fill="#08080b"/><path d="M0 800 Q288 740 576 790" fill="none" stroke="#2b2b33" stroke-width="3"/>`
  s += `<rect x="150" y="700" width="426" height="320" fill="url(#dg)"/>`
  const sway = Math.sin(t * 3.1) * 4
  s += `<g transform="rotate(${sway} 150 960)"><ellipse cx="150" cy="960" rx="150" ry="104" fill="none" stroke="#0f0f12" stroke-width="30"/><ellipse cx="150" cy="960" rx="150" ry="104" fill="none" stroke="#2a2a31" stroke-width="3" transform="translate(0,-10)"/><line x1="0" y1="960" x2="300" y2="960" stroke="#0f0f12" stroke-width="22"/><rect x="128" y="940" width="44" height="40" rx="10" fill="#17171b"/></g>`
  s += `<rect x="396" y="800" width="12" height="130" rx="5" fill="#1d1d22"/>`
  $('carSvg').innerHTML = s
  $('carPhone').style.transform = `translateY(${Math.sin(t * 15) * 1.1}px) rotate(${Math.sin(t * 6) * 0.5}deg)`
}

/* ---------- CAMINANDO ---------- */
const FRIENDS = [
  { x: 148, coat: '#3d4a36', pants: '#1f2430', skin: '#e3b38d', hair: '#2a1d16', ph: 0 },
  { x: 288, coat: '#8a6a4f', pants: '#2d2a36', skin: '#c68a62', hair: '#15100c', ph: 1.6, phone: true },
  { x: 428, coat: '#233a5e', pants: '#3a3a3a', skin: '#f0c9a5', hair: '#5a3a22', ph: 3.1 },
]
function person(f, t) {
  const w = (t * 2.5 + f.ph) * Math.PI * 2 * 0.5, sw = Math.sin(w), bob = Math.abs(Math.sin(w)) * 5
  const foot = 862, hip = foot - 124
  let s = `<g transform="translate(0,${-bob})">`
  for (const side of [1, -1]) {
    s += `<g transform="rotate(${sw * 26 * side} ${f.x + side * 12} ${hip})"><rect x="${f.x + side * 12 - 12}" y="${hip}" width="24" height="112" rx="10" fill="${f.pants}"/><rect x="${f.x + side * 12 - 14}" y="${hip + 104}" width="34" height="16" rx="8" fill="#16161a"/></g>`
  }
  s += `<rect x="${f.x - 38}" y="${hip - 138}" width="76" height="150" rx="26" fill="${f.coat}"/><rect x="${f.x - 5}" y="${hip - 130}" width="10" height="130" fill="rgba(0,0,0,.15)"/>`
  for (const side of [1, -1]) {
    if (f.phone && side === 1) {
      s += `<rect x="${f.x + 28}" y="${hip - 128}" width="20" height="84" rx="9" fill="${f.coat}" transform="rotate(-24 ${f.x + 38} ${hip - 128})"/>`
    } else {
      s += `<g transform="rotate(${-sw * 22 * side} ${f.x + side * 44} ${hip - 128})"><rect x="${f.x + side * 44 - 10}" y="${hip - 128}" width="20" height="100" rx="10" fill="${f.coat}"/><circle cx="${f.x + side * 44}" cy="${hip - 24}" r="10" fill="${f.skin}"/></g>`
    }
  }
  s += `<rect x="${f.x - 9}" y="${hip - 158}" width="18" height="26" fill="${f.skin}"/><circle cx="${f.x}" cy="${hip - 188}" r="31" fill="${f.skin}"/><path d="M${f.x - 32} ${hip - 190} a32 32 0 0 1 64 0 q-32 -16 -64 0z" fill="${f.hair}"/>`
  if (f.phone) {
    s += `<g transform="rotate(8 ${f.x + 60} ${hip - 170})"><rect x="${f.x + 38}" y="${hip - 232}" width="52" height="92" rx="9" fill="#0d0d0f"/><clipPath id="pc"><rect x="${f.x + 41}" y="${hip - 229}" width="46" height="86" rx="7"/></clipPath><image href="assets/out-6.png" x="${f.x + 41}" y="${hip - 229}" width="46" height="86" preserveAspectRatio="xMidYMid slice" clip-path="url(#pc)"/></g>`
  }
  return s + '</g>'
}
function drawWalk(t) {
  let s = `<defs><linearGradient id="dusk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4e4470"/><stop offset=".5" stop-color="#c4808a"/><stop offset="1" stop-color="#f5c394"/></linearGradient></defs>
  <rect width="576" height="1024" fill="url(#dusk)"/>`
  const layer = (speed, color, hs, y0, wmin, step) => {
    let g = ''
    for (let i = -2; i < 10; i++) {
      const x = i * step - ((t * speed) % step)
      const h = hs[(i + 20) % hs.length]
      g += `<rect x="${x}" y="${y0 - h}" width="${step - 8}" height="${h + 400}" fill="${color}"/>`
    }
    return g
  }
  s += layer(28, '#5d4e78', [180, 260, 210, 320, 240], 620, 0, 120)
  s += layer(70, '#3b3150', [250, 340, 290, 380, 310], 760, 0, 170)
  for (let i = -1; i < 4; i++) {
    const x = i * 220 - ((t * 140) % 220) + 40
    s += `<rect x="${x}" y="480" width="8" height="330" fill="#241d33"/><circle cx="${x + 4}" cy="474" r="12" fill="#ffd9a0"/><circle cx="${x + 4}" cy="474" r="34" fill="#ffd9a0" opacity=".25"/>`
  }
  s += `<rect y="812" width="576" height="212" fill="#2a2630"/><rect y="806" width="576" height="10" fill="#8f8aa0"/>`
  for (let i = -1; i < 6; i++) s += `<rect x="${i * 130 - ((t * 140) % 130)}" y="930" width="64" height="8" fill="#4a4556"/>`
  for (const f of FRIENDS) s += person(f, t)
  $('walkSvg').innerHTML = s
}

/* ---------- D: la función ---------- */
const TILE_FROM = [[10, 20], [168, 10], [4, 250], [170, 262], [86, 330]]
const TILES = ['in-6-0.jpg', 'in-6-3.jpg', 'in-6-1.jpg', 'in-6-2.jpg', 'in-6-4.jpg']
$('tiles').innerHTML = TILES.map((f, i) => `<div class="tile" id="tl${i}"><img src="assets/${f}"></div>`).join('')

function finger(id, rid, x, y, a, tap) {
  const f = $(id), r = $(rid)
  f.style.left = x + 'px'; f.style.top = y + 'px'; f.style.opacity = a
  f.style.transform = `scale(${1 - tap * 0.18})`
  r.style.left = x + 'px'; r.style.top = y + 'px'
  r.style.opacity = tap > 0 ? 0.9 * tap : 0
  r.style.transform = `scale(${1 + (1 - tap) * 1.6})`
}
function keyPos(t, keys) {
  if (t <= keys[0][0]) return { x: keys[0][1], y: keys[0][2], tap: 0 }
  for (let i = 0; i < keys.length - 1; i++) {
    const [a, ax, ay] = keys[i], [b, bx, by, tp] = keys[i + 1]
    if (t >= a && t < b) {
      const k = easeInOut(seg(t, a, b - 0.06))
      return { x: lerp(ax, bx, k), y: lerp(ay, by, k), tap: tp ? Math.max(0, 1 - Math.abs(t - b) / 0.2) : 0 }
    }
  }
  const l = keys[keys.length - 1]
  return { x: l[1], y: l[2], tap: l[3] ? Math.max(0, 1 - Math.abs(t - l[0]) / 0.2) : 0 }
}

function renderD(v) {
  const d = v - 1.2 // la voz de la función empieza a 1,2 s; la entrada del móvil va antes
  const e = easeBack(seg(v, 0, 0.7))
  $('phoneD').style.transform = `translateY(${(1 - e) * 150}px)`
  $('phoneD').style.opacity = seg(v, 0, 0.3)
  const chip = $('newChip')
  const swapped = d >= 6.5
  const txt = swapped ? '✦ Maniquí invisible' : 'Nuevo · Vista puesta'
  if (chip.dataset.t !== txt) { chip.textContent = txt; chip.dataset.t = txt; chip.className = 'chip ' + (swapped ? 'dark' : 'gold') }
  const c = pop(v, 0.35, 0.4) * (1 - seg(d, 7.95, 8.1))
  chip.style.opacity = clamp(c)
  const bump = swapped ? easeBack(seg(d, 6.5, 6.85)) : 1
  chip.style.transform = `scale(${lerp(0.9, 1, clamp(c))}) scale(${swapped ? lerp(0.85, 1, clamp(bump)) : 1})`
  chip.style.marginLeft = swapped ? '-92px' : '-100px'

  // botón
  const press = 1 - 0.04 * Math.max(0, 1 - Math.abs(d - 2.3) / 0.15)
  const pulse = seg(d, 1.5, 2.2) * (1 - seg(d, 2.3, 2.5))
  $('btnVista').style.transform = `scale(${press})`
  $('btnVista').style.boxShadow = `0 5px 12px rgba(20,18,12,.08),0 0 0 ${pulse * 5}px rgba(138,106,79,${0.28 * pulse})`

  // hoja
  const sh = easeOut(seg(d, 2.4, 2.9))
  $('sheet').style.transform = `translateY(${(1 - sh) * 100}%)`
  $('dim').style.opacity = sh
  const loading = seg(d, 2.7, 2.9) * (1 - seg(d, 3.9, 4.05))
  $('loadTxt').style.opacity = loading
  $('loadTxt').textContent = 'Montando el look' + '.'.repeat(1 + (Math.floor(Math.max(0, d) * 3) % 3)) + ' unos 20 segundos.'
  $('loadTxt').style.transform = 'translateY(150px)'
  // las prendas se juntan en el centro
  TILE_FROM.forEach((p, i) => {
    const k = easeInOut(seg(d, 3.0 + i * 0.05, 3.95))
    const cx = 88, cy = 130
    const x = lerp(p[0], cx, k), y = lerp(p[1], cy, k) + Math.sin(d * 5 + i) * 4 * (1 - k)
    const el = $('tl' + i)
    el.style.left = x + 'px'; el.style.top = y + 'px'
    el.style.transform = `scale(${lerp(1, 0.55, k)}) rotate(${lerp((i - 2) * 6, 0, k)}deg)`
    el.style.opacity = seg(d, 2.75, 3.0) * (1 - seg(d, 3.85, 4.05))
  })
  const gl = seg(d, 3.2, 3.95) * (1 - seg(d, 4.1, 4.9)) * 1.0
  $('glow').style.opacity = gl
  $('glow').style.transform = `scale(${lerp(0.6, 1.5, seg(d, 3.2, 4.4))})`
  // aparece el maniquí
  const r = easeOut(seg(d, 3.95, 4.7))
  const zoom = 1 + 0.045 * seg(d, 4.7, 8.1)
  const fig = $('fig')
  fig.style.opacity = r
  fig.style.filter = `blur(${(1 - r) * 16}px)`
  fig.style.transform = `translateX(-50%) scale(${lerp(0.93, 1, r) * zoom}) translateY(${Math.sin(d * 2) * 2}px)`

  // dedo
  const k = keyPos(d, [[0.9, 430, 820, 0], [2.3, 288, 659, 1]])
  finger('finger', 'ripple', k.x, k.y, seg(d, 0.9, 1.1) * (1 - seg(d, 2.55, 2.75)), k.tap)
}

/* ---------- E: galería y comparar ---------- */
const GALLERY = [['out-6.png', '8 nov'], ['out-3.png', '8 nov'], ['out-1.png', '7 nov'], ['out-8.png', '7 nov']]
const CAR = ['out-6.png', 'out-3.png', 'out-1.png', 'out-8.png']
$('cards').innerHTML = GALLERY.map((g, i) => `<div class="card" id="cd${i}" style="left:${16 + (i % 2) * 144}px;top:${142 + Math.floor(i / 2) * 238}px"><img src="assets/${g[0]}"><span>${g[1]}</span></div>`).join('')

function renderE(d) {
  const e = easeOut(seg(d, 0, 0.45))
  $('phoneE').style.transform = `translateX(${(1 - e) * 90}px)`
  $('phoneE').style.opacity = e
  GALLERY.forEach((_, i) => {
    const k = pop(d, 0.2 + i * 0.1, 0.35)
    const el = $('cd' + i)
    el.style.opacity = clamp(k)
    el.style.transform = `scale(${lerp(0.88, 1, clamp(k))}) translateY(${(1 - clamp(k)) * 24}px)`
  })
  // dedo toca la primera vista
  const k = keyPos(d, [[0.55, 440, 780, 0], [1.1, 216, 315, 1]])
  finger('fingerE', 'rippleE', k.x, k.y, seg(d, 0.55, 0.75) * (1 - seg(d, 1.3, 1.45)), k.tap)
  const sh = easeOut(seg(d, 1.2, 1.65))
  $('sheetE').style.transform = `translateY(${(1 - sh) * 100}%)`
  $('dimE').style.opacity = sh
  // pasa de una vista a otra
  const t0 = 1.75, per = 0.55
  const idx = clamp(Math.floor((d - t0) / per), 0, 3)
  const p = ((d - t0) % per) / per
  $('bigImg').setAttribute('src', 'assets/' + CAR[d < t0 ? 0 : idx])
  let dx = 0, op = 1
  if (d >= t0 && d < t0 + per * 4) {
    if (p < 0.22 && idx > 0) { dx = lerp(70, 0, easeOut(p / 0.22)); op = p / 0.22 }
    if (p > 0.86 && idx < 3) { dx = lerp(0, -70, (p - 0.86) / 0.14); op = 1 - (p - 0.86) / 0.14 }
  }
  $('bigImg').style.transform = `translateX(calc(-50% + ${dx}px))`
  $('bigImg').style.opacity = op

  // evento
  const ev = pop(d, 3.75, 0.4) * (1 - seg(d, 6.3, 6.5))
  $('evChip').style.opacity = clamp(ev)
  $('evChip').style.transform = `scale(${lerp(0.85, 1, clamp(ev))})`

  // compara
  const c = seg(d, 6.7, 7.0)
  $('cmpDim').style.opacity = c
  const a = easeOut(seg(d, 6.75, 7.2)), b = easeOut(seg(d, 6.9, 7.35))
  const A = $('cmpA'), B = $('cmpB')
  A.style.opacity = a; B.style.opacity = b
  A.style.left = lerp(-260, 40, a) + 'px'; A.style.top = '170px'
  B.style.left = lerp(576, 300, b) + 'px'; B.style.top = '170px'
  A.style.transform = `rotate(${-2.5 * a}deg) scale(${lerp(1, 0.97, seg(d, 7.5, 7.9))})`
  const win = pop(d, 7.5, 0.4)
  B.style.transform = `rotate(${2.5 * b}deg) scale(${lerp(1, 1.04, clamp(win))})`
  $('tickB').style.opacity = clamp(win)
  $('tickB').style.transform = `scale(${clamp(win) * 1})`
}

function render(t) {
  for (const id of SCENES) show(id, 0)
  if (t >= 0 && t <= 1.7) {
    const l = t
    show('car', 1)
    drawCar(l)
    $('car').style.transform = `scale(${lerp(1.05, 1, easeOut(seg(l, 0, 1.7)))})`
    const cc = pop(l, 0.2, 0.35)
    $('carChip').style.opacity = clamp(cc); $('carChip').style.transform = `scale(${lerp(0.85, 1, clamp(cc))})`
  } else if (t >= 2 && t <= 3.8) {
    const l = t - 2
    show('walk', 1)
    drawWalk(l)
    $('walk').style.transform = `scale(${lerp(1.05, 1, easeOut(seg(l, 0, 1.8)))})`
    const cc = pop(l, 0.2, 0.35)
    $('walkChip').style.opacity = clamp(cc); $('walkChip').style.transform = `scale(${lerp(0.85, 1, clamp(cc))})`
  } else if (t >= 4 && t <= 13.4) {
    show('sceneD', 1)
    renderD(t - 4)
  } else if (t >= 15 && t <= 23.4) {
    show('sceneE', 1)
    renderE(t - 15)
  }
}
window.render = render
