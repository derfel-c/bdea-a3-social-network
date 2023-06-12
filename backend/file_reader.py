import os
from mimesis import Person
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
        print("Finished creating users, took {} seconds".format(end - start))
        return users
