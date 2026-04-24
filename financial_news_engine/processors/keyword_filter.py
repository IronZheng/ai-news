from __future__ import annotations

from typing import List

from financial_news_engine.schemas import NewsItem


class KeywordFilter:
    @staticmethod
    def filter_items(items: List[NewsItem], keywords: List[str]) -> List[NewsItem]:
        lower_keywords = [k.lower() for k in keywords]
        return [
            item
            for item in items
            if any(k in f"{item.title} {item.summary}".lower() for k in lower_keywords)
        ]
