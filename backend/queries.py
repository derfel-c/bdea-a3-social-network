from typing import List

from arango.database import StandardDatabase


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
