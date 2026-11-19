// «Esto o esto»: vídeo corto de la novedad «Afina tu estilo». 576x1024 CSS px (x1.875 = 1080x1920).
// Prendas en emoji, como en el otro anuncio: sin ropa real ni datos de nadie.
const $ = (id) => document.getElementById(id)
const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v))
const seg = (t, a, b) => clamp((t - a) / (b - a))
const easeOut = (x) => 1 - Math.pow(1 - x, 3)
const easeInOut = (x) => (x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2)
const lerp = (a, b, x) => a + (b - a) * x

// Momentos (segundos).
const T = {
  hookEnd: 1.5,
  d1: 1.5, d1pick: 3.15,
  d2: 4.35, d2pick: 5.95,
  both: 7.0, bothPick: 8.35,
  mont: 9.2, montEnd: 11.0,
  res: 11.0, end: 13.6, total: 15.8,
}

const WHITE = 'filter:grayscale(1) brightness(2.1) contrast(.85)'
const BEIGE = 'filter:sepia(.7) saturate(.7) brightness(1.35)'
const DARK = 'filter:grayscale(1) brightness(.35)'

const LOOKS = {
  a1: { t: ['👕'], b: ['👖'], s: ['👟'], a: '⌚' },
  a2: { t: ['👔'], b: ['👖', BEIGE], s: ['👞'] },
  b1: { t: ['👕'], b: ['👖'], s: ['👟'] },
  b2: { t: ['👕'], b: ['👖', WHITE], s: ['👟'] },
  c1: { t: ['🧥'], b: ['👖', DARK], s: ['👞'] },
  c2: { t: ['👕', 'filter:hue-rotate(160deg)'], b: ['👖', BEIGE], s: ['👟'], a: '🧢' },
  m1: { t: ['👔'], b: ['👖', DARK], s: ['👞'] },
  m2: { t: ['🧥'], b: ['👖', BEIGE], s: ['👟'] },
  m3: { t: ['👕', DARK], b: ['👖'], s: ['👟'] },
  m4: { t: ['👔', BEIGE], b: ['👖', WHITE], s: ['👞'] },
  m5: { t: ['🧥', BEIGE], b: ['👖'], s: ['👟'] },
  m6: { t: ['👕', WHITE], b: ['👖', DARK], s: ['👞'], a: '⌚' },
}

function fill(el, look) {
  const piece = (cls, v) => (v ? `<div class="g ${cls} emo" style="${v[1] || ''}">${v[0]}</div>` : '')
  el.innerHTML =
    piece('t', look.t) + piece('b', look.b) + piece('s', look.s) +
    (look.a ? `<div class="g a emo">${look.a}</div>` : '') +
    '<div class="tick">✓</div>'
}

let shown = ''
function setPair(l, r) {
  const key = l + r
  if (key === shown) return
  shown = key
  fill($('bL'), LOOKS[l])
  fill($('bR'), LOOKS[r])
}

function mark(board, on, dim) {
  board.style.borderColor = on ? '#8a6a4f' : 'transparent'
  board.style.opacity = dim ? 0.38 : 1
  board.style.transform = on ? 'scale(1.025)' : 'scale(1)'
  const tick = board.querySelector('.tick')
  if (tick) tick.style.opacity = on ? 1 : 0
}

// Posiciones del cursor.
const POS = {
  rest: [288, 880],
  L: [147, 470],
  R: [429, 470],
  both: [147, 697],
  none: [429, 697],
}

function cursorAt(t, keys) {
  // keys: [[tiempo, pos, tap?], ...] ordenados.
  let p = keys[0]
  let n = keys[keys.length - 1]
  for (let i = 0; i < keys.length - 1; i++) {
    if (t >= keys[i][0] && t < keys[i + 1][0]) {
      p = keys[i]
      n = keys[i + 1]
      break
    }
  }
  if (t >= keys[keys.length - 1][0]) return { x: n[1][0], y: n[1][1], tap: 0 }
  const k = easeInOut(seg(t, p[0], n[0] - 0.12))
  const x = lerp(p[1][0], n[1][0], k)
  const y = lerp(p[1][1], n[1][1], k)
  const tap = n[2] ? Math.max(0, 1 - Math.abs(t - n[0]) / 0.16) : 0
  return { x, y, tap }
}

function caption(html, a) {
  const el = $('cap')
  if (el.dataset.h !== html) {
    el.innerHTML = html
    el.dataset.h = html
  }
  el.style.opacity = a
  el.style.transform = `translateY(${(1 - a) * 18}px)`
}

function render(t) {
  const hook = $('hook')
  const ui = $('ui')

  // --- Gancho ---------------------------------------------------------------
  const hookOut = seg(t, 1.1, 1.6)
  hook.style.opacity = 1 - hookOut
  hook.style.transform = `translateY(${-easeOut(hookOut) * 40}px) scale(${1 - hookOut * 0.05})`
  const hookIn = easeOut(seg(t, 0, 0.55))
  hook.firstElementChild.style.transform = `translateY(${(1 - hookIn) * 30}px)`
  hook.firstElementChild.style.opacity = hookIn

  // --- Interfaz -------------------------------------------------------------
  const uiA = t < T.res ? easeOut(seg(t, 1.25, 1.75)) : 1 - easeOut(seg(t, T.res, T.res + 0.4))
  ui.style.opacity = uiA

  const bL = $('bL')
  const bR = $('bR')
  let progress = 1
  let cap = ['', 0]
  let cursorKeys = [[0, POS.rest]]
  let chip = 0
  let ringA = 0

  if (t < T.d2 - 0.35) {
    // Duelo 1: dos looks distintos.
    setPair('a1', 'a2')
    progress = 1
    const sel = seg(t, T.d1pick, T.d1pick + 0.25)
    mark(bL, false, sel > 0.5)
    mark(bR, sel > 0.5, false)
    cap = ['Toca el look que <i>te pondrías</i>', easeOut(seg(t, 1.9, 2.4)) * (1 - seg(t, 4.0, 4.3))]
    cursorKeys = [[1.5, POS.rest], [2.9, POS.R], [T.d1pick, POS.R, true], [4.3, POS.R]]
  } else if (t < T.both - 0.3) {
    // Duelo 2: cambia una sola prenda.
    setPair('b1', 'b2')
    progress = 2
    const sel = seg(t, T.d2pick, T.d2pick + 0.25)
    mark(bL, sel > 0.5, false)
    mark(bR, false, sel > 0.5)
    cap = ['A veces cambia <i>solo una prenda</i>', easeOut(seg(t, 4.7, 5.2)) * (1 - seg(t, 6.6, 6.9))]
    chip = easeOut(seg(t, 4.5, 4.9)) * (1 - seg(t, 6.2, 6.5))
    ringA = easeOut(seg(t, 4.7, 5.1)) * (1 - seg(t, 6.0, 6.3))
    cursorKeys = [[4.3, POS.R], [5.6, POS.L], [T.d2pick, POS.L, true], [6.9, POS.L]]
  } else if (t < T.mont - 0.2) {
    // Duelo 3: «los dos» y «ninguno».
    setPair('c1', 'c2')
    progress = 3
    const sel = seg(t, T.bothPick, T.bothPick + 0.25)
    mark(bL, sel > 0.5, false)
    mark(bR, sel > 0.5, false)
    cap = ['¿Te gustan los dos? <i>¿Ninguno?</i>', easeOut(seg(t, 7.3, 7.8)) * (1 - seg(t, 8.9, 9.2))]
    cursorKeys = [[6.9, POS.L], [7.7, POS.none], [7.95, POS.none], [8.15, POS.both], [T.bothPick, POS.both, true], [9.3, POS.both]]
  } else if (t < T.res) {
    // Montaje rápido: duelos 4 a 6.
    const step = clamp(Math.floor((t - T.mont) / ((T.montEnd - T.mont) / 3)), 0, 2)
    const pairs = [['m1', 'm2'], ['m3', 'm4'], ['m5', 'm6']]
    setPair(pairs[step][0], pairs[step][1])
    progress = 4 + step
    const local = ((t - T.mont) % ((T.montEnd - T.mont) / 3)) / ((T.montEnd - T.mont) / 3)
    const pickRight = step % 2 === 0
    mark(bL, local > 0.55 && !pickRight, local > 0.55 && pickRight)
    mark(bR, local > 0.55 && pickRight, local > 0.55 && !pickRight)
    cap = ['Seis duelos. <i>Un minuto.</i>', easeOut(seg(t, 9.4, 9.8)) * (1 - seg(t, 10.7, 11.0))]
    cursorKeys = [[9.2, POS.both], [9.55, pickRight ? POS.R : POS.L, true], [11.0, POS.R]]
  } else {
    progress = 6
  }

  $('pn').textContent = `${Math.min(6, progress)} de 6`
  $('pbar').style.width = `${(Math.min(6, progress) / 6) * 100}%`
  ui.style.transform = ''

  // Anillos sobre los pantalones del duelo 2.
  for (const [id, x] of [['ringL', 12 + 135], ['ringR', 294 + 135]]) {
    const el = $(id)
    el.style.left = `${x - 62}px`
    el.style.top = `${282 + 108 + 56 - 62}px`
    el.style.width = '124px'
    el.style.height = '124px'
    el.style.opacity = ringA
    el.style.transform = `scale(${1 + 0.12 * Math.sin(t * 7)})`
  }
  caption(cap[0], cap[1])

  // Cursor.
  const c = cursorAt(t, cursorKeys)
  const cur = $('cursor')
  cur.style.left = `${c.x}px`
  cur.style.top = `${c.y}px`
  const curShow = t > 1.9 && t < T.res + 0.1 ? 1 : 0
  cur.style.opacity = curShow * 0.95
  cur.style.transform = `scale(${1 - c.tap * 0.28})`

  // --- Resultado ------------------------------------------------------------
  const res = $('result')
  const resA = easeOut(seg(t, T.res, T.res + 0.5)) * (t < T.end ? 1 : 1 - seg(t, T.end, T.end + 0.4))
  res.style.opacity = resA
  const bars = [['s1', 0.78, 0.2], ['s2', 0.70, 0.45], ['s3', 0.12, 0.7]]
  for (const [id, v, d] of bars) {
    $(id).querySelector('i').style.width = `${easeOut(seg(t, T.res + d, T.res + d + 0.9)) * v * 100}%`
    $(id).style.opacity = easeOut(seg(t, T.res + d - 0.1, T.res + d + 0.3))
  }
  $('rsub').style.opacity = easeOut(seg(t, T.res + 1.2, T.res + 1.7))
  res.querySelector('.h').style.transform = `translateY(${(1 - easeOut(seg(t, T.res + 0.1, T.res + 0.7))) * 24}px)`

  // --- Cierre ---------------------------------------------------------------
  const end = $('end')
  end.style.opacity = easeOut(seg(t, T.end, T.end + 0.5))
  const parts = [['k', 0], ['w', 0.1], ['p', 0.5], ['u', 0.8], ['s', 1.0]]
  for (const [cls, d] of parts) {
    const el = end.querySelector(`.${cls}`)
    const a = easeOut(seg(t, T.end + d, T.end + d + 0.5))
    el.style.opacity = a
    el.style.transform = `translateY(${(1 - a) * 18}px)`
  }
}

window.render = render
window.DURATION = T.total
