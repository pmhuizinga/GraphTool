# from app import db
from app import graph
from app.functions import neo4j_database_functions as dbf
import networkx as nx


def get_all_nodes_list(base, id="all"):
    """
    get nodes including node type using Neo4j as source
    Default is all, unless node id is entered
    Used for d3.js graph
    :param node: node id
    :return: list of nodes including node type
    """

    collections = dbf.get_node_names()

    node_list = []

    if id == 'all':
        for item in collections:
            if base == 'node':
                for identifier in dbf.getCollectionId(item):
                    node_list.append({"id": str(identifier), "type": item})

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
            for record in dbf.getCollectionId(item):
                if record in lst:
                    node_list.append({"id": record, "type": item})

    return node_list


def get_all_edge_list(base, id="all"):
    """
    returns a dict of edges in the graph [source, target, type]
    :param base:
    :param id:
    :return:
    """
    # collections = db.list_collection_names()
    collections = dbf.get_edge_names()
    edge_list = []

    if base == 'edge':
        if id == 'all':
            for item in collections:
                # if item[:4] == 'edge':
                coll = dbf.get_edge_relations(item)
                # coll = db[item].find()
                type = item
                for record in coll:
                    # record.pop('_id')
                    # record['type'] = item
                    if id == "all":
                        edge_list.append(
                            {"source": str(record[0]), "target": str(record[2]), "type": str(record[1])})

        else:
            coll = dbf.get_edge_relations(id)
            for record in coll:
                edge_list.append(
                    # {"source": str(record[0]), "target": str(record[2]), "type": str(record[1])})
                    {"source": str(record[0]), "target": str(record[2]), "type": str(record[1])})

    elif base == 'node':
        # get only nodes of the specific relation
        for item in collections:
                coll = dbf.get_edge_relations(item)
                for record in coll:
                    if id == "all":
                        # edge_list.append(record)
                        edge_list.append(
                            {"source": str(record[0]), "target": str(record[2]), "type": str(record[1])})
                    elif record[0] == id:
                        # edge_list.append(record)
                        edge_list.append(
                            {"source": str(record[0]), "target": str(record[2]), "type": str(record[1])})
                    elif record[2] == id:
                        # edge_list.append(record)
                        edge_list.append(
                            {"source": str(record[0]), "target": str(record[2]), "type": str(record[1])})

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
