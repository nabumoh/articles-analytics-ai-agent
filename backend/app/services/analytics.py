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


def weekday_distribution(db: Session) -> list[dict]:
    return query_rows(
        db,
        """
        SELECT
            TO_CHAR(published_at, 'Dy') AS weekday,
            EXTRACT(ISODOW FROM published_at)::int AS weekday_order,
            COUNT(*)::int AS total
        FROM articles
        GROUP BY weekday, weekday_order
        ORDER BY weekday_order
        """,
    )


def long_read_ratio(db: Session, threshold: int = 6) -> list[dict]:
    return query_rows(
        db,
        f"""
        SELECT
            CASE WHEN reading_time_minutes >= {threshold} THEN 'Long Reads' ELSE 'Short Reads' END AS bucket,
            COUNT(*)::int AS total
        FROM articles
        GROUP BY bucket
        ORDER BY total DESC
        """,
    )


def summary_kpis(db: Session) -> dict:
    rows = query_rows(
        db,
        """
        SELECT
            COUNT(*)::int AS total_articles,
            COUNT(DISTINCT source)::int AS total_sources,
            COUNT(DISTINCT category)::int AS total_categories,
            ROUND(AVG(reading_time_minutes)::numeric, 2) AS avg_read_minutes,
            MIN(DATE(published_at)) AS first_day,
            MAX(DATE(published_at)) AS last_day
        FROM articles
        """,
    )
    return rows[0] if rows else {
        "total_articles": 0,
        "total_sources": 0,
        "total_categories": 0,
        "avg_read_minutes": 0,
        "first_day": None,
        "last_day": None,
    }
