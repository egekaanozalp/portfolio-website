(function () {
  'use strict';

  const canvas = document.getElementById('space-canvas');
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  ctx.imageSmoothingEnabled = false;

  const PX = 3; // size of one "pixel block" in actual pixels
  let W, H, vW, vH;

  // Seeded deterministic RNG (XORshift)
  function makeRng(seed) {
    let s = seed >>> 0;
    return function () {
      s ^= s << 13; s ^= s >>> 17; s ^= s << 5;
      return (s >>> 0) / 0xFFFFFFFF;
    };
  }

  // ── Stars ──────────────────────────────────────────────────────────────────

  let stars = [];

  function initStars() {
    const rng = makeRng(0xDEADBEEF);
    const count = Math.max(100, Math.floor(vW * vH / 48));
    stars = [];
    for (let i = 0; i < count; i++) {
      const warm = rng() < 0.2;
      stars.push({
        x: Math.floor(rng() * vW),
        y: Math.floor(rng() * vH),
        size: rng() < 0.87 ? 1 : 2,
        base: 0.35 + rng() * 0.65,
        freq: 0.4 + rng() * 1.6,
        phase: rng() * Math.PI * 2,
        r: warm ? 255 : 190 + Math.floor(rng() * 65),
        g: warm ? 210 + Math.floor(rng() * 45) : 215 + Math.floor(rng() * 40),
        b: warm ? 140 + Math.floor(rng() * 60) : 255,
      });
    }
  }

  function drawStars(t) {
    for (const s of stars) {
      const a = s.base * (0.5 + 0.5 * Math.sin(t * s.freq + s.phase));
      ctx.fillStyle = `rgba(${s.r},${s.g},${s.b},${a.toFixed(2)})`;
      ctx.fillRect(s.x * PX, s.y * PX, s.size * PX, s.size * PX);
    }
  }

  // ── Planets ────────────────────────────────────────────────────────────────

  // Smooth lighting per pixel using dot product with a top-left light source
  function planetColor(dx, dy, r, colors, bands) {
    for (const b of bands) {
      if (dy >= b.yMin && dy <= b.yMax) return b.color;
    }
    const dot = (-dx * 0.55 - dy * 0.45) / r; // [-1, 1]
    const t = (dot + 1) / 2; // [0, 1]
    if (t > 0.62) return colors.light;
    if (t > 0.28) return colors.mid;
    return colors.dark;
  }

  function buildPlanet(def) {
    const r = def.r;
    const ring = def.ring;
    const padX = ring ? Math.ceil(r * ring.rx) + 2 : 0;
    const padY = ring ? Math.ceil(r * ring.ry) + 2 : 0;
    const cw = (r * 2 + 2 + padX * 2) * PX;
    const ch = (r * 2 + 2 + padY * 2) * PX;

    const oc = document.createElement('canvas');
    oc.width = cw;
    oc.height = ch;
    const octx = oc.getContext('2d');
    octx.imageSmoothingEnabled = false;

    const cx = r + 1 + padX; // planet center in virtual coords within oc
    const cy = r + 1 + padY;

    const drawRing = (startA, endA) => {
      if (!ring) return;
      const rx = r * ring.rx * PX;
      const ry = r * ring.ry * PX;
      octx.save();
      octx.beginPath();
      octx.ellipse(cx * PX, cy * PX, rx, ry, ring.tilt, startA, endA);
      const grd = octx.createLinearGradient(cx * PX - rx, cy * PX, cx * PX + rx, cy * PX);
      grd.addColorStop(0,    'transparent');
      grd.addColorStop(0.10, ring.edge);
      grd.addColorStop(0.32, ring.core);
      grd.addColorStop(0.50, ring.core);
      grd.addColorStop(0.68, ring.core);
      grd.addColorStop(0.90, ring.edge);
      grd.addColorStop(1,    'transparent');
      octx.strokeStyle = grd;
      octx.lineWidth = ring.width * PX;
      octx.stroke();
      octx.restore();
    };

    // Ring back half (behind planet)
    drawRing(Math.PI, 2 * Math.PI);

    // Planet body
    for (let dy = -r; dy <= r; dy++) {
      for (let dx = -r; dx <= r; dx++) {
        if (dx * dx + dy * dy <= r * r) {
          octx.fillStyle = planetColor(dx, dy, r, def.colors, def.bands || []);
          octx.fillRect((cx + dx) * PX, (cy + dy) * PX, PX, PX);
        }
      }
    }

    // Specular highlight
    const hx = Math.round(cx - r * 0.32);
    const hy = Math.round(cy - r * 0.38);
    octx.fillStyle = 'rgba(255,255,255,0.55)';
    octx.fillRect(hx * PX, hy * PX, PX, PX);
    if (r >= 7) {
      octx.fillStyle = 'rgba(255,255,255,0.28)';
      octx.fillRect((hx + 1) * PX, hy * PX, PX, PX);
      octx.fillRect(hx * PX, (hy + 1) * PX, PX, PX);
    }

    // Ring front half (in front of planet)
    drawRing(0, Math.PI);

    return { canvas: oc, cx, cy };
  }

  const PLANET_DEFS = [
    // Blue ocean planet — upper right
    {
      xf: 0.80, yf: 0.18, r: 9,
      colors: { light: '#80d4ff', mid: '#2e8fd4', dark: '#0c3a6e' },
      bands: [
        { yMin: -3, yMax: -1, color: '#56baf2' },
        { yMin:  2, yMax:  4, color: '#1a66b0' },
      ],
    },
    // Saturn — mid left
    {
      xf: 0.08, yf: 0.54, r: 13,
      colors: { light: '#f6e290', mid: '#d0a03a', dark: '#7c5a12' },
      bands: [
        { yMin: -5, yMax: -3, color: '#eace55' },
        { yMin: -1, yMax:  1, color: '#c89030' },
        { yMin:  3, yMax:  6, color: '#b07418' },
      ],
      ring: {
        core: 'rgba(218,172,68,0.62)',
        edge: 'rgba(195,145,50,0.22)',
        rx: 2.45, ry: 0.50, tilt: -0.22, width: 4.5,
      },
    },
    // Red-orange small planet — lower right
    {
      xf: 0.88, yf: 0.80, r: 5,
      colors: { light: '#ff9272', mid: '#d03818', dark: '#6c0e00' },
      bands: [
        { yMin: -2, yMax: -1, color: '#e86040' },
      ],
    },
    // Purple planet — lower left
    {
      xf: 0.25, yf: 0.82, r: 8,
      colors: { light: '#d4a8ff', mid: '#7c3abf', dark: '#2e0d5c' },
      bands: [
        { yMin: -3, yMax: -2, color: '#b07aee' },
        { yMin:  2, yMax:  4, color: '#5a1fa0' },
      ],
    },
  ];

  let planetImages = [];

  function buildPlanets() {
    planetImages = PLANET_DEFS.map(buildPlanet);
  }

  function drawPlanets() {
    PLANET_DEFS.forEach((def, i) => {
      const { canvas: oc, cx, cy } = planetImages[i];
      ctx.drawImage(oc,
        Math.round(def.xf * W) - cx * PX,
        Math.round(def.yf * H) - cy * PX
      );
    });
  }

  // ── Galaxies ───────────────────────────────────────────────────────────────

  const GALAXY_DEFS = [
    { xf: 0.50, yf: 0.1, arms: 3, dots: 75, maxR: 28, hue: 210, tilt: 0.5 },
    { xf: 0.58, yf: 0.78, arms: 2, dots: 48, maxR: 17, hue: 270, tilt: 1.1 },
  ];

  let galaxyImg = null;

  function buildGalaxies() {
    const oc = document.createElement('canvas');
    oc.width = W; oc.height = H;
    const octx = oc.getContext('2d');
    const rng = makeRng(0xCAFEBABE);

    for (const g of GALAXY_DEFS) {
      const cx = g.xf * vW;
      const cy = g.yf * vH;

      for (let arm = 0; arm < g.arms; arm++) {
        const base = (arm / g.arms) * Math.PI * 2 + g.tilt;
        for (let i = 0; i < g.dots; i++) {
          const t = i / g.dots;
          const angle = base + t * Math.PI * 2.9;
          const rad = t * g.maxR;
          const spread = rad * 0.32;
          const x = cx + Math.cos(angle) * rad + (rng() - 0.5) * spread;
          const y = cy + Math.sin(angle) * rad * 0.44 + (rng() - 0.5) * spread * 0.38;
          const a = ((1 - t * 0.72) * 0.68).toFixed(2);
          const dotSz = t < 0.12 ? 2 : 1;
          octx.fillStyle = `hsla(${g.hue},65%,78%,${a})`;
          octx.fillRect(Math.round(x) * PX, Math.round(y) * PX, dotSz * PX, dotSz * PX);
        }
      }

      // Glowing core
      const grd = octx.createRadialGradient(
        g.xf * W, g.yf * H, 0,
        g.xf * W, g.yf * H, 9 * PX
      );
      grd.addColorStop(0,   `hsla(${g.hue},80%,92%,0.9)`);
      grd.addColorStop(0.4, `hsla(${g.hue},70%,80%,0.35)`);
      grd.addColorStop(1,   'transparent');
      octx.fillStyle = grd;
      octx.fillRect(g.xf * W - 9 * PX, g.yf * H - 9 * PX, 18 * PX, 18 * PX);
    }

    galaxyImg = oc;
  }

  // ── Nebula colour clouds ───────────────────────────────────────────────────

  const NEBULA_DEFS = [
    { xf: 0.60, yf: 0.25, rf: 0.24, color: '68,28,118' },
    { xf: 0.16, yf: 0.74, rf: 0.20, color: '12,52,128' },
    { xf: 0.85, yf: 0.52, rf: 0.14, color: '128,28,58' },
    { xf: 0.42, yf: 0.65, rf: 0.16, color: '18,80,90'  },
  ];

  let nebulaImg = null;

  function buildNebula() {
    const oc = document.createElement('canvas');
    oc.width = W; oc.height = H;
    const octx = oc.getContext('2d');

    for (const n of NEBULA_DEFS) {
      const r = n.rf * Math.min(W, H);
      const grd = octx.createRadialGradient(n.xf * W, n.yf * H, 0, n.xf * W, n.yf * H, r);
      grd.addColorStop(0,   `rgba(${n.color},0.18)`);
      grd.addColorStop(0.5, `rgba(${n.color},0.07)`);
      grd.addColorStop(1,   `rgba(${n.color},0)`);
      octx.fillStyle = grd;
      octx.fillRect(0, 0, W, H);
    }
    nebulaImg = oc;
  }

  // ── Shooting Stars ─────────────────────────────────────────────────────────

  let shootingStars = [];
  let nextSpawnAt = 2;

  function spawnShootingStar() {
    const x = Math.random() * vW * 0.85;
    const y = Math.random() * vH * 0.35;
    const angle = 0.35 + Math.random() * 0.35;
    const speed = 5 + Math.random() * 5;
    shootingStars.push({
      x, y,
      vx: Math.cos(angle) * speed,
      vy: Math.sin(angle) * speed,
      trailLen: 9 + Math.floor(Math.random() * 7),
      life: 0,
      maxLife: 0.7 + Math.random() * 0.6,
    });
    nextSpawnAt = animT + 4 + Math.random() * 4;
  }

  function drawShootingStars() {
    if (animT >= nextSpawnAt) spawnShootingStar();

    for (let i = shootingStars.length - 1; i >= 0; i--) {
      const s = shootingStars[i];
      s.life += 0.016;
      s.x += s.vx * 0.016;
      s.y += s.vy * 0.016;

      const fade = Math.max(0, 1 - s.life / s.maxLife);
      const mag  = Math.hypot(s.vx, s.vy);
      const nx = s.vx / mag;
      const ny = s.vy / mag;

      for (let t = 0; t < s.trailLen; t++) {
        const a = fade * (1 - t / s.trailLen);
        if (a < 0.02) break;
        ctx.fillStyle = `rgba(255,255,220,${a.toFixed(2)})`;
        ctx.fillRect(Math.round(s.x - nx * t) * PX, Math.round(s.y - ny * t) * PX, PX, PX);
      }

      if (s.life >= s.maxLife || s.x >= vW || s.y >= vH) {
        shootingStars.splice(i, 1);
      }
    }
  }

  // ── Render loop ────────────────────────────────────────────────────────────

  let animT = 0;
  let rafId = null;

  function draw() {
    ctx.clearRect(0, 0, W, H);
    if (nebulaImg)  ctx.drawImage(nebulaImg, 0, 0);
    if (galaxyImg)  ctx.drawImage(galaxyImg, 0, 0);
    drawStars(animT);
    drawPlanets();
    drawShootingStars();
    animT += 0.016;
    rafId = requestAnimationFrame(draw);
  }

  function rebuild() {
    if (rafId) cancelAnimationFrame(rafId);
    W  = canvas.width  = canvas.offsetWidth;
    H  = canvas.height = canvas.offsetHeight;
    vW = Math.ceil(W / PX);
    vH = Math.ceil(H / PX);
    shootingStars = [];
    nextSpawnAt   = animT + 2;
    initStars();
    buildPlanets();
    buildGalaxies();
    buildNebula();
  }

  let resizeTimer;
  window.addEventListener('resize', () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => { rebuild(); draw(); }, 150);
  });

  function init() {
    rebuild();
    draw();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
