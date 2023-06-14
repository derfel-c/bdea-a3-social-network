from flask import Blueprint, request
from . import queries
from . import db

bp = Blueprint("api", __name__, url_prefix="/api/v1")


@bp.route("/posts/followedUsers/<path:user_key>", methods=["GET"])
def get_post_of_followed_users(user_key: str):
    db_client = db.get_db()
    result = queries.query_posts_of_followed_users(db_client, user_key)
    return result


@bp.route("/posts/<path:user_key>", methods=["GET"])
def get_post_by_id(user_key: str):
    db_client = db.get_db()
    result = queries.query_posts_of_user(db_client, user_key)
    return result


@bp.route("/followers/top100", methods=["GET"])
def get_top_100_users_with_most_followers():
    db_client = db.get_db()
    result = queries.query_users_with_most_followers(db_client, 100)
    return result


@bp.route("/followers/top100FollowingTop100", methods=["GET"])
def get_top_100_users_following_top_100_users():
    db_client = db.get_db()
    top_100_users = queries.query_users_with_most_followers(db_client, 100)
    top_100_ids = [u["user"]["_id"] for u in top_100_users]
    result = queries.query_top_followers_of_top_users(db_client, top_100_ids, 100)
    return result


@bp.route("/followers/count/<path:user_key>", methods=["GET"])
def get_follower_count_of_user(user_key: str):
    db_client = db.get_db()
    result = queries.query_follower_count_of_user(db_client, user_key)
    return result


@bp.route("/users/follows/count/<path:user_key>", methods=["GET"])
def get_count_of_users_user_follows(user_key: str):
    db_client = db.get_db()
    result = queries.query_count_user_is_following(db_client, user_key)
    return result


@bp.route("/posts/top25NewestFor/<path:user_key>", methods=["GET"])
def get_top_25_newest_tweets_for_user(user_key: str):
    db_client = db.get_db()
    result = queries.query_top25_newest_tweets_of_user(db_client, user_key)
    return result


@bp.route("/cache/<path:user_key>", methods=["GET"])
def get_tweets_for_user_from_cache(user_key: str):
    db_client = db.get_db()
    result = queries.query_tweets_for_user_from_cache(db_client, user_key)
    return result


@bp.route("/cache/<path:user_key>", methods=["POST"])
def post_tweets_for_user_from_cache(user_key: str):
    db_client = db.get_db()
    post = request.get_json()
    if not post:
        return f"No post provided", 400
    if not user_key:
        return f"No user_key provided", 400
    user_id = queries.query_users_user_follows(db_client, user_key, 1)[0]
    result = queries.insert_tweet_for_user_in_cache(db_client, user_id, post)
    return result


@bp.route("/posts/contains/<path:words>", methods=["GET"])
def get_top25_posts_containing_words(words: str):
    word_list = words.split("/")
    db_client = db.get_db()
    result = queries.query_top25_posts_containing_words(db_client, word_list)
    return result
