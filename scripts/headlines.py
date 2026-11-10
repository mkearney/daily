#!/usr/bin/env python3
"""Print the last 24 hours of top headlines from major outlets' news feeds.

Usage: python3 scripts/headlines.py [hours]

Groups the same story across outlets and lists stories covered by the most
outlets first, since broad coverage is a good sign a story matters. Use the
output to pick and date stories; still verify each one by search. Feeds that
fail are skipped.
"""
import concurrent.futures as cf
import datetime as dt
import email.utils
import html
import re
import sys
import urllib.request

# Editor-curated front-page feeds, spread across US, UK, international and
# left/right outlets. Checked Nov 2026; NPR, CNBC, AP and Reuters block or
# don't offer feeds, and WSJ's public feeds are stale.
FEEDS = {
    "NYT": "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
    "NYT Business": "https://rss.nytimes.com/services/xml/rss/nyt/Business.xml",
    "Washington Post": "https://feeds.washingtonpost.com/rss/national",
    "NBC News": "https://feeds.nbcnews.com/nbcnews/public/news",
    "CBS News": "https://www.cbsnews.com/latest/rss/main",
    "Fox News": "https://moxie.foxnews.com/google-publisher/latest.xml",
    "Politico": "https://rss.politico.com/politics-news.xml",
    "MarketWatch": "https://feeds.content.dowjones.io/public/rss/mw_topstories",
    "BBC": "https://feeds.bbci.co.uk/news/rss.xml",
    "BBC World": "https://feeds.bbci.co.uk/news/world/rss.xml",
    "Guardian World": "https://www.theguardian.com/world/rss",
    "Al Jazeera": "https://www.aljazeera.com/xml/rss/all.xml",
}
STOP = set("a an the of to in on for and or is are was were be by with at from as "
           "after over into says say said new its it this that his her their how "
           "why what who will can could may has have had not but about more".split())


def text(item, tag):
    m = re.search(rf"<{tag}[^>]*>(.*?)</{tag}>", item, re.S)
    if not m:
        return ""
    s = re.sub(r"<!\[CDATA\[(.*?)\]\]>", r"\1", m[1], flags=re.S)
    return html.unescape(re.sub(r"<[^>]+>", "", s)).strip()


def fetch(name, url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (daily-brief)"})
    with urllib.request.urlopen(req, timeout=20) as r:
        xml = r.read().decode("utf-8", "replace")
    out = []
    for pos, item in enumerate(re.findall(r"<item[\s>].*?</item>", xml, re.S)):
        title, link, date = text(item, "title"), text(item, "link"), text(item, "pubDate")
        try:
            when = email.utils.parsedate_to_datetime(date).astimezone(dt.timezone.utc)
        except (TypeError, ValueError):
            when = None
        if title:
            out.append({"title": title, "link": link, "when": when, "outlet": name, "pos": pos})
    return out


def org(name):
    """Count an outlet's extra feeds (e.g. BBC World) as the same outlet."""
    return name.replace(" World", "").replace(" Business", "")


def words(title):
    return {w for w in re.findall(r"[a-z0-9']+", title.lower()) if w not in STOP and len(w) > 2}


def main():
    hours = float(sys.argv[1]) if len(sys.argv) > 1 else 24
    cutoff = dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=hours)
    items, failed = [], []
    with cf.ThreadPoolExecutor(8) as ex:
        futs = {ex.submit(fetch, n, u): n for n, u in FEEDS.items()}
        for f in cf.as_completed(futs):
            try:
                items += f.result()
            except Exception:
                failed.append(futs[f])
    # Keep recent items. Undated items count only if near the top of their feed.
    items = [i for i in items if (i["when"] and i["when"] >= cutoff) or (not i["when"] and i["pos"] < 10)]

    # Group headlines that share 3+ key words (or 2 if the titles are short).
    groups = []
    for it in sorted(items, key=lambda i: (i["pos"], i["outlet"])):
        w = words(it["title"])
        for g in groups:
            shared = len(w & g["w"])
            if shared >= 3 or (shared >= 2 and min(len(w), len(g["w"])) <= 5):
                g["items"].append(it)
                g["w"] |= w
                break
        else:
            groups.append({"w": set(w), "items": [it]})

    def rank(g):
        outlets = {org(i["outlet"]) for i in g["items"]}
        return (-len(outlets), min(i["pos"] for i in g["items"]))

    groups.sort(key=rank)
    print(f"# Headlines, last {hours:g}h, {len(FEEDS) - len(failed)}/{len(FEEDS)} feeds"
          + (f" (failed: {', '.join(sorted(failed))})" if failed else ""))
    for g in groups[:40]:
        outlets = sorted({org(i["outlet"]) for i in g["items"]})
        lead = g["items"][0]  # the headline that started the group
        when = min((i["when"] for i in g["items"] if i["when"]), default=None)
        stamp = when.strftime("%m-%d %H:%MZ") if when else "undated"
        print(f"\n[{len(outlets)}] {lead['title']}\n    first seen {stamp} · {', '.join(outlets)}"
              f"\n    {lead['link']}")


if __name__ == "__main__":
    main()
