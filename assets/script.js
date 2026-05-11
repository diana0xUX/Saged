// Saged.club — minimal client-side behavior
// 1) cookie consent banner (EU-compliant: nothing tracks before opt-in)
// 2) smooth-scroll polish (browsers do this natively, but force focus for a11y)

(function () {
  const KEY = 'saged_consent_v1';
  const banner = document.getElementById('consent');
  const accept = document.getElementById('consent-accept');
  const decline = document.getElementById('consent-decline');

  const current = localStorage.getItem(KEY);
  if (!current && banner) banner.hidden = false;

  function setConsent(value) {
    localStorage.setItem(KEY, value);
    if (banner) banner.hidden = true;
    if (value === 'accepted') initTracking();
  }

  accept && accept.addEventListener('click', () => setConsent('accepted'));
  decline && decline.addEventListener('click', () => setConsent('declined'));

  if (current === 'accepted') initTracking();

  function initTracking() {
    // Meta Pixel + any other trackers go here.
    // For now, leave as a no-op until PIXEL_ID is configured.
    // The pixel <script> in the page <head> is commented out — uncomment + replace YOUR_PIXEL_ID after Phase 1.
  }

  // carousel — fade between slides, auto-advance every 6s, pause on hover/focus
  document.querySelectorAll('.carousel').forEach(c => {
    const slides = c.querySelectorAll('.carousel__slide');
    const dots = c.querySelectorAll('.carousel__dots button');
    if (slides.length < 2) return;
    let idx = 0;
    let timer = null;
    const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;

    function show(n) {
      slides[idx].classList.remove('is-active');
      dots[idx] && dots[idx].classList.remove('is-active');
      idx = (n + slides.length) % slides.length;
      slides[idx].classList.add('is-active');
      dots[idx] && dots[idx].classList.add('is-active');
    }
    function start() { if (!reduced) timer = setInterval(() => show(idx + 1), 6000); }
    function stop() { if (timer) { clearInterval(timer); timer = null; } }

    dots.forEach(d => d.addEventListener('click', () => {
      show(parseInt(d.dataset.slide, 10));
      stop(); start();
    }));
    c.addEventListener('mouseenter', stop);
    c.addEventListener('mouseleave', start);
    c.addEventListener('focusin', stop);
    c.addEventListener('focusout', start);

    // start only when in view (saves cycles before scroll)
    const io = new IntersectionObserver(entries => {
      entries.forEach(e => e.isIntersecting ? start() : stop());
    });
    io.observe(c);
  });

  // a11y: when a hash link is clicked, move focus to the target after scroll
  document.querySelectorAll('a[href^="#"]').forEach(link => {
    link.addEventListener('click', e => {
      const id = link.getAttribute('href').slice(1);
      const target = document.getElementById(id);
      if (target) {
        setTimeout(() => target.setAttribute('tabindex', '-1'), 0);
        setTimeout(() => target.focus({ preventScroll: true }), 400);
      }
    });
  });
})();
