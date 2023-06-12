import os
from mimesis import Person
from arango.collection import StandardCollection
import time


def read_users():
    script_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_path, 'resources/twitter_combined.txt')
    person = Person()
    start = time.time()
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
        end = time.time()
        print("Finished creating {} users, took {} seconds".format(len(users), end - start))
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
