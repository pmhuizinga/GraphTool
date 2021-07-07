# from app import db
from app import graph
import logging

logger = logging.getLogger(__name__)  # initialize logger
logger.handlers = []
c_handler = logging.StreamHandler()  # Create handlers
c_format = logging.Formatter('%(levelname)s - %(message)s')
c_handler.setFormatter(c_format)  # Create formatters and add it to handlers
logger.addHandler(c_handler)  # Add handlers to the logger
logger.setLevel(logging.DEBUG)

#
# def add_collection_identifier(in_list, type):
#     """
#     add 'node_' or 'edge_' to callection name
#     :return: list
#     """
#
#     # !!! NEEDS TO BE ADJUSTED TO NEO4J !!!!
#
#     out_list = [type + '_' + x for x in in_list]
#
#     return out_list


# def drop_collection_identifier(in_list, type):
#     """
#     drop 'node_' or 'edge_' from callection name
#     :return: list
#     """
#
#     # !!! NEEDS TO BE ADJUSTED TO NEO4J !!!!
#
#     out_list = [x[5:] for x in in_list if x[:4] == type]
#
#     return out_list


def find_matching_collections(input):
    """
    -check on lenght
    -check on matching characters

    :param user_input:
    :return:
    """

    # !!! NEEDS TO BE ADJUSTED TO NEO4J !!!!

    collections = db.list_collection_names()

    for collection in collections:
        c = 0
        for i in set(input):
            if i in set(collection):
                c += 1
        set_match = c / len(set(input))
        len_match = min(len(input), len(collection)) / max(len(input), len(collection))
        result = set_match * len_match
        # print('matching result {} for {} is {} (character match: {}, length match {})'.format(input, collection,
        #                                                                                       int(result * 100),
        #                                                                                       set_match, len_match))


def get_collection_keys(type, collection):
    """
    Get full set of keys from a collection
    :param collection: collection name
    :return: all keys for the collection as a list
    """
    if type == 'node':
        query = "match (n:{}) return properties(n)".format(collection)
    elif type == 'edge':
        query = "match(a)-[r:{}]-(b) return properties(r)".format(collection)

    result = graph.run(query).to_ndarray()
    list = [n[0] for n in result]
    all_keys = set().union(*(d.keys() for d in list))
    keys = [k for k in all_keys]

    return keys


def get_collection_id(collection):
    """Get full set of ids from a collection"""

    query = "match(a: {}) return a.name".format(collection)
    result = graph.run(query).to_ndarray()
    list = [n[0] for n in result]

    return list


def get_collection_detail(type, collection, name):
    """Get full set of ids from a collection"""

    # "match(a: {}) where a.name = '{}' return a".format(collection, name)
    query = "match(a: {}) where a.name = '{}' return a".format(collection, name)
    a = graph.evaluate(query)

    result = {}
    if a is None:
        return result

    for k in a.keys():
        result[k] = a[k]

    return result


def get_node_names():
    """

    """
    query = "CALL db.labels()"
    query_result = graph.run(query).to_ndarray()
    result = [n[0] for n in query_result]

    return result


def get_edge_names():
    """

    """
    query = "CALL db.relationshipTypes()"
    query_result = graph.run(query).to_ndarray()
    result = [n[0] for n in query_result]

    return result


def get_edge_relations(edge):
    """
    return a list of edges including sources and targets
    :param edge: edge label
    """
    query = "MATCH p=(a)-[r:{}]->(b) RETURN a.name as source,type(r), b.name as target".format(edge)
    query_result = graph.run(query).to_ndarray().tolist()

    return query_result


def get_node_id(data, source_target_id):
    """
    get node id from request.form based on source or target node.
    :param data: form.request
    :param source_target_id: source or target
    :return: id value (string)
    """
    if source_target_id + '_id' in data.keys():
        if data[source_target_id + '_id'] == '':
            id = data[source_target_id + '_collection_id'].lower()
        else:
            id = data[source_target_id + '_id'].lower()
            # update node id change in all edges -> not necessary for NEO4J
            # if data[source_target_id + '_id'].lower() != data[source_target_id + '_collection_id'].lower():
            #     update_node_id(data[source_target_id + "_collection_name"].lower(),
            #                    data[source_target_id + '_collection_id'].lower(),
            #                    data[source_target_id + '_id'].lower())
    else:
        id = data[source_target_id + '_collection_id'].lower()
        id = id.strip()

    return id

def create_neo_dict(d):
        """
        returns a dictionairy in neo4j format, so a key without string characters ('')
        :param d: dictionairy
        :return: neo dictionairy
        """
        neodict = ''
        for k, v in d.items():
            if type(v) == 'str':
                neodict = neodict + f"{k}:'{v}',"
            elif type(v) == int:
                neodict = neodict + f"{k}:{v},"
            else:
                neodict = neodict + f"{k}:'{v}',"
        neodict = neodict[:-1]

        return neodict

def upsert_node_data(data, source_target_id):
    """
    Update or insert new node data
    :param data: dictionairy with form request data
    :param source_target_id: 'source' or 'target
    :return:
    """
    props = {}
    logger.debug(data)
    for k, v in data.items():
        # filter by source or target node
        if source_target_id in k:
            # exclude property value and the *_id field. These are being handled within the procedure.
            if (source_target_id + '_property_value' not in k) and (source_target_id + '_id' not in k):

                # get node type
                if k == source_target_id + '_collection_name':
                    node_type = data[source_target_id + "_collection_name"].lower().strip()
                    # logger.debug('collection name')
                    # logger.debug(node_type)

                # get name stuff
                elif k == source_target_id + '_collection_id':
                    node_id = data[k]
                    props['name'] = node_id
                    # logger.debug('node_id {}'.format(node_id))

                # new properties
                elif source_target_id + '_property_name' in k:
                    value = source_target_id + "_property_value" + k[20:]
                    value2 = data[value]
                    if value2 != '':
                        props[v] = value2
                        # logger.debug('new property')
                        # logger.debug(v + " : " + value2)

                # all other properties
                else:
                    newkey = k[len(source_target_id) + 1:]
                    if not(newkey == 'name' and v == ''):
                        props[newkey] = v
                    # logger.debug('other property')
                    # logger.debug(newkey + " : " + v)

    # # update database
    try:
        if not node_id == '':
            # create cypher string
            neoprops = create_neo_dict(props)

            query = "merge(s:{} {{name: '{}'}}) on create set s = {{{}}} on match set  s += {{{}}}".format(node_type,
                                                                                                           node_id,
                                                                                                           neoprops,
                                                                                                           neoprops)
            # logger.debug(query)
            graph.run(query)
            logger.debug("upserting {} node {} as type {}".format(source_target_id, node_id, node_type))

    except:
        print('input error')


def upsert_edge_data(data):
    """
    insert or update a new edge.

    :param data:
    :return:
    """
    logger.debug(data)

    try:
        source_type = data['source_collection_name']
        source_id = data['source_collection_id']

        target_type = data['target_collection_name']
        target_id = data['target_collection_id']

        edge_type = data['edge_value']

        props = {}
        for k, v in data.items():
            if 'edge' in k:
                if k == 'edge_property_from_value':
                    value2 = data["edge_property_from_value"]
                    if value2 != '':
                        props['from'] = value2
                elif k == 'edge_property_to_value':
                    value2 = data["edge_property_to_value"]
                    if value2 != '':
                        props['to'] = value2
                elif 'edge_property_name' in k:
                    value2 = data["edge_property_value" + k[19:]]
                    if value2 != '':
                        props[v] = value2

        neoprops = create_neo_dict(props)

        query = """
            MATCH(NodeName1:{} {{name: '{}'}}), (NodeName2:{} {{name: '{}'}})
            MERGE(NodeName1) - [r:{} {{{}}}]->(NodeName2)
            """.format(source_type, source_id, target_type, target_id, edge_type, neoprops)

        logger.debug(query)
        graph.run(query)

    except:
        print('input error')
        return


def remove_node(data, source_target_id):
    """
    Remove a record from a collection.
    In case the collection is empty the collection will be removed

    :param data:
    :param source_target_id:
    :return:
    """

    source_type = data['source_collection_name']
    source_id = data['source_collection_id']

    query = "match(n:{} {{name:'{}'}}) detach delete n".format(source_type, source_id)
    graph.run(query)


# def update_node_id(type, old_id, new_id):
#     """
#     update a node id and also update al instances in the edge collections
#     :param type: node name
#     :param old_id: old id
#     :param new_id: new id
#     :return: nothing
#     """
#     mycol = db["node_" + type]
#
#     myquery = {"id": old_id}
#     newvalues = {"$set": {"id": new_id}}
#
#     # update node
#     mycol.update_one(myquery, newvalues)
#
#     # update edges
#     collections = db.list_collection_names()
#     for item in collections:
#         if item[:4] == 'edge':
#             coll = db[item]
#             my_source_query = {"source": old_id}
#             new_source_values = {"$set": {"source": new_id}}
#             my_target_query = {"target": old_id}
#             new_target_values = {"$set": {"target": new_id}}
#             coll.update_many(my_source_query, new_source_values)
#             coll.update_many(my_target_query, new_target_values)


def merge_nodes(data):
    """
    merge target node into source node. The source node properties will be leading.

    :param sourcetype:
    :param sourceid:
    :param targettype:
    :param targetid:
    :return: nothing
    """

    source_type = "node_" + data['source_collection_name']
    source_id = data['source_collection_id']
    target_type = "node_" + data['target_collection_name']
    target_id = data['target_collection_id']

    # handle non existing source node
    upsert_node_data(data, 'source')

    # handle null values

    # merge proc
    # if source_type == target_type:
    # remove target in node collection
    db[target_type].remove({'id': target_id})
    # replace target in edge collections
    collections = db.list_collection_names()
    for item in collections:
        if item[:4] == 'edge':
            coll = db[item]
            my_source_query = {"source": target_id}
            new_source_values = {"$set": {"source": source_id}}
            my_target_query = {"target": target_id}
            new_target_values = {"$set": {"target": source_id}}
            coll.update_many(my_source_query, new_source_values)
            coll.update_many(my_target_query, new_target_values)


def remove_key_from_collection(type, coll, key):
    """
    removes a key from a specified collection.
    keys {_id, id} cannot be removed from an node collection
    keys {_id, id, source, target} cannot be removed from an edge collection

    :param type: node or edge
    :param coll: collectiun nanme
    :param key: key name
    :return: nothinhg
    """
    mycol = db[type + '_' + coll]
    # print(mycol)

    node_exceptions = ['_id', 'id']
    edge_exceptions = ['_id', 'id', 'source', 'target']

    if type == 'node' and key not in node_exceptions:
        mycol.update_many({}, {"$unset": {key: ''}})

    elif type == 'edge' and key not in edge_exceptions:
        mycol.update_many({}, {"$unset": {key: ''}})

    # else:
    #     print('nothing removed')


