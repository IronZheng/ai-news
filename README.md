# Financial News Intelligence System

Production-grade Python 3.11 system for ingesting, enriching, storing, and serving financial news across multi-source APIs and RSS feeds.

## Features

- Multi-source ingestion:
  - Primary: NewsAPI, Finnhub, GDELT API
  - Secondary: Reuters RSS, Yahoo Finance RSS, Investing.com RSS
- Keywords tracked:
  - Tesla, Amazon, Nvidia, Apple, Gold, Oil, USD, Federal Reserve, Inflation
- Processing pipeline:
  - Last 7 days filtering
  - Deduplication using `hash(title + url)` semantics (SHA-256)
  - VADER sentiment (`-1..1`, label: Bullish/Bearish/Neutral)
  - spaCy entity extraction (companies/commodities/currencies)
  - Topic classification (Macro, Company, Commodity, Policy, Technology)
- PostgreSQL persistence
- APScheduler every 2 hours
- FastAPI endpoints for latest/search/sentiment
- Dockerized app + PostgreSQL via `docker-compose`

## Project Structure

```text
financial_news_engine/
  config.py
  schemas.py
  fetchers/
    common.py
    newsapi.py
    finnhub.py
    gdelt.py
    rss.py
  processors/
    keyword_filter.py
    dedup.py
    sentiment.py
    ner.py
    topic_classifier.py
  storage/
    db.py
  api/
    server.py
  scheduler/
    runner.py
  migrations/
    001_create_news.sql
main.py
requirements.txt
Dockerfile
docker-compose.yml
config.env.example
```

## Setup

1. Create environment file:

```bash
cp config.env.example config.env
```

2. Fill API keys in `config.env`:

```env
NEWSAPI_KEY=your_newsapi_key
FINNHUB_KEY=your_finnhub_key
```

3. Install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

4. Start PostgreSQL + app:

```bash
docker compose up --build
```

## Run Modes

### Run one-shot pipeline

```bash
python main.py pipeline
```

### Run scheduler (every 2 hours)

```bash
python main.py scheduler
```

### Run API server

```bash
python main.py api
```

## API Usage

### Get latest news

```bash
curl "http://localhost:8000/news/latest"
```

### Search by keyword

```bash
curl "http://localhost:8000/news/search?keyword=Tesla"
```

### Sentiment by ticker alias set

```bash
curl "http://localhost:8000/news/sentiment?ticker=TSLA"
```

## SQL Migration

Initial migration file:

- `financial_news_engine/migrations/001_create_news.sql`

Applied automatically by PostgreSQL container on first startup.

## Logging

The system logs:

- fetch errors
- API failures
- duplicates removed
- records saved

Configure log level through:

```env
LOG_LEVEL=INFO
```
