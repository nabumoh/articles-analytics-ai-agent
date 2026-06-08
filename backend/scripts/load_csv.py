import os
from datetime import datetime
import pandas as pd

from app.database import SessionLocal, Base, engine
from app.models import Article

CSV_PATH = os.getenv("CSV_PATH", "/app/data/articles_sample.csv")

CANONICAL_TO_ALIASES = {
    "title": ["title", "headline", "article_title"],
    "source": ["source", "publisher", "site", "news_source"],
    "category": ["category", "topic", "section", "genre"],
    "language": ["language", "lang", "locale"],
    "published_at": ["published_at", "published", "publish_date", "date", "datetime"],
    "reading_time_minutes": ["reading_time_minutes", "reading_time", "read_time", "minutes"],
    "url": ["url", "link", "article_url"],
    "content": ["content", "body", "text", "article_text"],
}


def build_column_mapping(df_columns: list[str]) -> dict[str, str]:
    mapping: dict[str, str] = {}
    lowered = {col.lower(): col for col in df_columns}

    for canonical, aliases in CANONICAL_TO_ALIASES.items():
        env_override = os.getenv(f"CSV_COL_{canonical.upper()}")
        if env_override and env_override in df_columns:
            mapping[canonical] = env_override
            continue

        for alias in aliases:
            if alias in lowered:
                mapping[canonical] = lowered[alias]
                break

    return mapping


def parse_datetime(value: str) -> datetime:
    raw = str(value).strip()
    try:
        return datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        parsed = pd.to_datetime(raw, utc=True, errors="coerce")
        if pd.isna(parsed):
            raise ValueError(f"Invalid datetime value: {value}")
        return parsed.to_pydatetime()


def parse_int(value: object, default_value: int = 5) -> int:
    try:
        return int(float(value))
    except (ValueError, TypeError):
        return default_value


def run() -> None:
    Base.metadata.create_all(bind=engine)
    if not os.path.exists(CSV_PATH):
        print(f"CSV file not found at {CSV_PATH}, skipping seed.")
        return

    df = pd.read_csv(CSV_PATH)
    mapping = build_column_mapping(list(df.columns))
    required_cols = set(CANONICAL_TO_ALIASES.keys())
    missing = required_cols - set(mapping.keys())
    if missing:
        raise ValueError(
            "Missing required canonical CSV fields: "
            f"{sorted(missing)}. "
            "Use expected aliases or set CSV_COL_<FIELD> env vars."
        )

    print(f"CSV column mapping: {mapping}")

    db = SessionLocal()
    inserted = 0
    try:
        for _, row in df.iterrows():
            url = str(row[mapping["url"]]).strip()
            existing = db.query(Article).filter(Article.url == url).first()
            if existing:
                continue

            article = Article(
                title=str(row[mapping["title"]]).strip(),
                source=str(row[mapping["source"]]).strip(),
                category=str(row[mapping["category"]]).strip(),
                language=str(row[mapping["language"]]).strip(),
                published_at=parse_datetime(str(row[mapping["published_at"]])),
                reading_time_minutes=parse_int(row[mapping["reading_time_minutes"]]),
                url=url,
                content=str(row[mapping["content"]]).strip(),
            )
            db.add(article)
            inserted += 1

        db.commit()
        print(f"Inserted {inserted} articles.")
    finally:
        db.close()


if __name__ == "__main__":
    run()
