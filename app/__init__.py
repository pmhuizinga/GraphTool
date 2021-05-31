# todo: add "ID already exists" warning
# todo: merge epic and project to project, include type 'epic'
# todo: put db conn in config
# todo: create blank db as an option
# todo: select db as an option
# todo: backup database
# todo: add function to merge tables
# todo: add function to rename table name
# todo: auto 'close' relations when a node is 'closed' (with dates).
# todo: add possibility to remove or modify an edge
# todo: add full dependencies as visual
# todo: switch graph view to community view (and back)
# todo: learn BERT for NLP
# todo: add 'api/' to api string

# done: drop collection when empty
# done: remove main.css / create.html
# done: make remove key function an api
# done: make nodes stick so it's easier to add multiple relations to the same node
# rejected: remove duplicate edges (or do not allow to be stored)
# rejected: rebase to objectID (not possible, you do not want to look for characteristics but for id's. It has to be unique)
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

from flask import Flask
import pymongo

conn = pymongo.MongoClient("mongodb://localhost:27017/")
db = conn['paul_db']
# db = conn['testdb']
# db = conn['blank']
# db = conn['familytree']

def create_app(config_name='default'):
    app = Flask(__name__)

    from .home import home as home_blueprint

    app.register_blueprint(home_blueprint, url_prefix="/")

    return app
