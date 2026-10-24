#!/usr/bin/env python3
"""Copy hygiene for window.SLH_LISTINGS in index.html (homepage directory data).
Removes records that are research notes or section headings instead of real listings,
strips internal labels, replaces em and en dashes, and rewrites placeholder blurbs
without adding any new facts. Removed records are written to docs/audit/removed-listings.json
for owner review. Idempotent."""
import re,json,os
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
JUNK_NAME=re.compile(r'^(EVENTS & VENUES|TRANSPORTATION & INDUSTRY|FAITH \u2014 |MEDIA & INFORMATION|NEW RULE APPLIED|Pets & Agriculture \u2014 |Final Tally|Wallace State program pages with confirmed social links$|Candidate noted|Entities surfaced)')
JUNK_DESC=re.compile(r'verify before publish',re.I)
def dash(t,name=False):
  if not t:return t
  t=re.sub(r'(?<=\w)[\u2013](?=\w)','-',t)          # K–12, A–Z
  t=t.replace(' \u2014 ',', ' ).replace('\u2014',', ').replace(' \u2013 ',', ').replace('\u2013','-')
  return re.sub(r' {2,}',' ',t).replace(', ,',',')
s=open('index.html').read()
m=re.search(r'(window\.SLH_LISTINGS = )(\[.*?\]);\n',s,re.S);d=json.loads(m.group(2))
keep,removed=[],[]
for x in d:
  if JUNK_NAME.match(x['name']) or JUNK_DESC.search(x.get('description','')):removed.append(x);continue
  x['name']=re.sub(r'\s*\u2014\s*retail anchor$','',x['name'])
  ph=re.match(re.escape(x['name'])+r' \u2014 (.+?) in (.+?), Alabama\.$',x.get('description',''))
  if ph:x['description']=f"{x['name']} appears in our {ph.group(1)} listings for {ph.group(2)}. Check the contact links on this listing for current hours and details before you visit."
  for k in('name','description','descEs','aka'):
    if isinstance(x.get(k),str):x[k]=dash(x[k])
  keep.append(x)
s=s[:m.start(2)]+json.dumps(keep,ensure_ascii=False,separators=(',',':'))+s[m.end(2):]
s=s.replace('"Nombre A\u2013Z"','"Nombre de la A a la Z"').replace('>Name A\u2013Z<','>Name A to Z<').replace(' \u2014 ',', ')
open('index.html','w').write(s)
os.makedirs('docs/audit',exist_ok=True)
old=json.load(open('docs/audit/removed-listings.json')) if os.path.exists('docs/audit/removed-listings.json') else []
names={r['name'] for r in old};old+=[r for r in removed if r['name'] not in names]
for r in old:r.pop('logo',None)
json.dump(old,open('docs/audit/removed-listings.json','w'),ensure_ascii=False,indent=1)
print(len(d),'->',len(keep),'removed',[r['name'] for r in removed])
