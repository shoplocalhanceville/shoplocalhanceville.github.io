# Hanceville Entertainment & Shopping landing page

Live: https://charliegamedevelop.github.io/hanceville-entertainment-shopping/

## Updating events
Events live in `events.json`. The page loads it fresh on every visit and hides any event once its end date (or start date, if there is no end) has passed, using America/Chicago time. Events are sorted by start date automatically.

Each event is an object with these fields:
- `name`, `start` (YYYY-MM-DD), `time`, `town`, `host`, `summary`, `url` (required)
- `end` (YYYY-MM-DD, optional, for multi day events)
- `venue`, `cost` (optional; leave out `cost` when it is not listed)

Edit `events.json`, commit and push. GitHub Pages updates within a minute or two. Keep copy friendly, factual and free of dashes.
