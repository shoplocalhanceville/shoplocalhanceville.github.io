# Lucide icons (ISC license, https://lucide.dev, lucide-static v1.59.0). Inlined as an SVG sprite.
import re,os
SRC=os.environ.get('SLH_LUCIDE_DIR') or os.path.join(os.path.dirname(os.path.abspath(__file__)),'node_modules','lucide-static','icons')
SRC=SRC.rstrip('/')+'/'
NAMES=['phone','mail','map-pin','navigation','globe','calendar','calendar-plus','landmark','users','droplet','tornado','clipboard-list','file-text','scale','scroll-text','piggy-bank','video','tree-pine','book-open','flame','shield','construction','building-2','utensils','shopping-bag','store','school','graduation-cap','heart-handshake','smile','newspaper','house','menu','x','sun','moon','search','trophy','clock','ticket','chevron-down','external-link','triangle-alert','wrench','map','languages','download','info','baby','apple','flag','heart-pulse','megaphone','cloud-sun','map-pinned','user-round','star','siren','lightbulb','traffic-cone','list-checks','hand-heart','life-buoy','arrow-right','thumbs-up','send','circle-help']
VER='15'
def _inner(n):
  s=open(SRC+n+'.svg').read()
  s=re.sub(r'<!--.*?-->','',s,flags=re.S)
  return re.sub(r'\s+',' ',re.search(r'<svg[^>]*>(.*)</svg>',s,re.S).group(1)).strip()
def sprite(names=None):
  names=names or NAMES
  return '<svg xmlns="http://www.w3.org/2000/svg" style="display:none" aria-hidden="true"><defs>'+''.join(f'<symbol id="i-{n}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{_inner(n)}</symbol>' for n in names)+'</defs></svg>'
def I(n,cls='ic'):
  assert n in NAMES,n
  return f'<svg class="{cls}" aria-hidden="true" focusable="false"><use href="icons.svg#i-{n}"></use></svg>'
