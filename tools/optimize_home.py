#!/usr/bin/env python3
"""Move inline base64 JPEG images out of index.html into small WebP files.
Idempotent: safe to rerun after any edit that pastes data: images back in.
Output: img/home/<hash>.webp (max 256px on the long side, quality 80)."""
import re,base64,hashlib,io,os,sys
from PIL import Image
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
os.makedirs('img/home',exist_ok=True)
s=open('index.html').read(); before=len(s); cache={}
def conv(m):
  b=m.group(2)
  if b in cache: return cache[b]
  raw=base64.b64decode(b); h=hashlib.sha1(raw).hexdigest()[:12]; p=f'img/home/{h}.webp'
  if not os.path.exists(p):
    im=Image.open(io.BytesIO(raw)); im=im.convert('RGBA' if im.mode in('RGBA','LA','P') else 'RGB')
    im.thumbnail((256,256)); im.save(p,'WEBP',quality=80,method=6)
  cache[b]=p; return p
def svg(m):
  raw=base64.b64decode(m.group(1))
  if len(raw)<1500: return m.group(0)  # tiny icons stay inline
  h=hashlib.sha1(raw).hexdigest()[:12]+('-w' if b'fill:#fff' in raw else ''); p=f'img/home/{h}.svg'  # -w = white artwork, homepage JS gives it a dark backdrop
  if not os.path.exists(p): open(p,'wb').write(raw)
  cache[m.group(1)]=p; return p
s=re.sub(r'data:image/svg\+xml;base64,([A-Za-z0-9+/=]+)',svg,s)
s=re.sub(r'data:image/(jpeg|jpg|png|webp);base64,([A-Za-z0-9+/=]+)',conv,s)
# lazy-load and async-decode every static <img> below the header that lacks it
s=re.sub(r'<img(?![^>]*\bloading=)([^>]*src="img/home/)',r'<img loading="lazy" decoding="async"\1',s)
open('index.html','w').write(s)
print(f'index.html {before:,} -> {len(s):,} bytes, {len(cache)} images extracted')
