#!/usr/bin/env python3
"""emit_ics.py - all-events iCalendar emitter (stdlib only).

Reads the site's events.json records and emits ONE subscribable
events.ics (RFC 5545) containing every emittable record.

Honesty rules (see EVENTS_DATA_INVENTORY.md for the measured basis):
  * `end` is optional in events.json (present on 9 of 56 records, all
    multi-day). A record with no `end` is treated as a single-day event
    on its `start` date. That is a reading of the record's shape, not an
    invented field: the site itself presents such records on one date.
  * A timed VEVENT is emitted ONLY when the record's `time` is exactly
    one clock range "H:MM AM to H:MM PM" AND the event is single-day.
    Both times are then verbatim from the record; nothing is rounded,
    extended, or given a duration.
  * Every other record (start-time only, annotated times, multi-day
    schedules, prose times, "All day", missing time) is emitted as a
    date-only all-day VEVENT: DTSTART;VALUE=DATE = start,
    DTEND;VALUE=DATE = day after the effective end (RFC 5545 DTEND for
    DATE values is exclusive). The record's verbatim `time` string is
    carried in DESCRIPTION prefixed "Time: " so no recorded information
    is lost and no time is invented.
  * No field is ever guessed: no end times, no durations, no venues.

Format: CRLF line endings everywhere, content lines folded at 75
octets (UTF-8 aware, never splitting a multi-byte character), TEXT
values escaped per RFC 5545 section 3.3.11, an explicit VTIMEZONE for
America/Chicago, a stable UID per event derived from the record's
name + start date (plus its verbatim time string when names repeat on
the same date), and DTSTAMP = run time in UTC (regenerated each pass;
it is a generation timestamp, not event data).

Usage:
    python3 tools/emit_ics.py events.json [--out DIR] [--all]

Production windowing (Expansion execution, 2026-11-11): by default only
events whose effective end (recorded ``end``, else ``start``) is today or
later in America/Chicago are emitted, matching the events page's own rule
that events drop off once they are over. ``--all`` emits every record, as
the Pass 1 prototype did. The filter reads the same records; it edits none.
"""

import argparse
import hashlib
import json
import re
import sys
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path

DOMAIN = "shoplocalhanceville.github.io"
CAL_NAME = "Hanceville Entertainment and Shopping - Community Events"
PRODID = "-//Hanceville Entertainment and Shopping//Events Subscription//EN"

RANGE_RE = re.compile(
    r"^(\d{1,2}):(\d{2})\s*(AM|PM)\s+to\s+(\d{1,2}):(\d{2})\s*(AM|PM)$",
    re.IGNORECASE,
)

VTIMEZONE_LINES = [
    "BEGIN:VTIMEZONE",
    "TZID:America/Chicago",
    "BEGIN:DAYLIGHT",
    "TZOFFSETFROM:-0600",
    "TZOFFSETTO:-0500",
    "TZNAME:CDT",
    "DTSTART:19700308T020000",
    "RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=2SU",
    "END:DAYLIGHT",
    "BEGIN:STANDARD",
    "TZOFFSETFROM:-0500",
    "TZOFFSETTO:-0600",
    "TZNAME:CST",
    "DTSTART:19701101T020000",
    "RRULE:FREQ=YEARLY;BYMONTH=11;BYDAY=1SU",
    "END:STANDARD",
    "END:VTIMEZONE",
]


def parse_date(s):
    return datetime.strptime(s, "%Y-%m-%d").date()


def to_24h(hour, minute, ampm):
    h = int(hour) % 12
    if ampm.upper() == "PM":
        h += 12
    return time(h, int(minute))


def slugify(name):
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return slug or "event"


def escape_text(value):
    """RFC 5545 section 3.3.11 TEXT escaping."""
    return (
        value.replace("\\", "\\\\")
        .replace(";", "\\;")
        .replace(",", "\\,")
        .replace("\r\n", "\\n")
        .replace("\n", "\\n")
    )


def fold_line(line):
    """Fold one logical line into physical lines of at most 75 octets.

    Continuation lines start with a single space, which counts toward
    the 75 octets. Folding never splits a multi-byte UTF-8 character.
    """
    raw = line.encode("utf-8")
    if len(raw) <= 75:
        return [line]
    physical = []
    first = True
    while raw:
        budget = 75 if first else 74  # continuation's leading space
        chunk = raw[:budget]
        # Back off until the cut does not split a UTF-8 sequence.
        while True:
            try:
                text = chunk.decode("utf-8")
                break
            except UnicodeDecodeError:
                chunk = chunk[:-1]
        physical.append(("" if first else " ") + text)
        raw = raw[len(chunk):]
        first = False
    return physical


def make_uid(record, seen):
    base = f"{slugify(record['name'])}-{record['start'].replace('-', '')}"
    uid = base
    if uid in seen:
        # Same name on the same date (e.g. a recurring market): keep the
        # UID stable by disambiguating from verbatim record fields.
        digest = hashlib.sha256(
            json.dumps(record, sort_keys=True).encode("utf-8")
        ).hexdigest()[:8]
        uid = f"{base}-{digest}"
    seen.add(uid)
    return f"{uid}@{DOMAIN}"


def build_event_lines(record, dtstamp, seen_uids):
    start = parse_date(record["start"])
    end = parse_date(record["end"]) if record.get("end") else start
    lines = ["BEGIN:VEVENT"]
    lines.append(f"UID:{make_uid(record, seen_uids)}")
    lines.append(f"DTSTAMP:{dtstamp}")

    timed = None
    time_str = (record.get("time") or "").strip()
    if end == start and time_str:
        m = RANGE_RE.match(time_str)
        if m:
            timed = (
                datetime.combine(start, to_24h(m.group(1), m.group(2), m.group(3))),
                datetime.combine(start, to_24h(m.group(4), m.group(5), m.group(6))),
            )
    if timed:
        lines.append(f"DTSTART;TZID=America/Chicago:{timed[0]:%Y%m%dT%H%M%S}")
        lines.append(f"DTEND;TZID=America/Chicago:{timed[1]:%Y%m%dT%H%M%S}")
    else:
        lines.append(f"DTSTART;VALUE=DATE:{start:%Y%m%d}")
        lines.append(f"DTEND;VALUE=DATE:{end + timedelta(days=1):%Y%m%d}")

    lines.append(f"SUMMARY:{escape_text(record['name'])}")
    venue = (record.get("venue") or "").strip()
    location = ", ".join(p for p in (venue, (record.get("town") or "").strip()) if p)
    if location:
        lines.append(f"LOCATION:{escape_text(location)}")

    desc_parts = []
    if (record.get("summary") or "").strip():
        desc_parts.append(record["summary"].strip())
    if time_str:
        desc_parts.append(f"Time: {time_str}")
    if (record.get("host") or "").strip():
        desc_parts.append(f"Host: {record['host'].strip()}")
    if (record.get("cost") or "").strip():
        desc_parts.append(f"Cost: {record['cost'].strip()}")
    if desc_parts:
        lines.append(f"DESCRIPTION:{escape_text(' '.join(desc_parts))}")
    if (record.get("url") or "").strip():
        lines.append(f"URL:{record['url'].strip()}")
    if (record.get("group") or "").strip():
        lines.append(f"CATEGORIES:{escape_text(record['group'].strip())}")
    lines.append("END:VEVENT")
    return lines


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("events_json", help="path to events.json")
    ap.add_argument("--out", default=".", help="output directory (default: .)")
    ap.add_argument("--all", action="store_true",
                    help="emit every record, including ended events")
    args = ap.parse_args(argv)

    records = json.loads(Path(args.events_json).read_text(encoding="utf-8"))
    if not isinstance(records, list):
        print("events.json must be a JSON list of event records", file=sys.stderr)
        return 1
    for r in records:
        if not r.get("name") or not r.get("start"):
            print(f"record missing name/start: {r!r}", file=sys.stderr)
            return 1
        parse_date(r["start"])  # raises on a malformed date: fail loudly
        if r.get("end"):
            parse_date(r["end"])

    if not args.all:
        from zoneinfo import ZoneInfo
        today_ct = datetime.now(ZoneInfo("America/Chicago")).date()
        kept = []
        for r in records:
            eff_end = parse_date(r["end"]) if r.get("end") else parse_date(r["start"])
            if eff_end >= today_ct:
                kept.append(r)
        print(f"windowing: {len(records) - len(kept)} ended event(s) omitted, "
              f"{len(kept)} emitted (use --all for every record)")
        records = kept
    records = sorted(records, key=lambda r: (r["start"], r["name"]))
    dtstamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    logical = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        f"PRODID:{PRODID}",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        f"X-WR-CALNAME:{CAL_NAME}",
        "X-WR-TIMEZONE:America/Chicago",
        "REFRESH-INTERVAL;VALUE=DURATION:PT12H",
        "X-PUBLISHED-TTL:PT12H",
        *VTIMEZONE_LINES,
    ]
    seen_uids = set()
    timed_count = 0
    for r in records:
        event_lines = build_event_lines(r, dtstamp, seen_uids)
        if any(l.startswith("DTSTART;TZID") for l in event_lines):
            timed_count += 1
        logical.extend(event_lines)
    logical.append("END:VCALENDAR")

    physical = []
    for line in logical:
        physical.extend(fold_line(line))
    payload = ("\r\n".join(physical) + "\r\n").encode("utf-8")

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    target = out / "events.ics"
    target.write_bytes(payload)
    print(f"wrote {target} ({len(payload)} bytes)")
    print(f"events emitted: {len(records)} "
          f"(timed: {timed_count}, date-only: {len(records) - timed_count})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
