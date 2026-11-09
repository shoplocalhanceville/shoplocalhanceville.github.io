import hashlib as _hl
# ---------- v15 extras: icons, PWA, map, report, search, Spanish, sitemap ----------
from icons import sprite as _sprite
open('icons.svg','w').write(_sprite())
def L(k):return _json.load(open(k+'.json'))
def page(k,f,body,extra='',lang='en',img='',noindex=False,dp=None,title=None,desc=None):
  t,d=(title,desc) if title else SEO[k]
  return head(t,d,f,extra,lang,img,noindex)+f'\n<body data-page="{dp or k}" data-lang="{lang}">\n'+header(f,True,lang)+body+foot(lang)
def crumbs(items,lang='en'):
  home='Inicio' if lang=='es' else 'Home';hf='es.html' if lang=='es' else 'index.html'
  return f'<div class="crumbbar"><div class="wrap"><nav class="crumbs" aria-label="{"Ruta de navegaci&oacute;n" if lang=="es" else "Breadcrumb"}"><a href="{hf}">{home}</a> &rsaquo; '+' &rsaquo; '.join(items)+'</nav></div></div>'
def crumb_ld(name,f,lang='en'):
  return ld({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Inicio" if lang=='es' else "Home","item":BASE+('es.html' if lang=='es' else '')},{"@type":"ListItem","position":2,"name":name,"item":BASE+f}]})

# ---------- PWA ----------
ICON_SVG='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40"><circle cx="20" cy="20" r="19" fill="#6d28d9"/><path d="M20 7l3.8 8 8.7 1-6.4 6 1.7 8.6L20 26.4l-7.8 4.2 1.7-8.6-6.4-6 8.7-1z" fill="#ffffff"/></svg>'
open('icon.svg','w').write(ICON_SVG)
open('manifest.webmanifest','w').write(_json.dumps({"name":"Hanceville Entertainment & Shopping","short_name":"Hanceville","description":"City services, news, events and local businesses in Hanceville, Alabama.","start_url":"./?source=pwa","scope":"./","display":"standalone","background_color":"#0B0B0F","theme_color":"#2E1065","lang":"en-US","icons":[{"src":"icons/icon-192.png","sizes":"192x192","type":"image/png"},{"src":"icons/icon-512.png","sizes":"512x512","type":"image/png"},{"src":"icons/maskable-512.png","sizes":"512x512","type":"image/png","purpose":"maskable"},{"src":"icon.svg","sizes":"any","type":"image/svg+xml"}],"shortcuts":[{"name":"Departments and Contacts","url":"departments.html"},{"name":"Report a Problem","url":"report.html"},{"name":"Events","url":"events.html"}]},indent=1))
SW_VER=V+'-'+_hl.sha1((open('app.js').read()+open('style.css').read()+open('icons.svg').read()).encode()).hexdigest()[:8]
open('sw.js','w').write("""// Hanceville Entertainment & Shopping service worker. Network first for pages and data, so nothing goes stale.
var VER='hes-"""+SW_VER+"""';
var CORE=['offline.html','style.css?v="""+V+"""','app.js?v="""+V+"""','icons.svg','icon.svg','manifest.webmanifest'];
self.addEventListener('install',function(e){e.waitUntil(caches.open(VER).then(function(c){return c.addAll(CORE);}).then(function(){return self.skipWaiting();}));});
self.addEventListener('activate',function(e){e.waitUntil(caches.keys().then(function(k){return Promise.all(k.filter(function(n){return n!==VER;}).map(function(n){return caches.delete(n);}));}).then(function(){return self.clients.claim();}));});
function net(req,key){return fetch(req).then(function(r){if(r&&r.ok&&r.type==='basic'){var c=r.clone();caches.open(VER).then(function(ca){ca.put(key||req,c);});}return r;});}
self.addEventListener('fetch',function(e){var r=e.request;if(r.method!=='GET')return;var u=new URL(r.url);if(u.origin!==location.origin)return;
 var acc=r.headers.get('accept')||'';
 if(r.mode==='navigate'||acc.indexOf('text/html')>=0){var key=new Request(u.origin+u.pathname);e.respondWith(net(r,key).catch(function(){return caches.match(key).then(function(m){return m||caches.match('offline.html');});}));return;}
 if(/\\.json$/.test(u.pathname)||/\\.ics$/.test(u.pathname)){var k2=new Request(u.origin+u.pathname);e.respondWith(net(r,k2).catch(function(){return caches.match(k2).then(function(m){return m||Response.error();});}));return;}
 e.respondWith(caches.match(r).then(function(m){return m||net(r);}));});
""")
open('offline.html','w').write(page('offline','offline.html',f'''
<main id="main"><div class="page-head"><div class="wrap"><h1>You are offline right now</h1><p>This page is not saved on your device yet. Pages you opened before will still work, and everything comes back as soon as your signal does.</p></div></div>
<section class="page-sec"><div class="wrap"><div class="infogrid"><div class="info"><h2>Emergency</h2><p><a href="tel:911">Call 911</a></p></div><div class="info"><h2>City Hall</h2><p><a href="tel:2563529830">(256) 352-9830</a></p></div><div class="info"><h2>Water Board</h2><p><a href="tel:2563529229">(256) 352-9229</a></p></div><div class="info"><h2>Fire, non emergency</h2><p><a href="tel:2563525544">(256) 352-5544</a></p></div></div>
<p><a class="btn" href="index.html">{I("house")} Try the home page</a></p></div></section></main>
''',noindex=True))

# ---------- Map ----------
GEO=_json.load(open(os.path.join(HERE,'geo-ok.json')))
def geo_of(a):
  if not a:return None
  for c in (a,a+', AL',_re.sub(r' \d{5}$','',a)):
    if c in GEO:return GEO[c]
  return None
places=[];unmapped=[];_seen=set()
SRC=[('departments','City office','departments.html'),('city','City service','city.html'),('directory','Community','directory.html'),('nonprofits','Nonprofit','nonprofits.html'),('businesses','Business','businesses.html'),('eats','Restaurant','eats.html'),('shops','Shop','shops.html')]
for k,kind,f in SRC:
  for e in L(k):
    nm=e['name'];a=e.get('address')
    if nm in _seen or not a:continue
    if 'Festival' in nm or 'Market' in nm or 'Storm Shelters'==nm:continue
    _seen.add(nm)
    grp='city' if k in('departments','city','directory') else 'biz'
    g=geo_of(a)
    item={"n":nm,"k":kind,"g":grp,"a":a,"u":f+'#'+_slug(nm)}
    if e.get('phone'):item["p"]=e['phone']
    if g:item["lat"]=round(g['lat'],6);item["lon"]=round(g['lon'],6);places.append(item)
    elif not _re.search(r'p\.?\s*o\.?\s*box',a,_re.I):unmapped.append(item)
open('geo.json','w').write(_json.dumps(places,ensure_ascii=False,separators=(',',':')))
def _pl(x):
  ph=f' &middot; <a href="{_tel(x["p"])}">{E(x["p"])}</a>' if x.get('p') else ''
  return f'<li><a href="{E(x["u"])}">{E(x["n"])}</a> <small>{E(x["k"])}</small><br><span>{E(x["a"])}</span>{ph} &middot; <a href="{E(_map(x["a"]))}" target="_blank" rel="noopener noreferrer">Directions</a></li>'
cityp=[x for x in places if x['g']=='city'];bizp=[x for x in places if x['g']=='biz']
map_html=page('map','map.html',f'''
<main id="main">{crumbs(['City Services','Map'])}<div class="page-head"><div class="wrap"><h1>Map of Hanceville City Offices and Local Businesses</h1><p>Find City Hall, the library, parks, schools and local businesses on one map. Tap a pin to call or get directions.</p></div></div>
<section class="page-sec" style="padding-top:18px"><div class="wrap">
<div class="map-tools" role="group" aria-label="Show on the map"><label><input type="checkbox" id="m-city" checked> {I("landmark")} City and community ({len(cityp)})</label><label><input type="checkbox" id="m-biz" checked> {I("store")} Businesses ({len(bizp)})</label></div>
<div id="map" class="map" role="region" aria-label="Map of Hanceville places"><p class="map-fallback">The map needs JavaScript. Every place is listed below with a directions link.</p></div>
<p class="map-note">Pins are placed from each listed street address using the U.S. Census geocoder and OpenStreetMap, and we only show a pin when the address matched cleanly. Map data &copy; <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener noreferrer">OpenStreetMap contributors</a>.</p>
</div></section>
<section class="page-sec alt-bg" id="city_places"><div class="wrap"><h2>City offices, schools and community places</h2><ul class="placelist">{''.join(_pl(x) for x in cityp)}</ul></div></section>
<section class="page-sec" id="businesses"><div class="wrap"><h2>Local businesses on the map</h2><ul class="placelist">{''.join(_pl(x) for x in bizp)}</ul></div></section>
<section class="page-sec alt-bg" id="not_mapped"><div class="wrap"><h2>Not on the map yet</h2><p>We could not match these addresses to an exact spot, so we left them off the map rather than guess. The directions links still work.</p><ul class="placelist">{''.join(_pl(x) for x in unmapped)}</ul></div></section>
</main>
<script src="vendor/leaflet/leaflet.js?v=1.9.4" defer></script><script src="map.js?v={V}" defer></script>
''',extra='<link rel="stylesheet" href="vendor/leaflet/leaflet.css?v=1.9.4">'+crumb_ld('Map','map.html'),img=' https://tile.openstreetmap.org')
open('map.html','w').write(map_html)

# ---------- Report a problem ----------
RDEP={
 'pw':("Public Works","rustyfields@cityofhanceville.net","(256) 352-9830","Rusty Fields, City Operations Manager. Phone rings at City Hall."),
 'water':("Hanceville Water and Sewer Board","maze.chase@hancevillewateral.gov","(256) 352-9229","Chase Maze, Manager."),
 'parks':("Parks and Recreation","parkdirector@cityofhanceville.net","(256) 352-9830","David Wasilewski, Parks Director. Phone rings at City Hall."),
 'permits':("Permits and Business Licenses","bhinkle@cityofhanceville.net","(256) 352-9830","Becky Hinkle at City Hall."),
 'cityhall':("Mayor's Office at City Hall","mayor@cityofhanceville.net","(256) 352-9811","The city does not publish a general City Hall email, so general reports go to the Mayor's Office."),
}
RCAT=[("Streets and Public Works",[("pothole","Pothole or street damage","pw"),("streetlight","Streetlight out","pw"),("tree","Fallen tree or limbs in the road","pw"),("brush","Brush pickup","pw"),("drainage","Drainage or flooding on a street","pw"),("sign","Damaged or missing street sign","pw")]),
 ("Water and Sewer",[("leak","Water leak","water"),("nowater","No water or low pressure","water"),("sewer","Sewer backup or odor","water"),("bill","Water bill question","water")]),
 ("Parks and Pool",[("park","Park, playground or ball field problem","parks"),("pool","City pool question","parks")]),
 ("City Hall",[("permit","Permit or business license question","permits"),("other","Something else for City Hall","cityhall")])]
def report_body(es=False):
  T=(lambda en,sp: sp if es else en)
  opts=''.join(f'<optgroup label="{E(T(g,gs))}">'+''.join(f'<option value="{v}" data-to="{d}">{E(T(lab,ES_CAT[v]))}</option>' for v,lab,d in items)+'</optgroup>' for (g,items),gs in zip(RCAT,ES_GRP))
  deps=''.join(f'<li data-key="{k}" data-name="{E(n)}" data-email="{E(m)}" data-phone="{E(p)}"><b>{E(n)}</b><br><a href="mailto:{E(m)}">{E(m)}</a> &middot; <a href="{_tel(p)}">{E(p)}</a><br><small>{E(T(note,ES_NOTE[k]))}</small></li>' for k,(n,m,p,note) in RDEP.items())
  return f'''
<section class="page-sec" style="padding-top:18px"><div class="wrap">
<div class="warnbox" role="note">{I("triangle-alert")}<div><p><b>{T("For an emergency, call 911.","En una emergencia, llame al 911.")}</b> {T("That includes fires, crashes, downed power lines, gas smells and anyone in danger.","Eso incluye incendios, choques, cables el&eacute;ctricos ca&iacute;dos, olor a gas y cualquier persona en peligro.")}</p><p>{T("This is not an official City of Hanceville portal. The form below simply opens a ready to send email in your own email app, addressed to the department the city lists for that kind of problem. Nothing is sent until you press send, and we never see or store your report.","Este no es un portal oficial de la Ciudad de Hanceville. El formulario solo abre un correo listo para enviar en su propia aplicaci&oacute;n de correo, dirigido al departamento que la ciudad indica para ese tipo de problema. No se env&iacute;a nada hasta que usted lo env&iacute;e, y nosotros nunca vemos ni guardamos su reporte.")}</p></div></div>
<form class="rp" id="rp-form" novalidate>
 <div class="rp-row"><label for="rp-cat">{T("What is the problem?","&iquest;Cu&aacute;l es el problema?")}</label><select id="rp-cat" required><option value="">{T("Choose one","Elija una opci&oacute;n")}</option>{opts}</select></div>
 <div class="rp-row"><label for="rp-where">{T("Where is it?","&iquest;D&oacute;nde est&aacute;?")}</label><input id="rp-where" type="text" required maxlength="200" autocomplete="street-address" placeholder="{T("Street address or nearest cross streets","Direcci&oacute;n o calles m&aacute;s cercanas")}"></div>
 <div class="rp-row"><label for="rp-what">{T("Tell them what you saw","Describa lo que vio")}</label><textarea id="rp-what" rows="4" maxlength="1200" placeholder="{T("For example: a deep pothole in the right lane, about the size of a tire","Por ejemplo: un bache profundo en el carril derecho, del tama&ntilde;o de una llanta")}"></textarea></div>
 <div class="rp-two"><div class="rp-row"><label for="rp-name">{T("Your name (optional)","Su nombre (opcional)")}</label><input id="rp-name" type="text" maxlength="80" autocomplete="name"></div><div class="rp-row"><label for="rp-phone">{T("Your phone (optional)","Su tel&eacute;fono (opcional)")}</label><input id="rp-phone" type="tel" maxlength="30" autocomplete="tel"></div></div>
 <p class="rp-to" id="rp-to" aria-live="polite">{T("Pick a problem to see which department gets your email.","Elija un problema para ver qu&eacute; departamento recibe su correo.")}</p>
 <p class="rp-err" id="rp-err" role="alert"></p>
 <div class="acts"><button class="btn" type="submit">{I("send")} {T("Open my email app","Abrir mi correo")}</button><a class="btn alt2" id="rp-call" href="tel:2563529830">{I("phone")} {T("Or call City Hall","O llame a la Alcald&iacute;a")}</a></div>
</form>
<p class="rp-tip">{T("Photos help. After your email app opens, attach a picture before you press send.","Las fotos ayudan. Cuando se abra su correo, adjunte una foto antes de enviarlo.")}</p>
</div></section>
<section class="page-sec alt-bg" id="who_to_contact"><div class="wrap"><h2>{T("Who handles what","Qui&eacute;n atiende cada cosa")}</h2><p>{T("You can also email or call these departments directly. Contacts come from the City of Hanceville and the Hanceville Water and Sewer Board, checked Oct. 17, 2026.","Tambi&eacute;n puede escribir o llamar directamente a estos departamentos. Los contactos vienen de la Ciudad de Hanceville y de la Junta de Agua y Alcantarillado, revisados el 17 de octubre de 2026.")}</p><ul class="rp-deps" id="rp-deps">{deps}</ul></div></section>'''
ES_GRP=["Calles y Obras P&uacute;blicas","Agua y alcantarillado","Parques y piscina","Alcald&iacute;a"]
ES_CAT={"pothole":"Bache o calle da&ntilde;ada","streetlight":"Luz de la calle apagada","tree":"&Aacute;rbol o ramas ca&iacute;das en la calle","brush":"Recogida de ramas y maleza","drainage":"Drenaje o inundaci&oacute;n en la calle","sign":"Se&ntilde;al de tr&aacute;nsito da&ntilde;ada o perdida","leak":"Fuga de agua","nowater":"Sin agua o con poca presi&oacute;n","sewer":"Alcantarillado tapado o mal olor","bill":"Pregunta sobre el recibo del agua","park":"Problema en un parque, juegos o campo deportivo","pool":"Pregunta sobre la piscina de la ciudad","permit":"Pregunta sobre permisos o licencias de negocio","other":"Otro asunto para la Alcald&iacute;a"}
ES_NOTE={"pw":"Rusty Fields, gerente de operaciones de la ciudad. El tel&eacute;fono es el de la Alcald&iacute;a.","water":"Chase Maze, gerente.","parks":"David Wasilewski, director de parques. El tel&eacute;fono es el de la Alcald&iacute;a.","permits":"Becky Hinkle, en la Alcald&iacute;a.","cityhall":"La ciudad no publica un correo general de la Alcald&iacute;a, as&iacute; que los reportes generales van a la oficina del alcalde."}
# HTML entities in ES_* are already escaped; E() would double escape, so unescape first
ES_CAT={k:_h.unescape(v) for k,v in ES_CAT.items()};ES_NOTE={k:_h.unescape(v) for k,v in ES_NOTE.items()};ES_GRP=[_h.unescape(x) for x in ES_GRP]
open('report.html','w').write(page('report','report.html',f'''
<main id="main" data-rp-lang="en">{crumbs(['City Services','Report a Problem'])}<div class="page-head"><div class="wrap"><h1>Report a Problem in Hanceville</h1><p>Spotted a pothole, a streetlight that is out or a water leak? Pick the problem, add where it is, and we will open an email to the right city department for you.</p></div></div>
{report_body()}
</main>''',extra=crumb_ld('Report a Problem','report.html')))

# ---------- Search ----------
idx=[]
for k in PAGE_ORDER:
  if k in SEO and not k.startswith('es'):idx.append({"t":_h.unescape(SEO[k][0]).split(' | ')[0],"u":'index.html' if k=='index' else k+'.html',"s":_h.unescape(SEO[k][1]),"c":"Page"})
LBL={'departments':'Departments','city':'City Services','council':'City Council','directory':'Directory','events':'Events','eats':'Places to Eat','shops':'Shops','businesses':'Business Directory','nonprofits':'Nonprofits','resources':'More Resources','wallace':'Wallace State','fun':'A Little Fun'}
for k,lab in LBL.items():
  for e in L(k):
    if k=='events' and (e.get('end') or e['start'])<TODAY:continue
    x=' '.join(str(e.get(f) or '') for f in ('type','service','category','group','address','venue','town','host','contact','title','level','role','place'))+' '+' '.join(e.get('tags') or [])
    it={"t":e['name'],"u":(k+'.html#'+_slug(e['name'])) if k!='council' else 'council.html#'+_slug(e['name']),"s":(e.get('summary') or '')[:180],"c":lab,"x":x.strip()}
    if k=='events':it["d"]=e['start']
    idx.append(it)
for e in NEWS:idx.append({"t":e['headline'],"u":story_url(e),"s":e['summary'][:180],"c":"News","d":e['date'],"x":e['category']})
for f,t,s in ES_SEARCH if 'ES_SEARCH' in globals() else []:idx.append({"t":t,"u":f,"s":s,"c":"Espa\u00f1ol"})
SEARCH_IDX=idx
open('search.html','w').write(page('search','search.html',f'''
<main id="main">{crumbs(['Search'])}<div class="page-head"><div class="wrap"><h1>Search the site</h1><p>Search every page, city department, business, event and news story on this site.</p></div></div>
<section class="page-sec" style="padding-top:18px"><div class="wrap">
<form class="sr-form" action="search.html" method="get" role="search"><label for="sr-q">Search for</label><div class="sr-row"><input id="sr-q" name="q" type="search" maxlength="100" autocomplete="off" placeholder="Try water bill, pool, pizza or council"><button class="btn" type="submit">{I("search")} Search</button></div></form>
<p id="sr-status" class="sr-status" aria-live="polite">Type a word or two and press Search.</p>
<ol id="sr-list" class="sr-list"></ol>
<noscript><p>Search needs JavaScript. You can still browse every section from the menu.</p></noscript>
</div></section></main>''',noindex=True))
exec(open(os.path.join(HERE,'es_pages.py')).read())
for f,t,s in ES_SEARCH:SEARCH_IDX.append({"t":t,"u":f,"s":s,"c":"Espa\u00f1ol"})
open('search-index.json','w').write(_json.dumps(SEARCH_IDX,ensure_ascii=False,separators=(',',':')))

# ---------- Sitemap (with hreflang) ----------
sm=['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
def _u(f):return BASE+('' if f=='index.html' else f)
for k in PAGE_ORDER:
  f=k+'.html';en=EN_OF.get(f,f);es=ES_PAIRS.get(en)
  alt=''.join(f'<xhtml:link rel="alternate" hreflang="{h}" href="{_u(x)}"/>' for h,x in (('en',en),('es',es),('x-default',en))) if es else ''
  sm.append("  <url><loc>%s</loc><lastmod>%s</lastmod><changefreq>%s</changefreq><priority>%s</priority>%s</url>"%(_u(f),TODAY,'daily' if k in('index','events','council','news') else 'weekly','1.0' if k=='index' else '0.8',alt))
for e in NEWS:sm.append("  <url><loc>%s</loc><lastmod>%s</lastmod><changefreq>monthly</changefreq><priority>0.6</priority></url>"%(BASE+story_url(e),e.get('updated',e['date'])))
sm.append('</urlset>')
open('sitemap.xml','w').write("\n".join(sm)+"\n")
print('v15 extras built',len(places),'mapped',len(unmapped),'unmapped',len(SEARCH_IDX),'search entries')
