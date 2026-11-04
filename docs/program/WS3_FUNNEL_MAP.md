# Workstream 3 — Funnel Maps, UTM Convention, and the Measurement Decision Brief

**Status:** Design document for the Complete Overhaul Program, 2026-11-03. Nothing in this document is built or published. Per program research addition 12, the measurement method is decided before any funnel is built, because the analytics choice determines what the funnels may honestly promise. The analytics choice is Charles Adams's; this document compares and does not choose.

**Standing facts the funnels are built on:** the site is a static site on GitHub Pages with no server access and no server logs available to the owner; the site email (shoplocalhanceville@gmail.com) is suspended and off the site, so every contact path in these funnels ends at the Hanceville Entertainment and Shopping Facebook Page's messages; sponsor pricing (Spotlight $175/month, Premium $350/month) was approved 2026-11-03, but nothing may be offered to a business until Charles approves the offer wording, and payments remain blocked until Stripe is fixed.

**Sources:** program research brief `~/workspace/overhaul_research_2026-11-03/STANDARDS_GAP_BRIEF.md`, sections 2E and 2F (analytics capabilities, consent consequences, funnel measurement limits); vendor documentation and pricing pages as noted per candidate (GoatCounter documentation and changelog on campaign and event handling; Plausible pricing page, checked October 2026; Google Analytics product terms).

---

## 1. Funnel A — Visitor to business

Purpose: turn a Facebook audience into a phone call, a directions request, or a visit for a listed business.

| Step | What happens | What can be counted, and by what |
|---|---|---|
| 1. Facebook post | A Page post (news item, This Week post, business spotlight) carries a link to the site, tagged under the UTM convention in section 3 | Reach, reactions, and link clicks as Meta reports them in Page insights. These are Meta's numbers, reported as Meta's |
| 2. Site landing | The visitor lands on the linked page: a news story, a category page, or a business profile | Pageviews and sessions for that page, attributed to the campaign, **only** by an analytics tool that reports UTM campaigns (section 4). Without such a tool this step is invisible |
| 3. Profile view | The visitor opens the business's profile page (directly, if the post linked there, or by tapping through from a category or search) | Profile pageviews in the analytics tool. Honest limit: cookieless tools attribute the campaign to the landing session; profile views reached after further browsing are counted as profile views, and campaign attribution for them is the tool's session model, not a per-person trail |
| 4. Action | The visitor taps Call (`tel:` link), Directions (the profile's map link), or the business's Facebook link | Countable **only** as a tap, and only if the chosen analytics tool supports custom click events and they are enabled for these links. See section 5 for what a tap does and does not prove |
| 5. Real-world result | A completed call, a visit, a purchase | Not measurable by this website in any configuration. Knowable only if the business itself reports it |

Design rules for Funnel A:

- Every Facebook post link to the site carries UTM tags under section 3, including the weekly content engine's drafted posts; the draft carries the tagged link so approval covers the exact URL.
- Posts link as deep as the content honestly allows: a spotlight post links to the profile, a category roundup to the category page, a news story to the story. Shallow links to the homepage waste the funnel's best-measured step.
- No step requires the visitor to create an account, install anything, or pass an interstitial. The funnel is: post, page, profile, tap.

## 2. Funnel B — Sponsor path

Purpose: turn the Page's audience and the site's visitors into a sponsor conversation Charles controls end to end.

| Step | What happens | What can be counted, and by what |
|---|---|---|
| 1. Recruitment content | A Page post or a site section explains that local sponsorships exist and points to the sponsors page (WS2, section 2.4) | Meta reach and clicks for the post (Meta's numbers); sponsors page pageviews by campaign (analytics, if UTM-capable) |
| 2. Sponsors page | The visitor reads the two approved packages and prices and the honest measurement note (WS2, section 11) | Pageviews; time on page only if the chosen tool reports it (the cookieless candidates report pageviews and events, not engagement time in any form Charles should quote) |
| 3. Contact | The visitor taps the contact route: a message to the Hanceville Entertainment and Shopping Facebook Page (Messenger). The site email is suspended and is not offered anywhere in this path | The tap is countable as an event only under the same condition as Funnel A step 4. The conversation itself happens in Messenger, where Charles sees it directly; no tool is needed to count his own inbox |
| 4. Agreement | Charles and the business agree terms in the Messenger conversation (or in person). Enrollment is manual | Nothing to count; recorded in the sponsor ledger when it happens |
| 5. Payment | Blocked today: no Stripe product, price, or payment link exists (two creation attempts returned HTTP 403 on 2026-11-03). Until Stripe is fixed, no payment step is built into the funnel and no offer wording may imply one | — |
| 6. Delivery and report | The sponsor's placement runs under WS2; at month end the sponsor receives the WS2 section 11 report | The report's numbers are defined in WS2 and limited to what section 4's chosen tool produces |

Design rules for Funnel B:

- The sponsors page never promises views, clicks, calls, or sales; it describes the placement, the price, and the exact report the sponsor will receive.
- Paid sponsor content anywhere in either funnel carries the labeling required by WS2 section 5 (on Facebook: Meta's "Paid partnership" label plus plain disclosure text).
- The Meme Factory Page carries no sponsor recruitment and no sponsor placements, per the approved sponsor terms; it may link the site editorially only.

## 3. Draft UTM naming convention (for Charles's approval)

Parameters on every link from Facebook (and any other external source) to the site:

| Parameter | Rule | Values in use |
|---|---|---|
| `utm_source` | The property the link appears on | `facebook-page` (Hanceville Entertainment and Shopping Page), `facebook-profile` (Charles's personal profile shares), `messenger` (links sent in Page message replies) |
| `utm_medium` | The format carrying the link | `post`, `reel`, `story`, `share`, `message` |
| `utm_campaign` | The content series and subject, lowercase, hyphens, no spaces | `news-<story-slug>`, `this-week-<yyyymmdd>`, `spotlight-<yyyymm>-<business-slug>`, `sponsor-recruit-<yyyymm>`, `guide-<category-slug>` |
| `utm_content` | Optional; only when two versions of the same post run | `a`, `b` |

Rules: values are lowercase with hyphens only; a campaign name is never reused for a different subject; UTM tags are never added to links inside the site itself (internal navigation stays clean so the tool's page reports are readable); every tagged link used in a post is the exact link Charles approved in the draft. A link log (post, date, full tagged URL) is kept with the content records so any number in any report can be traced back to the post that produced it.

## 4. The measurement decision brief

**The requirement, stated once:** the tool must (a) report traffic by UTM campaign, because without campaign reporting the funnels in sections 1 and 2 cannot be measured at all; (b) preferably support custom click events, because Funnel A's step 4 and Funnel B's step 3 are otherwise invisible; (c) stay cookieless if possible, because a cookie-setting tool changes the site's consent position (research brief section 2E: consent notices and do-not-sell mechanics arrive with GA4-class tooling, and with EEA/UK consent-management duties if personalized ads ever appear); (d) cost little or nothing in page weight, because every build is gated on Lighthouse scores; (e) retain history long enough to produce monthly sponsor reports and month-over-month comparisons.

| Candidate | UTM campaign reporting | Click events (tel:, directions, slot taps) | Cookies / consent effect | Performance cost | Price and history |
|---|---|---|---|---|---|
| **Cloudflare Web Analytics** | **No.** Documents no UTM campaign reporting | **No.** No custom events | None; cookieless, no personal data | Sub-kilobyte-class beacon; not measurable against this site's budgets | Free at every tier, no traffic limit. History about six months. **Fails requirement (a) and (b): cannot measure the funnels** |
| **GoatCounter** (hosted) | **Yes.** Campaigns are read automatically from `utm_campaign`, with source from `utm_source` (vendor changelog and campaign documentation) | **Yes, in the product.** Click events via a data attribute or a script call (`count({event: true})`), using sendBeacon, which is the mechanism that makes outbound and `tel:` taps countable at all. Event availability and limits on the specific hosted plan must be re-verified before Charles relies on tap counts | None; cookieless | Script under 1 KB gzipped | Hosted service free for reasonable non-commercial use (open source, EUPL). Caveat carried from the research brief: once sponsor revenue makes the site commercial, the hosted terms must be re-read before relying on the free tier, and self-hosting is not available in this stack. No goals or funnel reports: step counts are assembled from pageviews by campaign plus event counts, by hand |
| **Plausible** (hosted) | **Yes.** Full UTM reporting (source, medium, campaign) with automatic channel grouping | **Yes.** Custom events and goals on all paid plans, including outbound link clicks; tap events for `tel:` and directions links are set up as custom events | None; cookieless, no personal data, EU-hosted | Script under 1 KB | **Paid; no free hosted tier** (30-day trial only). From $9/month for 10,000 pageviews on one site (Starter, goals and custom events included); Growth $14/month; Business $19/month adds funnels, custom properties, and the Stats API. Prices checked against the vendor's pricing page, October 2026. Retention three to five years by plan |
| **Google Analytics 4** | **Yes.** Full campaign reporting (session campaign, source, medium) | **Yes.** Custom events for any tap; the deepest funnel and conversion reporting of the four | **Changes the site's position.** Sets cookies; brings consent-notice and do-not-sell/share mechanics and the heaviest compliance surface of the four (research brief, section 2E) | The heaviest script of the four by a wide margin, loaded from Google on every page; a standing cost against the performance gate | Free (the paid 360 tier is enterprise software and not relevant here). Retention and reporting limits apply on the free tier; the interface and data model are by far the most complex for a one-person newsroom to read monthly |

**Reading of the table (not a choice):** Cloudflare Web Analytics is the only candidate that fails the stated requirement outright, despite being free: a funnel program measured by it would be unmeasured. The remaining three all meet requirement (a). They separate on three axes Charles weighs himself: GoatCounter is free and cookieless but carries the commercial-terms re-read and manual report assembly; Plausible is cookieless and complete including tap events, at a real monthly price from the goal's earnings; GA4 is free and the most capable, at the cost of cookies, consent mechanics, script weight, and complexity.

## 5. What this stack cannot count (stated so no funnel ever promises it)

- **A `tel:` tap is not a phone call.** No server exists on this stack to observe anything after the tap; even with click events enabled, the number recorded is taps on the Call link. Some taps are accidental, some calls are abandoned, and calls made by dialing the number manually are invisible. Sponsor and business reporting must say "taps on the Call button," never "calls."
- **A directions tap is not a visit.** It records that a visitor opened the map link, nothing about arrival.
- **There are no server logs to fall back on.** GitHub Pages gives the owner no access logs, so any number not captured by the chosen analytics tool at the moment it happens is not recoverable later. This is why the measurement decision precedes the funnel build.
- **No cross-site or per-person journeys.** Cookieless tools count pages and events in aggregate. None of the candidates in this program will follow an individual from a Facebook post to a store counter, and the program does not attempt it.
- **Facebook-side numbers are Meta's.** Reach and click figures in Page insights are produced by Meta's systems and are reported to sponsors labeled as such, never merged with site analytics into a single invented total.

## 6. Decision list for Charles

1. **Analytics choice:** GoatCounter (free, cookieless, manual report assembly, commercial-terms re-read required once revenue starts), Plausible (from $9/month, cookieless, tap events and goals included, funnels at $19/month), or GA4 (free, full capability, cookies and consent mechanics, heaviest script). Cloudflare Web Analytics is listed for completeness and fails the funnel requirement. No option is chosen in this document.
2. **Tap counting:** whether counts of taps on Call, Directions, and sponsor contact links are wanted. Wanting them requires an events-capable tool (any of the three above) and one extra line in the sponsor report's honesty note, already drafted in WS2.
3. **UTM convention:** approve the draft in section 3, or amend the value lists before the first funnel post is drafted.
4. **Report history:** whether monthly sponsor reports need month-over-month history beyond about six months, which is a retention fact to weigh inside decision 1 (shortest retention among the candidates that pass: Cloudflare is already excluded; GoatCounter's hosted history and each Plausible plan's three-to-five-year retention differ).
