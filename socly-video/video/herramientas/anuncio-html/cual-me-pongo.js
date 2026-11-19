// «¿Cuál me pongo?»: anuncio de la votación del círculo. 576x1024 CSS px (x1.875 = 1080x1920).
// Prendas en emoji; cifras y cuenta atrás son solo de la maqueta.
const $ = (id) => document.getElementById(id)
const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v))
const seg = (t, a, b) => clamp((t - a) / (b - a))
const easeOut = (x) => 1 - Math.pow(1 - x, 3)
const easeInOut = (x) => (x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2)
const lerp = (a, b, x) => a + (b - a) * x
const win = (t, a, b, f = 0.3) => easeOut(seg(t, a, a + f)) * (1 - seg(t, b - f, b))

const T = { hookOut: 1.55, s1: 1.7, s1End: 6.6, v: 6.4, vEnd: 10.8, r: 10.6, rEnd: 12.8, dec: 12.6, decEnd: 14.2, end: 14.0, total: 16.0 }
const TINTS = ['#e8dfcf', '#dcd3c2', '#efe6d6', '#d9cdb8']
const LOOKS = [
  { l: 'A', e: ['👕', '👖', '👟', '🧢'] },
  { l: 'B', e: ['👗', '🧥', '👠', '👜'] },
  { l: 'C', e: ['👔', '🩳', '👞', '🧣'] },
]
// Votos en orden: B A B C B C B  => A 1, B 4, C 2 (7 votos)
const VOTES = [[6.95, 1], [7.4, 0], [7.8, 1], [8.3, 2], [8.8, 1], [9.3, 2], [9.8, 1]]

const row = (e) => `<div class="row">${e.map((x, i) => `<div class="g" style="background:${TINTS[i]}"><div class="e emo">${x}</div></div>`).join('')}</div>`
$('looks1').innerHTML = LOOKS.map((k, i) =>
  `<div class="look" id="l1_${i}" style="top:${232 + i * 134}px"><div class="lt">${k.l}</div>${row(k.e)}</div>`).join('')
$('looks2').innerHTML = LOOKS.map((k, i) =>
  `<div class="look vl" id="l2_${i}" style="top:${222 + i * 162}px"><div class="lt">${k.l}</div>${row(k.e.slice(0, 4))}` +
  `<div class="n" id="n${i}">0</div><div class="win" id="w${i}">VA GANANDO</div><div class="tr"><i id="b${i}"></i></div></div>`).join('')
$('rBig').innerHTML = `<div class="lt">B</div><div class="gr">${LOOKS[1].e.slice(0, 4).map((x, i) => `<div style="background:${TINTS[i]}"><div class="e emo">${x}</div></div>`).join('')}</div>` +
  `<div class="vt serif">4 de 7 <i>votos</i></div><div class="sm mono">Look B</div>`

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
const fmt = (s) => `${Math.floor(s / 60)}:${String(Math.round(s % 60)).padStart(2, '0')}`

function render(t) {
  // Gancho
  const hook = $('hook')
  const hOut = seg(t, T.hookOut, T.hookOut + 0.3)
  hook.style.opacity = 1 - hOut
  const hIn = easeOut(seg(t, 0, 0.55))
  hook.firstElementChild.style.transform = `translateY(${(1 - hIn) * 30 - easeOut(hOut) * 30}px)`
  hook.firstElementChild.style.opacity = hIn

  // Pantalla 1: tres looks + compartir
  $('s1').style.opacity = win(t, T.s1, T.s1End, 0.3)
  for (let i = 0; i < 3; i++) {
    const a = easeOut(seg(t, 2.0 + i * 0.3, 2.45 + i * 0.3))
    const el = $('l1_' + i)
    el.style.opacity = a
    el.style.transform = `translateY(${(1 - a) * 24}px)`
    el.style.filter = ''
  }
  const tapT = 5.0
  const shA = easeOut(seg(t, 3.3, 3.6)) * (1 - seg(t, tapT + 0.05, tapT + 0.2))
  $('share').style.opacity = shA
  $('share').style.transform = `scale(${1 - 0.05 * Math.max(0, 1 - Math.abs(t - tapT) / 0.16)})`
  const sh = easeOut(seg(t, tapT + 0.1, tapT + 0.5))
  $('sheet').style.opacity = sh
  $('sheet').style.transform = `translateY(${(1 - sh) * 40}px)`
  const dim = 1 - 0.7 * sh
  for (let i = 0; i < 3; i++) { /* las tarjetas se atenúan tras compartir */
    const el = $('l1_' + i)
    el.style.opacity = parseFloat(el.style.opacity) * dim
  }
  const left = 15 * 60 - Math.max(0, t - tapT) * 4
  $('shM').textContent = `Quedan ${fmt(left)}`
  $('sheet').querySelector('.bar small').textContent = `Quedan ${fmt(left)}`

  // Votación
  $('v').style.opacity = win(t, T.v, T.vEnd, 0.3)
  let counts = [0, 0, 0]
  let lastT = -9
  let lastI = -1
  for (const [vt, i] of VOTES) if (t >= vt) { counts[i]++; lastT = vt; lastI = i }
  const total = counts[0] + counts[1] + counts[2]
  const shown = Math.max(1, total)
  $('vcT').textContent = `${shown} ${shown === 1 ? 'voto' : 'votos'}`
  $('cdT').textContent = fmt(14 * 60 + 32 - Math.max(0, t - T.v) * 1.1)
  const leader = counts.indexOf(Math.max(...counts))
  for (let i = 0; i < 3; i++) {
    $('n' + i).textContent = String(counts[i])
    // anchura animada hacia el valor actual
    let w = counts[i] / 7
    if (i === lastI) w = lerp((counts[i] - 1) / 7, counts[i] / 7, easeOut(seg(t, lastT, lastT + 0.35)))
    $('b' + i).style.width = `${w * 100}%`
    const lead = total >= 4 && i === leader
    $('b' + i).style.background = lead ? '#8a6a4f' : '#b8a58f'
    $('w' + i).style.opacity = lead ? 1 : 0
    const pulse = i === lastI ? Math.max(0, 1 - (t - lastT) / 0.3) : 0
    const el = $('l2_' + i)
    const a = easeOut(seg(t, T.v + 0.15 + i * 0.12, T.v + 0.55 + i * 0.12))
    el.style.opacity = a
    el.style.transform = `translateY(${(1 - a) * 20}px) scale(${1 + pulse * 0.02})`
    el.style.borderColor = lead ? '#8a6a4f' : 'rgba(21,20,15,.1)'
  }

  // Resultado
  $('r').style.opacity = win(t, T.r, T.rEnd, 0.3)
  const tap2 = 11.7
  const bt = $('me')
  bt.style.transform = `scale(${1 - 0.05 * Math.max(0, 1 - Math.abs(t - tap2) / 0.16)})`
  const note = easeOut(seg(t, tap2 + 0.1, tap2 + 0.5))
  $('note').style.opacity = note
  $('note').style.transform = `translateY(${(1 - note) * 14}px)`
  $('rBig').style.transform = `translateY(${(1 - easeOut(seg(t, T.r, T.r + 0.5))) * 20}px)`

  // Frase y cierre
  const dec = easeOut(seg(t, T.dec, T.dec + 0.4)) * (1 - seg(t, T.decEnd - 0.2, T.decEnd))
  $('dec').style.opacity = dec
  $('dec').firstElementChild.style.transform = `translateY(${(1 - dec) * 20}px)`
  const end = $('end')
  end.style.opacity = easeOut(seg(t, T.end, T.end + 0.4))
  for (const [cls, d] of [['w', 0], ['p', 0.4], ['u', 0.65], ['s', 0.8]]) {
    const el = end.querySelector(`.${cls}`)
    const a = easeOut(seg(t, T.end + d, T.end + d + 0.45))
    el.style.opacity = a
    el.style.transform = `translateY(${(1 - a) * 18}px)`
  }

  // Subtítulos
  let cap = ['', 0]
  if (t < 4.9) cap = ['Tres looks <i>con tu ropa.</i>', win(t, 2.9, 4.7, 0.3)]
  else if (t < 6.4) cap = ['Pregunta <i>a tu círculo.</i>', win(t, 5.5, 6.35, 0.25)]
  else if (t < 10.6) cap = ['Votan <i>de un toque.</i>', win(t, 6.9, 10.4, 0.3)]
  caption(cap[0], cap[1])

  // Cursor
  let cx = 288, cy = 980, ca = 0, tap = 0
  if (t >= 3.9 && t < 5.6) {
    const c = cursorAt(t, [[4.0, [470, 1000]], [4.85, [288, 690]], [tapT, [288, 690], true], [5.5, [288, 690]]])
    cx = c.x; cy = c.y; tap = c.tap
    ca = easeOut(seg(t, 3.9, 4.1)) * (1 - seg(t, 5.25, 5.6))
  } else if (t >= 10.8 && t < 12.5) {
    const c = cursorAt(t, [[10.9, [470, 1000]], [11.6, [288, 566]], [tap2, [288, 566], true], [12.4, [288, 566]]])
    cx = c.x; cy = c.y; tap = c.tap
    ca = easeOut(seg(t, 10.8, 11.0)) * (1 - seg(t, 12.1, 12.5))
  }
  const cur = $('cursor')
  cur.style.left = `${cx}px`
  cur.style.top = `${cy}px`
  cur.style.opacity = ca * 0.95
  cur.style.transform = `scale(${1 - tap * 0.28})`
}

window.render = render
window.DURATION = T.total
