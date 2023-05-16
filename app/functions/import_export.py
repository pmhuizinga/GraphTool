import requests
import ast
import os
from time import sleep
import pandas as pd
from app.functions import log
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *

basedir = os.path.abspath(os.path.dirname(__file__))

# create flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'graph.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

# excel_folder = 'C:\\Users\\pahuizinga\\OneDrive - Aegon\\Desktop\\'
excel_folder = 'C:\\Users\\PaulMarjanIlseMeike\\Dropbox\\Paul\\DataScience\\Projects\\WIJ\\'
# excel_file = 'manual_inventory.xlsx'
excel_file = 'proces_inventory.xlsx'
excel_sheet = 'ontology'

# sqlite init to app
db = SQLAlchemy(app)
meta = MetaData()
meta.create_all(engine)


class Node(db.Model):
    __tablename__ = "nodes"
    __table_args__ = {'extend_existing': True}

    # columns
    id = db.Column(db.Integer(), primary_key=True)
    node_type = db.Column(db.String(64))
    node_id = db.Column(db.String(64))
    node_attr = db.Column(db.String(256))
    UniqueConstraint('node_type', 'node_id', name='uix_node_type_node_id')

    def __init__(self, node_type, node_id, node_attr):
        self.node_type = node_type
        self.node_id = node_id
        self.node_attr = node_attr


class Edge(db.Model):
    __tablename__ = "edges"
    __table_args__ = {'extend_existing': True}

    # columns
    id = db.Column(db.Integer(), primary_key=True)
    # source_node_id = db.Column(db.Integer())
    # target_node_id = db.Column(db.Integer())
    source_node_id = db.Column(db.Integer, db.ForeignKey(Node.id), nullable=False)
    target_node_id = db.Column(db.Integer, db.ForeignKey(Node.id), nullable=False)
    edge_type = db.Column(db.String(128))
    edge_attr = db.Column(db.String(256))
    source_node_id_R = db.relationship('Node', foreign_keys='Edge.source_node_id')
    target_node_id_R = db.relationship('Node', foreign_keys='Edge.target_node_id')
    UniqueConstraint('source_node', 'target_node', 'edge_type', name='uix_source_target_edge')

    def __init__(self, source_node_id, target_node_id, edge_type, edge_attr):
        self.source_node_id = source_node_id
        self.target_node_id = target_node_id
        self.edge_type = edge_type
        self.edge_attr = edge_attr

def upsert_node_data(data, source_target_id):
    """
    Update or insert new node data
    :param data: dictionairy with form request data
    :param source_target_id: 'source' or 'target
    :return:
    """
    props = {}
    log.logger.debug(data)
    if not data:
        print("data is empty")
        return None

    for k, v in data.items():
        # filter by source or target node
        if source_target_id in k:
            # exclude property value and the *_id field. These are being handled within the procedure.
            if (source_target_id + '_property_value' not in k) and (source_target_id + '_id' not in k):

                # get node type
                if k == source_target_id + '_collection_name':
                    node_type = data[source_target_id + "_collection_name"].lower().strip()
                    props['node_type'] = node_type
                    log.logger.debug('collection name')
                    log.logger.debug(node_type)

                # get id
                elif k == source_target_id + '_collection_id':
                    node_id = data[k]
                    props['node_id'] = node_id
                    props['name'] = node_id
                    log.logger.debug('node_id {}'.format(node_id))

                # new properties
                elif source_target_id + '_property_name' in k:
                    value = source_target_id + "_property_value" + k[20:]
                    value2 = data[value]
                    if value2 != '':
                        props[v] = value2
                        logging_settings.logger.debug('new property')
                        log.logger.debug(v + " : " + value2)

                # all other properties
                else:
                    newkey = k[len(source_target_id) + 1:]
                    if not (newkey == 'name' and v == ''):
                        props[newkey] = v
                    log.logger.debug('other property')
                    log.logger.debug(newkey + " : " + v)

    try:
        if not node_id == '':

            logging_settings.logger.debug('props')
            logging_settings.logger.debug(props)
            logging_settings.logger.debug('my node')
            my_node = db.session.query(Node).filter_by(node_type=node_type, node_id=node_id).first()
            logging_settings.logger.debug(my_node)

            if my_node:
                # if node exists
                log.logger.debug('my_node found')
                my_node.node_type = node_type
                my_node.node_id = node_id
                my_node.node_attr = str(props)
                logging_settings.logger.debug('add existing node to db')
                db.session.add(my_node)
                logging_settings.logger.debug('commit')
                try:
                    db.session.commit()
                except:
                    db.session.rollback()

            else:
                # new node
                logging_settings.logger.debug('add new node to db')
                db.session.add(Node(node_type, node_id, str(props)))
                try:
                    db.session.commit()
                except:
                    db.session.rollback()

            log.logger.debug(
                "upserting {} node {} as type {}".format(source_target_id, node_id, node_type))

            print(node_type, node_id)

            return None

        else:

            return None
    except:
        print('input error')
        raise


def upsert_edge_data(source_node_id, target_node_id, data):
    """
    insert or update a new edge.

    :param data:
    :return:
    """
    log.logger.debug(data)

    try:

        log.logger.debug('add new edge to db')
        db.session.add(Edge(source_node_id, target_node_id, edge_type, str(props)))
        try:
            db.session.commit()
        except:
            db.session.rollback()

        logging_settings.logger.debug("upserting edge with type {}".format(edge_type))

    except:
        print('edge input error')
        return


# read excel
def read_data(path_name, file_name, sheet_name):
    '''
    :param file: filename including path
    :param sheet: sheetname
    :return: dataframe
    '''
    # try:
    frame = pd.read_excel(path_name + file_name, sheet_name=sheet_name)
    frame['node_attr'] = frame['node_attr'].fillna('no attributes')
    # except:
    #     print("file not found")

    return frame


def create_nodes(df):

    for node_type, node_id, node_attributes in zip(df['node_type'], df['node_id'], df['node_attr'].astype(str)):

        if not node_attributes == 'no attributes':
            node_attributes_dict = ast.literal_eval(node_attributes)
        else:
            node_attributes_dict = {}

        node_attributes_dict['node_type'] = node_type
        node_attributes_dict['node_id'] = node_id
        # node_attributes_dict['name'] = node_id
        print('type: {}, id: {}, attr: {}'.format(node_type, node_id, str(node_attributes_dict)))
        db.session.add(Node(node_type, node_id, str(node_attributes_dict)))
        try:
            db.session.commit()
            print('node {} committed'.format(node_id))
        except:
            db.session.rollback()
            print('node {} NOT committed'.format(node_id))

    return None


def get_node_id(node_type, node_id):
    """
    get numeric node id from node table based on node_type & node_id unique combination
    """
    x = Node.query.filter_by(node_type=node_type, node_id=node_id).first()
    return x.id


def create_edges(df):
    df = df.dropna(subset=['edges'])
    for node_type, node_id, edges in zip(df['node_type'], df['node_id'], df['edges']):
        source_node_id = get_node_id(node_type, node_id)
        for edge in edges.split(";"):
            log.logger.debug('edge upsert {}'.format(edge))
            d = edge.split("|")
            target_node_id = get_node_id(d[1], d[2])
            db.session.add(Edge(source_node_id, target_node_id, d[0], ''))
            try:
                db.session.commit()
            except:
                db.session.rollback()

    return None

def database_clear():
    Node.query.delete()
    Edge.query.delete()
    db.session.commit()
    sleep(3)


def read_from_api(url):
    """
    read api data and return as json file
    """
    r = requests.get(url)
    data = r.json()
    return data


def read_manual_data(clear_database=False):

    if clear_database:
        database_clear()

    df = read_data(excel_folder, excel_file, excel_sheet)
    create_nodes(df)
    create_edges(df)
