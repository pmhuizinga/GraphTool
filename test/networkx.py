import networkx as nx
from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt

# %%
# import operator
# import warnings

# create sample data
node_list = ['A', 'B', 'C', 'D']
source = ['A', 'B', 'C', 'D']
target = ['B', 'C', 'D', 'A']
df = pd.DataFrame({'source': source, 'target': target})

# create graph database
G = nx.Graph()

# add nodes
G.add_nodes_from(node_list, type="test")

# add edges
edges = []
for index, row in df.iterrows():
    edges.append((row['source'], row['target']))

G.add_edges_from(edges)

# draw graph
plt.figure(3, figsize=(12, 12))
nx.draw(G)
plt.show()

# set attribute
attrs = {'A': {'prop1': 1, 'prop2': 2}}
nx.set_node_attributes(G, attrs)
G.nodes()

# get node attributes
G.nodes['A']
# %%
# Sqlalchemy
import json

G = nx.Graph()
cnx = create_engine('sqlite:///db.sqlite').connect()
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
#%%
node_id = 'marjan'
node_properties = {'firstname': 'marjan', 'lastname':'willemse'}
sql = 'insert into nodes (node_type, node_id, node_properties) values ("{}", "{}", "{}")'.format('test', node_id, str(node_properties))
print(sql)
cnx.execute(sql)
# add node to database
#
# print(G.nodes())
