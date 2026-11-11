#!/usr/bin/env python3
"""emit_feed.py - RSS 2.0 + Atom feed emitter (stdlib only).

Reads the site's news.json story records (the same records the generator
uses to build story-<id>.html pages) and emits feed files derived from
those records and nothing else. Never hand-maintained: re-running the
generator pass re-emits the feed.

Dates in news.json are bare YYYY-MM-DD calendar dates with no time of
day. They are rendered as midnight local time in America/Chicago with
the correct DST offset for that date (-05:00 CDT / -06:00 CST), computed
with zoneinfo. No time of day is invented beyond that stated midnight
convention; see FEED_DESIGN.md.

Usage:
    python3 tools/emit_feed.py news.json [--out DIR] [--rss] [--atom]

Called by tools/build_places.py at the end of every generator pass so
the feeds are always emitted from the same records as the pages.

Defaults: emit both feed.xml (RSS 2.0) and atom.xml (Atom 1.0) into the
current directory.
"""

import argparse
import json
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, time, timezone
from email.utils import format_datetime
from pathlib import Path
from zoneinfo import ZoneInfo

BASE_URL = "https://shoplocalhanceville.github.io/"
SITE_TITLE = "Hanceville Entertainment and Shopping - Local News"
SITE_DESCRIPTION = (
    "Hanceville, AL news from city hall, local schools, sports, public "
    "safety and weather in Cullman County. Every story is dated and "
    "links to its sources."
)
LANGUAGE = "en-us"
LOCAL_TZ = ZoneInfo("America/Chicago")


def story_url(record):
    return f"{BASE_URL}story-{record['id']}.html"


def local_midnight(date_str):
    """YYYY-MM-DD -> aware datetime at 00:00 America/Chicago that date."""
    d = datetime.strptime(date_str, "%Y-%m-%d").date()
    return datetime.combine(d, time(0, 0), tzinfo=LOCAL_TZ)


def sorted_records(records):
    """Newest first; id as a stable tiebreak for same-date stories."""
    return sorted(records, key=lambda r: (r["date"], r["id"]), reverse=True)


def build_rss(records):
    rss = ET.Element("rss", {"version": "2.0",
                             "xmlns:atom": "http://www.w3.org/2005/Atom"})
    channel = ET.SubElement(rss, "channel")
    ET.SubElement(channel, "title").text = SITE_TITLE
    ET.SubElement(channel, "link").text = BASE_URL + "news.html"
    ET.SubElement(channel, "description").text = SITE_DESCRIPTION
    ET.SubElement(channel, "language").text = LANGUAGE
    if records:
        latest = local_midnight(sorted_records(records)[0]["date"])
        ET.SubElement(channel, "lastBuildDate").text = format_datetime(latest)
    self_link = ET.SubElement(channel, "atom:link")
    self_link.set("href", BASE_URL + "feed.xml")
    self_link.set("rel", "self")
    self_link.set("type", "application/rss+xml")

    for r in sorted_records(records):
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = r["headline"]
        ET.SubElement(item, "link").text = story_url(r)
        guid = ET.SubElement(item, "guid", {"isPermaLink": "true"})
        guid.text = story_url(r)
        ET.SubElement(item, "pubDate").text = format_datetime(local_midnight(r["date"]))
        ET.SubElement(item, "category").text = r["category"]
        ET.SubElement(item, "description").text = r["summary"]
    return rss


def build_atom(records):
    ns = "http://www.w3.org/2005/Atom"
    ET.register_namespace("", ns)
    feed = ET.Element(f"{{{ns}}}feed")
    ET.SubElement(feed, f"{{{ns}}}title").text = SITE_TITLE
    ET.SubElement(feed, f"{{{ns}}}id").text = BASE_URL + "atom.xml"
    alt = ET.SubElement(feed, f"{{{ns}}}link")
    alt.set("rel", "alternate")
    alt.set("href", BASE_URL + "news.html")
    self_link = ET.SubElement(feed, f"{{{ns}}}link")
    self_link.set("rel", "self")
    self_link.set("href", BASE_URL + "atom.xml")
    if records:
        latest = local_midnight(sorted_records(records)[0]["date"])
        ET.SubElement(feed, f"{{{ns}}}updated").text = latest.isoformat()
    ET.SubElement(feed, f"{{{ns}}}subtitle").text = SITE_DESCRIPTION

    for r in sorted_records(records):
        entry = ET.SubElement(feed, f"{{{ns}}}entry")
        ET.SubElement(entry, f"{{{ns}}}title").text = r["headline"]
        ET.SubElement(entry, f"{{{ns}}}id").text = story_url(r)
        link = ET.SubElement(entry, f"{{{ns}}}link")
        link.set("href", story_url(r))
        stamp = local_midnight(r["date"]).isoformat()
        ET.SubElement(entry, f"{{{ns}}}published").text = stamp
        ET.SubElement(entry, f"{{{ns}}}updated").text = stamp
        ET.SubElement(entry, f"{{{ns}}}summary").text = r["summary"]
        cat = ET.SubElement(entry, f"{{{ns}}}category")
        cat.set("term", r["category"])
    return feed


def write_xml(root, path, root_name):
    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ")
    tree.write(path, encoding="utf-8", xml_declaration=True)
    print(f"wrote {path} ({root_name}, {path.stat().st_size} bytes)")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("news_json", help="path to news.json")
    ap.add_argument("--out", default=".", help="output directory (default: .)")
    ap.add_argument("--rss", action="store_true", help="emit RSS only")
    ap.add_argument("--atom", action="store_true", help="emit Atom only")
    args = ap.parse_args(argv)

    records = json.loads(Path(args.news_json).read_text(encoding="utf-8"))
    if not isinstance(records, list):
        print("news.json must be a JSON list of story records", file=sys.stderr)
        return 1
    for r in records:
        for field in ("id", "date", "headline", "summary", "category"):
            if not r.get(field):
                print(f"record missing required field {field!r}: {r.get('id')!r}",
                      file=sys.stderr)
                return 1

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    emit_rss = args.rss or not args.atom
    emit_atom = args.atom or not args.rss
    if emit_rss:
        write_xml(build_rss(records), out / "feed.xml", "rss")
    if emit_atom:
        write_xml(build_atom(records), out / "atom.xml", "atom")
    print(f"records read: {len(records)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
