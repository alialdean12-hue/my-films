// «سرقة الموناليزا» — fast documentary edit: museum wall + spotlight, archive photo cards, kinetic Arabic type, paper/grid/mat backgrounds.
const W = 1080, H = 1920, AX = W / 2;
const cv = document.getElementById('c'); cv.width = W; cv.height = H; const g = cv.getContext('2d');
const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x)), lerp = (a, b, t) => a + (b - a) * t, seg = (t, a, b) => clamp((t - a) / (b - a));
const eo = t => 1 - Math.pow(1 - clamp(t), 3), eio = t => { t = clamp(t); return t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; };
const back = (t, s = 1.8) => { t = clamp(t) - 1; return 1 + t * t * ((s + 1) * t + s); };
const hash = n => { n = Math.sin(n * 127.1 + 311.7) * 43758.5453; return n - Math.floor(n); };
const RED = '#e0262f', CREAM = '#f4ecdc', YEL = '#ffd21f';

const VO = { l1: .3, l2: 7.4, l3: 13.1, l4: 18.1, l5: 22.7 };
const K = { year: 2.1, gone: 3.96, louvre: 6.54, gang: 8.5, strike: 9.6, worker: 10.16, same: 11.74, box: 13.94, two: 15.4, back: 18.68, famous: 20.6, made: 23.1, fame: 24.02 };
const CUT = [0, 2.0, 3.9, 7.3, 10.0, 13.0, 17.9, 22.5];
const DUR = 26.5; window.DUR = DUR;
const IMG = {};

// ---------- backgrounds ----------
function wall(t, lamp = 1) {
  const gr = g.createLinearGradient(0, 0, 0, H); gr.addColorStop(0, '#3a2a1c'); gr.addColorStop(.6, '#2a1d13'); gr.addColorStop(1, '#140d08'); g.fillStyle = gr; g.fillRect(0, 0, W, H);
  // wainscot panels
  g.strokeStyle = 'rgba(0,0,0,.35)'; g.lineWidth = 6;
  for (const [x, y, w, h] of [[90, 1330, 400, 380], [590, 1330, 400, 380], [90, 140, 900, 1080]]) { g.strokeRect(x, y, w, h); g.strokeStyle = 'rgba(255,220,170,.06)'; g.lineWidth = 2; g.strokeRect(x + 4, y + 4, w, h); g.strokeStyle = 'rgba(0,0,0,.35)'; g.lineWidth = 6; }
  g.fillStyle = '#120b06'; g.fillRect(0, 1790, W, 130);
  // picture light: brass bar + cone
  g.fillStyle = '#b8955a'; g.fillRect(AX - 90, 230, 180, 16); g.fillRect(AX - 6, 200, 12, 34);
  g.save(); g.globalCompositeOperation = 'lighter';
  const c = g.createRadialGradient(AX, 250, 10, AX, 700, 760); c.addColorStop(0, `rgba(255,214,150,${.55 * lamp})`); c.addColorStop(.45, `rgba(255,170,90,${.22 * lamp})`); c.addColorStop(1, 'rgba(0,0,0,0)');
  g.fillStyle = c; g.fillRect(0, 0, W, H); g.restore();
}
function paper(t, tint = '#ecebe6') {
  g.fillStyle = tint; g.fillRect(0, 0, W, H);
  for (let i = 0; i < 160; i++) { g.fillStyle = `rgba(0,0,0,${.02 + hash(i) * .03})`; g.fillRect(0, hash(i * 3.1) * H, W, 1 + hash(i * 7) * 2); }
  const v = g.createRadialGradient(AX, H / 2, 300, AX, H / 2, 1300); v.addColorStop(0, 'rgba(0,0,0,0)'); v.addColorStop(1, 'rgba(0,0,0,.35)'); g.fillStyle = v; g.fillRect(0, 0, W, H);
}
function grid(t, base, line, spot = true) {
  g.fillStyle = base; g.fillRect(0, 0, W, H);
  g.strokeStyle = line; g.lineWidth = 1.5;
  for (let x = 0; x < W; x += 60) { g.beginPath(); g.moveTo(x, 0); g.lineTo(x, H); g.stroke(); }
  for (let y = 0; y < H; y += 60) { g.beginPath(); g.moveTo(0, y); g.lineTo(W, y); g.stroke(); }
  if (spot) { g.save(); g.globalCompositeOperation = 'lighter'; const c = g.createRadialGradient(AX, 900, 50, AX, 900, 800); c.addColorStop(0, 'rgba(255,190,120,.35)'); c.addColorStop(1, 'rgba(0,0,0,0)'); g.fillStyle = c; g.fillRect(0, 0, W, H); g.restore(); }
  const v = g.createRadialGradient(AX, H / 2, 400, AX, H / 2, 1250); v.addColorStop(0, 'rgba(0,0,0,0)'); v.addColorStop(1, 'rgba(0,0,0,.6)'); g.fillStyle = v; g.fillRect(0, 0, W, H);
}
function dark(t) { g.fillStyle = '#0d0d0f'; g.fillRect(0, 0, W, H); for (let i = 0; i < 2200; i++) { g.fillStyle = `rgba(255,255,255,${hash(i + Math.floor(t * 12)) * .05})`; g.fillRect(hash(i * 1.3) * W, hash(i * 2.7) * H, 2, 2); } }

// ---------- photo card (white border, shadow, spring drop) ----------
function card(img, cx, cy, w, rot, p, { border = 16, frame = null, sepia = 0 } = {}) {
  if (p <= 0 || !img) return;
  const h = w * img.height / img.width, s = lerp(1.35, 1, back(p, 1.4)), a = clamp(p * 3);
  g.save(); g.globalAlpha = a; g.translate(cx, cy - (1 - eo(p)) * 120); g.rotate(rot * (1 + (1 - eo(p)) * 1.5)); g.scale(s, s);
  g.shadowColor = 'rgba(0,0,0,.55)'; g.shadowBlur = 40; g.shadowOffsetY = 22;
  if (frame) { // gilded frame
    const fw = 34; const fg = g.createLinearGradient(-w / 2, -h / 2, w / 2, h / 2); fg.addColorStop(0, '#6e4a17'); fg.addColorStop(.3, '#e6c06a'); fg.addColorStop(.6, '#9a6b24'); fg.addColorStop(1, '#f3d58a');
    g.fillStyle = fg; g.fillRect(-w / 2 - fw, -h / 2 - fw, w + fw * 2, h + fw * 2); g.shadowColor = 'transparent';
    g.strokeStyle = 'rgba(60,35,8,.8)'; g.lineWidth = 4; g.strokeRect(-w / 2 - 6, -h / 2 - 6, w + 12, h + 12);
  } else { g.fillStyle = CREAM; g.fillRect(-w / 2 - border, -h / 2 - border, w + border * 2, h + border * 2); g.shadowColor = 'transparent'; }
  if (sepia) g.filter = `sepia(${sepia}) contrast(1.1)`;
  g.drawImage(img, -w / 2, -h / 2, w, h); g.filter = 'none';
  g.restore();
}

// ---------- kinetic words ----------
function word(text, x, y, size, t, t0, { font = 'Lalezar', color = '#fff', italic = false, out = Infinity, rot = 0, shadow = true, align = 'center' } = {}) {
  if (t < t0 || t > out + .25) return null;
  const p = seg(t, t0, t0 + .28), q = 1 - seg(t, out, out + .25);
  g.save(); g.globalAlpha = clamp(p * 2) * q; g.translate(x, y + (1 - eo(p)) * 40); g.rotate(rot); const s = lerp(1.6, 1, back(p, 2)); g.scale(s, s);
  g.font = `${font === 'Amiri' ? '700 ' : ''}${size}px ${font}`; g.direction = 'rtl'; g.textAlign = align; g.textBaseline = 'middle';
  if (shadow) { g.shadowColor = 'rgba(0,0,0,.6)'; g.shadowBlur = 24; g.shadowOffsetY = 8; }
  g.fillStyle = color; g.fillText(text, 0, 0);
  const w = g.measureText(text).width; g.restore(); return w;
}
function tag(text, x, y, t, t0, rot = -.06) { // yellow name tag like a label maker
  if (t < t0) return; const p = back(seg(t, t0, t0 + .3), 2.2);
  g.save(); g.translate(x, y); g.rotate(rot); g.scale(p, p); g.font = '54px Lalezar'; g.direction = 'rtl'; g.textAlign = 'center'; g.textBaseline = 'middle';
  const w = g.measureText(text).width + 50; g.fillStyle = YEL; g.shadowColor = 'rgba(0,0,0,.4)'; g.shadowBlur = 16; g.fillRect(-w / 2, -42, w, 84); g.shadowColor = 'transparent';
  g.fillStyle = '#c4161c'; g.fillText(text, 0, 4); g.restore();
}
function underline(x0, x1, y, t, t0) { const p = eo(seg(t, t0, t0 + .3)); if (p <= 0) return; g.fillStyle = RED; g.fillRect(x1 - (x1 - x0) * p, y, (x1 - x0) * p, 16); }
function strike(x0, x1, y, t, t0) { const p = eo(seg(t, t0, t0 + .2)); if (p <= 0) return; g.save(); g.strokeStyle = RED; g.lineWidth = 18; g.lineCap = 'round'; g.beginPath(); g.moveTo(x1, y + 10); g.lineTo(lerp(x1, x0, p), y - 10 * p); g.stroke(); g.restore(); }

// ---------- trunk (drawn) ----------
function trunk(cx, cy, lid, t) {
  const w = 620, h = 300;
  g.save(); g.translate(cx, cy);
  g.shadowColor = 'rgba(0,0,0,.5)'; g.shadowBlur = 40; g.shadowOffsetY = 20;
  const wd = g.createLinearGradient(0, -h / 2, 0, h / 2); wd.addColorStop(0, '#7a4a22'); wd.addColorStop(1, '#3d220e'); g.fillStyle = wd; g.fillRect(-w / 2, -h / 2, w, h); g.shadowColor = 'transparent';
  g.strokeStyle = '#2a1608'; g.lineWidth = 3; for (let y = -h / 2 + 50; y < h / 2; y += 50) { g.beginPath(); g.moveTo(-w / 2, y); g.lineTo(w / 2, y); g.stroke(); }
  g.fillStyle = '#b9a27a'; for (const x of [-w / 2, w / 2 - 30]) g.fillRect(x, -h / 2, 30, h);
  g.fillStyle = '#d8c08a'; g.fillRect(-30, -h / 2 - 6, 60, 50);
  // lid rotates up from the back edge
  const a = lerp(-1.25, 0, eo(lid));
  g.save(); g.translate(0, -h / 2); g.scale(1, Math.cos(a) * 1); g.translate(0, -120 * Math.sin(-a) * 0);
  const lg = g.createLinearGradient(0, -130, 0, 0); lg.addColorStop(0, '#8a5628'); lg.addColorStop(1, '#4a2a10'); g.fillStyle = lg; g.fillRect(-w / 2, -130 * (Math.sin(-a) > .1 ? -1 : 1) * 0 - 130, w, 130);
  g.restore();
  g.restore();
}

// ---------- camera helpers ----------
function punch(t, t0, k = .12) { const p = seg(t, t0, t0 + .35); return 1 + k * (1 - eo(p)); }
function shake(t, t0, amp = 14) { const d = t - t0; if (d < 0 || d > .3) return [0, 0]; const e = 1 - d / .3; return [Math.sin(d * 90) * amp * e, Math.cos(d * 70) * amp * e]; }

// ================= shots =================
function render(t) {
  g.setTransform(1, 0, 0, 1, 0, 0); g.globalAlpha = 1; g.filter = 'none';
  const shot = CUT.filter(c => c <= t).length - 1, t0 = CUT[shot];
  const z = punch(t, t0), [sx, sy] = shake(t, t0, 10);
  g.save(); g.translate(AX + sx, H / 2 + sy); g.scale(z, z); g.translate(-AX, -H / 2);
  [s1, s2, s3, s4, s5, s6, s7, s8][shot](t);
  g.restore();
  // flash on the cut
  const fl = 1 - seg(t, t0, t0 + .12); if (shot > 0 && fl > 0) { g.fillStyle = `rgba(255,248,235,${.55 * fl})`; g.fillRect(0, 0, W, H); }
  // light leak drift
  g.save(); g.globalCompositeOperation = 'lighter'; const lx = (t * 90) % (W + 800) - 400; const ll = g.createRadialGradient(lx, 300, 0, lx, 300, 500); ll.addColorStop(0, 'rgba(255,120,40,.08)'); ll.addColorStop(1, 'rgba(0,0,0,0)'); g.fillStyle = ll; g.fillRect(0, 0, W, H); g.restore();
}
// 1 · the painting on the wall (hook image)
function s1(t) { wall(t); const z = lerp(1, 1.08, seg(t, 0, 2)); g.save(); g.translate(AX, 760); g.scale(z, z); card(IMG.monalisa, 0, 0, 420, 0, 1, { frame: true }); g.restore(); word('صباحٌ عادي في اللوفر', AX, 1420, 64, t, .45, { color: CREAM }); }
// 2 · the year
function s2(t) { wall(t, .8); const w = word('1911', AX, 860, 300, t, K.year - .15, { color: '#fff', font: 'Lalezar' }); if (w) underline(AX - w / 2, AX + w / 2, 1010, t, K.year + .15); }
// 3 · the empty wall (archive) + «اختفت»
function s3(t) {
  grid(t, '#2a0f06', 'rgba(255,120,60,.18)');
  card(IMG.emptywall, AX + 30, 920, 640, .05, seg(t, 3.95, 4.4), { sepia: .3 });
  word('اختفت!', AX - 40, 330, 210, t, K.gone, { font: 'Amiri', color: RED, rot: -.06 });
  word('الموناليزا', AX + 120, 520, 96, t, K.gone + 1.3, { color: '#fff' });
  tag('متحف اللوفر · باريس', AX, 1540, t, K.louvre - .2, .04);
}
// 4 · not a gang
function s4(t) {
  dark(t);
  word('لم يكن', AX + 160, 760, 120, t, 7.95, { color: '#fff' });
  const w = word('عصابة', AX - 60, 960, 220, t, K.gang - .1, { color: '#fff' });
  if (w) strike(AX - 60 - w / 2, AX - 60 + w / 2, 960, t, K.strike);
  word('بل...', AX + 200, 1200, 100, t, 9.85, { color: RED, font: 'Amiri' });
}
// 5 · the worker
function s5(t) {
  paper(t);
  card(IMG.peruggia, AX + 20, 860, 560, -.04, seg(t, 10.05, 10.45), { sepia: .2 });
  tag('فينتشنزو بيروجيا', AX + 120, 1230, t, 10.5);
  word('عاملٌ إيطالي', AX, 290, 120, t, K.worker, { color: '#161616', shadow: false });
  word('عمل في المتحف نفسه', AX, 1500, 96, t, K.same, { font: 'Amiri', color: RED, shadow: false });
}
// 6 · hidden in a trunk for two years
function s6(t) {
  grid(t, '#174a35', 'rgba(255,255,255,.14)', false);
  const drop = eo(seg(t, K.box - .4, K.box + .2));
  const lid = seg(t, K.box + .3, K.box + .7);
  // painting drops into the trunk, clipped by the trunk's top edge
  g.save(); g.beginPath(); g.rect(0, 0, W, lerp(H, 1050, seg(t, K.box - .5, K.box - .4))); g.clip();
  card(IMG.monalisa, AX, lerp(600, 1150, drop), 300, .08 - drop * .08, seg(t, 13.0, 13.3), { frame: true });
  g.restore();
  trunk(AX, 1200, lid, t);
  if (lid > 0) { const lh = 150 * eo(lid); g.fillStyle = '#5e3818'; g.fillRect(AX - 310, 1050 - lh, 620, lh); g.fillStyle = '#d8c08a'; g.fillRect(AX - 30, 1050 - 20, 60, 30); }
  word('في صندوقٍ بغرفته', AX, 330, 96, t, K.box, { color: '#fff' });
  word('سنتين', AX, 560, 200, t, K.two, { font: 'Amiri', color: YEL });
}
// 7 · it came back — and became the most famous painting
function s7(t) {
  paper(t, '#efede8');
  const n = t < K.famous ? 0 : t < K.famous + .4 ? 4 : t < K.famous + .8 ? 9 : 16;
  if (n) { const c = Math.sqrt(n), cw = W / c; for (let i = 0; i < n; i++) { const x = (i % c + .5) * cw, y = 700 + (Math.floor(i / c) - (c - 1) / 2) * cw * 1.45; card(IMG.monalisa, x, y, cw * .62, (hash(i) - .5) * .12, 1, { frame: true }); } }
  else {
    card(IMG.recovered, AX - 60, 760, 780, -.05, seg(t, 17.95, 18.3), { sepia: .25 });
    card(IMG.uffizi, AX + 150, 1250, 520, .06, seg(t, K.back, K.back + .35), { sepia: .25 });
    word('عادت!', AX - 230, 300, 150, t, K.back, { font: 'Amiri', color: RED, shadow: false });
  }
  if (n) { g.fillStyle = 'rgba(10,10,10,.55)'; g.fillRect(0, 1390, W, 260); word('أشهر لوحة', AX, 1460, 140, t, K.famous, { color: '#fff' }); word('في العالم', AX, 1590, 90, t, K.famous + .45, { font: 'Amiri', color: YEL }); }
}
// 8 · back to the wall: the question
function s8(t) {
  wall(t);
  const z = lerp(1, 1.5, eio(seg(t, 22.5, 26.5)));
  g.save(); g.translate(AX, 760); g.scale(z, z); g.translate(0, lerp(0, 60, eio(seg(t, 22.5, 26.5)))); card(IMG.monalisa, 0, 0, 420, 0, 1, { frame: true }); g.restore();
  g.fillStyle = 'rgba(10,6,3,.55)'; g.fillRect(0, 1330, W, 420);
  word('هل صنعت السرقة', AX, 1430, 104, t, K.made - .1, { color: '#fff' });
  word('شهرتها؟', AX, 1590, 160, t, K.fame, { font: 'Amiri', color: RED });
}

window.TEXTS = () => [];
(async () => {
  for (const n of ['monalisa', 'emptywall', 'peruggia', 'recovered', 'uffizi']) { const im = new Image(); im.src = `img/${n}.jpg`; await im.decode(); IMG[n] = im; }
  await Promise.all(['80px Lalezar', '700 80px Amiri'].map(f => document.fonts.load(f, 'اختفت ١٩١١')));
  const EV = [];
  CUT.slice(1).forEach(c => { EV.push({ t: c - .18, type: 'whoosh' }); EV.push({ t: c, type: 'hit' }); });
  for (const [k, v] of Object.entries(K)) EV.push({ t: v, type: 'pop', k });
  for (const t of [3.95, 10.05, 13.0, 17.95, K.back]) EV.push({ t, type: 'card' });
  EV.push({ t: K.box + .7, type: 'thud' }); EV.push({ t: K.strike, type: 'scratch' });
  for (const [id, t] of Object.entries(VO)) EV.push({ t, type: 'vo', id });
  EV.push({ t: 0, type: 'grid', cuts: CUT, dur: DUR, K });
  window.EV = EV.sort((a, b) => a.t - b.t);
  window.render = render; window.READY = true;
})();
