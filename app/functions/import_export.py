import json
from py2neo import Graph, Node, NodeMatcher, Relationship
import requests
import os

# from app.home import home
# from flask import url_for

graph = Graph(host="localhost", port=7687, auth=('neo4j', 'admin'))
matcher = NodeMatcher(graph)

# f = 'C:\\Users\\pahuizinga\\OneDrive - Aegon\\Python\\GraphTool\\documentation\\'
f = 'C:\\Users\\PaulMarjanIlseMeike\\Dropbox\\Paul\\DataScience\\Projects\\GraphToolNeo4j\\databases\\'
nodes_url = 'http://127.0.0.1:5000/graph_nodes/node/all'
edges_url = 'http://127.0.0.1:5000/graph_edges/node/all'


def database_clear():
    delete_query = "MATCH(n) DETACH DELETE n"
    graph.run(delete_query)


def read_from_api(url):
    """
    read api data and return as json file
    """
    r = requests.get(url)
    data = r.json()
    return data


def database_save(folderpath, nodes_file_name='nodes.json', edges_file_name='edges.json'):
    """
    Write node file and edge file from api to a specified location
    """
    with open(folderpath + nodes_file_name, 'w') as f:
        json.dump(read_from_api(nodes_url), f)

    with open(folderpath + edges_file_name, 'w') as f:
        json.dump(read_from_api(edges_url), f)


def read_from_file(folderpath, nodes_file_name='nodes.json', edges_file_name='edges.json'):
    # read files
    # with open('C:\\Users\\pahuizinga\\OneDrive - Aegon\\Python\\GraphTool\\documentation\\nodes.json', 'r') as myfile:
    with open(folderpath + nodes_file_name, 'r') as myfile:
        node_set = myfile.read()

    nodes = json.loads(node_set)

    # with open('C:\\Users\\pahuizinga\\OneDrive - Aegon\\Python\\GraphTool\\documentation\\edges.json', 'r') as myfile:
    with open(folderpath + edges_file_name, 'r') as myfile:
        edge_set = myfile.read()
    edges = json.loads(edge_set)

    return nodes, edges


def create_nodes_in_neo4j(nodes):
    """
    Creates nodes in neo4j based on a list of dictionairies.
    Requires key 'type' to be in each dict.
    """
    for item in nodes:
        # a = Node(item['type'], name=item['id'])
        # graph.create(a)
        node_type = item['type']
        item.pop('type', None)
        a = Node(node_type, **item)
        graph.create(a)


def create_edges_in_neo4j(edges):
    # create edges in Neo
    for item in edges:
        NodeSource = matcher.match(name=item['source']).first()
        NodeTarget = matcher.match(name=item['target']).first()
        a = Relationship(NodeSource, item['type'], NodeTarget)
        graph.create(a)


def database_open(folderpath, db_delete=True):
    """
    Create a database in Neo4j based on source node and edge files
    """
    if db_delete == True:
        database_clear()

    nodes, edges = read_from_file(folderpath)
    create_nodes_in_neo4j(nodes)
    create_edges_in_neo4j(edges)


def read_current_db_name():
    with open(f + 'current_db.txt', 'r') as myfile:
        db_name = myfile.read()

    return db_name


def write_db_name(db_name):
    with open(f + 'current_db.txt', 'w') as myfile:
        myfile.write(db_name)
        print('current_db was changed to {}'.format(db_name))


def database_create(new_db_name, save_current_db=True):
    """
    create a new database. Current database will be saved
    """
    # save current database
    if save_current_db == True:
        db = read_current_db_name()
        save_folder = f + db + '\\'
        database_save(save_folder)
        print('Database {} was saved to {}'.format(db, save_folder))

    # clear current database
    database_clear()
    print('Current Neo4j database is truncated')

    # create new database
    # create folder
    newpath = f + new_db_name
    if not os.path.exists(newpath):
        os.makedirs(newpath)
        print('folder {} is created'.format(new_db_name))

    # change current_db.txt
    write_db_name(new_db_name)


def database_switch(db_name, save_current_db=True):
    # save current database
    if save_current_db == True:
        db = read_current_db_name()
        save_folder = f + db + '\\'
        database_save(save_folder)
        print('Database {} was saved to {}'.format(db, save_folder))

    # clear current database
    database_clear()
    print('Current Neo4j database is truncated')

    # open new database
    database_open(f + db_name + '\\')
    print('Database {} is loaded'.format(db_name))

    # change current_db.txt
    write_db_name(db_name)
