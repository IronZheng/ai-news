from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import List

from financial_news_engine.fetchers.common import BaseFetcher, parse_datetime
from financial_news_engine.schemas import NewsItem

logger = logging.getLogger(__name__)


class FinnhubFetcher(BaseFetcher):
    source_name = "Finnhub"
    endpoint = "https://finnhub.io/api/v1/news"

    def __init__(self, api_key: str) -> None:
        super().__init__()
        self.api_key = api_key

    def fetch_latest(self, keywords: List[str], from_date: datetime) -> List[NewsItem]:
        if not self.api_key:
            logger.warning("FINNHUB_KEY is missing; skipping Finnhub fetch")
            return []

        params = {
            "category": "general",
            "token": self.api_key,
        }
        data = self.get_json(self.endpoint, params)
        lower_keywords = [k.lower() for k in keywords]
        results: List[NewsItem] = []

        for item in data:
            headline = (item.get("headline") or "").strip()
            summary = (item.get("summary") or "").strip()
            if not headline or not item.get("url"):
                continue
            published = parse_datetime(datetime.fromtimestamp(item.get("datetime", 0), tz=timezone.utc).isoformat())
            if published < from_date:
                continue
            haystack = f"{headline} {summary}".lower()
            if not any(word in haystack for word in lower_keywords):
                continue
            results.append(
                NewsItem(
                    title=headline,
                    summary=summary,
                    url=item["url"],
                    published=published,
                    source=item.get("source", self.source_name),
                )
            )
        return results
