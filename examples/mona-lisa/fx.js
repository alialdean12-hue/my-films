// fx.js — motion-graphics toolkit for the house style (canvas 2D, deterministic in t).
// Every function draws for time t with its own start time t0; nothing keeps state between frames.
// Import: import * as FX from './fx.js';
export const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
export const lerp = (a, b, t) => a + (b - a) * t;
export const seg = (t, a, b) => clamp((t - a) / (b - a));
export const eo = t => 1 - Math.pow(1 - clamp(t), 3);
export const eo5 = t => 1 - Math.pow(1 - clamp(t), 5);                       // snappy ease-out (motion-design default)
export const eio = t => { t = clamp(t); return t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; };
export const back = (t, s = 1.8) => { t = clamp(t) - 1; return 1 + t * t * ((s + 1) * t + s); };
export const hash = n => { n = Math.sin(n * 127.1 + 311.7) * 43758.5453; return n - Math.floor(n); };
const font = (size, w = 900) => `${w} ${size}px Cairo`;

// ---------- TYPE ----------
// Words of a phrase rise one after another from behind a mask (the classic kinetic-type reveal). RTL: first word on the right.
export function maskWords(g, text, cx, cy, size, t, t0, { color = '#fff', stagger = .07, dur = .35, outline = true, accent = null, accentColor = '#FFD21F', maxW = 920 } = {}) {
  const words = text.split(' ');
  g.save(); g.font = font(size);
  { const w0 = g.measureText(text).width; if (w0 > maxW) { size = Math.floor(size * maxW / w0); g.font = font(size); } }   // auto-fit the safe area
  g.direction = 'rtl'; g.textBaseline = 'alphabetic';
  const sp = g.measureText(' ').width, ws = words.map(w => g.measureText(w).width), total = ws.reduce((a, b) => a + b, 0) + sp * (words.length - 1);
  let x = cx + total / 2;
  words.forEach((w, i) => {
    const p = eo5(seg(t, t0 + i * stagger, t0 + i * stagger + dur));
    if (p > 0) {
      g.save(); g.beginPath(); g.rect(x - ws[i] - 4, cy - size * 1.15, ws[i] + 8, size * 1.5); g.clip();
      const y = cy + (1 - p) * size * 1.2;
      g.textAlign = 'right';
      if (outline) { g.lineJoin = 'round'; g.lineWidth = size * .08; g.strokeStyle = 'rgba(0,0,0,.8)'; g.strokeText(w, x, y); }
      g.fillStyle = (accent != null && i === accent) ? accentColor : color; g.fillText(w, x, y);
      g.restore();
    }
    x -= ws[i] + sp;
  });
  g.restore();
  return total;
}
// A highlighter / marker box wipes in behind a word (right → left), then the word sits on it.
export function markerWord(g, text, cx, cy, size, t, t0, { box = '#FFD21F', color = '#111', pad = .22, rot = -.025 } = {}) {
  if (t < t0) return;
  g.save(); g.translate(cx, cy); g.rotate(rot); g.font = font(size); g.direction = 'rtl'; g.textAlign = 'center'; g.textBaseline = 'middle';
  const w = g.measureText(text).width + size * pad * 2, h = size * 1.25, p = eo5(seg(t, t0, t0 + .3));
  g.fillStyle = box; g.fillRect(w / 2 - w * p, -h / 2, w * p, h);
  const q = seg(t, t0 + .15, t0 + .35); g.globalAlpha = q; g.fillStyle = color; g.fillText(text, 0, size * .06);
  g.restore();
}
// Big number that slams in (scale 2.2 → 1 with overshoot + tiny shake) — static afterwards (no counting).
export function slamNumber(g, text, cx, cy, size, t, t0, { color = '#fff', underline = '#FF3B3B' } = {}) {
  if (t < t0) return;
  const p = seg(t, t0, t0 + .3), s = lerp(2.2, 1, back(p, 2.5)), sh = (1 - p) * 10 * Math.sin(t * 80);
  g.save(); g.translate(cx + sh, cy); g.scale(s, s); g.font = font(size); g.textAlign = 'center'; g.textBaseline = 'middle';
  g.lineJoin = 'round'; g.lineWidth = size * .07; g.strokeStyle = 'rgba(0,0,0,.85)'; g.strokeText(text, 0, 0); g.fillStyle = color; g.fillText(text, 0, 0);
  const w = g.measureText(text).width; g.restore();
  const u = eo5(seg(t, t0 + .25, t0 + .5)); if (u > 0) { g.fillStyle = underline; g.fillRect(cx + w / 2 - w * u, cy + size * .55, w * u, size * .07); }
}

// ---------- ANNOTATIONS (hand-drawn feel) ----------
// A red marker circle scribbled around a point (draws on over dur).
export function scribbleCircle(g, cx, cy, rx, ry, t, t0, { color = '#FF3B3B', w = 9, dur = .45, seed = 1 } = {}) {
  const p = eo(seg(t, t0, t0 + dur)); if (p <= 0) return;
  g.save(); g.strokeStyle = color; g.lineWidth = w; g.lineCap = 'round'; g.beginPath();
  const n = 60, a0 = -2.2, turns = 1.15;
  for (let i = 0; i <= n * p; i++) { const u = i / n, a = a0 + u * Math.PI * 2 * turns, j = 1 + (hash(i * .7 + seed) - .5) * .06; const x = cx + Math.cos(a) * rx * j * (1 + u * .05), y = cy + Math.sin(a) * ry * j; i ? g.lineTo(x, y) : g.moveTo(x, y); }
  g.stroke(); g.restore();
}
// An arrow that draws itself along a slight curve, head pops at the end.
export function drawArrow(g, x0, y0, x1, y1, t, t0, { color = '#FFD21F', w = 10, bend = .2, dur = .4 } = {}) {
  const p = eo(seg(t, t0, t0 + dur)); if (p <= 0) return;
  const mx = (x0 + x1) / 2 - (y1 - y0) * bend, my = (y0 + y1) / 2 + (x1 - x0) * bend;
  const Q = u => [(1 - u) * (1 - u) * x0 + 2 * (1 - u) * u * mx + u * u * x1, (1 - u) * (1 - u) * y0 + 2 * (1 - u) * u * my + u * u * y1];
  g.save(); g.strokeStyle = color; g.lineWidth = w; g.lineCap = 'round'; g.lineJoin = 'round'; g.beginPath();
  for (let i = 0; i <= 40 * p; i++) { const [x, y] = Q(i / 40); i ? g.lineTo(x, y) : g.moveTo(x, y); } g.stroke();
  if (p > .95) { const [ax, ay] = Q(1), [bx, by] = Q(.93), a = Math.atan2(ay - by, ax - bx), L = w * 3.2;
    g.beginPath(); g.moveTo(ax - Math.cos(a - .5) * L, ay - Math.sin(a - .5) * L); g.lineTo(ax, ay); g.lineTo(ax - Math.cos(a + .5) * L, ay - Math.sin(a + .5) * L); g.stroke(); }
  g.restore();
}
// A rubber stamp that thuds onto the frame (scale 3 → 1, rotation, ink texture).
export function stamp(g, text, cx, cy, size, t, t0, { color = '#FF3B3B', rot = -.18 } = {}) {
  if (t < t0) return;
  const p = seg(t, t0, t0 + .18), s = lerp(3, 1, eo5(p));
  g.save(); g.globalAlpha = clamp(p * 3) * .92; g.translate(cx, cy); g.rotate(rot); g.scale(s, s);
  g.font = font(size); g.direction = 'rtl'; g.textAlign = 'center'; g.textBaseline = 'middle';
  const w = g.measureText(text).width + size * .8, h = size * 1.5;
  g.strokeStyle = color; g.lineWidth = size * .09; g.strokeRect(-w / 2, -h / 2, w, h); g.lineWidth = size * .03; g.strokeRect(-w / 2 + size * .14, -h / 2 + size * .14, w - size * .28, h - size * .28);
  g.fillStyle = color; g.fillText(text, 0, size * .06);
  g.globalCompositeOperation = 'destination-out';
  for (let i = 0; i < 140; i++) { g.fillStyle = `rgba(0,0,0,${.35 + hash(i) * .5})`; g.fillRect((hash(i * 3.3) - .5) * w, (hash(i * 7.1) - .5) * h, 2 + hash(i) * 5, 2 + hash(i * 2) * 4); }
  g.restore();
}
// A route line drawing across a map/paper with a travelling dot (for journeys, escapes, migrations).
export function route(g, pts, t, t0, dur, { color = '#FF3B3B', w = 7, dash = [18, 12] } = {}) {
  const p = eio(seg(t, t0, t0 + dur)); if (p <= 0) return;
  let L = 0; const seglen = []; for (let i = 1; i < pts.length; i++) { const d = Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]); seglen.push(d); L += d; }
  let rem = L * p; g.save(); g.strokeStyle = color; g.lineWidth = w; g.setLineDash(dash); g.lineCap = 'round'; g.beginPath(); g.moveTo(...pts[0]);
  let end = pts[0];
  for (let i = 1; i < pts.length && rem > 0; i++) { const k = Math.min(1, rem / seglen[i - 1]); end = [lerp(pts[i - 1][0], pts[i][0], k), lerp(pts[i - 1][1], pts[i][1], k)]; g.lineTo(...end); rem -= seglen[i - 1]; }
  g.stroke(); g.setLineDash([]); g.beginPath(); g.arc(end[0], end[1], w * 1.8, 0, Math.PI * 2); g.fillStyle = '#fff'; g.fill(); g.lineWidth = w * .7; g.strokeStyle = color; g.stroke(); g.restore();
}

// ---------- IMAGES IN MOTION ----------
// 2.5D parallax: background, subject cut-out and foreground move at different speeds while the camera pushes in.
// layers: [{img, depth (0 far … 1 near), x, y, w}] ; drift: total horizontal camera move in px over [t0,t1]
export function parallax(g, layers, t, t0, t1, { drift = 120, push = .08, W = 1080, H = 1920 } = {}) {
  const u = eio(seg(t, t0, t1));
  for (const L of layers) {
    if (!L.img) continue;
    const s = 1 + push * u * (.4 + L.depth), dx = -drift * u * (.3 + L.depth), h = L.w * L.img.height / L.img.width;
    g.save(); g.translate(W / 2 + dx, H / 2); g.scale(s, s); g.drawImage(L.img, L.x - W / 2, L.y - H / 2, L.w, h); g.restore();
  }
}
// Light sweep (glint) across a rectangle — use on photo cards, frames, titles.
export function lightSweep(g, x, y, w, h, t, t0, { dur = .7, rot = -.4, alpha = .35 } = {}) {
  const p = seg(t, t0, t0 + dur); if (p <= 0 || p >= 1) return;
  g.save(); g.beginPath(); g.rect(x, y, w, h); g.clip(); g.globalCompositeOperation = 'lighter';
  const cx = lerp(x - w * .6, x + w * 1.6, eio(p)); g.translate(cx, y + h / 2); g.rotate(rot);
  const gr = g.createLinearGradient(-w * .18, 0, w * .18, 0); gr.addColorStop(0, 'rgba(255,255,255,0)'); gr.addColorStop(.5, `rgba(255,250,235,${alpha})`); gr.addColorStop(1, 'rgba(255,255,255,0)');
  g.fillStyle = gr; g.fillRect(-w * .18, -h * 2, w * .36, h * 4); g.restore();
}
// Magnifier: a circle that shows the image underneath zoomed in (detail reveal), with a ring.
export function magnifier(g, drawScene, cx, cy, r, zoom, t, t0) {
  const p = back(seg(t, t0, t0 + .35), 1.6); if (p <= 0) return;
  g.save(); g.beginPath(); g.arc(cx, cy, r * p, 0, Math.PI * 2); g.clip();
  g.translate(cx, cy); g.scale(zoom, zoom); g.translate(-cx, -cy); drawScene(); g.restore();
  g.save(); g.lineWidth = 14; g.strokeStyle = '#111'; g.beginPath(); g.arc(cx, cy, r * p, 0, Math.PI * 2); g.stroke();
  g.lineWidth = 5; g.strokeStyle = '#FFD21F'; g.stroke(); g.restore();
}
// Polaroid flip: a card turns over (scaleX) to show its back with a caption, or front ↔ back.
export function flipCard(g, drawFront, drawBack, cx, cy, t, t0, dur = .5) {
  const p = eio(seg(t, t0, t0 + dur)), a = p * Math.PI, sx = Math.cos(a);
  g.save(); g.translate(cx, cy); g.scale(Math.abs(sx) || .001, 1); (sx >= 0 ? drawFront : drawBack)(); g.restore();
}
// Dust / particles floating in the light (adds life to any static shot).
export function dust(g, t, { n = 60, W = 1080, H = 1920, alpha = .5, seed = 3 } = {}) {
  g.save(); g.globalCompositeOperation = 'lighter';
  for (let i = 0; i < n; i++) { const x = (hash(i + seed) * W + t * (8 + hash(i * 2) * 20)) % W, y = (hash(i * 3 + seed) * H - t * (10 + hash(i * 5) * 25) + H * 10) % H, r = 1 + hash(i * 7) * 3;
    g.fillStyle = `rgba(255,230,190,${alpha * (.3 + .7 * hash(i * 11)) * (.6 + .4 * Math.sin(t * 2 + i))})`; g.beginPath(); g.arc(x, y, r, 0, Math.PI * 2); g.fill(); }
  g.restore();
}

// ---------- TRANSITIONS (draw them over the cut point) ----------
// Zoom-through: the outgoing shot scales up into a point (e.g. a photo card's centre) while the next fades in from that point.
export function zoomThrough(g, drawOut, drawIn, t, tc, { cx = 540, cy = 960, dur = .45 } = {}) {
  const p = seg(t, tc - dur / 2, tc + dur / 2);
  if (p <= 0) return drawOut(); if (p >= 1) return drawIn();
  const e = eio(p);
  g.save(); g.translate(cx, cy); const s = lerp(1, 6, e); g.scale(s, s); g.translate(-cx, -cy); g.globalAlpha = 1 - seg(p, .45, .6); drawOut(); g.restore();
  g.save(); g.globalAlpha = seg(p, .4, .7); g.translate(cx, cy); const s2 = lerp(.6, 1, eo(seg(p, .4, 1))); g.scale(s2, s2); g.translate(-cx, -cy); drawIn(); g.restore();
}
// Whip-pan: the outgoing shot slides away with motion streaks, the incoming slides in (direction: -1 left, 1 right).
export function whipPan(g, drawOut, drawIn, t, tc, { dir = -1, dur = .3, W = 1080, H = 1920 } = {}) {
  const p = seg(t, tc - dur / 2, tc + dur / 2);
  if (p <= 0) return drawOut(); if (p >= 1) return drawIn();
  const e = eio(p), off = e * W * dir;
  for (let k = 0; k < 4; k++) { const o = off - dir * k * 26; g.save(); g.globalAlpha = k ? .22 : 1; g.translate(o, 0); drawOut(); g.restore(); g.save(); g.globalAlpha = k ? .22 : 1; g.translate(o - dir * W, 0); drawIn(); g.restore(); }
}
// Split-screen: two scenes side by side, divided by a sliding line (comparisons, then vs now).
export function split(g, drawA, drawB, t, t0, { W = 1080, H = 1920, line = '#FFD21F' } = {}) {
  const p = eo5(seg(t, t0, t0 + .45)), x = lerp(W, W / 2, p);
  drawA(); g.save(); g.beginPath(); g.rect(x, 0, W - x, H); g.clip(); drawB(); g.restore();
  if (p > 0) { g.fillStyle = line; g.fillRect(x - 5, 0, 10, H); }
}
