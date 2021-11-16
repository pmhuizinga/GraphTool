import pandas as pd
from py2neo import Graph
import spacy
from spacy.matcher import PhraseMatcher
import itertools
import logging

logger = logging.getLogger(__name__)  # initialize logger
logger.handlers = []
c_handler = logging.StreamHandler()  # Create handlers
c_format = logging.Formatter('%(levelname)s - %(message)s')
c_handler.setFormatter(c_format)  # Create formatters and add it to handlers
logger.addHandler(c_handler)  # Add handlers to the logger
logger.setLevel(logging.INFO)

# set spacy properties
nlp = spacy.load("en_core_web_sm")
# use 'lower' to create case insensitive matches
matcher = PhraseMatcher(nlp.vocab, attr="LOWER")

graph = Graph(host="localhost", port=7687, auth=('neo4j', 'admin'))

txt = "Aegon asset management is part of aegon"

doc = nlp(txt)


def read_from_neo4j():
    """
    # todo: selection should come from the API instead of a neo query
    """
    query = "match(n)-[:has_alias]-(a) return labels(n) as nodetype, a.name as name, labels(a) as node2"
    df = pd.DataFrame.from_dict(graph.run(query).data(), orient='columns')

    return df


def get_parentnode_from_neo4j(nodetype, nodename):
    """
    description
    """
    # remove space after comma
    nodename = nodename.replace(", ", ",")
    query = "match (n:{})-[:has_alias]-(a:alias) where a.name = '{}' return n.name as name".format(nodetype, nodename)
    logger.debug('nodetype: {}, nodename: {}'.format(nodetype,nodename))
    logger.debug('result: {}'.format(graph.run(query).data()[0]['name']))

    return graph.run(query).data()[0]['name']


def prepare_neo4j_dataframe(df):
    """
    remove alias nodes from dataframe and drop duplicates
    param df: dataframe
    return: dataframe
    """
    df.nodetype = [a[0] for a in df.nodetype]
    df.node2 = [a[0] for a in df.node2]
    df = df[df.nodetype != 'alias']
    df.drop(columns=['node2'], inplace=True)
    df.drop_duplicates(inplace=True)

    return df


def remove_duplicates_from_list(lst):
    lst.sort()
    output = list(k for k, _ in itertools.groupby(lst))
    return output


def populate_matcher(df):
    """
    description
    """
    for nodetype in df.nodetype.unique():
        df_selection = df[df.nodetype == nodetype]
        nodelist = df_selection.name.to_list()
        patterns = [nlp.make_doc(name) for name in nodelist]
        matcher.add(nodetype, patterns)


def get_entities_from_text():
    """
    get entiaties and entity typing from text
    """
    matches = matcher(doc)
    result_list = []
    for match_id, start, end in matches:
        rule_id = nlp.vocab.strings[match_id]
        span = doc[start:end]
        result = [rule_id, span.text.lower()]
        result_list.append(result)

    return remove_duplicates_from_list(result_list)


def get_cleansed_entities_from_text(txt):
    lst = get_entities_from_text()
    newlist = []
    for idx, item in enumerate(lst):
        new_item_name = get_parentnode_from_neo4j(item[0], item[1])
        newlist.append([item[0], new_item_name])

    return remove_duplicates_from_list(newlist)


def get_missing_entities():
    missing_entity_list = []
    existing_entity_list = df.name.to_list()
    for entity in doc.ents:
        if entity.text.lower() not in existing_entity_list:
            if entity.label_ not in ['DATE', 'TIME', 'CARDINAL', 'ORDINAL']:
                missing_entity_list.append([entity.label_, entity.text])

    return remove_duplicates_from_list(missing_entity_list)


df = read_from_neo4j()
df = prepare_neo4j_dataframe(df)
populate_matcher(df)
x = get_cleansed_entities_from_text(txt)
y = get_missing_entities()

print('found known entities')
[print(x) for x in x]
print(60*'-')
print('found unknown entities')
[print(y) for y in y]
