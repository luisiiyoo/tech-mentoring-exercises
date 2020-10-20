import pymongo
from typing import Dict, List
from pymongo import MongoClient
from pymongo.collection import Collection
from config import MONGO_STR_CONNECTION, MONGO_DB_NAME
from App.models import InteractiveGame
from App.util.constants import CARDS_TO_USE
from App.util.helpers import to_dict


class MongoManager:
    __client = None

    @staticmethod
    def get_client() -> MongoClient:
        """
        Gets a MongoClient instance for connecting with the data base

        Args:
            None

        Returns:
            MongoClient: Instance for connecting with the data base
        """
        if not MongoManager.__client:
            __client = pymongo.MongoClient(MONGO_STR_CONNECTION)
        return __client

    @staticmethod
    def get_game_collection(collection_name: str) -> Collection:
        """
        Gets a database collection

        Args:
            collection_name (str): Collection name

        Returns:
            Collection: Database collection
        """
        client = MongoManager.get_client()
        db = client[MONGO_DB_NAME]
        return db[collection_name]


def find_game(id_game: str) -> Dict:
    """
    Gets a game as a dictionary given its id

    Args:
        id_game (str): Player id

    Raises:
        Exception: If a game was not found

    Returns:
        Dict: models instance as a dictionary
    """
    collection = MongoManager.get_game_collection('models')
    raw_game = collection.find_one({'_id': id_game})
    if not raw_game:
        raise Exception(f"models {id_game} not found")
    return raw_game


def get_game(id_game: str) -> InteractiveGame:
    """
    Gets a game from the database and converts it to an InteractiveGame instance

    Args:
        id_game (str): Player id

    Returns:
        InteractiveGame: models instance
    """
    raw_game = find_game(id_game)
    return InteractiveGame.build_instance(raw_game)


def get_list_id_games() -> List[str]:
    """
    Gets a list of game ids created and stored at the database

    Args:
        None

    Returns:
        List[str]: List of game ids
    """
    collection = MongoManager.get_game_collection('models')
    cursor = collection.find({})
    return [raw_game['_id'] for raw_game in cursor]


def get_games_by_status(finished: bool) -> List[str]:
    """
    Gets a game ids list of games that have been finished or not

    Args:
        finished (bool): Flag to get all the game ids that have been finished or not

    Returns:
        List[str]: List of game id's that have the similar status provided
    """
    collection = MongoManager.get_game_collection('models')
    cursor = collection.find({})
    games = []
    for raw_game in cursor:
        game = InteractiveGame.build_instance(raw_game)
        game_winner = game.get_winner(CARDS_TO_USE)
        if bool(game_winner) == finished:
            games.append(game.get_id())
    return games


def add_game(game: InteractiveGame) -> None:
    """
    Creates a new game document and saves it to the database

    Args:
        game (InteractiveGame): models instance

    Returns:
        None
    """
    collection = MongoManager.get_game_collection('models')
    collection.insert_one(to_dict(game))


def update_game(game_updates: InteractiveGame) -> None:
    """
    Updates a game database document

    Args:
        game_updates (InteractiveGame): models instance

    Returns:
        None
    """
    collection = MongoManager.get_game_collection('models')
    query = {'_id': game_updates.get_id()}
    game_dict = to_dict(game_updates)

    fields_to_update = ['_num_turns', '_deck_p1', '_deck_p2', '_current_target', '_hand_p1', '_hand_p2', '_history']
    updates = {'$set': {key: game_dict[key] for key in fields_to_update}}
    collection.update_one(query, updates, upsert=False)


def delete_game(id_game: str) -> None:
    """
    Removes a game from the database

    Args:
        id_game (str): models id

    Returns:
        None
    """
    collection = MongoManager.get_game_collection('models')
    collection.delete_one({'_id': id_game})

