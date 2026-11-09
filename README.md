# Daily

A daily brief, built by a Claude Code scheduled task every morning.

- **Read it:** https://claude.ai/artifact/QYhgy3kWgyLZiEKsot1ZRU (the same link every day)
- **What it covers:** top news, a market update, viral social media, and the week ahead
- **How it works:** see [BRIEF.md](BRIEF.md). A scheduled task starts a fresh Claude
  session each morning. The session searches the web, verifies stories, rewrites the
  page and sends a push notification.
- **Page template:** [site/index.html](site/index.html)
- **Archive:** [briefs/](briefs/), one compact Markdown file per day (`briefs/YYYY/MM-DD.md`, ~1.5 KB each), pushed to `main` by the daily run

To change what's in the brief, edit BRIEF.md and ask Claude to update the scheduled
task's prompt to match.
