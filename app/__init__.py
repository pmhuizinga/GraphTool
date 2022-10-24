# todo: add "ID already exists" warning
# todo: put db conn in config
# todo: add possibility to remove or modify an edge
# todo: add full dependencies as visual
# todo: switch graph view to community view (and back)
# todo: add 'api/' to api string
# todo: move all database actions to database_functions.py (not in views.py)
# todo: property 'type' is used for d3.js. This should be changed to node_type
# todo: add ability to use space in node type (by adding `` in the create and select statements)
# todo: use consistent naming for node_type and node_id
# todo: import js libraries (otherwise dependent on internet connection)
# todo: on start -> create database if not exists

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()
# todo: change graph to open file and load into networkx graph

# engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

# sqlite init to app
# db = SQLAlchemy()

def create_app(config_name='default'):
    app = Flask(__name__)

    app.config.from_object(config[config_name])

    db.init_app(app)

    from .home import home as home_blueprint

    app.register_blueprint(home_blueprint, url_prefix="/")

    # db = SQLAlchemy(app)

    return app

