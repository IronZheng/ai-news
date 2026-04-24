from __future__ import annotations

import hashlib
import logging
from typing import List, Set

from financial_news_engine.schemas import NewsItem

logger = logging.getLogger(__name__)


class Deduplicator:
    @staticmethod
    def deduplicate(items: List[NewsItem]) -> List[NewsItem]:
        seen: Set[str] = set()
        unique: List[NewsItem] = []
        duplicates = 0

        for item in items:
            key = hashlib.sha256(f"{item.title}{item.url}".encode("utf-8")).hexdigest()
            if key in seen:
                duplicates += 1
                continue
            seen.add(key)
            unique.append(item)

        logger.info("Duplicates removed: %d", duplicates)
        return unique
