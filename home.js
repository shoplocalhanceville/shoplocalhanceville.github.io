/* Homepage behavior. Moved out of index.html so the page paints before this runs; each block keeps its original order and is isolated so one error cannot stop the others. Needs data.js (and data-es.js in Spanish) loaded first. */
try{
window.SLH_REG = "img/home/f7679b5094c0.webp";window.SLH_CONTENT=function(r){return ["Fun Facts","Sweet Tea Jokes","Getting Started","Everyone","Social Media"].indexOf(r.category)>=0||["Attractions, Farms & Recreation","Businesses & Services","Lodging & Campgrounds","Nonprofits, Counseling & Community Organizations","Restaurants, Food & Drink"].indexOf(r.name)>=0;};
}catch(e){if(window.console)console.error(e);}
try{
(function(){
"use strict";
var root=document.documentElement;
function paintToggle(){var b=document.getElementById("themeToggle");if(!b)return;
  var dark=root.getAttribute("data-theme")==="dark";
  b.innerHTML=dark?'<svg class="ic"><use href="#i-sun"/></svg> '+(window.SLH_LANG==="es"?"D\u00eda":"Day"):'<svg class="ic"><use href="#i-moon"/></svg> '+(window.SLH_LANG==="es"?"Noche":"Night");b.setAttribute("aria-pressed",dark?"true":"false");}
try{var t=localStorage.getItem("hes-theme");
  if(t)root.setAttribute("data-theme",t);
  else if(window.matchMedia&&window.matchMedia("(prefers-color-scheme: dark)").matches)
    root.setAttribute("data-theme","dark");}catch(e){}
paintToggle();
document.getElementById("themeToggle").addEventListener("click",function(){
  var cur=root.getAttribute("data-theme")==="dark"?"light":"dark";
  root.setAttribute("data-theme",cur);
  try{localStorage.setItem("hes-theme",cur);}catch(e){}
  paintToggle();});
var L=window.SLH_LISTINGS||[];
function slug(s){return (s||"").toLowerCase().replace(/[^a-z0-9]+/g,"-").replace(/^-|-$/g,"");}
function favs(){try{return JSON.parse(localStorage.getItem("slh-favs")||"[]");}catch(e){return[];}}
function setFavs(f){try{localStorage.setItem("slh-favs",JSON.stringify(f));}catch(e){}}
function T(en){return (LANG==="es"&&window.SLH_UI&&window.SLH_UI[en])||en;}
function hsStatus(r){var hs=r.hs;if(!hs)return null;
  var parts={};new Intl.DateTimeFormat("en-US",{timeZone:"America/Chicago",weekday:"short",hour:"2-digit",minute:"2-digit",hourCycle:"h23"}).formatToParts(new Date()).forEach(function(p){parts[p.type]=p.value;});
  var dm={Sun:"sun",Mon:"mon",Tue:"tue",Wed:"wed",Thu:"thu",Fri:"fri",Sat:"sat"};
  var v=hs[dm[parts.weekday]];if(v==="24")return "open";if(v==null)return null;if(v==="x")return "closed";
  var seg=v.split("-");function mn(t){var q=t.split(":");return (+q[0])*60+(+q[1]);}
  var now=(+parts.hour)*60+(+parts.minute);return (now>=mn(seg[0])&&now<mn(seg[1]))?"open":"closed";}


function isFav(n){return favs().indexOf(n)>=0;}
/* weather */
var wx=document.getElementById("wxNow");
if(wx){var wxCtl=window.AbortController?new AbortController():null;
 if(wxCtl)setTimeout(function(){wxCtl.abort();},9000);
 fetch("https://api.weather.gov/points/34.0614,-86.7633",{headers:{"Accept":"application/geo+json"},signal:wxCtl?wxCtl.signal:undefined})
 .then(function(r){return r.json();})
 .then(function(p){return fetch(p.properties.forecast,{headers:{"Accept":"application/geo+json"},signal:wxCtl?wxCtl.signal:undefined});})
 .then(function(r){return r.json();})
 .then(function(f){var t=f.properties.periods[0];
   wx.textContent="Hanceville now: "+t.temperature+"\u00B0"+t.temperatureUnit+", "+t.shortForecast+" (National Weather Service)";})
 .catch(function(){wx.textContent="Weather unavailable right now \u2014 see weather.gov.";});}
/* ---------- filtering state ---------- */
var q=document.getElementById("q"),catSel=document.getElementById("catSel"),
    sortSel=document.getElementById("sortSel"),savedOnly=document.getElementById("savedOnly"),openNow=document.getElementById("openNow"),
    grid=document.getElementById("grid"),count=document.getElementById("count"),
    more=document.getElementById("more"),townFilter="";
var SYN={food:"restaurant",eats:"restaurant",hair:"barber",doctor:"clinic",health:"clinic",gas:"gas station",fuel:"gas station",kids:"children"};
/* ---------- language + keyword search helpers ---------- */
var LANG=window.SLH_LANG||"en";

function catName(c){return (LANG==="es"&&window.SLH_CAT&&window.SLH_CAT[c])||c;}
function descOf(r){return (LANG==="es"&&window.SLH_DESC_ES&&SLH_DESC_ES[r.name])?SLH_DESC_ES[r.name]:(r.description||"");}
function norm(s){return (s||"").toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g,"");}
function hayOf(r){return norm(r.name+" "+(r.category||"")+" "+(r.address||"")+" "+(r.aka||"")+" "+(r.description||"")+" "+((window.SLH_DESC_ES&&SLH_DESC_ES[r.name])||""));}
var BATCH=24,shown=0,filtered=L.slice();
function variantize(im, sizes){
  var v=(window.SLH_VARIANTS||{})[im.getAttribute("src")||""];
  if(!v)return im;
  im.srcset=v.w;im.setAttribute("sizes",sizes);im.decoding="async";
  if(!v.a)return im;
  var pic=document.createElement("picture");pic.style.display="block";
  var so=document.createElement("source");so.type="image/avif";so.srcset=v.a;so.setAttribute("sizes",sizes);
  pic.appendChild(so);pic.appendChild(im);
  return pic;
}
function card(r){
  var art=document.createElement("article");art.className="card";art.id=slug(r.name);
  if(r.wallace)art.classList.add("wallace");
  var usePh=!r.logo&&window.SLH_CONTENT(r);var im=document.createElement(usePh?"div":"img");im.className=usePh?"logo ph":"logo";if(usePh){im.textContent="\u2605";im.setAttribute("role","img");im.setAttribute("aria-label",r.name);}else{im.loading="lazy";}
  if(!usePh){im.alt=r.logo?r.name+" logo":"Register your business";im.src=r.logo||window.SLH_REG;}
  if(r.logo&&(/-w\.svg$/.test(r.logo))){try{if(1){im.style.background="#241243";im.style.padding="10px";im.style.boxSizing="border-box";}}catch(e){}}
  if(!usePh)im.addEventListener("click",function(){openZoom(im.src,r.name);});
  im.onerror=function(){im.remove();};art.appendChild(variantize(im,"(max-width: 700px) 362px, 310px"));
  var h=document.createElement("h3");h.textContent=r.name;art.appendChild(h);
  if(r.category){var c=document.createElement("p");c.className="cat";c.textContent=catName(r.category);art.appendChild(c);}
  if(r.hs){var st=hsStatus(r);var sp=document.createElement("p");sp.className="openst";sp.textContent=st==="open"?T("Open now"):st==="closed"?T("Closed right now"):T("Hours not listed for today");art.appendChild(sp);}
  if(r.portraits){var pr=document.createElement("div");pr.style.display="flex";pr.style.gap="10px";pr.style.flexWrap="wrap";
    r.portraits.forEach(function(pp){var fig=document.createElement("figure");fig.style.margin="0";fig.style.textAlign="center";
      var pi=document.createElement("img");pi.src=pp.img;pi.alt=pp.name;pi.loading="lazy";
      pi.style.width="64px";pi.style.height="64px";pi.style.objectFit="cover";pi.style.borderRadius="50%";pi.style.border="2px solid var(--purple)";
      var cap=document.createElement("figcaption");cap.style.fontSize="12.5px";cap.style.maxWidth="86px";
      cap.textContent=pp.name+", "+pp.title;fig.appendChild(pi);fig.appendChild(cap);pr.appendChild(fig);});
    art.appendChild(pr);}
  if(r.address){var a=document.createElement("p");a.className="addr";a.textContent=r.address;art.appendChild(a);}
  var dtx=descOf(r);
  if(dtx){var dp=document.createElement("p");dp.className="desc";dp.textContent=dtx;art.appendChild(dp);}
  var acts=document.createElement("div");acts.className="actions";
  if(r.phone){var call=document.createElement("a");call.className="btn btn-primary";
    call.href="tel:"+r.phone.replace(/[^0-9+]/g,"");call.innerHTML='<svg class="ic"><use href="#i-phone"/></svg> '+T("Call");acts.appendChild(call);}
  if(r.website){var w=document.createElement("a");w.className="btn";w.href=r.website;
    w.target="_blank";w.rel="noopener";w.innerHTML='<svg class="ic"><use href="#i-globe"/></svg> '+T("Website");acts.appendChild(w);}
  if(r.address){var d=document.createElement("a");d.className="btn";
    d.href="https://www.google.com/maps/search/?api=1&query="+encodeURIComponent(r.name+" "+r.address);
    d.target="_blank";d.rel="noopener";d.innerHTML='<svg class="ic"><use href="#i-pin"/></svg> '+T("Directions");acts.appendChild(d);}
  var sv=document.createElement("button");sv.className="btn";sv.type="button";
  sv.setAttribute("aria-pressed",isFav(r.name)?"true":"false");
  var st=document.createElement("span");st.className="star";st.textContent=isFav(r.name)?"\u2605":"\u2606";
  sv.appendChild(st);sv.appendChild(document.createTextNode(" "+T("Save")));
  sv.addEventListener("click",function(){var f=favs(),i=f.indexOf(r.name);
    if(i>=0){f.splice(i,1);sv.setAttribute("aria-pressed","false");st.textContent="\u2606";}
    else{f.push(r.name);sv.setAttribute("aria-pressed","true");st.textContent="\u2605";}
    setFavs(f);});
  acts.appendChild(sv);
  var sh=document.createElement("button");sh.className="btn";sh.type="button";
  sh.innerHTML='<svg class="ic"><use href="#i-ext"/></svg> '+T("Share");
  sh.addEventListener("click",function(){
    var url=location.href.split("#")[0]+"#"+slug(r.name);
    if(navigator.share){navigator.share({title:r.name,text:r.name+" - Hanceville Entertainment and Shopping",url:url}).catch(function(){});}
    else if(navigator.clipboard){navigator.clipboard.writeText(url).then(function(){sh.lastChild.textContent=" Link copied";});}
    else{window.prompt("Copy this link:",url);}});
  acts.appendChild(sh);
  if(["Fun Facts","Sweet Tea Jokes","Social Media"].indexOf(r.category)<0){var fpg=document.createElement("a");fpg.className="btn";fpg.setAttribute("href",["place",slug(r.name)].join("-")+".html");fpg.textContent=T("See full page");acts.appendChild(fpg);}
  if(r.facebook){var fb=document.createElement("button");fb.className="btn";fb.type="button";
    fb.textContent=T("See latest post");
    fb.addEventListener("click",function(){loadEmbed(art,r);fb.remove();});
    acts.appendChild(fb);}
  art.appendChild(acts);return art;
}
var liveEmbeds=0;
function loadEmbed(art,r){
  var box=document.createElement("div");box.className="embedbox";
  if(liveEmbeds>=6){var p=document.createElement("p");p.textContent="Several posts are open. ";
    var b=document.createElement("a");b.href=r.facebook;b.target="_blank";b.rel="noopener";
    b.textContent="Open on Facebook";box.appendChild(p);box.appendChild(b);art.appendChild(box);return;}
  var f=document.createElement("iframe");f.title=r.name+" on Facebook";f.loading="lazy";f.height=420;
  f.setAttribute("allow","encrypted-media");
  f.src="https://www.facebook.com/plugins/page.php?href="+encodeURIComponent(r.facebook)+
    "&tabs=timeline&width=340&height=420&small_header=true&adapt_container_width=true&hide_cover=false&show_facepile=false";
  var loaded=false;
  f.addEventListener("load",function(){loaded=true;});
  box.appendChild(f);art.appendChild(box);liveEmbeds++;
  setTimeout(function(){if(loaded)return;box.textContent="";
    var p=document.createElement("p");p.textContent="This Facebook post could not be loaded here. ";
    var b=document.createElement("a");b.href=r.facebook;b.target="_blank";b.rel="noopener";
    b.textContent="Open on Facebook";box.appendChild(p);box.appendChild(b);},9000);
}
function apply(scroll){
  var term=norm(q.value||"").replace(/\bnear me\b/g," ").replace(/\bcerca de mi\b/g," ").trim();
  if(SYN[term])term=SYN[term];
  var toks=term.split(/\s+/).filter(Boolean);
  var cat=catSel.value;
  filtered=L.filter(function(r){
    if(cat&&r.category!==cat)return false;
    if(townFilter&&(r.address||"").indexOf(townFilter)<0&&(r.name||"").indexOf(townFilter)<0)return false;
    if(savedOnly.checked&&!isFav(r.name))return false;
    if(openNow.checked&&hsStatus(r)!=="open")return false;
    if(!toks.length)return true;
    var hay=hayOf(r);
    return toks.every(function(t){return hay.indexOf(t)>=0;});});
  if(sortSel.value==="kind")filtered.sort(function(a,b){return (a.category||"").localeCompare(b.category||"")||a.name.localeCompare(b.name);});
  else filtered.sort(function(a,b){return a.name.localeCompare(b.name);});
  shown=0;grid.textContent="";renderMore();
  count.textContent=filtered.length+" "+T("places found")+(townFilter?(LANG==="es"?" en ":" in ")+townFilter:"");
  document.getElementById("noresults").hidden=filtered.length>0;
  if(scroll)document.getElementById("results").scrollIntoView({behavior:"smooth"});
}
/* WS4 prototype: chunked rendering (INP pattern). Build cards in small
   chunks and yield to the main thread between chunks so no single task
   runs long; a generation counter makes a newer apply() supersede any
   render still in flight. Final DOM is identical to the original. */
function yieldToMain(){
  if(window.scheduler&&typeof scheduler.yield==="function")return scheduler.yield();
  return new Promise(function(res){setTimeout(res,0);});
}
var renderGen=0,CHUNK=6;
async function renderMore(){
  var gen=++renderGen;
  var end=Math.min(shown+BATCH,filtered.length);
  while(shown<end){
    if(gen!==renderGen)return;
    var frag=document.createDocumentFragment();
    var stop=Math.min(shown+CHUNK,end);
    for(var i=shown;i<stop;i++){frag.appendChild(card(filtered[i]));}
    shown=stop;
    grid.appendChild(frag);
    if(shown<end)await yieldToMain();
  }
  if(gen===renderGen)more.style.display=shown<filtered.length?"block":"none";
}
more.addEventListener("click",renderMore);
q.addEventListener("input",function(){apply(false);suggest();});
catSel.addEventListener("change",function(){apply(false);syncTiles();});
sortSel.addEventListener("change",function(){apply(false);});
openNow.addEventListener("change",function(){apply(false);});
savedOnly.addEventListener("change",function(){apply(false);});
/* categories into select */
var cats={};L.forEach(function(r){if(r.category)cats[r.category]=(cats[r.category]||0)+1;});
Object.keys(cats).sort().forEach(function(c){var o=document.createElement("option");
  o.value=c;o.textContent=catName(c);catSel.appendChild(o);});
/* ---------- kind rail ---------- */
var krail=document.getElementById("krail");
function syncTiles(){krail.querySelectorAll(".ktile").forEach(function(b){
  b.setAttribute("aria-pressed",b.getAttribute("data-cat")===catSel.value?"true":"false");});}
Object.keys(cats).sort(function(a,b){return cats[b]-cats[a];}).forEach(function(c){
  var b=document.createElement("button");b.className="ktile";b.type="button";b.setAttribute("data-cat",c);
  b.setAttribute("aria-pressed","false");
  var CATICON=[["barber","#i-scissors"],["salon","#i-scissors"],["restaurant","#i-food"],["food","#i-food"],["church","#i-church"],["school","#i-cap"],["education","#i-cap"],["auto","#i-wrench"],["government","#i-landmark"],["shopping","#i-bag"],["retail","#i-bag"],["community","#i-users"],["help","#i-heart"],["resource","#i-heart"],["health","#i-heart"],["business","#i-bag"],["local","#i-bag"]];
  var icn="#i-list";var cl=c.toLowerCase();
  for(var k=0;k<CATICON.length;k++){if(cl.indexOf(CATICON[k][0])>=0){icn=CATICON[k][1];break;}}
  var svg=document.createElementNS("http://www.w3.org/2000/svg","svg");svg.setAttribute("class","ic");
  var use=document.createElementNS("http://www.w3.org/2000/svg","use");use.setAttribute("href",icn);svg.appendChild(use);b.appendChild(svg);
  b.appendChild(document.createTextNode(catName(c)));
  var sm=document.createElement("small");sm.textContent=cats[c]+" "+(LANG==="es"?"lugares":"places");b.appendChild(sm);
  b.addEventListener("click",function(){
    catSel.value=(catSel.value===c)?"":c;syncTiles();apply(true);});
  krail.appendChild(b);});
/* quick chips */
document.querySelectorAll("[data-quick]").forEach(function(b){
  b.addEventListener("click",function(){q.value=b.getAttribute("data-quick");apply(true);});});
/* ---------- featured rail + spotlight ---------- */
var pool=L.filter(function(r){return r.logo;});
var day=Math.floor(Date.now()/86400000);
var feat=document.getElementById("frail");
var picks=[];var cnu=null;
pool.forEach(function(r){if(r.name==="Cut N Up Barber and Style")cnu=r;});
if(cnu)picks.push(cnu);
for(var i=0;picks.length<12&&picks.length<pool.length;i++){
  var cand=pool[(day*7+i)%pool.length];
  if(picks.indexOf(cand)<0)picks.push(cand);
}
picks.forEach(function(r){
  var fc=document.createElement("div");fc.className="fcard";if(r.wallace)fc.classList.add("wallace");
  var im=document.createElement("img");im.src=r.logo;im.alt="";if(r.logo&&(/-w\.svg$/.test(r.logo))){try{if(1){im.style.background="#241243";im.style.padding="10px";im.style.boxSizing="border-box";}}catch(e){}}fc.appendChild(variantize(im,"224px"));
  var h=document.createElement("h3");h.textContent=r.name;fc.appendChild(h);
  var lk=document.createElement("a");lk.className="btn btn-primary";lk.href=(["Fun Facts","Sweet Tea Jokes","Social Media"].indexOf(r.category)<0?"place-"+slug(r.name)+".html":"#"+slug(r.name));
  lk.textContent="See listing";
  lk.addEventListener("click",function(rr){return function(ev){if(ev.currentTarget.getAttribute("href").charAt(0)!=="#")return;ev.preventDefault();
    q.value="";catSel.value="";townFilter="";savedOnly.checked=false;apply(false);
    var fel=document.getElementById(slug(rr.name));
    while(!fel&&shown<filtered.length){renderMore();fel=document.getElementById(slug(rr.name));}
    if(fel)setTimeout(function(){fel.scrollIntoView({behavior:"smooth"});},80);};}(r));
  fc.appendChild(lk);feat.appendChild(fc);
});
var sp=document.getElementById("spotName");
if(sp&&pool.length){sp.textContent=pool[day%pool.length].name;}
/* ---------- towns rail ---------- */
var towns={};L.forEach(function(r){var m=(r.address||"").match(/,\s*([A-Za-z ]+),\s*AL/);
  if(m)towns[m[1].trim()]=(towns[m[1].trim()]||0)+1;});
var trail=document.getElementById("trail");
Object.keys(towns).sort(function(a,b){return towns[b]-towns[a];}).forEach(function(t){
  if(towns[t]<3)return;
  var b=document.createElement("button");b.className="ktile";b.type="button";
  b.appendChild(document.createTextNode(t));
  var sm=document.createElement("small");sm.textContent=towns[t]+" places";b.appendChild(sm);
  b.addEventListener("click",function(){
    townFilter=(townFilter===t)?"":t;
    trail.querySelectorAll(".ktile").forEach(function(x){x.setAttribute("aria-pressed","false");});
    if(townFilter)b.setAttribute("aria-pressed","true");
    apply(true);});
  trail.appendChild(b);});
/* rail arrows */
document.querySelectorAll("[data-rail]").forEach(function(btn){
  btn.addEventListener("click",function(){
    var rail=document.getElementById(btn.getAttribute("data-rail"));
    rail.scrollBy({left:(btn.getAttribute("data-dir")==="left"?-1:1)*rail.clientWidth*0.8,behavior:"smooth"});});});
/* ---------- live suggestions ---------- */
var sug=document.getElementById("suggest");
function suggest(){
  var term=(q.value||"").toLowerCase().trim();
  if(term.length<2){sug.hidden=true;sug.textContent="";return;}
  var hits=L.filter(function(r){return r.name.toLowerCase().indexOf(term)>=0;}).slice(0,6);
  if(!hits.length){sug.hidden=true;return;}
  sug.textContent="";
  hits.forEach(function(r){
    var b=document.createElement("button");b.type="button";
    var im=document.createElement("img");im.src=r.logo||window.SLH_REG;im.alt="";
    b.appendChild(variantize(im,"46px"));
    var tx=document.createElement("span");tx.textContent=r.name+" ";
    var sm=document.createElement("small");sm.textContent=r.category||"";
    tx.appendChild(sm);b.appendChild(tx);
    b.addEventListener("click",function(){sug.hidden=true;q.value=r.name;apply(false);
      setTimeout(function(){var el=document.getElementById(slug(r.name));if(el)el.scrollIntoView({behavior:"smooth"});},80);});
    sug.appendChild(b);});
  sug.hidden=false;
}
document.addEventListener("click",function(ev){if(!sug.contains(ev.target)&&ev.target!==q)sug.hidden=true;});
document.getElementById("qGo").addEventListener("click",function(){sug.hidden=true;apply(true);});
/* ---------- saved tab ---------- */
var svTab=document.getElementById("savedTab");
if(svTab)svTab.addEventListener("click",function(ev){ev.preventDefault();
  savedOnly.checked=true;apply(true);});
/* ---------- zoom ---------- */
var dlg=document.getElementById("zoomDlg"),zimg=document.getElementById("zoomImg"),scale=1;
function openZoom(src,name){zimg.src=src;zimg.alt=name;scale=1;zimg.style.transform="scale(1)";dlg.showModal();}
document.getElementById("zBig").addEventListener("click",function(){scale=Math.min(3,scale+.25);zimg.style.transform="scale("+scale+")";});
document.getElementById("zSmall").addEventListener("click",function(){scale=Math.max(.5,scale-.25);zimg.style.transform="scale("+scale+")";});
document.getElementById("zFit").addEventListener("click",function(){scale=1;zimg.style.transform="scale(1)";});
document.getElementById("zClose").addEventListener("click",function(){dlg.close();});
document.getElementById("toTop").addEventListener("click",function(){window.scrollTo({top:0,behavior:"smooth"});});
apply(false);
var h0=location.hash.slice(1);
if(h0){var tgt=null;
  for(var hi=0;hi<L.length;hi++){if(slug(L[hi].name)===h0){tgt=L[hi];break;}}
  if(tgt){q.value="";catSel.value="";townFilter="";savedOnly.checked=false;apply(false);
    var el=document.getElementById(h0);
    while(!el&&shown<filtered.length){renderMore();el=document.getElementById(h0);}
    if(el)setTimeout(function(){el.scrollIntoView({block:"center"});el.style.outline="3px solid var(--purple)";},80);}}
})();
}catch(e){if(window.console)console.error(e);}
try{
(function(){var live=0;
document.querySelectorAll(".pgload").forEach(function(b){
 b.addEventListener("click",function(){
   if(live>=2){window.open(b.getAttribute("data-url"),"_blank","noopener");return;}
   live++;var box=b.parentElement.querySelector(".pgbox");
   var f=document.createElement("iframe");
   f.src="https://www.facebook.com/plugins/page.php?href="+encodeURIComponent(b.getAttribute("data-url"))+"&tabs=timeline&width=500&height=420&small_header=false&adapt_container_width=true&hide_cover=false&show_facepile=false";
   f.style.width="100%";f.style.height="420px";f.style.border="0";f.style.borderRadius="12px";
   f.setAttribute("loading","lazy");f.title="Facebook page posts";
   var loaded=false;f.addEventListener("load",function(){loaded=true;});
   box.appendChild(f);b.remove();
   setTimeout(function(){if(loaded)return;box.textContent="";
     var p=document.createElement("p");p.textContent="This Facebook post could not be loaded here. ";
     var a=document.createElement("a");a.href=b.getAttribute("data-url");a.target="_blank";a.rel="noopener";
     a.textContent="Open on Facebook";box.appendChild(p);box.appendChild(a);},9000);
 });});
})();
}catch(e){if(window.console)console.error(e);}
try{
(function(){
var btn=document.getElementById("menuBtn"),panel=document.getElementById("menuPanel");
if(!btn||!panel)return;
function close(){panel.hidden=true;btn.setAttribute("aria-expanded","false");}
btn.addEventListener("click",function(e){e.stopPropagation();
  var open=panel.hidden;panel.hidden=!open;btn.setAttribute("aria-expanded",open?"true":"false");});
document.addEventListener("click",function(e){if(!panel.hidden&&!panel.contains(e.target))close();});
document.addEventListener("keydown",function(e){if(e.key==="Escape")close();});
panel.querySelectorAll("a").forEach(function(a){a.addEventListener("click",function(){
  close();
  if(a.id==="menuSaved"){var st=document.getElementById("savedTab");if(st)setTimeout(function(){st.click();},50);}
  if(a.getAttribute("data-menu")==="search"){setTimeout(function(){var q=document.getElementById("q");if(q)q.focus();},350);}
});});
})();
}catch(e){if(window.console)console.error(e);}
try{
(function(){
/* weather alerts for the Hanceville point */
var wxaCtl=window.AbortController?new AbortController():null;
if(wxaCtl)setTimeout(function(){wxaCtl.abort();},9000);
fetch("https://api.weather.gov/alerts/active?point=34.0614,-86.7633",{headers:{"Accept":"application/geo+json"},signal:wxaCtl?wxaCtl.signal:undefined})
 .then(function(r){return r.json();}).then(function(d){
  if(!d.features||!d.features.length)return;
  var box=document.getElementById("wxalert");if(!box)return;
  var names=d.features.map(function(f){return f.properties.event+" in effect until "+new Date(f.properties.ends||f.properties.expires).toLocaleString();});
  box.innerHTML="&#9888; Weather alert: "+names.join(" &#183; ")+' &#183; <a href="https://www.weather.gov/hun/" target="_blank" rel="noopener">National Weather Service Huntsville</a>';
  box.hidden=false;
 }).catch(function(){});
/* print */
var pb=document.getElementById("printBtn");
if(pb)pb.addEventListener("click",function(){window.print();});
/* share the directory itself */
var ss=document.getElementById("shareSite");
if(ss)ss.addEventListener("click",function(){
  var url=location.href.split("#")[0];
  if(navigator.share){navigator.share({title:"Hanceville Entertainment and Shopping",text:"Free local directory for Hanceville and Cullman County, Alabama",url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(url);ss.textContent="Link copied, share away!";}
});
/* ?q= deep search links */
try{var qv=new URLSearchParams(location.search).get("q");
 if(qv){var qi=document.getElementById("q");qi.value=qv;qi.dispatchEvent(new Event("input",{bubbles:true}));
  setTimeout(function(){document.getElementById("results").scrollIntoView();},450);}}catch(e){}
/* gentle reveal on scroll */
try{
 var secs=document.querySelectorAll("main#results, section.wrap");
 secs.forEach(function(s){s.setAttribute("data-reveal","");});
 var io=new IntersectionObserver(function(es){es.forEach(function(en){if(en.isIntersecting){en.target.classList.add("in");io.unobserve(en.target);}});},{threshold:.06});
 secs.forEach(function(s){io.observe(s);});
}catch(e){document.querySelectorAll("[data-reveal]").forEach(function(s){s.classList.add("in");});}
/* mouse drag to swipe rails on desktop */
document.querySelectorAll(".rail").forEach(function(rail){
 var down=false,sx=0,sl=0;
 rail.addEventListener("pointerdown",function(e){if(e.pointerType!=="mouse")return;down=true;sx=e.clientX;sl=rail.scrollLeft;});
 window.addEventListener("pointermove",function(e){if(down)rail.scrollLeft=sl-(e.clientX-sx);});
 window.addEventListener("pointerup",function(){down=false;});
});
})();
}catch(e){if(window.console)console.error(e);}
try{
(function(){
function setLang(l){try{localStorage.setItem("hes-lang",l);}catch(e){} location.reload();}
var lb=document.getElementById("langBtn");
if(lb){lb.textContent=(window.SLH_LANG==="es")?"EN \u00b7 English":"ES \u00b7 Espa\u00f1ol";
 lb.addEventListener("click",function(){setLang(window.SLH_LANG==="es"?"en":"es");});}
var ml=document.getElementById("menuLang");
if(ml){ml.textContent=(window.SLH_LANG==="es")?"View in English":"Ver en espa\u00f1ol";
 ml.addEventListener("click",function(e){e.preventDefault();setLang(window.SLH_LANG==="es"?"en":"es");});}
if(window.SLH_LANG==="es"&&window.SLH_UI){
 document.querySelectorAll("[data-i18n]").forEach(function(el){
  var es=window.SLH_UI[el.getAttribute("data-i18n")];if(!es)return;
  var nodes=el.childNodes,done=false;
  for(var i=nodes.length-1;i>=0;i--){var n=nodes[i];
   if(n.nodeType===3&&n.textContent.trim()){n.textContent=n.textContent.replace(n.textContent.trim(),es);done=true;break;}}
  if(!done)el.textContent=es;
 });
 var qi=document.getElementById("q");
 if(qi)qi.placeholder="Busca peluquer\u00edas, comida, iglesias, escuelas \u2014 o el nombre de un negocio";
 var pb=document.getElementById("printBtn"); if(pb)pb.textContent="Imprimir lista";
}
if(window.SLH_LANG!=="es"&&window.SLH_LISTINGS){
 var tlen=document.getElementById("trustline");
 if(tlen&&tlen.firstChild&&tlen.firstChild.nodeType===3){tlen.firstChild.nodeValue=tlen.firstChild.nodeValue.replace(/^\d+/,String(window.SLH_LISTINGS.length));}
}
if(window.SLH_LANG==="es"&&window.SLH_MINI&&window.SLH_MINI.trust_listings){
 var M=window.SLH_MINI;var tl=document.getElementById("trustline");
 if(tl){tl.innerHTML=(window.SLH_LISTINGS?window.SLH_LISTINGS.length+" ":"")+M.trust_listings+" &#183; "+M.trust_verified+" &#183; Hanceville &amp; Cullman County, Alabama &#183; ";
  var b=document.createElement("button");b.type="button";b.id="shareSiteEs";b.className="sharelink";b.textContent=M.share_site;
  b.addEventListener("click",function(){var url=location.href.split("#")[0];
   if(navigator.share){navigator.share({title:document.title,url:url}).catch(function(){});}
   else if(navigator.clipboard){navigator.clipboard.writeText(url);b.textContent="\u00a1Enlace copiado!";}});
  tl.appendChild(b);}
}
})();
}catch(e){if(window.console)console.error(e);}
try{
(function(){
"use strict";
var LANG=window.SLH_LANG||"en";
if(window.SLH_UI){
  var add={"View profile":"Ver perfil","Back to listings":"Volver a los listados","About":"Acerca de","Office":"Oficina","Employer":"Empleador","Position":"Cargo","Biography":"Biografía","Latest post":"Publicación reciente"};
  for(var k in add){if(!(k in window.SLH_UI))window.SLH_UI[k]=add[k];}
}
function T(en){return (LANG==="es"&&window.SLH_UI&&window.SLH_UI[en])||en;}
function slug(s){return (s||"").toLowerCase().replace(/[^a-z0-9]+/g,"-").replace(/^-|-$/g,"");}
function esc(s){var d=document.createElement("div");d.textContent=s||"";return d.innerHTML;}
var L=window.SLH_LISTINGS||[];
var bySlug={};L.forEach(function(r){bySlug[slug(r.name)]=r;});
var OFF=window.SLH_OFFICIALS||[];
function favs(){try{return JSON.parse(localStorage.getItem("slh-favs")||"[]");}catch(e){return[];}}
function setFavs(f){try{localStorage.setItem("slh-favs",JSON.stringify(f));}catch(e){}}
var FB_SVG='<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" style="vertical-align:-3px"><path fill="#1877F2" d="M24 12.07C24 5.4 18.63 0 12 0S0 5.4 0 12.07C0 18.1 4.39 23.09 10.13 24v-8.44H7.08v-3.49h3.04V9.41c0-3.02 1.8-4.7 4.54-4.7 1.31 0 2.68.24 2.68.24v2.97h-1.5c-1.5 0-1.96.93-1.96 1.89v2.26h3.32l-.53 3.49h-2.8V24C19.62 23.1 24 18.1 24 12.07z"/></svg>';
var view=document.getElementById("profileView");
var body=document.getElementById("pfBody");
var lastCard=null;
function showView(){view.hidden=false;document.body.style.overflow="hidden";view.scrollTop=0;document.getElementById("pfBack").focus();}
function hideView(){view.hidden=true;document.body.style.overflow="";if(lastCard){lastCard.scrollIntoView({block:"center"});lastCard.classList.add("deeplink-hit");var _pfT=lastCard.querySelector(".pf-open");if(_pfT)_pfT.focus();setTimeout(function(){if(lastCard)lastCard.classList.remove("deeplink-hit");},2600);}}
if(LANG==="es")document.getElementById("pfBackLabel").textContent="Volver a los listados";
document.getElementById("pfBack").addEventListener("click",hideView);
document.addEventListener("keydown",function(e){if(e.key==="Escape"&&!view.hidden)hideView();});
function btn(label,href,primary){var a=document.createElement("a");a.className="btn"+(primary?" btn-primary":"");a.innerHTML=label;if(href){a.href=href;}return a;}
function isFiller(r){var d=(r.description||"").trim();if(!d)return true;if(d===r.name)return true;if(d.indexOf(r.name+" is listed in ")===0)return true;if(d.indexOf(r.name+" appears in our ")===0)return true;return false;}
function openListing(r){
  lastCard=document.getElementById(slug(r.name));
  var fb=r.facebook||((r.website&&r.website.indexOf("facebook.com")>=0)?r.website:null);
  var site=(r.website&&r.website.indexOf("facebook.com")<0)?r.website:null;
  var h="";
  h+='<div class="pf-head"><img class="pf-logo" src="'+(r.logo||(window.SLH_CONTENT(r)?"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='480' height='320'><defs><linearGradient id='g' x1='0' y1='0' x2='1' y2='1'><stop offset='0' stop-color='%23241243'/><stop offset='1' stop-color='%236D28D9'/></linearGradient></defs><rect width='480' height='320' fill='url(%23g)'/><text x='50%' y='55%' font-size='150' fill='white' text-anchor='middle' dominant-baseline='middle'>★</text></svg>":window.SLH_REG))+'" alt="'+esc(r.name)+'">';
  h+='<div><h2 class="pf-name">'+esc(r.name)+'</h2>';
  h+='<p class="pf-sub">'+esc((window.SLH_CAT&&LANG==="es"&&window.SLH_CAT[r.category])||r.category||"")+((r.town)?' · '+esc(r.town):'')+'</p></div></div>';
  h+='<h3 class="pf-h">'+esc(T("About"))+'</h3>';
  if(isFiller(r)){h+='<p class="pf-text">'+esc(LANG==="es"?"La descripción completa de este listado está en preparación. Los botones de contacto siguientes llegan directamente a la organización.":"A full description for this listing is being completed. The contact buttons below reach the organization directly.")+'</p>';}
  else{var d=(LANG==="es"&&window.SLH_DESC_ES&&SLH_DESC_ES[r.name])?SLH_DESC_ES[r.name]:r.description;h+='<p class="pf-text">'+esc(d)+'</p>';}
  if(r.address){h+='<h3 class="pf-h">'+esc(LANG==="es"?"Ubicación":"Location")+'</h3><p class="pf-text">'+esc(r.address)+'</p>';}
  h+='<div class="pf-acts">';
  if(r.phone){h+='<a class="btn btn-primary" href="tel:'+r.phone.replace(/[^0-9+]/g,"")+'">'+esc(T("Call"))+' · '+esc(r.phone)+'</a>';}
  if(site){h+='<a class="btn" target="_blank" rel="noopener" href="'+esc(site)+'">'+esc(T("Website"))+'</a>';}
  if(fb){h+='<a class="btn" target="_blank" rel="noopener" href="'+esc(fb)+'">'+FB_SVG+' Facebook</a>';}
  if(r.address){h+='<a class="btn" target="_blank" rel="noopener" href="https://www.google.com/maps/search/?api=1&query='+encodeURIComponent(r.name+" "+r.address)+'">'+esc(T("Directions"))+'</a>';}
  h+='<button type="button" class="btn" id="pfSave"></button>';
  h+='<button type="button" class="btn" id="pfShare">'+esc(T("Share"))+'</button>';if(["Fun Facts","Sweet Tea Jokes","Social Media"].indexOf(r.category)<0)h+='<a class="btn" href='+JSON.stringify(['place',slug(r.name)].join('-')+'.html')+'>'+esc(T("See full page"))+'</a>';
  h+='</div>';
  if(fb){h+='<h3 class="pf-h">'+esc(T("Latest post"))+'</h3><div id="pfEmbed"><button type="button" class="btn" id="pfEmbedBtn">'+esc(T("See latest post"))+'</button></div>';}
  body.innerHTML=h;
  var _pfi=body.querySelector("img.pf-logo");if(_pfi&&r.logo){var _v=(window.SLH_VARIANTS||{})[_pfi.getAttribute("src")||""];if(_v){_pfi.srcset=_v.w;_pfi.setAttribute("sizes","150px");_pfi.decoding="async";if(_v.a){var _pic=document.createElement("picture");_pic.style.display="block";var _so=document.createElement("source");_so.type="image/avif";_so.srcset=_v.a;_so.setAttribute("sizes","150px");_pic.appendChild(_so);_pfi.parentNode.insertBefore(_pic,_pfi);_pic.appendChild(_pfi);}}}
  var sv=document.getElementById("pfSave");
  function paintSave(){var f=favs();sv.textContent=(f.indexOf(r.name)>=0?"★ ":"☆ ")+T("Save");}
  paintSave();
  sv.addEventListener("click",function(){var f=favs(),i=f.indexOf(r.name);if(i>=0)f.splice(i,1);else f.push(r.name);setFavs(f);paintSave();});
  document.getElementById("pfShare").addEventListener("click",function(){
    var url=location.href.split("#")[0]+"#"+slug(r.name);
    if(navigator.share){navigator.share({title:r.name,text:r.name+" - Hanceville Entertainment and Shopping",url:url}).catch(function(){});}
    else if(navigator.clipboard){navigator.clipboard.writeText(url);}
  });
  if(fb){document.getElementById("pfEmbedBtn").addEventListener("click",function(){
    var box=document.getElementById("pfEmbed");box.textContent="";
    var f=document.createElement("iframe");f.title=r.name+" on Facebook";f.loading="lazy";f.height=460;f.style.width="100%";f.style.border="0";
    f.setAttribute("allow","encrypted-media");
    f.src="https://www.facebook.com/plugins/page.php?href="+encodeURIComponent(fb)+"&tabs=timeline&width=340&height=460&small_header=true&adapt_container_width=true&hide_cover=false&show_facepile=false";
    var loaded=false;f.addEventListener("load",function(){loaded=true;});
    box.appendChild(f);
    setTimeout(function(){if(loaded)return;box.textContent="";var p=document.createElement("p");p.textContent="This Facebook post could not be loaded here. ";var b=document.createElement("a");b.href=fb;b.target="_blank";b.rel="noopener";b.textContent="Open on Facebook";box.appendChild(p);box.appendChild(b);},9000);
  });}
  try{history.replaceState(null,"","#"+slug(r.name));}catch(e){}
  showView();
}
function openOfficial(o,imgSrc){
  lastCard=null;
  var h='<div class="pf-head"><img class="pf-portrait" src="'+imgSrc+'" alt="'+esc(o.name)+'">';
  h+='<div><h2 class="pf-name">'+esc(o.name)+'</h2><p class="pf-sub">'+esc(o.position)+'</p>';
  h+='<p class="pf-sub">'+esc(T("Employer"))+': '+esc(o.employer)+'</p></div></div>';
  h+='<h3 class="pf-h">'+esc(T("Biography"))+'</h3><p class="pf-text">'+esc(o.bio)+'</p>';
  if(o.contact){h+='<h3 class="pf-h">'+esc(T("Office"))+'</h3><p class="pf-text">'+esc(o.contact)+'</p>';}
  body.innerHTML=h;showView();
}
/* ---- wire listing cards: profile buttons + logo/name clicks ---- */
function addProfileButton(cardEl,r){
  var acts=cardEl.querySelector(".actions");if(!acts||acts.querySelector(".pf-open"))return;
  var b=document.createElement("button");b.type="button";b.className="btn pf-open";b.textContent=T("View profile");
  b.addEventListener("click",function(ev){ev.stopPropagation();openListing(r);});
  acts.insertBefore(b,acts.firstChild);
}
var obs=new MutationObserver(function(muts){
  muts.forEach(function(mu){mu.addedNodes.forEach(function(n){
    if(n.nodeType!==1)return;
    if(n.classList&&n.classList.contains("card")&&n.id&&bySlug[n.id])addProfileButton(n,bySlug[n.id]);
    if(n.querySelectorAll)n.querySelectorAll(".card").forEach(function(c){if(c.id&&bySlug[c.id])addProfileButton(c,bySlug[c.id]);});
  });});
});
obs.observe(document.body,{childList:true,subtree:true});
document.querySelectorAll(".card").forEach(function(c){if(c.id&&bySlug[c.id])addProfileButton(c,bySlug[c.id]);});
document.addEventListener("click",function(e){
  var t=e.target;
  var cardEl=t.closest?t.closest(".card"):null;
  if(!cardEl||!cardEl.id||!bySlug[cardEl.id])return;
  if(t.tagName==="IMG"&&t.classList.contains("logo")){e.stopPropagation();e.preventDefault();openListing(bySlug[cardEl.id]);}
  else if(t.tagName==="H3"){openListing(bySlug[cardEl.id]);}
},true);
/* ---- wire officials rail ---- */
var orail=document.getElementById("orail");
if(orail){orail.querySelectorAll("figure").forEach(function(fig){
  var img=fig.querySelector("img");var cap=fig.querySelector("figcaption");
  if(!img||!cap)return;
  var alt=img.getAttribute("alt")||"";
  var nm=alt.split(",")[0].trim();
  var role=alt.slice(alt.indexOf(",")+1).trim();
  var match=null;
  function normName(x){return (x||"").toLowerCase().replace(/\./g,"").replace(/\b(jr|sr|pe|cfm|md|dds|phd)\b/g,"").replace(/[^a-z ]/g," ").replace(/\s+/g," ").trim();}
  OFF.forEach(function(o){if(normName(o.name)===normName(nm)&&(o.role===role||role.indexOf(o.role)===0||o.role.indexOf(role)===0))match=o;});
  if(!match)OFF.forEach(function(o){if(normName(o.name)===normName(nm)&&!match)match=o;});
  if(!match)return;
  fig.style.cursor="pointer";var vb=document.createElement("button");vb.type="button";vb.textContent=nm+", "+T("View profile");vb.style.cssText="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap";vb.addEventListener("click",function(ev){ev.stopPropagation();openOfficial(match,img.src);});fig.appendChild(vb);
  fig.addEventListener("click",function(){openOfficial(match,img.src);});
  fig.addEventListener("keydown",function(e){if(e.key==="Enter"||e.key===" "){e.preventDefault();openOfficial(match,img.src);}});
});}
/* ---- deep link: open the profile named in the hash ---- */
function openFromHash(){
  var h=(location.hash||"").slice(1);if(!h)return;
  var r=bySlug[h];if(r)openListing(r);
}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",openFromHash);else openFromHash();
})();
}catch(e){if(window.console)console.error(e);}
try{
if('serviceWorker' in navigator&&location.protocol==='https:')window.addEventListener('load',function(){navigator.serviceWorker.register('sw.js').catch(function(){});});
}catch(e){if(window.console)console.error(e);}
try{
/* === Language notice: strings, terms clause swap, and prompt behavior === */
(function(){
"use strict";
var ES={
 title:"Idioma y privacidad: su elección",
 textDetected:"Consultamos el ajuste de idioma de su navegador en su dispositivo y lo usamos para abrir este sitio en español. Ningún dato de esa consulta se nos envía. Permitir todo guarda su elección de idioma y esta respuesta en su dispositivo. Solo lo necesario guarda únicamente esta respuesta, y su idioma se consultará de nuevo en su próxima visita. Este sitio no instala cookies de seguimiento en ningún caso.",
 textNone:"No pudimos leer el ajuste de idioma de su navegador. Elija el idioma que prefiere en los botones siguientes y luego confirme su elección.",
 pickLabel:"Elija su idioma:",
 textPicked:"Usted eligió español para este sitio, y esa elección ya quedó guardada en su dispositivo. Confirme su respuesta a continuación. Permitir todo mantiene guardada esa elección. Solo lo necesario guarda únicamente esta respuesta y borra la elección de idioma guardada, de modo que se le preguntará de nuevo en su próxima visita. Este sitio no instala cookies de seguimiento en ningún caso.",
 termsLink:"Revisar las condiciones",
 checkLabel:"He leído las Condiciones de uso y las acepto.",
 allow:"Permitir todo",needed:"Solo lo necesario",review:"Revisar primero",
 termsClause:"Detección de idioma y traducción. En una primera visita, este sitio consulta el ajuste de idioma de su navegador en su propio dispositivo para abrirse en inglés o en español. La consulta se realiza en su dispositivo y no se envía ninguna información de idioma a este sitio ni a terceros. Si usted elige un idioma, o lo confirma en el aviso de idioma, su elección se guarda únicamente en su navegador, en su dispositivo, y puede cambiarla en cualquier momento con el botón de idioma. Este sitio se ofrece solamente en inglés y en español. Los nombres de negocios y organizaciones son nombres propios y mantienen su forma original en ambos idiomas. Cada descripción en español de este sitio es una traducción escrita preparada para este sitio. Una ficha que aún no tiene descripción en español aparece en inglés mientras el modo en español está activo, y ninguna traducción automática se presenta como información verificada."
};
var EN={
 textNone:"We could not read a language setting from your browser. Please choose your language with the buttons below, and then confirm your choice.",
 pickedEn:"Thank you. This site will stay in English. Please review the terms and confirm your choice below."
};
var tp=document.getElementById("termsLangP");
if(tp&&window.SLH_LANG==="es"){tp.textContent=(window.SLH_UI&&window.SLH_UI.terms_lang_p)||ES.termsClause;}
var root=document.documentElement;
if(root.getAttribute("data-access")!=="pending")return;
var bar=document.getElementById("accessBar");if(!bar)return;
function setText(id,txt){var el=document.getElementById(id);if(el)el.textContent=txt;}
if(window.SLH_LANG==="es"){
 setText("accessTitle",ES.title);setText("accessText",ES.textDetected);
 setText("accessPickLabel",ES.pickLabel);setText("accessTermsLink",ES.termsLink);
 setText("accessCheckLabel",ES.checkLabel);setText("accessAllow",ES.allow);
 setText("accessNeeded",ES.needed);setText("accessReview",ES.review);
}
if(window.SLH_LANG_SRC==="picked"&&window.SLH_LANG==="es"){setText("accessText",ES.textPicked);}
if(window.SLH_LANG_SRC==="none"){
 setText("accessText",window.SLH_LANG==="es"?ES.textNone:EN.textNone);
 var pk=document.getElementById("accessPick");if(pk)pk.hidden=false;
}
bar.hidden=false;
function openTerms(e){if(e)e.preventDefault();var d=document.getElementById("pol-terms");if(!d)return;d.open=true;d.scrollIntoView({block:"start"});var s=d.querySelector("summary");if(s)s.focus({preventScroll:true});}
var tl=document.getElementById("accessTermsLink");if(tl)tl.addEventListener("click",openTerms);
var rv=document.getElementById("accessReview");if(rv)rv.addEventListener("click",openTerms);
var chk=document.getElementById("accessCheck");
var allow=document.getElementById("accessAllow"),needed=document.getElementById("accessNeeded");
if(chk)chk.addEventListener("change",function(){allow.disabled=!chk.checked;needed.disabled=!chk.checked;});
function dismiss(mode){
 try{localStorage.setItem("hes-access",mode);}catch(e){}
 try{sessionStorage.removeItem("hes-access-pick");}catch(e){}
 if(mode==="all"){try{localStorage.setItem("hes-lang",window.SLH_LANG||"en");}catch(e){}}
 else if(window.SLH_LANG_SRC==="picked"){try{localStorage.removeItem("hes-lang");}catch(e){}}
 root.removeAttribute("data-access");bar.hidden=true;
 var lb=document.getElementById("langBtn");if(lb)lb.focus();
}
if(allow)allow.addEventListener("click",function(){dismiss("all");});
if(needed)needed.addEventListener("click",function(){dismiss("needed");});
var pEn=document.getElementById("accessPickEn"),pEs=document.getElementById("accessPickEs");
if(pEn)pEn.addEventListener("click",function(){window.SLH_LANG="en";var pk2=document.getElementById("accessPick");if(pk2)pk2.hidden=true;setText("accessText",EN.pickedEn);});
if(pEs)pEs.addEventListener("click",function(){try{sessionStorage.setItem("hes-access-pick","es");localStorage.setItem("hes-lang","es");}catch(e){}location.reload();});
})();
}catch(e){if(window.console)console.error(e);}
