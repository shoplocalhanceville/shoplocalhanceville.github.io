# Handoff CSV Master — Specification

Directed by Charles Adams, 2026-11-04: when the current website push is completely finished, Muse delivers a CSV master file for any and all of the website, so that any and all developments can be transferred to a different bot that can keep building. Charles's word for the file as given: "CSV master valve." Refined by Charles the same morning: the file is the one he submits to the **Grok Bot**, and it is built for that handoff specifically. This specification records what the deliverable is, so its assembly at completion is mechanical.

## Form

- One consolidated CSV file, delivered to Charles in `~/workspace/your_files/`, produced at complete finish of the push, never earlier and never from stale state.
- Highly organized: one row per tracked item, grouped by area in a fixed order, with columns: area, item, type, status, source_of_truth, live_location, rule_or_standard, implementation_prompt, next_action, owner, notes.
- The consolidated file is delivered together with the complete set of the program's existing master CSVs (listings_master, files_registry, releases_log, decisions_holds, troubleshooting_cases, error_codes, features_registry, roles_responsibilities, workstreams), because those CSVs are the living sources of truth. On any disagreement, the underlying master CSV wins, per the standing rule.
- Every row is verified against the live site and the masters at the moment of assembly. Nothing in the file is guessed, and any gap is stated as a gap in the notes column.

## The prompts layer (Charles, 2026-11-04)

The file carries detailed prompts inside it, in the implementation_prompt column and in a dedicated prompts section of rows, so the Grok Bot can work from the file alone. The prompts cover:

1. How to implement each area of the website, step by step, in the site's own established patterns.
2. How to identify implementation replacements: how to tell what needs replacing, what evidence settles it, and how to stage a replacement without breaking what works.
3. Raw coding rules for any new code: plain hand-written HTML, CSS, and JavaScript only, no frameworks, no build pipeline, plus the verification setups for new raw code (fresh-fetch base checks, byte proofs, render-and-exercise verification at phone, tablet, and desktop widths, and the rule that a release is verified by rendering the page, never by file comparison alone).
4. Full compliance requirements: the Charles Development Standard, the Quality and Rights Standard, the facts-only rule (a fact with no source is researched or held, never invented), the real-logo rule, the never-link domain list, the suspended-email rule, and the newsroom sourcing practice for news content.
5. The Lighthouse standard: the target is 100 out of 100 in all four categories, with the CI gate configuration carried in the file (five-run medians, all four categories asserted at 100 as merge-blocking errors, the metric and page-weight budgets, CI and local versions recorded separately), and measured scores always recorded as measured.

## Authority Charles grants the Grok Bot over the file (his words, 2026-11-04)

- The Grok Bot can change, organize, extract, replace, take out, build, and develop any and all of the CSV master file.
- The Grok Bot will research the entire CSV file for any new add-ons that need to be added, anything that needs to be developed, fixed, recoded, refilled, or reorganized, and anything Charles may have left out.
- The Grok Bot can adjust any part of the CSV file to ensure any professional standard score, including the Lighthouse 100 out of 100 score.

Boundary kept from the standing rules and stated inside the file for the receiving bot: authority over the CSV file is not authority to publish to the live website. Publishing follows Charles's approval rule (he is the only approver), and any scoped waiver in force at handoff is recorded as expired or scoped, never as a standing permission. Charles can change that with the Grok Bot directly; the file records the rule as it stands.

## Team structure and coordination (Charles, 2026-11-04)

- **Team structure, described in detail inside the file.** The CSV master carries a full description of how the Big Dog team build is structured, drawn from the governing records (BIG_DOG_EXPANDED_STRUCTURE_2026-11-03.md and TEAM_CHARTER_2026-11-03.md in the program masters): the nine Big Dog cells (Lead and Integrator; Research and Development; Prevention and Freshness; Sourcing and Verification; Raw Code Core; Design Integration; Media Pipeline; Integration and Automation; Records), what each cell owns, validation independent of the builders, the brief queue and named-package discipline, the masters and registries as sources of truth, and the master guide's handoff protocol. A receiving bot implements inside that structure; it does not invent a parallel one.
- **Big Dog stays in the loop.** Any bot working from the file communicates with Big Dog about any new updates to the CSV file and about any developments or changes, so Big Dog stays in the loop while building. Work is claimed before it is started, changes are reported as they land, and the masters are updated in the same pass as the work they record. The purpose, in Charles's words, is that there are no overlapping and conflicting issues with any bot the file is submitted to.
- The file states plainly which channel that communication takes ( Charles hands files to bots himself; the receiving bot's updates come back through Charles or the channel he names), and records that until a bot's update reaches Big Dog, the masters Big Dog holds remain the source of truth.

## Coverage checklist (any and all of the website)

1. Site identity: name, live URL, repository, publish route (signed-in browser, branch, pull request, merge once, verify by rendering), and the master HTML naming rule.
2. Listings state: the final live count, the listings master as source of truth, the logo rule, the Facebook link rules, the never-link domain list, and the suspended-email rule.
3. Releases: every pull request through the final one, from releases_log.
4. Brief queue: the final state of every brief, BD-001 onward, completed, held, or open, with its evidence location.
5. Workstreams: the final state of overhaul workstreams 1 through 5, each with its design document and its report.
6. Standards in force: the Charles Development Standard (current version), the Lighthouse CI gate configuration and its honest measured state, the raw coding rule, the facts-only rule, the Quality and Rights Standard, and the approval rule with the waiver status as it stands at handoff.
7. Decisions and holds: everything decided, everything still held for Charles, and every owner-only step still open, each named.
8. Watch items: the flapping sites, the Senior Services root link, and any other standing watch, with the decision each one stands under.
9. Scores: the score ledger's final measured state, CI and local runs recorded separately, never mixed.
10. Operations: the six-hour check, the status report schedule, the emergency playbook and troubleshooting guide locations, and the error code register.
11. Known gaps, stated honestly: any measured score below standard, any unreconciled item, and anything a receiving bot must not treat as done.
12. Team structure: the detailed description of the Big Dog team build (cells, ownership, validation independence, package discipline, sources of truth, handoff protocol), per the Team structure and coordination section above.
13. Coordination: the communication rule that any bot reports CSV updates, developments, and changes to Big Dog, the channel it uses, and the claim-before-starting rule that prevents overlap and conflicts.

## Build rule

The file is assembled from the masters and a fresh live verification pass in the same sitting. Its delivery is the closing act of the push, reported to Charles with the final completion report.
