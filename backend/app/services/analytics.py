from sqlalchemy import text
from sqlalchemy.orm import Session


def query_rows(db: Session, sql: str) -> list[dict]:
    rows = db.execute(text(sql)).mappings().all()
    return [dict(row) for row in rows]


def articles_by_day(db: Session) -> list[dict]:
    return query_rows(
        db,
        """
        SELECT DATE(published_at) AS day, COUNT(*)::int AS total
        FROM articles
        GROUP BY day
        ORDER BY day
        """,
    )


def articles_by_source(db: Session) -> list[dict]:
    return query_rows(
        db,
        """
        SELECT source, COUNT(*)::int AS total
        FROM articles
        GROUP BY source
        ORDER BY total DESC
        """,
    )


def articles_by_category(db: Session) -> list[dict]:
    return query_rows(
        db,
        """
        SELECT category, COUNT(*)::int AS total
        FROM articles
        GROUP BY category
        ORDER BY total DESC
        """,
    )


def articles_by_language(db: Session) -> list[dict]:
    return query_rows(
        db,
        """
        SELECT language, COUNT(*)::int AS total
        FROM articles
        GROUP BY language
        ORDER BY total DESC
        """,
    )


def average_reading_time(db: Session) -> list[dict]:
    return query_rows(
        db,
        """
        SELECT source, ROUND(AVG(reading_time_minutes)::numeric, 2) AS average_minutes
        FROM articles
        GROUP BY source
        ORDER BY average_minutes DESC
        """,
    )
