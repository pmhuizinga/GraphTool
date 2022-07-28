from app import db
import ast
# from app import graph
from app import models
import logging
from sqlalchemy import create_engine

logger = logging.getLogger(__name__)  # initialize logger
logger.handlers = []
c_handler = logging.StreamHandler()  # Create handlers
c_format = logging.Formatter('%(levelname)s - %(message)s')
c_handler.setFormatter(c_format)  # Create formatters and add it to handlers
logger.addHandler(c_handler)  # Add handlers to the logger
logger.setLevel(logging.DEBUG)


# engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
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

def get_node_type_attributes(node_edge, node_type):
    """
    retrieve a set of all attributes from a specified node_type
    """
    result = models.Node.query.filter_by(node_type=node_type)
    k = []
    for node in result:
        for key in ast.literal_eval(node.node_attr).keys():
            k.append(key)


    return list(set(k))

def get_collection_keys(node_edge, node_type):
    """
    retrieve a set of all attributes from a specified node_type
    """
    # todo: add code for edges
    result = models.Node.query.filter_by(node_type=node_type).first()
    k = []
    for key in ast.literal_eval(result.node_attr).keys():
        k.append(key)

    return k

    # for node in result:
    #     for key in ast.literal_eval(node.node_attr).keys():
    #         k.append(key)
    #
    # k.remove('node_id')
    # return list(set(k))
#
# def get_collection_keys(type, collection):
#     """
#     Get full set of keys from a collection
#     :param collection: collection name
#     :return: all keys for the collection as a list
#     """
#     if type == 'node':
#         query = "match (n:{}) return properties(n)".format(collection)
#     elif type == 'edge':
#         query = "match(a)-[r:{}]-(b) return properties(r)".format(collection)
#
#     result = graph.run(query).to_ndarray()
#     list = [n[0] for n in result]
#     all_keys = set().union(*(d.keys() for d in list))
#     keys = [k for k in all_keys]
#
#     return keys


def get_collection_id(collection):
    """Get full set of ids from a collection"""

    lst = []
    # todo: replace session with standard sqlalchemy query
    for value in db.session.query(models.Node.node_id).filter_by(node_type=collection):
        lst.append(value[0])

    return lst

def get_collection_detail(type, collection, name):
    """
    Get full set of ids from a collection
    """
    print(type, collection, name)
    a = models.Node.query.filter_by(node_type=collection, node_id=name).first()

    result = {}
    if a is None:
        return result
    else:
        print(a.node_attr)
        return ast.literal_eval(a.node_attr)



# def get_collection_detail(type, collection, name):
#     """Get full set of ids from a collection"""
#
#     # "match(a: {}) where a.name = '{}' return a".format(collection, name)
#     query = "match(a: {}) where a.name = '{}' return a".format(collection, name)
#     a = graph.evaluate(query)
#
#     result = {}
#     if a is None:
#         return result
#
#     for k in a.keys():
#         result[k] = a[k]
#
#     return result


def get_node_type():
    """
    retrieve a list of all node types
    """
    # lst = list(set([x.node_type for x in Node.query.distinct(Node.node_type)]))
    lst = list(set([x.node_type for x in models.Node.query.distinct(models.Node.node_type)]))
    # for value in db.session.query(models.Node.node_type).distinct():
    #     lst.append(value[0])
    #
    # print(lst)
    # print(list(set([x.node_type for x in models.Node.query.distinct(models.Node.node_type)])))
    return lst


def get_edge_names():
    """
    get all edge names
    """
    lst = []
    # todo: remove session query,  replace with models.edge.query...etc
    for value in db.session.query(models.Edge.edge_type).distinct():
        lst.append(value[0])

    return lst


def get_edge_relations(edge):
    """
    return a list of edges including sources and targets
    :param edge: edge label
    """
    # query = "MATCH p=(a)-[r:{}]->(b) RETURN a.name as source,type(r), b.name as target".format(edge)
    query = "MATCH p=(a)-[r:{}]->(b) RETURN a.name as source, type(r), b.name as target, labels(a) as source_type, labels(b) as target_type".format(
        edge)
    query_result = graph.run(query).to_ndarray(dtype=object).tolist()
    result = [[i[0] if isinstance(i, list) else i for i in x] for x in query_result]
    # query_result = graph.run(query).to_ndarray(dtype=object)
    # for idx, item in enumerate(query_result):
    #     if isinstance(item, list):
    #         query_result[idx] = item[0]
    #  [i[0] if isinstance(i, list) else i for i in t for i in i]

    return result


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


# def create_neo_dict(d):
#     """
#     returns a dictionairy in neo4j format, so a key without string characters ('')
#     :param d: dictionairy
#     :return: neo dictionairy
#     """
#     neodict = ''
#     for k, v in d.items():
#         if type(v) == 'str':
#             neodict = neodict + f"{k}:'{v}',"
#         elif type(v) == int:
#             neodict = neodict + f"{k}:{v},"
#         else:
#             neodict = neodict + f"{k}:'{v}',"
#     neodict = neodict[:-1]
#
#     return neodict


def upsert_node_data(data, source_target_id):
    """
    Update or insert new node data
    :param data: dictionairy with form request data
    :param source_target_id: 'source' or 'target
    :return:
    """
    props = {}
    logger.debug(data)
    if not data:
        print("data is empty")
        return None

    for k, v in data.items():
        # filter by source or target node
        if source_target_id in k:
            # exclude property value and the *_id field. These are being handled within the procedure.
            if (source_target_id + '_property_value' not in k) and (source_target_id + '_id' not in k):

                # get node type
                if k == source_target_id + '_collection_name':
                    node_type = data[source_target_id + "_collection_name"].lower().strip()
                    props['node_type'] = node_type
                    logger.debug('collection name')
                    logger.debug(node_type)

                # get id
                elif k == source_target_id + '_collection_id':
                    node_id = data[k]
                    props['node_id'] = node_id
                    props['name'] = node_id
                    logger.debug('node_id {}'.format(node_id))

                # new properties
                elif source_target_id + '_property_name' in k:
                    value = source_target_id + "_property_value" + k[20:]
                    value2 = data[value]
                    if value2 != '':
                        props[v] = value2
                        logger.debug('new property')
                        logger.debug(v + " : " + value2)

                # all other properties
                else:
                    newkey = k[len(source_target_id) + 1:]
                    if not (newkey == 'name' and v == ''):
                        props[newkey] = v
                    logger.debug('other property')
                    logger.debug(newkey + " : " + v)

    # # update database
    try:
        if not node_id == '':

            logger.debug('props')
            logger.debug(props)
            logger.debug('my node')
            my_node = db.session.query(models.Node).filter_by(node_type=node_type, node_id=node_id).first()
            logger.debug(my_node)

            if my_node:
                # if node exists
                logger.debug('my_node found')
                my_node.node_type = node_type
                my_node.node_id = node_id
                my_node.node_attr = str(props)
                logger.debug('add existing node to db')
                db.session.add(my_node)
                logger.debug('commit')
                try:
                    db.session.commit()
                except:
                    db.session.rollback()

            else:
                # new node
                logger.debug('add new node to db')
                db.session.add(models.Node(node_type, node_id, str(props)))
                try:
                    db.session.commit()
                except:
                    db.session.rollback()

            logger.debug("upserting {} node {} as type {}".format(source_target_id, node_id, node_type))

            print(node_type, node_id)

            return get_id(node_type,node_id)

        else:
            # no node id
            return None
    except:
        print('input error')
        raise

def get_id(node_type, node_id):
    """
    get the id for a specific node
    """
    id = db.session.query(models.Node.id).filter_by(node_type=node_type, node_id=node_id).first()[0]

    return id

def upsert_edge_data(source_node_id, target_node_id, data):
    """
    insert or update a new edge.

    :param data:
    :return:
    """
    logger.debug(data)

    try:
        # source_type = data['source_collection_name']
        # source_id = data['source_collection_id']
        #
        # target_type = data['target_collection_name']
        # target_id = data['target_collection_id']

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

        logger.debug('add new edge to db')
        db.session.add(models.Edge(source_node_id, target_node_id, edge_type, str(props)))
        try:
            db.session.commit()
        except:
            db.session.rollback()

        logger.debug("upserting edge with type {}".format(edge_type))

    except:
        print('edge input error')
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
    keys {name} cannot be removed from an node
    keys {from, to} cannot be removed from an edge

    :param type: node or edge
    :param coll: collectiun nanme
    :param key: key name
    :return: nothinhg
    """

    node_query = "MATCH (m:{}) REMOVE m.{} RETURN m".format(coll, key)
    edge_query = ""

    node_exceptions = ['name']
    edge_exceptions = ['from', 'to']

    if type == 'node' and key not in node_exceptions:
        graph.run(node_query)
    elif type == 'edge' and key not in edge_exceptions:
        graph.run(edge_query)
