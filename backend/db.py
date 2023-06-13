import json

from arango import ArangoClient
from arango.database import StandardDatabase
from flask import g, Flask
from typing import List, Dict, Tuple
import time

from . import file_reader


def setup_db(app: Flask):
    with app.app_context():
        client = ArangoClient(hosts="http://127.0.0.1:11001")
        sys_db = client.db('_system', username='root', password='passwd')

        if not sys_db.has_database('twitter2'):
            sys_db.create_database('twitter2')
        db = client.db(name='twitter2', username='root', password='passwd')
        g.db = db
        initial_data_load(db)


def initial_data_load(db: StandardDatabase):
    users = create_users(db)
    # create_relations(db)
    tweet_ids, tweets = create_tweets(db)
    create_author_relations(db, tweet_ids, tweets, users)


def create_users(db: StandardDatabase) -> List[Dict[str, str]]:
    print("Creating USERS")
    start = time.time()
    if not db.has_collection('users'):
        users_collection = db.create_collection('users')
    else:
        users_collection = db.collection('users')
    users = file_reader.read_users()
    users_collection.insert_many(users, overwrite=True)
    end = time.time()
    print("Finished creating {} users, took {} seconds".format(len(users), end - start))
    return users


def create_follower_relations(db: StandardDatabase):
    print("Creating FOLLOWER relation")
    if not db.has_collection('follows'):
        follows_edge_collection = db.create_collection('follows', edge=True)
    else:
        follows_edge_collection = db.collection('follows')
    file_reader.read_relations(follows_edge_collection)


def create_tweets(db: StandardDatabase) -> Tuple[List[str], List[Dict]]:
    print("Creating TWEETS")
    start = time.time()
    if not db.has_collection('tweets'):
        tweets_collection = db.create_collection('tweets')
    else:
        tweets_collection = db.collection('tweets')
    tweets = file_reader.read_tweets()
    result = tweets_collection.insert_many(tweets)
    tweet_ids = [x["_key"] for x in result]
    end = time.time()
    print("Finished creating {} tweets, took {} seconds".format(len(tweets), end - start))
    return tweet_ids, tweets


def create_author_relations(db: StandardDatabase, tweet_ids: List[str], tweets: List[Dict],
                            users: List[Dict[str, str]]):
    print("Creating WROTE relations")
    start = time.time()
    if not db.has_collection('wrote'):
        wrote_edge_collection = db.create_collection('wrote', edge=True)
    else:
        wrote_edge_collection = db.collection('wrote')
    wrote_relations = file_reader.map_tweets_to_users(tweets=tweets, tweet_ids=tweet_ids, users=users)
    wrote_edge_collection.insert_many(wrote_relations)
    end = time.time()
    print("Finished creating {} wrote relations, took {} seconds".format(len(tweets), end - start))
