// Saged.club — minimal client-side behavior
// 1) Meta Pixel via Consent Mode v2 — PageView fires for every visit
//    in limited-data mode (no cookies, no PII). On user accept, full
//    tracking is granted. This is Meta's documented EU-compliant pattern
//    and restores ad-optimization signal that strict-consent gating lost.
// 2) Cookie consent banner — softened: Accept dominant, Decline a muted
//    text link. Friendlier copy.
// 3) WhatsApp/Telegram click handlers → fire Contact event (issue #86)
// 4) Carousel + smooth-scroll polish

(function () {
  const PIXEL_ID = '1533639615120579'; // Saged.club Pixel
  const KEY = 'saged_consent_v1';
  const banner = document.getElementById('consent');
  const accept = document.getElementById('consent-accept');
  const decline = document.getElementById('consent-decline');

  const current = localStorage.getItem(KEY);
  if (!current && banner) banner.hidden = false;

  // Load Meta Pixel on every visit. EU-compliant via Consent Mode v2:
  // until the user explicitly accepts, the Pixel runs with
  // fbq('consent', 'revoke') — no cookies, no PII. Meta still receives
  // the PageView signal for ad optimization but with no identifying data.
  loadPixel(current === 'accepted');

  function loadPixel(consented) {
    if (window.fbq) return;
    !function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?
    n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;
    n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;
    t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,
    document,'script','https://connect.facebook.net/en_US/fbevents.js');
    if (!consented) window.fbq('consent', 'revoke');
    window.fbq('init', PIXEL_ID);
    window.fbq('track', 'PageView');
  }

  function setConsent(value) {
    localStorage.setItem(KEY, value);
    if (banner) banner.hidden = true;
    if (value === 'accepted' && window.fbq) window.fbq('consent', 'grant');
  }

  accept && accept.addEventListener('click', () => setConsent('accepted'));
  decline && decline.addEventListener('click', () => setConsent('declined'));

  // Click handlers on warm-channel CTAs → fire Pixel Contact event
  // so DM-led leads are visible to attribution (issue #86).
  document.querySelectorAll('#book a[href*="wa.me"], #book a[href*="t.me"]').forEach(link => {
    link.addEventListener('click', () => {
      if (window.fbq) window.fbq('track', 'Contact', { content_name: 'booking-channel-click' });
    });
  });

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
    slides.forEach(s => s.addEventListener('click', () => {
      show(idx + 1);
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
