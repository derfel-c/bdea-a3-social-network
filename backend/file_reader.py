import os
from typing import List, Dict

from mimesis import Person
from arango.collection import StandardCollection
import time
import pandas as pd


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
        for u in unique_user_ids:
            users.append({"_key": u, "name": person.full_name()})
        return users


def read_relations(collection: StandardCollection):
    script_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_path, 'resources/twitter_combined.txt')
    with open(file_path, 'r', encoding='utf8') as f:
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
            if len(follower_relations) > 10000:
                collection.insert_many(follower_relations, overwrite=True)
                follower_relations = []
            if count % 250000 == 0:
                print("Created {} follower relations".format(count))

        collection.insert_many(follower_relations, overwrite=True)
        end = time.time()
        print("Finished creating {} follower relations, took {} seconds".format(count, end - start))


def read_tweets() -> List[Dict]:
    script_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_path, 'resources/tweets.csv')
    tweet_df = pd.read_csv(file_path)
    tweet_df = tweet_df.fillna("null")
    tweet_df["number_of_likes"] = pd.to_numeric(tweet_df["number_of_likes"])
    tweet_df["number_of_shares"] = pd.to_numeric(tweet_df["number_of_shares"])
    tweet_df["date_time"] = pd.to_datetime(tweet_df["date_time"], format="%d/%m/%Y %H:%M").map(pd.Timestamp.timestamp)
    formatted = tweet_df.to_dict('records')
    return formatted


def map_tweets_to_users(tweets: List[Dict], tweet_ids: List[str], users: List[Dict[str, str]]) -> List[Dict[str, str]]:
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
    return wrote_relations
