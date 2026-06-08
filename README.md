# Articles Analytics AI Agent

End-to-end university project for article analytics and AI Q&A:
- CSV ingestion into PostgreSQL
- FastAPI backend analytics APIs
- React dashboard with 5+ insights and tag cloud
- MindsDB Agent integration for natural-language questions
- Full Docker Compose setup

## Project Structure

```text
.
|-- backend
|   |-- app
|   |   |-- main.py
|   |   |-- database.py
|   |   |-- models.py
|   |   `-- services
|   |       |-- analytics.py
|   |       |-- mindsdb_client.py
|   |       `-- text_processing.py
|   |-- data
|   |   `-- articles_sample.csv
|   |-- scripts
|   |   |-- load_csv.py
|   |   `-- start.sh
|   |-- Dockerfile
|   `-- requirements.txt
|-- frontend
|   |-- src
|   |   |-- components
|   |   |   `-- ChartCard.jsx
|   |   |-- api.js
|   |   |-- App.jsx
|   |   |-- main.jsx
|   |   `-- styles.css
|   |-- Dockerfile
|   |-- nginx.conf
|   `-- package.json
|-- mindsdb
|   `-- setup_guide.sql
|-- docker-compose.yml
`-- .env.example
```

## Features Implemented

Dashboard insights:
1. Articles per day
2. Articles per source
3. Articles per category
4. Articles per language
5. Average reading time by source
6. Weekday publication distribution
7. Long-read vs short-read ratio
8. KPI summary tiles
9. Tag cloud from cleaned article text

Text processing pipeline:
- lowercasing
- punctuation removal
- stop words removal
- token frequency counting

AI integration:
- POST endpoint to ask MindsDB Agent questions about the dataset

## Run With Docker

1. Copy env file:

```bash
cp .env.example .env
```

2. Start all services:

```bash
docker compose up --build
```

3. Open apps:
- Dashboard: http://localhost:8080
- Backend health: http://localhost:8000/health
- MindsDB Studio/API: http://localhost:47334

## MindsDB Agent Setup

After containers are running:

1. Open MindsDB SQL Editor.
2. Run commands from `mindsdb/setup_guide.sql`.
3. Ensure agent name is `articles_qa_agent`.

If your MindsDB version has different `CREATE AGENT` syntax, use Studio Agent Builder and keep the same agent name.

## Example Questions for Agent

- How many articles were published this week?
- Which source published the most articles?
- What are the top recurring topics?
- Are technology articles increasing over time?
- Which categories have the fewest articles?

## API Endpoints

- `GET /health`
- `GET /api/metrics/articles-by-day`
- `GET /api/metrics/articles-by-source`
- `GET /api/metrics/articles-by-category`
- `GET /api/metrics/articles-by-language`
- `GET /api/metrics/avg-reading-time`
- `GET /api/metrics/weekday-distribution`
- `GET /api/metrics/long-read-ratio`
- `GET /api/metrics/summary`
- `GET /api/metrics/top-keywords`
- `GET /api/metrics/tag-cloud`
- `POST /api/ai/ask`

Sample body for AI ask:

```json
{
	"question": "How many articles are from TechDaily?"
}
```

## Notes

- Sample CSV is included in `backend/data/articles_sample.csv`.
- On backend startup, CSV records are inserted once using URL as unique key.
- You can replace sample CSV with your real dataset even if headers differ.

### CSV Mapping For Real Datasets

The loader auto-detects common aliases for these canonical fields:
- title
- source
- category
- language
- published_at
- reading_time_minutes
- url
- content

If your column names still differ, set overrides in `.env`:

```bash
CSV_COL_TITLE=headline
CSV_COL_SOURCE=publisher
CSV_COL_CATEGORY=topic
CSV_COL_LANGUAGE=lang
CSV_COL_PUBLISHED_AT=publish_date
CSV_COL_READING_TIME_MINUTES=read_time
CSV_COL_URL=link
CSV_COL_CONTENT=body
```

### Loom Video Script

Use `docs/loom_script.md` for a ready 2-4 minute demo narration.