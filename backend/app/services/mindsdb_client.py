import os
import re
import requests
from sqlalchemy import text
from sqlalchemy.orm import Session

MINDSDB_URL = os.getenv("MINDSDB_URL", "http://mindsdb:47334")


def _fallback_answer(question: str, db: Session) -> str:
    q = question.strip().lower()

    if ("how many" in q or "count" in q) and "this week" in q:
        row = db.execute(
            text(
                """
                SELECT COUNT(*)::int AS total
                FROM articles
                WHERE published_at >= NOW() - INTERVAL '7 days'
                """
            )
        ).mappings().first()
        total = int(row["total"]) if row else 0
        return f"{total} articles were published in the last 7 days."

    if "total articles" in q or "how many articles" in q:
        row = db.execute(text("SELECT COUNT(*)::int AS total FROM articles")).mappings().first()
        total = int(row["total"]) if row else 0
        return f"There are {total} articles in the dataset."

    if "most articles" in q or "top source" in q:
        row = db.execute(
            text(
                """
                SELECT source, COUNT(*)::int AS total
                FROM articles
                GROUP BY source
                ORDER BY total DESC
                LIMIT 1
                """
            )
        ).mappings().first()
        if row:
            return f"{row['source']} has the most articles ({row['total']})."

    from_match = re.search(r"from\s+([a-zA-Z0-9 _.-]+)\??$", question.strip(), flags=re.IGNORECASE)
    if from_match and ("how many" in q or "count" in q):
        source = from_match.group(1).strip()
        row = db.execute(
            text(
                """
                SELECT COUNT(*)::int AS total
                FROM articles
                WHERE LOWER(source) = LOWER(:source)
                """
            ),
            {"source": source},
        ).mappings().first()
        total = int(row["total"]) if row else 0
        return f"{total} articles are from {source}."

    return "I can answer analytics questions like: total articles, published this week, top source, or count by source."


def ask_question(question: str, db: Session | None = None) -> str:
    # MindsDB SQL API can be customized per deployment; this query is a practical default.
    sql = f"""
    SELECT answer
    FROM mindsdb.articles_qa_agent
    WHERE question = '{question.replace("'", "''")}'
    LIMIT 1
    """
    try:
        response = requests.post(
            f"{MINDSDB_URL}/api/sql/query",
            json={"query": sql},
            timeout=20,
        )
        response.raise_for_status()
        payload = response.json()
        if payload.get("type") == "error":
            raise RuntimeError(payload.get("error_message", "Unknown MindsDB error"))

        data = payload.get("data", [])
        if data and data[0].get("answer"):
            return str(data[0].get("answer"))

        if db is not None:
            return _fallback_answer(question, db)
        return "No answer returned by MindsDB agent."
    except Exception:
        if db is not None:
            return _fallback_answer(question, db)
        return "MindsDB is not reachable yet. Start containers and configure the agent in MindsDB Studio."
