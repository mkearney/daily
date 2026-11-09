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
5. Save a compact copy to GitHub: `briefs/YYYY/MM-DD.md` on `main` in
   `mkearney/daily`. Target ~1.5 KB, hard cap 2 KB. Format:

   ```
   # YYYY-MM-DD Day · <headline>
   ## News
   - **<short title>**: <one line of key facts>. [Source](url)
   ## Markets (<day of session>)
   S&P <close> <day%> · Nasdaq <close> <day%> · Dow <close> <day%>
   - <one line per notable move or driver>
   ## Viral
   - <item> (<platform>) · <item> (<platform>)
   ## Next
   - MM/DD <event> · MM/DD <event>
   ```

   One link per news item, none elsewhere unless key. No lede, no HTML, no
   repeated background. On no-session days, the Markets section is one line.
   Commit message: `Brief YYYY-MM-DD`.
