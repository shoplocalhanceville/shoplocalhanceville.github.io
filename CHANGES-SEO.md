# SEO, Social and Security Changes (October 2026)

All changes are incremental. The look, listings and page structure did not change. Everything is reversible with Git; the pre-change state is saved on branch `backup-2026-10-23`.

## What changed
- **Homepage** (commit bf275b5): full meta, Open Graph and X card tags, JSON-LD `@graph` with WebSite (SearchAction), Organization (logo, areaServed, Facebook in sameAs, no personal founder name) and ItemList. Branded `og-image.jpg` (1200x630), `logo.png` (512x512), favicons and `site.webmanifest`.
- **Every category and story page**: unique title and description, absolute https canonical and og:url, robots, geo tags (US-AL, Hanceville, 34.0614;-86.7633), full og tags with the shared og-image, `twitter:card=summary_large_image`, hreflang (en and x-default pointing at the page itself), viewport and theme-color.
- **Story pages**: NewsArticle JSON-LD with headline, description, dates, section, sources (isBasedOn) and the publisher Organization with an ImageObject logo.
- **robots.txt** allows everything and points to the sitemap. **sitemap.xml** lists every page (google verification files excluded on purpose) with lastmod dates.
- **Security**: `SECURITY.md`, starter Content-Security-Policy and referrer meta tags on every page, `_headers` file ready for Cloudflare, Dependabot and secret scanning turned on. No http:// assets (no mixed content).
- **tools/seo_head.py**: one command that adds any missing tags, keeps JSON-LD valid, fixes the publisher logo, adds new pages to the sitemap and bumps lastmod on changed pages.

## How to handle future updates
1. Make the edit (new story, new listing, new page).
2. Run `python3 tools/seo_head.py` from the repo root. It must print `SEO OK`.
3. Commit and push. GitHub Pages updates in a minute or two.
4. New stories are copied from an existing story page, so they inherit every tag; the script fills anything missing. For a brand new section page, copy the head of `shops.html` and change the title, description, canonical and og:url.
5. After big changes, paste the URL into the Facebook Sharing Debugger (https://developers.facebook.com/tools/debug/) and tap Scrape Again.
6. Keep `google3d41a60ee1e55960.html`, `google5b15f6377dd49d2a.html` and the IndexNow key file in the root. Never commit passwords, tokens or personal info.

## Validation
- JSON-LD parses on all pages and uses schema.org types Google supports (NewsArticle, Organization, WebSite, BreadcrumbList, ItemList). Recheck any page with https://search.google.com/test/rich-results.
- Mozilla Observatory: GitHub Pages cannot send custom headers, so the header score stays low until Cloudflare is in front. The meta CSP covers the basics in the meantime.
- Desktop (1366 px) and mobile (390 px) checks: no layout overflow and no console errors.

## Next steps once shoplocalbama.com is bought
1. In Cloudflare, add the zone (free plan) if the registrar did not already.
2. Choose one:
   - **Cloudflare Pages (recommended)**: connect this GitHub repo, no build command, output folder `/`. Add `shoplocalbama.com` and `www` as custom domains. `_headers` then sends HSTS, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy and the CSP.
   - **Keep GitHub Pages**: add a `CNAME` file containing `shoplocalbama.com`, set DNS CNAME `www` to `shoplocalhanceville.github.io` and apex records to GitHub's Pages IPs, proxied through Cloudflare. Add the headers with a Cloudflare Transform Rule (free), then turn on Enforce HTTPS.
3. Turn on SSL/TLS Full (strict), Always Use HTTPS and HSTS in Cloudflare.
4. Replace `https://shoplocalhanceville.github.io/` with `https://shoplocalbama.com/` in canonicals, og:url, JSON-LD, sitemap.xml, robots.txt and the `BASE` value in tools/seo_head.py, then run the script.
5. Add the new domain to Google Search Console and Bing Webmaster Tools, submit the sitemap, and rescrape key pages in the Facebook Sharing Debugger.
6. Run https://observatory.mozilla.org, https://securityheaders.com and https://www.ssllabs.com/ssltest/ against the new domain.
