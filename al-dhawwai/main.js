// «الضوّاي» — Art Deco, 1080×1920, 24 fps. render(t) is deterministic in t.
import * as D from './engine/deco.js';
import * as TY from './engine/type.js';
import * as B from './engine/bulbs.js';
import { makeCam } from './engine/cam.js';
import { abuSide, abuBack, abuFace, noorFace, poleTip, CRIM, CRIM_D, CRIM_L } from './chars.js';
const { C, TAU, clamp, lerp, seg, ss, eio, eo, ei, back, mix, rgba, gline, airbrush, glow, sparkle, sunburst, hash, mulberry, toPath, arcPts } = D;

const W = 1080, H = 1920, AX = W / 2;
const cv = document.getElementById('c'); cv.width = W; cv.height = H;
const g = cv.getContext('2d');

// ---------- timeline (84 BPM) ----------
const BPM = 84, BEAT = 60 / BPM, b = n => n * BEAT;
const S = {
  hook: [0, b(10)], title: [b(10), b(16)], street: [b(16), b(22)], clock: [b(22), b(29)], skip: [b(29), b(43)],
  tele: [b(43), b(54)], face: [b(54), b(62)], tower: [b(62), b(77)], noor: [b(77), b(82)], end: [b(82), b(94)], card: [b(94), b(100)],
};
const DUR = b(100);
const VO = { l1: 1.0, l2: 11.6, l3: 17.3, l4: 21.0, l5: 28.2, l6: 31.3, l7: 39.0, l8: 49.6, l9: 60.0 };
const CUTS = [S.clock[0], S.skip[0], S.tele[0], S.face[0], S.tower[0], S.end[0], S.card[0]];
const LEAF = .36;
const T_ZOOM0 = 47.1, T_ZOOM1 = 48.4, T_WORD = 52.6;          // tower → window → city;  word complete on «بالضوّ»
const T_PULL0 = S.noor[0], T_PULL1 = S.noor[0] + 1.1;

const FONT_AR = 'Kufi';
window.DUR = DUR;

// ---------- small helpers ----------
const st2 = (t, fps = 12) => Math.floor(t * fps) / fps;       // characters step on twos
function sky(g, top = '#05070c', mid = C.night, hor = '#0f3a30', y0 = 0, y1 = H) {
  const gr = g.createLinearGradient(0, y0, 0, y1); gr.addColorStop(0, top); gr.addColorStop(.6, mid); gr.addColorStop(1, hor);
  g.fillStyle = gr; g.fillRect(0, 0, W, H);
}
function stars(g, t, n = 90, y1 = H * .6, seed = 3, alpha = 1) {
  for (let i = 0; i < n; i++) {
    const x = hash(i * 1.7 + seed) * W, y = hash(i * 3.3 + seed * 2) * y1, tw = .55 + .45 * Math.sin(t * (1 + hash(i) * 2) + i);
    const r = 1 + hash(i * 9.1) * 2.2;
    g.fillStyle = rgba(C.goldHi, .55 * tw * alpha); g.fillRect(x - r / 2, y - r / 2, r, r);
    if (hash(i * 5.5 + seed) > .93) sparkle(g, x, y, 9 + 6 * tw, { alpha: .7 * alpha, glow: 0 });
  }
}
function ground(g, top = C.black, bot = C.ink) { const gr = g.createLinearGradient(0, 0, 0, H); gr.addColorStop(0, top); gr.addColorStop(1, bot); g.fillStyle = gr; g.fillRect(0, 0, W, H); }

// ---------- the street lamp (deco lantern) ----------
// (x,y) = bottom of the lantern head (top of the post); s = scale (1 ≈ 120 px tall head). lit: 0..1.6 (ignition overshoot >1)
function lantern(g, x, y, s, lit = 0, t = 0) {
  const L = clamp(lit, 0, 1.6), on = Math.min(1, L);
  if (on > 0) { glow(g, x, y - 60 * s, 260 * s * (1 + .3 * Math.max(0, L - 1)), '#ffc45c', .42 * on); }
  const P = pts => pts.map(([a, c]) => [x + a * s, y + c * s]);
  // finial + stepped cap
  gline(g, P([[0, -150], [0, -128]]), { w: 2 * s });
  D.drawShape(g, D.starPts(x, y - 156 * s, 9 * s, .3), { lw: 1.2 * s });
  const cap = P([[-40, -96], [40, -96], [32, -108], [24, -108], [18, -120], [-18, -120], [-24, -108], [-32, -108]]);
  g.save(); g.fillStyle = D.goldGrad(g, x - 40 * s, y - 120 * s, x + 40 * s, y - 96 * s, { sheen: .35 }); g.fill(toPath(cap, true)); g.restore();
  gline(g, cap, { w: 1.4 * s, closed: true });
  // glass body (trapezoid) with mullions
  const body = P([[-34, -96], [34, -96], [24, -20], [-24, -20]]);
  const gr = g.createLinearGradient(x, y - 96 * s, x, y - 20 * s);
  if (on > 0) { gr.addColorStop(0, mix('#3a2a12', '#fff3c8', on)); gr.addColorStop(.5, mix('#2a1d0c', '#ffd27a', on)); gr.addColorStop(1, mix('#1a120a', '#e8963a', on)); }
  else { gr.addColorStop(0, '#2c2418'); gr.addColorStop(1, '#0d0a07'); }
  g.fillStyle = gr; g.fill(toPath(body, true));
  if (on <= 0) { g.fillStyle = 'rgba(255,240,210,.12)'; g.fill(toPath(P([[-30, -92], [-18, -92], [-16, -30], [-22, -30]]), true)); }
  if (on > 0) { // inner sunburst + filament
    g.save(); g.clip(toPath(body, true)); sunburst(g, x, y - 58 * s, { rays: 16, r0: 4 * s, r1: 60 * s, mode: 'lines', w: 1.2 * s, alpha: .5 * on }); g.restore();
    const f = 1 + .06 * Math.sin(t * 31); g.save(); g.globalCompositeOperation = 'lighter'; glow(g, x, y - 58 * s, 46 * s * f, '#fff1c0', .8 * on); g.restore();
  }
  for (const k of [-1, 0, 1]) gline(g, P([[k * 17, -96], [k * 12, -20]]), { w: 1.2 * s });
  gline(g, body, { w: 2 * s, closed: true, glow: .5 * on });
  // bottom cone + collar
  const cone = P([[-26, -20], [26, -20], [10, 0], [-10, 0]]);
  g.save(); g.fillStyle = D.goldGrad(g, x - 26 * s, y - 20 * s, x + 26 * s, y, { sheen: .5 }); g.fill(toPath(cone, true)); g.restore();
  gline(g, cone, { w: 1.2 * s, closed: true });
}
// fluted post from (x,y0) down to (x,y1)
function post(g, x, y0, y1, s) {
  const w = 9 * s;
  airbrush(g, [[x - w, y0], [x + w, y0], [x + w * 1.4, y1], [x - w * 1.4, y1]], { base: '#2a2116', dark: '#0c0906', light: '#5d4a2c', rim: .8 * s });
  gline(g, [[x, y0], [x, y1]], { w: Math.max(.8, 1.2 * s) });
  // stepped base
  const bh = 26 * s, bw = 22 * s;
  const base = [[x - bw, y1], [x - bw, y1 - bh * .5], [x - bw * .7, y1 - bh * .5], [x - bw * .7, y1 - bh], [x + bw * .7, y1 - bh], [x + bw * .7, y1 - bh * .5], [x + bw, y1 - bh * .5], [x + bw, y1]];
  airbrush(g, base, { base: '#2a2116', light: '#6d5733' }); gline(g, base, { w: Math.max(.8, 1.4 * s), closed: true });
  // bracket collar under the lantern
  gline(g, [[x - 14 * s, y0 + 6 * s], [x + 14 * s, y0 + 6 * s]], { w: Math.max(1, 2 * s) });
}
function ignite(t, t0, off = Infinity) {           // lamp level with ignition overshoot; switches off (with a short afterglow) at `off`
  if (t < t0) return 0;
  let v = t - t0 < .18 ? 1 + .6 * (1 - (t - t0) / .18) : 1;
  if (t - t0 < .04) v *= .3 + .7 * (t - t0) / .04;
  if (t >= off) v = Math.max(0, 1 - (t - off) / .22) * .6;
  return v;
}

// ---------- subtitles (Arabic, up to two lines, deco lacquer card) ----------
const SUBS = [];
function plaque(cx, cy, w, h, step = .16) {
  const hw = w / 2, hh = h / 2, s = Math.min(h * step, 22);
  return [[cx - hw, cy - hh], [cx + hw, cy - hh], [cx + hw, cy - hh + s], [cx + hw + s, cy - hh + s], [cx + hw + s, cy - hh + 2 * s], [cx + hw + 2 * s, cy - hh + 2 * s],
  [cx + hw + 2 * s, cy + hh - 2 * s], [cx + hw + s, cy + hh - 2 * s], [cx + hw + s, cy + hh - s], [cx + hw, cy + hh - s], [cx + hw, cy + hh],
  [cx - hw, cy + hh], [cx - hw, cy + hh - s], [cx - hw - s, cy + hh - s], [cx - hw - s, cy + hh - 2 * s], [cx - hw - 2 * s, cy + hh - 2 * s],
  [cx - hw - 2 * s, cy - hh + 2 * s], [cx - hw - s, cy - hh + 2 * s], [cx - hw - s, cy - hh + s], [cx - hw, cy - hh + s], [cx - hw, cy - hh]];
}
function splitLines(g, text, size, maxW) {
  g.font = `600 ${size}px ${FONT_AR}`;
  if (g.measureText(text).width <= maxW) return [text];
  const words = text.split(' '); let best = null;
  for (let i = 1; i < words.length; i++) {
    const a = words.slice(0, i).join(' '), c = words.slice(i).join(' ');
    const wa = g.measureText(a).width, wc = g.measureText(c).width, sc = Math.max(wa, wc) - (/[،.]$/.test(words[i - 1]) ? 120 : 0);
    if (!best || sc < best[0]) best = [sc, [a, c]];
  }
  return best[1];
}
function subtitle(g, text, k, cy = 1600) {
  if (k <= 0) return;
  const size = 46, lines = splitLines(g, text, size, 880);
  g.save(); g.font = `600 ${size}px ${FONT_AR}`;
  const tw = Math.max(...lines.map(l => g.measureText(l).width));
  const Wd = tw + size * 1.6, Ht = size * (lines.length === 1 ? 1.95 : 3.1);
  const w = Wd * ss(seg(k, 0, .7)), hh = Ht / 2 * ss(seg(k, .15, .75));
  gline(g, [[AX - w / 2 - 20, cy], [AX + w / 2 + 20, cy]], { w: 1.4, alpha: 1 - ss(seg(k, .3, .8)) });
  if (hh > 1) {
    const pts = plaque(AX, cy, w, hh * 2, .12);
    g.fillStyle = 'rgba(6,5,4,.9)'; g.fill(toPath(pts, true));
    gline(g, pts, { w: 2, closed: true, bb: [AX - Wd / 2, cy - Ht, AX + Wd / 2, cy + Ht], sheen: .35 });
    if (hh > 12) gline(g, plaque(AX, cy, w - 14, hh * 2 - 14, .12), { w: .9, closed: true, bb: [AX - Wd / 2, cy - Ht, AX + Wd / 2, cy + Ht], sheen: .6 });
  }
  const ta = ss(seg(k, .6, 1));
  if (ta > 0) {
    g.globalAlpha *= ta; g.direction = 'rtl'; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillStyle = C.ivory;
    const lh = size * 1.32; lines.forEach((l, i) => g.fillText(l, AX, cy + (i - (lines.length - 1) / 2) * lh + size * .02));
  }
  g.restore();
}

// ---------- Arabic gold text (no letter-spacing: it would break the joins) ----------
function goldAr(g, text, x, y, size, { sheen = .4, alpha = 1, weight = 700, shadow = true, fill = null, font = FONT_AR } = {}) {
  g.save(); g.globalAlpha *= alpha; g.font = `${weight} ${size}px ${font}`; g.direction = 'rtl'; g.textAlign = 'center'; g.textBaseline = 'alphabetic';
  const w = g.measureText(text).width;
  if (shadow) { g.fillStyle = 'rgba(0,0,0,.65)'; g.fillText(text, x + size * .03, y + size * .045); }
  g.fillStyle = fill || D.goldGrad(g, x - w / 2, y - size, x + w / 2, y + size * .2, { sheen });
  g.fillText(text, x, y); g.restore(); return w;
}
// title bar with an Arabic title (same unfold grammar as the engine's titleBar)
function titleAr(g, text, cx, cy, size, p, out = 0) {
  const k = p * (1 - out); if (k <= 0) return;
  g.save(); g.font = `700 ${size}px ${FONT_AR}`; const tw = g.measureText(text).width; g.restore();
  const Wd = tw + size * 1.6, Ht = size * 1.7;
  const lineP = ss(seg(k, 0, .35)), open = eio(seg(k, .22, .6)), txt = ss(seg(k, .42, .85)), orn = back(seg(k, .62, 1));
  const sh = lerp(-.2, 1.2, seg(p, .45, 1));
  if (lineP > 0) { glow(g, cx, cy, 80 + 260 * lineP, '#ffcf7a', .25 * (1 - open * .6)); if (open < .98) gline(g, [[cx - Wd * .5 * lineP, cy], [cx + Wd * .5 * lineP, cy]], { w: 2.4, glow: .6 * (1 - open) }); }
  if (open > 0) {
    const hh = Ht / 2 * open, pts = plaque(cx, cy, Wd, hh * 2, .14);
    const gr = g.createLinearGradient(0, cy - hh, 0, cy + hh); gr.addColorStop(0, '#16120c'); gr.addColorStop(.5, '#050403'); gr.addColorStop(1, '#16120c');
    g.fillStyle = gr; g.fill(toPath(pts, true));
    gline(g, pts, { w: 2.8, closed: true, bb: [cx - Wd / 2, cy - hh, cx + Wd / 2, cy + hh], sheen: .3 + sh * .4 });
    if (hh > 14) gline(g, plaque(cx, cy, Wd - 24, hh * 2 - 24, .14), { w: 1.2, closed: true, bb: [cx - Wd / 2, cy - hh, cx + Wd / 2, cy + hh], sheen: .5 });
    if (orn > 0) for (const sg of [-1, 1]) {
      const ex = Wd / 2 + 50, L = 90 * orn;
      for (let i = 0; i < 3; i++) gline(g, [[cx + sg * ex, cy + (i - 1) * hh * .3], [cx + sg * (ex + L * (i % 2 ? .65 : 1)), cy + (i - 1) * hh * .3]], { w: i === 1 ? 2 : 1.2 });
    }
  }
  if (txt > 0) {
    g.save(); const hh = Ht / 2 * open; g.beginPath(); g.rect(cx - Wd, cy - hh + 3, Wd * 2, hh * 2 - 6); g.clip();
    goldAr(g, text, cx, cy + size * .33 + (1 - txt) * size * .5, size, { sheen: sh, alpha: txt });
    g.restore();
  }
  if (orn > .6 && out < .2) sparkle(g, cx + Wd / 2 - 8, cy - Ht / 2 * open + 4, 30 * (1 - Math.abs(seg(p, .8, 1) - .5) * 2), { alpha: 1 });
}

// ---------- threshold leaves (sliding doors meeting on the axis) ----------
function leaves(g, k, t) {
  if (k <= 0) return;
  const e = eio(k), w = AX * e;
  for (const sg of [-1, 1]) {
    g.save();
    const x0 = sg < 0 ? 0 : W - w, x1 = sg < 0 ? w : W;
    g.beginPath(); g.rect(x0, 0, x1 - x0, H); g.clip();
    const gr = g.createLinearGradient(x0, 0, x1, 0); gr.addColorStop(0, '#120e09'); gr.addColorStop(1, '#050403');
    g.fillStyle = gr; g.fillRect(x0, 0, x1 - x0, H);
    const edge = sg < 0 ? w : W - w;       // the inner (moving) edge
    // panel art moves with the leaf
    const ox = sg < 0 ? w - AX : W - w;    // leaf's left x in its closed position frame
    g.translate(sg < 0 ? w - AX : W - w, 0);
    D.fishScale(g, 40, 260, AX - 80, 520, 30, { stroke: 'rgba(201,162,75,.55)' });
    D.fishScale(g, 40, 1140, AX - 80, 520, 30, { stroke: 'rgba(201,162,75,.55)' });
    D.chevrons(g, 40, AX - 40, 880, { n: 8, h: 34, rows: 4, gap: 22, w: 1.6 });
    for (const yy of [230, 820, 1100, 1690]) gline(g, [[30, yy], [AX - 30, yy]], { w: 2 });
    gline(g, D.rectPts(24, 24, AX - 48, H - 48), { w: 1.6, closed: true });
    // half sunburst on the seam side
    const sx = sg < 0 ? AX : 0;
    g.save(); g.beginPath(); g.rect(0, 0, AX, H); g.clip();
    sunburst(g, sx, H / 2, { rays: 30, r0: 40, r1: 230, a0: sg < 0 ? Math.PI / 2 : -Math.PI / 2, a1: sg < 0 ? Math.PI * 1.5 : Math.PI / 2, mode: 'lines', w: 2, alpha: .8 });
    g.restore();
    g.restore();
    gline(g, [[edge, 0], [edge, H]], { w: 3, glow: .4 * e });
  }
  if (e > .97) { glow(g, AX, H / 2, 300, '#ffcf7a', .5 * (e - .97) / .03); }
}
function leafK(t) {           // closing before each cut, opening after
  let k = 0;
  for (const c of CUTS) { if (t >= c - LEAF && t < c) k = Math.max(k, seg(t, c - LEAF, c)); if (t >= c && t < c + LEAF) k = Math.max(k, 1 - seg(t, c, c + LEAF)); }
  if (t >= S.street[0] && t < S.street[0] + LEAF * 1.4) k = Math.max(k, 1 - seg(t, S.street[0], S.street[0] + LEAF * 1.4));
  return k;
}

// ================= scenes =================

// 1 · hook: a point → a hairline → the lamp ignites. Slow pull-back.
const T_IGN = .72;
function sceneHook(g, t) {
  ground(g, '#1c1610', '#0b0806');
  sunburst(g, AX, 860, { rays: 64, r0: 60, r1: 1500, mode: 'wedges', colorA: 'rgba(201,162,75,.05)' });
  const lit = ignite(t, T_IGN);
  const pull = eio(seg(t, 1.0, S.hook[1] + .4));
  const sc = lerp(2.1, 1.0, pull), cx = AX, cy = lerp(1040, 820, pull);
  if (lit > 0) sunburst(g, cx, cy - 60 * sc, { rays: 64, r0: 120 * sc, r1: 1500, mode: 'wedges', colorA: `rgba(201,162,75,${.07 * Math.min(1, lit)})` });
  if (t < T_IGN + .1) {   // point → hairline
    const p = ss(seg(t, .15, T_IGN));
    glow(g, cx, cy - 58 * sc, 30 + 120 * p, '#ffcf7a', .5 * p);
    if (p > 0) gline(g, [[cx - 140 * p, cy - 58 * sc], [cx + 140 * p, cy - 58 * sc]], { w: 1.8, glow: .8, alpha: 1 - seg(t, T_IGN - .05, T_IGN + .1) });
  }
  if (t >= T_IGN - .05) {
    post(g, cx, cy, cy + 1400 * sc, sc * 1.4);
    lantern(g, cx, cy, sc * 1.7, lit, t);
  }
  // the pole arrives from lower right, touches, withdraws
  const touch = ss(seg(t, 0, T_IGN)) * (1 - ss(seg(t, T_IGN + .6, T_IGN + 2.2)));
  const tip = [cx + lerp(500, 40, touch) * sc, cy - 60 * sc + lerp(500, 40, touch) * sc];
  g.save(); g.strokeStyle = D.goldGrad(g, tip[0], tip[1], tip[0] + 700, tip[1] + 900, { sheen: .5 }); g.lineWidth = 7 * sc; g.lineCap = 'round';
  g.beginPath(); g.moveTo(tip[0], tip[1]); g.lineTo(tip[0] + 700 * sc, tip[1] + 1000 * sc); g.stroke(); g.restore();
  poleTip(g, tip[0], tip[1] - 6 * sc, 2 * sc, 1, t);
  D.vignette(g, W, H, .6);
}

// 2 · title on the lamp's sunburst
function sceneTitle(g, t) {
  ground(g, '#0d0b09', '#050403');
  const k = seg(t, S.title[0], S.title[0] + .6);
  sunburst(g, AX, 700, { rays: 64, r0: 110, r1: 1500, mode: 'wedges', colorA: 'rgba(201,162,75,.07)' });
  sunburst(g, AX, 700, { rays: 48, r0: 150, r1: lerp(400, 1100, eo(k)), mode: 'lines', w: 2, alpha: .45 });
  post(g, AX, 700, 2100, 1.4); lantern(g, AX, 700, 1.7, 1, t);
  titleAr(g, 'الضوّاي', AX, 1060, 170, seg(t, S.title[0] + .1, S.title[0] + 1.8), seg(t, S.title[1] - .45, S.title[1]));
  D.vignette(g, W, H, .6);
  TEXT('title', 'الضوّاي', AX - 330, 940, AX + 330, 1150, t >= S.title[0] + 1.3 && t < S.title[1] - .45);
}

// ---------- the street (shots 2 and 9): true one-point perspective down the axis ----------
const LAMPZ = [7, 14, 21, 28, 35, 42, 49, 56, 63, 70, 77];
function street(g, t, cam, lampLevel, abu) {
  sky(g, '#04060b', '#0a0f18', '#123c33', 0, H * .52);
  stars(g, t, 70, H * .4, 5);
  const P = cam.P;
  // far facade end (vanishing block)
  const far = 120;
  // road + pavements
  const road = [P(-5, 0, .3), P(5, 0, .3), P(5, 0, far), P(-5, 0, far)];
  g.fillStyle = '#0b0907'; g.fill(toPath(road, true));
  for (const x of [-5, 5]) gline(g, [P(x, 0, .3), P(x, 0, far)], { w: 2 });
  for (const x of [-9, 9]) { const pv = [P(x, 0, .3), P(Math.sign(x) * 5, 0, .3), P(Math.sign(x) * 5, 0, far), P(x, 0, far)]; g.fillStyle = '#16120d'; g.fill(toPath(pv, true)); }
  // paving chevrons on the road (gold, fading with distance)
  for (let z = 4; z < 60; z += 3) { const a = 1 - z / 60; gline(g, [P(-1.2, 0, z + 1), P(0, 0, z), P(1.2, 0, z + 1)], { w: 1.2, alpha: .5 * a }); }
  // facades both sides: arcade (pillars + arches) under a tall wall with deco windows
  for (const sgn of [-1, 1]) {
    const X = 9 * sgn;
    const wall = [P(X, 0, .3), P(X, 18, .3), P(X, 18, far), P(X, 0, far)];
    airbrush(g, wall, { base: '#1a1510', dark: '#070605', light: '#2c241a', dir: sgn < 0 ? -.3 : -2.8 });
    // window rows
    for (let z = 6; z < 90; z += 6) for (const y of [8.5, 12, 15.5]) {
      const q = [P(X, y, z), P(X, y + 2.2, z), P(X, y + 2.2, z + 2.4), P(X, y, z + 2.4)];
      const on = hash(z * 3.1 + y * 7 + sgn) > .72;
      g.fillStyle = on ? rgba('#ffcf7a', .35 * (1 - z / 100)) : 'rgba(0,0,0,.35)'; g.fill(toPath(q, true));
      gline(g, q, { w: .9, closed: true, alpha: .6 * (1 - z / 100) });
    }
    gline(g, [P(X, 7, .3), P(X, 7, far)], { w: 2.2 }); gline(g, [P(X, 18, .3), P(X, 18, far)], { w: 2.2 });
  }
  // pillars & arches & lamps sorted far → near
  const items = [];
  for (let z = 4; z < 100; z += 4) for (const sgn of [-1, 1]) items.push({ z, kind: 'pillar', sgn });
  LAMPZ.forEach((z, i) => { for (const sgn of [-1, 1]) items.push({ z, kind: 'lamp', sgn, i }); });
  if (abu) items.push({ z: abu.z, kind: 'abu' });
  items.sort((a, c) => c.z - a.z);
  for (const it of items) {
    if (it.kind === 'pillar') {
      const X = 8.2 * it.sgn, z = it.z;
      const p = [P(X - .35, 0, z), P(X + .35, 0, z), P(X + .35, 7, z), P(X - .35, 7, z)];
      airbrush(g, p, { base: '#241d14', light: '#4a3b26' });
      gline(g, p, { w: Math.max(.6, 1.6 * cam.scaleAt(X, 3, z) / 90), closed: true, alpha: 1 - z / 110 });
      // arch to the next pillar (in the plane x=X)
      const a = []; for (let i = 0; i <= 16; i++) { const u = i / 16; a.push(P(X, 5 + Math.sin(u * Math.PI) * 1.6, z + u * 4)); }
      gline(g, a, { w: Math.max(.6, 1.4 * cam.scaleAt(X, 5, z) / 90), alpha: 1 - z / 110 });
    } else if (it.kind === 'lamp') {
      const X = 5.6 * it.sgn, z = it.z, s = cam.scaleAt(X, 4.6, z) / 110;
      const top = P(X, 4.6, z), bot = P(X, 0, z);
      const lv = lampLevel(it.i, it.sgn, t);
      if (lv > 0) { const pool = P(X, 0, z); glow(g, pool[0], pool[1], 220 * s * 2, '#ffbf5a', .2 * Math.min(1, lv), .35); }
      post(g, top[0], top[1], bot[1], s);
      lantern(g, top[0], top[1], s, lv, t);
    } else if (it.kind === 'abu') {
      const sc = cam.scaleAt(abu.x, 0, abu.z) * 1.75 / 330, p = P(abu.x, 0, abu.z);
      glow(g, p[0], p[1], 140 * sc * 1.2, '#000000', .5, .3);
      abuBack(g, p[0], p[1], sc, abu.o);
    }
  }
  D.vignette(g, W, H, .55);
}
function sceneStreet(g, t) {
  const u = seg(t, S.street[0], S.street[1]);
  const cam = makeCam({ x: 0, y: 1.9, z: lerp(-2, 3.5, eio(u)), f: 820, pitch: .04, W, H, oy: H * .5 });
  const az = lerp(6, 11.5, u), tt = st2(t);
  // lamps ignite down the street: on beats, then eighths, then sixteenths (the routine accelerates)
  const t0 = S.street[0] + .55, times = [];
  let tc = t0; for (let i = 0; i < LAMPZ.length; i++) { times.push(tc); tc += i < 4 ? BEAT : i < 7 ? BEAT / 2 : BEAT / 4; }
  street(g, t, cam, (i, sgn) => ignite(t, times[i] + (sgn > 0 ? .06 : 0)), { x: -.4, z: az, o: { phase: (tt - S.street[0]) * .9, walk: 1, t } });
}
function sceneEnd(g, t) {
  const u = seg(t, S.end[0], S.end[1]);
  const cam = makeCam({ x: -1.2, y: lerp(2.6, 2.2, eio(u)), z: lerp(-.8, .4, u), f: 820, pitch: .05, W, H, oy: H * .5 });
  // lamps go out far → near, one pair per beat; the near-left lamp above him stays on
  const off0 = S.end[0] + BEAT * 1.0;
  const lvl = (i, sgn) => { if (i === 0 && sgn < 0) return 1; const n = 10 - i; return ignite(t, -1, off0 + n * BEAT * .6 + (sgn > 0 ? .1 : 0)); };
  // no-ops for the far lamps beyond index 10
  const wave = ss(seg(t, 64.2, 64.9)) * (1 - ss(seg(t, 65.9, 66.4)));
  street(g, t, cam, lvl, { x: -4.3, z: 6.4, o: { walk: 0, t, wave, lookUp: 1 } });
  // the plane far above: wing light blinks twice — her answer
  const px = lerp(1250, -200, seg(t, 61.2, 66.8)), py = lerp(330, 250, seg(t, 61.2, 66.8));
  plane(g, px, py, .28, t, { lights: true });
  const blink = (Math.abs(t - 63.7) < .12 || Math.abs(t - 64.3) < .12) ? 1 : 0;
  if (blink) { glow(g, px + 20, py + 8, 70, CRIM_L, .9); sparkle(g, px + 20, py + 8, 26, { color: '#ffd0d6' }); }
}

// 3 · the clock: push-in, 8:45 → 8:46 on the beat
function sceneClock(g, t) {
  const u = seg(t, S.clock[0], S.clock[1]);
  sky(g, '#05070c', '#0b1420', '#134236');
  stars(g, t, 50, H * .5, 9);
  g.save(); const z = lerp(1, 1.28, eio(u)); g.translate(AX, 860); g.scale(z, z); g.translate(-AX, -860);
  // tower shaft with setbacks
  const tw = [[AX - 330, H + 400], [AX - 330, 520], [AX - 270, 520], [AX - 270, 420], [AX - 200, 420], [AX - 200, 330], [AX + 200, 330], [AX + 200, 420], [AX + 270, 420], [AX + 270, 520], [AX + 330, 520], [AX + 330, H + 400]];
  airbrush(g, tw, { base: '#1c1712', dark: '#070605', light: '#3a2f22', dir: -2.2, rim: 2 });
  gline(g, tw, { w: 2.4 });
  for (const x of [-250, -150, 150, 250]) gline(g, [[AX + x, 1230], [AX + x, H + 400]], { w: 1.4 });
  sunburst(g, AX, 330, { rays: 22, r0: 30, r1: 200, a0: Math.PI, a1: TAU, mode: 'lines', w: 2, alpha: .8 });
  D.chevrons(g, AX - 260, AX + 260, 1250, { n: 10, h: 26, rows: 3, gap: 16 });
  const tick = S.clock[0] + BEAT * 4;   // the minute hand jumps on beat 4 of the shot
  const mj = t < tick ? 45 : 46 - .12 * Math.exp(-(t - tick) * 12) * Math.cos((t - tick) * 40);
  const sec = ((t - S.clock[0]) * 1 + 52) % 60;
  TY.clockFace(g, AX, 860, 300, { h: 8, m: mj, s: Math.floor(sec), lit: .5, sheen: lerp(.2, .8, u) });
  g.restore();
  D.vignette(g, W, H, .55);
}

// 4 · the wrong order: side tracking along the lamps; then tilt up to the windows
const SKIPX0 = 900, SKIPSTEP = 210;
function sceneSkip(g, t) {
  const t0 = S.skip[0], tLight1 = t0 + 1.0, walk0 = t0 + 1.55, walk1 = t0 + 5.9, tLight2 = walk1 + .55;
  const tt = st2(t);
  // Abu world x (walking right → left)
  const wx = lerp(SKIPX0 + 120, SKIPX0 - 11 * SKIPSTEP + 120, ss(seg(tt, walk0, walk1)) * .2 + seg(tt, walk0, walk1) * .8);
  const wxs = lerp(SKIPX0 + 120, SKIPX0 - 11 * SKIPSTEP + 120, ss(seg(t, walk0, walk1)) * .2 + seg(t, walk0, walk1) * .8);
  const camX = wxs - 40;
  const tilt = eio(seg(t, S.skip[1] - 3.55, S.skip[1] - 2.3));       // camera rises to the windows
  const camY = lerp(0, 1150, tilt);
  // background: sky + arcade facade (parallax .55)
  sky(g, '#04060b', '#0b1018', '#123c33');
  stars(g, t, 50, H * .3, 13);
  g.save(); g.translate(0, camY);
  const fx = -camX * .55;
  g.save(); g.translate(fx, 0);
  const x0 = -800, x1 = 3200;
  airbrush(g, [[x0, -900], [x1, -900], [x1, 1520], [x0, 1520]], { base: '#1a1510', dark: '#090706', light: '#2a2219', dir: -1.6 });
  // windows upstairs (rows), shutters per window
  for (let r = 0; r < 3; r++) for (let c = 0; c < 18; c++) {
    const wxp = x0 + 120 + c * 240, wy = -760 + r * 300;
    deoWindow(g, wxp, wy, 120, 210, t, r, c);
  }
  gline(g, [[x0, 120], [x1, 120]], { w: 2.4 }); gline(g, [[x0, 140], [x1, 140]], { w: 1.2 });
  // arcade arches at street level
  for (let c = 0; c < 22; c++) { const ax = x0 + c * 200; const pts = D.stepArchPts(ax + 100, 1520, 170, 560, { steps: 2, crown: 'round' }); g.fillStyle = '#080605'; g.fill(toPath(pts, true)); gline(g, pts, { w: 1.6, alpha: .9 }); }
  g.restore();
  // pavement
  airbrush(g, [[0, 1520], [W, 1520], [W, 2200], [0, 2200]], { base: '#16120d', dark: '#070605', dir: -1.57 });
  gline(g, [[0, 1520], [W, 1520]], { w: 2.4 });
  for (let i = -2; i < 30; i++) { const x = ((i * 120 - camX * 1.0) % 2400 + 2400) % 2400 - 200; gline(g, [[x, 1560], [x - 60, 1900]], { w: 1, alpha: .35 }); }
  // lamps (world x = SKIPX0 - i*SKIPSTEP), index 0 lit first, 11 lit last; 1..10 skipped
  for (let i = 0; i < 12; i++) {
    const x = SKIPX0 - i * SKIPSTEP - camX + AX;
    if (x < -150 || x > W + 150) continue;
    const lv = i === 0 ? ignite(t, tLight1) : i === 11 ? ignite(t, tLight2) : 0;
    post(g, x, 1010, 1540, 1.05); lantern(g, x, 1010, 1.15, lv, t);
  }
  // Abu
  const reach1 = ss(seg(tt, tLight1 - .5, tLight1)) * (1 - ss(seg(tt, tLight1 + .2, walk0)));
  const reach2 = ss(seg(tt, tLight2 - .55, tLight2)) * (1 - ss(seg(tt, tLight2 + .5, tLight2 + 1.1)));
  const walking = tt > walk0 && tt < walk1;
  abuSide(g, wx - camX + AX + 30, 1540, 1.32, { phase: (tt - walk0) * 1.6, walk: walking ? 1 : 0, reach: Math.max(reach1, reach2), t });
  g.restore();
  // skipped counter: Arabic-Indic digits ١…١٠ above, as each dark lamp passes behind him
  const passed = Math.floor(clamp((SKIPX0 + 120 - wx) / SKIPSTEP, 0, 10.99));
  if (t > walk0 + .2 && t < tLight2 + .3 && passed >= 1) {
    const d = '٠١٢٣٤٥٦٧٨٩'; const n = Math.min(10, passed); const str = n === 10 ? '١٠' : d[n];
    const pop = 1 + .25 * Math.exp(-((tt - walk0) * 1.6 % 1) * 6);
    g.save(); g.translate(AX, 560 + camY); g.scale(pop, pop);
    TY.floorMedallion(g, '', 0, 0, 110, { lit: .4 });
    goldAr(g, str, 0, 42, 120, { font: FONT_AR });
    g.restore();
  }
  D.vignette(g, W, H, .55);
}
function deoWindow(g, x, y, w, h, t, r, c) {
  const pts = D.stepArchPts(x + w / 2, y + h, w, h, { steps: 2, crown: 'round' });
  const open0 = S.skip[1] - 2.85 + ((r * 7 + c * 3) % 9) * BEAT / 3;   // shutters open in counted order
  const o = eio(seg(t, open0, open0 + .35));
  const who = (r * 5 + c * 11) % 4 !== 0;
  g.fillStyle = o > 0 && who ? rgba('#ffc96a', .55 * o) : '#060504'; g.fill(toPath(pts, true));
  if (o > 0 && who) { // a neighbour leans in: head + shoulders silhouette, shaking the head
    g.save(); g.clip(toPath(pts, true));
    const sh = Math.sin((t - open0) * 9 + c) * 5 * ss(seg(t, open0 + .3, open0 + .6));
    airbrush(g, [[x + 14, y + h], [x + w - 14, y + h], [x + w - 26, y + h - 50], [x + 26, y + h - 50]], { base: C.plum, light: C.plumL });
    g.beginPath(); g.ellipse(x + w / 2 + sh, y + h - 84, 26, 32, 0, 0, TAU); g.fillStyle = C.plum; g.fill();
    g.restore();
  }
  // shutters (two leaves) split open from the centre
  for (const sg of [-1, 1]) {
    const ww = w / 2 * (1 - o * .92);
    const xs = sg < 0 ? x : x + w - ww;
    g.save(); g.clip(toPath(pts, true));
    airbrush(g, [[xs, y], [xs + ww, y], [xs + ww, y + h], [xs, y + h]], { base: '#3a2a18', dark: '#120c06', light: '#6a4c2a' });
    for (let k = 1; k < 6; k++) gline(g, [[xs + 4, y + k * h / 6], [xs + ww - 4, y + k * h / 6]], { w: .8, alpha: .7 });
    g.restore();
  }
  gline(g, pts, { w: 1.6, closed: true });
}

// 5 · the telegram: the reason, typed right → left
const TELE = 'راجعة الليلة · طيارة الساعة ٩ · نور';
function sceneTele(g, t) {
  const t0 = S.tele[0];
  ground(g, '#0d0b09', '#050403');
  sunburst(g, AX, 1000, { rays: 72, r0: 0, r1: 1600, mode: 'wedges', colorA: 'rgba(201,162,75,.06)' });
  const push = eio(seg(t, t0 + 5.2, S.tele[1] - .3));
  g.save();
  // reveal geometry
  g.font = `700 64px ${FONT_AR}`; g.direction = 'rtl';
  const tw = g.measureText(TELE).width, noorW = g.measureText('نور').width;
  const scale0 = Math.min(1, 900 / tw), tapeW = tw * scale0 + 120, cy = 1000;
  const fx = AX - tw * scale0 / 2 + noorW * scale0 / 2, z = lerp(1, 2.6, push);
  g.translate(lerp(AX, fx, push), cy); g.scale(z, z); g.translate(-lerp(AX, fx, push), -cy);
  D.archFrame(g, AX, 1420, 900, 1080, { rings: 3, gap: 16, part: ss(seg(t, t0, t0 + .9)), burst: true });
  goldAr(g, 'برقية', AX, 620, 64, { alpha: ss(seg(t, t0 + .4, t0 + 1)) });
  gline(g, [[AX - 160, 650], [AX + 160, 650]], { w: 1.6, alpha: ss(seg(t, t0 + .4, t0 + 1)) });
  // ivory tape with perforations
  const tp = [[AX - tapeW / 2, cy - 70], [AX + tapeW / 2, cy - 70], [AX + tapeW / 2, cy + 70], [AX - tapeW / 2, cy + 70]];
  const tapeIn = ss(seg(t, t0 + .3, t0 + .8));
  g.save(); g.beginPath(); g.rect(AX - tapeW / 2 * tapeIn, cy - 80, tapeW * tapeIn, 160); g.clip();
  airbrush(g, tp, { base: C.ivory, dark: C.ivoryD, light: '#fffaf0', dir: -1.7 });
  for (let x = AX - tapeW / 2 + 20; x < AX + tapeW / 2; x += 26) { g.beginPath(); g.arc(x, cy - 54, 4, 0, TAU); g.arc(x, cy + 54, 4, 0, TAU); g.fillStyle = '#b8aa8c'; g.fill(); }
  // typed text, revealed from the right edge
  const r = seg(t, VO.l6 - .1, VO.l6 + 4.2);
  const xr = AX + tw * scale0 / 2;
  g.beginPath(); g.rect(xr - tw * scale0 * r - 4, cy - 60, tw * scale0 * r + 8, 120); g.clip();
  g.translate(AX, cy + 22); g.scale(scale0, scale0);
  g.textAlign = 'center'; g.fillStyle = '#1b130c'; g.fillText(TELE, 0, 0);
  // «نور» turns to the accent as the camera arrives
  if (push > 0) { g.fillStyle = rgba(CRIM, push); g.textAlign = 'left'; g.fillText('نور', -tw / 2, 0); }
  g.restore();
  gline(g, tp, { w: 2, closed: true, alpha: tapeIn });
  // the typing head (a small gold carriage) moving right → left
  if (r > 0 && r < 1) { const hx = xr - tw * scale0 * r; D.drawShape(g, [[hx - 8, cy - 92], [hx + 8, cy - 92], [hx + 4, cy - 70], [hx - 4, cy - 70]], { lw: 1.2 }); glow(g, hx, cy, 40, '#ffcf7a', .5); }
  g.restore();
  D.vignette(g, W, H, .6);
  TEXT('tele', TELE, AX - 470, cy - 70, AX + 470, cy + 70, t >= VO.l6 - .1 && t < t0 + 5.2);
}

// 6 · close on Abu Noor: he looks up. Then near-silence.
function sceneFace(g, t) {
  const t0 = S.face[0], u = seg(t, t0, S.face[1]);
  sky(g, '#04060b', '#0a1018', '#134236');
  stars(g, t, 60, H * .45, 21, .8);
  glow(g, 130, 300, 700, '#ffc45c', .35);             // the lamp above-left
  sunburst(g, 620, 760, { rays: 40, r0: 380, r1: 900, mode: 'lines', w: 1.6, alpha: .25 });
  const look = eio(seg(t, t0 + 3.0, t0 + 4.1));
  const blink = Math.max(0, 1 - Math.abs(t - (t0 + 1.7)) / .07);
  const z = lerp(1, 1.1, eio(u));
  g.save(); g.translate(AX, 1000); g.scale(z, z); g.translate(-AX, -1000);
  abuFace(g, 600, 1020, 1.85, { look, blink, t });
  g.restore();
  D.vignette(g, W, H, .6);
}

// ---------- the plane (streamlined, three-quarter side) ----------
function plane(g, x, y, s, t, { lights = false, win = null } = {}) {
  const P = pts => pts.map(([a, c]) => [x + a * s, y + c * s]);
  // wings (far)
  airbrush(g, P([[-40, -10], [120, -70], [170, -70], [80, -6]]), { base: '#8f8a80', dark: '#3b3832', light: '#cfc8ba' });
  // fuselage (nose to the left)
  const fus = P([[-330, 6], [-300, -30], [-200, -46], [200, -40], [330, -60], [360, -56], [330, 10], [200, 26], [-200, 34], [-300, 28]]);
  airbrush(g, fus, { base: '#b8b2a6', dark: '#4a463f', light: '#efe9dc', dir: -1.9, rim: 2 * s });
  gline(g, fus, { w: Math.max(1, 2.2 * s), closed: true });
  gline(g, P([[-300, 0], [330, -14]]), { w: Math.max(.8, 1.4 * s), closed: false });
  // tail fin (stepped)
  const fin = P([[250, -42], [300, -140], [330, -140], [340, -120], [352, -120], [360, -56]]);
  airbrush(g, fin, { base: '#a8a296', light: '#efe9dc', rim: 1.5 * s }); gline(g, fin, { w: Math.max(1, 1.8 * s), closed: true });
  // engines + propeller discs
  for (const ex of [-120, 40]) {
    const e = P([[ex - 40, 20], [ex + 50, 16], [ex + 50, 44], [ex - 40, 44]]);
    airbrush(g, e, { base: '#7c776d', light: '#d8d2c4' }); gline(g, e, { w: Math.max(.8, 1.4 * s), closed: true });
    const pc = P([[ex - 44, 32]])[0];
    g.save(); g.globalAlpha = .35; g.beginPath(); g.ellipse(pc[0], pc[1], 10 * s, 48 * s, 0, 0, TAU); g.fillStyle = '#f2e8d5'; g.fill(); g.restore();
    gline(g, [[pc[0], pc[1] - 48 * s], [pc[0], pc[1] + 48 * s]], { w: Math.max(.6, 1 * s), alpha: .4 });
  }
  // near wing
  airbrush(g, P([[-60, 10], [40, 120], [110, 130], [70, 10]]), { base: '#a49e92', dark: '#4a463f', light: '#e6dfd0', rim: 1.4 * s });
  gline(g, P([[-60, 10], [40, 120], [110, 130], [70, 10]]), { w: Math.max(.8, 1.6 * s), closed: true });
  // round windows, warm
  const wins = [];
  for (let i = 0; i < 9; i++) {
    const c = P([[-210 + i * 50, -14]])[0], r = 11 * s; wins.push([c[0], c[1], r]);
    g.beginPath(); g.arc(c[0], c[1], r, 0, TAU); g.fillStyle = '#ffd98a'; g.fill();
    g.beginPath(); g.arc(c[0], c[1], r, 0, TAU); g.strokeStyle = C.gold2; g.lineWidth = Math.max(.8, 2 * s); g.stroke();
  }
  if (lights) { const wl = P([[110, 128]])[0]; g.beginPath(); g.arc(wl[0], wl[1], 3.5 * Math.max(1, s * 2), 0, TAU); g.fillStyle = CRIM_L; g.fill(); }
  return wins;
}

// ---------- the tower (Cassandre low angle) ----------
function towerScene(g, t, pitch) {
  const cam = makeCam({ x: -3, y: 1.6, z: 0, f: 760, yaw: .22, pitch, W, H });
  sky(g, '#020309', '#070b14', '#0e2a26');
  stars(g, t, 120, H, 31);
  const P = cam.P;
  const block = (x0, x1, y0, y1, z0, z1) => {
    // front face (z0) and right face (x1)
    const f = [P(x0, y0, z0), P(x1, y0, z0), P(x1, y1, z0), P(x0, y1, z0)];
    const r = [P(x1, y0, z0), P(x1, y0, z1), P(x1, y1, z1), P(x1, y1, z0)];
    airbrush(g, r, { base: '#120f0b', dark: '#050403', light: '#241d14', dir: -.4 });
    airbrush(g, f, { base: '#221b13', dark: '#0a0806', light: '#4a3b26', dir: -2.2 });
    gline(g, f, { w: 2.2, closed: true }); gline(g, r, { w: 1.6, closed: true, alpha: .8 });
    for (let x = x0 + 2; x < x1; x += 2.5) gline(g, [P(x, y0, z0), P(x, y1, z0)], { w: 1.1, alpha: .75 });
    for (let y = y0 + 3; y < y1 - 1; y += 4) for (let x = x0 + 1; x < x1 - 1; x += 2.5) {
      if (hash(x * 3.3 + y * 1.7) < .78) continue;
      const q = [P(x + .25, y, z0), P(x + 1.6, y, z0), P(x + 1.6, y + 2, z0), P(x + .25, y + 2, z0)];
      g.fillStyle = rgba('#ffcf7a', .5); g.fill(toPath(q, true));
    }
  };
  block(-14, 14, -40, 60, 30, 58); block(-10, 10, 60, 85, 34, 54); block(-6, 6, 85, 100, 38, 50);
  // crown: sunburst fan + spire
  const c = P(0, 100, 38);
  const fanTop = P(0, 112, 38);
  D.fan(g, c[0], c[1], Math.abs(fanTop[1] - c[1]) * 1.1, { a0: Math.PI, a1: TAU, ribs: 11, fill: C.gold1, ring: .25 });
  gline(g, [P(0, 100, 40), P(0, 140, 40)], { w: 3, glow: .5 });
  const sp = P(0, 141, 40); glow(g, sp[0], sp[1], 60, CRIM_L, .6);
  D.vignette(g, W, H, .5);
}
// city seen from above: the lit lamps spell «نور»
let SIGN = null;
function citySign() { if (!SIGN) SIGN = wordSign(); return SIGN; }
function wordSign() {
  // the whole word as one shape (Arabic letters must keep their joins): raster → skeleton → bulbs
  const s = B.buildSign('نور', { font: FONT_AR, weight: 700, size: 760, spacing: 34, track: 0, whole: true });
  return s;
}
function city(g, t, zoom, cx, cy, roll = 0, litK = 1) {
  const sign = citySign();
  g.fillStyle = '#07090c'; g.fillRect(0, 0, W, H);
  g.save(); g.translate(AX, H * .46); g.rotate(roll); g.scale(zoom, zoom); g.translate(-cx, -cy);
  // river (emerald), blocks, streets
  const rv = []; for (let i = 0; i <= 40; i++) { const y = -1200 + i * 110; rv.push([1050 + Math.sin(i * .35) * 140, y]); }
  g.save(); g.lineWidth = 170; g.strokeStyle = '#0c3a2f'; g.lineCap = 'round'; g.stroke(toPath(rv)); g.lineWidth = 120; g.strokeStyle = '#11493b'; g.stroke(toPath(rv)); g.restore();
  gline(g, D.offsetPoly(rv, 85), { w: 1.4, alpha: .8 }); gline(g, D.offsetPoly(rv, -85), { w: 1.4, alpha: .8 });
  const G = 60;
  for (let x = -900; x < 1800; x += G) gline(g, [[x, -1300], [x, 3200]], { w: 1, alpha: .28 });
  for (let y = -1300; y < 3200; y += G) gline(g, [[-900, y], [1800, y]], { w: 1, alpha: .28 });
  // rooftops: a few deco blocks (fish-scale domes)
  for (let i = 0; i < 26; i++) {
    const bx = -900 + Math.floor(hash(i * 2.1) * 45) * G, by = -1300 + Math.floor(hash(i * 5.7) * 75) * G;
    g.fillStyle = 'rgba(40,32,22,.6)'; g.fillRect(bx + 6, by + 6, G - 12, G - 12);
  }
  // the dark lamps (grid) and the lit ones (the sign), sign centred at (0,0) of its own frame → world (OX,OY)
  const bl = sign.letters.flatMap(le => le.bulbs), bx = bl.map(p => p[0]), by = bl.map(p => p[1]);
  const OX = 540 - (Math.min(...bx) + Math.max(...bx)) / 2, OY = 900 - (Math.min(...by) + Math.max(...by)) / 2;
  const litPts = sign.letters.flatMap(le => le.bulbs).map(([x, y]) => [OX + x, OY + y]);
  for (let x = -900; x < 1800; x += 30) for (let y = -1300; y < 3200; y += G) {
    if (litPts.some(p => Math.abs(p[0] - x) < 26 && Math.abs(p[1] - y) < 26)) continue;
    g.fillStyle = 'rgba(120,96,60,.55)'; g.beginPath(); g.arc(x, y, 3, 0, TAU); g.fill();
  }
  for (let y = -1300; y < 3200; y += 30) for (let x = -900; x < 1800; x += G) {
    if (litPts.some(p => Math.abs(p[0] - x) < 26 && Math.abs(p[1] - y) < 26)) continue;
    g.fillStyle = 'rgba(120,96,60,.45)'; g.beginPath(); g.arc(x, y, 2.6, 0, TAU); g.fill();
  }
  B.drawSign(g, sign, OX, OY, 1, { lit: (li, bi, gi) => litK * (1 + .18 * Math.sin(t * 6 - gi * .5) * seg(t, T_WORD, T_WORD + .4)), channel: false, haloK: 1.4 });
  g.restore();
}
function sceneTower(g, t) {
  const t0 = S.tower[0];
  if (t < T_ZOOM0) {
    const pitch = lerp(.18, 1.12, eio(seg(t, t0 + .1, T_ZOOM0 - .2)));
    towerScene(g, t, pitch);
    const px = lerp(1350, 380, seg(t, t0 + 1.4, T_ZOOM1)), py = 330;
    plane(g, px, py, .9, t);
    return;
  }
  if (t < T_ZOOM1) {
    // zoom into one plane window; the city shows through it
    const px = lerp(1350, 380, seg(t, t0 + 1.4, T_ZOOM1)), py = 330, s = .9;
    const wc = [px + (-210 + 4 * 50) * s, py - 14 * s], r0 = 11 * s;
    const e = ei(seg(t, T_ZOOM0, T_ZOOM1)), k = Math.exp(lerp(0, Math.log(H / r0 * .9), e));
    const cx = lerp(wc[0], AX, ss(e)), cy = lerp(wc[1], H * .46, ss(e));
    g.save(); g.translate(cx, cy); g.scale(k, k); g.translate(-wc[0], -wc[1]);
    towerScene(g, t, 1.12); plane(g, px, py, s, t);
    g.restore();
    g.save(); g.beginPath(); g.arc(cx, cy, r0 * k, 0, TAU); g.clip();
    city(g, t, 4.2, 300, 760, .28, 1); g.globalAlpha = 1 - seg(t, T_ZOOM0, T_ZOOM0 + .5); g.fillStyle = '#ffd98a'; g.fillRect(0, 0, W, H); g.restore();
    g.beginPath(); g.arc(cx, cy, r0 * k, 0, TAU); g.strokeStyle = C.gold2; g.lineWidth = 2 * k * s; g.stroke();
    return;
  }
  // pull up over the city: scattered lights resolve into the name
  const u = eio(seg(t, T_ZOOM1, T_WORD));
  const zoom = Math.exp(lerp(Math.log(4.2), Math.log(1.45), u));
  city(g, t, zoom, lerp(300, 540, u), lerp(760, 900, u), lerp(.28, 0, u), 1);
  if (t > T_WORD) { const p = seg(t, T_WORD, T_WORD + .8); sparkle(g, 300, 700, 60 * Math.sin(Math.PI * p), { alpha: 1 }); sparkle(g, 820, 1080, 40 * Math.sin(Math.PI * seg(t, T_WORD + .3, T_WORD + 1.1)), { alpha: 1 }); }
  D.vignette(g, W, H, .5);
}

// 8 · Noor at the window (the pull-back reveals the porthole)
function sceneNoor(g, t) {
  const pc = [430, 820], R = 300;
  const e = eo(seg(t, T_PULL0, T_PULL1));
  const k = lerp(H / R * 1.05, 1, e);
  // cabin wall
  const cx = lerp(AX, pc[0], e), cy = lerp(H * .46, pc[1], e);
  g.save(); g.translate(cx, cy); g.scale(k, k); g.translate(-pc[0], -pc[1]);
  airbrush(g, [[-2000, -2000], [3000, -2000], [3000, 4000], [-2000, 4000]], { base: '#2b2130', dark: '#120d14', light: '#4a3a52', dir: -2.2 });
  for (const y of [300, 330, 1400, 1430]) gline(g, [[-200, y], [1300, y]], { w: 2 });
  D.chevrons(g, -100, 1200, 1460, { n: 14, h: 26, rows: 3, gap: 16 });
  g.restore();
  // porthole: the city through the glass
  g.save(); g.beginPath(); g.arc(cx, cy, R * k, 0, TAU); g.clip();
  city(g, t, lerp(1.45, .62, eo(seg(t, T_PULL0, T_PULL1))) * (1 + .03 * seg(t, T_PULL1, S.noor[1])), 540 + (t - T_PULL0) * 10, 900 + lerp(0, 60, eo(seg(t, T_PULL0, T_PULL1))), 0, 1);
  g.restore();
  g.save(); g.translate(cx, cy); g.scale(k, k); g.translate(-pc[0], -pc[1]);
  for (const [rr, w] of [[R, 10], [R + 18, 3], [R + 42, 2]]) gline(g, arcPts(pc[0], pc[1], rr, 0, TAU, 96), { w, glow: rr === R ? .3 : 0 });
  for (let i = 0; i < 16; i++) { const a = i * TAU / 16; D.sparkle(g, pc[0] + Math.cos(a) * (R + 30), pc[1] + Math.sin(a) * (R + 30), 0); g.beginPath(); g.arc(pc[0] + Math.cos(a) * (R + 30), pc[1] + Math.sin(a) * (R + 30), 5, 0, TAU); g.fillStyle = C.gold1; g.fill(); }
  // glass reflection
  g.save(); g.beginPath(); g.arc(pc[0], pc[1], R, 0, TAU); g.clip(); g.globalAlpha = .12; g.fillStyle = '#fff'; g.beginPath(); g.ellipse(pc[0] - 110, pc[1] - 130, 60, 200, -.6, 0, TAU); g.fill(); g.restore();
  g.restore();
  // Noor (enters as the pull-back lands)
  const nIn = eo(seg(t, T_PULL0 + .5, T_PULL1 + .4));
  if (nIn > 0) {
    g.save(); g.globalAlpha = nIn;
    noorFace(g, lerp(1000, 820, nIn), 1150, 2.6, { tear: seg(t, S.noor[0] + 1.9, S.noor[1] - .2), blink: Math.max(0, 1 - Math.abs(t - (S.noor[0] + 1.4)) / .07) });
    g.restore();
  }
  D.vignette(g, W, H, .55);
}

// 10 · end card
function sceneCard(g, t) {
  ground(g, '#0d0b09', '#050403');
  const t0 = S.card[0];
  sunburst(g, AX, 900, { rays: 64, r0: 100, r1: 1500, mode: 'wedges', colorA: 'rgba(201,162,75,.06)' });
  const off = DUR - .9;
  post(g, AX, 640, 760, 1.0); lantern(g, AX, 640, 1.3, t < off ? 1 : ignite(t, -1, off), t);
  titleAr(g, 'الضوّاي', AX, 1000, 150, seg(t, t0 + .2, t0 + 1.6));
  D.vignette(g, W, H, .6);
  TEXT('card', 'الضوّاي', AX - 300, 900, AX + 300, 1100, t >= t0 + 1.2);
}

// ================= dispatcher =================
let texts = [];
function TEXT(id, text, x0, y0, x1, y1, on) { if (on) texts.push({ id, text, x0, y0, x1, y1 }); }
const SUBCUES = [];
function render(t) {
  texts = [];
  g.setTransform(1, 0, 0, 1, 0, 0); g.globalAlpha = 1; g.globalCompositeOperation = 'source-over'; g.direction = 'ltr';
  if (t < S.title[0]) sceneHook(g, t);
  else if (t < S.street[0]) sceneTitle(g, t);
  else if (t < S.clock[0]) sceneStreet(g, t);
  else if (t < S.skip[0]) sceneClock(g, t);
  else if (t < S.tele[0]) sceneSkip(g, t);
  else if (t < S.face[0]) sceneTele(g, t);
  else if (t < S.tower[0]) sceneFace(g, t);
  else if (t < S.noor[0]) sceneTower(g, t);
  else if (t < S.end[0]) sceneNoor(g, t);
  else if (t < S.card[0]) sceneEnd(g, t);
  else sceneCard(g, t);
  leaves(g, leafK(t), t);
  for (const c of SUBCUES) if (t >= c.t0 - .25 && t < c.t1 + .3) subtitle(g, c.text, Math.min(seg(t, c.t0 - .25, c.t0 + .1), 1 - seg(t, c.t1, c.t1 + .3) * 0) * (1 - seg(t, c.t1, c.t1 + .3)));
}
window.TEXTS = t => { render(t); return texts; };

// ================= events for the mixer =================
function buildEvents(dur) {
  const EV = [];
  for (const [id, t] of Object.entries(VO)) EV.push({ t, type: 'vo', id, dur: dur[id] });
  EV.push({ t: T_IGN, type: 'ignite', pan: 0, gain: 1 });
  // clock ticks in the hook
  for (let tt = .1; tt < T_IGN; tt += BEAT) EV.push({ t: tt, type: 'tick', gain: .7 });
  // street: lamps ignite down the street + steps
  let tc = S.street[0] + .55; LAMPZ.forEach((z, i) => { EV.push({ t: tc, type: 'ignite', pan: -.3, gain: .7 * (1 - i / 14) }); EV.push({ t: tc + .06, type: 'ignite', pan: .3, gain: .6 * (1 - i / 14) }); tc += i < 4 ? BEAT : i < 7 ? BEAT / 2 : BEAT / 4; });
  for (let tt = S.street[0] + .1; tt < S.street[1]; tt += 1 / 1.8) EV.push({ t: tt, type: 'step', gain: .4 });
  // clock shot
  for (let k = 0; k < 6; k++) EV.push({ t: S.clock[0] + k, type: 'tick', gain: .8 });
  EV.push({ t: S.clock[0] + BEAT * 4, type: 'clunk', gain: .9 });
  // skip shot
  const t0 = S.skip[0], walk0 = t0 + 1.55, walk1 = t0 + 5.9;
  EV.push({ t: t0 + 1.0, type: 'ignite', pan: .2, gain: .9 });
  for (let i = 1; i <= 10; i++) EV.push({ t: lerp(walk0, walk1, (i - .5) / 10.5), type: 'skip', n: i });
  for (let tt = walk0; tt < walk1; tt += 1 / 3.2) EV.push({ t: tt, type: 'step', gain: .45 });
  EV.push({ t: walk1 + .55, type: 'ignite', pan: -.1, gain: .9 });
  for (let r = 0; r < 3; r++) for (let c = 0; c < 18; c++) { const o = S.skip[1] - 2.85 + ((r * 7 + c * 3) % 9) * BEAT / 3; if ((r + c) % 4 === 0) EV.push({ t: o, type: 'shutter', pan: ((c % 5) - 2) / 3, gain: .5 }); }
  // telegram ticks while typing
  for (let tt = VO.l6 - .1; tt < VO.l6 + 4.2; tt += .085) EV.push({ t: tt, type: 'tele', gain: .35 });
  // silence before the reveal: a clock and a far propeller (J-cut into the tower shot)
  for (let k = 0; k < 3; k++) EV.push({ t: 43.1 + k, type: 'tick', gain: .6 });
  EV.push({ t: 43.6, type: 'prop', t1: T_ZOOM1 + .3, gain: 1 });
  EV.push({ t: T_ZOOM0, type: 'whoosh', gain: .8 });
  EV.push({ t: T_WORD, type: 'reveal', gain: 1 });
  EV.push({ t: S.noor[0] + 1.9, type: 'sparkle', gain: .7 });
  // ending: lamps go out
  const off0 = S.end[0] + BEAT; for (let i = 1; i <= 10; i++) { const n = 10 - i; EV.push({ t: off0 + n * BEAT * .6, type: 'off', pan: .25, gain: .6 }); EV.push({ t: off0 + n * BEAT * .6 + .1, type: 'off', pan: -.25, gain: .5 }); }
  EV.push({ t: 63.7, type: 'blink', gain: .5 }); EV.push({ t: 64.3, type: 'blink', gain: .5 });
  EV.push({ t: DUR - .9, type: 'off', pan: 0, gain: .8 });
  for (const c of CUTS) { EV.push({ t: c - LEAF, type: 'leaf', gain: .55 }); EV.push({ t: c, type: 'seam', gain: .6 }); }
  EV.push({ t: S.street[0], type: 'leafopen', gain: .55 });
  EV.push({ t: S.title[0] + .1, type: 'title', gain: .8 }); EV.push({ t: S.card[0] + .2, type: 'title', gain: .7 });
  EV.push({ t: 0, type: 'grid', bpm: BPM, sections: S, dur: DUR, zoom0: T_ZOOM0, zoom1: T_ZOOM1, word: T_WORD });
  return EV.sort((a, c) => a.t - c.t);
}

// ================= boot =================
(async () => {
  await Promise.all(['700 64px Kufi', '600 46px Kufi', '700 64px Amiri', '40px Italiana', '40px Poiret'].map(f => document.fonts.load(f, 'نور abc')));
  await document.fonts.ready;
  const lines = await (await fetch('lines.json')).json();
  const dur = await (await fetch('voice/dur.json')).json();
  for (const L of lines) SUBCUES.push({ t0: VO[L.id], t1: Math.max(VO[L.id] + 1.8, VO[L.id] + dur[L.id] + .6), text: L.text.replace(/\.\.\./g, '…') });
  for (let i = 0; i + 1 < SUBCUES.length; i++) SUBCUES[i].t1 = Math.min(SUBCUES[i].t1, SUBCUES[i + 1].t0 - .35);
  window.SUBCUES = SUBCUES;
  window.EV = buildEvents(dur);
  wordSign();
  window.render = render;
  window.READY = true;
})();
