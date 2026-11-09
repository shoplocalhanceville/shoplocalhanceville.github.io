# Tools

Scripts that maintain the site. Run them from anywhere; each one finds the repo root from its own location.

## build_places.py
Builds every `place-*.html`, `category-*.html`, `places.html`, `sources.html` and the sitemaps from the data files.

    python3 tools/build_places.py                 normal run
    python3 tools/build_places.py --strict        exit code 2 if a listing lost data (see below)
    python3 tools/build_places.py --prune-lost    really delete tab pages whose data was dropped on purpose

Safety guard: a Contact, Social Links, Hours, Location, Media or Documents page of a listing that still exists is
no longer deleted when the listing loses the website, phone, hours and so on behind it. The pages are kept, stay in
sitemap.xml and the run prints a WARNING naming them. This is what removed the Hele Bowls pages on Nov 8, 2026 when a
stale copy of data.js overwrote the record. Pages of listings that were removed altogether are still pruned.
Source values with a note after the link, such as `https://x.com/ (checked Nov. 6, 2026)`, now link only the URL and
show the note in the label (the note used to end up inside the href and made a broken link on sources.html).

## monitor.py
Live site health check (HTTP, integrity against main, CSP, links, GitHub alerts). Copy of the routine's monitor with:
per-request connect and total timeouts, retries with backoff, 32 parallel requests, no second fetch of internal
links that were already fetched, and a `--budget` (default 200 seconds) after which the external link phase stops
starting requests. Links on other sites that time out, fail DNS or TLS, or refuse the connection are WARNINGS;
internal 404s and malformed hrefs, and external 404 or 410, are failures. Options: `--no-external --quiet --days N
--budget S --workers N --retries N --timeout S --connect-timeout S`.

## site-build/build.py
The old page generator (home, section pages, council, departments, stories, ics, sitemap, Spanish pages, map).
Its templates are older than the hand maintained pages in this repo, so it is SAFE BY DEFAULT:

    python3 tools/site-build/build.py                       build in a temp copy, apply only what is safe, list the rest
    python3 tools/site-build/build.py --out-dir /tmp/out    full build into /tmp/out, repo untouched (use this to diff)
    python3 tools/site-build/build.py --site-dir DIR        read a different source folder (or SLH_SITE_DIR)
    python3 tools/site-build/build.py --force               old behaviour, overwrites and deletes. Do not use on the repo.

Paths default to the repo root. Hands-off files (news.json, events.json, scores.json, story pages, sitemaps, ics,
Google verification files) and hand maintained pages (index and section pages, sw.js, style.css, app.js) are never
overwritten in place and nothing is ever deleted. Icons need `npm i lucide-static@1.59.0`; point `SLH_LUCIDE_DIR` at
`node_modules/lucide-static/icons` (default: `tools/site-build/node_modules/...`).
Other files in the folder: build_extra.py, es_pages.py, icons.py, geo-ok.json (helpers loaded by build.py).
