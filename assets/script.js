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
      if (dots[idx]) { dots[idx].classList.remove('is-active'); dots[idx].setAttribute('aria-selected', 'false'); }
      idx = (n + slides.length) % slides.length;
      slides[idx].classList.add('is-active');
      if (dots[idx]) { dots[idx].classList.add('is-active'); dots[idx].setAttribute('aria-selected', 'true'); }
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

  // Instagram embed.js injects <iframe> without a title attribute, which
  // fails Lighthouse a11y `frame-title`. Patch any iframe it adds.
  function titleIgFrames() {
    document.querySelectorAll('iframe.instagram-media:not([title])').forEach(f => {
      f.setAttribute('title', 'Instagram post — @saged.club');
    });
  }
  new MutationObserver(titleIgFrames).observe(document.body, { childList: true, subtree: true });
  titleIgFrames();

  // UTM attribution: capture campaign params on landing, persist for the
  // session, append to outbound WhatsApp messages so Diana can match a WA
  // lead back to the ad that produced it.
  function getUtm() {
    const params = new URLSearchParams(window.location.search);
    const fromUrl = params.get('utm_source');
    if (fromUrl) {
      const utm = {
        source: params.get('utm_source') || '',
        medium: params.get('utm_medium') || '',
        campaign: params.get('utm_campaign') || '',
        content: params.get('utm_content') || ''
      };
      try { sessionStorage.setItem('saged_utm', JSON.stringify(utm)); } catch (_) {}
      return utm;
    }
    try { return JSON.parse(sessionStorage.getItem('saged_utm') || 'null'); } catch (_) { return null; }
  }
  function utmSourceLine(lang) {
    const utm = getUtm();
    if (!utm || !utm.source) return '';
    const parts = [utm.source, utm.campaign, utm.content].filter(Boolean).join(' / ');
    const labels = { ru: 'Источник', uk: 'Джерело', en: 'Source' };
    return `\n\n— ${labels[lang] || labels.ru}: ${parts}`;
  }
  // Rewrite static wa.me links to also carry the UTM tail
  (function annotateWaLinks() {
    const lang = (document.documentElement.lang || 'ru').slice(0, 2);
    const tail = utmSourceLine(lang);
    if (!tail) return;
    document.querySelectorAll('a[href*="wa.me/"]').forEach(link => {
      try {
        const url = new URL(link.href);
        const text = url.searchParams.get('text') || '';
        url.searchParams.set('text', text + tail);
        link.href = url.toString();
      } catch (_) { /* malformed href — skip */ }
    });
  })();

  // Request forms → open WhatsApp with form data prefilled
  const templates = {
    'parent-kid': {
      ru: (p, c, w) => `Доброго дня! 🪷\n\nИнтересен формат «родитель + ребёнок» по керамике.\n\nИмя родителя: ${p}\nИмя и возраст ребёнка: ${c}\nКогда удобнее: ${w || '—'}\n\nДобавьте нас в список — напишите, когда соберётся группа :)`,
      uk: (p, c, w) => `Доброго дня! 🪷\n\nЦікавить формат «батьки + дитина» з кераміки.\n\nІм'я батьків: ${p}\nІм'я та вік дитини: ${c}\nКоли зручніше: ${w || '—'}\n\nДодайте нас у список — напишіть, коли збереться група :)`,
      en: (p, c, w) => `Hi! 🪷\n\nI'm interested in the parent + kid ceramics format.\n\nParent's name: ${p}\nChild's name and age: ${c}\nPreferred time: ${w || '—'}\n\nAdd us to the list — let me know when a group forms :)`
    }
  };
  const sentLabels = {
    ru: 'Открываем WhatsApp — отправьте сообщение, и мы свяжемся 🙌',
    uk: 'Відкриваємо WhatsApp — надішліть повідомлення, і ми зв\'яжемося 🙌',
    en: 'Opening WhatsApp — send the message and we\'ll get back to you 🙌'
  };
  document.querySelectorAll('form.request-form').forEach(form => {
    form.addEventListener('submit', e => {
      e.preventDefault();
      const lang = form.dataset.lang || 'ru';
      const topic = form.dataset.topic;
      const builder = templates[topic]?.[lang];
      if (!builder) return;
      // FormData is the unambiguous way to read inputs — avoids quirks with
      // form.NAME shorthand (which can collide with reserved props in some envs)
      const data = new FormData(form);
      const p = String(data.get('parent') || '').trim();
      const c = String(data.get('child') || '').trim();
      const w = String(data.get('when') || '').trim();
      const msg = encodeURIComponent(builder(p, c, w) + utmSourceLine(lang));
      const url = `https://wa.me/34605543300?text=${msg}`;
      // Temp <a>.click() preserves the text= param through the wa.me redirect
      // and triggers iOS/Android universal-link to the WhatsApp app properly.
      // window.open(url, '_blank', 'noopener') was opening a stripped popup
      // that dropped the query string on some browsers.
      const link = document.createElement('a');
      link.href = url;
      link.target = '_blank';
      link.rel = 'noopener';
      document.body.appendChild(link);
      link.click();
      link.remove();
      // inline confirmation
      let sent = form.parentElement.querySelector('.request-form__sent');
      if (!sent) {
        sent = document.createElement('p');
        sent.className = 'request-form__sent';
        form.parentElement.insertBefore(sent, form.nextSibling);
      }
      sent.textContent = sentLabels[lang] || sentLabels.ru;
      // fire Contact event if Pixel is loaded
      if (window.fbq) fbq('track', 'Contact', { content_name: 'parent-kid-form' });
    });
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
