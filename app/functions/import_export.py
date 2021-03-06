import json
from py2neo import Graph, Node, NodeMatcher, Relationship
graph = Graph(host="localhost", port=7687, auth=('neo4j', 'admin'))
matcher = NodeMatcher(graph)

# todo: make new api for all nodes/edges including properties

f = 'C:\\Users\\pahuizinga\\OneDrive - Aegon\\Python\\GraphTool\\documentation\\'
nodes_url = 'http://127.0.0.1:5000/graph_nodes/node/all'
edges_url =  'http://127.0.0.1:5000/graph_edges/node/all'


def read_from_api():
    pass

def read_from_file(folderpath, nodes_file_name = 'nodes.json', edges_file_name='edges.json'):

    # read files
    # with open('C:\\Users\\pahuizinga\\OneDrive - Aegon\\Python\\GraphTool\\documentation\\nodes.json', 'r') as myfile:
    with open(folderpath + nodes_file_name, 'r') as myfile:
        node_set = myfile.read()

    nodes = json.loads(node_set)

    # with open('C:\\Users\\pahuizinga\\OneDrive - Aegon\\Python\\GraphTool\\documentation\\edges.json', 'r') as myfile:
    with open(folderpath + edges_file_name, 'r') as myfile:
        edge_set=myfile.read()
    edges = json.loads(edge_set)

    return nodes, edges

a, b = read_from_file(folderpath=f)

def write_to_files(folderpath, nodes_file_name = 'nodes.json', edges_file_name='edges.json'):

    pass

def create_nodes_in_neo4j(nodes):
    # create nodes in Neo
    for item in nodes:
        a = Node(item['type'], name=item['id'])
        graph.create(a)

def create_edges_in_neo4j(edges):
    # create edges in Neo
    for item in edges:
        NodeSource = matcher.match(name=item['source']).first()
        NodeTarget = matcher.match(name=item['target']).first()
        a = Relationship(NodeSource, item['type'], NodeTarget)
        graph.create(a)

