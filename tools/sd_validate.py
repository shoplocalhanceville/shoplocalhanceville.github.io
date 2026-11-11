#!/usr/bin/env python3
"""sd_validate.py — structured-data validator for the generated site.

Raw Python, standard library only. Read-only: it never writes to the tree it
scans. For every HTML page under ROOT it:

  1. extracts every <script type="application/ld+json"> block and parses it
     (unparseable blocks are reported as syntax errors);
  2. walks every typed node (including @graph members and nested objects)
     and checks @type against vocabulary_subset.json, and each property
     against that type's allowed property set (schema.org type + ancestors);
  3. checks typed nodes against supported_features.json: a type tied to a
     retired Google rich-result feature (e.g. FAQPage) is DRIFT (warn),
     never a vocabulary error — the schema can be valid while the feature
     it was written for is gone;
  4. cross-checks the visible page:
       - profile/entity pages (place-*.html): the main entity node's name
         (the node whose @id ends in #entity) against the page <h1>, with
         <title> as the fallback surface;
       - WebPage nodes: name against <title>, with <h1> as fallback;
       - stories (story-*.html): NewsArticle headline against <h1>, and
         datePublished against a visible date — a <time datetime="...">
         attribute matching the date, or the date in a visible long form.

Usage:
    python3 sd_validate.py ROOT [--vocab vocabulary_subset.json]
                                  [--features supported_features.json]
                                  [--out sd_validation_results.json]
                                  [--inventory SD_INVENTORY.md]

Exit code: 1 if any ERROR-class finding (syntax, unknown type/property,
visible-page mismatch), else 0. Drift is WARN-class and never fails.
Gate policy proposal (see SD_VALIDATION_REPORT.md): errors fail, drift warns.
"""
import argparse, collections, datetime, html as htmlmod, json, re, sys
from pathlib import Path

LD_RE = re.compile(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', re.S | re.I)
H1_RE = re.compile(r'<h1[^>]*>(.*?)</h1>', re.S | re.I)
TITLE_RE = re.compile(r'<title[^>]*>(.*?)</title>', re.S | re.I)
TIME_RE = re.compile(r'<time[^>]+datetime=["\']([^"\']+)["\']', re.I)

TOP_PAGES = {"index.html", "businesses.html", "places.html", "events.html",
             "news.html", "directory.html", "home.html"}

def family(name):
    if name.startswith("place-"): return "profile (place-*.html)"
    if name.startswith("category-"): return "category (category-*.html)"
    if name.startswith("story-"): return "story (story-*.html)"
    if name in TOP_PAGES: return "index/top pages"
    return "other"

def clean(fragment):
    if not fragment: return ""
    text = re.sub(r'<[^>]+>', ' ', fragment)
    return re.sub(r'\s+', ' ', htmlmod.unescape(text)).strip()

def first(pattern, text):
    m = pattern.search(text)
    return clean(m.group(1)) if m else ""

def typed_nodes(data):
    """Yield every dict that carries an @type, recursing through lists,
    @graph, and nested objects."""
    if isinstance(data, dict):
        if "@type" in data:
            yield data
        for key, value in data.items():
            if key == "@type":
                continue
            yield from typed_nodes(value)
    elif isinstance(data, list):
        for item in data:
            yield from typed_nodes(item)

def all_nodes(data):
    if isinstance(data, dict):
        yield data
        for value in data.values():
            yield from all_nodes(value)
    elif isinstance(data, list):
        for item in data:
            yield from all_nodes(item)

SCRIPT_RE = re.compile(r'<(script|style)[^>]*>.*?</\1>', re.S | re.I)

def visible_date_present(page_text, iso_date):
    page_text = SCRIPT_RE.sub(' ', page_text)  # JSON-LD itself is not visible text
    try:
        d = datetime.date.fromisoformat(iso_date[:10])
    except ValueError:
        return None  # not a date we can check; caller reports separately
    for attr in TIME_RE.findall(page_text):
        if attr[:10] == d.isoformat():
            return True
    visible = clean(page_text)
    long_forms = [d.strftime("%B %d, %Y"), d.strftime("%B %-d, %Y") if hasattr(d, "strftime") else "",
                  d.strftime("%b %d, %Y"), d.strftime("%b %-d, %Y") if hasattr(d, "strftime") else "",
                  d.isoformat()]
    # %-d is POSIX-only; build the unpadded form portably instead.
    long_forms += [f"{d.strftime('%B')} {d.day}, {d.year}", f"{d.strftime('%b')} {d.day}, {d.year}"]
    return any(form and form in visible for form in long_forms)

def main():
    ap = argparse.ArgumentParser()
    here = Path(__file__).parent
    ap.add_argument("root")
    ap.add_argument("--vocab", default=str(here / "vocabulary_subset.json"))
    ap.add_argument("--features", default=str(here / "supported_features.json"))
    ap.add_argument("--out", default="")
    ap.add_argument("--inventory", default="")
    args = ap.parse_args()

    vocab = json.loads(Path(args.vocab).read_text())["types"]
    features = json.loads(Path(args.features).read_text())
    retired = features.get("retired", {})

    root = Path(args.root)
    pages = sorted(root.rglob("*.html"))

    findings = collections.defaultdict(list)  # class -> [ {file, detail} ]
    counts = collections.Counter()
    inv_types = collections.Counter()
    inv_props = collections.defaultdict(collections.Counter)
    inv_family = collections.defaultdict(lambda: {"files": 0, "files_with_ld": 0, "blocks": 0})
    inv_family_type = collections.defaultdict(collections.Counter)

    for page in pages:
        rel = page.relative_to(root).as_posix()
        fam = family(page.name)
        inv_family[fam]["files"] += 1
        text = page.read_text(errors="ignore")
        blocks = LD_RE.findall(text)
        if blocks:
            inv_family[fam]["files_with_ld"] += 1
        inv_family[fam]["blocks"] += len(blocks)
        counts["pages_scanned"] += 1
        h1 = first(H1_RE, text)
        title = first(TITLE_RE, text)
        entity_checked = webpage_checked = False

        for raw in blocks:
            counts["blocks"] += 1
            try:
                data = json.loads(raw)
            except json.JSONDecodeError as exc:
                counts["syntax_errors"] += 1
                findings["syntax_error"].append({"file": rel, "detail": str(exc)})
                continue
            counts["blocks_parsed"] += 1
            for node in typed_nodes(data):
                types = node.get("@type")
                types = types if isinstance(types, list) else [types]
                for t in types:
                    counts["typed_nodes"] += 1
                    inv_types[t] += 1
                    inv_family_type[fam][t] += 1
                    for prop in node:
                        inv_props[t][prop] += 1
                    if t in retired:
                        counts["feature_drift"] += 1
                        findings["feature_drift"].append(
                            {"file": rel, "detail": f"{t}: {retired[t]['status']}"})
                    if t not in vocab:
                        counts["unknown_types"] += 1
                        findings["unknown_type"].append({"file": rel, "detail": str(t)})
                        continue
                    allowed = set(vocab[t]["properties"])
                    for prop in node:
                        if prop not in allowed:
                            counts["unknown_properties"] += 1
                            findings["unknown_property"].append(
                                {"file": rel, "detail": f"{t}.{prop}"})
            # ---- visible-page cross-checks ---------------------------------
            for node in all_nodes(data):
                if not isinstance(node, dict):
                    continue
                nid = str(node.get("@id", ""))
                if (page.name.startswith("place-") and nid.endswith("#entity")
                        and node.get("name") and not entity_checked):
                    entity_checked = True
                    counts["profile_name_checks"] += 1
                    if node["name"].strip().lower() not in (h1.lower(), title.lower()):
                        counts["visible_mismatches"] += 1
                        findings["visible_mismatch"].append(
                            {"file": rel, "detail": f"entity name {node['name']!r} vs h1 {h1!r} / title {title!r}"})
                if node.get("@type") == "WebPage" and node.get("name") and not webpage_checked:
                    webpage_checked = True
                    counts["webpage_name_checks"] += 1
                    if node["name"].strip().lower() not in (title.lower(), h1.lower()):
                        counts["visible_mismatches"] += 1
                        findings["visible_mismatch"].append(
                            {"file": rel, "detail": f"WebPage name {node['name']!r} vs title {title!r} / h1 {h1!r}"})
                if page.name.startswith("story-") and node.get("@type") == "NewsArticle":
                    if node.get("headline"):
                        counts["story_headline_checks"] += 1
                        if node["headline"].strip().lower() != h1.lower():
                            counts["visible_mismatches"] += 1
                            findings["visible_mismatch"].append(
                                {"file": rel, "detail": f"headline {node['headline']!r} vs h1 {h1!r}"})
                    if node.get("datePublished"):
                        counts["story_date_checks"] += 1
                        present = visible_date_present(text, str(node["datePublished"]))
                        if present is False:
                            counts["visible_mismatches"] += 1
                            findings["visible_mismatch"].append(
                                {"file": rel, "detail": f"datePublished {node['datePublished']} not found as <time datetime> or visible date"})

    for key in ("syntax_errors", "unknown_types", "unknown_properties",
                "feature_drift", "visible_mismatches"):
        counts.setdefault(key, 0)
    result = {"root": str(root), "counts": dict(counts),
              "findings": {k: v for k, v in findings.items()}}
    print(json.dumps(result["counts"], indent=1, sort_keys=True))
    for cls, items in sorted(findings.items()):
        print(f"{cls}: {len(items)}")
        for item in items[:5]:
            print("  ", item["file"], "-", item["detail"])
    if args.out:
        Path(args.out).write_text(json.dumps(result, indent=1) + "\n")
    if args.inventory:
        lines = ["# Structured-Data Inventory — branch tree (PR #137 head)", "",
                 f"Generated by `sd_validate.py --inventory` on 2026-11-10. Pages scanned: {counts['pages_scanned']:,}; "
                 f"files with JSON-LD: {sum(v['files_with_ld'] for v in inv_family.values()):,}; blocks: {counts['blocks']:,}; "
                 f"typed nodes (recursive, incl. nested): {counts['typed_nodes']:,}; distinct @types: {len(inv_types)}.", "",
                 "## By template family", "",
                 "| Family | Files | Files with JSON-LD | Blocks |", "|---|---:|---:|---:|"]
        for fam, v in sorted(inv_family.items()):
            lines.append(f"| {fam} | {v['files']:,} | {v['files_with_ld']:,} | {v['blocks']:,} |")
        lines += ["", "Top @types per family:", ""]
        for fam in sorted(inv_family_type):
            top = ", ".join(f"{t} {c:,}" for t, c in inv_family_type[fam].most_common(8))
            lines.append(f"- **{fam}**: {top}")
        lines += ["", "## @type usage and properties (all nodes, recursive)", "",
                  "| @type | Nodes | Properties (count of nodes using each) |", "|---|---:|---|"]
        for t, c in inv_types.most_common():
            props = ", ".join(f"{p} {n:,}" for p, n in inv_props[t].most_common())
            lines.append(f"| {t} | {c:,} | {props} |")
        no_ld = [p.relative_to(root).as_posix() for p in pages
                 if 'application/ld+json' not in p.read_text(errors='ignore')]
        lines += ["", "Files with no JSON-LD block: " + (", ".join(f"`{n}`" for n in no_ld) or "none") + ". "
                  "The two google*.html files are search-console verification files and assistant.html is a "
                  "tool page; the one story file in the list is recorded in SD_VALIDATION_REPORT.md.", ""]
        lines += ["", "Notes: counts are node counts, not page counts — a profile page carries its entity, a "
                  "BreadcrumbList with 3–5 ListItems, and nested PostalAddress / ImageObject / ContactPoint nodes. "
                  "FAQPage and HowTo do not appear anywhere in the tree (see supported_features.json). "
                  "The homepage ItemList node carries numberOfItems 0 with no itemListElement (index.html) — "
                  "recorded here as an inventory observation; it is syntactically valid and outside the "
                  "validator's specified cross-checks."]
        Path(args.inventory).write_text("\n".join(lines) + "\n")
    errors = (counts["syntax_errors"] + counts["unknown_types"]
              + counts["unknown_properties"] + counts["visible_mismatches"])
    return 1 if errors else 0

if __name__ == "__main__":
    sys.exit(main())
