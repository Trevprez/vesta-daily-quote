# Vestra daily signature quote

Every morning a GitHub Action picks the next line from `quotes.txt`, renders it as
`docs/quote.png`, and publishes it at **https://sig.vestrafund.com/quote.png**.
Every Vestra email signature points at that one URL, so all signatures rotate together.

## Files
| File | What it does |
|---|---|
| `quotes.txt` | The quotes, one per line. Rotates daily, loops at the end. |
| `render.py` | Draws the image (Big Quote design, 520×80 shown, 2× for retina). |
| `docs/` | What GitHub Pages serves: `quote.png`, `CNAME`, a simple `index.html`. |
| `.github/workflows/daily-quote.yml` | Runs daily at ~5 AM Pacific. |
| `fonts/` | Liberation Sans (metric-identical to Arial, SIL Open Font License). |

## Editing quotes
Edit `quotes.txt` right on github.com (pencil icon) and commit. The Action re-renders
automatically. Keep quotes under ~90 characters; `python render.py --all proof/` flags any
that won't fit on two lines.

To force a refresh anytime: **Actions → Daily signature quote → Run workflow**.

## Notes
- Scheduled runs can start a few minutes to an hour late during GitHub's busy periods.
- If a run ever fails, yesterday's quote simply stays up. Nothing breaks.
- The daily commit also keeps the repo "active," so GitHub never auto-disables the schedule.
- This repo is public (required for free GitHub Pages), so the quote list is publicly visible.
