/* Draws the A to Z tiles on places.html from places-az.json (built by tools/build_places.py).
   Each row is [slug, name, category, logo path or initials, 1 when the fourth value is a logo]. */
(function(){
"use strict";
var box=document.getElementById("pl-az");
if(!box)return;
function esc(s){return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;").replace(/'/g,"&#x27;");}
function tile(r){
var pic=r[4]?'<img src="'+esc(r[3])+'" alt="" width="48" height="48" loading="lazy" decoding="async">':'<span class="pl-ini" aria-hidden="true">'+esc(r[3])+'</span>';
return '<li><a class="pl-tile" href="place-'+esc(r[0])+'.html">'+pic+'<span><strong>'+esc(r[1])+'</strong><small>'+esc(r[2])+'</small></span></a></li>';
}
function draw(groups){
var out="";
groups.forEach(function(g){
var id="l-"+(g[0]==="#"?"num":g[0]);
out+='<section class="pl-sec" id="'+esc(id)+'"><h2>'+esc(g[0])+'</h2><ul class="pl-grid">'+g[1].map(tile).join("")+'</ul></section>';
});
box.innerHTML=out;
box.style.minHeight="";
var h=location.hash;
if(h.length>1){var t=document.getElementById(decodeURIComponent(h.slice(1)));if(t)t.scrollIntoView();}
}
function fail(){box.innerHTML='<p>The full A to Z list could not load. Use the category links above to browse every listing.</p>';box.style.minHeight="";}
fetch(box.getAttribute("data-src")).then(function(r){if(!r.ok)throw new Error(r.status);return r.json();}).then(draw).catch(fail);
})();
