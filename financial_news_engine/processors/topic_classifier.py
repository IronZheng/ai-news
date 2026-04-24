from __future__ import annotations

from typing import Dict, List


class TopicClassifier:
    topic_keywords: Dict[str, List[str]] = {
        "Macro": ["inflation", "gdp", "economy", "recession", "employment"],
        "Company": ["tesla", "amazon", "nvidia", "apple", "earnings", "shares"],
        "Commodity": ["gold", "oil", "wti", "brent", "commodities"],
        "Policy": ["federal reserve", "fed", "fomc", "rates", "policy"],
        "Technology": ["ai", "chip", "semiconductor", "technology", "cloud"],
    }

    def classify(self, text: str) -> str:
        lowered = text.lower()
        for topic, words in self.topic_keywords.items():
            if any(word in lowered for word in words):
                return topic
        return "Macro"
