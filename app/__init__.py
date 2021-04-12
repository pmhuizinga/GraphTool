from flask import Flask
from config import config
import pymongo

# todo: rebase to objectID
# todo: fix input error
# todo: put db conn in config
# todo: create blank db as an option
# todo: select db as an option
# todo: backup database
# todo: add function to merge tables
# todo: add function to rename table name
# todo: add default 'geldigheid' to edges
# todo: remove unrelated nodes
# todo: auto 'close' relations when a node is 'closed' (with dates).
# todo: add possibility to remove an edge
# todo: add selection to graph (show what has been selected)
# done: add warning before removal and merge
# done: add option to merge 2 nodes into 1.
# done: add function to change a node id (also in all edges)
# done: add legend to graph viz
# done: visualize per edge type (show all datafeeds)
# done: enlarge graphics on graph
# done: add color code to nodes in graph
# done: avoid adding duplicate edges
# done: add view on a single node (view all nodes relations)

conn = pymongo.MongoClient("mongodb://localhost:27017/")
# db = conn['paul_db']
db = conn['testdb']
# db = conn['blank']
# db = conn['familytree']

def create_app(config_name='default'):
    app = Flask(__name__)

    from .home import home as home_blueprint

    app.register_blueprint(home_blueprint, url_prefix="/")

    return app
