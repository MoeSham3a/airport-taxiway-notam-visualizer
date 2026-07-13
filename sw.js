const CACHE_NAME = 'app-shell-v1';
const AIRPORT_CACHE = 'airports-v1';

const SHELL = [
  './',
  './index.html',
  './manifest.json',
  './airports/registry.json'
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE_NAME).then(c => c.addAll(SHELL))
  );
  self.skipWaiting();
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys => {
      return Promise.all(
        keys.filter(key => key !== CACHE_NAME && key !== AIRPORT_CACHE)
            .map(key => caches.delete(key))
      );
    })
  );
  self.clients.claim();
});

self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);
  
  // Airport chart/taxiway files: cache-then-network
  if (url.pathname.includes('/airports/')) {
    e.respondWith(
      caches.open(AIRPORT_CACHE).then(async c => {
        const cached = await c.match(e.request);
        if (cached) return cached;
        try {
          const resp = await fetch(e.request);
          if (resp.ok) {
            c.put(e.request, resp.clone());
          }
          return resp;
        } catch (err) {
          // Offline and not in cache
          return new Response('Offline', { status: 503, statusText: 'Service Unavailable' });
        }
      })
    );
  }
  // App shell: cache-first
  else {
    e.respondWith(
      caches.match(e.request).then(r => {
        return r || fetch(e.request).then(response => {
          return caches.open(CACHE_NAME).then(cache => {
            cache.put(e.request, response.clone());
            return response;
          });
        });
      })
    );
  }
});

// Listen for messages from client (e.g., force refresh)
self.addEventListener('message', event => {
  if (event.data.action === 'skipWaiting') {
    self.skipWaiting();
  } else if (event.data.action === 'clearAirportCache') {
    const icao = event.data.icao;
    event.waitUntil(
      caches.open(AIRPORT_CACHE).then(async cache => {
        const keys = await cache.keys();
        for (const req of keys) {
          if (req.url.includes(`/airports/${icao}/`)) {
            await cache.delete(req);
          }
        }
        event.ports[0].postMessage({ status: 'cleared' });
      })
    );
  }
});
