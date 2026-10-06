var CACHE_NAME = 'hangarin-pwa-v7';
var PRECACHE_URLS = [
  '/',
  '/accounts/login/',
  '/static/img/icon-192.png',
  '/static/img/icon-512.png'
];

self.addEventListener('install', function(e) {
  e.waitUntil(
    caches.open(CACHE_NAME).then(function(cache) {
      return Promise.all(
        PRECACHE_URLS.map(function(url) {
          return fetch(url).then(function(response) {
            if (response && response.status === 200) {
              return cache.put(url, response);
            }
          }).catch(function(err) {
            console.log('SW precache skip for ' + url + ':', err);
          });
        })
      );
    }).then(function() {
      return self.skipWaiting();
    })
  );
});

self.addEventListener('activate', function(e) {
  e.waitUntil(
    caches.keys().then(function(cacheNames) {
      return Promise.all(
        cacheNames.map(function(cacheName) {
          if (cacheName !== CACHE_NAME) {
            return caches.delete(cacheName);
          }
        })
      );
    }).then(function() {
      return self.clients.claim();
    })
  );
});

self.addEventListener('fetch', function(e) {
  if (e.request.method !== 'GET') return;

  e.respondWith(
    fetch(e.request).then(function(networkResponse) {
      if (networkResponse && networkResponse.status === 200 && networkResponse.type === 'basic') {
        var responseToCache = networkResponse.clone();
        caches.open(CACHE_NAME).then(function(cache) {
          cache.put(e.request, responseToCache);
        });
      }
      return networkResponse;
    }).catch(function() {
      return caches.match(e.request).then(function(cachedResponse) {
        if (cachedResponse) {
          return cachedResponse;
        }
        if (e.request.headers.get('accept') && e.request.headers.get('accept').includes('text/html')) {
          return caches.match('/accounts/login/') || caches.match('/');
        }
      });
    })
  );
});

