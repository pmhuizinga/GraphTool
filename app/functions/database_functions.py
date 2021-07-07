# from app import db
from app import graph


def add_collection_identifier(in_list, type):
    """
    add 'node_' or 'edge_' to callection name
    :return: list
    """
    out_list = [type + '_' + x for x in in_list]

    return out_list


def drop_collection_identifier(in_list, type):
    """
    drop 'node_' or 'edge_' from callection name
    :return: list
    """
    out_list = [x[5:] for x in in_list if x[:4] == type]

    return out_list


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
        print('matching result {} for {} is {} (character match: {}, length match {})'.format(input, collection,
                                                                                              int(result * 100),
                                                                                              set_match, len_match))


def getCollectionKeys(type, collection):
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
    print(result)
    list = [n[0] for n in result]
    all_keys = set().union(*(d.keys() for d in list))
    keys = [k for k in all_keys]

    #
    #
    # keys_list = []
    # collection_list = db[collection].find()
    #
    # for document in collection_list:
    #     for field in document.keys():
    #         keys_list.append(field)
    # keys_set = list(set(keys_list))

    # return keys_set
    return keys


def getCollectionId(collection):
    """Get full set of ids from a collection"""

    id_list = []

    query = "match(a: {}) return a.name".format(collection)
    result = graph.run(query).to_ndarray()
    list = [n[0] for n in result]
    # coll = db[collection].find()
    #
    # for record in coll:
    #     id_list.append(record['id'])
    #
    # id_set = list(set(id_list))

    # return id_set
    return list

def getCollectionDetail(type, collection, name):
    """Get full set of ids from a collection"""

    id_list = []
    # "match(a: {}) where a.name = '{}' return a".format(collection, name)
    query = "match(a: {}) where a.name = '{}' return a".format(collection, name)
    a = graph.evaluate(query)

    result = {}
    if a is None:
        return result

    for k in a.keys():
        result[k] = a[k]

    # query = "match(a: {}) where a.name = '{}' return a".format(collection, name)
    # result = graph.run(query).to_ndarray()
    # list = [n[0] for n in result]
    # result = [x for x in list[0]]

    # query = "match(a: {}) where a.name = '{}' return a".format(collection, name)
    # a = graph.evaluate(query)
    # for k in a.keys():

    # coll = db[collection].find()
    #
    # for record in coll:
    #     id_list.append(record['id'])
    #
    # id_set = list(set(id_list))

    # return id_set
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
            # update node id change in all edges
            if data[source_target_id + '_id'].lower() != data[source_target_id + '_collection_id'].lower():
                update_node_id(data[source_target_id + "_collection_name"].lower(), data[source_target_id + '_collection_id'].lower(), data[source_target_id + '_id'].lower())
    else:
        id = data[source_target_id + '_collection_id'].lower()
        id = id.strip()

    return id


def upsert_node_data(data, source_target_id):
    """
    Update or insert new node data
    :param data: dictionoiry with form request data
    :param source_target_id: 'source' or 'target
    :return:
    """
    props = {}
    for k, v in data.items():
        # filter by source or target node
        if source_target_id in k:
            # exclude property value and the *_id field. These are being handled within the procedure.
            if (source_target_id + '_property_value' not in k) and (source_target_id + '_id' not in k):
                # get node type
                if k == source_target_id + '_collection_name':
                    node_type = 'node_' + data[source_target_id + "_collection_name"].lower().strip()

                # get id stuff
                elif k == source_target_id + '_collection_id':
                    props['id'] = get_node_id(data, source_target_id)
                    node_id = props['id'].lower()
                    print(node_id)

                # new properties
                elif source_target_id + '_property_name' in k:
                    value = source_target_id + "_property_value" + k[20:]
                    value2 = data[value]
                    if value2 != '':
                        props[v] = value2

                # all other properties
                else:
                    newkey = k[len(source_target_id) + 1:]
                    props[newkey] = v
    # update database
    try:
        if not node_id == '':
            db[node_type].update_one({'id': node_id}, {"$set": props}, upsert=True)
            print("upserting {} node {} in collection {}".format(source_target_id, node_id, node_type))
    except:
        print('input error')


def upsert_edge_data(data):
    """
    insert or update a new edge.

    :param data:
    :return:
    """
    source_id = get_node_id(data, 'source')
    target_id = get_node_id(data, 'target')

    if source_id == '' or target_id == '':
        return

    props = {'source': source_id, 'target': target_id}

    # todo: handle null values in nodes
    for k, v in data.items():
        if 'edge' in k:
            print(k)
            if k == 'edge_value':
                value = data[k]
            elif k == 'edge_property_from_value':
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

    if value != '':
        db['edge_' + value].update_one(props, {"$set": props}, upsert=True)
        print("upserting edge {} with source {} and target {} in collection {}".format(v, source_id,
                                                                                           target_id, v))


def remove_node(data, source_target_id):
    """
    Remove a record from a collection.
    In case the collection is empty the collection will be removed

    :param data:
    :param source_target_id:
    :return:
    """
    node_type = 'node_' + data[source_target_id + "_collection_name"].lower()
    id = get_node_id(data, source_target_id)

    print(node_type, id)
    # 1 remove from edges
    collections = db.list_collection_names()

    edge_list = []
    for item in collections:
        if item[:4] == 'edge':
            db[item].delete_many({'source': id})
            db[item].delete_many({'target': id})

    # remove node
    db[node_type].remove({'id': id})

    # if collection is empty: remove collection
    if db[node_type].count_documents({}) == 0:
        db[node_type].drop()



def update_node_id(type, old_id, new_id):
    """
    update a node id and also update al instances in the edge collections
    :param type: node name
    :param old_id: old id
    :param new_id: new id
    :return: nothing
    """
    mycol = db["node_" + type]

    myquery = {"id": old_id}
    newvalues = {"$set": {"id": new_id}}

    # update node
    mycol.update_one(myquery, newvalues)

    # update edges
    collections = db.list_collection_names()
    for item in collections:
        if item[:4] == 'edge':
            coll = db[item]
            my_source_query = {"source": old_id}
            new_source_values = {"$set": {"source": new_id}}
            my_target_query = {"target": old_id}
            new_target_values = {"$set": {"target": new_id}}
            coll.update_many(my_source_query, new_source_values)
            coll.update_many(my_target_query, new_target_values)


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
    print(mycol)

    node_exceptions = ['_id', 'id']
    edge_exceptions = ['_id', 'id', 'source', 'target']

    if type == 'node' and key not in node_exceptions:
        mycol.update_many({}, {"$unset": {key: ''}})

    elif type == 'edge' and key not in edge_exceptions:
        mycol.update_many({}, {"$unset": {key: ''}})

    else:
        print('nothing removed')
