// «Subir varias fotos»: anuncio de la novedad. 576x1024 CSS px (x1.875 = 1080x1920).
// Prendas en emoji: sin ropa real ni datos de nadie. Misma estructura que duelo.js.
const $ = (id) => document.getElementById(id)
const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v))
const seg = (t, a, b) => clamp((t - a) / (b - a))
const easeOut = (x) => 1 - Math.pow(1 - x, 3)
const easeInOut = (x) => (x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2)
const lerp = (a, b, x) => a + (b - a) * x

const T = {
  hookOut: 1.3,
  s1: 1.5, tap: 3.78, up: 3.9,
  an: 4.8, anEnd: 8.6,
  nf: 8.6, nfEnd: 10.3,
  dk: 10.2, dkEnd: 13.1,
  res: 13.0, end: 14.2, total: 16.0,
}

const WHITE = 'filter:grayscale(1) brightness(2.1) contrast(.85)'
const BEIGE = 'filter:sepia(.7) saturate(.7) brightness(1.35)'
const DARK = 'filter:grayscale(1) brightness(.35)'
const HUE = 'filter:hue-rotate(160deg)'
const TINTS = ['#e8dfcf', '#dcd3c2', '#efe6d6', '#d9cdb8', '#e3d8c6']

// 15 fotos de prendas.
const PHOTOS = [
  ['👕'], ['👖'], ['🧥', BEIGE], ['👟'], ['👗'], ['👔'], ['🧣'], ['🧢'], ['👜'],
  ['👚'], ['🩳'], ['👞'], ['🧦'], ['👠'], ['👖', DARK],
]
// 23 prendas que saca la app.
const GARMENTS = [
  ['👕'], ['👖'], ['🧥', BEIGE], ['👟'], ['👗'], ['👔'], ['🧣'], ['🧢'], ['👜'], ['👚'], ['🩳'], ['👞'],
  ['🧦'], ['👠'], ['👖', DARK], ['👕', WHITE], ['👕', HUE], ['🧥'], ['👔', BEIGE], ['👟', WHITE], ['👖', WHITE], ['🧢', DARK], ['👚', BEIGE],
]

// Construcción de cuadrículas.
$('grid1').innerHTML = PHOTOS.map((p, i) => {
  const c = i % 3
  const r = Math.floor(i / 3)
  return `<div class="th" id="th${i}" style="left:${c * 162}px;top:${r * 124}px;background:${TINTS[i % 5]}">` +
    `<div class="e emo" style="${p[1] || ''}">${p[0]}</div><div class="k">✓</div></div>`
}).join('')
$('grid2').innerHTML = GARMENTS.map((p, i) => {
  const c = i % 5
  const r = Math.floor(i / 5)
  return `<div class="pc" id="pc${i}" style="left:${62 + c * 92}px;top:${400 + r * 92}px;background:${TINTS[(i * 2) % 5]}">` +
    `<div class="e emo" style="${p[1] || ''}">${p[0]}</div></div>`
}).join('')

// Baraja.
const DECK = [
  { e: '👕', f: WHITE, n: 'Camiseta · blanca', dir: 1 },
  { e: '👖', f: '', n: 'Vaqueros · azules', dir: 1 },
  { e: '🧥', f: BEIGE, n: 'Chaqueta · beige', dir: -1 },
  { e: '👟', f: WHITE, n: 'Zapatillas · blancas', dir: 1 },
]
const DK0 = 10.2
const DK_STEP = 0.93
const SWIPE_OFF = 0.52
const SWIPE_LEN = 0.3
function setCard(el, c) {
  const e = el.querySelector('.e')
  const n = el.querySelector('.n')
  if (el.dataset.k !== c.n) {
    el.dataset.k = c.n
    e.textContent = c.e
    e.style.cssText = c.f
    n.textContent = c.n
  }
}

function cursorAt(t, keys) {
  let p = keys[0]
  let n = keys[keys.length - 1]
  for (let i = 0; i < keys.length - 1; i++) {
    if (t >= keys[i][0] && t < keys[i + 1][0]) { p = keys[i]; n = keys[i + 1]; break }
  }
  if (t >= keys[keys.length - 1][0]) return { x: n[1][0], y: n[1][1], tap: 0 }
  const k = easeInOut(seg(t, p[0], n[0] - 0.08))
  const tap = n[2] ? Math.max(0, 1 - Math.abs(t - n[0]) / 0.16) : 0
  return { x: lerp(p[1][0], n[1][0], k), y: lerp(p[1][1], n[1][1], k), tap }
}

function caption(html, a) {
  const el = $('cap')
  if (el.dataset.h !== html) { el.innerHTML = html; el.dataset.h = html }
  el.style.opacity = a
  el.style.transform = `translateY(${(1 - a) * 18}px)`
}

const win = (t, a, b, f = 0.3) => easeOut(seg(t, a, a + f)) * (1 - seg(t, b - f, b))

function render(t) {
  // --- Gancho ---
  const hook = $('hook')
  const hOut = seg(t, T.hookOut, T.hookOut + 0.4)
  hook.style.opacity = 1 - hOut
  hook.style.transform = `translateY(${-easeOut(hOut) * 40}px) scale(${1 - hOut * 0.05})`
  const hIn = easeOut(seg(t, 0, 0.55))
  hook.firstElementChild.style.transform = `translateY(${(1 - hIn) * 30}px)`
  hook.firstElementChild.style.opacity = hIn
  const sIn = easeOut(seg(t, 0.7, 1.1))
  $('hsub').style.opacity = sIn
  $('hsub').style.transform = `translateY(${(1 - sIn) * 14}px)`

  // --- Pantalla 1: elegir fotos ---
  $('s1').style.opacity = win(t, T.s1, 4.95, 0.3)
  let shownN = 0
  for (let i = 0; i < 15; i++) {
    const a = easeOut(seg(t, 1.75 + i * 0.105, 1.75 + i * 0.105 + 0.25))
    const el = $('th' + i)
    el.style.opacity = a
    el.style.transform = `scale(${0.7 + 0.3 * a})`
    if (a > 0.5) shownN++
  }
  const full = shownN >= 15
  $('cntT').textContent = full ? '15 fotos · listo' : `${shownN} ${shownN === 1 ? 'foto' : 'fotos'}`
  $('cntT').className = full ? 'ok' : ''
  const upA = easeOut(seg(t, T.up, T.up + 0.3))
  const montA = easeOut(seg(t, 3.2, 3.5)) * (1 - seg(t, T.tap, T.tap + 0.15))
  const tapped = seg(t, T.tap, T.tap + 0.15)
  $('mont').style.opacity = montA
  $('mont').style.transform = `scale(${1 - 0.05 * Math.max(0, 1 - Math.abs(t - T.tap) / 0.16)})`
  $('grid1').style.opacity = 1 - 0.8 * upA
  $('grid1').style.transform = `scale(${1 - 0.04 * upA})`
  const up = $('up')
  up.style.opacity = upA
  up.style.transform = `translateY(${(1 - upA) * 24}px)`
  const upN = Math.round(lerp(2, 8, easeOut(seg(t, T.up + 0.1, T.up + 0.85))))
  $('upT').textContent = `Subiendo ${upN} de 15…`
  $('upB').style.width = `${(upN / 15) * 100}%`

  // --- Pantalla 2: análisis ---
  $('an').style.opacity = win(t, T.an, T.anEnd + 0.2, 0.3)
  const titles = ['Identificando prendas…', 'Anotando colores y cortes…', 'Montando tu armario…']
  const ti = t < 5.9 ? 0 : t < 7.2 ? 1 : 2
  const tStart = [T.an, 5.9, 7.2][ti]
  $('anT').textContent = titles[ti]
  $('anT').style.opacity = easeOut(seg(t, tStart, tStart + 0.25))
  $('anB').style.width = `${easeOut(seg(t, T.an, T.anEnd - 0.1)) * 100}%`
  let nAn = 0
  for (let i = 0; i < 23; i++) {
    const s0 = 4.95 + i * 0.145
    const a = easeOut(seg(t, s0, s0 + 0.22))
    const el = $('pc' + i)
    el.style.opacity = a
    el.style.transform = `scale(${0.6 + 0.4 * a})`
    if (t >= s0) nAn = i + 1
  }
  $('anN').textContent = String(nAn)

  // --- Notificación ---
  $('nf').style.opacity = win(t, T.nf, T.nfEnd, 0.25)
  const nk = easeOut(seg(t, 8.7, 9.25))
  $('nt').style.top = `${lerp(-200, 300, nk)}px`

  // --- Baraja ---
  $('dk').style.opacity = win(t, T.dk, T.dkEnd + 0.1, 0.25)
  const k = clamp(Math.floor((t - DK0) / DK_STEP), 0, 2)
  const sw = seg(t, DK0 + k * DK_STEP + SWIPE_OFF, DK0 + k * DK_STEP + SWIPE_OFF + SWIPE_LEN)
  const dir = DECK[k].dir
  setCard($('dcF'), DECK[k])
  setCard($('dcB'), DECK[k + 1])
  const front = $('dcF')
  const born = easeOut(seg(t, DK0 + k * DK_STEP, DK0 + k * DK_STEP + 0.2))
  const px = dir * easeInOut(sw) * 520
  front.style.transform = `translateX(${px}px) rotate(${dir * easeInOut(sw) * 16}deg) scale(${k === 0 ? 0.96 + 0.04 * born : 1})`
  front.style.opacity = 1 - seg(sw, 0.8, 1)
  $('dcB').style.transform = `scale(${0.94 + 0.04 * easeOut(sw)}) translateY(${14 - 14 * easeOut(sw)}px)`
  $('dcB').style.opacity = 0.7
  front.querySelector('.stamp.y').style.opacity = dir > 0 ? clamp(sw * 4) : 0
  front.querySelector('.stamp.x').style.opacity = dir < 0 ? clamp(sw * 4) : 0
  const shownIdx = Math.min(k + 1, 3)
  $('dkH').textContent = `Revisar ${shownIdx} de 23`
  $('dkB').style.width = `${(shownIdx / 23) * 100}%`
  $('rbx').style.transform = `scale(${dir < 0 ? 1 + 0.15 * sw : 1})`
  $('rby').style.transform = `scale(${dir > 0 ? 1 + 0.15 * sw : 1})`

  // --- Resultado y cierre ---
  const res = $('result')
  res.style.opacity = easeOut(seg(t, T.res, T.res + 0.4)) * (t < T.end ? 1 : 1 - seg(t, T.end, T.end + 0.35))
  res.querySelector('.h').style.transform = `translateY(${(1 - easeOut(seg(t, T.res + 0.1, T.res + 0.6))) * 24}px)`
  $('result').querySelector('.p').style.opacity = easeOut(seg(t, T.res + 0.45, T.res + 0.85))
  const end = $('end')
  end.style.opacity = easeOut(seg(t, T.end, T.end + 0.4))
  for (const [cls, d] of [['k', 0], ['w', 0.08], ['p', 0.4], ['u', 0.65], ['s', 0.8]]) {
    const el = end.querySelector(`.${cls}`)
    const a = easeOut(seg(t, T.end + d, T.end + d + 0.45))
    el.style.opacity = a
    el.style.transform = `translateY(${(1 - a) * 18}px)`
  }

  // --- Subtítulos ---
  let cap = ['', 0]
  if (t < 3.7) cap = ['Elige todas <i>de golpe</i>', win(t, 1.9, 3.6, 0.3)]
  else if (t < 8.6) cap = ['La app saca las prendas <i>por ti</i>', win(t, 5.1, 8.5, 0.3)]
  else if (t < 10.4) cap = ['Puedes salir. <i>Te avisa.</i>', win(t, 9.1, 10.2, 0.3)]
  else if (t < 13.0) cap = ['Revisa <i>de un vistazo</i>', win(t, 10.5, 12.95, 0.3)]
  caption(cap[0], cap[1])

  // --- Cursor ---
  let cx = 288, cy = 980, ca = 0, tap = 0
  if (t >= 2.9 && t < 4.4) {
    const c = cursorAt(t, [[3.0, [440, 985]], [3.7, [288, 858]], [T.tap, [288, 858], true], [4.3, [288, 858]]])
    cx = c.x; cy = c.y; tap = c.tap
    ca = easeOut(seg(t, 2.9, 3.1)) * (1 - seg(t, 4.0, 4.4))
  } else if (t >= DK0 && t < T.dkEnd) {
    const s0 = DK0 + k * DK_STEP + SWIPE_OFF
    cx = 288 + px
    cy = 445 + dir * 0
    const near = clamp((t - (s0 - 0.25)) / 0.2)
    ca = near * (1 - seg(sw, 0.75, 1)) * 0.95
    tap = clamp(1 - Math.abs(t - s0) / 0.12) * 0
    if (t > s0 - 0.25 && t < s0 + 0.02) tap = clamp((t - (s0 - 0.25)) / 0.25) * 0.3
    else if (t >= s0 + 0.02) tap = 0.3
    if (t < s0 - 0.25) ca = 0
  }
  const cur = $('cursor')
  cur.style.left = `${cx}px`
  cur.style.top = `${cy}px`
  cur.style.opacity = ca * 0.95
  cur.style.transform = `scale(${1 - tap * 0.28})`
}

window.render = render
window.DURATION = T.total
