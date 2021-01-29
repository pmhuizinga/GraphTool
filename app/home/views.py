from flask import request, render_template, redirect, url_for, jsonify
from app import db
from . import home
import logging
from app.functions import database_functions as dbf
from sqlalchemy.exc import IntegrityError


# from .forms import CreateNodeType

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
    types = db.list_collection_names()
    return jsonify(types)


@home.route('/get_collection_fieldnames/<collection>')
def get_collection_fieldnames(collection):
    field_list = dbf.getCollectionKeys(collection)

    return jsonify(field_list)


@home.route('/get_collection_ids/<collection>')
def get_collection_ids(collection):
    id_list = dbf.getCollectionId(collection)

    return jsonify(id_list)


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
        # prop_name1 = request.form["NewPropValue"]
        # prop_type1 = request.form["NewPropName"]
        print("inserting {} in collection {}".format(p, t))

        props = {prop_type1: prop_name1}

        try:
            db[t].insert_one({'id': p, prop_type1: prop_name1})
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
