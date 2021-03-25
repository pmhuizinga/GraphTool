from app import db
from app.functions import database_functions as dbf
import matplotlib.pyplot as plt
import networkx as nx

def get_all_nodes_list():

    collections = db.list_collection_names()

    node_list = []
    for item in collections:
        if item[:4] == 'node':
            for id in dbf.getCollectionId(item):
                # node_list.append({'id': id, 'type': item[5:]})
                # node_list.append((id, item[5:]))
                node_list.append({"id": str(id), "group": 1})

    return node_list


def get_all_edge_list():

    collections = db.list_collection_names()

    edge_list = []
    for item in collections:
        if item[:4] == 'edge':
            type = item[5:]
            coll = db[item].find()
            for record in coll:
                # edge_list.append({'source': record['source'], 'target': record['target'], 'type': type})
                # edge_list.append((record['source'], record['target']))
                edge_list.append({"source": str(record['source']), "target": str(record['target']), "value": 1 })

    return edge_list


# G = nx.Graph()
# # add nodes
# # G.add_nodes_from(get_all_nodes_list())
# # add edges
# G.add_edges_from(get_all_edge_list())
# # draw graph
# plt.figure(3, figsize=(12, 12))
# nx.draw(G)
# plt.show()
#
# # degrees
# G.degree()


