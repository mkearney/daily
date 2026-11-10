# Daily brief: requirements

The scheduled task's prompt implements these rules. Change both together.

## Schedule and delivery
1. Runs every day at 6:23am US Eastern, in a fresh Claude session.
2. Publishes to one page that keeps the same link: https://claude.ai/artifact/QYhgy3kWgyLZiEKsot1ZRU
3. Sends a push notification to the phone when done.
4. Commits a Markdown copy to `main` in `mkearney/daily` at `briefs/YYYY/MM-DD.md`,
   with the message `Brief YYYY-MM-DD`. Pushes directly, with no pull request.

## Content
5. Three sections, in this order: **Top stories**, **Markets**, **Going viral**.
6. Readable in under 5 minutes on a phone.
7. Starts with a headline about something new today and a one-sentence lede.
8. **Top stories:** up to 5 major US and world events from the last 24 hours. Each
   gets a headline, 2–4 sentences and source links.
9. **Markets:** S&P 500, Nasdaq and Dow (close, day %, week % when relevant). Adds
   the 10-year yield, oil, gold and bitcoin when reliable figures exist. Then 2–4
   bullets on why markets moved and notable movers.
10. **Going viral:** up to 4 viral items from TikTok, Instagram, X, YouTube or
    Reddit, each labeled with its platform.

## No repeats
11. The page keeps a hidden log of every item reported in the last 7 days.
12. A logged story returns only with a material new development (a decision,
    result, vote, official action, ruling, resignation or casualty count). It's
    tagged **Update** and says only what's new. Reaction and analysis don't count.
13. A slow news day means fewer stories (2 is fine), not old ones.
14. If the latest market close was already reported (weekends, holidays, Monday
    morning), there's no table. Markets shows "No new session" with 1–3 bullets on
    what's new (futures, overseas markets, crypto, oil, company news).
15. Viral items aren't repeated unless they take a big new turn. Fewer than 3 new
    items means fewer are shown.

## Accuracy
16. Every top story is checked with a second search against a major outlet (AP,
    Reuters, BBC, NYT, WSJ, Bloomberg, CNBC, networks). Stories found only on
    aggregators or blogs are dropped or labeled unconfirmed.
17. Event dates are checked, not article dates. Older events are left out, or
    their date is stated if they're new to the reader.
18. When sources disagree on numbers, the most precise primary source is used,
    and preliminary figures are labeled.

## Writing
19. Plain, neutral, short sentences. No opinion, hype or filler. Every sentence
    carries a fact.
20. Each section ends with source links.

## GitHub copy
21. A nice-looking Markdown file with the same content as the page. It matches
    the layout of the existing files in `briefs/`: a date title, the bold
    headline, `###` per story with a source link, a markets table with bullets,
    and viral bullets.
22. Written efficiently: about 2 KB per day, and under 3 KB.
