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
        len_match = min(len(input), len(collection)) / max(len(input),len(collection))
        result = set_match * len_match
        print('matching result {} for {} is {} (character match: {}, lenght match {})'.format(input, collection, int(result*100), set_match, len_match))

print(find_matching_collections('cas'))