/* Service worker: network first for pages and data (hourly updates always win),
   cache first for versioned assets and images. Bump V to drop old caches. */
var V='hes-v1';
self.addEventListener('install',function(e){self.skipWaiting();});
self.addEventListener('activate',function(e){e.waitUntil(caches.keys().then(function(k){return Promise.all(k.filter(function(n){return n!==V;}).map(function(n){return caches.delete(n);}));}).then(function(){return self.clients.claim();}));});
self.addEventListener('fetch',function(e){var r=e.request,u=new URL(r.url);
 if(r.method!=='GET'||u.origin!==location.origin)return;
 var asset=/\.(css|js|webp|avif|png|jpg|svg|ico|woff2)$/.test(u.pathname);
 if(asset){e.respondWith(caches.open(V).then(function(c){return c.match(r).then(function(hit){var net=fetch(r).then(function(res){if(res.ok)c.put(r,res.clone());return res;});return hit||net;});}));return;}
 e.respondWith(fetch(r).then(function(res){if(res.ok&&/\.html$|\/$/.test(u.pathname)){var cp=res.clone();caches.open(V).then(function(c){c.put(r,cp);});}return res;}).catch(function(){return caches.match(r).then(function(h){return h||caches.match('index.html');});}));});
