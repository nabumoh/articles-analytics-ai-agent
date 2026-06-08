import re
from collections import Counter

STOP_WORDS = {
    "the", "and", "or", "to", "in", "on", "for", "of", "a", "an", "is", "are",
    "was", "were", "be", "been", "with", "as", "by", "that", "this", "it", "from",
    "at", "not", "about", "after", "before", "into", "over", "under", "more", "most",
    "new", "will", "can", "could", "should", "would", "their", "there", "than", "you",
    "your", "our", "we", "they", "he", "she", "his", "her", "them", "who", "what",
    "when", "where", "why", "how"
}


def normalize_text(text: str) -> list[str]:
    text = text.lower()
    text = re.sub(r"[^a-z\s]", " ", text)
    tokens = [token.strip() for token in text.split() if token.strip()]
    tokens = [token for token in tokens if token not in STOP_WORDS and len(token) > 2]
    return tokens


def top_keywords(texts: list[str], limit: int = 20) -> list[dict]:
    counter = Counter()
    for text in texts:
        counter.update(normalize_text(text))
    return [{"word": word, "count": count} for word, count in counter.most_common(limit)]
