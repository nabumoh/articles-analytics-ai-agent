import os
import requests

MINDSDB_URL = os.getenv("MINDSDB_URL", "http://mindsdb:47334")


def ask_question(question: str) -> str:
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
        data = payload.get("data", [])
        if data:
            return str(data[0].get("answer", "No answer returned by agent."))
        return "No answer returned by MindsDB agent."
    except Exception:
        return "MindsDB is not reachable yet. Start containers and configure the agent in MindsDB Studio."
