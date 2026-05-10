(function () {
  'use strict';

  const canvas = document.getElementById('about-canvas');
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  let W, H, raf;

  const STEP = 7; // px between data points

  const series = [
    // main purple line — centered high, moderate amplitude, slow drift
    { pts: [], offset: 0, speed: 0.38, yFrac: 0.20, amp: 0.22, color: '139, 92, 246', alpha: 0.34, lw: 1.8 },
    // indigo line — centered low, wide swings, a bit faster
    { pts: [], offset: 0, speed: 0.55, yFrac: 0.36, amp: 0.18, color: '99, 102, 241',  alpha: 0.22, lw: 1.3 },
    // lavender ghost — mid, tiny noise, fastest (creates depth)
    { pts: [], offset: 0, speed: 0.80, yFrac: 0.28, amp: 0.10, color: '196, 181, 253', alpha: 0.13, lw: 1.0 },
  ];

  /* ── Geometry ──────────────────────────────────────────────── */
  function nextY(s) {
    const prev = s.pts[s.pts.length - 1] ?? H * s.yFrac;
    const delta = (Math.random() - 0.5) * H * s.amp * 0.45;
    const pull  = (H * s.yFrac - prev) * 0.07; // gentle mean-reversion
    return Math.max(H * 0.06, Math.min(H * 0.94, prev + delta + pull));
  }

  function initSeries(s) {
    s.pts   = [];
    s.offset = 0;
    const count = Math.ceil(W / STEP) + 6;
    for (let i = 0; i < count; i++) s.pts.push(nextY(s));
  }

  function resize() {
    W = canvas.width  = canvas.offsetWidth;
    H = canvas.height = canvas.offsetHeight;
    series.forEach(initSeries);
  }

  /* ── Drawing ───────────────────────────────────────────────── */
  function drawSeries(s) {
    const pts = s.pts;
    const n   = pts.length;
    if (n < 2) return;

    // Horizontal fade: invisible at edges, full alpha in the middle band
    const grad = ctx.createLinearGradient(0, 0, W, 0);
    grad.addColorStop(0,    `rgba(${s.color}, 0)`);
    grad.addColorStop(0.08, `rgba(${s.color}, ${s.alpha})`);
    grad.addColorStop(0.82, `rgba(${s.color}, ${s.alpha})`);
    grad.addColorStop(1,    `rgba(${s.color}, 0)`);

    ctx.save();
    ctx.strokeStyle = grad;
    ctx.lineWidth   = s.lw;
    ctx.lineJoin    = 'round';
    ctx.lineCap     = 'round';
    ctx.beginPath();

    const x0 = -s.offset;
    ctx.moveTo(x0, pts[0]);

    for (let i = 0; i < n - 1; i++) {
      const xA  = x0 + i * STEP;
      const xB  = x0 + (i + 1) * STEP;
      const midX = (xA + xB) / 2;
      const midY = (pts[i] + pts[i + 1]) / 2;
      ctx.quadraticCurveTo(xA, pts[i], midX, midY);
    }
    ctx.lineTo(x0 + (n - 1) * STEP, pts[n - 1]);

    ctx.stroke();
    ctx.restore();
  }

  /* ── Animation loop ────────────────────────────────────────── */
  function tick() {
    ctx.clearRect(0, 0, W, H);

    series.forEach(s => {
      s.offset += s.speed;
      while (s.offset >= STEP) {
        s.offset -= STEP;
        s.pts.shift();
        s.pts.push(nextY(s));
      }
      drawSeries(s);
    });

    raf = requestAnimationFrame(tick);
  }

  /* ── Intersection observer — pause when off-screen ─────────── */
  const section = document.getElementById('about');
  const io = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        if (!raf) tick();
      } else {
        cancelAnimationFrame(raf);
        raf = null;
      }
    });
  }, { threshold: 0.05 });

  if (section) io.observe(section);

  window.addEventListener('resize', () => {
    cancelAnimationFrame(raf);
    raf = null;
    resize();
    tick();
  });

  resize();
  tick();
})();
