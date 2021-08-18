from py2neo import Graph, Node, Relationship, NodeMatcher
from py2neo.matching import *

graph = Graph(host="localhost", port=7687, auth=('neo4j', 'admin'))
matcher = NodeMatcher(graph)

nodes = NodeMatcher(graph)


# functions
def truncate_database():
    graph.delete_all()

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


def return_parent_node_name(name, node_type):
    """
    Returns the parent node name for an alias node
    """
    if node_type == 'alias':
        return name
    else:
        query = "match(n:`{}`) where n.name = '{}' return count(n) as count".format(node_type, name)
        count = graph.run(query).data()[0]['count']
        if count > 0:
            return name
        else:
            query = "match(s:`alias`) where s.name = '{}' match (p:`{}`)-[:has_alias]-(s) return p.name as name".format(
                name, node_type)
            return graph.run(query).data()[0]['name']


def add_node(node_type, properties):
    """
    if the node or the alias does not exist: add new node
    if the node exists: add new properties or update properties (?)
    if the alias exists: add new properties or update properties in parent node
    """
    # key 'name' has to be in properties
    if not 'name' in properties:
        print('no name key found in properties')
        return

    name_value = properties['name']
    name_key = {'name': name_value}

    properties_exluding_name = properties.copy()
    del properties_exluding_name['name']
    # print('properties: {}'.format(properties))
    # print('properties_exluding_name: {}'.format(properties_exluding_name))

    query = "match(s:`alias`) where s.name = '{}' match (p:`{}`)-[:has_alias]-(s) return count(p) as count".format(name_value, node_type)
    output = graph.run(query).data()
    count = output[0]['count']
    # if the alias already exists for this node type...
    if count > 0:

        if len(properties_exluding_name) > 0:

            query = "match(s:`alias`) where s.name = '{}' match (p:`{}`)-[:has_alias]-(s) set p += {{{}}} return count(p) as count, p.name as name".format(
                name_value,
                node_type,
                create_neo_dict(properties_exluding_name))
            # print(query)
            output = graph.run(query).data()
            # print(output)
            count_level_2 = output[0]['count']
            # node_name = output[0]['name']
            if count_level_2 > 0:
                print('alias found, properties added to parent node')
                return

        else:
            query = "match(s:`alias`) where s.name = '{}' match (p:`{}`)-[:has_alias]-(s) return count(p) as count".format(
                name_value,
                node_type)

            # print(query)
            output = graph.run(query).data()
            count = output[0]['count']
            # print(output)
            if count > 0:
                print('alias found, no new properties added to parent node')
                return

    else:
        # create or update parent node
        query = "merge(s:`{}` {{{}}}) on create set s = {{{}}} on match set  s += {{{}}} return count(s) as count".format(
            node_type,
            create_neo_dict(name_key),
            create_neo_dict(properties),
            create_neo_dict(properties))
        # print(query)
        output = graph.run(query).data()
        # print(output)
        # create new alias for parent node
        if not node_type == 'alias':
            query = "match(s:`alias`) where s.name = '{}' return count(s) as count".format(name_value)
            output = graph.run(query).data()
            count = output[0]['count']
            # print(output)
            if count == 0:
                query = "create(a:alias {{name:'{}'}})".format(name_value)
                # print(query)
                graph.run(query)
                # print('new alias {} created'.format(name_value))
            add_relation2(node_type, name_value, 'alias', name_value, 'has_alias')


def add_relation2(source_type, source_name, target_type, target_name, relation):
    node_source_name = return_parent_node_name(source_name, source_type)
    # print(NodeSourceName)
    node_target_name = return_parent_node_name(target_name, target_type)
    # print(NodeTargetName)
    node_source = nodes.match(source_type, name=node_source_name).first()
    node_target = nodes.match(target_type, name=node_target_name).first()
    a = Relationship(node_source, relation, node_target)
    graph.create(a)

#%%
"""
SITUATION 0: basic setting with one node and one alias
Expected behaviour: 
    None
"""
truncate_database()
# create starter node
print('_' * 60)
print('SITUATION 0: add initial person and alias node')
print('_' * 60)
add_node('person', {'name': 'huizinga, paul'})
add_node('alias', {'name': 'pmhuizinga'})
add_node('alias', {'name': 'phuizinga'})
add_node('alias', {'name': 'paul huizinga'})
add_relation2('person', 'huizinga, paul', 'alias', 'pmhuizinga', 'has_alias')
add_relation2('person', 'huizinga, paul', 'alias', 'phuizinga', 'has_alias')
add_relation2('person', 'huizinga, paul', 'alias', 'paul huizinga', 'has_alias')
# starternode = Node('person', name='huizinga, paul')
# graph.create(starternode)
# %%
"""
SITUATION 1: node already exists
Expected behaviour: 
    No new node will be created. 
    Potential node properties will be added
    Relations will be related to the existing parent node
"""
print('_' * 60)
print('SITUATION 1: node already exists')
print('_' * 60)
add_node('person', {'name': 'huizinga, paul', 'hair': 'blond'})

"""
SITUATION 2: alias already exists
Expected behaviour: 
    No new node will be created
    Potential node properties will be added
"""
print('_' * 60)
print('SITUATION 2: alias already exists')
print('_' * 60)
print('add alias node with extra properties')
add_node('person', {'name': 'pmhuizinga', 'gender': 'female'})

"""
SITUATION 3: alias already exists, but has different properties from the parent node
Expected behaviour: 
    No new node will be created
    New node properties will be overwritten
"""
print('_' * 60)
print('SITUATION 2: alias already exists')
print('_' * 60)
print('add alias node with extra properties')
add_node('person', {'name': 'pmhuizinga', 'gender': 'male'})

"""
SITUATION 4: new relation is added to existing alias
Expected behaviour: 
    
"""
print('_' * 60)
print('SITUATION 2: alias already exists')
print('_' * 60)
print('add alias node with extra properties')
add_node('person', {'name': 'algra, pieter'})
add_relation2('person', 'pmhuizinga', 'person', 'algra, pieter', 'knows')

"""
SITUATION 5: two nodes with the same alias
Expected behaviour: 
    
"""
# add_node('party', {'name': 'aam'})
# add_relation2('person', 'pmhuizinga', 'party', 'aam', 'works_for')
# add_node('organisation', {'name': 'aam'})
# add_relation2('person', 'algra, pieter', 'party', 'aam', 'works_for')
# add_relation2('person', 'huizinga, paul', 'organisation', 'aam', 'works_for')

"""
SITUATION 6: similar client and mandate codes with similare reports
Expected behaviour: 

"""
# truncate_database()
# add_node('client', {'name': 'pf kpn'})
# add_node('mandate', {'name': 'kpn'})
# add_node('report', {'name': 'monthly report'})
# add_relation2('client', 'pf kpn', 'report', 'monthly report', 'recieves')
# add_relation2('mandate', 'kpn', 'report', 'monthly report', 'recieves')
