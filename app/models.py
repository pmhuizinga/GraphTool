from app import db
from sqlalchemy import UniqueConstraint

class Node(db.Model):
    __tablename__ = "nodes"
    __table_args__ = {'extend_existing': True}

    # columns
    id = db.Column(db.Integer(), primary_key=True)
    node_type = db.Column(db.String(64))
    node_name = db.Column(db.String(64))
    node_attr = db.Column(db.String(256))
    UniqueConstraint('node_type', 'node_name', name='uix_node_type_node_name')

    def __init__(self, node_type, node_name, node_attr):
        self.node_type = node_type
        self.node_name = node_name
        self.node_attr = node_attr


class Edge(db.Model):
    __tablename__ = "edges"
    __table_args__ = {'extend_existing': True}

    # columns
    id = db.Column(db.Integer(), primary_key=True)
    source_node = db.Column(db.Integer())
    target_node = db.Column(db.Integer())
    edge_type = db.Column(db.String(128))
    edge_attr = db.Column(db.String(256))
    UniqueConstraint('source_node', 'target_node', 'edge_type', name='uix_source_target_edge')

    def __init__(self, source_edge, target_edge, edge_type, edge_attr):
        self.source_edge = source_edge
        self.target_edge = target_edge
        self.edge_type = edge_type
        self.edge_attr = edge_attr