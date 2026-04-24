import { RSS_FEEDS } from "./config.js";
import { fetchAllRss } from "./rss.js";
import { fetchNewsApi } from "./newsapi.js";
import { formatDate, hashString, isRecent, normalizeText } from "./utils.js";

const keywordInput = document.getElementById("keyword");
const searchBtn = document.getElementById("searchBtn");
const statusEl = document.getElementById("status");
const resultsEl = document.getElementById("results");

function setStatus(message, type = "") {
  statusEl.textContent = message;
  statusEl.className = type ? `status ${type}` : "status";
}

function createCard(article) {
  const card = document.createElement("article");
  card.className = "card";

  const title = document.createElement("h3");
  title.textContent = article.title || "Untitled";

  const meta = document.createElement("div");
  meta.className = "meta";
  meta.textContent = `${article.source || "Unknown source"} · ${formatDate(article.publishedAt)}`;

  const summary = document.createElement("p");
  summary.textContent = article.summary || "No summary available.";

  const link = document.createElement("a");
  link.href = article.url;
  link.target = "_blank";
  link.rel = "noopener noreferrer";
  link.textContent = "Read Article";

  card.append(title, meta, summary, link);
  return card;
}

function dedupeArticles(articles) {
  const seen = new Set();
  return articles.filter((article) => {
    const key = `${normalizeText(article.title).toLowerCase()}::${article.url || ""}`;
    const hashed = hashString(key);
    if (seen.has(hashed)) {
      return false;
    }
    seen.add(hashed);
    return true;
  });
}

function keywordMatch(article, keyword) {
  const haystack = `${article.title} ${article.summary} ${article.source}`.toLowerCase();
  return haystack.includes(keyword.toLowerCase());
}

function clearResults() {
  resultsEl.innerHTML = "";
}

function renderResults(articles) {
  clearResults();
  const fragment = document.createDocumentFragment();
  articles.forEach((article) => fragment.appendChild(createCard(article)));
  resultsEl.appendChild(fragment);
}

async function performSearch() {
  const keyword = normalizeText(keywordInput.value);
  if (!keyword) {
    setStatus("Please enter a keyword.", "error");
    clearResults();
    return;
  }

  setStatus("Loading news...");
  clearResults();

  try {
    const [rssResult, newsApiResult] = await Promise.all([
      fetchAllRss(RSS_FEEDS),
      fetchNewsApi(keyword)
    ]);

    const combined = [...rssResult.articles, ...newsApiResult.articles]
      .filter((article) => article.title && article.url && article.publishedAt)
      .filter((article) => isRecent(article.publishedAt, 7))
      .filter((article) => keywordMatch(article, keyword));

    const unique = dedupeArticles(combined).sort(
      (a, b) => b.publishedAt.getTime() - a.publishedAt.getTime()
    );

    if (unique.length === 0) {
      setStatus("No news found");
      return;
    }

    const failedSources = rssResult.failures.length
      ? ` Some sources failed: ${rssResult.failures.join(", ")}.`
      : "";
    const skippedNewsApi = newsApiResult.skipped ? " NewsAPI skipped (missing API key)." : "";
    setStatus(`Showing ${unique.length} results.${failedSources}${skippedNewsApi}`.trim());
    renderResults(unique);
  } catch (error) {
    console.error(error);
    setStatus("Error fetching news", "error");
  }
}

searchBtn.addEventListener("click", performSearch);
keywordInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter") {
    performSearch();
  }
});
