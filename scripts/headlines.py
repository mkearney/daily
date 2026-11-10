#!/usr/bin/env python3
"""Print today's candidate top stories from Google News.

Usage:
  python3 scripts/headlines.py            # top stories + U.S., World, Business, Tech
  python3 scripts/headlines.py "query"    # past-day search, e.g. to check a story for updates

Google News already groups each story with coverage from other outlets, and
its Top Stories order reflects editorial weight across many sources. Stories
are listed in that order, with the outlets covering them. Items older than 36
hours are dropped. Links are Google News redirect links, which open the article.
"""
import concurrent.futures as cf
import datetime as dt
import email.utils
import html
import re
import signal
import sys
import time
import urllib.parse
import urllib.request

BASE = "https://news.google.com/rss"
PARAMS = "hl=en-US&gl=US&ceid=US:en"
SECTIONS = {
    "Top": f"{BASE}?{PARAMS}",
    "U.S.": f"{BASE}/headlines/section/topic/NATION?{PARAMS}",
    "World": f"{BASE}/headlines/section/topic/WORLD?{PARAMS}",
    "Business": f"{BASE}/headlines/section/topic/BUSINESS?{PARAMS}",
    "Tech": f"{BASE}/headlines/section/topic/TECHNOLOGY?{PARAMS}",
}
MAX_AGE = dt.timedelta(hours=36)
STOP = set("a an the of to in on for and or is are was were be by with at from as "
           "after over into says say said new its it this that his her their how "
           "why what who will can could may has have had not but about more".split())


def get(url, tries=3):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (daily-brief)"})
    for attempt in range(tries):
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                return r.read().decode("utf-8", "replace")
        except Exception:
            if attempt == tries - 1:
                raise
            time.sleep(3 * (attempt + 1))


def tag(item, name):
    m = re.search(rf"<{name}[^>]*>(.*?)</{name}>", item, re.S)
    return html.unescape(m[1]).strip() if m else ""


def parse(xml, section):
    out = []
    for pos, item in enumerate(re.findall(r"<item>(.*?)</item>", xml, re.S)):
        outlet = tag(item, "source")
        title = tag(item, "title")
        if outlet and title.endswith(" - " + outlet):
            title = title[: -len(outlet) - 3]
        try:
            when = email.utils.parsedate_to_datetime(tag(item, "pubDate")).astimezone(dt.timezone.utc)
        except (TypeError, ValueError):
            when = None
        # The description lists related coverage: <a ...>title</a> <font>Outlet</font>.
        related = re.findall(r"<font[^>]*>(.*?)</font>", tag(item, "description"))
        outlets = list(dict.fromkeys([outlet] + [html.unescape(o) for o in related]))
        out.append({"title": title, "outlets": [o for o in outlets if o], "when": when,
                    "link": tag(item, "link"), "section": section, "pos": pos})
    return out


def words(title):
    return {w for w in re.findall(r"[a-z0-9']+", title.lower()) if w not in STOP and len(w) > 2}


def show(items, limit):
    now = dt.datetime.now(dt.timezone.utc)
    shown = []
    for it in items:
        if it["when"] and now - it["when"] > MAX_AGE:
            continue
        w = words(it["title"])
        dup = next((s for s in shown if len(w & s["w"]) >= 3), None)
        if dup:  # same story from another section: merge outlets, keep the first
            dup["outlets"] = list(dict.fromkeys(dup["outlets"] + it["outlets"]))
            dup["sections"].add(it["section"])
            continue
        shown.append({**it, "w": w, "sections": {it["section"]}})
        if len(shown) >= limit:
            break
    for s in shown:
        stamp = s["when"].strftime("%m-%d %H:%MZ") if s["when"] else "undated"
        print(f"\n[{'/'.join(sorted(s['sections']))}] {s['title']}"
              f"\n    {stamp} · {len(s['outlets'])} outlets: {', '.join(s['outlets'][:6])}"
              f"\n    {s['link']}")


def main():
    if len(sys.argv) > 1:
        q = urllib.parse.quote_plus(" ".join(sys.argv[1:]) + " when:1d")
        print(f"# Google News, past day: {' '.join(sys.argv[1:])}")
        show(parse(get(f"{BASE}/search?q={q}&{PARAMS}"), "Search"), 12)
        return
    results, failed = {}, []
    with cf.ThreadPoolExecutor(5) as ex:
        futs = {ex.submit(get, u): n for n, u in SECTIONS.items()}
        for f in cf.as_completed(futs):
            try:
                results[futs[f]] = parse(f.result(), futs[f])
            except Exception:
                failed.append(futs[f])
    if not results:
        print("Google News unavailable; use web search only.")
        return
    print(f"# Google News headlines ({len(results)}/{len(SECTIONS)} sections"
          + (f"; failed: {', '.join(failed)}" if failed else "") + ")")
    # Top Stories first in Google's order, then each section's leading stories.
    items = results.get("Top", [])
    for name in ["U.S.", "World", "Business", "Tech"]:
        items += results.get(name, [])[:12]
    show(items, 40)


if __name__ == "__main__":
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)  # quiet exit when piped to head
    main()
