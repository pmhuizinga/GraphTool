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
        print('matching result {} for {} is {} (character match: {}, lenght match {})'.format(input, collection,
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
