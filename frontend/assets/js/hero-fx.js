(function () {
  'use strict';

  const canvas = document.getElementById('nn-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');

  // Layer node counts — diamond/hourglass shape matching the reference
  const LAYERS = [6, 8, 10, 12, 13, 12, 10, 8, 6];
  const NODE_RADIUS = 3;
  const MAX_PULSES = 25;

  let W, H, nodes, connections;
  const pulses = [];

  /* ── Build network ─────────────────────────────── */
  function build() {
    nodes = [];
    connections = [];

    const padX = W * 0.06;
    const padY = H * 0.22;
    const usableW = W - padX * 2;
    const usableH = H - padY * 2;
    const layerGap = usableW / (LAYERS.length - 1);

    const byLayer = LAYERS.map((count, li) => {
      const layer = [];
      const x = padX + li * layerGap;
      const nodeGap = count > 1 ? usableH / (count - 1) : 0;
      const offsetY = count > 1 ? padY : H / 2;
      for (let ni = 0; ni < count; ni++) {
        const y = offsetY + ni * nodeGap;
        const node = { x, y };
        nodes.push(node);
        layer.push(node);
      }
      return layer;
    });

    for (let li = 0; li < LAYERS.length - 1; li++) {
      for (const a of byLayer[li]) {
        for (const b of byLayer[li + 1]) {
          connections.push({ a, b });
        }
      }
    }
  }

  /* ── Color by x-position ───────────────────────── */
  function rgba(r, g, b, a) {
    return `rgba(${r},${g},${b},${Math.max(0, Math.min(1, a))})`;
  }

  function connectionColor(midX, alphaScale) {
    const t = midX / W;
    let r, g, b, a;

    if (t < 0.12) {
      // Left fade: very faint lavender
      const s = t / 0.12;
      r = 200; g = 185; b = 255;
      a = s * 0.30;
    } else if (t < 0.38) {
      // Ramp up to vivid purple
      const s = (t - 0.12) / 0.26;
      r = Math.round(200 - 95 * s);  // 200 → 105
      g = Math.round(185 - 150 * s); // 185 → 35
      b = 255;
      a = 0.30 + s * 0.40;           // 0.30 → 0.70
    } else if (t < 0.58) {
      // Deep purple core
      const s = (t - 0.38) / 0.20;
      r = Math.round(105 - 5 * s);   // 105 → 100
      g = Math.round(35 + 5 * s);    // 35 → 40
      b = 255;
      a = 0.70 + s * 0.10;           // 0.70 → 0.80
    } else if (t < 0.78) {
      // Purple → warm lavender
      const s = (t - 0.58) / 0.20;
      r = Math.round(100 + 125 * s); // 100 → 225
      g = Math.round(40 + 160 * s);  // 40 → 200
      b = Math.round(255 - 30 * s);  // 255 → 225
      a = 0.80 - s * 0.52;           // 0.80 → 0.28
    } else {
      // Right fade: cream → transparent
      const s = (t - 0.78) / 0.22;
      r = Math.round(225 + 30 * s);  // 225 → 255
      g = Math.round(200 + 45 * s);  // 200 → 245
      b = Math.round(225 - 5 * s);   // 225 → 220
      a = 0.28 * (1 - s);            // 0.28 → 0
    }

    return rgba(r, g, b, a * alphaScale);
  }

  /* ── Pulse helpers ─────────────────────────────── */
  function spawnPulse() {
    if (connections.length === 0 || pulses.length >= MAX_PULSES) return;
    const conn = connections[Math.floor(Math.random() * connections.length)];
    pulses.push({ conn, t: 0, speed: 0.006 + Math.random() * 0.010 });
  }

  /* ── Render ────────────────────────────────────── */
  function render() {
    ctx.clearRect(0, 0, W, H);

    // Connections
    ctx.lineWidth = 0.55;
    for (const { a, b } of connections) {
      const midX = (a.x + b.x) * 0.5;
      ctx.strokeStyle = connectionColor(midX, 1);
      ctx.beginPath();
      ctx.moveTo(a.x, a.y);
      ctx.lineTo(b.x, b.y);
      ctx.stroke();
    }

    // Nodes
    ctx.lineWidth = 0.9;
    for (const n of nodes) {
      ctx.strokeStyle = connectionColor(n.x, 1.4);
      ctx.fillStyle   = connectionColor(n.x, 0.12);
      ctx.beginPath();
      ctx.arc(n.x, n.y, NODE_RADIUS, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();
    }

    // Pulses
    for (let i = pulses.length - 1; i >= 0; i--) {
      const p = pulses[i];
      p.t += p.speed;
      if (p.t > 1) { pulses.splice(i, 1); continue; }

      const { a, b } = p.conn;
      const px = a.x + (b.x - a.x) * p.t;
      const py = a.y + (b.y - a.y) * p.t;
      // Fade in/out along travel
      const lifeAlpha = Math.sin(p.t * Math.PI);

      ctx.beginPath();
      ctx.arc(px, py, 1.8, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(255,255,255,${0.85 * lifeAlpha})`;
      ctx.fill();
    }

    // Spawn new pulse stochastically
    if (Math.random() < 0.04) spawnPulse();
  }

  /* ── Resize ────────────────────────────────────── */
  function resize() {
    const wrap = canvas.parentElement;
    W = canvas.width  = wrap.offsetWidth;
    H = canvas.height = wrap.offsetHeight;
    build();
  }

  /* ── RAF loop ──────────────────────────────────── */
  function loop() {
    render();
    requestAnimationFrame(loop);
  }

  window.addEventListener('resize', () => { resize(); });
  resize();
  requestAnimationFrame(loop);
})();
