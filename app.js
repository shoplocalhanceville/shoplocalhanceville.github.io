(function(){
'use strict';
var FB='https://www.facebook.com/ShopLocalAlabama';
var PAGES=[
 {k:'events',f:'events.html',t:'Upcoming Events',ic:'\ud83d\udcc5',j:'events.json'},
 {k:'businesses',f:'businesses.html',t:'Business Directory',ic:'\ud83d\udecd\ufe0f',j:'businesses.json',g:'category',o:['Restaurants & Food','Shopping & Retail','Services','Manufacturing & Industry','Other']},
 {k:'directory',f:'directory.html',t:'Community Directory',ic:'\ud83c\udfdb\ufe0f',j:'directory.json',g:'group',o:['Schools','City Hall & Government','Public Safety','Utilities & Public Works','Community Services']},
 {k:'resources',f:'resources.html',t:'Community Resources',ic:'\ud83e\udd1d',j:'resources.json',g:'group',o:['Crisis & Emergency','Everyone','Women','Children & Families','Seniors','Veterans']},
 {k:'wallace',f:'wallace.html',t:'Wallace State Services',ic:'\ud83c\udf93',j:'wallace.json',g:'group',o:['Getting Started','Paying for College','Help in the Classroom','Careers and Training','Health, Safety and Support','Campus Life','Community Services']}
];
var today=new Intl.DateTimeFormat('en-CA',{timeZone:'America/Chicago'}).format(new Date());
var cur=document.body.getAttribute('data-page');
var cache={};
function get(p){if(!cache[p.k])cache[p.k]=fetch(p.j+'?v='+Date.now(),{cache:'no-store'}).then(function(r){return r.json();}).then(function(d){if(p.k==='events')d=d.filter(function(e){return (e.end||e.start)>=today;}).sort(function(a,b){return a.start<b.start?-1:a.start>b.start?1:0;});return d;});return cache[p.k];}
function slug(s){return s.toLowerCase().replace(/&/g,'and').replace(/[^a-z0-9]+/g,' ').trim().replace(/ /g,'_');}
function el(t,c,x){var n=document.createElement(t);if(c)n.className=c;if(x!=null)n.textContent=x;return n;}
function btn(t,h,c,x,lbl){var a=el('a','btn'+(c?' '+c:''),t);a.href=h;if(x){a.target='_blank';a.rel='noopener';}if(lbl)a.setAttribute('aria-label',lbl);return a;}
var M=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],W=['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];
function dd(s){var p=s.split('-').map(Number),x=new Date(Date.UTC(p[0],p[1]-1,p[2]));return{w:W[x.getUTCDay()],m:M[p[1]-1],d:p[2]};}
function fmt(e){var a=dd(e.start);if(!e.end||e.end===e.start)return a.w+', '+a.m+' '+a.d;var b=dd(e.end);return a.m+' '+a.d+' to '+(a.m===b.m?'':b.m+' ')+b.d;}
function card(e,kind){var c=el('article','card '+(kind==='events'?'ev':'dc'));c.id=slug(e.name);c.appendChild(el('h3',null,e.name));
 if(kind==='events'){c.appendChild(el('p','when',fmt(e)+(e.time?' \u00b7 '+e.time:'')));c.appendChild(el('p','meta','\ud83d\udccd '+(e.venue?e.venue+', ':'')+e.town));c.appendChild(el('p','meta','Hosted by '+e.host));if(e.cost)c.appendChild(el('p','meta','\ud83c\udf9f\ufe0f '+e.cost));}
 else{if(e.type){var tp=el('p');tp.appendChild(el('span','tag',e.type));c.appendChild(tp);}if(e.address)c.appendChild(el('p','meta','\ud83d\udccd '+e.address));if(e.phone)c.appendChild(el('p','meta','\ud83d\udcde '+e.phone));if(e.email)c.appendChild(el('p','meta','\u2709\ufe0f '+e.email));}
 c.appendChild(el('p','sum',e.summary));var a=el('div','acts');
 if(kind==='events')a.appendChild(btn('View on Facebook',e.url,'',1,'View '+e.name+' on Facebook'));
 if(e.phone)a.appendChild(btn('Call','tel:'+e.phone.replace(/[^0-9]/g,''),'',0,'Call '+e.name));
 if(e.email)a.appendChild(btn('Email','mailto:'+e.email,'alt2',0,'Email '+e.name));
 if(e.website)a.appendChild(btn('Website',e.website,'alt2',1,e.name+' website'));
 if(e.facebook)a.appendChild(btn('Facebook',e.facebook,'',1,e.name+' on Facebook'));
 c.appendChild(a);return c;}
function groups(box,items,p){box.innerHTML='';p.o.forEach(function(g){var it=items.filter(function(e){return e[p.g]===g;});if(!it.length)return;var h=el('h3','group',g+' ('+it.length+')');h.id=slug(g);box.appendChild(h);var gr=el('div','grid');it.forEach(function(e){gr.appendChild(card(e,p.k));});box.appendChild(gr);});}
function jump(){if(location.hash){var t=document.getElementById(decodeURIComponent(location.hash.slice(1)));if(t){t.scrollIntoView();t.classList.add("hl");t.setAttribute("tabindex","-1");t.focus({preventScroll:true});}}}
// tabs
var P=PAGES.filter(function(p){return p.k===cur;})[0];
var nav=document.getElementById('tabs');
if(nav){var h=el('h2',null,'Pages');nav.appendChild(h);var home=el('a',null,'\ud83c\udfe0 Home');home.href='index.html';if(cur==='home')home.setAttribute('aria-current','page');nav.appendChild(home);
 PAGES.forEach(function(p){var a=el('a',null,p.ic+' '+p.t);a.href=p.f;if(p.k===cur)a.setAttribute('aria-current','page');nav.appendChild(a);});
 if(P&&P.o){nav.appendChild(el('h2',null,'On this page'));var s=el('div','sub');P.o.forEach(function(g){var a=el('a',null,g);a.href='#'+slug(g);s.appendChild(a);});nav.appendChild(s);}
 var tg=document.getElementById('tab-toggle');tg.addEventListener('click',function(){var o=nav.classList.toggle('open');tg.setAttribute('aria-expanded',o);tg.textContent=o?'\u2715 Close':'\u2630 Menu';});
 nav.addEventListener('click',function(e){if(e.target.tagName==='A'&&nav.classList.contains('open')){nav.classList.remove('open');tg.setAttribute('aria-expanded','false');tg.textContent='\u2630 Menu';}});
 document.addEventListener('keydown',function(e){if(e.key==='Escape'&&nav.classList.contains('open'))tg.click();});}
// global search
var q=document.getElementById('gs-q'),res=document.getElementById('gs-res');
if(q){var tmr;q.addEventListener('input',function(){clearTimeout(tmr);tmr=setTimeout(run,150);});
 q.addEventListener('keydown',function(e){if(e.key==='Escape'){res.classList.remove('open');}});
 document.addEventListener('click',function(e){if(!e.target.closest('.gs'))res.classList.remove('open');});
 document.getElementById('gs-form').addEventListener('submit',function(e){e.preventDefault();run();var f=res.querySelector('a');if(f)f.focus();});}
function run(){var t=q.value.trim().toLowerCase();if(t.length<2){res.classList.remove('open');res.innerHTML='';return;}
 Promise.all(PAGES.map(function(p){return get(p).then(function(d){return d.map(function(e){return{p:p,e:e};});}).catch(function(){return[];});})).then(function(all){
  var words=t.split(/\s+/),out=[];[].concat.apply([],all).forEach(function(x){var e=x.e,hay=[e.name,e.summary,e.type,e.category,e.group,e.address,e.venue,e.town,e.host].join(' ').toLowerCase();if(words.every(function(w){return hay.indexOf(w)>=0;}))out.push(x);});
  res.innerHTML='';if(!out.length){res.appendChild(el('p',null,'No matches yet. Try another word.'));}
  out.slice(0,30).forEach(function(x){var a=el('a');a.href=x.p.f+'#'+slug(x.e.name);a.appendChild(el('small',null,x.p.t));a.appendChild(el('div',null,x.e.name));res.appendChild(a);});
  res.classList.add('open');});}
// page bodies
var box=document.getElementById('list'),st=document.getElementById('status');
if(P&&box){get(P).then(function(d){
 if(P.k==='events'){var g=el('div','grid');d.forEach(function(e){g.appendChild(card(e,'events'));});box.appendChild(g);st.textContent=d.length?'':'No upcoming events right now. Follow the Page and we will post new ones soon!';}
 else if(P.k==='businesses'){d.sort(function(a,b){return a.name.localeCompare(b.name);});var bq=document.getElementById('biz-q'),ch=document.getElementById('biz-chips'),c='All';
  ['All'].concat(P.o).forEach(function(x){var n=el('button','chip',x);n.type='button';n.setAttribute('aria-pressed',x==='All');n.onclick=function(){c=x;[].forEach.call(ch.children,function(y){y.setAttribute('aria-pressed',y===n);});go();};ch.appendChild(n);});
  function go(){var t=bq.value.trim().toLowerCase();var f=d.filter(function(e){return(c==='All'||e.category===c)&&(!t||[e.name,e.type,e.category,e.summary,e.address].join(' ').toLowerCase().indexOf(t)>=0);});groups(box,f,P);st.textContent=f.length?f.length+' businesses shown':'No matches yet. Try another word or category.';}
  bq.addEventListener('input',go);go();}
 else{groups(box,d,P);st.textContent='';}
 jump();}).catch(function(){st.textContent='This list could not load right now. Please try again soon.';});}
// home counts
[].forEach.call(document.querySelectorAll('[data-count]'),function(n){var p=PAGES.filter(function(x){return x.k===n.getAttribute('data-count');})[0];get(p).then(function(d){n.textContent=d.length+(p.k==='events'?' upcoming':' listings');});});
})();
