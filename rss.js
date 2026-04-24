import { fetchJsonResilient } from "./request.js";
import { normalizeText, parseDate, stripHtml } from "./utils.js";

const RSS2JSON_ENDPOINT = "https://api.rss2json.com/v1/api.json";

function toRss2JsonUrl(feedUrl) {
  const params = new URLSearchParams({ rss_url: feedUrl });
  return `${RSS2JSON_ENDPOINT}?${params.toString()}`;
}

export async function fetchRssFeed(feed) {
  const payload = await fetchJsonResilient(toRss2JsonUrl(feed.url));

  if (payload.status !== "ok") {
    throw new Error(`RSS2JSON request failed for ${feed.name}`);
  }

  return (payload.items || []).map((item) => ({
    title: normalizeText(item.title),
    url: item.link,
    summary: stripHtml(item.description || "").slice(0, 220),
    source: feed.name,
    publishedAt: parseDate(item.pubDate)
  }));
}

export async function fetchAllRss(feeds) {
  const settled = await Promise.allSettled(feeds.map((feed) => fetchRssFeed(feed)));
  const articles = [];
  const failures = [];

  settled.forEach((result, index) => {
    if (result.status === "fulfilled") {
      articles.push(...result.value);
    } else {
      failures.push(feeds[index].name);
    }
  });

  return { articles, failures };
}
