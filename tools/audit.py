#!/usr/bin/env python3
"""Fast static site audit for the Hanceville Entertainment & Shopping site.
Usage:  python3 tools/audit.py [--lighthouse] [--quiet]
Exit 0 = clean, 1 = problems found, 2 = the audit itself crashed.
Checks
  1. Broken internal links: every local href/src points to a file that exists.
  2. Missing pages: every listing in the data files and window.SLH_LISTINGS has place-<slug>.html.
  3. Empty tabs and sections: generated pages have no empty <section> and every in-page tab (#id) has a target.
  4. Banned characters in visible copy: em dash, en dash, double spaces (HTML text and JSON strings).
  5. Spelling with codespell (if installed), using the ignore list in tools/codespell-ignore.txt.
  6. Weight guard: index.html under 1.5 MB and no inline base64 JPEG/PNG anywhere.
  8. Sitemap: every page in sitemap.xml and every sitemap URL exists, robots.txt points to it.
  9. Meta, footer, headings, images, JSON-LD: unique titles, description, canonical, OG, Twitter, footer links,
     one h1, alt text, width/height, JSON-LD parses, known types, no placeholders, geo/hours only when verified.
 10. Reminder (warning) when a tools/verified.json entry is older than 90 days.
  7. --lighthouse: mobile Lighthouse on the live home page and one listing page; fails if
     performance < 90 or any other category < 95 (needs the lighthouse npm package and Chrome).
Fixes: see docs/TROUBLESHOOTING.md."""
import os,re,sys,json,glob,html,subprocess,shutil
ROOT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..');os.chdir(ROOT)
Q='--quiet' in sys.argv;P=[];W=[]
def prob(k,m):P.append(f'[{k}] {m}')
files=set(glob.glob('*.html'))|set(glob.glob('*.json'))|set(glob.glob('*.css'))|set(glob.glob('*.js'))
def slug(s):return re.sub(r'^-|-$','',re.sub(r'[^a-z0-9]+','-',(s or '').lower()))
htmls=sorted(glob.glob('*.html'))
# 1 + 3
for f in htmls:
  s=open(f,encoding='utf-8').read()
  body=re.sub(r'<script.*?</script>','',s,flags=re.S)
  if re.search(r'(src|href)="http://',s):prob('insecure-link',f'{f}: has an http:// link (monitor.py fails on this)')
  ids=set(re.findall(r'\bid="([^"]+)"',body))
  for h in re.findall(r'(?:href|src)="([^"]+)"',body):
    h=html.unescape(h)
    if re.match(r'^(https?:|mailto:|tel:|sms:|data:|javascript:|//)',h):continue
    path,_,frag=h.partition('#');path=path.split('?')[0].lstrip('/')
    if path and not os.path.exists(path):prob('broken-link',f'{f}: {h}')
    if not path and frag and f.startswith(('place-','category-','places')) and frag not in ids:prob('dead-tab',f'{f}: #{frag} has no target')
  if f.startswith(('place-','category-','places')):
    for sec in re.findall(r'<section[^>]*>(.*?)</section>',body,re.S):
      if '<img' not in sec and len(re.sub(r'<[^>]+>|\s','',re.sub(r'<h2.*?</h2>','',sec)))<3:prob('empty-section',f'{f}: empty section')
# 2
names=[]
for k in 'businesses shops eats nonprofits city departments directory resources wallace council'.split():
  try:names+=[x['name'] for x in json.load(open(k+'.json'))]
  except Exception as e:prob('data',f'{k}.json unreadable: {e}')
idx=open('index.html',encoding='utf-8').read()
m=re.search(r'window\.SLH_LISTINGS = (\[.*?\]);\n',idx,re.S)
if m:names+=[x['name'] for x in json.loads(m.group(1)) if x.get('category') not in('Fun Facts','Sweet Tea Jokes','Social Media')]
miss=sorted({n for n in names if not os.path.exists(f'place-{slug(n)}.html')})
for n in miss:prob('missing-page',f'no full page for "{n}" (run python3 tools/build_places.py)')
# 4
def text_of(s):
  s=re.sub(r'<script.*?</script>|<style.*?</style>|<!--.*?-->','',s,flags=re.S)
  return [html.unescape(t) for t in re.findall(r'>([^<]+)<',s)]+[html.unescape(a) for a in re.findall(r'(?:alt|title|content|aria-label)="([^"]+)"',s)]
def strings(o):
  if isinstance(o,str):yield o
  elif isinstance(o,list):
    for v in o:yield from strings(v)
  elif isinstance(o,dict):
    for v in o.values():yield from strings(v)
bad={}
for f in htmls:
  for t in text_of(open(f,encoding='utf-8').read()):
    for nm,pat in(('em dash','\u2014'),('en dash','\u2013'),('double space',r'\S  +\S')):
      if re.search(pat,t):bad.setdefault((f,nm),t.strip()[:80])
for f in glob.glob('*.json'):
  try:d=json.load(open(f,encoding='utf-8'))
  except Exception:continue
  for t in strings(d):
    if t.startswith('data:'):continue
    for nm,pat in(('em dash','\u2014'),('en dash','\u2013'),('double space',r'\S  +\S')):
      if re.search(pat,t):bad.setdefault((f,nm),t.strip()[:80])
if m:
  for t in strings(json.loads(m.group(1))):
    for nm,pat in(('em dash','\u2014'),('en dash','\u2013')):
      if re.search(pat,t):bad.setdefault(('index.html SLH_LISTINGS',nm),t[:80])
for (f,nm),t in sorted(bad.items()):prob('banned-char',f'{f}: {nm} in "{t}"')
# 5
cs=shutil.which('codespell') or os.path.expanduser('~/.local/bin/codespell')
if os.path.exists(cs):
  ign='tools/codespell-ignore.txt'
  srcs=[f for f in htmls if not f.startswith(('place-','category-'))]+sorted(glob.glob('*.json'))
  r=subprocess.run([cs,'-q','3','-I',ign]+srcs,capture_output=True,text=True)
  for line in r.stdout.splitlines()[:50]:prob('spelling',line[:160])
else:W.append('codespell not installed: pip install --user --break-system-packages codespell')
# 6
sz=os.path.getsize('index.html')
if sz>1_500_000:prob('weight',f'index.html is {sz:,} bytes (limit 1.5 MB). Run python3 tools/optimize_home.py')
for f in htmls:
  if re.search(r'data:image/(jpeg|jpg|png);base64',open(f,encoding='utf-8').read()):prob('weight',f'{f} has inline base64 raster images. Run python3 tools/optimize_home.py')
# 8. Sitemap: every public page is listed and every listed URL exists
BASE='https://shoplocalhanceville.github.io/'
try:
  locs=re.findall(r'<loc>([^<]+)</loc>',open('sitemap.xml').read())
  inmap={l[len(BASE):] or 'index.html' for l in locs}
  for l in sorted(inmap):
    if not os.path.exists(l):prob('sitemap',f'sitemap lists {l} but the file does not exist')
  for f in htmls:
    if not f.startswith('google') and f not in inmap:prob('sitemap',f'{f} is missing from sitemap.xml')
  if 'Sitemap: '+BASE+'sitemap.xml' not in open('robots.txt').read():prob('sitemap','robots.txt does not point to sitemap.xml')
except Exception as e:prob('sitemap',f'sitemap check crashed: {e}')
# 9. Meta consistency, footer, headings, images
titles={};VER=json.load(open('tools/verified.json')) if os.path.exists('tools/verified.json') else {}
TYPES={'ServiceChannel','FastFoodRestaurant','FoodEstablishment','HairSalon','AutoBodyShop','HVACBusiness','ChildCare','Florist','Hotel','PlaceOfWorship','OrganizationRole','Role','BarberShop','NailSalon','BeautySalon','Pharmacy','Restaurant','CafeOrCoffeeShop','Bakery','Winery','Church','Library','School','CollegeOrUniversity','TireShop','AutomotiveBusiness','AutoDealer','AutoRepair','InsuranceAgency','BankOrCreditUnion','LodgingBusiness','Campground','SelfStorage','VeterinaryCare','ClothingStore','FurnitureStore','GroceryStore','Park','PoliceStation','FireStation','GovernmentOffice','LocalBusiness','Organization','Person','NGO','Store','WebPage','BreadcrumbList','ListItem','PostalAddress','OpeningHoursSpecification','GeoCoordinates','WebSite','NewsArticle','Article','Event','Place','ItemList','CollectionPage','City','ImageObject','SearchAction','EntryPoint','EducationalOrganization','CivicStructure','FAQPage','Question','Answer','AboutPage','ContactPage','Offer','VirtualLocation','EventVenue','PerformingGroup','MusicGroup','SportsTeam','SportsEvent','Thing','Country','State','AdministrativeArea','ContactPoint','DefinedRegion','GovernmentOrganization','GovernmentService','Service','NewsMediaOrganization','LocalBusiness'}
def walk(o,f,slugk):
  if isinstance(o,dict):
    t=o.get('@type');ts=t if isinstance(t,list) else [t]
    for t in ts:
      if t and t not in TYPES:prob('schema',f'{f}: unknown or unexpected @type {t}')
    if 'geo' in o and not (VER.get(slugk) or {}).get('geo'):prob('schema',f'{f}: geo present but not in tools/verified.json')
    if 'openingHoursSpecification' in o and not (VER.get(slugk) or {}).get('hours_spec'):prob('schema',f'{f}: openingHoursSpecification without verified hours_spec')
    for v in o.values():walk(v,f,slugk)
  elif isinstance(o,list):
    for v in o:walk(v,f,slugk)
for f in htmls:
  if f.startswith('google'):continue
  s=open(f,encoding='utf-8').read()
  t=re.search(r'<title>(.*?)</title>',s,re.S)
  if not t:prob('meta',f'{f}: no <title>')
  else:titles.setdefault(t.group(1).strip(),[]).append(f)
  for need,pat in(('description',r'<meta name="description" content="[^"]{20,}"'),('canonical',r'<link rel="canonical" href="'),('og:title',r'property="og:title"'),('og:image',r'property="og:image"'),('twitter:card',r'name="twitter:card"')):
    if not re.search(pat,s):prob('meta',f'{f}: missing {need}')
  c=re.search(r'<link rel="canonical" href="([^"]+)"',s)
  if c and c.group(1) not in(BASE+f,BASE+('' if f=='index.html' else f)):prob('meta',f'{f}: canonical points to {c.group(1)}')
  if 'class="foot-links"' not in s:prob('footer',f'{f}: footer links missing (run python3 tools/footer.py)')
  body=re.sub(r'<script.*?</script>','',s,flags=re.S)
  if len(re.findall(r'<h1[\s>]',body))!=1 and f!='index.html':prob('headings',f'{f}: has {len(re.findall(r"<h1[\s>]",body))} h1 headings')
  for im in re.findall(r'<img [^>]*>',body):
    if ' alt=' not in im:prob('a11y',f'{f}: image without alt: {im[:80]}')
    if f!='index.html' and not (' width=' in im and ' height=' in im):prob('cls',f'{f}: image without width/height: {im[:80]}')
  sk=re.sub(r'^place-|(-(hours|contact|location|social|media|documents|related))?\.html$','',f)
  for blk in re.findall(r'<script type="application/ld\+json">(.*?)</script>',s,re.S):
    if re.search(r'XXX|Verified Street|verified-page-url|example\.com|lorem',blk,re.I):prob('schema',f'{f}: placeholder text in JSON-LD')
    try:walk(json.loads(blk),f,sk)
    except Exception as e:prob('schema',f'{f}: JSON-LD does not parse: {e}')
for t,fs in titles.items():
  if len(fs)>1:prob('meta',f'duplicate title "{t[:60]}" on {", ".join(fs[:3])}')
# 10. Re-verification reminder: verified facts older than 90 days
import datetime
for k,v in VER.items():
  if k.startswith('_'):continue
  try:
    age=(datetime.date.today()-datetime.date.fromisoformat(v.get('verified',''))).days
    if age>90:W.append(f'{k}: verified {age} days ago, re-check its sources')
  except Exception:prob('verify',f'tools/verified.json {k}: missing or bad verified date')
# 7
if '--lighthouse' in sys.argv:
  lh=shutil.which('lighthouse') or '/workspace/hanceville/landing/tools/node_modules/.bin/lighthouse'
  for u in ['https://shoplocalhanceville.github.io/','https://shoplocalhanceville.github.io/place-cut-n-up-barber-and-style.html']:
    r=subprocess.run([lh,u,'--quiet','--output=json','--output-path=stdout','--chrome-flags=--headless=new --no-sandbox','--only-categories=performance,accessibility,best-practices,seo'],capture_output=True,text=True,timeout=300)
    try:
      c=json.loads(r.stdout)['categories'];sc={k:round((v['score'] or 0)*100) for k,v in c.items()}
      if not Q:print('lighthouse',u,sc)
      if sc['performance']<90 or min(v for k,v in sc.items() if k!='performance')<95:prob('speed',f'{u} {sc}')
    except Exception as e:prob('speed',f'lighthouse failed on {u}: {e}')
if not Q:
  for w in W:print('warning:',w)
for p in P:print(p)
print(f'audit: {len(P)} problem(s), {len(htmls)} pages checked')
sys.exit(1 if P else 0)
