from flask import Flask
from flask_migrate import Migrate
from .database import db
from .routes import routes

def create_app():

    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres@db:5432/scraperdb"

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    migrate = Migrate(app, db)

    app.register_blueprint(routes)

    return app

app = create_app()