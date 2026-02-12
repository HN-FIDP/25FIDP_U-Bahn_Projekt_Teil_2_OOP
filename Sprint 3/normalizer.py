import re
from difflib import SequenceMatcher
from typing import List

class InputNormalizer:
    UMLAUTS = {"ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss"}

    ABBREVIATIONS = {
        r"\bhbf\.?\b": "hauptbahnhof",
        r"\bstr\.?\b": "strasse",
        r"\bfr\.\-?\b": "friedrich"
    }

    @classmethod
    def normalize(cls, text: str) -> str:
        text = text.strip().lower().replace("-", " ")
        for k, v in cls.UMLAUTS.items():
            text = text.replace(k, v)
        for pattern, replacement in cls.ABBREVIATIONS.items():
            text = re.sub(pattern, replacement, text)
        return re.sub(r"\s+", " ", text)


class FuzzyMatcher:
    @staticmethod
    def similarity(a: str, b: str) -> float:
        return SequenceMatcher(None, a, b).ratio()


class HaltestellenFinder:
    def __init__(self, haltestellen: List[str]) -> None:
        self.haltestellen = haltestellen

    def finde(self, user_input: str) -> str | None:
        user_norm = InputNormalizer.normalize(user_input)
        kandidaten = []
        for name in self.haltestellen:
            score = FuzzyMatcher.similarity(user_norm, InputNormalizer.normalize(name))
            if score >= 0.8:
                kandidaten.append((name, score))
        if not kandidaten:
            print("❌ Haltestelle nicht gefunden.")
            return None
        kandidaten.sort(key=lambda x: x[1], reverse=True)
        return kandidaten[0][0]
