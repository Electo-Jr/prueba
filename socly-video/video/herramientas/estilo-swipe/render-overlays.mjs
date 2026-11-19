// Fotogramas PNG con fondo transparente de overlays.html (móvil del swipe y tarjetas del duelo).
// Uso: node render-overlays.mjs <carpetaSalida> <carpetaFotogramasGrabacion> <t0> <t1> <fps> <plan.json>
// Las imágenes se sacan por «t» del vídeo final (los tiempos del plan los pone go2.py); el nombre es s_0000.png desde t0.
import { spawn } from 'node:child_process'
import { mkdirSync, writeFileSync, readFileSync, rmSync } from 'node:fs'
import { pathToFileURL, fileURLToPath } from 'node:url'
import path from 'node:path'

const here = path.dirname(fileURLToPath(import.meta.url))
const [outDir, recDir, t0s, t1s, fpsArg, planPath] = process.argv.slice(2)
const plan = JSON.parse(readFileSync(planPath, 'utf-8'))
const t0 = Number(t0s)
const t1 = Number(t1s)
const fps = Number(fpsArg || 30)
mkdirSync(outDir, { recursive: true })

const profile = path.join(here, 'chrome-profile')
try { rmSync(profile, { recursive: true, force: true }) } catch {}
const proc = spawn('/usr/bin/google-chrome', [
  '--headless=new', '--remote-debugging-port=9353', `--user-data-dir=${profile}`, '--hide-scrollbars',
  '--no-first-run', '--allow-file-access-from-files', '--font-render-hinting=none', 'about:blank',
], { stdio: 'ignore' })
const sleep = (ms) => new Promise((r) => setTimeout(r, ms))
let target
for (let i = 0; i < 60 && !target; i++) {
  try { target = (await (await fetch('http://127.0.0.1:9353/json')).json()).find((x) => x.type === 'page')?.webSocketDebuggerUrl } catch {}
  await sleep(250)
}
const ws = new WebSocket(target)
await new Promise((r) => (ws.onopen = r))
let id = 0
const pending = new Map()
ws.onmessage = (m) => { const msg = JSON.parse(m.data); if (msg.id && pending.has(msg.id)) { pending.get(msg.id)(msg); pending.delete(msg.id) } }
const send = (method, params = {}) => new Promise((res) => { const i = ++id; pending.set(i, res); ws.send(JSON.stringify({ id: i, method, params })) })

await send('Page.enable')
await send('Emulation.setDeviceMetricsOverride', { width: 1080, height: 1920, deviceScaleFactor: 1, mobile: false })
if (process.env.OPAQUE !== '1') await send('Emulation.setDefaultBackgroundColorOverride', { color: { r: 0, g: 0, b: 0, a: 0 } })
await send('Page.navigate', { url: pathToFileURL(path.join(here, process.env.PAGE || 'overlays.html')).href })
await sleep(1200)
await send('Runtime.evaluate', { expression: 'document.fonts.ready.then(() => 1)', awaitPromise: true })
await sleep(300)
await send('Runtime.evaluate', { expression: `window.REC_DIR = ${JSON.stringify(pathToFileURL(recDir).href + '/')}; window.PLAN = ${JSON.stringify(plan)}; 1` })

let n = 0
for (let i = 0; t0 + i / fps <= t1 + 1e-9; i++) {
  const t = t0 + i / fps
  const r = await send('Runtime.evaluate', {
    expression: `render(${t}); new Promise((res) => { const im = document.getElementById('rec'); if (!im || im.complete) res(1); else im.onload = () => res(1); setTimeout(() => res(1), 400) })`,
    awaitPromise: true,
  })
  if (r.result?.exceptionDetails) { console.log(JSON.stringify(r.result.exceptionDetails).slice(0, 400)); break }
  const shot = await send('Page.captureScreenshot', { format: 'png', fromSurface: true })
  if (!shot.result) { console.log('captura fallida en t=' + t, JSON.stringify(shot).slice(0, 300)); break }
  writeFileSync(path.join(outDir, `s_${String(n).padStart(4, '0')}.png`), Buffer.from(shot.result.data, 'base64'))
  n++
}
console.log('fotogramas:', n)
ws.close()
proc.kill()
await sleep(1500)
try { rmSync(profile, { recursive: true, force: true }) } catch { /* Chrome aún suelta la carpeta: no importa */ }
