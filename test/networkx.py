import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
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
# plt.figure(3, figsize=(12, 12))
# nx.draw(G)
# plt.show()

# set attribute
attrs={'A': {'prop1': 1, 'prop2': 2}}
nx.set_node_attributes(G, attrs)
G.nodes()

# get node attributes
G.nodes['A']

