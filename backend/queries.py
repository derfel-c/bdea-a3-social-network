from typing import List, Dict

from arango.database import StandardDatabase
import json


def query_posts_of_followed_users(db: StandardDatabase, user_id: str, mode: str = "newest", limit: int = 25) -> List:
    if mode == "newest":
        sort_field = "t.date_time"
    else:
        sort_field = "t.number_of_likes"

    limit_string = ""
    if limit != -1:
        limit_string = "LIMIT {}".format(limit)
    query = """
        LET USERS = (
        FOR f IN follows
              FILTER f._from == 'users/{}'
              RETURN f._to
        )

        LET followedTweets = (
        FOR w IN wrote
            FILTER w._from IN USERS
            RETURN w._to
        )

        FOR t IN tweets
            FILTER t._id IN followedTweets
            SORT {} DESC
            {}
            RETURN t 
                   """.format(user_id, sort_field, limit_string)
    cursor = db.aql.execute(query)
    result = [res for res in cursor]
    return result


def query_posts_of_user(db: StandardDatabase, user_id: str):
    query = """
    FOR w IN wrote
      FILTER w._from == 'users/{}'
      RETURN {{user: DOCUMENT(w._from), post: DOCUMENT(w._to)}}
    """.format(user_id)
    cursor = db.aql.execute(query)
    result = [res for res in cursor]
    return result


def query_users_with_most_followers(db: StandardDatabase, qty: int):
    query = """
    FOR f IN follows
      COLLECT id = f._to WITH COUNT INTO count
      SORT count DESC
      LIMIT {}
      RETURN {{ user: DOCUMENT(id), count:count}}
    """.format(qty)
    cursor = db.aql.execute(query)
    result = [res for res in cursor]
    return result


def query_top_followers_of_top_users(db: StandardDatabase, top_100_user_ids: List[str], qty: int):
    query = """
    FOR f IN follows
      FILTER f._to IN {}
      COLLECT id = f._from WITH COUNT INTO count
      SORT count DESC
      LIMIT {}
      RETURN {{ user: DOCUMENT(id), count:count}}
    """.format(json.dumps(top_100_user_ids), qty)
    cursor = db.aql.execute(query)
    result = [res for res in cursor]
    return result


def query_follower_count_of_user(db: StandardDatabase, user_key: str):
    query = """
    FOR f IN follows
      FILTER f._to == 'users/{}'
      COLLECT id = f._to WITH COUNT INTO count
      RETURN {{ user: DOCUMENT(id), follower_count:count}}
    """.format(user_key)
    cursor = db.aql.execute(query)
    result = [res for res in cursor]
    return result


def query_count_user_is_following(db: StandardDatabase, user_key: str):
    query = """
    FOR f IN follows
      FILTER f._from == 'users/{}'
      COLLECT id = f._from WITH COUNT INTO count
      RETURN {{ user: DOCUMENT(id), following_count:count}}
    """.format(user_key)
    cursor = db.aql.execute(query)
    result = [res for res in cursor]
    return result


def query_random_user_id(db: StandardDatabase):
    query = """
    FOR u IN users
        SORT RAND()
        LIMIT 1
        RETURN u._key
    """
    cursor = db.aql.execute(query)
    result = [res for res in cursor]
    return result[0]


def query_random_user_id_with_tweets(db: StandardDatabase):
    query = """
    LET uniqueFroms = (
        FOR w IN wrote
        COLLECT fromValue = w._from WITH COUNT INTO num
        RETURN fromValue
        )

        RETURN uniqueFroms[RAND() * LENGTH(uniqueFroms)]
    """
    cursor = db.aql.execute(query)
    result = [res for res in cursor]
    return result[0].replace("users/", "")


def query_top25_newest_tweets_of_user(db: StandardDatabase, user_key: str):
    query = """
    LET USERS = (
        FOR f IN follows
              FILTER f._from == 'users/{}'
              RETURN f._to
        )
        
        LET followedTweets = (
        FOR w IN wrote
            FILTER w._from IN USERS
            RETURN w._to
        )
        
        FOR t IN tweets
            FILTER t._id IN followedTweets
            SORT t.date_time DESC
            LIMIT 25
            RETURN t
    """.format(user_key)
    cursor = db.aql.execute(query)
    result = [res for res in cursor]
    return result


def query_users_user_follows(db: StandardDatabase, user_key: str, limit: int = -1):
    if limit != -1:
        limit_str = "LIMIT {}".format(limit)
    else:
        limit_str = ""
    query = """
    FOR f IN follows
      FILTER f._from == 'users/{}'
      {}
      RETURN f._to
    """.format(user_key, limit_str)
    cursor = db.aql.execute(query)
    result = [res for res in cursor]
    return result


def query_tweets_for_user_from_cache(db: StandardDatabase, user_key: str):
    query = """
      FOR f IN cache
        FILTER f._from == 'users/{}'
        SORT DOCUMENT(f._to).dateTime DESC
        LIMIT {}
        RETURN DOCUMENT(f._to)
    """.format(user_key, 100)
    cursor = db.aql.execute(query)
    result = [res for res in cursor]
    return result


def query_top25_posts_containing_words(db: StandardDatabase, words: List[str]):
    filter_str = ""
    for w in words:
        if filter_str != "":
            filter_str += " && "
        filter_str += 'CONTAINS(LOWER(t.content), LOWER("{}"))'.format(w)

    if filter_str != "":
        filter_str = "FILTER {}".format(filter_str)
    query = """
    FOR t IN tweets
        {}
        SORT t.numberOfLikes DESC
        LIMIT 25
    RETURN t
    """.format(filter_str)
    cursor = db.aql.execute(query)
    result = [res for res in cursor]
    return result


def insert_tweet_for_user_in_cache(db: StandardDatabase, user_id: str, tweet):
    query = """
    let tweet = (INSERT {{
      content: '{}',
      country: '{}',
      dateTime: {},
      language: '{}',
      latitude: '{}',
      longitude: '{}',
      numberOfLikes: '{}',
      numberOfShares: '{}'
    }} INTO tweets RETURN NEW)

    FOR f IN follows
      FILTER f._to == '{}'
      UPSERT {{
        _from: f._from,
        _to: tweet[0]._id
      }}
      INSERT {{
        _from: f._from,
        _to: tweet[0]._id
      }}
      UPDATE {{ }}
      IN cache
    """.format(
        tweet["content"],
        tweet["country"],
        tweet["date_time"],
        tweet["language"],
        tweet["latitude"],
        tweet["longitude"],
        tweet["number_of_likes"],
        tweet["number_of_shares"],
        user_id)
    cursor = db.aql.execute(query)
    result = [res for res in cursor]
    return result
