import json

from arango import ArangoClient
from arango.database import StandardDatabase
from flask import g, Flask
from . import file_reader


def setup_db(app: Flask):
    with app.app_context():
        client = ArangoClient(hosts="http://127.0.0.1:11001")
        sys_db = client.db('_system', username='root', password='passwd')
        if not sys_db.has_database('twitter2'):
            sys_db.create_database('twitter2')
        db = client.db(name='twitter2', username='root', password='passwd')
        print(db.collections())
        if not db.has_collection('users'):
            users = db.create_collection('users', user_keys=True)
        g.db = db
        initial_data_load(db)


def initial_data_load(db: StandardDatabase):
    users = file_reader.read_users()
    users_collection = db.collection('users')
    success = users_collection.insert_many(users, overwrite=True)
    print(success)

