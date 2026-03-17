from flask import Blueprint, request, jsonify
from .scraper import scrape_website
from .summarizer import summarize_text
from .models import Summary
from .database import db

routes = Blueprint("routes", __name__)

@routes.route("/")
def home():
    return {
        "message": "Web Scraper Summarizer API 🚀",
        "endpoints": [
            "GET /summaries",
            "POST /summaries",
            "GET /summaries/<id>",
            "PUT /summaries/<id>",
            "DELETE /summaries/<id>"
        ]
    }

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
@routes.route("/summaries/<int:id>", methods=["GET"])
def get_summary(id):

    record = Summary.query.get(id)

    if not record:
        return jsonify({"error": "Summary not found"}), 404

    return jsonify({
        "id": record.id,
        "url": record.url,
        "summary": record.summary
    })
@routes.route("/summaries/<int:id>", methods=["PUT"])
def update_summary(id):

    record = Summary.query.get(id)

    if not record:
        return jsonify({"error": "Summary not found"}), 404

    data = request.json
    new_url = data.get("url")

    text = scrape_website(new_url)
    summary = summarize_text(text)

    record.url = new_url
    record.content = text
    record.summary = summary

    db.session.commit()

    return jsonify({"message": "Summary updated"})
@routes.route("/summaries/<int:id>", methods=["DELETE"])
def delete_summary(id):

    record = Summary.query.get(id)

    if not record:
        return jsonify({"error": "Summary not found"}), 404

    db.session.delete(record)
    db.session.commit()

    return jsonify({"message": "Summary deleted"})