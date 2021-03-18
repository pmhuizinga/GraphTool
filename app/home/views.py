from flask import request, render_template, redirect, url_for, jsonify
from app import db
from . import home
from bson.json_util import dumps
from bson.objectid import ObjectId
import logging
import requests
from app.functions import database_functions as dbf

# todo: use objectID as identifier

# logging setup
logging.basicConfig(filename='log/homelog.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.NOTSET)

logger = logging.getLogger(__name__)  # initialize logger
logger.handlers = []


@home.route('/index')
def index():
    return render_template('index.html')


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
def get_collection_ids2(type, collection):
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
def get_collection_record2(type, collection, id):
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

    if '' in available_fields: available_fields.remove('')
    for x in available_fields:
        if x not in result:
            result[x] = ''

    try:
        result.pop('_id')
    except:
        result = []

    return dumps(result)


@home.route('/create', methods=['GET', 'POST'])
def create():
    # get collections names for populating inputbox
    nodes = requests.get(url_for("home.get_collections", type='node', _external=True)).json()

    if request.method == 'GET':
        return render_template('create.html', types=nodes)

    elif request.method == 'POST':

        props = {}
        edge_data = {}
        for k, v in request.form.items():
            # print(k, v)
            if ('NewEdgeValue' not in k) and ('NewPropValue' not in k) and ('SourceNodeType' not in k) and ('id' not in k):
                if k == 'SourceNodeId':
                    # check if id has changed
                    if 'id' in request.form.keys():
                        if request.form['id'] == '':
                            props['id'] = v
                        else:
                            props['id'] = request.form['id']
                    else:
                        props['id'] = request.form["SourceNodeId"].lower()
                    # print(k, v)
                elif 'NewPropName' in k:
                    value = "NewPropValue" + k[11:]
                    value2 = request.form[value]
                    if value2 != '':
                        props[v] = value2
                elif 'Edge' in k[:4]:
                    if k == 'EdgeType':
                        edge_data['EdgeType'] = v
                elif 'NewEdgeName' in k:
                    print('hebbes')
                    value = "NewEdgeValue" + k[11:]
                    value2 = request.form[value]
                    if value2 != '':
                        edge_data[v] = value2
                else:
                    props[k] = v

        node_type = 'node_' + request.form["SourceNodeType"].lower()
        node_id = request.form["SourceNodeId"].lower()

        # update database
        try:
            if not node_id == '':
                db[node_type].update_one({'id': node_id}, {"$set": props}, upsert=True)
                print("upserting {} in collection {}".format(node_id, node_type))
        except:
            print('input error')

    return render_template('create.html', types=nodes)


@home.route('/')
@home.route('/read', methods=['GET'])
def read_all():
    data = {}
    for col in db.list_collection_names():
        print(col)
        content = []
        for record in db[col].find():
            content.append(record)
        data[col] = content

    return render_template('read.html', data=data)


@home.route('/d3_test_1')
def d3_test_1():
    return render_template('d3_test_1.html')


@home.route('/api')
def api():
    return render_template('api.html')


@home.route('/test')
def test():
    return render_template('test.html')