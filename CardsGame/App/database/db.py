import pymongo
from typing import Dict, List
from pymongo import MongoClient
from pymongo.database import Database
from config import MONGO_STR_CONNECTION, MONGO_DB_NAME
from App.Game import InteractiveGame
from App.util.constants import CARDS_TO_USE
from App.util.helpers import to_dict


class MongoManager:
    __client = None

    @staticmethod
    def get_client() -> MongoClient:
        if not MongoManager.__client:
            __client = pymongo.MongoClient(MONGO_STR_CONNECTION)
        return __client

    @staticmethod
    def get_game_collection(collection_name: str) -> Database:
        client = MongoManager.get_client()
        db = client[MONGO_DB_NAME]
        return db[collection_name]


def find_game(id_game: str) -> Dict:
    collection = MongoManager.get_game_collection('Game')
    raw_game = collection.find_one({'_id': id_game})
    if not raw_game:
        raise Exception(f"Game {id_game} not found")
    return raw_game


def get_game(id_game: str) -> InteractiveGame:
    raw_game = find_game(id_game)
    return InteractiveGame.build_instance(raw_game)


def get_list_id_games() -> List[str]:
    collection = MongoManager.get_game_collection('Game')
    cursor = collection.find({})
    return [raw_game['_id'] for raw_game in cursor]


def get_games_by_status(finished: bool) -> List[str]:
    collection = MongoManager.get_game_collection('Game')
    cursor = collection.find({})
    games = []
    for raw_game in cursor:
        game = InteractiveGame.build_instance(raw_game)
        game_winner = game.get_winner(CARDS_TO_USE)
        if bool(game_winner) == finished:
            games.append(game.get_id())
    return games


def add_game(game: InteractiveGame) -> None:
    collection = MongoManager.get_game_collection('Game')
    collection.insert_one(to_dict(game))


def update_game(game_updates: InteractiveGame) -> None:
    collection = MongoManager.get_game_collection('Game')
    query = {'_id': game_updates.get_id()}
    game_dict = to_dict(game_updates)

    fields_to_update = ['_num_turns', '_deck_p1', '_deck_p2', '_current_target', '_hand_p1', '_hand_p2', '_history']
    updates = {'$set': {key: game_dict[key] for key in fields_to_update}}
    collection.update_one(query, updates, upsert=False)


def delete_game(id_game: str) -> None:
    collection = MongoManager.get_game_collection('Game')
    collection.delete_one({'_id': id_game})

