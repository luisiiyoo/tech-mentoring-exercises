import traceback
from flask import Blueprint, jsonify, make_response, request, abort
from datetime import datetime
from typing import List
from App.Game import InteractiveGame
from App.util.constants import CARDS_TO_USE, NUM_RANKS, SUITS, SPECIAL_RANKS
from App.database import db

game_controllers = Blueprint('game', __name__, url_prefix='')

PLAYER_NAME = 'playerName'
CARD_INDEXES = 'cardIndexes'


def get_game_by_id(id_game: str) -> InteractiveGame:
    try:
        game = db.get_game(id_game)
        return game
    except:
        abort(404)


@game_controllers.route('/', methods=['GET'])
def index():
    return "Interactive Game is Running!"


@game_controllers.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@game_controllers.route('/game', methods=['GET'])
def get_games():
    game_ids = [id_game for id_game in db.get_list_games()]
    return jsonify(game_ids), 200


@game_controllers.route('/game/<string:id_game>', methods=['GET'])
def get_game(id_game: str):
    game = get_game_by_id(id_game)
    response = {
        'idGame': id_game,
        'player1': game.get_tag_player(1),
        'player2': game.get_tag_player(2),
        'createdAt': datetime.fromtimestamp(game.createdAt),
        'lenDeckPlayer1': len(game.deck_p1),
        'lenDeckPlayer2': len(game.deck_p2),
        'strDeckPlayer1': str(game.deck_p1),
        'strDeckPlayer2': str(game.deck_p2),
        'currentTurn': game.get_num_turns(),
        'winner': game.get_winner(CARDS_TO_USE),
        'history': game.history
    }
    return jsonify(response), 200


@game_controllers.route('/game', methods=['POST'])
def create_game():
    player = request.json.get(PLAYER_NAME)
    if not player:
        return jsonify({'error': f"No '{PLAYER_NAME}' field was provided"}), 400

    player = request.json[PLAYER_NAME]
    game = InteractiveGame(NUM_RANKS, SUITS,
                           SPECIAL_RANKS, player)
    id_game = game.get_id()
    response = {
        'idGame': id_game
    }
    db.add_game(game)
    return jsonify(response), 201


@game_controllers.route('/game/<string:id_game>/hand', methods=['GET'])
def take_player_hand(id_game: str):
    try:
        game = get_game_by_id(id_game)
        game.take_hand()
        pretty_hand = game.get_hand_player(1)
        hand = [{indx: card} for indx, card in enumerate(pretty_hand)]
        response = {
            'idGame': id_game,
            'player1': game.get_tag_player(1),
            'lenDeck': len(game.deck_p1),
            'hand': hand,
            'currentTurn': game.get_num_turns(),
            'target': game.get_target_rank()
        }
        return jsonify(response), 200
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 400)


@game_controllers.route('/game/<string:id_game>/hand', methods=['PUT'])
def play_turn(id_game: str):
    try:
        game = get_game_by_id(id_game)
        has_card_indexes: bool = CARD_INDEXES in request.json
        if not request.json or not has_card_indexes:
            return jsonify({'error': f"No '{CARD_INDEXES}' field was provided"}), 400
        if type(request.json[CARD_INDEXES]) is not list:
            return jsonify({'error': f"'{CARD_INDEXES}' must be a list of indexes"}), 400

        idxs_hand_p1: List[int] = request.json[CARD_INDEXES]
        hand_p1 = game.get_hand_player(1, False)
        hand_p2 = game.get_hand_player(2, False)
        turn_winner, idxs_hand_p2 = game.play_turn(idxs_hand_p1)
        target_approx_p1 = sum([card.get_rank() for idx, card in enumerate(hand_p1) if idx in idxs_hand_p1])
        target_approx_p2 = sum([card.get_rank() for idx, card in enumerate(hand_p2) if idx in idxs_hand_p2])
        response = {
            'idGame': id_game,
            'player1': game.get_tag_player(1),
            'player2': game.get_tag_player(2),
            'indexesPlayer1': idxs_hand_p1,
            'indexesPlayer2': idxs_hand_p2,
            'lenDeckPlayer1': len(game.deck_p1),
            'lenDeckPlayer2': len(game.deck_p2),
            'handPlayer1': [{idx: str(card)} for idx, card in enumerate(hand_p1)],
            'handPlayer2': [{idx: str(card)} for idx, card in enumerate(hand_p2)],
            'currentTurn': game.get_num_turns(),
            'turnWinner': turn_winner,
            'winner': game.get_winner(CARDS_TO_USE),
            'target': game.get_target_rank(),
            'targetApproxPlayer1': target_approx_p1,
            'targetApproxPlayer2': target_approx_p2,
        }
        return jsonify(response), 200
    except Exception as e:
        traceback.print_exc()
        return make_response(jsonify({'error': str(e)}), 400)
