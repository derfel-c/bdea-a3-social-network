import os
from typing import List, Dict, Tuple

from mimesis import Person
from arango.collection import StandardCollection
from arango.database import StandardDatabase
from . import queries
import time
import pandas as pd
import math
import json
import random
from progress.bar import Bar
import subprocess


def read_users() -> List[Dict[str, str]]:
    script_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_path, 'resources/twitter_combined.txt')
    person = Person()

    with open(file_path, 'r', encoding='utf8') as f:
        unique_user_ids = set()
        users = []
        for line in f:
            line = line.rstrip("\n")
            user_ids = line.split(" ")
            if user_ids[0]:
                unique_user_ids.add(user_ids[0])
            if user_ids[1]:
                unique_user_ids.add(user_ids[1])
        bar = Bar('Creating USERS', max=len(unique_user_ids), suffix='%(index)d/%(max)d Users - ~%(eta)ds remaining - %(elapsed)ds elapsed', poll_interval=0.2)
        for u in unique_user_ids:
            bar.next()
            users.append({"_key": u, "name": person.full_name()})
        bar.finish()
        return users


def create_followers(collection: StandardCollection):
    script_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_path, 'resources/twitter_combined.txt')
    with open(file_path, 'r', encoding='utf8') as f:
        num_lines = sum(1 for _ in f)
        f.seek(0)
        bar = Bar('Creating FOLLOWER relations', max=num_lines, suffix='%(index)d/%(max)d Follower relations - ~%(eta)ds remaining - %(elapsed)ds elapsed')
        follower_relations = []
        start = time.time()
        count = 0
        for line in f:
            line = line.rstrip("\n")
            user_ids = line.split(" ")
            count += 1
            if len(user_ids) != 2:
                continue
            if not user_ids[0] or not user_ids[1]:
                continue
            follower_relations.append({"_from": "users/" + user_ids[0], "_to": "users/" + user_ids[1]})
            if len(follower_relations) >= 10000:
                collection.insert_many(follower_relations, overwrite=True)
                follower_relations = []
                bar.goto(count)
        bar.finish()
        collection.insert_many(follower_relations, overwrite=True)
        end = time.time()
        print("Finished creating {} follower relations, took {} seconds".format(count, end - start))


def create_tweets(tweets_collection: StandardCollection, tweet_limit: int) -> Tuple[List[str], List[Dict]]:
    start = time.time()
    script_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_path, 'resources/tweets.csv')
    tweet_df = pd.read_csv(file_path)
    tweet_df = tweet_df.fillna("null")
    tweet_df["number_of_likes"] = pd.to_numeric(tweet_df["number_of_likes"])
    tweet_df["number_of_shares"] = pd.to_numeric(tweet_df["number_of_shares"])
    tweet_df["date_time"] = pd.to_datetime(tweet_df["date_time"], format="%d/%m/%Y %H:%M").map(pd.Timestamp.timestamp)
    tweets = tweet_df.to_dict('records')
    
    if tweet_limit != -1 and tweet_limit < len(tweets):
        tweets = tweets[0:tweet_limit]
    result = tweets_collection.insert_many(tweets, overwrite=True)
    tweet_ids = [x["_key"] for x in result]
    end = time.time()
    print(f"Finished creating {len(tweets)} tweets, took {end - start} seconds")
    return tweet_ids, tweets


def map_tweets_to_users(wrote_edge_collection: StandardCollection, tweets: List[Dict], tweet_ids: List[str], users: List[Dict[str, str]]) -> List[Dict[str, str]]:
    start = time.time()
    # Create mapping between author and actual tweets
    tweet_author_mapping = {}
    for idx, t in enumerate(tweets):
        if t["author"] not in tweet_author_mapping:
            tweet_author_mapping[t["author"]] = []
        tweet_author_mapping[t["author"]].append(idx)

    # Map our created users to these tweets
    tweet_user_mapping = {}
    for idx, tweet_indices in enumerate(tweet_author_mapping.values()):
        if idx >= len(users):
            break
        tweet_user_mapping[users[idx]["_key"]] = tweet_indices

    # Create relations fit for the db
    wrote_relations = []
    for author in tweet_user_mapping.keys():
        for tweet in tweet_user_mapping[author]:
            wrote_relations.append({"_from": "users/" + author, "_to": "tweets/" + tweet_ids[tweet]})
    end = time.time()
    print(f"Finished creating {len(tweets)} wrote relations, took {end - start} seconds")
    wrote_edge_collection.insert_many(wrote_relations, overwrite=True)
    return wrote_relations


def create_likes(tweets: List[Dict], tweet_ids: List[str], users: List[Dict[str, str]], output_file = 'resources/likes.json'):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    output_file = os.path.join(script_dir, output_file)
    max_like_count = max(tweets, key=lambda x: x["number_of_likes"])["number_of_likes"]
    share = math.floor(max_like_count / len(users))
    start = time.time()
    tweets_len = len(tweets)
    number_of_users = len(users)
    bar = Bar('Creating likes.json', max=tweets_len, suffix='%(index)d/%(max)d tweets - ~%(eta)ds remaining - %(elapsed)ds elapsed')
    with open(output_file, 'w') as f:
        for idx, t in enumerate(tweets):
            relations = []
            for i in range(0, int(t["number_of_likes"] / share)):
                random_user_idx = random.randint(0, number_of_users - 1)
                if users[random_user_idx]:
                    relations.append({"_from": "users/" + users[random_user_idx]["_key"], "_to": "tweets/" + tweet_ids[idx]})
            for relation in relations:
                f.write(json.dumps(relation) + '\n')
            bar.next()
    bar.finish()
    end = time.time()
    
    # docker exec -it coordinator1 arangoimport --file data/likes.json --type json --collection likes --server.username root --server.password passwd --server.database twitter2 --progress --overwrite
    command = [ "docker", "exec", "-it", "coordinator1", "arangoimport", "--file", "data/likes.json", "--type", "json", "--collection", "likes", "--server.username", "root", "--server.password", "passwd", "--server.database", "twitter2", "--progress", "--overwrite"]
    run_command(command)
    print(f"Finished creating like relations json file in {end - start} seconds")


def create_fanout(db: StandardDatabase, collection: StandardCollection, users: List[Dict[str, str]], limit: int):
    start = time.time()
    count = 0
    for u in users:
        count += 1
        if limit != -1 and count > limit:
            break
        tweets = queries.query_posts_of_followed_users(db, u["_key"], "newest", -1)
        relations = []
        for t in tweets:
            relations.append({"_from": "users/" + u["_key"], "_to": "tweets/" + t["_key"]})
        collection.insert_many(relations, overwrite=True)
    end = time.time()
    print(f"Finished creating fanout with limit {100}, took {end - start} seconds")

def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    for line in iter(process.stdout.readline, b''):
            print(line.decode('utf-8'), end='')
