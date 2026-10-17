# Hanceville Entertainment & Shopping landing page

Live: https://charliegamedevelop.github.io/hanceville-entertainment-shopping/

## Updating events
Events live in `events.json`. The page loads it fresh on every visit and hides any event once its end date (or start date, if there is no end) has passed, using America/Chicago time. Events are sorted by start date automatically.

Each event is an object with these fields:
- `name`, `start` (YYYY-MM-DD), `time`, `town`, `host`, `summary`, `url` (required)
- `end` (YYYY-MM-DD, optional, for multi day events)
- `venue`, `cost` (optional; leave out `cost` when it is not listed)

Edit `events.json`, commit and push. GitHub Pages updates within a minute or two. Keep copy friendly, factual and free of dashes.

## Updating the Community Directory
Entries live in `directory.json`. Fields: `group` (one of: Schools, City Hall & Government, Public Safety, Utilities & Public Works, Community Services), `name`, `summary` (required), plus optional `address`, `phone`, `website`. Leave out any field you cannot verify. Sources are tracked in `/workspace/hanceville/landing/directory-sources.md`.

## Updating the Business Directory
Entries live in `businesses.json`. Fields: `category` (must match the businesses list in `app.js`: Restaurants, Drinks & Coffee, Barbers & Salons, Auto Sales, Auto Repair & Mechanics, Tires, Small Engine Repair, Towing, Home Services, Health & Pharmacy, Pets & Child Care, Finance & Insurance, Shopping & Retail, Manufacturing & Industry, Lodging, Other), `service`, `tags` (keywords for search), `name`, `type`, `address`, `summary` (required), plus optional `phone`, `website`, `facebook`. The list sorts alphabetically, and the search box and category chips work automatically. Sources are tracked in `/workspace/hanceville/landing/business-sources.md`.

## Updating Wallace State Services and Community Resources
`wallace.json` and `resources.json` use the same fields: `group`, `name`, `summary`, `phone` (required), plus optional `email`, `address`, `website`. Group names must match the list in the page script (Wallace: Getting Started, Paying for College, Help in the Classroom, Careers and Training, Health, Safety and Support, Campus Life. Resources: Crisis & Emergency, Everyone, Women, Men, Children & Families, Seniors, Veterans). Sources: `wallace-sources.md` and `resources-sources.md` in `/workspace/hanceville/landing/`.

## v2 structure
- `index.html` home with category cards; one page per category: `events.html`, `businesses.html`, `directory.html`, `resources.html`, `wallace.html`.
- Shared `style.css` and `app.js`. Page lists, the site wide search bar and the quick access tab bar are all built by `app.js` from the JSON files.
- Group names for each page are set in the `PAGES` list at the top of `app.js`. Add a new group there if you add one to a JSON file.
- Every card gets an anchor from its name (for example `businesses.html#reyes_pizza`), and every group gets one too (for example `directory.html#public_safety`).
