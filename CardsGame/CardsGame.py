from termcolor import colored, cprint
from ClassicGame import ClassicGame
import constants

# %% MAIN
game = ClassicGame(constants.NUM_RANKS, constants.SUITS,
                   constants.SPECIAL_RANKS, 'Luis', 'Victor')
game.printDecks()
game.playGameOnTerminal()
cprint('Turns where there were ties: {}'.format(
    list(game.cards_discarted.keys())), constants.COLOR_TIE)
