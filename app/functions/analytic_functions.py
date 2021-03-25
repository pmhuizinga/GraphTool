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
                node_list.append({"id": str(id), "type": item[5:]})

    return node_list


def get_all_edge_list():

    collections = db.list_collection_names()

    edge_list = []
    for item in collections:
        if item[:4] == 'edge':
            type = item[5:]
            coll = db[item].find()
            for record in coll:
                edge_list.append({"source": str(record['source']), "target": str(record['target']), "value": 1 })

    return edge_list


def get_graph_degrees():
    """
    :return: sorted (desc) list of nodes and degrees
    """
    G = nx.Graph()
    G.add_edges_from([(x['source'], x['target']) for x in get_all_edge_list()])

    out = list(G.degree())
    a = dict(out)

    b = sorted(a.items(), key=lambda item: item[1], reverse=True)

    return b


def get_graph_pagerank():
    """
    PageRanks
    PageRank computes a ranking of the nodes in the graph G based on the structure of the incoming links.
    It was originally designed as an algorithm to rank web pages
    """
    G = nx.Graph()
    G.add_edges_from([(x['source'], x['target']) for x in get_all_edge_list()])

    a = dict(nx.pagerank(G))
    b = sorted(a.items(), key=lambda item: item[1], reverse=True)

    return b


def get_graph_betweennes_centrality():
    """
    Betweenness Centrality
    Betweenness Centrality is a way of detecting the amount of influence a node has over the flow of information
    in a graph. It is often used to find nodes that serve as a bridge from one part of a graph to another,
    for example in package delivery process or a telecommunication network.
    """
    G = nx.Graph()
    G.add_edges_from([(x['source'], x['target']) for x in get_all_edge_list()])

    a = dict(nx.betweenness_centrality(G))
    b = sorted(a.items(), key=lambda item: item[1], reverse=True)

    return b