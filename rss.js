import { normalizeText, parseDate, stripHtml } from "./utils.js";

const CORS_PROXY = "https://api.allorigins.win/raw?url=";

function getBestText(item, selectors) {
  for (const selector of selectors) {
    const node = item.querySelector(selector);
    if (node?.textContent) {
      return normalizeText(node.textContent);
    }
  }
  return "";
}

export async function fetchRssFeed(feed) {
  const response = await fetch(`${CORS_PROXY}${encodeURIComponent(feed.url)}`);
  if (!response.ok) {
    throw new Error(`RSS request failed for ${feed.name}`);
  }

  const xmlText = await response.text();
  const xml = new DOMParser().parseFromString(xmlText, "application/xml");
  const items = Array.from(xml.querySelectorAll("item"));

  return items.map((item) => {
    const title = getBestText(item, ["title"]);
    const url = getBestText(item, ["link"]);
    const descriptionRaw = getBestText(item, ["description", "content"]);
    const source = getBestText(item, ["source"]);
    const publishedText = getBestText(item, ["pubDate", "published", "dc\\:date"]);

    return {
      title,
      url,
      summary: stripHtml(descriptionRaw).slice(0, 220),
      source: source || feed.name,
      publishedAt: parseDate(publishedText)
    };
  });
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
