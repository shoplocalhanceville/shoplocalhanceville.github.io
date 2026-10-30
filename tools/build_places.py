#!/usr/bin/env python3
"""Build one full page per listing (place-<slug>.html), one hub per category
(category-<slug>.html) and an A to Z hub (places.html) from the site's data.

Data sources, merged by slug (later sources fill blanks, never overwrite):
  1. the per-section JSON files (businesses.json, shops.json, eats.json, ...)
  2. window.SLH_LISTINGS inside index.html (the homepage directory)
Rerun after any data change:  python3 tools/build_places.py
Nothing here invents facts. Each section only appears when its data exists."""
import json,re,os,html,datetime,urllib.parse,glob,subprocess
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
BASE='https://shoplocalhanceville.github.io/'
E=lambda x:html.escape(str(x),quote=True)
def slug(s):return re.sub(r'^-|-$','',re.sub(r'[^a-z0-9]+','-',(s or '').lower()))
SKIP_CATS={'Fun Facts','Sweet Tea Jokes','Social Media'}  # keep in sync with the list in index.html JS
KINDS=[('businesses','category','Business Directory'),('shops','group','Hometown Shops'),('eats','group','Local Eats'),
 ('nonprofits','group','Nonprofits'),('city','group','City Services'),('departments','group','Departments & Contacts'),
 ('directory','group','Community Directory'),('resources','group','More Resources'),('wallace','group','Wallace State Services'),('council','group','City Council')]
P={}
def add(r,kind,label,catkey):
  n=(r.get('name') or '').strip()
  if not n:return
  cat=r.get(catkey) or r.get('category') or 'Other'
  if kind=='index' and cat in SKIP_CATS:return
  s=slug(n); x=P.setdefault(s,{'name':n,'slug':s,'kinds':[]})
  if (kind,label) not in x['kinds']:x['kinds'].append((kind,label))
  m={'category':cat,'description':r.get('summary') or r.get('description'),'address':r.get('address'),'phone':r.get('phone'),
     'email':r.get('email'),'website':r.get('website') or r.get('link'),'facebook':r.get('facebook'),'hours':r.get('hours'),
     'hours_source':r.get('hours_source'),'source':r.get('source') or ((r.get('sources') or [None])[0] if isinstance(r.get('sources'),list) else None),
     'logo':r.get('logo'),'photo':r.get('photo'),'service':r.get('service') or r.get('type') or r.get('role') or r.get('title'),
     'contact':r.get('contact'),'who':r.get('who'),'how':r.get('how'),'tags':r.get('tags'),'verified':r.get('verified'),'term':r.get('term')}
  for k,v in m.items():
    if isinstance(v,dict):v=v.get('url')
    if v and not x.get(k):x[k]=v
for kind,ck,label in KINDS:
  for r in json.load(open(kind+'.json')):add(r,kind,label,ck)
idx=open('index.html').read()
mm=re.search(r'window\.SLH_LISTINGS = (\[.*?\]);\n',idx,re.S)
for r in json.loads(mm.group(1)) if mm else []:add(r,'index','Home Directory','category')
for x in P.values():
  w=x.get('website') or ''
  if 'facebook.com' in w and not x.get('facebook'):x['facebook']=w
  if x.get('logo') and not re.match(r'^(logos/[a-z0-9-]+\.webp|img/home/[0-9a-f]+(-w)?\.(webp|svg))$',x['logo']):x['logo']=None
  ph=x.get('photo')
  if ph and re.match(r'^[a-z0-9-]+$',ph) and os.path.exists(f'img/council/{ph}-600.webp'):x['photo']=f'img/council/{ph}-600.webp'
  elif ph and not os.path.exists(ph):x['photo']=None
  if x.get('website') and not re.match(r'^https?://',x['website']):x['website']=None
CATS={}
for x in sorted(P.values(),key=lambda x:x['name'].lower()):CATS.setdefault(x['category'],[]).append(x)
def street(a):
  m=re.match(r'^\s*\d+\s+(.+?)(,|$)',a or '');return m.group(1).strip().lower() if m else None
# shared chrome copied from an existing section page so nav, search and footer stay identical
tpl=open('shops.html').read()
HEADER=tpl[tpl.find('<a class="skip"'):tpl.find('<main')].replace(' aria-current="page"','')
FOOTER=tpl[tpl.find('</main>')+7:]
CSP="default-src 'self'; script-src 'self' 'sha256-/fikJO3y8/FfvJxadqacMFRHk8y+I5ng+WE0NyQXczI='; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self'; font-src 'self'; frame-src https://www.facebook.com; object-src 'none'; base-uri 'self'; form-action 'self'; upgrade-insecure-requests"
THEME="<script>(function(){try{var t=localStorage.getItem('hes-theme');if(t!=='dark'&&t!=='light')t=matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light';document.documentElement.setAttribute('data-theme',t);}catch(e){}})();</script>"
CSSV=re.search(r'style\.css\?v=(\d+)',tpl).group(1)
def head(title,desc,path,ld,ogtype='website',img=None):
  img=img or BASE+'og-image.jpg'
  url=BASE+path
  return f'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta http-equiv="Content-Security-Policy" content="{CSP}"><meta name="referrer" content="strict-origin-when-cross-origin"><meta name="viewport" content="width=device-width, initial-scale=1">
{THEME}
<title>{E(title)}</title><meta name="description" content="{E(desc)}">
<meta name="color-scheme" content="light dark"><link rel="canonical" href="{url}"><meta name="robots" content="index, follow, max-image-preview:large">
<meta property="og:type" content="{ogtype}"><meta property="og:site_name" content="Hanceville Entertainment &amp; Shopping"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{img}"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{E(title)}"><meta name="twitter:description" content="{E(desc)}"><meta name="twitter:image" content="{img}">
<meta name="theme-color" content="#0b0710"><link rel="icon" href="/favicon.ico" sizes="48x48"><link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png"><link rel="manifest" href="/site.webmanifest">
<link rel="stylesheet" href="style.css?v={CSSV}"><link rel="stylesheet" href="place.css?v=2">
<script type="application/ld+json">{json.dumps(ld,ensure_ascii=False)}</script>
</head>
'''
def crumbs(items):
  return '<div class="crumbbar"><div class="wrap"><nav class="crumbs" aria-label="Breadcrumb">'+' &rsaquo; '.join(f'<a href="{h}">{E(t)}</a>' if h else f'<span aria-current="page">{E(t)}</span>' for t,h in items)+'</nav></div></div>'
def bl(items):return {"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":i+1,"name":t,"item":BASE+(h or '')} for i,(t,h) in enumerate(items)]}
def tile(x):
  img=f'<img src="{x["logo"]}" alt="" width="48" height="48" loading="lazy" decoding="async">' if x.get('logo') else f'<span class="pl-ini" aria-hidden="true">{E("".join(w[0] for w in x["name"].split()[:2]).upper())}</span>'
  return f'<li><a class="pl-tile" href="place-{x["slug"]}.html">{img}<span><strong>{E(x["name"])}</strong><small>{E(x["category"])}</small></span></a></li>'
def maps(x):return 'https://www.google.com/maps/search/?api=1&query='+urllib.parse.quote(x['name']+' '+x['address'])
today=datetime.date.today().isoformat()
pages=[]
# ---------- verified overrides (tools/verified.json) ----------
VER=json.load(open('tools/verified.json'))
for k,v in VER.items():
  if k.startswith('_') or k not in P:continue
  for f in('facebook','phone','address','hours','hours_source','hours_source_label','hours_spec','sources','verified','schema_type','documents'):
    if v.get(f):P[k][f]=v[f]
# ---------- schema.org subtype, chosen from the listing's own name, category and service text ----------
RULES=[(r'barber','BarberShop'),(r'nail','NailSalon'),(r'salon|hair|beauty|spa\b','BeautySalon'),(r'pharmac|drug co','Pharmacy'),
 (r'pizza|bbq|barbecue|grill|restaurant|diner|kitchen|burger|taco|sushi|steak|deli|eatery|wings|subway|shrimp','Restaurant'),
 (r'coffee|barista|brew\b|cafe','CafeOrCoffeeShop'),(r'bakery|sunflour','Bakery'),(r'winery','Winery'),
 (r'church|abbey|shrine|parish|chapel|ministr|baptist|methodist|catholic|orthodox|pentecostal','Church'),
 (r'library','Library'),(r'high school|elementary|middle school|academy|preschool','School'),(r'college|university','CollegeOrUniversity'),
 (r'tire','TireShop'),(r'towing|wrecker','AutomotiveBusiness'),(r'auto sales|motors|car lot|dealer','AutoDealer'),
 (r'auto repair|mechanic|muffler|truck and trailer repair|service center','AutoRepair'),(r'insurance','InsuranceAgency'),
 (r'bank|credit union','BankOrCreditUnion'),(r'hotel|inn\b|motel|lodg','LodgingBusiness'),(r'rv park|campground','Campground'),
 (r'storage','SelfStorage'),(r'veterinar|animal medical','VeterinaryCare'),(r'thrift','ThriftStore' ),(r'boutique|clothing','ClothingStore'),
 (r'furniture','FurnitureStore'),(r'grocer|market\b|foods','GroceryStore'),(r'park\b|stadium','Park'),
 (r'police|sheriff','PoliceStation'),(r'fire department|fire dept|fire and rescue','FireStation'),(r'city hall|department|office|commission|council|town of|city of','GovernmentOffice')]
OK_TYPES={'BarberShop','NailSalon','BeautySalon','Pharmacy','Restaurant','CafeOrCoffeeShop','Bakery','Winery','Church','Library','School','CollegeOrUniversity','TireShop','AutomotiveBusiness','AutoDealer','AutoRepair','InsuranceAgency','BankOrCreditUnion','LodgingBusiness','Campground','SelfStorage','VeterinaryCare','ClothingStore','FurnitureStore','GroceryStore','Park','PoliceStation','FireStation','GovernmentOffice','LocalBusiness','Organization','Person','NGO'}
def stype(x):
  if x.get('schema_type'):return x['schema_type']
  k=x['kinds'][0][0]
  if k=='council':return 'Person'
  t=' '.join(str(x.get(f) or '') for f in('name','category','service')).lower()
  for pat,ty in RULES:
    if re.search(pat,t):return 'Store' if ty=='ThriftStore' else ty
  if k=='nonprofits':return 'NGO'
  if k in('city','departments'):return 'GovernmentOffice'
  return 'LocalBusiness' if k in('businesses','shops','eats','index') else 'Organization'
def postal(a):
  m=re.match(r'^\s*(.+?),\s*([A-Za-z .]+?),\s*(AL|Alabama)\.?\s*(\d{5})?\s*$',a or '')
  if not m:return a
  d={"@type":"PostalAddress","streetAddress":m.group(1),"addressLocality":m.group(2).strip(),"addressRegion":"AL","addressCountry":"US"}
  if m.group(4):d["postalCode"]=m.group(4)
  return d
def srcs_of(x):
  out=[]
  for sv in x.get('sources') or []:
    if isinstance(sv,dict):out.append((sv['url'],sv['label']))
  have={u for u,_ in out}
  for u,l in((x.get('source'),'Listing source'),(x.get('website'),'Official website'),(x.get('facebook'),'Official Facebook Page'),(x.get('hours_source'),x.get('hours_source_label') or 'Hours source')):
    if isinstance(u,str) and u not in have and re.match(r'^https?://',u):out.append((u,l));have.add(u)
  return out
TABS=[('bio','Bio'),('hours','Hours'),('contact','Contact'),('location','Location'),('social','Social Links'),('media','Media'),('documents','Documents'),('references','References'),('related','Related')]
def tab_file(s,k):return f'place-{s}.html' if k=='bio' else (f'sources.html#s-{s}' if k=='references' else f'place-{s}-{k}.html')
def tabs_for(x):
  t=['bio']
  if x.get('hours'):t.append('hours')
  if any(x.get(k) for k in('phone','email','website','contact')):t.append('contact')
  if x.get('address'):t.append('location')
  if x.get('facebook') or (x.get('website') and 'facebook.com' not in x['website']):t.append('social')
  if x.get('photo'):t.append('media')
  if x.get('documents'):t.append('documents')
  if srcs_of(x):t.append('references')
  t.append('related');return t
def place(x,prev,nxt):
  s=x['slug'];cat=x['category'];cs=slug(cat);n=x['name'];ty=stype(x)
  desc=x.get('description') or f'{n} is listed in the {cat} section of our Hanceville directory.'
  meta=(desc[:150].rsplit(' ',1)[0]+'...') if len(desc)>155 else desc
  img=BASE+x['logo'] if x.get('logo') else None
  ent={"@type":ty,"@id":BASE+f'place-{s}.html#entity',"name":n,"description":desc,"url":BASE+f'place-{s}.html'}
  if ty=='Person':
    ent.pop('url');ent["mainEntityOfPage"]=BASE+f'place-{s}.html'
    if x.get('service'):ent["jobTitle"]=x['service']
  if img:ent["image"]=img
  if x.get('phone'):ent["telephone"]=x['phone']
  if x.get('email'):ent["email"]=x['email']
  if x.get('address'):ent["address"]=postal(x['address'])
  same=[u for u in [x.get('website'),x.get('facebook')] if u and u.startswith('https://')]
  if same:ent["sameAs"]=same
  if x.get('hours_spec'):ent["openingHoursSpecification"]=[{"@type":"OpeningHoursSpecification","dayOfWeek":h['days'],"opens":h['opens'],"closes":h['closes']} for h in x['hours_spec']]
  tabs=tabs_for(x);lab=dict(TABS)
  cta=''
  if x.get('phone'):cta+=f'<a class="btn" href="tel:{re.sub(r"[^0-9]","",x["phone"])}">Call {E(x["phone"])}</a> '
  if x.get('address'):cta+=f'<a class="btn alt2" href="{E(maps(x))}" target="_blank" rel="noopener noreferrer">Get directions</a> '
  if x.get('website') and 'facebook.com' not in x['website']:cta+=f'<a class="btn alt3" href="{E(x["website"])}" target="_blank" rel="noopener noreferrer">Visit website</a> '
  if x.get('facebook'):cta+=f'<a class="btn alt3" href="{E(x["facebook"])}" target="_blank" rel="noopener noreferrer">Facebook Page</a>'
  logo=f'<img class="pl-logo" src="{x["logo"]}" alt="{E(n)} logo" width="96" height="96" decoding="async">' if x.get('logo') else ''
  sub=E(x['service']) if x.get('service') else E(cat)
  def page(k,body):
    path=tab_file(s,k);tl=lab[k]
    title=f'{n} | Hanceville, AL | {cat}' if k=='bio' else f'{n} {tl} | Hanceville Entertainment & Shopping'
    md=meta if k=='bio' else TABDESC[k](x)
    crumb=[('Home','index.html'),('All Places','places.html'),(cat,f'category-{cs}.html')]+([(n,None)] if k=='bio' else [(n,f'place-{s}.html'),(tl,None)])
    graph=[bl([(t,h or path) for t,h in crumb][0:1]+[(t,h or path) for t,h in crumb][1:])]
    if k=='bio':graph.insert(0,ent)
    else:graph.insert(0,{"@type":"WebPage","@id":BASE+path+'#webpage',"url":BASE+path,"name":title,"about":{"@id":ent["@id"]}})
    graph[-1]=bl([(t,(h if h else path)) for t,h in crumb])
    ld={"@context":"https://schema.org","@graph":graph}
    h=head(title,md,path,ld,'business.business' if k=='bio' and ty not in('Person','Organization','GovernmentOffice','NGO') else 'website',img)+f'<body data-page="place">\n{HEADER}<main id="main">'
    h+=crumbs(crumb)
    hx='h1' if k=='bio' else 'p class="pl-name"'
    h+=f'<div class="page-head pl-head"><div class="wrap">{logo}<div><p class="kick"><a class="catpill" href="category-{cs}.html">{E(cat)}</a></p><{hx}>{E(n)}</{hx.split()[0]}><p>{sub} in the Hanceville area</p><p class="pl-cta">{cta}</p></div></div></div>'
    h+='<nav class="pl-tabs" aria-label="Pages for this listing"><div class="wrap">'+''.join(f'<a href="{tab_file(s,t)}"{" aria-current=\"page\"" if t==k else ""}>{lab[t]}</a>' for t in tabs)+'</div></nav><div class="wrap pl-body">'
    if k!='bio':body=body.replace('<h2>','<h1 class="pl-h1">',1).replace('</h2>','</h1>',1)
    h+=body
    i=tabs.index(k);nx=[t for t in tabs[i+1:]];pv=tabs[:i]
    pn='<nav class="pl-pn" aria-label="Other pages for this listing">'
    if pv:pn+=f'<a rel="prev" href="{tab_file(s,pv[-1])}">&larr; {lab[pv[-1]]}</a>'
    if nx:pn+=f'<a rel="next" href="{tab_file(s,nx[0])}">{lab[nx[0]]} &rarr;</a>'
    h+=pn+'</nav>'
    h+=f'<p class="pl-note">Something out of date? Owners can request a correction by messaging <a href="https://www.facebook.com/2333964643484816" target="_blank" rel="noopener noreferrer">our Facebook Page</a>. Sources for this listing are on our <a href="sources.html#s-{s}">Sources and References</a> page.</p>'
    h+='</div></main>\n'+FOOTER.replace('<script src="app.js','<script src="place.js?v=1" defer></script>\n<script src="app.js')
    h=re.sub(r'<a [^>]*href="http://([^"]+)"[^>]*>(.*?)</a>',lambda m:f'<span class="pl-note">{m.group(2)}: {m.group(1).rstrip("/")} (this site has no secure https version, so type the address yourself if you want to visit)</span>',h)
    open(path,'w').write(h);pages.append(path)
  # Bio (main page)
  ab=f'<section class="pl-sec" id="bio"><h2>About {E(n)}</h2><p>{E(desc)}</p>'
  if x.get('who'):ab+=f'<p><strong>Who it serves:</strong> {E(x["who"])}</p>'
  if x.get('how'):ab+=f'<p><strong>How to get started:</strong> {E(x["how"])}</p>'
  if x.get('term'):ab+=f'<p><strong>Term:</strong> {E(x["term"])}</p>'
  if x.get('tags'):ab+='<p class="pl-tags">'+''.join(f'<span class="tag">{E(t)}</span>' for t in x['tags'][:8])+'</p>'
  ab+='</section>'
  cards=[t for t in tabs if t!='bio']
  ab+='<section class="pl-sec"><h2>Explore this listing</h2><ul class="pl-grid">'+''.join(f'<li><a class="pl-tile" href="{tab_file(s,t)}"><span><strong>{lab[t]}</strong><small>{E(TABHINT[t](x))}</small></span></a></li>' for t in cards)+'</ul>'
  ab+=''.join(f'<p class="pl-note">Also listed on <a href="{kind}.html">{E(label)}</a>.</p>' for kind,label in x['kinds'] if kind!='index')+'</section>'
  page('bio',ab)
  if 'hours' in tabs:
    hs=f' These hours come from the {E(x["hours_source_label"][0].lower()+x["hours_source_label"][1:])}.' if x.get('hours_source_label') else ''
    vv=f' Last checked {E(x["verified"])}.' if x.get('verified') else ''
    page('hours',f'<section class="pl-sec"><h2>Hours for {E(n)}</h2><p>{E(x["hours"])}</p><p class="pl-note">Hours can change around holidays, so a quick call before you drive over is always a good idea.{hs}{vv}</p></section>')
  if 'contact' in tabs:
    c='<dl class="pl-dl">'
    if x.get('contact'):c+=f'<dt>Contact</dt><dd>{E(x["contact"])}</dd>'
    if x.get('phone'):c+=f'<dt>Phone</dt><dd><a href="tel:{re.sub(r"[^0-9]","",x["phone"])}">{E(x["phone"])}</a></dd>'
    if x.get('email'):c+=f'<dt>Email</dt><dd><a href="mailto:{E(x["email"])}">{E(x["email"])}</a></dd>'
    if x.get('website'):c+=f'<dt>Website</dt><dd><a href="{E(x["website"])}" target="_blank" rel="noopener noreferrer">{E(re.sub(r"^https?://(www\.)?","",x["website"]).rstrip("/"))}</a></dd>'
    page('contact',f'<section class="pl-sec"><h2>Contact {E(n)}</h2>{c}</dl></section>')
  if 'location' in tabs:
    st=street(x['address']);near=[y for y in P.values() if y is not x and st and street(y.get('address'))==st][:6]
    b=f'<section class="pl-sec"><h2>Location and directions</h2><p>{E(x["address"])}</p><p><a class="btn alt2" href="{E(maps(x))}" target="_blank" rel="noopener noreferrer">Open directions in Google Maps</a></p></section>'
    if near:b+='<section class="pl-sec"><h2>Also on this street</h2><ul class="pl-grid">'+''.join(tile(y) for y in near)+'</ul></section>'
    page('location',b)
  if 'social' in tabs:
    b=f'<section class="pl-sec"><h2>{E(n)} online</h2><ul class="pl-links">'
    if x.get('facebook'):b+=f'<li><a href="{E(x["facebook"])}" target="_blank" rel="noopener noreferrer">Facebook Page</a></li>'
    if x.get('website') and 'facebook.com' not in x['website']:b+=f'<li><a href="{E(x["website"])}" target="_blank" rel="noopener noreferrer">Official website</a></li>'
    b+='</ul></section>'
    if x.get('facebook'):b+=f'<section class="pl-sec"><h2>Latest from Facebook</h2><p>The feed loads from Facebook only when you ask for it, which keeps this page fast and private until you choose to see it.</p><div class="fb-facade" data-href="{E(x["facebook"])}"><button type="button" class="btn fb-load">Show latest Facebook posts</button></div></section>'
    page('social',b)
  if 'media' in tabs:
    page('media',f'<section class="pl-sec"><h2>Photos of {E(n)}</h2><img src="{E(x["photo"])}" alt="{E(n)}" loading="lazy" decoding="async" width="240" height="240"></section>')
  if 'documents' in tabs:
    page('documents',f'<section class="pl-sec"><h2>Documents from {E(n)}</h2><ul class="pl-links">'+''.join(f'<li><a href="{E(d["url"])}" target="_blank" rel="noopener noreferrer">{E(d["title"])}</a></li>' for d in x['documents'])+'</ul></section>')
  samec=[y for y in CATS[cat] if y is not x][:12]
  b=f'<section class="pl-sec"><h2>More in {E(cat)}</h2>'+(('<ul class="pl-grid">'+''.join(tile(y) for y in samec)+'</ul>') if samec else '<p>This is the only listing in this category right now. Browse the full A to Z list for more places nearby.</p>')
  b+=f'<p><a class="btn alt3" href="category-{cs}.html">See every {E(cat)} listing</a> <a class="btn alt3" href="places.html">Browse all places A to Z</a></p>'
  ln='<nav class="pl-pn" aria-label="Previous and next listing in this category">'
  if prev:ln+=f'<a href="place-{prev["slug"]}.html">&larr; {E(prev["name"])}</a>'
  if nxt:ln+=f'<a href="place-{nxt["slug"]}.html">{E(nxt["name"])} &rarr;</a>'
  page('related',b+ln+'</nav></section>')
TABDESC={'hours':lambda x:f'Opening hours for {x["name"]} in the Hanceville area, with the source and the date we last checked them.',
 'contact':lambda x:f'Phone, email and website for {x["name"]} in the Hanceville area.',
 'location':lambda x:f'Address and directions for {x["name"]}, plus other listings on the same street.',
 'social':lambda x:f'Official Facebook Page and website for {x["name"]}, with recent posts that load only when you ask.',
 'media':lambda x:f'Photos of {x["name"]} from official sources.',
 'documents':lambda x:f'Official documents published by {x["name"]}.',
 'related':lambda x:f'More {x["category"]} listings near Hanceville, related to {x["name"]}.'}
TABHINT={'hours':lambda x:'Opening hours and when we last checked them','contact':lambda x:x.get('phone') or 'Phone, email and website',
 'location':lambda x:x.get('address') or 'Address and directions','social':lambda x:'Facebook Page and website','media':lambda x:'Photos',
 'documents':lambda x:'Official documents','references':lambda x:'Where this information comes from','related':lambda x:f'More in {x["category"]}'}
for cat,items in CATS.items():
  for i,x in enumerate(items):place(x,items[i-1] if i else None,items[i+1] if i+1<len(items) else None)
for cat,items in CATS.items():
  cs=slug(cat);items=CATS[cat]
  other=sorted(c for c in CATS if c!=cat)
  h=head(f'{cat} in Hanceville, AL | Hanceville Entertainment & Shopping',f'Every {cat} listing in our Hanceville directory, with a full page for each one.',f'category-{cs}.html',{"@context":"https://schema.org",**bl([('Home',''),('All Places','places.html'),(cat,f'category-{cs}.html')])})
  h+=f'<body data-page="category">\n{HEADER}<main id="main">'+crumbs([('Home','index.html'),('All Places','places.html'),(cat,None)])
  h+=f'<div class="page-head"><div class="wrap"><h1>{E(cat)}</h1><p>{len(items)} {"listing" if len(items)==1 else "listings"} in this category. Tap any name to open its full page with hours, contact details, directions and related places.</p></div></div><div class="wrap pl-body"><ul class="pl-grid">'+''.join(tile(x) for x in items)+'</ul>'
  h+='<section class="pl-sec"><h2>Other categories</h2><p class="pl-cats">'+''.join(f'<a class="tag" href="category-{slug(c)}.html">{E(c)}</a>' for c in other)+'</p></section></div></main>\n'+FOOTER
  open(f'category-{cs}.html','w').write(h);pages.append(f'category-{cs}.html')
h=head('All Hanceville Places A to Z | Hanceville Entertainment & Shopping','Every business, office, nonprofit and service in our Hanceville directory, each with its own full page.','places.html',{"@context":"https://schema.org",**bl([('Home',''),('All Places','places.html')])})
h+=f'<body data-page="places">\n{HEADER}<main id="main">'+crumbs([('Home','index.html'),('All Places',None)])
h+=f'<div class="page-head"><div class="wrap"><h1>All Places A to Z</h1><p>{len(P)} businesses, offices, nonprofits and services, each with its own page. Pick a category or jump to a letter.</p></div></div><div class="wrap pl-body"><p class="pl-cats">'+''.join(f'<a class="tag" href="category-{slug(c)}.html">{E(c)} ({len(v)})</a>' for c,v in sorted(CATS.items()))+'</p>'
by={}
for x in sorted(P.values(),key=lambda x:x['name'].lower()):by.setdefault(x['name'][0].upper() if x['name'][0].isalpha() else '#',[]).append(x)
h+='<nav class="pl-tabs" aria-label="Letters"><div class="wrap">'+''.join(f'<a href="#l-{k if k!="#" else "num"}">{k}</a>' for k in by)+'</div></nav>'
for k,v in by.items():h+=f'<section class="pl-sec" id="l-{k if k!="#" else "num"}"><h2>{k}</h2><ul class="pl-grid">'+''.join(tile(x) for x in v)+'</ul></section>'
h+='</div></main>\n'+FOOTER;open('places.html','w').write(h);pages.append('places.html')
# ---------- footer pages: About, Contact, Privacy, Terms, Sources & References, Sitemap ----------
FB='https://www.facebook.com/2333964643484816'
def simple(path,title,desc,h1,body,extra_ld=None):
  ld={"@context":"https://schema.org","@graph":[{"@type":"WebPage","@id":BASE+path+'#webpage',"url":BASE+path,"name":title,"description":desc},bl([('Home',''),(h1,path)])]}
  h=head(title,desc,path,ld)+f'<body data-page="info">\n{HEADER}<main id="main">'+crumbs([('Home','index.html'),(h1,None)])
  h+=f'<div class="page-head"><div class="wrap"><h1>{E(h1)}</h1></div></div><div class="wrap pl-body">{body}</div></main>\n'+FOOTER
  h=re.sub(r'<a [^>]*href="http://([^"]+)"[^>]*>(.*?)</a>',lambda m:f'{m.group(2)}: {m.group(1).rstrip("/")} (no secure https version)',h)
  open(path,'w').write(h);pages.append(path)
simple('about.html','About Us | Hanceville Entertainment & Shopping','Who we are, what this free Hanceville and Cullman County directory covers, and how we check every listing.','About Hanceville Entertainment & Shopping',
 '<section class="pl-sec"><h2>Who we are</h2><p>Hanceville Entertainment &amp; Shopping, also known as Shop Local Alabama, is an independent community page. We share the people, places and small businesses that make Hanceville and Cullman County feel like home.</p><p>We are not the Chamber of Commerce and we are not part of the City of Hanceville. City details on this site link back to the city\'s own pages so you can always check the original.</p></section>'
 f'<section class="pl-sec"><h2>What you will find here</h2><p>The directory lists {len(P)} businesses, offices, nonprofits and services, and every one has its own page. You can browse by <a href="places.html">name from A to Z</a>, by category, or start with <a href="city.html">City Services</a>, <a href="businesses.html">the Business Directory</a>, <a href="news.html">Local News</a> and <a href="events.html">Upcoming Events</a>.</p></section>'
 '<section class="pl-sec"><h2>How we check listings</h2><p>We only publish details we can confirm on an official source, such as a business\'s own website, its own Facebook Page, a listing the owner has claimed, or a public record. When we cannot confirm something, we leave it off rather than guess. Every listing shows its sources on our <a href="sources.html">Sources and References</a> page.</p></section>'
 f'<section class="pl-sec"><h2>Listings are free</h2><p>Business owners can ask to be added, corrected or removed at any time. See our <a href="contact.html">Contact page</a> or message <a href="{FB}" target="_blank" rel="noopener noreferrer">our Facebook Page</a>.</p></section>')
simple('contact.html','Contact Us | Hanceville Entertainment & Shopping','How to reach Hanceville Entertainment & Shopping to add a listing, fix a detail or share local news.','Contact Us',
 f'<section class="pl-sec"><h2>The fastest way to reach us</h2><p>Send a message to <a href="{FB}" target="_blank" rel="noopener noreferrer">our Facebook Page</a>. We read every message and usually reply within a day or two.</p><p><a class="btn" href="{FB}" target="_blank" rel="noopener noreferrer">Message us on Facebook</a></p></section>'
 '<section class="pl-sec"><h2>What to send us</h2><ul class="pl-links"><li><strong>A new listing:</strong> the business name, address, phone and a link to its website or Facebook Page.</li><li><strong>A correction:</strong> the listing name, what is wrong, and a link where we can confirm the right detail.</li><li><strong>A removal:</strong> the listing name. Owners can have a listing removed at any time.</li><li><strong>Local news or an event:</strong> a link to the official post or announcement.</li></ul></section>'
 '<section class="pl-sec"><h2>Business owners</h2><p>Want your business featured? Read how on the <a href="businesses.html#get-featured">Get Featured</a> section of the Business Directory.</p></section>')
simple('privacy.html','Privacy Policy | Hanceville Entertainment & Shopping','What this site stores, what it does not collect, and how Facebook content and map links work.','Privacy Policy',
 '<section class="pl-sec"><h2>The short version</h2><p>This site has no accounts, no sign up forms, no advertising and no analytics or tracking scripts. We do not collect your name, email or location.</p></section>'
 '<section class="pl-sec"><h2>What stays on your own device</h2><p>Your browser keeps a few small settings so the site remembers your choices: your light or dark theme, your language choice, and any listings you save as favorites. These live only in your browser\'s local storage. We never receive them, and you can clear them any time by clearing your browser\'s site data.</p><p>The site also uses a service worker that keeps copies of pages and images on your device so they load faster and still open with a weak signal.</p></section>'
 '<section class="pl-sec"><h2>Hosting</h2><p>The site is hosted on GitHub Pages. Like any web host, GitHub may log basic technical details such as your IP address to keep the service secure. See the <a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement" target="_blank" rel="noopener noreferrer">GitHub General Privacy Statement</a>.</p></section>'
 '<section class="pl-sec"><h2>Facebook posts and maps</h2><p>Facebook posts never load on their own. They appear only after you press a button such as "Show latest Facebook posts." Once you do, Facebook\'s own <a href="https://www.facebook.com/privacy/policy/" target="_blank" rel="noopener noreferrer">privacy policy</a> applies to that content.</p><p>Direction buttons open Google Maps in a new tab, where <a href="https://policies.google.com/privacy" target="_blank" rel="noopener noreferrer">Google\'s privacy policy</a> applies.</p></section>'
 '<section class="pl-sec"><h2>Questions</h2><p>Message us through the <a href="contact.html">Contact page</a>. This policy was last updated October 24, 2026.</p></section>')
simple('terms.html','Terms of Use | Hanceville Entertainment & Shopping','The terms for using the Hanceville Entertainment & Shopping community directory.','Terms of Use',
 '<section class="pl-sec"><h2>Information only</h2><p>Listings, hours and news on this site are shared for general information. We check details against official sources, but businesses and offices can change things without notice, so please confirm hours and details with them before you go.</p></section>'
 '<section class="pl-sec"><h2>Independent site</h2><p>This is an independent community page. It is not the official Chamber of Commerce and is not affiliated with the City of Hanceville or any business listed here. A listing is not an endorsement.</p></section>'
 '<section class="pl-sec"><h2>Names, logos and links</h2><p>Business names, logos and trademarks belong to their owners and are shown only to identify each listing. News stories are written in our own words with links to the original source. Links to other websites are for your convenience, and those sites have their own terms.</p></section>'
 '<section class="pl-sec"><h2>Corrections and removal</h2><p>Owners can ask us to correct or remove a listing at any time through the <a href="contact.html">Contact page</a>.</p></section>'
 '<section class="pl-sec"><h2>Changes</h2><p>We may update these terms as the site grows. They were last updated October 24, 2026.</p></section>')
# Sources and References: every citation for every listing lives here
sb='<section class="pl-sec"><h2>How we source information</h2><p>Every detail in the directory comes from an official source: the business or office\'s own website, its own Facebook Page, a listing its owner has claimed, or a public record. The sources for each listing are below, with the date we last checked when we have it. Listings without a source link here come from our original community directory and are queued for re-checking.</p></section>'
byl={}
for x in sorted(P.values(),key=lambda x:x['name'].lower()):byl.setdefault(x['name'][0].upper() if x['name'][0].isalpha() else '#',[]).append(x)
sb+='<nav class="pl-tabs" aria-label="Letters"><div class="wrap">'+''.join(f'<a href="#src-{k if k!="#" else "num"}">{k}</a>' for k in byl)+'</div></nav>'
nsrc=0
for k,v in byl.items():
  sb+=f'<section class="pl-sec" id="src-{k if k!="#" else "num"}"><h2>{k}</h2><dl class="pl-dl">'
  for x in v:
    ss=srcs_of(x)
    if ss:nsrc+=1
    li=''.join(f'<li><a href="{E(u)}" target="_blank" rel="noopener noreferrer">{E(l)}</a></li>' for u,l in ss) or '<li>Original community directory entry, queued for re-checking</li>'
    vv=f'<li>Last checked {E(x["verified"])}</li>' if x.get('verified') else ''
    sb+=f'<dt id="s-{x["slug"]}"><a href="place-{x["slug"]}.html">{E(x["name"])}</a></dt><dd><ul class="pl-links">{li}{vv}</ul></dd>'
  sb+='</dl></section>'
simple('sources.html','Sources and References | Hanceville Entertainment & Shopping','The official sources behind every listing in the Hanceville Entertainment & Shopping directory.','Sources and References',sb)
# HTML sitemap
grp=[('Start here',[('index.html','Home'),('places.html','All Places A to Z'),('about.html','About Us'),('contact.html','Contact Us')]),
 ('City and community',[('city.html','City Services'),('departments.html','Departments and Contacts'),('council.html','City Council'),('directory.html','Community Directory'),('nonprofits.html','Nonprofits'),('wallace.html','Wallace State'),('resources.html','More Resources')]),
 ('News, events and businesses',[('news.html','Local News'),('events.html','Upcoming Events'),('businesses.html','Business Directory'),('eats.html','Local Eats'),('shops.html','Hometown Shops'),('fun.html','A Little Fun')]),
 ('Site information',[('privacy.html','Privacy Policy'),('terms.html','Terms of Use'),('sources.html','Sources and References')])]
mb=''.join(f'<section class="pl-sec"><h2>{t}</h2><ul class="pl-links">'+''.join(f'<li><a href="{u}">{l}</a></li>' for u,l in v if os.path.exists(u) or u in pages)+'</ul></section>' for t,v in grp)
mb+='<section class="pl-sec"><h2>Categories</h2><p class="pl-cats">'+''.join(f'<a class="tag" href="category-{slug(c)}.html">{E(c)} ({len(v)})</a>' for c,v in sorted(CATS.items()))+'</p></section>'
st=sorted(glob.glob('story-*.html'))
def stitle(f):
  m=re.search(r'<h1[^>]*>(.*?)</h1>',open(f).read(),re.S);return re.sub(r'<[^>]+>','',m.group(1)).strip() if m else f
if st:mb+='<section class="pl-sec"><h2>News stories</h2><ul class="pl-links">'+''.join(f'<li><a href="{f}">{stitle(f)}</a></li>' for f in st)+'</ul></section>'
mb+=f'<section class="pl-sec"><h2>Every listing</h2><p>All {len(P)} listings, each with its own pages for hours, contact, location and more, are on <a href="places.html">All Places A to Z</a>.</p></section>'
simple('sitemap.html','Sitemap | Hanceville Entertainment & Shopping','Every section, category and news story on Hanceville Entertainment & Shopping in one list.','Sitemap',mb)
print(nsrc,'listings with source links')
# remove stale generated pages
for f in os.listdir('.'):
  if re.match(r'^(place|category)-.*\.html$',f) and f not in pages:os.remove(f)
# sitemap
sm=open('sitemap.xml').read();sm=re.sub(r'\s*<url><loc>'+re.escape(BASE)+r'(place|category)-[^<]*</loc>.*?</url>','',sm,flags=re.S)
sm=re.sub(r'\s*<url><loc>'+re.escape(BASE)+r'(places|about|contact|privacy|terms|sources|sitemap)\.html</loc>.*?</url>','',sm,flags=re.S)
sm=sm.replace('</urlset>',''.join(f'\n  <url><loc>{BASE}{p}</loc><lastmod>{today}</lastmod><changefreq>monthly</changefreq><priority>0.5</priority></url>' for p in sorted(pages))+'\n</urlset>')
open('sitemap.xml','w').write(sm)
json.dump({x['slug']:1 for x in P.values()},open('places.json','w'),separators=(',',':'))
print(len(P),'places',len(CATS),'categories',len(pages),'generated pages')
subprocess.run(['python3','tools/footer.py'],check=True)
