from flask import Flask
from App.controllers import game_controllers


def create_app():
    app = Flask(__name__)
    app.register_blueprint(game_controllers)
    return app

