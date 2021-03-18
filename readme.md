# GraphTool

## Requirements
Easy to use to tool for small scale graph analytics. Users should be able to add new nodes and edges fast and easy.
The tool should supply several analytical options, like
- shortest path to node y
- basic graph analytics: degree, centrality, betweenness
- proces analytics based on edge types
Graphical interface using d3.js
Containerized 
Deployed in AWS


## Database
Very basic setup  
tbl_node
- node_id
- node_name

tbl_relation
- relation_id
- relation_name

tbl_node_relation
- node_rel_id
- source_node_id
- relation_id
- target_node_id

Each table should be able to adapt to user requiremens. Adding a non-existing property to a node will automatically create a new column to the table

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

## Query

## Modify and delete


# Default Flask site for database interface

The idea is to have a default flask web interface for a transactional database.  
Users should only have to modify the datamodel (models.py) and the forms in order to easily create an interface.
Ideally the forms should be generated automatically based on the datamodel.

### SETUP

- add virtual environment
- add database connection in config.py, class Config (SQLALCHEMY_DATABASE_URI)
- create models (tables) in app/models.py
- run create database commands:

  
    ../CRUD/flask db init
    ../CRUD/flask db migrate
    ../CRUD/flask db upgrade


- add forms data (corresponding to models.py) in case of data entry forms
- adjust views.py for handling CRUD transactions

### DATABASE CHANGES 

on initiate flask website first create the database. This is based on models.py
in terminal run:

    ../default_flask_ui/flask db init
    ../default_flask_ui/flask db migrate
    ../default_flask_ui/flask db upgrade

flask db init, this will set up a migration directory in the project and a alembic table in the database (for storing version numbers)  
flask db migrate, this will extract all the settings from models.py  
flask db upgrade, this will make the actual changes to the database  

in case of database changes run:  

    ../default_flask_ui/flask db migrate
    ../default_flask_ui/flask db upgrade
    
Migrate will extract all the settings from models.py  
Upgrade will make the actual changes to the database
