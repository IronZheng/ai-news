from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import List

from financial_news_engine.config import settings
from financial_news_engine.fetchers.finnhub import FinnhubFetcher
from financial_news_engine.fetchers.gdelt import GDELTFetcher
from financial_news_engine.fetchers.newsapi import NewsAPIFetcher
from financial_news_engine.fetchers.rss import RSSFetcher
from financial_news_engine.processors.dedup import Deduplicator
from financial_news_engine.processors.keyword_filter import KeywordFilter
from financial_news_engine.processors.ner import EntityProcessor
from financial_news_engine.processors.sentiment import SentimentProcessor
from financial_news_engine.processors.topic_classifier import TopicClassifier
from financial_news_engine.schemas import NewsItem
from financial_news_engine.storage.db import Database

logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), logging.INFO),
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
logger = logging.getLogger(__name__)


class NewsPipeline:
    def __init__(self) -> None:
        self.keywords = settings.tracked_keywords
        self.fetchers = [
            NewsAPIFetcher(settings.newsapi_key),
            FinnhubFetcher(settings.finnhub_key),
            GDELTFetcher(),
            RSSFetcher(),
        ]
        self.sentiment_processor = SentimentProcessor()
        self.entity_processor = EntityProcessor()
        self.topic_classifier = TopicClassifier()

    def fetch_all(self) -> List[NewsItem]:
        from_date = settings.from_date
        items: List[NewsItem] = []
        for fetcher in self.fetchers:
            try:
                news = fetcher.fetch_latest(self.keywords, from_date)
                items.extend(news)
                logger.info("Fetched %d items from %s", len(news), fetcher.__class__.__name__)
            except Exception as exc:
                logger.exception("Fetcher failure (%s): %s", fetcher.__class__.__name__, exc)
        return items

    def process(self, items: List[NewsItem]) -> List[NewsItem]:
        recent_items = [item for item in items if item.published >= settings.from_date]
        filtered = KeywordFilter.filter_items(recent_items, self.keywords)
        deduped = Deduplicator.deduplicate(filtered)

        for item in deduped:
            text = f"{item.title}. {item.summary}"
            score, label = self.sentiment_processor.analyze(text)
            item.sentiment = score
            item.label = label
            item.entities = self.entity_processor.extract(text)
            item.topic = self.topic_classifier.classify(text)
        return deduped

    def run(self) -> int:
        logger.info("Pipeline started at %s", datetime.now(timezone.utc).isoformat())
        fetched = self.fetch_all()
        processed = self.process(fetched)
        db = Database()
        try:
            return db.save_news(processed)
        finally:
            db.close()


if __name__ == "__main__":
    saved = NewsPipeline().run()
    logger.info("Pipeline finished, saved=%d", saved)
