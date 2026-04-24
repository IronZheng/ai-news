from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass(slots=True)
class NewsItem:
    title: str
    summary: str
    url: str
    published: datetime
    source: str
    sentiment: float | None = None
    label: str | None = None
    entities: List[str] | None = None
    topic: str | None = None
