from termcolor import cprint
from App.Game import ClassicGame
from App.util.constants import NUM_RANKS, SUITS, SPECIAL_RANKS, COLOR_TIE

# %% MAIN
game = ClassicGame(NUM_RANKS, SUITS, SPECIAL_RANKS, 'Luis', 'Victor')
game.print_decks()
game.play_classic_game_on_terminal()
cprint('Turns where there were ties: {}'.format(
    list(game.cards_discarted.keys())), COLOR_TIE)
