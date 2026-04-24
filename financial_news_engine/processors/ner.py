from __future__ import annotations

from typing import List, Set

import spacy


class EntityProcessor:
    companies = {"Tesla", "Amazon", "Nvidia", "Apple"}
    commodities = {"Gold", "Oil", "Crude", "Brent", "WTI"}
    currencies = {"USD", "US dollar", "Dollar", "Euro", "Yen"}

    def __init__(self) -> None:
        self.nlp = spacy.load("en_core_web_sm")

    def extract(self, text: str) -> List[str]:
        doc = self.nlp(text)
        entities: Set[str] = set()
        for ent in doc.ents:
            token = ent.text.strip()
            if ent.label_ in {"ORG", "PRODUCT"} and token in self.companies:
                entities.add(token)
            if token in self.commodities:
                entities.add(token)
            if token in self.currencies:
                entities.add(token)
        return sorted(entities)
