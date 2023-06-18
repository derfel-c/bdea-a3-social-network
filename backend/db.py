from arango import ArangoClient
from arango.database import StandardDatabase
from flask import g, Flask
from typing import List, Dict, Tuple
import time

from . import db_util


def setup_db(app: Flask, tweet_limit: int):
    with app.app_context():
        db = get_db()
        if not db.has_collection('likes'):
            initial_data_load(db, tweet_limit)
        else:
            print("Database already initialized")


def get_db() -> StandardDatabase:
    if "db" not in g:
        client = ArangoClient(hosts="http://127.0.0.1:11001")
        sys_db = client.db('_system', username='root', password='passwd')
        if not sys_db.has_database('twitter2'):
            sys_db.create_database('twitter2')
        g.db = client.db(name='twitter2', username='root', password='passwd')
    return g.db


def initial_data_load(db: StandardDatabase, tweet_limit: int):
    print("Started initial data load")
    start = time.time()
    users = create_users(db)
    create_follower_relations(db)
    tweet_ids, tweets = create_tweets(db, tweet_limit)
    create_author_relations(db, tweet_ids, tweets, users)
    create_user_likes_relations(db, tweets, tweet_ids, users)
    create_fanout(db, users)
    end = time.time()
    print("Finished initial data load, took {}".format(end - start))


def create_users(db: StandardDatabase) -> List[Dict[str, str]]:
    if not db.has_collection('users'):
        users_collection = db.create_collection('users')
    else:
        users_collection = db.collection('users')
    users = db_util.read_users()
    users_collection.insert_many(users, overwrite=True)
    return users


def create_follower_relations(db: StandardDatabase):
    if not db.has_collection('follows'):
        follows_edge_collection = db.create_collection('follows', edge=True)
    else:
        follows_edge_collection = db.collection('follows')
    db_util.create_followers(follows_edge_collection)


def create_tweets(db: StandardDatabase, tweet_limit: int) -> Tuple[List[str], List[Dict]]:
    if not db.has_collection('tweets'):
        tweets_collection = db.create_collection('tweets')
    else:
        tweets_collection = db.collection('tweets')
    return db_util.create_tweets(tweets_collection, tweet_limit)


def create_author_relations(db: StandardDatabase, tweet_ids: List[str], tweets: List[Dict],
                            users: List[Dict[str, str]]):
    if not db.has_collection('wrote'):
        wrote_edge_collection = db.create_collection('wrote', edge=True)
    else:
        wrote_edge_collection = db.collection('wrote')
    db_util.map_tweets_to_users(wrote_edge_collection, tweets, tweet_ids, users)


def create_user_likes_relations(db: StandardDatabase, tweets: List[Dict], tweet_ids: List[str],
                                users: List[Dict[str, str]]):
    if not db.has_collection('likes'):
        db.create_collection('likes', edge=True)
    db_util.create_likes(tweets, tweet_ids, users)


def create_fanout(db: StandardDatabase, users: List[Dict[str, str]]):
    if not db.has_collection('cache'):
        cache_edge_collection = db.create_collection('cache', edge=True)
    else:
        cache_edge_collection = db.collection('cache')
    db_util.create_fanout(db, cache_edge_collection, users, 100)
