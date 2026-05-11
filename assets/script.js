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
