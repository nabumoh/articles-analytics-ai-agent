import os
from datetime import datetime
import pandas as pd

from app.database import SessionLocal, Base, engine
from app.models import Article

CSV_PATH = os.getenv("CSV_PATH", "/app/data/articles_sample.csv")


def parse_datetime(value: str) -> datetime:
    return datetime.fromisoformat(str(value).replace("Z", "+00:00"))


def run() -> None:
    Base.metadata.create_all(bind=engine)
    if not os.path.exists(CSV_PATH):
        print(f"CSV file not found at {CSV_PATH}, skipping seed.")
        return

    df = pd.read_csv(CSV_PATH)
    required_cols = {
        "title", "source", "category", "language", "published_at", "reading_time_minutes", "url", "content"
    }
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Missing required CSV columns: {sorted(missing)}")

    db = SessionLocal()
    inserted = 0
    try:
        for _, row in df.iterrows():
            existing = db.query(Article).filter(Article.url == str(row["url"])).first()
            if existing:
                continue

            article = Article(
                title=str(row["title"]),
                source=str(row["source"]),
                category=str(row["category"]),
                language=str(row["language"]),
                published_at=parse_datetime(str(row["published_at"])),
                reading_time_minutes=int(row["reading_time_minutes"]),
                url=str(row["url"]),
                content=str(row["content"]),
            )
            db.add(article)
            inserted += 1

        db.commit()
        print(f"Inserted {inserted} articles.")
    finally:
        db.close()


if __name__ == "__main__":
    run()
