from __future__ import annotations

import logging
from typing import Iterable, List

import psycopg2
from psycopg2.extras import execute_batch

from financial_news_engine.config import settings
from financial_news_engine.schemas import NewsItem

logger = logging.getLogger(__name__)


class Database:
    def __init__(self) -> None:
        self.conn = psycopg2.connect(
            host=settings.postgres_host,
            port=settings.postgres_port,
            dbname=settings.postgres_db,
            user=settings.postgres_user,
            password=settings.postgres_password,
        )
        self.conn.autocommit = True

    def close(self) -> None:
        self.conn.close()

    def save_news(self, items: Iterable[NewsItem]) -> int:
        records = [
            (
                item.title,
                item.summary,
                item.url,
                item.source,
                item.published,
                item.sentiment,
                item.label,
                item.entities or [],
                item.topic,
            )
            for item in items
        ]
        if not records:
            return 0

        query = """
        INSERT INTO news (title, summary, url, source, published, sentiment, label, entities, topic)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT (url) DO NOTHING
        """
        with self.conn.cursor() as cur:
            execute_batch(cur, query, records, page_size=100)
            inserted = cur.rowcount if cur.rowcount is not None else 0
        logger.info("Records saved: %d", inserted)
        return inserted

    def latest(self, limit: int = 100) -> List[dict]:
        query = """
        SELECT title, summary, url, source, published, sentiment, label, entities, topic
        FROM news
        ORDER BY published DESC
        LIMIT %s
        """
        with self.conn.cursor() as cur:
            cur.execute(query, (limit,))
            rows = cur.fetchall()
        return [
            {
                "title": row[0],
                "summary": row[1],
                "url": row[2],
                "source": row[3],
                "published": row[4].isoformat(),
                "sentiment": row[5],
                "label": row[6],
                "entities": row[7],
                "topic": row[8],
            }
            for row in rows
        ]

    def search(self, keyword: str, limit: int = 100) -> List[dict]:
        query = """
        SELECT title, summary, url, source, published, sentiment, label, entities, topic
        FROM news
        WHERE title ILIKE %s OR summary ILIKE %s
        ORDER BY published DESC
        LIMIT %s
        """
        like = f"%{keyword}%"
        with self.conn.cursor() as cur:
            cur.execute(query, (like, like, limit))
            rows = cur.fetchall()
        return [
            {
                "title": row[0],
                "summary": row[1],
                "url": row[2],
                "source": row[3],
                "published": row[4].isoformat(),
                "sentiment": row[5],
                "label": row[6],
                "entities": row[7],
                "topic": row[8],
            }
            for row in rows
        ]

    def sentiment_for_ticker(self, aliases: list[str]) -> dict:
        conditions = " OR ".join(["title ILIKE %s", "summary ILIKE %s"] * len(aliases))
        params: list[str] = []
        for alias in aliases:
            like = f"%{alias}%"
            params.extend([like, like])
        query = f"""
        SELECT COALESCE(AVG(sentiment), 0), COUNT(*)
        FROM news
        WHERE {conditions}
        """
        with self.conn.cursor() as cur:
            cur.execute(query, params)
            avg_score, count = cur.fetchone()
        return {"average_sentiment": float(avg_score), "article_count": count}
