# Daily brief: requirements

The scheduled task's prompt implements these rules. Change both together.

## Schedule and delivery
1. Runs every day at 8:23am US Eastern, in a fresh Claude session.
2. Output goes to GitHub only, pushed directly to `main` in `mkearney/daily` with
   no pull request. Commit message: `Brief YYYY-MM-DD`.
3. Each run writes the same brief to two files:
   - `briefs/YYYY/MM-DD.md`, the permanent archive.
   - `README.md`, overwritten daily so the repo's front page always shows today.
     It ends with a footer linking to the archive and this file.
4. A phone notification is sent when the run finishes.

## Content
5. Three sections, in this order: **Top stories**, **Markets**, **Going viral**.
6. Readable in under 5 minutes on a phone.
7. Opens with a bold headline about something new today.
8. **Top stories:** up to 5 major US and world events from the last 24 hours. Each
   gets a `###` headline, 1–3 sentences and a source link.
9. **Markets:** one line with the last session's % change for the S&P 500, Nasdaq
   and Dow, plus the 10-year Treasury yield level and its change in basis points.
   Example: `S&P 500 **+0.3%** · Nasdaq **+1.1%** · Dow **−0.5%** · 10-yr 4.31% (+4 bp)`.
   Add one sentence on why only if an index moved 1% or more, or the 10-year moved
   10 bp or more. No tables, index levels, weekly figures or other assets.
   - Numbers come from FRED via `python3 scripts/markets.py`, which also picks the
     session and handles no-trading days. Use its output as is.
   - At 8:23am FRED usually has the Dow and Nasdaq but not yet the S&P 500 or
     10-year. The script marks those `MISSING:<series>`; fill only those from web
     search, in the same format. If a value can't be found reliably, drop it.
   - Remove the script's trailing `<!-- ... -->` note from the brief.
10. **Going viral:** up to 4 viral items from TikTok, Instagram, X, YouTube or
    Reddit, each labeled with its platform.

## No repeats
11. Before researching, the run reads the last 7 days of `briefs/` to see what has
    already been reported.
12. A reported story returns only with a material new development (a decision,
    result, vote, official action, ruling, resignation or casualty count). Its
    headline ends with `(update)`, and it says only what's new. Reaction and
    analysis don't count.
13. A slow news day means fewer stories (2 is fine), not old ones.
14. Each trading session is reported once. If there has been no session since the
    last brief (Sundays, Mondays, days after holidays), Markets reads "No trading
    since the last brief." The script handles this.
15. Viral items aren't repeated unless they take a big new turn. Fewer than 3 new
    items means fewer are shown.

## Accuracy
16. Start top-story research with `python3 scripts/headlines.py`. It pulls Google
    News Top Stories plus its U.S., World, Business and Tech sections, in Google's
    order, with the outlets covering each story. Higher in the list and more
    outlets means a bigger story; a story from a single outlet needs a good reason
    to lead. To check a story from recent briefs for real updates, run
    `python3 scripts/headlines.py "<story keywords>"` (searches the past day). Use
    web search to fill gaps and to find details and direct article links.
17. Every top story is checked with a second search against a major outlet (AP,
    Reuters, BBC, NYT, WSJ, Bloomberg, CNBC, networks). Stories found only on
    aggregators or blogs are dropped or labeled unconfirmed.
18. Event dates are checked, not article dates. Older events are left out, or
    their date is stated if they're new to the reader.
19. When sources disagree on numbers, the most precise primary source is used,
    and preliminary figures are labeled.

## Writing
20. Plain, neutral, short sentences. No opinion, hype or filler. Every sentence
    carries a fact.
21. Nice-looking Markdown that matches the layout of the existing files in
    `briefs/`. About 1.5–2 KB per day, under 3 KB.
