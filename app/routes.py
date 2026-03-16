from flask import Blueprint, request, jsonify
from .scraper import scrape_website
from .summarizer import summarize_text
from .models import Summary
from .database import db

routes = Blueprint("routes", __name__)

@routes.route("/summaries", methods=["POST"])
def create_summary():

    data = request.json

    url = data.get("url")

    text = scrape_website(url)

    if not text:
        return jsonify({"error": "Failed to scrape website"}), 400

    summary = summarize_text(text)

    record = Summary(url=url, content=text, summary=summary)

    db.session.add(record)

    db.session.commit()

    return jsonify({"message": "Summary created"})


@routes.route("/summaries", methods=["GET"])
def get_summaries():

    records = Summary.query.all()

    result = []

    for r in records:

        result.append({
            "id": r.id,
            "url": r.url,
            "summary": r.summary
        })

    return jsonify(result)