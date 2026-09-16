// CropCare AI - PWA Service Worker (v5 - Network First with Auto-Recovery)
const CACHE_NAME = 'cropcare-ai-v5';
const basePath = self.location.pathname.substring(0, self.location.pathname.lastIndexOf('/') + 1);

const PRECACHE_ASSETS = [
  basePath,
  basePath + 'manifest.json',
  basePath + 'sample_leaves/sample_tomato_blight.jpg',
  basePath + 'sample_leaves/sample_potato_blight.jpg',
  basePath + 'sample_leaves/sample_rice_blast.jpg',
  basePath + 'sample_leaves/sample_apple_scab.jpg',
  basePath + 'sample_leaves/sample_corn_spot.jpg',
  basePath + 'sample_leaves/sample_tomato_healthy.jpg',
  basePath + 'sample_leaves/sample_unclear_leaf.jpg'
];

// Install: Activate immediately
self.addEventListener('install', (event) => {
  self.skipWaiting();
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(PRECACHE_ASSETS).catch((err) => {
        console.warn('Precache partial warning:', err);
      });
    })
  );
});

// Activate: Delete ALL old caches aggressively
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) {
            console.log('Cleaning old cache:', key);
            return caches.delete(key);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// Fetch: NETWORK-FIRST for HTML & Navigation (prevents stale blank screens!)
self.addEventListener('fetch', (event) => {
  // Ignore API calls or non-GET requests
  if (event.request.method !== 'GET' || event.request.url.includes('/api/')) {
    return;
  }

  const isNavigation = event.request.mode === 'navigate' || 
                       (event.request.headers.get('accept') && event.request.headers.get('accept').includes('text/html'));

  if (isNavigation) {
    // Network-First for HTML: Always fetch latest deployed index.html when online!
    event.respondWith(
      fetch(event.request)
        .then((response) => {
          if (response && response.status === 200) {
            const clone = response.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(event.request, clone));
          }
          return response;
        })
        .catch(() => {
          // If offline, fallback to cached HTML
          return caches.match(event.request)
            .then((res) => res || caches.match(basePath) || caches.match(basePath + 'index.html'));
        })
    );
    return;
  }

  // Stale-while-revalidate for JS/CSS/Images: Try network, fallback to cache
  event.respondWith(
    fetch(event.request)
      .then((networkResponse) => {
        if (networkResponse && networkResponse.status === 200) {
          const clone = networkResponse.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(event.request, clone));
        }
        return networkResponse;
      })
      .catch(() => {
        return caches.match(event.request);
      })
  );
});
