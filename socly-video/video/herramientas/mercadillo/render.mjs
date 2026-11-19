// Uso: node render.mjs <carpetaSalida> <escala> <t0> <t1> <fps>   |   node render.mjs <carpeta> <escala> t:1.5,3.2,7
import { spawn } from 'node:child_process';
import { mkdirSync, writeFileSync, rmSync } from 'node:fs';
import { pathToFileURL, fileURLToPath } from 'node:url';
import path from 'node:path';

const here = path.dirname(fileURLToPath(import.meta.url));
const [outDir, scaleArg, a, b, c] = process.argv.slice(2);
const scale = Number(scaleArg || 1);
let times;
if (a && a.startsWith('t:')) times = a.slice(2).split(',').map(Number);
else {
  const t0 = Number(a), t1 = Number(b), fps = Number(c);
  times = [];
  for (let i = 0; t0 + i / fps <= t1 + 1e-9; i++) times.push(t0 + i / fps);
}
mkdirSync(outDir, { recursive: true });

const chrome = '/usr/bin/google-chrome';
const profile = path.join(here, 'chrome-profile');
rmSync(profile, { recursive: true, force: true });
const proc = spawn(chrome, [
  '--headless=new', '--remote-debugging-port=9333', `--user-data-dir=${profile}`, '--hide-scrollbars',
  '--no-first-run', '--disable-gpu-vsync', '--allow-file-access-from-files', '--font-render-hinting=none', 'about:blank',
], { stdio: 'ignore' });

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
async function getTarget() {
  for (let i = 0; i < 60; i++) {
    try {
      const list = await (await fetch('http://127.0.0.1:9333/json')).json();
      const page = list.find((x) => x.type === 'page');
      if (page) return page.webSocketDebuggerUrl;
    } catch { /* aún arrancando */ }
    await sleep(250);
  }
  throw new Error('Chrome no arranca');
}
const ws = new WebSocket(await getTarget());
await new Promise((r) => (ws.onopen = r));
let id = 0;
const pending = new Map();
ws.onmessage = (m) => {
  const msg = JSON.parse(m.data);
  if (msg.id && pending.has(msg.id)) { pending.get(msg.id)(msg); pending.delete(msg.id); }
};
const send = (method, params = {}) => new Promise((res) => { const i = ++id; pending.set(i, res); ws.send(JSON.stringify({ id: i, method, params })); });

await send('Page.enable');
await send('Emulation.setDeviceMetricsOverride', { width: 576, height: 1024, deviceScaleFactor: scale, mobile: false });
await send('Page.navigate', { url: pathToFileURL(path.join(here, process.env.PAGE || 'ad.html')).href });
await sleep(1500);
const ready = await send('Runtime.evaluate', { expression: 'document.fonts.ready.then(()=>document.fonts.size)', awaitPromise: true });
console.log('fuentes cargadas:', ready.result?.result?.value);
await sleep(500);

let n = 0;
for (const t of times) {
  const r = await send('Runtime.evaluate', { expression: `render(${t}); 1` });
  if (r.result?.exceptionDetails) { console.log(JSON.stringify(r.result.exceptionDetails).slice(0, 500)); break; }
  const shot = await send('Page.captureScreenshot', { format: 'jpeg', quality: 93 });
  const name = a.startsWith('t:') ? `t_${t.toFixed(2)}.jpg` : `f_${String(n).padStart(4, '0')}.jpg`;
  writeFileSync(path.join(outDir, name), Buffer.from(shot.result.data, 'base64'));
  n++;
}
console.log('fotogramas:', n);
ws.close();
proc.kill();
