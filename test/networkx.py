import networkx as nx
from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt

# %%

# create sample data
node_list = ['A', 'B', 'C', 'D']
source = ['A', 'B', 'C', 'D']
target = ['B', 'C', 'D', 'A']
df = pd.DataFrame({'source': source, 'target': target})

# create graph database
G = nx.Graph()

# NODES
# add nodes from list
G.add_nodes_from(node_list, type="test")
# add single node (including attributes)
G.add_node("nodename", type="test")
G.add_node("nodename2", type="test")
# add attribute to existing node
attrs = {'nodename': {'prop1': 1, 'prop2': 2}}
nx.set_node_attributes(G, attrs)
# or
G.add_node("nodename", firstname='paul')
# get single node attributes
G.nodes['nodename']
# get all nodes with attribute 'firstname'
for k, v in G.nodes(data=True):
    if 'firstname' in v:
        print(k, v['firstname'])
# remove single node
G.remove_node("nodename2")
# remove attribute from node
del G.nodes["nodename"]['firstname']
# get all nodes
G.nodes()

# EDGES
# add edges from list
edges = []
for index, row in df.iterrows():
    edges.append((row['source'], row['target']))
G.add_edges_from(edges)
# remove edge
G.remove_edge('A', 'B')
# add attribute to edge
attrs = {('A', 'B'): {"attr1": 20, "attr2": "nothing"}, ('B', 'C'): {"attr2": 3}}
nx.set_edge_attributes(G, attrs)
# get all edges with attribute 'attr2'
for e in G.edges(data=True):
    if 'attr2' in e[2]:
        print(e)

# draw graph
plt.figure(3, figsize=(12, 12))
nx.draw(G)
plt.show()

# %%
node_id = 'marjan'
node_properties = {'firstname': 'marjan', 'lastname': 'willemse'}
sql = 'insert into nodes (node_type, node_id, node_properties) values ("{}", "{}", "{}")'.format('test', node_id,
                                                                                                 str(node_properties))
print(sql)
cnx.execute(sql)
# add node to database
#
# print(G.nodes())
# %%
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *

basedir = os.path.abspath(os.path.dirname(__file__))

# create flask app
app = Flask(__name__)
# set sqllite db connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'graph.sqlite')
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

# sqlite init to app
db = SQLAlchemy(app)
#%%
# drop tables
from sqlalchemy.ext.declarative import declarative_base

tables = ['nodes', 'edges']
base = declarative_base()
metadata = MetaData(engine, reflect=True)
for table in tables:
    table = metadata.tables.get(table)
    if table is not None:
        base.metadata.drop_all(engine, [table], checkfirst=True)
# %%
# define meta data for table
meta = MetaData()
Nodetable = Table('nodes', meta, Column('id', Integer, primary_key=True, autoincrement=True),
                  Column('node_type', String, unique=True),
                  Column('node_attr', String))

Edgetable = Table('edges', meta, Column('id', Integer, primary_key=True, autoincrement=True),
                  Column('source_edge', Integer, unique=False),
                  Column('target_edge', Integer, unique=False),
                  Column('edge_attr', String))

# create table to sqlite
meta.create_all(engine)

class Node(db.Model):
    # table name for nodes model
    __tablename__ = "nodes"

    # user columns
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    node_type = db.Column(db.String(64))
    node_name = db.Column(db.String(64))
    node_attr = db.Column(db.String(256))

    def __init__(self, node_type, node_attr):
        # self.id=id
        self.node_type = node_type
        self.node_attr = node_attr


class Edge(db.Model):
    # table name for edges model
    __tablename__ = "edges"

    # user columns
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    source_edge = db.Column(db.Integer(), unique=False)
    target_edge = db.Column(db.Integer(), unique=False)
    edge_attr = db.Column(db.String(128))

    def __init__(self, source_edge, target_edge, edge_attr):
        # self.id=id
        self.source_edge = source_edge
        self.target_edge = target_edge
        self.edge_attr = edge_attr


# %%
# create node  object
node = Node('person', '{"firstname":"paul"}')
# insert user object to sqlite
db.session.add(node)
# commit transaction
db.session.commit()

# todo: update node object

node_type = 'person'
node_attributes = {'firstname': 'marjan', 'lastname': 'willemse'}
db.session.add(node)
db.session.commit()


node = Node(node_type, node_attributes)
'''
wat zijn de keys voor nodes?
node_type
node_name (huizinga, paul)

keys voor edges zijn node_ids
'''
#%$
def create_node(node_type, node_name, node_attributes):
    '''
    Function for adding a new node to a networkx graph and a sqlite database
    '''
    # add to networkx graph
    G.add_node(node_type, firstname='paul')

# %%
# sqlalchemy
import json

# G = nx.Graph()
# Create database
cnx = create_engine('sqlite:///db.sqlite').connect()


# create tables (if they do not exist already)


# select nodes from database
def get_nodes_from_db():
    '''
    get nodes from database
    add nodes to networkx graph
    '''
    result = cnx.execute('SELECT * FROM nodes')

    # move nodes from database in networkx graph
    for row in result:
        G.add_nodes_from([([row['node_id'], json.loads(row['node_properties'])])])

    print('{} nodes add to graph'.format(len(G.nodes)))

