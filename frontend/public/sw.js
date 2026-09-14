const CACHE_NAME = 'cropcare-ai-v1';
const STATIC_ASSETS = [
  '/',
  '/index.html',
  '/manifest.json',
  '/sample_leaves/sample_tomato_blight.jpg',
  '/sample_leaves/sample_potato_blight.jpg',
  '/sample_leaves/sample_rice_blast.jpg',
  '/sample_leaves/sample_apple_scab.jpg',
  '/sample_leaves/sample_corn_spot.jpg',
  '/sample_leaves/sample_tomato_healthy.jpg',
  '/sample_leaves/sample_unclear_leaf.jpg'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('CropCare SW: Caching static assets');
      return cache.addAll(STATIC_ASSETS).catch(err => console.warn('Cache addAll error:', err));
    })
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key))
      );
    })
  );
  self.clients.claim();
});

self.addEventListener('fetch', (event) => {
  // Network first for API, cache first for static assets
  if (event.request.url.includes('/api/')) {
    event.respondWith(
      fetch(event.request).catch(() => {
        // Return offline mock response if API is unreachable
        return new Response(JSON.stringify({
          offline: true,
          message: 'Running in offline mode. Scan will be queued for synchronization.'
        }), {
          headers: { 'Content-Type': 'application/json' }
        });
      })
    );
  } else {
    event.respondWith(
      caches.match(event.request).then((cachedResponse) => {
        if (cachedResponse) {
          return cachedResponse;
        }
        return fetch(event.request).catch(() => {
          if (event.request.mode === 'navigate') {
            return caches.match('/');
          }
        });
      })
    );
  }
});
