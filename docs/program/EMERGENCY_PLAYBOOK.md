# Emergency Playbook
## Hanceville Entertainment and Shopping website
One page. Follow it in order. Owner and only approver: Charles Adams. Current as of November 3, 2026.

## The seven steps
1. **Reproduce it by rendering.** Open the live page and exercise it (grid renders, search filters, rails fill, links open). If you cannot render the live site from your machine, render the exact live file locally and say which you did. Never diagnose from file contents alone.
2. **Find the last change.** Check `releases_log.csv` in this folder and the repo's recent merges. Most emergencies are the most recent release. Name the pull request before touching anything.
3. **Decide: fix forward or revert.** Fix forward when the repair is small, understood, and verified (today's homepage repair took one file). Revert when the cause is unclear or the change was large: on GitHub, open the merged pull request and use Revert, merge the revert pull request, and verify the site is whole again. A revert is a normal tool, not a failure.
4. **Stage the fix.** Copy the current live file first. Change only what the diagnosis requires. If a helper, class, or block looks like a duplicate, prove the page still works without it by rendering, or do not remove it (see rule 8 in the master guide).
5. **Verify the staged fix by rendering it.** Zero console errors. Exercise the exact feature that broke. Compare counts before and after (cards, rail items, links). A file that merely matches expectations on disk is not verified.
6. **Publish through the normal route.** Branch from current main, check the base fingerprint first (size and a marker string) and stop if main moved, upload, verify the staged size, one pull request, merge once, wait for the Pages deployment, then verify the live result the same way you reproduced the problem.
7. **Log it the same day.** Add the incident and the fix to `releases_log.csv` and `decisions_holds.csv`, note the cause in one sentence, and update any registry the incident proved wrong. An unlogged emergency will be repeated by the next bot.

## Stop conditions
- The live base moved while you worked: stop, rebase the fix on the new base, verify again.
- The fix needs data you cannot verify (a phone, an address, a date): ship the fix without it; never invent a value to complete a page.
- Two problems at once (a content error inside a code emergency): fix the code first, log the content item, stage it separately.

## Fast contacts and facts
- Site: https://shoplocalhanceville.github.io/ · Repo: github.com/shoplocalhanceville/shoplocalhanceville.github.io (public, main)
- Publishing route: the signed-in browser on GitHub. The GitHub connector cannot write to this repo.
- Last known good homepage copies: `~/workspace/emergency_fix_staging/` (current live version) and `~/workspace/combined_release_package/` (the PR #44 version, which carries the regression described in the troubleshooting guide, do not restore it as a fix).
- The full symptom-by-symptom reference is `TROUBLESHOOTING_GUIDE.md` in this folder; the short code table is `error_codes.csv`.
