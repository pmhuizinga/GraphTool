# todo: add "ID already exists" warning
# todo: merge epic and project to project, include type 'epic'
# todo: put db conn in config
# todo: add function to merge tables
# todo: add function to rename table name
# todo: add possibility to remove or modify an edge
# todo: add full dependencies as visual
# todo: switch graph view to community view (and back)
# todo: learn BERT for NLP
# todo: add 'api/' to api string
# todo: move all database actions to database_functions.py (not in views.py)
# todo: make new api for all nodes/edges including properties
# todo: property 'type' is used for d3.js. This should be changed to node_type
# todo: add ability to use space in node type (by adding `` in the create and select statements)
# todo: update merge function to neo4j

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()
# todo: change graph to open file and load into networkx graph

def create_app(config_name='default'):
    app = Flask(__name__)

    app.config.from_object(config[config_name])

    db.init_app(app)

    from .home import home as home_blueprint

    app.register_blueprint(home_blueprint, url_prefix="/")

    return app

