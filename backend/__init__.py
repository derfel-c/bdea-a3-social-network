from flask import Flask


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY="dev")

    # init db
    from . import db

    db.setup_db(app, 10000)

    # setup api endpoints
    from . import api

    app.register_blueprint(api.bp)

    return app
