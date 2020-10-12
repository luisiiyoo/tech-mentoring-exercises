from typing import Dict, List
from App.Game import InteractiveGame
from App.util.constants import CARDS_TO_USE

games_dict: Dict[str, InteractiveGame] = dict()


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
    games_dict[id_game] = game
