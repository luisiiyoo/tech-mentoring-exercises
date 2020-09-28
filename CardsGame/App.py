from flask import Flask, jsonify, make_response, request, abort
from datetime import datetime
from typing import Dict, List
from InteractiveGame import InteractiveGame
import constants
import traceback

app = Flask(__name__)
game_collection: Dict[str, InteractiveGame] = dict()

PLAYER_NAME = 'playerName'
CARD_INDEXES = 'cardIndexes'


def getGamebyId(id_game: str) -> InteractiveGame:
    game = game_collection.get(id_game)
    if not game:
        abort(404)
    return game


@app.route('/', methods=['GET'])
def index():
    return "Interactive Game is Running!"


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/game', methods=['GET'])
def getGames():
    game_ids = [id_game for id_game in game_collection.keys()]
    return (jsonify(game_ids), 200)


@app.route('/game/<string:id_game>', methods=['GET'])
def getGame(id_game: str):
    game = getGamebyId(id_game)
    response = {
        'idGame': id_game,
        'player1': game.getTagPlayer1(),
        'player2': game.getTagPlayer2(),
        'createdAt': datetime.fromtimestamp(game.createdAt),
        'lenDeckPlayer1': len(game.deck_p1),
        'lenDeckPlayer2': len(game.deck_p2),
        'strDeckPlayer1': str(game.deck_p1),
        'strdeckPlayer2': str(game.deck_p2),
        'numTurn': game.getNumTurns(),
        'winner': game.getWinner(constants.CARDS_TO_USE),
    }
    return (jsonify(response), 200)


@app.route('/game', methods=['POST'])
def createGame():
    has_player_name: bool = PLAYER_NAME in request.json
    if not request.json or not has_player_name:
        return (jsonify({'error': f"No '{PLAYER_NAME}' field was provided"}), 400)
    player = request.json[PLAYER_NAME]
    game = InteractiveGame(constants.NUM_RANKS, constants.SUITS,
                           constants.SPECIAL_RANKS, player)
    id_game = game.getID()
    response = {
        'idGame': id_game
    }
    game_collection[id_game] = game
    return (jsonify(response), 201)


@app.route('/game/<string:id_game>/hand', methods=['GET'])
def takePlayerHand(id_game: str):
    try:
        game = getGamebyId(id_game)
        game.takeHand()
        pretty_hand = game.getPrettyHandPlayer1()
        hand = [{indx: card} for indx, card in enumerate(pretty_hand)]
        response = {
            'idGame': id_game,
            'player1': game.getTagPlayer1(),
            'lenDeck': len(game.deck_p1),
            'hand': hand,
            'numTurn': game.getNumTurns(),
            'target': game.getTargetRank()
        }
        return (jsonify(response), 200)
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 400)


@app.route('/game/<string:id_game>/hand', methods=['PUT'])
def playTurn(id_game: str):
    try:
        game = getGamebyId(id_game)
        has_card_indxs: bool = CARD_INDEXES in request.json
        if not request.json or not has_card_indxs:
            return (jsonify({'error': f"No '{CARD_INDEXES}' field was provided"}), 400)
        if type(request.json[CARD_INDEXES]) is not list:
            return (jsonify({'error': f"'{CARD_INDEXES}' must be a list of indexes"}), 400)

        card_indxs: List[int] = request.json[CARD_INDEXES]
        pretty_cards_p1 = game.getPrettyHandPlayer1()
        pretty_cards_p2 = game.getPrettyHandPlayer2()
        turn_winner, indx_cards_player2 = game.play(card_indxs)
        response = {
            'idGame': id_game,
            'player1': game.getTagPlayer1(),
            'player2': game.getTagPlayer2(),
            'lenDeckPlayer1': len(game.deck_p1),
            'lenDeckPlayer2': len(game.deck_p2),
            'handPlayer1': [{indx: card} for indx, card in enumerate(pretty_cards_p1)],
            'handPlayer2': [{indx: card} for indx, card in enumerate(pretty_cards_p2)],
            'numTurn': game.getNumTurns(),
            'turnWinner': turn_winner,
            'winner': game.getWinner(constants.CARDS_TO_USE),
            'target': game.getTargetRank(),
            'indxsPlayer1': card_indxs,
            'indxsPlayer2': indx_cards_player2,
        }
        return (jsonify(response), 200)
    except Exception as e:
        traceback.print_exc()
        return make_response(jsonify({'error': str(e)}), 400)


if __name__ == '__main__':
    app.run(debug=True)
