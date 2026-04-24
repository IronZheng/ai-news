from __future__ import annotations

from typing import Tuple

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class SentimentProcessor:
    def __init__(self) -> None:
        self.analyzer = SentimentIntensityAnalyzer()

    def analyze(self, text: str) -> Tuple[float, str]:
        score = self.analyzer.polarity_scores(text).get("compound", 0.0)
        if score >= 0.15:
            label = "Bullish"
        elif score <= -0.15:
            label = "Bearish"
        else:
            label = "Neutral"
        return score, label
