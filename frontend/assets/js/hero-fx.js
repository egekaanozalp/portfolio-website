(function () {
  'use strict';

  const canvas = document.getElementById('nn-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');

  const LAYERS_LANDSCAPE = [6, 8, 10, 12, 13, 12, 10, 8, 6];
  const LAYERS_MOBILE    = [3, 4,  5,  6,  5,  4,  3];
  const NODE_RADIUS = 3;
  const MAX_PULSES  = 25;

  let W, H, nodes, connections;
  const pulses = [];

  function isMobile() { return window.innerWidth < 992; }

  /* ── Position canvas over the name element ─────── */
  function positionMobileCanvas() {
    const nameEl = document.querySelector('.hero-name');
    const heroEl = document.getElementById('home') || document.querySelector('.hero');
    if (!nameEl || !heroEl) return;

    // Walk offsetParent chain — unaffected by CSS transforms (AOS)
    let top = 0, el = nameEl;
    while (el && el !== heroEl && el !== document.body) {
      top += el.offsetTop;
      el = el.offsetParent;
    }

    const pad  = 10;
    const wrap = canvas.parentElement;
    wrap.style.top    = Math.max(0, top - pad) + 'px';
    wrap.style.height = (nameEl.offsetHeight + pad * 2) + 'px';
    wrap.style.bottom = 'auto';
  }

  /* ── Build network ─────────────────────────────── */
  function build() {
    nodes = [];
    connections = [];

    const mobile = isMobile();
    const LAYERS = mobile ? LAYERS_MOBILE : LAYERS_LANDSCAPE;
    const padX   = W * (mobile ? 0.02 : 0.06);
    const padY   = H * (mobile ? 0.08 : 0.22);
    const usableW = W - padX * 2;
    const usableH = H - padY * 2;
    const layerGap = usableW / (LAYERS.length - 1);

    const byLayer = LAYERS.map((count, li) => {
      const layer = [];
      const x = padX + li * layerGap;
      const nodeGap = count > 1 ? usableH / (count - 1) : 0;
      const offsetY  = count > 1 ? padY : H / 2;
      for (let ni = 0; ni < count; ni++) {
        const node = { x, y: offsetY + ni * nodeGap };
        nodes.push(node);
        layer.push(node);
      }
      return layer;
    });

    for (let li = 0; li < LAYERS.length - 1; li++)
      for (const a of byLayer[li])
        for (const b of byLayer[li + 1])
          connections.push({ a, b });
  }

  /* ── Color helpers ─────────────────────────────── */
  function connectionColor(midX, midY, alphaScale) {
    const t = midX / W;

    let intensity;
    if (isMobile()) {
      // Hollow center: dim behind name text, bright at left/right flanks
      const dist     = Math.abs(t - 0.50);            // 0 at center, 0.5 at edges
      const hollow   = Math.min(1, dist * 2.2);        // ramps up quickly from center
      const edgeClip = Math.pow(Math.sin(t * Math.PI), 0.8); // fades at extreme edges
      intensity = hollow * edgeClip;
    } else {
      // Desktop: peak at badge column
      const envelope = Math.pow(Math.sin(t * Math.PI), 0.55);
      const peak     = Math.max(0, 1.0 - Math.abs(t - 0.65) * 1.6);
      intensity = peak * envelope;
    }

    const a = (0.04 + intensity * 0.50) * alphaScale;
    return `rgba(139, 92, 246, ${Math.min(1, a)})`;
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

    ctx.lineWidth = 0.55;
    for (const { a, b } of connections) {
      const midX = (a.x + b.x) * 0.5;
      const midY = (a.y + b.y) * 0.5;
      ctx.strokeStyle = connectionColor(midX, midY, 1);
      ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke();
    }

    ctx.lineWidth = 0.9;
    for (const n of nodes) {
      ctx.strokeStyle = connectionColor(n.x, n.y, 1.4);
      ctx.fillStyle   = connectionColor(n.x, n.y, 0.12);
      ctx.beginPath(); ctx.arc(n.x, n.y, NODE_RADIUS, 0, Math.PI * 2);
      ctx.fill(); ctx.stroke();
    }

    for (let i = pulses.length - 1; i >= 0; i--) {
      const p = pulses[i];
      p.t += p.speed;
      if (p.t > 1) { pulses.splice(i, 1); continue; }
      const { a, b } = p.conn;
      const px = a.x + (b.x - a.x) * p.t;
      const py = a.y + (b.y - a.y) * p.t;
      const lifeAlpha = Math.sin(p.t * Math.PI);
      ctx.beginPath(); ctx.arc(px, py, 1.8, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(255,255,255,${0.85 * lifeAlpha})`; ctx.fill();
    }

    if (Math.random() < 0.04) spawnPulse();
  }

  /* ── Resize ────────────────────────────────────── */
  function resize() {
    if (isMobile()) {
      positionMobileCanvas();
    } else {
      const wrap = canvas.parentElement;
      wrap.style.top = wrap.style.height = wrap.style.bottom = '';
    }
    const wrap = canvas.parentElement;
    W = canvas.width  = wrap.offsetWidth;
    H = canvas.height = wrap.offsetHeight;
    build();
  }

  /* ── RAF loop ──────────────────────────────────── */
  function loop() { render(); requestAnimationFrame(loop); }

  window.addEventListener('resize', resize);
  resize();
  requestAnimationFrame(loop);
})();
