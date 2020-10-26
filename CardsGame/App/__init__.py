from flask import Flask
from flask_cors import CORS
from App.controllers import game_controllers


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(game_controllers)
    return app

