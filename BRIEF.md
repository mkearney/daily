# Daily brief instructions

These are the instructions the scheduled task follows each morning. The task's
prompt holds a copy of this file, so change both together.

## Goal

A brief someone can read in under 5 minutes on a phone. It has four sections in
this order:

1. **Top stories**: 3–5 major news events from the last 24 hours (US and world). Each
   gets a headline, 2–4 plain sentences, and source links.
2. **Markets**: S&P 500, Nasdaq and Dow (close, day %, week % when relevant). Add
   10-year Treasury yield, oil, gold and bitcoin when reliable figures are found.
   Then 2–4 bullets on why markets moved and notable stock movers. On weekends
   and holidays, cover the last trading day and the week.
3. **Going viral**: 3–4 notable viral things on social media (TikTok, Instagram, X,
   YouTube, Reddit): memes, trends, moments people are talking about. Label the
   platform.
4. **Coming up**: 2–4 dated events in the next week (economic data, earnings,
   elections, launches, big games).

## No repeats

The reader reads every day, so the brief never repeats something already shown.
The page keeps a hidden coverage log (`<!-- COVERED:START ... COVERED:END -->`)
listing every item reported in the last 7 days with the latest facts given.

- A logged story comes back only with a material new development (a decision,
  result, vote, official action, ruling, resignation). It gets an **Update** tag
  and 1–2 sentences on only what's new. Otherwise it's left out.
- Slow news day means fewer stories, not old ones.
- If the latest market close is already logged (weekends, holidays, Monday
  morning), the Markets section becomes "No new session" with 1–3 bullets on
  what's new (futures, overseas, crypto, oil, company news).
- Viral items are never repeated unless they've taken a big new turn.
- "Coming up" may carry items over, minus anything already past.
- Each run adds its items to the log and drops lines older than 7 days.

## Research

- Use WebSearch. Run the searches in parallel: today's top news, yesterday's
  market close, viral/trending social media, and the week ahead. Use "extended"
  mode for news and markets.
- Verify every top story with a second search, preferring AP, Reuters, BBC, NYT,
  WSJ, Bloomberg, CNBC or major networks. Drop or clearly mark as unconfirmed
  anything only aggregators or blogs report.
- Check every item's date. Search results often mix in older stories; leave
  out anything that isn't from the last 24–48 hours (viral trends: the last week).
- When sources disagree on numbers, use the most precise primary source and
  say figures are preliminary if needed.
- Page fetches may be blocked by the network policy. Search results are enough.

## Writing

- Plain, neutral, short sentences. No opinion or hype.
- A one-line headline for the day (`h1`) and a one-sentence lede.
- Every section ends with source links.

## Output

1. Read the published page `https://claude.ai/artifact/QYhgy3kWgyLZiEKsot1ZRU` with
   the Artifact tool (`action: "read"`). It names a saved file holding the full page.
2. Replace only the content between `<!-- BRIEF:START -->` and `<!-- BRIEF:END -->`.
   Keep the same HTML structure and CSS classes (`story`, `tickers`, `num up/down`,
   `bullets`, `tag`, `src`). Update the dateline and footer date.
3. Republish to that same URL (`url` set to the link above) so the link stays the same.
4. Send a push notification with the headline and a one-line summary.
5. Save a Markdown copy to GitHub: `briefs/YYYY/MM-DD.md` on `main` in
   `mkearney/daily`. Commit message: `Brief YYYY-MM-DD`. Match the layout of the
   existing files in `briefs/`:
   - `# Weekday, Month D, YYYY`, then the day's headline in bold.
   - `## Top stories`, each story an `###` headline, 1–3 tight sentences, and a
     `<br>[Source](url)` line. Updates get `(update)` in the headline.
   - `## Markets · <session>` with a Markdown table (Index | Close | Day | Week),
     2–3 bold-labeled bullets, and one `Sources:` line. No-session days: just
     1–2 bullets.
   - `## Going viral`: bold item, platform in parentheses, one line each.
   - `## Coming up`: bold dates, short event names.

   Write efficiently: short sentences, no filler, no repeated background, no
   hedging beyond what accuracy needs. Typically about 2 KB; aim to stay under 3 KB.
