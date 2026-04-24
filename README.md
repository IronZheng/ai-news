# Financial News Search (GitHub Pages MVP)

A minimal static web app that searches **real financial news** across multiple sources:

- Reuters Business RSS
- Reuters Markets RSS
- Yahoo Finance RSS
- Investing.com RSS
- NewsAPI (`/v2/everything`)

The app merges all fetched stories, filters by keyword and last 7 days, deduplicates by `title + url` hash, and sorts by newest first.

## Project files

- `index.html` - page structure and app shell
- `style.css` - dark theme + responsive card layout
- `script.js` - search flow, aggregation, filter/sort/dedupe, rendering
- `config.js` - `NEWSAPI_KEY` and source config
- `rss.js` - RSS fetching and XML parsing
- `newsapi.js` - NewsAPI fetching
- `utils.js` - helper functions

## How to get a NewsAPI key

1. Go to [https://newsapi.org/](https://newsapi.org/).
2. Create an account and verify your email.
3. Copy your API key from your NewsAPI dashboard.
4. Open `config.js` and replace:

```js
export const NEWSAPI_KEY = "YOUR_NEWSAPI_KEY";
```

with your real key.

> Note: this is a frontend-only MVP. Your key is visible in client-side code.

## Run locally

Because the project uses ES modules, run it from a local server (not `file://`):

```bash
python3 -m http.server 8080
```

Then open `http://localhost:8080`.

## Deploy to GitHub Pages

1. Push the repository to GitHub.
2. In GitHub, open **Settings → Pages**.
3. Under **Build and deployment**:
   - **Source**: `Deploy from a branch`
   - **Branch**: `main` (or your default branch)
   - **Folder**: `/ (root)`
4. Save.
5. After deployment, open your Pages URL (shown in the Pages settings).

## How to test search

1. Open the deployed app or local server.
2. Enter a keyword like `Tesla`, `Amazon`, or `Gold`.
3. Click **Search** or press **Enter**.
4. Confirm:
   - Loading state appears (`Loading news...`)
   - Cards show title, source, published time, summary, and **Read Article** link
   - Only recent stories (last 7 days) are shown
   - Results are sorted newest first
   - No/failed states display correctly (`No news found`, `Error fetching news`)
