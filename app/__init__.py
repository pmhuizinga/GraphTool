from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()
# engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
# db = SQLAlchemy()

def create_app(config_name='default'):
    app = Flask(__name__)

    app.config.from_object(config[config_name])

    db.init_app(app)

    from .home import home as home_blueprint

    app.register_blueprint(home_blueprint, url_prefix="/")

    # db = SQLAlchemy(app)

    return app

