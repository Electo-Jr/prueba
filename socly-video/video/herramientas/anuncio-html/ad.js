// Anuncio de Socly Style: todo es una función del tiempo, así que cada fotograma se puede dibujar suelto.
const $ = (s) => document.querySelector(s);
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const lerp = (a, b, x) => a + (b - a) * x;
const inOut = (x) => (x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2);
const out = (x) => 1 - Math.pow(1 - x, 3);
const back = (x) => { const c = 1.7; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); };
const prog = (t, a, b) => clamp((t - a) / (b - a));
// ventana con entrada y salida suaves
const win = (t, a, b, fi = 0.3, fo = 0.3) => clamp((t - a) / fi) * clamp((b - t) / fo);

// ---- datos ----
const LOOKS = [
  { title: 'Jersey beis y pantalón marino', pct: 90, bar: 90, items: [['👕', 0], ['👖', 0], ['👞', 0]], side: ['👔'] },
  { title: 'Polo oliva y pantalón beis', pct: 88, bar: 84, items: [['👕', 80], ['👖', 25], ['👟', 0]], side: [] },
  { title: 'Sudadera blanca y chinos', pct: 87, bar: 78, items: [['🧥', 200], ['👖', 25], ['👞', 0]], side: ['🧣'] },
];
const lookEls = LOOKS.map((L) => {
  const d = document.createElement('div');
  d.className = 'look';
  const pos = [[169, 4, 112], [169, 116, 126], [169, 262, 84]];
  L.items.forEach(([e, hue], i) => {
    const s = document.createElement('span');
    s.className = 'em'; s.textContent = e;
    s.style.cssText = `left:${pos[i][0]}px;top:${pos[i][1]}px;font-size:${pos[i][2]}px;transform:translateX(-50%);filter:hue-rotate(${hue}deg) drop-shadow(0 8px 8px rgba(40,30,10,.25))`;
    d.appendChild(s);
  });
  L.side.forEach((e) => {
    const s = document.createElement('span');
    s.className = 'em'; s.textContent = e;
    s.style.cssText = 'left:268px;top:150px;font-size:84px;transform:translateX(-50%)';
    d.appendChild(s);
  });
  $('#looks').appendChild(d);
  return d;
});

const CHIPS = ['Trabajo', 'Diario', 'Cita', 'Deporte', 'Fiesta'];
CHIPS.forEach((c) => {
  const e = document.createElement('span');
  e.className = 'pill'; e.textContent = c; e.dataset.c = c;
  $('#chips').appendChild(e);
});

const MEM = [['🧔', 'Marcos', 'te deja ver su ropa'], ['👩', 'Sofía', 'te deja ver su ropa y vestirle'], ['👩‍🦰', 'Lucía', 'te deja ver su ropa']];
MEM.forEach(([a, n, p], i) => {
  const d = document.createElement('div');
  d.style.cssText = 'display:flex;align-items:center;gap:14px;padding:12px 14px;margin-bottom:10px;background:#fffdf8;border:1px solid rgba(21,20,15,.08);border-radius:18px;box-shadow:0 6px 16px rgba(20,18,12,.05)';
  d.innerHTML = `<span class="emo" style="width:46px;height:46px;border-radius:50%;background:#efe3d3;display:flex;align-items:center;justify-content:center;font-size:26px">${a}</span><span style="flex:1;font-family:'Instrument Serif';font-size:22px">${n}<br><span style="font:11px 'Courier New';opacity:.5">${p}</span></span><span style="background:#15140f;color:#fff;border-radius:999px;font:700 10px 'Courier New';padding:6px 10px">te vio</span>`;
  d.dataset.i = i;
  $('#mem').appendChild(d);
});

const VOTERS = ['👩', '🧔', '👨‍🦱', '👧'];
VOTERS.forEach((v) => {
  const s = document.createElement('span');
  s.className = 'emo';
  s.style.cssText = 'width:44px;height:44px;border-radius:50%;background:#efe3d3;border:2px solid #fff;display:flex;align-items:center;justify-content:center;font-size:24px;opacity:0';
  s.textContent = v;
  $('#voters').appendChild(s);
});

const BAG = ['👕', '👕', '👖', '👟', '🧥', '🩳', '🕶️', '👜', '⌚'];
BAG.forEach((v) => {
  const s = document.createElement('span');
  s.className = 'emo'; s.style.cssText = 'font-size:34px;opacity:0;display:inline-block'; s.textContent = v;
  $('#bagitems').appendChild(s);
});

const FLOATERS = [
  { t: 16.5, x: -190, y: -240, z: 110, html: '☀️ 20° Lisboa' },
  { t: 16.9, x: 60, y: -170, z: 140, html: '🧳 4 días' },
  { t: 17.3, x: -205, y: 190, z: 90, html: '✓ 9 prendas' },
  { t: 17.7, x: 20, y: 285, z: 130, html: '👟 Sin repetir nada' },
];
FLOATERS.forEach((f) => {
  const d = document.createElement('div');
  d.className = 'fl'; d.innerHTML = `<span class="emo">${f.html.slice(0, 2)}</span>${f.html.slice(2)}`;
  d.style.opacity = 0; $('#floaters').appendChild(d); f.el = d;
});

const FLAT = [
  ['🧥', 36, 120, 150, -15], ['👖', 350, 70, 130, 14], ['👟', 30, 760, 120, 20], ['🧢', 420, 780, 110, -20],
  ['⌚', 450, 440, 80, 10], ['🕶️', 20, 450, 90, -10], ['👜', 270, 860, 120, 8], ['👕', 150, 30, 120, 12], ['🧣', 150, 700, 110, -8],
];
FLAT.forEach(([e, x, y, s, r], i) => {
  const d = document.createElement('div');
  d.className = 'em'; d.textContent = e; d.dataset.i = i;
  d.style.cssText = `left:${x}px;top:${y}px;font-size:${s}px;opacity:0`;
  d.dataset.r = r; d.dataset.y = y;
  $('#flat').appendChild(d);
});

$('#endbox').style.cssText = 'left:104px;width:368px;top:380px;height:112px';

const SCREENS = {
  home: [3.2, 7.5], ask: [7.2, 10.6], circle: [10.3, 13.4], vote: [13.1, 15.6], bag: [15.7, 19.8],
};
const HEAD = [
  [4.55, 7.2, 'Elige<i>.</i>'], [7.55, 10.3, 'Pregunta<i>.</i>'], [10.6, 13.1, 'Presta<i>.</i>'],
  [13.35, 15.1, 'Vota<i>.</i>'], [16.0, 19.4, 'Viaja<i>.</i>'], [19.9, 22.2, 'Tu <i>estilo</i>.'],
];

// ---- cámara del móvil: [t, escala, rotX, rotY, rotZ, x, y] ----
const CAM = [
  [2.9, 0.42, 58, 0, -8, 0, -60], [4.5, 1.0, 6, -12, 0, 0, 20], [5.9, 1.05, 4, 8, 0, 0, 10],
  [7.3, 1.05, 4, 12, 0, 0, 10], [7.8, 1.0, 6, 0, 0, 0, 20], [9.0, 1.04, 4, -8, 0, 0, 8], [10.3, 1.04, 4, -8, 0, 0, 8],
  [10.9, 1.45, 8, 14, -2, -30, -120], [13.1, 1.5, 6, -10, 0, 10, -120],
  [13.5, 1.1, 5, 6, 0, 0, 20], [15.3, 1.15, 4, -6, 0, 0, 20],
  [16.0, 0.9, 6, 10, 0, 0, 40], [17.8, 0.95, 4, -12, 0, 0, 30], [19.6, 1.0, 4, 10, 0, 0, 30],
  [20.05, 1.0, 0, 0, 0, 0, 0],
];
function cam(t) {
  if (t <= CAM[0][0]) return CAM[0].slice(1);
  for (let i = 0; i < CAM.length - 1; i++) {
    const a = CAM[i], b = CAM[i + 1];
    if (t >= a[0] && t <= b[0]) {
      const k = inOut(prog(t, a[0], b[0]));
      return a.slice(1).map((v, j) => lerp(v, b[j + 1], k));
    }
  }
  return CAM[CAM.length - 1].slice(1);
}

function render(t) {
  // fondo vivo
  $('#glow').style.transform = `translate(${Math.sin(t * 0.6) * 60}px,${Math.cos(t * 0.45) * 50 + (t > 15 ? 120 : 0)}px) scale(${1 + 0.12 * Math.sin(t)})`;
  $('#glow').style.opacity = t < 1.2 ? 0 : 1;

  // 1) orbe -> logotipo
  const orb = $('#orb');
  const o = out(prog(t, 0.15, 1.6));
  const sz = lerp(6, 1000, o * o);
  orb.style.width = orb.style.height = sz + 'px';
  orb.style.opacity = t < 0.15 ? 0 : t < 1.6 ? 1 : 1 - prog(t, 1.6, 2.2);
  const lg = $('#logo');
  const lin = prog(t, 1.35, 2.1), lout = prog(t, 2.7, 3.1);
  lg.style.opacity = lin * (1 - lout);
  lg.style.filter = `blur(${(1 - lin) * 18 + lout * 12}px)`;
  lg.style.transform = `scale(${lerp(0.92, 1.0, out(lin)) + lout * 0.06})`;

  // 2) flat-lay
  const flat = $('#flat');
  flat.style.opacity = prog(t, 2.8, 3.15) * (1 - prog(t, 4.05, 4.6));
  document.querySelectorAll('#flat .em').forEach((e) => {
    const i = +e.dataset.i, d = 2.9 + i * 0.07;
    const k = back(prog(t, d, d + 0.55));
    e.style.opacity = clamp((t - d) / 0.15);
    e.style.transform = `translateY(${(1 - k) * -340}px) rotate(${+e.dataset.r * k}deg) scale(${lerp(0.4, 1, k)})`;
  });

  // 3) móvil
  const c = cam(t);
  const rig = $('#rig');
  const SCALE = c[0] * (c[0] > 0.8 ? 1.18 : 1);
  rig.style.transform = `translate3d(${c[4]}px,${c[5]}px,0) rotateX(${c[1]}deg) rotateY(${c[2]}deg) rotateZ(${c[3]}deg) scale(${SCALE})`;
  const phone = $('#phone');
  const pin = prog(t, 2.9, 3.3);
  const pout = 1 - prog(t, 19.6, 20.1);
  phone.style.opacity = pin * pout;
  // Algunas pantallas ocupan toda la zona; el texto va por encima.
  for (const [k, [a, b]] of Object.entries(SCREENS)) {
    $('#s-' + k).style.opacity = win(t, a, b, 0.3, 0.3);
  }

  // titulares
  let hd = '', ho = 0, hy = 0;
  for (const [a, b, txt] of HEAD) {
    if (t >= a && t <= b) { hd = txt; ho = win(t, a, b, 0.35, 0.3); hy = (1 - out(prog(t, a, a + 0.5))) * 24; }
  }
  const head = $('#head');
  head.innerHTML = hd; head.style.opacity = ho; head.style.transform = `translateY(${hy}px)`;

  // ---- Home ----
  {
    const lt = t - 4.3;
    const idx = lt < 1.5 ? 0 : lt < 2.7 ? 1 : 2;
    const sw = idx === 0 ? 1 : idx === 1 ? prog(lt, 1.5, 1.9) : prog(lt, 2.7, 3.1);
    lookEls.forEach((el, i) => {
      let op = 0, x = 0;
      if (i === idx) { op = out(sw); x = (1 - out(sw)) * 50; }
      else if (i === idx - 1) { op = 1 - out(sw); x = -out(sw) * 50; }
      el.style.opacity = op; el.style.transform = `translateX(${x}px)`;
    });
    const L = LOOKS[idx];
    $('#lk-title').textContent = L.title;
    $('#lk-pct').innerHTML = `${L.pct}% <span style="font:10px Inter;opacity:.6">encaja</span>`;
    $('#lk-bar').style.width = L.bar + '%';
    document.querySelectorAll('#dots .dot').forEach((d, i) => d.classList.toggle('on', i === idx));
  }

  // ---- ¿Qué me pongo? ----
  {
    const lt = t - 7.2;
    const text = 'Una cita esta noche';
    const n = Math.floor(clamp((lt - 0.7) / 1.2) * text.length);
    $('#typed').textContent = text.slice(0, n);
    $('#caret').style.opacity = Math.floor(t * 3) % 2 ? 0.2 : 1;
    document.querySelectorAll('#chips .pill').forEach((p) => {
      const on = p.dataset.c === 'Cita' && lt > 0.35;
      p.style.background = on ? '#15140f' : 'transparent';
      p.style.color = on ? '#fff' : '';
    });
    const r = out(prog(lt, 2.1, 2.7));
    const res = $('#ask-res');
    res.style.opacity = r; res.style.transform = `translateY(${(1 - r) * 60}px)`;
  }

  // ---- Círculo ----
  {
    const lt = t - 10.3;
    document.querySelectorAll('#mem > div').forEach((d, i) => {
      const k = out(prog(lt, 0.1 + i * 0.18, 0.55 + i * 0.18));
      d.style.opacity = k; d.style.transform = `translateX(${(1 - k) * 40}px)`;
    });
    const r = out(prog(lt, 1.0, 1.55));
    const req = $('#req');
    req.style.opacity = r; req.style.transform = `translateY(${(1 - r) * 80}px)`;
    const ok = prog(lt, 2.0, 2.3);
    const b = $('#rq-btn');
    b.textContent = ok > 0.5 ? '✓ Prestada hasta el sábado' : 'Aceptar';
    b.style.background = ok > 0.5 ? '#c9a178' : '';
    b.style.color = ok > 0.5 ? '#15140f' : '';
    b.style.transform = `scale(${1 - Math.sin(clamp((lt - 1.95) / 0.3) * Math.PI) * 0.06})`;
  }

  // ---- ¿Cuál me pongo? ----
  {
    const lt = t - 13.1;
    ['#vA', '#vB'].forEach((id, i) => {
      const k = out(prog(lt, i * 0.15, 0.5 + i * 0.15));
      $(id).style.opacity = k; $(id).style.transform = `translateY(${(1 - k) * 40}px)`;
    });
    const votes = [[0, 'B'], [0.5, 'B'], [0.9, 'A'], [1.3, 'B']];
    const sp = $('#voters').children;
    let a = 0, bb = 0;
    votes.forEach(([vt, who], i) => {
      const k = back(prog(lt, 0.5 + vt, 0.8 + vt));
      sp[i].style.opacity = clamp((lt - 0.5 - vt) / 0.1);
      sp[i].style.transform = `scale(${lerp(0.3, 1, k)})`;
      if (lt > 0.6 + vt) { who === 'A' ? a++ : bb++; }
    });
    $('#vbA').style.width = (a / 4) * 100 + '%';
    $('#vbB').style.width = (bb / 4) * 100 + '%';
    const win2 = out(prog(lt, 1.7, 2.1));
    $('#vwin').style.opacity = win2;
    $('#vB').style.boxShadow = win2 > 0 ? `0 0 0 2px #c9a178, 0 12px 40px rgba(201,161,120,${0.5 * win2})` : '';
  }

  // ---- Maleta ----
  {
    const lt = t - 15.7;
    const text = 'Lisboa';
    $('#bagtxt').textContent = text.slice(0, Math.floor(clamp((lt - 0.3) / 0.6) * text.length));
    const d = lerp(2, 4, inOut(prog(lt, 0.9, 1.5)));
    $('#bagdays').textContent = Math.round(d);
    const fillW = ((d - 1) / 13) * 100;
    $('#bagfill').style.width = fillW + '%';
    $('#bagknob').style.left = `calc(${fillW}% - 10px)`;
    $('#bagbtn').style.transform = `scale(${1 - Math.sin(clamp((lt - 1.7) / 0.3) * Math.PI) * 0.06})`;
    const s = back(prog(lt, 1.95, 2.45));
    $('#suit').style.opacity = clamp((lt - 1.95) / 0.2);
    $('#suit').style.transform = `scale(${lerp(0.3, 1, s)})`;
    document.querySelectorAll('#bagitems .emo').forEach((e, i) => {
      const k = back(prog(lt, 2.3 + i * 0.12, 2.7 + i * 0.12));
      e.style.opacity = clamp((lt - 2.3 - i * 0.12) / 0.1);
      e.style.transform = `translateY(${(1 - k) * -120}px) scale(${lerp(0.3, 1, k)})`;
    });
    $('#bagsum').style.opacity = out(prog(lt, 3.5, 3.9));
  }

  // piezas flotantes alrededor del móvil
  FLOATERS.forEach((f, i) => {
    const k = back(prog(t, f.t, f.t + 0.45)) * (1 - prog(t, 19.1, 19.55));
    const bob = Math.sin(t * 1.6 + i * 1.7) * 8;
    f.el.style.opacity = clamp(k);
    f.el.style.transform = `translate3d(${f.x}px,${f.y + bob}px,${f.z}px) scale(${clamp(k, 0, 1.1)}) rotateY(${Math.sin(t + i) * 8}deg)`;
  });

  // ---- destello ----
  {
    const fl = Math.sin(clamp((t - 15.1) / 0.9) * Math.PI);
    $('#flare').style.opacity = fl;
    $('#flare').style.transform = `rotate(${(t - 15) * 25}deg) scale(${lerp(0.5, 1.4, prog(t, 15.1, 16))})`;
    $('#white').style.opacity = Math.pow(Math.sin(clamp((t - 15.25) / 0.7) * Math.PI), 2) * 0.85;
  }

  // ---- tarjeta 3D ----
  {
    const card = $('#card3d');
    const a = prog(t, 19.7, 20.3), z = 1 - prog(t, 22.0, 22.5);
    card.style.opacity = a * z;
    const ry = lerp(-85, 12, out(prog(t, 19.7, 21.6))) + Math.sin(t * 1.2) * 4;
    const rx = 8 + Math.sin(t * 0.9) * 3;
    const sc = lerp(0.8, 1.12, out(prog(t, 19.7, 22.2)));
    card.style.transform = `rotateX(${rx}deg) rotateY(${ry}deg) scale(${sc})`;
    $('#shine').style.transform = `translateX(${lerp(-70, 70, prog(t, 20.4, 22.0))}%)`;
  }

  // ---- final ----
  {
    const eb = out(prog(t, 22.3, 23.0));
    $('#endbox').style.opacity = eb;
    $('#endbox').style.transform = `scale(${lerp(0.9, 1, eb)})`;
    const ew = prog(t, 22.6, 23.2);
    $('#endword').style.opacity = ew; $('#endword').style.filter = `blur(${(1 - ew) * 10}px)`;
    const tg = out(prog(t, 23.2, 23.8));
    $('#tag').style.opacity = tg; $('#tag').style.transform = `translateY(${(1 - tg) * 16}px)`;
    const dt = out(prog(t, 23.8, 24.4));
    $('#date').style.opacity = dt; $('#date').style.transform = `translateY(${(1 - dt) * 20}px)`;
  }
  // el fondo se oscurece al salir del flat-lay y todo se desvanece en los últimos fotogramas
  $('#stage').style.opacity = 1 - prog(t, 24.55, 24.9);
}
window.render = render;
render(0);
