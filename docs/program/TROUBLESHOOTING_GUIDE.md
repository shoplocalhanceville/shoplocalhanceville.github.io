# Troubleshooting Guide
## Hanceville Entertainment and Shopping website
Symptom-first reference for every problem this program has actually hit, with the fix that worked and the rule that prevents a repeat. The same content in table form is `troubleshooting_cases.csv` and `error_codes.csv` in this folder. Owner and only approver: Charles Adams. Current as of November 3, 2026.

## How to use this guide
Find the symptom, run the first check, apply the fix exactly, then read the prevention line so the problem stays fixed. Every fix follows the emergency playbook: reproduce by rendering, stage, render-verify, publish through the browser route with a base check, verify live, log it.

## 1. Homepage loads but the listings grid is empty, the featured rail is empty, or the spotlight name says "loading"
**Cause (hit on November 3, 2026, PR #44):** a script error stops the homepage's main engine. The console shows `ReferenceError: slug is not defined` (or another helper name). The homepage has two engines in separate script blocks; each block's functions are private to that block. Removing a function from one block because another block has one with the same name breaks the first block.
**First check:** render the page and read the console. Count rendered cards (a healthy first batch is 24) and featured rail items (12).
**Fix:** restore the missing helper definitions inside the failing block's own scope, using the surviving block's versions verbatim. Never make one block depend on another block's private functions.
**Prevention:** same-named functions in different blocks are not duplicates. Any cleanup of "duplicate" code ships only after a render test that exercises the grid, search, filters, and rails. This is rule 8 in the master guide.

## 2. A profile page returns 404 but the listing exists on the homepage
**Cause:** the listing was added to the homepage after the last generator run, so its profile family was never built. Eight listings were in this state on November 3, 2026 (Sevini Boutique and seven others).
**First check:** search `listings_master.csv` for the listing; `profile_page` says NONE. Confirm the live 404.
**Fix:** run the site's own generator, `tools/build_places.py`, in a staging tree with the current homepage data; ship the new family (main page plus whichever sibling pages the data supports) and add the URLs to `sitemap.xml` in the same release, matching the existing sitemap entry format.
**Prevention:** any release that adds a listing also runs the generator or schedules the family build in the same package. The six-hour watch flags new 404s.

## 3. A GitHub upload produces a file that is the wrong size, or the live page looks half-updated
**Cause:** web uploads in this repo have stalled and truncated before. The committed file silently differs from the staged file.
**First check:** compare the committed file's size (GitHub API or the repo view) with the staged file's exact byte size before merging.
**Fix:** delete the bad upload once on the branch and upload again, then re-check the size. Never merge a pull request whose file sizes you have not confirmed.
**Prevention:** every publishing pass records the expected byte size of each file in its instructions and verifies each one before merge. Large releases split into lettered parts.

## 4. A business's website link is dead, returns 502, or shows unrelated spam
**Cause:** businesses close, hosts fail, and domains get hijacked. Three linked sites returned 502 on November 3, 2026; two others (ssfoods.net, collegetire.com) had been taken over and carried injected casino links.
**First check:** retest the link directly, twice, at different times. A single failed fetch from a tool machine proves nothing on its own (this machine's connections are sometimes cut by its proxy on healthy servers), so corroborate before acting.
**Fix:** for a confirmed dead or hijacked domain, remove the website link everywhere it appears (homepage record, profile family, data JSONs, sources page) and keep the listing, following the PR #16 and PR #44 precedent. Add hijacked domains to the never-link list in the standard and both bot instruction files in the same pass.
**Prevention:** the six-hour watch re-tests outbound links and reports changes; it never edits on its own.

## 5. Scores disagree between two Lighthouse runs, or a "fix" does not move the number
**Cause (hit on November 3, 2026):** mixing measurement tools. `lhci collect` defaults are not the plain Lighthouse CLI defaults, and neither matches the CI gate exactly. One local layout shift score (0.142) attached to the fixed bottom tab bar stayed bit-identical across four different page variants, while an unthrottled real-browser load recorded no shift at all.
**First check:** confirm both runs used the same tool, the same emulation, and the same page version, served from a directory you verified (see item 8).
**Fix:** re-measure with the standard local method: the plain Lighthouse CLI bundled with the LHCI install, default mobile emulation, `CHROME_PATH` set to the persistent headless Chrome under `~/workspace/.tools/`. Report scores as local measurements, never as live scores; no live Lighthouse run is possible from this machine because its proxy blocks the headless browser.
**Prevention:** one measurement method per comparison. A fix that does not change the metric it targets is reported as unproven and does not ship on that claim.
**Gate runs (added November 3, 2026, after the first full CI run, on PR #51):** the gate serves the build under review with a plain `python3 -m http.server`, which sends no compression and no cache headers. Three asserted audits therefore measure the test server, not the site, and cannot pass as wired: `uses-text-compression`, `uses-long-cache-ttl` / `cache-insight`, and `document-latency-insight`. GitHub Pages itself serves compressed text with its own cache policy. Treat those three as gate configuration defects: correct them only as a config change with Charles's approval, never as site work, and never by quietly lowering an asserted score. Everything else in a failed gate run is real site work. That first run measured desktop homepage Performance 93 (median of five) and CLS 0.1463552769305371 against the 0.1 budget.
**Two facts that prevent false leads:** (1) The homepage loads no stylesheet file; its CSS is inline in the document, including the fixed `.tabbar` rule, so a homepage Lighthouse run legitimately shows zero stylesheet requests. Section and profile pages do use `style.css`. (2) Local runs from this machine cannot fetch the page's external assets (the proxy blocks the headless browser), so local and CI layout shift values are measurements under different conditions, not contradictions: local mobile 0.1423663131569324, CI desktop 0.1463552769305371, both attached to the tab bar, cause still unproven. The CI run is the reference for layout shift until a throttled trace names the moving element.
**Tooling note:** the LHCI install that lived under `/usr/lib/node_modules` did not survive a machine replacement. Lighthouse 13.6.0 is installed persistently at `~/workspace/.tools/lighthouse/`; run its `node_modules/.bin/lighthouse` with `CHROME_PATH` set to the persistent headless shell under `~/workspace/.tools/chrome-headless-shell/`.

## 6. A section page shows wrong or stale cards after a data fix
**Cause:** some pages render from a data file, not from their HTML. `businesses.html` renders `businesses.json`; editing the page alone changes nothing a visitor sees (the PR #17 lesson).
**First check:** in `files_registry.csv`, find the page's row; it names the data file behind it.
**Fix:** change the data file, then render the page and confirm the cards changed.
**Prevention:** registry first, edit second. Every data-backed page in the registry carries its data file's name.

## 7. Facebook embeds or links misbehave, or link checks show hundreds of Facebook 400s
**Cause:** Facebook answers unauthenticated checks with login walls (400) and bot defenses (403). In link tests these are expected noise, not dead links. Profile social pages load the embed only when a visitor taps (place.js), by design.
**First check:** open the Facebook link signed in before calling it dead. Check whether the page still exists and posted within the last 30 days (the rule for using a Page as a listing's main link when it has no website).
**Fix:** only act on a Page that is confirmed gone or confirmed to be a different business. Otherwise leave the link and note the check as unverifiable through the wall.
**Prevention:** link reports separate "confirmed dead" from "unverifiable through the login wall". The two are never merged into one count.

## 8. Local test results make no sense (wrong file measured, page will not load, server errors)
**Cause (hit repeatedly on November 3, 2026):** this machine accumulates stale local web servers. A new server can silently fail to bind a busy port, leaving an older server answering with a different directory's files. The machine's proxy also cuts some outbound connections on healthy sites, and the headless browser cannot reach the live site through it at all.
**First check:** fetch the page your server is actually serving and grep it for a marker string unique to the version you mean to test, before measuring anything.
**Fix:** use a fresh port for every test session, verify the marker, and only then measure. Judge the live site by exact byte fingerprints fetched through the working route, not by local browser fetches.
**Prevention:** marker verification is a required step in every local measurement procedure in this program.

## 9. A name change or removal leaves traces (old name on other pages, broken tiles)
**Cause:** a listing's name and address appear in more places than its own pages: related pages of neighboring listings, category pages, `places.html`, `sources.html`, the sitemap, and data JSONs.
**First check:** search the whole repository for the old name and the old web address; the count of remaining references should be zero (or each one explained, like a historical news story).
**Fix:** update every surface in one release; split into parts if the file count demands it, and verify a related page of a neighboring listing afterward. PR #44 and PR #45 are the worked example (Pro Temp rename, Shrimp Basket removal).
**Prevention:** the blast-radius checklist is rule 6 in the master guide; no rename or removal is called complete on the strength of its own pages alone.

## 10. A page or string shows English while Spanish mode is on
**Cause:** the Spanish UI dictionary has no entry for that string; the site's translator falls back to English by design. The same applies to structured data added before its translation.
**First check:** search the UI dictionary block in `index.html` for the English string.
**Fix:** add the Spanish entry in a staged release. Listings without a real Spanish description are a separate, tracked gap (18 records have no English source text to translate).
**Prevention:** new interface strings ship with their Spanish entries in the same release whenever the translation is known.

## 11. Visitors report an old version of the site after a release
**Cause:** GitHub Pages deployment lag, browser cache, and the site's service worker (`sw.js`). Shared code is versioned (`app.js?v=16`); a changed script with an unchanged version can sit in caches.
**First check:** confirm the Pages deployment for the merge completed, then check the live file's size and a marker string through a fresh fetch.
**Fix:** wait out the deployment; if a shared script changed, raise its `?v=` version in the pages that load it as part of the release.
**Prevention:** releases that change shared code note the cache version step in their summary.

## 12. An API or connector call fails with 403, 429, or a permission error
**Cause:** connector permissions and rate limits are real stops, not obstacles to route around. Stripe product creation returned 403 twice on November 3, 2026, and readback confirmed no product existed.
**First check:** read the error, then read back the state (did anything actually get created?) before retrying anything.
**Fix:** stop after the stated limit. Record the block in `decisions_holds.csv` with what would unblock it (a permission fix, or the owner doing the step in the provider's own dashboard).
**Prevention:** never retry a denied write blindly, never report a product, booking, or post as existing until a readback shows it.

## Incident log template
Add a row to `troubleshooting_cases.csv` and, when a release shipped, to `releases_log.csv`:
date · symptom · cause (one sentence, evidence-based) · fix · prevention rule · where the evidence lives.
