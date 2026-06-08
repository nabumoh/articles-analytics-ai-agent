# Loom Demo Script (2-4 minutes)

## 1) Intro (20-30 sec)
Hello, this is my assignment project: an Articles Analytics System with AI support.
The pipeline is CSV ingestion into PostgreSQL, analytics APIs with FastAPI, a React dashboard, and MindsDB Agent for natural-language questions.
Everything runs in Docker Compose.

## 2) Architecture (25-35 sec)
I have four services:
1. Postgres database stores cleaned article records.
2. Backend service loads CSV and exposes metrics endpoints.
3. Frontend service shows interactive charts and tag cloud.
4. MindsDB service provides AI question-answering over the dataset.

## 3) Run and Verify (30-40 sec)
I run:
- cp .env.example .env
- docker compose up --build

Then I open:
- Dashboard on localhost:8080
- Backend health on localhost:8000/health
- MindsDB on localhost:47334

## 4) Dashboard Walkthrough (50-70 sec)
In the dashboard, I show:
1. KPI tiles: total articles, total sources, total categories, average reading time.
2. Articles per day trend line.
3. Articles by source bar chart.
4. Category distribution pie chart.
5. Language distribution bar chart.
6. Average reading time by source.
7. Weekday distribution trend.
8. Long-read vs short-read ratio.
9. Tag cloud generated from cleaned text.

## 5) NLP and Tag Cloud (20-30 sec)
My text processing includes lowercasing, punctuation removal, stop words filtering, and word frequency counting.
The output drives the tag cloud and top keyword insights.

## 6) MindsDB Agent Demo (40-60 sec)
I ask a few sample questions:
- How many articles were published this week?
- Which source published the most articles?
- What are the main recurring topics?
- Which category has the fewest articles?

The backend forwards the question to the MindsDB Agent and returns the answer to the dashboard.

## 7) Closing (10-15 sec)
This project demonstrates full-stack data analytics with AI integration, containerized deployment, and clear documentation for reproducibility.
