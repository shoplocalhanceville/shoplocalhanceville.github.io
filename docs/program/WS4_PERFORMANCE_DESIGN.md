# Workstream 4 — Performance Design

**Lane:** Build (WS4). **Date:** 2026-11-03. **Status:** design, prototype, and local measurement only. Nothing published, no config changed.
**Governing facts:** measured scores live in `score_ledger.csv` beside this file. Every number below that comes from this machine is labeled **local/lab**; the gate's numbers are labeled **CI**. No CI mobile run exists yet, so there is no CI mobile baseline to design against; the first one arrives with the gate follow-up release.
**Version note (research item 1, already paying off):** the gate's own report JSONs record **Lighthouse 12.6.1** for the CI runs, while this machine's local CLI is **13.6.0**. The two runners are not the same version, so CI and local numbers are never mixed in the ledger, and the gate fairness package in section 4 includes pinning the gate's version on purpose.

---

## 1. The data.js delivery rework

### What the file actually is (measured on the live file, 592,499 bytes)

| Part | Bytes | Share |
|---|---|---|
| `SLH_LISTINGS` array (724 records) | 548,337 | 93% of the file |
| — of which `descEs` (Spanish descriptions) | 171,801 | biggest single field |
| — of which `description` (English) | 144,579 | |
| — of which `aka` (alternate names, search only) | 84,695 | |
| — all other fields combined | ~147,000 | |
| Everything else in data.js (UI/CAT dictionaries etc.) | ~44,000 | |

Compression reality, measured: `gzip -9` of data.js is **173,220 bytes**. GitHub Pages delivers the file compressed at roughly that size; the gate's plain test server delivers all 592,499 bytes (see section 4). On a real phone the cost that remains either way is parse and execution of 592 KB of JavaScript under CPU throttling — that is what the split attacks.

### Options

**Option A — split the Spanish descriptions out.** The generator emits `data.js` without `descEs`, plus a companion `data-es.js` (a name-to-text map) that the page loads only in Spanish mode. The site already reloads the page on a language switch (the choice is stored), so the companion file is simply part of the Spanish page load and is never downloaded by English visitors.
- Measured effect on payload: default (English) data drops from 592,499 raw / ~173 KB gzip to **378,860 raw / 103,023 gzip (−36% raw, −40% wire)**. The Spanish companion is 196,148 raw / 62,868 gzip, paid only by Spanish-mode loads.
- Risk: low. One source (the generator) emits both files from the same records; the service worker's network-first list gains one entry. Spanish rendering must be verified page by page in the build package, as always.

**Option B — defer the search-only `aka` field.** `aka` (alternate names) is read only by the search haystack. The generator emits it as a separate map file loaded on first focus of the search box; if a visitor types before it lands, `apply()` awaits it for term searches (the chunked renderer in section 2 already made `apply()` supersede-safe).
- Measured effect: core drops further to **287,649 raw / 81,233 gzip**; the deferred map is 109,575 raw / 26,652 gzip, paid only by visitors who search.
- Risk: moderate. A first keystroke can race the fetch on a slow connection; the await-guard covers correctness, and the fallback (searching name/category/address only until the map lands) is a brief, invisible narrowing. Needs a deliberate test in the build package.

**Option C — per-category or per-town data files.** Rejected: the homepage grid, search, and rails all range over the whole directory at once, so the split points would force most files to load anyway, at the cost of many more requests and a much more complex generator. The field-based split (A+B) follows actual use; a geography split does not.

**Option D — representation changes only** (shorter keys, JSON.parse of a string). Rejected as the main lever: gains are small next to the split, and short keys make the verified data harder to audit by eye, which this program's verification standard forbids trading away.

### Recommendation

Ship **A first** as its own package (biggest single win, lowest risk, and it is a generator change of the same kind as the already-proven rewiring), measure on the gate, then **B** as a second package. Combined expected result for the default English load, from the measured sizes above: **592 KB → ~288 KB raw (about half), 173 KB → ~81 KB on the wire**. Parse time should fall roughly in proportion; that is an expectation to be proven by the gate and local runs, not a promised score.

---

## 2. INP pattern — chunked rendering (research item 2)

### The pattern

Any render that builds more than a screenful of DOM is split into fixed-size chunks; between chunks the code yields to the main thread with `scheduler.yield()` where the browser supports it and a `setTimeout(0)` promise elsewhere. A generation counter makes a newer render request supersede one still in flight, so fast typing never queues stale work. Nothing about the final DOM, order, or content changes.

### Prototype (built and measured, local/lab)

`~/workspace/overhaul_ws4_prototype/` holds `before/` (byte-identical copy of the live mirror homepage) and `after/` (the same copy with the pattern applied to the grid renderer, `renderMore()`: chunks of 6 cards, fragment appends, yield between chunks; the patch is +771 bytes and the engine block passes `node --check`). The mirror itself was never touched.

**Interaction measurement (the measure this pattern exists for).** In-page `longtask` observer, headless Chrome, 412×915 viewport, 4× CPU throttling via CDP, typing "barber" at 60 ms per character into the search box, two samples per side:

| | Long tasks during typing | Longest task | Total blocking (sum of task time over 50 ms) | Result |
|---|---|---|---|---|
| Before | 6 (one per keystroke) | 79 ms / 99 ms | 115 ms / 174 ms | 18 places found |
| After (chunked) | 1 | 52 ms / 63 ms | 2 ms / 13 ms | 18 places found |

Identical results and identical final DOM on both sides (initial grid 24 cards, "724 places found", search settles on the same 18). The one residual ~50–60 ms task in the chunked version is the synchronous filter and sort over 724 records, which this prototype deliberately leaves in place; if a future profile shows it over budget, the follow-on step is memoizing the per-record search haystack once at boot instead of rebuilding it per keystroke.

**Load-phase Lighthouse (local/lab, reported for completeness, not attribution).** Two local mobile runs per side were too noisy on this machine to credit any difference: before Performance 0.67 / 0.71 with TBT 5,224 ms / 28 ms; after 0.69 / 0.71 with TBT 72 ms / 12 ms. The spread inside each side exceeds any difference between sides, so no load-score claim is made from them. The pattern targets interaction responsiveness (INP), which the interaction measurement above does evidence; load TBT is the data.js problem, addressed in section 1.

### Build package contents (when scheduled)

Apply the same chunked `renderMore()` to the real homepage, keep BATCH at 24 and CHUNK at 6, and verify by rendering plus the same interaction harness against the live-code mirror before anything is proposed for publish.

---

## 3. Speculation-rules experiment (research item 3)

**Design.** On the homepage and category pages only, after the page has settled, inject one `<script type="speculationrules">` block of type **prefetch** listing the profile-page URLs of the cards currently in the grid (at most 24, the visible batch), with **`"eagerness": "conservative"`** (the browser prefetches only when the visitor is about to click, the cheapest setting that still helps).
**Guards.** No rules are injected at all when `navigator.connection.saveData` is true, when the connection reports 2G-class, or when the browser does not support speculation rules (it is ignored harmlessly where unsupported; Chromium-only today). Same-origin URLs only. No prerender in this experiment.
**Measurement.** Lab A/B on the local harness: load the homepage, click the first profile card, and record the profile page's load and LCP with prefetch off versus on (cold cache both sides); in-page, count speculation prefetch responses in the performance resource log to prove the prefetches actually fired and were used. Field-style confirmation can only come later, from real visitor timing if analytics that can report it are ever adopted (a WS3 decision). **Promotion rule, set in advance:** prerender is considered only if prefetch shows a real navigation gain with no regression in the gate's numbers; otherwise the experiment ends at prefetch or is dropped.

---

## 4. Gate fairness fix — proposal for a named package (no config changed)

**The artifact.** Both gate configs serve the site with `"startServerCommand": "python3 -m http.server 8080"`, which sends every file uncompressed. GitHub Pages serves the same files compressed (measured above: data.js crosses the wire at ~173 KB, not 592 KB). The gate therefore measures paint timing against a delivery mode no visitor ever experiences, and the last 0.02 of desktop homepage performance (PR #54 run: FCP median 802 ms and LCP median 959 ms, both scoring 0.95, everything else perfect) is attributable to that artifact on the record.
**The proposed change (one package, two files plus one new file).**
1. Add `tools/gzip_server.py` to the repo: a small raw-Python static server on the standard library's http.server, identical in behavior except that it sends `Content-Encoding: gzip` for text types (HTML, CSS, JS, JSON, SVG) when the client offers `Accept-Encoding: gzip`, with correct `Vary: Accept-Encoding`.
2. Point `startServerCommand` in `.lighthouserc.json` and `.lighthouserc.mobile.json` at it (same port, same root).
3. Companion item, from research item 1: pin the gate's Lighthouse/lhci version in the workflow and record it in this ledger with every run, so a version change is a deliberate, visible event. The gate currently runs **12.6.1** per its own reports; the local CLI is 13.6.0. Whether to align them is part of the same package decision.
**Limits, written down in advance.** A local gzip server is still not a CDN: latency, TLS, and caching still differ from GitHub Pages, so the fix removes the compression artifact only and the gate remains a conservative floor, not a replica. Assertions that measure
...[truncated 5160 chars]
## Addendum, 2026-11-04: two ideas folded in from an audited outside media file

Source: muse_media_master_v2.csv, uploaded 2026-11-04 with a directive to execute a backend media refactor. Audited under the audit-first rule for uploaded documents; Charles decided the same day: do not execute it, and fold the useful parts into the existing raw-code plan. The file's backend, database, upload, and library machinery is not adopted; the site is static and raw code only. Two ideas are adopted, in raw form:

1. Logo containment geometry (from the file's LOGO_PRIMARY row, restating Charles's standing logo rule as a display rule): a logo is never cropped, warped, or stretched. Logo slots render with the image's own aspect preserved (contain behavior in plain CSS inside the slot's fixed box), so a wide or tall mark letterboxes instead of distorting. Applies wherever logos render: homepage cards, profile page heads, and tiles. Verified slot by slot in the IMP-04 pass, because some existing slots use cover behavior for photographs, which stays correct for photographs and wrong for logos.
2. Responsive image variants (from the file's ARTICLE_HERO row, already the IMP-04 direction): variants are pre-generated files produced by the build's own tooling (the Python generator counts as raw code), served with plain srcset and sizes markup and native lazy loading. No server component and no JavaScript library. Variant widths follow the measured plan in this document and Research Brief 2, with AVIF where it wins, not the outside file's fixed 400/800/1200 set, which was written for a different site's hero component.

Everything else in the outside file (user avatar cropping, sanitizing user-submitted SVG, AI outpainting, a media registry database) has no counterpart on this site and is not adopted.
