from typing import Dict, List, Union
from App.util.constants import CARDS_TO_USE
from App.util.helpers import to_dict
from App.models import InteractiveGame, Card, Deck
from . import db
from termcolor import cprint

GAME_COLLECTION = 'Game'
FIELDS_TO_UPDATE = ['_num_turns', '_deck_p1', '_deck_p2', '_current_target', '_hand_p1', '_hand_p2', '_history']


def delete_game(id_game: str) -> None:
    """
    Removes a game from the database

    Args:
        id_game (str): models id

    Returns:
        None
    """
    db.delete_one_by_id(id_game, GAME_COLLECTION)


def update_game(game: InteractiveGame, fields_to_update: List[str] = FIELDS_TO_UPDATE) -> None:
    """
    Updates a game database document

    Args:
        game (InteractiveGame): Game instance
        fields_to_update (List[str]): List of fields to update

    Returns:
        None
    """
    id_game = game.get_id()
    game_dict = to_dict(game)

    dict_updates = {field: game_dict[field] for field in fields_to_update}
    db.update_one_by_id(id_game, dict_updates, GAME_COLLECTION)


def add_game(game: InteractiveGame) -> None:
    """
    Creates a new game document and saves it to the database

    Args:
        game (InteractiveGame): game instance

    Returns:
        None
    """
    document: Dict = to_dict(game)
    db.add_one(document, GAME_COLLECTION)


def get_games_by_status(finished: bool, only_id: bool = True) -> List[Union[str, InteractiveGame]]:
    """
    Gets a game ids list of games that have been finished or not

    Args:
        finished (bool): Flag to get all the game ids that have been finished or not
        only_id (bool): Flag to return only the id of the game

    Returns:
        List[str]: List of game id's that have the similar status provided
    """
    cursor = db.find_all(GAME_COLLECTION)
    games = []
    for raw_game in cursor:
        game = build_interactive_game_instance(raw_game)
        game_winner = game.get_winner(CARDS_TO_USE)
        if bool(game_winner) == finished:
            games.append(game.get_id() if only_id else {**raw_game, '_winner': game_winner})
    return games


def get_list_all_games(only_id: bool = True) -> List[Union[str, InteractiveGame]]:
    """
    Gets a list of all game ids created and stored at the database

    Args:
        only_id (bool): Flag to return only the id of the game

    Returns:
        List[str]: List of game ids
    """
    cursor = db.find_all(GAME_COLLECTION)
    games = []
    for raw_game in cursor:
        if only_id:
            games.append(raw_game['_id'])
        else:
            game_instance = build_interactive_game_instance(raw_game)
            game_dict = {
                **raw_game,
                '_winner': game_instance.get_winner(CARDS_TO_USE)
            }
            games.append(game_dict)
    return games


def get_game(id_game: str) -> InteractiveGame:
    """
    Gets a game_instance from the database and converts it to an InteractiveGame instance

    Args:
        id_game (str): Player id

    Returns:
        InteractiveGame: Games instance
    """
    raw_game: Dict = db.find_one_by_id(id_game, GAME_COLLECTION)
    instance = build_interactive_game_instance(raw_game)
    return instance


def build_interactive_game_instance(raw_game: Dict) -> InteractiveGame:
    _id: str = raw_game.get('_id')
    _name_p1: str = raw_game.get('_name_p1')
    _name_p2: str = raw_game.get('_name_p2')
    _num_turns: int = raw_game.get('_num_turns')
    _created_date: int = raw_game.get('_created_date')
    _current_target: int = raw_game.get('_current_target')
    _history: Dict = raw_game.get('_history')
    _deck_p1: Dict = raw_game.get('_deck_p1')
    _deck_p2: Dict = raw_game.get('_deck_p2')
    _hand_p1: List[Card] = [Card(raw_card.get('rank'), raw_card.get('suit')) for raw_card
                            in raw_game.get('_hand_p1')]
    _hand_p2: List[Card] = [Card(raw_card.get('rank'), raw_card.get('suit')) for raw_card
                            in raw_game.get('_hand_p2')]

    num_ranks: int = _deck_p1.get('num_ranks')
    suits: Dict = _deck_p1.get('suits')
    special_ranks: Dict = _deck_p1.get('special_ranks')

    cards_deck_p1: List[Card] = [Card(raw_card.get('rank'), raw_card.get('suit')) for raw_card in _deck_p1.get('cards')]
    cards_deck_p2: List[Card] = [Card(raw_card.get('rank'), raw_card.get('suit')) for raw_card in _deck_p2.get('cards')]

    deck_p1 = Deck(num_ranks=num_ranks, suits=suits, special_ranks=special_ranks, cards=cards_deck_p1)
    deck_p2 = Deck(num_ranks=num_ranks, suits=suits, special_ranks=special_ranks, cards=cards_deck_p2)

    game_instance = InteractiveGame(num_ranks=num_ranks, suits=suits, special_ranks=special_ranks, name_p1=_name_p1,
                                    name_p2=_name_p2, id_game=_id, created_date=_created_date,
                                    curr_target=_current_target, hand_p1=_hand_p1, hand_p2=_hand_p2, history=_history,
                                    deck_p1=deck_p1, deck_p2=deck_p2, num_turns=_num_turns)
    return game_instance
