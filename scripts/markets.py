#!/usr/bin/env python3
"""Print the Markets section for today's brief using FRED data.

Usage: python3 scripts/markets.py [briefs_dir]

Finds the last trading session already reported in briefs/, picks the next
session FRED has, and prints the Markdown section. Any figure FRED hasn't
published yet is printed as MISSING:<series> so it can be filled from search.
Needs FRED_API_KEY in the environment.
"""
import datetime as dt
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

SERIES = [("SP500", "S&P 500"), ("NASDAQCOM", "Nasdaq"), ("DJIA", "Dow")]
YIELD = "DGS10"
MINUS = "−"


def fetch(series_id):
    """Return {date: value} for the latest observations, skipping blanks."""
    url = (
        "https://api.stlouisfed.org/fred/series/observations"
        f"?series_id={series_id}&api_key={os.environ['FRED_API_KEY']}"
        "&file_type=json&sort_order=desc&limit=15"
    )
    with urllib.request.urlopen(url, timeout=30) as r:
        obs = json.load(r)["observations"]
    return {o["date"]: float(o["value"]) for o in obs if o["value"] != "."}


def last_reported(briefs_dir):
    """Date of the most recent session named in a '## Markets · Ddd Mon D' heading."""
    for path in sorted(Path(briefs_dir).glob("*/*.md"), reverse=True):
        year = int(path.parent.name)
        m = re.search(r"^## Markets · \w{3} (\w{3}) (\d{1,2})\s*$", path.read_text(), re.M)
        if m:
            d = dt.datetime.strptime(f"{m[1]} {m[2]} {year}", "%b %d %Y").date()
            file_month = int(path.stem.split("-")[0])
            if d.month > file_month:  # e.g. a January brief reporting a December session
                d = d.replace(year=year - 1)
            return d
    return None


def change(values, date):
    """Return (value, previous value) for date, or None if FRED lacks it."""
    if date not in values:
        return None
    earlier = sorted(d for d in values if d < date)
    return (values[date], values[earlier[-1]]) if earlier else None


def signed(x, fmt):
    s = format(abs(x), fmt)
    return ("+" if x >= 0 else MINUS) + s


def main():
    briefs_dir = sys.argv[1] if len(sys.argv) > 1 else "briefs"
    after = last_reported(briefs_dir)
    data = {sid: fetch(sid) for sid, _ in SERIES}
    data[YIELD] = fetch(YIELD)

    # The session to report: the earliest index date after the last one reported.
    # Use the earliest so no session is skipped if two have passed (e.g. a missed run).
    dates = sorted({d for sid, _ in SERIES for d in data[sid]})
    new = [d for d in dates if after is None or dt.date.fromisoformat(d) > after]
    if not new:
        print("## Markets\n\nNo trading since the last brief.")
        return
    session = new[0]

    parts, missing, big = [], [], False
    for sid, name in SERIES:
        c = change(data[sid], session)
        if c:
            pct = (c[0] / c[1] - 1) * 100
            big |= abs(pct) >= 1
            parts.append(f"{name} **{signed(pct, '.1f')}%**")
        else:
            parts.append(f"{name} MISSING:{sid}")
            missing.append(sid)
    c = change(data[YIELD], session)
    if c:
        bp = round((c[0] - c[1]) * 100)
        big |= abs(bp) >= 10
        parts.append(f"10-yr {c[0]:.2f}% ({signed(bp, 'd')} bp)")
    else:
        parts.append(f"10-yr MISSING:{YIELD}")
        missing.append(YIELD)

    label = dt.date.fromisoformat(session).strftime("%a %b %-d")
    print(f"## Markets · {label}\n\n" + " · ".join(parts))
    print(f"\n<!-- session={session} missing={','.join(missing) or 'none'} "
          f"big_move={'yes' if big else 'no (so far)'} -->")


if __name__ == "__main__":
    main()
