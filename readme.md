# GraphTool

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
Show basic network analytics: degrees, pagerank, betweenness 



