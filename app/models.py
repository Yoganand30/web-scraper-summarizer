from .database import db
from datetime import datetime

class Summary(db.Model):

    __tablename__ = "summaries"

    id = db.Column(db.Integer, primary_key=True)

    url = db.Column(db.String, nullable=False)

    content = db.Column(db.Text)

    summary = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)