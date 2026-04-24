from __future__ import annotations

import os

from dotenv import load_dotenv

load_dotenv("config.env", override=False)
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Dict, List


@dataclass(slots=True)
class Settings:
    newsapi_key: str = field(default_factory=lambda: os.getenv("NEWSAPI_KEY", ""))
    finnhub_key: str = field(default_factory=lambda: os.getenv("FINNHUB_KEY", ""))
    postgres_host: str = field(default_factory=lambda: os.getenv("POSTGRES_HOST", "localhost"))
    postgres_port: int = field(default_factory=lambda: int(os.getenv("POSTGRES_PORT", "5432")))
    postgres_db: str = field(default_factory=lambda: os.getenv("POSTGRES_DB", "financial_news"))
    postgres_user: str = field(default_factory=lambda: os.getenv("POSTGRES_USER", "postgres"))
    postgres_password: str = field(default_factory=lambda: os.getenv("POSTGRES_PASSWORD", "postgres"))
    fetch_lookback_days: int = field(default_factory=lambda: int(os.getenv("LOOKBACK_DAYS", "7")))
    scheduler_hours: int = field(default_factory=lambda: int(os.getenv("SCHEDULER_HOURS", "2")))
    log_level: str = field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))

    @property
    def from_date(self) -> datetime:
        return datetime.now(timezone.utc) - timedelta(days=self.fetch_lookback_days)

    @property
    def tracked_keywords(self) -> List[str]:
        return [
            "Tesla",
            "Amazon",
            "Nvidia",
            "Apple",
            "Gold",
            "Oil",
            "USD",
            "Federal Reserve",
            "Inflation",
        ]

    @property
    def ticker_map(self) -> Dict[str, List[str]]:
        return {
            "TSLA": ["Tesla", "TSLA"],
            "AMZN": ["Amazon", "AMZN"],
            "NVDA": ["Nvidia", "NVDA"],
            "AAPL": ["Apple", "AAPL"],
            "XAU": ["Gold", "XAU", "bullion"],
            "OIL": ["Oil", "crude", "WTI", "Brent"],
            "USD": ["USD", "US dollar", "dollar index", "DXY"],
            "FED": ["Federal Reserve", "Fed", "FOMC"],
        }


settings = Settings()
