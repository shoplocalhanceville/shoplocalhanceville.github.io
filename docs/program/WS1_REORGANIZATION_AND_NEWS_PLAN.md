# WS1 Plan — Reorganization, Standards Rebuild, and News-First Repositioning

**Workstream:** WS1 of the Complete Overhaul Program (confirmed by Charles Adams, 2026-11-03).
**Status:** Plan only. Nothing in this document is built or published. Every build item below ships only as a staged package that Charles approves by name, after the already-approved publish queue (gate follow-ups, cleanup release, program docs sync, regeneration package) finishes.
**Grounding:** OVERHAUL_PROGRAM_2026-11-03.md, 00_MASTER_GUIDE.md, files_registry.csv, imperfections_register.csv (IMP-01 to IMP-12), decisions_holds.csv, all as read on 2026-11-03. Where a fact is not in those files, this plan says so instead of assuming it.
**Conventions:** (a) = mechanical, safe to build in a staged package once the package is approved. (b) = Charles decision, collected in the decision list at the end of Section 1 and in Section 3.

---

## Section 1 — News-first repositioning spec

### 1.1 Where the site stands today (evidence)

- The site's name is **Hanceville Entertainment and Shopping** (Shop Local Hanceville); the PWA manifest carries the same name with standalone display and theme #6D28D9 (files_registry.csv).
- It already publishes news: **60 story pages** (`story-*.html`, generated from stories data; Maggie drafts, Big Dog validates) and a **news** page among the 21 root content pages (files_registry.csv).
- The homepage already carries stories among its sections, alongside the hero, search, five script-filled rails, the officials rail, and site information (00_MASTER_GUIDE.md, files_registry.csv).
- The guide itself — 724 listings in data.js, 725 profile main pages, category pages, places.html, map view, search, Open Now, full Spanish mode — is the service layer the repositioning re-labels, not replaces.

The repositioning is therefore a presentation and information-architecture change: news leads, the guide is named and framed as a feature of the news organization. No listing data changes are required by this section.

### 1.2 Identity and naming

1. **Keep the existing name.** "Hanceville Entertainment and Shopping" stays as the site's name in the masthead, the manifest, and structured data. (a) A rename would put every URL-adjacent reference, the Facebook Page identity, and the media kit at risk for no measured benefit, and no evidence in the program files supports one. If Charles ever wants a rename, it is (b) and a program of its own.
2. **Add a news-organization descriptor line** under the masthead name, on the pattern of a newspaper's descriptor: the site presented as Hanceville's local news organization, with the Community Guide named as its guide service. Placing the descriptor (masthead, page titles' suffix pattern, Open Graph description, manifest description) is (a). The exact wording of the descriptor is (b): it is the organization's public identity sentence and Charles approves it before any package carrying it is staged.
3. **Newsroom furniture:** an About-level statement of newsroom practice (items sourced and dated, corrections recorded, nothing published on rumor, per the program's positioning section) added to the existing about/news pages. Building the block is (a); the policy wording is (b), same approval as item 2.
4. **Spanish parity is mandatory, not optional.** Every new label or descriptor added by this section gets its Spanish entry in the data.js UI dictionary in the same package (the IMP-02 lesson: labels added without dictionary entries fall back to English). (a)

### 1.3 Homepage hierarchy

Current order (per the registry): hero, search, five rails, officials, stories, site information. Target order:

1. **Emergency and service strip stays where it is.** No evidence in the program files describes moving it, and nothing in the repositioning requires it. (a) — no change.
2. **Masthead with the new descriptor** (Section 1.2, item 2). (a) build, (b) wording.
3. **Latest News leads the content.** A news lead section built from the existing stories data: the most recent stories first, each with its date shown, linking to the story pages and the news page. Building this section into index.html and feeding it from the same stories data the story pages generate from is (a). How many stories lead, and whether one story is featured above the rest, is an editorial composition choice — (b) if Charles wants a say, otherwise the builder's default (a short lead list, no single featured story) is used and reported.
4. **The Community Guide block follows the news.** The existing search, listings grid, rails, and category entry points are grouped under a visible "Community Guide" heading with a one-line description of the guide as a service of the news organization. This is re-labeling and re-ordering existing blocks inside index.html, plus dictionary entries. (a)
5. **Everything else keeps its place:** officials rail, photo and town rails, map view entry, sources and policy pages. (a) — no change beyond the grouping above.

### 1.4 Navigation naming

1. Add a **News** entry pointing at the existing news root page if the current navigation does not already label it that way, and a **Community Guide** entry pointing at the directory experience (places.html / the homepage guide block). Adding or re-labeling navigation entries is (a); the underlying URLs do not change (Section 1.5).
2. The bottom tab bar and menu keep their existing structure and accessibility properties (the manual WCAG pass measured the tab bar links at 44 to 52 px; IMP-12's focus fixes are staged separately and are not redone here). Any tab-bar label change rides the same staged package as the navigation change and is re-verified by rendering. (a)
3. The label text in both languages is part of the package; if Charles wants different label words, that is (b) wording, handled with the descriptor approval.

### 1.5 What deliberately does NOT change

- **No URL changes.** Every existing URL (homepage, 725 profile mains, 1,970 sibling tabs, 66 category pages, 60 story pages, 21 root pages, map-view.html) keeps its address. No redirects are needed because nothing moves. This protects search indexing, the sitemap, Facebook links, and every printed or shared link.
- **No listing data changes.** data.js records, the generator, and the profile/category families are untouched by the repositioning itself.
- **No guide function changes.** Search, Open Now, map view, Spanish mode, favorites, and the Facebook embeds behave exactly as today; only their framing and grouping change.
- **No Facebook change.** The Pages, their names, and the content engine are outside this spec; nothing here posts or renames anything.
- **No theme change.** Black, purple, and white (Wallace State orange, blue, and white) stands; what already measures at standard is protected per the program's standing rule.

### 1.6 Newsroom mechanics the repositioning needs

1. **Every story shows its date and its source.** Story pages are generated from stories data; adding visible date and source lines is a generator/stories-data change, built once and applied to the story family in one package, with one regenerated story rendered and exercised as proof before the family ships. (a) mechanism. Stories already published without a recorded source are not back-filled with invented ones; the verification-gap method (Section 4) applies to them in batch order.
2. **A corrections mechanism.** A corrections block on the news page: dated entries, what changed, and why. Building the block is (a); the standing corrections policy wording is (b) (approved with the descriptor wording).
3. **Dating discipline for the homepage news lead:** the lead section sorts by the story dates recorded in the stories data; a story with no recorded date does not lead. (a)

### 1.7 Charles decisions arising from this section

- D1. Descriptor wording (1.2 item 2) and newsroom-practice wording (1.2 item 3, 1.6 item 2).
- D2. News lead composition, only if he wants a say (1.3 item 3).
- D3. Navigation label words, only if he wants different words than News / Community Guide (1.4 item 3).
- D4. Any site or Page rename — recommended against; listed so the record shows it was considered (1.2 item 1).

---

## Section 2 — File-structure audit (registry vs known live structure)

Reference structure (files_registry.csv, measured 2026-11-03; sitemap 2,843 URLs live, becoming 2,842 when the queued cleanup release lands): 725 profile mains, 1,970 sibling tab pages (contact 519, related 721, social 507, location 181, hours 42), 66 category pages, 60 story pages, 21 root pages in the sitemap plus map-view.html live.

- **F1. The master guide disagrees with the registry it points to.** 00_MASTER_GUIDE.md's one-paragraph picture says the homepage "carries the listing records themselves" (untrue since PR #51 moved them to data.js) and counts 717 profile mains plus 1,943 tab pages, while files_registry.csv measures 725 and 1,970. Its "Known gaps" section also still says eight real listings have no profile page, which PR #48 closed. *Disposition: correct the guide in a WS1 records package (WS1-A). Mechanical; the registry is the evidence.*
- **F2. The sitemap registry row contradicts itself.** files_registry.csv gives the sitemap's purpose as "Search engine map (2,808 URLs)" while its own note records 2,843 measured live, and the cleanup release takes it to 2,842. *Disposition: correct the row's wording when the cleanup release lands (WS1-A). Mechanical.*
- **F3. Cache-version inconsistency across pages.** The registry and guide record pages loading app.js?v=16 and style.css?v=15, while events.html still references style.css?v=14 (flagged in the PR #53 staging work). Mixed versions mean some visitors keep stale styles after shared-CSS changes. *Disposition: normalize all root and section pages to the current versions and record the audit in one small staged package (WS1-B). Mechanical.*
- **F4. The inert `_headers` file.** The repo carries `_headers`, but GitHub Pages does not honor it and cannot set custom security headers (registry note; IMP-08). The file implies protection it does not provide. *Disposition: Charles decision (remove it, or keep it with an explicit comment that the platform ignores it). Recommendation on record: remove, since Workstream 1's own CSP evaluation (program addition 11) is handled separately and honestly. No build until he decides.*
- **F5. A stale master HTML sits beside current deliverables.** `~/workspace/your_files/Shop_Local_Hanceville_MASTER.html` holds 734 listings synced through PR #28 (guide and registry both flag it). It is an archive, but its name and location invite a bot or a person to treat it as current. *Disposition: rename and move it to an archive location with a dated name in WS1-A. Deleting it outright is a Charles decision; archiving is mechanical once approved as part of WS1-A.*
- **F6. Program documents exist in two places by design.** The working masters live in `~/workspace/your_files/Website_Program_Master/`; a snapshot lives in the repo at docs/program/ (refreshed by the queued docs sync). The design is sound (working masters lead) but the snapshot drifts between syncs. *Disposition: keep the design; add the standing rule that the snapshot refresh rides the next major release after any master change, recorded in WS1-A. Mechanical.*
- **F7. Two listing data paths invite confusion.** data.js is the listings source of truth; places.json is a generated subset that app.js renders from, and the registry already warns against treating it as truth. No drift is in evidence, but nothing in the registry states which build step regenerates places.json. *Disposition: no structural change. WS1-E confirms and records the regeneration path so the subset cannot drift silently; if it is not produced by the generator run, that becomes a finding for a later package.*
- **F8. Dual-purpose Google verification files are correct as-is.** The two Search Console verification files sit in the repo root, correctly absent from the sitemap, marked do-not-touch. *Disposition: none. Noted so the audit does not "fix" them.*
- **F9. The story family has no recorded dating/sourcing structure.** The registry describes story pages only as "generated from stories data," with no date or source fields named — the gap the news-first repositioning must close (Section 1.6). *Disposition: handled as a build item in WS1-D, not as a records fix.*
- **F10. Image assets (~700 in img/) show no structural finding.** Provenance rules are recorded in the registry and the standard; no duplication or misplacement is in evidence. *Disposition: none. The per-size variant question is IMP-04, handled in Section 3.*

---

## Section 3 — Register sweep: every IMP item and every open decisions/holds row

### 3.1 Imperfections register (IMP-01 to IMP-12)

| Item | Disposition in the overhaul |
|---|---|
| IMP-01 Registry staleness | Closed in the full pass. WS1-A keeps the registries current per release from here (standing records duty). |
| IMP-02 Spanish Open Now labels | Staged in the queued cleanup release (dictionary entries plus the data-i18n hook). WS1 duty: verify live after it lands; no WS1 package. |
| IMP-03 Map-view plain-text names | Staged in the queued cleanup release. WS1 duty: verify live after it lands. |
| IMP-04 Oversized shared logos | Charles decision. If approved, its own generator release producing per-size srcset variants; it is also a WS4 performance lever, so the package is sequenced with WS4 input. Not built on silence. |
| IMP-05 Real-phone layout check | Charles decision/step: the check needs a real phone viewport, which is his device to provide or a session he arranges. If approved, WS1 adds it to the verification routine and records results per page family. |
| IMP-06 Manual WCAG layer | First manual pass done (5 of 8 clean). Remainder: the screen-reader pass and real-phone focus check need human sessions (Charles decision/scheduling); zoom, reflow, and contrast spot checks fold into the WS1 accessibility sweep (WS1-G). The profile-overlay focus item closes by design in WS5 (native dialog/Popover, program addition 4) and is verified there. |
| IMP-07 PWA installability | Closed (verified in the full pass). The manifest rich-install upgrade is a separate enhancement, WS1-H (program addition 8). |
| IMP-08 Inert `_headers` | Charles decision (see F4). WS1-L is the conditional package that executes whichever way he calls it. |
| IMP-09 Coffee Hour stale family and dead tiles | Staged in the queued cleanup release (3 page deletions, tile corrections, sitemap update). WS1 duty: verify live after it lands (deleted URLs return 404, no coffee-hour reference remains). |
| IMP-10 Two pages missing from sitemap | Staged in the queued cleanup release. WS1 duty: verify both URLs appear in the live sitemap after it lands. |
| IMP-11 Generated index drift / generator inputs | Regeneration package staged (9 category pages + 5 tool/input files) and approved by Charles on 2026-11-03; publishes in queue order. Two residues WS1 owns: (i) category-hanceville.html stays held until the Pro Temp profile-family rename is decided (Charles decision; conditional package WS1-M); (ii) the Civitan website field in the generator inputs (nonprofits.json) still holds the old events URL because overrides cannot set the website field — WS1-E corrects the input itself, using only a value the validation lane has verified, or an honestly blank field if no website is verified. |
| IMP-12 Keyboard focus fixes | Staged a11y package (index.html, +201 bytes) awaiting Charles's approval of the named package. On approval it publishes in queue order and WS1 verifies by rendering and computed styles. The checkbox and brand-link minors are documented with exception analysis; fixing them is optional and also his call. |

### 3.2 Decisions and holds (decisions_holds.csv, all rows)

| Item | Disposition in the overhaul |
|---|---|
| Stripe sponsor products (blocked) | Charles or connector fix only. WS1 takes no action; WS2 cannot sell until this clears. Records stay as they are. |
| Deals and Offers board backend | Charles decision. WS1 builds nothing; the localStorage prototype must not publish (standing rule). |
| Gizmo homepage card | Blocked on information only Charles has (what it does, label, placement, card vs embed). No WS1 action until he answers. |
| Hope Pantry Facebook link (held) | Research task under the Section 4 method: a verifiable Page at the correct location (Hanceville Public Library, per Cullman Times 2025-08-27). Link changes only in a staged package after verification. |
| Bitcoin ATM listing link (held) | Ready to stage when Charles approves staging: the link uses LibertyX's own location data (Dale's, 100 Arkadelphia Rd) rather than the 1-follower Facebook stub. Candidate for the first WS1 data package after the queue. |
| Grace Baptist Facebook link (held) | Research task under the Section 4 method. gbchanceville.org is hijacked and is never linked under any outcome. |
| Council roster watch | One fresh authoritative check (city roster) before any council change, run as a research batch; any change then ships in a staged package. WS1 schedules the check; it does not pre-judge the result (the site lists Carla Cain, the roster lists Kenneth Cornelius). |
| Three 502 websites (on watch) | The six-hour watch detects recovery; a restore ships only in a staged release Charles approves. No WS1 action while they return 502. |
| alabamaageline.gov root link (on watch) | Stays linked by Charles's own 2026-11-01 decision, injected footer links notwithstanding. No action; the watch continues. |
| Site email (suspended by rule) | Charles only (Google account recovery). Until he confirms sign-in, every WS1 package is checked to keep the address and mailto links out — a standing guardrail, not a task. |
| Choices items 15, 17, 19, 23, 24 | Awaiting Charles's per-item calls. WS1 packages any outcome he decides; nothing is pre-built. |
| Search Console verification | Charles's click. WS1-I stages everything around it (IndexNow key file ready, sitemap submission and Bing import steps written) so his part takes minutes; also program addition 7. |
| Gate follow-ups (approved, in flight) | Not a WS1 package. On landing, the records duty closes the row: releases log entry, removal of the in-flight decisions row, and the first true CI mobile baseline recorded as measured (feeds WS4). Sequenced ahead of all WS1 publishing. |

---

## Section 4 — Verification-gap plan (recorded sources for the listings that lack them)

**The gap, as measured:** 528 of 724 listings carry recorded source links (program document, generator count). Roughly 196 listings have no recorded source. This section is method and batching only; the research itself runs later, batch by batch, under this method.

### 4.1 Rules of evidence (no exceptions)

1. A source is recorded only when it has actually been found, opened, and read in the research pass. A URL copied from another listing, a search snippet, or a researcher's memory is not a source.
2. The recorded reference states what it supports: the source URL, the date checked, and which fields it backs (name, address, phone, hours, status). A source that supports the address but not the hours leaves the hours unsourced; the listing's other facts are unchanged.
3. Nothing is invented to close the gap: no phone, address, hour, or status is added or altered on the strength of a weak source. Status words (open, closed, moved) are recorded only where the source itself says so.
4. Source quality order: the organization's own official site or official government page first; its official Facebook Page second (subject to the site's existing 30-day activity rule where the Page serves as the main link); reputable local news (for example the Cullman Times) and established directories third. Spam aggregators and every domain on the never-link list are disqualified as sources, as are the spam mirrors named in the program records.
5. Every batch is maker/checker split (master guide rule 5): the validation lane independently re-opens each recorded source in the batch and confirms it says what the record claims, before the batch's package is presented.

### 4.2 Working list and batching

1. Extract the working list from data.js: the listings with no recorded source link, with their category and town attached. The extract, not memory, defines the batches.
2. Batch by category family, about 25 listings per batch (about 8 batches for ~196), so one research session works one kind of source at a time: government and utilities first (official .gov sources), then schools and churches, then businesses by category, then nonprofits and community organizations. Town grouping is the tiebreaker inside a family.
3. Each batch produces one staged package: span-level edits to data.js adding the source references (data.js is edited at span level only, never re-serialized — files_registry.csv), the matching sources.html entries (sources.html entries mirror listing sources, per the registry), and the listings_master.csv update, all in the same package.
4. A listing whose source cannot be found after a genuine pass stays unsourced and is marked researched-with-date in the batch record, so it is not re-researched every cycle; it re-enters only on a schedule the validation lane sets or when new information surfaces.
5. The same method covers, in their own later batches: the held-link research items (Hope Pantry, Grace Baptist), the council roster check, and any published story pages that lack a recorded source (Section 1.6).

### 4.3 What this plan deliberately does not do

It does not research any listing here, does not estimate how many of the 196 will resolve, and does not promise a completion date. Each batch reports its own count: sourced, still unsourced, and any listing whose live facts a source contradicted (those go to Charles as a decision item, not a silent edit).

---

## Section 5 — WS1 package sequence

Precondition (not WS1): the approved queue finishes in order — gate follow-ups, cleanup release, program docs sync, regeneration package — each verified live and logged before the next starts.

1. **WS1-A — Records truth pass.** Correct the master guide's stale picture and counts (F1), the sitemap registry wording (F2), archive-rename the stale local master HTML (F5), record the docs-snapshot standing rule (F6). Files: 00_MASTER_GUIDE.md, files_registry.csv, the archived master file. No live-site files.
2. **WS1-B — Cache version normalization.** Bring every page referencing style.css?v=14 (events.html and any others found in the audit) to the current version; record the full ?v= audit. Files: the affected root/section pages only.
3. **WS1-C — News-first homepage.** Descriptor in the masthead (wording per D1), Latest News lead section fed from stories data, Community Guide grouping and labeling of the guide block, navigation additions (Section 1.4), Spanish dictionary entries for every new label. Files: index.html, data.js (UI dictionary spans only).
4. **WS1-D — Newsroom mechanics.** Visible date and source lines on story pages via the generator/stories data, corrections block on the news page (wording per D1). Files: tools/build_places.py (story template), stories data, the regenerated story family, news root page.
5. **WS1-E — Generator inputs hygiene.** Correct the Civitan website field in nonprofits.json from verified evidence (or honestly blank), confirm and record the places.json regeneration path (F7). Files: tools input JSONs in the repo, files_registry.csv note.
6. **WS1-F — Verification batches V1 to V8 (approximate).** One staged package per Section 4 batch (~25 listings each): source references added from sources actually read, checker-verified. Files per batch: data.js (span edits), sources.html, listings_master.csv.
7. **WS1-G — Accessibility platform-preference sweep.** Forced-colors survival, prefers-reduced-motion, prefers-contrast checks and fixes (program addition 6), plus the zoom/reflow/contrast spot checks left open by IMP-06. Files: style.css, place.css, homepage inline styles in index.html.
8. **WS1-H — Manifest rich-install upgrade.** Description, narrow and wide screenshots (real captures of the site itself), stable id (program addition 8). Files: site.webmanifest, two screenshot assets under img/.
9. **WS1-I — Discovery setup support.** IndexNow key file staged and the Search Console / Bing steps written for Charles (program addition 7). Files: one key file at repo root, program records. His verification clicks complete it.
10. **WS1-J — Longevity operations.** The manual repo-export routine (code plus listings master CSV, kept outside GitHub), the post-release Wayback snapshot checklist, and the GitHub account two-factor/recovery note recorded in the masters as the single point of failure (program addition 10). Files: program records only. Turning the export into a schedule is a new schedule and needs Charles's separate approval under the program's exclusions.
11. **WS1-K — Meta CSP evaluation.** The limits written first (no frame-ancestors, no reporting, no report-only in a meta tag), one candidate policy drafted and gate-tested in staging only (program addition 11). Files: staging only; any live change returns to Charles with the measurements.
12. **Conditional packages, only on the named decisions:** WS1-L (_headers disposition, IMP-08/F4), WS1-M (Pro Temp profile-family rename, unblocks the held category-hanceville.html, IMP-11), WS1-N (per-size image variants, IMP-04, sequenced with WS4).

*End of plan. Prepared for the WS1 lane, 2026-11-03. Nothing in this plan publishes; each package is staged, independently validated, and approved by Charles by name before it goes live.*
