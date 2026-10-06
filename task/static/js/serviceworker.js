var CACHE_NAME = 'hangarin-pwa-v5';
var urlsToCache = [
  '/',
  '/accounts/login/',
  '/tasks/',
  '/subtasks/',
  '/notes/',
  '/categories/',
  '/priorities/',
  '/static/img/icon-192.png',
  '/static/img/icon-512.png'
];

self.addEventListener('install', function(e) {
  e.waitUntil(
    caches.open(CACHE_NAME).then(function(cache) {
      return Promise.all(
        urlsToCache.map(function(url) {
          return fetch(url).then(function(response) {
            if (response && response.status === 200) {
              return cache.put(url, response);
            }
          }).catch(function(err) {
            console.log('SW cache skip for ' + url + ':', err);
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
    caches.match(e.request).then(function(response) {
      if (response) {
        return response;
      }
      return fetch(e.request).then(function(networkResponse) {
        return networkResponse;
      }).catch(function() {
        if (e.request.headers.get('accept') && e.request.headers.get('accept').includes('text/html')) {
          return caches.match('/accounts/login/') || caches.match('/');
        }
      });
    })
  );
});

