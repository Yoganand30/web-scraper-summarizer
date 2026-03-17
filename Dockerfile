# BUILD STAGE 
FROM python:3.11-slim AS builder

WORKDIR /install

COPY requirements.txt .

RUN pip install --prefix=/install --no-cache-dir -r requirements.txt


# RUN STAGE
FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /install /usr/local

COPY . .

RUN python -m nltk.downloader punkt punkt_tab

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app.main:app"]