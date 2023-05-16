from app import db
from app import models
from app.functions import log
from app.functions import networkx_database_functions as dbf
import networkx as nx
import scipy
import ast  # om text om te zetten, dus "'txt'" naar 'txt'


def get_all_nodes_list(base, id="all"):
    """
    get nodes including node type
    Default is all.
    When a node_id is supplied this node and all directly related nodes will be returned
    Used for d3.js graph
    d3.js requires an "id" attribute in the node list for creating the edges to the nodes
    :param node: node id
    :return: list of nodes including node type
    """
    log.logger.debug('base is {} and id = {}'.format(base, id))
    collections = dbf.get_node_names()
    log.logger.debug('collections:  {}'.format(collections))
    node_list = []

    if base == 'node' and id == 'all':
        all_nodes = models.Node.query.all()
        for node in all_nodes:
            node_list.append(
                {"id": node.id, "node_id": node.node_id, "node_type": node.node_type,
                 "name": node.node_id, "type": node.node_type, "node_attr": node.node_attr})

    elif base == 'node' and id != 'all':
        # get all edges that include the specified node
        # base can be 'node' or 'edge'.
        edge_list = get_all_edge_list(base=base, id=id)
        log.logger.debug('edges: {}'.format(edge_list))

        lst = []
        # create (set) list of nodes from edge list
        for record in edge_list:
            lst.append(record['source'])
            lst.append(record['target'])
        # make list of unique nodes
        lst = list(set(lst))

        # populate node_list based on the node id's found in the edge list
        node_list = []
        for node_id in lst:
            node_details = models.Node.query.filter_by(id=node_id).first()
            node_list.append(
                {"id": node_details.id, "node_id": node_details.node_id, "node_type": node_details.node_type,
                 "name": node_details.node_id, "type": node_details.node_type, "node_attr": node_details.node_attr})

    elif base == 'edge':
        # get all edges that include the specified node
        # base can be 'node' or 'edge'.
        edge_list = get_all_edge_list(base=base, id=id)
        log.logger.debug('edges: {}'.format(edge_list))

        lst = []
        # create (set) list of nodes from edge list
        for record in edge_list:
            lst.append(record['source'])
            lst.append(record['target'])
        # make list of unique nodes
        lst = list(set(lst))

        # populate node_list based on the node id's found in the edge list
        node_list = []
        for node_id in lst:
            node_details = models.Node.query.filter_by(id=node_id).first()
            node_list.append(
                {"id": node_details.id, "node_id": node_details.node_id, "node_type": node_details.node_type,
                 "name": node_details.node_id, "type": node_details.node_type, "node_attr": node_details.node_attr})


    return node_list


def get_all_edge_list(base, id="all"):
    """
    returns a dict of edges in the graph [source, target, type]
    :param base:
    :param id:
    :return:
    """
    # collections = db.list_collection_names()

    # ALERT; the sequence of selections in the query below matter.
    if base == 'node' and id == 'all':
        query = """
        select  source.node_type as source_node_type
                ,source.id as source_node_id
                ,e.edge_type as edge_type
                ,target.node_type as target_node_type
                ,target.id as target_node_id
                ,source.node_id as source_node_name
                ,target.node_id as target_node_name 
                ,source.node_attr as source_node_attributes
                ,target.node_attr as target_node_attributes
        from Edges as e 
        left join Nodes as source
                on e.source_node_id = source.id
        left join Nodes as target
                on e.target_node_id = target.id
        """
    elif base == 'node' and id != 'all':
        query = """
        select  source.node_type as source_node_type
                ,source.id as source_node_id
                ,e.edge_type as edge_type
                ,target.node_type as target_node_type
                ,target.id as target_node_id
                ,source.node_id as source_node_name
                ,target.node_id as target_node_name 
                ,source.node_attr as source_node_attributes
                ,target.node_attr as target_node_attributes
        from Edges as e 
        left join Nodes as source
                on e.source_node_id = source.id
        left join Nodes as target
                on e.target_node_id = target.id
        where source.node_id ='{}' or target.node_id = '{}'
        """.format(id, id)
    elif base == 'edge':
        query = """
        select  source.node_type as source_node_type
                ,source.id as source_node_id
                ,e.edge_type as edge_type
                ,target.node_type as target_node_type
                ,target.id as target_node_id
                ,source.node_id as source_node_name
                ,target.node_id as target_node_name 
                ,source.node_attr as source_node_attributes
                ,target.node_attr as target_node_attributes
        from Edges as e 
        left join Nodes as source
                on e.source_node_id = source.id
        left join Nodes as target
                on e.target_node_id = target.id
        where e.edge_type ='{}'
        """.format(id)

    edge_list = []

    for idx, record in enumerate(db.engine.execute(query)):
        # print(idx)
        edge_list.append({
            'sourcenodetype': record[0]
            , 'source': record[1]
            , 'type': record[2]
            , 'targetnodetype': record[3]
            , 'target': record[4]
            , 'sourcenodename': record[5]
            , 'targetnodename': record[6]})


    log.logger.debug('edge_list: {}'.format(edge_list))
    log.logger.debug('end of function get_all_edge_list')
    return edge_list


def create_networkx_graph():
    G = nx.Graph()
    G.add_edges_from([(x['sourcenodename'], x['targetnodename']) for x in get_all_edge_list(base='node')])
    return G

def get_graph_degrees():
    """
    :return: sorted (desc) list of nodes and degrees
    """
    G = create_networkx_graph()
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
    G = create_networkx_graph()
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
    G = create_networkx_graph()
    a = dict(nx.betweenness_centrality(G))
    b = sorted(a.items(), key=lambda item: item[1], reverse=True)

    return b


