from flask import request, render_template, redirect, url_for, jsonify
from app import db
from . import home
from bson.json_util import dumps
from bson.objectid import ObjectId
import logging
from app.functions import database_functions as dbf


# logging setup
# logging.basicConfig(filename='log/homelog.log',
#                     filemode='a',
#                     format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
#                     datefmt='%H:%M:%S',
#                     level=logging.NOTSET)
#
# logger = logging.getLogger(__name__)  # initialize logger
# logger.handlers = []


@home.route('/index')
def index():
    return render_template('index.html')


@home.route('/get_collections')
def get_collections():
    """
    get all collectino names
    :return: list of collections names
    """
    types = db.list_collection_names()
    return jsonify(types)


@home.route('/get_collection_fieldnames/<collection>')
def get_collection_fieldnames(collection):
    """
    get all field names of a specified collection
    :param collection: collection name
    :return: list of fieldnames
    """
    field_list = dbf.getCollectionKeys(collection)

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

    return dumps(result)


@home.route('/create', methods=['GET', 'POST'])
def create():
    # get collections names for populating inputbox
    types = db.list_collection_names()
    # get fieldnames
    # todo: make dependent on collection type input
    fieldlist = dbf.getCollectionKeys('persons')

    if request.method == 'GET':
        return render_template('create.html', types=types, fieldlist=fieldlist)

    elif request.method == 'POST':
        # get all form keys
        test = [k for k in request.form.keys()]
        print(test)

        t = request.form["SourceNodeType"].lower()
        p = request.form["SourceNodeName"].lower()
        prop_name1 = request.form["NewPropValue"]
        prop_type1 = request.form["NewPropName"]

        props = {prop_type1: prop_name1}

        try:
            if not p == '':
                # todo: change to upsert
                # db[t].insert_one({'id': p, prop_type1: prop_name1})
                db[t].update_one({'id': p}, {"$set": props}, upsert=True)
                print("inserting {} in collection {}".format(p, t))
        except:
            print('input error')
            print  # db[t].insert_one({'id': p})

        # get collections names for populating inputbox
        types = db.list_collection_names()

    return render_template('create.html', types=types, fieldlist=fieldlist)


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
