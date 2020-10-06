from termcolor import cprint
from App.Game.classic_game import ClassicGame
from App.util.constants import NUM_RANKS, SUITS, SPECIAL_RANKS, COLOR_TIE

# %% MAIN
game = ClassicGame(NUM_RANKS, SUITS, SPECIAL_RANKS, 'Luis', 'Victor')
game.printDecks()
game.playClasssicGameOnTerminal()
cprint('Turns where there were ties: {}'.format(
    list(game.cards_discarted.keys())), COLOR_TIE)
