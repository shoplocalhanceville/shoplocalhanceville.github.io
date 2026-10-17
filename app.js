(function(){
'use strict';
var FB='https://www.facebook.com/ShopLocalAlabama';
var PAGES=[
 {k:'events',f:'events.html',t:'Upcoming Events',ic:'\ud83d\udcc5',j:'events.json',g:'group',o:['Community and Fun','Sports']},
 {k:'eats',f:'eats.html',t:'Local Eats',ic:'\ud83c\udf7d\ufe0f',j:'eats.json',g:'group',o:['Hometown Favorites','New Spots','Daily Specials','More Places to Eat'],info:1},
 {k:'shops',f:'shops.html',t:'Hometown Shops',ic:'\ud83d\udecd\ufe0f',j:'shops.json',g:'group',o:['Downtown Shops','Makers','Markets'],info:1},
 {k:'news',f:'news.html',t:'Community News',ic:'\ud83d\udcf0',j:'news.json',g:'group',o:['City Council','City Budget','Roads and ALDOT','Announcements','Official City Updates'],info:1},
 {k:'nonprofits',f:'nonprofits.html',t:'Nonprofits',ic:'\ud83d\udc9c',j:'nonprofits.json',g:'group',o:['Feeding Neighbors','Community Builders','Support and Safety'],info:1},
 {k:'fun',f:'fun.html',t:'A Little Fun',ic:'\ud83d\ude03',j:'fun.json',g:'group',o:['Fun Facts','Local Landmarks','Sweet Tea Jokes'],info:1},
 {k:'businesses',f:'businesses.html',t:'Business Directory',ic:'\ud83c\udfea',j:'businesses.json',g:'category',o:['Restaurants','Drinks & Coffee','Barbers & Salons','Auto Sales','Auto Repair & Mechanics','Tires','Small Engine Repair','Towing','Home Services','Health & Pharmacy','Pets & Child Care','Finance & Insurance','Shopping & Retail','Manufacturing & Industry','Lodging','Other']},
 {k:'directory',f:'directory.html',t:'Community Directory',ic:'\ud83c\udfdb\ufe0f',j:'directory.json',g:'group',o:['Schools','City Hall & Government','Public Safety','Utilities & Public Works','Community Services']},
 {k:'resources',f:'resources.html',t:'Community Resources',ic:'\ud83e\udd1d',j:'resources.json',g:'group',o:['Crisis & Emergency','Seniors & Elderly','Food & SNAP','DHR Services','Child Care','Federal Programs','Everyone','Women','Children & Families','Veterans']},
 {k:'wallace',f:'wallace.html',t:'Wallace State Services',ic:'\ud83c\udf93',j:'wallace.json',g:'group',o:['Getting Started','Paying for College','Help in the Classroom','Careers and Training','Health, Safety and Support','Campus Life','Community Services']}
];
var today=new Intl.DateTimeFormat('en-CA',{timeZone:'America/Chicago'}).format(new Date());
var cur=document.body.getAttribute('data-page');
var cache={};
function get(p){if(!cache[p.k])cache[p.k]=fetch(p.j+'?v='+Math.floor(Date.now()/6e5)).then(function(r){return r.json();}).then(function(d){if(p.k==='events')d=d.filter(function(e){return (e.end||e.start)>=today;}).sort(function(a,b){return a.start<b.start?-1:a.start>b.start?1:0;});return d;});return cache[p.k];}
function slug(s){return s.toLowerCase().replace(/&/g,'and').replace(/[^a-z0-9]+/g,' ').trim().replace(/ /g,'_');}
function el(t,c,x){var n=document.createElement(t);if(c)n.className=c;if(x!=null)n.textContent=x;return n;}
function safe(h){return /^(https:\/\/|tel:|mailto:|sms:)/i.test(String(h||''))?h:null;}
function btn(t,h,c,x,lbl){var a=el('a','btn'+(c?' '+c:''),t);h=safe(h);if(!h)return document.createComment('');a.href=h;if(x||/^https:/i.test(h)){a.target='_blank';a.rel='noopener noreferrer';}if(lbl)a.setAttribute('aria-label',lbl);return a;}
var M=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],W=['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];
function dd(s){var p=s.split('-').map(Number),x=new Date(Date.UTC(p[0],p[1]-1,p[2]));return{w:W[x.getUTCDay()],m:M[p[1]-1],d:p[2]};}
function fmt(e){var a=dd(e.start);if(!e.end||e.end===e.start)return a.w+', '+a.m+' '+a.d;var b=dd(e.end);return a.m+' '+a.d+' to '+(a.m===b.m?'':b.m+' ')+b.d;}
function initials(n){var w=String(n).replace(/[^A-Za-z0-9 ]/g,' ').split(/\s+/).filter(function(x){return x&&!/^(the|of|and|at|a|an)$/i.test(x);});return ((w[0]||'?').charAt(0)+(w[1]?w[1].charAt(0):'')).toUpperCase();}
function mapsUrl(a){return 'https://www.google.com/maps/dir/?api=1&destination='+encodeURIComponent(/\bAL\b|Alabama/.test(a)?a:a+', AL');}
function placeOf(e,kind){if(kind==='events'){if(!e.venue)return null;var v=e.venue.replace(/\s*\(away game\)/i,'');return v.indexOf(e.town)>=0?v+', AL':v+', '+e.town+', AL';}var a=e.address;if(!a||/p\.?\s*o\.?\s*box/i.test(a)||/^\s*hanceville,?\s*al/i.test(a))return null;return a;}
function isFb(u){return /^https:\/\/(www\.|m\.)?facebook\.com\//i.test(u||'');}
function icsName(e){return 'ics/'+slug(e.name)+'_'+e.start+'.ics';}
function card(e,kind){var c=el('article','card '+(kind==='events'?'ev':'dc'));c.id=slug(e.name);
 var hd=el('div','c-head');
 if(kind==='events'){var x=dd(e.start),db=el('div','datebadge');db.setAttribute('aria-hidden','true');db.appendChild(el('span','m',x.m));db.appendChild(el('span','d',String(x.d)));hd.appendChild(db);}
 else if(e.logo&&/^logos\/[a-z0-9-]+\.webp$/.test(e.logo)){var im=document.createElement('img');im.className='blogo';im.src=e.logo;im.alt=e.name+' logo';im.width=56;im.height=56;im.loading='lazy';im.decoding='async';hd.appendChild(im);}
 else{var ini=el('span','ini',initials(e.name));ini.setAttribute('aria-hidden','true');hd.appendChild(ini);}
 var ht=el('div','c-title');ht.appendChild(el('h3',null,e.name));
 if(kind==='events'){ht.appendChild(el('p','when',fmt(e)+(e.time?' \u00b7 '+e.time:'')));}
 else if(e.type||e.service||e.level||e.category){var tp=el('p','tags');if(e.level)tp.appendChild(el('span','tag lv lv-'+e.level.toLowerCase(),e.level));var t2=e.service||e.type;if(t2)tp.appendChild(el('span','tag',t2));if(tp.childNodes.length)ht.appendChild(tp);}
 hd.appendChild(ht);c.appendChild(hd);
 if(kind==='events'){c.appendChild(el('p','meta','\ud83d\udccd '+(e.venue?e.venue+', ':'')+e.town));c.appendChild(el('p','meta','\ud83d\udc65 Hosted by '+e.host));if(e.cost)c.appendChild(el('p','meta','\ud83c\udf9f\ufe0f '+e.cost));}
 else{if(e.date)c.appendChild(el('p','when',e.date));if(e.address)c.appendChild(el('p','meta','\ud83d\udccd '+e.address));if(e.phone)c.appendChild(el('p','meta','\ud83d\udcde '+e.phone));if(e.email)c.appendChild(el('p','meta','\u2709\ufe0f '+e.email));if(e.hours)c.appendChild(el('p','meta','\ud83d\udd52 '+e.hours));}
 c.appendChild(el('p','sum',e.summary));if(e.who){var w=el('p','who');w.appendChild(el('strong',null,'Who qualifies: '));w.appendChild(document.createTextNode(e.who));c.appendChild(w);}if(e.how)c.appendChild(el('p','meta','\ud83d\udc49 '+e.how));
 var a=el('div','acts');
 if(e.phone)a.appendChild(btn('\ud83d\udcde Call','tel:'+e.phone.replace(/[^0-9]/g,''),'',0,'Call '+e.name));
 var pl=placeOf(e,kind);if(pl)a.appendChild(btn('\ud83e\udded Directions',mapsUrl(pl),'alt2',1,'Directions to '+(kind==='events'&&e.venue?e.venue:e.name)));
 if(kind==='events'){if(e.url)a.appendChild(btn(isFb(e.url)?'View on Facebook':'Event details',e.url,'alt3',1,(isFb(e.url)?'View on Facebook: ':'Event details: ')+e.name));var ia=el('a','btn alt3','\ud83d\udcc5 Add to calendar');ia.href=icsName(e);ia.setAttribute('download','');ia.setAttribute('aria-label','Add to calendar: '+e.name);a.appendChild(ia);}
 else{var site=e.website&&!isFb(e.website)?e.website:null,fb=e.facebook||(isFb(e.website)?e.website:null);if(site)a.appendChild(btn('\ud83c\udf10 Website',site,'alt3',1,'Website: '+e.name));else if(fb)a.appendChild(btn('Facebook',fb,'alt3',1,'Facebook: '+e.name));}
 if(e.email)a.appendChild(btn('\u2709\ufe0f Email','mailto:'+e.email,'alt3',0,'Email '+e.name));
 if(a.childNodes.length)c.appendChild(a);
 var src=safe(e.source);if(src&&src!==e.website&&src!==e.url){var sp=el('p','src');var sl=el('a',null,'Source');sl.href=src;sl.target='_blank';sl.rel='noopener noreferrer';sl.setAttribute('aria-label','Source for '+e.name);sp.appendChild(sl);c.appendChild(sp);}
 return c;}
function groups(box,items,p){box.replaceChildren();p.o.forEach(function(g){var it=items.filter(function(e){return e[p.g]===g;});if(!it.length)return;var h=el('h2','group',g+' ('+it.length+')');h.id=slug(g);box.appendChild(h);var gr=el('div','grid');it.forEach(function(e){gr.appendChild(card(e,p.k));});box.appendChild(gr);});}
function jump(){if(location.hash){var t=document.getElementById(decodeURIComponent(location.hash.slice(1)));if(t){window.scrollTo(0,t.getBoundingClientRect().top+window.pageYOffset-((document.querySelector(".site-head")||{}).offsetHeight||0)-12);t.classList.add("hl");t.setAttribute("tabindex","-1");t.focus({preventScroll:true});}}}
// tabs
var P=PAGES.filter(function(p){return p.k===cur;})[0];
var nav=document.getElementById('tabs');
if(nav){var GR=[['Explore',['events','eats','shops','businesses']],['Community',['news','nonprofits','resources','directory']],['More',['wallace','fun']]];
 var home=el('a',null,'\ud83c\udfe0 Home');home.href='index.html';if(cur==='home')home.setAttribute('aria-current','page');nav.appendChild(home);
 GR.forEach(function(g){nav.appendChild(el('h2',null,g[0]));g[1].forEach(function(k){var p=PAGES.filter(function(x){return x.k===k;})[0];var a=el('a',null,p.ic+' '+p.t);a.href=p.f;if(p.k===cur)a.setAttribute('aria-current','page');nav.appendChild(a);});});
 if(P&&P.o){nav.appendChild(el('h2',null,'On this page'));var s=el('div','sub');P.o.forEach(function(g){var a=el('a',null,g);a.href='#'+slug(g);s.appendChild(a);});nav.appendChild(s);}
 if(cur==='home'){nav.appendChild(el('h2',null,'On this page'));var s2=el('div','sub');[['looking','I\u2019m looking for'],['help','Get help'],['upcoming','Coming up soon'],['contact','Contact us']].forEach(function(x){var a=el('a',null,x[1]);a.href='#'+x[0];s2.appendChild(a);});nav.appendChild(s2);}
 var tg=document.getElementById('tab-toggle');
 var desk=matchMedia('(min-width:1200px)');
 function isOpen(){return desk.matches?!document.body.classList.contains('tabs-off'):nav.classList.contains('open');}
 function sync(){tg.setAttribute('aria-expanded',isOpen()?'true':'false');}
 function setMenu(o,keep){if(desk.matches){if(keep)return;document.body.classList.toggle('tabs-off',!o);sync();return;}nav.classList.toggle('open',o);sync();if(o){var f=nav.querySelector('a,button');if(f)f.focus();}else if(!keep&&nav.contains(document.activeElement))tg.focus();}
 tg.addEventListener('click',function(e){e.preventDefault();setMenu(!isOpen());});
 var cx=el('button','tabs-close','\u2715 Close menu');cx.type='button';cx.addEventListener('click',function(){setMenu(false);});nav.insertBefore(cx,nav.firstChild);
 var ct=el('div','tabs-contact');ct.appendChild(el('h2',null,'Contact us'));var m1=el('a',null,'\u2709\ufe0f Email us');m1.href='mailto:shoplocalhanceville@gmail.com';ct.appendChild(m1);var m2=el('a',null,'\ud83d\udc4d Facebook Page');m2.href=FB;m2.target='_blank';m2.rel='noopener noreferrer';ct.appendChild(m2);nav.appendChild(ct);
 try{desk.addEventListener('change',function(){nav.classList.remove('open');sync();});}catch(e){}sync();
 function headH(){var t=document.querySelector('.site-head');return (t?t.offsetHeight:0)+12;}
 function scrollToId(id){var t=document.getElementById(id);if(!t)return false;var y=t.getBoundingClientRect().top+window.pageYOffset-headH();window.scrollTo({top:y,behavior:'smooth'});return true;}
 function mark(a){[].forEach.call(nav.querySelectorAll('.sub a'),function(x){x.removeAttribute('aria-current');x.classList.remove('active');});if(a){a.classList.add('active');a.setAttribute('aria-current','location');}}
 nav.addEventListener('click',function(e){var a=e.target.closest('a');if(!a)return;var h=a.getAttribute('href')||'';
  if(h.charAt(0)==='#'){e.preventDefault();var id=h.slice(1);if(!document.getElementById(id)&&resetFilter)resetFilter();if(scrollToId(id)){history.replaceState(null,'','#'+id);mark(a);}setMenu(false,true);}
  else{setMenu(false,true);}});
 var subs=[].slice.call(nav.querySelectorAll('.sub a'));
 if(subs.length){var ticking=false;window.addEventListener('scroll',function(){if(ticking)return;ticking=true;requestAnimationFrame(function(){ticking=false;var cur=null,lim=headH()+30;subs.forEach(function(a){var t=document.getElementById(a.getAttribute('href').slice(1));if(t&&t.getBoundingClientRect().top<=lim)cur=a;});mark(cur);});},{passive:true});}
 document.addEventListener('keydown',function(e){if(e.key==='Escape'&&nav.classList.contains('open'))setMenu(false);});}
// global search
var q=document.getElementById('gs-q'),res=document.getElementById('gs-res');
if(q){var tmr;q.addEventListener('input',function(){clearTimeout(tmr);tmr=setTimeout(run,150);});
 q.addEventListener('keydown',function(e){if(e.key==='Escape'){res.classList.remove('open');}});
 document.addEventListener('click',function(e){if(!e.target.closest('.gs'))res.classList.remove('open');});
 document.getElementById('gs-form').addEventListener('submit',function(e){e.preventDefault();run();var f=res.querySelector('a');if(f)f.focus();});}
var IDX=null,resetFilter=null;
if(q){try{var qs=new URLSearchParams(location.search).get('q');if(qs){q.value=qs.slice(0,100);setTimeout(run,0);}}catch(e){}}
function run(){var t=q.value.trim().toLowerCase();if(t.length<2){res.classList.remove('open');res.replaceChildren();return;}
 (IDX||(IDX=Promise.all(PAGES.map(function(p){return get(p).then(function(d){return d.map(function(e){return{p:p,e:e,h:[e.name,e.summary,e.type,e.service,(e.tags||[]).join(' '),e.category,e.group,e.address,e.venue,e.town,e.host,e.level,e.who].join(' ').toLowerCase()};});}).catch(function(){return[];});})).then(function(a){return [].concat.apply([],a);}))).then(function(all){
  var words=t.split(/\s+/),out=[];all.forEach(function(x){if(words.every(function(w){return x.h.indexOf(w)>=0;}))out.push(x);});
  res.replaceChildren();if(!out.length){res.appendChild(el('p',null,'No matches yet. Try another word.'));}
  out.slice(0,30).forEach(function(x){var a=el('a');a.href=x.p.f+'#'+slug(x.e.name);a.appendChild(el('small',null,x.p.t));a.appendChild(el('div',null,x.e.name));res.appendChild(a);});
  res.classList.add('open');});}
// page bodies
var box=document.getElementById('list'),st=document.getElementById('status');
if(P&&box){get(P).then(function(d){
 if(P.k==='businesses'){d.sort(function(a,b){return a.name.localeCompare(b.name);});var bq=document.getElementById('biz-q'),ch=document.getElementById('biz-chips'),c='All';
  ['All'].concat(P.o).forEach(function(x){var n=el('button','chip',x);n.type='button';n.setAttribute('aria-pressed',x==='All');n.onclick=function(){c=x;[].forEach.call(ch.children,function(y){y.setAttribute('aria-pressed',y===n);});go();};ch.appendChild(n);});
  function go(){var t=bq.value.trim().toLowerCase();var f=d.filter(function(e){return(c==='All'||e.category===c)&&(!t||[e.name,e.service,(e.tags||[]).join(' '),e.category,e.summary,e.address].join(' ').toLowerCase().indexOf(t)>=0);});groups(box,f,P);st.textContent=f.length?f.length+' businesses shown':'No matches yet. Try another word or category.';}
  bq.addEventListener('input',go);go();}
 else if(document.getElementById('f-chips')){var fq=document.getElementById('f-q'),fc=document.getElementById('f-chips'),cur='All';
  function addD(t,n){var p=t.split('-').map(Number),x=new Date(Date.UTC(p[0],p[1]-1,p[2]+n));return x.toISOString().slice(0,10);}
  var dow=new Date(Date.UTC.apply(null,today.split('-').map(function(v,i){return i===1?v-1:+v;}))).getUTCDay();
  var wkS=dow===0?addD(today,-1):addD(today,6-dow),wkE=addD(wkS,1);if(dow===0)wkS=today;
  var defs=P.k==='events'?[['All','Show all'],['week','This week'],['weekend','This weekend'],['Sports','Sports'],['free','Free']]:P.k==='resources'?[['All','Show all'],['Local','Local'],['State','State'],['Federal','Federal']]:[['All','Show all']].concat(P.o.map(function(g){return[g,g];}));
  function ok(e){if(cur==='All')return true;if(P.k==='events'){if(cur==='week')return e.start<=addD(today,6);if(cur==='weekend')return e.start<=wkE&&(e.end||e.start)>=wkS;if(cur==='free')return /free/i.test(e.cost||'');return e.group===cur;}if(P.k==='resources')return e.level===cur;return e[P.g]===cur;}
  defs.forEach(function(x){var n=el('button','chip',x[1]);n.type='button';n.setAttribute('aria-pressed',x[0]==='All');n.onclick=function(){cur=x[0];[].forEach.call(fc.children,function(y){y.setAttribute('aria-pressed',y===n);});go();};fc.appendChild(n);});
  function go(){var t=fq.value.trim().toLowerCase();var f=d.filter(function(e){return ok(e)&&(!t||[e.name,e.summary,(e.tags||[]).join(' '),e.address,e.service,e.who,e.venue,e.host,e.town,e.group,e.level].join(' ').toLowerCase().indexOf(t)>=0);});groups(box,f,P);
   st.textContent=(P.k==='events'&&!d.length)?'No upcoming events right now. Follow the Page and we will post new ones soon!':(cur==='All'&&!t)?'':(f.length?f.length+' shown. Tap Show all to see everything.':'No matches yet. Try another word or tap Show all.');}
  resetFilter=function(){fq.value='';if(cur!=='All')fc.children[0].click();else go();};fq.addEventListener('input',go);go();}
 else{groups(box,d,P);st.textContent='';}
 jump();}).catch(function(){st.textContent='This list could not load right now. Please try again soon.';});}

// theme toggle
var tday=document.getElementById('day-btn'),tnight=document.getElementById('night-btn');
function curTheme(){return document.documentElement.getAttribute('data-theme')==='dark'?'dark':'light';}
function syncTheme(){if(tday){var d=curTheme()==='dark';tday.setAttribute('aria-pressed',d?'false':'true');tnight.setAttribute('aria-pressed',d?'true':'false');}}
function setTheme(n){document.documentElement.setAttribute('data-theme',n);try{localStorage.setItem('hes-theme',n);}catch(e){}syncTheme();}
if(tday){syncTheme();tday.addEventListener('click',function(){setTheme('light');});tnight.addEventListener('click',function(){setTheme('dark');});}
try{matchMedia('(prefers-color-scheme: dark)').addEventListener('change',function(e){if(!localStorage.getItem('hes-theme')){document.documentElement.setAttribute('data-theme',e.matches?'dark':'light');syncTheme();}});}catch(e){}
// dropdowns (tap friendly)
[].forEach.call(document.querySelectorAll('.mainnav button'),function(bt){bt.addEventListener('click',function(e){e.stopPropagation();var li=bt.parentNode,o=!li.classList.contains('open');[].forEach.call(document.querySelectorAll('.mainnav li.open'),function(x){x.classList.remove('open');x.querySelector('button').setAttribute('aria-expanded','false');});li.classList.toggle('open',o);bt.setAttribute('aria-expanded',o);});});
document.addEventListener('click',function(){[].forEach.call(document.querySelectorAll('.mainnav li.open'),function(x){x.classList.remove('open');x.querySelector('button').setAttribute('aria-expanded','false');});});
// home previews
function pg(k){return PAGES.filter(function(x){return x.k===k;})[0];}
var fs=document.getElementById('feat-strip');
if(fs)get(pg('businesses')).then(function(d){var pick=d.filter(function(e){return e.website||e.facebook;});pick.sort(function(){return Math.random()-.5;});pick.slice(0,8).forEach(function(e){var c=card(e,'businesses');var lk=el('a','more','More in '+e.category+' \u2192');lk.href='businesses.html#'+slug(e.category);c.appendChild(lk);fs.appendChild(c);});});
var ep=document.getElementById('ev-prev');
if(ep)get(pg('events')).then(function(d){d.slice(0,3).forEach(function(e){ep.appendChild(card(e,'events'));});if(!d.length)ep.appendChild(el('p',null,'New events are on the way. Follow the Page to hear first!'));});
var np=document.getElementById('news-prev');
if(np)get(pg('news')).then(function(d){d.slice(0,3).forEach(function(e){np.appendChild(card(e,'news'));});});
})();
