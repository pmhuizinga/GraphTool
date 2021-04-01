from flask import Flask
from config import config
import pymongo

# todo: put db conn in config
# todo: add color code to nodes in graph
# todo: create blank db as an option
# todo: select db as an option
# todo: add function to merge tables
# todo: add function to rename table name
# todo: avoid adding duplicate relations
# todo: add view on a single node (view all relations)
# todo: remove unrelated nodes
# todo: enlarge graphics on graph
# todo: write data to neo4j
# todo: add default 'geldigheid' to edges

conn = pymongo.MongoClient("mongodb://localhost:27017/")
db = conn['paul_db']
# db = conn['testdb']

def create_app(config_name='default'):
    app = Flask(__name__)

    from .home import home as home_blueprint

    app.register_blueprint(home_blueprint, url_prefix="/")

    return app
