from app import db


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


def getCollectionKeys(collection):
    """
    Get full set of keys from a collection
    :param collection: collection name
    :return: all keys for the collection as a list
    """

    keys_list = []
    collection_list = db[collection].find()

    for document in collection_list:
        for field in document.keys():
            keys_list.append(field)
    keys_set = list(set(keys_list))

    return keys_set


def getCollectionId(collection):
    """Get full set of ids from a collection"""

    id_list = []
    coll = db[collection].find()

    for record in coll:
        id_list.append(record['id'])

    id_set = list(set(id_list))

    return id_set


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
    else:
        id = data[source_target_id + '_collection_id'].lower()

    return id


def upsert_node_data(data, source_target_id):
    """
    Update or insert new node data
    :param data: dictionoiry with form request data
    :param source_target_id: 'source' or 'target
    :return:
    """
    # todo: when changing an id a new node is created...should be fixed
    props = {}
    for k, v in data.items():
        # filter by source or target node
        if source_target_id in k:
            # exclude property value and the *_id field. These are being handled within the procedure.
            if (source_target_id + '_property_value' not in k) and (source_target_id + '_id' not in k):
                # get node type
                if k == source_target_id + '_collection_name':
                    node_type = 'node_' + data[source_target_id + "_collection_name"].lower()

                # get id stuff
                elif k == source_target_id + '_collection_id':
                    props['id'] = get_node_id(data, source_target_id)
                    node_id = props['id'].lower()

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
    source_id = get_node_id(data, 'source')
    target_id = get_node_id(data, 'target')

    if source_id == '' or target_id == '':
        return

    props = {'source': source_id, 'target': target_id}

    # todo: handle null values in nodes
    # todo: add edge properties
    for k, v in data.items():
        if 'edge' in k:
            if k == 'edge_value':
                value = data[k]
                if value != '':
                    db['edge_' + v].update_one(props, {"$set": props}, upsert=True)
                    print("upserting edge {} with source {} and target {} in collection {}".format(v, source_id,
                                                                                                   target_id, v))


def remove_node(data, source_target_id):
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

    # 2 remove node
    db[node_type].remove({'id': id})
    # todo: if node is completely empty -> remove node

