(function () {
  const canvas = document.getElementById('resume-canvas');
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  const COUNT = 32;
  const MAX_DIST = 110;
  const MAX_DIST_SQ = MAX_DIST * MAX_DIST;
  const TARGET_FPS = 24;
  const INTERVAL = 1000 / TARGET_FPS;

  let W, H, particles, lastTime = 0, raf = null;

  function mkParticle(randomY) {
    return {
      x: Math.random() * W,
      y: randomY ? Math.random() * H : H + Math.random() * 20,
      r: Math.random() * 1.3 + 0.4,
      vx: (Math.random() - 0.5) * 0.11,
      vy: -(Math.random() * 0.2 + 0.07),
      alpha: Math.random() * 0.15 + 0.08,
    };
  }

  function resize() {
    W = canvas.width = canvas.offsetWidth;
    H = canvas.height = canvas.offsetHeight;
  }

  function init() {
    resize();
    particles = Array.from({ length: COUNT }, () => mkParticle(true));
  }

  function draw(ts) {
    raf = requestAnimationFrame(draw);
    if (ts - lastTime < INTERVAL) return;
    lastTime = ts;

    ctx.clearRect(0, 0, W, H);

    // Connections — O(n²) is fine for n=32
    ctx.lineWidth = 0.6;
    for (let i = 0; i < COUNT; i++) {
      const a = particles[i];
      for (let j = i + 1; j < COUNT; j++) {
        const b = particles[j];
        const dx = a.x - b.x, dy = a.y - b.y;
        const d2 = dx * dx + dy * dy;
        if (d2 < MAX_DIST_SQ) {
          const alpha = (1 - Math.sqrt(d2) / MAX_DIST) * 0.12;
          ctx.beginPath();
          ctx.moveTo(a.x, a.y);
          ctx.lineTo(b.x, b.y);
          ctx.strokeStyle = `rgba(124,58,237,${alpha})`;
          ctx.stroke();
        }
      }
    }

    // Particles
    for (let i = 0; i < COUNT; i++) {
      const p = particles[i];
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(167,139,250,${p.alpha})`;
      ctx.fill();

      p.x += p.vx;
      p.y += p.vy;

      // Wrap: respawn at bottom when leaving top
      if (p.y < -4) { Object.assign(p, mkParticle(false)); }
      if (p.x < -4)  p.x = W + 4;
      if (p.x > W + 4) p.x = -4;
    }
  }

  // Only animate when section is in viewport
  const section = document.getElementById('resume');
  if (section && window.IntersectionObserver) {
    new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          if (!raf) { lastTime = 0; raf = requestAnimationFrame(draw); }
        } else {
          if (raf) { cancelAnimationFrame(raf); raf = null; }
        }
      });
    }, { threshold: 0 }).observe(section);
  } else {
    raf = requestAnimationFrame(draw);
  }

  // Pause when tab hidden
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
      if (raf) { cancelAnimationFrame(raf); raf = null; }
    } else {
      if (!raf) { lastTime = 0; raf = requestAnimationFrame(draw); }
    }
  });

  let resizeTimer;
  window.addEventListener('resize', () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(init, 150);
  });

  init();
})();
