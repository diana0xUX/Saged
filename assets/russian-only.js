(function () {
  var path = window.location.pathname.replace(/^\/(?:ua|en|es)(?=\/|$)/, '');
  if (!path || path === '/') path = '/';

  var supported = [
    '/',
    '/studio/',
    '/kids/',
    '/events/',
    '/private/',
    '/gifts/',
    '/coworking/',
    '/kundoglini/',
    '/privacy.html',
    '/cookies.html'
  ];

  var target = supported.indexOf(path) === -1 ? '/' : path;
  window.location.replace(target + window.location.search + window.location.hash);
}());
