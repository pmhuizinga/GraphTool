from flask import request, render_template, redirect, url_for, jsonify
# from app import graph
from . import home
from app import models, db
import logging
import requests
from app.functions import networkx_database_functions as dbf
from app.functions import networkx_analytic_functions as af
# from app.functions import import_export as db_functions
# from py2neo import Graph, Node, Relationship


logger = logging.getLogger(__name__)  # initialize logger
logger.handlers = []
c_handler = logging.StreamHandler()  # Create handlers
c_format = logging.Formatter('%(levelname)s - %(message)s')
c_handler.setFormatter(c_format)  # Create formatters and add it to handlers
logger.addHandler(c_handler)  # Add handlers to the logger
logger.setLevel(logging.INFO)

# pages
@home.route('/')
@home.route('/index')
def index():
    return render_template('index.html')


@home.route('/create', methods=['GET', 'POST'])
def create():
    '''
    docstring
    '''
    # get all node types
    nodes = requests.get(url_for("home.get_collections", type='node', _external=True)).json()
    sticky_source = [0]
    sticky_edge = [0]
    sticky_target = [0]

    if request.method == 'GET':
        return render_template('create2.html', types=nodes, sticky_source=sticky_source, sticky_edge=sticky_edge,
                               sticky_target=sticky_target)

    elif request.method == 'POST':
        if request.form['submitbutton'] == 'enter':

            # handle sticky inputs
            if request.form.get('sticky_source'):
                sticky_source = [1, request.form['source_collection_name'], request.form['source_collection_id']]

            if request.form.get('sticky_edge'):
                sticky_edge = [1, request.form['edge_value']]

            if request.form.get('sticky_target'):
                sticky_target = [1, request.form['target_collection_name'], request.form['target_collection_id']]

            logger.debug('upserting source node')
            source_node_id = dbf.upsert_node_data(request.form, 'source')
            print(source_node_id)

            logger.debug('upserting target node')
            target_node_id = dbf.upsert_node_data(request.form, 'target')
            print(target_node_id)

            if target_node_id and source_node_id:
                # logger.debug('upserting edge')
                dbf.upsert_edge_data(source_node_id, target_node_id, request.form)

        elif request.form['submitbutton'] == 'remove':
            try:
                id = dbf.get_id(request.form['source_collection_name'], request.form['source_collection_id'])
                # print('node id for removal: {}'.format(id))
                dbf.remove_node(id)
            except:
                logger.debug('id not found for delete')

        elif request.form['submitbutton'] == 'merge':
            pass
            # dbf.merge_nodes(request.form)

        return render_template('create2.html', types=nodes, sticky_source=sticky_source, sticky_edge=sticky_edge,
                               sticky_target=sticky_target)



@home.route('/graph_nodes/<base>/<id>')
def get_graph_nodes(base, id):
    return jsonify(af.get_all_nodes_list(base=base, id=id))


@home.route('/graph_edges/<base>/<id>')
def get_graph_edges(base, id):
    return jsonify(af.get_all_edge_list(base=base, id=id))

#
@home.route('/get_collections/<type>')
def get_collections(type):
    # todo: rename collections to nodes (use graph terminology)
    """
    get collection names depending on type node or type edge
    :param type: collection type, can be node or edge
    :return: list of collections names
    """

    if type == 'node':
        result = dbf.get_node_type()
        # query = "CALL db.labels()"
    elif type == 'edge':
        result = dbf.get_edge_names()

    return jsonify(result)


@home.route('/get_collection_fieldnames/<type>/<collection>')
def get_collection_fieldnames2(type, collection):
    """
    get all field names of a specified collection
    :param type: collection type, can be node or edge
    :param collection: collection name
    :return: list of fieldnames
    """
    # print('get collection fieldnames')
    # print(type)
    # print(collection)

    # collection = type + "_" + collection
    try:
        field_list = dbf.get_collection_keys(type, collection)

        field_list.remove('node_id')
        field_list.remove('node_type')

    except:

        field_list = []

    return jsonify(field_list)
    # return field_list


@home.route('/get_collection_ids/<type>/<collection>')
def get_collection_ids(type, collection):
    """
    get all record id's of a specified collection
    :param type: collection type, can be node or edge
    :param collection: collection name
    :return: list of record is's
    """
    # collection = type + "_" + collection
    id_list = dbf.get_collection_id(collection)

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
    # collection = type + "_" + collection
    available_fields = dbf.get_collection_keys(type, collection)
    # print('available fields')
    # print(available_fields)
    # get node data
    result = dbf.get_collection_detail(type, collection, id)
    # print('node data')
    # print(result)
    # result = db[collection].find_one({'id': id})

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
        result.pop('node_id')
        result.pop('node_type')
    except:
        result = []

    # return dumps(result)
    # todo: remove dumps method (change to dict)
    return jsonify(result)


# @home.route('/remove_key/<type>/<collection>/<key>')
# def remove_key(type, collection, key):
#     """
#     remove a key from all records in a specified collection (node and edge).
#     keys used for processing are not allowed to be removed
#
#     :param type: node or edge
#     :param collection: collection name
#     :param key: key name
#     :return: nothing
#     """
#     dbf.remove_key_from_collection(type, collection, key)
#
#     return jsonify(['removed'])

# @home.route('/database/<action>/<dbname>')
# def database_action(action,dbname):
#
#     if action == 'switch':
#         db_functions.database_switch(dbname)
#         return jsonify(['Database changed to: {}'.format(dbname)])
#
#     if action == 'create':
#         db_functions.database_create(dbname)
#         return jsonify(['Database {} created'.format(dbname)])



# @home.route('/read', methods=['GET'])
# def read_all():
#     data = {}
#     for col in db.list_collection_names():
#         content = []
#         for record in db[col].find():
#             content.append(record)
#         data[col] = content
#
#     return render_template('read.html', data=data)


@home.route('/api')
def api():
    return render_template('api.html')


# @home.route('/analytics')
# def analytics():
#     degrees = dict(af.get_graph_degrees())
#     pagerank = dict(af.get_graph_pagerank())
#     betweennes_centrality = dict(af.get_graph_betweennes_centrality())
#
#     data = [degrees, pagerank, betweennes_centrality]
#
#     return render_template('analytics.html', data=data)
#
#
# @home.route('/pagerank')
# def pagerank():
#     return jsonify(dict(af.get_graph_pagerank()))
#
#
# @home.route('/betweenness')
# def betweennes():
#     return jsonify(dict(af.get_graph_betweennes_centrality()))


# @home.route('/degrees')
# def degrees():
#     return jsonify(dict(af.get_graph_degrees()))


