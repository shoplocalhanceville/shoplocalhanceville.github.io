# Complete Overhaul Program — confirmed by Charles Adams, 2026-11-03

Governing rules: Charles Development Standard v1.1; raw hand-written code only (plain HTML, CSS, JavaScript; the Python page generator counts as raw code that writes raw pages); facts only; scores reported as measured, never guaranteed; nothing publishes without Charles's approval of the named package; the already-approved publish queue (gate follow-ups, cleanup release, program docs sync, regeneration package) finishes first.

Form: five workstreams, one scoped pass each, each pass ending in a report to Charles before the next begins. Excluded unless Charles adds them: new schedules, account changes, outside ad networks, any message sent to a business, any offer made to a business before he approves the wording.

Standing rule: the overhaul is targeted, not blanket. What already measures 100 is protected, not rewritten. No package merges if it drops any tested page below the standard.

## Positioning — news first (directed by Charles, 2026-11-03)

The website presents first as a local news organization. The community guide (the directory of listings, profiles, and town information) is a featured service within that news organization, not the other way around: the site gives visitors purpose for being on it besides news, but the focus and identity are news. Workstream 1's reorganization plan leads with this repositioning: identity and naming, homepage hierarchy with news in front, and the Community Guide presented as a named feature of the news organization. Newsroom practice applies to all news content: every item sourced and dated, corrections recorded, nothing published on rumor.

## Quality and rights standard (directed by Charles, 2026-11-03)

The full text lives in QUALITY_AND_RIGHTS_STANDARD_2026-11-03.md in these masters and governs every workstream below: accuracy before building on every surface (code, labels, writing, spelling, fonts, images, video) with nothing guessed or assumed; documentation written as the work happens (detailed notes, finals, coding sheets, cheat sheets, troubleshooting entries); and copyright and legal compliance across the whole site and all its content and media, with any item whose rights cannot be verified simply not used.

## Verification standard (directed by Charles, 2026-11-03)

Everything on the site is valid and confirmed, with no misinformation, and every piece of information carries a backup reference. Concretely: each listing and each news item records its source (the sources registry and the site's sources page), a fact with no source is researched or held rather than published, and the validation lane checks references, not just links. The generator's current count of listings with recorded source links is 528 of 724; closing that gap honestly, by research and never by invention, is part of Workstream 1.

## Workstream 1 — Reorganization and standards rebuild
Full pass over the site's file structure against the program registry (files_registry.csv) and the Development Standard. Any file or aspect that falls short is rewritten, recoded, or rebuilt in raw code and reorganized into its proper place. Explicitly sweeps the open register (imperfections_register.csv), including the per-size image variants decision (IMP-04), the real phone layout check (IMP-05), the _headers keep-or-remove decision (IMP-08), and the Civitan generator-input residual. Deliverable: a reorganization plan first, then staged fix packages.

## Workstream 2 — Ads (local sponsors)
Sponsor ad placements designed and built into the site in raw code, sized to the approved pricing (Spotlight $175/month, Premium $350/month). Local sponsors only. Fixed slot sizes so ads cannot shift layout. Paid placements labeled as sponsored. Nothing offered or sold until Charles approves the offer wording; payments remain blocked until Stripe is fixed. Deliverable: ad placement design first, then a staged build package.

## Workstream 3 — Funnels
Paths that turn visitors into business: Facebook post to website to business profile to a call or visit action; and a sponsor path from the Page to a sponsor section to contact. Measurement without cookies: link discipline and first-party counts. Deliverable: a funnel map first, then staged build packages.

## Workstream 4 — Performance to 100
The measured gap: desktop homepage Performance 0.98 (paint timing, measured against the gate's uncompressed test server); Accessibility, Best Practices, and SEO at 100 on the other tested pages; the first true mobile baseline arrives with the gate follow-up release. Levers: rework delivery of the 592 KB listings data file so a phone does less work up front; per-size image variants (IMP-04); the gate fairness fix (the gate's plain test server serves uncompressed, which GitHub Pages does not). Every step measured and reported as measured.

## Workstream 5 — On-site intelligence in raw code
Visitor-facing intelligence with no server: typo-tolerant search with synonyms, recommendation rails, and a directory assistant that answers strictly from the verified listing data and says when it does not know. Rule: intelligence loads lazily, after the page is fast, and any feature that drops a gate score does not ship.

## Research additions — folded in 2026-11-03 (brief: ~/workspace/overhaul_research_2026-11-03/STANDARDS_GAP_BRIEF.md)

Fourteen additions, each verdicted and sourced in the brief:

**Into WS4 (performance):**
1. Pin and record the Lighthouse version in the gate and in a per-release score ledger. Lighthouse 13.6 changed the simulation so scores move on unchanged pages; an unrecorded version makes any score change unattributable.
2. Adopt an explicit INP pattern for data-heavy interactions: render the 724-record lists and search results in chunks, yielding to the main thread (scheduler.yield() where supported, setTimeout fallback), so no interaction handler runs a task over about 50 ms.
3. Run a measured speculation-rules experiment: same-origin prefetch of profile pages at conservative eagerness from home and category pages, honoring Save-Data, with before and after measurement; promote to prerender only if prefetch proves out.

**Into WS5 (on-site intelligence):**
4. Build the directory assistant and the profile overlay on native dialog (showModal) and the Popover API, so the browser supplies focus trapping, Escape to close, and focus restoration. This also closes the manual WCAG pass's one unassessed item, the profile overlay's focus management.
5. Optional voice input for search and the assistant, feature-detected, with its limits stated on the label: speech recognition is absent in Firefox, Chrome sends the audio to Google's servers, and the API is a community group report, not a finished standard. Typing always remains the primary path.

**Into WS1 (reorganization and standards):**
6. Add a platform-preference hardening check to the accessibility sweep: the theme must survive Windows forced-colors mode with no information carried by background images or color alone; all animation must honor prefers-reduced-motion; prefers-contrast is checked.
7. Complete the owner-gated discovery setup as named program steps: Search Console URL-prefix verification and sitemap submission, Bing Webmaster Tools import from Search Console, and an IndexNow key file with a publish-time ping. The verification clicks are Charles's alone.
8. Upgrade the web app manifest for Chrome's rich install sheet: description, screenshots (one narrow, one wide), and a stable id. The install criteria themselves are already met.
9. Add a short plain-language privacy page when analytics or a form backend lands: what is collected, that form submissions sit on the form vendor's servers until Charles deletes them, and the deletion routine.
10. Add longevity insurance to program operations: a scheduled full export of the repo (code plus the listings master CSV) kept outside GitHub, Wayback Machine snapshots of the homepage and key town pages after major releases, and the GitHub account itself (two-factor authentication and recovery) recorded in these masters as the site's single point of failure.
11. Evaluate one meta-delivered Content-Security-Policy, gate-tested, with its limits written down first: a meta CSP can restrict resource loading, but frame-ancestors, reporting directives, and sandbox are ignored in a meta tag, there is no report-only mode, and it can never provide clickjacking protection on GitHub Pages.

**Into WS3 (funnels):**
12. Decide the funnel measurement method before any funnel is built: a written UTM naming convention plus an analytics choice that can actually report campaigns. Cloudflare Web Analytics documents no UTM campaign reporting and no custom events, so it cannot measure funnels; the analytics decision is made against the funnel requirement, not price alone.

**Into WS2 (ads):**
13. Write sponsor-slot design rules into the build spec before anything is sold: fixed IAB sizes (320x50 mobile banner, 300x250 rectangle, 728x90 leaderboard), the slot's space reserved in CSS so a late creative causes zero layout shift, every Coalition for Better Ads disallowed format banned outright (pop-ups, prestitials, large sticky ads, auto-playing video with sound, flashing animation, ad density over 30 percent on mobile), and every paid placement labeled Sponsored.
14. Define the sponsor report format before selling: on a static site the only honest numbers are the chosen analytics tool's pageview counts for the sponsor's profile page and slot pages. That format goes into the sponsor package so no number is ever promised that the stack cannot produce.

**Checked and already covered (from the brief, section 4):** Core Web Vitals thresholds and the field-data rule; WCAG 2.2 AA targeting with the IMP-12 fixes; HTTPS and the header platform limits; the structured data plan (every type in it survived Google's 2025-2026 retirements); Search Console and sitemap hygiene; local visibility basics (NAP consistency, the Register page Google Business Profile nudge).

**Do not chase (from the brief, section 5, each evidenced):** llms.txt (a one-person proposal; Google states in writing it does not use it); WCAG 3 and APCA (a draft whose contrast algorithm is officially yet to be determined; APCA was removed in 2023); on-device ML models (30 MB to 5 GB downloads to answer questions the verified-data lookup answers exactly); Brotli and compression dictionaries as site work (real standards, but gated on response headers GitHub Pages will not let the owner set).

**Stale items flagged in older research (brief, section 3):** the October infrastructure document's 36-page sitemap figure (live sitemap: 2,843 URLs) and its pre-externalization page sizes; its analytics recommendation now carries the funnel caveat in item 12 above; tonight's earlier standards brief overstated Chrome's install criteria (they are met; item 8 is the enhancement). The IMP-11 drift estimate was already corrected in the register.
