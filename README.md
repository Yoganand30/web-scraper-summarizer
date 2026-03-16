# Web Scraper Summarizer

A Flask microservice that scrapes web pages, summarizes content using extractive summarization (Sumy/LSA), and stores results in PostgreSQL.

## Features

- POST `/summaries` : scrape given URL, summarize text, and persist in DB
- GET `/summaries` : list all saved summaries
- GET `/summaries/<id>` : get a single summary by ID
- PUT `/summaries/<id>` : re-scrape URL and update summary
- DELETE `/summaries/<id>` : delete summary record

## Project structure

- `app/main.py` : Flask app factory
- `app/routes.py` : API endpoints
- `app/scraper.py` : website scraping logic (BeautifulSoup)
- `app/summarizer.py` : summarization (Sumy LSA)
- `app/models.py` : SQLAlchemy model for `Summary`
- `app/database.py` : SQLAlchemy instance

## Requirements

- Python 3.11+ (or 3.10+)
- PostgreSQL (via Docker in compose)

Dependencies (from `requirements.txt`):
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- psycopg2-binary
- requests
- beautifulsoup4
- sumy
- python-dotenv
- gunicorn
- numpy

## Setup (Docker)

1. Build images:

```bash
make build
```

2. Start services:

```bash
make up
```

3. Stop services:

```bash
make down
```

4. View logs:

```bash
make logs
```

API server runs on `http://localhost:5000`.

## Database migrations

If you add/modify models, run migrations in container or local env:

```bash
docker compose run --rm app flask db init   # only once
docker compose run --rm app flask db migrate -m "Add summary model"
docker compose run --rm app flask db upgrade
```

> NOTE: `DATABASE_URL` is already configured in `docker-compose.yml` as `postgresql://postgres:postgres@db:5432/scraperdb`.

## Usage examples

### Create summary

```bash
curl -X POST http://localhost:5000/summaries \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

### List summaries

```bash
curl http://localhost:5000/summaries
```

### Get summary by ID

```bash
curl http://localhost:5000/summaries/1
```

### Update summary

```bash
curl -X PUT http://localhost:5000/summaries/1 \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

### Delete summary

```bash
curl -X DELETE http://localhost:5000/summaries/1
```

## Notes

- Scraper extracts text from `<p>` tags only.
- Summarizer returns top 3 sentences (LSA).
- No authentication currently.
- Error responses for invalid URL / missing record.
