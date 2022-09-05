from app import db
# from app import graph
from app import models
from app.functions import networkx_database_functions as dbf
import networkx as nx
import ast


def get_nodes_per_type(type):
    """

    """
    lst = [x.node_id for x in models.Node.query.filter_by(node_type='person')]
    query = "MATCH(a:{}) return a".format(type)
    query_result = graph.run(query).to_ndarray()
    result = [n[0] for n in query_result]
    return result


# def get_nodes_per_type(type):
#     query = "MATCH(a:{}) return a".format(type)
#     query_result = graph.run(query).to_ndarray()
#     result = [n[0] for n in query_result]
#     return result

def get_all_nodes_list(base, id="all"):
    """
    get nodes including node type using Neo4j as source
    Default is all, unless node id is entered
    Used for d3.js graph
    :param node: node id
    :return: list of nodes including node type
    """

    # collections = dbf.get_node_names()

    node_list = []

    if id == 'all' and base == 'node':
        node_list = ([ast.literal_eval(x.node_attr) for x in models.Node.query.distinct(models.Node.node_type)])
        # todo: onderstaande moet weg. Alle functies moeten werken op node_id en node_type
        for d in node_list:
            d['id'] = d['node_id']
            d['type'] = d['node_type']

    # if id == 'all':
    #     for item in collections:
    #         if base == 'node':
    #             for node in get_nodes_per_type(item):
    #                 node_val = dict(node)
    #                 if 'id' in node_val:
    #                     node_val['name'] = node_val['id']
    #                 if 'name' in node_val:
    #                     node_val['id'] = node_val['name']
    #                 node_val['type'] = item
    #                 node_list.append(node_val)
    #             # for identifier in dbf.get_collection_id(item):
    #             #     node_list.append({"id": str(identifier), "type": item})
    #
    # else:
    #     # get all edges that include the specified node
    #     if base == 'node':
    #         edge_list = get_all_edge_list(base='node', id=id)
    #         print(edge_list)
    #     elif base == 'edge':
    #         edge_list = get_all_edge_list(base='edge', id=id)
    #
    #     lst = []
    #     # create (set) list of nodes
    #     for record in edge_list:
    #         lst.append(record['source'])
    #         lst.append(record['target'])
    #     lst = list(set(lst))
    #     # add node characteristics to node list
    #     for item in collections:
    #         for record in dbf.get_collection_id(item):
    #             if record in lst:
    #                 node_list.append({"id": record, "type": item})

    return node_list


def get_all_edge_list(base, id="all"):
    """
    returns a dict of edges in the graph [source, target, type]
    :param base:
    :param id:
    :return:
    """
    # collections = db.list_collection_names()

    query = """
    select  source.node_type as source_node_type
            ,source.node_id as source_node_id
            ,e.edge_type
            ,target.node_type as target_node_type
            ,target.node_id as target_node_id 
    from Edges as e 
    left join Nodes as source
            on e.source_node_id = source.id
    left join Nodes as target
            on e.target_node_id = target.id
    """

    edge_list = []

    for record in db.engine.execute(query):
        edge_list.append({
            'sourcenodetype': record[0]
            , 'source': record[1]
            , 'target': record[3]
            , 'targetnodetype': record[4]
            , 'type': record[2]})

    # if id == 'all' and base == 'node':
    #     edge_list = ([ast.literal_eval(x.edge_type) for x in models.Edge.query.join(models.Node, models.Node.id == models.Edge.source_node_id).add_columns(models.Edge.edge_type, models.Node.node_type)])
    # edge_list = ([ast.literal_eval(x.edge_type) for x in models.Edge.query.distinct(models.Edge.edge_type)])
    print(edge_list)
    return edge_list

    # collections = dbf.get_edge_names()
    # edge_list = []
    #
    # if base == 'edge':
    #     if id == 'all':
    #         for item in collections:
    #             # if item[:4] == 'edge':
    #             coll = dbf.get_edge_relations(item)
    #             # coll = db[item].find()
    #             type = item
    #             for record in coll:
    #                 # record.pop('_id')
    #                 # record['type'] = item
    #                 if id == "all":
    #                     edge_list.append(
    #                         {"source": str(record[0]), "target": str(record[2]), "type": str(record[1]), "sourcenodetype": str(record[3]), "targetnodetype": str(record[4])})
    #
    #     else:
    #         coll = dbf.get_edge_relations(id)
    #         for record in coll:
    #             edge_list.append(
    #                 # {"source": str(record[0]), "target": str(record[2]), "type": str(record[1])})
    #                 # {"source": str(record[0]), "target": str(record[2]), "type": str(record[1])})
    #                 {"source": str(record[0]), "target": str(record[2]), "type": str(record[1]),
    #                  "sourcenodetype": str(record[3]), "targetnodetype": str(record[4])})
    #
    # elif base == 'node':
    #     # get only nodes of the specific relation
    #     for item in collections:
    #             coll = dbf.get_edge_relations(item)
    #             for record in coll:
    #                 if id == "all":
    #                     # edge_list.append(record)
    #                     edge_list.append(
    #                         # {"source": str(record[0]), "target": str(record[2]), "type": str(record[1])})
    #                     {"source": str(record[0]), "target": str(record[2]), "type": str(record[1]),
    #                      "sourcenodetype": str(record[3]), "targetnodetype": str(record[4])})
    #                 elif record[0] == id:
    #                     # edge_list.append(record)
    #                     edge_list.append(
    #                         # {"source": str(record[0]), "target": str(record[2]), "type": str(record[1])})
    #                         {"source": str(record[0]), "target": str(record[2]), "type": str(record[1]),
    #                          "sourcenodetype": str(record[3]), "targetnodetype": str(record[4])})
    #                 elif record[2] == id:
    #                     # edge_list.append(record)
    #                     edge_list.append(
    #                         # {"source": str(record[0]), "target": str(record[2]), "type": str(record[1])})
    #                         {"source": str(record[0]), "target": str(record[2]), "type": str(record[1]),
    #                          "sourcenodetype": str(record[3]), "targetnodetype": str(record[4])})

    # return edge_list


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