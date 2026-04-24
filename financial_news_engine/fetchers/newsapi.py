from __future__ import annotations

import logging
from datetime import datetime
from typing import List

from financial_news_engine.fetchers.common import BaseFetcher, parse_datetime
from financial_news_engine.schemas import NewsItem

logger = logging.getLogger(__name__)


class NewsAPIFetcher(BaseFetcher):
    source_name = "NewsAPI"
    endpoint = "https://newsapi.org/v2/everything"

    def __init__(self, api_key: str) -> None:
        super().__init__()
        self.api_key = api_key

    def fetch_latest(self, keywords: List[str], from_date: datetime) -> List[NewsItem]:
        if not self.api_key:
            logger.warning("NEWSAPI_KEY is missing; skipping NewsAPI fetch")
            return []

        params = {
            "q": " OR ".join(keywords),
            "from": from_date.isoformat(),
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": 100,
            "apiKey": self.api_key,
        }
        data = self.get_json(self.endpoint, params)
        articles = data.get("articles", [])

        return [
            NewsItem(
                title=article.get("title", "").strip(),
                summary=(article.get("description") or "").strip(),
                url=article.get("url", "").strip(),
                published=parse_datetime(article.get("publishedAt")),
                source=(article.get("source") or {}).get("name", self.source_name),
            )
            for article in articles
            if article.get("title") and article.get("url")
        ]
