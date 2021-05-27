from flask import request, render_template, redirect, url_for, jsonify
from app import db
from . import home
from bson.json_util import dumps
from bson.objectid import ObjectId
import logging
import requests
from app.functions import database_functions as dbf
from app.functions import analytic_functions as af

# logging setup
logging.basicConfig(filename='log/homelog.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.NOTSET)

logger = logging.getLogger(__name__)  # initialize logger
logger.handlers = []


# API's
# @home.route('/graph_nodes/<node>')
# def get_graph_nodes(node):
#     return jsonify(af.get_all_nodes_list(node=node))


@home.route('/graph_nodes/<base>/<id>')
def get_graph_nodes(base, id):
    return jsonify(af.get_all_nodes_list(base=base, id=id))


#
# @home.route('/graph_edges/<node>')
# def get_graph_edges(node):
#     return jsonify(af.get_all_edge_list(node=node))

@home.route('/graph_edges/<base>/<id>')
def get_graph_edges(base, id):
    return jsonify(af.get_all_edge_list(base=base, id=id))


@home.route('/get_collections/<type>')
def get_collections(type):
    """
    get collectino names depending on type node or type edge
    :param type: collection type, can be node or edge
    :return: list of collections names
    """
    collections = db.list_collection_names()
    # colls = dbf.drop_collection_identifier(collections)

    try:
        if type == 'node':
            colls = [x[5:] for x in collections if x[:5] == 'node_']

        elif type == 'edge':
            colls = [x[5:] for x in collections if x[:5] == 'edge_']

    except:
        colls = []

    return jsonify(colls)


@home.route('/get_collection_fieldnames/<type>/<collection>')
def get_collection_fieldnames2(type, collection):
    """
    get all field names of a specified collection
    :param type: collection type, can be node or edge
    :param collection: collection name
    :return: list of fieldnames
    """
    collection = type + "_" + collection
    try:
        field_list = dbf.getCollectionKeys(collection)
        field_list.remove('_id')
    except:

        field_list = []

    return jsonify(field_list)


@home.route('/get_collection_ids/<type>/<collection>')
def get_collection_ids(type, collection):
    """
    get all record id's of a specified collection
    :param type: collection type, can be node or edge
    :param collection: collection name
    :return: list of record is's
    """
    collection = type + "_" + collection
    id_list = dbf.getCollectionId(collection)

    return jsonify(id_list)


@home.route('/get_collection_record/<type>/<collection>/<id>')
def get_collection_record(type, collection, id):
    """
    get all field names of a specified collection
    remove empty values
    get all fields for a specific record
    add missing fields to the record.
    :param type: collection type, can be node or edge
    :param collection:
    :param id:
    :return:
    """
    collection = type + "_" + collection
    available_fields = dbf.getCollectionKeys(collection)

    result = db[collection].find_one({'id': id})

    # fetch non existing records
    if result is None:
        result = {}

    if '' in available_fields: available_fields.remove('')
    for x in available_fields:
        # if result is not None:
        if x not in result:
            result[x] = ''

    try:
        # remove '_id'
        result.pop('_id')
    except:
        result = []

    return dumps(result)


# pages
@home.route('/')
@home.route('/index')
def index():
    return render_template('index.html')


@home.route('/barcharts')
def barcharts():
    return render_template('barcharts.html')


@home.route('/create', methods=['GET', 'POST'])
def create():
    nodes = requests.get(url_for("home.get_collections", type='node', _external=True)).json()
    sticky_source = [0]
    sticky_edge= [0]
    sticky_target = [0]

    if request.method == 'GET':
        return render_template('create2.html', types=nodes, sticky_source=sticky_source, sticky_edge=sticky_edge, sticky_target=sticky_target)

    elif request.method == 'POST':
        if request.form['submitbutton'] == 'enter':

            # hand sticky inputs
            if request.form.get('sticky_source'):
                sticky_source = [1, request.form['source_collection_name'], request.form['source_collection_id']]

            if request.form.get('sticky_edge'):
                sticky_edge = [1, request.form['edge_value']]

            if request.form.get('sticky_target'):
                sticky_target = [1, request.form['target_collection_name'], request.form['target_collection_id']]

            logger.debug('upserting source node')
            dbf.upsert_node_data(request.form, 'source')

            logger.debug('upserting target node')
            dbf.upsert_node_data(request.form, 'target')

            logger.debug('upserting edge')
            dbf.upsert_edge_data(request.form)

        elif request.form['submitbutton'] == 'remove':
            dbf.remove_node(request.form, 'source')

        elif request.form['submitbutton'] == 'merge':
            dbf.merge_nodes(request.form)

        return render_template('create2.html', types=nodes, sticky_source=sticky_source, sticky_edge=sticky_edge, sticky_target=sticky_target)


@home.route('/read', methods=['GET'])
def read_all():
    data = {}
    for col in db.list_collection_names():
        content = []
        for record in db[col].find():
            content.append(record)
        data[col] = content

    return render_template('read.html', data=data)


@home.route('/api')
def api():
    return render_template('api.html')


@home.route('/analytics')
def analytics():
    degrees = dict(af.get_graph_degrees())
    pagerank = dict(af.get_graph_pagerank())
    betweennes_centrality = dict(af.get_graph_betweennes_centrality())

    data = [degrees, pagerank, betweennes_centrality]

    return render_template('analytics.html', data=data)


@home.route('/pagerank')
def pagerank():
    return jsonify(dict(af.get_graph_pagerank()))


@home.route('/betweenness')
def betweennes ():
    return jsonify(dict(af.get_graph_betweennes_centrality()))

@home.route('/degrees')
def degrees ():
    return jsonify(dict(af.get_graph_degrees()))