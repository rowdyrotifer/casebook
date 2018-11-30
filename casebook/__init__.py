import os

from flask import Flask

from . import auth, posts


def create_app():
    """
    Creates an instance of the casebook app
    """

    app = Flask(__name__)

    @app.route("/")
    def index():
        return "Casebook backend operational."

    app.register_blueprint(auth.bp)
    app.register_blueprint(posts.bp)

    return app
