import os,sys,shutil,argparse
# ---- paths and safety (configurable) ----
# HERE      : folder holding this script and its helpers (icons.py, build_extra.py, es_pages.py, geo-ok.json)
# SITE_DIR  : the site source (JSON data, app.js, style.css, and the existing pages). Default: the repo root
#             (two folders above this script). Override with --site-dir DIR or SLH_SITE_DIR.
# OUT_DIR   : with --out-dir DIR (or SLH_OUT_DIR) the whole build lands in DIR (a full copy of SITE_DIR with the
#             build applied). SITE_DIR is never touched. Use this to preview and diff.
# Without --out-dir the build runs in a temporary copy and the result is applied to SITE_DIR in place, but ONLY
# for files that already exist, are not hands-off and are not hand maintained (see PROTECTED below). Nothing is
# ever deleted. Every skipped or changed file is listed. --force restores the old "overwrite everything,
# delete old stories" behaviour and should not be used on the live repo.
import re as _pre,fnmatch as _fn,tempfile as _tf,atexit as _ax
HERE=os.path.dirname(os.path.abspath(__file__))
_ap=argparse.ArgumentParser(description='Build the Hanceville site pages from the JSON data.')
_ap.add_argument('--site-dir',default=os.environ.get('SLH_SITE_DIR') or os.path.abspath(os.path.join(HERE,'..','..')),help='site source folder (default: repo root)')
_ap.add_argument('--out-dir',default=os.environ.get('SLH_OUT_DIR') or None,help='write the full build here instead of in place')
_ap.add_argument('--force',action='store_true',default=os.environ.get('SLH_FORCE')=='1',help='in place: overwrite and delete everything the old script touched (dangerous)')
_ARGS,_=_ap.parse_known_args()
SITE_DIR=os.path.abspath(_ARGS.site_dir)
OUT_DIR=os.path.abspath(_ARGS.out_dir) if _ARGS.out_dir else None
if not os.path.isfile(os.path.join(SITE_DIR,'news.json')):sys.exit('build.py: %s does not look like the site folder (no news.json). Use --site-dir.'%SITE_DIR)
# Hands-off files: owned by the hourly refresh or by Charles. The build never writes these in place.
HANDS_OFF=['news.json','events.json','scores.json','story-*.html','sitemap.xml','news-sitemap.xml','ics/*','google*.html','*.txt','robots.txt']
# Hand maintained: the repo copies of these pages were edited by hand after this generator's templates were last
# in sync (new header, footer links, place pages, theme). Regenerating them would undo that work.
HAND_MAINTAINED=['index.html','businesses.html','city.html','council.html','departments.html','directory.html','eats.html','events.html','fun.html','news.html','nonprofits.html','resources.html','shops.html','wallace.html','sw.js','style.css','app.js','map.js','*.json']
PROTECTED=HANDS_OFF+HAND_MAINTAINED
def _protected(rel):return any(_fn.fnmatch(rel,p) for p in PROTECTED)
if OUT_DIR:
  WORK=OUT_DIR
  if WORK==SITE_DIR:sys.exit('build.py: --out-dir must differ from --site-dir')
  if os.path.exists(WORK):shutil.rmtree(WORK)
else:
  WORK=_tf.mkdtemp(prefix='slh-build-');_ax.register(shutil.rmtree,WORK,True)
shutil.copytree(SITE_DIR,WORK,ignore=shutil.ignore_patterns('.git','node_modules'),dirs_exist_ok=True)
os.chdir(WORK)
sys.path.insert(0,HERE)
os.environ['SLH_BUILD_HERE']=HERE
from icons import I, sprite as _sprite
import icons as _icons
BASE="https://shoplocalhanceville.github.io/"
FB="https://www.facebook.com/ShopLocalAlabama"
EMAIL="shoplocalhanceville@gmail.com"
MAIL=f'<a href="mailto:{EMAIL}">{EMAIL}</a>'
V="15"
_icons.VER=V
SIGNUP_URL=""  # paste the MailerLite hosted form URL here (https://...) once he creates it
# Visitor stats (GoatCounter). Leave empty to keep stats switched off. To switch on, put the site code here, like "hanceville".
GOATCOUNTER_CODE=""
import urllib.parse as _up
INDEXNOW_KEY="72f4bc93fc4ca032564afcff5a82c1fa"
import json as _json, datetime as _dt
from zoneinfo import ZoneInfo as _ZI
TODAY=_dt.datetime.now(_ZI("America/Chicago")).date().isoformat()
PAGE_ORDER=["index","city","departments","council","report","map","events","news","businesses","eats","shops","directory","nonprofits","resources","wallace","fun","es","es-servicios","es-departamentos","es-concejo","es-reportar"]
def ld(obj):
  return '<script type="application/ld+json">'+_json.dumps(obj,ensure_ascii=False).replace("</","<\\/")+'</script>'
NAV=[("City Services","landmark",[("city.html","City Services"),("departments.html","Departments &amp; Contacts"),("council.html","City Council"),("council.html#meeting_schedule","Council Meetings"),("report.html","Report a Problem"),("map.html","Map")]),
("News &amp; Events","newspaper",[("news.html","Local News"),("events.html","Upcoming Events")]),
("Local Businesses","store",[("businesses.html","Business Directory"),("eats.html","Local Eats"),("shops.html","Hometown Shops"),("map.html#businesses","Business Map")]),
("Community","heart-handshake",[("directory.html","Community Directory"),("nonprofits.html","Nonprofits"),("wallace.html","Wallace State"),("fun.html","Fun")]),
("resources.html","More Resources","life-buoy")]
NAV_ES=[("Servicios","landmark",[("es-servicios.html","Servicios de la ciudad"),("es-departamentos.html","Departamentos y contactos"),("es-concejo.html","Concejo municipal"),("es-reportar.html","Reportar un problema"),("map.html","Mapa (en ingl&eacute;s)")]),
("Noticias y eventos","newspaper",[("news.html","Noticias (en ingl&eacute;s)"),("events.html","Eventos (en ingl&eacute;s)")]),
("Negocios","store",[("businesses.html","Directorio de negocios (en ingl&eacute;s)"),("eats.html","Restaurantes (en ingl&eacute;s)")]),
("resources.html","M&aacute;s recursos","life-buoy")]
STAR='<svg width="38" height="38" viewBox="0 0 40 40" aria-hidden="true"><circle cx="20" cy="20" r="19" fill="#6d28d9"/><path d="M20 7l3.8 8 8.7 1-6.4 6 1.7 8.6L20 26.3 12.2 30.6l1.7-8.6-6.4-6 8.7-1z" fill="#ffffff"/></svg>'
THEME_HASH="'sha256-/fikJO3y8/FfvJxadqacMFRHk8y+I5ng+WE0NyQXczI='"
GC_HOST=f"https://{GOATCOUNTER_CODE}.goatcounter.com" if GOATCOUNTER_CODE else ""
def csp(img='',conn=''):
  g=(' '+GC_HOST) if GC_HOST else ''
  return f"default-src 'self'; script-src 'self' {THEME_HASH}; style-src 'self' 'unsafe-inline'; img-src 'self' data:{img}{g}; connect-src 'self' https://api.weather.gov{conn}{g}; font-src 'self'; object-src 'none'; base-uri 'self'; form-action 'self'; manifest-src 'self'; worker-src 'self'; upgrade-insecure-requests"
ES_PAIRS={'index.html':'es.html','city.html':'es-servicios.html','departments.html':'es-departamentos.html','council.html':'es-concejo.html','report.html':'es-reportar.html'}
EN_OF={v:k for k,v in ES_PAIRS.items()}
def head(title,desc,f,extra='',lang='en',img='',noindex=False):
  url=BASE+('' if f=='index.html' else f)
  alt=''
  en=EN_OF.get(f,f) if lang=='es' else f;es=ES_PAIRS.get(en)
  if es:alt=f'<link rel="alternate" hreflang="en" href="{BASE+("" if en=="index.html" else en)}"><link rel="alternate" hreflang="es" href="{BASE+es}"><link rel="alternate" hreflang="x-default" href="{BASE+("" if en=="index.html" else en)}">'
  gc=f'<script data-goatcounter="{GC_HOST}/count" async src="vendor/goatcounter/count.js"></script>' if GC_HOST and not noindex else ''
  loc='es_US' if lang=='es' else 'en_US'
  return f'''<!doctype html>
<html lang="{lang}"><head>
<meta charset="utf-8"><meta http-equiv="Content-Security-Policy" content="{csp(img)}"><meta name="referrer" content="strict-origin-when-cross-origin"><meta name="viewport" content="width=device-width, initial-scale=1">
<script>(function(){{try{{var t=localStorage.getItem('hes-theme');if(t!=='dark'&&t!=='light')t=matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light';document.documentElement.setAttribute('data-theme',t);}}catch(e){{}}}})();</script>
<title>{title}</title><meta name="description" content="{desc}">
<meta name="color-scheme" content="light dark">
<link rel="canonical" href="{url}">{alt}<meta name="robots" content="{'noindex, follow' if noindex else 'index, follow, max-image-preview:large'}">
<meta property="og:type" content="website"><meta property="og:locale" content="{loc}"><meta property="og:site_name" content="Hanceville Entertainment &amp; Shopping">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}og-image.jpg">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="Hanceville Entertainment and Shopping, Shop Local Alabama">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{title}"><meta name="twitter:description" content="{desc}"><meta name="twitter:image" content="{BASE}og-image.jpg"><meta name="twitter:image:alt" content="Hanceville Entertainment and Shopping, Shop Local Alabama"><meta name="theme-color" content="#2e1065">
<link rel="icon" href="icon.svg" type="image/svg+xml"><link rel="icon" href="icons/icon-192.png" sizes="192x192" type="image/png"><link rel="apple-touch-icon" href="icons/apple-touch-icon.png"><link rel="manifest" href="manifest.webmanifest">
<link rel="stylesheet" href="style.css?v={V}">
{extra}{gc}
</head>'''
def nav(cur,lang='en'):
  out=['<nav class="mainnav" aria-label="'+('Principal' if lang=='es' else 'Main')+'"><ul>']
  for item in (NAV_ES if lang=='es' else NAV):
    if isinstance(item[2],list):
      out.append(f'<li><button type="button" aria-haspopup="true" aria-expanded="false">{I(item[1])}{item[0]} {I("chevron-down","ic chev")}</button><ul class="dd">')
      for f,t in item[2]:out.append(f'<li><a href="{f}"'+(' aria-current="page"' if f==cur else '')+f'>{t}</a></li>')
      out.append('</ul></li>')
    else:out.append(f'<li><a href="{item[0]}"'+(' aria-current="page"' if item[0]==cur else '')+f'>{I(item[2])}{item[1]}</a></li>')
  out.append('</ul></nav>');return ''.join(out)
def header(cur,search=True,lang='en'):
  es=lang=='es'
  ph='Buscar en el sitio...' if es else 'Search Hanceville...'
  s=f'<div class="head-search"><form class="gs" id="gs-form" role="search" action="search.html" method="get"><label for="gs-q" class="sr">{"Buscar en todo el sitio" if es else "Search the whole site"}</label><input id="gs-q" name="q" type="search" placeholder="{ph}" autocomplete="off" aria-controls="gs-res" aria-autocomplete="list"><button type="submit" class="gs-go" aria-label="{"Buscar" if es else "Search"}">{I("search")}</button><div class="gs-res" id="gs-res" aria-live="polite"></div></form></div>' if search else ''
  other=EN_OF.get(cur,'index.html') if es else ES_PAIRS.get(cur,'es.html')
  lt=f'<a class="lang" href="{other}" hreflang="{"en" if es else "es"}" lang="{"en" if es else "es"}">{I("languages")}<span>{"English" if es else "Espa&ntilde;ol"}</span></a>'
  sig=('Reciba noticias de Hanceville por correo.' if es else 'Get Hanceville updates by email.')
  sigb=('Suscribirme' if es else 'Sign me up')
  return f'''<a class="skip" href="#main">{"Saltar al contenido" if es else "Skip to content"}</a>
<header class="site-head"><div class="wrap">
 <a class="logo" href="{"es.html" if es else "index.html"}">{STAR}<span>Hanceville<small>ENTERTAINMENT &amp; SHOPPING</small></span></a>
 <button class="tab-toggle" id="tab-toggle" type="button" aria-controls="tabs" aria-expanded="false">{I("menu")}<span>{"Men&uacute;" if es else "Menu"}</span></button>
 <div class="head-row2">{s}<div class="mode" role="group" aria-label="{"Modo de color" if es else "Color mode"}"><button type="button" id="day-btn" aria-pressed="true">{I("sun")}<span>{"D&iacute;a" if es else "Day"}</span></button><button type="button" id="night-btn" aria-pressed="false">{I("moon")}<span>{"Noche" if es else "Night"}</span></button></div>{lt}</div>
</div><div class="navbar">{nav(cur,lang)}</div></header>
<div class="wx" id="wx" hidden></div>
<div class="alertbar"><div class="wrap"><span>{sig}</span> <a href="{SIGN_HREF}"{SIGN_EXT}>{sigb}</a></div></div>
<nav class="tabs" id="tabs" aria-label="{"Men&uacute; completo" if es else "Full menu"}"></nav>'''
SIGN_HREF=SIGNUP_URL or "mailto:"+EMAIL+"?subject="+_up.quote("Sign me up for updates")+"&body="+_up.quote("Please add me to the Hanceville Entertainment & Shopping email list for event updates and special offers.\n\nMy name:\nMy ZIP code (optional):")
SIGN_EXT=' target="_blank" rel="noopener noreferrer"' if SIGNUP_URL else ''
def signup(idv,h='h2'):
  return f'''<section id="{idv}" class="signup-sec"><div class="wrap"><div class="signup">
 <div class="su-text"><{h}>Get Hanceville updates by email</{h}>
 <p class="big-p">Be the first to hear about city news, things to do this weekend and shop local deals. We send one friendly email at a time and never spam.</p>
 <p class="privacy">Your privacy matters to us. We use your email only for Hanceville updates and offers. We never sell it or share it, and you can unsubscribe any time{'' if SIGNUP_URL else ' by replying "unsubscribe"'}.</p></div>
 <p class="su-act"><a class="btn" href="{SIGN_HREF}"{SIGN_EXT}>{I("mail")} Sign me up</a></p>
</div></div></section>'''
def foot(lang='en'):
  es=lang=='es'
  if es:
    cols=f'''  <div><h3>{I("landmark")}Servicios</h3><ul><li><a href="es-servicios.html">Servicios de la ciudad</a></li><li><a href="es-departamentos.html">Departamentos y contactos</a></li><li><a href="es-concejo.html">Concejo municipal</a></li><li><a href="es-reportar.html">Reportar un problema</a></li></ul></div>
  <div><h3>{I("languages")}English</h3><ul><li><a href="index.html">Home</a></li><li><a href="city.html">City Services</a></li><li><a href="departments.html">Departments</a></li><li><a href="events.html">Events</a></li></ul></div>
  <div><h3>{I("life-buoy")}Ayuda</h3><ul><li><a href="tel:911">Emergencias: 911</a></li><li><a href="resources.html">M&aacute;s recursos (en ingl&eacute;s)</a></li><li><a href="map.html">Mapa (en ingl&eacute;s)</a></li></ul></div>'''
    about='Tambi&eacute;n conocido como Shop Local Alabama. Compartimos la gente, los lugares y los negocios que hacen de Hanceville un buen hogar.'
    legal='Esta es una gu&iacute;a comunitaria independiente. No es la C&aacute;mara de Comercio oficial y no pertenece a la Ciudad de Hanceville.'
    contact='Cont&aacute;ctenos'
  else:
    cols=f'''  <div><h3>{I("landmark")}City Services</h3><ul><li><a href="city.html">City Services</a></li><li><a href="departments.html">Departments &amp; Contacts</a></li><li><a href="council.html">City Council</a></li><li><a href="council.html#meeting_schedule">Council Meetings</a></li><li><a href="report.html">Report a Problem</a></li><li><a href="map.html">Map</a></li></ul></div>
  <div><h3>{I("newspaper")}News, Events &amp; Businesses</h3><ul><li><a href="news.html">Local News</a></li><li><a href="events.html">Upcoming Events</a></li><li><a href="businesses.html">Business Directory</a></li><li><a href="eats.html">Local Eats</a></li><li><a href="shops.html">Hometown Shops</a></li></ul></div>
  <div><h3>{I("heart-handshake")}Community &amp; More</h3><ul><li><a href="directory.html">Community Directory</a></li><li><a href="nonprofits.html">Nonprofits</a></li><li><a href="wallace.html">Wallace State</a></li><li><a href="fun.html">A Little Fun</a></li><li><a href="resources.html">More Resources (State &amp; Federal)</a></li><li><a href="businesses.html#get-featured">Get Featured</a></li><li><a href="es.html" lang="es" hreflang="es">En espa&ntilde;ol</a></li></ul></div>'''
    about='Also known as Shop Local Alabama. We share the people, places and small businesses that make Hanceville and Cullman County feel like home.'
    legal='This is an independent community guide. It is not the official Chamber of Commerce and is not affiliated with the City of Hanceville.'
    contact='Contact us'
  fl='' if es else f'''<p class="foot-legal">Listings are for information only, so please check hours and details with each business before you go. Logos and trademarks belong to their owners, and news stories are written by us with links to every source. Business owners can request changes or removal any time at <a href="mailto:{EMAIL}?subject=Listing%20change%20request">{EMAIL}</a>. Icons by <a href="https://lucide.dev" target="_blank" rel="noopener noreferrer">Lucide</a> (ISC license). Map data &copy; <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener noreferrer">OpenStreetMap</a> contributors.</p>'''
  return f'''<footer><div class="wrap">
 <div class="foot-grid">
  <div><h3>Hanceville Entertainment &amp; Shopping</h3><p>{about}</p><p><a href="{FB}" target="_blank" rel="noopener noreferrer">{I("thumbs-up")}{"S&iacute;ganos en Facebook" if es else "Follow us on Facebook"}</a></p><p><strong>{contact}:</strong> {MAIL}</p></div>
{cols}
 </div>
 <div class="foot-signup"><p><strong>{"Reciba noticias y ofertas locales por correo." if es else "Get event updates and local offers by email."}</strong> <a href="{SIGN_HREF}"{SIGN_EXT}>{"Suscribirme" if es else "Sign me up"}</a></p></div>
 {fl}
 <p class="foot-note">&copy; 2026 Hanceville Entertainment &amp; Shopping. {legal}</p>
</div></footer>
<script src="app.js?v={V}"></script>
</body></html>
'''
FOOT=foot('en')
FEAT=f'''<section id="get-featured"><div class="wrap"><div class="feature">
 <h2>Want your business featured? It&rsquo;s free.</h2>
 <p>We love telling people about the folks who make Hanceville a good place to live. Restaurants, shops, service businesses, churches, schools and nonprofits are all welcome, and there is never a charge.</p>
 <ol><li>Visit our Facebook Page and tap Message, or email us at {MAIL}.</li><li>Tell us who you are, what you do and what is coming up.</li><li>Add a photo or two if you have them, and we will take it from there.</li></ol>
 <p class="acts"><a class="btn" href="{FB}" target="_blank" rel="noopener noreferrer">{I("thumbs-up")} Message us on Facebook</a> <a class="btn" href="mailto:{EMAIL}?subject=Submit%20an%20event%20or%20business">{I("mail")} Email us</a></p>
</div></div></section>'''
SEO={
'index':("Hanceville, AL City Services, City Hall Phone Numbers, News &amp; Events","Hanceville, AL 35077 in one place: City Hall phone numbers, every department and who to call, City Council meetings, paying your water bill, storm shelters, local news and things to do this weekend."),
'events':("Things to Do in Hanceville &amp; Cullman This Weekend | Events","Things to do in Hanceville and Cullman this weekend: fall festivals, pumpkin patches, ballgames, library storytimes, markets and free, kid friendly events across Cullman County."),
'eats':("Hanceville, AL Restaurants: Mexican, Pizza, Coffee &amp; Diners","Restaurants in Hanceville, AL: hometown diners, Mexican restaurants, pizza, coffee shops and a classic soda fountain near Wallace State, with addresses, phone numbers and daily specials."),
'shops':("Hanceville, AL Shops, Boutiques &amp; Markets | Shop Local","Shop local in Hanceville, AL: a historic soda fountain and drugstore, vintage finds, flowers, handmade guitars and holiday markets in Cullman County."),
'businesses':("Hanceville, AL Business Directory: Banks, Mechanics, Barbers &amp; More","Hanceville, AL business directory with phone numbers, directions and open now hours where we could verify them: banks, auto repair, tires, barbers, florists, vets and more."),
'news':("Hanceville, AL News: City Council, Schools, Sports &amp; Weather","Hanceville, AL news from City Hall, the City Council, Hanceville schools, Bulldogs and Wallace State sports, public safety and weather. Every story is dated and links to its sources."),
'nonprofits':("Hanceville, AL Nonprofits, Food Pantries &amp; Volunteer Groups","Food pantries, Knapsacks for Kids, civic clubs and other nonprofits in Hanceville, AL and Cullman County, plus simple ways to volunteer or give."),
'resources':("More Resources for Hanceville, AL: State, Federal &amp; County Help","State, federal and county help for Hanceville, AL families: SNAP and food assistance, DHR, child care, senior services, Medicare, Social Security and crisis lines."),
'directory':("Hanceville, AL Schools, Public Safety &amp; Community Directory","Hanceville, AL schools, the Sheriff and fire department, water and sewer, the library, parks and the senior center, with phone numbers and directions."),
'wallace':("Wallace State Community College Services | Hanceville, AL","Who to call at Wallace State Community College in Hanceville, AL: admissions, financial aid, free tutoring, career help, counseling, housing and the dental clinic."),
'fun':("Hanceville, AL Fun Facts, Landmarks &amp; Local History","How Hanceville, AL got its name, local history, landmarks like the Shrine of the Most Blessed Sacrament, and a few sweet tea jokes."),
'council':("Hanceville City Council: Members, Meeting Dates, Agendas &amp; Minutes","Meet the Hanceville, AL City Council and Mayor, see the next City Council meeting dates at City Hall, add them to your calendar, and find agendas, minutes and meeting videos."),
'city':("Hanceville, AL City Services: Pay Water Bill, Permits, Parks &amp; Shelters","Hanceville, AL city services in one place: City Hall, the Mayor's Office, the water department phone number and bill pay, permits, car tags, storm shelters, the city pool and parks."),
'departments':("Hanceville City Hall Phone Number &amp; Department Contacts","Hanceville City Hall phone number, the City Clerk and every city department with the person to contact, title, phone, email, address and hours: water, fire, public works, parks and library."),
'report':("Report a Problem in Hanceville, AL: Potholes, Streetlights, Water Leaks","Report a pothole, streetlight outage, water leak or park problem in Hanceville, AL. Pick a problem and we open a ready to send email to the right city department."),
'map':("Map of Hanceville, AL City Offices &amp; Local Businesses","An interactive map of Hanceville, AL city offices, parks, schools and local businesses, with directions and phone numbers for each place."),
'search':("Search Hanceville Entertainment &amp; Shopping","Search every page and listing on this Hanceville, AL community guide."),
'offline':("You are offline | Hanceville Entertainment &amp; Shopping","This page is not saved on your device yet."),
}
ORG={"@type":"Organization","@id":BASE+"#org","name":"Hanceville Entertainment & Shopping","alternateName":"Shop Local Alabama","url":BASE,"logo":BASE+"og-image.jpg","image":BASE+"og-image.jpg","email":EMAIL,"sameAs":[FB],"description":"An independent community guide to Hanceville, Alabama. Not the official Chamber of Commerce and not affiliated with the City of Hanceville.","areaServed":[{"@type":"City","name":"Hanceville, Alabama"},{"@type":"AdministrativeArea","name":"Cullman County, Alabama"}],"contactPoint":{"@type":"ContactPoint","contactType":"customer support","email":EMAIL,"areaServed":"US","availableLanguage":["English","Spanish"]}}
SITE={"@type":"WebSite","@id":BASE+"#website","name":"Hanceville Entertainment & Shopping","alternateName":"Shop Local Alabama","url":BASE,"inLanguage":"en-US","publisher":{"@id":BASE+"#org"},"potentialAction":{"@type":"SearchAction","target":{"@type":"EntryPoint","urlTemplate":BASE+"search.html?q={search_term_string}"},"query-input":"required name=search_term_string"}}
import html as _h, re as _re
def _slug(x):return _re.sub(r' +','_',_re.sub(r'[^a-z0-9]+',' ',x.lower().replace('&','and')).strip())
def _addr(a):
  if not a or 'P.O. Box' in a or 'PO Box' in a:return None
  parts=[x.strip() for x in a.split(',')]
  m=_re.match(r'^(AL|Alabama)\s*(\d{5})?$',parts[-1]) if parts else None
  if len(parts)>=3 and m:
    o={"@type":"PostalAddress","streetAddress":', '.join(parts[:-2]),"addressLocality":parts[-2],"addressRegion":"AL","addressCountry":"US"}
    if m.group(2):o["postalCode"]=m.group(2)
    return o
  return None
def _btype(e):
  s=(e.get('service') or e.get('type') or '').lower();c=e.get('category','')
  for k,t in [('fast food','FastFoodRestaurant'),('coffee','CafeOrCoffeeShop'),('restaurant','Restaurant'),('cafe','CafeOrCoffeeShop'),('taqueria','Restaurant'),('pizza','Restaurant'),('sandwich','Restaurant'),('smoothie','FoodEstablishment'),('barber','HairSalon'),('car dealer','AutoDealer'),('truck dealer','AutoDealer'),('body shop','AutoBodyShop'),('tire','TireShop'),('auto repair','AutoRepair'),('hvac','HVACBusiness'),('pharmacy','Pharmacy'),('veterinar','VeterinaryCare'),('child care','ChildCare'),('bank','BankOrCreditUnion'),('insurance','InsuranceAgency'),('florist','Florist'),('hotel','Hotel'),('shrine','PlaceOfWorship'),('roastery','CafeOrCoffeeShop'),('vintage','ClothingStore'),('guitar','Store')]:
    if k in s:return 'Restaurant' if (t=='CafeOrCoffeeShop' and c=='Restaurants') else t
  if c=='Restaurants':return 'Restaurant'
  return 'LocalBusiness'
def biz_ld(items,page):
  out=[]
  for e in items:
    ad=_addr(e.get('address'))
    if not ad:continue
    b={"@type":_btype(e),"@id":BASE+page+"#"+_slug(e['name']),"name":e['name'],"description":e['summary'],"address":ad}
    if e.get('phone'):b["telephone"]=e['phone']
    site=e.get('website') if e.get('website') and 'facebook.com' not in e.get('website','') else None
    if site:b["url"]=site
    fbs=[x for x in [e.get('facebook'),e.get('website') if 'facebook.com' in (e.get('website') or '') else None] if x]
    if fbs:b["sameAs"]=fbs
    if e.get('logo'):b["logo"]=BASE+e['logo'];b["image"]=BASE+e['logo']
    if e.get('hours_week'):
      DN={'mon':'Monday','tue':'Tuesday','wed':'Wednesday','thu':'Thursday','fri':'Friday','sat':'Saturday','sun':'Sunday'}
      b["openingHoursSpecification"]=[{"@type":"OpeningHoursSpecification","dayOfWeek":"https://schema.org/"+DN[dk],"opens":o,"closes":c} for dk,sl in e['hours_week'].items() for o,c in sl]
    out.append({"@type":"ListItem","position":len(out)+1,"item":b})
  return {"@context":"https://schema.org","@type":"ItemList","name":"Local businesses in Hanceville, Alabama","itemListElement":out} if out else None
GOV_DIR={"Hanceville City Hall":"City of Hanceville","Mayor's Office":"City of Hanceville","City Council":"City of Hanceville","Hanceville Municipal Court":"City of Hanceville","Hanceville Fire and Rescue":"City of Hanceville","Cullman County Sheriff's Office":"Cullman County Sheriff's Office","Hanceville Water and Sewer Board":"Hanceville Water and Sewer Board","Public Works Department":"City of Hanceville","Shirley Burden Public Library":"City of Hanceville","Parks and Recreation":"City of Hanceville","Hanceville Senior Center":"Cullman County Commission on Aging","Hanceville Post Office":"United States Postal Service","Cullman County Emergency Management Agency":"Cullman County","Secret Witness Tip Line":"Cullman County Sheriff's Office","Cullman County Sanitation Department":"Cullman County"}
DHR="Alabama Department of Human Resources";ADPH="Alabama Department of Public Health"
GOV_RES={"Cullman County Health Department":ADPH,"Women's Health and Family Planning":ADPH,"WIC Nutrition Program":ADPH,"ALL Kids and Medicaid for Children":ADPH,"Alabama Department of Rehabilitation Services":"Alabama Department of Rehabilitation Services","Cullman Housing Authority":"Cullman Housing Authority","Alabama Career Center, Cullman":"Alabama Department of Workforce","Cullman County Commission on Aging":"Cullman County Commission on Aging","Hanceville Senior Center":"Cullman County Commission on Aging","Colony Senior Center":"Cullman County Commission on Aging","Meals for Homebound Seniors":"Cullman County Commission on Aging","SHIP Medicare Counseling":"Alabama Department of Senior Services","Alabama Department of Senior Services":"Alabama Department of Senior Services","Medicaid Waiver Care at Home":"Alabama Medicaid Agency","Report Elder Abuse: Adult Abuse Hotline":DHR,"Social Security Office, Cullman":"Social Security Administration","SNAP Food Assistance at Cullman County DHR":DHR,"Apply for SNAP Online (MyDHR)":DHR,"Alabama Food Assistance Information Line":DHR,"Simple SNAP Application for Seniors (AESAP)":DHR,"Cullman County DHR Office":DHR,"Report Child Abuse or Neglect":DHR,"Adult Protective Services, Cullman County":DHR,"Family Assistance (TANF)":DHR,"Child Support Services":DHR,"Help Paying for Child Care (Child Care Subsidy)":DHR,"Find a Licensed Child Care Provider":DHR,"First Class Pre-K":"Alabama Department of Early Childhood Education","USA.gov Benefit Finder":"U.S. General Services Administration","Social Security Administration":"Social Security Administration","Medicare":"Centers for Medicare and Medicaid Services","Veterans Crisis Line":"U.S. Department of Veterans Affairs","Cullman County Extension Office (ACES)":"Alabama Cooperative Extension System","Cullman County Veterans Service Office":"Alabama Department of Veterans Affairs"}
def gov_ld(items,page,prov):
  out=[]
  for e in items:
    if e['name'] not in prov:continue
    g={"@type":"GovernmentService","@id":BASE+page+"#"+_slug(e['name']),"name":e['name'],"description":e['summary'],"serviceType":e.get('group',''),"provider":{"@type":"GovernmentOrganization","name":prov[e['name']]},"areaServed":{"@type":"AdministrativeArea","name":"Cullman County, Alabama"}}
    ch={"@type":"ServiceChannel"}
    if e.get('phone'):ch["servicePhone"]={"@type":"ContactPoint","telephone":e['phone']}
    if e.get('website'):ch["serviceUrl"]=e['website']
    ad=_addr(e.get('address'))
    if ad:ch["serviceLocation"]={"@type":"Place","address":ad}
    if len(ch)>1:g["availableChannel"]=ch
    out.append(g)
  return {"@context":"https://schema.org","@graph":out} if out else None

NEWS=_json.load(open('news.json'))
NEWS.sort(key=lambda e:e['date'],reverse=True)
CATCLS=lambda c:'cat-'+_re.sub(r'[^a-z]+','',c.lower())
def nice_date(d):
  x=_dt.date.fromisoformat(d);return x.strftime('%b ')+str(x.day)+x.strftime(', %Y')
def long_date(d):
  x=_dt.date.fromisoformat(d);return x.strftime('%A, %B ')+str(x.day)+x.strftime(', %Y')
def story_url(e):return 'story-'+e['id']+'.html'
def E(x):return _h.escape(x,quote=True)
CAT_IC={'City Hall':'landmark','Schools':'school','Sports':'trophy','Public Safety':'shield','Weather':'cloud-sun','Around the County':'map-pinned','Announcements':'megaphone'}
def CI(c):return I(CAT_IC.get(c,'newspaper'),'ic art-ic')
def story_card(e,hl='h3'):
  return f'''<article class="story-card {CATCLS(e['category'])}"><div class="cat-art sm" aria-hidden="true">{CI(e['category'])}</div><div class="sc-body"><p class="kick"><span class="catpill">{E(e['category'])}</span> <time datetime="{e['date']}">{nice_date(e['date'])}</time></p><{hl}><a href="{story_url(e)}">{E(e['headline'])}</a></{hl}><p class="sum">{E(e['summary'])}</p></div></article>'''
COUNCIL=_json.load(open('council.json'))
COUNCIL_URL="https://www.cityofhanceville.net/o/coh/page/city-council"
DEPS=_json.load(open('departments.json'))
DEP_ORDER=[]
for _e in DEPS:
  if _e['group'] not in DEP_ORDER:DEP_ORDER.append(_e['group'])
HOME_DEPS=["Mayor's Office","City Clerk","Permits, Business Licenses and Facility Rentals","Public Works","Hanceville Water and Sewer Board","Hanceville Fire and Rescue"]
def _tel(p):return 'tel:'+_re.sub(r'[^0-9]','',p)
def _map(a):return "https://www.google.com/maps/dir/?api=1&destination="+_up.quote(a)
def _ini(n):
  w=[x for x in _re.sub(r"[^A-Za-z0-9 ]"," ",n).split() if x.lower() not in('the','of','and','at','a','an')]
  return ((w[0][0] if w else '?')+(w[1][0] if len(w)>1 else '')).upper()
DEP_IC={"Mayor's Office":"landmark","City Clerk":"file-text","Permits, Business Licenses and Facility Rentals":"clipboard-list","Accounts Payable and Receivable":"piggy-bank","Human Resources":"users","Hanceville Fire and Rescue":"flame","Law Enforcement":"shield","Storm Shelters":"tornado","Public Works":"construction","Hanceville Water and Sewer Board":"droplet","Parks and Recreation":"tree-pine","Shirley Burden Public Library":"book-open","Planning Commission":"map","Events and Community Development Committee":"calendar","Cullman County Satellite Office":"building-2"}
def dep_card(e,h='h3',compact=False):
  nm=E(e['name']);o=[f'<article class="dep" id="{_slug(e["name"])}"><div class="dep-head"><span class="ini dep-ic">{I(DEP_IC.get(e["name"],"landmark"))}</span><div><{h}>{nm}</{h}><p class="dep-who"><b>{E(e["contact"])}</b><span>{E(e["title"])}</span></p></div></div>']
  dl=[]
  if e.get('phone'):dl.append(f'<dt>Phone</dt><dd><a href="{_tel(e["phone"])}">{E(e["phone"])}</a></dd>')
  if e.get('emergency'):dl.append('<dt>Emergency</dt><dd><a href="tel:911">911</a></dd>')
  if e.get('email'):dl.append(f'<dt>Email</dt><dd><a href="mailto:{E(e["email"])}">{E(e["email"])}</a></dd>')
  if e.get('fax') and not compact:dl.append(f'<dt>Fax</dt><dd>{E(e["fax"])}</dd>')
  if e.get('address'):dl.append(f'<dt>Address</dt><dd>{E(e["address"])}</dd>')
  if e.get('hours') and not compact:dl.append(f'<dt>Hours</dt><dd>{E(e["hours"])}</dd>')
  o.append('<dl class="dep-dl">'+''.join(dl)+'</dl>')
  if not compact:o.append(f'<p class="sum">{E(e["summary"])}</p>')
  if not compact:o.append(board_next_html(e['name']))
  a=[]
  if e.get('phone'):a.append(f'<a class="btn" href="{_tel(e["phone"])}" aria-label="Call {nm}"><svg class="ic" aria-hidden="true" focusable="false"><use href="icons.svg#i-phone"></use></svg>Call</a>')
  if e.get('email'):a.append(f'<a class="btn alt3" href="mailto:{E(e["email"])}" aria-label="Email {nm}"><svg class="ic" aria-hidden="true" focusable="false"><use href="icons.svg#i-mail"></use></svg>Email</a>')
  if e.get('address'):a.append(f'<a class="btn alt2" href="{E(_map(e["address"]))}" target="_blank" rel="noopener noreferrer" aria-label="Directions to {nm}"><svg class="ic" aria-hidden="true" focusable="false"><use href="icons.svg#i-navigation"></use></svg>Directions</a>')
  if e.get('website') and not compact:a.append(f'<a class="btn alt3" href="{E(e["website"])}" target="_blank" rel="noopener noreferrer" aria-label="Website for {nm}"><svg class="ic" aria-hidden="true" focusable="false"><use href="icons.svg#i-globe"></use></svg>Website</a>')
  o.append('<div class="acts">'+''.join(a)+'</div>')
  if not compact and e.get('source'):o.append(f'<p class="src"><a href="{E(e["source"])}" target="_blank" rel="noopener noreferrer" aria-label="Source for {nm}">Source</a></p>')
  o.append('</article>');return ''.join(o)
# School themes: official colors only (see city-sources.md). key -> regex
SCHOOL_RX=[('wallace',r'Wallace State'),('hes',r'Hanceville (Elementary|Primary)'),('hhs',r'Hanceville (High|Middle)|\bHHS\b|Bulldogs'),('ccs',r'Cullman County (Schools|Board of Education)')]
def school_of(*txt):
  for t in txt:
    for k,rx in SCHOOL_RX:
      if t and _re.search(rx,t):return k
  return None
CITY_HALL="112 Main Street SE, Hanceville, AL 35077"
CH_MAP="https://www.google.com/maps/dir/?api=1&destination="+_up.quote(CITY_HALL)
# Regular meetings: 2nd and 4th Thursday, work session 6:00 PM then regular meeting
CONFIRMED={"2026-10-22":"Confirmed on the city calendar and the Oct. 8 agenda","2026-11-12":"Confirmed on the city's Oct. 8 and Oct. 22 agendas"}
CANCELLED={"2026-11-26":"Moved off Thanksgiving Day. The council voted Oct. 22 to meet Tuesday, Nov. 24 instead"}
RESCHEDULED={"2026-11-24":"Moved from Thanksgiving Day by council vote on Oct. 22. Check the city calendar to confirm the start time"}  # date -> note, when the city posts a cancellation
def _holiday(d):
  if d.month==11 and d.weekday()==3 and 22<=d.day<=28:return "Thanksgiving Day"
  if d.month==12 and d.day in(24,25):return "Christmas Eve" if d.day==24 else "Christmas Day"
  if d.month==1 and d.day==1:return "New Year's Day"
  if d.month==7 and d.day==4:return "Independence Day"
  return None
def next_meetings(n=4):
  d=_dt.date.fromisoformat(TODAY);out=[]
  while len(out)<n:
    if (d.weekday()==3 and (d.day-1)//7 in(1,3) and d.isoformat() not in CANCELLED) or d.isoformat() in RESCHEDULED:out.append(d)
    d+=_dt.timedelta(days=1)
  return out
def gcal(text,start,end,details,location):
  if isinstance(start,_dt.datetime):dates=start.strftime('%Y%m%dT%H%M%S')+'/'+end.strftime('%Y%m%dT%H%M%S')
  else:dates=start.strftime('%Y%m%d')+'/'+end.strftime('%Y%m%d')
  return 'https://calendar.google.com/calendar/render?'+_up.urlencode({'action':'TEMPLATE','text':text,'dates':dates,'details':details[:900],'location':location,'ctz':'America/Chicago'})
def cal_btns(ics,g,label):
  return f'<div class="acts cal-acts"><a class="btn alt3" href="{ics}" download aria-label="Download a calendar file for {E(label)}">{I("download")} Add to calendar (.ics)</a><a class="btn alt3" href="{E(g)}" target="_blank" rel="noopener noreferrer" aria-label="Add {E(label)} to Google Calendar">{I("calendar-plus")} Google Calendar</a></div>'
def council_gcal(d):
  hol=_holiday(d)
  return gcal('Hanceville City Council Meeting',_dt.datetime(d.year,d.month,d.day,18,0),_dt.datetime(d.year,d.month,d.day,19,30),'Work session at 6:00 PM, followed by the regular Hanceville City Council meeting. Open to the public.'+(' This date falls on '+hol+', so check the city calendar for changes.' if hol else '')+' '+COUNCIL_URL,'Hanceville City Hall, 112 Main Street SE, Hanceville, AL 35077')
def mtg_ics_name(d):return f"ics/hanceville_city_council_{d.isoformat()}.ics"
MEETINGS=next_meetings(4)
def nth_weekday(nth,wd):
  d=_dt.date.fromisoformat(TODAY)
  for _ in range(90):
    if d.weekday()==wd and (d.day-1)//7==nth-1:return d
    d+=_dt.timedelta(days=1)
BOARDS=[('planning_commission','Hanceville Planning Commission Meeting','Hanceville Civic Center, 902 Commercial Street, Hanceville, AL 35077','The Planning Commission meets the fourth Monday of each month at 6 PM at the Civic Center. Check the city website for changes before you go. https://www.cityofhanceville.net/o/coh/page/planning-commission','https://www.cityofhanceville.net/o/coh/page/planning-commission',4),
 ('events_committee','Hanceville Events and Community Development Committee Meeting','Shirley Burden Public Library, 201 Commercial Street, Hanceville, AL 35077','The committee meets the first Monday of each month at 6 PM at the library and is open to the public. Check the city website for changes before you go. https://www.cityofhanceville.net/page/events-community-development-committee','https://www.cityofhanceville.net/page/events-community-development-committee',1)]
BOARD_NEXT=[(b[:5],nth_weekday(b[5],0)) for b in BOARDS]
def board_ics_name(k,d):return f"ics/hanceville_{k}_{d.isoformat()}.ics"
BOARD_BY_DEP={'Planning Commission':0,'Events and Community Development Committee':1}
def board_next_html(depname):
  if depname not in BOARD_BY_DEP:return ''
  (k,nm,loc,desc,url),d=BOARD_NEXT[BOARD_BY_DEP[depname]]
  g=gcal(nm,_dt.datetime(d.year,d.month,d.day,18,0),_dt.datetime(d.year,d.month,d.day,19,0),desc,loc)
  return f'<p class="next-mtg">{I("calendar")} Next regular meeting: <b>{d.strftime("%A, %B ")}{d.day} at 6 PM</b>. Check the city website for changes before you go.</p>'+cal_btns(board_ics_name(k,d),g,nm)
def meeting_li(d):
  hol=_holiday(d);iso=d.isoformat()
  status=CONFIRMED.get(iso) or RESCHEDULED.get(iso) or ("Falls on "+hol+". The city often moves holiday meetings, so check the city calendar before you go." if hol else "Regular schedule. Check the city calendar for any change.")
  lab=f"the {d.strftime('%B ')}{d.day} City Council meeting"
  return f'''<li><span class="datebadge" aria-hidden="true"><span class="m">{d.strftime('%b')}</span><span class="d">{d.day}</span></span><div><b>{d.strftime('%A, %B ')}{d.day}</b><small>Work session 6:00 PM, regular meeting right after &middot; City Hall</small><small>{E(status)}</small>{cal_btns(mtg_ics_name(d),council_gcal(d),lab)}</div></li>'''
latest=NEWS[0]['date']
front=[e for e in NEWS if e['date']==latest]
lead=next((e for e in front if e.get('top')),front[0])
more=[e for e in NEWS if e is not lead][:6]
GC='''<section id="game-center" class="gc-sec"><div class="wrap"><div class="gc-head"><h2><svg class="ic" aria-hidden="true" focusable="false"><use href="icons.svg#i-trophy"></use></svg>Hanceville Game Center</h2><p class="big-p">The last game, the next game and any game in progress for Hanceville High and Wallace State. Keep this page open and the scores check for updates every minute.</p></div><div id="gc" class="gc"><p class="gc-load">Loading scores...</p></div><p class="gc-upd" id="gc-upd" aria-live="polite"></p><p class="gc-src">We get scores from official school and college athletics pages, MaxPreps and local news. Live scores show up here once we post them. For play by play, check each school&rsquo;s own pages.</p></div></section>'''
home=head(SEO["index"][0],SEO["index"][1],"index.html",ld({"@context":"https://schema.org","@graph":[ORG,SITE]}))+'\n<body data-page="home">\n'+header('index.html')+f'''
<main id="main">
<section class="city-hero"><div class="wrap">
 <h1>Hanceville City Services</h1>
 <p class="big-p">Find a city department and who to call, see when the City Council meets next, pay a water bill or find a storm shelter. Local news, events and businesses are right below.</p>
</div></section>
<nav class="qlinks" aria-label="Quick links"><ul>
 <li><a href="departments.html"><svg class="ic" aria-hidden="true" focusable="false"><use href="icons.svg#i-phone"></use></svg>Departments &amp; Contacts</a></li>
 <li><a href="council.html"><svg class="ic" aria-hidden="true" focusable="false"><use href="icons.svg#i-landmark"></use></svg>City Council</a></li>
 <li><a href="council.html#meeting_schedule"><svg class="ic" aria-hidden="true" focusable="false"><use href="icons.svg#i-calendar"></use></svg>Council Meetings</a></li>
 <li><a href="https://hancevillewwsb.epayub.com/" target="_blank" rel="noopener noreferrer"><svg class="ic" aria-hidden="true" focusable="false"><use href="icons.svg#i-droplet"></use></svg>Pay Water Bill</a></li>
 <li><a href="departments.html#storm_shelters"><svg class="ic" aria-hidden="true" focusable="false"><use href="icons.svg#i-tornado"></use></svg>Storm Shelters</a></li>
 <li><a href="city.html"><svg class="ic" aria-hidden="true" focusable="false"><use href="icons.svg#i-clipboard-list"></use></svg>All City Services</a></li>
</ul></nav>
<section id="city-hall"><div class="wrap">
 <div class="sec-title"><h2>City Departments</h2><a class="btn" href="departments.html">See every department</a></div>
 <p class="big-p" style="margin-top:8px">Here is who to contact at City Hall and around town. Tap to call, email or get directions.</p>
 <div class="dep-grid">{''.join(dep_card(e,'h3',True) for e in DEPS if e['name'] in HOME_DEPS)}</div>
 <div class="city-next" style="margin-top:22px">
  <div><h3 style="margin:0 0 4px">Next City Council meetings</h3><p style="margin:0">Meetings are at City Hall, 112 Main Street SE, and anyone is welcome.</p><ul class="meetings" style="grid-template-columns:1fr">{''.join(meeting_li(d) for d in MEETINGS[:2])}</ul></div>
  <div class="note" style="margin:0"><h3 style="margin:0 0 6px">Quick city links</h3><ul class="doclist" style="grid-template-columns:1fr"><li><a href="council.html#council_members"><svg class="ic" aria-hidden="true" focusable="false"><use href="icons.svg#i-users"></use></svg>Meet the Mayor and Council</a></li><li><a href="city.html#utilities_and_public_works"><svg class="ic" aria-hidden="true" focusable="false"><use href="icons.svg#i-droplet"></use></svg>Water, power, gas and streets</a></li><li><a href="city.html#parks_library_and_civic_center"><svg class="ic" aria-hidden="true" focusable="false"><use href="icons.svg#i-tree-pine"></use></svg>Parks, library and Civic Center</a></li><li><a href="council.html#agendas_and_minutes"><svg class="ic" aria-hidden="true" focusable="false"><use href="icons.svg#i-file-text"></use></svg>Council agendas and minutes</a></li></ul></div>
 </div>
</div></section>
<section class="front alt-bg" id="news"><div class="wrap">
 <div class="masthead"><h2 class="mh">Hanceville Today</h2><p class="dateline"><time datetime="{latest}">{long_date(latest)}</time> &middot; City news, schools and things to do</p></div>
 <article class="lead-story {CATCLS(lead['category'])}">
  <div class="cat-art" aria-hidden="true">{CI(lead['category'])}</div>
  <div class="ls-body"><p class="kick"><span class="catpill">{E(lead['category'])}</span> <span class="topflag">Top Story</span></p>
  <h3 class="ls-h"><a href="{story_url(lead)}">{E(lead['headline'])}</a></h3>
  <p class="ls-sum">{E(lead['summary'])}</p>
  <p class="when">Published <time datetime="{lead['date']}">{nice_date(lead['date'])}</time></p>
  <p><a class="btn" href="{story_url(lead)}" aria-label="Read the full story: {E(lead['headline'])}">Read the full story</a></p></div>
 </article>
 <h3 class="sec-h">More local news</h3>
 <div class="story-grid">{''.join(story_card(e,'h4') for e in more)}</div>
 <p class="more-news"><a class="btn alt3" href="news.html">See all news and older stories</a></p>
</div></section>
<section id="upcoming" class="band"><div class="wrap"><div class="sec-title"><h2>Hanceville Events</h2><a class="btn" href="events.html">See all events</a></div><p class="big-p" style="margin-top:8px">Here are a few local events coming up soon.</p><div class="grid" id="ev-prev"></div></div></section>
'''+'''<section id="looking"><div class="wrap">
 <h2>Local businesses and more</h2>
 <p class="big-p">Tap a box to find what you need around town.</p>
 <div class="tiles">
  <a class="tile" href="businesses.html"><span class="ti"><svg class="ic" aria-hidden="true" focusable="false"><use href="icons.svg#i-store"></use></svg></span><span><b>Business Directory</b><small>Barbers, mechanics, banks and more</small></span></a>
  <a class="tile" href="eats.html"><span class="ti"><svg class="ic" aria-hidden="true" focusable="false"><use href="icons.svg#i-utensils"></use></svg></span><span><b>Places to Eat</b><small>Local restaurants and specials</small></span></a>
  <a class="tile" href="shops.html"><span class="ti"><svg class="ic" aria-hidden="true" focusable="false"><use href="icons.svg#i-shopping-bag"></use></svg></span><span><b>Hometown Shops</b><small>Downtown stores, makers and markets</small></span></a>
  <a class="tile" href="directory.html"><span class="ti"><svg class="ic" aria-hidden="true" focusable="false"><use href="icons.svg#i-school"></use></svg></span><span><b>Schools &amp; Directory</b><small>Schools, safety and community services</small></span></a>
  <a class="tile" href="nonprofits.html"><span class="ti"><svg class="ic" aria-hidden="true" focusable="false"><use href="icons.svg#i-heart-handshake"></use></svg></span><span><b>Nonprofits</b><small>Food pantries and volunteer groups</small></span></a>
  <a class="tile" href="wallace.html"><span class="ti"><svg class="ic" aria-hidden="true" focusable="false"><use href="icons.svg#i-graduation-cap"></use></svg></span><span><b>Wallace State</b><small>College services and help</small></span></a>
 </div>
</div></section>
'''+GC+'''
<section id="help" class="alt-bg"><div class="wrap">
 <h2>More Resources: state and federal help</h2>
 <p class="big-p">Programs run by the State of Alabama, the federal government and Cullman County agencies. These are not city services, but they can help families and seniors in Hanceville.</p>
 <div class="helpgrid">
  <a href="resources.html#seniors_and_elderly"><svg class="ic" aria-hidden="true" focusable="false"><use href="icons.svg#i-user-round"></use></svg>Seniors</a>
  <a href="resources.html#food_and_snap"><svg class="ic" aria-hidden="true" focusable="false"><use href="icons.svg#i-apple"></use></svg>Food &amp; SNAP</a>
  <a href="resources.html#dhr_services"><svg class="ic" aria-hidden="true" focusable="false"><use href="icons.svg#i-building-2"></use></svg>DHR Services</a>
  <a href="resources.html#child_care"><svg class="ic" aria-hidden="true" focusable="false"><use href="icons.svg#i-baby"></use></svg>Child Care</a>
  <a href="resources.html#federal_programs"><svg class="ic" aria-hidden="true" focusable="false"><use href="icons.svg#i-flag"></use></svg>Federal Programs</a>
  <a href="resources.html"><svg class="ic" aria-hidden="true" focusable="false"><use href="icons.svg#i-clipboard-list"></use></svg>All more resources</a>
 </div>
 <div class="crisis" role="region" aria-label="Emergency numbers"><h3>In an emergency</h3><p>Call 911 if someone is hurt or in danger. For a mental health crisis, call or text 988. Both are free and open 24 hours.</p><div class="acts"><a class="btn" href="tel:911">Call 911</a><a class="btn" href="tel:988">Call 988</a><a class="btn" href="sms:988">Text 988</a></div></div>
</div></section>
'''+signup("signup")+f'''
<section id="contact" class="alt-bg"><div class="wrap"><div class="feature">
 <h2>Contact us</h2>
 <p class="big-p">Got a question, an event to share or a business we should list? We would love to hear from you, and listings are always free.</p>
 <div class="contact-acts"><a class="btn" href="mailto:{EMAIL}?subject=Hanceville%20website"><svg class="ic" aria-hidden="true" focusable="false"><use href="icons.svg#i-mail"></use></svg>Email {EMAIL}</a><a class="btn" href="{FB}" target="_blank" rel="noopener noreferrer"><svg class="ic" aria-hidden="true" focusable="false"><use href="icons.svg#i-thumbs-up"></use></svg>Message us on Facebook</a></div>
 <p class="small-note">Hanceville Entertainment &amp; Shopping is an independent community page. It is not the official Chamber of Commerce and is not run by the City of Hanceville.</p>
</div></div></section>
</main>
'''+FOOT
open('index.html','w').write(home)
PAGES={'events':("Upcoming Events","Explore","Festivals, ballgames, library storytimes, markets and other things to do around Hanceville and Cullman County. Events drop off the list once they are over.",GC),
'eats':("Local Eats","Explore","Hometown restaurants, newer places and daily specials around Hanceville. Fair warning: you might get hungry.",''),
'shops':("Hometown Shops","Explore","Shop local at the stores, makers and markets around Hanceville.",''),
'businesses':("Business Directory","Explore","Restaurants, barbers, car lots, mechanics, banks, vets and more in Hanceville. Search by name or service, or tap a category.",'<label for="biz-q" class="flabel">Search businesses</label><input id="biz-q" class="field" type="search" placeholder="Filter businesses, like oil change or haircut" autocomplete="off"><div class="chips" id="biz-chips" role="group" aria-label="Filter by category"></div>'),
'news':("Local News","Community","Every story we have published, newest first. Tap a headline to read it, with links to the original sources.",'<p class="note">Want to know who serves on the City Council or when it meets next? Visit our <a href="council.html">City Council page</a> for photos, the meeting schedule, agendas and minutes.</p>'),
'nonprofits':("Nonprofits","Community","Local groups that feed neighbors and support families in Hanceville, and how you can pitch in.",''),
'resources':("More Resources: State and Federal Help","More Resources","These programs are run by the State of Alabama, the federal government and Cullman County agencies rather than the City of Hanceville. For city departments, see <a href=\"departments.html\">Departments and Contacts</a>.",'<div class="crisis" role="region" aria-label="Crisis numbers"><h2 class="ch">Need help right now?</h2><p>If you or someone else is in danger, call 911. For a mental health crisis, call or text 988. For domestic violence, call 1&#8209;800&#8209;650&#8209;6522. All are free and open 24 hours.</p><div class="acts"><a class="btn" href="tel:911">Call 911</a><a class="btn" href="tel:988">Call 988</a><a class="btn" href="sms:988">Text 988</a><a class="btn" href="tel:18006506522">DV Hotline</a></div></div><p class="big-p" style="margin-top:18px">Each listing is marked <b>Local</b> (in or serving Cullman County), <b>State</b> (Alabama programs) or <b>Federal</b> (national programs). Tap a button to show only one kind.</p>'),
'city':("City Services","City Hall","City offices, utilities, storm shelters, parks and city boards in Hanceville, with the phone numbers and addresses the City of Hanceville publishes. Tap a button to call, get directions or visit the official page.",'<div class="infogrid"><div class="info"><h2>City Hall</h2><p>112 Main Street SE</p></div><div class="info"><h2>Main phone</h2><p><a href="tel:2563529830">(256) 352-9830</a></p></div><div class="info"><h2>Water and sewer</h2><p><a href="tel:2563529229">(256) 352-9229</a></p></div><div class="info"><h2>Emergency</h2><p><a href="tel:911">Call 911</a></p></div></div><p class="official-src">Source: the City of Hanceville&rsquo;s official website, <a href="https://www.cityofhanceville.net/" target="_blank" rel="noopener noreferrer">cityofhanceville.net</a>, checked Oct. 17, 2026. This is an independent community guide and is not run by the city.</p>'),
'directory':("Community Directory","Community","Public schools, city offices and community services in one place. Tap a phone number to call.",''),
'wallace':("Wallace State Services","Wallace State","Wallace State Community College is right here in Hanceville, and it offers plenty of help for students and neighbors. Here is who to call.",'<p class="sch-legend">This page uses Wallace State&rsquo;s official college colors: <span class="sw" style="background:#00294D" aria-hidden="true"></span> blue and <span class="sw" style="background:#F68026" aria-hidden="true"></span> orange.</p>'),
'fun':("A Little Fun","Fun","Fun facts, local landmarks and a few sweet tea jokes. Pour yourself a glass.",'')}
FILTER_HINT={'city':'water or shelter','events':'football or storytime','eats':'pizza or coffee','shops':'flowers or vintage','news':'council or roads','nonprofits':'food or volunteer','resources':'Medicare or SNAP','directory':'school or water','wallace':'tutoring or financial aid','fun':'tea or history'}
for k,(t,sec,d,extra) in PAGES.items():
  after=f'<p><strong>Is your Hanceville business missing?</strong> We would love to add you. <a href="{FB}" target="_blank" rel="noopener noreferrer">Message our Facebook Page</a> or email {MAIL} with your business name, address and phone number.</p>' if k=='businesses' else ''
  crumb={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":BASE},{"@type":"ListItem","position":2,"name":t,"item":BASE+k+".html"}]}
  extra_ld=ld(crumb)
  _data=_json.load(open(k+'.json'))
  _bnames={x['name'] for x in _json.load(open('businesses.json'))}
  if k=='businesses':_x=biz_ld(_data,'businesses.html')
  elif k in('eats','shops'):_x=biz_ld([x for x in _data if x['name'] not in _bnames and 'Festival' not in x['name'] and 'Market' not in x['name']],k+'.html')
  elif k=='directory':_x=gov_ld(_data,'directory.html',GOV_DIR)
  elif k=='city':_x=gov_ld(_data,'city.html',{e['name']:("Cullman County" if 'County' in e.get('type','') else "Cullman Electric Cooperative" if 'Electric' in e['name'] else "Cullman Jefferson Gas" if 'Gas' in e['name'] else "Hanceville Water and Sewer Board" if 'Water' in e['name'] else "Cullman County 911" if e['name'].startswith('Emergency') else "City of Hanceville") for e in _data})
  elif k=='resources':_x=gov_ld(_data,'resources.html',GOV_RES)
  else:_x=None
  if _x:extra_ld+=ld(_x)
  if k=='events':
    evs=[]
    for e in _json.load(open('events.json')):
      if (e.get('end') or e['start'])<TODAY: continue
      loc={"@type":"Place","name":e.get('venue') or e['town']+", Alabama","address":{"@type":"PostalAddress","addressLocality":e['town'],"addressRegion":"AL","addressCountry":"US"}}
      ev={"@type":"Event","name":e['name'],"startDate":e['start'],"description":e['summary'],"eventStatus":"https://schema.org/EventScheduled","eventAttendanceMode":"https://schema.org/OfflineEventAttendanceMode","location":loc,"organizer":{"@type":"Organization","name":e['host']},"image":[BASE+"og-image.jpg"]}
      if e.get('end') and e['end']!=e['start']: ev["endDate"]=e['end']
      if e.get('url'): ev["url"]=e['url']
      if e.get('cost') and 'free' in e['cost'].lower(): ev["isAccessibleForFree"]=True
      evs.append(ev)
    extra_ld+=ld({"@context":"https://schema.org","@graph":evs})
  FILT=f'<div class="filters"><label class="flabel" for="f-q">Search this page</label><input id="f-q" class="field" type="search" placeholder="Type a word, like {FILTER_HINT.get(k,"name")}" autocomplete="off"><div class="chips" id="f-chips" role="group" aria-label="Filter {t}"></div></div>'
  html=head(SEO[k][0],SEO[k][1],k+'.html',extra_ld)+f'\n<body data-page="{k}"'+(' data-school="wallace"' if k=='wallace' else '')+'>\n'+header(k+'.html')+f'''
<main id="main"><div class="crumbbar"><div class="wrap"><nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a> &rsaquo; {sec} &rsaquo; {t}</nav></div></div><div class="page-head"><div class="wrap"><h1>{t}</h1><p>{d}</p></div></div>
<section style="padding-top:20px"><div class="wrap">
{extra}
{FILT if k!='businesses' else ''}
<div id="list"></div><p id="status" aria-live="polite">Loading...</p>
{after}
</div></section>
{signup('signup') if k=='events' else ''}
{FEAT if k in ('businesses','shops','eats') else ''}
</main>
'''+FOOT
  open(k+'.html','w').write(html)

# ---------- City Council page ----------
def _srcs(m):
  return '<details class="msrc"><summary>Sources for '+E(m['name'])+'</summary><ul>'+''.join(f'<li><a href="{E(u)}" target="_blank" rel="noopener noreferrer">{E(t)}</a></li>' for t,u in m.get('sources',[]))+'</ul></details>'
def member_card(m):
  ph=m['photo'];alt=f"Official portrait of Hanceville City Council member {m['name']}, {m['place']}"
  return f"""<article class="member" id="{_slug(m['name'])}"><picture><source type="image/webp" srcset="img/council/{ph}-600.webp 600w, img/council/{ph}-1200.webp 1200w" sizes="(min-width:1000px) 340px, (min-width:620px) 45vw, 92vw"><img src="img/council/{ph}-600.jpg" width="600" height="400" alt="{E(alt)}" loading="lazy" decoding="async"></picture><div class="mb"><span class="place">{E(m['place'])}</span><h3>{E(m['name'])}</h3><p class="role">{E(m['role'])}</p><p class="mterm">{E(m.get('term',''))}</p><p class="mbio">{E(m['summary'])}</p><p class="mcontact"><b>Contact:</b> through City Hall at <a href="tel:2563529830">(256) 352-9830</a>, 112 Main Street SE. The city does not publish a separate phone or email for this seat.</p><div class="acts"><a class="btn" href="tel:2563529830" aria-label="Call City Hall to reach {E(m['name'])}"><svg class="ic" aria-hidden="true" focusable="false"><use href="icons.svg#i-phone"></use></svg>Call City Hall</a><a class="btn alt2" href="{E(CH_MAP)}" target="_blank" rel="noopener noreferrer" aria-label="Directions to City Hall"><svg class="ic" aria-hidden="true" focusable="false"><use href="icons.svg#i-navigation"></use></svg>Directions</a></div>{_srcs(m)}</div></article>"""
MEM=[m for m in COUNCIL if m.get('photo')]
MAYOR=next(m for m in COUNCIL if m['role']=='Mayor')
c_ld={"@context":"https://schema.org","@graph":[
 {"@type":"GovernmentOrganization","@id":BASE+"council.html#council","name":"Hanceville City Council","url":COUNCIL_URL,"description":"The legislative body of the City of Hanceville, Alabama: the Mayor and five council members, each elected to a four year term.","address":{"@type":"PostalAddress","streetAddress":"112 Main Street SE","addressLocality":"Hanceville","addressRegion":"AL","postalCode":"35077","addressCountry":"US"},"telephone":"+1-256-352-9830","areaServed":{"@type":"City","name":"Hanceville, Alabama"},"parentOrganization":{"@type":"GovernmentOrganization","name":"City of Hanceville","url":"https://www.cityofhanceville.net/"},
  "member":[{"@type":"OrganizationRole","roleName":m['place']+(", "+m['role'] if m['role']!='Councilor' else ", Council Member"),"member":{"@type":"Person","name":m['name'],"description":m['summary'],"jobTitle":"Hanceville City Council, "+m['place'],"image":BASE+"img/council/"+m['photo']+"-600.jpg"}} for m in MEM]+[{"@type":"OrganizationRole","roleName":"Mayor","member":{"@type":"Person","name":MAYOR['name'],"jobTitle":"Mayor of Hanceville"}}]},
 {"@type":"WebPage","@id":BASE+"council.html","url":BASE+"council.html","name":"Hanceville City Council","isBasedOn":COUNCIL_URL,"about":{"@id":BASE+"council.html#council"},"publisher":{"@id":BASE+"#org"}},
 {"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":BASE},{"@type":"ListItem","position":2,"name":"City Council","item":BASE+"council.html"}]}]+
 [{"@type":"Event","name":"Hanceville City Council Meeting","startDate":_dt.datetime(d.year,d.month,d.day,18,0,tzinfo=_ZI("America/Chicago")).isoformat(),"endDate":_dt.datetime(d.year,d.month,d.day,19,30,tzinfo=_ZI("America/Chicago")).isoformat(),"eventStatus":"https://schema.org/EventScheduled","eventAttendanceMode":"https://schema.org/OfflineEventAttendanceMode","isAccessibleForFree":True,"description":"Work session at 6:00 PM followed by the regular City Council meeting. Open to the public.","location":{"@type":"Place","name":"Hanceville City Hall","address":{"@type":"PostalAddress","streetAddress":"112 Main Street SE","addressLocality":"Hanceville","addressRegion":"AL","postalCode":"35077","addressCountry":"US"}},"organizer":{"@id":BASE+"council.html#council"},"url":COUNCIL_URL} for d in MEETINGS]}
AG="https://www.cityofhanceville.net/documents/council---meeting-agendas/2026/25520828"
MN="https://www.cityofhanceville.net/documents/council---meeting-minutes/2026/25520797"
council_html=head(SEO['council'][0],SEO['council'][1],'council.html',ld(c_ld))+'\n<body data-page="council">\n'+header('council.html')+f"""
<main id="main"><div class="crumbbar"><div class="wrap"><nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a> &rsaquo; City Hall &rsaquo; City Council</nav></div></div>
<div class="page-head"><div class="wrap"><h1>Hanceville City Council</h1><p>Hanceville is run by a Mayor and five City Council members. Each one is elected to a four year term, and together they make the city&rsquo;s laws, set its budget and decide where Hanceville goes next.</p></div></div>
<section class="page-sec" id="council_members"><div class="wrap">
 <h2>Council Members</h2>
 <p class="lede">Each council seat is called a Place. Here is who holds each seat, as listed by the City of Hanceville.</p>
 <div class="member-grid">{''.join(member_card(m) for m in MEM)}</div>
 <div class="mayor-card" id="nolan_bradford"><div><span class="place" style="background:#0b0b0f;color:#fff;border-radius:8px;padding:2px 10px;font-weight:800;font-size:.9rem;text-transform:uppercase;letter-spacing:.4px">Mayor</span><h3 style="margin-top:8px">Mayor {E(MAYOR['name'])}</h3><p class="mterm">{E(MAYOR.get('term',''))}</p><p>{E(MAYOR['summary'])}</p><p class="mcontact"><b>Mayor&rsquo;s Office:</b> <a href="tel:2563529811">(256) 352-9811</a> &middot; <a href="mailto:mayor@cityofhanceville.net">mayor@cityofhanceville.net</a> &middot; 112 Main Street SE</p>{_srcs(MAYOR)}</div><div class="acts"><a class="btn" href="tel:2563529811" aria-label="Call the Mayor&rsquo;s Office"><svg class="ic" aria-hidden="true" focusable="false"><use href="icons.svg#i-phone"></use></svg>Call the Mayor&rsquo;s Office</a><a class="btn alt3" href="mailto:mayor@cityofhanceville.net" aria-label="Email the Mayor&rsquo;s Office"><svg class="ic" aria-hidden="true" focusable="false"><use href="icons.svg#i-mail"></use></svg>Email</a><a class="btn alt2" href="{E(CH_MAP)}" target="_blank" rel="noopener noreferrer" aria-label="Directions to the Mayor&rsquo;s Office"><svg class="ic" aria-hidden="true" focusable="false"><use href="icons.svg#i-navigation"></use></svg>Directions</a></div></div>
 <p class="official-src">Names, seats, titles and photos come from the City of Hanceville&rsquo;s <a href="{COUNCIL_URL}" target="_blank" rel="noopener noreferrer">official City Council page</a>, checked Oct. 17, 2026. Short profiles draw only on the city&rsquo;s pages and reporting by The Cullman Times, The Cullman Tribune and ABC 33/40, with every source listed under each person. The city does not list individual contact details for council members, so please reach them through City Hall.</p>
</div></section>
<section class="page-sec alt-bg" id="meeting_schedule"><div class="wrap">
 <h2>Meeting Schedule</h2>
 <p class="lede">The council meets on the <b>second and fourth Thursday of every month</b> at Hanceville City Hall. A work session starts at 6:00 PM, and the regular meeting follows right after. Every regular meeting is open to the public, and there is time for public comments.</p>
 <div class="infogrid"><div class="info"><h3>Where</h3><p>Hanceville City Hall<br>112 Main Street SE</p></div><div class="info"><h3>When</h3><p>2nd and 4th Thursday<br>6:00 PM</p></div><div class="info"><h3>Who can come</h3><p>Everyone. It&rsquo;s free.</p></div><div class="info"><h3>Can&rsquo;t make it?</h3><p><a href="https://www.youtube.com/@OfficialCityofHancevilleAL" target="_blank" rel="noopener noreferrer">Watch on YouTube</a></p></div></div>
 <div class="acts" style="margin:6px 0 4px"><a class="btn alt2" href="{CH_MAP}" target="_blank" rel="noopener noreferrer" aria-label="Directions to Hanceville City Hall"><svg class="ic" aria-hidden="true" focusable="false"><use href="icons.svg#i-navigation"></use></svg>Directions to City Hall</a><a class="btn alt3" href="https://www.cityofhanceville.net/events" target="_blank" rel="noopener noreferrer">City meeting calendar</a></div>
 <h3 style="margin:22px 0 0">Next regular meetings</h3>
 <ul class="meetings">{''.join(meeting_li(d) for d in MEETINGS)}</ul>
 <p class="note">Dates are worked out from the council&rsquo;s regular schedule. The city sometimes moves or cancels a meeting, especially around holidays, and posts special called meetings with short notice. We check the city&rsquo;s calendar and agendas every hour, but please confirm on the <a href="https://www.cityofhanceville.net/events" target="_blank" rel="noopener noreferrer">city calendar</a> before you go.</p>
</div></section>
<section class="page-sec" id="agendas_and_minutes"><div class="wrap">
 <h2>Agendas and Minutes</h2>
 <p class="lede">The city posts each agenda before the meeting and the minutes afterward. Both are drafts until the council approves them, so they can still change.</p>
 <ul class="doclist"><li><a href="{AG}" target="_blank" rel="noopener noreferrer"><svg class="ic" aria-hidden="true" focusable="false"><use href="icons.svg#i-file-text"></use></svg>2026 council agendas</a></li><li><a href="{MN}" target="_blank" rel="noopener noreferrer"><svg class="ic" aria-hidden="true" focusable="false"><use href="icons.svg#i-list-checks"></use></svg>2026 council minutes</a></li><li><a href="https://www.cityofhanceville.net/news" target="_blank" rel="noopener noreferrer"><svg class="ic" aria-hidden="true" focusable="false"><use href="icons.svg#i-video"></use></svg>Meeting records and videos</a></li><li><a href="https://www.cityofhanceville.net/documents/ordinances/25520974" target="_blank" rel="noopener noreferrer"><svg class="ic" aria-hidden="true" focusable="false"><use href="icons.svg#i-scale"></use></svg>City ordinances</a></li><li><a href="https://www.cityofhanceville.net/documents/resolutions/25526621" target="_blank" rel="noopener noreferrer"><svg class="ic" aria-hidden="true" focusable="false"><use href="icons.svg#i-scroll-text"></use></svg>Council resolutions</a></li><li><a href="https://www.cityofhanceville.net/documents/budget/25526038" target="_blank" rel="noopener noreferrer"><svg class="ic" aria-hidden="true" focusable="false"><use href="icons.svg#i-piggy-bank"></use></svg>City budgets</a></li></ul>
 <p>Want the short version? Our <a href="news.html#city_hall">City Hall news</a> sums up what the council decides at each meeting, with links to the sources.</p>
</div></section>
<section class="page-sec alt-bg" id="what_the_council_does"><div class="wrap">
 <h2>What the Council Does</h2>
 <p class="lede">The council is the city&rsquo;s lawmaking body. It works with the Mayor, city departments and residents to keep city services running and plan for the future. Its main jobs are to:</p>
 <ul class="duties"><li>Pass city ordinances, resolutions and policies</li><li>Review and approve the city budget each year</li><li>Keep watch over how city money and property are used</li><li>Set up and support city services and departments</li><li>Plan road, drainage and other improvements, along with future growth</li><li>Appoint people to some city boards and offices, as state law allows</li><li>Speak up for the needs and concerns of Hanceville residents</li></ul>
</div></section>
<section class="page-sec" id="contact_city_hall"><div class="wrap">
 <h2>Contact City Hall</h2>
 <p class="lede">To reach the council or ask how to get on an agenda, call or visit City Hall.</p>
 <div class="infogrid"><div class="info"><h3>Address</h3><p>112 Main Street SE<br>Hanceville, AL 35077</p></div><div class="info"><h3>City Hall</h3><p><a href="tel:2563529830">(256) 352-9830</a></p></div><div class="info"><h3>Mayor&rsquo;s Office</h3><p><a href="tel:2563529811">(256) 352-9811</a></p></div><div class="info"><h3>Official website</h3><p><a href="https://www.cityofhanceville.net/" target="_blank" rel="noopener noreferrer">cityofhanceville.net</a></p></div></div>
 <div class="acts"><a class="btn" href="tel:2563529830" aria-label="Call Hanceville City Hall"><svg class="ic" aria-hidden="true" focusable="false"><use href="icons.svg#i-phone"></use></svg>Call City Hall</a><a class="btn alt2" href="{CH_MAP}" target="_blank" rel="noopener noreferrer" aria-label="Directions to Hanceville City Hall"><svg class="ic" aria-hidden="true" focusable="false"><use href="icons.svg#i-navigation"></use></svg>Directions</a><a class="btn alt3" href="{COUNCIL_URL}" target="_blank" rel="noopener noreferrer"><svg class="ic" aria-hidden="true" focusable="false"><use href="icons.svg#i-globe"></use></svg>Official council page</a></div>
 <p class="small-note" style="color:var(--muted)">Hanceville Entertainment &amp; Shopping is an independent community guide. It is not run by or affiliated with the City of Hanceville.</p>
</div></section>
</main>
"""+FOOT
open('council.html','w').write(council_html)

# ---------- Departments page ----------
d_ld={"@context":"https://schema.org","@graph":[{"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":BASE},{"@type":"ListItem","position":2,"name":"Departments and Contacts","item":BASE+"departments.html"}]}]+[dict({"@type":"GovernmentOrganization","@id":BASE+"departments.html#"+_slug(e['name']),"name":e['name'],"description":e['summary'],"areaServed":{"@type":"City","name":"Hanceville, Alabama"}},**({"telephone":e['phone']} if e.get('phone') else {}),**({"email":e['email']} if e.get('email') else {}),**({"address":_addr(e['address'])} if _addr(e.get('address')) else {}),**({"url":e['website']} if e.get('website') else {})) for e in DEPS]}
dep_secs=''.join(f'<section class="page-sec{" alt-bg" if n%2 else ""}" id="{_slug(g)}"><div class="wrap"><h2>{E(g)}</h2><div class="dep-grid">'+''.join(dep_card(e) for e in DEPS if e['group']==g)+'</div></div></section>' for n,g in enumerate(DEP_ORDER))
dep_html=head(SEO['departments'][0],SEO['departments'][1],'departments.html',ld(d_ld))+'\n<body data-page="departments">\n'+header('departments.html')+f"""
<main id="main"><div class="crumbbar"><div class="wrap"><nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a> &rsaquo; City Services &rsaquo; Departments and Contacts</nav></div></div>
<div class="page-head"><div class="wrap"><h1>City Departments and Contacts</h1><p>Every City of Hanceville department in one place, with the person to ask for, their title, and the phone, email, address and hours the city publishes. Tap a button to call, email or get directions.</p></div></div>
<section class="page-sec" style="padding-bottom:0"><div class="wrap">
<div class="infogrid"><div class="info"><h2>City Hall</h2><p>112 Main Street SE</p></div><div class="info"><h2>Main phone</h2><p><a href="tel:2563529830">(256) 352-9830</a></p></div><div class="info"><h2>Fax</h2><p>(256) 352-1200</p></div><div class="info"><h2>Emergency</h2><p><a href="tel:911">Call 911</a></p></div></div>
<p class="note">Not sure who to call? Start with City Hall at <a href="tel:2563529830">(256) 352-9830</a> and the staff will point you to the right person.</p>
</div></section>
{dep_secs}
<section class="page-sec"><div class="wrap"><p class="official-src">Names, titles, phone numbers, emails, addresses and hours come from the City of Hanceville&rsquo;s <a href="https://www.cityofhanceville.net/o/coh/page/city-departments" target="_blank" rel="noopener noreferrer">City Departments page</a>, <a href="https://www.cityofhanceville.net/staff" target="_blank" rel="noopener noreferrer">staff directory</a> and each department page, checked Oct. 17, 2026, and cross checked with recent local news. Where the city&rsquo;s own pages disagree, we list the number the department itself publishes. See something out of date? Email <a href="mailto:{EMAIL}?subject=Department%20correction">{EMAIL}</a>.</p><p class="small-note" style="color:var(--muted)">Hanceville Entertainment &amp; Shopping is an independent community guide. It is not run by or affiliated with the City of Hanceville.</p></div></section>
</main>
"""+FOOT
open('departments.html','w').write(dep_html)
def story_page(e):
  url=BASE+story_url(e)
  art_ld={"@context":"https://schema.org","@graph":[{"@type":"NewsArticle","headline":e['headline'][:110],"description":e['summary'],"datePublished":e['date'],"dateModified":e.get('updated',e['date']),"articleSection":e['category'],"inLanguage":"en-US","mainEntityOfPage":url,"url":url,"image":[BASE+"og-image.jpg"],"author":{"@id":BASE+"#org"},"publisher":{"@id":BASE+"#org"},"isBasedOn":[x['url'] for x in e['sources']]},ORG,
   {"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":BASE},{"@type":"ListItem","position":2,"name":"Local News","item":BASE+"news.html"},{"@type":"ListItem","position":3,"name":e['headline'],"item":url}]}]}
  title=E(e['headline'])+" | Hanceville, AL News"
  rel=[x for x in NEWS if x is not e][:3]
  body=''.join(f'<p>{E(x)}</p>' for x in e['body'])
  srcs=''.join(f'<li><a href="{E(x["url"])}" target="_blank" rel="noopener noreferrer">{E(x["name"])}</a></li>' for x in e['sources'])
  corr=_up.quote('Correction: '+e['headline'])
  h=head(title,E(e['summary']),story_url(e),ld(art_ld)).replace('<meta property="og:type" content="website">','<meta property="og:type" content="article">')+'\n<body data-page="story"'+((' data-school="'+school_of(e['headline'],e['summary'])+'"') if school_of(e['headline'],e['summary']) else '')+'>\n'+header('news.html')+f'''
<main id="main"><article class="story {CATCLS(e['category'])}">
<div class="crumbbar"><div class="wrap"><nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a> &rsaquo; <a href="news.html">Local News</a> &rsaquo; {E(e['category'])}</nav></div></div><div class="page-head story-head"><div class="wrap">
<div class="sh-row"><div class="cat-art" aria-hidden="true">{CI(e['category'])}</div><div><p class="kick"><span class="catpill">{E(e['category'])}</span></p><h1>{E(e['headline'])}</h1></div></div>
<p class="story-meta">Published <time datetime="{e['date']}">{long_date(e['date'])}</time> by Hanceville Today</p></div></div>
<div class="wrap story-wrap">
<p class="story-lead">{E(e['summary'])}</p>
<div class="story-body">{body}</div>
{'<p class="note">Meet the council members and see upcoming meetings on our <a href="council.html">City Council page</a>.</p>' if e['category']=='City Hall' else ''}<section class="sources" aria-labelledby="src-h"><h2 id="src-h">Sources</h2><p>We wrote this story ourselves and checked each fact against these sources. Short quotes belong to the people and outlets named.</p><ul>{srcs}</ul></section>
<p class="story-note">See something we should fix? Email <a href="mailto:{EMAIL}?subject={corr}">{EMAIL}</a>.</p>
<p class="story-acts"><a class="btn alt3" href="news.html">Back to all news</a> <a class="btn alt3" href="index.html">Today&rsquo;s front page</a></p>
</div></article>
<section class="alt-bg"><div class="wrap"><h2>More local news</h2><div class="story-grid">{''.join(story_card(x) for x in rel)}</div></div></section>
</main>
'''+FOOT
  return h
for f in os.listdir('.'):
  if f.startswith('story-') and f.endswith('.html'):os.remove(f)
for e in NEWS:
  assert _re.fullmatch(r'[a-z0-9-]+',e['id'])
  open(story_url(e),'w').write(story_page(e))
print('built')
open('robots.txt','w').write("User-agent: *\nAllow: /\n\nSitemap: "+BASE+"sitemap.xml\n")
sm=['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for k in PAGE_ORDER:
  sm.append("  <url><loc>%s</loc><lastmod>%s</lastmod><changefreq>%s</changefreq><priority>%s</priority></url>"%(BASE+('' if k=='index' else k+'.html'),TODAY,'daily' if k in('index','events','council') else 'weekly','1.0' if k=='index' else '0.8'))
for e in NEWS:sm.append("  <url><loc>%s</loc><lastmod>%s</lastmod><changefreq>monthly</changefreq><priority>0.6</priority></url>"%(BASE+story_url(e),e.get('updated',e['date'])))
sm.append('</urlset>')
open('sitemap.xml','w').write("\n".join(sm)+"\n")
open(INDEXNOW_KEY+'.txt','w').write(INDEXNOW_KEY)
# Google Search Console verification: never delete, never list in sitemap
for GSC_FILE in ('google5b15f6377dd49d2a.html','google3d41a60ee1e55960.html'):
  open(GSC_FILE,'w').write('google-site-verification: '+GSC_FILE)
print('seo files written')
import re as _re
def _slug(x):return _re.sub(r' +','_',_re.sub(r'[^a-z0-9]+',' ',x.lower().replace('&','and')).strip())
def _t(x):
  m=_re.match(r'\s*(\d{1,2}):(\d{2})\s*([AP]M)',x or '',_re.I)
  if not m:return None
  h=int(m.group(1))%12+(12 if m.group(3).upper()=='PM' else 0);return h,int(m.group(2))
def _esc(x):return x.replace('\\','\\\\').replace(';','\\;').replace(',','\\,').replace('\n','\\n')
os.makedirs('ics',exist_ok=True)
for f in os.listdir('ics'):os.remove('ics/'+f)
TZ="BEGIN:VTIMEZONE\r\nTZID:America/Chicago\r\nBEGIN:DAYLIGHT\r\nTZOFFSETFROM:-0600\r\nTZOFFSETTO:-0500\r\nTZNAME:CDT\r\nDTSTART:19700308T020000\r\nRRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=2SU\r\nEND:DAYLIGHT\r\nBEGIN:STANDARD\r\nTZOFFSETFROM:-0500\r\nTZOFFSETTO:-0600\r\nTZNAME:CST\r\nDTSTART:19701101T020000\r\nRRULE:FREQ=YEARLY;BYMONTH=11;BYDAY=1SU\r\nEND:STANDARD\r\nEND:VTIMEZONE\r\n"
nics=0;CAL={}
def _fold(l):
  b=l.encode();out=[]
  while len(b)>73:
    cut=73
    while (b[cut]&0xC0)==0x80:cut-=1
    out.append(b[:cut].decode());b=b[cut:]
  out.append(b.decode());return '\r\n '.join(out)
def make_ics(path,uid,summary,start,end,loc,desc,url=None,prod='Events'):
  global nics
  if isinstance(start,_dt.datetime):when=f"DTSTART;TZID=America/Chicago:{start.strftime('%Y%m%dT%H%M%S')}\r\nDTEND;TZID=America/Chicago:{end.strftime('%Y%m%dT%H%M%S')}\r\n"
  else:when=f"DTSTART;VALUE=DATE:{start.strftime('%Y%m%d')}\r\nDTEND;VALUE=DATE:{end.strftime('%Y%m%d')}\r\n"
  ics=("BEGIN:VCALENDAR\r\nVERSION:2.0\r\nPRODID:-//Hanceville Entertainment and Shopping//"+prod+"//EN\r\nCALSCALE:GREGORIAN\r\nMETHOD:PUBLISH\r\n"+TZ+"BEGIN:VEVENT\r\n"
       f"UID:{uid}@hanceville-entertainment-shopping\r\nDTSTAMP:{TODAY.replace('-','')}T120000Z\r\n"+when+
       f"SUMMARY:{_esc(summary)}\r\nLOCATION:{_esc(loc)}\r\nDESCRIPTION:{_esc(desc)}\r\n"+(f"URL:{url}\r\n" if url else '')+"END:VEVENT\r\nEND:VCALENDAR\r\n")
  ics='\r\n'.join(_fold(l) for l in ics.split('\r\n'))
  open(path,'w',newline='').write(ics);nics+=1
  g=gcal(summary,start,end,desc,loc);CAL[path.split('/')[-1]]=g;return g
for e in _json.load(open('events.json')):
  d0=_dt.date.fromisoformat(e['start']);end=e.get('end') or e['start'];st=_t(e.get('time'))
  loc=((e.get('venue') or '').replace(' (away game)','')+', '+e['town']+', AL').lstrip(', ')
  if st and end==e['start']:
    m2=_re.search(r'to\s+(\d{1,2}:\d{2}\s*[AP]M)',e.get('time',''),_re.I);et=_t(m2.group(1)) if m2 else ((st[0]+2)%24,st[1])
    if et<=st: et=(23,59)
    a=_dt.datetime(d0.year,d0.month,d0.day,*st);b=_dt.datetime(d0.year,d0.month,d0.day,*et)
  else:
    a=d0;b=_dt.date.fromisoformat(end)+_dt.timedelta(days=1)
  desc=e['summary']+(' Time: '+e['time']+'.' if e.get('time') else '')+(' '+e['url'] if e.get('url') else '')
  make_ics(f"ics/{_slug(e['name'])}_{e['start']}.ics",f"{_slug(e['name'])}-{e['start'].replace('-','')}",e['name'],a,b,loc,desc,e.get('url'))
for d in MEETINGS:
  hol=_holiday(d)
  desc="Work session at 6:00 PM, followed by the regular Hanceville City Council meeting. Open to the public."+(" This date falls on "+hol+", so check the city calendar for changes." if hol else "")+" "+COUNCIL_URL
  make_ics(mtg_ics_name(d),f"hanceville-city-council-{d.isoformat().replace('-','')}","Hanceville City Council Meeting",_dt.datetime(d.year,d.month,d.day,18,0),_dt.datetime(d.year,d.month,d.day,19,30),'Hanceville City Hall, 112 Main Street SE, Hanceville, AL 35077',desc,COUNCIL_URL,'Council')
for (bk,bname,loc,desc,url),d in BOARD_NEXT:
  make_ics(board_ics_name(bk,d),f"hanceville-{bk}-{d.isoformat().replace('-','')}",bname,_dt.datetime(d.year,d.month,d.day,18,0),_dt.datetime(d.year,d.month,d.day,19,0),loc,desc,url,'Boards')
open('ics/cal.json','w').write(_json.dumps(CAL,separators=(',',':')))
print('ics files',nics)
exec(open(os.path.join(HERE,'build_extra.py')).read())

# ---------- apply the build ----------
def _tree(root):
  out={}
  for d,ds,fs in os.walk(root):
    ds[:]=[x for x in ds if x not in('.git','node_modules')]
    for f in fs:
      p=os.path.join(d,f);out[os.path.relpath(p,root)]=p
  return out
def _same(a,b):
  with open(a,'rb') as x,open(b,'rb') as y:return x.read()==y.read()
_old=_tree(SITE_DIR);_new=_tree(WORK)
_changed=sorted(r for r in _new if r in _old and not _same(_old[r],_new[r]))
_added=sorted(r for r in _new if r not in _old)
_gone=sorted(r for r in _old if r not in _new)
print('build result vs %s: %d files differ, %d new, %d would be deleted'%(SITE_DIR,len(_changed),len(_added),len(_gone)))
if OUT_DIR:
  print('Full build written to',OUT_DIR,'(source untouched). Compare with:  diff -rq %s %s'%(SITE_DIR,OUT_DIR))
else:
  _applied=[];_skipped=[]
  for r in _changed:
    if _ARGS.force or not _protected(r):
      shutil.copy2(_new[r],_old[r]);_applied.append(r)
    else:_skipped.append(r)
  for r in _added:
    if _ARGS.force:
      os.makedirs(os.path.dirname(os.path.join(SITE_DIR,r)) or '.',exist_ok=True);shutil.copy2(_new[r],os.path.join(SITE_DIR,r));_applied.append(r)
    else:_skipped.append(r+' (new)')
  if _ARGS.force:
    for r in _gone:os.remove(_old[r])
  print('Applied %d file(s) in place, skipped %d (hands-off, hand maintained or new). Nothing deleted%s.'%(len(_applied),len(_skipped),' (--force: deleted %d)'%len(_gone) if _ARGS.force else ''))
  for r in _applied:print('  applied',r)
  if _skipped:print('  skipped (use --out-dir DIR to inspect them): %d, first 15: %s'%(len(_skipped),', '.join(_skipped[:15])))
