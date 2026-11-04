# Workstream 2 — Sponsor Placement Design (Design Only)

**Status:** Design document for the Complete Overhaul Program, 2026-11-03. Nothing in this document is built, sold, offered, or published. Pricing referenced here (Spotlight $175/month, Premium $350/month) was approved by Charles Adams on 2026-11-03 and is recorded in `~/workspace/goals/800-a-week-from-facebook-posting-with-the-website/GOAL.md`. No placement may be offered to any business until Charles approves the offer wording, and payments remain blocked until Stripe is fixed (two connector product-creation attempts returned HTTP 403; zero Stripe products exist as of 2026-11-03).

**Sources for the standards cited:** IAB Standard Ad Unit Portfolio (320x50, 300x250, 728x90, 300x600 sizes); Coalition for Better Ads, Better Ads Standards (disallowed ad experiences, mobile ad density under 30 percent); FTC Act Section 5 and the FTC Endorsement Guides, 16 CFR Part 255 (revised 2023), requiring clear and conspicuous disclosure of paid material connections; program research brief `~/workspace/overhaul_research_2026-11-03/STANDARDS_GAP_BRIEF.md`, sections 2E and 2F.

---

## 1. Governing principles

1. **News first, guide protected.** This site presents as a local news organization, with the Community Guide as a featured service inside it. Sponsor slots are additive furniture around that product. A slot may never displace a news story, sit above the lead news on the homepage, interrupt the emergency strip, occupy the bottom tab bar, or reduce the guide's search, listings, or profile content. If a page layout cannot hold a slot without pushing news or guide content down a screen, the page gets no slot.
2. **Zero layout shift, by construction.** Every slot reserves its exact box in CSS before any creative exists (section 3). A late, missing, or unsold creative can never move page content. This restates the reserved-space discipline Standard v1.1 already imposes on embeds.
3. **House-served only.** Creatives are first-party static files served from the site's own repository. No third-party ad scripts, no iframes from ad networks, no programmatic auctions, no tracking pixels. Consequences recorded in the research brief (section 2E): direct-sold static placements set no cookies, sell no data, and create no new consent duties; ads.txt and sellers.json are not applicable unless a third-party network is ever adopted, which is excluded from this program.
4. **Labeled, always.** Every paid placement carries a visible "Sponsored" label (Spanish: "Patrocinado"), in the placement itself, per section 5.
5. **Spanish parity and accessibility are build requirements**, not follow-ups (sections 8 and 9).
6. **The gate rules.** Any slot build that drops a tested page below the Development Standard's Lighthouse gate does not ship. Creative weight caps and lazy loading are in section 10.

## 2. Slot inventory

Sizes are IAB standard units. Each slot has one desktop form and one mobile form; the box is reserved at both breakpoints (section 3). Density is held far below the Better Ads Standards ceiling of 30 percent of mobile page height: no page carries more than one in-flow slot per screen-length of content, and no page carries more than two slots in total.

### 2.1 Homepage (news-first hierarchy)

| Slot | Position | Desktop | Mobile | Notes |
|---|---|---|---|---|
| H-1 Sponsor strip | Between the lead news block and the Community Guide rails, in the page flow | 728x90 leaderboard | 320x50 banner | Never above the lead story; never inside or beside the emergency strip; the strip is visually part of the guide furniture, not the news column |
| H-2 Sponsor row card | One card inside a dedicated "Our Sponsors" row, styled as a row of the guide, separate from every editorial rail | 300x250 card | 300x250 card | Distinct heading ("Our Sponsors" / "Nuestros patrocinadores") so the row can never be mistaken for the Featured listings rail or a news rail |

The homepage carries no other sponsor slots. The rotating free Business Spotlight and all news rails are editorial space and are never sold and never shared with paid creative (section 7).

### 2.2 Category pages

| Slot | Position | Desktop | Mobile | Notes |
|---|---|---|---|---|
| C-1 In-flow rectangle | After the first group of listing tiles, in the tile flow | 300x250 | 300x250 | One per category page. The tile grid keeps its reserved box even when the slot is unsold, so tile positions never move between sold and unsold states |

### 2.3 Profile pages

| Slot | Position | Desktop | Mobile | Notes |
|---|---|---|---|---|
| P-1 Page sponsor rectangle | Below the profile's own facts, hours, and action buttons; never between the business name and its contact actions | 300x250 | 300x250 | When the profile's own business is the sponsor, this slot may carry that sponsor's own creative ("Sponsor of this page"); otherwise it carries a rotating sponsor from the general pool. A business is never required to sponsor its own profile to keep its listing, and an unpaid profile looks identical in structure |

### 2.4 Sponsors section page

One dedicated page, "Sponsors" (Spanish: "Patrocinadores"), which is the landing target of the sponsor funnel in WS3. It holds: the labeled list of current sponsors at full size, the two approved packages and their approved prices, and the contact route (Facebook Page messages; the site email is suspended and appears nowhere). Sponsor creative on this page is presented at 300x250 per sponsor with the same labeling rule. This page is program furniture, not a slot, and it is the only page whose primary content is advertising.

### 2.5 What gets no slot

News story pages carry no in-story advertising in this design; if that ever changes it is a new design decision for Charles, not an extension of this one. Search results, the assistant, the map view, and utility pages (sources, accessibility, privacy) carry no slots.

## 3. Reserved space: the CSS rule

Every slot is a fixed container whose dimensions are declared before content loads:

- Desktop leaderboard: `aspect-ratio: 728 / 90` with the container width capped at 728px; mobile banner: `aspect-ratio: 320 / 50`; rectangles: `aspect-ratio: 300 / 250`. Where aspect-ratio alone is insufficient (older engines), an equivalent `min-height` at each breakpoint is declared in the same rule.
- The creative image inside carries explicit `width` and `height` attributes matching the slot, `loading="lazy"` below the fold, and `decoding="async"`.
- An unsold slot renders the reserved box with a house message (section 4.3) or, where Charles prefers, collapses only on pages where collapse cannot move other content (never on the homepage strip). The default is: the box never changes size.

## 4. House-served architecture

### 4.1 Creative as first-party static files

Each sponsor creative is a static image file (WebP preferred, JPEG fallback) stored in the site repository alongside the site's other images, plus a text alternative (section 9). No creative is hot-linked from a sponsor's server: hot-linking would hand layout, weight, and availability control to a third party and would break if the sponsor's host changes.

### 4.2 Rotation by the existing daily pattern

Sponsors are entries in a small sponsor data array maintained in the same data-driven pattern as the listings. Rotation reuses the site's existing daily-rotation pattern (the same day-index approach that rotates the featured listings): on a given day, each slot shows the sponsor selected by the day index for that slot, so rotation is deterministic, cache-friendly, identical for every visitor on that day, and requires no server, no cookies, and no script library. Where a slot has more sponsors than days in a billing month, the rotation cycles through all of them evenly before repeating.

### 4.3 Unsold inventory

Unsold slot time is filled with house messages only: promotion of the Community Guide, the Register or Update Your Business page, the sponsors section itself, or public-service content already on the site (for example the emergency information). House messages are never styled to imitate a commercial sponsor and never carry the "Sponsored" label; they carry "From Hanceville Entertainment and Shopping" or no label, so the labeling signal stays meaningful.

### 4.4 Creative intake

A sponsor supplies: the creative image at the slot's exact pixel dimensions (or source art the build lane crops to size), the destination link (the sponsor's profile page on this site by default; the sponsor's own website only if that link already passes the site's normal link verification), and the text alternative in English and Spanish (section 8). Creative is checked like any other site content under the verification standard: no claim in a creative is published that the site could not stand behind, and no creative runs before Charles approves it as part of the sponsor package.

## 5. The Sponsored labeling rule

Labeling is law, not style. Under the FTC Act Section 5 and the Endorsement Guides (16 CFR Part 255, revised 2023), a paid connection a reader would not expect must be disclosed clearly and conspicuously: difficult to miss, easily understandable, and placed with the content itself. Accordingly:

- Every paid placement carries the word **Sponsored** (Spanish mode: **Patrocinado**) as visible text at the top of the slot, in the site's normal text styling at a readable size, not in an image, not in a tooltip, not in a footer.
- The label is part of the slot markup, so it appears in every state of the slot (sold, rotated, or in the sponsors section) and is present for screen readers as text.
- The same duty applies on the Facebook side of the funnels (WS3): paid posts carry Meta's "Paid partnership" label plus plain disclosure text in the post.
- An unlabeled paid placement is a stop condition: it does not publish.

## 6. Banned formats

The following Coalition for Better Ads disallowed experiences are banned outright in this design, on every page, at every tier (Better Ads Standards; Chrome enforces these against offending sites):

- Pop-up ads of any kind
- Prestitial ads, with or without a countdown
- Large sticky ads
- Auto-playing video with sound
- Flashing or strobing animation
- Full-screen scrollover ads
- Ad density above 30 percent of mobile page height (this design stays far below it; see section 2)
- Any format that imitates site navigation, system warnings, or news content

Animated creative of any kind is additionally constrained by the accessibility rules in section 9; the default creative is a still image.

## 7. Rotation and fairness: paid sponsors and the free editorial spotlight

Two different things carry similar furniture on this site, and the design keeps them visibly and mechanically separate:

- **The free rotating editorial Business Spotlight continues unchanged.** It is an editorial feature, selected by the site, never sold. Per the approved "no free" rule in the sponsor program: sponsor spotlights are paid only, and the editorial spotlight is not a sponsor product. Paid placements never appear inside the editorial spotlight's position, never borrow its heading, and are never described with its name.
- **Paid rotation is even.** Within a slot and tier, every active sponsor receives an equal share of days over each billing month under the daily rotation (section 4.2). No sponsor can buy extra rotation share in the same slot; position priority is sold only as the tier defines it below.
- **Proposed website entitlements by tier** (for Charles to approve as part of the offer wording; the approved Facebook deliverables for each tier are recorded in the goal file and are not changed by this design):
  - *Spotlight, $175/month:* rotation share in the H-1 homepage sponsor strip and the C-1 category rectangle pool, plus a listing-card entry on the sponsors section page.
  - *Premium, $350/month:* everything in Spotlight, plus a fixed card in the H-2 "Our Sponsors" homepage row for the full month (not rotated out), and P-1 page-sponsor presence on the sponsor's own profile page for the full month.
- **No displacement.** A sold slot never removes, demotes, or delays an editorial feature, a listing, or another sponsor's contracted rotation. If inventory in a capped slot is oversold, the excess is wait-listed, not squeezed in.
- **No promised results.** Consistent with the approved sponsor terms, no views, clicks, calls, or sales are promised to any sponsor at any tier; the report in section 11 is the entire measurement commitment.

## 8. Spanish parity

The site runs a full Spanish mode through an on-page dictionary, and sponsor furniture follows the same pattern:

- Every fixed string a slot adds ("Sponsored", "Our Sponsors", the sponsors section headings, house messages, the package descriptions on the sponsors page) is a dictionary entry with an English and a Spanish form, shipped in the same release as the slot itself. A slot does not ship with English-only furniture.
- Sponsor creative that contains words must be supplied or approved in both languages, and the slot serves the version matching the visitor's language mode. Image-only creative must still carry its text alternative in both languages (section 9).
- The sponsor report (section 11) is delivered to the sponsor in English; the numbers are the same regardless of language mode because the analytics counts pageviews, not language states. This limitation is stated in the report rather than papered over.

## 9. Accessibility requirements for slots

Slots are held to the site's WCAG 2.2 AA standard, the same bar as every other component:

- A creative is a link with a meaningful text alternative naming the sponsor and the action (for example, "Sponsored: Cut N Up Barber and Style, view profile"), never "ad" or "image" alone. The Sponsored label is real text adjacent to the link, available to assistive technology.
- Slot links are keyboard-reachable in the page's logical order, show the site's standard visible focus treatment, and meet the site's target-size practice.
- No creative carries information by color or background image alone (forced-colors survival, per research addition 6): the sponsor's name exists as text in the alternative and, on the sponsors page, as visible text.
- No flashing content (also banned, section 6). Any motion in a future creative format honors `prefers-reduced-motion`; the default still image has no motion.
- The reserved box is present in the accessibility tree in all states, so an unsold slot's house message is announced the same way a creative is.

## 10. Performance budget for slots

- Creative image weight cap: 60 KB per creative file, enforced at intake (section 4.4). A homepage view loads at most one sponsor creative image (H-1 or the visible rotation), lazy-loaded unless it is the day's H-1 creative, which sits below the lead news and still loads with `fetchpriority` left at default so it can never compete with the lead news image.
- Slots add no JavaScript beyond the rotation selection already implied by the site's data pattern, no external requests, and no fonts.
- The build package for any slot must pass the Development Standard gate on every tested page it touches; a slot that costs a category point does not ship.

## 11. The honest sponsor report (defined before anything is sold)

Each sponsor receives one report per month, generated from the analytics tool chosen under WS3 (the numbers below exist only once that choice is made; before then, no report and no measurement of any kind is promised to anyone). The report contains exactly:

1. The sponsor's profile page pageviews for the month, as reported by the named analytics tool, with the tool named in the report.
2. The sponsors section page pageviews for the month, same source.
3. Where the chosen tool supports click events and they are enabled: the count of taps on the sponsor's slot creative and on the sponsor's profile contact actions, labeled as taps, not calls or customers.
4. The Facebook-side numbers for the sponsor's posts that month, as shown in the Page's own insights (reach and link clicks as Meta reports them), labeled as Meta's numbers.
5. Total site pageviews for the month, for context, same analytics source.
6. A standing plain-language note, printed in every report: these are counts of pages viewed and taps recorded by the named tools. They are not counts of phone calls completed, visits to the business, or sales, which this website cannot measure, and no such numbers have been promised.

What the report never contains: unique-visitor claims the cookieless tool cannot support, per-person tracking of any kind, estimates presented as measurements, or comparisons against other sponsors' numbers.

## 12. Decision state

This design is complete as a document. What it waits on, in order: (1) the WS3 analytics decision, which determines whether section 11's item 3 exists; (2) Charles's approval of the offer wording, into which section 7's proposed tier entitlements must be folded before any business hears of them; (3) a staged build package under the overhaul program's normal rules. Nothing is offered or sold before all three.
