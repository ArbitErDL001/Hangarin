// Simple, robust PWA service worker for Hangarin
const CACHE_VERSION = 'v3';
const STATIC_CACHE = `hangarin-static-${CACHE_VERSION}`;

// Only include assets that exist to prevent install failures
const PRECACHE_URLS = [
  '/static/css/bootstrap.min.css',
  '/static/css/ready.min.css',
  '/static/js/ready.min.js',
  '/static/js/core/jquery.3.2.1.min.js',
  '/static/js/core/bootstrap.min.js',
  '/static/img/menu.png',
  '/static/img/profile.jpg',
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(STATIC_CACHE).then((cache) => cache.addAll(PRECACHE_URLS))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => Promise.all(
      keys.filter((k) => k.startsWith('hangarin-') && k !== STATIC_CACHE)
          .map((k) => caches.delete(k))
    )).then(() => self.clients.claim())
  );
});

function isNavigationRequest(request) {
  return request.mode === 'navigate' || (request.method === 'GET' && request.headers.get('accept')?.includes('text/html'));
}

self.addEventListener('fetch', (event) => {
  const { request } = event;
  if (request.method !== 'GET') return; // let non-GET pass through

  const url = new URL(request.url);

  // Strategy: Network-first for navigations (HTML), cache-first for others
  if (isNavigationRequest(request)) {
    event.respondWith(
      fetch(request)
        .then((response) => {
          const respClone = response.clone();
          caches.open(STATIC_CACHE).then((cache) => cache.put(request, respClone));
          return response;
        })
        .catch(() => caches.match(request))
    );
    return;
  }

  // For same-origin static assets, prefer cache, update in background
  if (url.origin === self.location.origin) {
    event.respondWith(
      caches.match(request).then((cached) => {
        const networkFetch = fetch(request).then((response) => {
          if (response && response.status === 200 && response.type === 'basic') {
            const respClone = response.clone();
            caches.open(STATIC_CACHE).then((cache) => cache.put(request, respClone));
          }
          return response;
        }).catch(() => cached);
        return cached || networkFetch;
      })
    );
  }
});
