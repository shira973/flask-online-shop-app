from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(config_class=None):
    app = Flask(__name__)

    if config_class is None:
        from .config import DevelopmentConfig
        config_class = DevelopmentConfig

    app.config.from_object(config_class)

    db.init_app(app)

    from app.seller import seller_bp
    from app.customer import customer_bp

    app.register_blueprint(seller_bp)
    app.register_blueprint(customer_bp)

    with app.app_context():
        from . import models  # noqa: F401
        db.create_all()

    return app