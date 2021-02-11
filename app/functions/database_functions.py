from app import db

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
    """Get full set of keys from a collection"""

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

