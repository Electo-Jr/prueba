// «Antes vs. ahora»: pantalla dividida, una por una (arriba) vs. de golpe (abajo). 576x1024 CSS px (x1.875).
// Prendas en emoji. Sin tiempos ni cifras no reales: solo 12 prendas, 5 pasos por prenda y hasta 18 fotos.
const $ = (id) => document.getElementById(id)
const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v))
const seg = (t, a, b) => clamp((t - a) / (b - a))
const easeOut = (x) => 1 - Math.pow(1 - x, 3)
const easeInOut = (x) => (x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2)
const lerp = (a, b, x) => a + (b - a) * x
const win = (t, a, b, f = 0.3) => easeOut(seg(t, a, a + f)) * (1 - seg(t, b - f, b))

const T = { hookOut: 1.4, split: 1.6, race: 3.2, tap: 5.0, ready: 7.9, zoom: 10.4, tag: 12.6, end: 14.0, total: 16.0 }
const CYC = 1.4 // duración de un ciclo por prenda (arriba)

const BEIGE = 'filter:sepia(.7) saturate(.7) brightness(1.35)'
const DARK = 'filter:grayscale(1) brightness(.35)'
const TINTS = ['#e8dfcf', '#dcd3c2', '#efe6d6', '#d9cdb8', '#e3d8c6']
const G = [
  ['👕'], ['👖'], ['🧥', BEIGE], ['👟'], ['👗'], ['👔'], ['🧣'], ['🧢'], ['👜'], ['👚'], ['🩳'], ['👖', DARK],
]
const NAMES = ['Camiseta', 'Vaqueros', 'Chaqueta', 'Zapatillas', 'Vestido']
const STEPS = ['Añadir', 'Galería', 'Elegir foto', 'Rellenar por mí', 'Añadir al armario']

$('steps').innerHTML = STEPS.map((s, j) =>
  `<div class="st" id="st${j}" style="left:${18 + j * 108}px"><b>${j + 1}</b>${s}</div>`).join('')
$('slots').innerHTML = Array.from({ length: 12 }, (_, i) =>
  `<div class="slot" id="sl${i}" style="left:${24 + i * 44}px"><div class="e emo">${G[i][0]}</div></div>`).join('')
$('grid').innerHTML = G.map((p, i) => {
  const c = i % 3
  const r = Math.floor(i / 3)
  return `<div class="th" id="th${i}" style="left:${c * 162}px;top:${r * 64}px;background:${TINTS[i % 5]}">` +
    `<div class="e emo" style="${p[1] || ''}">${p[0]}</div><div class="k">✓</div></div>`
}).join('')

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

function render(t) {
  // --- Gancho ---
  const hook = $('hook')
  const hOut = seg(t, T.hookOut, T.hookOut + 0.3)
  const hIn = easeOut(seg(t, 0, 0.5))
  hook.style.opacity = hIn * (1 - hOut)
  hook.style.transform = `translateY(${(1 - hIn) * 30 - easeOut(hOut) * 30}px)`

  // --- Pantalla dividida ---
  const sp = easeOut(seg(t, T.split, T.split + 0.4)) * (1 - seg(t, T.tag - 0.05, T.tag + 0.2))
  $('split').style.opacity = sp
  const zoom = easeInOut(seg(t, T.zoom, T.zoom + 0.7))
  $('top').style.opacity = 1 - zoom
  $('div').style.opacity = 1 - zoom
  $('lBot').style.opacity = 1 - zoom
  $('bArea').style.transform = `translateY(${-360 * zoom}px) scale(${1 + 0.15 * zoom})`
  // Etiquetas entran con un pequeño deslizamiento
  const lab = easeOut(seg(t, T.split + 0.1, T.split + 0.5))
  $('lTop').style.transform = `translateY(${(1 - lab) * -16}px)`
  $('lBot').style.transform = `translateY(${(1 - lab) * 16}px)`

  // --- ARRIBA: una por una ---
  const topLive = t >= T.race
  const c = clamp(Math.floor((t - T.race) / CYC), 0, 4)
  const lt = topLive ? clamp(t - T.race - c * CYC, 0, CYC) : 0 // tiempo local del ciclo
  const SD = 0.28
  const doneIdx = topLive ? Math.min(5, Math.floor((lt - 0.06) / SD) + 1) : 0 // pasos marcados
  const cycleDone = topLive && t - T.race >= (c + 1) * CYC - 0.001
  for (let j = 0; j < 5; j++) {
    const el = $('st' + j)
    const on = topLive && j < Math.max(0, doneIdx)
    el.className = 'st' + (on ? ' on' : '') + (topLive && j === doneIdx && doneIdx < 5 ? ' cur' : '')
    el.firstElementChild.textContent = on ? '✓' : String(j + 1)
  }
  $('tCnt').textContent = `Prenda ${c + 1} de 12`
  const card = $('tCard')
  const fly = seg(lt, 1.12, 1.4)
  const hasPhoto = topLive && doneIdx >= 3
  const hasName = topLive && doneIdx >= 4
  card.querySelector('.p').style.opacity = hasPhoto ? 0 : 1
  const e = card.querySelector('.e')
  e.textContent = G[c][0]
  e.style.cssText = G[c][1] || ''
  e.style.opacity = hasPhoto ? 1 : 0
  card.querySelector('.n').textContent = hasName ? '✨ ' + NAMES[c] : ''
  const f = easeInOut(fly)
  const tx = lerp(0, (24 + c * 44 + 19) - 288, f)
  const ty = lerp(0, 399 - 284, f)
  const sc = lerp(1, 0.26, f)
  const born = easeOut(seg(t, T.split + 0.2, T.split + 0.6))
  const cardA = (topLive && cycleDone && c === 4) || (fly >= 1) ? 0 : 1
  card.style.opacity = cardA * born
  card.style.transform = `translate(${tx}px,${ty}px) scale(${sc})`
  let filled = 0
  for (let i = 0; i < 12; i++) {
    const done = topLive && (i < c || (i === c && fly >= 1))
    $('sl' + i).className = 'slot' + (done ? ' f' : '')
    if (done) filled++
  }
  $('tMeta').textContent = topLive ? `${filled} de 12 en el armario` : ''

  // --- ABAJO: de golpe ---
  let sel = 0
  for (let i = 0; i < 12; i++) {
    const a = easeOut(seg(t, T.race + 0.1 + i * 0.12, T.race + 0.1 + i * 0.12 + 0.25))
    const el = $('th' + i)
    el.style.opacity = a
    el.style.transform = `scale(${0.7 + 0.3 * a})`
    if (a > 0.5) sel++
  }
  // conversión a tarjetas de prenda, mientras avanza la barra
  let made = 0
  for (let i = 0; i < 12; i++) {
    const cs = 5.5 + i * 0.2
    const isCard = t >= cs
    const el = $('th' + i)
    el.className = 'th' + (isCard ? ' card' : '')
    if (isCard) {
      made++
      const pop = easeOut(seg(t, cs, cs + 0.25))
      el.style.transform = `scale(${0.92 + 0.08 * pop})`
    }
  }
  const allMade = made >= 12 && t >= 7.7
  const bc = $('bCntT')
  if (t < 5.2) {
    const full = sel >= 12
    bc.textContent = full ? '12 fotos · listo' : `${sel} ${sel === 1 ? 'foto' : 'fotos'}`
    bc.className = full ? 'ok' : ''
  } else {
    bc.textContent = allMade ? '12 de 12 ✓' : `${made} de 12`
    bc.className = allMade ? 'ok' : ''
  }
  const bBtn = $('bBtn')
  const btnA = easeOut(seg(t, T.race + 1.0, T.race + 1.4))
  bBtn.style.opacity = btnA
  const prog = clamp((t - 5.3) / (7.7 - 5.3))
  $('bBar').style.width = `${easeInOut(prog) * 100}%`
  const tapPulse = Math.max(0, 1 - Math.abs(t - T.tap) / 0.16)
  bBtn.style.transform = `scale(${1 - 0.05 * tapPulse})`
  const bt = $('bBtnT')
  if (t < 5.2) bt.textContent = 'Montar mi armario'
  else if (t < T.ready) bt.textContent = 'Montando tu armario…'
  else bt.textContent = '✓ Tu armario está listo para revisar'
  bBtn.style.background = t >= T.ready ? '#4f7a48' : '#15140f'
  bBtn.querySelector('.bar').style.opacity = t < T.ready ? 1 : 0

  // --- Subtítulo central ---
  $('sub').style.opacity = win(t, 5.0, 10.4, 0.35) * sp
  // --- Revisión sí/no ---
  const capA = win(t, 11.0, 12.6, 0.35)
  $('cap2').style.opacity = capA
  $('cap2').style.transform = `translateY(${(1 - capA) * 18}px)`
  $('yn').style.opacity = win(t, 11.2, 12.6, 0.35)
  $('rby').style.transform = `scale(${1 + 0.1 * clamp(1 - Math.abs(t - 12.0) / 0.2)})`

  // --- Texto final y cierre ---
  const tg = win(t, T.tag, T.end + 0.1, 0.35)
  $('tag').style.opacity = tg
  $('tag').style.transform = `translateY(${(1 - easeOut(seg(t, T.tag, T.tag + 0.5))) * 24}px)`
  const end = $('end')
  end.style.opacity = easeOut(seg(t, T.end, T.end + 0.4))
  for (const [cls, d] of [['k', 0], ['w', 0.08], ['p', 0.4], ['u', 0.65], ['s', 0.8]]) {
    const el = end.querySelector(`.${cls}`)
    const a = easeOut(seg(t, T.end + d, T.end + d + 0.45))
    el.style.opacity = a
    el.style.transform = `translateY(${(1 - a) * 18}px)`
  }

  // --- Cursor: toca «Montar mi armario» ---
  let cx = 288, cy = 980, ca = 0, tapv = 0
  if (t >= 4.2 && t < 5.7) {
    const k = cursorAt(t, [[4.3, [440, 1000]], [4.9, [288, 940]], [T.tap, [288, 940], true], [5.5, [288, 940]]])
    cx = k.x; cy = k.y; tapv = k.tap
    ca = easeOut(seg(t, 4.2, 4.4)) * (1 - seg(t, 5.3, 5.7))
  }
  const cur = $('cursor')
  cur.style.left = `${cx}px`
  cur.style.top = `${cy}px`
  cur.style.opacity = ca * 0.95
  cur.style.transform = `scale(${1 - tapv * 0.28})`
}

window.render = render
window.DURATION = T.total
