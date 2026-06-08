from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .models import Article
from .services import analytics, text_processing, mindsdb_client

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Articles Analytics API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QuestionRequest(BaseModel):
    question: str


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/api/metrics/articles-by-day")
def get_articles_by_day(db: Session = Depends(get_db)) -> list[dict]:
    return analytics.articles_by_day(db)


@app.get("/api/metrics/articles-by-source")
def get_articles_by_source(db: Session = Depends(get_db)) -> list[dict]:
    return analytics.articles_by_source(db)


@app.get("/api/metrics/articles-by-category")
def get_articles_by_category(db: Session = Depends(get_db)) -> list[dict]:
    return analytics.articles_by_category(db)


@app.get("/api/metrics/articles-by-language")
def get_articles_by_language(db: Session = Depends(get_db)) -> list[dict]:
    return analytics.articles_by_language(db)


@app.get("/api/metrics/avg-reading-time")
def get_avg_reading_time(db: Session = Depends(get_db)) -> list[dict]:
    return analytics.average_reading_time(db)


@app.get("/api/metrics/weekday-distribution")
def get_weekday_distribution(db: Session = Depends(get_db)) -> list[dict]:
    return analytics.weekday_distribution(db)


@app.get("/api/metrics/long-read-ratio")
def get_long_read_ratio(db: Session = Depends(get_db)) -> list[dict]:
    return analytics.long_read_ratio(db)


@app.get("/api/metrics/summary")
def get_summary(db: Session = Depends(get_db)) -> dict:
    return analytics.summary_kpis(db)


@app.get("/api/metrics/top-keywords")
def get_top_keywords(db: Session = Depends(get_db)) -> list[dict]:
    texts = [row[0] for row in db.query(Article.content).all()]
    return text_processing.top_keywords(texts, limit=25)


@app.get("/api/metrics/tag-cloud")
def get_tag_cloud(db: Session = Depends(get_db)) -> list[dict]:
    texts = [row[0] for row in db.query(Article.content).all()]
    return text_processing.top_keywords(texts, limit=60)


@app.post("/api/ai/ask")
def ask_ai(request: QuestionRequest) -> dict:
    answer = mindsdb_client.ask_question(request.question)
    return {"question": request.question, "answer": answer}
