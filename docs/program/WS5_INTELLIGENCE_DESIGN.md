# Workstream 5 — On-Site Intelligence Design (raw code, no server)

**Date:** 2026-11-03 · **Lane:** Design (documents and measurement only; nothing built into the site, nothing publishes) · **Governed by:** OVERHAUL_PROGRAM_2026-11-03.md WS5 and folded research items 4 and 5; gap brief area G. **Standard:** raw hand-written code, no framework, no third-party script on initial load; any feature that drops a gate score does not ship.

**Data facts this design rests on (measured 2026-11-03 against the live-copy data.js, 592,499 bytes):** 724 records; every record has `name`, `category`, and a curated `aka` token string; `description` and `descEs` on 707; `logo` 516; `website` 467; `phone` 215; `facebook` 174; `address` 171; text `hours` 25; structured `hs` hours 24. There is no `town` field in the data; town is derivable (see §1). The `aka` field already carries Spanish search terms (for example `cafeteria`, `almuerzo`, `iglesia`, `peluqueria`) and town tokens — Spanish search parity is largely a data property the directory already owns, verified by the test queries in §1.

---

## 1. Typo-tolerant search

### Algorithm (staged matching, cheapest first, all over a prebuilt token index)

1. **Normalize** query and data the same way: lowercase, strip diacritics (so `peluquería` and `peluqueria` are the same token), split on non-alphanumerics.
2. **Exact token match** against the inverted index (token → record ids), with field boosts: a token found in `name` scores highest, then `category`, then `aka`, then derived town. (The scratch scorer used flat weights; the field-boost ordering is a specified refinement, because scratch tests showed flat weights let `aka`-only matches crowd out name matches.)
3. **Prefix match** on tokens of length ≥ 3 (covers "restau…" while typing, and plural/singular stems).
4. **Fuzzy match, only for query tokens that produced no exact or prefix hit** — bounded Levenshtein with early exit: edit distance ≤ 1 for tokens of length 4–6, ≤ 2 for length 7+. A fuzzy hit on a town token (for example `hancevile`) is treated as a town constraint, not a name hint.
5. **Combine** multi-token queries by summing per-token scores; a record must match at least one content token, and town tokens filter rather than rank when a town is recognized.
6. **Render results in chunks** of at most 20 cards per task, yielding between chunks (`scheduler.yield()` where supported, `setTimeout` fallback) — folded research item 2's INP rule: no handler task over about 50 ms. The lookup itself is far under that bound (measured below); the chunking is for the rendering of large result sets, which is where a 724-record directory can actually jank.

### Where the work runs

**Main thread; no Web Worker.** The gap brief (area G) already verdicted Workers unnecessary at this scale, and the measurements confirm it: a full fuzzy scan of the entire 2,277-token vocabulary takes 3.9 ms, and the worst measured end-to-end query took 5.15 ms (both Node on this VM, desktop-class CPU; a modest phone will be slower, still far under the 50 ms task bound for lookup). The index is **prebuilt by the generator and shipped as a static file**, so there is no index-build cost in the visitor's browser at all; the build timing below is a build-machine figure, reported for the record.

### Synonyms and local terms

Three sources, in priority order, all curated data — no runtime guessing:

- **The `aka` field is the primary synonym table.** It already maps local and Spanish vocabulary onto records (a coffee search already finds `cafeteria` records; `iglesia` already returns churches). WS5 does not replace it; the generator keeps it as the single source.
- **A small generator-side alias table** for terms that belong to no single record: town nicknames and area names (Smith Lake, Crane Hill), school names and short forms (Wallace State / WSCC), agency short forms (DHR, SNAP), and common service words mapped to category tokens (haircut → barber/salon tokens; tow truck → towing). Each alias is one line, reviewed like any other listing fact.
- **A measured misspelling watch:** the fixed edit-distance bounds above absorb ordinary typos without a misspelling dictionary. Scratch tests of real misspellings: `barbr` → barber records; `cofee` → 7 Brew Coffee, Berkeley Bob's Coffee House, HanceVegas Coffee Shop, Karma's Coffee House; `hancevile` → Hanceville listings via the town rule; `resturant` → restaurant records including the Restaurants, Food & Drink directory page. A hand-kept misspelling list is added only if the six-hour watch or visitor feedback shows a recurring miss.

### Measured byte budget (scratch build: ~/workspace/overhaul_ws5_scratch/build_index.js, real data.js)

| Item | Measured |
|---|---|
| Distinct index tokens (name + category + aka + derived town) | 2,277 |
| Token index serialized (JSON, token → record ids) | 79,190 bytes |
| Token index, gzip-9 | 22,689 bytes |
| Index build time, generator side (Node, this VM; median of 20 runs) | 13.96 ms (min 10.76, max 26.57) |
| Records with a derivable town (address parse → name parenthetical → aka token) | 482 of 724 |
| Lazy search payload option: per-record subset (name, category, town, aka, phone, address) | 132,528 bytes raw / 32,080 bytes gzip-9 — against 592,499 bytes for the full data.js |
| Worst measured query latency (fuzzy included) | 5.15 ms; full-vocabulary fuzzy scan 3.9 ms |

Two payload shapes are acceptable under the gate; the release chooses one and records the measured cost in the release ledger, per gap brief area G: (a) ship the token index (≈22.7 KB gzip) and resolve hits against the already-loaded listings data; or (b) ship the search subset (≈32.1 KB gzip) as the lazy search file. Option (a) is smaller and reuses data the page already has; it is the recommended default.

---

## 2. Recommendation rails — deterministic rules, no tracking

Rails are computed from fields already on the record being viewed. No cookies, no behavioral data, no visitor history; the same listing always produces the same rail, and each rail can be explained in one sentence shown or statable with it.

1. **Same service, same town.** Records sharing the viewed record's category and derived town. *"More barbers in Hanceville."* Example: on Cut N Up Barber and Style (Barbers & Salons, Hanceville) this yields Hanceville Barber and Style Shop, 112 Commercial St NE.
2. **Same service, nearby towns.** If rule 1 returns fewer than three, fill from the same category in other towns, Cullman County first. *"Other barbers in Cullman County."* Example: The Warehouse Barber joins the rail above.
3. **Same town, related errands.** Records in the viewed record's town whose categories the generator's static pairing table links (for example Barbers & Salons ↔ Downtown Shops; Food ↔ Drinks & Coffee), capped at four. *"While you are in Hanceville."* The pairing table is a curated static list in the generator, reviewed like any other fact — it is not learned from visitors.
4. **Official and emergency neighbors** (profile pages for government and help listings only): same-category records from City Hall & Government, Public Safety, and Help & Resources. *"Related offices and help."*

Determinism is a verification feature: the validation lane can regenerate any rail and compare it byte for byte, and a wrong recommendation is a data bug with a named source, never a model opinion.

---

## 3. The directory assistant — verified answers only, on native dialog

**Shell.** A `<dialog>` opened with `showModal()`, per folded research item 4: the browser supplies focus trapping, Escape to close, and focus restoration to the Ask button on close, in raw code with no library. This also closes the manual WCAG pass's one unassessed item, the overlay's focus management, for the assistant; the same pattern is specified for the profile overlay when WS1 reaches it.

**Answer discipline (the whole point of the feature).**
- The assistant may state only values present in the record's own verified fields: `name`, `category`, `address`, `phone`, `website`, `facebook`, and `hours`/`hs` **only when that record carries them**. It never paraphrases the description into new claims, never merges facts across records, and never computes facts it was not given (no "open now" unless the record has structured `hs` hours to compute from).
- Every answer names and links the listing it came from, rendered as that listing's normal card under the answer text, so the visitor sees the source, not just the claim.
- Question handling is intent matching over the same token index as §1 (phone? address? hours? where/what is…?), not free generation. An intent with no matching record, or a fact the matched record does not carry, gets the fixed refusal, word for word:
  > "I don't have that in the verified listings. Try the search above, or browse the Community Guide — every listing there shows exactly what we have confirmed."
- Spanish mode uses the fixed Spanish equivalent of the refusal and answers from `descEs`-carrying records (§6).

**Examples, drawn from real records (fields verified 2026-11-03):**
- *"Where can I get a haircut in Hanceville?"* → Cut N Up Barber and Style, 105 Commercial St SE, Hanceville, (256) 636-2018; and Hanceville Barber and Style Shop, 112 Commercial St NE, (256) 352-7271. Both cards shown.
- *"What is the phone number for Cut N Up?"* → (256) 636-2018, from the record's `phone` field, with its card.
- *"Is 7 Brew open late?"* → Yes, per its verified `hours` field: Sunday to Thursday 5:30 AM to 10 PM; Friday and Saturday 5:30 AM to 11 PM. 7 Brew Coffee, 1715 Cherokee Ave SW, Cullman. (This record carries `hours` and `hs`; the answer is allowed.)
- *"Is Cut N Up open on Sunday?"* → The fixed refusal's fact form: Cut N Up's record carries no verified hours field (its hours exist only inside its prose description), so the assistant says it does not have confirmed hours for that listing and shows the card with the phone number to call. The assistant does not lift hours out of description prose — prose is for readers, fields are for answers.
- *"Can I get a tire changed in Hanceville at 2 in the morning?"* → College Tire, 315 Main St NW, Hanceville, (256) 352-2221, and Tire Barn Plus, 102 Main St NE, (256) 962-5540, are the tire listings; neither record carries verified hours, so the assistant states plainly that it cannot confirm any 2 AM service and offers the phone numbers. No invented answer.
- *"I need help right now."* → The Crisis & Emergency records lead: 988 Suicide and Crisis Lifeline (phone 988) and Emergency: Call 911, shown first and unranked by score — crisis intents bypass ordinary ranking entirely.

---

## 4. Voice input — a labeled option, never the only path

- **Feature detection only:** the mic button renders solely when `window.SpeechRecognition || window.webkitSpeechRecognition` exists. No detection, no button, no dead control.
- **The label states the limits, next to the button, in plain words:** "Voice search uses your browser's speech service. It is not available in Firefox, and in Chrome your voice is sent to Google to be recognized. Typing always works." Spanish mode carries the same sentence in Spanish, and recognition language follows the site mode (`en-US` / `es-US`).
- Typing is the primary path in layout, tab order, and documentation; voice fills the same search box and the same assistant input, so a recognition error is visible and correctable before anything runs — recognition output is never submitted silently.
- Per folded research item 5, the underlying API is a W3C Community Group report, not a finished standard; the feature is specified as removable in one commit if browser support changes, and its presence or absence never affects the gate (it ships inside the lazily loaded intelligence file, §5).

---

## 5. Lazy-load architecture and gate protection

**Zero cost to first paint is a hard rule, not a goal.** Nothing in this workstream — not the index, not the search code, not the assistant, not the voice code — is referenced by the initial HTML, CSS, or the listings data load of any page. Each feature loads on its own explicit trigger:

| Feature | Trigger (the first moment any of its bytes are requested) |
|---|---|
| Typo-tolerant search | First focus of, or first keystroke in, the search box |
| Recommendation rails | The profile overlay or profile page section is opened for a specific listing (rails computed from data already on the page; no extra fetch) |
| Directory assistant | The visitor activates the "Ask the directory" button (dialog markup and code load then; the button itself is plain HTML) |
| Voice input | Loaded with the search/assistant code it serves; the button appears only after feature detection passes |

**Gate-protection test plan (applies to every WS5 release, no exceptions):**
1. The gate runs on the release branch exactly as Standard v1.1 specifies (five-run medians, all four categories at 100 as errors, budgets as errors). A WS5 package merges only on a full pass, with the Lighthouse version recorded in the ledger (folded item 1).
2. A **cold-load control measurement** accompanies each WS5 package: the tested pages are measured with the intelligence features present but never triggered, and the report shows zero added requests and zero added bytes on initial load against the pre-WS5 baseline. Any nonzero figure is a defect, not a discussion.
3. An **interaction measurement** accompanies each package: with throttling on, a search keystroke and an assistant open are exercised, and the report shows no handler task over about 50 ms and results rendering chunked per §1.
4. If a feature cannot pass all three, it does not ship; the program's standing rule already says so, and this workstream names no exceptions for itself.

---

## 6. Spanish parity — every feature, no exceptions

- **Search:** normalization strips diacritics in both directions, and the `aka` field's Spanish terms are already in the index — measured tonight: `iglesia` returns the church listings and `peluqueria` returns the barber and salon listings with the data exactly as it stands. Spanish service words in the alias table (§1) get Spanish entries in the same review pass, never as an afterthought release.
- **Rails:** rail headings and the one-sentence explanations render from the existing UI string mechanism in both languages ("More barbers in Hanceville" / its Spanish equivalent), and the records shown are the same records — parity of content, not a reduced Spanish rail.
- **Assistant:** in Spanish mode the assistant answers in Spanish from the same fields, shows the same cards, and uses the fixed Spanish refusal: "No tengo ese dato en los listados verificados. Pruebe la búsqueda o explore la Guía de la Comunidad; cada listado muestra exactamente lo que hemos confirmado." Hours and phone answers are field values and identical in both languages.
- **Voice:** recognition language follows site mode (`es-US` in Spanish mode), and the limits label is displayed in Spanish (§4).
- **Descriptions:** where a record lacks `descEs` (17 records tonight), the assistant and rails behave identically in both modes — the card shows what exists and nothing is machine-translated or invented to fill the gap, matching the site's standing facts-only rule.
