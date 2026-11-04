// Characters of «الضوّاي», drawn the deco way: faceted lacquer planes, airbrush, gold rim on the lit side.
// Abu Noor: tall streamline figure, crimson coat (the film's one accent), black sidara cap with gold piping, grey moustache, brass lamp pole.
// Noor: crimson headscarf (same accent: father and daughter rhyme).
import { C, TAU, clamp, lerp, mix, rgba, gline, airbrush, glow, sparkle, toPath, goldGrad } from './engine/deco.js';

export const CRIM = '#a01c2c', CRIM_D = '#4e0b14', CRIM_L = '#d4475a';
const SKIN = C.skin, SKIN_D = C.skinD, SKIN_L = C.skinL;
const CAP = '#14100c';

// ---------- helpers ----------
const T = (pts, x, y, s, flip = 1) => pts.map(([a, b]) => [x + a * s * flip, y + b * s]);
function poly(g, pts, o) { return airbrush(g, pts, o); }
function rimLine(g, pts, w = 1.6, closed = true) { gline(g, pts, { w, closed }); }

// pole tip: brass hook + small flame (lit 0..1)
export function poleTip(g, x, y, s, lit = 1, t = 0) {
  g.save();
  g.strokeStyle = goldGrad(g, x - 20 * s, y - 20 * s, x + 20 * s, y + 20 * s, { sheen: .4 }); g.lineWidth = 3 * s; g.lineCap = 'round';
  g.beginPath(); g.moveTo(x, y + 26 * s); g.lineTo(x, y + 6 * s); g.stroke();
  g.beginPath(); g.arc(x + 6 * s, y + 6 * s, 6 * s, Math.PI, TAU * .98); g.stroke();
  if (lit > 0) {
    const fl = 1 + .12 * Math.sin(t * 37) + .08 * Math.sin(t * 23.3);
    glow(g, x, y - 2 * s, 34 * s * fl, '#ffb050', .55 * lit);
    g.beginPath(); g.moveTo(x, y - 14 * s * fl); g.quadraticCurveTo(x + 5 * s, y - 2 * s, x, y + 3 * s); g.quadraticCurveTo(x - 5 * s, y - 2 * s, x, y - 14 * s * fl);
    g.fillStyle = rgba('#ffe2a0', lit); g.fill();
  }
  g.restore();
}

// ---------- Abu Noor, side view (facing left by default; flip=-1 faces right) ----------
// o: phase (walk 0..1, stepped by caller), walk (0..1 amount), reach (0..1 raise pole to lamp), poleLit, t
export function abuSide(g, x, y, s, o = {}) {
  const { phase = 0, walk = 1, reach = 0, poleLit = 1, t = 0, flip = 1, alpha = 1 } = o;
  g.save(); g.globalAlpha *= alpha;
  const ph = phase * TAU, sw = Math.sin(ph) * walk, bob = Math.abs(Math.cos(ph)) * walk * 4;
  const Y = y - bob * s * .3;
  const P = pts => T(pts, x, Y, s, flip);
  // figure units: feet at 0, head top at -330 (≈7 heads of 47)
  // legs (far leg darker)
  const leg = (k, dark) => {
    const a = k * sw * .42;
    const hip = [0, -150], knee = [Math.sin(a) * 70 - 4, -150 + Math.cos(a) * 72], foot = [Math.sin(a * 1.25) * 140 - 4, -6];
    const L = [[hip[0] - 13, hip[1]], [hip[0] + 13, hip[1]], [knee[0] + 10, knee[1]], [foot[0] + 7, foot[1] - 4], [foot[0] - 9, foot[1] - 4], [knee[0] - 11, knee[1]]];
    poly(g, P(L), { base: dark ? '#1a1612' : '#2a241d', dir: -2.3 });
    const shoe = [[foot[0] - 12, -8], [foot[0] + 14, -10], [foot[0] + 22, -2], [foot[0] + 18, 0], [foot[0] - 12, 0]].map(([a, b]) => [-a, b]).map(([a, b]) => [-a, b]);
    // shoe points forward (towards -x when flip=1)
    const sh = [[foot[0] + 10, -10], [foot[0] - 22, -6], [foot[0] - 24, 0], [foot[0] + 10, 0]];
    poly(g, P(sh), { base: '#0e0b08', rim: dark ? 0 : 1 });
  };
  leg(-1, true);
  // far arm (holds pole low hand)
  const reachA = lerp(.25, -1.05, reach);           // shoulder angle of the pole arm
  // coat (long, to below the knee) — faceted
  const sway = sw * 6;
  const coat = [[-34, -262], [30, -262], [42, -200], [48, -95 + sway * .3], [36, -84], [-46 - sway, -88], [-50 - sway * .6, -110], [-40, -205]];
  poly(g, P(coat), { base: CRIM, dark: CRIM_D, light: CRIM_L, dir: flip > 0 ? -2.3 : -.8, rim: 1.4 });
  // facet plane (shadow side)
  poly(g, P([[6, -262], [30, -262], [42, -200], [48, -95 + sway * .3], [36, -84], [10, -86], [16, -180]]), { base: mix(CRIM, '#000', .35), dark: CRIM_D, dir: -2.3, alpha: .7 });
  gline(g, P([[-8, -250], [-12, -92]]), { w: 1.2, alpha: .8 });   // front edge seam
  gline(g, P([[-46, -150], [44, -150]]), { w: 1.8 });             // belt line
  // neck + head
  poly(g, P([[-10, -280], [8, -280], [9, -258], [-11, -258]]), { base: SKIN_D });
  const head = [[-22, -318], [6, -326], [20, -312], [20, -290], [10, -276], [-12, -272], [-24, -282], [-30, -296], [-26, -300]];
  poly(g, P(head), { base: SKIN, dark: SKIN_D, light: SKIN_L, dir: -2.4, rim: 1 });
  // nose & moustache (face looks to -x)
  gline(g, P([[-26, -300], [-33, -290], [-26, -288]]), { w: 1.4, closed: false });
  poly(g, P([[-30, -286], [-14, -289], [-8, -282], [-20, -280], [-31, -280]]), { base: '#d9d2c4', dark: '#8f877a', rim: 0 });
  // eye
  g.save(); g.fillStyle = '#1b1310'; g.beginPath(); const e = P([[-18, -303]])[0]; g.ellipse(e[0], e[1], 4.5 * s, 2 * s, 0, 0, TAU); g.fill(); g.restore();
  gline(g, P([[-25, -308], [-12, -310]]), { w: 1.2, closed: false, color: '#cfc6b6' });
  // sidara cap (boat-shaped, pinched top)
  const cap = [[-28, -312], [24, -314], [26, -322], [10, -336], [-4, -330], [-18, -338], [-30, -322]];
  poly(g, P(cap), { base: CAP, dark: '#000', light: '#3a2f22', rim: 0 });
  gline(g, P([[-28, -313], [24, -315]]), { w: 1.6, closed: false });
  gline(g, P([[-6, -331], [-4, -315]]), { w: 1, closed: false });
  // near arm + pole. Hand position depends on reach.
  const sh = [6, -250];
  const ua = lerp(.35, -1.6, reach) + sw * .25 * (1 - reach), fa = lerp(-.25, -2.0, reach) + sw * .2 * (1 - reach);
  const el = [sh[0] + Math.sin(ua) * -70, sh[1] + Math.cos(ua) * 70];
  const ha = [el[0] + Math.sin(fa) * -62, el[1] + Math.cos(fa) * 62];
  const arm = (a, b, w) => { const dx = b[0] - a[0], dy = b[1] - a[1], L = Math.hypot(dx, dy) || 1, nx = -dy / L * w, ny = dx / L * w; return [[a[0] + nx, a[1] + ny], [b[0] + nx * .8, b[1] + ny * .8], [b[0] - nx * .8, b[1] - ny * .8], [a[0] - nx, a[1] - ny]]; };
  // pole: from hand, angled forward-up; length 300
  const pa = lerp(-2.55, -1.75, reach);           // angle of the pole (screen, pointing up-forward)
  const pl = 310;
  const p0 = [ha[0] - Math.cos(pa) * 70, ha[1] - Math.sin(pa) * 70], p1 = [ha[0] + Math.cos(pa) * pl, ha[1] + Math.sin(pa) * pl];
  const PP = P([p0, p1]);
  g.save(); g.strokeStyle = goldGrad(g, PP[0][0], PP[0][1], PP[1][0], PP[1][1], { sheen: .45 }); g.lineWidth = 4 * s; g.lineCap = 'round';
  g.beginPath(); g.moveTo(PP[0][0], PP[0][1]); g.lineTo(PP[1][0], PP[1][1]); g.stroke(); g.restore();
  poleTip(g, PP[1][0], PP[1][1] - 8 * s, s * .9, poleLit, t);
  poly(g, P(arm(sh, el, 11)), { base: mix(CRIM, '#000', .1), dark: CRIM_D, light: CRIM_L, rim: 1 });
  poly(g, P(arm(el, ha, 9)), { base: mix(CRIM, '#000', .1), dark: CRIM_D, light: CRIM_L, rim: 1 });
  const hp = P([ha])[0]; g.beginPath(); g.arc(hp[0], hp[1], 8 * s, 0, TAU); g.fillStyle = SKIN_D; g.fill();
  leg(1, false);
  g.restore();
  return { tip: PP[1] };
}

// ---------- Abu Noor, back view (walking away / standing on the axis) ----------
export function abuBack(g, x, y, s, o = {}) {
  const { phase = 0, walk = 1, t = 0, poleLit = 1, alpha = 1, wave = 0, lookUp = 0 } = o;
  g.save(); g.globalAlpha *= alpha;
  const ph = phase * TAU, sw = Math.sin(ph) * walk;
  const P = pts => T(pts, x, y, s);
  // legs: alternate lift
  for (const k of [-1, 1]) {
    const lift = Math.max(0, k * sw) * 16;
    poly(g, P([[k * 6 - 12, -150], [k * 6 + 12, -150], [k * 10 + 9, -6 - lift], [k * 10 - 9, -6 - lift]]), { base: '#221d17' });
    poly(g, P([[k * 10 - 11, -10 - lift], [k * 10 + 11, -10 - lift], [k * 10 + 10, -lift], [k * 10 - 10, -lift]]), { base: '#0d0a07' });
  }
  const coat = [[-38, -262], [38, -262], [50, -190], [56, -90], [-56, -90], [-50, -190]];
  poly(g, P(coat), { base: CRIM, dark: CRIM_D, light: CRIM_L, dir: -2.0, rim: 1.4 });
  poly(g, P([[0, -262], [38, -262], [50, -190], [56, -90], [0, -90]]), { base: mix(CRIM, '#000', .4), dark: CRIM_D, alpha: .55 });
  gline(g, P([[0, -240], [0, -92]]), { w: 1.2, alpha: .8 });
  gline(g, P([[-52, -150], [52, -150]]), { w: 1.8 });
  // head from behind
  poly(g, P([[-10, -282], [10, -282], [11, -260], [-11, -260]]), { base: SKIN_D });
  const hy = -300 - lookUp * 4;
  g.save(); const hc = P([[0, hy]])[0]; g.beginPath(); g.ellipse(hc[0], hc[1], 21 * s, 25 * s, 0, 0, TAU);
  const gr = g.createLinearGradient(hc[0] - 20 * s, hc[1] - 20 * s, hc[0] + 20 * s, hc[1] + 20 * s); gr.addColorStop(0, '#7d7568'); gr.addColorStop(1, '#2a2622'); g.fillStyle = gr; g.fill(); g.restore();
  const cap = [[-24, hy - 12], [24, hy - 12], [22, hy - 26], [0, hy - 36 + lookUp * 6], [-22, hy - 26]];
  poly(g, P(cap), { base: CAP, light: '#3a2f22' });
  gline(g, P([[-24, hy - 12], [24, hy - 12]]), { w: 1.6, closed: false });
  // right arm holds pole up over the shoulder; left arm swings or waves
  const la = wave > 0 ? lerp(.2, -2.6, wave) + Math.sin(t * 9) * .25 * wave : sw * .3;
  const ls = [-38, -250], le = [ls[0] - Math.sin(-la) * 0 - 10 + Math.sin(la) * -60, ls[1] + Math.cos(la) * 62];
  poly(g, P([[ls[0] - 9, ls[1]], [ls[0] + 9, ls[1]], [le[0] + 7, le[1]], [le[0] - 7, le[1]]]), { base: mix(CRIM, '#000', .15), rim: 1 });
  const lh = P([le])[0]; g.beginPath(); g.arc(lh[0], lh[1], 7 * s, 0, TAU); g.fillStyle = SKIN_D; g.fill();
  const rs = [38, -250], rh = [52, -200];
  poly(g, P([[rs[0] - 9, rs[1]], [rs[0] + 9, rs[1]], [rh[0] + 7, rh[1]], [rh[0] - 7, rh[1]]]), { base: mix(CRIM, '#000', .3), rim: 0 });
  const p0 = P([[40, -150]])[0], p1 = P([[110, -470]])[0];
  g.save(); g.strokeStyle = goldGrad(g, p0[0], p0[1], p1[0], p1[1], { sheen: .45 }); g.lineWidth = 4 * s; g.lineCap = 'round';
  g.beginPath(); g.moveTo(p0[0], p0[1]); g.lineTo(p1[0], p1[1]); g.stroke(); g.restore();
  poleTip(g, p1[0], p1[1] - 8 * s, s * .9, poleLit, t);
  g.restore();
}

// ---------- Abu Noor, close-up 3/4 (faces screen-left), big ----------
// look: 0 = level, 1 = looking up at the sky. blink 0..1.
export function abuFace(g, cx, cy, s, o = {}) {
  const { look = 0, blink = 0, light = 1, t = 0 } = o;
  g.save();
  g.translate(cx, cy); g.rotate(-.16 * look); g.translate(-cx, -cy);
  const P = pts => T(pts, cx, cy, s);
  // shoulders + coat collar
  poly(g, P([[-260, 330], [-150, 150], [-60, 120], [90, 120], [210, 170], [300, 330], [300, 520], [-260, 520]]), { base: CRIM, dark: CRIM_D, light: CRIM_L, dir: -2.4, rim: 2 });
  poly(g, P([[-90, 125], [-20, 260], [10, 135]]), { base: '#e9dfcc', dark: '#a69a85' });      // shirt
  gline(g, P([[-150, 150], [-20, 330], [90, 120]]), { w: 2.2, closed: false });                 // lapel keyline
  gline(g, P([[-60, 125], [-20, 260], [10, 135]]), { w: 1.4, closed: false });
  // neck
  poly(g, P([[-62, 40], [40, 40], [44, 140], [-50, 150]]), { base: SKIN_D, dark: '#8a5a3e' });
  // head (3/4, faceted). Face side towards -x.
  // profile-ish 3/4 head: forehead → brow → nose → lip → chin → jaw → back of head
  const head = [[-118, -150], [-60, -205], [40, -210], [100, -160], [112, -60], [96, 20], [60, 70], [6, 104], [-60, 104], [-100, 92], [-118, 74], [-116, 54],
    [-124, 40], [-128, 30], [-150, 20], [-140, -6], [-128, -40], [-130, -62], [-118, -90]];
  poly(g, P(head), { base: SKIN, dark: SKIN_D, light: SKIN_L, dir: -2.5, rim: 2.2 * light });
  // shadow plane (cheek side away from the light)
  poly(g, P([[30, -190], [100, -160], [112, -60], [96, 20], [60, 70], [20, 86], [40, -40]]), { base: mix(SKIN_D, '#5a2d1c', .3), dark: '#5c3422', alpha: .55 });
  // ear
  poly(g, P([[62, -70], [86, -84], [98, -50], [84, -14], [64, -20]]), { base: SKIN_D, light: SKIN });
  gline(g, P([[70, -60], [84, -66], [88, -40]]), { w: 1, closed: false, color: '#8a5a3e' });
  // grey temple hair
  poly(g, P([[50, -150], [100, -158], [108, -96], [82, -96], [60, -120]]), { base: '#bdb5a6', dark: '#6b655c' });
  // eyebrow (raises with look)
  const by = -70 - look * 10;
  poly(g, P([[-118, by + 4], [-92, by - 10], [-48, by - 8], [-44, by], [-90, by + 2]]), { base: '#d8d0c2', dark: '#7c7568' });
  // eye: almond, pupil goes up with look
  const ey = -40, ex = -80;
  const open = 1 - blink;
  g.save(); g.beginPath(); const e0 = P([[ex - 24, ey], [ex, ey - 12 * open], [ex + 24, ey - 2], [ex, ey + 8 * open]]);
  g.moveTo(e0[0][0], e0[0][1]); g.quadraticCurveTo(e0[1][0], e0[1][1] - 6 * s, e0[2][0], e0[2][1]); g.quadraticCurveTo(e0[3][0], e0[3][1] + 4 * s, e0[0][0], e0[0][1]);
  g.fillStyle = '#efe6d6'; g.fill(); g.clip();
  const pu = P([[ex - 7, ey - 2 - look * 7]])[0];
  g.beginPath(); g.arc(pu[0], pu[1], 10 * s, 0, TAU); g.fillStyle = '#2b1a12'; g.fill();
  g.beginPath(); g.arc(pu[0] - 3 * s, pu[1] - 3 * s, 3 * s, 0, TAU); g.fillStyle = rgba('#fff4d2', .9); g.fill();
  g.restore();
  gline(g, P([[ex - 26, ey - 1], [ex - 4, ey - 15 * open], [ex + 26, ey - 3]]), { w: 2, closed: false, color: '#3b2418' });
  gline(g, P([[ex - 16, ey + 18], [ex + 18, ey + 16]]), { w: 1, closed: false, color: '#9a6a4c', alpha: .7 });   // under-eye line (age)
  // nose: one stroke along the bridge + nostril
  gline(g, P([[-112, -52], [-122, 0], [-108, 18]]), { w: 1.6, closed: false, color: '#9a5c40', alpha: .8 });
  // moustache (grey, faceted) under the nose, inside the face
  poly(g, P([[-132, 34], [-104, 24], [-70, 30], [-52, 50], [-82, 50], [-108, 46], [-130, 50]]), { base: '#ddd5c6', dark: '#7f786c', rim: 1 });
  gline(g, P([[-120, 66], [-82, 64]]), { w: 1.6, closed: false, color: '#6a3324' });
  // cheek line
  gline(g, P([[-44, 4], [-40, 56]]), { w: 1, closed: false, color: '#9a6a4c', alpha: .6 });
  // sidara cap
  const cap = [[-142, -150], [110, -168], [104, -196], [60, -232], [0, -224], [-40, -250], [-120, -214]];
  poly(g, P(cap), { base: CAP, dark: '#000', light: '#40342a', rim: 0 });
  gline(g, P([[-142, -150], [110, -168]]), { w: 2.6, closed: false, glow: .3 * light });
  gline(g, P([[-38, -246], [-24, -160]]), { w: 1.4, closed: false });
  g.restore();
}

// ---------- Noor in profile (faces screen-left), crimson headscarf ----------
export function noorFace(g, cx, cy, s, o = {}) {
  const { tear = 0, blink = 0, smile = 0 } = o;
  const P = pts => T(pts, cx, cy, s);
  g.save();
  // scarf back mass
  poly(g, P([[-40, -190], [60, -200], [140, -120], [160, 40], [140, 230], [-10, 260], [10, 120], [30, -40]]), { base: CRIM, dark: CRIM_D, light: CRIM_L, dir: -2.6, rim: 1.6 });
  // face profile
  const face = [[-50, -130], [0, -150], [40, -120], [40, 40], [20, 110], [-20, 118], [-50, 96], [-60, 74], [-74, 60], [-66, 50], [-78, 36], [-70, 24], [-74, 0], [-100, -30], [-78, -40], [-68, -80]];
  poly(g, P(face), { base: SKIN, dark: SKIN_D, light: SKIN_L, dir: -2.8, rim: 1.4 });
  // neck
  poly(g, P([[-30, 110], [30, 100], [36, 220], [-20, 230]]), { base: SKIN_D });
  // scarf front fold over the head (frames the face)
  poly(g, P([[-62, -120], [-20, -175], [50, -185], [80, -120], [60, -60], [40, -110], [0, -138], [-52, -112]]), { base: mix(CRIM, '#fff', .08), dark: CRIM_D, light: CRIM_L, rim: 1.4 });
  poly(g, P([[30, -20], [60, -60], [80, 60], [60, 200], [20, 220], [30, 110]]), { base: mix(CRIM, '#000', .25), dark: CRIM_D });
  gline(g, P([[-60, -116], [-18, -170], [50, -182]]), { w: 1.6, closed: false });
  // eye (looking down-left)
  const open = 1 - blink;
  g.save(); const e = P([[-44, -36]])[0];
  g.beginPath(); g.ellipse(e[0], e[1], 14 * s, 6 * s * open + .5, -.15, 0, TAU); g.fillStyle = '#efe6d6'; g.fill();
  g.beginPath(); g.arc(e[0] - 6 * s, e[1] + 2 * s, 5 * s * open, 0, TAU); g.fillStyle = '#2b1a12'; g.fill();
  g.restore();
  gline(g, P([[-60, -42], [-44, -46], [-28, -40]]), { w: 2, closed: false, color: '#2b1a12' });
  gline(g, P([[-62, -60], [-30, -66]]), { w: 1.6, closed: false, color: '#3a2418' });
  // lips
  poly(g, P([[-74, 58], [-62, 52], [-52, 60], [-62, 66]]), { base: '#b4485a', dark: '#6e2030' });
  if (tear > 0) {
    const ty = lerp(-28, 40, tear);
    const tp = P([[-56, ty]])[0];
    g.beginPath(); g.ellipse(tp[0], tp[1], 3 * s, 4.5 * s, 0, 0, TAU); g.fillStyle = rgba('#fff4d2', .85); g.fill();
    sparkle(g, tp[0], tp[1], 18 * s * Math.sin(Math.PI * clamp(tear)), { alpha: .9 });
  }
  g.restore();
}
