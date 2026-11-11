#!/usr/bin/env python3
"""Print today's candidates for the Going viral section.

Usage:
  python3 scripts/viral.py

Sources, all free:
  Reddit     top posts of the day from a few big subreddits (public RSS, no key).
             Reddit's .json endpoints are blocked from cloud servers; RSS is not,
             but it rate-limits fast, so feeds are fetched slowly, one at a time.
  Signals    Bluesky trending topics, Google Trends daily searches and the most-read
             Wikipedia pages. These show what people are talking about, to help
             spot and confirm viral items; they are not items themselves.
"""
import datetime as dt
import html
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

UA = "Mozilla/5.0 (compatible; daily-brief/0.1)"
SUBREDDITS = ["popular", "videos", "nextfuckinglevel", "memes", "TikTokCringe"]
REDDIT_PER_SUB = 8
REDDIT_GAP = 6  # seconds between Reddit requests, to stay under its rate limit
BLUESKY = "https://public.api.bsky.app/xrpc/app.bsky.unspecced.getTrendingTopics"
TRENDS = "https://trends.google.com/trending/rss?geo=US"
WIKI = "https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia/all-access/{}"
WIKI_SKIP = re.compile(r"^(Main_Page|Special:|Wikipedia:|Portal:|File:|Help:|Talk:|-$)")


def get(url, headers=None, tries=3, wait=10):
    req = urllib.request.Request(url, headers={"User-Agent": UA, **(headers or {})})
    for attempt in range(tries):
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                return r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            # Retry rate limits and server errors; other errors are final.
            if e.code not in (429, 500, 502, 503) or attempt == tries - 1:
                raise
        except (urllib.error.URLError, TimeoutError):
            if attempt == tries - 1:
                raise
        time.sleep(wait * (attempt + 1))


def tag(text, name):
    m = re.search(rf"<{name}[^>]*>(.*?)</{name}>", text, re.S)
    return html.unescape(m[1]).strip() if m else ""


def age(when):
    hours = (dt.datetime.now(dt.timezone.utc) - when).total_seconds() / 3600
    return f"{hours:.0f}h ago"


def reddit():
    print("## Reddit (top posts today, in Reddit's order)\n")
    seen = set()
    for i, sub in enumerate(SUBREDDITS):
        if i:
            time.sleep(REDDIT_GAP)
        try:
            xml = get(f"https://www.reddit.com/r/{sub}/top/.rss?t=day&limit={REDDIT_PER_SUB}")
        except Exception as e:
            print(f"[r/{sub}] failed: {e}\n")
            continue
        for entry in re.findall(r"<entry>(.*?)</entry>", xml, re.S)[:REDDIT_PER_SUB]:
            link = re.search(r'<link href="([^"]+)"', entry)
            link = link[1] if link else ""
            if link in seen:
                continue
            seen.add(link)
            cat = re.search(r'<category[^>]*label="([^"]+)"', entry)
            where = cat[1] if cat else f"r/{sub}"
            try:
                when = age(dt.datetime.fromisoformat(tag(entry, "published")))
            except ValueError:
                when = "?"
            print(f"[r/{sub}] {tag(entry, 'title')}\n    {where} · {when}\n    {link}\n")



def signals():
    print("## Signals (context only, not items)\n")
    try:
        topics = json.loads(get(BLUESKY)).get("topics", [])
        print("Bluesky trending: " + "; ".join(t["topic"] for t in topics[:12]))
    except Exception as e:
        print(f"Bluesky trending: failed: {e}")
    try:
        xml = get(TRENDS)
        items = re.findall(r"<item>(.*?)</item>", xml, re.S)
        print("Google Trends US: " + "; ".join(
            f"{tag(i, 'title')} ({tag(i, 'ht:approx_traffic')})" for i in items[:12]))
    except Exception as e:
        print(f"Google Trends US: failed: {e}")
    yesterday = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=1)).strftime("%Y/%m/%d")
    try:
        arts = json.loads(get(WIKI.format(yesterday)))["items"][0]["articles"]
        top = [a for a in arts if not WIKI_SKIP.match(a["article"])][:12]
        print(f"Wikipedia most read ({yesterday}): " + "; ".join(
            f"{a['article'].replace('_', ' ')} ({a['views'] // 1000}k)" for a in top))
    except Exception as e:
        print(f"Wikipedia most read: failed: {e}")


def main():
    print("# Viral candidates\n")
    signals()
    print()
    reddit()


if __name__ == "__main__":
    sys.exit(main())
