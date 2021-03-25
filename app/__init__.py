from flask import Flask
from config import config
import pymongo

# todo: put db conn in config
# todo: create blank db as an option
# todo: select db as an option

conn = pymongo.MongoClient("mongodb://localhost:27017/")
db = conn['testdb']

def create_app(config_name='default'):
    app = Flask(__name__)

    from .home import home as home_blueprint

    app.register_blueprint(home_blueprint, url_prefix="/")

    return app
