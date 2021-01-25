from flask import Flask
from flask_pymongo import PyMongo
from flask import jsonify
import requests
import pymongo

from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify, request
# from werkzeug.security import generate_password_hash,check_password_hash
# from app import mongo,app
import json

app = Flask(__name__)

# app.config['MONGODB_NAME'] = 'testdb'
# app.config['MONGO_URI'] = "mongodb://localhost:27017/"
mongo = PyMongo(app)

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
db = myclient['testdb']
c_users = db.users

@app.route('/')
@app.route('/read_all_users', methods=['GET'])
def get_all_users():
    # users = db.users
    output = []
    for s in c_users.find():
        output.append({'first_name': s['first_name'], 'last_name': s['last_name']})
    return jsonify({'result': output})


@app.route('/update_user', methods=['POST'])
def updateUser():
    # logger.debug("inside put method")
    # _id = taskId
    json = request.get_json()
    name = json['first_name']
    # email = json['email']
    # password = json['password']
    # basic validation
    if name and request.method == 'PUT':
        # GENERATE HASH PASSWORD
        # hashed_password = generate_password_hash(password)
        # Update the data

        user_id = c_users.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},
                                     {'$set': {'first_name': name}})
        update_user = c_users.find_one({'_id': user_id})
        output = {'name': update_user['name'], 'password': update_user['password'], 'email': update_user['email']}
        return jsonify({'result': output}, 201)


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=4000, debug=True, use_reloader=True)
