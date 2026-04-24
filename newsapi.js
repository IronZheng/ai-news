import { NEWSAPI_ENDPOINT, NEWSAPI_KEY } from "./config.js";
import { normalizeText, parseDate, stripHtml } from "./utils.js";

const CORS_PROXY = "https://api.allorigins.win/raw?url=";

export async function fetchNewsApi(keyword) {
  if (!NEWSAPI_KEY || NEWSAPI_KEY === "YOUR_NEWSAPI_KEY") {
    return { articles: [], skipped: true };
  }

  const params = new URLSearchParams({
    q: keyword,
    language: "en",
    sortBy: "publishedAt",
    pageSize: "50",
    apiKey: NEWSAPI_KEY
  });

  const targetUrl = `${NEWSAPI_ENDPOINT}?${params.toString()}`;
  const response = await fetch(`${CORS_PROXY}${encodeURIComponent(targetUrl)}`);
  if (!response.ok) {
    throw new Error("NewsAPI request failed");
  }

  const payload = await response.json();
  if (payload.status !== "ok") {
    throw new Error(payload.message || "NewsAPI error");
  }

  const articles = (payload.articles || []).map((item) => ({
    title: normalizeText(item.title),
    url: item.url,
    source: item.source?.name || "NewsAPI",
    summary: stripHtml(item.description || item.content || "").slice(0, 220),
    publishedAt: parseDate(item.publishedAt)
  }));

  return { articles, skipped: false };
}
