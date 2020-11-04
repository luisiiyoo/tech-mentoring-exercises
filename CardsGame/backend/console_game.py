from App.models import ClassicGame
from App.util.constants import NUM_RANKS, SUITS, SPECIAL_RANKS

# %% MAIN
game = ClassicGame(NUM_RANKS, SUITS, SPECIAL_RANKS, 'Luis', 'Victor')
game.print_decks()
game.play_classic_game_on_terminal()
