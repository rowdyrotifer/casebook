from flask import Flask
def create_app():
    """
    Creates an instance of the casebook app
    """

    app = Flask(__name__)

    @app.route("/")
    def index():
        return "Casebook backend operational."

    return app
