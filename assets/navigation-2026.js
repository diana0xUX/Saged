(function () {
  var dropdowns = Array.from(document.querySelectorAll('.mobile-nav, .language-select'));

  dropdowns.forEach(function (dropdown) {
    dropdown.addEventListener('toggle', function () {
      if (!dropdown.open) return;
      dropdowns.forEach(function (other) {
        if (other !== dropdown) other.open = false;
      });
    });
  });

  document.addEventListener('click', function (event) {
    dropdowns.forEach(function (dropdown) {
      if (dropdown.open && !dropdown.contains(event.target)) dropdown.open = false;
    });
  });

  var currentPath = window.location.pathname.replace(/index\.html$/, '');
  document.querySelectorAll('.mobile-nav__panel a[href^="/"]:not(.mobile-nav__cta)').forEach(function (link) {
    var linkPath = new URL(link.href, window.location.origin).pathname.replace(/index\.html$/, '');
    if (linkPath === currentPath) link.setAttribute('aria-current', 'page');
  });
}());
