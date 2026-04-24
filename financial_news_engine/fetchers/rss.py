from __future__ import annotations

import logging
from datetime import datetime
from typing import Dict, List

import feedparser

from financial_news_engine.fetchers.common import parse_datetime
from financial_news_engine.schemas import NewsItem

logger = logging.getLogger(__name__)


class RSSFetcher:
    feeds: Dict[str, str] = {
        "Reuters": "https://www.reutersagency.com/feed/?best-topics=business-finance&post_type=best",
        "Yahoo Finance": "https://finance.yahoo.com/news/rssindex",
        "Investing.com": "https://www.investing.com/rss/news.rss",
    }

    def fetch_latest(self, keywords: List[str], from_date: datetime) -> List[NewsItem]:
        lower_keywords = [k.lower() for k in keywords]
        collected: List[NewsItem] = []

        for source, url in self.feeds.items():
            try:
                parsed = feedparser.parse(url)
            except Exception as exc:
                logger.exception("RSS fetch error for %s: %s", source, exc)
                continue

            for entry in parsed.entries:
                title = (entry.get("title") or "").strip()
                summary = (entry.get("summary") or "").strip()
                link = (entry.get("link") or "").strip()
                published = parse_datetime(entry.get("published") or entry.get("updated"))
                if not title or not link or published < from_date:
                    continue
                haystack = f"{title} {summary}".lower()
                if not any(k in haystack for k in lower_keywords):
                    continue
                collected.append(
                    NewsItem(
                        title=title,
                        summary=summary,
                        url=link,
                        published=published,
                        source=source,
                    )
                )
        return collected
