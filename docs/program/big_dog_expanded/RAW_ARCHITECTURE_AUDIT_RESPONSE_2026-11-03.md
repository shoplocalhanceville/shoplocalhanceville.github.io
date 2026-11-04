# Raw Architecture Master Audit — Response, 2026-11-03

Source document: raw_architecture_master_audit.csv, supplied by Charles Adams on 2026-11-03 (an outside generated standards list with a copy and paste audit prompt). Per the standing audit first rule, the document was audited before anything in it was executed. Nothing was built, installed, or changed on the website from this document.

## Document audit findings

Secrets: none. The full CSV was scanned for passwords, tokens, keys, and credential patterns. No matches. The file contains standards rows only.

Weakened security settings: none. The security rows propose strengthening measures (content security policy, subresource integrity). No step disables a protection.

Steps needing separate approval: every implementation step. This report classifies and recommends only.

Items that cannot work as written on this platform: the dynamic nonce content security policy (row 17) requires a server edge that generates a fresh nonce per request. The site is static GitHub Pages and has no such edge. Zstandard compression (row 15) cannot change what visitors receive, because GitHub Pages controls serving compression. History API micro routing (row 4) conflicts with the site's multi page architecture and its search visibility, which rests on more than 2,800 real indexed URLs.

Checked against the real files: the classifications below rest on the 2026-11-03 live site scan (page_scan_2026-11-03) and the current livebase copies, plus tonight's gate results. Patterns verified directly in code: importmap absent, cascade layers absent, speculation rules absent, scheduler.postTask absent, data-testid absent, font face rules zero in style.css, one native dialog present (the zoomDlg logo viewer), AbortController present in homepage code.

## Row classifications

The source prompt demands exactly four labels. Forcing platform impossible rows into those labels would misreport them, so each row carries its closest label plus a verdict where the label alone would mislead.

1. Native ESM Import Maps: [NEEDS TO BE ADDED]. Verdict: not needed. The site already loads with zero bundler through classic scripts (app.js, data.js, place.js). No measured gain. Do not chase.
2. Native CSS Cascade Layers: [NEEDS TO BE ADDED]. Verdict: defer. A style.css layer refactor risks regressions across every page for no metric gain while scores are climbing.
3. Native Interactivity Elements: [NEEDS BUILDING]. One native dialog is live today (zoomDlg). The dialog and Popover build for the directory assistant and profile overlay is already designed in Workstream 5 and also closes the open accessibility overlay focus item.
4. History API Micro Routing: [NEEDS TO BE ADDED] by label only. Verdict: DO NOT IMPLEMENT. Real pages are the architecture and the search strategy. Client side routing would break deep links, the news sitemap model, and share links.
5. Speculation Rules API: [NEEDS BUILDING]. Already in Workstream 4 as a measured prefetch experiment only, never prerender by default, adopted only on a measured gate gain.
6. Native View Transitions API: [NEEDS TO BE ADDED]. Verdict: defer. Cosmetic, Chromium led, no Core Web Vitals gain. Behind every real performance lever.
7. Prioritized Task Scheduling: [NEEDS BUILDING] in corrected form. The chosen pattern, chunked rendering, already shipped in the performance package (PR #62). scheduler.postTask stays a fallback only if a measured INP failure appears, because its browser support is uneven.
8. CSS Containment and Layout Shift Lock: [IMPLEMENTED] by measured outcome. The technique differs (reserved heights and explicit containers rather than CSS contain properties, which are absent), and the gate measured homepage mobile layout shift at 0.0003 across five runs on PR #63, with layout assertions passing on every tested page.
9. Font Metric Overrides: [NEEDS TO BE ADDED] by label only. Verdict: NOT APPLICABLE today. style.css declares no webfonts; the site uses a system font stack, so there is no font swap to shift layout. Revisit only if a webfont is ever adopted.
10. AbortController Memory Hygiene: [NEEDS BUILDING]. Present in homepage code, not yet a universal standard across the dynamic work in app.js and place.js. Folded into the open raw code audit.
11. Explicit Object Pooling: verdict DO NOT IMPLEMENT. The site has no high frequency typed array workloads; garbage collection pauses are not a measured problem anywhere in the records. This is speculative complexity.
12. Origin Private File System: verdict DO NOT IMPLEMENT. The service worker cache already covers the site's caching needs. OPFS solves a storage problem this site does not have and adds failure modes.
13. Asynchronous Video Hydration: [NEEDS BUILDING], low priority. Poster first patterns exist on some media; the site is image led. Formalize in the media pipeline where real video appears.
14. Metadata Stripped Deterministic Tarballs: [NEEDS TO BE ADDED], archive only. Zero effect on the site or its scores. The longevity decision already on record is off GitHub exports plus Wayback snapshots; deterministic packaging is an optional upgrade to that archive step.
15. Zstandard Ultra Compression: [NEEDS TO BE ADDED], archive only. Cannot affect delivery on GitHub Pages, which sets its own compression. Compression header work is already on the evidenced do not chase list.
16. BLAKE3 Manifest and PAR2 Recovery: [NEEDS TO BE ADDED], archive only. A hash manifest is cheap and genuinely useful for archive integrity; PAR2 is optional. Zero Lighthouse effect either way.
17. Dynamic Nonce Based CSP Level 3: [NEEDS BUILDING] in corrected form only. As written it is impossible on GitHub Pages. The applicable form, a gate tested meta content security policy evaluation with its limits written first, is already in Workstream 1 from the standards gap brief.
18. Subresource Integrity: verdict MOSTLY NOT APPLICABLE. First party files are same origin, where integrity hashes add nothing. The one major third party script, the Facebook embed loader, is injected dynamically by Meta and cannot carry a fixed hash. SRI applies the day a static third party asset is ever adopted.
19. Lighthouse CI Headless Gating: [IMPLEMENTED]. Shipped as PR #46 and verified on main: both configuration files assert 1.0 in all four categories with five run medians and merge blocking, and the gate ran on tonight's releases (PR #63 results reported to Charles).
20. Real User Monitoring Telemetry: [NEEDS BUILDING] only by Charles's decision. It conflicts with the measurement decision already made in Workstream 3 (the free analytics choice) and with the site's no tracking posture, including the on device language detection shipped tonight. Field data for the origin is partially available without adding any script. No telemetry script is added without his word.
21. Explicit Automated Test Hooks: [NEEDS TO BE ADDED] if end to end testing is adopted. Verified absent in today's scan. Current gates are Lighthouse CI plus link, HTML, accessibility, and security checks. Hooks belong with the first Playwright suites if the validation lane adopts them, not before.

## Top 5 high impact priorities, from tonight's measured state

1. Close the last homepage mobile performance gap, which is paint timing (0.83 mobile, first paint 3.25 seconds under gate conditions), through the Workstream 4 per size image variants and largest paint work. This, not any row in the CSV, is the real distance to a mobile 100.
2. Finish and publish the automatic language package, in its final rebase tonight, completing today's confirmed scope.
3. Build the Workstream 5 native dialog and Popover package for the assistant and profile overlay (CSV row 3 in its useful form), closing the open accessibility overlay item at the same time.
4. Run the corrected content security policy evaluation from Workstream 1 (CSV row 17 in its possible form), gate tested, limits written first.
5. Run the speculation rules prefetch experiment (CSV row 5) as a measured A and B against the gate, and adopt it only on a measured gain.

## What was not done

No row was implemented from this document, no code was changed, and nothing was published. The full line by line code audit beyond the patterns verified above is queued as brief BD-012 in the first brief queue, as its own scoped pass.
