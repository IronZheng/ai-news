from __future__ import annotations

from fastapi import FastAPI, HTTPException, Query

from financial_news_engine.config import settings
from financial_news_engine.storage.db import Database

app = FastAPI(title="Financial News Intelligence API", version="1.0.0")


def get_db() -> Database:
    return Database()


@app.get("/news/latest")
def latest_news(limit: int = Query(default=100, ge=1, le=500)) -> dict:
    db = get_db()
    try:
        return {"items": db.latest(limit=limit)}
    finally:
        db.close()


@app.get("/news/search")
def search_news(keyword: str = Query(..., min_length=1), limit: int = Query(default=100, ge=1, le=500)) -> dict:
    db = get_db()
    try:
        return {"items": db.search(keyword=keyword, limit=limit)}
    finally:
        db.close()


@app.get("/news/sentiment")
def sentiment_by_ticker(ticker: str = Query(..., min_length=2, max_length=10)) -> dict:
    aliases = settings.ticker_map.get(ticker.upper())
    if not aliases:
        raise HTTPException(status_code=404, detail=f"Unknown ticker {ticker}")

    db = get_db()
    try:
        result = db.sentiment_for_ticker(aliases)
        result["ticker"] = ticker.upper()
        return result
    finally:
        db.close()
