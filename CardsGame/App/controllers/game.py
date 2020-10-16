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
FINISHED = 'finished'


def get_game_by_id(id_game: str) -> InteractiveGame:
    try:
        game = db.get_game(id_game)
        return game
    except:
        abort(404)


@game_controllers.route('/', methods=['GET'])
def index():
    return "Interactive Game is running!"


@game_controllers.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@game_controllers.route('/game', methods=['GET'])
def get_games():
    finished_status = request.args.get(FINISHED)
    game_ids = []
    if finished_status is None:
        game_ids = db.get_list_id_games()
    else:
        is_finished = not (finished_status.lower() in ['false', '0'])
        game_ids = db.get_games_by_status(is_finished)
    return jsonify(game_ids), 200


@game_controllers.route('/game/<string:id_game>', methods=['GET'])
def get_game(id_game: str):
    game = get_game_by_id(id_game)
    response = {
        'idGame': id_game,
        'player1': game.get_name_player(1),
        'player2': game.get_name_player(2),
        'createdAt': datetime.fromtimestamp(game.get_created_date()),
        'handPlayer1': [card for card in game.get_hand_player(1, pretty=True)],
        'handPlayer2': [card for card in game.get_hand_player(2, pretty=True)],
        'lenDeckPlayer1': game.get_deck_len_player(1),
        'lenDeckPlayer2': game.get_deck_len_player(2),
        'strDeckPlayer1': str(game.get_deck_player(1)),
        'strDeckPlayer2': str(game.get_deck_player(2)),
        'currentTurn': game.get_num_turns(),
        'winner': game.get_winner(CARDS_TO_USE),
        'history': game.get_history()
    }
    return jsonify(response), 200


@game_controllers.route('/game', methods=['POST'])
def create_game():
    player = request.json.get(PLAYER_NAME)
    print('Luis', player)
    if player is None:
        return jsonify({'error': f"No '{PLAYER_NAME}' field was provided"}), 400

    game = InteractiveGame(NUM_RANKS, SUITS, SPECIAL_RANKS, player)
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
        update_hand = game.take_hand()
        if update_hand:
            db.update_game(game)
        pretty_hand = game.get_hand_player(1)
        hand = [{idx: card} for idx, card in enumerate(pretty_hand)]
        response = {
            'idGame': id_game,
            'player1': game.get_name_player(1),
            'lenDeck': game.get_deck_len_player(1),
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

        idx_hand_p1: List[int] = request.json[CARD_INDEXES]
        hand_p1 = game.get_hand_player(1, False)
        hand_p2 = game.get_hand_player(2, False)
        turn_winner, idx_hand_p2 = game.play_turn(idx_hand_p1)
        db.update_game(game)

        target_approx_p1 = sum([card.get_rank() for idx, card in enumerate(hand_p1) if idx in idx_hand_p1])
        target_approx_p2 = sum([card.get_rank() for idx, card in enumerate(hand_p2) if idx in idx_hand_p2])
        response = {
            'idGame': id_game,
            'player1': game.get_name_player(1),
            'player2': game.get_name_player(2),
            'indexesPlayer1': idx_hand_p1,
            'indexesPlayer2': idx_hand_p2,
            'lenDeckPlayer1': game.get_deck_len_player(1),
            'lenDeckPlayer2': game.get_deck_len_player(2),
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


@game_controllers.route('/game/<string:id_game>', methods=['DELETE'])
def delete_game(id_game: str):
    db.delete_game(id_game)
    return make_response(jsonify({'success': True}), 200)
