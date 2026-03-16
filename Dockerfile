FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Install NLTK tokenizer data
RUN python -m nltk.downloader punkt
RUN python -m nltk.downloader punkt_tab

COPY . .

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app.main:app"]