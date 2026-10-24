# Audit handoff (Oct 24, 2026)

## Done this run
1. Before baseline in `docs/audit/before/` (Lighthouse JSON for 6 pages, mobile and desktop, plus `crawl.json`).
2. Homepage weight: 14 MB to 0.5 MB (440 inline base64 images moved to `img/home/`). Mobile performance 28 to 98.
3. Spiderweb: 719 `place-*.html` listing pages, 66 `category-*.html` hubs, `places.html` A to Z, all in the sitemap.
   "See full page" buttons on every card (section pages via `app.js`, homepage cards, homepage profile modal,
   featured "See listing" buttons).
4. Click-to-load Facebook Page Plugin on the 97 listing pages that have an official Facebook Page.
5. Removed 11 records that were section headings or research notes showing as listings
   (`docs/audit/removed-listings.json`). Removed all em and en dashes. Rewrote 20 placeholder blurbs.
6. Cut N Up: canonical Facebook URL, hours, services wording from its Facebook Page.
7. `tools/audit.py` (exit 1 on problems), `tools/crawl.js`, `tools/optimize_home.py`, `tools/clean_listings.py`,
   `tools/build_places.py`, `sw.js`, docs (SITE-GUIDE, TROUBLESHOOTING, STYLE-GUIDE).
8. `landing/monitor.py` accepts the listing page CSP (`PLACE_CSP`) and `place.js`. Backup: `monitor.pre-places.py`.
9. After results in `docs/audit/after/`: crawl of 1,670 page views (desktop and mobile) with 0 broken links,
   0 dead tabs and 0 console errors.

## Hook for the hourly refresh routines
After any change to a `*.json` data file or to `SLH_LISTINGS` in `index.html`, run
`python3 tools/build_places.py && python3 tools/audit.py` before committing.
The security and health scan should run `python3 tools/audit.py` (and `--lighthouse` once a day).

## Still to do
* Copy rewrite: about 650 listing blurbs are factual but short. Rewrite them in batches using
  docs/STYLE-GUIDE.md, only from verified sources. Nothing was rewritten that would change facts.
* Verification: hours exist for only 18 listings and street addresses for 167 of 719. Fill from each business's
  own site or Facebook Page; add `hours_source` and `verified` fields so the page shows them.
* Owner review: the 11 removed records in `removed-listings.json`. Several describe real businesses
  (a Joppa florist, a Cullman vet, a dog bakery, a parts store, St. Paul's Lutheran) but the business
  name was replaced by a section heading, so they cannot be published until the real name is confirmed.
* Homepage accessibility 95: Lighthouse flags color contrast on the help bar (likely measured during its fade in)
  and a layout shift in the officials rail on desktop.
* Homepage still carries about 480 KB of inline listing JSON. Moving it to a cached `listings.json` would trim
  first load further but needs the homepage scripts changed to load it asynchronously.
* Lighthouse "uses long cache TTL" cannot be fixed on GitHub Pages (10 minute max-age). Cloudflare's free plan
  would fix it but needs a custom domain.
* 15 listings link to websites with no https version. Their pages show the address as text.
