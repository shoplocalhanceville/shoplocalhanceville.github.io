# Site Guide: Hanceville Entertainment & Shopping

Live site: https://shoplocalhanceville.github.io/ (GitHub Pages, served through Fastly's CDN).
Repo: shoplocalhanceville/shoplocalhanceville.github.io, branch `main`. Pages deploy a minute or two after each push.

## How the site is put together

| Layer | Files | Who edits it |
|---|---|---|
| Homepage | `index.html` (inline data `window.SLH_LISTINGS`, inline app scripts, its own baseline CSP) | Hourly refresh scripts and audit passes |
| Section pages | `businesses.html`, `shops.html`, `eats.html`, `nonprofits.html`, `city.html`, `departments.html`, `council.html`, `directory.html`, `resources.html`, `wallace.html`, `events.html`, `news.html`, `fun.html` | Static shells. `app.js` fills them from the matching `.json` file |
| Section data | `*.json` with the same name as the page | Refresh scripts |
| Stories | `story-<id>.html`, built from `news.json` entries | Refresh scripts |
| Listing pages | `place-<slug>.html` (one per listing), `category-<slug>.html` (one per category), `places.html` (A to Z) | **Generated** by `tools/build_places.py`. Never hand edit |
| Calendar files | `ics/` | Refresh scripts |
| Images | `logos/*.webp` (listing logos), `img/home/*` (homepage images moved out of the HTML), `img/council/*` | `tools/optimize_home.py`, logo fetchers |
| Styles and scripts | `style.css`, `place.css`, `app.js`, `place.js` (Facebook click to load), `sw.js` (service worker) | By hand |

## Listing pages (the spiderweb)

`tools/build_places.py` merges every listing from the section JSON files and from `window.SLH_LISTINGS`, matched by slug
(lowercase, every run of non letters and digits becomes `-`). Section JSON wins when both have a value.

Each `place-<slug>.html` is a mini homepage:

* Breadcrumbs: Home > All Places > Category > Listing (also in JSON-LD).
* Hero with logo, category pill and call, directions, website and Facebook buttons.
* A sticky section bar linking to About, Hours, Contact, Location and Directions, Social, Photos and Related.
  A section is only written when its data exists, so no tab ever opens an empty block.
* Social: a click-to-load Facebook Page Plugin (timeline tab). Nothing loads from Facebook until the visitor taps
  "Show latest Facebook posts". The page CSP allows only `frame-src https://www.facebook.com`.
* Related: up to 8 listings in the same category, "Also on this street" (same street name), previous and next
  within the category, links to the category hub and to the A to Z hub, and "Also listed on" links back to section pages.

Inbound links: every card on every section page has a "See full page" button (`app.js`, `card()`), homepage cards and
the homepage profile modal have "See full page", and the homepage "See listing" featured buttons go straight to the page.
Categories in `SKIP_CATS` (Fun Facts, Sweet Tea Jokes, Social Media) are not places and get no page. The same list lives
in the homepage JS; keep them in sync.

## Regular commands (run from the repo root)

```
python3 tools/optimize_home.py   # after anything pastes base64 images into index.html
python3 tools/clean_listings.py  # after the homepage data changes (dashes, junk records)
python3 tools/build_places.py    # after ANY data change: rebuilds listing pages, hubs and sitemap entries
python3 tools/audit.py           # must print "0 problem(s)" before you push
node tools/crawl.js <base> out.json   # full click crawl, desktop and mobile (about 12 minutes for the whole site)
python3 /workspace/hanceville/landing/monitor.py   # live health and security monitor
```

Always `git pull --rebase` before committing. Small commits, never force push.

## Speed setup

* Homepage went from 14 MB to about 0.5 MB by moving 440 inline base64 images into `img/home/` (WebP, max 256 px).
* Every static image has width, height, `loading="lazy"` and `decoding="async"`. Logos are WebP.
* `sw.js`: network first for HTML and JSON (hourly updates always show), cache first for versioned assets.
* Cache busting: bump `?v=` on `app.js`, `style.css` and `place.css` when they change. `sed` across `*.html` and
  `tools/build_places.py`.
* CDN: GitHub Pages already serves through Fastly with HTTP/2 and gzip. Cloudflare's free plan would add Brotli,
  longer cache rules and real `_headers` support, but it needs a custom domain pointed at it. Documented only; no change made.
* Free monitoring without accounts: PageSpeed Insights web page (https://pagespeed.web.dev/) and
  `python3 tools/audit.py --lighthouse`.
