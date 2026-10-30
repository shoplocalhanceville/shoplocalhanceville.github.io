#!/usr/bin/env python3
"""Put the same footer navigation (About, Contact, Privacy Policy, Terms of Use,
Sources & References, Sitemap) on every page. Safe to run again and again: the block
between the foot-links markers is replaced, never duplicated. build_places.py runs this."""
import glob,os,re
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
NAV=('<!--foot-links--><nav class="foot-links" aria-label="Footer navigation"><ul>'
 '<li><a href="about.html">About</a></li><li><a href="contact.html">Contact</a></li>'
 '<li><a href="privacy.html">Privacy Policy</a></li><li><a href="terms.html">Terms of Use</a></li>'
 '<li><a href="sources.html">Sources &amp; References</a></li><li><a href="sitemap.html">Sitemap</a></li>'
 '</ul></nav><!--/foot-links-->')
n=0
for f in glob.glob('*.html'):
  if f.startswith('google'):continue
  s=open(f,encoding='utf-8').read();o=s
  s=re.sub(r'(?:\n[ \t]*)*<!--foot-links-->.*?<!--/foot-links-->\n?','\n',s,flags=re.S)
  if '<p class="foot-note">' in s:s=s.replace('<p class="foot-note">',NAV+'\n <p class="foot-note">',1)
  elif '</footer>' in s:s=s.replace('</footer>',NAV+'\n</footer>',1)
  else:print('no footer in',f);continue
  if s!=o:open(f,'w',encoding='utf-8').write(s);n+=1
print('footer links on',n,'changed pages')
