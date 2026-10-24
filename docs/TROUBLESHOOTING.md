# Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `audit.py` reports `missing-page` | A listing was added or renamed in a JSON file or in `SLH_LISTINGS` | `python3 tools/build_places.py`, then rerun the audit |
| `broken-link` to `place-...html` | Listing removed or renamed but an old page links to it | Rebuild places. If the link is in hand written HTML, update it |
| `banned-char` em dash or en dash | New copy pasted with dashes | Rewrite the sentence with a comma, period or "to" (for ranges). For homepage data run `python3 tools/clean_listings.py` |
| `banned-char` double space | Copy joined with two spaces | Replace with one space |
| `spelling` | Typo, or a real name or Spanish word | Fix typos. Add real names or Spanish words to `tools/codespell-ignore.txt` (lowercase, one per line) |
| `weight` index.html too large | A script pasted base64 images back in | `python3 tools/optimize_home.py` |
| `empty-section` | Generated section with no data | Check the generator condition in `tools/build_places.py`; sections must be skipped when data is empty |
| `dead-tab` | Section bar link with no matching section | Same as above. Each `sec.append` must match a written `<section id>` |
| Homepage white screen | JS error in an inline script, often from a bad regex replace by a refresh script | Open the page in Chrome with the console, or run `node tools/crawl.js http://localhost:8799/ /tmp/c.json` against `python3 -m http.server 8799`. `git log -p -1 -- index.html` shows the last change |
| Facebook feed does not appear | Page privacy settings, browser blocking third party frames, or the URL is not a Facebook Page | The fallback "Open the Facebook Page" link always works. Check `facebook` in the data is `https://www.facebook.com/...` |
| Old content after a push | Browser or service worker cache | HTML is network first, so a reload fixes it. For CSS or JS, bump `?v=`. To force all clients, bump `V` in `sw.js` |
| `monitor.py` says CSP changed on a place page | Generator CSP edited | The policy must equal `PLACE_CSP` in monitor.py (v14 policy plus `frame-src https://www.facebook.com`) |
| Lighthouse best practices shows no score | Page timed out loading (this happened when index.html was 14 MB) | Check weight first |
| Push rejected | An hourly routine pushed first | `git pull --rebase` then push. Never force push |
