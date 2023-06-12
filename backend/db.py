import json

from arango import ArangoClient
from arango.database import StandardDatabase
from flask import g, Flask
from . import file_reader


def setup_db(app: Flask):
    with app.app_context():
        client = ArangoClient(hosts="http://127.0.0.1:11001")
        sys_db = client.db('_system', username='root', password='passwd')

        if sys_db.has_database('twitter2'):
            return

        sys_db.create_database('twitter2')
        db = client.db(name='twitter2', username='root', password='passwd')
        g.db = db
        initial_data_load(db)


def initial_data_load(db: StandardDatabase):
    create_users(db)
    create_relations(db)


def create_users(db: StandardDatabase):
    if not db.has_collection('users'):
        users_collection = db.create_collection('users')
    else:
        users_collection = db.collection('users')
    users = file_reader.read_users()
    users_collection.insert_many(users, overwrite=True)
    print("Created users")


def create_relations(db: StandardDatabase):
    if not db.has_collection('follows'):
        follows_edge_collection = db.create_collection('follows', edge=True)
    else:
        follows_edge_collection = db.collection('follows')
    file_reader.read_relations(follows_edge_collection)
