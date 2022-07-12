import networkx as nx
import ast
from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *

db = SQLAlchemy()

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
basedir = os.path.abspath(os.path.dirname(__file__))

# create flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'graph.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

# sqlite init to app
db = SQLAlchemy(app)
# %%
# define meta data for table
db.drop_all()

meta = MetaData()
Nodetable = Table('nodes', meta,
                  Column('id', Integer, primary_key=True),
                  Column('node_type', String),
                  Column('node_id', String),
                  Column('node_attr', String),
                  UniqueConstraint('node_type', 'node_id', name='uix_node_type_node_id'))

Edgetable = Table('edges', meta,
                  Column('id', Integer, primary_key=True),
                  Column('source_node_id', Integer),
                  Column('target_node_id', Integer),
                  Column('edge_type', String),
                  Column('edge_attr', String),
                  UniqueConstraint('source_node_id', 'target_node_id','edge_type', name='uix_source_target_edge'))

# create table to sqlite
meta.create_all(engine)

class Node(db.Model):
    __tablename__ = "nodes"
    __table_args__ = {'extend_existing': True}

    # columns
    id = db.Column(db.Integer(), primary_key=True)
    node_type = db.Column(db.String(64))
    node_id = db.Column(db.String(64))
    node_attr = db.Column(db.String(256))
    UniqueConstraint('node_type', 'node_id', name='uix_node_type_node_id')

    def __init__(self, node_type, node_id, node_attr):
        self.node_type = node_type
        self.node_id = node_id
        self.node_attr = node_attr


class Edge(db.Model):
    __tablename__ = "edges"
    __table_args__ = {'extend_existing': True}

    # columns
    id = db.Column(db.Integer(), primary_key=True)
    source_node_id = db.Column(db.Integer())
    target_node_id = db.Column(db.Integer())
    edge_type = db.Column(db.String(128))
    edge_attr = db.Column(db.String(256))
    UniqueConstraint('source_node', 'target_node', 'edge_type', name='uix_source_target_edge')

    def __init__(self, source_node_id, target_node_id, edge_type, edge_attr):
        self.source_node_id = source_node_id
        self.target_node_id = target_node_id
        self.edge_type = edge_type
        self.edge_attr = edge_attr

# %%

def initiate_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM nodes"))
        for row in result:
            print(row)

def get_node_types():
    with engine.connect() as conn:
        result = conn.execute(text("select distinct node_type from nodes"))
        for row in result:
            print(row)
        # return result


def get_all_attributes(node_type):
    """
    retrieve a set of all attributes from a specified node_type
    """
    with engine.connect() as conn:
        result = conn.execute(text("SELECT node_attr FROM nodes WHERE node_type = '{}'".format(node_type)))
        k = []
        for row in result:
            for ky in ast.literal_eval(row[0]).keys():
                k.append(ky)

        return set(k)

def update_node_attributes(node_type):
    """

    """
    full_attribute_list = get_all_attributes(node_type)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT node_type, node_id, node_attr FROM nodes WHERE node_type = '{}'".format(node_type)))
        for row in result:
            print(row)
            # get attributes dict
            d = ast.literal_eval(row[2])
            missing_attributes = [x for x in full_attribute_list if x not in d.keys()]
            if len(missing_attributes) > 0:
                for missing_key in missing_attributes:
                    d[missing_key] = ''

                my_node = db.session.query(Node).filter_by(node_type = row[0], node_id=row[1]).first()
                if my_node:
                    print('my_node found')
                    my_node.node_attr = d
                    db.session.add(my_node)
                    db.session.commit()

def update_node_attributes(node_type):
    """
    update node attribute 'key' with an empty 'value' if it does not already exist. All node_types should have the same attributes
    """
    #   UPDATE EXISTING NODE
    my_node = db.session.query(Node).filter_by(node_type='place', node_id='leek').first()
    # my_node = db.session.models.Node.query.filter_by(node_type=node_type, node_id=node_id).first()
    print(my_node)
    if my_node:
        print('my_node found')
        my_node.node_type = 'place'
        my_node.node_id = 'leek'
        my_node.node_attr = "{'a':'b'}"
        # db.session.add(models.Node(node_type, node_id, str(props)))
        db.session.add(my_node)
        db.session.commit()

    return 0

class create_node():
    def __init__(self, node_type, node_id, node_attributes):
        self.node_type = node_type
        self.node_id = node_id
        self.node_attributes = node_attributes

    def create_node(self):
        '''
        Function for adding a new node to a networkx graph and a sqlite database
        '''
        self.create_node_nx()
        self.create_node_sl()

    def create_node_nx(self):
        '''
        add to networkx graph
        '''
        G.add_node(self.node_id, type=self.node_type)
        if self.node_attributes is not null:
            attrs = {self.node_id: self.node_attributes}
            nx.set_node_attributes(G, attrs)

    # def create_node_sl(self, node_type, node_id, node_attributes=null):
    def create_node_sl(self):
        '''
        add node to sqlite database
        '''
        try:
            print('pre db session add')
            db.session.add(Node(self.node_type, self.node_id, str(self.node_attributes)))
            print('pre commit')
            db.session.commit()
            print('commit')
        except:
            print('pre rollback')
            db.session.update(Node(self.node_type, self.node_id, str(self.node_attributes)))
            db.session.rollback()
            print('transaction rollback')

# %%
create_node('person', 'willemse,marjan', {'node_type':'person', 'node_id':'willemse,marjan','firstname': 'marjan', 'lastname': 'willemse'}).create_node()
create_node('person', 'huizinga,paul', {'node_type':'person', 'node_id':'huizinga,paul','firstname': 'paul', 'lastname': 'huizinga'}).create_node()
create_node('place', 'groningen', {'node_type':'place', 'node_id':'groningen'}).create_node()
create_node('place', 'leek', {'node_type':'place', 'node_id':'leek'}).create_node()

#%%
#   UPDATE EXISTING NODE
my_node = db.session.query(Node).filter_by(node_type = 'place', node_id='leek').first()
# my_node = db.session.models.Node.query.filter_by(node_type=node_type, node_id=node_id).first()
    print(my_node)
    if my_node:
        print('my_node found')
        my_node.node_type = 'place'
        my_node.node_id = 'leek'
        my_node.node_attr = "{'a':'b'}"
        # db.session.add(models.Node(node_type, node_id, str(props)))
        db.session.add(my_node)
        db.session.commit()
# %%
# sqlalchemy
# import json
#
# # G = nx.Graph()
# # Create database
# cnx = create_engine('sqlite:///db.sqlite').connect()
# # create tables (if they do not exist already)
#
# # select nodes from database
# def get_nodes_from_db():
#     '''
#     get nodes from database
#     add nodes to networkx graph
#     '''
#     result = cnx.execute('SELECT * FROM nodes')
#
#     # move nodes from database in networkx graph
#     for row in result:
#         G.add_nodes_from([([row['node_id'], json.loads(row['node_properties'])])])
#
#     print('{} nodes add to graph'.format(len(G.nodes)))

# %%
node_id = 'marjan'
node_properties = {'firstname': 'marjan', 'lastname': 'willemse'}
sql = 'insert into nodes (node_type, node_id, node_properties) values ("{}", "{}", "{}")'.format('test', node_id,
                                                                                                 str(node_properties))
print(sql)
cnx.execute(sql)
add node to database