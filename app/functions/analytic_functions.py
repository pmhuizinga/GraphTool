from app import db
from app.functions import database_functions as dbf
import networkx as nx


def get_all_nodes_list(base, id="all"):
    """
    get nodes including node type
    Default is all, unless node id is entered
    Used for d3.js graph
    :param node: node id
    :return: list of nodes including node type
    """

    collections = db.list_collection_names()

    node_list = []

    if id == 'all':
        for item in collections:
            if item[:4] == 'node':
                for identifier in dbf.getCollectionId(item):
                    node_list.append({"id": str(identifier), "type": item[5:]})

    else:
        # get all edges that include the specified node
        if base == 'node':
            edge_list = get_all_edge_list(base='node', id=id)
        elif base == 'edge':
            edge_list = get_all_edge_list(base='edge', id=id)
        lst = []
        # create (set) list of nodes
        for record in edge_list:
            lst.append(record['source'])
            lst.append(record['target'])
        lst = list(set(lst))

        # add node characteristics to node list
        for item in collections:
            if item[:4] == 'node':
                type = item[5:]
                for record in db[item].find():
                    if record['id'] in lst:
                        node_list.append({"id": record['id'], "type": type})

    return node_list


def get_all_edge_list(base, id="all"):
    collections = db.list_collection_names()
    edge_list = []

    if base == 'edge':
        if id == 'all':
            for item in collections:
                if item[:4] == 'edge':
                    coll = db[item].find()
                    for record in coll:
                        if id == "all":
                            edge_list.append(
                                {"source": str(record['source']), "target": str(record['target']), "value": 1})
        else:
            coll = db['edge_' + id].find()
            for record in coll:
                edge_list.append({"source": str(record['source']), "target": str(record['target']), "value": 1})
    elif base == 'node':
        for item in collections:
            if item[:4] == 'edge':
                coll = db[item].find()
                for record in coll:
                    if id == "all":
                        edge_list.append({"source": str(record['source']), "target": str(record['target']), "value": 1})
                    elif record['source'] == id:
                        edge_list.append({"source": str(record['source']), "target": str(record['target']), "value": 1})
                    elif record['target'] == id:
                        edge_list.append({"source": str(record['source']), "target": str(record['target']), "value": 1})

    return edge_list


def get_graph_degrees():
    """
    :return: sorted (desc) list of nodes and degrees
    """
    G = nx.Graph()
    G.add_edges_from([(x['source'], x['target']) for x in get_all_edge_list(base='node')])

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
    G.add_edges_from([(x['source'], x['target']) for x in get_all_edge_list(base='node')])

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
    G.add_edges_from([(x['source'], x['target']) for x in get_all_edge_list(base='node')])

    a = dict(nx.betweenness_centrality(G))
    b = sorted(a.items(), key=lambda item: item[1], reverse=True)

    return b


def get_direct_node_relations():
    pass
