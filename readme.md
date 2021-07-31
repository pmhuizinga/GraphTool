# GraphTool

## Description
Make inventory of all entities  
Could be a knowledge graph
can be used as master data set?  
Easy to use to tool for small scale or ad-hoc graph analytics. Users should be able to add new nodes and edges fast and easy.
read data from several sources and transform into graph  
sources can be: emails, jira, confluence, word documents, etc.

## Database
main db is neo4j  
there is also need for storage of node aliases (paul, paul huizinga, mr. p huizinga, pmhuizinga, etc.)  
(or should the aliases be added to neo4j as a unique node?)

# Knowledge graph
## Steps
1. Preprocess
2. Resolve Co References, Classify entities (NER)  
   - use neuralcoref for co reference  
   - use spacy for NER
3. Extract Relations
4. Link to Knowledgebase
5. Ingest into target Knowledge Graph

## Neuralcoref library
### Install
git clone https://github.com/huggingface/neuralcoref.git  
cd neuralcoref  
pip install -r requirements.txt  
pip install -e .  

### Sample code
    doc = nlp(u'My sister has a dog. She loves him.')  
    print('All the clusters of corefering mentions in the doc')  
    print(doc._.coref_clusters)
    print(doc._.coref_clusters[1].mentions)
    print(doc._.coref_clusters[1].mentions[-1]._.coref_cluster.main)
    
    print('Unicode representation of the doc where each corefering mention is replaced by the main mention in the associated cluster.')
    print(doc._.coref_resolved)
    
    print('Scores of the coreference resolution between mentions.')
    print(doc._.coref_scores)
    
    span = doc[-1:]
    print('	Whether the span has at least one corefering mention')
    print(span._.is_coref)
    # print(span._.coref_cluster.main)
    # print(span._.coref_cluster.main._.coref_cluster)
    
    token = doc[-1]
    print(token._.in_coref)
    print(token._.coref_clusters)

## Definitions
> ### Ontology
> In computer science and information science, an ontology encompasses a representation, formal naming and definition of the categories, properties and relations between the concepts, data and entities that substantiate one, many, or all domains of discourse. More simply, an ontology is a way of showing the properties of a subject area and how they are related, by defining a set of concepts and categories that represent the subject.

> ### Taxonomy
> Taxonomy is the practice and science of categorization or classification. The word finds its roots in the Greek language τάξις, taxis (meaning 'order', 'arrangement') and νόμος, nomos ('law' or 'science').
Every academic discipline or field creates ontologies to limit complexity and organize data into information and knowledge. New ontologies improve problem solving within that domain. Translating research papers within every field is a problem made easier when experts from different countries maintain a controlled vocabulary of jargon between each of their languages.[1]
############################################# OLD #################################################
## Requirements
Easy to use to tool for small scale or ad-hoc graph analytics. Users should be able to add new nodes and edges fast and easy.
The tool should supply several analytical options, like
- shortest path to node y
- basic graph analytics: degree, centrality, betweenness
- proces analytics based on edge types
Graphical interface using d3.js  
Containerized  
Deployed in AWS  


## Database
Very basic setup. 1 'table' per node type, 1 'table' per edge type.  
tbl_node [node type name, eg. 'person']  
- node_id
- node_name
- node_property_1 etc.

tbl_edge [edge type name, eg. 'knows']    
- source_node_id  
- target_node_id  
- edge_property_1 etc.

Each table should be able to adapt to user requirements. Adding a non-existing property to a node will automatically create a new column to the table

## Input
Basic HTML setup: 
  - source node type
  - source node id (example: person name, city name, etc)
  - relation type
  - target node type
  - target node id

On selection each of the basic inputs the tool should supply suggestions.
Sample:
1. user enters field 'source node type'
2. user enters character 'p'
3. tool suggest all known node types starting with 'p', adjusting itself on each new character
4. user enters field 'source node id'
5. user enters character 'p'
6. tool suggest all known node name, of the previously selected node type, starting with 'p', adjusting itself on each new character
7. if node exists all know properties of the node will be displayed below the 2 source node fields.

Furthermore, the user should be able to add supplementary properties to the nodes and/or edges

## Visualization
- show full graph
- selection per node, show all direct relations
- selection per edge type

## Analytics
Show basic network analytics: degrees, pagerank, betweennes








