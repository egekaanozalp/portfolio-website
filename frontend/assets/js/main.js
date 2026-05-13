(function() {
  "use strict";

  /**
   * Header toggle
   */
  const headerToggleBtn = document.querySelector('.header-toggle');

  function headerToggle() {
    document.querySelector('#header').classList.toggle('header-show');
    headerToggleBtn.classList.toggle('bi-list');
    headerToggleBtn.classList.toggle('bi-x');
  }
  headerToggleBtn.addEventListener('click', headerToggle);

  /**
   * Hide mobile nav on same-page/hash links
   */
  document.querySelectorAll('#navmenu a').forEach(navmenu => {
    navmenu.addEventListener('click', () => {
      if (document.querySelector('.header-show')) {
        headerToggle();
      }
    });

  });

  /**
   * Toggle mobile nav dropdowns
   */
  document.querySelectorAll('.navmenu .toggle-dropdown').forEach(navmenu => {
    navmenu.addEventListener('click', function(e) {
      e.preventDefault();
      this.parentNode.classList.toggle('active');
      this.parentNode.nextElementSibling.classList.toggle('dropdown-active');
      e.stopImmediatePropagation();
    });
  });

  /**
   * Preloader
   */
  const preloader = document.querySelector('#preloader');
  if (preloader) {
    window.addEventListener('load', () => {
      preloader.remove();
    });
  }

  /**
   * Scroll top button
   */
  let scrollTop = document.querySelector('.scroll-top');

  function toggleScrollTop() {
    if (scrollTop) {
      window.scrollY > 100 ? scrollTop.classList.add('active') : scrollTop.classList.remove('active');
    }
  }
  scrollTop.addEventListener('click', (e) => {
    e.preventDefault();
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  });

  window.addEventListener('load', toggleScrollTop);
  document.addEventListener('scroll', toggleScrollTop);

  /**
   * Animation on scroll function and init
   */
  function aosInit() {
    AOS.init({
      duration: 600,
      easing: 'ease-in-out',
      once: true,
      mirror: false
    });
  }
  window.addEventListener('load', aosInit);

  /**
   * Init typed.js
   */
  const selectTyped = document.querySelector('.typed');
  if (selectTyped) {
    let typed_strings = selectTyped.getAttribute('data-typed-items');
    typed_strings = typed_strings.split(',');
    new Typed('.typed', {
      strings: typed_strings,
      loop: true,
      typeSpeed: 100,
      backSpeed: 50,
      backDelay: 2000
    });
  }

  /**
   * Initiate Pure Counter
   */
  new PureCounter();

  /**
   * Animate the skills items on reveal
   */
  let skillsAnimation = document.querySelectorAll('.skills-animation');
  skillsAnimation.forEach((item) => {
    new Waypoint({
      element: item,
      offset: '80%',
      handler: function(direction) {
        let progress = item.querySelectorAll('.progress .progress-bar');
        progress.forEach(el => {
          el.style.width = el.getAttribute('aria-valuenow') + '%';
        });
      }
    });
  });

  /**
   * Initiate glightbox
   */
  const glightbox = GLightbox({
    selector: '.glightbox'
  });

  /**
   * Init isotope layout and filters
   */
  document.querySelectorAll('.isotope-layout').forEach(function(isotopeItem) {
    let layout = isotopeItem.getAttribute('data-layout') ?? 'masonry';
    let filter = isotopeItem.getAttribute('data-default-filter') ?? '*';
    let sort = isotopeItem.getAttribute('data-sort') ?? 'original-order';
    const PF_LIMIT = 6;

    let initIsotope;
    let currentFilter = filter;
    let pfExpanded = false;
    const container = isotopeItem.querySelector('.isotope-container');

    // Build "Show all" button and inject after the grid
    const pfWrap = document.createElement('div');
    pfWrap.className = 'pf-show-all-wrap';
    pfWrap.innerHTML = '<button class="pf-show-all" type="button"><i class="bi bi-grid-3x3-gap-fill"></i> <span class="pf-show-all-label">Show all (<span class="pf-show-all-count"></span>)</span></button>';
    pfWrap.style.display = 'none';
    container.parentElement.appendChild(pfWrap);
    const pfBtn = pfWrap.querySelector('.pf-show-all');
    const pfCount = pfWrap.querySelector('.pf-show-all-count');
    const pfLabel = pfWrap.querySelector('.pf-show-all-label');

    function applyPortfolioFilter(filterSel, isExpanded) {
      const allItems = Array.from(container.querySelectorAll('.isotope-item'));
      allItems.forEach(function(el) { el.removeAttribute('data-pf-over'); });

      if (isExpanded) {
        initIsotope.arrange({ filter: filterSel });
        pfWrap.style.display = 'none';
        return;
      }

      const matching = filterSel === '*'
        ? allItems
        : allItems.filter(function(el) { return el.matches(filterSel); });

      if (matching.length <= PF_LIMIT) {
        initIsotope.arrange({ filter: filterSel });
        pfWrap.style.display = 'none';
        return;
      }

      matching.slice(PF_LIMIT).forEach(function(el) { el.setAttribute('data-pf-over', '1'); });
      const limitedFilter = filterSel === '*'
        ? ':not([data-pf-over])'
        : filterSel + ':not([data-pf-over])';
      initIsotope.arrange({ filter: limitedFilter });
      pfCount.textContent = matching.length;
      pfLabel.textContent = 'Show all (' + matching.length + ')';
      pfWrap.style.display = 'flex';
    }

    imagesLoaded(container, function() {
      initIsotope = new Isotope(container, {
        itemSelector: '.isotope-item',
        layoutMode: layout,
        filter: filter,
        sortBy: sort
      });
      applyPortfolioFilter(currentFilter, false);
    });

    isotopeItem.querySelectorAll('.isotope-filters li').forEach(function(filters) {
      filters.addEventListener('click', function() {
        isotopeItem.querySelector('.isotope-filters .filter-active').classList.remove('filter-active');
        this.classList.add('filter-active');
        currentFilter = this.getAttribute('data-filter') || '*';
        pfExpanded = false;
        applyPortfolioFilter(currentFilter, false);
        if (typeof aosInit === 'function') {
          aosInit();
        }
      }, false);
    });

    pfBtn.addEventListener('click', function() {
      if (pfExpanded) {
        pfExpanded = false;
        applyPortfolioFilter(currentFilter, false);
        const section = document.getElementById('portfolio');
        if (section && section.getBoundingClientRect().top < 0) {
          section.scrollIntoView({ behavior: 'instant', block: 'start' });
        }
      } else {
        pfExpanded = true;
        initIsotope.arrange({ filter: currentFilter });
        pfLabel.textContent = 'Show less';
        pfWrap.style.display = 'flex';
      }
    });


  });

  /**
   * Init swiper sliders
   */
  function initSwiper() {
    document.querySelectorAll(".init-swiper").forEach(function(swiperElement) {
      let config = JSON.parse(
        swiperElement.querySelector(".swiper-config").innerHTML.trim()
      );

      if (swiperElement.classList.contains("swiper-tab")) {
        initSwiperWithCustomPagination(swiperElement, config);
      } else {
        new Swiper(swiperElement, config);
      }
    });
  }

  window.addEventListener("load", initSwiper);

  /**
   * Correct scrolling position upon page load for URLs containing hash links.
   */
  window.addEventListener('load', function(e) {
    if (window.location.hash) {
      if (document.querySelector(window.location.hash)) {
        setTimeout(() => {
          let section = document.querySelector(window.location.hash);
          let scrollMarginTop = getComputedStyle(section).scrollMarginTop;
          window.scrollTo({
            top: section.offsetTop - parseInt(scrollMarginTop),
            behavior: 'smooth'
          });
        }, 100);
      }
    }
  });

  /**
   * Navmenu Scrollspy
   */
  let navmenulinks = document.querySelectorAll('.navmenu a');

  function navmenuScrollspy() {
    navmenulinks.forEach(navmenulink => {
      if (!navmenulink.hash) return;
      let section = document.querySelector(navmenulink.hash);
      if (!section) return;
      let position = window.scrollY + 200;
      if (position >= section.offsetTop && position <= (section.offsetTop + section.offsetHeight)) {
        document.querySelectorAll('.navmenu a.active').forEach(link => link.classList.remove('active'));
        navmenulink.classList.add('active');
      } else {
        navmenulink.classList.remove('active');
      }
    })
  }
  window.addEventListener('load', navmenuScrollspy);
  document.addEventListener('scroll', navmenuScrollspy);

})();