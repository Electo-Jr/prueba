// «¿Te vas de viaje?»: primero la función «La maleta» y después la maleta de cabina en time lapse. 576x1024 CSS px (x1.875 = 1080x1920).
// Fotos propias ya orientadas y alineadas (sin censura, a petición del dueño; las censuradas están en ..\..\fotos-propias\maleta\censuradas\) en ..\..\fotos-propias\maleta\procesadas\.
const $ = (id) => document.getElementById(id)
const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v))
const seg = (t, a, b) => clamp((t - a) / (b - a))
const easeOut = (x) => 1 - Math.pow(1 - x, 3)
const easeInOut = (x) => (x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2)
const lerp = (a, b, x) => a + (b - a) * x
const win = (t, a, b, f = 0.3) => easeOut(seg(t, a, a + f)) * (1 - seg(t, b - f, b))

// Orden: gancho -> app (adónde y cuántos días) -> maleta en time lapse -> cierre.
const T = { hookOut: 1.5, app: 1.8, appEnd: 7.0, sm: 7.0, stampIn: 9.95, smEnd: 13.0, end: 13.0, total: 15.4 }
const DIR = '../../fotos-propias/maleta/procesadas/'
const NAMES = ['Maleta vacía', '+ Chinos verdes', '+ Camiseta clara', '+ Camiseta blanca', '+ Sudadera gris',
  'Todo en su sitio', '+ Jersey blanco', '+ Pantalón gris', '+ Camiseta azul marina']
// Time lapse: la vacía dura medio segundo y el resto, un corte cada 0,3 s.
const CUTS = [T.sm]
for (let i = 1; i < 9; i++) CUTS.push(T.sm + 0.5 + (i - 1) * 0.3)
$('ph').innerHTML = NAMES.map((_, i) => `<img id="im${i}" src="${DIR}0${i + 1}.jpg">`).join('')

const TINTS = ['#e8dfcf', '#dcd3c2', '#efe6d6', '#d9cdb8']
const CARDS = ['👕', '👖', '🧥', '👟']
$('cards').innerHTML = CARDS.map((e, i) => `<div class="cd" id="cd${i}" style="left:${i * 124}px;background:${TINTS[i]}"><div class="e emo">${e}</div></div>`).join('')
const DAYS = [['Día 1', '👕👖'], ['Día 2', '👔👖'], ['Día 3', '🧥👟'], ['Día 4', '👕🩳']]
$('rows').innerHTML = DAYS.map((d, i) => `<div class="row" id="rw${i}" style="top:${170 + i * 54}px"><span>${d[0]}</span><span class="e emo">${d[1]}</span></div>`).join('')

function cursorAt(t, keys) {
  let p = keys[0], n = keys[keys.length - 1]
  for (let i = 0; i < keys.length - 1; i++) if (t >= keys[i][0] && t < keys[i + 1][0]) { p = keys[i]; n = keys[i + 1]; break }
  if (t >= keys[keys.length - 1][0]) return { x: n[1][0], y: n[1][1], tap: 0 }
  const k = easeInOut(seg(t, p[0], n[0] - 0.08))
  const tap = n[2] ? Math.max(0, 1 - Math.abs(t - n[0]) / 0.16) : 0
  return { x: lerp(p[1][0], n[1][0], k), y: lerp(p[1][1], n[1][1], k), tap }
}

function render(t) {
  // Gancho
  const hook = $('hook')
  const hOut = seg(t, T.hookOut, T.hookOut + 0.3)
  hook.style.opacity = 1 - hOut
  const hIn = easeOut(seg(t, 0, 0.55))
  hook.firstElementChild.style.transform = `translateY(${(1 - hIn) * 30}px)`
  hook.firstElementChild.style.opacity = hIn

  // Stop-motion + sello
  const smOn = t >= T.sm - 0.02 && t < T.smEnd
  $('sm').style.opacity = smOn ? 1 : 0
  let idx = 0
  for (let i = 0; i < 9; i++) if (t >= CUTS[i]) idx = i
  const since = t - CUTS[idx]
  for (let i = 0; i < 9; i++) $('im' + i).style.display = i === idx ? 'block' : 'none'
  const pop = 1 + 0.02 * (1 - easeOut(seg(since, 0, 0.14)))
  $('ph').firstElementChild && ($('ph').style.transform = `scale(${pop})`)
  $('cn').textContent = `${idx + 1} de 9`
  $('chipT').textContent = NAMES[idx]
  const doneA = easeOut(seg(t, T.stampIn, T.stampIn + 0.35))
  $('chip').style.opacity = 1 - doneA
  $('done').style.opacity = doneA
  $('done').style.transform = `translateY(${(1 - doneA) * 16}px)`
  const st = easeOut(seg(t, T.stampIn, T.stampIn + 0.25))
  $('stamp').style.opacity = st
  $('stamp').style.transform = `rotate(-6deg) scale(${1.25 - 0.25 * st})`
  // la escena sm sale con fundido breve al pasar a la app
  if (smOn) $('sm').style.opacity = Math.min(easeOut(seg(t, T.sm, T.sm + 0.2)), 1 - seg(t, T.smEnd - 0.3, T.smEnd))

  // App
  const appA = t >= T.app - 0.01 && t < T.appEnd ? easeOut(seg(t, T.app, T.app + 0.3)) * (1 - seg(t, T.appEnd - 0.25, T.appEnd)) : 0
  $('app').style.opacity = appA
  const tap = T.app + 1.25
  const bt = Math.max(0, 1 - Math.abs(t - tap) / 0.16)
  $('btn').style.transform = `scale(${1 - 0.05 * bt})`
  const resA = easeOut(seg(t, tap + 0.1, tap + 0.5))
  $('res').style.opacity = resA
  for (let i = 0; i < 4; i++) {
    const a = easeOut(seg(t, tap + 0.3 + i * 0.12, tap + 0.6 + i * 0.12))
    $('cd' + i).style.opacity = a
    $('cd' + i).style.transform = `scale(${0.7 + 0.3 * a})`
    const b = easeOut(seg(t, tap + 0.9 + i * 0.22, tap + 1.2 + i * 0.22))
    $('rw' + i).style.opacity = b
    $('rw' + i).style.transform = `translateY(${(1 - b) * 12}px)`
  }
  // Subtítulo de la app
  const cap = $('cap')
  const capA = win(t, tap + 1.8, T.appEnd - 0.1, 0.3)
  if (cap.dataset.h !== 'x') { cap.innerHTML = 'Te dice qué meter <i>y qué te pones.</i>'; cap.dataset.h = 'x' }
  cap.style.opacity = capA
  cap.style.transform = `translateY(${(1 - capA) * 18}px)`

  // Cierre
  const end = $('end')
  end.style.opacity = easeOut(seg(t, T.end, T.end + 0.4))
  for (const [cls, d] of [['w', 0], ['u', 0.4], ['s', 0.55]]) {
    const el = end.querySelector(`.${cls}`)
    const a = easeOut(seg(t, T.end + d, T.end + d + 0.45))
    el.style.opacity = a
    el.style.transform = `translateY(${(1 - a) * 18}px)`
  }

  // Cursor
  let cx = 288, cy = 980, ca = 0, ctap = 0
  if (t >= tap - 0.65 && t < tap + 0.85) {
    const c = cursorAt(t, [[tap - 0.55, [470, 640]], [tap - 0.1, [288, 436]], [tap, [288, 436], true], [tap + 0.65, [288, 436]]])
    cx = c.x; cy = c.y; ctap = c.tap
    ca = easeOut(seg(t, tap - 0.65, tap - 0.45)) * (1 - seg(t, tap + 0.45, tap + 0.85))
  }
  const cur = $('cursor')
  cur.style.left = `${cx}px`; cur.style.top = `${cy}px`
  cur.style.opacity = ca * 0.95
  cur.style.transform = `scale(${1 - ctap * 0.28})`
}
window.render = render
window.DURATION = T.total
