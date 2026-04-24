import { NEWSAPI_ENDPOINT, NEWSAPI_KEY } from "./config.js";
import { fetchJsonViaProxy } from "./request.js";
import { normalizeText, parseDate, stripHtml } from "./utils.js";

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
  const payload = await fetchJsonViaProxy(targetUrl);
  if (payload.status !== "ok") {
    console.warn("NewsAPI responded with non-ok status:", payload.message || payload.status);
    return { articles: [], skipped: true, failed: true };
  }

  const articles = (payload.articles || []).map((item) => ({
    title: normalizeText(item.title),
    url: item.url,
    source: item.source?.name || "NewsAPI",
    summary: stripHtml(item.description || item.content || "").slice(0, 220),
    publishedAt: parseDate(item.publishedAt)
  }));

  return { articles, skipped: false, failed: false };
}
