(function () {
  'use strict';

  /* ---- Helpers ---- */
  function easeOutQuart(t) { return 1 - Math.pow(1 - t, 4); }
  function lerp(a, b, f) { return a + (b - a) * f; }

  /* ============ 1. NAV SCROLL ============ */
  const nav = document.getElementById('nav');
  let lastScroll = 0;

  function onScroll() {
    const y = window.scrollY;
    if (nav) nav.classList.toggle('scrolled', y > 50);
    // Back to top
    const btt = document.getElementById('backToTop');
    if (btt) btt.classList.toggle('visible', y > 500);
    lastScroll = y;
  }
  window.addEventListener('scroll', onScroll, { passive: true });

  /* ============ 2. MOBILE NAV ============ */
  const navToggle = document.getElementById('navToggle');
  const navLinks = document.getElementById('navLinks');

  if (navToggle && navLinks) {
    navToggle.addEventListener('click', function () {
      navToggle.classList.toggle('active');
      navLinks.classList.toggle('active');
    });
    navLinks.querySelectorAll('.nav-link').forEach(function (link) {
      link.addEventListener('click', function () {
        navToggle.classList.remove('active');
        navLinks.classList.remove('active');
      });
    });
  }

  /* ============ 3. SMOOTH SCROLL ============ */
  document.querySelectorAll('a[href^="#"]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      var target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        var top = target.getBoundingClientRect().top + window.scrollY - 80;
        window.scrollTo({ top: top, behavior: 'smooth' });
      }
    });
  });

  /* ============ 4. SCROLL REVEAL ============ */
  var revealEls = document.querySelectorAll('.reveal');

  var revealObserver = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('active');
        revealObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

  revealEls.forEach(function (el, i) {
    // Stagger within parent section
    var parent = el.closest('section') || el.closest('.about-section') || el.closest('.collection-section');
    if (parent) {
      var siblings = parent.querySelectorAll('.reveal');
      var idx = Array.prototype.indexOf.call(siblings, el);
      el.style.transitionDelay = Math.min(idx * 0.08, 0.5) + 's';
    }
    revealObserver.observe(el);
  });

  /* ============ 5. COUNTER ANIMATION ============ */
  var counters = document.querySelectorAll('.stat-number');
  var counterDone = false;

  var counterObserver = new IntersectionObserver(function (entries) {
    if (counterDone) return;
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        counterDone = true;
        animateCounters();
        counterObserver.disconnect();
      }
    });
  }, { threshold: 0.3 });

  if (counters.length) counterObserver.observe(counters[0].closest('.hero-stats') || counters[0]);

  function animateCounters() {
    counters.forEach(function (el) {
      var target = parseFloat(el.getAttribute('data-count'));
      var hasDecimal = target % 1 !== 0;
      var start = performance.now();
      var duration = 2000;
      function tick(now) {
        var t = Math.min((now - start) / duration, 1);
        var val = easeOutQuart(t) * target;
        el.textContent = hasDecimal ? val.toFixed(1) : Math.round(val);
        if (t < 1) requestAnimationFrame(tick);
      }
      requestAnimationFrame(tick);
    });
  }

  /* ============ 6. LIGHTBOX ============ */
  var lightbox = document.getElementById('lightbox');
  var lbImg = document.getElementById('lightboxImg');
  var lbTitle = document.getElementById('lightboxTitle');
  var lbDesc = document.getElementById('lightboxDesc');
  var lbCounter = document.getElementById('lightboxCounter');
  var lbClose = document.getElementById('lightboxClose');
  var lbPrev = document.getElementById('lightboxPrev');
  var lbNext = document.getElementById('lightboxNext');

  var currentItems = [];
  var currentIndex = 0;

  function openLightbox(item, items) {
    currentItems = items;
    currentIndex = Array.prototype.indexOf.call(items, item);
    showLightboxItem();
    lightbox.classList.add('active');
    document.body.style.overflow = 'hidden';
  }

  function showLightboxItem() {
    var item = currentItems[currentIndex];
    if (!item) return;
    var img = item.querySelector('img');
    var overlay = item.querySelector('.item-overlay');
    lbImg.src = img.src;
    lbImg.alt = img.alt;
    lbTitle.textContent = overlay ? (overlay.querySelector('h4') || {}).textContent || '' : '';
    lbDesc.textContent = overlay ? (overlay.querySelector('p') || {}).textContent || '' : '';
    lbCounter.textContent = (currentIndex + 1) + ' / ' + currentItems.length;
  }

  function closeLightbox() {
    lightbox.classList.remove('active');
    document.body.style.overflow = '';
  }

  function nextItem() {
    currentIndex = (currentIndex + 1) % currentItems.length;
    showLightboxItem();
  }
  function prevItem() {
    currentIndex = (currentIndex - 1 + currentItems.length) % currentItems.length;
    showLightboxItem();
  }

  if (lbClose) lbClose.addEventListener('click', closeLightbox);
  if (lbPrev) lbPrev.addEventListener('click', prevItem);
  if (lbNext) lbNext.addEventListener('click', nextItem);

  if (lightbox) {
    lightbox.addEventListener('click', function (e) {
      if (e.target === lightbox) closeLightbox();
    });
  }

  document.addEventListener('keydown', function (e) {
    if (!lightbox || !lightbox.classList.contains('active')) return;
    if (e.key === 'Escape') closeLightbox();
    if (e.key === 'ArrowRight') nextItem();
    if (e.key === 'ArrowLeft') prevItem();
  });

  // Attach click to all gallery items grouped by section
  document.querySelectorAll('.collection-section').forEach(function (section) {
    var items = section.querySelectorAll('.gallery-item');
    items.forEach(function (item) {
      item.addEventListener('click', function (e) {
        // Prevent opening if user was dragging (scroll gallery)
        if (item.dataset.dragging === 'true') return;
        openLightbox(item, items);
      });
    });
  });

  /* ============ 7. DRAG-TO-SCROLL (Horizontal Gallery) ============ */
  document.querySelectorAll('.gallery-scroll').forEach(function (scroll) {
    var isDown = false, startX, scrollLeft, moved = false;
    var items = scroll.querySelectorAll('.gallery-item');

    scroll.addEventListener('mousedown', function (e) {
      isDown = true; moved = false;
      startX = e.pageX - scroll.offsetLeft;
      scrollLeft = scroll.scrollLeft;
      scroll.style.cursor = 'grabbing';
    });
    scroll.addEventListener('mouseleave', function () { isDown = false; scroll.style.cursor = 'grab'; });
    scroll.addEventListener('mouseup', function () {
      isDown = false; scroll.style.cursor = 'grab';
      // Mark items as not dragging after a tick
      setTimeout(function () {
        items.forEach(function (it) { it.dataset.dragging = 'false'; });
      }, 10);
    });
    scroll.addEventListener('mousemove', function (e) {
      if (!isDown) return;
      e.preventDefault();
      var x = e.pageX - scroll.offsetLeft;
      var walk = (x - startX) * 1.5;
      if (Math.abs(walk) > 5) {
        moved = true;
        items.forEach(function (it) { it.dataset.dragging = 'true'; });
      }
      scroll.scrollLeft = scrollLeft - walk;
    });
  });

  /* ============ 8. BACK TO TOP ============ */
  var backToTop = document.getElementById('backToTop');
  if (backToTop) {
    backToTop.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  /* ============ 9. ACTIVE NAV LINK ============ */
  var sections = document.querySelectorAll('section[id], div#collections');

  var navObserver = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        var id = entry.target.id;
        document.querySelectorAll('.nav-link').forEach(function (link) {
          link.classList.remove('active');
          if (link.getAttribute('href') === '#' + id) link.classList.add('active');
        });
      }
    });
  }, { threshold: 0.2, rootMargin: '-80px 0px -50% 0px' });

  sections.forEach(function (s) { navObserver.observe(s); });

  /* ============ 10. COLLECTION IN-VIEW ============ */
  var collectionObserver = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      entry.target.classList.toggle('in-view', entry.isIntersecting);
    });
  }, { threshold: 0.05 });

  document.querySelectorAll('.collection-section').forEach(function (s) {
    collectionObserver.observe(s);
  });

  /* ============ 11. PAGE LOAD ============ */
  document.addEventListener('DOMContentLoaded', function () {
    setTimeout(function () {
      document.body.classList.add('loaded');
    }, 300);
    onScroll();
  });

  // Trigger scroll once
  onScroll();

  /* ============ 12. PDF CAROUSEL (Swipable) ============ */
  var pdfTrack = document.getElementById('pdfTrack');
  var pdfPrev = document.getElementById('pdfPrev');
  var pdfNext = document.getElementById('pdfNext');
  var pdfCounter = document.getElementById('pdfCurrent');
  if (pdfTrack) {
    var pdfSlides = pdfTrack.querySelectorAll('.pdf-slide');
    var pdfTotal = pdfSlides.length;
    var pdfIndex = 0;
    var pdfStartX = 0;
    var pdfDiffX = 0;
    var pdfDragging = false;

    function pdfGo(idx) {
      pdfIndex = Math.max(0, Math.min(idx, pdfTotal - 1));
      pdfTrack.style.transform = 'translateX(-' + (pdfIndex * 100) + '%)';
      if (pdfCounter) pdfCounter.textContent = pdfIndex + 1;
    }

    if (pdfPrev) pdfPrev.addEventListener('click', function () { pdfGo(pdfIndex - 1); });
    if (pdfNext) pdfNext.addEventListener('click', function () { pdfGo(pdfIndex + 1); });

    // Touch/swipe support
    pdfTrack.addEventListener('touchstart', function (e) {
      pdfStartX = e.touches[0].clientX;
      pdfDragging = true;
      pdfTrack.style.transition = 'none';
    }, { passive: true });

    pdfTrack.addEventListener('touchmove', function (e) {
      if (!pdfDragging) return;
      pdfDiffX = e.touches[0].clientX - pdfStartX;
      var offset = -(pdfIndex * 100) + (pdfDiffX / pdfTrack.offsetWidth) * 100;
      pdfTrack.style.transform = 'translateX(' + offset + '%)';
    }, { passive: true });

    pdfTrack.addEventListener('touchend', function () {
      pdfDragging = false;
      pdfTrack.style.transition = 'transform 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94)';
      if (Math.abs(pdfDiffX) > 50) {
        pdfGo(pdfDiffX > 0 ? pdfIndex - 1 : pdfIndex + 1);
      } else {
        pdfGo(pdfIndex);
      }
      pdfDiffX = 0;
    });

    // Keyboard arrow support
    document.addEventListener('keydown', function (e) {
      var rect = pdfTrack.getBoundingClientRect();
      if (rect.top < window.innerHeight && rect.bottom > 0) {
        if (e.key === 'ArrowLeft') pdfGo(pdfIndex - 1);
        if (e.key === 'ArrowRight') pdfGo(pdfIndex + 1);
      }
    });
  }

})();
