from flask import request, render_template, redirect, url_for, jsonify
from app import db
from . import home
from bson.json_util import dumps
from bson.objectid import ObjectId
import logging
from app.functions import database_functions as dbf

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


@home.route('/get_collections')
def get_collections():
    """
    get all collectino names
    :return: list of collections names
    """
    try:
        types = db.list_collection_names()
    except:
        types = []

    return jsonify(types)


@home.route('/get_collection_fieldnames/<collection>')
def get_collection_fieldnames(collection):
    """
    get all field names of a specified collection
    :param collection: collection name
    :return: list of fieldnames
    """
    try:
        field_list = dbf.getCollectionKeys(collection)
        field_list.remove('_id')
    except:

        field_list = []

    return jsonify(field_list)


@home.route('/get_collection_ids/<collection>')
def get_collection_ids(collection):
    """
    get all record id's of a specified collection
    :param collection: collection name
    :return: list of record is's
    """
    id_list = dbf.getCollectionId(collection)

    return jsonify(id_list)


@home.route('/get_collection_record/<collection>/<id>')
def get_collection_record(collection, id):
    """
    get all field names of a specified collection
    remove empty values
    get all fields for a specific record
    add missing fields to the record.
    :param collection:
    :param id:
    :return:
    """
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
    types = db.list_collection_names()

    if request.method == 'GET':
        return render_template('create.html', types=types)

    elif request.method == 'POST':

        fixed_values = ['SourceNodeType', 'NewPropValue', 'NewPropName']
        new_prop_fields = ['NewPropValue', 'NewPropName']

        existing_props = {}
        for k, v in request.form.items():
            if k not in fixed_values and v != '':
                print('existing props; key: {}, value: {}'.format(k, v))
                if k == 'SourceNodeId':
                    existing_props['id'] = v
                else:
                    existing_props[k] = v

        new_props2 = {}
        for k, v in request.form.items():
            if ('NewPropValue' in k or 'NewPropName' in k) and v != '':
                print('new props2; key: {}, value: {}'.format(k, v))
                new_props2[k] = v
        print(new_props2)

        node_type = request.form["SourceNodeType"].lower()
        node_id = request.form["SourceNodeId"].lower()
        prop_name1 = request.form["NewPropValue1"]
        prop_type1 = request.form["NewPropName1"]

        new_props = {prop_type1: prop_name1}
        props = {}
        if existing_props:
            props.update(existing_props)
            if prop_name1 != '':
                props.update(new_props)
        elif prop_name1 != '':
            props = new_props

        # update database
        try:
            if not node_id == '':
                db[node_type].update_one({'id': node_id}, {"$set": props}, upsert=True)
                print("upserting {} in collection {}".format(node_id, node_type))
        except:
            print('input error')

    return render_template('create.html', types=types)


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
