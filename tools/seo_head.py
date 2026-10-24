#!/usr/bin/env python3
"""Idempotent SEO pass for every page. Run from repo root before each commit:
    python3 tools/seo_head.py          # fix + check
    python3 tools/seo_head.py --check  # check only, exit 1 on problems
Adds geo and hreflang tags when missing, points the publisher logo at logo.png,
makes sure story pages carry NewsArticle JSON-LD, and keeps sitemap.xml complete."""
import glob, json, re, sys, datetime, html, subprocess
BASE = "https://shoplocalhanceville.github.io/"
TODAY = datetime.date.today().isoformat()
CHECK = "--check" in sys.argv
LOGO = {"@type": "ImageObject", "url": BASE + "logo.png", "width": 512, "height": 512}
ORG = {"@type": "Organization", "@id": BASE + "#org", "name": "Hanceville Entertainment & Shopping",
       "alternateName": "Shop Local Alabama", "url": BASE, "logo": LOGO, "image": BASE + "og-image.jpg",
       "sameAs": ["https://www.facebook.com/ShopLocalAlabama"],
       "areaServed": [{"@type": "City", "name": "Hanceville, Alabama"}, {"@type": "AdministrativeArea", "name": "Cullman County, Alabama"}]}
GEO = ('<meta name="geo.region" content="US-AL"><meta name="geo.placename" content="Hanceville, Cullman County, Alabama">'
       '<meta name="geo.position" content="34.0614;-86.7633"><meta name="ICBM" content="34.0614, -86.7633">')
REQ = ['<title>', 'name="description"', 'rel="canonical"', 'name="robots"', 'name="geo.region"', 'name="geo.placename"',
       'name="geo.position"', 'name="ICBM"', 'og:type', 'og:url', 'og:title', 'og:description', 'property="og:image"',
       'og:image:width', 'og:image:height', 'og:image:alt', 'og:site_name', 'og:locale" content="en_US',
       'twitter:card" content="summary_large_image', 'twitter:title', 'twitter:description', 'name="twitter:image"',
       'twitter:image:alt', 'hreflang', 'theme-color', 'name="viewport"']
problems = []; pages = []; titles = {}

def fix_org(node):
    if isinstance(node, dict):
        if node.get("@type") == "Organization":
            node["logo"] = LOGO; node.pop("founder", None)
        for v in node.values(): fix_org(v)
    elif isinstance(node, list):
        for v in node: fix_org(v)

for f in sorted(glob.glob("*.html")):
    if f.startswith("google"): continue
    pages.append(f)
    s = open(f, encoding="utf-8").read(); head, sep, rest = s.partition("</head>"); orig = head
    url = BASE if f == "index.html" else BASE + f
    if 'name="geo.position"' not in head:
        head = re.sub(r'<meta name="geo\.(region|placename)"[^>]*>\n?', '', head)
        head = head.replace('<meta name="theme-color"', GEO + '\n<meta name="theme-color"', 1)
    if 'hreflang' not in head:
        head = head.replace('<link rel="icon"', f'<link rel="alternate" hreflang="en" href="{url}"><link rel="alternate" hreflang="x-default" href="{url}">\n<link rel="icon"', 1)
    def ld_fix(m):
        try: g = json.loads(m.group(2))
        except Exception as e: problems.append(f"{f}: bad JSON-LD {e}"); return m.group(0)
        fix_org(g); return m.group(1) + json.dumps(g, ensure_ascii=False) + m.group(3)
    head = re.sub(r'(<script type="application/ld\+json">)(.*?)(</script>)', ld_fix, head, flags=re.S)
    if f.startswith("story-") and '"NewsArticle"' not in head:
        t = html.unescape(re.search(r'<h1>(.*?)</h1>', rest, re.S).group(1))
        d = re.search(r'<meta name="description" content="([^"]*)"', head).group(1)
        dt = re.search(r'<time datetime="([0-9-]+)"', rest); dt = dt.group(1) if dt else TODAY
        art = {"@context": "https://schema.org", "@graph": [{"@type": "NewsArticle", "headline": t, "description": html.unescape(d),
               "datePublished": dt, "dateModified": dt, "inLanguage": "en-US", "mainEntityOfPage": url, "url": url,
               "image": [BASE + "og-image.jpg"], "author": {"@id": BASE + "#org"}, "publisher": {"@id": BASE + "#org"}}, ORG]}
        head += '<script type="application/ld+json">' + json.dumps(art, ensure_ascii=False) + '</script>\n'
    for r in REQ:
        if r not in head: problems.append(f"{f}: missing {r}")
    if f'rel="canonical" href="{url}"' not in head: problems.append(f"{f}: canonical not {url}")
    if f'property="og:url" content="{url}"' not in head: problems.append(f"{f}: og:url not {url}")
    if re.search(r'(src|href|action)="http://', s): problems.append(f"{f}: mixed content")
    titles.setdefault(re.search(r'<title>(.*?)</title>', head).group(1), []).append(f)
    if head != orig and not CHECK: open(f, "w", encoding="utf-8").write(head + sep + rest)

for t, fs in titles.items():
    if len(fs) > 1: problems.append(f"duplicate title {t}: {fs}")

sm = open("sitemap.xml", encoding="utf-8").read(); sm0 = sm
changed = set(subprocess.run(["git", "diff", "--name-only", "HEAD"], capture_output=True, text=True).stdout.split())
for f in pages:
    url = BASE if f == "index.html" else BASE + f
    if f"<loc>{url}</loc>" not in sm:
        pr = "0.6" if f.startswith("story-") else "0.8"
        sm = sm.replace("</urlset>", f"  <url><loc>{url}</loc><lastmod>{TODAY}</lastmod><changefreq>{'monthly' if f.startswith('story-') else 'weekly'}</changefreq><priority>{pr}</priority></url>\n</urlset>")
    elif f in changed:
        sm = re.sub(r'(<loc>' + re.escape(url) + r'</loc><lastmod>)[0-9-]+', r'\g<1>' + TODAY, sm)
for loc in re.findall(r"<loc>([^<]+)</loc>", sm):
    p = loc[len(BASE):] or "index.html"
    if p not in pages: problems.append(f"sitemap lists missing page {p}")
if sm != sm0 and not CHECK: open("sitemap.xml", "w", encoding="utf-8").write(sm)
robots = open("robots.txt").read().split()
if robots != ["User-agent:", "*", "Allow:", "/", "Sitemap:", BASE + "sitemap.xml"]: problems.append("robots.txt changed")
print("\n".join(problems) or f"SEO OK: {len(pages)} pages")
sys.exit(1 if problems else 0)
