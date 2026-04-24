from __future__ import annotations

import logging
from datetime import datetime
from typing import List

from financial_news_engine.fetchers.common import BaseFetcher, parse_datetime
from financial_news_engine.schemas import NewsItem

logger = logging.getLogger(__name__)


class GDELTFetcher(BaseFetcher):
    source_name = "GDELT"
    endpoint = "https://api.gdeltproject.org/api/v2/doc/doc"

    def fetch_latest(self, keywords: List[str], from_date: datetime) -> List[NewsItem]:
        query = " OR ".join(keywords)
        params = {
            "query": query,
            "mode": "ArtList",
            "format": "json",
            "maxrecords": 250,
            "sort": "DateDesc",
            "startdatetime": from_date.strftime("%Y%m%d%H%M%S"),
        }
        data = self.get_json(self.endpoint, params)
        articles = data.get("articles", [])
        return [
            NewsItem(
                title=(item.get("title") or "").strip(),
                summary=(item.get("seendate") or "").strip(),
                url=(item.get("url") or "").strip(),
                published=parse_datetime(item.get("seendate")),
                source=(item.get("sourceCommonName") or self.source_name),
            )
            for item in articles
            if item.get("title") and item.get("url")
        ]
