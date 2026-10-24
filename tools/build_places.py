#!/usr/bin/env python3
"""Build one full page per listing (place-<slug>.html), one hub per category
(category-<slug>.html) and an A to Z hub (places.html) from the site's data.

Data sources, merged by slug (later sources fill blanks, never overwrite):
  1. the per-section JSON files (businesses.json, shops.json, eats.json, ...)
  2. window.SLH_LISTINGS inside index.html (the homepage directory)
Rerun after any data change:  python3 tools/build_places.py
Nothing here invents facts. Each section only appears when its data exists."""
import json,re,os,html,datetime,urllib.parse
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
def head(title,desc,path,ld):
  url=BASE+path
  return f'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta http-equiv="Content-Security-Policy" content="{CSP}"><meta name="referrer" content="strict-origin-when-cross-origin"><meta name="viewport" content="width=device-width, initial-scale=1">
{THEME}
<title>{E(title)}</title><meta name="description" content="{E(desc)}">
<meta name="color-scheme" content="light dark"><link rel="canonical" href="{url}"><meta name="robots" content="index, follow, max-image-preview:large">
<meta property="og:type" content="website"><meta property="og:site_name" content="Hanceville Entertainment &amp; Shopping"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}og-image.jpg"><meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0b0710"><link rel="icon" href="/favicon.ico" sizes="48x48"><link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png"><link rel="manifest" href="/site.webmanifest">
<link rel="stylesheet" href="style.css?v={CSSV}"><link rel="stylesheet" href="place.css?v=1">
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
def place(x,prev,nxt):
  s=x['slug'];cat=x['category'];cs=slug(cat);n=x['name']
  sec=[('about','About')]
  if x.get('hours'):sec.append(('hours','Hours'))
  if x.get('phone') or x.get('email') or x.get('website') or x.get('contact'):sec.append(('contact','Contact'))
  if x.get('address'):sec.append(('location','Location and Directions'))
  if x.get('facebook'):sec.append(('social','Social'))
  if x.get('photo'):sec.append(('photos','Photos'))
  sec.append(('related','Related'))
  desc=x.get('description') or f'{n} is listed in the {cat} section of our Hanceville directory.'
  meta=(desc[:150].rsplit(' ',1)[0]+'...') if len(desc)>155 else desc
  ld={"@context":"https://schema.org","@graph":[{"@type":"LocalBusiness" if x['kinds'][0][0] in('businesses','shops','eats','index') else "Organization","name":n,"description":desc,"url":BASE+f'place-{s}.html',
     **({"telephone":x['phone']} if x.get('phone') else {}),**({"address":x['address']} if x.get('address') else {}),
     **({"sameAs":[u for u in [x.get('website'),x.get('facebook')] if u]} if (x.get('website') or x.get('facebook')) else {})},
     bl([('Home',''),('All Places','places.html'),(cat,f'category-{cs}.html'),(n,f'place-{s}.html')])]}
  h=head(f'{n} | Hanceville, AL | {cat}',meta,f'place-{s}.html',ld)+f'<body data-page="place">\n{HEADER}<main id="main">'
  h+=crumbs([('Home','index.html'),('All Places','places.html'),(cat,f'category-{cs}.html'),(n,None)])
  logo=f'<img class="pl-logo" src="{x["logo"]}" alt="{E(n)} logo" width="96" height="96" decoding="async">' if x.get('logo') else ''
  sub=E(x['service']) if x.get('service') else E(cat)
  cta=''
  if x.get('phone'):cta+=f'<a class="btn" href="tel:{re.sub(r"[^0-9]","",x["phone"])}">Call {E(x["phone"])}</a> '
  if x.get('address'):cta+=f'<a class="btn alt2" href="{E(maps(x))}" target="_blank" rel="noopener noreferrer">Get directions</a> '
  if x.get('website') and 'facebook.com' not in x['website']:cta+=f'<a class="btn alt3" href="{E(x["website"])}" target="_blank" rel="noopener noreferrer">Visit website</a> '
  if x.get('facebook'):cta+=f'<a class="btn alt3" href="{E(x["facebook"])}" target="_blank" rel="noopener noreferrer">Facebook Page</a>'
  h+=f'<div class="page-head pl-head"><div class="wrap">{logo}<div><p class="kick"><a class="catpill" href="category-{cs}.html">{E(cat)}</a></p><h1>{E(n)}</h1><p>{sub} in the Hanceville area</p><p class="pl-cta">{cta}</p></div></div></div>'
  h+='<nav class="pl-tabs" aria-label="Sections of this page"><div class="wrap">'+''.join(f'<a href="#{a}">{t}</a>' for a,t in sec)+'</div></nav><div class="wrap pl-body">'
  ab=f'<p>{E(desc)}</p>'
  if x.get('who'):ab+=f'<p><strong>Who it serves:</strong> {E(x["who"])}</p>'
  if x.get('how'):ab+=f'<p><strong>How to get started:</strong> {E(x["how"])}</p>'
  if x.get('term'):ab+=f'<p><strong>Term:</strong> {E(x["term"])}</p>'
  if x.get('tags'):ab+='<p class="pl-tags">'+''.join(f'<span class="tag">{E(t)}</span>' for t in x['tags'][:8])+'</p>'
  h+=f'<section id="about" class="pl-sec"><h2>About {E(n)}</h2>{ab}</section>'
  if x.get('hours'):
    hs=f' <a href="{E(x["hours_source"])}" target="_blank" rel="noopener noreferrer">Hours source</a>.' if x.get('hours_source') else ''
    h+=f'<section id="hours" class="pl-sec"><h2>Hours</h2><p>{E(x["hours"])}</p><p class="pl-note">Hours can change around holidays, so a quick call before you drive over is always a good idea.{hs}</p></section>'
  if any(x.get(k) for k in('phone','email','website','contact')):
    c='<dl class="pl-dl">'
    if x.get('contact'):c+=f'<dt>Contact</dt><dd>{E(x["contact"])}</dd>'
    if x.get('phone'):c+=f'<dt>Phone</dt><dd><a href="tel:{re.sub(r"[^0-9]","",x["phone"])}">{E(x["phone"])}</a></dd>'
    if x.get('email'):c+=f'<dt>Email</dt><dd><a href="mailto:{E(x["email"])}">{E(x["email"])}</a></dd>'
    if x.get('website'):c+=f'<dt>Website</dt><dd><a href="{E(x["website"])}" target="_blank" rel="noopener noreferrer">{E(re.sub(r"^https?://(www\.)?","",x["website"]).rstrip("/"))}</a></dd>'
    h+=f'<section id="contact" class="pl-sec"><h2>Contact</h2>{c}</dl></section>'
  near=[]
  if x.get('address'):
    st=street(x['address']);near=[y for y in P.values() if y is not x and st and street(y.get('address'))==st][:6]
    h+=f'<section id="location" class="pl-sec"><h2>Location and Directions</h2><p>{E(x["address"])}</p><p><a class="btn alt2" href="{E(maps(x))}" target="_blank" rel="noopener noreferrer">Open directions in Google Maps</a></p>'
    if near:h+='<h3>Also on this street</h3><ul class="pl-grid">'+''.join(tile(y) for y in near)+'</ul>'
    h+='</section>'
  if x.get('facebook'):
    h+=f'<section id="social" class="pl-sec"><h2>Latest from Facebook</h2><p>See recent posts from {E(n)} right here. The feed loads from Facebook only when you ask for it, which keeps this page fast.</p><div class="fb-facade" data-href="{E(x["facebook"])}"><button type="button" class="btn fb-load">Show latest Facebook posts</button></div><p class="pl-note"><a href="{E(x["facebook"])}" target="_blank" rel="noopener noreferrer">Open the {E(n)} Facebook Page</a></p></section>'
  if x.get('photo'):
    h+=f'<section id="photos" class="pl-sec"><h2>Photos</h2><img src="{E(x["photo"])}" alt="{E(n)}" loading="lazy" decoding="async" width="240" height="240"></section>'
  same=[y for y in CATS[cat] if y is not x][:8]
  h+=f'<section id="related" class="pl-sec"><h2>More in {E(cat)}</h2>'
  h+=('<ul class="pl-grid">'+''.join(tile(y) for y in same)+'</ul>') if same else '<p>This is the only listing in this category right now.</p>'
  h+=f'<p><a class="btn alt3" href="category-{cs}.html">See every {E(cat)} listing</a> <a class="btn alt3" href="places.html">Browse all places A to Z</a></p>'
  pn='<nav class="pl-pn" aria-label="Previous and next listing">'
  if prev:pn+=f'<a rel="prev" href="place-{prev["slug"]}.html">&larr; {E(prev["name"])}</a>'
  if nxt:pn+=f'<a rel="next" href="place-{nxt["slug"]}.html">{E(nxt["name"])} &rarr;</a>'
  h+=pn+'</nav></section>'
  srcs=[u for u in [x.get('source'),x.get('website'),x.get('facebook')] if u]
  ver=f' Last checked {x["verified"]}.' if x.get('verified') else ''
  h+=f'<p class="pl-note pl-src">Information on this page comes from {"public sources linked above" if srcs else "our directory"}.{ver} Owners can request a correction by messaging <a href="https://www.facebook.com/2333964643484816" target="_blank" rel="noopener noreferrer">our Facebook Page</a>.</p>'
  for kind,label in x['kinds']:
    if kind!='index':h+=f'<p class="pl-note">Also listed on <a href="{kind}.html">{E(label)}</a>.</p>'
  h+='</div></main>\n'+FOOTER.replace('<script src="app.js','<script src="place.js?v=1" defer></script>\n<script src="app.js')
  # http-only sites: no insecure links (monitor.py rule); show the address as text instead
  h=re.sub(r'<a [^>]*href="http://([^"]+)"[^>]*>(.*?)</a>',lambda m:f'<span class="pl-note">{m.group(2)}: {m.group(1).rstrip("/")} (this site has no secure https version, so type the address yourself if you want to visit)</span>',h)
  open(f'place-{s}.html','w').write(h);pages.append(f'place-{s}.html')
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
# remove stale generated pages
for f in os.listdir('.'):
  if re.match(r'^(place|category)-.*\.html$',f) and f not in pages:os.remove(f)
# sitemap
sm=open('sitemap.xml').read();sm=re.sub(r'\s*<url><loc>'+re.escape(BASE)+r'(place|category)-[^<]*</loc>.*?</url>','',sm,flags=re.S)
sm=re.sub(r'\s*<url><loc>'+re.escape(BASE)+r'places\.html</loc>.*?</url>','',sm,flags=re.S)
sm=sm.replace('</urlset>',''.join(f'\n  <url><loc>{BASE}{p}</loc><lastmod>{today}</lastmod><changefreq>monthly</changefreq><priority>0.5</priority></url>' for p in sorted(pages))+'\n</urlset>')
open('sitemap.xml','w').write(sm)
json.dump({x['slug']:1 for x in P.values()},open('places.json','w'),separators=(',',':'))
print(len(P),'places',len(CATS),'categories')
