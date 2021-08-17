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

# done: create blank db as an option
# done: select db as an option
# done: backup database
# done: drop collection when empty
# done: remove main.css / create.html
# done: make remove key function an api
# done: make nodes stick so it's easier to add multiple relations to the same node
# done: add trim function when adding new collection (names)
# done: add default 'geldigheid' to edges
# done: add edge properties
# done: fix input error
# done: add selection to graph (show what has been selected)
# done: add warning before removal and merge
# done: add option to merge 2 nodes into 1.
# done: add function to change a node id (also in all edges)
# done: add legend to graph viz
# done: visualize per edge type (show all datafeeds)
# done: enlarge graphics on graph
# done: add color code to nodes in graph
# done: avoid adding duplicate edges
# done: add view on a single node (view all nodes relations)
# rejected: auto 'close' relations when a node is 'closed' (with dates). (no longer needed: neo4j does automatically)
# rejected: remove duplicate edges (or do not allow to be stored)
# rejected: rebase to objectID (not possible, you do not want to look for characteristics but for id's. It has to be unique)

from flask import Flask
from py2neo import Graph

graph = Graph(host="localhost", port=7687, auth=('neo4j', 'admin'))
# graph = Graph()
# import pymongo

# conn = pymongo.MongoClient("mongodb://localhost:27017/")
# db = conn['paul_db']
# db = conn['testdb']
# db = conn['blank']
# db = conn['familytree']

def create_app(config_name='default'):
    app = Flask(__name__)

    from .home import home as home_blueprint

    app.register_blueprint(home_blueprint, url_prefix="/")

    return app
