#!/usr/bin/env python3
"""Health and security monitor for the live Hanceville Entertainment & Shopping site.

Usage:  python3 tools/monitor.py [--no-external] [--quiet] [--days N] [--budget SECONDS] [--workers N] [--retries N]
Exit code 0 = all good, 1 = problems found, 2 = monitor itself failed.
Speed and noise rules (added Nov 9 2026 so a run stays well under 5 minutes):
  * every request has a connect timeout and a total timeout; transient failures (timeouts, connection errors,
    HTTP 429/5xx) are retried with exponential backoff and jitter
  * an internal link that is already a fetched live file is not fetched a second time
  * links on other sites that time out, fail DNS or TLS, or refuse the connection are WARNINGS, never failures.
    A host that fails 3 times in a row is skipped for the rest of the run. Only a definite 404 or 410 from another
    site is a failure. Internal 404s, 5xx and timeouts (after retries) are still failures.
  * links are read out of data fields with a URL finder, so notes such as "https://x.com/ (checked Nov. 6, 2026)"
    check only the URL
  * the external link phase stops starting new requests when --budget seconds (default 200) of total run time are
    used up; whatever was not reached is reported as info, not as a failure
Checks:
  1. HTTP 200 for every page in the sitemap plus core assets
  2. Integrity: every tracked file on the live site is byte-identical to origin/main
  3. CSP meta tag present and unchanged on every page; no external <script src>; no unexpected inline scripts
  4. Broken links: internal links and data links (website, facebook, source, url, news sources, score sources) on the live site
  5. GitHub: commits in the last N days not authored by CharlieGamedevelop, open Dependabot / secret scanning alerts
"""
import sys,json,re,hashlib,subprocess,time,random,html as _html,threading,urllib.parse,concurrent.futures as cf
T0=time.time()
REPO='shoplocalhanceville/shoplocalhanceville.github.io'
OWNER='CharlieGamedevelop'
BASE='https://shoplocalhanceville.github.io/'
# v15 CSP: adds api.weather.gov (NWS alerts), manifest-src and worker-src (installable app). map.html also allows the OpenStreetMap tile host.
# If GOATCOUNTER_CODE is set in build.py, https://CODE.goatcounter.com is added to img-src and connect-src.
import os as _os
_gc=''
try:
  _here=_os.path.dirname(_os.path.abspath(__file__))
  _bp=next(p for p in (_os.path.join(_here,'site-build','build.py'),_os.path.join(_here,'build.py')) if _os.path.exists(p))
  _m=re.search(r'^GOATCOUNTER_CODE="([a-z0-9-]*)"',open(_bp).read(),re.M)
  if _m and _m.group(1):_gc=' https://'+_m.group(1)+'.goatcounter.com'
except Exception:pass
def EXPECTED(p):
  img=(' https://tile.openstreetmap.org' if p=='map.html' else '')+_gc
  return f"default-src 'self'; script-src 'self' 'sha256-/fikJO3y8/FfvJxadqacMFRHk8y+I5ng+WE0NyQXczI='; style-src 'self' 'unsafe-inline'; img-src 'self' data:{img}; connect-src 'self' https://api.weather.gov{_gc}; font-src 'self'; object-src 'none'; base-uri 'self'; form-action 'self'; manifest-src 'self'; worker-src 'self'; upgrade-insecure-requests"
EXPECTED_CSP=EXPECTED('index.html')
# The deployed pages still use the v14 policy (v15 was never shipped); accept either.
V14_CSP="default-src 'self'; script-src 'self' 'sha256-/fikJO3y8/FfvJxadqacMFRHk8y+I5ng+WE0NyQXczI='; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self'; font-src 'self'; object-src 'none'; base-uri 'self'; form-action 'self'; upgrade-insecure-requests"
# Generated listing pages (tools/build_places.py, Oct 24 2026): v14 policy plus frame-src for the click-to-load Facebook Page Plugin.
PLACE_CSP=V14_CSP.replace("font-src 'self'; ","font-src 'self'; frame-src https://www.facebook.com; ")
INDEX_BASE_CSP="object-src 'none'; base-uri 'self'; form-action 'self'; upgrade-insecure-requests"  # homepage baseline meta CSP (inline data scripts)
ALLOWED_SRC=r'^(app\.js|place\.js|map\.js|data\.js|data-es\.js|vendor/leaflet/leaflet\.js|vendor/goatcounter/count\.js)(\?v=[0-9.]+)?$'

UA='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36 HancevilleMonitor/1.0'
args=sys.argv[1:];EXT='--no-external' not in args;QUIET='--quiet' in args
def _opt(name,default,cast=int):return cast(args[args.index(name)+1]) if name in args else default
DAYS=_opt('--days',7)
BUDGET=_opt('--budget',200,float)      # seconds of total run time after which the external link phase stops starting new requests
WORKERS=_opt('--workers',32)           # parallel requests
RETRIES=_opt('--retries',2)            # extra attempts after the first for transient failures
CONNECT_T=_opt('--connect-timeout',8,float);TOTAL_T=_opt('--timeout',20,float)
problems=[];warnings=[];info=[]
CURL_ERR={6:'DNS lookup failed',7:'connection refused',28:'timed out',35:'TLS handshake failed',51:'TLS certificate problem',52:'empty reply',55:'send error',56:'connection reset',60:'TLS certificate problem',47:'too many redirects',3:'malformed URL'}
def curl_once(url,head=False,timeout=None,want_body=True):
  """One request. Returns (http_code, body, final_url, error). code 0 means no HTTP answer and error says why."""
  timeout=timeout or TOTAL_T
  cmd=['curl','-sL','--connect-timeout',str(CONNECT_T),'-m',str(timeout),'--max-redirs','8','-A',UA,'-o','-' if want_body else '/dev/null','-w','\n__META__%{http_code} %{url_effective}',url]
  if head:cmd[1:1]=['-I']
  r=subprocess.run(cmd,capture_output=True)
  body,_,meta=r.stdout.rpartition(b'\n__META__')
  code,_,eff=meta.decode(errors='ignore').partition(' ')
  code=int(code or 0)
  err=None if code else CURL_ERR.get(r.returncode,'curl error %d'%r.returncode)
  return code,body,eff,err
def backoff(i):time.sleep(min(8,(2**i))*(0.6+random.random()*0.8))
def curl(url,head=False,timeout=None,want_body=True,retries=None,retry_codes=(0,429,500,502,503,504)):
  """Request with retries and exponential backoff for transient failures. Returns (code, body, final_url, error)."""
  n=RETRIES if retries is None else retries
  for i in range(n+1):
    code,body,eff,err=curl_once(url,head,timeout,want_body)
    if code not in retry_codes or i==n:return code,body,eff,err
    backoff(i)
def gh(path):
  r=subprocess.run(['gh','api',path,'--paginate'],capture_output=True,text=True)
  if r.returncode!=0:return None,(r.stderr or r.stdout).strip()[:200]
  try:return json.loads(r.stdout),None
  except Exception:
    try:return json.loads('['+r.stdout.replace('][',',').strip('[]')+']'),None
    except Exception as e:return None,str(e)
def say(*a):
  if not QUIET:print(*a,flush=True)
# ---- repo file list and hashes (from GitHub, origin/main)
tree,err=gh(f'repos/{REPO}/git/trees/main?recursive=1')
if not tree:print('MONITOR ERROR: cannot read repo tree:',err);sys.exit(2)
files=[t for t in tree['tree'] if t['type']=='blob' and not t['path'].startswith('.github/')]
say(f'Repo main has {len(files)} files')
def git_blob_sha(data):return hashlib.sha1(b'blob %d\0'%len(data)+data).hexdigest()
# ---- 1+2: fetch every tracked file live and compare
def check_file(t):
  path=t['path'];url=BASE+urllib.parse.quote(path)
  code,body,_,_e=curl(url)
  same=(git_blob_sha(body)==t['sha']) if code==200 else None
  if same is False:
    # a CDN edge can serve a copy from before the latest deploy: look once more with a cache buster before calling it a mismatch
    time.sleep(1+random.random());c2,b2,_,_e=curl(url+('&' if '?' in url else '?')+'nocache=%d'%int(time.time()),retries=0)
    if c2==200 and git_blob_sha(b2)==t['sha']:body,same=b2,True
  return path,code,body,same
live={};okpaths=set()
with cf.ThreadPoolExecutor(WORKERS) as ex:
  for path,code,body,same in ex.map(check_file,[f for f in files if f['path']!='README.md']):
    if code!=200:problems.append(f'HTTP {code} for {path}')
    elif not same:problems.append(f'INTEGRITY: live {path} differs from the committed version on main')
    else:okpaths.add(path)
    live[path]=body
say(f'Checked {len(live)} live files against main')
pages=[p for p in live if p.endswith('.html') and not re.fullmatch(r'google[0-9a-f]+\.html',p)
         and not (b'http-equiv="refresh"' in live[p] and b'content="noindex"' in live[p])]  # removed stories kept as noindex redirect stubs have no CSP on purpose
root_code,_,_,_e=curl(BASE)
if root_code!=200:problems.append(f'HTTP {root_code} for site root')
# ---- 3: CSP and scripts
for p in pages:
  h=live[p].decode('utf8','ignore')
  m=re.search(r'http-equiv="Content-Security-Policy" content="([^"]+)"',h)
  if not m:problems.append(f'CSP missing on {p}')
  elif m.group(1)!=EXPECTED(p) and m.group(1)!=V14_CSP and not (p=='index.html' and m.group(1)==INDEX_BASE_CSP) and not (re.match(r'^(place-|category-|places\.html|about\.html|contact\.html|privacy\.html|terms\.html|sources\.html|sitemap\.html|hanceville-library\.html|map-view\.html)',p) and m.group(1)==PLACE_CSP):problems.append(f'CSP changed on {p}: {m.group(1)[:120]}')
  for src in re.findall(r'<script[^>]*\ssrc="([^"]+)"',h):
    if not re.match(ALLOWED_SRC,src):problems.append(f'Unexpected script src on {p}: {src}')
  inl=[s for s in re.findall(r'<script(?![^>]*\ssrc=)([^>]*)>',h) if 'application/ld+json' not in s]
  # Homepage (since commit bf275b5, Oct 23 2026) ships its own inline app and data scripts under the baseline meta CSP; only external script src is policed there.
  if p=='index.html' and m and m.group(1)==INDEX_BASE_CSP:
    if not inl:problems.append('index.html has no inline scripts (theme/app script missing)')
  elif len(inl)!=1:problems.append(f'{p} has {len(inl)} inline executable scripts (expected 1, the theme script)')
  if re.search(r'''(src|href)="http://''',h):problems.append(f'Mixed content (http://) on {p}')
# ---- 4: links
links=set()
URLRX=re.compile(r"https?://[^\s<>\"'`;,]+")
def urls_in(v):
  """Every http(s) URL inside a data value. Notes like 'https://x.com/ (checked Nov. 6, 2026)' yield only the URL."""
  if not isinstance(v,str):return []
  return [u.rstrip('.:)]}') for u in URLRX.findall(_html.unescape(v))]
malformed={}
for p in pages:
  for href in re.findall(r'href="([^"#][^"]*)"',live[p].decode('utf8','ignore')):
    href=href.replace('&amp;','&')
    if re.search(r'\s',href) and re.match(r'https?://',href):
      # a note such as "(checked Nov. 9, 2026)" got glued into the link: a real bug on our own page, not an outside problem
      malformed.setdefault(href.split()[0],set()).add(p)
      href=href.split()[0]
    links.add(urllib.parse.urljoin(BASE+p,href))
if malformed:
  _n=sorted({p for ps in malformed.values() for p in ps})
  problems.append(f'Malformed links (a note such as "(checked Nov. 9, 2026)" is inside the href) in {len(_n)} page(s): {len(malformed)} links, e.g. {sorted(malformed)[0]} on {_n[0]}. Fix: rebuild with tools/build_places.py')
for p in live:
  if p.endswith('.json') and not p.startswith('.'):
    try:data=json.loads(live[p])
    except Exception:problems.append(f'Invalid JSON: {p}');continue
    if isinstance(data,list):
      for e in data:
        for k in ('website','facebook','source','url'):
          if isinstance(e,dict) and e.get(k):links.update(urls_in(e[k]))
        if isinstance(e,dict) and e.get('logo'):links.add(BASE+e['logo'])
        if isinstance(e,dict):
          for s in e.get('sources') or []:
            if isinstance(s,dict) and s.get('url'):links.update(urls_in(s['url']))
    if isinstance(data,dict):
      for g in data.get('games') or []:
        if isinstance(g,dict) and isinstance(g.get('source'),dict) and g['source'].get('url'):links.update(urls_in(g['source']['url']))
links={l for l in links if l.startswith('http')}
fbblocked=[]
links={l for l in links if not re.search(r"[+'()]|encodeURIComponent|esc\(",l[len(BASE):] if l.startswith(BASE) else '')}  # skip JS string fragments
internal=[l for l in links if l.startswith(BASE)];external=sorted(l for l in links if not l.startswith(BASE))
def known_ok(u):
  """True when an internal link points at a file this run already fetched and verified (no second request needed)."""
  pth=urllib.parse.unquote(urllib.parse.urlsplit(u).path.lstrip('/'))
  return pth in okpaths or (pth=='' and root_code==200)
HOST_FAILS={};HOST_LOCK=threading.Lock();HOST_LIMIT=3
def host_of(u):return urllib.parse.urlsplit(u).netloc.lower()
def chk_internal(u):
  if known_ok(u):return u,200,u,None
  c,_,eff,err=curl(u)
  return u,c,eff,err
def chk_external(u):
  """Returns (url, code, final_url, error). code 0 with an error text means no HTTP answer (timeout, DNS, TLS, refused)."""
  h=host_of(u)
  with HOST_LOCK:
    if HOST_FAILS.get(h,0)>=HOST_LIMIT:return u,0,u,'skipped, host failed %d times in a row'%HOST_LIMIT
  if time.time()-T0>BUDGET:return u,-1,u,'time budget used up'
  c,_,eff,err=curl(u,want_body=False,retries=min(1,RETRIES))
  if c in(400,403,405,999):  # some sites refuse the first request from a script: try once more as a plain GET
    c2,_,eff2,err2=curl(u,want_body=False,retries=0)
    if c2 and c2!=c:c,eff,err=c2,eff2,err2
  with HOST_LOCK:
    HOST_FAILS[h]=HOST_FAILS.get(h,0)+1 if c==0 else 0
  return u,c,eff,err
unchecked=[]
with cf.ThreadPoolExecutor(WORKERS) as ex:
  for u,c,eff,err in ex.map(chk_internal,internal):
    if c!=200:problems.append(f'Broken internal link ({c or err}): {u}')
  if EXT:
    for u,c,eff,err in ex.map(chk_external,external):
      fb='facebook.com' in u
      if c==-1:unchecked.append(u)
      elif c in(404,410):problems.append(f'Broken external link ({c}): {u}')
      elif c==0:warnings.append(f'External link did not answer ({err}): {u}')
      elif c>=500:warnings.append(f'External link server error ({c}): {u}')
      elif c in(400,401,403,429,999):
        if fb:fbblocked.append(u)
        else:warnings.append(f'External link blocks automated checks ({c}), check by hand: {u}')
if unchecked:info.append(f'{len(unchecked)} external links were not checked because the {BUDGET:.0f} second time budget ran out (they are checked on the next run)')
if fbblocked:info.append(f'{len(fbblocked)} Facebook links answer bots with 400 as usual (not counted as broken)')
say(f'Checked {len(internal)} internal and {len(external) if EXT else 0} external links')
# ---- 5: GitHub
import datetime
since=(datetime.datetime.now(datetime.timezone.utc)-datetime.timedelta(days=DAYS)).strftime('%Y-%m-%dT%H:%M:%SZ')
commits,err=gh(f'repos/{REPO}/commits?since={since}&per_page=100')
if commits is None:warnings.append(f'Could not list commits: {err}')
else:
  for c in commits:
    login=(c.get('author') or {}).get('login');cl=(c.get('committer') or {}).get('login')
    if login!=OWNER:problems.append(f"Commit {c['sha'][:7]} by {login or c['commit']['author']['email']} (not {OWNER}): {c['commit']['message'][:70]}")
  info.append(f'{len(commits)} commits in the last {DAYS} days, all checked')
for kind,path in (('Dependabot',f'repos/{REPO}/dependabot/alerts?state=open'),('Secret scanning',f'repos/{REPO}/secret-scanning/alerts?state=open'),('Code scanning',f'repos/{REPO}/code-scanning/alerts?state=open')):
  a,err=gh(path)
  if a is None:
    if err and ('disabled' in err.lower() or 'not enabled' in err.lower() or 'no analysis' in err.lower() or '404' in err):info.append(f'{kind}: not enabled for this repo ({err[:80]})')
    else:warnings.append(f'{kind}: could not check ({err[:120]})')
  elif a:problems.append(f'{kind}: {len(a)} open alert(s)')
  else:info.append(f'{kind}: no open alerts')
pub,_=gh(f'repos/{REPO}/pages')
if pub and pub.get('status') not in ('built',None):warnings.append(f"GitHub Pages status: {pub.get('status')}")
# ---- summary
print('='*60);print('Hanceville site monitor:',BASE)
for i in info:print('  info:',i)
for w in warnings:print('  WARN:',w)
for p in problems:print('  PROBLEM:',p)
print(f'RESULT: {"FAIL" if problems else "OK"}  ({len(problems)} problems, {len(warnings)} warnings, runtime {time.time()-T0:.0f}s)')
sys.exit(1 if problems else 0)
