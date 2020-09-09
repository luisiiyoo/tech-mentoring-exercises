import math
SPECIAL_RANKS: dict = {
    1: 'A',
    11: 'J',
    12: 'Q',
    13: 'K'
}
SUITS: dict = {
    'club': '♣',
    'diamond': '♦',
    'heart': '♥',
    'spade': '♠'
}
NUM_CARDS = 52  # 52
NUM_SUITS = len(SUITS)  # 4
NUM_RANKS = math.floor(NUM_CARDS / NUM_SUITS)  # 13

COLOR_A = 'yellow'
COLOR_B = 'green'
COLOR_TIE = 'red'
COLOR_WINNER = 'blue'
