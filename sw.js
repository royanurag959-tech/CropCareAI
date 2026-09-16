const CACHE_NAME = 'cropcare-ai-v2';
const basePath = self.location.pathname.substring(0, self.location.pathname.lastIndexOf('/') + 1);

const STATIC_ASSETS = [
  basePath,
  basePath + 'index.html',
  basePath + 'manifest.json',
  basePath + 'sample_leaves/sample_tomato_blight.jpg',
  basePath + 'sample_leaves/sample_potato_blight.jpg',
  basePath + 'sample_leaves/sample_rice_blast.jpg',
  basePath + 'sample_leaves/sample_apple_scab.jpg',
  basePath + 'sample_leaves/sample_corn_spot.jpg',
  basePath + 'sample_leaves/sample_tomato_healthy.jpg',
  basePath + 'sample_leaves/sample_unclear_leaf.jpg'
];

self.addEventListener('install', (event) => {
  self.skipWaiting();
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(STATIC_ASSETS).catch(err => console.warn('Cache addAll error:', err));
    })
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key))
      );
    }).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  if (event.request.url.includes('/api/')) {
    return;
  }

  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      if (cachedResponse) {
        return cachedResponse;
      }
      return fetch(event.request).catch(() => {
        if (event.request.mode === 'navigate') {
          return caches.match(basePath) || caches.match(basePath + 'index.html');
        }
      });
    })
  );
});
