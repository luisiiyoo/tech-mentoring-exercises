import pymongo
from typing import Dict, List
from pymongo import MongoClient
from pymongo.database import Database
from config import MONGO_STR_CONNECTION, MONGO_DB_NAME
from App.Game import InteractiveGame
from App.util.constants import CARDS_TO_USE
from App.util.helpers import to_dict

games_dict: Dict[str, InteractiveGame] = dict()


class MongoManager:
    __client = None

    @staticmethod
    def get_client() -> MongoClient:
        if not MongoManager.__client:
            __client = pymongo.MongoClient(MONGO_STR_CONNECTION)
        return __client

    @staticmethod
    def get_game_collection() -> Database:
        db_client = MongoManager.get_client()
        collection = db_client['Game']
        return collection


def get_game(id_game: str) -> InteractiveGame:
    game = games_dict.get(id_game)
    if not game:
        raise Exception(f"Game {id_game} not found")
    return game


def get_list_games() -> List[str]:
    return list(games_dict.keys())


def get_games_by_status(alive: bool) -> List[str]:
    keys = games_dict.keys()
    return [id_game for id_game in keys if bool(get_game(id_game).get_winner(CARDS_TO_USE)) == alive]


def add_game(game: InteractiveGame) -> None:
    id_game = game.get_id()
    client = MongoManager.get_client()
    db = client[MONGO_DB_NAME]
    collection = db['Game']
    game_dict = to_dict(game)
    insertion = collection.insert_one(game_dict)
    games_dict[id_game] = game
