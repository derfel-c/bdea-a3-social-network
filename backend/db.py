from arango import ArangoClient
from arango.database import StandardDatabase
from flask import g, Flask
from typing import List, Dict, Tuple
import time

from . import db_util


def setup_db(app: Flask, tweet_limit: int):
    with app.app_context():
        db = get_db()
        #initial_data_load(db, tweet_limit)


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
    #create_user_likes_relations(db, tweets, tweet_ids, users)
    #create_fanout(db, users)
    end = time.time()
    print("Finished initial data load, took {}".format(end - start))


def create_users(db: StandardDatabase) -> List[Dict[str, str]]:
    print("Creating USERS")
    start = time.time()
    if not db.has_collection('users'):
        users_collection = db.create_collection('users')
    else:
        users_collection = db.collection('users')
    users = db_util.read_users()
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
    db_util.read_relations(follows_edge_collection)


def create_tweets(db: StandardDatabase, tweet_limit: int) -> Tuple[List[str], List[Dict]]:
    print("Creating TWEETS")
    start = time.time()
    if not db.has_collection('tweets'):
        tweets_collection = db.create_collection('tweets')
    else:
        tweets_collection = db.collection('tweets')
    tweets = db_util.read_tweets()
    if tweet_limit != -1 and tweet_limit < len(tweets):
        tweets = tweets[0:tweet_limit]
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
    wrote_relations = db_util.map_tweets_to_users(tweets, tweet_ids, users)
    wrote_edge_collection.insert_many(wrote_relations)
    end = time.time()
    print("Finished creating {} wrote relations, took {} seconds".format(len(tweets), end - start))


def create_user_likes_relations(db: StandardDatabase, tweets: List[Dict], tweet_ids: List[str],
                                users: List[Dict[str, str]]):
    print("Creating LIKES relations")
    if not db.has_collection('likes'):
        likes_edge_collection = db.create_collection('likes', edge=True)
    else:
        likes_edge_collection = db.collection('likes')
    db_util.create_likes(likes_edge_collection, tweets, tweet_ids, users)


def create_fanout(db: StandardDatabase, users: List[Dict[str, str]]):
    print("Creating FANOUT cache")
    start = time.time()
    if not db.has_collection('cache'):
        cache_edge_collection = db.create_collection('cache', edge=True)
    else:
        cache_edge_collection = db.collection('cache')
    db_util.create_fanout(db, cache_edge_collection, users, 100)
    end = time.time()
    print("Finished creating fanout with limit {}, took {} seconds".format(100, end - start))
